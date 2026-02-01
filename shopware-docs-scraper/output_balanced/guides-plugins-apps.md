# Guides Plugins Apps

*Scraped from Shopware Developer Documentation*

---

## Apps

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/

# Apps [​](#apps)

Apps are the extension mechanism designed for Shopware’s [Cloud environment](./../../../products/saas.html). Unlike [plugins](./../plugins/), they don't run code directly inside the shop system. Instead, they work in an event-driven way and communicate with external services through APIs. This makes them less intrusive while still highly flexible.

Apps are well-suited for use cases such as:

* Integrating with third-party services (e.g., ERP, CRM, marketing tools)
* Providing payment methods and forwarding to external payment providers
* Adding storefront customizations, including themes
* Handling data or processes outside the shop system (e.g., product synchronization, advanced shipping logic, analytics workflows)
* Extending or modifying core functionality such as checkout behavior, pricing and discount logic, payment flows, product catalog management, or search behavior
* Customizing the Storefront or Administration; creating custom themes, adding custom blocks or Storefront elements, or modifying the appearance and layout of the Administration panel
* Facilitating integration with external systems to allow seamless data synchronization, order and product management, and cross-platform workflows

You can develop apps using the Shopware [App SDK](./app-sdks/), [App Scripts](./app-scripts/), and external services via the [App API](./../../../resources/references/app-reference/). Apps offer a modular and scalable way to extend and customize the platform according to specific business requirements.

Follow our [App Base Guide](./app-base-guide/) and [App Starter Guide](./starter/) to learn how to develop an app.

INFO

Apps also provide theme support, so everything you can do with a theme plugin is also possible in an app. This makes them the preferred option for customizing design in Cloud shops.

To understand how apps differ from other extension types, see the [Overview table](./../../../guides/plugins/index/).

---

## App Base Guide

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-base-guide.html

# App Base Guide [​](#app-base-guide)

## Overview [​](#overview)

This guide will walk you through the process of adding your own app to Shopware and configuring it to be able to communicate with your external backend server.

## Prerequisites [​](#prerequisites)

If you are not familiar with the app system, take a look at the [App concept](./../../../concepts/extensions/apps-concept.html) first.

## Name your app [​](#name-your-app)

Choose a technical name for your application that accurately reflects its plugin functionality. Specify the name using UpperCamelCase. For instance: "PaymentGatewayApp".

However, throughout this section "MyExampleApp" is used as it serves as an illustrative example of the plugin.

## File structure [​](#file-structure)

To get started with your app, create an `apps` folder inside the `custom` folder of your Shopware dev installation. In there, create another folder for your application and provide a manifest file in it.

text

```shiki
└── custom
    ├── apps
    │   └── MyExampleApp
    │       └── manifest.xml
    └── plugins
```

## Manifest file [​](#manifest-file)

The manifest file is the central point of your app. It defines the interface between your app and the Shopware instance. It provides all the information concerning your app, as seen in the minimal version below:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>MyExampleApp</name>
        <label>Label</label>
        <label lang="de-DE">Name</label>
        <description>A description</description>
        <description lang="de-DE">Eine Beschreibung</description>
        <author>Your Company Ltd.</author>
        <copyright>(c) by Your Company Ltd.</copyright>
        <version>1.0.0</version>
        <icon>Resources/config/plugin.png</icon>
        <license>MIT</license>
    </meta>
</manifest>
```

WARNING

The name of your app that you provide in the manifest file needs to match the folder name of your app.

The app can now be installed and activated by running the following command:

bash

```shiki
bin/console app:install --activate MyExampleApp
```

After activating an app, you might need to clear the cache for the changes to take effect. First try:

bash

```shiki
bin/console cache:clear
```

If the changes are still not visible, try:

bash

```shiki
bin/console cache:clear:http
```

or

bash

```shiki
bin/console cache:clear:all
```

By default, your app files will be [validated](./app-base-guide.html#validation) before installation. To skip the validation, you may use the `--no-validate` flag.

INFO

Without the `--activate` flag the Apps get installed as inactive. By executing the `app:activate` command after installation this can be activated, too.

For a complete reference of the manifest file structure, take a look at the [Manifest reference](./../../../resources/references/app-reference/manifest-reference.html).

## Setup (optional) [​](#setup-optional)

INFO

Only if your app backend server and Shopware need to communicate, it is necessary that registration is performed during the installation of your app. This process is called setup.

WARNING

Suppose your app makes use of the Admin Module, Payment Method, Tax providers or Webhook app system features. In that case, you need to implement the registration, to exchange a secret key; that is later used to authenticate the shops.

During the setup, it is verified that Shopware connects to the right backend server and keys are exchanged to secure all further communications. During the setup process, your app backend will get credentials that can be used to authenticate against the Shopware API. Additionally, your app will provide a secret that Shopware will use to sign all further requests it makes to your app backend, allowing you to verify that the incoming requests originate from authenticated Shopware installations.

The setup workflow is shown in the following schema. Each step will be explained in detail.

![Setup request workflow](/assets/plugins-apps-appBaseGuide.D7L2OL3t.svg)

INFO

The timeout for the requests against the app server is 5 seconds.

### SDK Integration [​](#sdk-integration)

Integrating apps into your application can be a daunting task, but with our PHP SDK, the process becomes much easier. Our SDK simplifies the registration flow and other typical tasks.

* [Official PHP SDK](./app-sdks/php/01-getting_started.html)
* [Official Symfony Bundle](./app-sdks/symfony-bundle/index.html)

If there is no SDK available for your language, you can implement the registration process by yourself.

### Registration request [​](#registration-request)

The registration request is made as a `GET` request against a URL you provide in your app's manifest file.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <setup>
        <!-- The URL which will be used for the registration -->
        <registrationUrl>https://my.example.com/registration</registrationUrl>
        <!-- Dev only, the secret that is used to sign the registration request -->
        <secret>mysecret</secret>
    </setup>
</manifest>
```

The following query parameters will be sent with the request:

* `shop-id`: The unique identifier of the shop the app was installed.
* `shop-url`: The URL of the shop, this can later be used to access the Shopware API.
* `timestamp`: The Unix timestamp when the request was created.

Additionally, the request has the following headers:

* `shopware-app-signature`: The signature of the query string
* `sw-version`: The Shopware version of the shop *(since 6.4.1.0)*

An example request looks like this:

txt

