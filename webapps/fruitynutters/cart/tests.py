from django.test import TestCase
from fruitynutters.cart.models import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create()

    def test_cart_num_items(self):
        """Test num_items returns as expected."""

        self.assertEqual(self.cart.num_items, 0)
