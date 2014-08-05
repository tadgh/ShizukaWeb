from __future__ import absolute_import
import logging
from ShizukaWeb.server_poller import ServerPoller
from ShizukaWeb.celery import app as celery_app
from shizuka_webserver.models import Client, Monitor, MonitoringInstance, MountPoint, Command
from django.utils import timezone


@celery_app.task(base=ServerPoller)
def get_data():
    res = get_data.reporting_server.get_all_data()
    for report in res:
        client_identifier = report["client_id"]
        try:
            client = Client.objects.get(identifier=client_identifier)
        except Client.DoesNotExist:
            logging.error("No knowledge of Client: huh?! {}".format(client_identifier))
            return
        client.most_recent_ping = report["timestamp"]
        client.save()
        for monitor_name, values in report["polled_data"].items():
            try:
                monitor = Monitor.objects.get(name=monitor_name)
                monitoring_instance = MonitoringInstance.objects.get(client=client, monitor=monitor)
                monitoring_instance.minimum = values[0]
                monitoring_instance.maximum = values[2]
                monitoring_instance.report_set.create(value=values[1], timestamp=report["timestamp"])
                monitoring_instance.save()
            except Monitor.DoesNotExist:
                logging.error("Monitor: {} DOES NOT EXIST!".format(monitor_name))
            except MonitoringInstance.DoesNotExist:
                logging.error("MONITOR: {} ")


#TODO split this out to several different parsing functions.
@celery_app.task(base=ServerPoller)
def get_messages():
    results = get_messages.reporting_server.get_all_messages()
    for result in results:

        client_name = result["client_id"]# Get the basic name and client
        message = result["message"]

        #monitor reports sort the reports and save them to the database.
        if message["type"] == "Monitor Report":
            process_monitor_report(client_name, message["data"])

        #discovery is for new clients. Creates new clients and then saves them.
        elif message["type"] == "Discovery":
            process_discovery(message["data"])


def process_discovery(message):

    logging.info("Found Discovery message from Server.")
    defaults_dict = {
       "ip": message["IP"],
        "mac": message["MAC"],
        "name": message["FQDN"],
        "cpu_count": message["CPU_COUNT"],
        "ram_count": message["RAM_COUNT"],
        "platform": message["PLATFORM"],
        "most_recent_ping": timezone.now()
    }
    #
    client, created = Client.objects.get_or_create(identifier=message["CLIENT_ID"], defaults=defaults_dict)
    if created:
        client.ip = message["IP"]
        client.mac = message["MAC"]
        client.name = message["FQDN"]
        client.cpu_count = message["CPU_COUNT"]
        client.ram_count = message["RAM_COUNT"]
        client.platform = message["PLATFORM"]
        client.most_recent_ping = timezone.now()
        client.save()
    try:
        mp_list = [MountPoint.objects.get_or_create(name=mount_point)[0] for mount_point in message["MOUNT_POINTS"]]
        client.mount_points.add(*mp_list)# the * is to unpack the list, as list is not accepted.
    except MountPoint.MultipleObjectsReturned:
        logging.error("Found a duplicate mountpoint in the table. Please investigate: {}")
    except KeyError:
        logging.error("Couldn't find Key: MOUNT_POINTS in the message dict.")

    try:
        command_list = [Command.objects.get_or_create(tag=command_tag) for command_tag in message["COMMANDS"]]
    except MountPoint.MultipleObjectsReturned:
        logging.error("Found a duplicate Command in the table. Please investigate: {}")
    except KeyError:
        logging.error("Couldn't find Key: COMMANDS in the message dict.")


def process_monitor_report(client_name, message):
    client = Client.objects.get(name=client_name)

    #Iterate through the monitors to be added, creating new instances in the DB as necessary.
    for new_monitor_type in message["Added"]:
        new_mon = Monitor.objects.get_or_create(name=new_monitor_type)
        if MonitoringInstance.objects.filter(client=client, monitor=new_mon).exists():
            logging.warning("Attempting to add a monitor that already exists in the DB!:{} ---> {}".format(client.name, new_monitor_type))
        else:
            MonitoringInstance.objects.create(client=client, monitor=new_mon)
            logging.info("Successfully added new monitor: {} ---> {}".format(client.name, new_monitor_type))

    #Iterate through the monitors to be deleted. Removing them from the DB as necessary.
    for new_monitor_type in message["Removed"]:
        old_mon = Monitor.objects.get_or_create(name=new_monitor_type)
        if MonitoringInstance.objects.filter(client=client, monitor=old_mon).exists():
            MonitoringInstance.objects.filter(client=client, monitor=old_mon).delete()
            logging.info("Successfully removed monitor: {} ---> {}".format(client.name, new_monitor_type))
        else:
            logging.warning("Attempting to add a monitor that already exists in the DB!:{} ---> {}".format(client.name, new_monitor_type))



@celery_app.task()
def send_command(client, command):
    pass

@celery_app.task(base=ServerPoller)
def configure_monitors_on_client(client, config_dict):
    logging.info("Attempting to Send monitor configuration dictionary to server.")
    results = configure_monitors_on_client.reporting_server.configure_monitors(client, config_dict)
    logging.info("Done sending monitor conf dictionary to server. ")



@celery_app.task()
def test_task():
    return "Tested!"