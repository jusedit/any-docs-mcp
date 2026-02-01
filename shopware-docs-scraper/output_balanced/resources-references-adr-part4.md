# Resources References Adr Part4

*Scraped from Shopware Developer Documentation*

---

## [A11y] Offer HTML alternative to our pdf standard documents

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-12-19-offer-html-alternative-to-our-pdf-standard-document.html

# "[A11y] Offer HTML alternative to our pdf standard documents" [​](#a11y-offer-html-alternative-to-our-pdf-standard-documents)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-12-19-offer-html-alternative-to-our-pdf-standard-document.md)

## Context [​](#context)

To comply with Web Content Accessibility Guidelines (WCAG), we aim to make Shopware 6's document solution accessible (A11y-compliant). This ensures that our solution remains usable while meeting legal requirements and making documents accessible to customers with disabilities.

Currently, our PDF generation library, DomPDF, does not meet accessibility standards, posing a significant challenge.

## Decision [​](#decision)

We have decided to make HTML documents available in addition to PDF documents, as these are more accessible.

* **Better for Accessibility**: HTML is naturally organized, making it easier for accessibility tools to read and present content to people with disabilities.
* **Lack of Support**: As our current PDFs lack support for accessibility. Few tools, especially in PHP, can create accessible tagged PDFs, making it difficult to maintain PDF accessibility.
* **Industry Trends**: Many organizations are already moving from PDFs to HTML for accessibility. For example, government websites have been required to meet accessibility standards since the early 2000s. Most of them now use HTML for most of their content because it meets these standards better.

Providing HTML documents aligns with these trends and ensures we are using best practices for accessibility.

### Affected Areas [​](#affected-areas)

We will integrate HTML A11y document support in the following areas:

1. **Document Type Support**:
   * Support includes all document types Shopware provides by default, `invoice`, `delivery note`, `credit note`, and `cancellation invoice`. Extensions must adapt themselves.
2. **Administration**:
   * **Order Detail Page**: Option to download HTML alongside PDF for each document type.
   * **Document Settings**: Toggle to generate HTML documents.
3. **Storefront**:
   * **Order History**: Customers can access HTML and PDF versions of documents.
4. **Flow Builder**:
   * This setup requires no additional special actions, and merchants can customize file generation for "Generate documents" in the `Document Settings`
5. **Email Delivery**:
   * Enhance the original email by including a link to the HTML document. Customers will need to log in to access the document, and additional guidance will be provided.
   * We can’t attach the HTML file directly due to issues with "virus scanners", as many email providers do not allow HTML file attachments. Instead we will provide a link inside the Email.
   * A lot of the major platforms (Microsoft, Google, Amazon, etc.) will also email a summary with a link to the customer account for things like Azure/Google Cloud/etc.

### Core concept [​](#core-concept)

#### Document Template [​](#document-template)

1. **Adjust Twig Template for A11y**:

   * Modify the `html.twig` templates to support accessibility (A11y) by adding elements like `tabindex` and appropriate CSS styles.

   `src/Core/Framework/Resources/views/documents/invoice.html.twig`:

   twig

   ```shiki
   {% block document_headline %}
       <h1 class="headline" tabindex="0">
           <!-- Headline content -->
       </h1>
   {% endblock %}
   ```

   `src/Core/Framework/Resources/views/documents/style_base_html.css.twig`:

   twig

   ```shiki
   {% block document_style_html %}
       body {
           max-width: 1200px;
           margin: auto;
           font-size: 14px;
           line-height: 18px;
       }
       ...
   {% endblock %}
   ```
2. **Metadata and Security**:

   * The generation date of the HTML will be "fingerprinted" by adding a metadata header. This allows users to track the creation date of the document.
   * Implement a Content-Security-Policy meta-tag to minimize XSS attack risks, such as disallowing JavaScript and Restricts  to the same domain, protecting against base URL manipulation.

   Added new Twig block for metadata`src/Core/Framework/Resources/views/documents/base.html.twig`:

   twig

   ```shiki
   {% block document_head_meta_protection %}
       <meta http-equiv="Content-Security-Policy" content="script-src 'none'; base-uri 'self';">
       <meta name="date" content="{{ 'now'|date('c') }}">
   {% endblock %}
   ```

#### Core [​](#core)

1. **Abstract Class for Multi-Format Rendering**

   * We will introduce an abstract class, `src/Core/Checkout/Document/Service/AbstractDocumentTypeRenderer`, to support rendering multiple document types, including `PDF` and `HTML`.

   php

   ```shiki
   abstract class AbstractDocumentTypeRenderer
   {
       abstract public function render(RenderedDocument $document): string;
   }

   class HtmlRenderer extends AbstractDocumentTypeRenderer
   {
     public function render(RenderedDocument $document): string
     {
         $content = $this->documentTemplateRenderer->render(
             ...$options
         );
         
         $document->setContentType(self::FILE_CONTENT_TYPE);
         $document->setFileExtension(self::FILE_EXTENSION);
         $document->setContent($content);
         
         return $content;
     }
   }

   class PdfRenderer extends AbstractDocumentTypeRenderer {}
   ```
2. **Service Registration**:

   * We need to use the service tag `document_type.renderer` for the `Shopware\Core\Checkout\Document\Service\DocumentFileRendererRegistry` to recognize this service. This is essential for the proper registration and functioning of the `HtmlRenderer`.

   xml

   ```shiki
   <service id="...\HtmlRenderer">
       <tag name="document_type.renderer" key="html"/>
   </service>
   ```
3. **Database Schema**:

   * We will add a new column `document_a11y_media_file_id` to the `document` table to store the media file ID for HTML A11y documents.

   sql

   ```shiki
   ALTER TABLE `document`
   ADD COLUMN `document_a11y_media_file_id` BINARY(16);
   ```

   * The column is intended to link each document entry with its corresponding A11y media file `src/Core/Checkout/Document/DocumentDefinition.php`

   php

   ```shiki
   (new FkField('document_a11y_media_file_id', 'documentA11yMediaFileId', MediaDefinition::class))
       ->addFlags(new ApiAware());
   ```

### Email Migration [​](#email-migration)

* For templates that have been customized, new content must be migrated same as code below:

  `src/Core/Migration/Fixtures/mails/invoice_mail/de-plain.html.twig`

  twig

  ```shiki
  {% if a11yDocuments %}
  For better accessibility, we also provide an HTML version of the documents here:

  {% for a11y in a11yDocuments %}
  {% set documentLink = rawUrl(
      'frontend.account.order.single.document.a11y',
      {
          documentId: a11y.documentId,
          deepLinkCode: a11y.deepLinkCode,
          fileType: a11y.fileExtension,
      },
      salesChannel.domains|first.url
  ) %}

      - {{ documentLink }}
  {% endfor %}
  {% endif %}
  ```

## Consequences [​](#consequences)

With this implementation, Shopware 6 will support HTML A11y documents alongside PDFs for standard document types. This change will have the following consequences:

