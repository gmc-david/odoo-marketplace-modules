/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    start: function () {
        this._super.apply(this, arguments);
    },

    /**
     * Override _onChangeCombination method.
     * @override
     */
    _onChangeCombination: function (ev, $parent, combination) {
        this._super.apply(this, arguments);
        var $message = $parent.find("#encouraging_view");
        if (
            combination.is_combination_possible &&
            combination["encourage_message"] != "NA"
        ) {
            let row = `<div class="border-start border-3 border-primary bg-light rounded-end px-3 py-2">
                <small class="text-muted d-block mb-1">Save more</small>
                <span class="fw-semibold">${combination["encourage_message"]}</span>
            </div>`;
            $message.html(row);
        } else {
            $message.html("");
        }
    },
});
