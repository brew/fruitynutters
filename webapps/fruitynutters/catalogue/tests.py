from django.test import TestCase

# from fruitynutters.cart.models import Cart, CartItem
from fruitynutters.catalogue.models import Aisle


class AisleTestCase(TestCase):

    def test_get_next_none(self):
        '''Get next Aisle when there isn't one.'''
        aisle = Aisle.objects.create(active=True)
        self.assertEqual(aisle.get_next_aisle(), None)

    def test_get_previous_none(self):
        '''Get previous Aisle when there isn't one.'''
        aisle = Aisle.objects.create(active=True)
        self.assertEqual(aisle.get_previous_aisle(), None)

    def test_get_next_previous(self):
        '''Get next and previous Aisle when there is one.'''
        aisle_a = Aisle.objects.create(active=True, name="A Aisle",
                                       sort_name="a_aisle")
        aisle_b = Aisle.objects.create(active=True, name="B Aisle",
                                       sort_name="b_aisle")
        aisle_c = Aisle.objects.create(active=True, name="C Aisle",
                                       sort_name="c_aisle")

        self.assertEqual(aisle_b.get_next_aisle(), aisle_c)
        self.assertEqual(aisle_b.get_previous_aisle(), aisle_a)
