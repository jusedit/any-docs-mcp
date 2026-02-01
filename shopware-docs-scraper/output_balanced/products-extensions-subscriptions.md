# Products Extensions Subscriptions

*Scraped from Shopware Developer Documentation*

---

## Subscriptions

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/

# Subscriptions [​](#subscriptions)

To enable flexibility in product offerings, the subscription extension aims to provide a subscription-based model for products. This extension allows you to offer products on a subscription basis. The subscription model is a recurring payment model where customers can subscribe to a product and receive it at regular intervals. This model is beneficial for products that are consumed regularly, such as groceries, cosmetics, or magazines.

We suggest that you first familiarize yourself with the [subscription concepts](./concept.html) as well as the [user documentation](https://docs.shopware.com/en/shopware-6-en/settings/shop/subscriptions) before you start using the extension.

---

## Guides

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/guides/

# Guides [​](#guides)

This section will help with common topics regarding the usage of subscriptions.

Please familiarize yourself with the [concept](./../concept.html) first before continuing.

## Available Guides [​](#available-guides)

* [Separate Checkout](./separate-checkout.html) - Using the separate subscription checkout flow
* [Mixed Checkout](./mixed-checkout.html) - Using the mixed cart checkout with subscriptions and regular products
* [Template Scoping](./template-scoping.html) - Working with scoped templates in subscriptions
* [B2B Employee Integration](./b2b-employee-integration.html) - Using subscriptions with B2B employee management

---

## Separate checkout

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/guides/separate-checkout.html

# Separate subscription checkout [​](#separate-subscription-checkout)

This guide describes how buying a subscription via the separate checkout flow works and how extensions should integrate with it. The **separated subscription checkout** allows customers to purchase subscription products via an isolated checkout process and dedicated cart. This process is best described as an *express checkout* for subscription products.

Please familiarize yourself with the [concept](./../concept.html) first before continuing here.

## Overview [​](#overview)

Subscription line items are added to a new subscription cart containing **only** the subscription product. The checkout process will start right away, and the customer will not be able to add any additional products. If a customer leaves the subscription checkout, they can only return to it via their browser history or by starting a new checkout with their desired product. The main cart and the original sales channel context will be left untouched.

## Retrieving information [​](#retrieving-information)

In a separated subscription checkout a [subscription cart](./../concept.html#subscription-cart) and [subscription context](./../concept.html#subscription-context) and replaces the main cart and sales channel context. Additional information about the subscription can be retrieved from the subscription context via it's `subscription` extension.

When an order is placed from a subscription cart, the order will contain an `subscriptionId` / `subscription` extension that references the created subscription as well as an `initialSubscriptions` extension like a [mixed order](./mixed-checkout.html#retrieving-information). Any subsequent orders generated will only contain the `subscriptionId` / `subscription` extension.

## Manipulate subscription cart [​](#manipulate-subscription-cart)

The [subscription cart](./../concept.html#subscription-cart) is calculated with the subscription cart calculator. To add cart collectors or processors to the calculation process, they have to be tagged with `subscription.cart.collector` and `subscription.cart.processor` respectively. If you need to differentiate between a separate and mixed subscription cart calculation, check `salesChannelContext.extensions.subscription.isManaged`.

The cart processor `Shopware\Commercial\Subscription\Checkout\Cart\Discount\SubscriptionDiscountProcessor` can serve as example how to add line items to subscription carts. But note that the processor supports [mixed carts](./mixed-checkout.html) too.

### Adding subscription line items [​](#adding-subscription-line-items)

To add a line item to a subscription cart, the relevant subscription plan and interval IDs must be added.

The following methods are available to do so via the **Store-API**, remember to use the subscription endpoints including necessary headers:

* Add `subscription-plan-option` and `subscription-plan-option-<subscription-plan-id>-interval` IDs besides `lineItems`.

Information added through the first two methods will be remapped to the line item's payload, as shown in the last method.

To do so via the **backend**, like in cart collectors or processors, the following methods are available:

* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line items payload

## Events [​](#events)

Most of the events triggered within subscription checkout are prefixed with `subscription.`. These events are identical to normal checkout events. If you wish to use these events, you need to subscribe to them. A list of known prefixed events can be found in `Subscription/Framework/Event/SubscriptionEventRegistry.php`

php

```shiki
// Normal Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}

// Subscription Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return ['subscription.' . CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}
```

## Request scoping [​](#request-scoping)

In Storefront, there is an additional URL parameter (`subscriptionToken`) that gets resolved. In headless, there are two header parameters that need to be set namely `sw-subscription-plan` and `sw-subscription-interval`.

Below is an example of the context set on a subscription cart in the Storefront:

xml

```shiki
<route id="frontend.subscription.checkout.cart.page"
        path="/subscription/checkout/cart/{subscriptionToken}"
        methods="GET"
        controller="subscription.storefront.controller.checkout::cartPage">
    <default key="_noStore">true</default>
    <default key="_routeScope"><list><string>storefront</string></list></default>
    <default key="_subscriptionCart">true</default>
    <default key="_subscriptionContext">true</default>
    <default key="_controllerName">checkout</default>
    <default key="_controllerAction">cartpage</default>
    <default key="_templateScopes">subscription</default>
    <option key="seo">false</option>
</route>
```

And, here is an example of the headers set on a subscription cart using headless:

sh

```shiki
curl -XPOST '/store-api/subscription/checkout/cart/line-item' /
    -H 'sw-subscription-plan: <subscription-plan-id>' /
    -H 'sw-subscription-interval: <subscription-interval-id>' /
    -d '{
      "lineItems": [{
        "id": <product-id>,
        "subscriptionPlan": <subscription-plan-id>,
        "subscriptionInterval": <subscription-interval-id>
        ...
      }]
    }'
```

These context definitions can be found in `Subscription/Resources/app/config/routes/storefront.xml` or `Subscription/Resources/app/config/routes/store-api.xml`.

## Subscription carts in the Storefront [​](#subscription-carts-in-the-storefront)

To change Storefront pages while a customer is a subscription checkout process, the template scope `subscription` must be added to the page's Twig templates and subsequent Twig templates used. This affects at least the following pages:

* `frontend.checkout.cart.page` / `@Storefront/storefront/page/checkout/cart/index.html.twig`
* `frontend.checkout.confirm.page` / `@Storefront/storefront/page/checkout/confirm/index.html.twig`
* `frontend.checkout.register.page` / `@Storefront/storefront/page/checkout/address/index.html.twig`
* `frontend.account.edit-order.page` / `@Storefront/storefront/page/account/order/index.html.twig`
* `frontend.account.login.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.account.register.page` / `@Storefront/storefront/page/account/register/index.html.twig`

Further information can be found in the [dedicated guide here](./template-scoping.html).

---

## Mixed checkout

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/guides/mixed-checkout.html

# Mixed subscription checkout [​](#mixed-subscription-checkout)

INFO

Available since Shopware version 6.7.4.0

This guide describes how the so-called `mixed carts` for subscriptions work and how extensions should integrate with it. Mixed carts let customers buy subscription products and one‑time products during a single checkout while keeping subscription calculation isolated and predictable.

Please familiarize yourself with the [concept](./../concept.html) first before continuing here.

## Overview [​](#overview)

Subscription line items are ordinary product line items in the main cart, but they carry subscription plan and interval IDs in their payload. During cart calculation, line items containing subscription plan and interval IDs in their payload are collected and grouped by plan and interval. For each group a derived *managed* subscription context and a *managed* subscription cart are created and calculated using the subscription cart calculation path. These represent the context and content of the upcoming generated subscription.

Managed subscription contexts and carts are persisted in the database as well. They are linked back to the main context by the `subscription_cart` database table.

## Retrieving information [​](#retrieving-information)

You can access the managed carts through the cart extension named `subscriptionManagedCarts`, which maps keys in the form `<plan-id>-<interval-id>` to their corresponding [managed cart](./../concept.html#subscription-cart). The sales channel context extension named `subscriptionManagedContexts` provides the same mapping for [managed sales channel contexts](./../concept.html#subscription-context). The intended way of retrieving plan and interval IDs is to split the composite ID out of this mapping.

When an order is placed from a mixed cart, the order will contain an `initialSubscriptions` extension that includes all created subscriptions. As any subsequent orders are generated per subscription, the orders will contain a `subscriptionId` / `subscription` extension instead.

## Manipulate mixed cart [​](#manipulate-mixed-cart)

With subscription mixed carts, you manipulate the main cart as [you are used to](./../../../../guides/plugins/plugins/checkout/cart/). This is different from the [separate checkout](./separate-checkout.html#manipulate-subscription-cart), where you manipulate a separate subscription cart directly, e.g. by subscription scoped cart processors or separate Store API routes. Therefore, to support mixed carts, your cart collectors and processors should process both subscription carts and regular carts, so they need to be tagged with `subscription.cart.collector` (or `subscription.cart.processor`) as well as `shopware.cart.collector` (or `shopware.cart.processor`). If you need to differentiate between main and subscription cart calculations, check the sales channel context for the [subscription extension](./../concept.html#subscription-context). If you need to differentiate between a mixed and a separate subscription cart calculation, check `salesChannelContext.extensions.subscription.isManaged`.

The cart processor `Shopware\Commercial\Subscription\Checkout\Cart\Discount\SubscriptionDiscountProcessor` is a good example how to add line items to mixed carts.

WARNING

We discourage the use of subscription collectors and processors for adding new line items **only** to subscription carts. Instead, always make sure to add line items to the main cart as well. This is because it's potentially confusing for customers, and handling line items in subscription carts missing in the main cart is more difficult. Instead, follow [the steps described below](#adding-subscription-line-items) to add additional line items.

If you still want to add line items to subscription carts only, please add a subscriber to the `SubscriptionOrderLineItemRestoredEvent` event to correctly show the line item in Shopware's after order process.

### Adding subscription line items [​](#adding-subscription-line-items)

To add a line item to a subscription cart, the relevant subscription plan and interval IDs must be added.

The following methods are available to do so via the **Store-API**:

* Add `lineItem.subscriptionPlan` and `lineItem.subscriptionInterval` IDs to a line item
* Add `lineItem.subscriptionPlan` and `lineItem.subscriptionInterval-<plan-id>` IDs to a line item (useful when submitting HTML forms)
* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line item's payload

Information added through the first two methods will be remapped to the line item's payload, as shown in the last method.

To do so via the **backend**, like in cart collectors or processors, the following methods are available:

* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line items payload

## Events [​](#events)

A mixed cart will fire all events like usual. Additionally, any event fired during the subscription cart calculation will be prefixed with `subscription.` like it is the case in the [separate checkout](./separate-checkout.html#events).

INFO

Note that unlike the separate checkout, only the normal `CheckoutOrderPlacedEvent` but no `'subscription.' . CheckoutOrderPlacedEvent` (or similar) will be fired, as the subscription carts are not placed as separate orders.

## Mixed carts in the Storefront [​](#mixed-carts-in-the-storefront)

To change the following Storefront pages if a mixed cart is present, the template scope `mixed-subscription` must be added to the page's Twig templates and subsequent Twig templates used:

* `frontend.checkout.cart.page` / `@Storefront/storefront/page/checkout/cart/index.html.twig`
* `frontend.checkout.confirm.page` / `@Storefront/storefront/page/checkout/confirm/index.html.twig`
* `frontend.checkout.register.page` / `@Storefront/storefront/page/checkout/address/index.html.twig`
* `frontend.account.edit-order.page` / `@Storefront/storefront/page/account/order/index.html.twig`
* `frontend.account.login.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.account.register.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.cart.offcanvas` / `@Storefront/storefront/component/checkout/offcanvas-cart.html.twig`

Further information can be found in the [dedicated guide here](./template-scoping.html). The list can be changed through the `subscription.routes.mixed-storefront-scope` Symfony container parameter.

Besides the scope change in Twig templates, the following additional information is available in Twig templates:

* The global `context` will have the `subscriptionManagedContexts` extension available. See [here](#retrieving-information)
* `page.cart` will have the `subscriptionManagedCarts` extension available. See [here](#retrieving-information)
* `page.order` will have the `initialSubscriptions` extension available, containing the collection

---

## Template scoping

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/guides/template-scoping.html

# Subscription template scoping [​](#subscription-template-scoping)

Please familiarize yourself with the [concept](./../concept.html) first before continuing here.

In a subscription context, it's important to ensure that certain twig template adjustments, which are applicable to the standard storefront, are not automatically applied. This precaution helps in maintaining a clear distinction between the regular checkout process and the subscription checkout process. For instance, elements or buttons that facilitate immediate purchases or third-party payment options, like PayPal Express, should not be visible during the subscription checkout to avoid confusion.

To achieve this separation, templates used within the subscription context should explicitly define their scope. The subscription feature adds two scopes: `subscription` and `mixed-subscription`. Read more about the two checkout processes in the [subscription concept](./../concept.html#checkout-processes).

Below is an example of extending a template in the default and subscription context:

twig

```shiki
{% sw_extends {
    template: '@Storefront/storefront/base.html.twig',
    scopes: ['default', 'subscription']
} %}
```

A specific scope also assures the availability of certain data: **`subscription`**: The global `context` is replaced with the [subscription context](./../concept.html#subscription-context), therefore having the `subscription` extension available

---

## B2B Employee Integration

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/guides/b2b-employee-integration.html

# B2B Employee Integration for Subscriptions [​](#b2b-employee-integration-for-subscriptions)

When using Subscriptions together with B2B Components Employee Management, subscriptions can be managed and tracked in a B2B employee context.

## Overview [​](#overview)

The B2B Employee Integration extends subscription functionality to support employee-based workflows in B2B scenarios. This integration enables:

* **Permission-based subscription access** - Control which subscriptions employees can view based on their assigned permissions
* **Employee tracking** - Track which employee created each subscription for audit and reporting purposes
* **Organization context** - Maintain organization information in both initial and renewal subscription orders

## When to Use [​](#when-to-use)

This integration is relevant when you have:

* A B2B store with employee management enabled
* Subscriptions that employees should manage on behalf of their organization
* Requirements for permission-based access control to subscription data
* Need for tracking which employee initiated subscriptions

## Prerequisites [​](#prerequisites)

To use this integration, you need:

* Shopware 6.7 with the **Subscriptions** extension installed
* **B2B Components** with Employee Management module enabled
* Employees configured with appropriate roles and permissions

## Key Capabilities [​](#key-capabilities)

### 1. Permission-Based Viewing [​](#_1-permission-based-viewing)

Employees can view subscriptions based on three permission levels:

* **`subscription.read.all`** - View all subscriptions in the system
* **`organization_unit.subscription.read`** - View subscriptions from their organization unit plus their own
* **No subscription permission** - View only subscriptions they personally created

### 2. Employee Context in Orders [​](#_2-employee-context-in-orders)

When an employee creates a subscription:

* The **initial order** includes employee and organization data
* All **renewal orders** automatically maintain this context
* Employee information is preserved for reporting and compliance

### 3. Transparent Integration [​](#_3-transparent-integration)

The integration works seamlessly with existing subscription workflows:

* Works with both [separate checkout](./separate-checkout.html) and [mixed checkout](./mixed-checkout.html) flows
* No changes required to existing subscription products or plans
* Employee context is automatically added when an employee is logged in

## Technical Documentation [​](#technical-documentation)

For detailed technical information including architecture, event flows, database schema, and developer integration points, see:

**[B2B Employee Subscription Integration Guide](./../../b2b-components/employee-management/guides/subscription-integration.html)**

The technical guide covers:

* Architecture and integration patterns (decorators, event subscribers, entity extensions)
* Database schema for employee-subscription relationships
* Detailed flow diagrams for initial orders, renewals, and permission filtering
* Code examples for accessing employee data from subscriptions and orders
* Extension points for adding custom B2B logic

## Related Documentation [​](#related-documentation)

* [Subscription Concept](./../concept.html) - Understanding subscription fundamentals
* [Mixed Checkout](./mixed-checkout.html) - Mixed cart checkout with subscriptions
* [Separate Checkout](./separate-checkout.html) - Separate subscription checkout flow
* [B2B Employee Management](./../../b2b-components/employee-management/) - Employee and role management basics

---

## Subscription concept

**Source:** https://developer.shopware.com/docs/products/extensions/subscriptions/concept.html

# Subscription concept [​](#subscription-concept)

To use subscriptions, you will need to be familiar with three core concepts: **Subscription Plans**, **Subscription Intervals**, and the **Checkout Processes**.

## Terminology [​](#terminology)

### Subscription Plans [​](#subscription-plans)

A plan is a set of rules that define the subscription. This includes the [billing interval](#subscription-intervals) and the product that the customer will receive. Multiple intervals can be assigned to a single plan. Plans can be created and managed in the Shopware administration.

### Subscription Intervals [​](#subscription-intervals)

An interval is the time between each delivery cycle. For example, a delivery can be monthly, quarterly, or annually. Billing is triggered each time a delivery cycle repeats. The interval is defined in the plan and can be set to any time frame. This is also created and managed in the Shopware administration.

Intervals can be of two different types:

1. **Relative**  
    A relative interval is determined by a previous interval. For example, if a customer subscribes to a monthly plan, the next interval will be one month after the first delivery. These intervals are determined using PHP's `DateInterval`.
2. **Absolute**  
    An absolute interval is determined by a fixed date. For example, if a customer subscribes to a monthly plan, the next interval will be on a fixed day like the 1st or 15th of each month. These intervals are defined using cron expressions.

   Absolute intervals can also possess a relative element, such as a delivery occurring every 12 weeks (relative component), but exclusively on Fridays (absolute component). Note that both parts will be satisfied in sequence. Depending on the order date, in this example the next calculated date could exceed 12 weeks by an additional 6 days in order to fulfil the requirement of being a Friday.

### Subscription products [​](#subscription-products)

A product with a [subscription plan](#subscription-plans) assigned. You can purchase the product as a one-off or subscribe to it at the intervals assigned to the plan.

Subscription products are ordinary product line items when added to the cart, but since 6.7.4.0 carry the selected subscription plan and interval IDs in their payload.

### Subscription [​](#subscription)

A subscription contains all the information needed to generate new orders on a recurring basis. This includes among other things:

* The subscription plan and interval
* The schedule for subsequent orders
* The number of deliveries left to fulfil the minimum delivery cycles
* The payment method used
* A copy of the order to be placed on a recurring basis

INFO

Please note that the necessary payment information for paying subsequent orders is not included in a subscription. It is the responsibility of the recurring payment method to store this information.

### Subscription cart [​](#subscription-cart)

A subscription cart contains [subscription products](#subscription-products) from a single [subscription plan](#subscription-plans) and [interval](#subscription-intervals) combination. It has been calculated using the subscription cart calculator. The only difference between this and the normal cart calculator is the subset of cart processors and collectors used. After checkout, the subscription cart will be converted into a [subscription](#subscription).

Read more about how to work with [subscription carts here](./guides/separate-checkout.html#how-to-manipulate-cart).

The database table `subscription_cart` is used to link the cart / context token to any subscription cart / context.

### Subscription context [​](#subscription-context)

A subscription context is a sales channel context that has additional subscription metadata added as an extension called `subscription`. It can be accessed via `salesChannelContext.extensions.subscription`. It contains the selected subscription plan, interval as well as the context token of the main sales channel context.

As the subscription context is derived from the sales channel context, the original sales channel context is referred to as the *main context* further on.

## Checkout Processes [​](#checkout-processes)

### Separate Subscription Checkout [​](#separate-subscription-checkout)

The **separate subscription checkout** allows customers to purchase subscription products via an isolated checkout process and dedicated cart. This process is best described as an express checkout for subscription products.

**Key aspects:**

* Subscription products have to be checked out one by one
* For each subscription product a new [subscription cart](#subscription-cart) is created, preserving the contents of the main cart
* For each subscription checkout a new [subscription context](#subscription-context) is derived, preserving the address, shipping method and payment method selections of the main cart

### Mixed Cart Checkout [​](#mixed-cart-checkout)

INFO

Available since Shopware version 6.7.4.0

The **mixed cart checkout** allows customers to purchase subscription products and one-time products together in a single cart.

**Key aspects:**

* Subscription products are added to the main cart as normal product line items, but additionally containing subscription plan and subscription interval metadata in its payload
* For each combination of subscription interval and subscription plan a new *managed* subscription cart will be derived, only containing matching products of the main cart
* For each combination of subscription interval and subscription plan a new *managed* subscription context will be derived, allowing for context changes in a managed subscription cart
* Each managed subscription cart will be calculated and serves as the point of truth for the later generated subscriptions and are shown as subscription group in the storefront

\* as context and cart are *always* derived from their original counterparts and only a subset of information will be inherited from the existing managed context or cart, we call context and cart *managed*.

## Reasons for the architectural design [​](#reasons-for-the-architectural-design)

To understand the subscription feature better, it may help to know the reasons behind the architecture:

The Subscriptions feature is designed to prevent interference from existing extensions and avoid applying potentially incompatible business logic to subscriptions. Developers who want to have their manipulations, PHP or Storefront, applied to subscriptions have to "opt-in" via [scoped templates](./guides/template-scoping.html), [scoped events](./guides/separate-checkout.html#events) or by [special service tags](./guides/separate-checkout.html#manipulate-subscription-cart). This is done to ensure that existing extensions do not manipulate the cart in a way that is not intended in a subscription context or hinder the subsequent generation of orders. This should ensure a smooth subscription process from the beginning, eliminating the need to ask extension authors to adapt their integration before the feature can be used. For that reason [Storefront scopes](./guides/template-scoping.html) were introduced to avoid template additions like express checkout buttons, which are incompatible due to being a guest checkout or may not support recurring payments and would not be possible to hide otherwise. The same applies to the isolated subscription calculation process and event scoping - all to avoid undesirable cart manipulation.  
 Note that promotions are one example for undesirable business logic due to their complexity when it comes to including them in recurring orders or excluding specific cases, such as one-use codes.

The subscription feature was first implemented with the [separate checkout](#separate-subscription-checkout) experience. It was chosen because it only handles one subscription at a time, which keeps the complexity low. Generated subscription orders are straight forward and look exactly like their storefront cart representation.  
 In order for such a checkout to be possible, a cart containing only the subscription product is required. A new cart and context are created to avoid manipulating the main cart and context if it has already been filled. As this subscription cart is independent of the main cart, all cart routes were copied and scoped to be able to resolve the correct subscription cart. You can find out more about [request scoping here](./guides/separate-checkout.html#request-scoping).

The mixed cart checkout was added later and is built on top of the existing codebase for calculating and managing additional [subscription carts](#subscription-cart). This was done so that orders generated from subscriptions created by a mixed cart would appear as if they had been placed independently, with their own total price, shipping costs, and so on. Reusing existing logic reduces the friction to adapt existing extensions too.  
 It would be far too complex to treat subscription carts as separate entities, so they are always derived from the main cart. This is possible because any subscription item must be in the main cart to end up in the initial order anyway.

## Further Reading [​](#further-reading)

You can read more about the setup of plans, intervals, and checkout processes in the [Shopware documentation](https://docs.shopware.com/en/shopware-6-en/settings/shop/subscriptions).

---

