=========================
Website Product Pricelist
=========================

Display quantity-based pricing tiers directly on your website product pages, making it easy for customers to see bulk pricing discounts at a glance.

**Table of contents**

.. contents::
   :local:

Features
========

* **Dynamic Price Display**: Automatically shows tiered pricing based on quantity breaks
* **Variant Support**: Updates pricing table when customers select different product variants
* **Responsive Design**: Mobile-friendly table that adapts to all screen sizes
* **Theme Integration**: Automatically matches your website's color scheme
* **Easy Toggle**: Simple on/off control per product page
* **Currency Support**: Displays prices in the correct currency with proper formatting
* **Clean Interface**: Professional, modern design that integrates seamlessly with Odoo

Installation
============

1. Download the module from the Odoo Apps Store
2. Go to Apps menu in your Odoo instance
3. Click "Update Apps List"
4. Search for "Website Product Pricelist"
5. Click "Install"

Configuration
=============

**Prerequisites:**

* You must have pricelists configured in Odoo (Sales > Products > Pricelists)
* Your pricelist should include quantity-based pricing rules

**Setup Steps:**

1. Navigate to **Sales > Configuration > Pricelists**
2. Create or edit a pricelist
3. Add pricelist items with quantity-based rules:
   
   * Select a product or product template
   * Set "Min. Quantity" (e.g., 1, 50, 100, 250)
   * Set "Fixed Price" for each quantity tier
   * Save the pricelist

4. Assign the pricelist to your website:
   
   * Go to **Website > Configuration > Settings**
   * Under "Shop - Products" section
   * Select your pricelist in the "Default Pricelist" field

5. Enable the price list display on product pages:
   
   * Go to your website
   * Navigate to any product page
   * Click "Edit" (website builder)
   * Click on the product area
   * In the right sidebar, check the "Price List" option
   * Click "Save"

Usage
=====

**For Website Administrators:**

Once configured, the pricelist table will automatically appear on product pages where you've enabled the "Price List" option. The table will show:

* Minimum quantity required for each price tier
* Price per unit at each tier
* Automatic updates when customers select different variants

**For Customers:**

Customers will see a clear pricing table showing:

* How much they'll pay at different quantity levels
* Instant savings from bulk purchases
* Real-time price updates as they select different product options

**Example Display:**

::

    MINIMUM QTY    PRICE
    1              £10.00
    50             £8.00
    100            £5.00
    250            £3.00

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