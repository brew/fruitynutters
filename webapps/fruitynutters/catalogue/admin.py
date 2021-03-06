from django.contrib import admin
from models import Aisle, Item, Brand, Bundle, Page
from forms import PageAdminModelForm


class AisleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('name', 'sort_name'), 'description', 'active')
        }),
    )
    list_display = ('name', 'sort_name', 'active')
    prepopulated_fields = {'sort_name': ('name',)}


admin.site.register(Aisle, AisleAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


admin.site.register(Brand, BrandAdmin)


class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('name', 'sort_name'),
                       'order_name',
                       ('aisle', 'brand'),
                       ('active', 'organic', 'new_changed'),
                       'bundle',
                       'picking_order')
        }),
        ('Price options', {
            'fields': (('unit_number', 'measure_per_unit', 'measure_type'),
                       'price', 'price_change')
        }),
    )
    radio_fields = {"price_change": admin.HORIZONTAL}
    list_display = (
        'id',
        'active',
        'name',
        'order_name',
        'price',
        'brand',
        'sort_name',
        'unit_number',
        'size',
        'aisle',
        'picking_order',
        'organic',
        '_has_bundle'
    )
    list_editable = (
        'active',
        'name',
        'order_name',
        'price',
    )
    search_fields = ['name', 'id']
    list_filter = ['aisle']
    prepopulated_fields = {'order_name': ('name',)}
    save_as = True


admin.site.register(Item, ItemAdmin)


class BundleAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)


admin.site.register(Bundle, BundleAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    form = PageAdminModelForm


admin.site.register(Page, PageAdmin)
