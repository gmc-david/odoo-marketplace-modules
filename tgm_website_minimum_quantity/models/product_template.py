# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tgm_minimum_qty = fields.Char('Minimum Order Quantity', default='1')