```shiki
GET https://my.example.com/registration?shop-id=KIPf0Fz6BUkN&shop-url=http%3A%2F%2Fmy.shop.com&timestamp=159239728
shopware-app-signature: a8830aface4ac4a21be94844426e62c77078ca9a10f694737b75ca156b950a2d
sw-version: 6.4.5.0
```

Additionally, the `shopware-app-signature` header will be provided, which contains a cryptographic signature of the query string.  
 The secret used to generate this signature is the `app secret`, which is unique per app and will be provided by the Shopware Account if you upload your app to the store. This secret won't leave the Shopware Account, so it won't even be leaked to the shops installing your app.

DANGER

You and the Shopware Account are the only parties that should know your `app-secret`. Therefore, make sure you never accidentally publish your `app-secret`.

WARNING

For **local development**, you can specify a `<secret>` in the manifest file that is used for signing the registration request. However, if an app uses a hard-coded secret in the manifest, it can't be uploaded to the store.

If you are developing a **private app** not published in the Shopware Store, you **must** provide the `<secret>` in case of an external app server.

To verify that the registration can only be triggered by authenticated Shopware shops, you need to recalculate the signature and check that the signatures match. Thus, you have verified that the sender of the request possesses the `app secret`.

The following code snippet can be used to recalculate the signature:

### Registration response [​](#registration-response)

There may be valid cases where the app installation fails because the domain is blocked or some other prerequisite in that shop is not met, in which case you can return the message error as follows:

json

```shiki
{
  "error": "The shop URL is invalid"
}
```

When the registration is successful. To verify that you are also in possession of the `app secret`, you need to provide proof that it is signed with the `app secret` too. The proof consists of the sha256 hmac of the concatenated `shopId`, `shopUrl`, and your app's name.

The following code snippet can be used to calculate the proof:

For detailed instructions on signing requests and responses, refer to the app signing guide.

[Signing & Verification in the App System](app-signature-verification)

Besides the proof, your app needs to provide a randomly generated secret that should be used to sign every further request from this shop. Make sure to save the `shopId`, `shopUrl`, and generated secret so that you can associate and use this information later.

INFO

This secret will be called `shop-secret` to distinguish it from the `app-secret`. The `app-secret` is unique to your app and is used to sign the registration request of every shop that installs your app. The `shop-secret` will be provided by your app during the registration and should be unique for every shop and have a minimum length of 64 characters and maximum length of 255 characters.

The last thing needed in the registration response is a URL to which the confirmation request will be sent.

A sample registration response looks like this:

json

```shiki
{
  "proof": "94b42d39280141de84bd6fc8e538946ccdd182e4558f1e690eabb94f924e7bc7",
  "secret": "random secret string",
  "confirmation_url": "https://my.example.com/registration/confirm"
}
```

### Confirmation request [​](#confirmation-request)

