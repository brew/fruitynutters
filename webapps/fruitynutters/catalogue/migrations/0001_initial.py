# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Aisle'
        db.create_table('catalogue_aisle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('sort_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalogue', ['Aisle'])

        # Adding model 'Brand'
        db.create_table('catalogue_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
        ))
        db.send_create_signal('catalogue', ['Brand'])

        # Adding model 'Item'
        db.create_table('catalogue_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('sort_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('order_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('aisle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Aisle'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Brand'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('organic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('new_changed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bundle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Bundle'], null=True, blank=True)),
            ('unit_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('measure_per_unit', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('measure_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('price_change', self.gf('django.db.models.fields.CharField')(default='no_change', max_length=30, null=True)),
            ('picking_order', self.gf('django.db.models.fields.IntegerField')(default=9)),
        ))
        db.send_create_signal('catalogue', ['Item'])

        # Adding model 'Bundle'
        db.create_table('catalogue_bundle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('catalogue', ['Bundle'])

        # Adding M2M table for field items on 'Bundle'
        db.create_table('catalogue_bundle_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bundle', models.ForeignKey(orm['catalogue.bundle'], null=False)),
            ('item', models.ForeignKey(orm['catalogue.item'], null=False))
        ))
        db.create_unique('catalogue_bundle_items', ['bundle_id', 'item_id'])

        # Adding model 'Page'
        db.create_table('catalogue_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('catalogue', ['Page'])

        # Adding model 'VirtualShopPage'
        db.create_table('catalogue_virtualshoppage', (
            ('page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.Page'], unique=True, primary_key=True)),
            ('shopPdf', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('catalogue', ['VirtualShopPage'])


    def backwards(self, orm):
        
        # Deleting model 'Aisle'
        db.delete_table('catalogue_aisle')

        # Deleting model 'Brand'
        db.delete_table('catalogue_brand')

        # Deleting model 'Item'
        db.delete_table('catalogue_item')

        # Deleting model 'Bundle'
        db.delete_table('catalogue_bundle')

        # Removing M2M table for field items on 'Bundle'
        db.delete_table('catalogue_bundle_items')

        # Deleting model 'Page'
        db.delete_table('catalogue_page')

        # Deleting model 'VirtualShopPage'
        db.delete_table('catalogue_virtualshoppage')


    models = {
        'catalogue.aisle': {
            'Meta': {'ordering': "['sort_name']", 'object_name': 'Aisle'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'catalogue.brand': {
            'Meta': {'ordering': "['name']", 'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'catalogue.bundle': {
            'Meta': {'object_name': 'Bundle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bundle_item'", 'symmetrical': 'False', 'to': "orm['catalogue.Item']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'catalogue.item': {
            'Meta': {'ordering': "['sort_name']", 'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aisle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Aisle']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Brand']", 'null': 'True', 'blank': 'True'}),
            'bundle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Bundle']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_per_unit': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'measure_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'new_changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'organic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picking_order': ('django.db.models.fields.IntegerField', [], {'default': '9'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'price_change': ('django.db.models.fields.CharField', [], {'default': "'no_change'", 'max_length': '30', 'null': 'True'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'unit_number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'catalogue.page': {
            'Meta': {'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'catalogue.virtualshoppage': {
            'Meta': {'object_name': 'VirtualShopPage', '_ormbases': ['catalogue.Page']},
            'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'shopPdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalogue']
