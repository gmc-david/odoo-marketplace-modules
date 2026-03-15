from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_sale_order_line_multiline_description_variants(self):
        """Remove the Colour Group attribute from the sale order line description.

        We match on the attribute ID rather than the display name so this
        works correctly in non-English installations.
        """
        res = super()._get_sale_order_line_multiline_description_variants()
        colour_group_attr = self.env.ref(
            "tgm_colour_group.colour_group", raise_if_not_found=False
        )
        if not colour_group_attr:
            return res

        attr_name = colour_group_attr.name
        filtered_lines = [
            line
            for line in res.splitlines()
            if not line.startswith(attr_name + ":")
        ]
        return "\n".join(filtered_lines)
