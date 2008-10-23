from django.contrib import admin
from models import Aisle, Item, Brand, Bundle

class AisleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Aisle, AisleAdmin)


class BrandAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Brand, BrandAdmin)


class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'aisle', 'brand', 'description', 'active', 'organic', 'new_changed', 'bundle', 'picking_order')
        }),
        ('Price options', {
            'fields': ('unit_number', ('measure_per_unit', 'measure_type'), 'price', 'price_change')
        }),
    )
    radio_fields = {"price_change": admin.HORIZONTAL}
    list_display = ('name', 'measure_per_unit', 'measure_type', 'price', 'aisle', 'active', 'has_bundle')
    search_fields = ['name']
    list_filter = ['aisle']


admin.site.register(Item, ItemAdmin)


class BundleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Bundle, BundleAdmin)