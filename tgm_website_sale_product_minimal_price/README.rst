=======================================
Website Sale Product Price Range Display
=======================================

Replace static product prices with dynamic "from X to Y" price ranges on your
shop listing pages and individual product pages. When a product has quantity-based
pricing, customers instantly see the full price range — making it clear that
volume discounts are available before they even click through.

**Table of contents**

.. contents::
   :local:

Features
========

* **Price Range on Shop Listings**: Shows "from £3.00 to £5.00" instead of a single price on the shop grid
* **Price Range on Product Pages**: Dynamic "from/to" display replaces the standard price when quantity tiers exist
* **Qty Price Display**: Shows the current per-unit cost based on the selected quantity
* **Variant Support**: Updates price range when customers select different product variants
* **Extended Shop Search**: Price filter on the shop page searches pricelist prices, not just list prices
* **Currency Support**: Displays prices in the correct currency with proper formatting
* **Automatic**: No per-product configuration needed — works from your existing pricelists

Installation
============

1. Download the module from the Odoo Apps Store
2. Go to Apps menu in your Odoo instance
3. Click "Update Apps List"
4. Search for "Website Sale Product Price Range Display"
5. Click "Install"

Configuration
=============

**Prerequisites:**

* You must have pricelists configured with quantity-based pricing rules
* Your pricelist must be linked to your website via eCommerce settings
* Products need at least two different price tiers for the range to display

**Setup Steps:**

1. Navigate to **Sales > Configuration > Pricelists**
2. Create or edit a pricelist with quantity-based rules (at least 2 tiers per product)
3. Assign the pricelist to your website via **Website > Configuration > eCommerce**
4. Visit your shop — price ranges will appear automatically

Usage
=====

**Shop Listing Page:**

Products with multiple price tiers will show:

::

    from £3.00 to £5.00

Instead of a single static price. Products without quantity-based pricing
continue to show their normal price.

**Product Page:**

The product page shows the full price range at the top, and a "Qty Price"
section that updates in real time as customers change quantities.

**Price Filter:**

The shop's price filter now searches pricelist prices in addition to list prices,
so products with lower quantity-tier prices correctly appear when customers
filter by price range.

Credits
=======

Authors
~~~~~~~

* The Great Merch Developers

Contributors
~~~~~~~~~~~~

* David Lynn <development@thegreatmerch.com>

Maintainers
~~~~~~~~~~~

This module is maintained by The Great Merch.

.. image:: https://thegreatmerch.com/logo.png
   :alt: The Great Merch
   :target: https://thegreatmerch.com

To learn more about The Great Merch, please visit https://thegreatmerch.com.
