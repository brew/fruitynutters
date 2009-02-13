from django.contrib import admin
from models import Aisle, Item, Brand, Bundle, Page, VirtualShopPage
from forms import PageAdminModelForm

class AisleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields':(('name', 'sort_name'), 'description', 'active')
        }),
    )
    list_display = ('name', 'sort_name', 'active')
    prepopulated_fields = {'sort_name': ('name',)}
    
admin.site.register(Aisle, AisleAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Brand, BrandAdmin)


class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('name', 'sort_name'), 'order_name', ('aisle', 'brand'), ('active', 'organic', 'new_changed'), 'bundle', 'picking_order')
        }),
        ('Price options', {
            'fields': (('unit_number', 'measure_per_unit', 'measure_type'), 'price', 'price_change')
        }),
    )
    radio_fields = {"price_change": admin.HORIZONTAL}
    list_display = ('name', 'organic', 'order_name', 'sort_name', 'brand', 'unit_number', 'size', 'price', 'aisle', 'picking_order', 'active', 'has_bundle')
    search_fields = ['name']
    list_filter = ['aisle']
    prepopulated_fields = {'sort_name': ('name',)}


admin.site.register(Item, ItemAdmin)


class BundleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Bundle, BundleAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    form = PageAdminModelForm
    
admin.site.register(Page, PageAdmin)

class VirtualShopPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'shopPdf')
    form = PageAdminModelForm
    
admin.site.register(VirtualShopPage, VirtualShopPageAdmin)
