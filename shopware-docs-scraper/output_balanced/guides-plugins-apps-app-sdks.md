# Guides Plugins Apps App Sdks

*Scraped from Shopware Developer Documentation*

---

## App SDKs

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/

# App SDKs [​](#app-sdks)

The Shopware app SDK enables you to build applications and plugins that extend the functionality of the Shopware e-commerce platform. It provides the necessary resources and tools to simplify the development process and integrate custom logic into the Shopware environment.

---

## Official JavaScript SDK

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/

# JavaScript [​](#javascript)

The App SDK for JavaScript abstracts and simplifies creating Shopware apps. The SDK uses JavaScript standardized Request/Response objects and therefore is supported to run in Node/Deno/Bun/Cloudflare Workers.

The app SDK provides a context object that grants access to relevant information and services within the Shopware environment. This context is essential for interacting with Shopware's APIs, accessing database entities, and executing various operations.

To ensure secure communication between the application and Shopware, this SDK supports signing mechanisms, allowing developers to validate the authenticity and integrity of requests and responses.

It also includes an HTTP client that simplifies making API requests to Shopware endpoints. It provides methods for handling authentication, executing HTTP requests, and processing responses.

---

## Getting started

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/01-getting_started.html

# Getting Started [​](#getting-started)

The app server written in TypeScript and is an open-source project accessible at [app-sdk-js](https://github.com/shopware/app-sdk-js).

## Installation [​](#installation)

Install the App PHP SDK via NPM:

bash

```shiki
npm install --save @shopware-ag/app-sdk-server
```

After the installation, you can use the SDK in your project. Here is an example:

## Registration process [​](#registration-process)

javascript

```shiki
import { AppServer, InMemoryShopRepository } from '@shopware-ag/app-server-sdk'

const app = new AppServer({
  appName: 'MyApp',
  appSecret: 'my-secret',
  authorizeCallbackUrl: 'http://localhost:3000/authorize/callback',
}, new InMemoryShopRepository());

export default {
  async fetch(request) {
    const { pathname } = new URL(request.url);
    if (pathname === '/authorize') {
      return app.registration.authorize(request);
    } else if (pathname === '/authorize/callback') {
      return app.registration.authorizeCallback(request);
    }

    return new Response('Not found', { status: 404 });
  }
};
```

First we create an AppServer instance with the app name, app secret and the authorize callback URL. The `InMemoryShopRepository` is used to store the shops in memory. You can also use a custom repository to store the shops in a database.

With this code, you can register your app with our custom app backend.

Next, we will look into the [lifecycle handling](./02-lifecycle.html).

---

## Lifecycle

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/02-lifecycle.html

# Lifecycle [​](#lifecycle)

The Shopware App System manages the lifecycle of an app. Shopware will send any change if registered a webhook to our backend server.

To track the state in our Database correctly, we need to implement some lifecycle methods.

## Lifecycle Methods [​](#lifecycle-methods)

* `activate`
* `deactivate`
* `uninstall`

The lifecycle registration in the `manifest.xml` would look like this:

xml

```shiki
<webhooks>
    <webhook name="appActivate" url="https://app-server.com/app/activate" event="app.activated"/>
    <webhook name="appDeactivated" url="https://app-server.com/app/deactivate" event="app.deactivated"/>
    <webhook name="appDelete" url="https://app-server.com/app/delete" event="app.deleted"/>
</webhooks>
```

## Usage [​](#usage)

The implementation is similar to [Registration](./01-getting_started.html),

javascript

```shiki
import { AppServer, InMemoryShopRepository } from '@shopware-ag/app-server-sdk'

const app = new AppServer({
  appName: 'MyApp',
  appSecret: 'my-secret',
  authorizeCallbackUrl: 'http://localhost:3000/authorize/callback',
}, new InMemoryShopRepository());

export default {
  async fetch(request) {
    const { pathname } = new URL(request.url);
    if (pathname === '/authorize') {
      return app.registration.authorize(request);
    } if (pathname === '/authorize/callback') {
      return app.registration.authorizeCallback(request);
    } if (pathname === '/app/activate') {
      return app.registration.activate(request);
    } if (pathname === '/app/deactivate') {
      return app.registration.deactivate(request);
    } if (pathname === '/app/delete') {
      return app.registration.delete(request);
    }

    return new Response('Not found', { status: 404 });
  }
};
```

So, in this case, our backend gets notified of any app change, and we can track the state in our database.

Next, we will look into the [Context resolving](./03-context.html).

---

## Context

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/03-context.html

# Context [​](#context)

The ContextResolver helps you to validate the Request, resolve the Shop and provide types for the Context.

## Usage [​](#usage)

javascript

```shiki
import { AppServer } from '@shopware-ag/app-server-sdk'

const app = new AppServer(/** ... */);

// Resolve the context from the request like iframe
app.contextResolver.fromBrowser(/** Request */);

// Resolve the context from the request like webhook, action button
app.contextResolver.fromAPI(/** Request */);
```

Both methods accepts a Type to specify the context type.

ts

```shiki
import { BrowserAppModuleRequest } from '@shopware-ag/app-server-sdk/types'

const ctx = await app.contextResolver.fromBrowser<BrowserAppModuleRequest>(/** Request */);

// This is now typed
console.log(ctx.payload['sw-version']);
```

You can checkout the [types.ts](https://github.com/shopware/app-sdk-js/blob/main/src/types.ts) to see all available types.

If you miss a type, feel free to open a PR or an issue. Otherwise you can also specify the type also in your project.

ts

```shiki
type MyCustomWebHook = {
  foo: string;
}

const ctx = await app.contextResolver.fromBrowser<MyCustomWebHook>(/** Request */);

ctx.payload.foo; // This is now typed and the IDE will help you
```

Next, we will look into the [Signing of responses](./04-signing.html).

---

## Signing

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/04-signing.html

# Signing of responses [​](#signing-of-responses)

The Shopware App System requires you to sign your responses to the Shopware server.

The signing is required for all responses that are sent to the Shopware server. The signature is used to verify the authenticity of the response and to ensure that the response was not tampered with.

To sign the response, you can call the signer with `signResponse` method. The signer will sign the response with the provided shop.

php

```shiki
import { AppServer } from '@shopware-ag/app-server-sdk'

const app = new AppServer(/** ... */);

// Or you get it from the context resolver
const shop = await app.repository.getShopById('shop-id');

const response = new Response('Hello World', {
    headers: {
        'Content-Type': 'text/plain',
    },
});

const signedResponse = await app.signer.signResponse(response, shop);
```

Next, we will look into the [Making HTTP requests to the Shop](./05-http-client.html).

---

## HTTP-client

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/05-http-client.html

# Making HTTP requests to the Shop [​](#making-http-requests-to-the-shop)

The SDK offers a simple HTTP client for sending requests to the Shopware server. You can access the HTTP client when you resolved a context using ContextResolver or create it manually. The client will automatically fetch the OAuth2 token for the shop and add it to the request.

## Using ContextResolver [​](#using-contextresolver)

ts

```shiki
import { AppServer } from '@shopware-ag/app-server-sdk'

const app = new AppServer(/** ... */);

const ctx = await app.contextResolver.fromBrowser<BrowserAppModuleRequest>(/** Request */);

const response = await ctx.httpClient.get<{version: string}>('/_info/version')

console.log(response.body.version)
```

## Creating the client manually [​](#creating-the-client-manually)

ts

```shiki
import { HttpClient } from "@shopware-ag/app-server-sdk"

// Get the shop by repository directly
const shop = ...;

const httpClient = new HttpClient(shop);

const response = await httpClient.get<{version: string}>('/_info/version')

console.log(response.body.version)
```

## Abstraction to EntityRepository [​](#abstraction-to-entityrepository)

The SDK offers an abstraction to the EntityRepository. This offers a much simpler way to interact with the Shopware API and fetch entities by the generic Shopware API.

ts

```shiki
import { HttpClient } from "@shopware-ag/app-server-sdk"
import { EntityRepository } from "@shopware-ag/app-server-sdk/helper/admin-api";
import { Criteria } from "@shopware-ag/app-server-sdk/helper/criteria";

// Get the shop by repository directly
const shop = ...;

const httpClient = new HttpClient(shop);

type Product = {
  id: string;
  name: string;
};

const repository = new EntityRepository<Product>(httpClient, "product");

// Fetch all products
const products = await repository.search(new Criteria());

// Get the first product and print the name
console.log(products.first().name);
// Same as above
console.log(products.data[0].name);

// Fetch a single product

const product = await repository.search(new Criteria(['my-uuid'])).first();

// Product can be null
console.log(product.name);

// Upserts update the given product if found, otherwise creates it
await repository.upsert(['id': 'my-uuid', 'name': 'My Product']);

// This would try to create a product, but fail as not all required fields are provided
await repository.upsert(['name': 'My Product']);

// Delete a product
await repository.delete([{id: 'my-uuid'}]);
```

## Abstraction of Sync API [​](#abstraction-of-sync-api)

The Sync API offers to create/update/delete entities in the Shopware API in a batch. This is useful for syncing data from your app to the Shopware API.

The EntityRepository `upsert` and `delete` uses the Sync API under the hood as the traditional API does not support batch operations. You can use also the Sync API directly.

ts

```shiki
import { SyncOperation, SyncService } from "@shopware-ag/app-server-sdk/helper/admin-api";

// The same http client as usual
const httpClient = ...;

const syncService = new SyncService(httpClient);

await syncService.sync([
  // the key will be shown in the error response if that failed
  new SyncOperation('my-custom-key', 'product', 'upsert', [{id: 'my-uuid', name: 'My Product'}]),

  // delete a product
  new SyncOperation('my-custom-key', 'product', 'delete', [{id: 'my-uuid'}]),
]);
```

The second argument also allows a ApiContext to be passed to configure the API behaviour like disable indexing, or do it using queue asynchronous, disable triggering of flows, etc.

## Abstraction of Media APIs [​](#abstraction-of-media-apis)

The SDK offers helpers to manage the Shopware Media Manager. This allows you to easily upload an media, lookup folders or create new folder.

ts

```shiki
import { createMediaFolder, uploadMediaFile, getMediaFolderByName } from '@shopware-ag/app-server-sdk/helper/media';

// The same http client as usual
const httpClient = ...;

// Create a new folder
const folderId = await createMediaFolder(httpClient, 'My Folder', {});

// Create a new folder with parent folder id
const folderId = await createMediaFolder(httpClient, 'My Folder', {parentId: "parent-id"});

// Lookup a folder by name
const folderId = await getMediaFolderByName(httpClient, 'My Folder');

// Lookup a folder by default folder for an entity
// Returns back the folderId to be used when using a media for a product
const folderId = await getMediaDefaultFolderByEntity(httpClient, 'product');

// Upload a file to the media manager
await uploadMediaFile(httpClient, {
    file: new Blob(['my text'], { type: 'text/plain' }),
    fileName: `foo.text`,
    // Optional, a folder id to upload the file to
    mediaFolderId: folderId
});
```

Next, we will look into the [Integrations](./06-integration.html).

---

## Integrations

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/06-integration.html

The SDK offers many optional integrations into several JavaScript ecosystems, so you can easily integrate your app into your existing project.

## Hono [​](#hono)

The SDK offers a simple integration into the Hono ecosystem. It will register automatically all necessary routes and provide a simple way to interact with the Hono API.

ts

```shiki
import { InMemoryShopRepository } from '@shopware-ag/app-server-sdk'
import type {
  AppServer,
  ShopInterface,
  Context,
} from "@shopware-ag/app-server-sdk";
import { Hono } from "hono";
import { configureAppServer } from "@shopware-ag/app-server-sdk/integration/hono";

const app = new Hono();

// You can configure all registered routes here
configureAppServer(app, {
  appName: "Test",
  appSecret: "Test",
  shopRepository: new InMemoryShopRepository(),
});

declare module "hono" {
  interface ContextVariableMap {
    app: AppServer;
    shop: ShopInterface;
    context: Context;
  }
}

export default app;
```

The `configureAppServer` will automatically register following routes:

* `/app/register` - Registration URL
* `/app/register/confirm` - Registration Confirmation
* `/app/activate` - Notify using app.activated webhook
* `/app/deactivate` - Notify using app.deactivated webhook
* `/app/delete` - Notify using app.delete webhook

This could look like this in the `manifest.xml`:

xml

```shiki
<setup>
    <registrationUrl>http://localhost:3000/app/register</registrationUrl>
</setup>
<webhooks>
    <webhook name="appActivated" url="http://localhost:3000/app/activate" event="app.activated"/>
    <webhook name="appDeactivated" url="http://localhost:3000/app/deactivate" event="app.deactivated"/>
    <webhook name="appDeleted" url="http://localhost:3000/app/delete" event="app.deleted"/>
</webhooks>
```

Additionally a middleware is configured to automatically validate the incoming requests and resolve the called Shop. This is my default configured to `/app/*` routes.

ts

```shiki
import { createNotificationResponse } from "@shopware-ag/app-server-sdk/helper/app-actions";

app.post("/app/action-button", async (c) => {
  const ctx = c.get("context") as Context<SimpleShop, ActionButtonRequest>;

  // Do something with the context, this is typed by second generic argument of Context
  console.log(ctx.payload.data.ids);

  return createNotificationResponse("success", "Yeah, it worked!");
});
```

So in this case the Request will be validated by the shop secret and the shop will be resolved by the shopId in the request. Additionally the response will be signed by the app secret. This is all done by the Integration, so you don't have to worry about it.

## Various Repositories (DynamoDB, Deno KV, Cloudflare KV, Bun SQLite, Better SQLite3) [​](#various-repositories-dynamodb-deno-kv-cloudflare-kv-bun-sqlite-better-sqlite3)

The SDK offers a ready-to-use Repository for several storage solutions to store the shops.

Next, we will look into the [External Frontend](./07-external-frontend.html).

---

## External Frontend

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/javascript/07-external-frontend.html

Some times apps consists of a frontend to render the admin interface using the admin-extension-sdk. Mostly it is easier to create an second application and use that as the frontend. This way you can use the full power of the frontend frameworks like Next.js, Nuxt.js, Angular, React, Vue.js, etc.

To verify that the request is from a registered shop and gather further information from the app-server backend, you can use Hono integration to authenticate the request.

So the idea is that the Browser makes a request against our app server and this verifies the request, sets a cookie and forwards the request to the frontend. The frontend can do then regular ajax requests against the app server and the app server uses the cookie to verify the request.

ts

```shiki
import { Hono } from "hono/tiny";
import { configureAppServer } from "@shopware-ag/app-server-sdk/integration/hono";

const app = new Hono();

configureAppServer(app, {
  /** ... */
  appIframeEnable: true,
  appIframeRedirects: {
    '/app/browser': '/client'
  }
});

app.get('/client-api/test', (c) => {
  console.log(c.get('shop').getShopId());

  return c.json({ shopId: c.get('shop').getShopId() });
});
```

Now we can configure in the manifest.xml the URL to `/app/browser` and the app server will verify and afterwards redirect to `/client`.

And in the frontend application we can just do a regular `fetch("/client-api/test")` and the app server will verify the request and return the shopId.

The path `/client-api/*` is automatically protected for you by a Hono middleware. The path `/client-app/*` can be changed in the `configureAppServer` function with `appIframePath`.

---

## Official Symfony bundle

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/symfony-bundle/

# App Bundle [​](#app-bundle)

App Bundle integrates the PHP App SDK for Symfony. This can be accessed at [app-bundle-symfony](https://github.com/shopware/app-bundle-symfony).

## Installation [​](#installation)

### With SQL based storage (Doctrine) [​](#with-sql-based-storage-doctrine)

bash

```shiki
composer require shopware/app-bundle doctrine/orm symfony/doctrine-bridge
```

### With NoSQL based storage (DynamoDB) [​](#with-nosql-based-storage-dynamodb)

bash

```shiki
composer require shopware/app-bundle async-aws/async-aws-bundle async-aws/dynamo-db
```

## Quick Start using SQL based storage (Doctrine) [​](#quick-start-using-sql-based-storage-doctrine)

### 1. Create a new Symfony Project (skip if existing) [​](#_1-create-a-new-symfony-project-skip-if-existing)

bash

```shiki
composer create-project symfony/skeleton:"6.2.*" my-app
```

### 2. Install the App Bundle in your Symfony Project [​](#_2-install-the-app-bundle-in-your-symfony-project)

bash

```shiki
composer require shopware/app-bundle doctrine/orm symfony/doctrine-bridge
```

It is also recommended to install the monolog bundle to have logging:

bash

```shiki
composer require logger
```

### 3. Create a new App manifest [​](#_3-create-a-new-app-manifest)

Here is an example app manifest

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>TestApp</name>
        <label>TestApp</label>
        <label lang="de-DE">TestApp</label>
        <description/>
        <description lang="de-DE"/>
        <author>Your Company</author>
        <copyright>(c) by Your Company</copyright>
        <version>1.0.0</version>
        <icon>Resources/config/plugin.png</icon>
        <license>MIT</license>
    </meta>
    <setup>
        <registrationUrl>http://localhost:8000/app/lifecycle/register</registrationUrl>
        <secret>TestSecret</secret>
    </setup>
    <webhooks>
        <webhook name="appActivated" url="http://localhost:8000/app/lifecycle/activate" event="app.activated"/>
        <webhook name="appDeactivated" url="http://localhost:8000/app/lifecycle/deactivate" event="app.deactivated"/>
        <webhook name="appDeleted" url="http://localhost:8000/app/lifecycle/delete" event="app.deleted"/>
    </webhooks>
</manifest>
```

change the app name and the app secret to your needs and also adjust the environment variables inside your `.env` file to match them.

By default, the following routes are registered:

* `/app/lifecycle/register` - Register the app
* `/app/lifecycle/activate` - Activate the app
* `/app/lifecycle/deactivate` - Deactivate the app
* `/app/lifecycle/delete` - Delete the app

You can change the prefix by editing the `config/routes/shopware_app.yaml` file.

The registration also dispatches events to react to the different lifecycle events. See APP SDK docs for it

### 4. Connecting Doctrine to a Database [​](#_4-connecting-doctrine-to-a-database)

The App Bundle ships with a basic Shop entity to store the shop information. You can extend this entity to store more information about your app if needed.

Symfony configures doctrine to use PostgreSQL by default. Change the `DATABASE_URL` environment variable in your `.env` file if you want to use MySQL. You can also use SQLite by setting the `DATABASE_URL` to `sqlite:///%kernel.project_dir%/var/app.db` for development.

After choosing your database engine, you need to require two extra composer packages.

shell

```shiki
composer req symfony/maker-bundle migrations
```

And create your first migration using `bin/console make:migration` (which is using the `AbstractShop` Class) and apply it to your database with `bin/console doctrine:migrations:migrate`.

### 5. Implement first ActionButtons, Webhooks, Payment [​](#_5-implement-first-actionbuttons-webhooks-payment)

[Check out the official app documentation to learn more about the different integration points with this SDK](/docs/guides/plugins/apps/app-base-guide.html#sdk-integration).

You can also check out the [APP SDK](https://github.com/shopware/app-php-sdk) documentation.

### Optional: Webhook as Symfony Events [​](#optional-webhook-as-symfony-events)

The app bundle also registers a generic webhook controller, which dispatches the webhook as a Symfony event. To use that, register your Shopware webhooks to the generic webhook, which is by default `/app/webhook`.

xml

```shiki
<webhook name="productWritten" url="http://localhost:8000/app/webhook" event="product.written"/>
```

With that, you can write a Symfony EventListener/Subscriber to listen to and react to the event.

php

```shiki
#[AsEventListener(event: 'webhook.product.written')]
class ProductUpdatedListener
{
    public function __invoke(WebhookAction $action): void
    {
        // handle the webhook
    }
}
```

---

## Official PHP SDK

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/

# PHP [​](#php)

The App SDK in PHP is a comprehensive software development kit provided by Shopware for creating custom applications and plugins. It offers a straightforward installation process, and once installed, developers can utilize its lifecycle management features to handle the activation, deactivation, and uninstallation of their applications.

The app SDK provides a context object that grants access to relevant information and services within the Shopware environment. This context is essential for interacting with Shopware's APIs, accessing database entities, and executing various operations.

To ensure secure communication between the application and Shopware, this SDK supports signing mechanisms, allowing developers to validate the authenticity and integrity of requests and responses.

It also includes an HTTP client that simplifies making API requests to Shopware endpoints. It provides methods for handling authentication, executing HTTP requests, and processing responses.

Furthermore, it supports event handling, allowing developers to subscribe to and react to specific events triggered within the Shopware system. This enables the customization and extension of Shopware's functionality by executing custom logic when specific events occur.

Overall, the App SDK in PHP offers installation, lifecycle management, context handling, signing mechanisms, an HTTP client, and event handling capabilities. It provides a robust foundation for developing custom applications and plugins for the Shopware e-commerce platform using PHP.

---

## Getting started

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/01-getting_started.html

# Getting Started [​](#getting-started)

The app server written in PHP is an open-source project accessible at [app-php-sdk](https://github.com/shopware/app-php-sdk).

## Installation [​](#installation)

Install the Shopware APP SDK via composer:

bash

```shiki
composer require shopware/app-php-sdk
```

After the package installation, Composer will automatically install the http client if missing.

## Registration process [​](#registration-process)

php

```shiki
$app = new AppConfiguration('Foo', 'test', 'http://localhost:6001/register/callback');
// for a repository to save stores implementing \Shopware\App\SDK\Shop\ShopRepositoryInterface, see FileShopRepository as an example
$repository = ...;

// Create a psr 7 request or convert it (HttpFoundation Symfony)
$psrRequest = ...;

// you can also use the AppLifecycle see Lifecycle section
$registrationService = new \Shopware\App\SDK\Registration\RegistrationService($app, $repository);

$response = match($_SERVER['REQUEST_URI']) {
    '/app/register' => $registrationService->register($psrRequest),
    '/app/register/confirm' => $registrationService->registerConfirm($psrRequest),
    default => throw new \RuntimeException('Unknown route')
};

// return the response
```

With this code, you can register your app with our custom app backend.

Next, we will look into the [lifecycle handling](./02-lifecycle.html).

---

## Lifecycle

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/02-lifecycle.html

# Lifecycle [​](#lifecycle)

The Shopware App System manages the lifecycle of an app. Shopware will send any change if registered a webhook to our backend server.

To track the state in our Database correctly, we need to implement some lifecycle methods.

## Lifecycle Methods [​](#lifecycle-methods)

* `activate`
* `deactivate`
* `uninstall`

The lifecycle registration in the `manifest.xml` would look like this:

xml

```shiki
<webhooks>
    <webhook name="appActivate" url="https://app-server.com/app/activate" event="app.activated"/>
    <webhook name="appDeactivated" url="https://app-server.com/app/deactivated" event="app.deactivated"/>
    <webhook name="appDelete" url="https://app-server.com/app/delete" event="app.deleted"/>
</webhooks>
```

## Usage [​](#usage)

The implementation is similar to [Registration](./01-getting_started.html) and wraps the RegistrationService to inject only one controller for all lifecycle methods.

php

```shiki
$app = new AppConfiguration('Foo', 'test', 'http://localhost:6001/register/callback');
// for a repository to save stores implementing \Shopware\App\SDK\Shop\ShopRepositoryInterface, see FileShopRepository as an example
$repository = ...;

// Create a psr 7 request or convert it (HttpFoundation Symfony)
$psrRequest = ...;

$registrationService = new \Shopware\App\SDK\Registration\RegistrationService($app, $repository);
$shopResolver = new \Shopware\App\SDK\Shop\ShopResolver($repository);
$lifecycle = new \Shopware\App\SDK\AppLifecycle($registrationService, $shopResolver, $repository);

$response = match ($_SERVER['REQUEST_URI']) {
    '/app/register' => $lifecycle->register($psrRequest),
    '/app/register/confirm' => $lifecycle->registerConfirm($psrRequest),
    '/app/activate' => $lifecycle->activate($psrRequest),
    '/app/deactivate' => $lifecycle->deactivate($psrRequest),
    '/app/delete' => $lifecycle->delete($psrRequest),
    default => throw new \RuntimeException('Unknown route')
};

// return the response
```

So, in this case, our backend gets notified of any app change, and we can track the state in our database.

Next, we will look into the [Context resolving](./03-context.html).

---

## Context

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/03-context.html

# Context [​](#context)

The ContextResolver helps you map the Shopware requests to struct classes to work with them more easily. It also does some validation and checks if the request is valid.

## Usage [​](#usage)

php

```shiki
$app = new AppConfiguration('Foo', 'test', 'http://localhost:6001/register/callback');
// for a repository to save stores implementing \Shopware\App\SDK\Shop\ShopRepositoryInterface, see FileShopRepository as an example
$repository = ...;

// Create a psr 7 request or convert it (HttpFoundation Symfony)
$psrRequest = ...;

$registrationService = new \Shopware\App\SDK\Registration\RegistrationService($app, $repository);
$shopResolver = new \Shopware\App\SDK\Shop\ShopResolver($repository);

$contextResolver = new \Shopware\App\SDK\Context\ContextResolver();

// Find the actual shop by the request
$shop = $shopResolver->resolveShop($psrRequest);

// Parse the request as a webhook
$webhook = $contextResolver->assembleWebhook($psrRequest, $shop);

$webhook->eventName; // the event name
$webhook->payload; // the event data
```

## Supported requests [​](#supported-requests)

* [Webhook](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Webhook/WebhookAction.php) - Webhooks or App lifecycle events
* [ActionButton](https://github.com/shopware/app-php-sdk/blob/main/src/Context/ActionButton/ActionButtonAction.php) - Administration buttons
* [Module](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Module/ModuleAction.php) - Iframe
* [TaxProvider](https://github.com/shopware/app-php-sdk/blob/main/src/Context/TaxProvider/TaxProviderAction.php) - Tax calculation
* [Payment Pay](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Payment/PaymentPayAction.php) - Payment pay action
* [Payment Capture](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Payment/PaymentCaptureAction.php) - Payment capture action
* [Payment Validate](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Payment/PaymentValidateAction.php) - Payment validate action
* [Payment Finalize](https://github.com/shopware/app-php-sdk/blob/main/src/Context/Payment/PaymentFinalizeAction.php) - Payment finalize action

Next, we will look into the [Signing of responses](./04-signing.html).

---

## Signing

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/04-signing.html

# Signing of responses [​](#signing-of-responses)

The Shopware App System requires you to sign your responses to the Shopware server.

The signing is required for the following actions:

* ActionButton
* TaxProvider
* Payment

To sign the response, you need to create a `ResponseSigner` and call the `signResponse` method with our PSR 7 Response.

php

```shiki
$app = new AppConfiguration('Foo', 'test', 'http://localhost:6001/register/callback');
// for a repository to save stores implementing \Shopware\App\SDK\Shop\ShopRepositoryInterface, see FileShopRepository as an example
$repository = ...;

// Create a psr 7 request or convert it (HttpFoundation Symfony)
$psrRequest = ...;

$shopResolver = new \Shopware\App\SDK\Shop\ShopResolver($repository);

$shop = $shopResolver->resolveShop($psrRequest);

// do something
$response = ....;

$signer = new \Shopware\App\SDK\Authentication\ResponseSigner();
$signer->signResponse($psrResponse, $shop);
```

Next, we will look into the [Making HTTP requests to the Shop](./05-http-client.html).

---

## HTTP-client

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/05-http-client.html

# Making HTTP requests to the Shop [​](#making-http-requests-to-the-shop)

The SDK offers a simple HTTP client for sending requests to the Shopware server. To utilize it, you will require the Shop entity, which you can obtain by using the `shopResolver` from the current request. Alternatively, you can use the `ShopRepository` to obtain the Shop entity by its ID.

php

```shiki
$app = new AppConfiguration('Foo', 'test', 'http://localhost:6001/register/callback');
// for a repository to save stores implementing \Shopware\App\SDK\Shop\ShopRepositoryInterface, see FileShopRepository as an example
$repository = ...;

// Create a psr 7 request or convert it (HttpFoundation Symfony)
$psrRequest = ...;

$shopResolver = new \Shopware\App\SDK\Shop\ShopResolver($repository);

$shop = $shopResolver->resolveShop($psrRequest);

$clientFactory = new Shopware\App\SDK\HttpClient\ClientFactory();
$httpClient = $clientFactory->createClient($shop);

$response = $httpClient->sendRequest($psrHttpRequest);
```

The client will automatically fetch the OAuth2 token for the shop and add it to the request.

## SimpleHttpClient [​](#simplehttpclient)

The SimpleHttpClient is a wrapper around the PSR18 ClientInterface and provides a simple interface to make requests.

php

```shiki
$simpleClient = new \Shopware\App\SDK\HttpClient\SimpleHttpClient\SimpleHttpClient($httpClient);

$response = $simpleClient->get('https://shop.com/api/_info/version');
$response->getHeader('Content-Type'); // application/json
$response->ok(); // true when 200 <= status code < 300
$body = $response->json(); // json decoded body
echo $body['version'];

$simpleClient->post('https://shop.com/api/_action/sync', [
    'entity' => 'product',
    'offset' => 0,
    'total' => 100,
    'payload' => [
        [
            'id' => '123',
            'name' => 'Foo',
        ],
    ],
]);

// and the same with put, patch, delete
```

## Testing [​](#testing)

The `\Shopware\App\SDK\HttpClient\ClientFactory::factory` method accepts as a second argument a PSR18 ClientInterface. So you can overwrite the client with a mock client for testing.

php

```shiki
$clientFactory = new Shopware\App\SDK\HttpClient\ClientFactory();
$httpClient = $clientFactory->createClient($shop, $myMockClient);
```

Next, we will look into the [Events](./06-events.html).

---

## Events

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-sdks/php/06-events.html

# Events [​](#events)

The `Shopware\App\SDK\AppLifecycle` and `Shopware\App\SDK\Registration\RegistrationService` class accepts a PSR event dispatcher. When a PSR Dispatcher is passed, the following events will be fired:

* [BeforeShopActivateEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/BeforeShopActivateEvent.php)
* [ShopActivatedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/ShopActivatedEvent.php)
* [BeforeShopDeactivatedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/BeforeShopDeactivatedEvent.php)
* [ShopDeactivatedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/ShopDeactivatedEvent.php)
* [BeforeShopDeletionEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/BeforeShopDeletionEvent.php)
* [ShopDeletedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/ShopDeletedEvent.php)
* [BeforeRegistrationCompletedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/BeforeRegistrationCompletedEvent.php)
* [RegistrationCompletedEvent](https://github.com/shopware/app-php-sdk/blob/main/src/Event/RegistrationCompletedEvent.php)

With that event, you can react to several actions during the app lifecycle or a registration process to run your code.

---

