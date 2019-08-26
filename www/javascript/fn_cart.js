class FNCart {
  constructor() {
    // Intercept the product add form submit event.
    this.boundAddSubmit = this.onAddFormSubmit.bind(this);

    $('.product_add').submit(this.boundAddSubmit);

    if($('#virtualshop_form')) {
      this.boundAddVirtualSubmit = this.onVirtualShopAddFormSubmit.bind(this);
      $('#virtualshop_form').submit(this.boundAddVirtualSubmit);
    }

    if($('#save_details_button')) {
      $('#save_details_button').click(this.onSaveDetailsButtonClick.bind(this));
    }

    this._prepareCart();
  }

  /**
   *  Handler for the Submit event on the product add forms.
   */
  onAddFormSubmit(ev){
    ev.preventDefault();

    // Get the quantity to add.
    var quantity = $(ev.target).find('.quantity').val();
    // Bail out if the quantity isn't a number.
    if(!this._isStringANumber(quantity)) return false;

    var url = ev.target.action;
    var serializedData = $(ev.target).serialize();
    this.updateCart(url, serializedData);
  }

  /**
   *  Handler for submission of the add write-in form.
   */
  onAddWriteinFormSubmit(ev) {
    ev.preventDefault();
    this.updateCart(ev.target.action, $(ev.target).serialize());
  }

  /**
   *  Handler for submission of the add virtual shop item form.
   */
  onVirtualShopAddFormSubmit(ev) {
    ev.preventDefault();
    var completeAction = function(transport) {
      this._prepareCart();
      if($('.cart_error').length == 0)
        ev.target.reset();
    }.bind(this);
    this.updateCart(ev.target.action, $(ev.target).serialize(), completeAction);
  }

  /**
   *  Handler for the remove item button.
   */
  onRemoveItem(ev) {
    ev.preventDefault();
    this.updateCart($(ev.target).parent('a.remove_item').attr('href'));
  }

  /**
   *  Handler for the click event on the empty list link.
   */
  onEmptyList(ev) {
    ev.preventDefault();
    this.updateCart("/cart/empty/");
  }

  /**
   *  Handler for the submission of the cart form (Update cart).
   */
  onCartUpdateSubmit(ev) {
    ev.preventDefault();
    if($(ev.target).serialize() != this.serializedCart) {
      // console.info($(ev.target).serialize());
      this.updateCart(ev.target.action, $(ev.target).serialize());
    } else {
      // console.info('Cart has not changed.');
    }
  }

  /**
   *  Handler for when a key is pressed in the cart inputs.
   */
  onCartKeyUp(ev) {
    if($(ev.target).serialize() != this.serializedCart)
      $('#update_list_button').prop('disabled', false);
    else
      $('#update_list_button').prop('disabled', true);
  }

  /**
   *  Updates the cart with a given url and parameters, updating the cart container with the successful return value.
   */
  updateCart(url, parameters, completeAction) {
    completeAction = completeAction || function() {this._prepareCart();}.bind(this);

    this._prepareCartForUpdate();

    $('#cart_load_indicator').show();

    $.ajax(url, {
      method:'post',
      data:parameters
    })
    .done(function(data) {
      $('#cart_content').html(data);
    })
    .fail(function(data) {
      $('#cart_notice').html(data);
    })
    .always(completeAction);
  }

  /**
   *  Handler for click of the save details button.
   */
  onSaveDetailsButtonClick(ev) {
    $.ajax('/cart/savedetails/', {
      method: 'post',
      data:$('#order_details').serialize(),
    })
    .done(function() {
      window.location.replace("/catalogue/aisle/");
    });
  }

  /**
   *  Prepares the cart at initialize and each time it's been updated.
   */
  _prepareCart() {
    this.serializedCart = $('#cart_form').serialize();

    this.boundEmptyList = this.onEmptyList.bind(this);
    $('#empty_list').on('click', this.boundEmptyList);

    this.boundCartSubmit = this.onCartUpdateSubmit.bind(this);
    $('#cart_form').on('submit', this.boundCartSubmit);

    this.boundRemoveItem = this.onRemoveItem.bind(this);
    $('#cart_form .remove_item').on('click', this.boundRemoveItem);


    this.boundCartKeydown = this.onCartKeyUp.bind(this);
    $('#cart_form').on('keyup', this.boundCartKeydown);

    // Prepare writein elements.
    $('#writein_opener').click(function(ev) {
      ev.preventDefault();
      $('#writein_elements').slideToggle();
    });

    this.boundAddWriteinSubmit = this.onAddWriteinFormSubmit.bind(this);
    $('#writein_form').on('submit', this.boundAddWriteinSubmit);
  }

  /**
   *  Prepares cart for update by removing listeners.
   */
  _prepareCartForUpdate() {
    $('#empty_list').off('click');

    $('#cart_form').off('submit');

    $('#cart_form .remove_item').off('click');

    $('#cart_form').off('keyup');

    $('#writein_form').off('submit');
  }

  /**
   *  Returns boolean determining if the passed string contains only digits.
   */
  _isStringANumber(str) {
    return (/^\d+$/.test(str));
  }
};
