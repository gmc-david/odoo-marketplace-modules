# -*- coding: utf-8 -*-

{
    "name": "Website Minimum Order Quantity",
    "summary": "Set minimum order quantities per product on your website shop with automatic enforcement",
    "description": """
Website Minimum Order Quantity
===============================

Define minimum order quantities for individual products on your Odoo website shop.
When customers try to add fewer items than the minimum, the quantity is automatically
adjusted to meet the minimum requirement.

Key Features:
-------------
* Set minimum quantity per product template
* Automatic enforcement on the product page and in the cart
* Multi-website support with a simple toggle
* Default quantity on product pages matches the minimum
* Customers cannot reduce below the minimum quantity
* Clean integration with the standard Odoo website shop

Perfect for wholesale, B2B, and any store where minimum order quantities apply.
    """,
    "version": "18.0.1.0.1",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "author": "The Great Merch Developers",
    "website": "https://thegreatmerch.com",
    "support": "hello@thegreatmerch.com",
    "price": 9.99,
    "currency": "EUR",
    "license": "LGPL-3",
    "images": [
        "static/description/banner.png",
    ],
    "data": [
        "views/product_views.xml",
        "views/website_templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
