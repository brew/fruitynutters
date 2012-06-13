var FNBundle = Class.create({
  initialize: function(bundle_container) {
    this.bundle_container = bundle_container;

    // Initially disable the add button
    $(bundle_container).down('.add_button').disable();

    // Set up the keyup event for the bundle's input fields.
    this.boundBundleInputKeyUp = this.onBundleKeyUp.bind(this);
    $(bundle_container).select('.bundle input.quantity').each(function(input, index) {
      input.observe('keyup',this.boundBundleInputKeyUp);
    }.bind(this));

    // Set up the keyup event for the bundle_container's quantity input field.
    this.boundQuantityInputKeyUp = this.onQuantityKeyUp.bind(this);
    $(bundle_container).down('.product_add input.quantity').observe('keyup', this.boundQuantityInputKeyUp);

    // this.setTotalUnitsElement();
  },

  /**
   *  Handler for keyup events on the bundle input fields.
   */
  onBundleKeyUp: function(ev) {
    // First check that the field contains a number. If it doesn't abort.
    if(ev.target.getValue() != "" && !this._isStringANumber(ev.target.getValue())) {
      ev.target.focus();
      return false;
    }

    this.setAddButton();

    // Reselect the input.
    ev.target.focus();

  },

  /**
   *  Handler for the keyup event on the product_add form's quantity input field.
   */
  onQuantityKeyUp: function(ev) {
    // First check that the field contains a number. If it doesn't abort.
    if(!this._isStringANumber(ev.target.getValue())) {
      ev.target.focus();
      return false;
    }

    // Set the new totalUnit quantity.
    this.setTotalUnitsElement();

    ev.target.focus();
  },

  /**
   *  Sets the total units element's innerhtml with the current quantity * the number of units in the item.
   */
  setTotalUnitsElement: function() {
    var currentQuantity = Number($(this.bundle_container).down('.product_add input.quantity').getValue());
    var totalUnits = currentQuantity * Number($(this.bundle_container).down('.single_unit').innerHTML);
    if( totalUnits != Number($(this.bundle_container).down('.total_units').innerHTML)) {
      $(this.bundle_container).down('.total_units').update(totalUnits);
      new Effect.Highlight($(this.bundle_container).down('.total_units'), { startcolor: '#ffff99', endcolor: '#E7F3EA', restorecolor: 'transparent'});
      this.setAddButton();
    }
  },

  /**
   *  Determines if the bundle is valid or not.
   *  Does it have enough bundle items choosen?
   */
  isBundleValid: function() {
    var allBundleInputs = $(this.bundle_container).select('.bundle input.quantity');
    var totalUnits = Number($(this.bundle_container).down('.total_units').innerHTML);

    var numberOfUnitsSelected = 0;

    for (var i=0;i<allBundleInputs.length;i++) {
      // If the input doesn't contain a number, the bundle is invalid.
      if(!this._isStringANumber(allBundleInputs[i].getValue()) && allBundleInputs[i].getValue() != "") return false;

      // Add the value of the context input to the numberOfUnitsSelected.
      numberOfUnitsSelected += Number(allBundleInputs[i].getValue());
    }

    return (numberOfUnitsSelected == totalUnits);
  },

  /**
   *  Sets the enabled state of the add button based on results from the isBundleValid method.
   */
  setAddButton: function() {
    // Now check that the bundle is valid and enable the add button if it is.
    if(this.isBundleValid()) {
      $(this.bundle_container).down('.add_button').enable();
    } else {
      $(this.bundle_container).down('.add_button').disable();
    }
  },

  /**
   *  Returns boolean determining if the passed string contains only digits.
   */
  _isStringANumber: function(str) {
    return (/^\d+$/.test(str));
  }


});


// Set up the bundles!
Event.observe(window, 'load', function(event){
  $$('.has_bundle').each(function(li, index) {
    new FNBundle(li);
  });
});
