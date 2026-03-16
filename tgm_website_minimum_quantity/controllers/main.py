# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
from odoo.addons.payment import utils as payment_utils
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.json import scriptsafe as json_scriptsafe


class MinQtyWebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(
        self, product_id, line_id=None, add_qty=None, set_qty=None, display=True,
        product_custom_attribute_values=None, no_variant_attribute_values=None, **kw
    ):
        """
        Override to enforce minimum order quantity.
        Called when changing quantity from the cart, adding from wishlist,
        or adding a product to cart on the same page.
        """

        # Enforce minimum quantity
        if request.website.tgm_min_qty_enabled:
            get_product = request.env['product.product'].sudo().browse(product_id)
            min_qty = int(get_product.tgm_minimum_qty)

            if add_qty is not None and add_qty < min_qty:
                add_qty = min_qty

            if set_qty is not None and set_qty != 0 and set_qty < min_qty:
                set_qty = min_qty

        order = request.website.sale_get_order(force_create=True)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=True)
            else:
                return {}

        if product_custom_attribute_values:
            product_custom_attribute_values = json_scriptsafe.loads(product_custom_attribute_values)

        if no_variant_attribute_values:
            no_variant_attribute_values = json_scriptsafe.loads(no_variant_attribute_values)

        values = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kw
        )

        request.session['website_sale_cart_quantity'] = order.cart_quantity

        values['notification_info'] = self._get_cart_notification_information(order, [values['line_id']])
        request.session['website_sale_cart_quantity'] = order.cart_quantity

        if not order.cart_quantity:
            request.website.sale_reset()
            return values

        values['cart_quantity'] = order.cart_quantity
        values['minor_amount'] = payment_utils.to_minor_currency_units(
            order.amount_total, order.currency_id
        ),
        values['amount'] = order.amount_total

        if not display:
            return values

        values['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template(
            "website_sale.cart_lines", {
                'website_sale_order': order,
                'date': fields.Date.today(),
                'suggested_products': order._cart_accessories()
            }
        )
        values['website_sale.total'] = request.env['ir.ui.view']._render_template(
            "website_sale.total", {
                'website_sale_order': order,
            }
        )
        return values
