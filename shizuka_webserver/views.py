from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import TemplateView
from shizuka_webserver.models import Client, MonitoringInstance, Monitor
from django.http import Http404
from django.views import generic
from django.forms import ModelForm
from shizuka_webserver.tasks import configure_monitors_on_client


#  Create your views here.
#
# def detail(request, client_id):
#  #return HttpResponse("You're looking at client: %s" % client_id)
#  try:
#     client = Client.objects.get(pk=client_id)
#     except Client.DoesNotExist:
#         raise Http404
#
#     #This is a shortcut of all of the above! it combines the getting and the 404.
#     #client = get_object_or404(Client, pk=client_id)
#
#     return render(request, 'shizuka_webserver/detail.html', {'client': client})
#
#
def monitors(request, client_id):
    return HttpResponse("You're looking at monitors for client: %s" % client_id)
#
#
def alerts(request, client_id):
    return HttpResponse("You're looking at alerts for client: %s" % client_id)
#
# def index(request):
#     recent_client_list = Client.objects.order_by('most_recent_ping')[:5]
#     context = {'recent_client_list':recent_client_list}
#     return render(request,'shizuka_webserver/index.html', context)


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


class IndexView(generic.ListView):
    template_name = 'shizuka_webserver/index.html'
    context_object_name = 'recent_client_list'

    def get_queryset(self):
        """return the last five clients to report in."""
        return Client.objects.filter(
            most_recent_ping__lte=timezone.now()
        ).order_by("most_recent_ping")


class DetailView(generic.DetailView):
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