If the proof you provided in the [registration response](./app-base-guide.html#registration-response) matches the one generated on the shop side, the registration is completed. As a result, your app will receive a `POST` request against the URL specified as the `confirmation_url` of the registration with the following parameters send in the request body:

* `apiKey`: The API key used to authenticate against the Shopware Admin API.
* `secretKey`: The secret key used to authenticate against the Shopware Admin API.
* `timestamp`: The Unix timestamp when the request was created.
* `shopUrl`: The URL of the shop.
* `shopId`: The unique identifier of the shop.

The payload of that request may look like this:

json

```shiki
{
  "apiKey":"SWIARXBSDJRWEMJONFK2OHBNWA",
  "secretKey":"Q1QyaUg3ZHpnZURPeDV3ZkpncXdSRzJpNjdBeWM1WWhWYWd0NE0",
  "timestamp":"1592398983",
  "shopUrl":"http:\/\/my.shop.com",
  "shopId":"sqX6cqHi6hbj"
}
```

Make sure that you save the API credentials for that `shopId`. You can use the `apiKey` and the `secretKey` as `client_id` and `client_secret`, respectively, when you request an OAuth token from the Admin API.

You can find out more about how to use these credentials in our Admin API authentication guide:

[Admin API Authentication & Authorisation](https://shopware.stoplight.io/docs/admin-api/authentication#integration-client-credentials-grant-type)

INFO

Starting from Shopware version 6.4.1.0, the current Shopware version will be sent as a `sw-version` header. Starting from Shopware version 6.4.5.0, the current language id of the Shopware context will be sent as a `sw-context-language` header, and the locale of the user or locale of the context language is available under the `sw-user-language` header.

The request is signed with the `shop-secret` that your app provided in the [registration response](./app-base-guide.html#registration-response) and the signature can be found in the `shopware-shop-signature` header.  
 You need to recalculate that signature and check that it matches the provided one to make sure that the request is really sent from the shop with that shopId.

You can use the following code snippet to generate the signature:

## Permissions [​](#permissions)

Shopware comes with the possibility to create fine-grained [Access Control Lists](./../plugins/administration/permissions-error-handling/add-acl-rules.html) (ACLs). It means you need to request permissions if your app needs to read or write data over the API or wants to receive webhooks. The permissions your app needs are defined in the manifest file and are composed of the privilege (`read`, `create`, `update`, `delete`) and the entity. Since version 6.4.12.0, your app can also request additional non-CRUD privileges with the `<permission>` element.

For entities that need all CRUD operations (create, read, update, delete), you can use the `<crud>` shortcut element instead of declaring each permission individually:

* `<crud>product</crud>` automatically grants `read`, `create`, `update`, and `delete` permissions for the product entity

INFO

The `<crud>` shortcut element is available since version 6.7.3.0. If your app needs to support earlier Shopware versions, use the individual permission elements (`read`, `create`, `update`, `delete`) instead.

Sample permissions using the CRUD shortcut for products, individual permission for orders, as well as reading the cache configuration look like this:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <permissions>
        <read>product</read>
        <create>product</create>
        <update>product</update>

        <delete>order</delete>

        <!-- Since version 6.4.12.0 your app can request additional non-CRUD privileges-->
        <permission>system:cache:info</permission>
    </permissions>
</manifest>
```

The permissions you request need to be accepted by the user during the installation of your app. After that, these permissions are granted for your app and your API access through the credentials from the [confirmation request](./app-base-guide.html#confirmation-request) of the [setup workflow](./app-base-guide.html#setup) are limited to those permissions.

WARNING

Keep in mind that read permissions also extend to the data contained in the requests, so your app needs read permissions for the entities contained in the subscribed [webhooks](./webhook.html).

### App notification [​](#app-notification)

Starting from Shopware version 6.4.7.0, if you want to send notifications to the admin to inform the user about some actions that happened on the app side, the app should send a `POST` request to the `api/notification` endpoint with a valid body and the header `Authorization` token. Your app can request 10 times before being delayed by the system.

After 10 attempts, you need to wait 10 seconds before trying to make requests again. After 15 attempts, it's 30 seconds. After 20 attempts, it's 60 seconds. After 24 hours without a failed request, the limit is reset.

Examples request body: You need to pass the `status` property, the content of the notification as `message` property, and you can restrict users who can read the notification by passing `requiredPrivileges` property and `adminOnly` property inside the payload. When `adminOnly` is true, only admins can read this notification. If you don't send the `adminOnly` or `adminOnly` is false, you can pass the `requiredPrivileges` property so that users with specific permissions can read the notification. Otherwise, it will be displayed to every user.

txt

```shiki
POST /api/notification

{
    "status": "success",
    "message": "This is a successful message",
    "adminOnly": "true",
    "requiredPrivileges": []
}
```

* `status`: Notification status - `success`, `error`, `info`, `warning`.
* `message`: The content of the notification.
* `adminOnly`: Only admins can read this notification if this value is true.
* `requiredPrivileges`: The required privileges that users need to have to read the notification.

Remember that your app needs the `notification:create` permission to access this API.

### App lifecycle events [​](#app-lifecycle-events)

Apps can also register to lifecycle events of their own lifecycle, namely their installation, updates, and deletion. For example, they may be used to delete user relevant data from your data stores once somebody removes your app from their shop.

| Event | Description |
| --- | --- |
| `app.installed` | Triggers once the app is installed |
| `app.updated` | Triggers if the app is updated |
| `app.deleted` | Triggers once the app is removed |
| `app.activated` | Triggers if an inactive app is activated |
| `app.deactivated` | Triggers if an active app is deactivated |

#### App lifecycle events for app scripts [​](#app-lifecycle-events-for-app-scripts)

Since Shopware 6.4.9.0, it is also possible to create [App scripts](./app-scripts/) that are executed during the lifecycle of your app. You get access to the database and can change or create some data, e.g., when your app is activated, without needing an external server.

For a full list of the available hook points and the available services, refer to the [reference documentation](./../../../resources/references/app-reference/script-reference/script-hooks-reference.html#app-lifecycle).

## Validation [​](#validation)

You can run the `app:validate` command to validate the configuration of your app. It will check for common errors, like:

* non-matching app names
* missing translations
* unknown events registered as webhooks
* missing permissions for webhooks
* errors in the config.xml file, if it exists

To validate all apps in your `custom/apps` folder run:

bash

```shiki
bin/console app:validate
```

Additionally, you can specify which app should be validated by providing the app name as an argument;

bash

```shiki
bin/console app:validate MyExampleApp
```

## Handling the migration of shops [​](#handling-the-migration-of-shops)

In the real world, it may happen that shops are migrated to new servers and are available under a new URL. In the same regard, it is possible that a running production shop is duplicated and treated as a staging environment. These cases are challenging for app developers. In the first case, you may have to make a request against the shop, but the URL you saved during the registration process may not be valid anymore, and the shop cannot be reached over this URL. In the second case, you may receive webhooks from both shops (prod & staging) that look like they came from the same shop (as the whole database was duplicated). Thus, it may corrupt the data associated with the original production shop. The main reason that this is problematic is that two Shopware installations in two different locations (on two different URLs) are associated with the same shopId, because the whole database was replicated.

That is why we implemented a safeguard mechanism that detects such situations, stops communication with the apps to prevent data corruption, and then ultimately lets the user decide how to solve the situation.

INFO

This mechanism relies on the fact that the `APP_URL` environment variable will be set to the correct URL for the shop. It is especially assumed that the environment variable will be changed when a shop is migrated to a new domain or a staging shop is created as a duplicate of a production shop.

Remember that this is only relevant for apps that have their own backends and where communication between app backends and shopware is necessary. That is why simple themes are not affected by shop migrations, and they will continue to work.

### Detecting APP\_URL changes [​](#detecting-app-url-changes)

Every time a request should be made against an app backend, Shopware will check whether the current APP\_URL differs from the one used when Shopware generated an ID for this shop. If the APP\_URL differs, Shopware will stop sending any requests to the installed apps to prevent data corruption on the side of the apps. Now the user has the possibility to resolve the solution by using one of the following strategies. The user can either run a strategy with the `bin/console app:url-change:resolve` command, or with a modal that pops up when the Administration is opened.

### APP\_URL change resolver [​](#app-url-change-resolver)

* **MoveShopPermanently**: This strategy should be used if the live production shop is migrated from one URL to another one. This strategy will ultimately notify all apps about the change of the APP\_URL and the apps will continue working like before, including all the data the apps may already have associated with the given shop. It is important to notice that in this case, the apps in the old installation on the old URL (if it is still running) will stop working.

Technically, this is achieved by rerunning the registration process for all apps. During the registration, the same shopId is used as before, but now with a different shop-url and a different key pair used to communicate over the Shopware API. Also, you must generate a new communication secret during this registration process that is subsequently used to communicate between Shopware and the app backend.

This way, it is ensured that the apps are notified about the new URL and the integration with the old installation stops working, because a new communication secret is associated with the given shopId that the old installation does not know.

* **ReinstallApps**: This strategy makes sense to use in the case of the staging shop. By running this strategy, all installed apps will be reinstalled. This means that this installation will get a new shopId, that is used during registration.

As the new installation will get a new shopId, the installed apps will continue working on the old installation as before, but as a consequence, the data on the app's side that was associated with the old shopId cannot be accessed on the new installation.

* **UninstallApps**: This strategy will simply uninstall all apps on the new installation, thus keeping the old installation working like before.

## API Docs [​](#api-docs)

### Registration [​](#registration)

`GET https://my.example.com`

#### Parameters [​](#parameters)

| Parameter | Type | Description |
| --- | --- | --- |
| **Query** |  |  |
| timestamp\* | integer | The current Unix timestamp when the request was created |
| shop-url\* | string | The URL of the shop where the app was installed can be used to access to the Shopware API |
| shop-id\* | string | The unique identifier of the shop, where the app was installed |
| **Header** |  |  |
| shopware-app-signature\* | string | The hmac-signature of the query string, signed with the app secret |

#### Responses [​](#responses)

`200`

json

```shiki
{
  "error": "The shop URL is invalid"
}
```

json

```shiki
{
  "proof": "94b42d39280141de84bd6fc8e538946ccdd182e4558f1e690eabb94f924e7bc7",
  "secret": "random secret string",
  "confirmation_url": "https://my.example.com/registration/confirm"
}
```

### Confirmation [​](#confirmation)

`POST https://my.example.com`

#### Parameters [​](#parameters-1)

| Parameter | Type | Description |
| --- | --- | --- |
| **Header** |  |  |
| shopware-shop-signature\* | string | The hmac-signature of the body content, signed with the shop secret returned from the registration request |
| sw-version\* | string | Starting from Shopware version 6.4.1.0, the current Shopware version will be sent as a `sw-version` header. Starting from Shopware version 6.4.5.0, the current language id of the Shopware context will be sent as a `sw-context-language` header, and the locale of the user or locale of the context language is available under the `sw-user-language` header. |
| **Body** |  |  |
| shopId\* | string | The unique identifier of the shop |
| shopUrl\* | string | The URL of the shop |
| timestamp\* | integer | The current nix timestamp when the request was created |
| secretKey\* | string | SecretKey used to authenticate against the Shopware API |
| apiKey\* | string | ApiKey used to authenticate against the Shopware API |

#### Responses [​](#responses-1)

`200`

---

## Configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/configuration.html

# Configuration [​](#configuration)

INFO

Configurations for apps adhere to the same schema as [Plugin Configurations](./../plugins/plugin-fundamentals/add-plugin-configuration.html).

To offer configuration possibilities to your users you can provide a `config.xml` file that describes your configuration options. You can find detailed information about the possibilities and the structure of the `config.xml` in the according documentation page. To include a `config.xml` file in your app put it into the `Resources/config` folder:

text

```shiki
...
└── DemoApp
      └── Resources
            └── config  
                  └── config.xml
      └── manifest.xml
```

The configuration page will be displayed in the Administration under `Extensions > My extensions`. For development purposes you can use the Administration component to configure plugins to provide configuration for your app, therefore use the URL `{APP_URL}/admin#/sw/extension/config/{appName}`.

## Reading the configuration values [​](#reading-the-configuration-values)

The configuration values are saved as part of the `SystemConfig` and you can use the key `{appName}.config.{fieldName}` to identify the values. There are two possibilities to access the configuration values from your app. If you need those values on your app-backend server, you can read them over the API. If you need the configuration values in your Storefront twig templates you can use the `systemConfig()`-twig function.

### Reading the config over the API [​](#reading-the-config-over-the-api)

To access your apps configuration over the API make a GET request against the `/api/_action/system-config` route. You have to add the prefix for your configuration as the `domain` query parameter. Optionally you can provide a `SalesChannelId`, if you want to read the values for a specific SalesChannel, as the `salesChannelId` query param. The API call will return a JSON-Object containing all of your configuration values. A sample Request and Response may look like this.

txt

```shiki
GET /api/_action/system-config?domain=DemoApp.config&salesChannelId=98432def39fc4624b33213a56b8c944d

{
    "DemoApp.config.field1": true,
    "DemoApp.config.field2": "successfully configured"
}
```

WARNING

Keep in mind that your app needs the `system_config:read` permission to access this API.

### Writing the config over the API [​](#writing-the-config-over-the-api)

To write your app's configuration over the API, make a `POST`request against the `/api/_action/system-config` route. You have to provide the configurations as JSON object and optionally provide a `salesChannelId` query param, if you want to write the values for a specific Sales Channel.

txt

```shiki
POST /api/_action/system-config?salesChannelId=98432def39fc4624b33213a56b8c944d
Content-Type: application/json

{
    "DemoApp.config.field1": true
}
```

WARNING

Keep in mind that your app needs the `system_config:update`, `system_config:create` and `system_config:delete` permission to access this API.

### Reading the config in templates [​](#reading-the-config-in-templates)

Inside twig templates you can use the twig function `config` (see [Shopware Twig functions](./../../../resources/references/storefront-reference/twig-function-reference.html)). An example twig template could look like this:

twig

```shiki
{{ config('DemoApp.config.field1') }}
```

### Reading the config in app scripts [​](#reading-the-config-in-app-scripts)

In app scripts you have access to the [`config` service](./../../../resources/references/app-reference/script-reference/miscellaneous-script-services-reference.html#SystemConfigFacade), that can be used to access config values.

INFO

Note that app scripts were introduced in Shopware 6.4.8.0, and are not supported in previous versions.

The `config` service provides an `app()` method, that can be used to access your app's configuration. When using this method you don't need to provide the `{appName}.config` prefix and your app does not need any additional permissions.

twig

```shiki
{% set configValue = services.config.app('field1') %}
```

Additionally, you can use the `get()` method, to access any configuration value and not just the ones of your app.

WARNING

Keep in mind that your app needs the `system_config:read` permission to use the `config.get()` method.

twig

```shiki
{% set configValue = services.config.get('core.listing.productsPerPage') %}
```

For a detailed description about app scripts refer to this [guide](./app-scripts/).

For a full description of the `config` service take a look at the [service's reference](./../../../resources/references/app-reference/script-reference/miscellaneous-script-services-reference.html#servicesconfig-shopwarecoresystemsystemconfigfacadesystemconfigfacade).

---

## Tax provider

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/tax-provider.html

# Tax provider [​](#tax-provider)

Tax calculations differ from country to country. Especially in the US, the sales tax calculation can be tedious, as the laws and regulations differ from state to state, country-wise, or even based on cities. Therefore, most shops use a third-party service (so-called tax provider) to calculate sales taxes.

With version 6.5.0.0, Shopware allows apps to integrate custom tax calculations, which could include an automatic tax calculation with a tax provider. An app has to provide an endpoint, which is called during the checkout to provide new tax rates. The requests and responses of all of your endpoints will be signed and featured as JSON content.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App Base Guide](app-base-guide)

Your app server must be also accessible for the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration [​](#manifest-configuration)

To indicate to Shopware that your app uses a custom tax calculation, you must provide one or more `tax-provider` properties inside a `tax` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working tax provider.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>
    <tax>
        <tax-provider>
            <!-- Unique identifier of the tax provider -->
            <identifier>myCustomTaxProvider</identifier>
            <!-- Display name of the tax provider -->
            <name>My custom tax provider</name>
            <!-- Priority of the tax provider - can be changed in the administration as well -->
            <priority>1</priority>
            <!-- Url of your implementation - is called during checkout to provide taxes -->
            <process-url>https://tax-provider.app/provide-taxes</process-url>
        </tax-provider>
    </tax>
</manifest>
```

After successful installation of your app, the tax provider will already be used during checkout to provide taxes. You should also see the new tax provider showing up in the administration in `Settings > Tax`.

## Tax provider endpoint [​](#tax-provider-endpoint)

During checkout, Shopware checks for any active tax providers - sorted by priority - and will call the `processUrl` to provide taxes one-by-one, until one of endpoint successfully provides taxes for the current cart.

WARNING

**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds. Be sure, that your tax provider implementation responds in time, otherwise Shopware will time out and drop the connection.

In response, you can adjust the taxes of the entire cart, the entire delivery, or each item in the cart.

If you wish to use a tax provider, you will probably have to provide the whole cart for the tax provider to correctly calculate taxes during checkout and you will probably get sums of the specific tax rates, which you can respond to Shopware via `cartPriceTaxes`. If given, Shopware does not recalculate the tax sums and will use those given by your tax provider.

---

## Payment

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/payment.html

# Payment [​](#payment)

Starting with version `6.4.1.0`, Shopware also provides functionality for your app to be able to integrate payment providers. You can choose between just a simple request for approval in the background (synchronous payment) and the customer being forwarded to a provider for payment (asynchronous payment). You provide one or two endpoints, one for starting the payment and providing a redirect URL and one for finalization to check for the resulting status of the payment. The requests and responses of all of your endpoints will be signed and feature JSON content.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App Base Guide](app-base-guide)

Your app server must be also accessible for the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration [​](#manifest-configuration)

If your app should provide one or multiple payment methods, you need to define these in your manifest. The created payment methods in Shopware will be identified by the name of your app and the identifier you define per payment method. You should therefore not change the identifier after release, otherwise new payment methods will be created.

You may choose between a synchronous and an asynchronous payment method. These two types are differentiated by defining a `finalize-url` or not. If no `finalize-url` is defined, the internal Shopware payment handler will default to a synchronous payment. If you do not want or need any communication during the payment process with your app, you can also choose not to provide a `pay-url`, then the payment will remain on open on checkout.

Below, you can see different definitions of payment methods.

Depending on the URLs you provide, Shopware knows which kind of payment flow your payment method supports.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise, all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>

    <payments>
        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>asynchronousPayment</identifier>
            <name>Asynchronous payment</name>
            <name lang="de-DE">Asynchrone Zahlung</name>
            <description>This payment method requires forwarding to payment provider.</description>
            <description lang="de-DE">Diese Zahlungsmethode erfordert eine Weiterleitung zu einem Zahlungsanbieter.</description>
            <pay-url>https://payment.app/async/pay</pay-url>
            <finalize-url>https://payment.app/async/finalize</finalize-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>synchronousPayment</identifier>
            <name>Synchronous payment</name>
            <name lang="de-DE">Synchrone Zahlung</name>
            <description>This payment method does everything in one request.</description>
            <description lang="de-DE">Diese Zahlungsmethode arbeitet in einem Request.</description>
            <!-- This URL is optional for synchronous payments (see below). -->
            <pay-url>https://payment.app/sync/pay</pay-url>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>simpleSynchronousPayment</identifier>
            <name>Simple Synchronous payment</name>
            <name lang="de-DE">Einfache synchrone Zahlung</name>
            <description>This payment will not do anything and stay on 'open' after order.</description>
            <description lang="de-DE">Diese Zahlungsmethode wird die Transaktion auf 'offen' belassen.</description>
            <!-- No URL is provided. -->
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>preparedPayment</identifier>
            <name>Payment, that offers everything</name>
            <name lang="de-DE">Eine Zahlungsart, die alles kann</name>
            <validate-url>https://payment.app/validate</validate-url>
            <pay-url>https://payment.app/pay</pay-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>refundPayment</identifier>
            <name>Refund payments</name>
            <name lang="de-DE">Einfache Erstattungen</name>
            <refund-url>https://payment.app/refund</refund-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>recurringPayment</identifier>
            <name>Recurring payments</name>
            <name lang="de-DE">Einfache wiederkehrende Zahlungen</name>
            <recurring-url>https://payment.app/recurring</recurring-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>
    </payments>
</manifest>
```

## Synchronous payments [​](#synchronous-payments)

INFO

Be aware, that from Shopware 6.7.0.0 onwards your app-server **has to** respond with a payment state in its response, if you intend to change the transaction state.

There are different types of payments. Synchronous payment is the simplest of all and does not need any additional interaction with the customer. If you have defined a `pay-url`, you can choose to be informed about and possibly process the payment or not. If you do not need to communicate with your app, you can stop reading here and the transaction will stay open. But if you do define a `pay-url`, you can respond to the request with a different transaction status like authorize, paid, or failed. This is useful if you want to add a payment provider that only needs the information if the customer has already provided it in the checkout process or not. For example, a simple credit check for payment upon invoice. Below you can see an example of a simple answer from your app to mark a payment as authorized.

## Asynchronous payments [​](#asynchronous-payments)

INFO

Be aware, that from Shopware 6.7.0.0 onwards your app-server **has to** respond with a payment state in its response, if you intend to change the transaction state.

Asynchronous payments are more complicated than synchronous payments. They require interaction with the customer and a redirect to the payment provider, such as PayPal or Stripe.

Here is how it works:

* Shopware sends the first pay `POST` request to start the payment with the payment provider. The request includes all necessary data such as the `order`, `orderTransaction`, and a `returnUrl`, where the customer should be redirected once the payment process with the payment provider has been finished.
* Your app server returns a response with a `redirectUrl` to the payment provider.
* The browser will be redirected to this URL and processes his order, and the payment provider will redirect the customer back to the `returnUrl` provided in the first request.
* Shopware sends a second `POST` request to the `finalize-url` with the `orderTransaction` and all the query parameters passed by the payment provider to Shopware.
* Your app server responds with a `status` and, if necessary a `message`, like in the synchronous payment.

The second `finalize` POST request will be called once the customer has been redirected back to the shop. This second request is only provided with the `orderTransaction` for identification purposes and `requestData` with all query parameters passed by the payment provider. The response `status` value determines the outcome of the payment, e.g.:

| Status | Description |
| --- | --- |
| `cancel` | Customer has aborted the payment at the payment provider's site |
| `fail` | Payment has failed (e.g. missing funds) |
| `paid` | Successful immediate payment |
| `authorize` | Delayed payment |

## Prepared payments [​](#prepared-payments)

With Shopware `6.4.9.0`, you can use prepared payments to enhance your checkout process beyond forwarding to a payment provider. This feature enables you to integrate more deeply into the checkout process. This method allows you to prepare the payment before placing the order, e.g., with credit card fields on the checkout confirmation page. Once you add specific parameters to the order placement request in the Storefront, which is also known as the checkout confirmation form, you can pass these parameters to your prepared payment handler. This enables your payment handler to capture the payment successfully when the order is placed.

For this, you have two calls available during the order placement, the `validate` call to verify, that the payment reference is valid and if not, stop the placement of the order, and the `pay` call, which then allows the payment to be processed to completion after the order has been placed and persisted.

Let's first talk about the `validate` call. Here, you will receive three items to validate your payment. The `cart` with all its line items, the `requestData` from the `CartOrderRoute` request and the current `salesChannelContext`. This allows you to validate, if the payment reference you may have given your payment handler via the Storefront implementation is valid and will be able to be used to pay the order which is about to be placed. The array data you may send as the `preOrderPayment` object in your response will be forwarded to your `pay` call, so you don't have to worry about identifying the order by looking at the cart from the `validate` call. If the payment is invalid, either return a response with an error response code or provide a `message` in your response.

INFO

Be aware, that from Shopware 6.7.0.0 onwards your app-server **has to** respond with a payment state in its response, if you intend to change the transaction state.

If the payment has been validated and the order has been placed, you then receive another call to your `pay` endpoint. You will receive the `order`, the `orderTransaction` and also the `preOrderPayment` array data, that you have sent in your validate call.

WARNING

Keep in mind that if the integration into the checkout process does not work as expected, your customer might not be able to use the prepared payment. This is especially valid for after order payments, since there the order already exists. For these cases, you should still offer a traditional synchronous / asynchronous payment flow. Don't worry, if you have set the transaction state in your capture call to anything but open, the asynchronous payment process will not be started immediately after the prepared payment flow.

## Refund [​](#refund)

With Shopware `6.4.12.0`, we have also added basic functionality to be able to refund payments. Your app will need to register captured amounts and create and persist a refund beforehand for Shopware to be able to process a refund of a capture.

Similar to the other requests, on your `refund` call you will receive the data required to process your refund. This is the `order` with all its details and also the `refund` which holds the information on the `amount`, the referenced `capture` and, if provided, a `reason` and specific `positions` which items are being refunded.

INFO

Be aware, that from Shopware 6.7.0.0 onwards your app-server **has to** respond with a payment state in its response, if you intend to change the transaction state.

## Recurring captures [​](#recurring-captures)

INFO

Recurring orders and payments require the Subscriptions feature, available exclusively in our [paid plans](https://www.shopware.com/en/pricing/).

Recurring payments are a special case of payment that is used for handling recurring orders, such as subscriptions. The request and response payloads are similar to the synchronous payment flow. At this point, a valid running billing agreement between the customer and the PSP should exist. Use any of the other payment flows to capture the initial order and create such an agreement during the checkout. Afterward, this flow can capture the payment for every recurring payment order.

INFO

Be aware, that from Shopware 6.7.0.0 onwards your app-server **has to** respond with a payment state in its response, if you intend to change the transaction state.

## All possible payment states [​](#all-possible-payment-states)

The following lists are all possible payment state options:

* `open` - The payment is open and can be processed
* `paid` - The payment has been paid
* `cancelled` - The payment has been canceled
* `refunded` - The payment has been refunded
* `failed` - The payment has failed
* `authorize` - The payment has been authorized
* `unconfirmed` - The payment has not been confirmed yet
* `in_progress` - The payment is in progress
* `reminded` - The payment has been reminded
* `chargeback` - The payment has been charged back

## All possible refund states [​](#all-possible-refund-states)

The following lists are all possible refund state options:

* `open` - The refund is open and can be processed
* `in_progress` - The refund is in progress
* `cancelled` - The refund has been canceled
* `failed` - The refund has failed
* `completed` - The refund has been refunded

## API docs [​](#api-docs)

You can further take a look at [Payment references](./../../../resources/references/app-reference/payment-reference.html).

---

## Webhook

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/webhook.html

# Webhook [​](#webhook)

With webhooks, you can subscribe to events occurring in Shopware. Whenever such an event occurs, a `POST` request will be sent to the URL specified for this particular event.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, especially their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server, as that is required to authenticate the webhooks coming from the shops and showing the correct content in your modules.

[App Base Guide](app-base-guide)

## Webhook configuration [​](#webhook-configuration)

To use webhooks in your app, you need to implement a `<webhooks>` element in your manifest file as shown below:

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <webhooks>
        <webhook name="product-changed" url="https://example.com/event/product-changed" event="product.written"/>
    </webhooks>
</manifest>
```

This example illustrates how to define a webhook with the name `product-changed` and the URL `https://example.com/event/product-changed`, which will be triggered if the event `product.written` is fired. So every time a product is changed, your custom logic will get executed. Further down, you will find a list of the most important events you can hook into.

An event contains as much data as is needed to react to that event. The data is sent as JSON in the request body:

The `source` property contains all necessary information about the Shopware instance that sent the request:

* `url` is the URL under which your app can reach the Shopware instance and its API.
* `appVersion` is the version of the app that is installed.
* `shopId` is the id by which you can identify the Shopware instance.
* `eventId` is a unique identifier of the event. This id will not change if sending of the webhook is retried, etc. **Since 6.4.11.0**.

The next property, `data` contains the name of the event so that a single endpoint can handle several different events. `data` also contains the event data in the `payload` property. Due to the asynchronous nature of these webhooks, the `payload` for `entity.written` events does not contain complete entities as these might become outdated. Instead, the entity in the payload is characterized by its id, stored under `primaryKey`, so the app can fetch additional data through the shop API. This also has the advantage of giving the app explicit control over the associations that get fetched instead of relying on the associations determined by the event. Other events, in contrast, contain the entity data that defines the event but keep in mind that the event might not contain all associations.

The next property, `timestamp` is the time at which the webhook was handled. This can be used to prevent replay attacks, as an attacker cannot change the timestamp without making the signature invalid. If the timestamp is too old, your app should reject the request. This property is only available from 6.4.1.0 onwards

INFO

Starting from Shopware version 6.4.1.0, the current Shopware version will be sent as a `sw-version` header. Starting from Shopware version 6.4.5.0, the current language id of the shopware context will be sent as a `sw-context-language` header, and the locale of the user or locale of the context language is available under the `sw-user-language` header.

You can verify the authenticity of the incoming request by checking the `shopware-shop-signature` every request should have a SHA256 HMAC of the request body that is signed with the secret your app assigned the shop during the [registration](./app-base-guide.html#setup). The mechanism to verify the request is exactly the same as the one used for the [confirmation request](./app-base-guide.html#confirmation-request).

You can use a variety of events to react to changes in Shopware that way. See that table [Webhook-Events-Reference](./../../../resources/references/app-reference/webhook-events-reference.html) for an overview.

## Webhooks for live version only [​](#webhooks-for-live-version-only)

INFO

This feature has been introduced with Shopware version 6.5.7.0

There might be cases when you only want to call the webhook when an entry is written to the database with live version ID (`Shopware\Core\Defaults::LIVE_VERSION`). For example when orders are created, you want to filter out drafts and only call your webhook when an order is actually placed. See more on versioning entities [here](./../plugins/framework/data-handling/versioning-entities.html).

You can achieve this by adding the option `onlyLiveVersion` to your webhook definition in the manifest file:

xml

```shiki
<webhook name="order-created" url="https://example.com/event/order-created" event="order.written" onlyLiveVersion="true"/>
```

By default, this option is set to `false` and the webhook will be called for every version of the entity.

This option is only checked for instances of `HookableEntityWrittenEvent`. For other events, the option is ignored.

If this option is enabled the payload of your webhook will also be filtered to only contain entries that have live version id.

---

## Shipping methods

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/shipping-methods.html

# Shipping methods [​](#shipping-methods)

Starting with version 6.5.7.0 as **experimental feature**. Shopware has introduced experimental functionality for adding shipping methods via the App Manifest to a shop. **The entire functionality and API are subject to change during the development process.**

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

[App Base Guide](app-base-guide)

Your app server must be also accessible for the Shopware server.

## Manifest configuration [​](#manifest-configuration)

### Basic configuration [​](#basic-configuration)

The following example represents the most minimal configuration for a shipping method.

**Important!**

Ensure that the `<identifier>` of your shipping method remains unchanged, as Shopware will deactivate or delete shipping methods that do no longer appear in the manifest during app updates.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- Make sure that the name of your app does not change anymore, otherwise there will be duplicates of your shipping methods -->
        <name>NameOfYourShippingMethodApp</name>
        <!-- ... -->
    </meta>

    <shipping-methods>

        <shipping-method>
            <!-- The identifier should not change after the first release -->
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>

            <delivery-time>
                <!-- Requires a new generated UUID for your new delivery time -->
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Delivery Time [​](#delivery-time)

The app manufacturer should initially display the standard delivery time to the shop manager, who can subsequently adjust it as needed. The delivery time requires some configurations.

#### Id [​](#id)

The ID should only be generated initially and should remain unchanged thereafter. Changing it will result in the creation of a new one.

INFO

Please note that you should not modify the ID of the shipping time.

#### Name [​](#name)

The name should describe the delivery time simply, briefly and comprehensibly.

#### Min / Max [​](#min-max)

The min and max values depend on the unit. Assuming the unit is days, in our example, the delivery time has a range from 2 to 4 days.

#### Unit [​](#unit)

The following values are possible units

* hour
* day
* week
* month
* year

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <delivery-time>
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Extended configuration [​](#extended-configuration)

The functionality offers more than one identifier name. The following examples represent all possible configurations.

* Translation of fields that are visible to the customer and requires a translation
* Shipping method description
* Shipping method icon
* Shipping method active (expects true or false). Default value is `false`

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">

    ...

    <shipping-methods>

        <shipping-method>
            <!-- Identifier should not change after the first release -->
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            <name lang="de-DE">Erste Versandmethode</name>
            <delivery-time>
                <!-- Remember to remove the dashes from generated UUID -->
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
            <!-- The following configurations are optional -->
            <description>This is a simple description</description>
            <description lang="de-DE">Das ist eine einfache Beschreibung</description>
            <icon>icon.png</icon>
            <active>true</active>
            <tracking-url>https://www.yourtrackingurl.com</tracking-url>
            <position>2</position>
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Description [​](#description)

You can initially add a description for the customer.

INFO

Please note that the manifest cannot modify the description once you install the app, as the merchant can change it.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <description>This is a simple description</description>
            <description lang="de-DE">Das ist eine einfache Beschreibung</description>
            <description lang="fr-FR">C'est une description simple</description>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Icon [​](#icon)

You can initially add a shipping method icon. You must specify the path to this icon as relative to the manifest.xml file. For example, you have the following directory structure:

text

```shiki
YourAppDirectory/
├── assets/
│   └── icons/
│       └── yourIcon.png
└── manifest.xml
```

The path should be: `assets/icons/yourIcon.png`

INFO

Please note that the manifest cannot modify the icon once you install the app, as the merchant can change it.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <icon>assets/icons/yourIcon.png</icon>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Active [​](#active)

You can activate the shipping method by default. Possible values for active are `true` or `false`

* true: Activates the shipping method
* false: Deactivates the shipping method. Alternatively, you can leave out active

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <active>true</active>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Tracking url [​](#tracking-url)

It is possible to add a tracking URL for customers to monitor the delivery status.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <tracking-url>https://www.yourtrackingurl.com</tracking-url>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

### Position [​](#position)

Here, you can set the display order of the shipping methods in the checkout. If you omit the tag, the position of the shipping method is 1 by default.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">

    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <position>2</position>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

---

## Client-side communication to the app backend

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/clientside-to-app-backend.html

# Client-App backend communication [​](#client-app-backend-communication)

Direct communication from the browser to the app backend involves generating a JSON Web Token (JWT). This token contains session-specific information, as [claims](#the-json-web-token), and is securely signed by the shop. This mechanism ensures a secure exchange of data between the client and the app backend.

WARNING

The JWT can be only generated when in the browser the user is logged-in.

## The Flow [​](#the-flow)

## The JSON Web Token [​](#the-json-web-token)

The JWT contains the following claims:

* `languageId` - the language ID of the current session
* `currencyId` - the currency ID of the current session
* `customerId` - the customer ID of the current session
* `countryId` - the country ID of the current session
* `salesChannelId` - the sales channel ID of the current session

The claims are only set when the app has permission to that specific entity like `sales_channel:read` for `salesChannelId` claim.

The JWT is signed with `SHA256-HMAC` and the secret is the `appSecret` from the app registration and the `issued by` is the shopId also from the registration.

## Generate JSON Web Token [​](#generate-json-web-token)

INFO

This feature has been introduced with Shopware version 6.5.5.0

The JWT is generated with a POST request against `/store-api/app-system/{name}/generate-token` or `/app-system/{name}/generate-token`.

INFO

Requesting from the browser to the app backend is only possible when your app backend allows [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) requests. Example:

* Access-Control-Allow-Origin: \*
* Access-Control-Allow-Methods: GET, POST, OPTIONS
* Access-Control-Allow-Headers: shopware-app-shop-id, shopware-app-token

## Validate the JSON Web Token [​](#validate-the-json-web-token)

---

## Signing & Verification in the App System

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-signature-verification.html

# Signing & Verification in the App System [​](#signing-verification-in-the-app-system)

To ensure secure communication between Shopware shops and your app server, Shopware signs all outgoing requests using a cryptographic signature. The signature is generated using [HMAC-SHA256](https://en.wikipedia.org/wiki/HMAC), hashing either the query string or the request body, depending on the request method, with your app secret. By verifying this signature on your server, you can confirm that the request originates from Shopware and remains unaltered during transmission. This mechanism safeguards your app against request forgery and unauthorized access.

WARNING

**Breaking Change Considerations**

Shopware may add parameters used for signature generation without considering it a breaking change. Your app should be flexible enough to handle variations in the signature generation data.

To simplify signature verification and response signing, use our [App PHP SDK](https://github.com/shopware/app-php-sdk) or the [Symfony Bundle](https://github.com/shopware/app-bundle-symfony).

If you are not using these tools, ensure that you base signature generation on all query parameters or the entire request body, rather than selecting specific parameters.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps and their registration flow.

[App Base Guide](app-base-guide)

Your app server must be also accessible for the Shopware server. You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Validating requests [​](#validating-requests)

INFO

**Query parsing of signature**

Avoid re-parsing and re-encoding the query string for HMAC validation, as parameter order and URL encoding may vary depending on the programming language used.

Shopware signs all requests sent to your app server using a cryptographic signature. This signature is generated by hashing the request's query string with your app secret.

To ensure the request originates from Shopware, you should verify this signature before processing it.

## Signing responses [​](#signing-responses)

Shopware expects a signature in the response to verify that the response is coming from your app server.

---

## In-App Purchases (IAP)

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/in-app-purchases.html

# In-App Purchases [​](#in-app-purchases)

INFO

In-App Purchase is available since Shopware version 6.6.9.0

In-App Purchases are a way to lock certain features behind a paywall within the same extension. This is useful for developers who want to offer a free version of their extension with limited features and a paid version with more features.

[In-App purchases concept](../../../concepts/framework/in-app-purchases)[Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/in-app-purchases)

## Allow users to buy an In-App Purchase [​](#allow-users-to-buy-an-in-app-purchase)

In order to enable others to purchase your In-App Purchase, you must request a checkout for it via the `sw.iap.purchase()` function of the [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk). The checkout process itself is provided by Shopware. As this is purely functional, it is your responsibility to provide a button and hide it if the IAP cannot be purchased more than once.

vue

```shiki
<template>
    <!-- ... -->
    <p>
        If you buy this you'll get an incredible useful feature: ...
    </p>
    <mt-button @click="onClick">
        Buy
    </mt-button>
    <!-- ... -->
</template>

<script setup>
import * as sw from '@shopware/meteor-admin-sdk';

function onClick() {
    sw.iap.purchase({ identifier: 'my-iap-identifier' });
}
</script>
```

Alternatively, you can trigger a checkout manually by sending a properly formatted [post message](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) with an In-App purchase identifier to the Admin.

## Check active In-App Purchases [​](#check-active-in-app-purchases)

Whenever Shopware sends you a request, you'll receive a [JWT](./../../../concepts/framework/in-app-purchases.html#token) as a query parameter `in-app-purchases` or in the request body as `inAppPurchases` as part of the `source`, depending on whether the request is a GET or POST. The claims of the JWT will contain all bought In-App Purchases.

### Symfony or PHP app servers [​](#symfony-or-php-app-servers)

You can use the `shopware/app-php-sdk` for plain PHP or the `shopware/app-bundle` for Symfony to validate and decode the JWT. An example for plain PHP is available [here](https://github.com/shopware/app-php-sdk/blob/main/examples/index.php). For Symfony applications, use the appropriate action argument for your route.

#### Admin [​](#admin)

You will also receive In-App Purchases with the initial `sw-main-hidden` admin request. To make them accessible, inject them into your JavaScript application.

Here is an example of retrieving active In-App Purchases in an example `admin.html.twig` using the `shopware/app-bundle`:

php

```shiki
#[Route(path: '/app/admin', name: 'admin')]
public function admin(ModuleAction $action): Response {
    return $this->render('admin.html.twig', [
        'inAppPurchases' => $action->inAppPurchases->all(),
    ]);
}
```

html

```shiki
<!DOCTYPE html>
<html>
    <head>
        <script>
            try {
                window.inAppPurchases = JSON.parse('{{ inAppPurchases | json_encode | raw }}');
            } catch (e) {
                window.inAppPurchases = {};
                console.error('Unable to decode In-App Purchases', e);
            }
        </script>

        <!-- ... -->
    </head>

    <!-- ... -->
</html>
```

### Non-PHP app servers [​](#non-php-app-servers)

To validate In-App Purchase tokens on non-PHP app servers, use a JWT/JOSE library appropriate for your language. These tokens are signed JSON Web Tokens (JWT) and include the list of purchased features in their claims. To ensure the token’s authenticity, you must verify its signature using Shopware’s public keys, available as a JWKS (JSON Web Key Set) at `https://api.shopware.com/inappfeatures/jwks`.

Most modern JWT libraries support loading JWKS endpoints directly. After successful verification, you can extract and use the claims to enable or restrict features based on the user’s purchases.

Example (Node.js with `jose`):

js

```shiki
import { jwtVerify, createRemoteJWKSet } from 'jose';

const JWKS = createRemoteJWKSet(new URL('https://api.shopware.com/inappfeatures/jwks'));

const { payload } = await jwtVerify(token, JWKS);
console.log(payload); // Contains list of purchased IAP identifiers
```

## Event [​](#event)

Apps are also able to manipulate the available In-App Purchases as described in

[In App purchase gateway](./gateways/in-app-purchase/in-app-purchase-gateway)

---

