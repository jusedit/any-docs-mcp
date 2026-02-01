# Guides Hosting Configurations

*Scraped from Shopware Developer Documentation*

---

## Configurations

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/

# Configurations [​](#configurations)

## Overview [​](#overview)

When running Shopware 6 there are various configuration options you can use to customize your installation.

## Configuration [​](#configuration)

The configuration for Shopware 6 resides in the general bundle configuration:

text

```shiki
<project root>
└── config
   └── packages
      └── shopware.yaml
```

If you want to aim at a specific environment, you can create a configuration file for that as follows:

text

```shiki
<project root>
└── config
   └── packages
      └── dev
         └── mailer.yaml
```

text

```shiki
<project root>
└── config
   └── packages
      └── prod
         └── mailer.yaml
```

For more information on environment-specific configurations, check out the [Symfony Configuration Environments](https://symfony.com/doc/current/configuration.html#configuration-environments) section.

---

## Shopware

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/

# Shopware configurations [​](#shopware-configurations)

## Overview [​](#overview)

The following section guides you on the security, performance or structural configurations specific to Shopware 6.

---

## HTML sanitizer

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/html-sanitizer.html

# HTML Sanitizer [​](#html-sanitizer)

INFO

This feature has been introduced with Shopware version 6.5. This is exclusively intended for self-hosted shops. However, it's important to note that the implementation is currently not available for cloud stores.

## Overview [​](#overview)

HTML sanitizer improves security, reliability and usability of the text editor by removing potentially unsafe or malicious HTML code. It also sanitizes styles and attributes for consistent and correct code rendering regardless of platform and browser. For example, if the `<img>` tag is added, it is automatically removed by the editor after a few seconds and an additional notice appears that some of your inputs have been sanitized.

## Configuration [​](#configuration)

Through a workaround or an adjustment of the `z-shopware.yaml` file, it is possible to add the `<img>` tag to the allowed code.

The `z-shopware.yaml` is located below `config/packages/` on the server where Shopware is installed. By default, this file does not exist. A simple copy of the `shopware.yaml` in the same directory solves this obstacle.

In the copied `shopware.yaml` file (z-shopware.yaml), you should include an additional key called `html_sanitizer:` inside the `shopware:` section. This key will contain all the other values and wildcards required for whitelisting.

In this example, the `<img>` tag, as well as the CSS attributes `src`, `alt` and `style` are added to the whitelist:

yaml

```shiki
shopware:
  html_sanitizer:
    sets:
      -   name: basic
          tags: [ "img" ]
          attributes: [ "src", "alt", "style" ]
          options:
            - key: HTML.Trusted
              value: true
            - key: CSS.Trusted
              value: true
```

If you want to deactivate the sanitizer despite security risks, you can also do this in the `z-shopware.yaml` using the following code:

yaml

```shiki
shopware:
  html_sanitizer:
    enabled: false
```

WARNING

Disabling the HTML sanitizer will allow potentially unsafe or malicious HTML code to be inserted.

---

## Staging

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/staging.html

# Staging [​](#staging)

Since Shopware 6.6.1.0, Shopware has an integrated staging mode. This mode prepares the shop to be used in a staging environment. This means the shop is prepared to be used in a test environment, where changes can be made without affecting the live shop.

## The workflow [​](#the-workflow)

The staging mode is designed to modify data only inside the Shopware instance. This means the staging mode does not duplicate the current installation, copy the database, or copy the files. It only changes the data inside the Shopware instance.

So, the real-world use case would be something like this:

### Creating the second Shopware instance [​](#creating-the-second-shopware-instance)

The recommended way to create a second Shopware instance would be to deploy from your Git repository to the new environment. This way, you ensure the codebase is equal to the live environment.

An alternative way would be to copy the files from the live environment to the staging environment.

### Copying the database [​](#copying-the-database)

INFO

Ensure that the `mysqldump` and `mysql` binary are from the same major version and vendor. If you use `mysqldump` from MariaDB, you should also use `mysql` from MariaDB. The same applies to MySQL.

To have the staging environment similar to the live environment, it's recommended that the database be duplicated. You can use the `mysqldump` command to export the database and import it into the staging environment.

INFO

`shopware-cli` is a separate Go command line application that contains a lot of useful commands for Shopware. [Checkout the docs](./../../../../products/cli/installation.html) to learn how to install it.

We recommend using `shopware-cli project dump` to create a dump of the database and import it with the regular mysql command. Shopware cli also has a flag to anonymize the data, so you can be sure that no personal data is in the staging environment.

bash

```shiki
# creating a regular dump, the clean parameter will not dump the data of cart table
shopware-cli project dump --clean --host localhost --username db_user --password db_pass --output shop.sql shopware

# create a dump with anonymize data
shopware-cli project dump --clean --anonymize --host localhost --username db_user --password db_pass --output shop.sql shopware
```

You can configure the dump command with a `.shopware-project.yml`. This file allows you to specify tables that should be skipped, define additional fields for anonymization, and more. Check out the [CLI](./../../../../products/cli/project-commands/mysql-dump.html) for more information.

### Configuration [​](#configuration)

INFO

It is not recommended to share resources like MySQL, Redis, ElasticSearch/OpenSearch between the live and staging environments. This could lead to data corruption when the configuration is not done correctly. Also, the performance of the live environment could be affected by the staging environment.

After importing the database, you should modify the `.env` to use the staging database. If you use ElasticSearch/OpenSearch, you should set a `SHOPWARE_ES_INDEX_PREFIX` to avoid conflicts with the live environment.

### Activate the staging mode [​](#activate-the-staging-mode)

After the database is imported and the configuration is done, you can activate the staging mode. This can be done using:

bash

```shiki
./bin/console system:setup:staging
```

This command will modify the database to be used in a staging environment. You can pass `--no-interaction --force` to the command to avoid the interactive questions.

### Protecting the staging environment [​](#protecting-the-staging-environment)

The staging environment should be protected from unauthorized access. It is advisable to employ protective measures like password protection, IP restriction, or OAuth authentication.

The simplest way to protect the staging environment is utilizing `.htaccess` for Apache or `auth_basic` for Nginx. You can also use a firewall to restrict access to the staging environment based on IP addresses.

Example configuration for Apache:

apache

```shiki
# <project-root>/public/.htaccess
SetEnvIf Request_URI /api noauth=1
<RequireAny>
Require env noauth
Require env REDIRECT_noauth
Require valid-user
</RequireAny>
```

An alternative way could be to use an Application Proxy before the staging environment like:

* [Cloudflare Access](https://www.cloudflare.com/zero-trust/products/access/)
* [Azure Application Gateway](https://azure.microsoft.com/en-us/products/application-gateway/)
* [Generic oauth2 proxy](https://oauth2-proxy.github.io/oauth2-proxy/)

## Staging mode [​](#staging-mode)

The staging mode is designed to be used in a test environment. This means the shop is prepared to be used in a test environment, where changes can be made without affecting the live shop.

### What staging mode does? [​](#what-staging-mode-does)

* Deletes all apps that have an active connection to an external service and the integrations in Shopware.
* Resets the instance ID used for registration of apps.
* It turns off the sending of emails.
* Rewrites the URLs to the staging domain (if configured).
* Checks that the ElasticSearch/OpenSearch indices do not exist yet.
* Shows a banner in the administration and storefront to indicate that the shop is in staging mode.

### What staging mode does not? [​](#what-staging-mode-does-not)

* Doesn't duplicate the current installation.
* Doesn't copy database or files.
* Doesn't modify the live environment.

### Configuration [​](#configuration-1)

The staging mode is fully configurable with `config/packages/staging.yaml`. You can configure the following options:

yaml

```shiki
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        mailing:
            # Disables the sending of mails (default: true)
            disable_delivery: true
        storefront:
            # Shows a banner in the storefront when staging mode is active (default: true)
            show_banner: true
        administration:
            # Shows a banner in the administration when staging mode is active (default: true)
            show_banner: true
        sales_channel:
            domain_rewrite:
                # See below for more information
        elasticsearch:
            # Checks that no indices are existing yet (default: true)
            check_for_existence: true
```

One of the most important options is the `domain_rewrite`. This option allows you to rewrite the URLs to the staging domain. This allows multiple ways to rewrite the URLs:

* Using direct match (`equal`)

yaml

```shiki
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: equal
                  match: https://my-live-store.com
                  replace: https://my-staging-store.com
                - # ... second rule
```

This compares the Sales Channel URLs. When it's equal to `https://my-live-store.com`, it will be replaced with `https://my-staging-store.com`.

* Replace using prefix (`prefix`)

yaml

```shiki
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: prefix
                  match: https://my-live-store.com
                  replace: https://my-staging-store.com
                - # ... second rule
```

The difference here to the `equal` type is that it will only replace the URL when it starts with `https://my-live-store.com`, so all paths to that beginning will be replaced. For example, `https://my-live-store.com/en` will be replaced with `https://my-staging-store.com/en`

* Replace using regex (`regex`)

yaml

```shiki
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: regex
                  match: '/https?:\/\/(\w+)\.(\w+)$/m'
                  replace: 'http://$1-$2.local'
                - # ... second rule
```

This will use the regex to replace the URL. The match and replace are regular expressions. In this example, `https://my-live-store.com` will be replaced with `http://my-live-store.local`.

### Usage of apps [​](#usage-of-apps)

The staging command will delete all apps that have an active connection to an external service. This will be done to avoid data corruption or leaks in the live environment, as the staging environment is a copy of the live environment, so they keep a connection. After executing the command, you can install the app again, creating a new instance ID, so the app will think it's an entirely different shop. In this way, the app installation is completely isolated from the live environment.

## Integration into plugins [​](#integration-into-plugins)

The `system:setup:staging` is dispatching an Event which all plugins can subscribe to `Shopware\Core\Maintenance\Staging\Event\SetupStagingEvent` and modify the database for them to be in staging mode.

Example of a subscriber for a payment provider to turn on the test mode:

php

```shiki
<?php

namespace Swag\PaymentProvider\Subscriber;

use Shopware\Core\Maintenance\Staging\Event\SetupStagingEvent;

class StagingSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            SetupStagingEvent::class => 'onSetupStaging'
        ];
    }

    public function onSetupStaging(SetupStagingEvent $event): void
    {
        // modify the database to turn on the test mode
    }
}
```

---

## Stock

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/stock.html

# Stock Configuration [​](#stock-configuration)

When running Shopware 6 there are various configuration options you can use to customize your installation. These configurations reside in the general [bundle configuration](./../../../../guides/hosting/configurations/).

Some features of Shopware are only activated when the corresponding feature flag is enabled. Feature flags can be enabled in your project's `.env` file:

sh

```shiki
// <project root>/.env
STOCK_HANDLING=1
```

## Enable stock management system [​](#enable-stock-management-system)

As of Shopware 6.5.5, the stock management system has been rewritten. The `product.stock` field is now the primary source for real-time product stock values.

The new system is not enabled by default. To enable it, set the `STOCK_HANDLING` feature flag to `1`.

sh

```shiki
// <project root>/.env
STOCK_HANDLING=1
```

In the next major version of Shopware, the new stock management system will become the default.

## Disable stock management system [​](#disable-stock-management-system)

Please note this only applies if you have the `STOCK_HANDLING` feature flag enabled.

You can completely disable Shopware's default stock management system. When disabled, none of the event subscribers for order transitions will be executed. In practice, this means that none of the subscribers in `Shopware\Core\Content\Product\Stock\OrderStockSubscriber` will be executed.

To disable, set `shopware.stock.enable_stock_management` to `false`:

yaml

```shiki
# <project root>/config/packages/shopware.yaml
shopware:
  stock:
    enable_stock_management: false
```

For more detailed implementation refer to [Stock](./../../../../guides/plugins/plugins/content/stock/) guide section.

---

## Static System Configuration

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/static-system-config.html

# Static System Configuration [​](#static-system-configuration)

INFO

This feature is available since Shopware 6.6.4.0

The static system configuration is a feature that allows you to configure system configurations inside the `config/packages` directory and **overwrite** the configuration set in the database. This is useful for setting up configurations that should not be changed by the user, or properly configuring the system for different environments without the need to change the database.

## How it works [​](#how-it-works)

The statically set configuration is an overlay of the database loaded configuration. This means that the configuration in the database is loaded first, and then the configuration set in the `config/packages` directory is loaded. If a configuration key is set in both places, the value from the `config/packages` directory will be used. Additionally, when the configuration is overwritten, the user is not able to change the configuration in the administration anymore.

## Why to use? [​](#why-to-use)

* When the configuration should be fixed and should not be changed by the user
* When you want to have the configuration versioned in the repository
* When you want to have different configurations for different environments (e.g., development, staging, production)

## Usage [​](#usage)

To use this feature, you will need to create a new file at `config/packages/<name>.yaml`

The file should contain the configuration in the following format:

yaml

```shiki
shopware:
  system_config:
    default:
      core.listing.allowBuyInListing: true
    # Disable it for the specific sales channel
    0188da12724970b9b4a708298259b171:
      core.listing.allowBuyInListing: false
```

In this example, the `core.listing.allowBuyInListing` configuration is set to `true` by default. However, for the sales channel with the ID `0188da12724970b9b4a708298259b171`, the configuration is set to `false`.

You can also use regular Symfony Configuration processors like the usage of environment variables:

yaml

```shiki
shopware:
  system_config:
    default:
      core.listing.allowBuyInListing: '%env(bool:ALLOW_BUY_IN_LISTING)%'
```

and then set the environment variable in your `.env` file:

dotenv

```shiki
# .env.local
ALLOW_BUY_IN_LISTING=true
```

---

## Environment Variables

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/shopware/environment-variables.html

# Environment Variables [​](#environment-variables)

This page lists all environment variables that can be used to configure Shopware.

| Variable | Default Value | Description |
| --- | --- | --- |
| `ADMIN_OPENSEARCH_URL` | (empty) | OpenSearch URL for administration |
| `APP_BUILD_DIR` | `{projectRoot}/var/cache` | Path to a temporary directory to create cache folder (since 6.6.8.0) |
| `APP_CACHE_DIR` | `{projectRoot}/var/cache` | Path to a directory to store caches (since 6.6.8.0) |
| `APP_ENV` | `prod` | Environment |
| `APP_LOG_DIR` | `{projectRoot}/var/log` | Path to a directory to store logs (since 6.6.8.0) |
| `APP_SECRET` | (empty) | Can be generated with `openssl rand -hex 32` |
| `APP_URL` | (empty) | Where Shopware will be accessible |
| `APP_URL_CHECK_DISABLED` | `false` | Disable URL validation checks |
| `BLUE_GREEN_DEPLOYMENT` | `0` | This needs super privilege to create trigger |
| `COMPOSER_HOME` | `/tmp/composer` | Caching for the Plugin Manager |
| `COMPOSER_PLUGIN_LOADER` | (empty) | When set to a non-empty value (e.g., `1` or `true`), enables the Composer plugin loader instead of the database plugin loader. All plugins defined in the root `composer.json` will be automatically active, regardless of database settings. |
| `DATABASE_SSL_CA` | (empty) | Path to SSL CA file |
| `DATABASE_SSL_CERT` | (empty) | Path to SSL Cert file |
| `DATABASE_SSL_DONT_VERIFY_SERVER_CERT` | (empty) | Disables verification of the server certificate (1 disables it) |
| `DATABASE_SSL_KEY` | (empty) | Path to SSL Key file |
| `DATABASE_URL` | (empty) | MySQL credentials as DSN |
| `ENABLE_SERVICES` | `auto` | Determines if services are enabled, auto detects that based on `APP_ENV`, other possible values are `true` (or `1`) and `false` (or `0`). When set to `0`, Shopware Services won't be installed on the system |
| `FASTLY_API_KEY` | (empty) | API key for Fastly CDN integration. **Keep this value secure and do not commit it to version control.** |
| `INSTANCE_ID` | (empty) | Unique Identifier for the Store: Can be generated with `openssl rand -hex 32` |
| `JWT_PRIVATE_KEY` | (empty) | Can be generated with `shopware-cli project generate-jwt --env` |
| `JWT_PUBLIC_KEY` | (empty) | Can be generated with `shopware-cli project generate-jwt --env` |
| `LOCK_DSN` | `flock` | DSN for Symfony locking |
| `MAILER_DSN` | `null://localhost` | Mailer DSN (Admin Configuration overwrites this) |
| `MESSENGER_TRANSPORT_DSN` | (empty) | DSN for default async queue (example: `amqp://guest:guest@localhost:5672/%2f/default`) |
| `MESSENGER_TRANSPORT_FAILURE_DSN` | (empty) | DSN for failed messages queue (example: `amqp://guest:guest@localhost:5672/%2f/failure`) |
| `MESSENGER_TRANSPORT_LOW_PRIORITY_DSN` | (empty) | DSN for low priority queue (example: `amqp://guest:guest@localhost:5672/%2f/low_prio`) |
| `OPENSEARCH_URL` | (empty) | Open Search Hosts |
| `REDIS_PREFIX` | (empty) | Prefix for Redis keys |
| `REDIS_URL` | (empty) | Redis connection URL for caching and sessions (example: `redis://host:port`) |
| `SHOPWARE_ADMIN_ES_ENABLED` | (empty) | Enable Elasticsearch for administration |
| `SHOPWARE_ADMIN_ES_INDEX_PREFIX` | `sw-admin` | Index prefix for administration Elasticsearch |
| `SHOPWARE_ADMIN_ES_REFRESH_INDICES` | (empty) | Refresh administration indices |
| `SHOPWARE_ADMINISTRATION_PATH_NAME` | `admin` | Custom path name for administration interface |
| `SHOPWARE_DBAL_TIMEZONE_SUPPORT_ENABLED` | `0` | Enable timezone support in DBAL |
| `SHOPWARE_DBAL_TOKEN_MINIMUM_LENGTH` | `3` | Minimum token length for DBAL (@deprecated v6.8.0) |
| `SHOPWARE_DISABLE_UPDATE_CHECK` | (empty) | Disable automatic update checks |
| `SHOPWARE_ES_ENABLED` | `0` | Open Search Support Enabled? |
| `SHOPWARE_ES_EXCLUDE_SOURCE` | `0` | Exclude source from Elasticsearch |
| `SHOPWARE_ES_INDEX_PREFIX` | (empty) | Open Search Index Prefix |
| `SHOPWARE_ES_INDEXING_BATCH_SIZE` | `100` | Batch size for Elasticsearch indexing |
| `SHOPWARE_ES_INDEXING_ENABLED` | `0` | Open Search Indexing Enabled? |
| `SHOPWARE_ES_NGRAM_MAX_GRAM` | `5` | Maximum n-gram size for Elasticsearch |
| `SHOPWARE_ES_NGRAM_MIN_GRAM` | `4` | Minimum n-gram size for Elasticsearch |
| `SHOPWARE_ES_THROW_EXCEPTION` | `1` | Whether to throw exceptions on Elasticsearch errors (`1` to enable, `0` to disable) |
| `SHOPWARE_ES_USE_LANGUAGE_ANALYZER` | `1` | Controls whether language-specific analyzers (like `sw_english_analyzer`, `sw_german_analyzer`) are used for search queries. When set to `1`, search queries use the same analyzer as the indexed field, providing broader, more fuzzy search results. When set to `0`, search queries use `sw_whitespace_analyzer` instead, providing less fuzzy search results with fewer matches. |
| `SHOPWARE_HTTP_CACHE_ENABLED` | `1` | Is HTTP Cache enabled? |
| `SHOPWARE_HTTP_DEFAULT_TTL` | `7200` | Default TTL for HTTP Cache |

---

## Framework

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/framework/

# Framework configurations [​](#framework-configurations)

## Overview [​](#overview)

Framework configurations are originated in the [Symfony FrameworkBundle](https://symfony.com/doc/current/reference/configuration/framework.html) and are partially documented in this guide.

---

## Custom routes

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/framework/routes.html

# Custom routes [​](#custom-routes)

## Overview [​](#overview)

Your default routes in Shopware 6 are defined in the controllers of the core or your plugins. An example could be the wishlist route:

php

```shiki
<?php declare(strict_types=1);

#[Route(path: '/wishlist', name: 'frontend.wishlist.page', options: ['seo' => false], defaults: ['_noStore' => true], methods: ['GET'])]
public function index(Request $request, SalesChannelContext $context): Response
{
    $customer = $context->getCustomer();

    if ($customer !== null && $customer->getGuest() === false) {
        $page = $this->wishlistPageLoader->load($request, $context, $customer);
        $this->hook(new WishlistPageLoadedHook($page, $context));
    } else {
        $page = $this->guestPageLoader->load($request, $context);
        $this->hook(new GuestWishlistPageLoadedHook($page, $context));
    }

    return $this->renderStorefront('@Storefront/storefront/page/wishlist/index.html.twig', ['page' => $page]);
}
```

It defines that your wishlist page is available at `/wishlist`. This is fine for an English-only shop, but for a multilingual shop, you might want to have a different route for each language.

For example, you could have `/wishlist` for English and `/merkliste` for German.

## Configuration [​](#configuration)

To easily configure those routes, you can use the `routes.yaml` file in ROOT/config/routes/routes.yaml. Symfony loads this file, which allows you to define your custom `paths`, in our case, for the wishlist index page.

yaml

```shiki
frontend.wishlist.page:
  path:
    en-GB: '/wishlist'
    de-DE: '/merkliste'
  controller: 'Shopware\Storefront\Controller\WishlistController::index'
  methods: ['GET']
  defaults:
    _noStore: true
    _routeScope: ['storefront']
  options:
    seo: false
```

You can configure the `path` with the **locales** (for example, `de-DE`) your shop uses.

If you want to learn more about routes in Symfony, check out the [Symfony documentation](https://symfony.com/doc/current/routing.html#creating-routes-as-attributes).

---

## SameSite protection

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/framework/samesite-protection.html

# SameSite protection [​](#samesite-protection)

INFO

This feature has been introduced with Shopware version 6.4.3.1

## Overview [​](#overview)

The [SameSite configuration](https://symfony.com/doc/current/reference/configuration/framework.html#cookie-samesite) comes with the Symfony FrameworkBundle and supersedes the removed `sw_csrf` Twig function. It is widely [available](https://caniuse.com/same-site-cookie-attribute) in modern browsers and is set to `lax` per default.

For more information, refer to [SameSite cookies site](https://web.dev/articles/samesite-cookies-explained?hl=en)

## Configuration [​](#configuration)

Changes to the `cookie_samesite` attribute can be applied to your `framework.yaml`. The `cookie_secure` ensures that cookies are sent via HTTP or HTTPS, depending on the request's origin.

yaml

```shiki
framework:
  session:
    cookie_secure: 'auto'
    cookie_samesite: lax
```

If you want to deactivate the SameSite protection despite security risks, change the value from `lax` to `null`. For detailed configuration options, check the official [Symfony Docs](https://symfony.com/doc/current/reference/configuration/framework.html#cookie-samesite).

---

## Logging

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/observability/logging.html

# Logging [​](#logging)

## Overview [​](#overview)

Monolog is the logging library for PHP. It is used by Shopware to log errors and debug information. The log files are located in the `var/log` directory of your Shopware installation.

## Configuration [​](#configuration)

Configuration of Monolog is done in the `config/packages/prod/monolog.yaml` file. The following example shows the default configuration:

yaml

```shiki
monolog:
  handlers:
    main:
      type: fingers_crossed
      action_level: error
      handler: nested
      excluded_http_codes: [404, 405]
      buffer_size: 30 # How many messages should be saved? Prevent memory leaks
    business_event_handler_buffer:
      level: error
    nested:
      type: rotating_file
      path: "%kernel.logs_dir%/%kernel.environment%.log"
      level: error
    console:
      type: console
      process_psr_3_messages: false
      channels: ["!event", "!doctrine"]
```

## Log levels [​](#log-levels)

Monolog supports the following log levels:

* `DEBUG`: Detailed debug information.
* `INFO`: Interesting events. Examples: User logs in, SQL logs.
* `NOTICE`: Normal but significant events.
* `WARNING`: Exceptional occurrences that are not errors. Examples: Use of deprecated APIs, poor use of an API, undesirable things that are not necessarily wrong.
* `ERROR`: Runtime errors that do not require immediate action but should typically be logged and monitored.
* `CRITICAL`: Critical conditions. Example: Application component unavailable, unexpected exception.
* `ALERT`: Action must be taken immediately. Example: Entire website down, database unavailable, etc. This should trigger the SMS alerts and wake you up.
* `EMERGENCY`: Emergency: system is unusable.

## Log sent e-mails and other flow events [​](#log-sent-e-mails-and-other-flow-events)

To monitor all sent e-mails and other flow events set the `business_event_handler_buffer` to `info` level:

yaml

```shiki
monolog:
  handlers:
    business_event_handler_buffer:
      level: info
```

INFO

Be aware that this will cost you some performance.

---

## Profiling / Tracing

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/observability/profiling.html

# Profiling [​](#profiling)

Shopware provides a built-in profiler abstraction to measure the performance of code parts and publish this data to a profiler backend.

## Enabling the profiler backends [​](#enabling-the-profiler-backends)

By default, only the Stopwatch profiler (Symfony Profiler Bar) is enabled. To enable the other profiler backends, you have to add the following configuration to your `config/packages/shopware.yaml` file:

yaml

```shiki
shopware:
    profiler:
        integrations:
            - Symfony
            # Requires the dd-trace PHP extension
            - Datadog
            # Requires the tideways PHP extension
            - Tideways
            # Requires the opentelemetry PHP extension
            - OpenTelemetry
```

INFO

The OpenTelemetry profiler is not installed by default. Checkout the [OpenTelemetry Integration](./opentelemetry.html) to learn how to install it.

## Adding custom spans [​](#adding-custom-spans)

To add custom spans to the profiler, you can use the `Shopware\Core\Profiling\Profiler::trace` method:

php

```shiki
use Shopware\Core\Profiling\Profiler;

$value = Profiler::trace('my-example-trace', function () {
    return $myFunction();
});
```

And then you can see the trace in the configured profiler backends.

## Adding a custom profiler backend [​](#adding-a-custom-profiler-backend)

To add a custom profiler backend, you need to implement the `Shopware\Core\Profiling\Integration\ProfilerInterface` interface and register it as a service with the tag `shopware.profiler`.

The following example shows a custom profiler backend that logs the traces to the console:

php

```shiki
namespace App\Profiler;

use Shopware\Core\Profiling\Integration\ProfilerInterface;

class ConsoleProfiler implements ProfilerInterface
{
    public function start(string $title, string $category, array $tags): void
    {
        echo "Start $name\n";
    }

    public function stop(string $title): void
    {
        echo "Stop $name\n";
    }
}
```

XML

```shiki
<service id="App\Profiler">
    <tag name="shopware.profiler" integration="Console"/>
</service>
```

The attribute `integration` is used to identify the profiler backend in the configuration.

---

## OpenTelemetry

**Source:** https://developer.shopware.com/docs/guides/hosting/configurations/observability/opentelemetry.html

# OpenTelemetry [​](#opentelemetry)

OpenTelemetry is a standard to collect distributed traces, metrics and logs from the application. It is similar to tools like NewRelic, Datadog, Blackfire Monitoring and Tideways, but it is completely open source and vendor neutral. That means you can use OpenTelemetry to collect the data and push it to one of the vendors mentioned earlier, or you can use it to collect the data and push it to your own infrastructure with tools like Grafana Stack (Tempo, Loki, Prometheus, Grafana) or other tools.

## Requirements [​](#requirements)

To use OpenTelemetry with Shopware, you need to have the following requirements met:

* `ext-opentelemetry` [PHP extension](https://github.com/open-telemetry/opentelemetry-php-instrumentation)
* `ext-grpc` (optional, required when the transport method is gRPC)

## Installation [​](#installation)

To install the OpenTelemetry Shopware extension, you need to run the following command:

bash

```shiki
composer require shopware/opentelemetry
```

This will install the OpenTelemetry Shopware bundle and create new configuration file `config/packages/prod/opentelemetry.yaml` with Symfony Flex plugin.

This configuration file enables the Shopware Profiler integration with OpenTelemetry in a production environment. Additionally, it specifies that the Monolog output will be directed to OpenTelemetry.

## Configuration [​](#configuration)

After the installation, you will need to set some environment variables to configure both, the OpenTelemetry and its exporter.

### Basic configuration [​](#basic-configuration)

The following configuration enables the OpenTelemetry auto-instrumentation and sets the service name.

text

```shiki
OTEL_PHP_AUTOLOAD_ENABLED=true
OTEL_SERVICE_NAME=shopware
```

Refer to all possible [environment variables](https://opentelemetry.io/docs/instrumentation/php/sdk/#configuration) for better understanding.

### Exporter configuration [​](#exporter-configuration)

The OpenTelemetry extension needs to be configured to export the data to your collector. Here is an example configuration for the OpenTelemetry Collector using gRPC:

text

```shiki
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

If you use gRPC with OpenTelemetry Protocol (OTLP) , you will need to install `open-telemetry/transport-grpc open-telemetry/exporter-otlp` as composer packages.

Refer to this doc for more information about the [exporters](https://opentelemetry.io/docs/languages/php/exporters/).

## Available instrumentation [​](#available-instrumentation)

The OpenTelemetry instrumentation collects following traces:

* Controller
* Symfony HTTP Client
* MySQL Queries

![Example Trace in Grafana](/assets/otel-grafana-trace.BADSwSm_.png)

## Example Grafana Stack [​](#example-grafana-stack)

You can find an example [Stack](https://github.com/shopware/opentelemetry/tree/main/docker) with:

* Grafana (Dashboard)
* Loki (Log storage)
* Prometheus (Metrics storage)
* Tempo (Trace storage)
* OpenTelemetry Collector (Collector for all data and batches it to the storage)

You will need to have the following environment variables in Shopware:

text

```shiki
OTEL_PHP_AUTOLOAD_ENABLED=true
OTEL_SERVICE_NAME=shopware
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

And following two composer packages installed: `open-telemetry/transport-grpc open-telemetry/exporter-otlp`.

The example Grafana is pre-configured to use the data sources, and it is enabled to go from logs to traces and from traces to the logs.

![Explore](/assets/otel-grafana-explore.DJErq7A7.png)![Trace](/assets/otel-grafana-trace.BADSwSm_.png)

---

