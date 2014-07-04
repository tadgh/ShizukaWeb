from django.conf.urls import patterns, url
from shizuka_webserver import views


urlpatterns = patterns('',
    # ex: /clients/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /clients/1
    url(r'^(?P<pk>\d+)/$', views.ClientDetailView.as_view(), name='detail'),
    # ex: /clients/1/moni´tors
    #url(r'^(?P<client_id>\d+)/monitors/$', views.monitors, name='monitors'),
    # ex: /clients/1/execute/
    url(r'^(?P<client_id>\d+)/execute/$', views.execute, name='execute'),
    # ex: /clients/1/results
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /clients/1/resource/ram
    url(r'^(?P<client_id>\d+)/resource/(?P<pk>\d+)/', views.ResourceDetailView.as_view(), name='resource'),
    # ex: /clients/1/configure
    url(r'^(?P<client_id>\d+)/configure/$', views.configurationView, name='configure'),
    # ex: /clients/2/alerts
    url(r'^(?P<client_id>\d+)/alerts/$', views.CreateAlertView.as_view(), name='create_alert'),
    # ex: /clients/2/alerts/5/delete
    url(r'^(?P<client_id>\d+)/alerts/(?P<pk>\d+)/delete$', views.DeleteAlertView.as_view(), name='delete_alert'),
    # ex: /clients/alerts
    url(r'^alerts/$', views.ListAlertView.as_view(), name='alert_list')
)
