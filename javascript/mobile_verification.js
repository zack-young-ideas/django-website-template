/*
Sends an API request to verify a user's mobile phone number.
*/

const $ = require('jquery');

const getCookie = (name) => {
  /*
  Retrieves the value of a specified cookie.
  */
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

window.userManager = {

  verifyPhone: (endpoint) => {
    const mobileFormField = $('#id_mobile_number');
    const smsFormField = $('#id_sms_token');
    const verifyButton = $('#verify_button');
    const submitButton = $('#submit_button');
    const errorMessage = $('#error_message');
    const csrfToken = getCookie('csrftoken');

    verifyButton.click((event) => {
      event.preventDefault();
      $.ajax({
          url: endpoint,
          type: 'POST',
          data: JSON.stringify({ mobile_number: mobileFormField.val() }),
          headers: { 'X-CSRFToken': csrfToken },
          dataType: 'text',
        })
        .done((data, textStatus, xhr) => {
          if (xhr.status === 200) {
            // Prompt the user to enter the SMS token.
            smsFormField.show();
            submitButton.show();
            verifyButton.hide();
          } else {
            // Display an error message that prompts the user to try
            // again.
            errorMessage.text(
              'Invalid mobile number.'
            );
            errorMessage.show();
          }
        })
        .fail(() => {
          errorMessage.text(
            'Unable to connect to server. Please try again later'
          );
          errorMessage.show();
        });
    });
  },

}
