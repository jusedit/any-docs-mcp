# Guides Hosting Infrastructure

*Scraped from Shopware Developer Documentation*

---

## Infrastructure

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/

# Infrastructure [​](#infrastructure)

The Hosting infrastructure for Shopware includes Elasticsearch for advanced search, a database cluster for data storage, a filesystem for media files, a message queue for asynchronous communication, a rate limiter for request management, and a reverse HTTPS proxy for secure communication.

More detailed information is described in the following sections.

---

## Elasticsearch

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/elasticsearch/

# Elasticsearch [​](#elasticsearch)

Elasticsearch is a robust search engine that can be integrated into Shopware to provide advanced search capabilities. It also supports AND/OR operations.

The following sections will help you to set up, configure, debug, resolve indexing issues, and optimize performance. By following these steps, you can leverage Elasticsearch to enhance search functionality in your Shopware store.

---

## Set up Elasticsearch

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.html

# Set up Elasticsearch [​](#set-up-elasticsearch)

## Overview [​](#overview)

When a project uses several thousand data sets, it's worth integrating Elasticsearch. Shopware's Elasticsearch integration is provided in the [shopware/elasticsearch](https://github.com/shopware/elasticsearch) bundle. If your project doesn't include it yet, you can add it via `composer require shopware/elasticsearch`. This documentation gives you an overview of Elasticsearch's functionalities on your server, as well as the configuration, activation, and indexing processes in Shopware for live and test environments.

INFO

Currently, the implementation for Elasticsearch/Opensearch works in the same way.

## Requirements [​](#requirements)

* A supported OpenSearch (or Elasticsearch) server

[Requirements](../../../installation/requirements#recommended-stack-and-supported-versions)

* [Running message queue workers in the background](./../message-queue.html)

## Server basics [​](#server-basics)

Elasticsearch installation and configuration greatly depend on your operating system and hosting provider. You will find extensive documentation online regarding the installation and configuration of Elasticsearch on most common Linux distributions. Some hosting providers might also provide specific documentation regarding this subject. Installation on macOS or Windows is also possible but not officially supported.

The current Shopware 6 integration is designed to work with the out-of-the-box configuration of Elasticsearch. This does not mean, of course, that these are the best settings for a production environment. Although they will affect performance and security, the settings you choose to use on your Elasticsearch setup will be mostly transparent to your Shopware installation. The best setting constellation for your shop will greatly depend on your server setup, the number, and structure of products, and replication requirements, to name a few. In this document, we can't give you specific examples for your setup, but provide you with hints and basics you might need to choose your perfect setup. More detailed information can be found on the official [Elasticsearch](https://www.elastic.co/guide/index.html) documentation page.

### Elasticsearch server setup [​](#elasticsearch-server-setup)

Elasticsearch is meant to be used as a cluster setup so it can scale properly and provide you with reliability. In this cluster, you can choose how many nodes you want to use and which different type each node in the cluster shall have. A one-node cluster should only be used for development or test environments, because it can't scale and does not provide additional reliability. Reliability is given when you have at least three nodes because of the process of election of the master node. This is further explained in more detail in the [Master Node](#master-node) section. From our experience, the best way is to have a cluster with five nodes. You can have the three needed master-eligible nodes and 2 nodes which are data nodes and do not proceed in the election process. Which cluster is really needed in your setup and fits your needs best is up to you.

Most configurations of the Elasticsearch cluster can be done in the elasticsearch.yml file you find in the [config folder](https://www.elastic.co/guide/en/elasticsearch/reference/master/settings.html#config-files-location). This file configures, for example, the name of your cluster (`cluster.name`), the name of your node (`node.name`), nodes that know each other (`discovery.seed_hosts`), the type of the node (`node.master`, `node.data`, `node.ingest`), the host (`network.host`) and the port (`network.host`). Sometimes it makes sense to configure your [JVM](https://www.elastic.co/guide/en/elasticsearch/reference/master/advanced-configuration.html#set-jvm-options) as well. You should only make changes here if you know exactly what you do. Most hosting partners will provide you with a fitting setup that will not require many changes here. The data files of the index will be found in the data directory later on. Another important folder is the `logs` folder. If not configured differently, you will find the different logfiles for your cluster here in case you ever need to check an error or slowlog.

### Nodes [​](#nodes)

Every instance of Elasticsearch starts a node. A collection of connected nodes is called a cluster. All nodes can handle HTTP and transport traffic. Depending on your setup, the necessary performance, and reliability, you might want to have dedicated nodes of the following types in your cluster.

#### Master nodes [​](#master-nodes)

Master nodes are in charge of the cluster-wide settings and changes like CRUD operations of indices, including mappings and settings of those, adding nodes, removing nodes, and allocating the [shards](#shards) to the nodes. A productive cluster of Elasticsearch should always contain three nodes that are all master-eligible nodes set by the `node.master` property in the elasticsearch.yml file. The master node is chosen by an election process of which only the master-eligible nodes are part. In an election process, you have to mind a quorum of master-eligible nodes, so you get a specific result of the election, so you should have N/2+1 master-eligible nodes. Three is the minimum number for this because then the currently elected master node fails, you can still have a correct election process for a new master. The setting "cluster.initial\_master\_nodes: ["masternode1","masternode2","masternode3"]" should be provided on each of those master-eligible nodes on start.

#### Ingest nodes [​](#ingest-nodes)

Ingest nodes provide the ability to pre-process a document before it gets indexed. The ingest node intercepts bulk and index requests, applies transformations, and then passes the documents back to the index or bulk APIs. All nodes are Ingest nodes by default. This can be changed by the `node.ingest` property in the elasticsearch.yml file.

#### Data nodes [​](#data-nodes)

Data nodes have two main features: they hold the [shards](#shards) that contain the documents/elements you have indexed and execute data-related operations like CRUD, search, and aggregations. By default, all nodes are Data nodes, which can be changed using the `node.data` property in the elasticsearch.yml file. Data nodes are very resource-intensive, so you definitely want to monitor the resources and add more data nodes if they are overloaded.

### Shards [​](#shards)

A shard is a worker unit that holds the data of the index and can be assigned to a node. There are two types of shards:

* **Primary**: A primary shard contains the original data.
* **Replica**: A replica is a copy of a primary shard.

The number of replica shards is up to you and the reliability you need in your cluster. The more replica shards you have, the more nodes can fail before the data in the shard becomes unavailable. But reliability is not the only usage of a replica shard. Queries like search can be performed on a primary or replica. So if you have replicas of your shards, you can better scale your data and cluster resources. A replica is only created when there are enough nodes because a replica can never be created in the same node as its primary or another replica of its primary. The master node determines where the shard is distributed. Normally a shard in Elasticsearch can hold at least tens of gigabytes, so you might want to keep this in mind when setting your number of shards and replicas.

## Prepare Shopware for Elasticsearch [​](#prepare-shopware-for-elasticsearch)

### Variables in your *.env* [​](#variables-in-your-env)

| Variable | Possible values | Description |
| --- | --- | --- |
| `APP_ENV` | `prod` / `dev` | This variable is important if you want to activate the debug mode and see possible errors of Elasticsearch. You have to set the variable to dev for debug mode and prod if you want to use Elasticsearch in a productive system. |
| `OPENSEARCH_URL` | `localhost:9200` | A comma separated list of Elasticsearch hosts. You can find the possible formats [here](https://www.elastic.co/guide/en/elasticsearch/client/php-api/current/host-config.html#inline-host-config) |
| `SHOPWARE_ES_INDEXING_ENABLED` | `0` / `1` | This variable activates the indexing to Elasticsearch |
| `SHOPWARE_ES_ENABLED` | `0` / `1` | This variable activates the usage of Elasticsearch for your shop |
| `SHOPWARE_ES_INDEX_PREFIX` | `sw_myshop` | This variable defines the prefix for the Elasticsearch indices |
| `SHOPWARE_ES_THROW_EXCEPTION` | `0` / `1` | This variable activates the debug mode for Elasticsearch. Without this variable as = 0 you will get a fallback to mysql without any error message if Elasticsearch is not working |

INFO

The `SHOPWARE_ES_INDEXING_ENABLED` and `SHOPWARE_ES_ENABLED` can seem as a duplicate setting, but has it's purpose. Here are two use cases for setting these differently:

## Full Support [​](#full-support)

`SHOPWARE_ES_ENABLED=1` + `SHOPWARE_ES_INDEXING_ENABLED=1` - Both search and indexing enabled.

## Read-Only [​](#read-only)

`SHOPWARE_ES_ENABLED=1` + `SHOPWARE_ES_INDEXING_ENABLED=0` - Search enabled, indexing disabled. Could be useful in bigger setups where some AppServers can only read the index but not update it.

### Example file for productive environments [​](#example-file-for-productive-environments)

bash

```shiki
APP_ENV=prod
APP_SECRET=1
INSTANCE_ID=1
DATABASE_URL=mysql://mysqluser:mysqlpassword@localhost:3306/shopwaredatabasename
APP_URL=http://localhost
MAILER_URL=smtp://localhost:1025
COMPOSER_HOME=/var/www/html/var/cache/composer

OPENSEARCH_URL="elasticsearchhostname:9200"
SHOPWARE_ES_ENABLED="1"
SHOPWARE_ES_INDEXING_ENABLED="1"
SHOPWARE_ES_INDEX_PREFIX="sw"
SHOPWARE_ES_THROW_EXCEPTION=0
```

### Example file for debug configuration [​](#example-file-for-debug-configuration)

bash

```shiki
APP_ENV=dev
APP_SECRET=1
INSTANCE_ID=1
DATABASE_URL=mysql://mysqluser:mysqlpassword@localhost:3306/shopwaredatabasename
APP_URL=http://localhost
MAILER_URL=smtp://localhost:1025
COMPOSER_HOME=/var/www/html/var/cache/composer

OPENSEARCH_URL="elasticsearchhostname:9200"
SHOPWARE_ES_ENABLED="1"
SHOPWARE_ES_INDEXING_ENABLED="1"
SHOPWARE_ES_INDEX_PREFIX="sw"
SHOPWARE_ES_THROW_EXCEPTION=1
```

### Example for changing index configuration [​](#example-for-changing-index-configuration)

Shopware will use by default three shards and three replicas for the created index. This configuration can be overwritten with a new config file in `config/packages/elasticsearch.yml`

INFO

This configuration is available since Shopware version 6.4.12.0

yaml

```shiki
elasticsearch:
  index_settings:
    number_of_shards: 1
    number_of_replicas: 0
```

## Indexing [​](#indexing)

Before indexing, you might want to clear your cache with `bin/console cache:clear` so the changes from your *.env* can be processed.

### Basic Elasticsearch indexing [​](#basic-elasticsearch-indexing)

Normally, you can index by executing the command `bin/console es:index`.

INFO

For additional support with common Elasticsearch errors and more tips please refer to [elasticsearch troubleshooting](https://developer.shopware.com/docs/resources/guidelines/troubleshooting/elasticsearch.html).

### Indexing the whole shop [​](#indexing-the-whole-shop)

Sometimes you want to reindex your whole shop, including Elasticsearch, SEO-URLs, product index, and more. For a reindex of the whole shop, you can use the command `bin/console dal:refresh:index --use-queue`. Use the `--use-queue` option because you will have too many products to index without the [message queue](./../message-queue.html) involved.

### Alias creation [​](#alias-creation)

Some systems require you to manually execute `bin/console es:create:alias` after the indexing is processed completely. Try that command if your index was created fully without errors, and you still don't see products in your Storefront.

### What happens when indexing [​](#what-happens-when-indexing)

When you are indexing, the data is written in bulks to the message queue and the respective table enqueue. If a messenger process is active, the entries of that table are processed one by one. In case a message runs into an error, it is written into the `dead_messages` table and will be processed again after a specific time frame.

You can start multiple messenger consumer processes by using the command `bin/console messenger:consume` and also add output to the processed messages by adding the parameter `bin/console messenger:consume -vv`. In a production environment, you want to deactivate the admin messenger which is started automatically when opening a session in your Administration view by following this [documentation](./../../../../guides/hosting/infrastructure/message-queue.html#admin-worker).

Our experience has shown that up to three worker processes are normal and useful for a production environment. If you want more than that, a tool like [RabbitMQ](./../message-queue.html#message-queue-on-production-systems) to handle the queue is needed so your database will not become a bottleneck.

## Configuration [​](#configuration)

Keep in mind that the search configuration of Shopware has no effect when using Elasticsearch. To configure which fields and elements are searchable when using Elasticsearch, you must install the extension [Advanced Search](https://docs.shopware.com/en/shopware-6-en/extensions/advanced-search).

## Elasticsearch for Admin [​](#elasticsearch-for-admin)

Shopware 6.4.19.0 and above supports "AND/OR Search" functionality in Administration for more flexible search queries using either "AND" or "OR" operators.

Add the below config variables to set up Elasticsearch for Administration:

bash

```shiki
ADMIN_OPENSEARCH_URL=YOUR OPEN SEARCH URL
SHOPWARE_ADMIN_ES_ENABLED=1
SHOPWARE_ADMIN_ES_REFRESH_INDICES=1
SHOPWARE_ADMIN_ES_INDEX_PREFIX=sw-admin
```

Also, the CLI commands can be used as below:

bash

```shiki
bin/console es:admin:index
bin/console es:admin:reset
bin/console es:admin:test
```

INFO

Advanced admin users can refer to [elasticsearch reference guide](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-simple-query-string-query) for complex search queries.

---

## Debugging Elasticsearch

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/elasticsearch/elasticsearch-debugging.html

# Debugging Elasticsearch [​](#debugging-elasticsearch)

## Overview [​](#overview)

This article shows you how to debug the status and indexing process of your Elasticsearch environment. Ensure that the [Debug-Mode](./elasticsearch-debugging.html) is activated in your *.env* file.

## Shopware 6 CLI commands [​](#shopware-6-cli-commands)

### Cache clear [​](#cache-clear)

`cache:clear` clears the cache

bash

```shiki
bin/console cache:clear
```

**> Output:**

bash

```shiki
// Clearing the cache for the dev environment with debug
// true
​[OK] Cache for the "dev" environment (debug=true) was successfully cleared.
```

### ES index [​](#es-index)

`es:index` creates only the index for ES

bash

```shiki
bin/console es:index // Creates only the index for ES
```

**> No Output**

### ES create alias [​](#es-create-alias)

`es:create:alias` will create an alias linking to the index after `es:index` is done. Normally this is done automatically. In the older version, this has to be done.

bash

```shiki
bin/console es:create:alias
```

**> No Output**

### DAL refresh index [​](#dal-refresh-index)

`dal:refresh:index --use-queue` creates a complete reindex from the Shopware DAL (ES/SEO/Media/Sitemap...) **ALWAYS** "`--use-queue`" since big request can outperform the server!

bash

```shiki
bin/console dal:refresh:index --use-queue
```

**> Output:**

bash

```shiki
[landing_page.indexer]
1/1 [============================] 100% < 1 sec/< 1 sec 38.5 MiB
​
[product.indexer]
22/22 [============================] 100% < 1 sec/< 1 sec 40.5 MiB
​
[customer.indexer]
2/2 [============================] 100% < 1 sec/< 1 sec 40.5 MiB
​
[sales_channel.indexer]
2/2 [============================] 100% < 1 sec/< 1 sec 40.5 MiB
​
[category.indexer]
9/9 [============================] 100% < 1 sec/< 1 sec 40.5 MiB
​
[...]
```

### Messenger consume [​](#messenger-consume)

`messenger:consume -vv` starts a message consumer working on all tasks. This could be started *X* times. When using more than 3 message consumers, you will need something like RabbitMq to handle the data.

bash

```shiki
bin/console messenger:consume -vv
```

**> Output:**

bash

```shiki
[OK] Consuming messages from transports "default".
​​
// The worker will automatically exit once it has received a stop signal via the messenger:stop-workers command.
​
// Quit the worker with CONTROL-C.
​
09:47:28 INFO      [messenger] Received message Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage ["message" => Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage^ { …},"class" => "Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage"]
​
[...]
```

### Index cleanup [​](#index-cleanup)

`es:index:cleanup` to remove unused indices, because each indexing will generate a new Elasticsearch index.

bash

```shiki
bin/console es:index:cleanup
```

## Helpful Elasticsearch REST APIs [​](#helpful-elasticsearch-rest-apis)

bash

```shiki
curl -XGET 'http://elasticsearch:9200/?pretty'
```

**> Output:**

bash

```shiki
{
  "name" : "TZzynG6",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "tHklOFWPSwm-j8Yn-8PRoQ",
  "version" : {
    "number" : "6.8.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "1fad4e1",
    "build_date" : "2019-06-18T13:16:52.517138Z",
    "build_snapshot" : false,
    "lucene_version" : "7.7.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

### API for cluster health [​](#api-for-cluster-health)

Returns the health status of a cluster:

bash

```shiki
curl -XGET 'http://elasticsearch:9200/_cluster/health?pretty'
```

**> Output:**

bash

```shiki
{
  "cluster_name" : "docker-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1210,
  "active_shards" : 1210,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1210,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```

### API for cat indices [​](#api-for-cat-indices)

Returns high-level information about indices in a cluster, including backing indices for data streams:​

bash

```shiki
curl -XGET 'http://elasticsearch:9200/_cat/indices/?pretty'
```

**> Output:**

bash

```shiki
yellow open sw1_manufacturer_20210906113224 AYKMT4NJS7eZgU29ww7z6Q 5 1  3 0  33.2kb  33.2kb
yellow open sw1_emotion_20210903165112      he19OP_UR3mMIAKI7ry2mg 5 1  1 0  11.6kb  11.6kb
yellow open sw1_emotion_20210903171353      jBzApKujRPu73CkKA79F7w 5 1  1 0  11.6kb  11.6kb
yellow open sw1_synonym_20210903175037      EexqHsXyTK202XsalUednQ 5 1  1 0     6kb     6kb
yellow open sw1_synonym_20210903170128      NRjlZZ3AQ0Wat1ILB_9L8Q 5 1  0 0   1.2kb   1.2kb
​
[...]
```

### API to delete the index [​](#api-to-delete-the-index)

With `_all` it will delete all indices.

bash

```shiki
curl -X DELETE 'elasticsearch:9200/_all'
```

**> Output:**

bash

```shiki
{"acknowledged":true}
```

## Show the indexing status in the database [​](#show-the-indexing-status-in-the-database)

Returns the status of your indexing:

sql

```shiki
select * from message_queue_stats mqs ;
select count(*) from enqueue e ;
select count(*) from dead_message dm ;
```

The number of entries in the enqueue should match the sum of the size values in the `message_queue_stats`. As long as there are entries in your `enqueue`, the indexing is in process and your message consumer has to work those messages.

## Reset the indexing in the database [​](#reset-the-indexing-in-the-database)

Sometimes you want to reset the indexing in your database because your indexing is stuck or you run into an error. If the database queue is used, third-party services will differ. You can do so with the following queries.

sql

```shiki
truncate enqueue ;
truncate dead_message ;
truncate message_queue_stats ;
update scheduled_task set status = 'scheduled' where status = 'queued';
```

## Completely reset your Elasticsearch and reindex [​](#completely-reset-your-elasticsearch-and-reindex)

This is mainly for debugging purposes and is only meant for testing and staging environments. First, execute the database reset (only working for the database queue):

sql

```shiki
truncate enqueue ;
truncate dead_message ;
truncate message_queue_stats ;
update scheduled_task set status = 'scheduled' where status = 'queued';
```

Now delete the old Elasticsearch index, clear your cache, reindex and ensure that the indexing process is finished:

bash

```shiki
curl -X DELETE 'elasticsearch:9200/_all'
bin/console cache:clear
bin/console es:index
bin/console messenger:consume -vv
```

After the last message has been processed, your index should be found in your Storefront else execute:

bash

```shiki
bin/console es:create:alias
```

## Logfiles and tipps [​](#logfiles-and-tipps)

You can usually find the Elasticsearch logfiles at [`/var/log/elasticsearch`](https://www.elastic.co/guide/en/elasticsearch/reference/master/settings.html#_config_file_format) to check for any issues when indexing. Also, tools like [Kibana](https://www.elastic.co/kibana) or [Cerebro](https://help.profihost.com/hc/de/articles/18918050563729-Cerebro) can help you better understand what is happening in your Elasticsearch.

---

## Redis

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/redis.html

# Redis [​](#redis)

[Redis](https://redis.io/docs/latest/get-started/) is an in-memory data storage, that offers high performance and can be used as a cache, message broker, and database. It is a key-value store that supports various data structures like strings, hashes, lists, sets, and sorted sets. Especially in high-performance and high-throughput scenarios it can give better results, than relying on a traditional relational database. Therefore, multiple adapter exists in shopware, to offload some tasks from the DB to Redis.

However, as the data that is stored in Redis differs and also the access patterns to this data differ, it makes sense to use different Redis instances with different configurations for different tasks.

The data stored in Redis can be roughly classified into those three categories:

1. Ephemeral data: This data is not critical and can be easily recreated when lost, e.g., caches.
2. Durable, but "aging" data: This data is important and cannot easily be recreated, but the relevance of the data decreases over time, e.g. sessions.
3. Durable and critical data: This data is important and cannot easily be recreated, e.g. carts, number ranges.

Please note that in current Redis versions, it is not possible to use different eviction policies for different databases in the same Redis instance. Therefore, it is recommended to use separate Redis instances for different types of data.

## Ephemeral data [​](#ephemeral-data)

As ephemeral data can easily be restored and is most often used in cases where high performance matters, this data can be stored with no durable persistence. This means the data is only stored in memory and is lost when the Redis instance is restarted.

For key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as the application explicitly manages the TTL for each cache item.

The caching data (HTTP-Cache & Object cache) is what should be stored in this instance.

[Cache](../performance/caches)

## Durable, but "aging" data [​](#durable-but-aging-data)

As the data stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

`allkeys-lru` should be used as key eviction policy here, as by default more recent data is more important than older data, therefore the oldest values should be discarded, when Redis reach the max memory.

The session data is what should be stored in this instance.

[Session](../performance/session)

## Durable and critical data [​](#durable-and-critical-data)

Again this is durable data, that can not easily be recreated, therefore it should be persisted as well.

As the data is critical, it is important to use a key eviction policy that will not delete data that is not expired, therefore `volatile-lru` should be used.

The cart, number range, lock store and increment data is what should be stored in this instance.

## Configuration [​](#configuration)

Starting with v6.6.8.0 Shopware supports configuring different reusable Redis connections in the`config/packages/shopware.yaml` file under the `shopware` section:

yaml

```shiki
shopware:
    # ...
    redis:
        connections:
            ephemeral:
                dsn: 'redis://host1:port/dbindex'
            persistent:
                dsn: 'redis://host2:port/dbindex'
```

Connection names should reflect the actual connection purpose/type and be unique. Also, the names are used as part of the service names in the container, so they should follow the service naming conventions. After defining connections, you can reference them by name in the configuration of different subsystems.

It's possible to use environment variables in the DSN string, e.g. if `REDIS_EPHEMERAL` is set to `redis://host1:port`, the configuration could look like this:

yaml

```shiki
shopware:
    # ...
    redis:
        connections:
            ephemeral_1:
                dsn: '%env(REDIS_EPHEMERAL)%/1' # using database 1
            ephemeral_2:
                dsn: '%env(REDIS_EPHEMERAL)%/2' # using database 2
```

### Connection pooling [​](#connection-pooling)

In high-load scenarios, it is recommended to use persistent connections to avoid the overhead of establishing a new connection for each request. This can be achieved by setting the `persistent` flag in DSN to `1`:

yaml

```shiki
shopware:
    redis:
        connections:
            ephemeral:
                dsn: 'redis://host:port/dbindex?persistent=1'
```

Please note that the persistent flag influences connection pooling, not persistent storage of data.

[Cart Storage](../performance/cart-storage)[Number Ranges](../performance/number-ranges)[Lock Storage](../performance/lock-store)[Increment Storage](../performance/increment)[Performance Tweaks](../performance/performance-tweaks#delayed-invalidation)

---

## Filesystem

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/filesystem.html

# Filesystem [​](#filesystem)

## Overview [​](#overview)

Shopware 6 stores and processes a wide variety of files. This goes from product images or videos to generated documents such as invoices or delivery notes. This data should be stored securely, and backups should be generated regularly. Therefore, it is advisable to set up storage service, which scales with the size of the data, performs backups, and ensures data redundancy. In addition, for cluster setups with multiple setups, it is **necessary** to share the files via external storage so that each app server can access the corresponding data.

## Flysystem overview [​](#flysystem-overview)

Shopware 6 can be used with several cloud storage providers. It uses [Flysystem](https://flysystem.thephpleague.com/docs/) to provide a common interface between different providers as well as the local file system. This enables your shops to read and write files through a common interface.

The file system can be divided into multiple adapters. Each adapter can handle one or more of the following directories: media, sitemaps, and more. Of course, you can also use the same configuration for:

* private files: invoices, delivery notes, plugin files, etc.
* public files: product pictures, media files, plugin files in general
* theme files
* sitemap files
* bundle assets files

## Configuration [​](#configuration)

The configuration for file storage of Shopware 6 resides in the general bundle configuration:

text

```shiki
<project root>
└── config
   └── packages
      └── shopware.yml
```

To set up a non-default filesystem for your shop, you need to add the `filesystem:` map to the `shopware.yml`. Under this key, you can separately define your storage for the public, private, theme, sitemap, and asset (bundle assets).

INFO

You can also change the URL of the file systems. This is useful if you want to use a different domain for your files. For example, you can use a CDN for your public files.

yaml

```shiki
shopware:
  filesystem:
    public:
      url: "{url-to-your-public-files}"
      # The Adapter Configuration
    private:
      visibility: "private"
      # The Adapter Configuration
    theme:
      url: "{url-to-your-theme-files}"
      # The Adapter Configuration
    asset:
      url: "{url-to-your-asset-files}"
      # The Adapter Configuration
    sitemap:
      url: "{url-to-your-sitemap-files}"
      # The Adapter Configuration
```

### Using YAML anchors to avoid repetition [​](#using-yaml-anchors-to-avoid-repetition)

You can use YAML anchors to avoid repeating the same configuration for multiple filesystems. This is particularly useful when you want to use the same storage backend for public, theme, and sitemap files:

yaml

```shiki
shopware:
  filesystem:
    public: &s3_config
      type: "amazon-s3"
      url: "{{S3_URL}}"
      config:
        bucket: "{{AWS_BUCKET}}"
        region: "{{AWS_REGION}}"
        endpoint: "{{AWS_ENDPOINT}}"
        use_path_style_endpoint: true
        credentials:
          key: "{{AWS_ACCESS_KEY_ID}}"
          secret: "{{AWS_SECRET_ACCESS_KEY}}"
    theme: *s3_config
    sitemap: *s3_config
```

In this example, the `&s3_config` creates an anchor that can be referenced with `*s3_config` in other filesystem configurations, avoiding duplication.

### Fallback adapter configuration [​](#fallback-adapter-configuration)

By default, the configuration for the theme, asset and sitemap filesystem will use the configuration from the `public` filesystem if they are not specifically configured. This means when you want to change the configuration used for the public filesystem, but the others should use the old configuration you have to set them explicitly.

E.g. before you had the following configuration:

yaml

```shiki
shopware:
  filesystem:
    public:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
```

Now you want to change the public filesystem to use an S3 adapter, but the theme, asset and sitemap filesystem should still use the local adapter. You have to set them explicitly:

yaml

```shiki
shopware:
  filesystem:
    public:
      url: "{{S3_URL}}"
      type: "amazon-s3"
      config:
        bucket: "{{AWS_BUCKET}}"
        region: "{{AWS_REGION}}"
        endpoint: "{{AWS_ENDPOINT}}"
        credentials:
          key: "{{AWS_ACCESS_KEY_ID}}"
          secret: "{{AWS_SECRET_ACCESS_KEY}}"
    theme:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
    asset:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
    sitemap:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
```

### Additional configuration [​](#additional-configuration)

If you want to regulate the uploaded file types, then you could add the keys `allowed_extensions`for the public filesystem or `private_local_download_strategy` for the private filesystem. With the `private_local_download_strategy` key you could choose the download strategy for private files (e.g., the downloadable products):

yaml

```shiki
shopware:
  filesystem:
    public:
      # The Adapter Configuration
    private:
      # The Adapter Configuration
    allowed_extensions: # Array with allowed file extensions for public filesystem
    private_allowed_extensions: # Array with allowed file extensions for private filesystem
    private_local_download_strategy: # Name of the download strategy: php, x-sendfile or x-accel
```

The following download strategies are valid:

* `php` (default): A streamed response of content type `application/octet-stream` with binary data
* `x-sendfile` (Apache only): X-Sendfile allows you to use PHP to instruct the server to send a file to a user, without having to load that file into PHP. You must have the [`mod_xsendfile`](https://github.com/nmaier/mod_xsendfile) Apache module installed.
* `x-accel` (Nginx only): X-accel allows for internal redirection to a location determined by a header returned from a backend. See the [example configuration](https://docs.nginx.com/).

## CDN configuration [​](#cdn-configuration)

If your public files are available on a CDN, you can use the following config to serve images and other assets via that CDN.

yaml

```shiki
# <project root>/config/packages/prod/shopware.yml
shopware:
  filesystem:
    public:
      url: "YOUR_CDN_URL"
      type: "local"
      config:
        root: "%kernel.project_dir%/public"
```

INFO

Be aware of the **prod** in the config path. CDNs are typically for production environments, but you can also set them for all environments in `config/packages/shopware.yml`.

## Supported adapter configurations [​](#supported-adapter-configurations)

### Local [​](#local)

yaml

```shiki
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "local"
        config:
          root: "%kernel.project_dir%/public"
```

### Amazon S3 [​](#amazon-s3)

In order to use the S3 adapter you need to install the `league/flysystem-async-aws-s3` package.

bash

```shiki
composer require league/flysystem-async-aws-s3
```

Example configuration:

yaml

```shiki
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "amazon-s3"
        url: "https://your-cloudfront-url"
        visibility: "private" # Default is "public", can be set only on shopware.filesystem.private
        config:
            bucket: "{your-public-bucket-name}"
            region: "{your-bucket-region}"
            endpoint: "{your-s3-provider-endpoint}"
            root: "{your-root-folder}"
            # Optional, otherwise will be automatically discovered with AWS content discovery
            credentials:
              key: '{your-access-key}'
              secret: '{your-secret-key}'
```

If your S3 provider does not use buckets as subdomain like Minio in default configuration, you need to set `use_path_style_endpoint` to `true` inside `config`.

### Google Cloud Platform [​](#google-cloud-platform)

In order to use the Google Cloud Platform adapter you need to install the `league/flysystem-google-cloud-storage` package.

bash

```shiki
composer require league/flysystem-google-cloud-storage
```

Example configuration:

yaml

```shiki
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "google-storage"
        url: "https://storage.googleapis.com/{your-public-bucket-name}"
        visibility: "private" # Default is "public", can be set only on shopware.filesystem.private
        config:
            bucket: "{your-public-bucket-name}"
            projectId: "{your-project-id}"
            keyFilePath: "{path-to-your-keyfile}"
```

The bucket needs to use the "Fine-grained" [ACL mode](https://cloud.google.com/storage/docs/access-control#choose_between_uniform_and_fine-grained_access). This is required so that Shopware can manage the ACL of the objects.

## Add your own adapter [​](#add-your-own-adapter)

To create your own adapter, check out the [official Flysystem guide](https://flysystem.thephpleague.com/v1/docs/advanced/creating-an-adapter/).

To make your adapter available in Shopware, you will need to create an AdapterFactory for your Flysystem provided adapter. An example of that could look like this:

php

```shiki
<?php

use Shopware\Core\Framework\Adapter\Filesystem\Adapter\AdapterFactoryInterface;
use League\Flysystem\AdapterInterface;

class MyFlysystemAdapterFactory implements AdapterFactoryInterface
{
    public function getType(): string
    {
        return 'my-adapter-prefix'; // This must match with the type in the yaml file
    }

    public function create(array $config): AdapterInterface
    {
        // $config contains the given config from the yaml
        return new MyFlysystemAdapter($config);
    }
}
```

This new class needs to be registered in the DI with the tag `shopware.filesystem.factory` to be usable.

---

## Rate Limiter

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/rate-limiter.html

# Rate Limiter [​](#rate-limiter)

INFO

This functionality is available starting with Shopware 6.4.6.0.

## Overview [​](#overview)

Shopware 6 provides certain rate limits by default that reduces the risk of brute-force attacks for pages like login or password reset.

## Configuration [​](#configuration)

The configuration for the rate limiter of Shopware 6 resides in the general bundle configuration:

text

```shiki
<shop root>
└── config
   └── packages
      └── shopware.yml
```

To configure the default rate limiters for your shop, you need to add the `shopware.api.rate_limiter` map to the `shopware.yml`. Under this key, you can separately define the rate limiters.

In the following, you can find a list of the default limiters:

* `login`: Storefront / Store-API customer authentication.
* `guest_login`: Storefront / Store-API after order guest authentication.
* `oauth`: API oauth authentication / Administration login.
* `reset_password`: Storefront / Store-API customer password reset.
* `user_recovery`: Administration user password recovery.
* `contact_form`: Storefront / Store-API contact form.

yaml

```shiki
// <shop root>/config/packages/shopware.yaml
shopware:
  api:
    rate_limiter:
      login:
        enabled: false
      oauth:
        enabled: true
        policy: 'time_backoff'
        reset: '24 hours'
        limits:
          - limit: 3
            interval: '10 seconds'
          - limit: 5
            interval: '60 seconds'
```

### Configuring time backoff policy [​](#configuring-time-backoff-policy)

The `time_backoff` policy is built by Shopware itself. It enables you to throttle the request in multiple steps with different waiting times. Below you can find an example which throttles the request for 10 seconds after 3 requests and starting from 5 requests it always throttles for 60 seconds. If there are no more requests, it will be reset after 24 hours.

yaml

```shiki
// <plugin root>/src/Resources/config/rate_limiter.yaml
example_route:
    enabled: true
    policy: 'time_backoff'
    reset: '24 hours'
    limits:
        - limit: 3
          interval: '10 seconds'
        - limit: 5
          interval: '60 seconds'
```

---

## Database Cluster

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/database-cluster.html

# Database Cluster [​](#database-cluster)

INFO

This functionality is available starting with Shopware 6.4.12.0.

To scale Shopware even further, we recommend using a database cluster. A database cluster consists of multiple read-only servers managed by a single primary instance.

Shopware already splits read and write SQL queries by default. When a write [`INSERT`/`UPDATE`/`DELETE`/...](https://github.com/shopware/shopware/blob/v6.4.11.1/src/Core/Profiling/Doctrine/DebugStack.php#L48) query is executed, the query is delegated to the primary server, and the current connection uses only the primary node for subsequent calls. This is ensured by the `executeStatement` method in the [DebugStack decoration](https://github.com/shopware/shopware/blob/v6.4.11.1/src/Core/Profiling/Doctrine/DebugStack.php#L48). That way, Shopware can ensure read-write consistency for records within the same request. However, it doesn't take into account that read-only child nodes might not be in sync with the primary node. This is left to the database replication process.

## Preparing Shopware [​](#preparing-shopware)

We suggest following the steps below to make the splitting the most effective.

### Using the optimal MySQL configuration [​](#using-the-optimal-mysql-configuration)

By default, Shopware does not set specific MySQL configurations that make sure the database is optimized for Shopware usage. These variables are set in cluster mode only on the read-only server. To make sure that Shopware works flawlessly, these configurations must be configured directly on the MySQL server so these variables are set on any server.

The following options should be set:

* Make sure that `group_concat_max_len` is by default higher or equal to `320000`
* Make sure that `sql_mode` doesn't contain `ONLY_FULL_GROUP_BY`

After this change, you can set also `SQL_SET_DEFAULT_SESSION_VARIABLES=0` in the `.env` file so Shopware does not check for those variables at runtime.

### Cart in Redis [​](#cart-in-redis)

As we learned in the beginning, Shopware queries a read-only MySQL server until the first write attempt. To maximize this behavior, it is highly recommended to outsource as many write operations as possible from the database. One of the easiest solutions is to use the Redis as storage for store carts. To use Redis, add the following snippet to `config/packages/cart.yml`

yaml

```shiki
shopware:
    cart:
        redis_url: 'redis://localhost:6379/0?persistent=1'
```

It is recommended to use a persistent Redis connection to avoid connection issues in high-load scenarios. There is also a `cart:migrate` command to migrate the existing carts between MySQL and Redis, so the migration does not influence end-user experience.

For a detailed explanation refer to the cart storage docs:

[Cart Storage](../performance/cart-storage)

## Configure the database cluster [​](#configure-the-database-cluster)

INFO

We recommend the usage of [ProxySQL](https://proxysql.com/) as a proxy for the database cluster instead of configuring the application to connect to different database servers directly. ProxySQL allows you to manage the database cluster more efficiently and provides additional features like query caching, load balancing, and failover.

To use the MySQL cluster, you have to configure the following in the `.env` file:

* `DATABASE_URL` is the connection string for the MySQL primary.
* `DATABASE_REPLICA_x_URL` (e.g `DATABASE_REPLICA_0_URL`, `DATABASE_REPLICA_1_URL`) - is the connection string for the MySQL read-only server.

---

## Message Queue

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/message-queue.html

# Message Queue [​](#message-queue)

## Overview [​](#overview)

Shopware uses the Symfony Messenger component and Enqueue to handle asynchronous messages. This allows tasks to be processed in the background. Thus, tasks can be processed independently of timeouts or system crashes. By default, tasks in Shopware are stored in the database and processed via the browser as long as you are logged into the Administration. This is a simple and fast method for the development process, but not recommended for production systems. With multiple users logged into the Administration, this can lead to a high CPU load and interfere with the smooth execution of PHP FPM.

## Message queue on production systems [​](#message-queue-on-production-systems)

On a production system, the message queue should be processed via the CLI instead of the browser in the Administration ([Admin worker](#admin-worker)). This way, tasks are also completed when no one is logged into the Administration and high CPU load due to multiple users in the admin is also avoided. Furthermore, you can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/). This would, relieve the database and, on the other hand, use a much more specialized service for handling message queues. The following are examples of the steps needed.  
 It is recommended to run one or more `messenger:consume` workers. To automatically start the processes again after they stopped because of exceeding the given limits you can use a process control system like [systemd](https://www.freedesktop.org/wiki/Software/systemd/) or [supervisor](http://supervisord.org/running.html). Alternatively, you can configure a cron job that runs the command periodically.

INFO

Using cron jobs won't take care of maximum running worker, like supervisor can do. They don't wait for another worker to stop. So there is a risk of starting an unwanted amount of workers when you have messages running longer than the set time limit. If the time limit has been exceeded worker will wait for the current message to be finished.

Find here the docs of Symfony: <https://symfony.com/doc/current/messenger.html#deploying-to-production>

INFO

It is recommended to use a third-party message queue to support multiple consumers and/or a greater amount of data to index.

## Execution methods [​](#execution-methods)

### CLI worker [​](#cli-worker)

INFO

The CLI worker is the recommended way to consume messages.

You can configure the command just to run a certain amount of time and to stop if it exceeds a certain memory limit like:

bash

```shiki
bin/console messenger:consume async --time-limit=60 --memory-limit=128M
```

You can also configure the command to consume messages from multiple transports to prioritize them to your needs, as it is recommended by the [Symfony documentation](https://symfony.com/doc/current/messenger.html#prioritized-transports):

bash

```shiki
bin/console messenger:consume async low_priority
```

For more information about the command and its configuration, use the -h option:

bash

```shiki
bin/console messenger:consume -h
```

If you have configured the cli-worker, you should turn off the admin worker in the Shopware configuration file. Therefore, create or edit the configuration `shopware.yaml`.

yaml

```shiki
# config/packages/shopware.yaml
shopware:
    admin_worker:
        enable_admin_worker: false
```

WARNING

Make sure to set up the CLI worker also for the failed queue. Otherwise, failed messages will not be processed.

#### systemd example [​](#systemd-example)

We assume the services to be called `shopware_consumer`.

Create a new file `/etc/systemd/system/shopware_consumer@.service`

bash

```shiki
[Unit]
Description=Shopware Message Queue Consumer, instance %i
PartOf=shopware_consumer.target

[Service]
Type=simple
User=www-data # Change this to webserver's user name
Restart=always
# Change the path to your shop path
WorkingDirectory=/var/www/html
ExecStart=php /var/www/html/bin/console messenger:consume --time-limit=60 --memory-limit=512M async low_priority

[Install]
WantedBy=shopware_consumer.target
```

Create a new file `/etc/systemd/system/shopware_consumer.target`

bash

```shiki
[Install]
WantedBy=multi-user.target

[Unit]
Description=shopware_consumer service
```

Enable multiple instances. Example for three instances: `systemctl enable shopware_consumer@{1..3}.service`

Enable the dummy target: `systemctl enable shopware_consumer.target`

At the end start the services: `systemctl start shopware_consumer.target`

#### supervisord example [​](#supervisord-example)

Please refer to the [Symfony documentation](https://symfony.com/doc/current/messenger.html#supervisor-configuration) for the setup.

### Admin worker [​](#admin-worker)

The admin worker, if used, can be configured in the general `shopware.yml` configuration. If you want to use the admin worker, you have to specify each transport that was previously configured. The poll interval is the time in seconds that the admin worker polls messages from the queue. After the poll interval is over, the request terminates, and the Administration initiates a new request.

yaml

```shiki
# config/packages/shopware.yaml
shopware:
    admin_worker:
        enable_admin_worker: true
        poll_interval: 30
        transports: ["async", "low_priority"]
```

## Sending mails over the message queue [​](#sending-mails-over-the-message-queue)

By default, Shopware sends the mails synchronously. Since this can affect the page speed, you can switch it to use the Message Queue with a small configuration change.

yaml

```shiki
# config/packages/framework.yaml
framework:
    mailer:
        message_bus: 'messenger.default_bus'
```

## Failed messages [​](#failed-messages)

If a message fails, it will be moved to the failed transport. The failed transport is configured using the `MESSENGER_TRANSPORT_FAILURE_DSN` env. The default is the Doctrine transport. The messages are retried automatically 3 times. If the message fails again, it will be deleted. You can learn more about the failed transport and how you can configure it in the Symfony Messenger documentation: <https://symfony.com/doc/current/messenger.html#retries-failures>

## Changing the transport [​](#changing-the-transport)

By default, Shopware uses the Doctrine transport. This is simple transport that stores the messages in the database. This is a good choice for development, but not recommended for production systems. You can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/). This would, relieve the database and, on the other hand, use a much more specialized service for handling message queues. The following are examples of the steps needed.

You can find all available transport options in the Symfony Messenger documentation: <https://symfony.com/doc/current/messenger.html#transport-configuration>

Following environment variables are in use out of the box:

* `MESSENGER_TRANSPORT_DSN` - The DSN to the transport to use (e.g. `doctrine://default`).
* `MESSENGER_TRANSPORT_LOW_PRIORITY_DSN` - The DSN to the transport to use for low priority messages (e.g. `doctrine://default?queue_name=low_priority`).
* `MESSENGER_TRANSPORT_FAILURE_DSN` - The DSN to the transport to use for failed messages (e.g. `doctrine://default?queue_name=failed`).

## Worker count for efficient message processing [​](#worker-count-for-efficient-message-processing)

The number of workers depends on the number of messages queued and the type of messages they are. Product indexing messages are usually slow, while other messages are processed very fast. Therefore, it is difficult to give a general recommendation. You should be able to monitor the queue and adjust the number of workers accordingly. Sometimes, it also makes sense to route messages to a different transport to limit the number of workers for a specific type of message to avoid database locks or prioritize messages like sending emails.

## Configuration [​](#configuration)

### Message bus [​](#message-bus)

The message bus is used to dispatch your messages to your registered handlers. While dispatching your message, it loops through the configured middleware for that bus. The message bus used inside Shopware can be found under the service tag `messenger.bus.default`. It is mandatory to use this message bus if your messages should be handled inside Shopware. However, if you want to send messages to external systems, you can define your custom message bus for that.

You can configure an array of buses and define one default bus in your `framework.yaml`.

yaml

```shiki
// <platform root>/src/Core/Framework/Resources/config/packages/framework.yaml
framework:
    messenger:
        default_bus: my.messenger.bus
        buses:
            my.messenger.bus:
```

For more information on this check the [Symfony docs](https://symfony.com/doc/current/messenger.html).

### Transport [​](#transport)

A [transport](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages) is responsible for communicating with your 3rd party message broker. You can configure multiple transports and route messages to multiple or different transports. Supported are all transports that are either supported by [Symfony](https://symfony.com/doc/current/messenger.html#transport-configuration) itself. If you don't configure a transport, messages will be processed synchronously like in the Symfony event system.

You can configure an amqp transport directly in your `framework.yaml` and simply tell Symfony to use your transports.

In a simple setup you only need to set the transport to a valid DSN like:

yaml

```shiki
// <platform root>/src/Core/Framework/Resources/config/packages/queue.yaml
framework:
  messenger:
    transports:
      my_transport:
        dsn: "%env(MESSENGER_TRANSPORT_DSN)%"
```

For more information on this check the [symfony docs](https://symfony.com/doc/current/messenger.html#transport-configuration).

### Routing [​](#routing)

You can route messages to different transports. For that, just configure your routing in the `framework.yaml`.

yaml

```shiki
// <plugin root>/src/
framework:
    messenger:
      transports:
        async: "%env(MESSENGER_TRANSPORT_DSN)%"
        another_transport: "%env(MESSENGER_TRANSPORT_ANOTHER_DSN)%"
      routing: 
        'Swag\BasicExample\MessageQueue\Message\SmsNotification': another_transport
        'Swag\BasicExample\MessageQueue\Message\AnotherExampleNotification': [async, another_transport]
        '*': async
```

You can route messages by their classname and use the asterisk as a fallback for all other messages. If you specify a list of transports the messages will be routed to all of them. For more information on this check the [Symfony docs](https://symfony.com/doc/current/messenger.html#routing-messages-to-a-transport).

#### Routing overwrites [​](#routing-overwrites)

By default, all messages that implement the `AsyncMessageInterface` will be routed to the `async` transport. The default symfony config detailed above will only let you add additional routing to those messages, however if you need to overwrite the additional routing you can do so by adding the following to your `shopware.yaml`:

yaml

```shiki
shopware:
  messenger:
    routing_overwrite:
      'Shopware\Core\Framework\DataAbstractionLayer\Indexing\EntityIndexingMessage': entity_indexing
```

The `shopware.messenger.routing_overwrite` config option accepts the same format as the `framework.messenger.routing` option, but it will overwrite the routing for the given message class instead of adding to it. This is especially useful if there is a default routing already configured based on a message interface, but you need to change the routing for a specific message.

INFO

This configuration option was added in Shopware 6.6.4.0 and 6.5.12.0.

---

## Scheduled Task

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/scheduled-task.html

# Scheduled task [​](#scheduled-task)

## What are scheduled tasks? [​](#what-are-scheduled-tasks)

Scheduled tasks are a way to schedule messages to the queue on time. Shopware uses it to run cleanup tasks, update tasks, and other non-time critical tasks in the background.

## Default scheduled tasks [​](#default-scheduled-tasks)

These tasks are registered by default:

| Name | Run interval (seconds) |
| --- | --- |
| log\_entry.cleanup | 86400 |
| shopware.invalidate\_cache | 20 |
| app\_update | 86400 |
| app\_delete | 86400 |
| version.cleanup | 86400 |
| webhook\_event\_log.cleanup | 86400 |
| sales\_channel\_context.cleanup | 86400 |
| product\_keyword\_dictionary.cleanup | 604800 |
| product\_download.media.cleanup | 2628000 |
| delete\_newsletter\_recipient\_task | 86400 |
| product\_stream.mapping.update | 86400 |
| product\_export\_generate\_task | 60 |
| import\_export\_file.cleanup | 86400 |
| shopware.sitemap\_generate | 86400 |
| cart.cleanup | 86400 |
| shopware.elasticsearch.create.alias | 300 |

INFO

Some tasks like `shopware.elasticsearch.create.alias` and `shopware.invalidate_cache` are only running when necessary. Elasticsearch task only runs when an Elasticsearch server is configured and enabled.

## Creating a scheduled task [​](#creating-a-scheduled-task)

[Add scheduled task](../../plugins/plugins/plugin-fundamentals/add-scheduled-task)

INFO

The following commands or flags (--no-wait) are available starting with Shopware 6.5.5.0.

## List all scheduled tasks [​](#list-all-scheduled-tasks)

You can list all scheduled tasks with `bin/console scheduled-task:list` command.

## Scheduling a scheduled task [​](#scheduling-a-scheduled-task)

INFO

Available starting with Shopware 6.7.2.0.

You can schedule a scheduled task with the command `bin/console scheduled-task:schedule`.

## Deactivating a scheduled task [​](#deactivating-a-scheduled-task)

INFO

Available starting with Shopware 6.7.2.0.

You can deactivate a scheduled task with the command `bin/console scheduled-task:deactivate`.

## Running scheduled tasks [​](#running-scheduled-tasks)

To run the scheduled tasks, you must set up a background worker like the [Message Queue](./message-queue.html) and run the command `bin/console scheduled-task:run`. The command schedules all tasks to the queue and waits until a task needs to be scheduled. It consumes little CPU time or memory.

You can use the flag `--no-wait` and run the command from an operating system scheduler like cron. Check your scheduled task interval to determine the best interval to trigger the command. Example:

bash

```shiki
*/5 * * * * /usr/bin/php /var/www/html/bin/console scheduled-task:run --no-wait
```

## Using the symfony scheduler to run tasks [​](#using-the-symfony-scheduler-to-run-tasks)

INFO

Running tasks with the symfony scheduler is available starting with Shopware 6.6

WARNING

This feature is experimental.

You can run scheduled tasks as part of your queue workers with the help of the symfony scheduler component.

bash

```shiki
bin/console messenger:consume scheduler_shopware
```

On startup of this command reads the `scheduled_task` database table and applies the stored intervals, an entry in this table is optional. In the event that these intervals are modified in the database, it is necessary to restart the command for the updated intervals to take effect. To deactivate tasks, set status to `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskDefinition::STATUS_INACTIVE` in this table, and restart the `consume` command.

## Debugging scheduled tasks [​](#debugging-scheduled-tasks)

You can directly run a single scheduled task without the queue. This is useful for debugging purposes or to have better control of when and which tasks are executed. You can use `bin/console scheduled-task:run-single <task-name>` to run a single task. Example:

shell

```shiki
bin/console scheduled-task:run-single log_entry.cleanup
```

INFO

Available starting with Shopware 6.7.2.0.

You can schedule a scheduled task with the command `scheduled-task:schedule` or deactivate a scheduled task with the command `scheduled-task:deactivate`

shell

```shiki
bin/console scheduled-task:schedule log_entry.cleanup
bin/console scheduled-task:deactivate log_entry.cleanup
```

---

## Reverse HTTP Cache

**Source:** https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html

# Reverse HTTP Cache [​](#reverse-http-cache)

## Overview [​](#overview)

A reverse HTTP cache is a cache server placed before the web shop. If you are not familiar with HTTP caching, please refer to the [HTTP cache](./../../../concepts/framework/http_cache.html) concept. The reverse http cache needs the following capabilities to function fully with Shopware:

* Able to differentiate the request with multiple cookies
* Allow clearing the cache using a web request for a specific site or with `/` for all pages

INFO

In this guide, we will use Varnish as an example for HTTP cache.

### The example Setup with Varnish [​](#the-example-setup-with-varnish)

WARNING

This setup is compatible with Shopware version 6.4 and higher

![Http cache](/assets/hosting-infrastructure-reverseHttpCache.FAT4Lr2k.svg)

### Shopware Varnish Docker image [​](#shopware-varnish-docker-image)

Feel free to check out the [Shopware Varnish Docker image](https://github.com/shopware/varnish-shopware) for a quick start. It contains the Shopware default VCL (Varnish Configuration Language). The containing VCL is for the usage with `xkeys`.

### Configure Shopware [​](#configure-shopware)

WARNING

From version v6.6.x onwards, this method is deprecated and will be removed in v6.7.0. Utilising Varnish with Redis involves LUA scripts to determine URLs for the BAN request. This can cause problems depending on the setup or network. Furthermore, Redis clusters are not supported. Therefore, it is advisable to opt for the [Varnish with `XKey`](#configure-varnish) integration instead.

First, we need to activate the reverse proxy support in Shopware. To enable it, we need to create a new file in `config/packages/storefront.yaml`:

yaml

```shiki
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
    http_cache:
        reverse_proxy:
            enabled: true
            ban_method: "BAN"
            # This needs to point to your varnish hosts
            hosts: [ "http://varnish" ]
            # Max parallel invalidations at the same time for a single worker
            max_parallel_invalidations: 3
            use_varnish_xkey: true
```

Also set `SHOPWARE_HTTP_CACHE_ENABLED=1` in your `.env` file.

INFO

The configuration key changed from `storefront.reverse_proxy` up to Shopware 6.5.x to `shopware.http_cache.reverse_proxy` starting with Shopware 6.6.0.0. So you will need to adjust your config while upgrading. If you look for the old documentation and examples, you can find it [here](https://developer.shopware.com/docs/v6.5/guides/hosting/infrastructure/reverse-http-cache.html)

#### Trusted proxies [​](#trusted-proxies)

INFO

Since Shopware 6.6, the `TRUSTED_PROXIES` environment variable is no longer taken into account out of the box. Make sure to create a Symfony configuration to make it configurable again, as shown in the [trusted\_env.yaml example](https://github.com/shopware/recipes/blob/main/shopware/docker/0.1/config/packages/trusted_env.yaml).

For the most part, using Symfony and Varnish doesn't cause any problem. But, when a request passes through a proxy, certain request information is sent using either the *standard Forwarded* header or *X-Forwarded* headers. For example, instead of reading the `REMOTE_ADDR` header (which will now be the IP address of your reverse proxy), the user's true IP will be stored in a standard Forwarded: for="..." header or an *X-Forwarded-For* header.

If you don't configure Symfony to look for these headers, you will get incorrect information about the client's IP address. Whether or not the client connects via HTTPS, the client's port and the hostname are requested.

Go through [Proxies](https://symfony.com/doc/current/deployment/proxies.html) section for more information.

### Varnish Docker Image [​](#varnish-docker-image)

Shopware offers a Varnish Docker image that is pre-configured to work with Shopware. Find the [image](https://github.com/shopware/varnish-shopware) here. The image is based on the official Varnish image and contains the Shopware default VCL with few configurations as environment variables.

### Configure Varnish [​](#configure-varnish)

Varnish `XKey` is a cache key module that allows you to use Varnish with surrogate keys. It is a module not included in the default Varnish installation. It is available for Varnish 6.0 or higher.

Checkout the official Varnish installation guide [here](https://github.com/varnish/varnish-modules#installation).

And also needs to be enabled in the `config/packages/shopware.yml` file:

yaml

```shiki
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
  http_cache:
      reverse_proxy:
        enabled: true
        use_varnish_xkey: true
        hosts:
          - 'varnish-host'
```

[Varnish Configuration](https://github.com/shopware/varnish-shopware/blob/main/rootfs/etc/varnish/default.vcl)

Make sure to replace the `__XXX__` placeholders with your actual values.

### Soft Purge vs Hard Purge [​](#soft-purge-vs-hard-purge)

The default configuration Varnish uses hard purges, so when you update a product, the page will be removed from the cache and the next request takes longer because the cache is empty. To avoid this, you can use soft purges. Soft purge keeps the old page in case and serves it still to the clients and refreshes the cache in the background. This way the client gets **always** a cached page and the cache is updated in the background.

To enable soft purge, you need to change the varnish configuration.

diff

```shiki
-set req.http.n-gone = xkey.purge(req.http.xkey);
+set req.http.n-gone = xkey.softpurge(req.http.xkey);
```

### Debugging [​](#debugging)

The default configuration removes all headers except the `Age` header, which is used to determine the cache age. If you see only `0` as the `Age` header, it means that the cache is not working.

This problem is mostly caused as the application didn't set `Cache-Control: public` header. To check this you can use `curl` against the upstream server:

bash

```shiki
curl -vvv -H 'Host: <sales-channel-domain>' <app-server-ip> 1> /dev/null
```

and you should get a response like:

text

```shiki
< HTTP/1.1 200 OK
< Cache-Control: public, s-maxage=7200
< Content-Type: text/html; charset=UTF-8
< Xkey: theme.sw-logo-desktop, ...
```

If you don't see the `Cache-Control: public` header or the `Xkey` header, you need to check the application configuration that you really have enabled the reverse proxy mode.

For more details, please refer to the [Varnish documentation](https://www.varnish-software.com/developers/tutorials/logging-cache-hits-misses-varnish/) on logging cache hits and misses.

## Configure Fastly [​](#configure-fastly)

Fastly is supported since Shopware 6.4.11.0 is out-of-the-box with some configurations. To enable it, we need to create a new file in `config/packages/storefront.yaml`

yaml

```shiki
# Be aware that the configuration key changed from `storefront.reverse_proxy` to `shopware.http_cache.reverse_proxy` starting with Shopware 6.6
shopware:
  http_cache:
    reverse_proxy:
        enabled: true
        fastly:
          enabled: true
          api_key: '<personal-token-from-fastly>'
          service_id: '<service-id>'
```

### Fastly soft-purge [​](#fastly-soft-purge)

WARNING

This feature has been introduced with Shopware version 6.4.15.0

By default, the cache will be immediately purged and the next requesting user will get a slow response as the cache has been deleted. On soft purge, the user still gets the cached response after the purge, but in the configured time interval, the cache will be refreshed. This makes sure that the client gets the fastest response possible.

yaml

```shiki
# Be aware that the configuration key changed from `storefront.reverse_proxy` to `shopware.http_cache.reverse_proxy` starting with Shopware 6.6
shopware:
  http_cache:
    # Allow to serve the out-dated cache for 300 seconds
    stale_while_revalidate: 300
    # Allow to serve the out-dated cache for an hour if the origin server is offline
    stale_if_error: 3600
    reverse_proxy:
        enabled: true
        fastly:
          enabled: true
          api_key: '<personal-token-from-fastly>'
          service_id: '<service-id>'
          soft_purge: '1'
```

### Fastly VCL Snippets [​](#fastly-vcl-snippets)

You can use the [Deployment Helper to automatically deploy Fastly VCL Snippets and keep them up to date](./../installation-updates//deployments/deployment-helper.html).

For manual deployment, you can find the VCL Snippets here:

[Fastly VCL snippets](https://github.com/shopware/recipes/tree/main/shopware/fastly-meta/6.7/config/fastly)

### Cache Invalidations [​](#cache-invalidations)

The Reverse Proxy Cache shares the same invalidation mechanism as the Object Cache and has the same tags. So, when a product is invalidated, the object cache and the HTTP cache will also be invalidated.

There are a few different cache clearing commands:

1. `bin/console cache:clear` - Clears and warms up the application cache (In versions before 6.7 this command also cleared the HTTP cache)
2. `bin/console cache:clear:all` - Clears everything, including application cache, cache pools and the HTTP cache (Since version 6.6.8)
3. `bin/console cache:clear:http` - Clears the reverse proxy cache if enabled, if not it clears the `http` cache pool (Since version 6.6.10)
4. `bin/console cache:pool:clear --all` - Clears only the object cache (Useful for when you don't want to clear the http cache, pre version 6.6.10)

If you only want to clear the http cache, use `bin/console cache:clear:http`

WARNING

`bin/console cache:clear` will also clear the HTTP cache. If this is not intended, you should manually delete the `var/cache` folder. The object cache can be cleared with `bin/console cache:pool:clear --all` explicitly.

---

