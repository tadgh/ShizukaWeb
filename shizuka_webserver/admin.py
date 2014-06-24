from django.contrib import admin
from shizuka_webserver.models import Client, Monitor, MonitoringInstance
# Register your models here.




class MonitoringInstanceInline(admin.StackedInline):
    model = MonitoringInstance
    extra = 3

class MonitoringInstanceInlineTabular(admin.TabularInline):
    model = MonitoringInstance
    exclude = ("minimum", "maximum")
    extra = 3


class ClientAdmin(admin.ModelAdmin):
    fields = ['identifier', 'name', 'most_recent_ping', 'ip', 'mac', 'platform', 'cpu_count', 'ram_count', 'mount_points']
    #inlines = [MonitoringInstanceInline]

    #in list of all clients, this is the data that shows in the short descriptions.
    list_display = ('identifier', 'was_recently_seen')
    #adds a filtering option for narrowing down choices in admin console
    list_filter = ['most_recent_ping']

    #allows monitoring instances to be added inline when you define a new client.
    inlines = [MonitoringInstanceInlineTabular]

    #creates a search box that searches whatever fields add in the list, using LIKE operator in sql.
    search_fields = ['name']


class MonitorAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General Information: ", {'fields': ['name']})
    ]
admin.site.register(Client, ClientAdmin)
admin.site.register(Monitor, MonitorAdmin)

