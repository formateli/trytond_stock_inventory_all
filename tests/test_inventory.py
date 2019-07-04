# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class InventoryAllTestCase(ModuleTestCase):
    'Test Stock Inventory All'
    module = 'stock_inventory_all'

    @with_transaction()
    def test_stock_inventory_all(self):
        pool = Pool()
        Inventory = pool.get('stock.inventory')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        InventoryAllTestCase))
    return suite
