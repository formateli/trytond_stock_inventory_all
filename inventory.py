# This file is part of trytond-stock_inventory_all module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Inventory', ]


class Inventory:
    __metaclass__ = PoolMeta
    __name__ = 'stock.inventory'

    @classmethod
    def __setup__(cls):
        super(Inventory, cls).__setup__()
        cls._buttons.update({
            'complete_all': {
                'readonly': Eval('state') != 'draft',
                },
            })

    @classmethod
    @ModelView.button
    def complete_all(cls, inventories):
        pool = Pool()
        Product = pool.get('product.product')
        products = Product.search(
                [('active', '=', True), ('type', '!=', 'service')],
                order=[('name', 'ASC')]
            )
        for inventory in inventories:
            if inventory.lines: # Just once
                continue
            lines = []
            for product in products:
                line = cls.get_line_4_all(product)
                if line:
                    lines.append(line)
            if lines:
                inventory.lines = lines
                inventory.save()

    @classmethod
    def get_line_4_all(cls, product):
        line = Pool().get('stock.inventory.line')()
        line.product = product
        if product.template.count_uom:
            line.uom_1 = product.template.count_uom
        else:
            line.uom_1 = product.default_uom
        line.quantity_1 = 0.0
        line.quantity = 0.0
        # This way difference is calculated as expected
        line.expected_quantity = -1.0
        return line