* **Renderer Updates**: Document renderers need changes to handle HTML output, using the `AbstractDocumentTypeRenderer` [here](#core).
* **Email Integration**: For templates that have been customized, new content must be migrated as detailed in [here](#email-migration).
* **Improved Accessibility**: HTML documents make content easier to access for users with disabilities, aligning with WCAG standards.
* **Customizability**: Options in Document settings to enable or disable HTML documents should be added, giving merchants choice in document format.

---

## Remove the asterisk next to every price and replace it with actual text

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-01-01-remove-asterisk-next-to-every-price.html

# Remove the asterisk next to every price and replace it with actual text [​](#remove-the-asterisk-next-to-every-price-and-replace-it-with-actual-text)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-01-01-remove-asterisk-next-to-every-price.md)

## Context [​](#context)

Currently, all product prices that are displayed in the default Storefront have an asterisk `*` next to them, for example: `€ 50,00 *` This asterisk refers to the tax and shipping costs information in the page footer `* All prices incl. VAT plus shipping costs and possible delivery charges, if not stated otherwise.`

Using the asterisk `*` next to every price has several downsides that we want to address:

### Footer text not always in viewport [​](#footer-text-not-always-in-viewport)

When adding products to the shopping cart from within the listing the text might never be recognized.

### Redundant and confusing information [​](#redundant-and-confusing-information)

In some areas, the asterisk `*` referring to the footer text is more confusing than helpful. For example:

* On the product detail page the "tax and shipping information" link is already displayed right underneath the price.
* Inside the summary of the shopping cart the "tax and shipping information" is already part of the summary itself.
* When a form is shown on the same page, the asterisks `*` of the required fields are conflicting with the asterisks `*` of the prices.
* In general the asterisk `*` might give the impression that the shown price is not the actual price and might change later.

### Accessibility issues [​](#accessibility-issues)

The asterisk `*` is only plain text at the moment and has no actual relationship to its corresponding footer info text. A screen reader will always read "50 euros star" without further context. For a screen reader user, the asterisk is not accessible.

## Decision [​](#decision)

The asterisk `*` next to every price will be removed because of the reasons mentioned above. In most areas of the Storefront, the information that the asterisk `*` refers to is already given, and it is therefore redundant. In areas where the asterisk `*` was actually needed, it will be replaced by the actual text "Prices incl. VAT plus shipping costs" instead to resolve the accessibility issues.

### Affected areas [​](#affected-areas)

| Area | Explanation |
| --- | --- |
| Shopping cart and order line items | Asterisk removed. Info is already shown in the cart summary. |
| Shopping cart summary | Asterisk removed. Info is already part of the cart summary itself. (shipping, taxes) |
| Header cart widget | Asterisk removed. Info is not needed because no product can be added to the cart here. |
| Header search suggest box | Info is not needed because no product can be added to the cart here. |
| Product-box (listing, product slider etc.) | Info is displayed as text instead when setting `core.listing.allowBuyInListing` is enabled. |
| Buy-widget on product detail page | Info is already shown on the product detail page underneath the price. |

The changes can be activated by using the `ACCESSIBILITY_TWEAKS` feature flag and will be the default in the upcoming major version `v6.7.0`.

See `2025-01-16-remove-the-asterisk-next-to-every-price.md` for the technical changelog.

## Consequences [​](#consequences)

* With the next major `v6.7.0` or active `ACCESSIBILITY_TWEAKS` the asterisk `*` next to every price will be removed.
* Product boxes that allow an "Add to cart" action from within the product listing will display the "Prices incl. VAT plus shipping costs" information as text instead. Only displayed when setting `core.listing.allowBuyInListing` is enabled.

---

## Make Rule classes internal

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-01-29-make-rule-classes-internal.html

# Make Rule classes internal [​](#make-rule-classes-internal)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-01-29-make-rule-classes-internal.md)

## Context [​](#context)

The existing rule system is flexible but complex, making it difficult to evolve and maintain. Allowing unrestricted extensions of rule classes slows down improvements and increases the complexity of the system.

See RFC: <https://github.com/shopware/shopware/discussions/5785>

## Decision [​](#decision)

We will mark existing rule classes as internal, limiting direct usage by third parties. Developers should create new rule classes instead of modifying existing ones.

Nearly all rule classes will be marked as internal, with a few exceptions:

```shiki
LineItemOfTypeRule
LineItemProductStatesRule
PromotionCodeOfTypeRule
ZipCodeRule
BillingZipCodeRule
ShippingZipCodeRule
```

These classes will remain public for now, because they rely on configuration which is reasonably expected to be extended by third-party developers.

## Consequences [​](#consequences)

* Faster evolution of the rule system
* Clearer extension mechanisms for developers
* Potential migration efforts for third-party developers currently extending rule classes
* Internal rule implementations may evolve

---

## Move flow execution after business process

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-01-31-move-flow-execution-after-business-process.html

# Move flow execution after business process [​](#move-flow-execution-after-business-process)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-01-31-move-flow-execution-after-business-process.md)

## Context [​](#context)

Currently, flows are executed during the business process. A business process is any event that is triggered by the user, like a checkout or a product update. Flows are used to react to these events and execute user defined actions.

There are several downsides to this approach. The most straightforward is the possibility of a fatal error during the execution of any flow. This will inevitably cancel the in progress business process. While there are remedies in place to avoid any trivial errors in flow execution disrupting the business process, certain errors can not be avoided.

Further, even if all flows execute without error, they noticeably impact business process performance. Flows are often employed to, for example, send mails, an expensive operation that is not necessary to complete the business process.

In addition to these concrete disadvantages, there are also some more abstract ones. For one, currently flows are executed directly from a decorator of Symfony's `EventDispatcher`, leading to cumbersome debugging and bloated stack traces. This would be improved if flows are executed by a dedicated event listener. Additionally moving flows to their own execution environment would not only simplify debugging, but also potentially make expanding their capabilities easier.

> *The following is all experimental and only takes effect if the associated feature flag `FLOW_EXECUTION_AFTER_BUSINESS_PROCESS` is enabled*

## Decision [​](#decision)

We will move the flow execution after the business process. As outlined above we believe that this will simplify the development around flows, while also improving their performance and safeguarding the main execution environment.

To ensure that flows are executed as close to the business process that triggered them as possible, we will 'queue' the flow execution. This means that flows will be executed after the business process has finished. Flows are stored in memory and executed as soon as the execution environment signals, that it has finished a unit of work. The associated events are as follows:

1. After a controller action has been executed (Web) => `KernelEvents::TERMINATE`
2. After a queued message has been processed (Queue) => `WorkerMessageHandledEvent`
3. After a command has been executed (CLI) => `ConsoleEvents::TERMINATE`

Another option would be to handle flow executions as queue messages. This would entirely remove flow executions from the runtime of the business process. While this would be a simpler solution, it would both make debugging more complex and introduce an unpredictable delay between the business process and the flow execution. While this delay could be mitigated by using a high priority queue, it could not reliably be kept under a certain threshold. To entirely avoid this delay, we decided that the flow execution should be handled as close to the business process as possible.

## Consequences [​](#consequences)

1. Flows can no longer fail the business process.
2. The interface for registering flows will not change.
3. Any plugins that rely on flows being executed during the business process will have to be updated.
4. Total execution time is not expected to increase significantly.
5. Business process performance is expected to improve.

---

## Deprecate Iterator.helper in Storefront JS

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-02-06-deprecate-iterator-iterate.html

# Deprecate Iterator.helper in Storefront JS [​](#deprecate-iterator-helper-in-storefront-js)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-02-06-deprecate-iterator-iterate.md)

## Context [​](#context)

The Storefront JavaScript currently offers a helper class `src/helper/iterator.helper.js` that can iterate over different objects like Maps, FormData, plain arrays etc. Using this approach has several downsides we want to address.

* It creates an unnecessary abstraction over the native alternative. Very often the `Iterator.iterate()` directly uses js plain `forEach` loop without any additional logic. Using the abstraction is actually creating more complexity.
* It prevents the developer from using the appropriate loop for the given data type and instead passes it to an iterator that does it with arbitrary data types.
* The iterator is a special shopware syntax that needs to be understood and documented. It is way easier to use web standards that everyone knows and that is also officially documented already.
* The usage throughout the codebase is inconsistent and the iterator helper is used alongside the native loops which can create confusion.
* It creates the impression that the data that is being iterated is some special custom object that needs a special iterator helper. In reality, it is a simple `NodeList` in 90% of the time.
* It creates an additional dependency/import in every file that is using it.

## Decision [​](#decision)

For all the above reasons we have decided to deprecate `src/helper/iterator.helper.js`, stop using it, and use native alternatives instead. We want to have a more lean and simple Storefront JavaScript that needs less special things to learn and understand.

## Consequences [​](#consequences)

* The `src/helper/iterator.helper.js` is deprecated for v6.8.0.
* The usages of `Iterator.iterate()` are replaced with native alternatives.
* See `2025-01-28-use-native-iteration-instead-of-iterator-helper.md` for the changelog and upgrade documentation.

---

## Context Gateway

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-04-01-context-gateway.html

# Context Gateway [​](#context-gateway)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-04-01-context-gateway.md)

# ADR: Context Gateway Feature [​](#adr-context-gateway-feature)

## Context [​](#context)

Previously, we introduced the `CheckoutGateway` to allow app servers to influence the checkout process based on the current cart and sales channel context.  
 This was a significant step toward enabling dynamic, app-driven decision-making during checkout.

However, this approach does not support modifying the storefront experience **outside** of the checkout flow.  
 There is a growing need to allow app servers to influence the **sales channel context** — e.g. customer data, language, and currency — based on external logic or user-specific criteria.

In particular, some use cases require **context manipulation before a cart or checkout process begins**.  
 To address this, we propose the introduction of a dedicated `ContextGateway`, which provides a secure and structured communication channel between the storefront and the app server.

The gateway is initiated from the storefront client and allows apps to request context changes based on external decision logic.

### Example Use Cases [​](#example-use-cases)

* Registering customers with custom or prefilled data (including guest and full customer registration)
* Logging in existing customers
* Switching the current language or currency
* Updating the active customer address

## Decision [​](#decision)

### AppContextGateway [​](#appcontextgateway)

To encapsulate the logic for context-driven decisions, a new `AppContextGateway` will be introduced.

It receives a `ContextGatewayPayloadStruct`, which includes:

* The current `SalesChannelContext`
* The current `Cart`
* A `RequestDataBag` containing all custom data provided by the client

The gateway will return a `ContextTokenResponse`, which includes the updated token of the `SalesChannelContext` after executing all applicable commands.

Example implementation:

php

```shiki
<?php declare(strict_types=1);

class AppCheckoutGateway
{
    public function process(ContextGatewayPayloadStruct $payload): ContextTokenResponse;
}
```

#### Store-API [​](#store-api)

A new store API route, `ContextGatewayRoute` '/store-api/context/gateway', will be introduced. This route will call the `AppContextGateway` implementation and respond accordingly.

Example implementation:

php

```shiki
<?php declare(strict_types=1);

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
class ContextGatewayRoute extends AbstractContextGatewayRoute
{
    public function __construct(
        private readonly AppContextGateway $contextGateway,
    ) {
    }

    public function getDecorated(): AbstractContextGatewayRoute
    {
        throw new DecorationPatternException(self::class);
    }

    #[Route(path: '/store-api/context/gateway', name: 'store-api.context.gateway', methods: ['GET', 'POST'])]
    public function load(Request $request, Cart $cart, SalesChannelContext $context): ContextTokenResponse
    {
        $data = new RequestDataBag($request->request->all());

        return $this->contextGateway->process(new ContextGatewayPayloadStruct($cart, $context, $data));
    }
}
```

#### Storefront [​](#storefront)

A new `ContextGatewayController` for the Storefront will be introduced. This controller will be the entry point for the Storefront client to interact with the `ContextGatewayRoute`.

Example implementation:

php

```shiki
<?php declare(strict_types=1);

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ContextGatewayController extends StorefrontController
{
    public function __construct(
        private readonly AbstractContextGatewayRoute $contextGatewayRoute,
        private readonly CartService $cartService,
    ) {
    }

    #[Route('/gateway/context', name: 'frontend.gateway.context', defaults: ['XmlHttpRequest' => true], methods: ['GET', 'POST'])]
    public function gateway(Request $request, SalesChannelContext $context): Response
    {
        $cart = $this->cartService->getCart($context->getToken(), $context);

        try {
            $response = $this->contextGatewayRoute->load($request, $cart, $context);
        } catch (\Throwable $e) {
            $this->addFlash(self::DANGER, $e->getMessage());
            return new JsonResponse(status: Response::HTTP_BAD_REQUEST);
        }

        return $response;
    }
}
```

#### Storefront SDK [​](#storefront-sdk)

Even though the client is free to initiate the context workflow in any manner, as long as an `XMLHttpRequest` is made to the `/store-api/gateway/context` endpoint, we propose the introduction of a helper class, `ContextGatewayClient`, within the Storefront SDK.

This client provides a convenient and consistent interface for apps to interact with the context gateway, reducing the need for manual request setup and improving developer experience.

This client will work similarly to the existing `AppClient`, but is specifically designed for initiating context gateway flows from the storefront.

The `ContextGatewayClient` will be instantiated with the app name and expose a `request()` method to trigger the `/store-api/gateway/context` endpoint, optionally including custom parameters.

Example implementation:

typescript

```shiki
export default class ContextGatewayClientService {
    private readonly name: string;

    constructor(name: string) {
        this.name = name;
    }
    
    public async request(options: Record<string, any> = {}, handleRedirect: boolean = true): Promise<Response> {
        const body = { appName: this.name, ...options };
        
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(body)
        }
        
        const response = await fetch(window.router['frontend.gateway.context'], requestOptions);
        const result = await response.json();

        if (result.redirectUrl) {
            window.location.href = result.redirectUrl;
        }
        
        window.location.reload();
    }
}
```

#### App Manifest [​](#app-manifest)

To enable support for the `ContextGateway`, apps must declare a new endpoint in their `manifest.xml` file. This is done by defining a `context` sub-key under the existing `<gateways>` section. The provided URL will be called by the `AppContextGateway` when the context flow is initiated from the storefront.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <!-- Optional: existing checkout gateway -->
        <!-- <checkout>https://example.com/checkout/gateway</checkout> -->

        <!-- Required for context gateway -->
        <context>https://example.com/context/gateway</context>
    </gateways>
</manifest>
```

### Command Structure [​](#command-structure)

The `ContextGateway` will implement a command pattern inspired by the established structure used in the `CheckoutGateway`.

It will support a predefined set of commands that can be returned by the app server in the response.

Commands are executed **in the order they are provided**, with the following exception:

* The `context_register-customer` and `context_login-customer` commands are executed **first**, as they establish a new or updated context.
* All remaining commands will be executed **sequentially**, based on the order in the response, and operate on the resulting context.

This structure ensures that commands depending on user identity, language, or currency changes always act on the correct state.

#### Context Gateway App Payload [​](#context-gateway-app-payload)

The app server receives a structured payload when invoked through the `AppContextGateway`.

The payload contains:

* The app source
* The current `SalesChannelContext`
* The current `Cart`
* Any **custom data** sent from the client (e.g., app name, user metadata, intent flags)

This payload enables app servers to make contextual decisions based on both the current session and additional input from the storefront. Example payload sent to app-server:

json5

```shiki
{
    "source": {
        // information about the app source (version, shopId, etc.)
    },
    "salesChannelContext": SalesChannelContextObject,
    "cart": CartObject,
    "custom": {
        "anyCustomKey": "anyCustomValue"
        // "anyOtherCustomDataKey": "anyOtherCustomDataValue"
    },
    
}
```

Note that custom data sent by the client will be sent as a key-value pair under `custom` to the app-server.

#### Context Gateway App Response [​](#context-gateway-app-response)

Example response from app-server:

json

```shiki
[
  {
    "command": "context_register-customer",
    "payload": RegisterCustomerData,
  },
  {
    "command": "context_switch-language",
    "payload": {
        "iso": "de-DE"
    }
  },
  {
    "command": "context_switch-currency",
    "payload": {
        "iso": "USD"
    }
  }
]
```

Shopware will apply validation rules to ensure consistency and prevent conflicting command execution.

* The response must not contain more than **one `register-customer` or `login-customer` command**.
* All other command types must appear **at most once** in the response.

These constraints help prevent ambiguous or conflicting state changes during context manipulation.

### Command Structure [​](#command-structure-1)

Each command in the context gateway is composed of two key elements:

* **Command class**  
   A class extending `AbstractContextGatewayCommand`.  
   This class holds the command’s payload and is uniquely identified by its command name.
* **Command handler class**  
   A class extending `AbstractContextGatewayCommandHandler`.  
   It contains the logic to execute supported commands and may handle multiple command types by implementing the `getSupportedCommands()` method.

This separation of data and execution logic ensures modularity and extensibility of the command processing system.

Example command class:

php

```shiki
<?php declare(strict_types=1);

class ChangeCurrencyCommand extends AbstractContextGatewayCommand
{
    public const COMMAND_KEY = 'context_change-currency';

    public function __construct(
        public readonly string $iso,
    ) {
    }

    public static function getDefaultKeyName(): string
    {
        return self::COMMAND_KEY;
    }
}
```

Example command handler class:

php

```shiki
<?php declare(strict_types=1);

class ChangeCurrencyCommandHandler extends AbstractContextGatewayCommandHandler
{
    public function __construct(
        private readonly EntityRepository $currencyRepository
    ) {
    }

    /**
     * @param ChangeCurrencyCommand $command
     */
    public function handle(AbstractContextGatewayCommand $command, SalesChannelContext $context, array &$parameters): void
    {
        $criteria = new Criteria();
        $criteria->addFilter(new EqualsFilter('isoCode', $command->iso));

        $currencyId = $this->currencyRepository->searchIds($criteria, $context->getContext())->firstId();

        if ($currencyId === null) {
            return;
        }

        // $parameters will be used by ContextSwitchRoute to update the context
        $parameters['currencyId'] = $currencyId;
    }

    public static function supportedCommands(): array
    {
        return [ChangeCurrencyCommand::class];
    }
```

#### Command Registry [​](#command-registry)

Command handlers will be registered in the `ContextGatewayCommandRegistry` using a registry pattern.

All implementations of `AbstractContextGatewayCommandHandler` must be tagged with the `shopware.context.gateway.command` service tag. This ensures they are automatically discovered and made available to the app system for command execution.

#### Event [​](#event)

A new event, `ContextGatewayCommandsCollectedEvent`, will be introduced. This event is dispatched after the `AppContextGateway` collects all command responses from registered app servers, but before the commands are executed.

It allows plugins to inspect, modify, or append commands based on the full context and payload provided to the app servers.

## Consequences [​](#consequences)

### App PHP SDK [​](#app-php-sdk)

The `app-php-sdk` will be extended to support the new gateway and its data contract.

Enhancements include:

* Context gateway requests can be deserialized into a `ContextGatewayAction` object.
* Responses can easily be created with a `ContextGatewayResponse` object.
* Each supported context command will have a dedicated class, allowing strongly-typed manipulation and validation of its payload.

### App Bundle (Symfony) [​](#app-bundle-symfony)

The App Bundle will be updated to support the new gateway endpoint automatically.

Incoming context gateway requests and outgoing responses will be automatically resolved to the appropriate DTOs (`ContextGatewayAction`, `ContextGatewayResponse`), making it seamless for app developers to implement handlers using standard Symfony controllers.

## Security Considerations [​](#security-considerations)

The `ContextGateway` introduces new responsibilities and associated risks due to its ability to manipulate the `SalesChannelContext`.

Potential concerns include:

* **Customer impersonation**: App servers have the ability to log in existing customers, even without knowing their passwords.
* **Trust boundary risks**: If an app server is compromised or malicious, it could exploit the gateway to impersonate users, access sensitive customer data, or perform unauthorized actions. However, this issue has always existed with the plugin system.

Particularly, allowing login based solely on an email address — without verifying credentials — poses a significant security risk.

### Mitigation [​](#mitigation)

* Gateway command execution must enforce strict validation, logging, and safeguards (e.g., rate limiting).
* The ability to log in a customer should be gated by additional checks or explicit trust settings per app (a proposal could be custom ACL permissions per app and action).
* All actions performed via the context gateway should be auditable and traceable for monitoring and incident response.

---

## Implement measurement system

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-05-12-implement-measurement-system.html

# Implement measurement system [​](#implement-measurement-system)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-05-12-implement-measurement-system.md)

## Context [​](#context)

We want to provide merchants with the ability to define the measurement system for their products—e.g., metric or imperial.

This configuration should be available per sales channel domain or per product.

We also need to offer a convenient way to display or persist preferred units in the storefront, administration, and APIs.

## Decision [​](#decision)

We will introduce two measurement systems: Metric and Imperial. The default will be Metric, with millimeters for length and kilograms for weight, matching the current system.

When users or store API consumers fetch products, the system will resolve the configured measurement system and units based on the sales channel domain. These configured units will be used to display product measurements in the storefront or in store API responses.

Consumers can override the returned measurement units by setting preferred units in the request headers.

## Technical Details [​](#technical-details)

### Resolving Sales Channel Domain Measurement System Configuration [​](#resolving-sales-channel-domain-measurement-system-configuration)

We will expose a `MeasurementUnits` DTO in the `SalesChannelContext` (`SalesChannelContext.measurementSystem`), allowing quick look up of current configured product measurements of given context.

php

```shiki
class MeasurementUnits extends Struct
{
    public function __construct(public readonly string $system, public array $units)
    {
    }

    public function addMeasurementType(string $type, string $unit): void
    {
        $this->units[$type] = $unit;
    }

    public function setUnit(string $type, string $unit): void
    {
        if (\array_key_exists($type, $this->units)) {
            throw MeasurementSystemException::unsupportedMeasurementUnit($unit, array_keys($this->units));
        }

        $this->units[$type] = $unit;
    }
    
    public function getUnit(string $type): string
    {
        if (!\array_key_exists($type, $this->units)) {
            throw MeasurementSystemException::unsupportedMeasurementType($type, array_keys($this->units));
        }

        return $this->units[$type];
    }
}

// By default, only weight and length units are supported
$measurementSystem = new MeasurementUnits('metric', [
    'lengthUnit' => 'mm',
    'weightUnit' => 'kg',
]);

$salesChannelContext->setMeasurementSystem($measurementSystem);
```

The `MeasurementUnits` will be initialized in `\Shopware\Core\System\SalesChannel\Context\SalesChannelContextFactory::create` based on current sales channel domain

The measurement configuration will be visible in `/store-api/context`:

json

```shiki
{
  "token": "<context_token>",
  ...,
  "measurementUnits": {
    "system": "metric",
    "units": {
      "length": "mm",
      "weight": "kg",
      // added by externals
      "volume": "m3"
    }
  },
  "apiAlias": "sales_channel_context"
}
```

### Runtime Field for Product Measurement Units [​](#runtime-field-for-product-measurement-units)

Measurement units will be dynamically converted based on the configured measurement system and units for the sales channel domain. If no domain is specified, it will fall back to the default sales channel units.

The `measurementUnits` is a runtime-calculated field based on the product’s measurement values and selected units.

php

```shiki
namespace Shopware\Core\Content\Product\Subscriber;

class ProductSubscriber implements EventSubscriberInterface 
{
    public function salesChannelLoaded(SalesChannelEntityLoadedEvent $event): void
    {        
        foreach ($event->getEntities() as $product) {
            $product->assign([
                'measurementUnits' => $this->productMeasurementBuilder->build($product, $event->getSalesChannelContext()),
            ]);
        }
    }
}
```

The `ProductPackageMeasurementBuilder` will convert product's default packaging measurements to the configured measurement system and units.

php

```shiki
/**
 * @internal
 */
class ProductPackageMeasurementBuilder
{
    public function __construct(
        private readonly MeasurementUnitConverter $unitConverter
    ) {}
    
    public function build(SalesChannelProductEntity $product, SalesChannelContext $context): MeasurementUnits
    {
        $measurementUnit = new MeasurementUnits();
        
        $lengthUnit = $context->getMeasurementSystem()->getUnit('length');
        $weightUnit = $context->getMeasurementSystem()->getUnit('weight');
        
        $measurementUnit->add('width', $this->unitConverter->convert($product->getWidth(), 'mm', $lengthUnit));
        $measurementUnit->add('height', $this->unitConverter->convert($product->getHeight(), 'mm', $lengthUnit));
        $measurementUnit->add('length', $this->unitConverter->convert($product->getLength(), 'mm', $lengthUnit));
        $measurementUnit->add('weight', $this->unitConverter->convert($product->getWeight(), 'kg', $weightUnit));
                
        return $measurementUnit;
    }
}
```

Internal or external services can listen to `SalesChannelEntityLoadedEvent` to inject additional fields into the product’s measurement units.

Example product output:

json

```shiki
{
  ...other product fields,
  "width": 150,
  "length": 120,
  "height": 200,
  "weight": 1.2,
  "measurementUnits": {
    "width": {
      "value": 1.5,
      "unit": "m"
    },
    "length": {
      "value": 1.2,
      "unit": "m"
    },
    "height": {
      "value": 2.0,
      "unit": "m"
    },
    "weight": {
      "value": 1.2,
      "unit": "kg"
    },
    // added by externals
    "volume": {
      "value": 1.2,
      "unit": "m3"
    },
    "customFields.fooField": {
      "value": 1.2,
      "unit": "m"
    }
  }
}
```

We will also introduce a `MeasurementUnitConverter` to handle unit conversion.

php

```shiki
abstract class AbstractMeasurementUnitConverter
{
    public function convert(float $value, string $fromUnit = 'mm', string $toUnit = 'in', float $precision = 3): ConvertedUnit;
}
```

### Overriding Product measurement Units via API Headers [​](#overriding-product-measurement-units-via-api-headers)

By default, product measurement units are stored in the metric system. Two new request headers allow overriding the default units, useful for external services:

* `sw-measurement-length-unit`: overrides the default length unit
* `sw-measurement-weight-unit`: overrides the default weight unit

When reading product measurements, we check these headers and convert values accordingly. If not provided, we fall back to the configured system.

php

```shiki
class ProductSubscriber implements EventSubscriberInterface 
{
    public function productLoaded(SalesChannelEntityLoadedEvent $event): void
    {        
        $lengthUnit = $request->headers->get('sw-measurement-length-unit', 'mm');
        $weightUnit = $request->headers->get('sw-measurement-weight-unit', 'kg');

        foreach ($event->getEntities() as $product) {
            $product->setWidth($this->unitConverter->convert($product->getWidth(), 'mm', $lengthUnit));
            $product->setHeight($this->unitConverter->convert($product->getHeight(), 'mm', $lengthUnit));
            $product->setLength($this->unitConverter->convert($product->getLength(), 'mm', $lengthUnit));
            $product->setWeight($this->unitConverter->convert($product->getWeight(), 'kg', $weightUnit));
        }
    }
}
```

The same logic applied for searching products in the API.

When saving product measurements, values will be converted back to the default (metric) units before persisting to the database.

This enables API consumers to use their preferred units without worrying about converting values manually.

**Note**: Converted values are only available in API requests and responses. The stored product measurements will always use the metric system to avoid inconsistencies.

### Storefront Integration [​](#storefront-integration)

Storefront templates currently use fixed units (mm, kg):

twig

```shiki
{{ product.width }} mm
{{ product.weight }} kg
```

With the new system, the value and unit will be dynamically resolved based on the configured measurement system and units.

twig

```shiki
{{ product.measurements.type('width').value }} {{ product.measurements.type('width').unit }}
{{ product.measurements.type('weight').value }} {{ product.measurements.type('weight').unit }}
```

#### New Twig Filters for On-the-Fly Conversion [​](#new-twig-filters-for-on-the-fly-conversion)

We provide new Twig filters for on-the-fly unit conversion.

twig

```shiki
{# Convert to domain-configured units (e.g., m and g) #}
{{ 1500|sw_convert_unit(from: 'mm') }}  {# Output: 1.5m #}
{{ 1.2|sw_convert_unit(from: 'kg') }}   {# Output: 1200g #}

{# Convert to specific units #}
{{ 100|sw_convert_unit(from: 'kg', to: 'lb') }}  {# Output: 220.462 #}
{# Convert to with specific rounding (default as 2) #}
{{ 100|sw_convert_unit(from: 'kg', to: 'lb', precision: 1) }}  {# Output: 220.5 #}
```

## Consequences [​](#consequences)

* Provides flexibility for merchants and API consumers to work with preferred units, enhancing usability and customization.
* Increases complexity due to runtime fields, conversion logic, and additional request headers.
* Needs to be careful not to introduce performance overhead for large datasets or high-traffic APIs.
* API consumers might need to adapt their implementation to leverage the new system.

### Backward Compatibility [​](#backward-compatibility)

* No existing functionality will break, as the default units (mm and kg) remain unchanged.

---

## Integrating the language pack into platform

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-06-03-integrating-the-language-pack-into-platform.html

# Integrating the language pack into platform [​](#integrating-the-language-pack-into-platform)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-06-03-integrating-the-language-pack-into-platform.md)

## Context [​](#context)

The Shopware Language Pack plugin enables us to distribute translations from Crowdin to Shopware installations. While this was a convenient solution in the past, when most of our repositories and workflows were kept private. This approach is unnecessarily convoluted and cumbersome for developers and users, because changes to any snippet require multiple steps:

1. Translations are updated in CrowdIn (by the shopware team and community)
2. Merging the changes from CrowdIn into `shopware/translations` (automated, requires manual review)
3. Merging the changes from `shopware/translations` into `shopware/SwagLanguagePack`, which primarily just distributes json files (automated)
4. Publishing Language Pack releases to the store (automated, may require manual input)
5. Updating Language Pack installation
   * OnPrem: Manually updating the plugin in a Shopware installation
   * Cloud: Updating the docker image dependency

This sequence also introduces overhead in maintenance and CI/CD.

### Background and Motivation [​](#background-and-motivation)

* The current setup was influenced by limitations of our previous GitLab-based workflow, where distribution via plugin was the most practical method. This workflow has been in place for ~6 years.
* Crowdin remains our single source of truth for all supported language snippets, and community members can contribute translations directly.
* `shopware/translations` serves as an intermediary data layer to decouple core Shopware repositories from Crowdin.
* The primary goal of this change is to reduce maintenance effort by replacing steps 3–5 with a single step, and removing `shopware/SwagLanguagePack` from the workflow entirely. The new step should be targeting `shopware/shopware` instead.

## Decision [​](#decision)

We will implement a new service in `shopware/shopware` (i.e. as part of the Shopware platform) to download translations right from the [GitHub Repository](https://github.com/shopware/translations/) and manage them without the need of any extension. Translations will be downloaded as JSON files (via admin user interaction or command execution) and stored on the local file system, just like existing platform snippet files. In addition, we will provide new `bin/console` commands in `shopware/shopware` to manage installed languages, for example when building an image for deployment. The initial set of commands will look like this:

bash

```shiki
$ php bin/console translation

Available commands:
    install [translation] [--all, --locales]
    activate [translation] [--all]
    deactivate [translation] [--all]
    uninstall [translation] [--all]
    list
```

## Consequences [​](#consequences)

* The Language Pack plugin will be maintained for Shopware versions < v6.8.0.
* Translations can be installed and updated on-demand, instead of waiting for platform/plugin release cycles.
* Translation versions will be mapped to platform version ranges.
* The general translations workflow remains the same. This has no impact on other extensions and their snippet files.
* For admin users the UX will improve: Available translations will now be listed directly in the administration and can be installed with a single click.

---

## Cache layer for navigation loader

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-08-19-cache-layer-for-navigation-loader.html

# Cache layer for navigation loader [​](#cache-layer-for-navigation-loader)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-08-19-cache-layer-for-navigation-loader.md)

## Context [​](#context)

We see in multiple performance analysis that the navigation loader can be a bottleneck for the performance of the storefront, especially with a huge number of categories in the first levels of the category tree. The navigation loader is responsible for loading the categories and their children, which are then used to render the navigation in the storefront. This process can be quite expensive, not just because of the query time on the DB, but also for hydrating the entities into PHP objects. The other part with a huge performance impact is the rendering performance on twig side for the many nested categories, however that is not part of this ADR.

The navigation loader is used in the storefront for every header and every listing page (when they use the sidebar navigation CMS element). However, the data that is loaded is always the same for the same sales channel, because we always show/load the category tree for the main navigation of the sales channel to the depth that is configured in the sales channel config.

Adding support for ESI for the header and footer addresses the same fundamental performance issue, however it does not solve the problem for the listing pages, where the sidebar navigation CMS element is used. Additionally, for ESI to be effective you would need a reverse proxy that supports ESI, and you need to disable compression your responses from your webserver, which could increase your infrastructure costs. So ESI is not a viable solution for every use case.

## Decision [​](#decision)

We will implement a cache layer for the navigation loader to improve the performance of the storefront. To not only safe the query time, but also the hydration time, we will store the categories as PHP serialized objects. That should be fine, because when the structure of the PHP objects changes, that means there is a new platform version, in which case the cache needs to be cleared anyway. Also in order to be most effective and not store too much data, we will only cache the category tree for the main navigation for every sales channel and up to the depths that is configured in the sales channel, because that info is loaded on every header and every listing page (when they use the sidebar navigation CMS element). We use the `CacheCompressor` to compress the serialized data before storing it in the cache, which should reduce the size of the cache entries significantly, however it adds some more processing time when reading and writing the cache entries.

This cache layer will work complementary to ESI, because ESI would also cache the rendered HTML of the navigation, the performance impact of ESI will be faster, but category information for the sidebar navigation is still loaded on every listing page, so this change is still beneficial in regard to performance, even when you use ESI.

## Consequences [​](#consequences)

* The loaded categories for the main navigation will be cached to the level defined in the sales channel config.
* Additional categories that might be loaded because e.g. the currently active category is below the configured depth will be loaded dynamically per request and merged with the default categories.
* The cache needs to be invalidated whenever a category is written or deleted. We use immediate cache invalidation for that, so that the behaviour is as before, even with deactivated HTTP-Cache.
* We encode the information about the `salesChannelId`, `language`, `root category id` and `depth` in the cache key, so that we can cache the categories for different sales channels and languages.
* We will add a `CategoryLevelLoaderCacheKeyEvent` so that plugins can modify the cache key if they dynamically influence which categories should be loaded/shown.

---

## Adding a country-agnostic language layer

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-09-01-adding-a-country-agnostic-language-layer.html

# Adding a country-agnostic language layer [​](#adding-a-country-agnostic-language-layer)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-09-01-adding-a-country-agnostic-language-layer.md)

## Context [​](#context)

Currently, Shopware’s language system uses a specific language locale (e.g. `de-DE` for German in Germany) for its translation, while falling back to another specific locale (e.g. `en-GB` for English in Great Britain).

This works well, but it is quite maintenance-heavy. If you use multiple versions or dialects of a language, such as British and American English, it will result in a lot of duplicated snippets.

### Some facts and figures [​](#some-facts-and-figures)

* Shopware has approximately 12,000 snippets.
* By default, the US translation is an automated copy of the GB translation, which is later adjusted by our community via Crowdin.
* When running them through a comparison tool, we find about 70 differences. This means that roughly 99.5% of our American snippets are identical to the British ones.

### Current structure [​](#current-structure)

## Decision [​](#decision)

Another layer containing a country-agnostic language (e.g., `en` for both `en-GB` and `en-US`) will provide an additional fallback layer. This means dialects are now treated as patch files. In Shopware, `en-GB` will be renamed to `en`, as you have to select a base dialect, retaining its 12,000 snippets, while `en-US` will shrink to around 70 snippets. This also eliminates the need for tools to initially copy-paste or pre-translate from "English to English," which, of course, incurs costs.

## Consequences [​](#consequences)

* Every additional dialect’s snippet file (e.g., `en-US` for `en`) will shrink from around 12,000 entries to likely fewer than 100.
* We will also provide an additional layer to maximize compatibility with existing installations. This means that `en-GB` will still be available as a fallback for other languages like `de-DE`, but `en` will be the primary fallback for everything.
* We will also provide an additional layer to ensure maximum compatibility with existing translations (e.g. via extensions). This means `en-GB` will remain available as a fallback for other languages such as `de-DE` and `de`, while `en` will serve as the final fallback.
* Translations provided via the community (Crowdin) will show a lower coverage percentage, but will more accurately reflect the actual differences between `en-US` and `en`.
* In Crowdin and in our product, the base language is set declaratively, so we will inform the community that British English is our base language, and we simply refer to it as `en`.
* All snippet files in Shopware’s core will be renamed to the country-agnostic language
  + `en-GB.json` -> `en.json`, `messages.en-GB.base.json` -> `messages.en.base.json` and so on.
  + Similarly: `de-DE` -> `de`
* The community translations / language pack will update their locales to their country-agnostic versions as well (e.g., `es-ES` -> `es`).
* The system’s default language or active language handling will remain unchanged.
* Plugins and apps do not require immediate adjustments, as the previous structure will continue to function as before as well.

### New structure [​](#new-structure)

---

## Caching Strategy for Store API

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-09-15-store-api-cache-strategy.html

# Caching Strategy for Store API [​](#caching-strategy-for-store-api)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-09-15-store-api-cache-strategy.md)

## Context [​](#context)

Store API performance is critical for all headless installations. Currently, Store API responses are not cached by default, which leads to unnecessary server load and reduced performance for end users.

At the same time, Storefront (classical Shopware frontend based on twig templates, mentioned here and further in this doc only for context and strategy alignment) already has a caching mechanism in place and Shopware provides a reference configuration for reverse proxies like Varnish, that supports Storefront caching.

The goal is to introduce a caching strategy for Store API, while reusing existing approaches and keeping required changes on the client and infrastructure side to a minimum.

Important details:

* Store API response may differ by context (e.g. logged in customer, currency, language, active rules, etc).
* Storefront uses cookies to track differences in the contexts.
* Storefront marks cacheable routes via the `'_httpCache' => true` route defaults attribute. If this attribute is present (and other conditions are met), `CacheResponseSubscriber` adds `Cache-Control: public, s-maxage=7200` header to the response (TTL is controlled via configuration).
* Storefront's `Cache-Control` header is prepared for reverse-proxy (only when reverse proxy is enabled in the configuration). Client-side caching remains `no-cache, private` as we lack the ability to invalidate client caches, unlike reverse proxies.
* Storefront caches may be invalidated via cache tags (x-tag in Varnish).
* Several non-mutating Store API endpoints that return non-sensitive data use `POST` to support larger payloads (see Criteria object). Some of them already support both `POST` and `GET`.
* `RequestCriteriaBuilder` supports building Criteria from separate query parameters for `GET` requests (`filter`, `grouping`, `fields`, `page`, `limit`, etc). Criteria as a separate parameters leads to a more complex OpenAPI schema. Also differences between standard and php array query parameters serialization makes clients implementation more complex (`colors[]=red&colors[]=blue` vs `colors=red,blue`).

## Decision [​](#decision)

1. HTTP methods
   * Prefer `GET` for non-mutating endpoints returning non-sensitive data.
   * For endpoints that currently use `POST` but are non-mutating and return non-sensitive data, add `GET` support (of fully transition to `GET` if possible).
2. Criteria in query parameters
   * Introduce `_criteria` parameter to support passing Criteria in `GET` requests as a single query parameter.
   * Format: JSON -> gzip -> base64url (url-safe Base64) of the Criteria object.
   * Provide SDK helpers for encoding/decoding and canonicalization (stable key ordering, normalized arrays) to improve cache hit ratio across clients.
   * Introduce phaseout plan for separate criteria parameters (e.g. `filter`, `grouping`, `fields`, `page`, `limit`, etc).
3. Use cache headers (not cookies) to differentiate contexts on Store API
   * Use `sw-currency-id` and `sw-language-id` to differentiate currency and language. Shopware must update currency and language ids in the context of the current request based on these headers.
   * Use `sw-context-hash` to differentiate other context aspects (e.g. logged in customer, active rules, etc). Use the same algorithm as for storefront context hash cookie.
   * All three headers must be returned in the Store API responses. If clients want to utilize caching, they should send these headers in subsequent requests. When client sends these headers, reverse proxy uses them to detect the cache bucket. Additionally, the language and currency headers change the currency and language in the response.
   * `Vary` header should include all three headers, so reverse proxies and CDNs can differentiate cache entries.
4. Mark cacheable routes
   * Use `'_httpCache'` route default attribute to mark cacheable Store API routes.
   * Extend `CacheResponseSubscriber` to add `Cache-Control` header to Store API responses similar to Storefront responses, but ignoring cookies (relying on headers + `Vary` instead). Default `Cache-Control` value for cacheable routes should be `public, max-age=0, s-maxage=1800, stale-while-revalidate=86400, stale-if-error=7200`, non-cacheable `no-cache, private`
5. Invalidation strategy
   * Reuse existing cache tags implementation to invalidate cached Store API responses.

## Consequences [​](#consequences)

* SDK updates
  + Switch relevant endpoints to GET where safe
  + Add support for `_criteria` parameter (encoding, decoding, canonicalization)
  + Implement automatic request method selection (fallback to POST when the compressed \_criteria would exceed practical URL limits).
  + Track and resend `sw-currency-id`, `sw-language-id`, and `sw-context-hash` headers on subsequent requests.
* Clients
  + No changes required if caching is not desired.
  + To utilize caching, clients should adopt the updated SDK or implement the same strategy.
  + Client should beware that `sw-currency-id`, `sw-language-id` can change the response language and currency.
* Extensions
  + Custom Store API endpoints can opt into caching using the same route flags.
* Trade-offs
  + Using compressed `_criteria` reduces request readability and makes debugging and logging harder.
  + Without canonicalization, compressed `_criteria` parameter may lead to a decreased cache hit ratio.
  + Operators may need minor reverse-proxy adjustments, depending on the level of customization.

## Considered alternatives [​](#considered-alternatives)

1. Keep using cookies for context differentiation similarly to Storefront:

   * Less explicit for the clients, cache can be used unintentionally.
   * More complex configuration for reverse proxies (e.g. Varnish).
   * No need to change the client implementation. Rejected in favor of explicit request headers.
2. Cache POST requests with big payloads if possible:

   * Not aligned with HTTP semantics (POST is not cacheable by default).
   * More complex configuration for reverse proxies and CDNs.
   * Not transparent for the clients that caching is used.
   * Transparent request - easier logging and debugging. Rejected in favor of alignment with HTTP semantics and minimal changes on infra side were preferred.
3. Two-step flow: POST returns a request hash; GET retrieves cached data by hash:

   * More complex implementation for clients (changed workflow).
   * More complex implementation for Shopware (need to store request hashes and map them to actual requests).
   * Additional round-trip for the requests.
   * Transparent request - easier to debug and log. Rejected in favor of simplicity of implementation, limited number of requests and minimal changes on clients side.
4. Use “plain” structured query parameters (filter[...][]=...)

   * Can hit url length limits more easily.
   * More complex OpenAPI schema, problem with array format differences between clients persists.
   * Transparent request - easier to debug and log. Rejected in favor of more compact representation and simpler OpenAPI schema.

---

## Co-locate Administration Technical Documentation with Source Code

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-10-14-colocate-administration-technical-docs.html

# Co-locate Administration Technical Documentation with Source Code [​](#co-locate-administration-technical-documentation-with-source-code)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-10-14-colocate-administration-technical-docs.md)

## Context [​](#context)

The Shopware Administration codebase contains AGENTS.md files throughout the source tree (`src/Administration/Resources/app/administration/src/**`) that serve as concise reference guides for AI assistants and developers. These files provide quick architectural guidance, critical rules, and key patterns.

However, comprehensive technical documentation traditionally lives in a separate documentation repository. This separation creates several challenges:

1. **Difficult Cross-Referencing**: AGENTS.md files cannot easily reference detailed documentation when it lives in a different repository, requiring absolute URLs or external links that may break.
2. **Information Duplication**: Without easy references, AGENTS.md files would need to duplicate detailed explanations, leading to maintenance overhead and potential inconsistencies.
3. **AI Context Limitations**: AI assistants working with the codebase cannot easily access external documentation repositories, limiting their ability to understand complex architectural patterns and make informed suggestions.
4. **Version Synchronization**: Keeping documentation in sync with code changes across repositories is error-prone, especially for rapidly evolving areas.

## Decision [​](#decision)

We will co-locate the technical documentation for the Administration component directly within the source tree at `src/Administration/Resources/app/administration/technical-docs/` instead of maintaining it in a separate documentation repository.

This approach enables:

* **Direct References**: AGENTS.md files can reference detailed documentation using relative paths (e.g., `> **Detailed Docs**: technical-docs/04-data-layer/`)
* **Single Source of Truth**: Documentation lives alongside the code it describes, ensuring version alignment
* **AI-Accessible Context**: AI assistants can access both code and comprehensive documentation in a single workspace, improving code understanding and suggestions
* **Atomic Changes**: Documentation updates can be committed with related code changes in the same pull request

The technical documentation is organized in numbered sections (01-overview, 02-architecture, etc.) to provide structured, comprehensive guides that AGENTS.md files can reference without duplication.

## Consequences [​](#consequences)

### Positive [​](#positive)

* AGENTS.md files remain concise while providing access to detailed documentation through references
* AI assistants have complete context when analyzing or modifying Administration code
* Documentation changes are automatically synchronized with code changes
* Reduced duplication between AGENTS.md files and detailed documentation
* Easier for developers to find relevant documentation when working in the codebase

### Neutral [​](#neutral)

* This is an experimental pattern initially applied only to the Administration component
* If successful, this pattern may be adopted for other parts of Shopware 6 (Core, Storefront, etc.)
* The effectiveness of this approach will be evaluated based on real-world usage

### Trade-offs [​](#trade-offs)

* Documentation for the technical Administration component is separated from the central documentation repository

We will monitor the effectiveness of this pattern for the Administration component before deciding whether to expand it to other areas of the codebase.

---

## Pin All NPM Dependencies to Exact Versions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-10-23-pin-npm-dependencies.html

# Pin All NPM Dependencies to Exact Versions [​](#pin-all-npm-dependencies-to-exact-versions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-10-23-pin-npm-dependencies.md)

## Context [​](#context)

NPM dependencies with range specifiers (e.g., `^1.2.3` or `~1.2.3`) allow automatic updates to newer compatible versions during installation. While convenient for library development, this creates several risks for application development:

1. **Non-Deterministic Builds**: Different developers or CI runs may install different versions, leading to "works on my machine" issues
2. **Security Risk Window**: Malicious packages can be introduced through automatic version updates without explicit review
3. **Breaking Changes**: Even minor/patch updates can introduce bugs or breaking changes despite semantic versioning
4. **Difficult Debugging**: Inconsistent dependency versions across environments make issues harder to reproduce and diagnose

## Decision [​](#decision)

All NPM dependencies in Shopware 6 must be pinned to exact versions without range specifiers:

* ❌ `"package": "^1.2.3"` or `"package": "~1.2.3"`
* ✅ `"package": "1.2.3"`

This applies to both `dependencies` and `devDependencies` in all `package.json` files throughout the repository.

Automated CI checks have been implemented to:

* Discover all `package.json` files in the repository
* Validate that no unpinned dependencies exist
* Block merges if unpinned dependencies are found

These checks run via the `npm-audit-check.yml` workflow on every pull request and push to trunk.

## Consequences [​](#consequences)

### Positive [​](#positive)

* **Reproducible Builds**: Identical dependency versions across all environments (local, CI, production)
* **Explicit Updates**: Dependency updates require intentional changes and code review
* **Enhanced Security**: Prevents automatic installation of compromised package versions
* **Easier Debugging**: Consistent versions make issues reproducible and easier to diagnose
* **Automated Enforcement**: CI pipeline ensures compliance without manual review

### Negative [​](#negative)

* **Manual Dependency Updates**: Developers must explicitly update dependencies using `npm update` or `npm install package@version`
* **Increased Maintenance**: Regular dependency updates require more conscious effort
* **More Frequent PRs**: Security patches and updates must be applied through explicit pull requests

### For Developers [​](#for-developers)

When adding or updating dependencies:

1. Always specify exact versions in `package.json`
2. Run `npm install` to update `package-lock.json`
3. The CI pipeline will reject PRs with unpinned dependencies
4. Use tools like `npm outdated` to check for available updates

---

## Replace changelog ADR with "Changelog & Release Info Process"

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-10-28-changelog-release-info-process.html

# Replace changelog ADR with "Changelog & Release Info Process" [​](#replace-changelog-adr-with-changelog-release-info-process)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-10-28-changelog-release-info-process.md)

## Context [​](#context)

Historically, Shopware used a changelog file workflow based on per-change markdown files under `/changelog/_unreleased` with an automated build step that aggregated them into `CHANGELOG.md` and `UPGRADE.md`.  
 While technically useful, this caused friction: duplication, missing high-level developer-facing context, and the release notes living in a separate repository.  
 The team now prefers a curated, in-repo workflow for developer-facing release notes.

---

## Decision [​](#decision)

1. The ADR `2020-08-03-implement-new-changelog.md` is **superseded** and archived under `adr/_superseded/`.
2. We adopt a **curated in-repo model**:
   * `RELEASE_INFO-6.<currentMajor>.md`: developer-facing release notes with per-minor sections.
   * `UPGRADE-6.<upcomingMajor>.md`: upgrade instructions and breaking changes.

```shiki
Example: RELEASE_INFO-6.7.md

## 6.7.5 (Upcoming)
### Core
- Added new `CartRoute` parameter `guestLogin` (PR #12326)
- Improved indexing performance for product categories (PR #12657)
### Administration
- Updated TypeScript target to ES2023 (PR #12408)
```

```shiki
Example: UPGRADE-6.8.md

## Deprecated SalesChannelContextSwitcher

The `SalesChannelContextSwitcher` service is deprecated and will be removed in 6.8.  
Plugins using it should migrate to `ContextResolverInterface`.

_(Tip: You can use short headings like “What changed” or “How to adjust” if it helps readability, but they’re not mandatory.)_
```

3. PR authors must add developer-facing entries as part of their PRs:
   * Information that benefits external developers → `RELEASE_INFO-6.X.md` (in the “Upcoming” section).
   * Breaking changes → `UPGRADE-6.Y.md`.
4. Entries should follow this minimal structure (category, concise description, PR reference). CI will not enforce a strict format initially, but reviewers are responsible for verifying consistency and readability.
5. The full, exhaustive changelog for each release will be generated automatically and linked from the release notes.
6. The changelog is the raw, machine-produced record of merged PRs and commits and is intended for engineering/support/partners.
7. The changelog automation will group changes by labels (e.g., `bug`, `feature`, `performance`) and include links to PRs and authors to make the raw changelog navigable.
8. Human-curated files `RELEASE_INFO-6.<minor>.md` and `UPGRADE-6.<major>.md` are the primary sources for developer-facing and merchant-facing communications; the autogenerated changelog is complementary and always linked for full traceability.
9. The PR template is updated to reference this process and provide checklist guidance.
10. CI will later validate that either `RELEASE_INFO` or `UPGRADE` was updated when relevant (or explicitly skipped with justification).

---

For details about how to write entries for these files, please refer to the release [documentation guide](./../delivery-process/documenting-a-release.html).

## Consequences [​](#consequences)

* The old ADR is preserved in `_superseded` for historical reference.
* PR reviewers must ensure developer-facing entries are added or explicitly marked unnecessary.
* Marketing and Comms will pull content **only** from `RELEASE_INFO` and `UPGRADE`, not from the raw changelog.
* Internal documentation (Confluence, DevRel guides) links to these files as the single source of truth for developer-facing release information.
* A future CI enhancement will enforce the presence of these updates where required.

---

## References [​](#references)

* Superseded ADR: `adr/_superseded/2020-08-03-implement-new-changelog.md`

---

## Improved HTTP Cache Layer

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-11-03-improved-http-cache-layer.html

# Improved HTTP Cache Layer [​](#improved-http-cache-layer)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-11-03-improved-http-cache-layer.md)

## Context [​](#context)

Shopware currently supports an HTTP-cache layer; however, the current implementation has some limitations:

* **Only storefront requests are cached**: The cache is only used for storefront requests, store-api is not supported out of the box, leading to performance penalties in headless projects.
* **Cache-Hit rate is rather low**: All matched rule ids are included in the cache-hash, this leads to a lot of cache permutations. As one consequence of that, by default, the whole caching is disabled as soon as the cart is filled or a customer logged in.
* **Complex reverse proxy configuration**: The reverse proxy configuration is quite complex because of the use of different cache headers and cookies, as a result we only support Fastly and Varnish, other reverse proxies are hard to add.
* **Actual cache-control configuration is hard-coded and splattered**: The values set for `cache-control` headers are hard-coded and splattered (e.g., hardcoded in the reverse proxy config and in shopware), they cannot be configured based on projects needs, and also on route level only the max-age is configurable.

## Decision [​](#decision)

We will rework the HTTP-cache layer to address the limitations mentioned above, for that the following changes will be made:

### Only use cache-relevant rule-ids inside cache-hash [​](#only-use-cache-relevant-rule-ids-inside-cache-hash)

Most rule-ids are not relevant for caching, e.g., when they are not used at all, or only for checkout-related features (e.g., payment-methods, promotions). Therefore, we will only include the rule-ids that are relevant for caching in the cache-hash, we do the distinction based on the existing `rule-areas`. By default, all rule-ids, that are used in the `product` area, will be included in the cache-hash. For extensibility, a new event will be introduced that allows modifying the list of rule-areas that are relevant for caching.

### Configurable caching policies [​](#configurable-caching-policies)

The caching policies used will be moved from the code directly to the configuration. We will allow defining default caching policies based on the area (storefront or store-api), as well as use-case (cached or uncached). We also allow route level configuration that will override the default caching policies.

### Simplify reverse proxy configuration [​](#simplify-reverse-proxy-configuration)

We will simplify the reverse proxy configuration by only relying on the `sw-cache-hash`, as the only application state that the reverse proxy needs to take into account. The `sw-cache-hash` will be set as a cookie and as a header, additionally we add the `sw-cache-hash` header name as a `vary` header to the response. So the response headers will look like this:

```shiki
sw-cache-hash: theHash
vary: sw-cache-hash
set-cookie: sw-cache-hash=theHash;
```

Adding it as header allows the default [`vary` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Vary) implementation of reverse proxies to work. The cookie is used to make it easier for clients to pass along the correct hash with all further requests, without the need to manually handle the header. The only shopware specific reverse proxy configuration will be to set the `sw-cache-hash` header based on the `sw-cache-hash` cookie on the reverse proxy.

Additionally, the use of clear and configurable policies for the cache-control headers will remove the need to manually override the cache-control headers on the reverse proxy side.

### HTTP-Cache support for store-api [​](#http-cache-support-for-store-api)

We will add HTTP-Cache support for the store-api as well. The caching behaviour and used patterns are the same as for the storefront. So the configuration (on the shopware side, as well as on the reverse proxy) will be the same as in the storefront. To make the caching applicable for the store-api, we will adjust the store-api routes to support `GET` requests where it makes sense, clients should preferably use the `GET` requests.

For detailed documentation on why and how we added support for the store-api caching, refer to the [specific store-api caching ADR](./2025-09-15-store-api-cache-strategy.html).

## Consequences [​](#consequences)

### Storefront pages for logged-in users and filled carts are cached by default [​](#storefront-pages-for-logged-in-users-and-filled-carts-are-cached-by-default)

By removal of the state header, those pages will be cached by default. This might be a breaking change for some projects when their customizations rely on the cache not being used for logged-in users or filled carts. This is especially the case when context/user-specific information is used in the template. In those cases the more dynamic content should be refetched over async AJAX calls to uncached routes, so that the main content can still be cached.

### Not all rules influence the cache-hash [​](#not-all-rules-influence-the-cache-hash)

As only the rules used in some rule areas will be included in the cache-hash, some rules will not influence the cache-hash. This could be a breaking change for some projects, when they built customization based on rules but did not include them in the rule-areas.

### Store-API routes will be cached by default [​](#store-api-routes-will-be-cached-by-default)

The store-api routes will be cached by default; this might be a breaking change for some projects when they rely on the cache not being used for store-api routes. Also, they need to adjust their clients to correctly pass the cache-hash head or cookie, otherwise it could lead to the wrong data being returned from the cache.

### Feature flag handling [​](#feature-flag-handling)

All the breaking changes (and caching benefits) can be already used by opting in and enabling the `CACHE_REWORK` feature flag.

---

## Introduce Product Type And Deprecate Product States

**Source:** https://developer.shopware.com/docs/resources/references/adr/2025-11-14-introduce-product-type-and-deprecate-states.html

# Introduce Product Type And Deprecate Product States [​](#introduce-product-type-and-deprecate-product-states)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2025-11-14-introduce-product-type-and-deprecate-states.md)

# Introduce Product Type And Deprecate Product States [​](#introduce-product-type-and-deprecate-product-states-1)

## Context [​](#context)

Currently, the product.states field has various issues:

* Not clear semantics:

  + It mixes multiple responsibilities (download/physical markers, per-row flags).
  + A product never changes from digital to physical or vice versa, but the field is updated on every save even if no relevant changes were made. Hence, the term "states" is ambiguous and does not clearly convey the purpose of the field, as for other `states` in other entities, for e.g `order.states`, it should represent the lifecycle state of the entity, but in this case, it represents product types.
  + A product cannot be both digital and physical, but the field is a JSON array.
  + We need a single authoritative indicator for whether a product/line-item is digital or physical that can be easily queried by DAL, Elasticsearch, Cart processors, and rule conditions.
* Performance:

  + The field is not indexed as it is a JSON array, so simple filtering (e.g. "only digital products") is slow and complex.
  + `StatesUpdater` was also not optimal for performance, it runs on every product save and updates the entire product record even if no relevant changes were made but in theory, once a product is marked as digital or physical, it should not be changed.
* Extensibility:

  + `product.states` are updated by the `StatesUpdater` based on the presence of downloads; if a product has downloads, it gets the `is-download` state, otherwise `is-physical`. This should be fine for platform use cases, but it is not flexible for third-party extensions that may want to introduce new product types.
  + The current implementation does not provide a straightforward way for third-party developers to add new product types or states (e.g. bundle, container, etc.).
  + The rule conditions and product stream filters are tightly coupled to the legacy states (hard coded in both client-side and server-side), making it difficult to extend or modify their behavior. For e.g a third-party developer wanting to add a new product type, they would need to modify the existing rule conditions, product stream filters, product listing filters which is not ideal.

## Decision [​](#decision)

### Deprecation of `product.states`: [​](#deprecation-of-product-states)

* Deprecate the `product.states` field in the database in favor of a new `product.type` field that clearly indicates whether a product is `digital` or `physical`.
* Deprecate `order_line_item.states` in favor of `order_line_item.payload.product_type` in a similar manner.
* Deprecate `LineItemProductStatesRule` in favor of `LineItemProductTypeRule`.
* Deprecate `StatesUpdater` service and its related dispatched events (`ProductStatesBeforeChangeEvent`, `ProductStatesChangedEvent`).
* Deprecate product stream filters and product listing filters that rely on `product.states`, guiding users to use the new `product.type` field instead.

### Introduce `product.type` field [​](#introduce-product-type-field)

Product type field should have a clear definition: It represents the type of product, whether it's physical or digital or bundle etc, and it should be immutable once set. A product can only have one type at a time.

In a more detailed manner, we will make the following changes:

* Add a dedicated `product.type` column (possible values by default: `physical` or `digital`) with DAL exposure, new entity constants, defaulting to `physical`.
* Also add `order_line_item.payload.product_type` and populate it when line items are converted from the cart; `LineItemTransformer` also reconstructs legacy states when needed.
* Introduce `LineItemProductTypeRule` for rule builder usage and deprecate the legacy `LineItemProductStatesRule`.
* Rules automatically pick up custom product types registered via the shared registry (@See `ProductTypeRegistry`), so PHP-based conditions stay consistent with storefront/admin filters.

#### Introduce a server-side `ProductTypeRegistry` [​](#introduce-a-server-side-producttyperegistry)

* This registry help both core rules and plugins can register additional product types via the parameter `%shopware.product.allowed_types%` as an array.

php

```shiki
class ProductTypeRegistry
{
    /**
     * @var array<string>
     */
    private array $types = [];

    public function addType(string $type): void

    public function getTypes(): array
```

* By default, the platform registers two types: `digital` and `physical`.

#### New admin API endpoint to fetch all registered product types [​](#new-admin-api-endpoint-to-fetch-all-registered-product-types)

* Introduce a new admin api `GET /api/_action/product/types` to list all registered product types for use in admin UI for e.g product stream filters or Product listing filters

## Consequences [​](#consequences)

### For the platform [​](#for-the-platform)

* Querying by digital/physical products now becomes trivial (`product.type = 'digital'`), improving DAL and search performance and clarity.
* The core will migrate existing `product.states` to `product.type` and the same from `order_line_item.states` to `order_line_item.payload.product_type` to preserve existing behavior.
* Rule conditions must be updated to reference `cartLineItemProductType`; existing rules referencing `cartLineItemProductStates` will continue to work until 6.8 but should be migrated.
* Similar to rule conditions, existing product stream filters must be updated to transition from `product.states` to the new `product.type` field.
* We should warn on the UI when users use `states` field in product streams, rule conditions, product listing filters, guiding them to use to the new `type` field instead.

### For third-party developers [​](#for-third-party-developers)

* You can now easily register new product types by override `shopware.product.allowed_types` in your `config/packages/shopware.yaml`. For e.g:

yaml

```shiki
shopware:
    product:
        allowed_types:
        - bundle
        - container
```

* If you have existing code that relies on `product.states`, you should plan to migrate to the new `product.type` field.
* If you are creating digital products, you should explicitly set the `type` field to `digital` when creating new products.
* Be specific to use `type` field if you want to be safe to not have issues which fetching product types that you are not aware of. For examples, a third-party developer may introduce a new product type `container`, if you're not specific in your queries, you may incur unexpected results.
* Backwards compatibility must be maintained for 6.7, but in 6.8 the `states` fields should disappear entirely.
* Keep writing to the legacy `states` column only when `Feature::isActive('v6.8.0.0') === false`, wrapping all DAL fields, hydrators, and entity accessors in deprecation notices so tooling warns consumers.

---

