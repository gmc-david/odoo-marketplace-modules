{
    'name': 'PDF Flipbook Catalogue for Website',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Host your own PDF catalogues as interactive page-flip flipbooks on your Odoo website. No third-party hosting, unlimited catalogues, crisp pages on any device.',
    'description': """
PDF Flipbook Catalogue for Website
==================================

Turn any PDF into an interactive, page-flipping catalogue embedded directly
on your Odoo website. Upload a PDF, publish it, and your customers get a
smooth, magazine-style reading experience — no external services, no
recurring hosting fees, no per-view charges.

Key Features
------------
* Upload PDF catalogues, brochures, menus, lookbooks and magazines
* Realistic page-flip animation powered by StPageFlip
* Pages rendered live in the browser via PDF.js — always crisp, never pixelated
* Responsive design: works on desktop, tablet and mobile
* Fullscreen reading mode
* Keyboard, mouse and touch/swipe navigation
* Clean SEO-friendly URLs (/flipbook/your-slug)
* Publish / unpublish per catalogue
* Unlimited catalogues — host as many as you like
* Chunked upload for large PDFs (up to 2 GiB)
* No external dependencies on paid flipbook hosting services

Perfect For
-----------
* Retail catalogues and lookbooks
* Restaurant menus
* Brochures and sales material
* Magazines and newsletters
* Price lists
* Product brochures
* Annual reports
* Digital publishing

Why Self-Host Your Flipbooks?
-----------------------------
Stop paying monthly subscriptions to Issuu, FlippingBook, Yumpu and other
SaaS flipbook hosts. With this module your catalogues live on your own
Odoo website, your brand, your domain, your data.

Support
-------
Installs on Odoo 18 Community and Enterprise.
""",
    'author': 'The Great Merch Developers',
    'maintainer': 'The Great Merch Developers',
    'website': 'https://thegreatmerch.com',
    'support': 'development@thegreatmerch.com',
    'license': 'OPL-1',
    'price': 14.99,
    'currency': 'EUR',
    'images': [
        'static/description/banner.png',
    ],
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/tgm_flipbook_views.xml',
        'views/tgm_flipbook_menus.xml',
        'views/tgm_flipbook_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tgm_flipbook/static/src/scss/tgm_flipbook.scss',
            'tgm_flipbook/static/src/js/tgm_flipbook_viewer.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
