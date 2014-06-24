# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MountPoint'
        db.create_table('shizuka_webserver_mountpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal('shizuka_webserver', ['MountPoint'])

        # Adding model 'Message'
        db.create_table('shizuka_webserver_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shizuka_webserver.Client'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('shizuka_webserver', ['Message'])

        # Deleting field 'Client.uri'
        db.delete_column('shizuka_webserver_client', 'uri')

        # Adding field 'Client.ip'
        db.add_column('shizuka_webserver_client', 'ip',
                      self.gf('django.db.models.fields.GenericIPAddressField')(default='192.168.1.100', max_length=39),
                      keep_default=False)

        # Adding field 'Client.mac'
        db.add_column('shizuka_webserver_client', 'mac',
                      self.gf('django.db.models.fields.CharField')(default='AA:AA:AA', max_length=17),
                      keep_default=False)

        # Adding field 'Client.cpu_count'
        db.add_column('shizuka_webserver_client', 'cpu_count',
                      self.gf('django.db.models.fields.IntegerField')(default=4),
                      keep_default=False)

        # Adding field 'Client.ram_count'
        db.add_column('shizuka_webserver_client', 'ram_count',
                      self.gf('django.db.models.fields.IntegerField')(default=5),
                      keep_default=False)

        # Adding field 'Client.platform'
        db.add_column('shizuka_webserver_client', 'platform',
                      self.gf('django.db.models.fields.CharField')(default='Windows', max_length=30),
                      keep_default=False)

        # Adding M2M table for field mount_points on 'Client'
        m2m_table_name = db.shorten_name('shizuka_webserver_client_mount_points')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['shizuka_webserver.client'], null=False)),
            ('mountpoint', models.ForeignKey(orm['shizuka_webserver.mountpoint'], null=False))
        ))
        db.create_unique(m2m_table_name, ['client_id', 'mountpoint_id'])


    def backwards(self, orm):
        # Deleting model 'MountPoint'
        db.delete_table('shizuka_webserver_mountpoint')

        # Deleting model 'Message'
        db.delete_table('shizuka_webserver_message')

        # Adding field 'Client.uri'
        db.add_column('shizuka_webserver_client', 'uri',
                      self.gf('django.db.models.fields.CharField')(default='Test', max_length=200),
                      keep_default=False)

        # Deleting field 'Client.ip'
        db.delete_column('shizuka_webserver_client', 'ip')

        # Deleting field 'Client.mac'
        db.delete_column('shizuka_webserver_client', 'mac')

        # Deleting field 'Client.cpu_count'
        db.delete_column('shizuka_webserver_client', 'cpu_count')

        # Deleting field 'Client.ram_count'
        db.delete_column('shizuka_webserver_client', 'ram_count')

        # Deleting field 'Client.platform'
        db.delete_column('shizuka_webserver_client', 'platform')

        # Removing M2M table for field mount_points on 'Client'
        db.delete_table(db.shorten_name('shizuka_webserver_client_mount_points'))


    models = {
        'shizuka_webserver.client': {
            'Meta': {'object_name': 'Client'},
            'cpu_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'monitors': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['shizuka_webserver.MonitoringInstance']", 'symmetrical': 'False', 'to': "orm['shizuka_webserver.Monitor']"}),
            'most_recent_ping': ('django.db.models.fields.DateTimeField', [], {}),
            'mount_points': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shizuka_webserver.MountPoint']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ram_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'shizuka_webserver.message': {
            'Meta': {'object_name': 'Message'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shizuka_webserver.monitor': {
            'Meta': {'object_name': 'Monitor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shizuka_webserver.monitoringinstance': {
            'Meta': {'object_name': 'MonitoringInstance'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'minimum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'monitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.Monitor']"})
        },
        'shizuka_webserver.mountpoint': {
            'Meta': {'object_name': 'MountPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'shizuka_webserver.report': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoringInstance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.MonitoringInstance']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'shizuka_webserver.server': {
            'Meta': {'object_name': 'Server'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['shizuka_webserver']