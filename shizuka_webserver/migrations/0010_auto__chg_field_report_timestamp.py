# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Report.timestamp'
        db.alter_column('shizuka_webserver_report', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Report.timestamp'
        db.alter_column('shizuka_webserver_report', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shizuka_webserver.alert': {
            'Meta': {'object_name': 'Alert'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoring_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.MonitoringInstance']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'threshold': ('django.db.models.fields.IntegerField', [], {})
        },
        'shizuka_webserver.client': {
            'Meta': {'object_name': 'Client'},
            'cpu_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'monitors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'through': "orm['shizuka_webserver.MonitoringInstance']", 'to': "orm['shizuka_webserver.Monitor']"}),
            'most_recent_ping': ('django.db.models.fields.DateTimeField', [], {}),
            'mount_points': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['shizuka_webserver.MountPoint']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'shizuka_webserver.report': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoringInstance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.MonitoringInstance']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'shizuka_webserver.server': {
            'Meta': {'object_name': 'Server'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'})
        }
    }

    complete_apps = ['shizuka_webserver']