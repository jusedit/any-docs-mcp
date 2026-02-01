# Concepts

*Scraped from Shopware Developer Documentation*

---

## Extensions

**Source:** https://developer.shopware.com/docs/concepts/extensions/

# Extensions [​](#extensions)

In order to provide users (i.e., developers) with a clear abstraction, Shopware consists of a Core designed in a way that allows for a lot of extensibility without sacrificing maintainability or structural integrity. Some of those concepts were already introduced in the [Frameworks](./../framework/) section.

## Apps [​](#apps)

![App concept](/assets/concepts-extensions-apps.CyeuOIop.svg)

Starting with Shopware 6.4.0.0, we introduced a new way to extend Shopware using the newly created app system. Apps are not executed within the process of the Shopware Core but are notified about events via webhooks, which they can register. They can modify and interact with Shopware resources through the [Admin REST API](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide).

## Plugins [​](#plugins)

![Plugin concept](/assets/concepts-extensions-plugins.DfBDQz1L.svg)

Plugins are executed within the Shopware Core process and can react to events, execute custom code or extend services. They have direct access to the database and guidelines are in place to ensure update-compatibility, such as a service facade or database migrations.

WARNING

**Plugins and Shopware cloud** - Due to their direct access to the Shopware process and the database, plugins are not supported by Shopware cloud.

## Start coding [​](#start-coding)

Refer to our Guides section for an [overview of how apps and plugins differ](./../../guides/plugins/index.html).

---

## Apps

**Source:** https://developer.shopware.com/docs/concepts/extensions/apps-concept.html

# Apps [​](#apps)

The app system allows you to extend and modify the functionality and appearance of Shopware. It leverages well defined extension points you can hook into to implement your specific use case.

The app system is designed to be decoupled from Shopware itself. This has two great advantages:

1. **Freedom of choice:** You need to understand only the interface between Shopware and your app to get started with developing your own app. You don't need special knowledge of the inner workings and internal structure of Shopware itself. Additionally, you have the freedom to choose a programming language or framework of your choice to implement your app. This is achieved by decoupling the deployment of Shopware itself and your app and by using the Admin API and webhooks to communicate between Shopware and your app instead of using programming language constructs directly.
2. **Fully cloud compatible:** By decoupling Shopware and your app, your app is automatically compatible for use in a multi-tenant cloud system. Therefore your app can be used within self-hosted shops and shops on [Shopware SaaS](./../../products/saas.html).

The central interface between your app and Shopware is defined by a dedicated manifest file. The manifest is what glues Shopware and your app together. It defines your app's features and how Shopware can connect to it. You can find more information about how to use the manifest file in the [App base Guide](./../../guides/plugins/apps/app-base-guide.html).

## Communication between Shopware and your app [​](#communication-between-shopware-and-your-app)

Shopware communicates with your app only exclusively via HTTP-Requests. Therefore you are free to choose a tech stack for your app, as long as you can serve HTTP-Requests. Shopware will notify you of events happening in the shop that your app is interested in by posting to HTTP-Endpoints that you define in the manifest file. While processing these events, your app can use the Shopware API to get additional data that your app needs. A schematic overview of the communication may look like this:

![Communication between Shopware and your app](/assets/extensions-apps-shopwareCommunication.CNZDRWoI.svg)

To secure this communication, a registration handshake is performed during the installation of your app. During this registration, it is verified that Shopware talks to the right app backend server, and your app gets credentials used to authenticate against the API. You can read more on the registration workflow in the [App base guide](./../../guides/plugins/apps/app-base-guide.html).

INFO

Notice that this is optional if Shopware and your app don't need to communicate, e.g., because your app provides a [Theme](./apps-concept.html).

## Modify the appearance of the Storefront [​](#modify-the-appearance-of-the-storefront)

Your app can modify the Storefront's appearance by shipping your Storefront assets (template files, javascript sources, SCSS sources, snippet files) alongside your manifest file. You don't need to serve those assets from your external server, as Shopware will rebuild the Storefront upon the installation of your app and will consider your modifications in that process. Find out more about modifying the appearance of the Storefront in the [App Storefront guide](./../../guides/plugins/apps/storefront/)

