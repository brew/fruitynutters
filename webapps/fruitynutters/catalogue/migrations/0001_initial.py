# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aisle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Display name for the aisle.', max_length=60, unique=True)),
                ('sort_name', models.CharField(help_text=b'Name the aisle is sorted on. Not displayed to the user.', max_length=60, verbose_name=b'Order')),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(help_text=b"Determines whether the Aisle is active to the user. This doesn't affect the active status of items.")),
            ],
            options={
                'ordering': ['sort_name'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name=b'Internal name')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Display name for the item.', max_length=60)),
                ('sort_name', models.CharField(help_text=b'Name the item is sorted on. Not displayed to the user.', max_length=60, verbose_name=b'Sort No.')),
                ('order_name', models.CharField(help_text=b'Used in the order form.', max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField()),
                ('organic', models.BooleanField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('new_changed', models.BooleanField(verbose_name=b'New/Changed')),
                ('unit_number', models.PositiveIntegerField(help_text=b'How many units make up this item?', verbose_name=b'Unit')),
                ('measure_per_unit', models.FloatField(blank=True, null=True)),
                ('measure_type', models.CharField(blank=True, max_length=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('price_change', models.CharField(choices=[(b'increase', b'Increase'), (b'no_change', b'No change'), (b'decrease', b'Decrease')], default=b'no_change', max_length=30, null=True)),
                ('picking_order', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10'), (11, b'11'), (12, b'12'), (13, b'13'), (14, b'14'), (15, b'15'), (16, b'16'), (17, b'17'), (18, b'18'), (19, b'19'), (20, b'20')], default=9, verbose_name=b'Picking Order')),
                ('aisle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Aisle')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.Brand')),
                ('bundle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.Bundle')),
            ],
            options={
                'ordering': ['sort_name'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name=b'Internal name')),
                ('title', models.CharField(max_length=60, verbose_name=b'Page title')),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VirtualShopPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalogue.Page')),
                ('shopPdf', models.FileField(upload_to=b'files', verbose_name=b'Shop PDF file')),
            ],
            bases=('catalogue.page',),
        ),
        migrations.AddField(
            model_name='bundle',
            name='items',
            field=models.ManyToManyField(related_name='bundle_item', to='catalogue.Item'),
        ),
    ]
