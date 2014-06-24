from shizuka_webserver.models import Client, MonitoringInstance, Monitor, Report
import random

clients = Client.objects.all()
for client in clients:
    monitor_set = MonitoringInstance.objects.filter(client=client)
    for m_instance in monitor_set:
        for i in range(0, 1000):
            m_instance.report_set.create(value=random.randint(0,9999))