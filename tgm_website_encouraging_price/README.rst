============================
Website Encouraging Price
============================

Boost your average order value by showing customers how close they are to the next
price break. This module displays a dynamic encouraging message on product pages
that nudges customers to add more items to unlock lower unit prices.

**Table of contents**

.. contents::
   :local:

Features
========

* **Dynamic Encouraging Messages**: Automatically calculates and displays how many more items a customer needs to reach the next price tier
* **Real-Time Updates**: Message updates instantly when customers change variants or quantities
* **Variant Support**: Works with both product templates and individual variants
* **Clean Badge Display**: Professional green badge that integrates with any theme
* **Easy Toggle**: Simple on/off control per product page via Website Builder
* **Currency Support**: Displays prices in the correct currency with proper formatting
* **Smart Logic**: Only shows when a genuine saving is available at the next tier

Installation
============

1. Download the module from the Odoo Apps Store
2. Go to Apps menu in your Odoo instance
3. Click "Update Apps List"
4. Search for "Website Encouraging Price"
5. Click "Install"

Configuration
=============

**Prerequisites:**

* You must have pricelists configured with quantity-based pricing rules
* Your pricelist must be linked to your website via eCommerce settings

**Setup Steps:**

1. Navigate to **Sales > Configuration > Pricelists**
2. Create or edit a pricelist with quantity-based rules
3. Assign the pricelist to your website via **Website > Configuration > eCommerce**
4. Enable the encouraging message on product pages:

   * Go to your website and navigate to any product page
   * Click "Edit" (website builder)
   * In the right sidebar, check the "Encouraging Price" option
   * Click "Save"

Usage
=====

Once configured, customers will see messages like:

::

    "Order 25 more to reduce the price to £3.50 each"

The message automatically updates as customers change quantities or select
different variants, always showing the next available price break.

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
