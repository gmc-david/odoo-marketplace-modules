{
    "name": "Website Colour Group Filter",
    "summary": "Group 100+ supplier colour shades into clean, browsable categories for your eCommerce store.",
    "description": """
Website Colour Group Filter
============================

When you source products from multiple suppliers, your colour attribute can
quickly balloon to 100+ values — Navy, French Navy, Dark Navy, Midnight Blue,
and so on.  Shoppers just want to find "Blues".

This module lets you define Colour Groups (e.g. Blues, Reds, Greens) and
auto-assign products to them based on configurable colour terms.  On the
website the groups appear as a single, tidy filter that replaces the
overwhelming per-shade list.

Pre-configured groups
=====================
Installs with 12 ready-to-use colour groups — Blacks, Whites, Greys, Blues,
Reds, Greens, Yellows, Oranges, Pinks, Purples, Browns, and Multi-Colour —
each with comprehensive search terms covering hundreds of common colour names
from promotional merchandise, fashion, and homeware suppliers.

Key features
============
* 12 pre-configured colour groups with 500+ search terms out of the box.
* Auto-assign products to groups based on comma-separated colour terms.
* Batch processing with configurable batch size for large catalogues.
* Colour Group attribute hidden from sale order descriptions,
  the product configurator, and the website variant selector.
* Published / Unpublished product counts per group.
* Prevents accidental deletion of the system attribute.

Perfect for promotional merchandise, fashion, homeware, and any multi-supplier
marketplace where colour naming is inconsistent.
""",
    "version": "18.0.1.1.0",
    "category": "Website/Website",
    "depends": ["sale_management", "website_sale"],
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
        "security/ir.model.access.csv",
        "data/product_attribute_data.xml",
        "data/default_colour_groups.xml",
        "views/variant_templates.xml",
        "views/product_color_group_views.xml",
        "views/product_attribute_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "tgm_colour_group/static/src/js/product.js",
        ],
    },
    "application": False,
    "installable": True,
}
