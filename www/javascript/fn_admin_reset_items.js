function initResetButton() {
  $('#reset_items_button').on('click', resetItems.bind(this));
}

function resetItems(ev) {
  if (!window.confirm('Are you sure you want to reset all items in the catalogue?')) {
    ev.preventDefault();
  }
}

$(document).ready(initResetButton);
