from django.contrib import admin
from models import Aisle, Item, Brand, Quantity, Bundle

class AisleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Aisle, AisleAdmin)


class BrandAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Brand, BrandAdmin)


class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)


class QuantityAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Quantity, QuantityAdmin)

class BundleAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Bundle, BundleAdmin)