## Integrate payment providers [​](#integrate-payment-providers)

INFO

This functionality is available starting with Shopware 6.4.1.0.

Shopware provides functionality for your app to be able to integrate payment providers. You can use the synchronous payment to provide payment with a provider that does not require any user interaction, for which you can choose a simple request for approval in the background. You can use an asynchronous payment if you would like to redirect a user to a payment provider. Your app, therefore, provides a URL for redirection. After the user returns to the shop, Shopware will verify the payment status with your app. Find out more about providing payment endpoints in the [App payment guide](./../../guides/plugins/apps/payment.html).

## Execute business logic inside Shopware with App Scripts [​](#execute-business-logic-inside-shopware-with-app-scripts)

INFO

This functionality is available starting with Shopware 6.4.8.0.

[App scripts](./../../guides/plugins/apps/app-scripts/) allow your app to execute custom business logic inside the Shopware execution stack. This allows for new use cases, e.g., if you need to load additional data that should be rendered in the Storefront or need to manipulate the cart.

## Add conditions to the Rule Builder [​](#add-conditions-to-the-rule-builder)

INFO

This functionality is available starting with Shopware 6.4.12.0.

Your app may introduce custom conditions for use in the [Rule builder](./../framework/rules.html). For additional information refer to [Add custom rule conditions](./../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html) from the guides.

---

## Plugins

**Source:** https://developer.shopware.com/docs/concepts/extensions/plugins-concept.html

# Plugins [​](#plugins)

