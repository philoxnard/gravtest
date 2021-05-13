
// checks if stripe public key is in sessionStorage and fetches it if it isn't
function startCheckout(sku) {

	console.log( "startCheckout: sku = " + sku )

	if (sessionStorage.stripe_pk_key === null || sessionStorage.stripe_pk_key === undefined) {
		getStripeKeys(sku);
	} else {
		redirectToCheckout(sku);
	}
}

// Fetch Stripe public key from the Gravity Server
function getStripeKeys(sku) {

	let message = {
		msg_type: "request",
		command: "stripe_get_keys"
	};

	message_request = JSON.stringify(message);

	// Sending AJAX Request to get stripe publick key.
	$.ajax({
		type: "POST",
		url: "/api",
		contentType: "application/json",
		data: message_request,
		success: function(response) {
			if ("stripe_pk_key" in response) {
				sessionStorage.stripe_pk_key = response["stripe_pk_key"];
				redirectToCheckout(sku);
			} else {
				console.log("Stripe public key was not found");
			}
		},
		error: function(response) {
			console.log("Error while trying to get Stripe public key");
		}
	});
}

// redirects to stripe checkout
function redirectToCheckout(sku) {

	console.log( "redirectToCheckout: sky = " + sku )

	var stripe = Stripe(sessionStorage.stripe_pk_key);
	let message = {
		msg_type: "request",
		command: "stripe_get_session",
		stripe_sku: sku
	};

	message_request = JSON.stringify(message);

	// Sending AJAX Request to get stripe checkout session.
	$.ajax({
		type: "POST",
		url: "/api",
		contentType: "application/json",
		data: message_request,
		// Fetch the stored token from sessionStorage and set in the header
		success: function(response) {

			if ("session" in response) {

				console.log( "redirectToCheckout: redirecting to checkout page" )

				// redirect the client to the checkout page
				stripe
					.redirectToCheckout({
						sessionId: response.session.id
					})
					.then(function(result) {
						// If `redirectToCheckout` fails due to a browser or network error
						if (result.error) {
							alert(
								`Redirecting to checkout failed with error: ${result.error.message}`
							);
						}
					});
			} else {
				console.log("Stripe checkout session was not found");
			}
		},
		error: function(response) {
			console.log("Error while trying to get Stripe checkout session");
		}
	});
}
