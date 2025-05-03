/*
Sends an API request to verify a user's mobile phone number.
*/

const verifyPhone = function(endpoint) {
  const formField = document.getElementById('id_mobile_number');
  const submitButton = document.getElementById('submit_button');
  const errorMessage = document.getElementById('error_message');
  submitButton.addEventListener('click', function(event) {
    fetch(endpoint)
      .then((response) => {
        if (response.ok) {
          // Display a "Continue" button that takes the user to the
          // next step.
        } else {
          // Display an error message that prompts the user to try
          // again.
        }
      })
  });
}
