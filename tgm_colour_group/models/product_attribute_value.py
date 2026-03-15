from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    product_count = fields.Integer(
        string="Products Count",
        compute="_compute_product_count",
    )

    @api.depends("pav_attribute_line_ids")
    def _compute_product_count(self):
        for pav in self:
            pav.product_count = len(pav.pav_attribute_line_ids)
