# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('tapmunk_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ads_viewed', self.gf('django.db.models.fields.IntegerField')()),
            ('cash', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('tapmunk', ['UserProfile'])

        # Adding model 'PreSignupProfile'
        db.create_table('tapmunk_presignupprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('tapmunk', ['PreSignupProfile'])

        # Adding model 'Advertiser'
        db.create_table('tapmunk_advertiser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('tapmunk', ['Advertiser'])

        # Adding model 'Campaign'
        db.create_table('tapmunk_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('impressions', self.gf('django.db.models.fields.IntegerField')()),
            ('advertiser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.Advertiser'])),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('tapmunk', ['Campaign'])

        # Adding model 'Ad'
        db.create_table('tapmunk_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('ad_type', self.gf('django.db.models.fields.IntegerField')()),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.Campaign'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('tapmunk', ['Ad'])

        # Adding model 'AdQuiz'
        db.create_table('tapmunk_adquiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.Ad'])),
        ))
        db.send_create_signal('tapmunk', ['AdQuiz'])

        # Adding model 'AdQuizQuestion'
        db.create_table('tapmunk_adquizquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.AdQuiz'])),
        ))
        db.send_create_signal('tapmunk', ['AdQuizQuestion'])

        # Adding model 'AdQuizAnswer'
        db.create_table('tapmunk_adquizanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.AdQuizQuestion'])),
        ))
        db.send_create_signal('tapmunk', ['AdQuizAnswer'])

        # Adding model 'AdQuizResult'
        db.create_table('tapmunk_adquizresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.AdQuizQuestion'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.AdQuizAnswer'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('tapmunk', ['AdQuizResult'])

        # Adding model 'ViewedAd'
        db.create_table('tapmunk_viewedad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.UserProfile'])),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tapmunk.Ad'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('tapmunk', ['ViewedAd'])

        # Adding model 'Consumable'
        db.create_table('tapmunk_consumable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=14)),
        ))
        db.send_create_signal('tapmunk', ['Consumable'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('tapmunk_userprofile')

        # Deleting model 'PreSignupProfile'
        db.delete_table('tapmunk_presignupprofile')

        # Deleting model 'Advertiser'
        db.delete_table('tapmunk_advertiser')

        # Deleting model 'Campaign'
        db.delete_table('tapmunk_campaign')

        # Deleting model 'Ad'
        db.delete_table('tapmunk_ad')

        # Deleting model 'AdQuiz'
        db.delete_table('tapmunk_adquiz')

        # Deleting model 'AdQuizQuestion'
        db.delete_table('tapmunk_adquizquestion')

        # Deleting model 'AdQuizAnswer'
        db.delete_table('tapmunk_adquizanswer')

        # Deleting model 'AdQuizResult'
        db.delete_table('tapmunk_adquizresult')

        # Deleting model 'ViewedAd'
        db.delete_table('tapmunk_viewedad')

        # Deleting model 'Consumable'
        db.delete_table('tapmunk_consumable')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tapmunk.ad': {
            'Meta': {'object_name': 'Ad'},
            'ad_type': ('django.db.models.fields.IntegerField', [], {}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.Campaign']"}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'tapmunk.adquiz': {
            'Meta': {'object_name': 'AdQuiz'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.Ad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tapmunk.adquizanswer': {
            'Meta': {'object_name': 'AdQuizAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.AdQuizQuestion']"})
        },
        'tapmunk.adquizquestion': {
            'Meta': {'object_name': 'AdQuizQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.AdQuiz']"})
        },
        'tapmunk.adquizresult': {
            'Meta': {'object_name': 'AdQuizResult'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.AdQuizAnswer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.AdQuizQuestion']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tapmunk.advertiser': {
            'Meta': {'object_name': 'Advertiser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tapmunk.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.Advertiser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.IntegerField', [], {}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tapmunk.consumable': {
            'Meta': {'object_name': 'Consumable'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'tapmunk.presignupprofile': {
            'Meta': {'object_name': 'PreSignupProfile'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'tapmunk.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'ads_viewed': ('django.db.models.fields.IntegerField', [], {}),
            'cash': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'tapmunk.viewedad': {
            'Meta': {'object_name': 'ViewedAd'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.Ad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tapmunk.UserProfile']"})
        }
    }

    complete_apps = ['tapmunk']