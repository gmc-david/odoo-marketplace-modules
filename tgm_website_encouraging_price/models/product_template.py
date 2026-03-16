# -*- coding: utf-8 -*-

from odoo import models


class ProductTemplates(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, parent_combination=False, only_template=False):
        combination_info = super()._get_combination_info(
            combination, product_id, add_qty, parent_combination, only_template)
        website = self.env['website'].get_current_website().with_context(self.env.context)
        pricelist_id = website.pricelist_id
        pricelist_item = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', combination_info['product_template_id'])])
        product_price_list = []
        product_template_price_list = []
        for price_list in pricelist_item:
            # filter the price list according the product_id, product_template_id and available currency_id
            if price_list.product_id.id == combination_info['product_id'] and price_list.pricelist_id == pricelist_id:
                product_price_list.append(price_list)
            if not price_list.product_id and price_list.pricelist_id == pricelist_id:
                product_template_price_list.append(price_list)
        price_list_table = []
        # if product variant has price list defined
        if product_price_list:
            for price_list in product_price_list:
                price_list_table.append({
                    'min_quantity': int(price_list.min_quantity),
                    'fixed_price': price_list.fixed_price
                })
        # else use price list which does not have the product_id (refers to the product template, applies to all variants)
        else:
            for price_list in product_template_price_list:
                price_list_table.append({
                    'min_quantity': int(price_list.min_quantity),
                    'fixed_price': price_list.fixed_price
                })
        pricelist = sorted(price_list_table, key=lambda x: x['min_quantity'])
        price = combination_info['price']
        combination_info['encourage_message'] = self.encourage_more_purchase(add_qty, pricelist, price, combination_info['currency'].position, combination_info['currency'].symbol)
        return combination_info

    def encourage_more_purchase(self, quantity, pricelist, base_unit_price, currency_position, currency_symbol):
        new_price = 0
        temp_qty = 0
        for item in pricelist:
            if quantity < item['min_quantity']:
                temp_qty = item['min_quantity']
                new_price = item['fixed_price']
                break
        price_display = (f"{currency_symbol}{'{:.2f}'.format(new_price)}" if currency_position == "before" else f"{'{:.2f}'.format(new_price)}{currency_symbol}")
        if new_price < base_unit_price and temp_qty > 0:
            return f"Order {int(temp_qty - quantity)} more to reduce the price to {price_display} each"
        return "NA"
