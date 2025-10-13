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
      var $priceView = $parent.find('#price_list_view');
      if(combination.pricelist.length > 0 && combination.is_combination_possible){
        let bodyView = `<div class="d-flex w-auto border rounded-top border-bottom-0 text-center">
                            <span class="list-group-item w-50 border-end rounded-0">Minimum Qty</span>
                            <span class="list-group-item w-50">Price (${combination.currency_symbol})</span>
                        </div>
                        <div id="price_list_body" class="border border-top-0 rounded-bottom">
                        `
        let row = ``
        combination.pricelist.forEach(priceList => {
           row += `
            <div class=" d-flex border-top text-center">
              <span class="list-group-item w-50 border-end">${priceList.min_quantity}</span>
              <span class="list-group-item w-50">${combination.currency_position == 'before' ? combination.currency_symbol+''+priceList.fixed_price : priceList.fixed_price+''+combination.currency_symbol}</span>
            </div>
          `;
        });

        bodyView += row
        bodyView += `</div>`
        $priceView.html(bodyView)
      }else{
        $priceView.html('')
      }
    },
});
