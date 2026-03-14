# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class ProductMinimalWebsiteSale(WebsiteSale):

    def min_max_price_list(self, product_templ_ids, pricelist_id):
        domain = [
            '&',
            ('product_tmpl_id', 'in', product_templ_ids.ids),
            ('pricelist_id', '=', pricelist_id.id)
        ]
        price_list = request.env['product.pricelist.item'].search(domain)
        result = {}
        for prices in price_list:
            product_id = prices.product_tmpl_id
            price = prices.fixed_price
            if product_id in result:
                result[product_id]['min_price'] = min(result[product_id]['min_price'], price)
                result[product_id]['max_price'] = max(result[product_id]['max_price'], price)
            else:
                result[product_id] = {'min_price': price, 'max_price': price}
        return result

    @route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        response = super().shop(page, category, search, min_price, max_price, ppg, **post)
        website = request.env['website'].get_current_website()
        response.qcontext['product_min_max_prices'] = self.min_max_price_list(response.qcontext.get('search_product'), website.pricelist_id)
        return response

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_product = super()._shop_lookup_products(attrib_set, options, post, search, website)
        options['min_max_search'] = True
        options['pricelist_id'] = website.pricelist_id.id
        product_count_2, details, fuzzy_search_term_2 = website._search_with_fuzzy("products_only", search,
                                                                               limit=None,
                                                                               order=self._get_search_order(post),
                                                                               options=options)
        search_result = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        existing_product_ids = [product.id for product in search_product]
        # Iterate through search_result and add products that don't already exist
        for product in search_result:
            if product.id not in existing_product_ids:
                search_product += product
        product_ids = list({product.id for product in search_product})
        search_product = request.env['product.template'].search([('id', 'in', product_ids)], order=self._get_search_order(post))
        product_count = len(search_product)
        return fuzzy_search_term, product_count, search_product
