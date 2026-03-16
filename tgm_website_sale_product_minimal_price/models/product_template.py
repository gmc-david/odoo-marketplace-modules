# -*- coding: utf-8 -*-

from odoo import api, models


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
        price_arr = []
        # if product variant has price list defined
        if product_price_list:
            for price_list in product_price_list:
                price_arr.append(price_list.fixed_price)
            price_arr.sort()
        # else use price list which does not have the product_id (refers to the product template, applies to all variants)
        else:
            for price_list in product_template_price_list:
                price_arr.append(price_list.fixed_price)
            price_arr.sort()
        combination_info['min'] = 0.0
        combination_info['max'] = 0.0
        if len(price_arr) >= 2 and price_arr[0] != price_arr[-1]:
            combination_info['min'] = price_arr[0]
            combination_info['max'] = price_arr[-1]
        return combination_info

    @api.model
    def _search_get_detail(self, website, order, options):
        result = super()._search_get_detail(website, order, options)
        base_domain = result['base_domain']
        if(options.get('min_max_search')):
            product_tmpl_ids = self.get_min_max_price(options)
            base_domain = [sublist for sublist in base_domain if 'list_price' not in str(sublist)]
            base_domain.append([('id', 'in', product_tmpl_ids)])
            result['base_domain'] = base_domain
        return result

    def get_min_max_price(self, options):
        product_tmpl_ids = []
        domain = [
            ('pricelist_id', '=', options.get('pricelist_id')),
            ('product_tmpl_id', '!=', False)
        ]
        # Add price conditions only if they are provided
        if options.get('min_price') != 0.0:
            domain.append(('fixed_price', '>=', options['min_price']))
        if options.get('max_price') != 0.0:
            domain.append(('fixed_price', '<=', options['max_price']))
        price_list = self.env['product.pricelist.item'].sudo().search(domain)
        for price in price_list:
            product_tmpl_ids.append(price.product_tmpl_id.id)
        return product_tmpl_ids
