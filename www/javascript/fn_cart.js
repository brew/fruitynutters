var FNCart = Class.create({
  initialize: function() {
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
  },
  
  /**
   *  Handler for the Submit event on the product add forms.
   */
  onAddFormSubmit: function(ev){
    ev.stop();
    
    // Get the quantity to add.
    quantity = $(ev.target).down('.quantity').value;
    // Bail out if the quantity isn't a number.
    if(!this._isStringANumber(quantity)) return false;
    
    url = ev.target.action+quantity+"/";
    
    // If the item is a bundle, submit its sub items and their quantities.
    if($(ev.target).up('.has_bundle')) {
      var serializedBundleData = $(ev.target).up('.has_bundle').down('.bundle_product_add').serialize();
      this.updateCart(url, serializedBundleData);
    } else {
      this.updateCart(url);
    }
    
  },
  
  onAddWriteinFormSubmit: function(ev) {
    ev.stop();
    this.updateCart(ev.target.action, ev.target.serialize());
  },
  
  onVirtualShopAddFormSubmit: function(ev) {
    ev.stop();
    this.updateCart(ev.target.action, ev.target.serialize());
  },

  onRemoveItem: function(ev) {
    ev.stop();
    this.updateCart($(ev.target).up('a.remove_item').href);
  },
  
  /**
   *  Handler for the click event on the empty list link.
   */
  onEmptyList: function(ev) {
    ev.stop();
    this.updateCart("/cart/empty/");
  },
  
  /**
   *  Handler for the submittion of the cart form (Update cart).
   */
  onCartUpdateSubmit: function(ev) {
    ev.stop();
    if(ev.target.serialize() != this.serializedCart) {
      // console.info(ev.target.serialize());
      this.updateCart(ev.target.action, ev.target.serialize());
    } else {
      // console.info('Cart has not changed.');
    }
  },
  
  /**
   *  Handler for when a key is pressed in the cart inputs.
   */
  onCartKeyUp: function(ev) {
    if(ev.target.serialize() != this.serializedCart)
      $('update_list_button').enable();
    else
      $('update_list_button').disable();
  },
  
  /**
   *  Updates the cart with a given url.
   */
  updateCart: function(url, parameters) {
    
    this._prepareCartForUpdate();
    
    $('cart_load_indicator').show();
    
    new Ajax.Updater({success:'cart_content', failure:'cart_notice'}, url, {
      method:'post',
      parameters:parameters,
      onComplete: function() {
        this._prepareCart();
      }.bind(this)
    });    
  },
  
  onSaveDetailsButtonClick: function(ev) {
    new Ajax.Request('/cart/savedetails/', {
      method: 'post',
      parameters:$('order_details').serialize(),
      onSuccess: function(transport) {
        window.location.replace("/catalogue/aisle/");
      },
      onFailure: function(transport) {

      }
    });
  },
  
  /**
   *  Prepares the cart at initialize and each time it's been updated.
   */
  _prepareCart: function() {
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
  
  },
  
  /**
   *  Prepares cart for update by removing listeners.
   */
  _prepareCartForUpdate: function() {
    $('empty_list').stopObserving('click', this.boundEmptyList);
    
    $('cart_form').stopObserving('submit', this.boundCartSubmit);

    $$('#cart_form a.remove_item').each(function(alink, index){
      alink.stopObserving('click', this.boundRemoveItem);
    }.bind(this));
    
    $('cart_form').getInputs().each(function(input, index){
      input.stopObserving('keyup', this.boundCartKeydown);
    }.bind(this));
    
    $('writein_form').stopObserving('submit', this.boundAddWriteinSubmit);
    
  },
  
  /**
   *  Returns boolean determining if the passed string contains only digits.
   */
  _isStringANumber: function(str) {
    return (/^\d+$/.test(str));
  }
  
  
});
