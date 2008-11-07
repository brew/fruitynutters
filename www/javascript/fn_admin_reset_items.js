function initResetButton() {
  var resetButton = $('reset_items_button');
  resetButton.observe('click', function() {
    if (!window.confirm('Are you sure you want to reset all items in the catalogue?')) {
      ev.stop();
    }    
  });
}

// Set up reset button!
Event.observe(window, 'load', function(event){
  initResetButton();
});