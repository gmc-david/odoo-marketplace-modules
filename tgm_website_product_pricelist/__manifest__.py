# -*- coding: utf-8 -*-

{
    "name": "Website Quantity Tiered Pricing Table",
    "summary": "Display dynamic quantity-based pricing tables on product pages with automatic variant updates",
    "description": """
Website Quantity Tiered Pricing Table
======================================

Showcase your volume discounts and quantity-based pricing directly on product pages.
This module automatically displays a professional pricing table that updates in real-time
as customers select different product variants.

Key Features:
-------------
* Automatic tiered pricing display based on Odoo pricelists
* Real-time updates when variants are selected
* Clean, responsive design for all devices
* Easy to enable/disable via website builder
* Supports both product variants and templates
* Multi-currency compatible

Perfect for B2B stores, wholesale operations, or any business offering volume discounts.
    """,
    "version": "18.0.1.0.1",
    "category": "Website/Website",
    "depends": ['website_sale'],
    "author": "The Great Merch Developers",
    "website": "https://thegreatmerch.com",
    "support": "hello@thegreatmerch.com",
    "price": 49.99,
    "currency": "EUR",
    "license": "LGPL-3",
    "images": [
        "static/description/banner.png",
        "static/description/icon.png",
    ],
    "data": [
        'views/templates.xml',
        'views/snippets.xml'
    ],
    "assets": {
        "web.assets_frontend": [
            'tgm_website_product_pricelist/static/src/css/pricelist_styles.css',
            'tgm_website_product_pricelist/static/src/js/**'
        ]
    },
    "application": False,
    "installable": True,
}