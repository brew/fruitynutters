from django.db import models

class Aisle(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

class Quantity(models.Model):
    """
    An model to collate quantity/price information.
    An Item can be made up of several units. Each unit has a measure of a measure type.
    eg. 1 item of Flour can be 6 units of 1.5 kg each.

    """

    unit_number = models.PositiveIntegerField()
    measure_per_unit = models.FloatField()
    measure_type = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    price_increase = models.BooleanField()
    price_decrease = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Quantities'

    def __unicode__(self):
        return u'%s for %sx%s%s' % (self.price, self.unit_number, self.measure_per_unit, self.measure_type)

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
    quantities = models.ForeignKey('Quantity', null=True, blank=True)

    def __unicode__(self):
        return self.name
        
class Bundle(models.Model):
    name = models.CharField(max_length=30, verbose_name='Internal name')
    items = models.ManyToManyField('Item', related_name='item_bundle')
    
    def __unicode__(self):
        return self.name