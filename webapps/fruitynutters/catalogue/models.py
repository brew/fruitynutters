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

    def get_next_by_sort_name(self):
        all_aisles = Aisle.objects.filter(active=True)
        all_aisle_names = [aisle.name for aisle in all_aisles]
        this_aisle_index = all_aisle_names.index(self.name)
        try:
            next_aisle = all_aisles[this_aisle_index + 1]
        except IndexError:
            next_aisle = None

        return next_aisle

    def get_previous_by_sort_name(self):
        all_aisles = Aisle.objects.filter(active=True).reverse()
        all_aisle_names = [aisle.name for aisle in all_aisles]
        this_aisle_index = all_aisle_names.index(self.name)
        try:
            prev_aisle = all_aisles[this_aisle_index + 1]
        except IndexError:
            prev_aisle = None

        return prev_aisle

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
    has_bundle = property(_has_bundle)

    def _size(self):
        measure_unit = "%g" % self.measure_per_unit
        return str(measure_unit) + self.measure_type
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


class VirtualShopPage(Page):
    """Model for a virtual shop launch page."""
    shopPdf = models.FileField(upload_to='files', verbose_name="Shop PDF file")
