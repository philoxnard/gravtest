let stripe; // will be initialized with stripe
let card; // our card dom element

// checks if public key already exists in localStorage
if (localStorage.pk_test === null || localStorage.pk_test === undefined) {
  getStripeElementsKeys(); // fetches stripe key
} else {
  injectStripeElements(); // injects stripe into our dom form
}

// fetches stripe public key
function getStripeElementsKeys() {
  let message = {
    msg_type: "request",
    command: "stripe_get_keys"
  };

  message_request = JSON.stringify(message);

  // Sending AJAX Request to get stripe public key.
  $.ajax({
    type: "POST",
    url: "/api",
    contentType: "application/json",
    data: message_request,
    success: function(response) {
      // stores our fetched key into localStorage
      if ("pk_test" in response) {
        localStorage.pk_test = response["pk_test"];
        injectStripeElements();
      } else {
        console.log("Stripe public key was not found");
      }
    },
    error: function(response) {
      console.log("Error while trying to get Stripe public key");
    }
  });
}

// sends our stripe token to the backend to get charged
function chargeCard(token) {
  // we send our stripe token we just created as well as the sku we want to charge against
  let stripe_object = {
    token,
    sku: "sku_123"
  };

  let message = {
    msg_type: "request",
    command: "stripe_charge_card",
    stripe_token: stripe_object
  };

  message_request = JSON.stringify(message);

  // Sending AJAX Request to charge our stripe token.
  $.ajax({
    type: "POST",
    url: "/api",
    contentType: "application/json",
    data: message_request,
    success: function(response) {
      // displays an alert with the status of our charge request
      let alert = "Charge failed";
      if ("charge_result" in response) {
        if (response.charge_result === "succeeded") {
          alert = "Charge went through successfully";
        }
      }
      window.alert(alert);
    },
    error: function(response) {
      console.log("Error while trying to get Stripe checkout session");
    }
  });
}

// initializes stripe and injects stripe elements into the card element of the form
function injectStripeElements() {
  stripe = Stripe(localStorage.pk_test);
  var elements = stripe.elements();
  card = elements.create("card", {
    style: {
      base: {
        iconColor: "#666EE8",
        color: "#31325F",
        lineHeight: "40px",
        fontWeight: 300,
        fontFamily: "Helvetica Neue",
        fontSize: "15px",
        "::placeholder": {
          color: "#CFD7E0"
        }
      }
    }
  });
  card.mount("#card-element");

  card.on("change", function(event) {
    setOutcome(event);
  });
}

// updates the dom with our stripe token.  can be omitted in release versions
function setOutcome(result) {
  var successElement = document.querySelector(".success");
  var errorElement = document.querySelector(".error");
  successElement.classList.remove("visible");
  errorElement.classList.remove("visible");

  if (result.token) {
    chargeCard(result.token);
    successElement.querySelector(".token").textContent = result.token.id;
    successElement.classList.add("visible");
  } else if (result.error) {
    errorElement.textContent = result.error.message;
    errorElement.classList.add("visible");
  }
}

// handles form submission by creating a new stripe token and then calling our function
// that will send the token to our backend
document.querySelector("form").addEventListener("submit", function(e) {
  e.preventDefault();
  var form = document.querySelector("form");
  var extraDetails = {
    name: form.querySelector("input[name=cardholder-name]").value,
    phone: form.querySelector("input[name=cardholder-phone]").value
  };
  stripe.createToken(card, extraDetails).then(setOutcome);
});
