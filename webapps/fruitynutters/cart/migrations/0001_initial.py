# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cart'
        db.create_table('cart_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('cart_comment', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('cart_username', self.gf('django.db.models.fields.CharField')(default='', max_length=60, null=True, blank=True)),
            ('cart_useremail', self.gf('django.db.models.fields.CharField')(default='', max_length=60, null=True, blank=True)),
            ('cart_userphone', self.gf('django.db.models.fields.CharField')(default='', max_length=60, null=True, blank=True)),
        ))
        db.send_create_signal('cart', ['Cart'])

        # Adding model 'CartItem'
        db.create_table('cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Item'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('cart_bundle', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bundle_owner', null=True, to=orm['cart.Cart'])),
        ))
        db.send_create_signal('cart', ['CartItem'])

        # Adding model 'CartWriteinItem'
        db.create_table('cart_cartwriteinitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('cart', ['CartWriteinItem'])

        # Adding model 'CartVirtualShopItem'
        db.create_table('cart_cartvirtualshopitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cart', ['CartVirtualShopItem'])


    def backwards(self, orm):
        
        # Deleting model 'Cart'
        db.delete_table('cart_cart')

        # Deleting model 'CartItem'
        db.delete_table('cart_cartitem')

        # Deleting model 'CartWriteinItem'
        db.delete_table('cart_cartwriteinitem')

        # Deleting model 'CartVirtualShopItem'
        db.delete_table('cart_cartvirtualshopitem')


    models = {
        'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'cart_comment': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'cart_useremail': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cart_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cart_userphone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cart.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Cart']"}),
            'cart_bundle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bundle_owner'", 'null': 'True', 'to': "orm['cart.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Item']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cart.cartvirtualshopitem': {
            'Meta': {'object_name': 'CartVirtualShopItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cart.cartwriteinitem': {
            'Meta': {'object_name': 'CartWriteinItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Cart']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
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
        }
    }

    complete_apps = ['cart']
