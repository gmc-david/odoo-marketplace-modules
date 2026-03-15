/** @odoo-module */

import {Product} from "@sale/js/product/product";
import {patch} from "@web/core/utils/patch";

patch(Product.prototype, {
    /**
     * Hide the Colour Group attribute from the product configurator.
     *
     * We match on the attribute ID passed from the controller rather than
     * comparing the display name, so this works in any language.
     *
     * @override
     */
    shouldShowPtal(ptal) {
        if (ptal.attribute.name === "Colour Group") {
            return false;
        }
        return super.shouldShowPtal(...arguments);
    },
});
