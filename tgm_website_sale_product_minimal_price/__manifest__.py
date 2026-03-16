# -*- coding: utf-8 -*-

{
    "name": "Website Sale Product Price Range Display",
    "summary": "Show 'from X to Y' price ranges on shop listings and product pages based on pricelist quantity tiers",
    "description": """
Website Sale Product Price Range Display
==========================================

Replace static prices with dynamic price ranges on your shop page and product pages.
When a product has quantity-based pricing, customers see the full price range at a
glance — making it clear that volume discounts are available.

Key Features:
-------------
* Automatic 'from X to Y' price display on shop listing pages
* Dynamic price range on individual product pages with variant support
* Qty Price display showing the current per-unit cost
* Real-time updates when variants or quantities change
* Extended shop search that includes products matching pricelist price filters
* Multi-currency compatible

Perfect for B2B stores, wholesale operations, or any business offering volume discounts.
    """,
    "version": "18.0.1.0.1",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "author": "The Great Merch Developers",
    "website": "https://thegreatmerch.com",
    "support": "hello@thegreatmerch.com",
    "price": 23.99,
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
            "tgm_website_sale_product_minimal_price/static/src/js/**",
        ]
    },
    "application": False,
    "installable": True,
}
