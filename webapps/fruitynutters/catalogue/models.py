from django.db import models

class Aisle(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=60)
    aisle = models.ForeignKey(Aisle)
    brand = models.ForeignKey(Brand, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField()
    organic = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    new_changed = models.BooleanField(verbose_name='New/Changed')
    
    bundle = models.ForeignKey('Bundle', null=True, blank=True)
    
    unit_number = models.PositiveIntegerField()
    measure_per_unit = models.FloatField(null=True, blank=True)
    measure_type = models.CharField(max_length=10, null=True, blank=True)
    price = models.DecimalField(max_digits=4,decimal_places=2, null=True, blank=True)
    
    price_change_choices = (
        ('increase','Increase'),
        ('no_change','No change'),
        ('decrease','Decrease')
    )
    price_change = models.CharField(max_length=30, null=True, default='no_change', choices=price_change_choices)
    
    def _has_bundle(self):
        return self.bundle is not None
    has_bundle = property(_has_bundle)

    def __unicode__(self):
        return self.name
        
class Bundle(models.Model):
    name = models.CharField(max_length=30, verbose_name='Internal name')
    items = models.ManyToManyField('Item', related_name='bundle_item')
        
    def __unicode__(self):
        return self.name