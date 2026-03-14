# -*- coding: utf-8 -*-

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    tgm_min_qty_enabled = fields.Boolean("Enable Minimum Order Quantity", default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tgm_min_qty_enabled = fields.Boolean(
        related="website_id.tgm_min_qty_enabled",
        string="Enable Minimum Order Quantity",
        readonly=False,
    )
