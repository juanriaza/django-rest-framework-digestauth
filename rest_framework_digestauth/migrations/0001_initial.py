# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DigestAuthCounter'
        db.create_table(u'rest_framework_digestauth_digestauthcounter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_nonce', self.gf('django.db.models.fields.TextField')()),
            ('client_nonce', self.gf('django.db.models.fields.TextField')()),
            ('client_counter', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'rest_framework_digestauth', ['DigestAuthCounter'])

        # Adding unique constraint on 'DigestAuthCounter', fields ['server_nonce', 'client_nonce']
        db.create_unique(u'rest_framework_digestauth_digestauthcounter', ['server_nonce', 'client_nonce'])


    def backwards(self, orm):
        # Removing unique constraint on 'DigestAuthCounter', fields ['server_nonce', 'client_nonce']
        db.delete_unique(u'rest_framework_digestauth_digestauthcounter', ['server_nonce', 'client_nonce'])

        # Deleting model 'DigestAuthCounter'
        db.delete_table(u'rest_framework_digestauth_digestauthcounter')


    models = {
        u'rest_framework_digestauth.digestauthcounter': {
            'Meta': {'unique_together': "(('server_nonce', 'client_nonce'),)", 'object_name': 'DigestAuthCounter'},
            'client_counter': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'client_nonce': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server_nonce': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['rest_framework_digestauth']