from odoo import models
from odoo.exceptions import UserError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    def unlink(self):
        colour_group_attr = self.env.ref(
            "tgm_colour_group.colour_group", raise_if_not_found=False
        )
        if colour_group_attr and colour_group_attr in self:
            raise UserError(
                "This attribute is managed by the 'Colour Group' module. "
                "Uninstall the module to remove it."
            )
        return super().unlink()
