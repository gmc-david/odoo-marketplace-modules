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
            # filter the price list according the product_id , product_tempalte_id and available currency_id
            if price_list.product_id.id == combination_info['product_id'] and price_list.pricelist_id == pricelist_id:
                product_price_list.append(price_list)
            if not price_list.product_id and price_list.pricelist_id == pricelist_id:
                product_template_price_list.append(price_list)
        price_list_table = []
        # if product variant have price list defien
        if product_price_list:
            for price_list in product_price_list:
                price_list_table.append({
                    'min_quantity':int(price_list.min_quantity),
                    'fixed_price': "{:.2f}".format(price_list.fixed_price)
                })
        # else use price list which not have the product_id mean refer to the product template implement on all variant
        else:
            for price_list in product_template_price_list:
                price_list_table.append({
                    'min_quantity':int(price_list.min_quantity),
                    'fixed_price': "{:.2f}".format(price_list.fixed_price)
                })
        combination_info['pricelist'] = sorted(price_list_table, key=lambda x: x['min_quantity'])
        combination_info['currency_position'] = combination_info['currency'].position
        combination_info['currency_symbol'] = combination_info['currency'].symbol
        return combination_info
