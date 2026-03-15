import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

MAX_BATCH_SIZE = 300


class ProductColorGroup(models.Model):
    _name = "product.color.group"
    _description = "Product Colour Group"
    _order = "sequence, name"

    name = fields.Char(string="Colour Group Name", required=True)
    color_code = fields.Char(
        required=True,
        default="#FFFFFF",
        help="HTML colour code (e.g. #FF0000 for red)",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    color_terms = fields.Text(
        help="Comma-separated colour terms for auto-assignment "
        "(e.g. navy, french navy, dark navy, midnight blue)",
    )
    product_ids = fields.Many2many("product.template")
    attribute_id = fields.Many2one(
        "product.attribute",
        string="Attribute",
        default=lambda self: self.env.ref(
            "tgm_colour_group.colour_group", raise_if_not_found=False
        ),
        readonly=True,
    )
    value_id = fields.Many2one(
        "product.attribute.value",
        string="Attribute Value",
        domain="[('attribute_id', '=', attribute_id)]",
    )
    published_count = fields.Integer(
        string="Published",
        compute="_compute_product_counts",
    )
    unpublished_count = fields.Integer(
        string="Unpublished",
        compute="_compute_product_counts",
    )
    product_count = fields.Integer(
        string="Total Products",
        compute="_compute_product_counts",
    )
    batch_size = fields.Integer(
        string="Batch Size",
        default=100,
        help="Number of products to process in each batch operation.",
    )
    total_batches = fields.Integer(
        string="Total Batches",
        compute="_compute_total_batches",
        store=True,
        help="Total number of batches based on selected products and batch size.",
    )
    current_batch = fields.Integer(
        string="Current Batch",
        readonly=True,
        default=0,
    )
    last_processed_id = fields.Integer(
        string="Last Processed Product ID",
        default=0,
    )
    current_remove_batch = fields.Integer(
        string="Recent Removed Batch",
        readonly=True,
        default=0,
    )
    last_remove_processed_id = fields.Integer(
        string="Last Remove Processed Product ID",
        default=0,
    )

    # -------------------------------------------------------------------------
    # Computed fields
    # -------------------------------------------------------------------------

    @api.depends("product_ids", "product_ids.website_published")
    def _compute_product_counts(self):
        for group in self:
            published = group.product_ids.filtered("website_published")
            group.published_count = len(published)
            group.unpublished_count = len(group.product_ids) - len(published)
            group.product_count = len(group.product_ids)

    @api.depends("product_ids", "batch_size")
    def _compute_total_batches(self):
        for rec in self:
            if rec.batch_size > MAX_BATCH_SIZE:
                raise UserError(
                    "Batch size cannot exceed %d to avoid timeout issues."
                    % MAX_BATCH_SIZE
                )
            if rec.batch_size > 0:
                rec.total_batches = (
                    len(rec.product_ids) + rec.batch_size - 1
                ) // rec.batch_size
            else:
                rec.total_batches = 0

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def refresh_batch_data(self):
        """Reset all batch tracking counters."""
        self.write({
            "last_remove_processed_id": 0,
            "current_remove_batch": 0,
            "current_batch": 0,
            "last_processed_id": 0,
        })

    def auto_assign_products(self):
        """Auto-assign products to this colour group based on colour terms.

        Products are *added* to the existing set — manually assigned products
        are preserved.
        """
        self.ensure_one()
        if not self.color_terms:
            return False

        terms = [
            term.strip().lower()
            for term in self.color_terms.split(",")
            if term.strip()
        ]
        if not terms:
            return False

        # Find colour-related attributes
        color_attrs = self.env["product.attribute"].search(
            ["|", ("name", "ilike", "color"), ("name", "ilike", "colour")]
        )
        if not color_attrs:
            return False

        # Build domain for matching attribute values
        value_domain = [("attribute_id", "in", color_attrs.ids)]
        value_domain += ["|"] * (len(terms) - 1) + [
            ("name", "ilike", term) for term in terms
        ]
        matching_values = self.env["product.attribute.value"].search(value_domain)

        if matching_values:
            matching_products = self.env["product.template"].search(
                [("attribute_line_ids.value_ids", "in", matching_values.ids)]
            )
            # Use (4, id) to ADD products rather than replacing the set
            new_products = matching_products - self.product_ids
            if new_products:
                self.write(
                    {"product_ids": [(4, pid) for pid in new_products.ids]}
                )
            return True
        return False

    def action_update_product_attribute(self):
        """Assign the colour group attribute value to products in batches."""
        self.ensure_one()
        if not self.value_id:
            raise UserError("Please select an Attribute Value before updating.")

        sorted_products = self.product_ids.sorted(key=lambda p: p.id)
        remaining = sorted_products.filtered(
            lambda p: p.id > self.last_processed_id
        )

        if not remaining:
            return self._batch_notification(
                "Completed", "All products have been updated.", "success"
            )

        batch = remaining[: self.batch_size]
        attr_id = self.value_id.attribute_id.id
        value_id = self.value_id.id

        for product in batch:
            existing_line = product.attribute_line_ids.filtered(
                lambda l: l.attribute_id.id == attr_id
            )
            if existing_line:
                if self.value_id not in existing_line.value_ids:
                    existing_line.write({"value_ids": [(4, value_id)]})
            else:
                product.write({
                    "attribute_line_ids": [
                        (0, 0, {
                            "attribute_id": attr_id,
                            "value_ids": [(4, value_id)],
                        })
                    ]
                })

        self.write({
            "last_processed_id": batch[-1].id,
            "current_batch": self.current_batch + 1,
        })
        batches_left = self.total_batches - self.current_batch
        return self._batch_notification(
            "Batch %d/%d" % (self.current_batch, self.total_batches),
            "%d products processed. %d batches left." % (len(batch), batches_left),
            "info",
        )

    def action_remove_product(self):
        """Remove the colour group attribute value from products in batches."""
        self.ensure_one()
        if not self.value_id:
            raise UserError("Please select an Attribute Value before removing.")

        sorted_products = self.product_ids.sorted(key=lambda p: p.id)
        remaining = sorted_products.filtered(
            lambda p: p.id > self.last_remove_processed_id
        )

        if not remaining:
            return self._batch_notification(
                "Completed", "All products have been removed.", "success"
            )

        batch = remaining[: self.batch_size]
        batch_ids = batch.ids
        self._update_attribute_lines(self.value_id, batch_ids)
        self.write({"product_ids": [(3, pid) for pid in batch_ids]})

        self.write({
            "last_remove_processed_id": batch[-1].id,
            "current_remove_batch": self.current_remove_batch + 1,
        })
        batches_left = self.total_batches - self.current_remove_batch
        return self._batch_notification(
            "Batch %d/%d" % (self.current_remove_batch, self.total_batches),
            "%d products processed. %d batches left." % (len(batch), batches_left),
            "info",
        )

    # -------------------------------------------------------------------------
    # CRUD overrides
    # -------------------------------------------------------------------------

    def write(self, vals):
        res = super().write(vals)
        if "product_ids" in vals:
            for rec in self:
                if not rec.value_id:
                    continue
                removed_ids = self._extract_removed_ids(vals["product_ids"])
                if removed_ids:
                    rec._update_attribute_lines(rec.value_id, removed_ids)
        return res

    def unlink(self):
        for rec in self:
            if rec.product_ids:
                raise UserError(
                    "Please remove all products from '%s' before deleting it."
                    % rec.name
                )
        return super().unlink()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _extract_removed_ids(m2m_operations):
        """Extract product IDs from M2M write operations that represent removals.

        Handles both (3, id) individual unlinks and (6, 0, ids) full replacements.
        """
        removed_ids = []
        for op in m2m_operations:
            if not isinstance(op, (list, tuple)):
                continue
            if op[0] == 3:
                removed_ids.append(op[1])
        return removed_ids

    def _update_attribute_lines(self, removed_value, product_ids):
        """Remove an attribute value from the given products' attribute lines.

        If the attribute line has no remaining values after removal, the line
        is deleted entirely.
        """
        products = self.env["product.template"].browse(product_ids)
        for product in products:
            lines_to_remove = product.attribute_line_ids.filtered(
                lambda l: (
                    l.attribute_id == removed_value.attribute_id
                    and removed_value in l.value_ids
                )
            )
            for line in lines_to_remove:
                new_values = line.value_ids - removed_value
                if new_values:
                    line.write({"value_ids": [(6, 0, new_values.ids)]})
                else:
                    line.unlink()

    @staticmethod
    def _batch_notification(title, message, notif_type):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": notif_type,
                "sticky": False,
            },
        }
