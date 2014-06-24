# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('shizuka_webserver_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('shizuka_webserver', ['Client'])

        # Adding model 'Monitor'
        db.create_table('shizuka_webserver_monitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('shizuka_webserver', ['Monitor'])

        # Adding model 'MonitoringInstance'
        db.create_table('shizuka_webserver_monitoringinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shizuka_webserver.Client'])),
            ('monitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shizuka_webserver.Monitor'])),
            ('minimum', self.gf('django.db.models.fields.FloatField')()),
            ('maximum', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('shizuka_webserver', ['MonitoringInstance'])

        # Adding model 'Report'
        db.create_table('shizuka_webserver_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monitoringInstance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shizuka_webserver.MonitoringInstance'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('shizuka_webserver', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('shizuka_webserver_client')

        # Deleting model 'Monitor'
        db.delete_table('shizuka_webserver_monitor')

        # Deleting model 'MonitoringInstance'
        db.delete_table('shizuka_webserver_monitoringinstance')

        # Deleting model 'Report'
        db.delete_table('shizuka_webserver_report')


    models = {
        'shizuka_webserver.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'maximum': ('django.db.models.fields.FloatField', [], {}),
            'minimum': ('django.db.models.fields.FloatField', [], {}),
            'monitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.Monitor']"})
        },
        'shizuka_webserver.report': {
            'Meta': {'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoringInstance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.MonitoringInstance']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shizuka_webserver']