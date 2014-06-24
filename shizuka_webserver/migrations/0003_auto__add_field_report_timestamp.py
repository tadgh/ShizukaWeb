# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Report.timestamp'
        db.add_column('shizuka_webserver_report', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 29, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Report.timestamp'
        db.delete_column('shizuka_webserver_report', 'timestamp')


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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shizuka_webserver']