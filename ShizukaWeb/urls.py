from django.conf.urls import patterns, include, url
import shizuka_webserver
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'shizuka_webserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', include("shizuka_webserver.urls", namespace='client')),
    url(r'^clients/', include("shizuka_webserver.urls", namespace='client')),
    url(r'^admin/', include(admin.site.urls)),
)
