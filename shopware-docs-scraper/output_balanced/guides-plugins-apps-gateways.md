# Guides Plugins Apps Gateways

*Scraped from Shopware Developer Documentation*

---

## Checkout Gateway

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/gateways/checkout/checkout-gateway.html

# Checkout Gateway [​](#checkout-gateway)

## Context [​](#context)

As of Shopware version 6.6.3.0, the Checkout Gateway was introduced.

The Checkout Gateway aims to allow a streamlined implementation for making informed decisions during the checkout process, based on both the cart contents and the current sales channel context. In particular, the app system benefits from this solution, enabling seamless communication and decision-making on the app server during the checkout.

While this documentation focuses on the app integration of the Checkout Gateway, the design is intended to allow a custom replacement solution via the plugin system."

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App base guide](../../app-base-guide.md)

Your app server must be also accessible for the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration [​](#manifest-configuration)

To indicate to Shopware that your app uses the checkout gateway, you must provide a `checkout` property inside a `gateways` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working checkout gateway configuration.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <checkout>https://my-app.server.com/checkout/gateway</checkout>
    </gateways>
</manifest>
```

After successful installation of your app, the checkout gateway will already be used during checkout.

## Checkout gateway endpoint [​](#checkout-gateway-endpoint)

During checkout, Shopware checks for any active checkout gateways and will call the `checkout` url. The app server will receive the current `SalesChannelContext`, `Cart`, and available payment and shipping methods as part of the payload.

WARNING

**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds. Be sure that your checkout gateway implementation on your app server responds in time, otherwise Shopware will time out and drop the connection.

Your app server can then respond with a list of commands to manipulate the cart, payment methods, shipping methods, or add cart errors.

You can find a reference of all currently available commands [here](./command-reference.html).

Let's assume that your payment method is not available for carts with a total price above 1000€.

## Event [​](#event)

Plugins can listen to the `Shopware\Core\Checkout\Gateway\Command\Event\CheckoutGatewayCommandsCollectedEvent`. This event is dispatched after the Checkout Gateway has collected all commands from all app servers. It allows plugins to manipulate the commands before they are executed, based on the same payload the app servers retrieved.

---

## Checkout Gateway Command Reference

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/gateways/checkout/command-reference.html

# Checkout Gateway Command Reference [​](#checkout-gateway-command-reference)

| Command | Description | Payload | Since |
| --- | --- | --- | --- |
| `remove-payment-method` | Removes a payment method from the available payment methods. | `{"paymentMethodTechnicalName": "string"}` | 6.6.3.0 |
| `remove-shipping-method` | Removes a shipping method from the available shipping methods. | `{"shippingMethodTechnicalName": "string"}` | 6.6.3.0 |
| `add-cart-error` | Adds an error to the cart. The level decides the severity of the cart error flash message. Blocking decides, whether to block the checkout for the customer. | `{"message": "string", "level": "int", "blocking": "boolean"}` | 6.6.3.0 |

---

## Context Gateway Command Reference

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/gateways/context/command-reference.html

# Context Gateway Command Reference [​](#context-gateway-command-reference)

## Available commands [​](#available-commands)

| Command | Description | Payload | Since |
| --- | --- | --- | --- |
| `context_add-customer-message` | Adds an error message to be displayed to the customer in the Storefront via FlashBag messages. | `{"message": "string"}` | 6.7.1.0 |
| `context_change-billing-address` | Changes the billing address of a customer to the specified address ID. | `{"addressId": "string"}` | 6.7.1.0 |
| `context_change-shipping-address` | Changes the shipping address of a customer to the specified address ID. | `{"addressId": "string"}` | 6.7.1.0 |
| `context_change-currency` | Changes the active currency for a customer to the currency with the specified ISO 4217 currency code. | `{"iso": "string"}` | 6.7.1.0 |
| `context_change-language` | Changes the active language for a customer to the language with the specified BCP 47 language tag. | `{"iso": "string"}` | 6.7.1.0 |
| `context_change-payment-method` | Changes the active payment method for a customer to the method with the specified technical name. | `{"technicalName": "string"}` | 6.7.1.0 |
| `context_change-shipping-method` | Changes the active shipping method for a customer to the method with the specified technical name. | `{"technicalName": "string"}` | 6.7.1.0 |
| `context_change-shipping-location` | Changes the active shipping location for a customer to the specified country / country state. | `{"countryIso": "string", "countryStateIso": "string"}` | 6.7.1.0 |
| `context_login-customer` | Logs in an existing customer with the specified email. | `{"customerEmail": "string"}` | 6.7.1.0 |
| `context_register-customer` | Register a new customer with the specified data and log them in. | `{"data": "object (s. RegisterCustomerCommand)"}` | 6.7.1.0 |

## Available data for RegisterCustomerCommand [​](#available-data-for-registercustomercommand)

These properties are available to set in the custom `data` object of the `context_register-customer` command.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | string |  | The title of the customer, e.g. "Mr." or "Mrs." |
| `accountType` | string |  | The type of account, either "private" or "business" |
| `firstName` | string | Yes | The first name of the customer |
| `lastName` | string | Yes | The last name of the customer |
| `email` | string | Yes | The email address of the customer |
| `salutationId` | string |  | The ID of the salutation to use for the customer |
| `guest` | bool |  | Whether the customer is a guest (default: true) |
| `storefrontUrl` | string | Yes | The storefront URL of the sales channel (You find available domains in the sales channel context -> sales channel -> domains) |
| `requestedGroupId` | string |  | The ID of the customer group to assign to the customer |
| `affiliateCode` | string |  | The affiliate code to assign to the customer |
| `campaignCode` | string |  | The campaign code to assign to the customer |
| `birthdayDay` | int |  | The day of the customer's birthday |
| `birthdayMonth` | int |  | The month of the customer's birthday |
| `birthdayYear` | int |  | The year of the customer's birthday |
| `password` | string | (for non-guest customers) | The password for the customer (plain text, will be hashed by the shop before stored) |
| `billingAddress` | object | Yes | The billing address of the customer, s. `AddressResponseStruct` for available fields |
| `shippingAddress` | object |  | The shipping address of the customer, s. `AddressResponseStruct` for available fields |
| `vatIds` | array |  | An array of VAT IDs for the customer |
| `acceptedDataProtection` | bool |  | Whether the customer has accepted the data protection policy (default: false) |

### AddressResponseStruct [​](#addressresponsestruct)

This structure is used for the `billingAddress` and `shippingAddress` fields in the `RegisterCustomerCommand`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | string |  | The title of the address, e.g. "Mr." or "Mrs." |
| `firstName` | string | Yes | The first name of the address owner |
| `lastName` | string | Yes | The last name of the address owner |
| `salutationId` | string |  | The ID of the salutation to use for the address owner |
| `street` | string | Yes | The street of the address |
| `zipcode` | string | Yes | The ZIP code of the address |
| `city` | string | Yes | The city of the address |
| `company` | string |  | The company name for the address |
| `department` | string |  | The department name for the address |
| `countryStateId` | string |  | The ID of the country state for the address |
| `countryId` | string | Yes | The ID of the country for the address |
| `additionalAddressLine1` | string |  | Additional address line 1 |
| `additionalAddressLine2` | string |  | Additional address line 2 |
| `phoneNumber` | string |  | The phone number for the address |

---

## Context Gateway

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/gateways/context/context-gateway.html

# Context Gateway [​](#context-gateway)

DANGER

**Security and privacy**

With the Context Gateway, Shopware allows your app to manipulate the customer context, which includes sensitive information like customer addresses, payment methods, and more. It is your responsibility to ensure that the commands are valid and do not compromise the security or privacy of customers.

Due to the powerful nature of this feature, it should only be used if your app server is properly secured and the commands it sends are fully trusted and validated.

## Context [​](#context)

As of Shopware version 6.7.1.0, the Context Gateway has been introduced.

The Context Gateway is a powerful feature that enables apps to securely access and interact with the customer context — based on the current cart and sales channel — allowing for more informed decision-making on the app server. This enhancement empowers app developers to dynamically tailor the shopping experience by manipulating the customer context.

It serves as the bridge between your app’s JavaScript and your app server.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App base guide](../../app-base-guide.md)

Your app server must also be accessible to the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration [​](#manifest-configuration)

To indicate to Shopware that your app uses the context gateway, you must provide a `context` property inside a `gateways` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working checkout gateway configuration.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <!-- ... -->
        <context>https://my-app.server.com/context/gateway</context>
    </gateways>
</manifest>
```

After the successful installation of your app, the context gateway is ready to be called by Shopware.

## Context Gateway Endpoint [​](#context-gateway-endpoint)

To trigger the context gateway, your integration can call the additional Store API route: . This endpoint will forward the request to your app server’s context gateway endpoint, which must be [configured in your app's manifest](#manifest-configuration).

To allow the shop to identify your app, the request must include the `appName`, which is defined in your [app’s `manifest.xml`](./../../app-base-guide.html#manifest-file).

Your app server will receive the following payload:

* The request source, including:
  + The URL of the Shopware shop
  + The Shop ID
  + The app version
  + Any active [in-app purchase](./../../in-app-purchases.html).
* The current `SalesChannelContext`
* The current `Cart`
* Any custom data you include in the request body

INFO

Communication between Shopware and your app server is secured via the [app signature verification mechanism](./../../app-signature-verification.html), ensuring that only your app server can respond to context gateway requests.

### Storefront Integration [​](#storefront-integration)

To trigger the context gateway from the Storefront, use the  endpoint. This route is automatically registered by Shopware.

You can include any custom data in the request body - Shopware will forward this data to your app server.

To simplify this integration, Shopware provides the `ContextGatewayClient` service. This JavaScript client is intended for use within your app and handles communication with the context gateway endpoint. It returns a response containing:

* A (new) context token
* An optional redirect URL

Here is an example JavaScript plugin that triggers the context gateway when a button is clicked in the Storefront:

context-gateway.js

javascript

```shiki
import Plugin from 'src/plugin-system/plugin.class';
import ContextGatewayClient from 'src/service/context-gateway-client.service';

export default class MyPlugin extends Plugin {
  init() {
    this._registerEvents();
  }

  _registerEvents() {
    this.el.addEventListener('click', this._onClick.bind(this));
  }

  async _onClick() {
    // create client with your app name
    const gatewayClient = new ContextGatewayClient('myAppName');

    // call the gateway with optional custom data
    const tokenResponse = await gatewayClient.call({ some: 'data', someMore: 'data' });

    // either: you can work with the new token or redirect URL
    // this means you have to handle the navigation yourself, e.g. reloading the page or redirecting to the URL
    const token = tokenResponse.token;
    const redirectUrl = tokenResponse.redirectUrl;

    // or: if you want shopware to handle the navigation automatically, even supplying an optional custom target path is possible
    await gatewayClient.navigate(tokenResponse, '/custom/target/path');
  }
}
```

INFO

**Navigation `customTarget` Behavior**

The `customTarget` parameter allows you to optionally control the redirect path used by the `navigate` method.

* If `customTarget` is an **absolute path** (starts with `/`), it completely replaces the path portion of the `redirectUrl`. This can be used to override sales channel subpaths in the `redirectUrl`. *Example:* `https://example.com/en` → `https://example.com/custom/target/path`
* If `customTarget` is a **relative path**, it is appended to the existing path of the `redirectUrl`.
* If `customTarget` is `null`, the behavior depends on whether a `redirectUrl` is present:

  + If present: the `redirectUrl` is used as-is.
  + If not: the current page is reloaded to apply context changes.

Trailing slashes are automatically removed to ensure clean and consistent URLs.

### App server response [​](#app-server-response)

WARNING

**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds. Be sure that your context gateway implementation on your app server responds in time, otherwise Shopware will time out and drop the connection.

Your app server can respond with a list of commands to modify the current sales channel context. These commands can be used to perform actions such as:

* Changing aspects of the customer context, like:
  + Changing the active currency
  + Changing the active language and more
* Registering a new customer
* Logging in an existing customer

You can find a complete reference of all available commands in the [command reference](./command-reference.html).

For example, you might want to update the context to a different currency and language if the current currency is not GBP.

### Command Validation [​](#command-validation)

Shopware performs basic validation on the commands returned by your app server to ensure they are reasonable to execute.

The following checks are enforced:

* The command must be recognized as valid, e.g. . See the full list of available [commands](./command-reference.html#available-commands).
* The payload must be valid for the respective command type.
* Only **one command per type** is allowed. For example, you cannot include two  commands in a single response.
* A maximum of **one  or**  command is allowed per response.

## Event [​](#event)

Plugins can listen to the `Shopware\Core\Framework\Gateway\Context\Command\Event\ContextGatewayCommandsCollectedEvent`. This event is dispatched after all commands have been collected from the app server and allow plugins to modify or add commands based on the same payload the app received.

## Special Considerations [​](#special-considerations)

* The `context_login-customer` command allows your app to log in a customer **without requiring their password**. Use this feature with caution to uphold the shop’s security and privacy standards.
* The `context_register-customer` command will create a new customer account and **automatically log them in**. Make sure to validate the provided data before issuing this command. See the [RegisterCustomerCommand reference](./command-reference.html#available-data-for-registercustomercommand) for the list of accepted fields.

In both cases, your app must ensure that the customer has **explicitly consented** to be registered or logged in.

---

## In-App Purchase Gateway

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/gateways/in-app-purchase/in-app-purchase-gateway.html

# In-App Purchase Gateway [​](#in-app-purchase-gateway)

## Context [​](#context)

INFO

In-App Purchase is available since Shopware version 6.6.9.0

In-App Purchase Gateway was introduced to enhance flexibility in managing In-App Purchases.

The gateway enables app servers to restrict specific In-App Purchases based on advanced decision-making processes handled on the app server side.

INFO

**Current Limitations:**  
 At present, the In-App Purchase Gateway supports only restricting the checkout process for new In-App Purchases.  
**Plans:**  
 We aim to expand its functionality to include filtering entire lists of In-App Purchases before they are displayed to users.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App base guide](../../app-base-guide.md)

Your app server must be also accessible for the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest Configuration [​](#manifest-configuration)

To indicate that your app leverages the In-App Purchase Gateway, include the `inAppPurchase` property within the `gateways` property in your app's `manifest.xml`.

Below is an example of a properly configured manifest snippet for enabling the checkout gateway:

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <inAppPurchases>https://my-app.server.com/inAppPurchases/gateway</inAppPurchases>
    </gateways>
</manifest>
```

After successful installation of your app, the In-App Purchases gateway will already be used.

## In-App Purchases gateway endpoint [​](#in-app-purchases-gateway-endpoint)

During checkout of an In-App Purchase, Shopware checks for any active In-App Purchases gateways and will call the `inAppPurchases` url. The app server will receive a list containing the single only In-App Purchase the user wants to buy as part of the payload.

WARNING

**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds. Be sure that your In-App Purchases gateway implementation on your app server responds in time, otherwise Shopware will time out and drop the connection.

## Event [​](#event)

Plugins can listen to the `Shopware\Core\Framework\App\InAppPurchases\Event\InAppPurchasesGatewayEvent`. This event is dispatched after the In-App Purchases Gateway has received the app server response. It allows plugins to manipulate the available In-App Purchases, based on the same payload the app servers retrieved.

---

