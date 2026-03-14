# -*- coding: utf-8 -*-

{
    "name": "Website Encouraging Price Message",
    "summary": "Show dynamic 'order more to save' messages on product pages based on pricelist quantity tiers",
    "description": """
Website Encouraging Price Message
==================================

Boost your average order value by showing customers how close they are to the next
price break. This module displays a dynamic message on product pages that encourages
customers to add more items to unlock lower unit prices.

Key Features:
-------------
* Automatic encouraging messages based on Odoo pricelist quantity tiers
* Real-time updates when variants are selected or quantities change
* Clean badge-style display that integrates with any theme
* Easy to enable/disable via Website Builder toggle
* Supports both product variants and templates
* Multi-currency compatible

Perfect for B2B stores, wholesale operations, or any business offering volume discounts.
    """,
    "version": "18.0.1.0.1",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "author": "The Great Merch Developers",
    "website": "https://thegreatmerch.com",
    "support": "hello@thegreatmerch.com",
    "price": 19.99,
    "currency": "GBP",
    "license": "LGPL-3",
    "images": [
        "static/description/banner.png",
    ],
    "data": [
        "views/templates.xml",
        "views/snippets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "tgm_website_encouraging_price/static/src/js/**",
        ]
    },
    "application": False,
    "installable": True,
}
