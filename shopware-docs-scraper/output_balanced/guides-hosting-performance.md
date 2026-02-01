# Guides Hosting Performance

*Scraped from Shopware Developer Documentation*

---

## Performance

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/

# Performance [​](#performance)

By fine-tuning cache usage, optimizing session and storage management, and employing efficient locking mechanisms, you can significantly improve the overall performance of your online store. Optimizing hosting performance involves considering these factors and implementing appropriate strategies to enhance the speed, scalability, and reliability of your Shopware store.

---

## Cache

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/caches.html

# Cache [​](#cache)

There are several caches in Shopware that can be used to optimize performance. This page gives a brief overview and shows how to configure them.

## Overview [​](#overview)

The HTTP Cache is a *must-have* for every production system. With an enabled cache, the performance of the shop can be greatly increased.

### How to configure the HTTP cache [​](#how-to-configure-the-http-cache)

Basic HTTP cache configuration takes place in the `.env.local` file.

| Name | Description |
| --- | --- |
| `SHOPWARE_HTTP_CACHE_ENABLED` | Enables the HTTP cache |
| `SHOPWARE_HTTP_DEFAULT_TTL` | Defines the default cache time |

`SHOPWARE_HTTP_DEFAULT_TTL` is deprecated and will be removed in Shopware v6.8.0.0. Use [HTTP Caching Policies](#http-caching-policies) instead to define default cache times.

To provide more detailed control over the HTTP cache behavior, use the [HTTP Caching Policies](#http-caching-policies) feature.

The storage used for HTTP Cache is always the [App Cache](#app-cache), see below how to configure it. If you want to move this out of the application cache, you should use an external reverse proxy cache like [Varnish](https://varnish-cache.org/) or [Fastly](https://www.fastly.com/). For more [see here](./../infrastructure/reverse-http-cache.html).

### HTTP Caching Policies [​](#http-caching-policies)

> **Note:** This feature is experimental and subject to change. It will be the default behavior in Shopware v6.8.0.0. To use it now, enable the `CACHE_REWORK` feature flag.

Caching policies allow you to define HTTP cache behavior per area (storefront, store\_api) and per route via configuration. Shopware comes with reasonable defaults, but you can customize them.

#### Configuration [​](#configuration)

##### Defining a policy [​](#defining-a-policy)

By default, Shopware ships with `storefront.cacheable`, `store_api.cacheable` and `no_cache_private` policies. You can define your own policies:

yaml

```shiki
# config/packages/shopware.yaml
shopware:
  http_cache:
    policies:
      custom_policy:
        headers:
          cache_control:
            public: true
            max_age: 600  # browser ttl
            s_maxage: 3600  # reverse proxy ttl
```

Supported `cache_control` directives: `public`, `private`, `no_cache`, `no_store`, `no_transform`, `must_revalidate`, `proxy_revalidate`, `immutable`, `max_age`, `s_maxage`, `stale_while_revalidate`, `stale_if_error`. For more information on these directives, see the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control).

You can redefine existing policies. Note that policy definitions are not merged; redefining an existing policy overrides it completely.

Currently, you can only configure the `cache_control` header.

##### Setting default policies [​](#setting-default-policies)

You can change default `cacheable` and `uncacheable` policies per area (`storefront`, `store_api`):

yaml

```shiki
shopware:
  http_cache:
    default_policies:
      store_api: # the area name
        cacheable: custom_policy # policy to use for cacheable responses
```

##### Fine-tuning per route or app hook [​](#fine-tuning-per-route-or-app-hook)

You can override default policies per route:

yaml

```shiki
shopware:
  http_cache:
    route_policies:
      store-api.product.search: custom_policy
```

App developers can override TTLs from the default policies via script configuration. See [custom endpoints](./../../plugins/apps/app-scripts/custom-endpoints.html#set-the-max-age-of-the-cache-item) for details. You can override this by configuring hook-specific policies using the `route#hook` pattern:

yaml

```shiki
shopware:
  http_cache:
    route_policies:
      frontend.script_endpoint#storefront-acme-feature: storefront.my_custom_policy # storefront-acme-feature is the normalized hook name
```

##### Policy precedence [​](#policy-precedence)

Shopware resolves policies in the following order (highest to lowest priority):

1. `route_policies[route#hook]` - most specific, for script endpoints with hooks (e.g., `frontend.script_endpoint#acme-app-hook`).
2. `route_policies[route]` - route-level override.
3. `default_policies[area].{cacheable|uncacheable}` - area defaults; TTLs (`max-age`, `s-maxage`) can be overridden by values from the request attribute or script configuration.

## How to change the cache storage [​](#how-to-change-the-cache-storage)

The standard Shopware HTTP cache can be exchanged or reconfigured in several ways. The standard cache comes with an `adapter.filesystem`. This is a file-based cache that stores the cache in the `var/cache` directory. This allows Shopware to work out of the box on a single server without any additional configuration. However, this may not be the best solution for a production system, especially if you are using a load balancer or multiple servers. In this case, you should use a shared cache like [Redis](https://redis.io/).

This is a Symfony cache pool configuration and therefore supports all adapters from the [Symfony FrameworkBundle](https://symfony.com/doc/current/cache.html#configuring-cache-with-frameworkbundle).

### Using Redis [​](#using-redis)

Redis is a very fast in-memory key-value store. It is a good choice for caching data that is frequently accessed and does not need to be persisted. Redis can be used as a cache adapter in Shopware. As the cached information is ephemeral and can be recreated, it is not necessary to configure Redis to store the data on disk. For maximum performance, you can configure Redis to use no persistence. Refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details. As key eviction policy, you should use `volatile-lru`. This policy only automatically deletes expired data, as the application explicitly manages the TTL for each cache item. For a detailed overview of Redis key eviction policies, see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

For `cache.adapter.redis_tag_aware` minimum Shopware 6.5.8.3 is required. Otherwise use `cache.adapter.redis`.

yaml

```shiki
# config/packages/cache.yaml
framework:
  cache:
    app: cache.adapter.redis_tag_aware
    system: cache.adapter.redis_tag_aware
    default_redis_provider: redis://localhost
```

Make sure that you have installed the PHP Redis extension before applying this configuration.

The Redis URL can have various formats. The following are all valid:

text

```shiki
# With explicit port
redis://localhost:6379

# With authentication
redis://auth@localhost:6379

# With database
redis://localhost:6379/1

# With options
redis://localhost:6379?timeout=1

# With unix socket

redis:///var/run/redis.sock

# With unix socket and authentication
redis://auth@/var/run/redis.sock
```

For more information or other adapters checkout [Symfony FrameworkBundle](https://symfony.com/doc/current/cache.html#configuring-cache-with-frameworkbundle) documentation.

---

## Performance Test with K6

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/k6.html

# Testing Shopware Performance with K6 [​](#testing-shopware-performance-with-k6)

K6 is a modern load testing tool that makes it easy to test the performance of your Shopware store. It runs scenario's defined in JavaScript and can be used to simulate hundreds of users accessing your store at the same time, so you can see how your store performs under load.

## Prerequisites [​](#prerequisites)

Before you start, make sure you have the following prerequisites:

* A Shopware store
* [K6 installed locally](https://github.com/grafana/k6/releases)
* [Bun](https://bun.sh/)

## Setting up K6 to run against your Shop [​](#setting-up-k6-to-run-against-your-shop)

1.) First we need to clone the [Shopware K6 repository](https://github.com/shopware/k6-shopware) and install the dependencies:

bash

```shiki
git clone https://github.com/shopware/k6-shopware.git
cd k6-shopware
bun install
```

2.) Next copy `.env.example` to `.env` and adjust the values to your Shopware store:

bash

```shiki
cp .env.example .env
```

3.) After setting up the credentials we need to fetch the fixtures (salutation IDs, country IDs, sales channel configuration):

bash

```shiki
bun run fetch-fixtures.ts
```

The K6 test will use the fixtures to find the correct sales channel domain and basic information to create user and orders.

## Preparations on Shopware end [​](#preparations-on-shopware-end)

Before running the tests on your Shopware store, you need to make sure that the following settings are configured:

* No captcha is active in login/register form
* Email sending has been disabled (Admin -> Settings -> System -> Mailer -> Disable email sending)

Also, make sure the Shopware Store has some products and categories, so the test can interact with the store. If you don't have any products, you can use the following command to create some test products:

bash

```shiki
APP_ENV=prod php bin/console framework:demodata
APP_ENV=prod php bin/console dal:refresh:index
```

If you need more than the default 1000 products, you can run the command again with:

bash

```shiki
APP_ENV=prod php bin/console framework:demodata --reset-defaults --products=5000
APP_ENV=prod php bin/console dal:refresh:index
```

The command `framework:demodata` can also execute multiple times in parallel, so you can create a lot of products in a short time. Just make sure that you run `dal:refresh:index` after all processes are finished.

## Running the tests [​](#running-the-tests)

WARNING

When running against a production environment, make sure you have informed your hosting provider. Your IP may be blocked for a short time or limited to a certain number of requests, which could lead to a false positive. Grafana Cloud is generally recommended as it allows you to distribute the load across multiple locations.

To run the tests, we need an scenario file. The repository comes with a example scenario file that you can use to test your store.

javascript

```shiki
// example.js
import {
  accountRegister,
  addProductToCart,
  placeOrder,
  visitCartPage,
  visitConfirmPage,
  visitNavigationPage,
  visitProductDetailPage,
  visitSearchPage,
  visitStorefront,
} from "./helpers/storefront.js";

export default function () {
  visitStorefront();
  visitSearchPage();
  visitNavigationPage();
  accountRegister();
  visitNavigationPage();
  addProductToCart(visitProductDetailPage().id);
  visitCartPage();
  visitConfirmPage();
  placeOrder();
}
```

So the test does:

* Visits home page
* Visits a search page with random term
* Visits a random navigation page
* Registers a new account
* Visits a random navigation page
* Visits a product detail page and adds the product to the cart
* Visits the cart page
* Visits the confirm page
* Places an order

and then the session ends and a new session starts and does it again.

To run the test, you can use the following command:

bash

```shiki
k6 run example.js
```

This will run the test with 1 virtual user and 1 iteration, so you can verify that the test is working correctly. To run the test with more virtual users and iterations, you can use the following command:

bash

```shiki
k6 run --vus 10 --iterations 100 example.js
```

so now the test will run with 10 virtual users and 100 iterations.

## Running multiple scenarios [​](#running-multiple-scenarios)

You can also run multiple scenarios in the same file. To do this, you can define them in the options like so:

javascript

```shiki
// example.js
import { productChangePrice, productChangeStocks, fetchBearerToken, useCredentials, productImport } from "./helpers/api.js";
import {
  accountRegister,
  addProductToCart,
  placeOrder,
  visitNavigationPage,
  visitProductDetailPage,
  visitSearchPage,
  visitStorefront,
} from "./helpers/storefront.js";

export const options = {
  scenarios: {
    browse_only: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m',
      exec: 'browseOnly',
    },
    fast_buy: {
      executor: 'constant-vus',
      vus: 1,
      duration: '5m',
      exec: 'fastBuy',
    },
    import: {
      executor: 'constant-vus',
      vus: 1,
      duration: '5m',
      exec: 'importer',
    }
  },
};

export function browseOnly() {
  visitStorefront();
  visitSearchPage();
  visitNavigationPage();
  visitProductDetailPage();
}

export function fastBuy() {
  addProductToCart(visitProductDetailPage().id);
  accountRegister();
  placeOrder();
}

export function setup() {
  const token = fetchBearerToken();

  return { token };
}

export function importer(data) {
  useCredentials(data.token);
  productImport();
  productChangePrice();
  productChangeStocks();
}
```

and then you can run the test with the following command:

bash

```shiki
k6 run example.js
```

This will run the test with 3 scenarios, `browse_only`, `fast_buy` and `import`. When using scenarios, you cannot define the users and iterations anymore in the command-line. They need to be configured in the `options` object in your script.

There are a lot of options how the scenarios should work together, you can find more information in the [K6 documentation](https://grafana.com/docs/k6/latest/using-k6/scenarios/).

## Enabling the K6 dashboard [​](#enabling-the-k6-dashboard)

K6 has an embedded dashboard that you can use to monitor the test results in real-time. To enable the dashboard, you can use the following command:

bash

```shiki
K6_WEB_DASHBOARD=true k6 run --vus 10 --duration 5m example.js
```

and then you can open <http://127.0.0.1:5665/ui/?endpoint=/> in your browser to see the dashboard.

![K6 Dashboard](/assets/k6-dashboard.nV1u_fGE.png)

## Running the tests in the Cloud with K6 Cloud [​](#running-the-tests-in-the-cloud-with-k6-cloud)

You can also run the tests in the cloud with K6 Cloud. To do this, you need to create an account on the [K6 Cloud](https://grafana.com/products/cloud/k6/) and get an API token. This allows you to utilize the K6 Cloud infrastructure to run the tests with a lot of more users, customize the location of the users and get more detailed reports with Grafana Dashboards.

![K6 Cloud Dashboard](/assets/k6-cloud.CfxkREwa.png)

---

## Session

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/session.html

# Shopware Session [​](#shopware-session)

Shopware, by default, uses the session storage configured in PHP. On most installations, this is the file system. In smaller setups, you will not need to take care of sessions. However, for larger setups using clustering or with a lot of traffic, you will probably configure alternative session storage, such as Redis, to reduce the load on the database.

## Session adapters [​](#session-adapters)

### Configure Redis using PHP.ini [​](#configure-redis-using-php-ini)

By default, Shopware uses the settings configured in PHP. You can reconfigure the Session config directly in your `php.ini`. Here is an example of configuring it directly in PHP.

ini

```shiki
session.save_handler = redis
session.save_path = "tcp://host:6379?database=0"
```

Please refer to the official [PhpRedis documentation](https://github.com/phpredis/phpredis#php-session-handler) for all possible options.

### Configure Redis using Shopware configuration [​](#configure-redis-using-shopware-configuration)

If you don't have access to the php.ini configuration, you can configure it directly in Shopware itself. For this, create a `config/packages/redis.yml` file with the following content:

yaml

```shiki
# config/packages/redis.yml
framework:
    session:
        handler_id: "redis://host:port/0"
```

### Redis configuration [​](#redis-configuration)

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `allkeys-lru`, which only automatically deletes the last recently used entries when Redis reaches max memory consumption. For a detailed overview of Redis key eviction policies see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

### Other adapters [​](#other-adapters)

Symfony also provides PHP implementations of some adapters:

* [PdoSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/PdoSessionHandler.php)
* [MemcachedSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/MemcachedSessionHandler.php)
* [MongoDbSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/MongoDbSessionHandler.php)

To use one of these handlers, you must create a new service in the dependency injection and set the `handler_id` to the service id.

Example service definition:

xml

```shiki
<service id="session.db" class="Symfony\Component\HttpFoundation\Session\Storage\Handler\PdoSessionHandler">
    <argument ....></argument>
</service>
```

Example session configuration:

yaml

```shiki
# config/packages/redis.yml
framework:
    session:
        handler_id: "session.db"
```

---

## Increment Storage

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/increment.html

# Increment Storage [​](#increment-storage)

The increment storage is used to store status and display it in the Administration. This can include

* Status of the message queue
* Last used module of Administration users

This storage increments or decrements a given key in a transaction-safe way, which causes locks upon the storage.

Shopware uses the `increment` table to store such information by default. When multiple message consumers are running, this table can be locked very often, decreasing workers' performance. By using different storage, the performance of those updates can be improved.

## Using Redis as storage [​](#using-redis-as-storage)

To use Redis, create a `config/packages/shopware.yml` file with the following content

### Redis configuration [​](#redis-configuration)

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as otherwise you might risk losing data. For a detailed overview of Redis key eviction policies refer to the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

## Disabling the increment storage [​](#disabling-the-increment-storage)

The usage of the increment storage is optional and can be disabled. When this feature is disabled, Queue Notification and Module Usage Overview will not work in the Administration.

To disable it, create a `config/packages/shopware.yml` file with the following content:

yaml

```shiki
shopware:
    increment:
        user_activity:
            type: 'array'

        message_queue:
            type: 'array'
```

---

## Lock Storage

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/lock-store.html

# Lock store [​](#lock-store)

Shopware uses [Symfony's lock component](https://symfony.com/doc/5.x/lock.html) to implement locking functionality. By default, Symfony will use a local lock store. This means in multi-machine (cluster) setups, naive file locks will break the system; therefore, it is highly recommended to use one of the [supported remote stores](https://symfony.com/doc/5.x/components/lock.html#available-stores).

## Using Redis as a lock store [​](#using-redis-as-a-lock-store)

As Redis can already be used for [caching](./caches.html), [increment store](./increment.html), and [session storage](./session.html), you can also use that Redis host as a remote lock store. To use Redis, configure the lock store to use a Redis DSN. Create a `config/packages/lock.yaml` file with the following content:

yaml

```shiki
framework:
    lock: 'redis://host:port/dbindex'
```

For example, to use Redis running on localhost port 6379 with database 0:

yaml

```shiki
framework:
    lock: 'redis://127.0.0.1:6379/0'
```

## Other lock stores [​](#other-lock-stores)

As Shopware uses [Symfony's lock component](https://symfony.com/doc/5.x/lock.html), all lock stores supported by Symfony can be used. Keep in mind that you should always use a remote store if you host Shopware in a cluster setup. For a list of all available lock stores, refer to [Symfony's documentation](https://symfony.com/doc/5.x/components/lock.html#available-stores). There is also more detailed information on the [configuration options](https://symfony.com/doc/5.x/lock.html#configuring-lock-with-frameworkbundle).

---

## Number Ranges

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/number-ranges.html

# Number Ranges [​](#number-ranges)

Number Ranges provide a consistent way to generate a consecutive number sequence that is used for order numbers, invoice numbers, etc. The generation of the number ranges is an **atomic** operation. This guarantees that the sequence is consecutive and that no number is generated twice.

By default, the number range states are stored in the database. In scenarios where high throughput is required (e.g., thousands of orders per minute), the database can become a performance bottleneck because of the requirement for atomicity. Redis offers better support for atomic increments than the database. Therefore the number ranges should be stored in Redis in such scenarios.

## Using Redis as storage [​](#using-redis-as-storage)

To use Redis, create a `config/packages/shopware.yml` file with the following content:

### Redis configuration [​](#redis-configuration)

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as otherwise you might risk losing data. For a detailed overview of Redis key eviction policies refer to the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

## Migrating between storages [​](#migrating-between-storages)

You can migrate the current state of the number ranges from your current storage to a new one by running the following CLI command:

shell

```shiki
bin/console number-range:migrate {fromStorage} {toStorage}
```

For example, if you want to migrate from the default `SQL` storage to the high-performing `Redis` storage, the command is:

shell

```shiki
bin/console number-range:migrate SQL Redis
```

INFO

If you want to migrate from or to `Redis`, ensure the `shopware.number_range.redis_url` is correctly configured, regardless if `Redis` is currently configured as the `increment_storage`.

WARNING

The migration of the number ranges between different storages is **not atomic**. This means that if you migrate the number ranges and simultaneously generate new number increments, this may lead to the same number being generated twice. Therefore, this command should normally not run during normal operations of the shop but rather during part of a deployment or maintenance.

---

## Cart Storage

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/cart-storage.html

# Cart Storage [​](#cart-storage)

By default, shopware stores the cart in the database. This can be a performance bottleneck in scenarios where high throughput is required (e.g., thousands of orders per minute), especially if a DB cluster with a read/write-split is used. Additionally, as the content in that table can change quite quickly, it can lead to an explosion of the databases `binlog` file.

Redis is better suited in high-throughput scenarios, therefore you should use Redis as storage for the cart in such scenarios.

## Using Redis as storage [​](#using-redis-as-storage)

To use Redis, create a `config/packages/shopware.yml` file with the following content:

 Note that the `?persistent=1` parameter here refers to the connection pooling, not the persistent storage of data. Please refer to the [Redis configuration guide](../infrastructure/redis) for more information.\*

## Migrating between storages [​](#migrating-between-storages)

You can migrate the current carts from the DB to Redis by running the following CLI command:

shell

```shiki
bin/console cart:migrate {fromStorage} {redisUrl?}
```

INFO

Providing the redis URL is optional. If not provided, the value from the configuration will be used. If it is not configured in the yaml file, you need to provide the URL.

For example, if you want to migrate from the default `SQL` storage to the high-performing `Redis` storage, the command is:

shell

```shiki
bin/console cart:migrate sql
```

## Redis configuration [​](#redis-configuration)

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes carts that are expired, as otherwise you might risk of losing data. For a detailed overview of Redis key eviction policies see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

---

## Performance Tweaks

**Source:** https://developer.shopware.com/docs/guides/hosting/performance/performance-tweaks.html

# Performance Tweaks [​](#performance-tweaks)

Shopware is a platform for many different projects. It needs to handle a broad range of load characteristics and environments. It means that the default configuration is optimized for the best out-of-the-box experience. However, there are many opportunities to increase the performance by fitting the configuration to your needs.

## HTTP cache [​](#http-cache)

To ensure a high RPS (Requests Per Second), Shopware offers an integrated HTTP cache with a possible reverse proxy configuration. Any system that handles high user numbers should always use HTTP caching to reduce server resources.

To enable this, set `SHOPWARE_HTTP_CACHE_ENABLED=1` in the `.env`

### Reverse proxy cache [​](#reverse-proxy-cache)

When you have many app servers, you should consider using a [reverse proxy cache](./../infrastructure/reverse-http-cache.html) like Varnish. Shopware offers a default configuration for Varnish out-of-the-box and a [Varnish Docker image](https://github.com/shopware/varnish-shopware) for development.

### Logged-in / cart-filled [​](#logged-in-cart-filled)

By default, Shopware can no longer deliver complete pages from a cache for a logged-in customer or if products are in the shopping cart. As soon as this happens, the user sessions differ, and the context rules could be different depending on the user. This results in different content for each customer. A good example is the [Dynamic Access](https://docs.shopware.com/en/shopware-6-en/extensions/dynamiccontent) plugin.

However, if the project does not require such functionality, pages can also be cached by the HTTP cache/reverse proxy. To disable cache invalidation in these cases:

yaml

```shiki
# config/packages/prod/shopware.yaml
shopware:
    cache:
        invalidation:
            http_cache: []
```

### Redis for delayed cache invalidation [​](#redis-for-delayed-cache-invalidation)

The HTTP cache will be invalidated in regular intervals, benefitting systems with a high update frequency for the inventory (products, categories). Once the instruction to delete the cache entries for a specific product or category occurs, they are not deleted instantly but processed later by a background task. Thus, if two processes invalidate the cache in quick succession, the timer for the invalidation of this cache entry will only reset. By default, the scheduled task will run every 20 seconds, but the interval can be adjusted over the `scheduled_taks` DB table, by setting the `run_interval` to the desired value (it is configured in seconds) for the entry with the name `shopware.invalidate_cache`.

Information about which tags need to be invalidated is stored in the DB. However, especially in systems which have a high number of concurrent write requests, this can become a bottleneck, and at a certain load, deadlocks are inevitable. If you already use Redis, use it also for the delayed cached. The MySQL adapter should only be used when you cannot use Redis. To offload this to a Redis instance, you can configure the following:

yaml

```shiki
# config/packages/prod/shopware.yaml
shopware:
    cache:
        invalidation:
            delay_options:
                storage: redis
                connection: 'ephemeral' # connection name from redis configuration
```

### Cache control header for assets [​](#cache-control-header-for-assets)

If you are using a CDN to provide assets, ensure that the assets utilize the `Cache-Control` header. E.g., `public, max-age=86400`. How this is achieved is highly dependent on the setup. Please refer to the docs of your server components in use.

## MySQL configuration [​](#mysql-configuration)

Shopware sets some MySQL configuration variables on each request to ensure it works in any environment. You can disable this behavior if you have correctly configured your MySQL server.

* Make sure that `group_concat_max_len` is by default higher or equal to `320000`
* Make sure that `sql_mode` doesn't contain `ONLY_FULL_GROUP_BY`

## SQL is faster than DAL [​](#sql-is-faster-than-dal)

The DAL (Data Abstraction Layer) has been designed suitably to provide developers with flexible and extensible data management. However, features in such a system come at the cost of performance. Therefore, using DBAL (plain SQL) is much faster than using the DAL in many scenarios, especially when it comes to internal processes, where often only one ID of an entity is needed.

Refer to this article to know more on [when to use plain SQL and DAL](./../../../resources/references/adr/2021-05-14-when-to-use-plain-sql-or-dal.html).

## Elasticsearch/Opensearch [​](#elasticsearch-opensearch)

Elasticsearch/Opensearch is a great tool to reduce the load of the MySQL server. Especially for systems with large product assortments, this is a must-have since MySQL simply does not cope well above a certain assortment size.

When using Elasticsearch, it is important to set the `SHOPWARE_ES_THROW_EXCEPTION=1` `.env` variable. This ensures that there is no fallback to the MySQL server if an error occurs when querying the data via Elasticsearch. In large projects, the failure of Elasticsearch leads to the MySQL server being completely overloaded otherwise.

Read more on [Elasticsearch setup](./../infrastructure/elasticsearch/elasticsearch-setup.html)

## Prevent mail data updates [​](#prevent-mail-data-updates)

To provide auto-completion for different mail templates in the Administration UI, Shopware has a mechanism that writes an example mail into the database when sending the mail.

With the `shopware.mail.update_mail_variables_on_send` configuration, you can disable this source of database load:

yaml

```shiki
# config/packages/prod/shopware.yaml
shopware:
    mail:
        update_mail_variables_on_send: false
```

If you ever wonder why it is in `prod`, take a look into the [Symfony configuration environments](https://symfony.com/doc/current/configuration.html#configuration-environments).

## Increment storage [​](#increment-storage)

The [Increment storage](./../performance/increment.html) is used to store the state and display it in the Administration. This storage increments or decrements a given key in a transaction-safe way, which causes locks upon the storage. Therefore, we recommend moving this source of server load to a separate Redis, as described in [Increment storage Redis configuration](./increment.html#redis-configuration).  
 If you don't need such functionality, it is highly recommended that you disable this behavior by using `array` as a type.

## Lock storage [​](#lock-storage)

Shopware uses [Symfony's Lock component](https://symfony.com/doc/5.x/lock.html) to implement locking functionality. By default, Symfony will use a local file-based [lock store](./../performance/lock-store.html), which breaks into multi-machine (cluster) setups. This is avoided using one of the [supported remote stores](https://symfony.com/doc/5.x/components/lock.html#available-stores). For more information on how to configure the lock store, refer to the [Lock storage guide](./lock-store.html).

## Number ranges [​](#number-ranges)

[Number Ranges](./../performance/number-ranges.html) provide a consistent way to generate a consecutive number sequence that is used for order numbers, invoice numbers, etc. The generation of the number ranges is an **atomic** operation, which guarantees that the sequence is consecutive and no number is generated twice.

By default, the number range states are stored in the database. In scenarios where high throughput is required (e.g., thousands of orders per minute), the database can become a performance bottleneck because of the requirement for atomicity. Redis offers better support for atomic increments than the database. Therefore, the number ranges should be [stored in Redis](./number-ranges.html#using-redis-as-storage) in such scenarios.

## Sending mails with the Queue [​](#sending-mails-with-the-queue)

Shopware sends the mails synchronously by default. This process can take a while when the remote SMTP server is struggling. For this purpose, it is possible to handle the mails in the message queue. To enable this, add the following config to your config:

yaml

```shiki
# config/packages/prod/framework.yaml
framework:
    mailer:
        message_bus: 'messenger.default_bus'
```

## PHP Config tweaks [​](#php-config-tweaks)

ini

```shiki
; don't evaluate assert()
zend.assertions=-1

; cache file_exists,is_file
; WARNING: this will lead to thrown errors after clearing cache while it tries to access cached Shopware_Core_KernelProdDebugContainer.php
opcache.enable_file_override=1

; increase opcache string buffer as shopware has many files
opcache.interned_strings_buffer=20

; disables opcache validation for timestamp for reinvalidation of the cache
; WARNING: you need to clear on deployments the opcache by reloading php-fpm or cachetool (https://github.com/gordalina/cachetool)
opcache.validate_timestamps=0

; disable check for BOM
zend.detect_unicode=0

; increase default realpath cache
realpath_cache_ttl=3600
```

INFO

The web updater is not compatible with opcache, as updates require an opcache clear.

Also, PHP PCRE Jit Target should be enabled. This can be checked using `php -i | grep 'PCRE JIT Target'` or looking into the *phpinfo* page.

For an additional 2-5% performance improvement, it is possible to provide a preload file to opcache. Preload also brings a lot of drawbacks:

* Each cache clear requires a PHP-FPM restart
* Each file change requires a PHP-FPM restart
* The Extension Manager does not work

The PHP configuration would look like:

ini

```shiki
opcache.preload=/var/www/html/var/cache/opcache-preload.php
opcache.preload_user=nginx
```

## .env.local.php [​](#env-local-php)

[Symfony recommends](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production) that a `.env.local.php` file is used in production instead of a `.env` file to skip parsing of the `.env` file on every request. If you are using a containerized environment, all those variables can also be set directly in the environment variables instead of dumping them into a file.

Since Shopware v6.4.15.0, you can dump the content of the `.env` file to a `.env.local.php` file by running `bin/console system:setup --dump-env` or `bin/console dotenv:dump {APP_ENV}`.

## Benchmarks [​](#benchmarks)

In addition to the benchmarks that Shopware regularly performs with the software, we strongly recommend integrating your benchmark tools and pipelines for larger systems. A generic benchmark of a product can rarely be adapted to individual, highly customized projects. Tools such as [locust](https://locust.io/) or [k6](https://k6.io/) can be used for this purpose.

## Logging [​](#logging)

Set the log level of the monolog to `error` to reduce the number of logged events. Also, limiting the `buffer_size` of monolog prevents memory overflows for long-lived jobs:

yaml

```shiki
# config/packages/prod/monolog.yaml
monolog:
    handlers:
        main:
            level: error
            buffer_size: 30
        business_event_handler_buffer:
            level: error
```

The `business_event_handler_buffer` handler logs flow. Setting it to `error` will disable the logging of flow activities that succeed.

## Disable App URL external check [​](#disable-app-url-external-check)

On any Administration load, Shopware tries to request itself to test that the configured `APP_URL` inside `.env` is correct. If your `APP_URL` is correct, you can disable this behavior with an environment variable `APP_URL_CHECK_DISABLED=1`.

## Using zstd instead of gzip for compression [​](#using-zstd-instead-of-gzip-for-compression)

Shopware uses `gzip` for compressing the cache elements and the cart when enabled. `gzip` saves a lot of storage, but it can be slow with huge values.

Since Shopware v6.6.4.0, it has been possible to use `zstd` as an alternative compression algorithm. `zstd` is faster than `gzip` and has a better compression ratio. Unfortunately, `zstd` is not included by default in PHP, so you need to install the extension first.

yaml

```shiki
# Enabling cart compression with zstd
shopware:
    cart:
      compress: true
      compression_method: zstd
```

DANGER

If you are changing the **cache** compression method, you need to clear the cache after changing the configuration.

yaml

```shiki
# Enabling cache compression with zstd
shopware:
  cache:
    cache_compression: true
    cache_compression_method: 'zstd'
```

## Disable Symfony Secrets [​](#disable-symfony-secrets)

Symfony has a [secret](https://symfony.com/doc/current/configuration/secrets.html) implementation. That allows the encryption of environment variables and their decryption on the fly. If you don't use Symfony Secrets, you can disable this complete behaviour, saving some CPU cycles while booting the application.

yaml

```shiki
framework:
  secrets:
    enabled: false
```

## Disable auto\_setup [​](#disable-auto-setup)

By default, [Symfony Messenger](https://symfony.com/doc/current/messenger.html#transport-configuration) checks if the queue exists and creates it when not. This can be an overhead when the system is under load. Therefore, make sure that you disable the `auto_setup` in the connection URL like so: `redis://localhost?auto_setup=false`. That query parameter can be passed to all transports. After disabling `auto_setup`, make sure you are running `bin/console messenger:setup-transports` during deployment to make sure that the transports exist, or when you use the [Deployment Helper](./../installation-updates/deployments/deployment-helper.html) it will do that for you.

## Disable Product Stream Indexer [​](#disable-product-stream-indexer)

INFO

This is available starting with Shopware 6.6.10.0

The **Product Stream Indexer** is a background process that creates a mapping table of products to their streams. It is used to find which category pages are affected by product changes. On a larger inventory set or a high update frequency, the **Product Stream Indexer** can be a performance bottleneck.

Disabling the Product Stream Indexer has the following disadvantages:

* When you change a product in a stream, the category page is not updated until the HTTP cache expires
  + You could also explicitly update the category page containing the stream to workaround if that is a problem
* Also, the Line Item in the Stream Rule will always be evaluated to `false`

To disable the Product Stream Indexer, you can set the following configuration:

yaml

```shiki
shopware:
  product_stream:
    indexing: false
```

## Disable Scheduled Sitemap Generation [​](#disable-scheduled-sitemap-generation)

INFO

This is available starting with Shopware v6.7.1.0

The sitemap generation can be a resource-intensive and time-consuming task, especially for shops with large product catalogs. When running as a scheduled task through the message queue, it can block the queue for an extended period, preventing other important tasks from being processed.

To disable the scheduled sitemap generation and set up your own cronjob instead, you can use the following configuration:

yaml

```shiki
# config/packages/prod/shopware.yaml
shopware:
    sitemap:
        scheduled_task:
            enabled: false
```

After disabling the scheduled task, you should set up a dedicated cronjob to generate the sitemap at a time that suits your needs:

bash

```shiki
# Example crontab entry to run sitemap generation daily at 2 AM
0 2 * * * cd /path/to/shopware && php bin/console sitemap:generate
```

This approach offers several advantages:

* The message queue remains available for other tasks
* You can schedule sitemap generation during off-peak hours
* You have better control over when this resource-intensive task runs
* You can run it on a dedicated worker server if needed

## Enable the Speculation Rules API [​](#enable-the-speculation-rules-api)

INFO

This feature is available starting with Shopware 6.6.10.0

The Speculation Rules API allows browsers to pre-render pages based on user interactions or immediately, depending on the eagerness setting. This can improve the perceived performance of a website by loading pages in the background before the user navigates to them.

You can enable that **experimental feature** via `Admin > Settings > System > Storefront`. The JavaScript Plugin will then check if the [Browser supports the Speculation Rules API](https://caniuse.com/mdn-http_headers_speculation-rules) and if so, it will add a script tag to the head of the document. For the [eagerness setting](https://developer.chrome.com/docs/web-platform/prerender-pages#eagerness) we are using `moderate` everywhere. That means **a user must interact** with a link to execute the pre-rendering.

INFO

Keep in mind that pre-rendering puts extra load on your server and also can affect your [Analytics](https://developer.chrome.com/docs/web-platform/prerender-pages#impact-on-analytics).

## Optimize class loading [​](#optimize-class-loading)

### opcache.max\_accelerated\_files [​](#opcache-max-accelerated-files)

PHP loads many classes on each request, which can be a performance bottleneck. To optimize this, make sure `opcache.max_accelerated_files` is set to `20000` or higher.

### classmap-authoritative [​](#classmap-authoritative)

Additionally, when all plugins are installed directly through Composer and managed by Composer, you can generate a static autoloader which does no class mapping at runtime.

To enable this, set the following configuration in your `composer.json`:

diff

```shiki
"config": {
        "allow-plugins": {
            "symfony/flex": true,
            "symfony/runtime": true
        },
        "optimize-autoloader": true,
+       "classmap-authoritative": true,
        "sort-packages": true
},
```

For more information, check out the [Composer documentation](https://getcomposer.org/doc/articles/autoloader-optimization.md#optimization-level-2-a-authoritative-class-maps).

### opcache.preload [​](#opcache-preload)

To completely reduce the class loading at runtime, you can enable `opcache.preload` by setting it to `<project-root>/var/cache/opcache-preload.php` and `opcache.preload_user` to the user running the PHP process. This will preload all classes into the opcache on PHP-FPM startup and reduce the class loading at runtime.

WARNING

When using `opcache.preload`, you need to **restart** the PHP-FPM after each modification to reload the preloaded classes.

---

