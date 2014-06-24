from django.test import TestCase
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse

from shizuka_webserver.models import Client, Monitor, MonitoringInstance
from shizuka_webserver.tasks import process_discovery, process_monitor_report


def create_client(name, days):
    #Creates a client with a given name and assigns it a last ping time N days away from today.
    return Client.objects.create(name=name, most_recent_ping=timezone.now() + datetime.timedelta(days=days),
                                 ip="test",
                                 mac="test",
                                 cpu_count=1,
                                 ram_count=2,
                                 platform="windows")


def start_monitoring(client, monitor, minimum, maximum):
    return MonitoringInstance.objects.create(client=client, monitor=monitor, minimum=minimum, maximum=maximum)


def create_monitor(name):
    return Monitor.objects.create(name=name)


class ClientMethodTests(TestCase):

    def test_was_recently_seen_with_future_client(self):
        """
        Should return false for ping dates erroneously set in the future.
        :return:
        """
        future_client = Client(most_recent_ping = timezone.now() + datetime.timedelta(days=30))
        self.assertFalse(future_client.was_recently_seen())

    def test_old_clients_do_not_come_up_as_recent(self):
        old_client = Client(most_recent_ping=timezone.now() - datetime.timedelta(days=30))
        self.assertFalse((old_client.was_recently_seen()))

    def test_recent_clients_show_up_as_recent(self):
        current_client = Client(most_recent_ping=timezone.now() - datetime.timedelta(hours=1))
        self.assertTrue(current_client.was_recently_seen())


class ClientViewTests(TestCase):

    def test_index_as_redirect_from_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_index_view_with_no_clients(self):
        response = self.client.get(reverse('client:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No clients have checked in recently.")
        self.assertQuerysetEqual(response.context['recent_client_list'], [])

    def test_index_with_old_client(self):
        create_client("Tadgh", -30)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(
            response.context['recent_client_list'],
            ['<Client: Tadgh>']
        )

    def test_index_with_future_client(self):
        create_client("Tadgh", -30)
        create_client("Tadgh2", 100)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(
            response.context['recent_client_list'],
            ['<Client: Tadgh>']
        )

    def test_index_with_two_past_clients(self):
        create_client("Tadgh", -31)
        create_client("Tadgh2", -30)
        response = self.client.get(reverse('client:index'))
        self.assertQuerysetEqual(
            response.context['recent_client_list'],
            ['<Client: Tadgh>', '<Client: Tadgh2>' ]
        )


class ClientIndexDetailTests(TestCase):

    def test_detail_view_with_future_client_404s(self):
        future_client = create_client("Tadgh", 30)
        response = self.client.get(reverse("client:detail", args=(future_client.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_current_client(self):
        current_client = create_client("Tadgh", -1)
        response = self.client.get(reverse("client:detail", args=(current_client.id,)))
        self.assertContains(response, current_client.name, status_code=200)


class ResourceDetailViewTests(TestCase):

    def test_non_existent_resource_404s(self):
        client = create_client("Tadgh", -1)
        response = self.client.get(reverse("client:resource", args=(client.id,1)))
        self.assertEqual(response.status_code, 404)

    def test_resource_appears_with_no_reports(self):
        client = create_client("Tadgh", -1)
        mon = create_monitor("RAM")
        mon_inst = start_monitoring(client, mon, 0, 100)
        response = self.client.get(reverse("client:resource", args=(client.id, mon_inst.id)))
        self.assertContains(response, "No reports")

    def test_reports_appear_when_they_exist(self):
        client = create_client("Tadgh", -1)
        mon = create_monitor("RAM")
        mon_inst = start_monitoring(client, mon, 0, 100)
        mon_inst.report_set.create(value=50)
        response = self.client.get(reverse("client:resource", args=(client.id, mon_inst.id)))
        self.assertContains(response, 50)


class PollingTaskTests(TestCase):

    def test_process_discovery_for_new_client(self):
        import Utils

        message = {
            "type": "Discovery",
            "data": Utils.discover()
        }

        process_discovery(message["data"])
        client = Client.objects.get(name=message["data"]["FQDN"])
        print(client.name, client.mount_points, client.mac)
        self.assertTrue(Client.objects.filter(name=message["data"]["FQDN"]).exists())
