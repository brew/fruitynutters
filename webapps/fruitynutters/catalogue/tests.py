from decimal import Decimal

from django.test import TestCase

from fruitynutters.catalogue.models import Aisle, Item


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


class ItemSizeTestCase(TestCase):

    def setUp(self):
        self.aisle = Aisle.objects.create(active=True)

    def test_size_none(self):
        '''Item with no measure_per_unit, returns None size.'''
        product = Item.objects.create(name="My Product",
                                      active=True,
                                      organic=True,
                                      new_changed=False,
                                      unit_number=1,
                                      aisle=self.aisle,
                                      price=Decimal('2.50'))
        self.assertEqual(product.size, None)

    def test_size_with_type(self):
        '''Item with a measure_per_unit and a measure_type returns a correct
        size.'''
        product = Item.objects.create(name="My Product",
                                      active=True,
                                      organic=True,
                                      new_changed=False,
                                      unit_number=1,
                                      aisle=self.aisle,
                                      price=Decimal('2.50'),
                                      measure_per_unit=25,
                                      measure_type='g')
        self.assertEqual(product.size, '25g')

    def test_size_with_no_type(self):
        '''Item with a measure_per_unit but no measure_type returns a correct
        size.'''
        product = Item.objects.create(name="My Product",
                                      active=True,
                                      organic=True,
                                      new_changed=False,
                                      unit_number=1,
                                      aisle=self.aisle,
                                      price=Decimal('2.50'),
                                      measure_per_unit=25)
        self.assertEqual(product.size, '25')
