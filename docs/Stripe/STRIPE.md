# Stripe Integration

At this current point in time we currently only have a basic one time charge API for Stripe using
either [Stripe Checkout](https://stripe.com/docs/payments/checkout) or [Stripe Elements](https://stripe.com/docs/stripe-js).

## Installation

You will need to get api keys from [Stripe](https://stripe.com).  Put your secret key(SK key) and public key(PK key) in a .env file at the projects root.

## Stripe Checkout

### How it works

Stripe Checkout takes much of the API logic and allows you to create a button that will redirect a customer to Stripes hosted checkout.  You just need to provide the API with product information and Stripe will take ccare of the rest.

### Checkout Setup

Most of the logic for Stripe Checkout sits in the `gravityApp/app/GravityCharge.py` file's **getSkuInfo**
method.  In order to set up your products you will have to set up your product inventory.  These steps should take you from start to finish:

1. In the **getSkuInfo** method, add in a new product by creating a new **elif** with the syntax `elif sku == "sku_12345"`.  The product should have a field for name, description, images, amount, currency and quantity.
2. Create a new button where you would like it to show up in the front end.  Make sure you import both Stripe and the checkout.js.
3. Set the buttons onclick to `startCheckout('sku_12345')`.

#### Example of front end implementation

```html
<body>
    <button onclick="startCheckout('sku_123')">Checkout Product 1</button>
    <script src="https://js.stripe.com/v3/"></script>
    <script src="/js/stripe/checkout.js"></script>
</body>
```

## Stripe Elements Form

### Elements Setup

Most of the logic for Stripe Checkout sits in the `gravityApp/app/GravityCharge.py` file's **getSkuInfo**
method.  In order to set up your products you will have to set up your product inventory.  These steps should take you from start to finish:

1. In the **getSkuInfo** method, add in a new product by creating a new **elif** with the syntax `elif sku == "sku_12345"`.  The product should have a field for name, description, statementDescriptor, images, amount, currency and quantity.
2. Create a checkout form.  An example of a Stripe Elements form is listed below
3. In the **chargeCard** method of `public/js/elements.js` enter the **sku** of the desired product.
4. After sending a post request to the charge api, the browser will either get a json message back stating that the charge was successfully or they will receive a json error back.

#### Example of front end implementation

```html
<body>
    <div class="container>
        <div class="row">
            <div class="col-12">
                <form>
                    <div class="group">
                        <label>
                            <span>Name</span>
                            <input name="cardholder-name" class="field" placeholder="Jane Doe" />
                        </label>
                        <label>
                            <span>Phone</span>
                            <input name="cardholder-phone" class="field" placeholder="(123) 456-7890" type="tel" />
                        </label>
                    </div>
                    <div class="group">
                        <label>
                            <span>Card</span>
                            <div id="card-element" class="field"></div>
                        </label>
                        </div>
                        <button type="submit">Pay $25</button>
                        <div class="outcome">
                        <div class="error"></div>
                        <div class="success">
                            Success! Your Stripe token is <span class="token"></span>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
```

## Testing

A test page with a basic card form is located at `/checkout`.  You can use "4242 4242 4242 4242" as a test card.  The form will create a stripe token, display the token id undernearth the charge button, charge $20 against that stripe token and then return whether it was successful or not.

## TODO

- Add in Stripe customer API functionality
- Add in reoccuring payments(subscriptions)
- Add in Order API functionality
- Sendgrid integration
- Create Stripe example page

pull request are always welcomed :).
