var FNCart = Class.create({
  initialize: function() {
    // Intercept the product add form submit event.
    
    this.boundAddSubmit = this.onAddFormSubmit.bind(this);
    $$('.product_add').each(function(form, index) {
      form.observe('submit', this.boundAddSubmit);
    }, this);

    
    this._prepareCart();
  },
  
  /**
   *  Handler for the Submit event on the product add forms.
   */
  onAddFormSubmit: function(ev){
    this.updateCart(ev.target.action);
    ev.stop();
  },
  
  
  onEmptyList: function(ev) {
    this.updateCart("/cart/empty/");
    ev.stop();
  },
  
  /**
   *  Updates the cart with a given url.
   */
  updateCart: function(url) {
    
    this._prepareForUpdate();
    
    new Ajax.Updater({success:'cart_content'}, url, {
      method:'post',
      onComplete: function() {
        console.info('completed update');
        this._prepareCart();
      }.bind(this)
    });    
  },
  
  /**
   *  Prepares cart for update by removing listeners.
   */
  _prepareForUpdate: function() {
    this.boundEmptyList =this.onEmptyList.bind(this);
    $('empty_list').stopObserving('click', this.boundEmptyList);
  },
  
  _prepareCart: function() {
    this.boundEmptyList =this.onEmptyList.bind(this);
    $('empty_list').observe('click', this.boundEmptyList);
  }
  
});
