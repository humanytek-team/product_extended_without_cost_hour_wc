# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _calc_price(self, bom):
        price = 0.0
        workcenter_cost = 0.0
        result, result2 = bom.explode(self, 1)
        for sbom, sbom_data in result2:
            if not sbom.attribute_value_ids:
                # No attribute_value_ids means the bom line is not variant specific
                price += sbom.product_id.uom_id._compute_price(sbom.product_id.standard_price, sbom.product_uom_id) * sbom_data['qty']

        # Convert on product UoM quantities
        if price > 0:
            price = bom.product_uom_id._compute_price(price / bom.product_qty, self.uom_id)
        return price
