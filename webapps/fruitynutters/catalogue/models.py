from django.db import models


class Aisle(models.Model):
    name = models.CharField(max_length=60, unique=True,
                            help_text="Display name for the aisle.")
    sort_name = models.CharField(
        max_length=60, verbose_name="Order",
        help_text="Name the aisle is sorted on. Not displayed to the user.")

    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(
        help_text="Determines whether the Aisle is active to the user. "
        "This doesn\'t affect the active status of items.")

    def _get_next_aisle(self, aisle_list):
        '''Helper method to get next aisle from aisle_list.'''
        aisle_names = [aisle.name for aisle in aisle_list]
        this_aisle_index = aisle_names.index(self.name)
        try:
            next_aisle = aisle_list[this_aisle_index + 1]
        except IndexError:
            next_aisle = None
        return next_aisle

    def get_next_aisle(self):
        '''Get next active aisle'''
        active_aisles = Aisle.objects.filter(active=True)
        return self._get_next_aisle(active_aisles)

    def get_previous_aisle(self):
        '''Get previous active aisle'''
        active_aisles_reversed = Aisle.objects.filter(active=True).reverse()
        return self._get_next_aisle(active_aisles_reversed)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort_name']


class Brand(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class Item(models.Model):
    name = models.CharField(max_length=60,
                            help_text='Display name for the item.')
    sort_name = models.CharField(
        max_length=60, verbose_name="Sort No.",
        help_text='Name the item is sorted on. Not displayed to the user.')

    order_name = models.CharField(max_length=60,
                                  help_text='Used in the order form.')

    aisle = models.ForeignKey(Aisle)
    brand = models.ForeignKey(Brand, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField()
    organic = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    new_changed = models.BooleanField(verbose_name='New/Changed')

    bundle = models.ForeignKey('Bundle', null=True, blank=True)

    unit_number = models.PositiveIntegerField(
        help_text='How many units make up this item?', verbose_name='Unit')
    measure_per_unit = models.FloatField(null=True, blank=True)
    measure_type = models.CharField(max_length=10, null=True, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2,
                                null=True, blank=True)

    price_change_choices = (
        ('increase', 'Increase'),
        ('no_change', 'No change'),
        ('decrease', 'Decrease')
    )
    price_change = models.CharField(max_length=30, null=True,
                                    default='no_change',
                                    choices=price_change_choices)

    def _has_bundle(self):
        return self.bundle is not None
    _has_bundle.boolean = True
    has_bundle = property(_has_bundle)

    def _size(self):
        if self.measure_per_unit:
            return "{0:g}{1}".format(self.measure_per_unit,
                                     self.measure_type or '')
        else:
            return None
    size = property(_size)

    picking_order_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, '18'),
        (19, '19'),
        (20, '20'),
    )
    picking_order = models.IntegerField(choices=picking_order_choices,
                                        default=9,
                                        verbose_name='Picking Order')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort_name']


class Bundle(models.Model):
    name = models.CharField(max_length=30, verbose_name='Internal name')
    items = models.ManyToManyField('Item', related_name='bundle_item')

    def __unicode__(self):
        return self.name


class Page(models.Model):
    """Model for simple ancillary pages, like the home page."""
    name = models.CharField(max_length=30, verbose_name='Internal name',
                            unique=True)
    title = models.CharField(max_length=60, verbose_name='Page title')
    body = models.TextField()

    def __unicode__(self):
        return self.name
