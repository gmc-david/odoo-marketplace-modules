===============================
Website Minimum Order Quantity
===============================

Define minimum order quantities for individual products on your Odoo website shop.
When customers try to order fewer items than the minimum, the quantity is automatically
adjusted — ensuring every order meets your requirements.

**Table of contents**

.. contents::
   :local:

Features
========

* **Per-Product Minimum Quantity**: Set a minimum order quantity on each product template
* **Automatic Enforcement**: Quantities below the minimum are automatically adjusted on the product page and in the cart
* **Multi-Website Support**: Enable or disable the feature per website via a simple toggle in Website Settings
* **Default Quantity Display**: Product pages show the minimum quantity as the default, so customers see the correct starting point
* **Cart Protection**: Customers cannot reduce quantity below the minimum in the cart
* **Clean Integration**: Works with the standard Odoo website shop — no theme modifications required

Installation
============

1. Download the module from the Odoo Apps Store
2. Go to Apps menu in your Odoo instance
3. Click "Update Apps List"
4. Search for "Website Minimum Order Quantity"
5. Click "Install"

Configuration
=============

**Step 1: Enable the Feature**

1. Go to **Website > Configuration > Settings**
2. Find the **Minimum Order Quantity** section
3. Tick **Enable Minimum Order Quantity**
4. Save

**Step 2: Set Minimum Quantities on Products**

1. Go to **Sales > Products > Products**
2. Open a product
3. Set the **Minimum Order Quantity** field (e.g. 5, 10, 25)
4. Save

Usage
=====

Once configured:

* The product page will show the minimum quantity as the default value
* If a customer manually enters a quantity below the minimum, it is automatically adjusted
* The cart enforces the same minimum — quantities cannot be reduced below the threshold
* Products without a minimum quantity set (default = 1) behave normally

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
