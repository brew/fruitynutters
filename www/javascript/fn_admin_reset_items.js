function initResetButton() {
  var resetButton = $('reset_items_button');
  resetButton.observe('click', resetItems.bind(this));
}

function resetItems(ev) {
  if (!window.confirm('Are you sure you want to reset all items in the catalogue?')) {
    ev.stop();
  }
}


// Set up reset button!
Event.observe(window, 'load', function(event){
  initResetButton();
});