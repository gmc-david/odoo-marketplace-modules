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
      const $priceMain = $parent.find('#oe_price_main');
      var $price = $parent.find("#product_page_price");
      var $qtyPriceContainer = $parent.find('#product_qty_price_container')

      if(combination.min > 0 && combination.max > 0){
        $priceMain.addClass('d-none')
        $qtyPriceContainer.removeClass('d-none')

        // show product price container if the min and max price available
        const formatToTwoDecimals = num => {
          let numStr = num.toString();
          return numStr.includes('.') ? num.toFixed(2) : `${num}.00`;
        };
        $price.removeClass('d-none');

        //  update the dynamic value of min price
        var $minPrice = $parent.find("#product_min_price:first .oe_currency_value");
        $minPrice.text(formatToTwoDecimals(combination.min))

        //  update the dynamic value of max price
        var $maxPrice = $parent.find("#product_max_price:first .oe_currency_value");
        $maxPrice.text(formatToTwoDecimals(combination.max));

        // update the qty price dynamic
        var $qtyPrice = $parent.find('#product_qty_price .oe_currency_value')
        $qtyPrice.text(formatToTwoDecimals(combination.price))
      }else{
        // if not available min and max price show default price
        $priceMain.removeClass('d-none')
        $price.addClass('d-none');
        $qtyPriceContainer.addClass('d-none');
      }
      // hide if combination not possible
      if(!combination.is_combination_possible){
        var $qtyPriceContainer = $parent.find('#product_qty_price_container')
        $qtyPriceContainer.addClass('d-none')
      }
    },
});
