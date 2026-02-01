# Concepts Commerce

*Scraped from Shopware Developer Documentation*

---

## Commerce

**Source:** https://developer.shopware.com/docs/concepts/commerce/

# Commerce [​](#commerce)

At core, Shopware is an **ecommerce platform**. If you want to understand the commerce-related concepts of our software, make sure to go here.

INFO

The **Concepts** section does not contain code examples, instead we focus on conveying the concepts and ideas behind the software. If you want more guided, step-by-step tutorials, please head to the [Guides](./../../guides/installation/) section.

---

## Catalog

**Source:** https://developer.shopware.com/docs/concepts/commerce/catalog/

# Catalog [​](#catalog)

In this section, we will go through the structure that organizes products, prices and everything related to maintaining a **product catalog** within the store.

First, let us understand about products and how they are defined.

---

## Products

**Source:** https://developer.shopware.com/docs/concepts/commerce/catalog/products.html

# Products [​](#products)

Products are sellable entities (physical and digital products) within your shop.

Depending on your setup, Shopware can easily handle thousands of products. However, an upsurge in the product quantity (in millions) needs some tweaks for robust running of the environment as it depends on factors like the number of [categories](./../../../concepts/commerce/catalog/categories.html), [sales channels](./../../../concepts/commerce/catalog/sales-channels.html), [product properties](./../../../concepts/commerce/catalog/products.html), etc. Every product added to your shop can be made available on one or more [sales channels](./../../../concepts/commerce/catalog/sales-channels.html).

Let's delve into a more detailed understanding of products using the example of garments:

* **Product details**: General information about a Product.

| Title | Product Id | Manufacturer | Prices | .... |
| --- | --- | --- | --- | --- |
| Levis Ocean Hoodie | SW1001 | CA | 40 | ... |

* **Product properties**: Product properties encapsulate property groups and options. They are displayed in a table on product details page, in listings, or even be used for filtering. A product can have arbitrarily many property group options.

| Property Group | Property Group Options |
| --- | --- |
| Size | *S*, *M*, *L*, *XL*, etc |
| Color | *Red*, *Blue*, *Green*, *Black* |
| Material | *Leather*, *Cotton*, *Jeans* |

* **Category**: Products in Shopware are organized in categories. It is a grouping of products based on characteristics, marketing or search concerns. Categories are represented as a hierarchical tree to form a navigation menu. A product can be contained in multiple categories.
* **Packaging dimensions**: Physical dimensions and weight of the product packaging. These values are stored in standardized units: weight in kilograms (kg) and dimensions (width, length, height) in millimeters (mm). This information is crucial for shipping calculations, storage planning, and logistics operations. However, these units can be configured to be displayed differently on storefront and APIs depending on the sales channel context.

| Dimension | Stored Value | Display Value (configurable) |
| --- | --- | --- |
| Weight | 1.5 | 3.3 lbs/1500g/1.5kg |
| Width | 300 | 11.8 in/300mm/0.3m |
| Length | 400 | 15.7 in/400mm/0.4m |
| Height | 200 | 7.9 in/200mm/0.2m |

INFO

The configurable measurement units are only available in Shopware v6.7.1.0 and later version. Before that, the values are always stored in the metric system and displayed in the same way.

Below you find an overview of relationships between the entities. Products, categories, options, and property groups are interconnected in the database schema.

* **Product variant**: A sellable product. Products are a self-referencing entity, which is interpreted as a parent-child relationship. Similarly, product variants are also generally mapped to products. This mechanism is used to model variants. This also provides inheritance between field values from parent products to child products.

It is also useful to attach some additional properties to differentiate product variants next to the field inheritance. For that reason, it is critical to understand the difference between *properties* and *options*:

**Properties** are used to model facts about a product, but usually, different product variants share these facts. We can refer to properties as *non variant defining*. They could be useful to represent the following information:

* Product Series / Collection
* Washing Instructions
* Manufacturing country

Opposed to that, **options** are considered variant defining, as they are the facts that differ from one product variant to another. Such as

* Shirt Size
* Color
* Container volume

It is important to understand the difference between those two because both provide a relation between the *product* and the *property group option* entity. However, only one constitutes to *product variants*.

| Variant | Product | Category | Product Group | Product Group Option |
| --- | --- | --- | --- | --- |
| Variant 1 | Levis Ocean Hoodie | Hoodie & Sweaters | Color | Red |
| Variant 2 | Levis Ocean Hoodie | Hoodie & Sweaters | Color | Black |

## Configurator [​](#configurator)

When a variant product is loaded for a [Store API](./../../api/store-api.html)-scoped request, Shopware assembles a configurator object which includes all different property groups and the corresponding variants. This way client applications, such as the [Storefront](./../../../guides/plugins/plugins/storefront/) or [Composable Frontends](./../../../../frontends/) can display the different variant options of the product.

The following section is a detailed understanding on category.

---

## Categories

**Source:** https://developer.shopware.com/docs/concepts/commerce/catalog/categories.html

# Categories [​](#categories)

