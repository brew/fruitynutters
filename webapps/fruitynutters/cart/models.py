from django.db import models
from decimal import Decimal
import datetime

import fruitynutters

"""
These models are loosely based on models in the Shop app used by http://www.satchmoproject.com/ [BSD]

"""


class Cart(models.Model):
    """
    Store items currently in a cart
    """
    date_created = models.DateField(auto_now_add=True)

    def _get_count(self):
        itemCount = 0
        for item in self.cartitem_set.all():
            itemCount += item.quantity
        return (itemCount)
    numItems = property(_get_count)

    def _get_total(self):
        total = Decimal("0")
        for item in self.cartitem_set.all():
            total += item.line_total
        return(total)
    total = property(_get_total)

    def __iter__(self):
        return iter(self.cartitem_set.all())

    def __len__(self):
        return self.cartitem_set.count()

    def __unicode__(self):
        return u"Shopping Cart (%s)" % self.date_created

    def add_item(self, chosen_item, number_added, bundle_items=None):
        """
        Adds items to the cart.
        chosen_item     the product to add
        number_added    number to add
        bundle          a list of tuples containing the id and quantity of subitems
        """
        
        alreadyInCart = False

        # Initially create a CartItem
        item_to_modify = CartItem(cart=self, product=chosen_item, quantity=0)
        # If there's an item in the cart that already corresponds with the chosen_item, select it. 
        for similarItem in self.cartitem_set.filter(product__id = chosen_item.id):
            item_to_modify = similarItem
            alreadyInCart = True
            break
            
        if not alreadyInCart:
            self.cartitem_set.add(item_to_modify)
            
        # If we need to deal with a bundle...
        if bundle_items:
            # ... and our item doesn't yet have a bundle ...
            if not item_to_modify.cart_bundle:
                # ... create a bundle ...
                bundle = CartBundle()
                # ... save it...
                bundle.save()
                # ...add bundle to item_to_modify
                item_to_modify.cart_bundle = bundle

            # ... add bundle items to it...
            for bundle_item, bundle_item_quantity in bundle_items:
                item_to_modify.cart_bundle.add_item(bundle_item, bundle_item_quantity)
                
                

        item_to_modify.quantity += number_added
        item_to_modify.save()

        return item_to_modify


    def update_item(self, update_item_id, quantity):
        item_to_modify = self.cartitem_set.get(product__id = update_item_id)
        item_to_modify.quantity = quantity
        if item_to_modify.quantity <= 0:
            item_to_modify.delete()
            self.save()
        else:
            item_to_modify.save()

    def remove_item(self, chosen_item_id, number_removed):
        item_to_modify = self.cartitem_set.get(product__id = chosen_item_id)
        item_to_modify.quantity -= number_removed
        if item_to_modify.quantity <= 0:
            item_to_modify.delete()
        self.save()

    def empty(self):
        for item in self.cartitem_set.all():
            if item.cart_bundle:
                item.cart_bundle.empty()
            item.delete()
        self.save()

    def save(self, force_insert=False, force_update=False):
        """Ensure we have a date_time_created before saving the first time."""
        if not self.pk:
            self.date_created = datetime.datetime.now()
        super(Cart, self).save(force_insert=force_insert, force_update=force_update)


    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"


class CartItem(models.Model):
    """
    An individual item in the cart
    """
    cart = models.ForeignKey(Cart, verbose_name='Cart')
    product = models.ForeignKey(fruitynutters.catalogue.models.Item, verbose_name='Catalogue Item')
    quantity = models.IntegerField("Quantity", )
    cart_bundle = models.ForeignKey('CartBundle', null=True, blank=True, related_name="bundle")
    
    def _get_line_total(self):
        """Get the total price based on the product unit price and quantity"""
        return self.product.price * self.quantity
    line_total = property(_get_line_total)

    def _product_has_bundle(self):
        return product.has_bundle
        
    def delete(self):
        """Try deleting associated bundle carts before deleting this."""
        try:
            bundle_cart_id = self.cart_bundle.id
            self.cart_bundle = None
            self.save()
            cart_to_delete = CartBundle.objects.get(id__exact=bundle_cart_id)
            cart_to_delete.delete()
        except AttributeError:
            pass
        super(CartItem, self).delete()

    def __unicode__(self):
        return u"%s - %s %s" % (self.quantity, self.product.name, self.line_total)
        
        
    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        
class CartBundle(Cart):
    """A Bundle of CartItems (inherits from Cart)."""
    
    class Meta:
        verbose_name = "Cart Bundle"
        verbose_name_plural = "Cart Bundles"



