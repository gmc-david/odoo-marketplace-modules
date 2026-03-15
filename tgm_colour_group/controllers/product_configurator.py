from odoo.http import request

from odoo.addons.sale.controllers.product_configurator import (
    SaleProductConfiguratorController,
)
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductConfigurator(SaleProductConfiguratorController, WebsiteSale):

    def _get_product_information(
        self,
        product_template,
        combination,
        currency,
        pricelist,
        so_date,
        quantity=1,
        product_uom_id=None,
        parent_combination=None,
        **kwargs,
    ):
        res = super()._get_product_information(
            product_template=product_template,
            combination=combination,
            currency=currency,
            pricelist=pricelist,
            so_date=so_date,
            quantity=quantity,
            product_uom_id=product_uom_id,
            parent_combination=parent_combination,
            **kwargs,
        )
        colour_group_attr = request.env.ref(
            "tgm_colour_group.colour_group", raise_if_not_found=False
        )
        if colour_group_attr:
            attribute_id = colour_group_attr.id
            res["attribute_lines"] = [
                attr_line
                for attr_line in res.get("attribute_lines", [])
                if attr_line.get("attribute", {}).get("id") != attribute_id
            ]
        return res
