# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alert'
        db.create_table('shizuka_webserver_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monitoring_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shizuka_webserver.MonitoringInstance'])),
            ('threshold', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('shizuka_webserver', ['Alert'])

        # Adding M2M table for field recipients on 'Alert'
        m2m_table_name = db.shorten_name('shizuka_webserver_alert_recipients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alert', models.ForeignKey(orm['shizuka_webserver.alert'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['alert_id', 'user_id'])

        # Deleting field 'Server.uri'
        db.delete_column('shizuka_webserver_server', 'uri')

        # Adding field 'Server.ip'
        db.add_column('shizuka_webserver_server', 'ip',
                      self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, default='127.0.0.1'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Alert'
        db.delete_table('shizuka_webserver_alert')

        # Removing M2M table for field recipients on 'Alert'
        db.delete_table(db.shorten_name('shizuka_webserver_alert_recipients'))

        # Adding field 'Server.uri'
        db.add_column('shizuka_webserver_server', 'uri',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default=None),
                      keep_default=False)

        # Deleting field 'Server.ip'
        db.delete_column('shizuka_webserver_server', 'ip')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
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
            'monitors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['shizuka_webserver.Monitor']", 'through': "orm['shizuka_webserver.MonitoringInstance']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'shizuka_webserver.report': {
            'Meta': {'object_name': 'Report', 'ordering': "['timestamp']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoringInstance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shizuka_webserver.MonitoringInstance']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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