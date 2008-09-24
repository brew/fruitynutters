var FNCart = Class.create({
  initialize: function() {
    // Intercept the product add form submit event.
    $$('.product_add').each(function(form, index) {
      form.observe('submit', this.onAddFormSubmit.bind(this));
    }, this);
    
    $('empty_list').observe('click', this.onEmptyList.bind(this));
    
    
  },
  
  /**
   *  Handler for the Submit event on the product add forms.
   */
  onAddFormSubmit: function(ev){
    this.updateCart(ev.target.action);
    ev.stop();
  },
  
  
  onEmptyList: function(ev) {
    
  },
  
  /**
   *  Updates the cart with a given url.
   */
  updateCart: function(url) {
    new Ajax.Updater({success:'cart_content'}, ev.target.action, {
      method:'post'
    });    
  }
});
