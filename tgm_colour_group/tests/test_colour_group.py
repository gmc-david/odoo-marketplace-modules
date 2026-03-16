from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestColourGroup(TransactionCase):
    """Tests for the Colour Group module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.colour_group_attr = cls.env.ref("tgm_colour_group.colour_group")

        # Create an attribute value for testing
        cls.attr_value_blue = cls.env["product.attribute.value"].create({
            "name": "Blues",
            "attribute_id": cls.colour_group_attr.id,
            "html_color": "#0000FF",
        })

        cls.attr_value_red = cls.env["product.attribute.value"].create({
            "name": "Reds",
            "attribute_id": cls.colour_group_attr.id,
            "html_color": "#FF0000",
        })

        # Create a colour attribute (simulating supplier data)
        cls.color_attribute = cls.env["product.attribute"].create({
            "name": "Colour",
            "display_type": "color",
            "create_variant": "always",
        })

        cls.color_val_navy = cls.env["product.attribute.value"].create({
            "name": "Navy",
            "attribute_id": cls.color_attribute.id,
        })
        cls.color_val_french_navy = cls.env["product.attribute.value"].create({
            "name": "French Navy",
            "attribute_id": cls.color_attribute.id,
        })
        cls.color_val_crimson = cls.env["product.attribute.value"].create({
            "name": "Crimson",
            "attribute_id": cls.color_attribute.id,
        })

        # Create test products
        cls.product_navy = cls.env["product.template"].create({
            "name": "Navy T-Shirt",
            "attribute_line_ids": [(0, 0, {
                "attribute_id": cls.color_attribute.id,
                "value_ids": [(4, cls.color_val_navy.id)],
            })],
        })
        cls.product_french_navy = cls.env["product.template"].create({
            "name": "French Navy Polo",
            "attribute_line_ids": [(0, 0, {
                "attribute_id": cls.color_attribute.id,
                "value_ids": [(4, cls.color_val_french_navy.id)],
            })],
        })
        cls.product_crimson = cls.env["product.template"].create({
            "name": "Crimson Hoodie",
            "attribute_line_ids": [(0, 0, {
                "attribute_id": cls.color_attribute.id,
                "value_ids": [(4, cls.color_val_crimson.id)],
            })],
        })

    # -------------------------------------------------------------------------
    # Colour Group CRUD
    # -------------------------------------------------------------------------

    def test_create_colour_group(self):
        """A colour group can be created with basic fields."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "value_id": self.attr_value_blue.id,
        })
        self.assertEqual(group.name, "Blues")
        self.assertEqual(group.attribute_id, self.colour_group_attr)

    def test_cannot_delete_group_with_products(self):
        """Deleting a group that still has products raises UserError."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "value_id": self.attr_value_blue.id,
            "product_ids": [(4, self.product_navy.id)],
        })
        with self.assertRaises(UserError):
            group.unlink()

    def test_delete_empty_group(self):
        """An empty colour group can be deleted."""
        group = self.env["product.color.group"].create({
            "name": "Empty Group",
            "color_code": "#CCCCCC",
        })
        group.unlink()

    # -------------------------------------------------------------------------
    # Auto-assignment
    # -------------------------------------------------------------------------

    def test_auto_assign_finds_matching_products(self):
        """Auto-assign matches products by colour term."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "color_terms": "navy, french navy",
            "value_id": self.attr_value_blue.id,
        })
        result = group.auto_assign_products()
        self.assertTrue(result)
        self.assertIn(self.product_navy, group.product_ids)
        self.assertIn(self.product_french_navy, group.product_ids)
        self.assertNotIn(self.product_crimson, group.product_ids)

    def test_auto_assign_preserves_manual_products(self):
        """Auto-assign adds to existing products rather than replacing."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "color_terms": "navy",
            "value_id": self.attr_value_blue.id,
            "product_ids": [(4, self.product_crimson.id)],  # manually added
        })
        group.auto_assign_products()
        # Crimson was manually added and should still be there
        self.assertIn(self.product_crimson, group.product_ids)
        self.assertIn(self.product_navy, group.product_ids)

    def test_auto_assign_no_terms_returns_false(self):
        """Auto-assign with empty terms returns False."""
        group = self.env["product.color.group"].create({
            "name": "Empty",
            "color_code": "#000000",
        })
        self.assertFalse(group.auto_assign_products())

    # -------------------------------------------------------------------------
    # Batch processing
    # -------------------------------------------------------------------------

    def test_batch_size_limit(self):
        """Batch size above MAX_BATCH_SIZE raises UserError."""
        with self.assertRaises(UserError):
            self.env["product.color.group"].create({
                "name": "Too Big",
                "color_code": "#000000",
                "batch_size": 500,
                "product_ids": [(4, self.product_navy.id)],
            })

    def test_total_batches_calculation(self):
        """Total batches is correctly computed from product count and batch size."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "batch_size": 2,
            "product_ids": [
                (4, self.product_navy.id),
                (4, self.product_french_navy.id),
                (4, self.product_crimson.id),
            ],
        })
        self.assertEqual(group.total_batches, 2)  # ceil(3/2) = 2

    def test_refresh_batch_data(self):
        """Refresh resets all batch counters to zero."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "value_id": self.attr_value_blue.id,
        })
        group.write({
            "current_batch": 5,
            "last_processed_id": 999,
            "current_remove_batch": 3,
            "last_remove_processed_id": 888,
        })
        group.refresh_batch_data()
        self.assertEqual(group.current_batch, 0)
        self.assertEqual(group.last_processed_id, 0)
        self.assertEqual(group.current_remove_batch, 0)
        self.assertEqual(group.last_remove_processed_id, 0)

    # -------------------------------------------------------------------------
    # Attribute update
    # -------------------------------------------------------------------------

    def test_update_adds_attribute_to_product(self):
        """Batch update assigns the colour group attribute value to products."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "value_id": self.attr_value_blue.id,
            "batch_size": 100,
            "product_ids": [(4, self.product_navy.id)],
        })
        group.action_update_product_attribute()

        # Check the product now has the Colour Group attribute
        cg_line = self.product_navy.attribute_line_ids.filtered(
            lambda l: l.attribute_id == self.colour_group_attr
        )
        self.assertTrue(cg_line)
        self.assertIn(self.attr_value_blue, cg_line.value_ids)

    def test_update_completed_notification(self):
        """When all products processed, returns success notification."""
        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "value_id": self.attr_value_blue.id,
            "batch_size": 100,
            "product_ids": [(4, self.product_navy.id)],
        })
        # First call processes the product
        group.action_update_product_attribute()
        # Second call should report completion
        result = group.action_update_product_attribute()
        self.assertEqual(result["params"]["type"], "success")

    # -------------------------------------------------------------------------
    # Product counts
    # -------------------------------------------------------------------------

    def test_product_counts(self):
        """Published and unpublished counts are correct."""
        self.product_navy.website_published = True
        self.product_french_navy.website_published = False

        group = self.env["product.color.group"].create({
            "name": "Blues",
            "color_code": "#0000FF",
            "product_ids": [
                (4, self.product_navy.id),
                (4, self.product_french_navy.id),
            ],
        })
        self.assertEqual(group.product_count, 2)
        self.assertEqual(group.published_count, 1)
        self.assertEqual(group.unpublished_count, 1)

    # -------------------------------------------------------------------------
    # Attribute protection
    # -------------------------------------------------------------------------

    def test_cannot_delete_colour_group_attribute(self):
        """The system Colour Group attribute cannot be deleted."""
        with self.assertRaises(UserError):
            self.colour_group_attr.unlink()

    def test_can_delete_other_attributes(self):
        """Other attributes can still be deleted normally."""
        attr = self.env["product.attribute"].create({
            "name": "Disposable Test Attribute",
            "create_variant": "no_variant",
        })
        attr.unlink()  # Should not raise

    # -------------------------------------------------------------------------
    # Sale order line description
    # -------------------------------------------------------------------------

    def test_sale_line_strips_colour_group(self):
        """The Colour Group line is removed from the SO line description."""
        sol = self.env["sale.order.line"].new({})
        # Simulate what the parent method returns
        original = "Colour Group: Blues\nColour: Navy\nSize: M"
        # Patch the super to return our test string
        with self._mock_sol_description(sol, original):
            result = sol._get_sale_order_line_multiline_description_variants()
        self.assertNotIn("Colour Group", result)
        self.assertIn("Colour: Navy", result)
        self.assertIn("Size: M", result)

    @staticmethod
    def _mock_sol_description(sol, description):
        """Context manager to mock the parent description method."""
        import unittest.mock as mock

        return mock.patch.object(
            type(sol).__mro__[1],
            "_get_sale_order_line_multiline_description_variants",
            return_value=description,
        )