Plugins in Shopware are essentially an extension of [Symfony bundles](https://symfony.com/doc/current/bundles.html#creating-a-bundle). Such bundles and plugins can provide their own resources like assets, controllers, services, or tests. To reduce friction when programming plugins for Shopware, there is an abstract [Base class](./../../guides/plugins/plugins/plugin-base-guide.html#create-your-first-plugin), which every plugin extends from the plugin base class. In this class, there are helper methods to initialize parameters like the plugin's name and root path in the dependency injection container. Also, each plugin is represented as a Composer package and may for example, define dependencies this way.

Plugins are deeply integrated into Shopware. You can do nearly everything with plugins, like "new User Provider" or "custom Search Engine".

WARNING

Plugins are not compatible with Shopware cloud stores. To extend Shopware cloud stores, you need an [App](./apps-concept.html).

Learn more about plugins from the [Plugin base guide](./../../guides/plugins/plugins/plugin-base-guide.html)

---

## API

**Source:** https://developer.shopware.com/docs/concepts/api/

# API [​](#api)

The Shopware API allows developers to interact with and integrate Shopware with other systems and applications. It provides a set of services that enable developers to perform various operations, such as managing products, customers, orders, and shopping carts.The API supports both read and write operations, allowing developers to retrieve information from Shopware and make modifications or additions to the e-commerce platform. By leveraging the Shopware API, developers can extend the functionality of Shopware, integrate it with external systems, and create seamless experiences for managing and operating online stores.

Shopware supports two major functional APIs: the Store API and the Admin API. These APIs serve different purposes. The Store API is designed to interact with the front-end or storefront of a Shopware online store while the Admin API is intended for administrative operations related to managing the back-end of the Shopware platform.

The API documentation provides details on the available endpoints, request/response formats, authentication mechanisms, and data structures. It supports different authentication methods, including token-based authentication and OAuth 2.0, to ensure secure communication between the API client and the Shopware platform.

---

## Store API

**Source:** https://developer.shopware.com/docs/concepts/api/store-api.html

# Store API [​](#store-api)

Every interaction between the store and a customer can be modeled using the Store API. It serves as a normalized layer or an interface to communicate between customer-facing applications and the Shopware Core. It can be used to build custom frontends like SPAs, native apps, or simple catalog apps. It doesn't matter what you want to build as long as you are able to consume a JSON API via HTTP.

![Data and logic flow in Shopware 6 top to bottom and vice versa](/assets/concepts-api-storeApiLogic.mw5QvIuh.svg)

Whenever additional logic is added to Shopware, the method of the corresponding service is exposed via a dedicated HTTP route. At the same time, it can be programmatically used to provide data to a controller or other services in the stack. This way, you can ensure that there is always common logic between the API and the Storefront and almost no redundancy. It also allows us to build core functionalities into our Storefront without compromising support for our API consumers.

## Extensibility [​](#extensibility)

Using plugins, you can add custom routes to the Store API (as well as any other routes) and also register custom services. We don't force developers to provide API coverage for their functionalities. However, if you want to support headless applications, ensure that your plugin provides its functionalities through dedicated routes.

[Store API](../../guides/plugins/plugins/framework/store-api/)

## Store API and the traditional TWIG storefront [​](#store-api-and-the-traditional-twig-storefront)

When using the server-side rendered TWIG storefront, the Store API is not used. Instead, the storefront uses custom [storefront controllers](./../../guides/plugins/plugins/storefront/add-custom-controller.html) which internally use the Store API to fetch data.

The storefront controllers are optimized for the usage in our TWIG storefront. And the biggest difference is the way that authentication and authorization are handled. As the Store-API is a proper REST API, the main design is stateless, which means authentication info needs to be provided via the request headers in form of the `sw-context-token`. The storefront relies on the session to store the authentication info, that way you do not have to handle the authentication manually with every request.

## What next? [​](#what-next)

* To start working with the Store API, check out our [Quick Start guide](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide) and explore all endpoints in our reference guide.
* An interesting project based on the Store API is [Composable Frontends](./../../../frontends/).

---

## Admin API

**Source:** https://developer.shopware.com/docs/concepts/api/admin-api.html

# Admin API [​](#admin-api)

The Admin API provides CRUD operations for every entity within Shopware and is used to build integrations with external systems.

For more information, refer to the [Guides section](./../../guides/integrations-api/).

---

## Translations

**Source:** https://developer.shopware.com/docs/concepts/translations/

# Translations [​](#translations)

Shopware 6 is a multilingual platform that supports multiple languages and locales. This section provides an overview of how translations are managed in Shopware 6.

---

## Built-in Translation Handling

**Source:** https://developer.shopware.com/docs/concepts/translations/built-in-translation-system.html

# Built-in Translation Handling [​](#built-in-translation-handling)

## Overview [​](#overview)

The built-in translation system allows you to install and update translations that are not shipped with Shopware by default. It provides the same set of translations as the **Language Pack** plugin and is planned to fully replace it.

> **Note:** The Language Pack plugin is deprecated and will be removed with Shopware version **6.8.0.0**. If you are currently using the Language Pack plugin, please refer to the [Migration guide](./../../resources/references/upgrades/core/translation/language-pack-migration.html) for instructions on switching to the new system.

## Where do the translations come from? [​](#where-do-the-translations-come-from)

Translations are fetched from a public GitHub repository: [shopware/translations](https://github.com/shopware/translations). This repository is managed using [Crowdin](https://crowdin.com/project/shopware6) and contains translations for Shopware as well as for some official plugins. The repository syncs with Crowdin every day to ensure that the latest translations are always available.

## How to Install and Update Translations? [​](#how-to-install-and-update-translations)

To use the built-in translation system, you can use the following console commands:

### Install translations [​](#install-translations)

The `translation:install` command is used to download and install translations for Shopware and its plugins from the configured GitHub repository. It allows you to specify which locales to install, whether to install all available locales, and whether to skip activation of the installed translations. Re-installing an already installed locale will override its translations.

bash

```shiki
$ php bin/console translation:install [--all, --locales, --skip-activation]

# example
$ php bin/console translation:install --locales=fr-FR,pl-PL --skip-activation
```

### Update command [​](#update-command)

The `translation:update` command is used to update existing translations for Shopware and its plugins from the configured GitHub repository.

bash

```shiki
$ php bin/console translation:update
```

## Language activation [​](#language-activation)

By default, installed translations are automatically activated, making them available for use in Shopware. If you want to install translations without activating them, you can use the `--skip-activation` option with the `translation:install` command. The `active` flag in the `language` table indicates whether a language is active or not. If a language is not active, it will not be available for selection in the storefront.

## How does the system recognize new updates? [​](#how-does-the-system-recognize-new-updates)

The `translations` repository includes [metadata](https://github.com/shopware/translations/blob/main/crowdin-metadata.json) that provides information about the translations, such as available locales, last update timestamps, and completion percentages for each language. The `updatedAt` field in the metadata is used to determine if a translation needs to be updated. Installing or updating translations will create or update a `crowdin-metadata.lock` file on your private filesystem which stores the last known update timestamps for each locale. This file is used to compare the last update timestamps of installed locales with the ones in the metadata file to determine if an update is necessary.

## Loading priority [​](#loading-priority)

When loading translations, the system follows a defined priority order to resolve conflicts:

1. Database translations – These have the highest priority. You can define them to override all other translations.
2. Country-specific translations (e.g. `en-GB`, `en-US` or `de-DE`) – These can be provided for country-dependent translations or dialects as small patch files. For more information about the language-layer changes, you can have a look at its documentation.
3. Country-agnostic translations (`en` and `de`) – These are shipped with Shopware and its plugins. They ensure that the system always has a reliable fallback language and provide a consistent developer experience without requiring you to wait until your translations are accepted at [translate.shopware.com](https://crowdin.com/project/shopware6). For more details on selecting a fallback language and structuring your snippet files, see the [Fallback Languages guide](./../../concepts/translations/fallback-language-selection.html).
4. Built-in translation system – Finally, the translations installed via the built-in translation system are applied.

## Built-in translation system and Flysystem [​](#built-in-translation-system-and-flysystem)

The built-in translation system relies on Flysystem for storage abstraction. This allows great flexibility when working with translations, as Flysystem supports multiple storage backends. For example, external systems can configure the translation storage to use:

* Local file system (default)
* Cloud storage services such as Amazon S3, Google Cloud Storage, or Azure Blob Storage
* Custom storage adapters that integrate with other systems

This means you can adapt translation storage to your infrastructure needs, whether you want to keep everything local or centralize it in a cloud-based storage solution.

## Translation configuration [​](#translation-configuration)

This configuration file is in YAML format and defines how translations for Shopware core and plugins are managed and retrieved. It specifies the repository sources, supported plugins and languages, and more. You can find the configuration file at `src/Core/System/Resources/translation.yaml`.

### Fields [​](#fields)

#### `repository-url` [​](#repository-url)

**Type:** `string`**Example:**

yaml

```shiki
repository-url: https://raw.githubusercontent.com/shopware/translations/main/translations
```

**Description:** The base URL of the translation repository. Translation files for different languages and plugins are fetched from here.

---

#### `metadata-url` [​](#metadata-url)

**Type:** `string`**Example:**

yaml

```shiki
metadata-url: https://raw.githubusercontent.com/shopware/translations/main/crowdin-metadata.json
```

**Description:** The URL for [metadata information](#how-does-the-system-recognize-new-updates) about the translations.

---

#### `plugins` [​](#plugins)

**Type:** `array[string]`**Example:**

yaml

```shiki
plugins: [
  'PluginPublisher',
  'SwagB2bPlatform',
  'SwagCmsExtensions'
]
```

**Description:** A list of supported plugins for which translations are available.

---

#### `excluded-locales` [​](#excluded-locales)

**Type:** `array[string]`**Example:**

yaml

```shiki
excluded-locales: [ 'de-DE', 'en-GB' ]
```

**Description:** A list of language locales to be excluded from translation processing. German (Germany) and English (UK) are excluded by default since they are shipped with Shopware. The exclusion applies to plugins too.

---

#### `plugin-mapping` [​](#plugin-mapping)

**Type:** `array[object]`**Example:**

yaml

```shiki
plugin-mapping:
  - plugin: 'SwagPublisher'
    name: 'PluginPublisher'
```

**Fields:**

* `plugin` (`string`): The internal plugin identifier (e.g., directory or code name).
* `name` (`string`): The corresponding plugin name in the translation repository.

**Description:** Allows mapping between internal plugin identifiers and repository names in case they differ.

---

#### `languages` [​](#languages)

**Type:** `array[object]`**Example:**

yaml

```shiki
languages:
  - name: 'Français'
    locale: 'fr-FR'
```

**Fields:**

* `name` (`string`): Human-readable language name (preferably in the native script).
* `locale` (`string`): Language code according to [IETF BCP 47](https://www.rfc-editor.org/info/bcp47), restricted to [ISO 639-1 (2-letter) language codes](https://en.wikipedia.org/wiki/ISO_639-1), used by Shopware for translations.

**Description:** Defines the set of supported languages for which translations should be retrieved. Each entry specifies a display name and a locale code.

---

## How to extend or modify the configuration handling [​](#how-to-extend-or-modify-the-configuration-handling)

### TranslationConfigLoader [​](#translationconfigloader)

The `TranslationConfigLoader` (`src/Core/System/Snippet/Service/TranslationConfigLoader.php`) is part of the Shopware core and is responsible for loading and validating the `translation.yaml` file. It provides a `TranslationConfig` object that contains all configured fields from the `translation.yaml`. It ensures that URLs are valid, languages and plugins are properly structured, and plugin mappings are resolved. Errors such as missing files or invalid configuration values are raised as `SnippetException`. To extend or modify its behavior, the decoration pattern is used: services should depend on the abstract class `AbstractTranslationConfigLoader`, and custom decorators can override methods like `load()` or the configuration path while delegating to the original loader.

### TranslationConfig [​](#translationconfig)

The `TranslationConfig` (`src/Core/System/Snippet/Service/TranslationConfig.php`) is a data structure that holds the configuration details loaded from the `translation.yaml` file. You can require it via dependency injection and because of the usage of the `TranslationConfigLoader` with lazy loading, the configuration is always available when needed.

---

## Fallback language selection

**Source:** https://developer.shopware.com/docs/concepts/translations/fallback-language-selection.html

# Fallback language selection [​](#fallback-language-selection)

With Shopware 6.7 a **country-agnostic snippet layer** was introduced to reduce duplicate translations. In this model the snippet loader first attempts to load a country-specific variant (e.g. `de-DE`), then looks for an agnostic **fallback language** (e.g. `de`), and as a last resort falls back to `en` as a universal default. The fallback layer concept and fallback order are explained in detail in the [Built-in Translation Handling](./built-in-translation-system.html) page, which you should read alongside this guide.

## Why an extra fallback layer? [​](#why-an-extra-fallback-layer)

Before v6.7, Shopware shipped only country-specific snippet files. Developers often duplicated existing files (for example `en-GB` to `en-US`) and changed a handful of keys. This practice led to bloated repositories and inconsistent fallbacks. The **country-independent layer** centralizes common translations into a neutral fallback file (`en`, `de`, `pt`, etc.) and isolates regional differences in small patch files. Detailed examples of how Shopware resolves translations are available in the [Built-in Translation Handling](./built-in-translation-system.html) guide.

## Fallback languages [​](#fallback-languages)

The **fallback code** is the plain language code (e.g. `en` or `de`), and the **defining dialect** is the standard locale from which the fallback translations derive (for example `en` instead of `en-US` or `en-GB`). The table shows some examples of common cases:

| Fallback code | Standard variant (defining dialect) | Example dialects |
| --- | --- | --- |
| **`en`** | `en-GB` (British English) | `en-US`, `en-CA`, `en-IN` |
| **`de`** | `de-DE` (German in Germany) | `de-AT`, `de-CH` |
| **`es`** | `es-ES` (Castilian Spanish) | `es-AR`, `es-MX` |
| **`pt`** | `pt-PT` (European Portuguese) | `pt-BR` |
| **`fr`** | `fr-FR` (French in France) | `fr-CA`, `fr-CH` |
| **`nl`** | `nl-NL` (Dutch in the Netherlands) | `nl-BE` |

## Migration and linting via command [​](#migration-and-linting-via-command)

To support these processes, the `LintTranslationFilesCommand` can be executed using `bin/console translation:lint-filenames` to validate translation filenames.

The command outputs tables for each domain (Administration, Core/base files, and Storefront) containing the following information:

* **Filename** – The name of the translation file, e.g. `storefront.de.json`.
* **Path** – The file path where this translation file was found, e.g. `src/Storefront/Resources/snippet`.
* **Domain** – The prefix of the corresponding storefront translation file. For administration files, `administration` is shown in this column. For extensions, it can be helpful to name storefront files accordingly, for example `cms-extensions.en.json`. Please note: language-defining base files **must always** use `messages` here, like in `messages.fr.base.json`!
* **Locale** – The language code following [IETF BCP 47](https://www.rfc-editor.org/info/bcp47), restricted to [ISO 639-1 (2-letter) language codes](https://en.wikipedia.org/wiki/ISO_639-1). Example: `de-DE` for German (Germany).
* **Language** – The first part of the locale, representing the language used. Example: `de` (German) when the full locale is `de-DE`.
* **Script** – Specifies the writing system used for the language when multiple scripts exist. This part is optional and rarely used, as Shopware processes currently do not support or distinguish between scripts and only offer it for extensibility. For example, Serbian (Serbia) can be written in both Cyrillic and Latin (`sr-Cyrl-RS` vs. `sr-Latn-RS`).
* **Region** – The suffix of the locale, used to specify a regional variant of a language. Shopware’s best practice is to avoid using regional locales for the base language so that regional differences can be handled through overrides. Example: `de-AT` (German for Austria) can be used to patch differences from the base `de` locale.

### Command parameters [​](#command-parameters)

The command supports several options:

* **`--fix`** – This parameter helps you **migrate** to Shopware's best practices by automatically renaming files to their agnostic equivalents. If multiple country-specific candidates exist for a single agnostic file, you’ll need to select one manually via prompt.
* **`--all`** – Includes the `custom` directory in the linting of filenames to **include all extensions as well**. If specified, the `extensions` option will be ignored.
* **`--extensions`** – Restricts the search to the given **technical** extension names (for example: `SwagCmsExtensions`), if provided. Multiple values can be passed as a comma-separated list.
* **`--ignore`** – Excludes the specified paths relative to `src`, or, if applicable, the provided (bundle) paths. Multiple values can be passed as a comma-separated list.
* **`--dir`** – Limits the search to a specific directory for translation files, **taking precedence over** the `ignore` parameter.

## Implementation guidelines for extension developers [​](#implementation-guidelines-for-extension-developers)

For detailed instructions, see the [Extension Translation Migration](./../../resources/references/upgrades/core/translation/extension-translation.html) guide. In short:

* **Create a complete base file** (`messages.<language>.base.json`) for each supported language.
* **Add patch files only when needed** – keep them minimal.
* **Aim for neutrality** – Avoid country-specific terminology in the fallback files.
* **Properly select which dialect is your standard** — for example, looking at Spanish, a neutral Castilian is recommended to maximize comprehension.
* **Follow naming conventions** – E.g., agnostic file: `storefront.nl.json`; patch file: `storefront.nl-BE.json`.
* **Validate your translations** – clear the cache and run `bin/console translation:validate`, as well as `bin/console translation:lint-filenames` to be ready to go.

## Conclusion [​](#conclusion)

The country-independent snippet layer streamlines translation maintenance by consolidating common strings into a neutral fallback file and isolating regional vocabulary into small patch files. For further examples, refer to [Built-in Translation Handling](./built-in-translation-system.html) and [Extension Translation Migration](./../../resources/references/upgrades/core/translation/extension-translation.html).

---

