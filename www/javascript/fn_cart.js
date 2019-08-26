class FNCart {
  constructor() {
    // Intercept the product add form submit event.
    this.boundAddSubmit = this.onAddFormSubmit.bind(this);
    $$('.product_add').each(function(form, index) {
      form.observe('submit', this.boundAddSubmit);
    }, this);

    if($('virtualshop_form')) {
      this.boundAddVirtualSubmit = this.onVirtualShopAddFormSubmit.bind(this);
      $('virtualshop_form').observe('submit', this.boundAddVirtualSubmit);
    }

    if($('save_details_button')) {
      $('save_details_button').observe('click', this.onSaveDetailsButtonClick.bind(this));
    }

    this._prepareCart();
  }

  /**
   *  Handler for the Submit event on the product add forms.
   */
  onAddFormSubmit(ev){
    ev.stop();

    // Get the quantity to add.
    var quantity = $(ev.target).down('.quantity').value;
    // Bail out if the quantity isn't a number.
    if(!this._isStringANumber(quantity)) return false;

    var url = ev.target.action;
    var serializedData = ev.target.serialize();
    this.updateCart(url, serializedData);
  }

  /**
   *  Handler for submission of the add write-in form.
   */
  onAddWriteinFormSubmit(ev) {
    ev.stop();
    this.updateCart(ev.target.action, ev.target.serialize());
  }

  /**
   *  Handler for submission of the add virtual shop item form.
   */
  onVirtualShopAddFormSubmit(ev) {
    ev.stop();
    var completeAction = function(transport) {
      this._prepareCart();
      if($$('.cart_error').length == 0)
        ev.target.reset();
    }.bind(this);
    this.updateCart(ev.target.action, ev.target.serialize(), completeAction);
  }

  /**
   *  Handler for the remove item button.
   */
  onRemoveItem(ev) {
    ev.stop();
    this.updateCart($(ev.target).up('a.remove_item').href);
  }

  /**
   *  Handler for the click event on the empty list link.
   */
  onEmptyList(ev) {
    ev.stop();
    this.updateCart("/cart/empty/");
  }

  /**
   *  Handler for the submission of the cart form (Update cart).
   */
  onCartUpdateSubmit(ev) {
    ev.stop();
    if(ev.target.serialize() != this.serializedCart) {
      // console.info(ev.target.serialize());
      this.updateCart(ev.target.action, ev.target.serialize());
    } else {
      // console.info('Cart has not changed.');
    }
  }

  /**
   *  Handler for when a key is pressed in the cart inputs.
   */
  onCartKeyUp(ev) {
    if(ev.target.serialize() != this.serializedCart)
      $('update_list_button').enable();
    else
      $('update_list_button').disable();
  }

  /**
   *  Updates the cart with a given url and parameters, updating the cart container with the successful return value.
   */
  updateCart(url, parameters, completeAction) {

    completeAction = completeAction || function() {this._prepareCart();}.bind(this);

    this._prepareCartForUpdate();

    $('cart_load_indicator').show();

    new Ajax.Updater({success:'cart_content', failure:'cart_notice'}, url, {
      method:'post',
      parameters:parameters,
      onComplete: completeAction
    });
  }

  /**
   *  Handler for click of the save details button.
   */
  onSaveDetailsButtonClick(ev) {
    new Ajax.Request('/cart/savedetails/', {
      method: 'post',
      parameters:$('order_details').serialize(),
      onSuccess: function(transport) {
        window.location.replace("/catalogue/aisle/");
      },
      onFailure: function(transport) {

      }
    });
  }

  /**
   *  Prepares the cart at initialize and each time it's been updated.
   */
  _prepareCart() {
    this.serializedCart = $('cart_form').serialize();

    this.boundEmptyList = this.onEmptyList.bind(this);
    $('empty_list').observe('click', this.boundEmptyList);

    this.boundRemoveItem = this.onRemoveItem.bind(this);
    $$('#cart_form .remove_item').each(function(alink, index){
      alink.observe('click', this.boundRemoveItem);
    }.bind(this));

    this.boundCartSubmit = this.onCartUpdateSubmit.bind(this);
    $('cart_form').observe('submit', this.boundCartSubmit);

    this.boundCartKeydown = this.onCartKeyUp.bind(this);
    $('cart_form').getInputs().each(function(input, index){
      input.observe('keyup', this.boundCartKeydown);
    }.bind(this));

    // Prepare writein elements.
    $('writein_opener').observe('click', function(ev) {
      ev.stop();
      Effect.toggle('writein_elements','blind');
    });

    this.boundAddWriteinSubmit = this.onAddWriteinFormSubmit.bind(this);
    $('writein_form').observe('submit', this.boundAddWriteinSubmit);
  }

  /**
   *  Prepares cart for update by removing listeners.
   */
  _prepareCartForUpdate() {
    $('empty_list').stopObserving('click', this.boundEmptyList);

    $('cart_form').stopObserving('submit', this.boundCartSubmit);

    $$('#cart_form a.remove_item').each(function(alink, index){
      alink.stopObserving('click', this.boundRemoveItem);
    }.bind(this));

    $('cart_form').getInputs().each(function(input, index){
      input.stopObserving('keyup', this.boundCartKeydown);
    }.bind(this));

    $('writein_form').stopObserving('submit', this.boundAddWriteinSubmit);
  }

  /**
   *  Returns boolean determining if the passed string contains only digits.
   */
  _isStringANumber(str) {
    return (/^\d+$/.test(str));
  }
};
