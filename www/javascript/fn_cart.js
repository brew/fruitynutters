var FNCart = Class.create({
  initialize: function() {
    // Intercept the product add form submit event.
    
    this.fetchCart();
    
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
    if(ev.target.serialize() != this.serializedCart)
      this.updateCart(ev.target.action, ev.target.serialize());
    else
      console.info('Cart has not changed.');
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
   *  Fetches the cart.
   */
  fetchCart: function(url) {
    new Ajax.Updater({success:'cart_content', failure:'cart_notice'}, "/cart/", {
      method:'get',
      onComplete: function() {
        this.boundAddSubmit = this.onAddFormSubmit.bind(this);
        $$('.product_add').each(function(form, index) {
          form.observe('submit', this.boundAddSubmit);
        }, this);
        this._prepareCart();
      }.bind(this)
    });
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
  
  /**
   *  Prepares the cart at initialize and each time it's been updated.
   */
  _prepareCart: function() {
    this.serializedCart = $('cart_form').serialize();
    
    this.boundEmptyList = this.onEmptyList.bind(this);
    $('empty_list').observe('click', this.boundEmptyList);
    
    this.boundCartSubmit = this.onCartUpdateSubmit.bind(this);
    $('cart_form').observe('submit', this.boundCartSubmit);
    
    this.boundCartKeydown = this.onCartKeyUp.bind(this);
    $('cart_form').getInputs().each(function(input, index){
      input.observe('keyup', this.boundCartKeydown);
    }.bind(this));

  },
  
  /**
   *  Prepares cart for update by removing listeners.
   */
  _prepareCartForUpdate: function() {
    $('empty_list').stopObserving('click', this.boundEmptyList);
    
    $('cart_form').stopObserving('submit', this.boundCartSubmit);
    
    $('cart_form').getInputs().each(function(input, index){
      input.stopObserving('keyup', this.boundCartKeydown);
    }.bind(this));
  },
  
  /**
   *  Returns boolean determining if the passed string contains only digits.
   */
  _isStringANumber: function(str) {
    return (/^\d+$/.test(str));
  }
  
  
});
