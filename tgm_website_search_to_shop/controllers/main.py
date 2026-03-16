# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class WebsiteSearchRedirect(Website):
    """
    Override the default website search to redirect to the /shop page,
    so customers see product cards in a grid instead of a plain text list.
    """

    @http.route('/website/search', type='http', auth='public', website=True, sitemap=False)
    def hybrid_content_search(self, search='', search_type='all', **kwargs):
        return request.redirect(f'/shop?search={request.httprequest.args.get("search", search)}')