Categories in Shopware organize products, drive storefront navigation, and define SEO-relevant URLs. The entire catalog lives in one category tree, and every sales channel chooses entry points inside that tree. For how to use the Admin UI, see the [user documentation on categories](https://docs.shopware.com/en/shopware-6-en/catalogues/categories) and [Dynamic Product Groups](https://docs.shopware.com/en/shopware-6-de/Catalogues/Dynamicproductgroups). This page focuses on developer details.

![category](/assets/concept-categories.CC1K7cB5.png)

## Category model and tree [​](#category-model-and-tree)

* Each category stores `parentId`, `path`, and `level` to build breadcrumbs, infer inheritance, and traverse efficiently.
* Flags:
  + `active` determines whether the category participates in navigation and listings.
  + `visible` and `hideInNavigation` control menu rendering without disabling the category entirely.
* Types:
  + `page`: regular category (listing or landing page).
  + `folder`: structuring element; not rendered as a page and typically used to group children.
  + `link`: redirects to an external URL or internal static link.

## Entity associations and database schema [​](#entity-associations-and-database-schema)

* `category`: tree structure plus `cmsPageId` for layout inheritance; `productAssignmentType` controls explicit vs. stream-based listings.
* `category_translation`: localized names, breadcrumbs, links, and SEO text.
* `product_category`: explicit product links used for listings when not driven by a product stream.
* `product_stream`: dynamic filters attached to a category when assignments are stream-based.
* `cms_page`: CMS layout referenced by categories (inherited when missing).
* `sales_channel`: entry categories (`navigation`, `footer`, `service`) anchoring storefront menus.
* `seo_url`: generated URLs per category and sales channel domain, rebuilt by the SEO indexer.

## Sales channel entry points and navigation [​](#sales-channel-entry-points-and-navigation)

Every [Sales Channel](./sales-channels.html) defines `navigation`, `footer`, and `service` entry categories. The storefront builds menus from the children of those entry points, inheriting explicit assignments from lower levels.

Store API endpoints:

* `/store-api/navigation/{activeId}/{rootId}` for hierarchical menus.
* `/store-api/category/{navigationId}` for category details including assigned CMS layout data.

Navigation responses are cached. Adjust cache identity or tags via `NavigationRouteCacheKeyEvent` and `NavigationRouteCacheTagsEvent`. Use `NavigationLoadedEvent` to enrich or modify the tree before it is returned.

INFO

Categories can be hidden from navigation via the hide-in-navigation flag while remaining reachable by direct URL if they are still `active`.

## Product assignments and Dynamic Product Groups [​](#product-assignments-and-dynamic-product-groups)

* Explicit assignments: stored in `product_category` (and `product_category_tree` for inherited links) to put category IDs directly on products.
* Dynamic Product Groups (product streams): attached to a category to evaluate saved filters at runtime and automate listings (for example, brand filters or price ranges). See the [user docs](https://docs.shopware.com/en/shopware-6-de/Catalogues/Dynamicproductgroups) for configuration guidance.

Both assignment types are merged for a category listing. `ProductListingRoute` builds the listing criteria from the category configuration, sales channel, and request filters. Extend or alter the listing query with `ProductListingCriteriaEvent`.

## CMS layout integration [​](#cms-layout-integration)

Categories can reference a [CMS layout](./../content/shopping-experiences-cms.html). Layout selection is inherited: if `cmsPageId` is missing, the parent layout is used. Category-specific slot configuration is stored on the category and merged at runtime, so one layout can serve many categories with different media and copy. `folder` categories ignore layouts; `link` categories redirect immediately.

## SEO and URLs [​](#seo-and-urls)

Per-category SEO fields include `metaTitle`, `metaDescription`, `keywords`, `seoUrl`, and robot flags (`noIndex`, `noFollow`). SEO URLs are generated from templates under *Settings → SEO* and are rebuilt when categories change or when the SEO indexer runs.

* Customize URL templates (e.g., include the breadcrumb) and priorities per sales channel domain.
* React to regenerated URLs via `SeoUrlUpdateEvent`, or enqueue additional updates when categories are changed programmatically.
* Emit canonical links when rendering custom category pages.

## Extensibility and events [​](#extensibility-and-events)

* `NavigationLoadedEvent`: navigation tree loaded; enrich or adjust nodes.
* `SalesChannelCategoryIdsFetchedEvent`: category IDs resolved for a sales channel.
* `CategoryIndexerEvent`: keep de-normalized data or external search indices in sync.
* `ProductListingCriteriaEvent`: customize listing filters, sorting, and aggregations for category pages.
* `SeoUrlUpdateEvent`: observe or react to SEO URL regeneration.

Categories are fully extensible via custom fields or entity extensions. Expose custom data through Store API response extensions when it is needed in storefronts or external channels.

---

## Sales Channels

**Source:** https://developer.shopware.com/docs/concepts/commerce/catalog/sales-channels.html

# Sales Channels [​](#sales-channels)

Sales channels define how your catalog is exposed to a concrete audience (storefront, headless client, feed, or app). Each channel carries defaults for language, currency, taxes, payment/shipping, domains, and navigation entry points so one Shopware instance can serve multiple “stores” without duplicating data.

## What a sales channel controls [​](#what-a-sales-channel-controls)

* Channel type: Storefront, headless Store API, product feed, or custom type.
* Audience defaults: language, currency, country, tax calculation mode, customer group, default payment/shipping methods.
* Navigation roots: `navigation`, `footer`, and `service` entry categories that drive storefront menus and listings.
* Presentation: home CMS page (`homeCmsPageId` with slot config) and storefront theme config for Storefront channels.
* Availability: which domains, payment/shipping methods, languages, currencies, and countries are allowed and which products are visible.

## Core model and relations [​](#core-model-and-relations)

* `sales_channel`: Holds defaults (language, currency, country, payment/shipping, tax calculation), navigation roots, home CMS page, access key, maintenance flags, hreflang config.
* `sales_channel_domain`: URL + language + currency + snippet set. Matched by host/path to build the sales channel context.
* `sales_channel_translation`: Localized channel names and home page fields.
* `product_visibility`: Per-channel visibility level for products. Required for products to appear.
* `sales_channel_*` mappings: Allow additional currencies, languages, countries, payment, and shipping methods beyond the defaults.
* `cms_page`: Optional home page layout with channel-specific slot configuration.

## Domains and localization [​](#domains-and-localization)

Configure multiple domains per sales channel. Each domain pins language, currency, and snippet set (translations). Example:

* `https://example.com/` → en-GB, GBP
* `https://example.com/de` → de-DE, EUR
* `https://example.es/` → es-ES, EUR

`hreflangActive` and `hreflangDefaultDomainId` control hreflang links across these domains.

## Navigation entry categories [​](#navigation-entry-categories)

Every sales channel defines three category entry points: `navigation`, `footer`, and `service`. Storefront menus are built from the children of those entries. Category listings under these roots merge explicit product assignments and, if configured, dynamic product streams.

## Product availability per channel [​](#product-availability-per-channel)

Products must have a `product_visibility` row for each sales channel. Visibility values decide whether a product is searchable and/or directly accessible. A canonical category (`main_category`) can be set per product and sales channel for SEO-friendly URLs.

## Context creation and Store API [​](#context-creation-and-store-api)

Incoming requests resolve a sales channel by access key or matched domain. `SalesChannelContextService` builds a `SalesChannelContext` with the defaults above plus token, customer, rule-based pricing, and permissions. Store API routes such as `/store-api/context`, `/store-api/navigation/{activeId}/{rootId}`, and `/store-api/category/{navigationId}` use that context to filter data to the channel.

## Extension points and events [​](#extension-points-and-events)

* `SalesChannelContextCreatedEvent`: context built; use to enrich the context or persist session data.
* `SalesChannelContextSwitchEvent`: fired when `/store-api/context` switches currency, language, payment, shipping, or addresses.
* `SalesChannelContextRestoredEvent`: emitted when a stored context token is restored.
* Entity extensions: add custom fields or associations on `sales_channel` or mapping entities and expose them through Store API responses as needed.

---

## Checkout

**Source:** https://developer.shopware.com/docs/concepts/commerce/checkout-concept/

# Checkout [​](#checkout)

The checkout holds a series of steps to purchase items in your store. The checkout in Shopware deals with the entire process of turning a cart into an order and initiating all associated processes like payment, shipping, etc.

This section further focuses on carts, orders and payment.

---

## Cart

**Source:** https://developer.shopware.com/docs/concepts/commerce/checkout-concept/cart.html

# Cart [​](#cart)

Shopping cart management is a central feature of Shopware 6. The shopping cart resides in the checkout bundle and is a central part of the checkout process.

## Design goals [​](#design-goals)

The cart was designed with a few design goals in mind.

### Adaptability [​](#adaptability)

Although many services exist to make working with the cart simple and intuitive, the cart itself can be changed through various processes and adapt to numerous use cases.

### Performance [​](#performance)

The cart is designed by identifying key processes and optimizing upon them. Therefore the amount of calculations, queries, and iterations are kept to a minimum, and a clear state management is implemented.

### Abstraction [​](#abstraction)

The cart has very few hard dependencies on other core entities in Shopware 6. Entities such as products, surcharges, or discounts are referenced through interfaces that the line items in the cart reference.

## Cart Struct [​](#cart-struct)

`\Shopware\Core\Checkout\Cart\Cart`

An instance of this class represents one single cart. As shown in the diagram below, relations to central Entities of the system are omitted. This allows Shopware 6 to manage multiple carts per user, per sales channel, or across all sales channels. The only identification is a token hash.

![Representation of the cart struct](/assets/commerce-checkout-cartStruct.Bx41cIUR.svg)

This highly mutable data structure is acted upon from requests and calculated and validated through services. It contains:

### Line Items [​](#line-items)

A line item represents an order position.

* It may be a shippable good, a download article, or even a bundle of many products.
* Line items contain properties that tell the cart how to handle changes in line items. E.g., *stackable* - quantity can be changed, *removable* - removable through the API, and so on.
* A line item is the main extension point for the cart process. Therefore a promotion, a discount, or a surcharge is also a line item.
* A line item can even contain other line items. So a single order position can be the composition of multiple single line items.

### Transaction [​](#transaction)

It is the payment in the cart. Contains a payment handler and the amount.

### Delivery [​](#delivery)

It is a shipment in the cart. It contains a date, a method, a target location, and the line items that should be shipped together.

### Error [​](#error)

Validation errors which prevent ordering from that cart.

### Tax [​](#tax)

The calculated tax rate for the cart.

### Price [​](#price)

The price of all line items, including tax, delivery costs, voucher discounts, and surcharges.

## State [​](#state)

Shopware 6 manages the cart's state through different services. The diagram below illustrates the different states the cart can have and the state changes it can go through.

| Cart state | Description |
| --- | --- |
| Empty | A cart with no items will have default shipping and payment settings. |
| Dirty | On adding a new line item, the cart undergoes modifications with invalid prices, raw line items, and uncertain delivery validity. Consequently, calculations are necessary. |
| Calculated | After accurate calculations, the cart can be either submitted as an order or may contain errors that need to be addressed. |

## Calculation [​](#calculation)

Calculating a cart is one of the more costly operations an ecommerce system must support. Therefore the interfaces of the cart are designed as precise and as quick as possible. The calculation is a multi-stage process that revolves around the mutation of the data structure of the cart struct shown in the diagram below:

| Cart calculation state | Description |
| --- | --- |
| Enrich | The calculation process in the **enrich state** for line items involves adding images, its descriptions and determining prices |
| Process | During the **process state**, price updates occur, adjustments to shipping and payment are made |
| Validate | In the **validate state**, validation is performed using the rule system and cart changes based on plausibility checks. |
| Persist | The **persist state** is responsible for updating the storage. |

### Cart enrichment [​](#cart-enrichment)

Enrichment secures the *Independence\_ and \_Adaptability* of Shopware 6. As shown in the below code snippet, the cart can create and contain line items that are initially empty and will only be loaded (enriched) during the calculation.

php

```shiki
<?php

use Shopware\Core\Checkout\Cart\Cart;
use Shopware\Core\Checkout\Cart\LineItem\LineItem;

$lineItem = new LineItem(/* ... */);
/** @var $cart Cart */
$cart->getLineItems()->add($lineItem);

$lineItem->getPrice(); // is now null
// enrich the cart
$lineItem->getPrice(); // now set up
```

This process is transparently controlled from the cart but executed through implementations of `\Shopware\Core\Checkout\Cart\CartDataCollectorInterface`. This interface is cut in order to reduce the number of database calls necessary to set up the cart's data structure for **price calculation** and **inspection** (meaning: rendering in a storefront, reading from the API).

A default set of collectors is implemented in Shopware 6, which has a set call order shown in the diagram below.

| Service ID | Task |
| --- | --- |
| Shopware\Core\Content\Product\Cart\ProductCartProcessor | Enrich all referenced products |
| Shopware\Core\Checkout\Promotion\Cart\CartPromotionsCollector | Enrich add, remove and validate promotions |
| Shopware\Core\Checkout\Shipping\Cart\ShippingMethodPriceCollector | Handle shipping prices |

## Cart processors - price calculation and validation [​](#cart-processors-price-calculation-and-validation)

After a cart is enriched, the cart is processed. The price information for all individual `LineItems` is now set up to calculate the sums. This happens in the `\Shopware\Core\Checkout\Cart\Processor` class, following these steps:

* The `lineItem` prices are calculated by applying the quantity and the tax rate.
* Deliveries are set up and cost calculated.
* Different cart values are summed up (incl, excl. vat, inc. excl. shipping).

Then the calculation of prices is done, and the cart can be inspected from the rule system.

## Context rules [​](#context-rules)

After the cart has been processed, it is validated against the rules, which can lead to a change in the carts' data, so a revalidation becomes necessary. We can envision a scenario where we sell cars and have the following rules:

* Everybody buying a car gets a pair of sunglasses for free.
* Every cart containing two products gets a discount of 2%.

As you can see in the diagram above, the cart is modified during the enrichment process. The sunglasses are added in the first iteration, and in the second iteration, the discount is added as the cart contains two products. This results in the expected state of one car, one pair of sunglasses, and a two-percent discount.

## Cart storage [​](#cart-storage)

Contrary to other entities in the system, the cart is not managed through the [Data Abstraction Layer](./../../../concepts/framework/data-abstraction-layer.html)(DAL). The cart can only be written and retrieved as a whole. As discussed in the sections, the workload of Shopware 6 can only be performed on the whole object in memory.

## Cart control [​](#cart-control)

The state changes and cart mutation is handled automatically by a facade the `\Shopware\Core\Checkout\Cart\SalesChannel\CartService`. It controls, sets up, and modifies the cart struct.

---

## Orders

**Source:** https://developer.shopware.com/docs/concepts/commerce/checkout-concept/orders.html

# Orders [​](#orders)

From a cart instance, an `Order` can be created. The whole structure of the cart is stored in the database. Contrary to the cart, a structure that allows a great degree of freedom and is *calculation optimized*, the order is *workflow optimized*.

## Design goals [​](#design-goals)

### Denormalization [​](#denormalization)

The order itself does not depend on the catalog or the products. The line item with all of its data, as well as all calculated prices, is persisted in the database. Orders only get recalculated when triggered explicitly through the API.

### Workflow dependant [​](#workflow-dependant)

The order state changes in a defined, predictable and configurable way - other state transitions are blocked.

## State management [​](#state-management)

TIP

The state machines displayed in the following sections can actually be modified through the API, this is just the default setup.

During the order placement, at least three distinct state machines are started as described in the below diagrams.

These can be used to track the progress during the order process and notify the customer about the current state of the order.

**The order state machine**

**The order transaction state machine**

**The order delivery state machine**

---

## Payments

**Source:** https://developer.shopware.com/docs/concepts/commerce/checkout-concept/payments.html

# Payments [​](#payments)

Shopware 6 payment system is an integral part of the checkout process. A payment is applied to a transaction of an order. As with any order change, this is done through the state machine. At its core, the payment system is composed of payment handlers. These extend Shopware to support multiple different payment types. A list of all payment handlers is stored in the database.

INFO

If you want to directly skip to implementation details, then head to the [Add payment plugin](./../../../guides/plugins/plugins/checkout/payment/add-payment-plugin.html) section.

## Payment flow [​](#payment-flow)

The payment and checkout flow consist of two essential steps:

* Placing the order and
* Handling the payment

These steps are outlined in the diagram below:

![Headless payment flow](/assets/checkoutConcept-payment-paymentFlow.pPfHI3T1.svg)

The diagram above shows the payment flow for headless environments; however, for the single-stack scenario (i.e., when the default Storefront is used) the differences are minor and described in the section below.

If you want to see a specific example of a headless payment using the Store API, head to [API documentation](https://shopware.stoplight.io/docs/store-api/8218801e50fe5-handling-the-payment).

### 1. Select payment method [​](#_1-select-payment-method)

The first step for a user is to select their desired payment. The current payment method is stored in the user context, which can be manipulated by calling the corresponding route or endpoint (`/store-api/context`).

### 2. Place order [​](#_2-place-order)

In this step, an order is created. It takes no required parameters but creates the order based on the user's current context and cart. You can add additional information like tracking parameters or comments. Shopware creates the order internally together with an open transaction which acts as a placeholder for the payment.

A transaction contains information like a unique ID, the payment method, or the total amount to be paid. An order can have multiple transactions, but only a single one is created in this step.

#### 2.1 Prepare payment (optional) [​](#_2-1-prepare-payment-optional)

Some payment integrations already create a payment reservation or authorization at this point. This totally depends on the specific payment extension and is not standardized by Shopware in any way. However, usually, some type of payment intent or transaction reference is stored in the meantime.

### 3. Handle payment [​](#_3-handle-payment)

This step can only be executed after an order has been placed. It starts the payment by determining the correct payment handler for the selected payment method.

INFO

Although from a functional perspective, steps 2 and 3 are separated but in the default Storefront both are initiated in the same request.

#### 3.1 Payment handler [​](#_3-1-payment-handler)

There are two types of payment handlers in Shopware:

* **Synchronous payment**

In this scenario, the payment integration usually makes a request to the payment gateway to execute or authorize the payment. The gateway immediately responds with a status and Shopware can give feedback to the user.

* **Asynchronous payment**

These payments include a user redirect. The redirect target is defined by the payment integration and contains information about the transaction as well as a callback URL for the payment gateway.

The frontend can also define success and error URLs that will be used for the eventual redirect after step 3.3.

In the default Storefront, this redirect takes place automatically. In the headless scenario, Shopware returns the redirect URL within the API response so that the frontend can perform the redirect.

#### 3.2 Payment execution on gateway (optional) [​](#_3-2-payment-execution-on-gateway-optional)

This step is only executed for asynchronous payments. After being redirected, the user can perform final checks or authorizations on the payment gateway UI. After that, the payment gateway redirects the user to the callback URL provided in step 3.1 along with a parameter indicating the outcome of the payment.

#### 3.3 Payment finalize (optional) [​](#_3-3-payment-finalize-optional)

This step is only executed for asynchronous payments. It is triggered by the callback URL (which points to `/payment/finalize-transaction`) that has been provided to the payment gateway in step 3.1. Depending on the payment success, Shopware updates the transaction status and redirects the user to the corresponding finish page from step 3.

WARNING

**Disclaimer**

The actual implementation of payment integrations differs between providers. Therefore, our specification does not include any guidelines about payment states or specific API calls to be made. Some integrations share data between the steps or provide and call upon webhooks after the payment process has been finished. These implementations go beyond our standards.

### Session and state [​](#session-and-state)

The session should not be used in headless payment integrations. Read more about [session guidelines](./../../../resources/guidelines/code/session-and-state.html).

### Controllers and API [​](#controllers-and-api)

Do not add any logic inside your controllers and remember to add your Store API routes to the payment, so it can be used in headless scenarios. For Storefront and Store API route integration see the [Add store-api route guide](./../../../guides/plugins/plugins/framework/store-api/add-store-api-route.html)

## Next steps [​](#next-steps)

[Add payment plugin](../../../guides/plugins/plugins/checkout/payment/add-payment-plugin)

---

## Content

**Source:** https://developer.shopware.com/docs/concepts/commerce/content/

# Content [​](#content)

Shopware 6 has an integrated content management system based upon layouts which is called *Shopping Experiences*. The tool used to compose and manage layouts is part of the [Admin panel](./../../framework/architecture/administration-concept.html) and referred to as *Page Builder*.

Beyond content management, Shopware also provides [Cookie Consent Management](./cookie-consent-management.html) with features to help support GDPR compliance by handling customer privacy preferences and cookie handling transparently.

---

## Shopping Experiences (CMS)

**Source:** https://developer.shopware.com/docs/concepts/commerce/content/shopping-experiences-cms.html

# Shopping Experiences (CMS) [​](#shopping-experiences-cms)

Shopware comes with an extensive CMS system referred to as *Shopping Experiences* built upon pages or layouts, which can be reused and dynamically hydrated based on their assignments to categories or other entities.

In the following concept, we will take a look at the following aspects:

* Structure of CMS pages
* Hydration of dynamic content
* Separation of content and presentation

We will start by taking a rather abstract approach to content organization and later translate that into more specific applications.

## Structure [​](#structure)

Every CMS page or layout (they are really technically the same) is a hierarchical structure made of sections, blocks, elements, and additional configurations within each of those components. An exemplary CMS page printed in JSON would look similar to this:

json

```shiki
{
  cmsPage: {
      sections: [{
          blocks: [{
              slots: [{
                  slot: "content",
                  type: "product-listing",
                  /* ... */
              }]
          }, /* ... */]
      }, /* ... */]
  }
}
```

It is a tree where the root node is a **page**. Each page can have multiple **sections**. Each section can contain multiple **blocks**. Each block can have zero or more **slots** where each slot contains exactly one **element**. Easy as that.

Let's go through these structural components in a top-down approach, starting from the biggest element:

### Page [​](#page)

A page serves as a wrapper and contains all content information as well as a `type` which denotes whether it serves as a

* Category/Listing page
* Shop page
* Static page
* Product pages

### Section [​](#section)

Defines a horizontal container segment within your page which can be either:

* Two-Columns which we refer to as `sidebar` and `content` or
* A single column

A section contains blocks that are usually stacked upon each other.

### Block [​](#block)

A block represents a unit usually spanning an entire row which can provide custom layout and stylings. For UI purposes, blocks are clustered into categories such as:

* Text
* Images
* Commerce
* Video

Each block can contain none up to multiple slots. A slot has a name and is just a container for one element. To be more precise, take the following block as an example:

javascript

```shiki
block: {
    type: "text-hero",
    slots: [{
        type: "text",
        slot: "content",
        config: {
            content: {
                source: "static",
                value: "Hello World"
            }
        },
    }]
}
```

It is pretty clear what this will look like. There is a block called `text-hero` containing the text "Hello World". The block is of `type: "text-hero"` and `"type": "text"` here in the nested structure, which displays the text.

Let's take a look at another example:

javascript

```shiki
block: {
    type: "text-hero",
    slots: [{
        type: "image",
        slot: "content",
        config: {
            media: {
                source: "static",
                value: "ebc314b11cb74c2080f6f27f005e9c1d"
            }
        },
        data: {
            media: {
                url: "https://my-shop-host.com/media/ab/cd/ef/image.jpg"
            }
        }
    }]
}
```

Here, we still have the `text-hero` block, but it contains an image. That is due to the internal structure of our CMS and the generic nature of blocks. The slots defined by a block are abstract. In the examples shown above, the `text-hero` block only contains one slot, named `content`.

### Elements [​](#elements)

Elements are the "primitives" in our tree hierarchy of structural components. Elements have no knowledge of their context and usually just contain very little markup. Ultimately and most importantly, elements are rendered inside the slots of their "parent" blocks.

Types of elements comprise:

* text,
* image,
* product-listing,
* video and more

### Configuration [​](#configuration)

Every component (section, block, element) contains a configuration that specifies detailed information about how it's supposed to be rendered. Such configuration can contain:

* Product ID
* Mapped field (e.g. category.description)
* Static values
* CSS config (properties, classes)

Static values will be passed to the page as-is. Mapped fields will be resolved at runtime based on the dynamic content hydration - described subsequently.

## Hydration of dynamic content [​](#hydration-of-dynamic-content)

Whereas the structure of a CMS page remains somewhat static, its content can be dynamic and context-aware. This way, you can, for example, reuse the same layout for multiple category pages where product listing, header image, and description are always loaded based on the category configuration.

### Resolving process [​](#resolving-process)

The following diagram illustrates how that works using the example of a category:

![Flow of resolving CMS page content](/assets/commerce-content-cms.Cio8hoOn.svg)

Let's go through the steps one by one.

1. **Load category**: This can be initiated through an API call or a page request (e.g., through the Storefront).
2. **Load CMS layout**: Shopware will load the CMS layout associated with the category.
3. **Build resolver context**: This object will be passed on and contains information about the request and the sales channel context.
4. **Assemble criteria for every element**: Every CMS element within the layout has a `type` configuration which determines the correct page resolver to resolve its content. Together with the **resolver context**, the resolver is able to resolve the correct criteria for the element. All criteria are collected in a criteria collection. Shopware will optimize those criteria (e.g. by splitting searches from direct lookups or merging duplicate requests) and execute the resulting queries.
5. **Override slot configuration**: The resulting configuration determine the ultimate configuration of the slots that will be displayed, so Shopware will use it to override the existing configuration.
6. **Respond with CMS page**: Since the page data is finally assembled, it can be passed on to the view layer where it will be interpreted and displayed.

### Extensibility [​](#extensibility)

As you can see, the **element resolvers** play a central role in the whole process of getting the configuration ( by extension, content) of CMS elements.

Shopware allows registering custom resolvers by implementing a corresponding interface, which dictates the following methods:

* `getType() : string` -returns the matching type of elements
* `collect(CmsSlot, ResolverContext) : CriteriaCollection`- prepares the criteria object
* `enrich(CmsSlot, ResolverContext, ElemetDataCollection) : void` - performs additional logic on the data that has been resolved

## Separation of content and presentation [​](#separation-of-content-and-presentation)

The CMS is designed in a way that doesn't fix it to a single presentation channel (also referred to it as "headless"). What at first might seem like an unnecessary abstraction turns out to give us a lot of flexibility. Each presentation channel can have its own twist on interpreting the content and displaying it to the user. A browser can leverage the [Shopware Storefront](./../../../guides/plugins/plugins/storefront/) and display the HTML or use the resulting markup from a single page application that interprets the API responses. A native mobile application can strip out unnecessary blocks and only display texts and images as view components. A smart speaker simply reads out the content of elements with the `voice` type.

By default, Shopware provides the server-side rendered Storefront as a default presentation channel, but [Composable Frontends](./../../../../frontends/) also supports CMS pages. Using the CMS through the API, you will have full flexibility in how to display your content.

INFO

All this comes at a price: The admin preview of your content is only as representative of your content presentation as your presentation channel resembles it. **A major implication for headless frontends.** For that reason, Shopware PWA has functionality built into the plugin, allowing you to preview content pages in the PWA.

---

## Cookie Consent Management

**Source:** https://developer.shopware.com/docs/concepts/commerce/content/cookie-consent-management.html

# Cookie Consent Management [​](#cookie-consent-management)

## Overview [​](#overview)

Shopware provides a cookie consent management system with features designed to support GDPR compliance. The system allows shop administrators and developers to manage cookies transparently and give customers control over their data privacy. It handles cookie categorization, user consent tracking, and automatic re-consent when cookie configurations change.

WARNING

While Shopware provides tools and features to help with GDPR compliance, shop owners are ultimately responsible for ensuring their shop complies with GDPR and other applicable data protection regulations. This includes proper cookie configuration, privacy policies, and legal review of all data processing activities.

INFO

The cookie-hash and re-consent functionality is available starting with Shopware 6.7.3.0.

## How it works [​](#how-it-works)

The cookie consent system operates through several integrated components:

1. **Cookie Provider Service**: Collects all cookie definitions from core, plugins, and apps
2. **Store API Endpoint**: Exposes cookie configuration with a configuration hash
3. **Storefront Component**: Manages the cookie consent UI and user preferences
4. **Configuration Hash**: Tracks changes to trigger re-consent when needed

### Cookie Configuration Flow [​](#cookie-configuration-flow)

## Cookie Categories [​](#cookie-categories)

Cookies in Shopware are organized into four main categories according to GDPR requirements:

### Technically Required [​](#technically-required)

Cookies that are essential for the shop to function (`cookie.groupRequired`). These cookies cannot be disabled by users.

**Examples:**

* Session management
* Shopping cart
* Security tokens
* Language preferences

### Comfort Functions [​](#comfort-functions)

Cookies that enhance user experience but are not essential for basic functionality (`cookie.groupComfortFeatures`).

**Examples:**

* Video platform cookies (YouTube, Vimeo)
* Social media integrations
* Chat widgets
* Personalized content

### Marketing [​](#marketing)

Cookies used for marketing and advertising purposes, including tracking user behavior for personalized ads and remarketing (`cookie.groupMarketing`).

**Examples:**

* Marketing pixels (Facebook Pixel, Google Ads)
* Remarketing and advertising cookies
* Conversion tracking
* Affiliate tracking

### Statistics and Tracking [​](#statistics-and-tracking)

Cookies used for analytics and website optimization purposes (`cookie.groupStatistical`).

**Examples:**

* Google Analytics
* User interaction tracking (Hotjar, Crazy Egg)
* A/B testing
* User behavior analytics

## Configuration Hash Mechanism [​](#configuration-hash-mechanism)

The configuration hash is an important feature that helps support GDPR compliance by ensuring users are re-prompted when cookie handling changes.

### Mechanism Details [​](#mechanism-details)

1. **Hash Generation**: A hash is calculated from all cookie configurations (names, descriptions, expiration times)
2. **Hash Storage**: The hash is stored in the browser as `cookie-config-hash`
3. **Change Detection**: On each visit, the current hash is compared with the stored hash
4. **Re-Consent Trigger**: If hashes differ, all non-essential cookies are removed and consent is requested again

### When Hash Changes [​](#when-hash-changes)

The configuration hash changes when:

* New cookies are added by plugins/apps
* Existing cookies are modified or removed
* Cookie groups are restructured
* Cookie descriptions or settings change

This ensures users are always informed about changes to cookie handling, maintaining GDPR compliance.

## Cookie Groups vs Individual Cookies [​](#cookie-groups-vs-individual-cookies)

### Individual Cookies [​](#individual-cookies)

Single cookies that can be accepted or rejected independently.

**Use when:**

* Cookie serves a specific, standalone purpose
* No logical grouping with other cookies
* Maximum granular control needed

### Cookie Groups [​](#cookie-groups)

Multiple related cookies grouped together for easier management.

**Use when:**

* Multiple cookies serve the same purpose (e.g., video platform)
* Cookies are interdependent
* Simplified user interface is desired

**Example:** YouTube group containing multiple YouTube-related cookies

## Key Cookies Used by the System [​](#key-cookies-used-by-the-system)

The cookie consent system itself uses special cookies:

| Cookie | Purpose | Lifetime |
| --- | --- | --- |
| `cookie-preference` | Stores user's consent choices | 30 days |
| `cookie-config-hash` | Tracks configuration changes | 30 days |

### Protected Cookies [​](#protected-cookies)

Certain cookies are **never removed** by the consent system, even during re-consent:

* `session-*` - Session cookies required for shop functionality
* `timezone` - User's timezone preference

## Technical Implementation [​](#technical-implementation)

Cookie configurations are defined using structured objects for type safety:

* **`CookieEntry`** - Individual cookie definition
* **`CookieGroup`** - Group of related cookies

This provides better IDE support, type checking, and consistency across implementations.

## Store API Integration [​](#store-api-integration)

INFO

The Store API endpoint for cookie groups is available starting with Shopware 6.7.3.0.

The cookie consent system exposes its configuration through the Store API endpoint:

**Endpoint:** `GET /store-api/cookie/groups`

This endpoint enables headless implementations, custom frontends, and third-party integrations to retrieve cookie configuration and the configuration hash.

For full API documentation, see the [Store API - Fetch all cookie groups](https://shopware.stoplight.io/docs/store-api/f9c70be044a15-fetch-all-cookie-groups) reference.

## Extension Points [​](#extension-points)

The cookie consent system can be extended in multiple ways:

### For Plugins [​](#for-plugins)

Use an event listener to add custom cookies.

[Add cookie to manager](../../../guides/plugins/plugins/storefront/add-cookie-to-manager)

### For Apps [​](#for-apps)

Define cookies in your `manifest.xml` file.

[Add cookies to the consent manager](../../../guides/plugins/apps/storefront/cookies-with-apps)

### JavaScript Events [​](#javascript-events)

React to user consent changes in your custom JavaScript.

[Reacting to cookie consent changes](../../../guides/plugins/plugins/storefront/reacting-to-cookie-consent-changes)

## Best Practices [​](#best-practices)

### 1. Categorize Correctly [​](#_1-categorize-correctly)

Place cookies in the appropriate category:

* Only truly essential cookies should be "technically required" (`cookie.groupRequired`)
* User convenience features belong in "comfort functions" (`cookie.groupComfortFeatures`)
* Marketing and advertising cookies belong in "marketing" (`cookie.groupMarketing`)
* Analytics and optimization belong in "statistics and tracking" (`cookie.groupStatistical`)

### 2. Provide Clear Descriptions [​](#_2-provide-clear-descriptions)

Write clear, user-friendly cookie descriptions:

* Explain what the cookie does in simple terms
* Mention what data is collected
* State how long the cookie persists
* Link to privacy policy if relevant

### 3. Set Appropriate Expiration [​](#_3-set-appropriate-expiration)

Choose sensible expiration times:

* Session cookies for temporary data
* Days/weeks for user preferences
* Months/year for long-term settings
* Consider GDPR recommendations

### 4. Handle Consent Changes [​](#_4-handle-consent-changes)

Always check consent status before:

* Loading third-party scripts
* Setting marketing or advertising cookies
* Collecting analytics or statistics data
* Storing user behavior data

### 5. Test Re-Consent Flow [​](#_5-test-re-consent-flow)

When updating cookie configurations:

* Test that hash changes trigger re-consent
* Verify non-essential cookies are removed
* Check that protected cookies remain
* Ensure UI displays correctly

## Features Supporting GDPR Compliance [​](#features-supporting-gdpr-compliance)

Shopware's cookie consent system includes several features designed to help shop owners meet GDPR requirements:

* ✅ **Opt-in by default** - Users must actively consent (no pre-checked boxes)
* ✅ **Granular control** - Users can accept/reject individual categories
* ✅ **Re-consent on changes** - Automatic re-prompting when configuration changes
* ✅ **Clear information** - Transparent cookie descriptions and purposes
* ✅ **Easy withdrawal** - Users can change preferences at any time
* ✅ **Configuration tracking** - Hash mechanism ensures change detection
* ✅ **Documented lifecycle** - Full audit trail of cookie changes

INFO

These features provide technical support for GDPR compliance, but shop owners must also ensure they have proper legal documentation (privacy policy, terms of service), data processing agreements, and regular compliance audits. Consult with legal counsel to ensure full compliance with GDPR and other applicable regulations.

---

