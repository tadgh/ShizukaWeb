# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Server'
        db.create_table('shizuka_webserver_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('shizuka_webserver', ['Server'])


    def backwards(self, orm):
        # Deleting model 'Server'
        db.delete_table('shizuka_webserver_server')


    models = {
        'shizuka_webserver.client': {
            'Meta': {'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitors': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['shizuka_webserver.MonitoringInstance']", 'to': "orm['shizuka_webserver.Monitor']", 'symmetrical': 'False'}),
            'most_recent_ping': ('django.db.models.fields.DateTimeField', [], {}),
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