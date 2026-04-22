# -*- coding: utf-8 -*-

{
    "name": "Website Search Redirect to Shop",
    "summary": "Redirect website search results to the shop page so customers see product cards instead of a plain text list",
    "description": """
Website Search Redirect to Shop
=================================

Replaces Odoo's default website search results page with your shop product grid.
When a visitor searches from the website search bar, they are redirected to the
shop page with their search term applied — showing product cards in a familiar
grid layout instead of a generic text-based results list.

Key Features:
-------------
* Automatic redirect from website search to /shop
* Customers see product cards with images and prices instead of plain text
* Works with all standard Odoo themes
* No configuration needed — install and it just works
* Lightweight — no database changes, no new fields

Perfect for any Odoo eCommerce store that wants a better search experience.
    """,
    "version": "18.0.1.0.1",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "author": "The Great Merch Developers",
    "website": "https://thegreatmerch.com",
    "support": "hello@thegreatmerch.com",
    "price": 4.99,
    "currency": "EUR",
    "license": "LGPL-3",
    "images": [
        "static/description/banner.png",
    ],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "tgm_website_search_to_shop/static/src/js/search_redirect.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}
