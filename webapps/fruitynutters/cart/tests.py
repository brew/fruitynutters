from decimal import Decimal

from django.test import TestCase

from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.catalogue.models import Item, Aisle


class CartTestCase(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create()
        self.aisle = Aisle.objects.create(active=True)
        self.product = Item.objects.create(name="My Product",
                                           active=True,
                                           organic=True,
                                           new_changed=False,
                                           unit_number=1,
                                           aisle=self.aisle,
                                           price=Decimal('2.50'))

    def test_cart_num_items(self):
        """Test num_items returns as expected."""
        self.assertEqual(self.cart.num_items, 0)

        CartItem.objects.create(quantity=2, cart=self.cart,
                                product_id=self.product.id)

        # 2 num_items (1 product x 2)
        self.assertEqual(self.cart.num_items, 2)
        # but only one product 1
        self.assertEqual(len(self.cart), 1)

    def test_cart_total(self):
        self.assertEqual(self.cart.total, 0)
        CartItem.objects.create(quantity=2, cart=self.cart,
                                product_id=self.product.id)
        self.assertEqual(self.cart.total, Decimal('5'))


class CartItemTestCase(TestCase):

    def setUp(self):
        self.cart = Cart.objects.create()
        self.aisle = Aisle.objects.create(active=True)

    def test_cart_item_line_total_no_price(self):
        '''Product without a price, returns Not for sale'''
        product = Item.objects.create(name="My Product",
                                      active=True,
                                      organic=True,
                                      new_changed=False,
                                      unit_number=1,
                                      aisle=self.aisle)

        cart_item = CartItem.objects.create(quantity=1, cart=self.cart,
                                            product_id=product.id)
        self.assertEqual(cart_item.line_total, 'Not for sale')

    def test_cart_item_line_total(self):
        product = Item.objects.create(name="My Product",
                                      active=True,
                                      organic=True,
                                      new_changed=False,
                                      unit_number=1,
                                      aisle=self.aisle,
                                      price=Decimal('2.50'))
        cart_item = CartItem.objects.create(quantity=2, cart=self.cart,
                                            product_id=product.id)
        self.assertEqual(cart_item.line_total, Decimal('5'))
