import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Server(models.Model):
    host = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()


class Monitor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MountPoint(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    most_recent_ping = models.DateTimeField()
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)
    cpu_count = models.IntegerField()
    ram_count = models.IntegerField()
    platform = models.CharField(max_length=30)
    mount_points = models.ManyToManyField(MountPoint)

    monitors = models.ManyToManyField(Monitor, through='MonitoringInstance')

    def was_recently_seen(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) < self.most_recent_ping <= now

    def is_online(self):
        now = timezone.now()
        return self.most_recent_ping > now - datetime.timedelta(minutes=5)

    #sorting and descriptions for the admin clients.
    was_recently_seen.admin_order_field = 'most_recent_ping'
    was_recently_seen.boolean = True
    was_recently_seen.short_description = "Was the client seen within the last 24 hours?"

    def __str__(self):
        return self.name


class Message(models.Model):
    client = models.ForeignKey(Client)
    type = models.CharField(max_length=100)
    msg = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.client.name + " " + self.type + " " + str(self.timestamp)


class MonitoringInstance(models.Model):
    client = models.ForeignKey(Client)
    monitor = models.ForeignKey(Monitor)
    minimum = models.FloatField(null=True)
    maximum = models.FloatField(null=True)

    def __str__(self):
        return self.monitor.name


class Command(models.Model):
    tag = models.CharField(max_length=100)
    glyph_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Alert(models.Model):
    monitoring_instance = models.ForeignKey(MonitoringInstance)
    #ensure the threshold is a percent.
    threshold = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    recipients = models.ManyToManyField(User)

    def __str__(self):
        return self.monitoring_instance.monitor.name + " on client: " + self.monitoring_instance.client.name + " (" + str(self.threshold) + "%)"


class Report(models.Model):
    monitoringInstance = models.ForeignKey(MonitoringInstance)
    value = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ['timestamp']