from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import TemplateView, FormView
from shizuka_webserver.models import Client, MonitoringInstance, Monitor, Alert
from django.http import Http404
from django.views import generic
from django.forms import ModelForm, CheckboxSelectMultiple
from shizuka_webserver.tasks import configure_monitors_on_client
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


#  Create your views here.


def execute(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    try:
        selected_command = client.monitoringinstance_set.get(pk=request.POST['monitor'])
    except(KeyError, MonitoringInstance.DoesNotExist):
        #redisplay the client
        return render(request, 'shizuka_webserver/detail.html', {
            'client': client,
            'error_message': "You did not select a command to execute!"
        })
    else:
        print("Executing Command: {}".format(selected_command))
        #here we actually fire off the command. server.execute_command(client, command)
        #Apparently after dealing with POST data, we should always return a ResponseRedirect, as this prevents data
        #from being posted twice if a user hits back.
        return HttpResponseRedirect(reverse('client:detail', args=(client.id,)))


def configurationView(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            print("FORM WAS VALID!", form)
            print(form.cleaned_data)
            config_dict = {}
            config_dict["add"] = []
            config_dict["remove"] = []
            for monitor in form.cleaned_data['monitors']:
                MonitoringInstance.objects.get_or_create(client=client, monitor=monitor)
                config_dict["add"].append(monitor.name)
            configure_monitors_on_client.delay(client.identifier, config_dict)
            return HttpResponseRedirect(reverse('client:detail', args=(client.id,)))
    else:
        form = ClientForm(instance=client)
        return render(request, 'shizuka_webserver/configure.html', {'client': client, 'form': form})


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['monitors', ]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['monitors'].widget = CheckboxSelectMultiple(choices=self.fields['monitors'].choices)


class AlertForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "new_alert_form"
        self.helper.form_class = "creation_form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", 'Submit'))
    class Meta:
        model = Alert


class CreateAlertView(FormView):
    template_name = "shizuka_webserver/create_alert.html"
    form_class = AlertForm

    def get_success_url(self):
        return reverse("client:detail", args=(self.kwargs["client_id"],))

    def get_context_data(self, **kwargs):
        context = super(CreateAlertView, self).get_context_data(**kwargs)
        context["form"].fields["monitoring_instance"].queryset = MonitoringInstance.objects.filter(client=self.kwargs['client_id'])
        return context

    def form_valid(self, form):
        form.save(commit=True)
        return super(CreateAlertView, self).form_valid(form)



class DeleteAlertView(generic.DeleteView):
    model = Alert
    template_name = "shizuka_webserver/delete_alert.html"

    def get_success_url(self):
        if "client_id" in self.kwargs.keys():
            return reverse("client:detail", args=(self.kwargs["client_id"],))
        else:
            return reverse("client:alert_list")

class ListAlertView(generic.ListView):
    model = Alert
    template_name = 'shizuka_webserver/alert_list.html'
    context_object_name = "alert_list"




class IndexView(generic.ListView):
    template_name = 'shizuka_webserver/index.html'
    context_object_name = 'recent_client_list'

    def get_queryset(self):
        """return the last five clients to report in."""
        return Client.objects.filter(
            most_recent_ping__lte=timezone.now()
        ).order_by("-most_recent_ping")


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'shizuka_webserver/detail.html'
    #determines the name of the object that is passed to the template. By default it is "client" as we are using the
    # Client class.  I am setting it here explicitly as a reminder.
    context_object_name = "client"

    def get_queryset(self):
        #excludes clients with future pings.
        return Client.objects.filter(most_recent_ping__lte=timezone.now())


class ResourceDetailView(generic.DetailView):
    model = MonitoringInstance
    template_name = 'shizuka_webserver/resource_report.html'
    context_object_name = 'monitoringinstance'


class ResultsView(generic.DetailView):
    model = Client
    template_name = 'shizuka_webserver/detail.html'


def home(request):
    return HttpResponseRedirect(reverse('client:index'))