# Guides

*Scraped from Shopware Developer Documentation*

---

## Extensions

**Source:** https://developer.shopware.com/docs/guides/plugins/

# Extensions [​](#extensions)

As a Shopware developer, your primary focus is developing extensions that enhance or modify Shopware's functionality. Shopware offers three extension types—Plugins, Themes, and Apps—each with its own benefits and implications.

To dive straight in, take a look at our introduction guides, which provide essential information on how to create, configure, and extend your store with Shopware extensions:

[Plugin Base Guide](plugins/plugin-base-guide)[App Base Guide](apps/app-base-guide)[Theme Base Guide](themes/theme-base-guide)

## At a glance [​](#at-a-glance)

This comparison table aims to help you decide which Shopware extension type best fits your use case.

| Task | Plugin | Theme | App | Remarks |
| --- | --- | --- | --- | --- |
| Change Storefront appearance | ✅ | ✅ | ✅ |  |
| Add admin modules | ✅ | ❌ | ✅ |  |
| Execute webhooks | ✅ | ❌ | ✅ | Apps' main functionality is to call webhooks, but plugins can be implemented to do that as well. |
| Add custom entities | ✅ | ❌ | ✅ |  |
| Modify database structure | ✅ | ❌ | ❌ |  |
| Integrate payment providers | ✅ | ❌ | ✅ |  |
| Publish in the Shopware Store | ✅ | ✅ | ✅ |  |
| Install in Shopware 6 Cloud Shops | ❌ | ❌ (unless delivered via App) | ✅ | While theme plugins can’t be installed in Cloud, Apps can include themes and provide the same functionality. |
| Install in Shopware 6 self-hosted Shops | ✅ | ✅ | ✅ | Apps can be installed and used since Shopware 6.4.0.0. |
| Add custom logic/routes/commands | ✅ | ❌ | ✅ | Apps extract functionalities/logic into separate services, so technically, they can add custom logic. |
| Control order of style/template inheritance | ❌ | ✅ | ✅ |  |

---

## Elasticsearch

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/elasticsearch/

# Elasticsearch [​](#elasticsearch)

By extending fields of an entity to the Elasticsearch engine, you expand the search capabilities of Shopware, allowing users to search based on additional attributes or metadata. This enhances the overall search experience and enables more targeted and precise search results for customers.

---

## Add product entity extension to elasticsearch

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/elasticsearch/add-product-entity-extension-to-elasticsearch.html

# Adding Product Entity Extension to Elasticsearch [​](#adding-product-entity-extension-to-elasticsearch)

## Overview [​](#overview)

In this guide you'll learn how to add extended fields of the product entity to the elasticsearch engine to make it searchable.

In this example we'll assume an extension of the `ProductDefinition` with a string field `customString` like described in [Adding Complex data to existing entities](./../framework/data-handling/add-complex-data-to-existing-entities.html#adding-a-field-without-database).

## Prerequisites [​](#prerequisites)

This guide is built upon the [Plugin Base Guide](./../plugin-base-guide.html), and the entity extension described in [Adding Complex data to existing entities](./../framework/data-handling/add-complex-data-to-existing-entities.html#adding-a-field-without-database). We will extend the product extension with an `OneToOneAssociationField` and `OneToManyAssociationField`.

## Decorate the ElasticsearchProductDefinition [​](#decorate-the-elasticsearchproductdefinition)

To extend the elasticsearch definition we need to extend the product definition first and add the subscriber. This is described in the above mentioned articles. Here we show you how this could look like in the end.

The service.xml with all needed definitions.

xml

```shiki
// <plugin root>/src/Core/Content/DependencyInjection/product.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Extension\Content\Product\CustomExtension">
            <tag name="shopware.entity.extension"/>
        </service>

        <service id="Swag\BasicExample\Extension\Content\Product\OneToOneExampleExtensionDefinition">
            <tag name="shopware.entity.definition" entity="one_to_one_swag_example_extension" />
        </service>

        <service id="Swag\BasicExample\Extension\Content\Product\OneToManyExampleExtensionDefinition">
            <tag name="shopware.entity.definition" entity="one_to_many_swag_example_extension" />
        </service>

        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>

        <service id="Swag\BasicExample\Elasticsearch\Product\MyProductEsDecorator" decorates="Shopware\Elasticsearch\Product\ElasticsearchProductDefinition">
            <argument type="service" id="Swag\BasicExample\Elasticsearch\Product\MyProductEsDecorator.inner"/>
            <argument type="service" id="Doctrine\DBAL\Connection"/>
        </service>
    </services>
</container>
```

The product extension `CustomExtension.php` provides the extensions to the product entity.

php

```shiki
// <plugin root>/src/Extension/Content/Product/CustomExtension.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ObjectField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToManyAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Runtime;

class CustomExtension extends EntityExtension
{
    public function extendFields(FieldCollection $collection): void
    {
        //Add ApiAware flag to make this field searchable
        $collection->add(
            (new OneToOneAssociationField('oneToOneExampleExtension', 'id', 'product_id', OneToOneExampleExtensionDefinition::class, true))->addFlags(new ApiAware())
        );
        //Add ApiAware flag to make this field searchable
        $collection->add(
            (new OneToManyAssociationField('oneToManyExampleExtension', OneToManyExampleExtensionDefinition::class, 'product_id'))->addFlags(new ApiAware())
        );
        //Runtime fields are not searchable
        $collection->add(
            (new ObjectField('custom_string', 'customString'))->addFlags(new Runtime())
        );
    }

    public function getDefinitionClass(): string
    {
        return ProductDefinition::class;
    }
}
```

The entity definition `OneToManyExampleExtensionDefinition.php`.

php

```shiki
// <plugin root>/src/Extension/Content/Product/OneToManyExampleExtensionDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\ApiAware;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ManyToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ReferenceVersionField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;

class OneToManyExampleExtensionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'one_to_many_swag_example_extension';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return Entity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new ApiAware(), new Required(), new PrimaryKey()),
            new FkField('product_id', 'productId', ProductDefinition::class),
            (new ReferenceVersionField(ProductDefinition::class))->addFlags(new Required()),
            (new StringField('custom_string', 'customString'))->addFlags(new ApiAware()),

            new ManyToOneAssociationField('product', 'product_id', ProductDefinition::class),
        ]);
    }
}
```

The entity definition `OneToOneExampleExtensionDefinition.php`.

php

```shiki
// <plugin root>/src/Extension/Content/Product/OneToOneExampleExtensionDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\ApiAware;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ReferenceVersionField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;

class OneToOneExampleExtensionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'one_to_one_swag_example_extension';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return Entity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new ApiAware(), new Required(), new PrimaryKey()),
            new FkField('product_id', 'productId', ProductDefinition::class),
            (new ReferenceVersionField(ProductDefinition::class))->addFlags(new Required()),
            (new StringField('custom_string', 'customString'))->addFlags(new ApiAware()),

            new OneToOneAssociationField('product', 'product_id', 'id', ProductDefinition::class, false)
        ]);
    }
}
```

Here is a decoration to add a new field named `customString`, an `oneToOneAssociationField` named `oneToOneExampleExtension` and an `oneToManyAssociationField` named `oneToManyExampleExtension` to the index. For adding more information from the database you should execute a single query with all document ids `(array_column($documents, 'id'))` and map the values.

php

```shiki
// <plugin root>/src/Elasticsearch/Product/MyProductEsDecorator.php
<?php

namespace Swag\BasicExample\Elasticsearch\Product;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;
use Doctrine\DBAL\Connection;
use Swag\BasicExample\Subscriber\ProductSubscriber;

class MyProductEsDecorator extends AbstractElasticsearchDefinition
{
    private AbstractElasticsearchDefinition $productDefinition;
    private Connection $connection;

    public function __construct(AbstractElasticsearchDefinition $productDefinition, Connection $connection)
    {
        $this->productDefinition = $productDefinition;
        $this->connection = $connection;
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->productDefinition->getEntityDefinition();
    }

    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->productDefinition->buildTermQuery($context, $criteria);
    }

    /**
     * Extend the mapping with your own changes
     * Take care to get the default mapping first by `$this->productDefinition->getMapping($context);`
     */
    public function getMapping(Context $context): array
    {
        $mapping = $this->productDefinition->getMapping($context);

        //The mapping for a simple keyword field
        $mapping['properties']['customString'] = AbstractElasticsearchDefinition::KEYWORD_FIELD;

        // Adding an association as keyword
        $mapping['properties']['oneToOneExampleExtension'] = [
                'type' => 'nested',
                'properties' => [
                    'customString' => AbstractElasticsearchDefinition::KEYWORD_FIELD,
            ],
        ];

        // Adding a nested field with id
        $mapping['properties']['oneToManyExampleExtension'] = [
            'type' => 'nested',
            'properties' => [
                'id' => AbstractElasticsearchDefinition::KEYWORD_FIELD,
            ],
        ];

        return $mapping;
    }

    public function fetch(array $ids, Context $context): array
    {
        $documents = $this->productDefinition->fetch($ids, $context);

        $associationOneToOne = $this->fetchOneToOneExample($ids);
        $associationOneToMany = $this->fetchOneToManyExample($ids);

        foreach ($documents as &$document) {
            /**
             * A field directly on the product.
             * The value should be filled with the same Runtime value which will be set by the ProductSubscriber
             */
            $document['customString'] = ProductSubscriber::getRuntimeValue($document['id'])->getValue();

            /**
             * Field with value from associated entity
             */
            if (isset($associationOneToOne[$document['id']])) {
                $document['oneToOneExampleExtension']['customString'] = $associationOneToOne[$document['id']];
            }

            /**
             * Field with multiple id entries from associated entity
             */
            if (isset($associationOneToMany[$document['id']])) {
                $document['oneToManyExampleExtension'] = array_map(function (string $id) {
                    return ['id' => $id];
                }, array_filter(explode('|', $associationOneToMany[$document['id']] ?? '')));
            }
        }

        return $documents;
    }

    /**
     * Read the associated entries directly from the database
     */
    private function fetchOneToOneExample(array $ids): array
    {
        $query = <<<SQL
            SELECT LOWER(HEX(product_id)) as id, custom_string
            FROM one_to_one_swag_example_extension
            WHERE
                product_id IN(:ids)
        SQL;

        return $this->connection->fetchAllKeyValue(
            $query,
            [
                'ids' => $ids,
            ],
            [
                'ids' => Connection::PARAM_STR_ARRAY
            ]
        );
    }

    /**
     * Read the associated entries directly from the database
     */
    private function fetchOneToManyExample(array $ids): array
    {
        $query = <<<SQL
            SELECT LOWER(HEX(product_id)) as id, GROUP_CONCAT(id SEPARATOR "|")
            FROM one_to_many_swag_example_extension
            WHERE
                product_id IN(:ids)
        SQL;

        return $this->connection->fetchAllKeyValue(
            $query,
            [
                'ids' => $ids,
            ],
            [
                'ids' => Connection::PARAM_STR_ARRAY
            ]
        );
    }
}
```

---

## Framework

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/

# Framework [​](#framework)

Shopware is a flexible e-commerce framework that allows developers to extend and customize the platform according to specific business needs, creating scalable and personalized online stores. The Shopware framework offers data abstraction, custom fields, events, rules, message queues, file systems, flows, and rate limiters.

More about these features and their extensibility is mentioned in the further sections.

---

## Caching

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/caching/

# Caching [​](#caching)

Caching is a technique to store frequently accessed data in a temporary storage layer for faster retrieval, reducing latency and improving performance by avoiding repeated and costly data retrieval operations

While caching enhances performance, it requires careful management of data consistency, cache invalidation strategies, and storage efficiency to prevent serving outdated or incorrect data.

This guide will show you how you can modify the default caching mechanisms to suite your needs. If you are looking for information on how to add your routes to the HTTP-Cache, take a look at [this guide](./../../storefront/add-caching-to-custom-controller.html).

## Cache Layers [​](#cache-layers)

The current cache system of Shopware is based on a multi-layer system, in which the individual layers build on each other to improve performance and scalability. There is the [HTTP-Cache](./../../../../../concepts/framework/http_cache.html) on the outer level and then multiple smaller internal "Object Caches" that are used to cache data in the application.

For information on how to configure the different cache layers, please refer to the [caching hosting guide](./../../../../hosting/performance/caches.html).

### HTTP-Cache [​](#http-cache)

Before jumping in and adjusting the HTTP-Caching, please familiarize yourself with the general [HTTP-Cache concept](./../../../../../concepts/framework/http_cache.html) first.

#### Manipulating the cache key [​](#manipulating-the-cache-key)

There are several entry points to manipulate the cache key.

* `Shopware\Core\Framework\Adapter\Cache\Http\Extension\CacheHashRequiredExtension`: used to determine whether the cache hash should be calculated or if the request in running in the default state, and therefore no cache-hash is needed.
* `Shopware\Core\Framework\Adapter\Cache\Event\HttpCacheCookieEvent`: used to calculate the cache hash based on the application state, supports both reverse proxy caches and the default symfony HTTP-cache component.
* `Shopware\Core\Framework\Adapter\Cache\Http\Extension\ResolveCacheRelevantRuleIdsExtension`: used to determine which rule IDs are relevant for the cache hash.
* `Shopware\Core\Framework\Adapter\Cache\Event\HttpCacheKeyEvent`: used to calculate the exact cache key based on the response, only for symfony's default HTTP-cache component.

##### Modifying when the cache hash is calculated [​](#modifying-when-the-cache-hash-is-calculated)

By default, the cache hash is only calculated when the request is not in the default state, which is: no logged in customer, default currency, and an empty cart. The reason is that the very first request to the application from a client should always be cached in the best case, the state that the application is in then is the "default state", which does not require a cache hash. You can overwrite the default behaviour and add more conditions where the cache hash needs to be applied, e.g., when you shop needs to be more dynamic e.g. based on campaign query parameters:

php

```shiki
class RequireCacheHash implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            CacheHashRequiredExtension::NAME . '.post' => 'onRequireCacheHash',,
        ];
    }

    public function onRequireCacheHash(CacheHashRequiredExtension $extension): void
    {
        if ($extension->request->query->has('campaignId')) {
            $extension->result = true;
        }
    }
}
```

##### Modifying the cache hash [​](#modifying-the-cache-hash)

The cache hash is used as the basis for the cache key. It is calculated based on the application state, which includes the current user, the current language, and so on. As the cache hash is calculated based on the application state, you have access to the resolved `SalesChannelContext` to determine the cache hash. It is stored alongside the response as a cookie and thus also provided with all following requests, to allow differentiating the cache based on the application state. As the cache hash will be carried over to the next request, the computed cache hash can be used inside reverse proxy caches as well as the default symfony HTTP-cache component.

INFO

The cache hash is only computed on every response as soon as the application state differs from the default state, which is: no logged in customer, default currency, and an empty cart.

By default, the cache hash will consist of the following parts:

* `rule-ids`: The matched rule IDs, to reduce possible cache permutations starting with v6.8.0.0, this will only include the rule IDs in `rule areas` that are cache relevant. See the next chapter how to extend this.
* `version-id`: The context version used to load versioned DAL entities.
* `currency-id`: The currency ID of the context.
* `tax-state`: The tax state of the context (gross/net).
* `logged-in`: Whether a customer is logged in in the current state or not.

To modify the cache hash, you can subscribe to the `HttpCacheCookieEvent` event and add your own parts to the cache hash. This allows you to add more parts to the cache hash, e.g., the current customer's group. You can also disable the cache for certain conditions, because if that condition is met, the content is so dynamic that caching is not efficiently possible e.g., if the cart is filled.

php

```shiki
class HttpCacheCookieListener implements EventSubscriberInterface
{
    public function __construct(
        private readonly CartService $cartService
    ) {
    }
    
    public static function getSubscribedEvents(): array
    {
        return [
            HttpCacheCookieEvent::class => 'onCacheCookie',
        ];
    }

    public function onCacheCookie(HttpCacheCookieEvent $event): void
    {
        // you can add custom parts to the cache hash
        // keep in mind that every possible value will increase the number of possible cache permutations
        // and therefore directly impact cache hit rates, which in turn decreases performance
        $event->add('customer-group', $event->context->getCustomerId());

        // disable cache for filled carts
        $cart = $this->cartService->getCart($event->context->getToken(), $event->context);
        if ($cart->getLineItems()->count() > 0) {
            // you can also explicitly disable caching based on specific conditions
            $event->isCacheable = false;
        }
    }
}
```

Additionally, you can modify the cache hash from the frontend client directly by adding separate cookies with the relevant value. You can configure custom cookies that are relevant for the cache hash in the `shopware.http_cache.cookies` option:

yaml

```shiki
shopware:
    http_cache:
        cookies:
            - 'my-custom-cookie'
```

As soon as the cookie is set, that value will be included in the cache hash. Essentially, it saves you the effort to implement a custom cache cookie listener as shown above. This makes it especially suited for headless projects where the frontend implementation is more decoupled from the backend.

##### Marking rule areas as cache relevant [​](#marking-rule-areas-as-cache-relevant)

Starting with v6.8.0.0, the cache hash will only include the rule IDs in `rule areas` that are cache relevant. The reason is that a lot of rules are not relevant for the cache, e.g., rules that only affect pricing or shipping methods. This greatly reduces the number of possible cache permutations, which in turn improves the cache hit rate.

By default, only the following rule areas are cache relevant:

* `RuleAreas::PRODUCT_AREA`

If you use the rule system in a way that is relevant for the cache (because the response differs based on the rules), you should add your rule area to the list of cache relevant rule areas. To do so, you need to subscribe to the `ResolveCacheRelevantRuleIdsExtension` event.

php

```shiki
class ResolveRuleIds implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ResolveCacheRelevantRuleIdsExtension::NAME . '.pre' => 'onResolveRuleAreas',
        ];
    }

    public function onResolveRuleAreas(ResolveCacheRelevantRuleIdsExtension $extension): void
    {
        $extension->ruleAreas[] = RuleExtension::MY_CUSTOM_RULE_AREA;
    }
}
```

This implies that you defined the rule area in your custom entities that have an associated rule entity, by using the DAL flag `Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\RuleAreas` on the rule association in the entity extension.

php

```shiki
class RuleExtension extends EntityExtension
{
    public const MY_CUSTOM_RULE_AREA = 'custom';

    public function getEntityName(): string
    {
        return RuleDefinition::ENTITY_NAME;
    }

    public function extendFields(FieldCollection $collection): void
    {
        $collection->add(
            (new ManyToManyAssociationField(
                'myPropertyName',
                MyCustomDefinition::class,
                MyMappingDefinition::class,
                RuleDefinition::ENTITY_NAME . '_id',
                MyCustomDefinition::ENTITY_NAME . '_id',
            ))->addFlags(new CascadeDelete(), new RuleAreas(self::MY_CUSTOM_RULE_AREA)),
        );
    }
}
```

For details on how to extend core definitions refer to the [DAL Guide](./../../framework/data-handling/add-complex-data-to-existing-entities.html).

##### Modifying the cache keys [​](#modifying-the-cache-keys)

You can also modify the exact cache key used to store the response in the [symfony HTTP-Cache](https://symfony.com/doc/current/http_cache.html). If possible, you should manipulate the cache hash (as already explained above) instead, as that is also used in reverse proxy caches. You can do so by subscribing to the `HttpCacheKeyEvent` event and add your specific part to the key.

php

```shiki
class CacheKeySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            HttpCacheKeyEvent::class => 'addKeyPart',
        ];
    }
    
    public function addKeyPart(HttpCacheKeyEvent $event): void
    {
        $request = $event->request;
        // Perform checks to determine the key
        $key = $this->determineKey($request);
        $event->add('myCustomKey', $key);
        
        // You can also disable caching for certain conditions
        $event->isCacheable = false;
    }
}
```

INFO

The event is called on any Request; make sure that you don't use expensive operations like Database Queries.

Also, with an external reverse proxy, the cache key might be generated on the proxy and not in your application. In that case, you need to add the key part to the reverse proxy configuration.

#### Adding cache tags [​](#adding-cache-tags)

One problem with caching is that you not only need to retrieve the correct data, but also need to have a performant way to invalidate the cache when the data changes. Only invalidating the caches based on the unique cache key is often not that helpful, because you don't know which cache keys are affected by the change of a specific data set. Therefore, a tagging system is used alongside the cache keys to make cache invalidations easier and more performant. Every cache entry can be tagged with multiple tags, thus we can invalidate the cache based on the tags. For example, all pages that contain product data are tagged with product IDs of all products they contain. So if a product is changed, we can invalidate all cache entries that are tagged with the product ID of the changed product.

To add your own cache tags to the HTTP-Cache, you can use the `CacheTagCollector` service.

php

```shiki
class MyCustomEntityExtension
{
    public function __construct(
        private readonly CacheTagCollector $cacheTagCollector,
    ) {}
    
    public function loadAdditionalData(): void
    {
        // Load the additional data you need, add it to the response, then add the correct tag to the cache entry
        $this->cacheTagCollector->addTag('my-custom-entity-' . $idOfTheLoadedData);
    }
}
```

#### Invalidating the cache [​](#invalidating-the-cache)

Adding custom cache tags is only useful if you also use them to invalidate the cache when the data changed. To invalidate the cache, you need to call the `CacheInvalidator` service and pass the tag you want to invalidate.

php

```shiki
class CacheInvalidationSubscriber implements EventSubscriberInterface
{
    public function __construct(private CacheInvalidator $cacheInvalidator) 
    {
    }
    
    public static function getSubscribedEvents()
    {
        return [
            // The EntityWrittenContainerEvent is a generic event always thrown when an entities are written. This contains all changed entities
            EntityWrittenContainerEvent::class => 'invalidate'
            ],
        ];
    }
    
    public function invalidate(EntityWrittenContainerEvent $event): void
    {
        // Check if own entity written. In some cases, you want to use the primary keys for further cache invalidation
        $changes = $event->getPrimaryKeys(ExampleDefinition::ENTITY_NAME);
        
        // No example entity changed? Then the cache does not need to be invalidated
        if (empty($changes)) {
            return;
        }

        foreach ($changes as $id) {
            // Invalidate the cache for the changed entity
            $this->cacheInvalidator->invalidate([
                'my-custom-entity-' . $id
            ]);
        }
    }
}
```

##### Overwrite default cache invalidation behaviour [​](#overwrite-default-cache-invalidation-behaviour)

The default tags that shopware adds to the HTTP-Cache are also invalidated automatically when the data changes. This is done by the `CacheInvalidationSubscriber` class, which listens to various events and invalidates the cache based on the tags that are added to the cache entries. However, the subscriber adheres to an exact invalidation concept, where any data written to the product invalidates cache tags for that specific product, even if the data is not used in the corresponding pages. This might lead to cases where the cache is invalidated too often, and the invalidation can be tweaked to the project's needs. Moreover, due to project-specific variations, it is not feasible to generalize the process. Therefore, all events it listens to are configured over the service configuration, so that all events, on which the subscriber listens to, can be manipulated via compiler passes.

PLUGIN\_ROOT/src/Core/Framework/DependencyInjection/cache.xml

xml

```shiki
<service id="Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber">
    <tag name="kernel.event_listener" event="Shopware\Core\Content\Category\Event\CategoryIndexerEvent" method="invalidateCategoryRouteByCategoryIds" priority="2000" />

    <tag name="kernel.event_listener" event="Shopware\Core\Content\Category\Event\CategoryIndexerEvent" method="invalidateListingRouteByCategoryIds" priority="2001" />

    <tag name="kernel.event_listener" event="Shopware\Core\Content\LandingPage\Event\LandingPageIndexerEvent" method="invalidateIndexedLandingPages" priority="2000" />
    
    <!-- ... -->
</service>
```

For example, if you want to disable all cache invalidations in a project, you can remove the `kernel.event_listener` tag of the service definition via compiler pass and implement your own cache invalidation.

php

```shiki
use Shopware\Core\Content\Product\Events\ProductIndexerEvent;
use Shopware\Core\Content\Product\Events\ProductNoLongerAvailableEvent;
use Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener;
use Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber;

class TweakCacheInvalidation implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        $container
            ->getDefinition(CacheInvalidationSubscriber::class)
            ->clearTag('kernel.event_listener')
    }

}
```

However, suppose only certain parts of the cache invalidation are to be adjusted, finer adjustments to the class can be made using `Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener`, in which it is possible to define which event listeners of the service are to be removed.

php

```shiki
use Shopware\Core\Content\Product\Events\ProductIndexerEvent;
use Shopware\Core\Content\Product\Events\ProductNoLongerAvailableEvent;
use Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener;
use Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber;

class TweakCacheInvalidation implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        RemoveEventListener::remove(
            $container,
            CacheInvalidationSubscriber::class,
            [
                [ProductIndexerEvent::class, 'invalidateListings'],
                [ProductNoLongerAvailableEvent::class, 'invalidateListings'],
            ]
        );
    }
}
```

### Object Cache [​](#object-cache)

The internal caches are built upon the [Symfony Cache](https://symfony.com/doc/current/components/cache.html) component and are used internally to cache data that is expensive to compute or retrieve. As the object caches are handled internally, it should not be necessary to control them directly, therefore adding custom tags or manipulating the cache key is not supported for the various object caches.

#### Cache invalidation [​](#cache-invalidation)

However, you can still manually invalidate the object caches, via the same mechanism as you invalidate the HTTP-Cache, the `CacheInvalidator` service.

You can use the `CacheInvalidator` service to invalidate the object caches by passing the tag you want to invalidate.

php

```shiki
public function invalidateSystemConfigCache(): void
{
    $this->cacheInvalidator->invalidate([
        CachedSystemConfigLoader::CACHE_TAG
    ]);
}
```

## Delayed Invalidation [​](#delayed-invalidation)

By default, the cache invalidation happens delayed (for both http and object caches). This means that the invalidation is not instant, but rather all the tags that should be invalidated are invalidated in a regular interval. For special cases where you need to immediately clear the cache take a look at the [force immediate invalidation](#force-immediate-invalidation) section. This really benefits the performance of the system, as the invalidation is not done immediately, but rather in a batch process. Additionally, it prevents cases where sometimes the caches are written and deleted more often than they are read, which only leads to overhead, more resource needs on the caching side and a bad cache-hit rate.

The invalidation of the delayed cache is done via the `shopware.invalidate_cache` task, that runs every 5 minutes (default setting). However, that run interval can be adjusted in the database. If your caches don't seem to be invalidated at all, please ensure that the scheduled tasks are running correctly.

You can also manually invalidate the cache entries that are marked for delayed invalidation by running the `cache:clear:delayed` command or calling the `CacheInvalidator::invalidateExpired()` method from your plugin or send an API request to the `DELETE /api/_action/cache-delayed` endpoint. For debug purposes you can also watch the tags that are marked for delayed invalidation by running the `cache:watch:delayed` command.

### Force immediate invalidation [​](#force-immediate-invalidation)

Some changes require that the caches should be invalidated immediately and returning stale content is not acceptable. In that case you can pass the `force=true` flag to the CacheInvalidator service, which will invalidate the cache immediately.

php

```shiki
public function invalidateSystemConfigCache(): void
{
    $this->cacheInvalidator->invalidate([
        CachedSystemConfigLoader::CACHE_TAG
    ], true);
}
```

If you sent an API request with critical information, where the cache should be invalidated immediately, you can set the `sw-force-cache-invalidate` header on your request.

http

```shiki
POST /api/product
sw-force-cache-invalidate: 1
```

## Manual cache clear [​](#manual-cache-clear)

You can also manually clear the caches when you performed some actions that made a cache invalidation necessary, but where it was not triggered automatically. To clear all caches, you can execute the `cache:clear:all` command, which clears the HTTP-Cache, the object caches as well as any other caches that are registered in the system. The `cache:clear` command on the other hand will only clear the object caches, but won't invalidate the HTTP-Cache. On the other hand, the `cache:clear:http` command will clear the complete HTTP-Cache, but won't invalidate the object caches.

---

## Custom Fields

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/custom-field/

# Custom Fields [​](#custom-fields)

Custom fields in Shopware refer to additional data fields that can be added to entities such as products, customers, or orders. These fields allow businesses to store and manage extra information that may be specific to their operations.

With custom fields, you can define and store data beyond the standard attributes provided by Shopware. For example, a clothing store might add a custom field to track fabric composition, while a hardware store could add a custom field to store product dimensions.

Through the administration or via the API, users can create and manage custom fields, define their data types (such as text, number, date, etc.), and assign them to specific entities. This allows businesses the ability to extend the default data structure enabling a more tailored and personalized e-commerce experience.

---

## Add custom field

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/custom-field/add-custom-field.html

# Add Custom Field [​](#add-custom-field)

## Overview [​](#overview)

Shopware's custom field system allows you to extend entities without writing a complete entity extension. This is possible by storing the additional data in a [JSON-Field](https://dev.mysql.com/doc/refman/8.0/en/json.html). Custom fields, therefore, can only be used to store scalar values. If you'd like to create associations between entities, you'll need to use an [Entity extension](./../data-handling/add-complex-data-to-existing-entities.html).

This guide will cover two similar subjects:

* Supporting custom fields with your entity
* Add custom fields to an entity

## Prerequisites [​](#prerequisites)

This guide is built upon both the [Plugin base guide](./../../plugin-base-guide.html) and the [Add custom complex data](./../data-handling/add-custom-complex-data.html) guide. The latter explained how to create your very first entity, which is used in the following examples.

Since migrations will also be used here, it won't hurt to have a look at our guide about [Executing database queries](./../../plugin-fundamentals/database-migrations.html).

Also, adding translatable custom fields is covered here in short as well, for which you'll need to understand how translatable entities work in general. This is covered in our guide about [Adding data translations](./../data-handling/add-data-translations.html). This subject will **not** be covered in depth in this guide.

## Supporting custom fields with your entity [​](#supporting-custom-fields-with-your-entity)

This short section will cover how to add a custom field support for your custom entity. As previously mentioned, the example from our [Add custom complex data](./../data-handling/add-custom-complex-data.html) guide is used and extended here.

To support custom fields with your custom entity, there are three necessary steps :

* Add `EntityCustomFieldsTrait` trait to your `Entity`.
* Add a `CustomFields` field to your `EntityDefinition`.
* Add a column `custom_fields` to your entities' database table via migration.

Also, you may want to add translatable custom fields, which is also covered in very short here.

### Add a custom field to an entity [​](#add-a-custom-field-to-an-entity)

INFO

Available starting with Shopware 6.4.1.0.

Let's assume you already got a working and running entity definition. If you want to support custom fields with your custom entity, you may add the `EntityCustomFieldsTrait` to your entity class, so the methods `getCustomFields()` and `setCustomFields()` can be used.

php

```shiki
// <plugin root>/src/Core/Content/Example/ExampleEntity.php
use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityCustomFieldsTrait;
use Shopware\Core\Framework\DataAbstractionLayer\EntityIdTrait;

[...]
class ExampleEntity extends Entity
{
    use EntityIdTrait;
    use EntityCustomFieldsTrait;

    [...]

}
```

### Add a custom field to entity definition [​](#add-a-custom-field-to-entity-definition)

Now follows the important part. For this to work, you have to add the Data Abstraction Layer (DAL) field `CustomFields` to your entity definition.

php

```shiki
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\CustomFields;                                                                    

[...]
class ExampleDefinition extends EntityDefinition
{

    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active')),

            new CustomFields()
        ]);
    }
}
```

Note the new field that was added in the `FieldCollection`. That's already it for your custom entity definition. Now go ahead and add the column to the database.

### Add a column in the database table [​](#add-a-column-in-the-database-table)

Once again, this example is built upon the [Add custom complex data](./../data-handling/add-custom-complex-data.html) guide, which also comes with an example migration. This one will be used in this example here as well.

If you want to support custom fields now, you have to add a new column `custom_fields` of type `JSON` to your migration.

php

```shiki
// <plugin root>/src/Migration/Migration1611664789Example.php
public function update(Connection $connection): void
{
    $sql = <<<SQL
        CREATE TABLE IF NOT EXISTS `swag_example` (
        `id` BINARY(16) NOT NULL,
        `name` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
        `description` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
        `active` TINYINT(1) COLLATE utf8mb4_unicode_ci,

        `custom_fields` json DEFAULT NULL,

        `created_at` DATETIME(3) NOT NULL,
        `updated_at` DATETIME(3),
        PRIMARY KEY (`id`)
        )
        ENGINE = InnoDB
        DEFAULT CHARSET = utf8mb4
        COLLATE = utf8mb4_unicode_ci;
    SQL;
    $connection->executeStatement($sql);
}
```

Note the new `custom_fields` column here. It has to be a JSON field and should default to `NULL`, since it doesn't have to contain values.

### Add translatable custom field to entity definition [​](#add-translatable-custom-field-to-entity-definition)

Make sure to understand entity translations in general first, which is explained here [Add data translations](./../data-handling/add-data-translations.html). If you want your custom fields to be translatable, you can simply work with a `TranslatedField` here as well.

php

```shiki
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\TranslatedField;                                                               

[...]

class ExampleDefinition extends EntityDefinition
{
    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active')),

            new TranslatedField('customFields'),
        ]);
    }
}
```

Just add the `TranslatedField` and apply `customFields` as a parameter.

In your translated entity definition, you then add the `CustomFields` field instead.

php

```shiki
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\CustomFields;                                                                    

[...]
class ExampleTranslationDefinition extends EntityTranslationDefinition
{
    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new StringField('name', 'name'))->addFlags(new Required()),

            new CustomFields()
        ]);
    }
}
```

## Add custom fields to an entity [​](#add-custom-fields-to-an-entity)

The previous section was about adding support for custom fields in your entity, but this section will cover how to add an actual custom field to an entity and how to fill it with data.

Technically, there is no need to define a custom field set and its fields first, before actually inserting values into the `custom_fields` column of your entities' database table via the DAL. Defining a custom field set is only necessary, if you want it to be editable in the Administration or if you need validation when writing your custom field.

Because of that, we'll start with filling data to an actual entities' custom field, before actually defining it.

### Filling data into custom fields [​](#filling-data-into-custom-fields)

So let's assume you've got your own `example` entity up and running, and now you want to add data to its custom fields via the DAL.

In that case, you can use your entities' repository and start creating or updating entities with custom fields. If you don't understand what's going on here, head over to our guide about [Writing data](./../data-handling/writing-data.html) first.

php

```shiki
$this->swagExampleRepository->upsert([[
    'id' => '<your ID here>',
    'customFields' => ['swag_example_size' => 15]
]], $context);
```

This will execute perfectly fine, and you just saved a custom field with name `swag_example_size` with its value `15` to your entity. And you haven't even defined the custom field `swag_example_size` yet.

As already mentioned, you do not have to define a custom field first before saving it. That's because there is no validation happening here yet, you can write whatever valid JSON you want to that column, so the following example would also execute without any issues:

php

```shiki
$this->swagExampleRepository->upsert([[
    'id' => '<your ID here>',
    'customFields' => [ 'foo' => 'bar', 'baz' => [] ]
]], $context);
```

### Add a custom field to the Administration [​](#add-a-custom-field-to-the-administration)

You can skip this section if you don't want your new custom field to be editable in the Administration.

So now you've already filled the custom fields of one of your entity instances via code. But what if you want your user to do that, which is the more common case?

Only if you want your custom field to show up in the Administration and to be editable in there, you have to define the custom fields first in a custom field set. For this you have to use the custom fieldset repository, which can be retrieved from the dependency injection container via the `custom_field_set.repository` key and is used like any other repository.

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\CustomFieldClass">
          <argument type="service" id="custom_field_set.repository"/>
          ...
        </service>
    </services>
</container>
```

If you need to learn how that is done in full, head to our guide regarding [Writing data](./../data-handling/writing-data.html).

Now use the `create` method of the repository to create a new custom field set. Plugin lifecycle events are perfect for this as the container can provide the `custom_field_set.repository` service and can be used to set up on installation and remove the set on removal.

php

```shiki
use Shopware\Core\System\CustomField\CustomFieldTypes;
use \Shopware\Core\Defaults;

[...]

$this->customFieldSetRepository->create([
    [
        'name' => 'swag_example_set',
        'global' => true,
        'config' => [
            'label' => [
                'en-GB' => 'English custom field set label',
                'de-DE' => 'German custom field set label',
                Defaults::LANGUAGE_SYSTEM => "Mention the fallback label here"
            ]
        ],
        'customFields' => [
            [
                'name' => 'swag_example_size',
                'type' => CustomFieldTypes::INT,
                'includeInSearch' => true,
                'config' => [
                    'label' => [
                        'en-GB' => 'English custom field label',
                        'de-DE' => 'German custom field label',
                        Defaults::LANGUAGE_SYSTEM => "Mention the fallback label here"
                    ],
                    'customFieldPosition' => 1
                ]
            ]
        ]
    ]
], $context);
```

This will now create a custom field set with the name `swag_example_set` and the field, `swag_example_size`. This time we also define its type, which should be of type integer here. The type is important to mention, because the Administration will use this information to display a proper field. Also, when trying to write the custom field `swag_example_size`, the value has to be an integer.

The translated labels are added to both the field and the set, which are going to be displayed in the Administration. Also, the fallback language can be defined in case the system language is not guaranteed to be either en\_GB or de\_DE.

If you have several custom fields and want to order them within a specific order, you can do so with the `customFieldPosition` property.

INFO

Available starting with Shopware 6.7.6.0.

By default, custom fields are **not searchable**. To make a custom field searchable, you need to set the `includeInSearch` property to `true` when creating the custom field. Only custom fields explicitly marked as searchable are available in search configurations. This helps optimize index storage size and improve search performance, especially for stores with many custom fields.

If you enable searchability for an existing product custom field, you must rebuild the search index or update the products manually to include the custom field data in search results.

INFO

If you want the custom field set to be deletable and editable in the administration, you need to set global to false

While theoretically your custom field is now properly defined for the Administration, you'll still have to do some work in your custom entities' Administration module. Head over to this guide to learn how to add your field to the Administration:

[Using custom fields](../../administration/data-handling-processing/using-custom-fields)

### Deleting a custom field [​](#deleting-a-custom-field)

On uninstallation of your plugin, you should remove your custom field definition. To update or delete a `custom_field_set`, you can use the standard repository methods like `update`, `upsert`, or `delete`:

php

```shiki
$setId = $this->customFieldSetRepository->searchIds((new Criteria())->addFilter(new EqualsFilter('name', 'swag_example_set')), $context)->firstId();
$this->customFieldSetRepository->delete([['id' => $setId]], $context);
```

When you delete a custom field in a set or a complete set, you should remove the values from the entity's customFields property. Without the custom field definition, the data is still taking up space, and some checks regarding API usage are no longer performed. This batch operation is fast in SQL with a query like:

sql

```shiki
UPDATE swag_example SET custom_fields = JSON_REMOVE(custom_fields, '$.swag_example_size') WHERE JSON_CONTAINS_PATH(custom_fields, 'one', '$.swag_example_size');
```

If you have a table with a lot of data, like orders or products, you should not approach it carelessly to avoid overwhelming the database with too many changes at once. This can look like this instead:

php

```shiki
$updateLimit = 1000;

do {
    $ids = $connection->fetchFirstColumn(
        'SELECT `id` FROM `order` WHERE JSON_CONTAINS_PATH(`custom_fields`, \'one\', \'$.swag_example_size\') LIMIT :limit',
        ['limit' => $updateLimit],
        ['limit' => ParameterType::INTEGER]
    );

    if ($ids === []) {
        break;
    }

    $connection->executeStatement(
        'UPDATE `order` SET `custom_fields` = JSON_REMOVE(`custom_fields`, \'$.swag_example_size\') WHERE `id` IN (:ids)',
        ['ids' => $ids],
        ['ids' => ArrayParameterType::BINARY]
    );
} while (\count($ids) === $updateLimit);
```

## Next steps [​](#next-steps)

If you want to extend an entity with new associations and non-scalar values, head over to our guide regarding [Extending existing entities](./../data-handling/add-complex-data-to-existing-entities.html).

---

## Fetching data from "entity selection" custom field

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/custom-field/fetching-data-from-entity-selection.html

# Fetching Data from "Entity Selection" Custom Field [​](#fetching-data-from-entity-selection-custom-field)

## Overview [​](#overview)

If you set up a custom field with an entity selection in the Administration, you may need a data resolver to resolve the ID to an entity object.

## Prerequisites [​](#prerequisites)

This guide will not explain how to create custom field in general, so head over to the official guide about [custom field](./add-custom-field.html) to learn this first.

## Fetching data [​](#fetching-data)

In this example we assume that we already set up a custom field called `custom_linked_product`, which is assigned to the products entity. The type of the custom field `custom_linked_product` is also a product.

If you now update a product in the Administration and select a value for `custom_linked_product` only the `id` of the selected product entity gets store in the custom field.

To resolve the `id` and getting access to the product we have linked here, we can create a `ProductSubscriber` which listens to the `ProductEvents::PRODUCT_LOADED_EVENT`. The event will be triggered, when the associated main product will be loaded. So we can easily resolve the id in the custom field.

Lets create a `ProductSubscriber` first which will listen to the `ProductEvents::PRODUCT_LOADED_EVENT`.

php

```shiki
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {
    }
}
```

For this subscriber to work we need to register it in the service container via the `services.xml` file:

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Now our `ProductSubscriber` should be called every time a product is loaded, so we can resolve the custom field `custom_linked_product`.

php

```shiki
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {

        // loop through all loaded product      
        /** @var ProductEntity $productEntity */
        foreach ($event->getEntities() as $productEntity) {
            $customFields = $productEntity->getCustomFields();

            // loop through each product's custom fields
            foreach($customFields as $name => $value) {
                if ($name !== 'custom_linked_product' || empty($value)) {
                    continue;
                }

               // resolve the $value here
            }

            $productEntity->setCustomFields($customFields);
        }
    }
}
```

Inside the `onProductLoaded` method we can get access to the loaded product entities by calling `$event->getEntities()`. Now for every product we look for our `custom_linked_product` custom field.

But, how we can load the linked product by its `id` if the custom field was set? We have to inject the product repository to achieve it.

First we update the `services.xml` and inject the product repository.

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <argument type="service" id="product.repository"/>
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Now we can use the product repository in our subscriber.

php

```shiki
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEntity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository) 
    {
        $this->productRepository = $productRepository;
    }

   //...
}
```

As you can see, the product repository was injected and is now available to the `ProductRepository`. The last step is to resolve the `custom_linked_product` value inside the `onProductLoaded` method.

Let's have a look at the final implementation of the subscriber.

php

```shiki
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEntity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository) 
    {
        $this->productRepository = $productRepository;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {
        // extract all ids of our custom field
        $ids = array_map(function (ProductEntity $entity) {
            return $entity->getCustomFields()['custom_demo_test'] ?? null;
        }, $event->getEntities());

        // filter empty ids
        $ids = array_filter($ids);

        // load all products in one request instead of one request per product (big performance boost)
        $products = $this->productRepository->search(new Criteria($ids), $event->getContext());

        /** @var ProductEntity $entity */
        foreach ($event->getEntities() as $entity) {
            // check if the custom field is set
            if (!$id = $entity->getCustomFields()['custom_demo_test'] ?? null) {
                continue;
            }

            // add the product to the entity as entity extension
            $entity->addExtension('my_custom_demo_product', $products->get($id));
        }
    }
}
```

---

## Event

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/event/

# Event [​](#event)

Shopware events provide a flexible and powerful way to extend the functionality of the e-commerce platform. Events in Shopware are triggered at specific actions. You can extend the platform's functionality by intercepting and executing custom logic during specific system actions. By leveraging events like Storefront events, administration events, or flow builder events, to mention a few, developers can hook into core system actions, such as order placement or product updates, and perform additional tasks, such as sending notifications, modifying data, or integrating with external services, etc. This event-driven architecture enables seamless integration of custom functionalities, making it easier to extend and customize the Shopware platform to meet specific business requirements.

---

## Add custom event

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/event/add-custom-event.html

# Add Custom Event [​](#add-custom-event)

## Overview [​](#overview)

In this guide, you will learn how to create your own event. You can read more about events in the [Symfony documentation](https://symfony.com/doc/current/event_dispatcher.html).

## Prerequisites [​](#prerequisites)

To create your own event for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html).

INFO

Refer to this video on **[Event dispatching and handling](https://www.youtube.com/watch?v=JBpa5nBoC78)** which is a live coding example on custom events. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Event interfaces and classes [​](#event-interfaces-and-classes)

In Shopware, you have multiple interfaces and classes for different types of events, in the following you can find a list of them:

* `ShopwareEvent`: This interface is just a basic event providing a `Context` we need for almost all events.
* `ShopwareSalesChannelEvent`: This interface extends from `ShopwareEvent` and additionally provides a `SalesChannelContext`.
* `SalesChannelAware`: This interface provides the `SalesChannelId`.
* `GenericEvent`: This interface will be used if you want to give your event a specific name like the database events (e.g. `product.written.`). Otherwise, you have to reference to the event class.
* `NestedEvent`: This class will be used for events using other events, for example, the `EntityDeletedEvent` extends from the `EntityWrittenEvent`.
* `BusinessEventInterface`: This interface extends from `ShopwareEvent` and will be used for dynamic assignment and is always named.

## Create the event class [​](#create-the-event-class)

First, we create a new class for our event, which we name `ExampleEvent`. In this example we implement the `Shopware\Core\Framework\Event\ShopwareSalesChannelEvent`. As mentioned above our class already implements a method for the `SalesChannelContext` and the `Context`. Now we pass an `ExampleEntity` and the `SalesChannelContext` through the constructor and create a function which returns our `ExampleEntity`.

Therefore, this is what your event class could look like:

php

```shiki
// <plugin root>/src/Core/Content/Example/Event/ExampleEvent.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\Event;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\Event\ShopwareSalesChannelEvent;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExampleEvent implements ShopwareSalesChannelEvent
{
    protected ExampleEntity $exampleEntity;

    protected SalesChannelContext $salesChannelContext;

    public function __construct(ExampleEntity $exampleEntity, SalesChannelContext $context)
    {
        $this->exampleEntity = $exampleEntity;
        $this->salesChannelContext = $context;
    }

    public function getExample(): ExampleEntity
    {
        return $this->exampleEntity;
    }

    public function getContext(): Context
    { 
        return $this->salesChannelContext->getContext();
    }

    public function getSalesChannelContext(): SalesChannelContext
    {
        return $this->salesChannelContext;
    }
}
```

## Fire the event [​](#fire-the-event)

After we've created our event class, we need to fire our new event. For this we need the service `event_dispatcher` which provides a method called `dispatch`. In this example we created a service `ExampleEventService` which fires our event. Below, you can find the example implementation.

php

```shiki
// <plugin root>/src/Service/ExampleEventService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Swag\BasicExample\Core\Content\Example\Event\ExampleEvent;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

class ExampleEventService
{
    private EventDispatcherInterface $eventDispatcher;

    public function __construct(EventDispatcherInterface $eventDispatcher)
    {
        $this->eventDispatcher = $eventDispatcher;
    }

    public function fireEvent(ExampleEntity $exampleEntity, SalesChannelContext $context)
    {
        $this->eventDispatcher->dispatch(new ExampleEvent($exampleEntity, $context));
    }
}
```

## Next steps [​](#next-steps)

Now that you know how to create your own event, you may want to act on it. To get a grip on this, head over to our [Listening to events](./../../plugin-fundamentals/listening-to-events.html) guide.

---

## Finding events

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/event/finding-events.html

# Finding Events [​](#finding-events)

## Overview [​](#overview)

Shopware 6 is fully extensible via plugins. Part of this extensibility is the usage of events, upon which one could react.

This guide will cover how you can find those events in the first place, in order to use them in your plugin.

## DAL Events [​](#dal-events)

At first we will start with the [Data Abstraction Layer events](./../data-handling/using-database-events.html). They're fired whenever a [DAL entity](./../data-handling/add-custom-complex-data.html) is read, written, created, or deleted.

There usually is no need to find them, since the pattern for them is always the same. You can use them by following this pattern: `entity_name.event`. For products, this could be e.g. `product.written` or `product.deleted`. For your custom entity, this then would be `custom_entity.written` or `custom_entity.deleted`.

However, some default Shopware entities come with special "Event classes", which are basically a class, which contains all possible kinds of events as constants. Have a look at the [product event class](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Product/ProductEvents.php) for example. This way you can also find out about all the possible DAL events available in Shopware.

Finding those "event classes" can be done by searching for the term `@Event` in your project.

You can use those events in a [subscriber](./../../plugin-fundamentals/listening-to-events.html) like the following:

php

```shiki
public static function getSubscribedEvents(): array
{
    return [
        ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded',
        'custom_entity.written' => 'onCustomEntityWritten'
    ];
}
```

As you can see, you can either use the event class constants, if available, or the string itself.

You'll then have access to several event specific information, e.g. your listener method will have access to an [EntityWrittenEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenEvent.php) instance when subscribing to the `written` event.

php

```shiki
public function onCustomEntityWritten(EntityWrittenEvent $event): void
{
}
```

You can find all of those DAL event classes [here](https://github.com/shopware/shopware/tree/v6.4.0.0/src/Core/Framework/DataAbstractionLayer/Event).

## General PHP events [​](#general-php-events)

If the [DAL events](#DAL events) didn't match your use case, there are a few more events built into Shopware. These are not auto-generated events, but rather events we built in with purpose.

There are multiple ways to find them:

* By actually looking at the code, that you want to extend
* By specifically searching for them
* By having a look at the service definition of a given class

### Looking at the code [​](#looking-at-the-code)

You will most likely look into our Core code quite a lot, while trying to understand what's happening and why things are happening. On your journey looking through the code, you may stumble upon code looking like this:

php

```shiki
$someEvent = new SomeEvent($parameters, $moreParameters);
$this->eventDispatcher->dispatch($someEvent, $someEvent->getName());
```

This is an event that's being fired manually, which you can react upon. Make sure to always have a look at the event class itself in order to find out which information it contains.

The second parameter of the `dispatch` is optional and represents the actual event's name. If the second parameter is not applied, the class name will be used as a fallback.

When subscribing to those events, your event listener method will have access to the previously created event instance.

php

```shiki
public static function getSubscribedEvents(): array
{
    return [
        'some_event' => 'registeringToSomeEvent',
        // If there is no name applied to the event, the class name is the fallback
        SomeEvent::class => 'registeringToSomeEvent'
    ];
}

public function registeringToSomeEvent(SomeEvent $event): void
{
}
```

The [next section](#Specifically searching for events) will cover how to find those events without randomly stumbling upon them.

### Specifically searching for events [​](#specifically-searching-for-events)

If you're really looking for a fitting event for your purpose, you might want to directly search for them. This can be done by searching through the `<shopware root>/platform/src` or the `<shopware root>/vendor/shopware/shopware/src` directory, depending on whether you are using the [development](https://github.com/shopwareArchive/development) or the [production template](https://github.com/shopware/template). Use one of the following search terms:

* `extends NestedEvent`: This way you will find the events themselves.
* `extends Event`: This way you will find the events themselves.
* `implements ShopwareEvent`: This way you will find the events themselves.
* `->dispatch`: Here you will find all the occurrences where the events are actually being fired.

### Looking at the service definition [​](#looking-at-the-service-definition)

Every service, that wants to fire an event sooner or later, needs access to the `event_dispatcher` in order to do so.

Hence, you can have a look at all the service definitions for the [Dependency injection container](./../../plugin-fundamentals/dependency-injection.html) and therefore quickly figure out, which services and classes are having access to the said `event_dispatcher`:

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Some\Service">
            <argument type="service" id="Another/Service"/>
            <argument type="service" id="event_dispatcher"/>
        </service>
    </services>
</container>
```

Therefore, you could simply search for occurrences of the `event_dispatcher` in the respective `.xml` files.

You can also do this the other way around, by having a look at the service's constructor parameters.

php

```shiki
public function __construct(
    Some\Service $someService,
    EventDispatcherInterface $eventDispatcher
) {
    $this->someService = $someService;
    $this->eventDispatcher = $eventDispatcher;
}
```

If it's having access to the `EventDispatcherInterface`, you're most likely going to find at least one event being fired in that service.

### Other common event types [​](#other-common-event-types)

There's a few more event "types" or classes that you may stumble upon, which are worth knowing.

#### Page Loaded Events [​](#page-loaded-events)

Usually when a [Storefront page](./../../storefront/add-custom-page.html) is being loaded, a respective "page is being loaded" event is fired as well.

You can find an example in the [GenericPageLoader](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Storefront/Page/GenericPageLoader.php), which is kinda a "default page" to be used pretty often. It dispatches an `GenericPageLoadedEvent` every time the page is being loaded.

This way, you can react to this and e.g. add more meta information to the said page.

You can find those events by searching for the term "PageLoadedEvent".

#### Criteria Events [​](#criteria-events)

You should be familiar with the `Criteria` class, at least if you've dealt with the [Data Abstraction Layer](./../data-handling/). There are many methods, that will dispatch a "criteria" event whenever a given default Shopware entity is being loaded using a `Criteria` instance.

Let's have a look at an [example code](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Product/SalesChannel/Listing/ResolveCriteriaProductListingRoute.php#L55-L59):

php

```shiki
#[Route(path: '/store-api/product-listing/{categoryId}', name: 'store-api.product.listing', methods: ['POST'], defaults: ['_entity' => 'product'])]
public function load(string $categoryId, Request $request, SalesChannelContext $context, Criteria $criteria): ProductListingRouteResponse
{
    $this->eventDispatcher->dispatch(
        new ProductListingCriteriaEvent($request, $criteria, $context)
    );

    return $this->getDecorated()->load($categoryId, $request, $context, $criteria);
}
```

So whenever the product listing route is being called, and therefore products are being loaded via the DAL and therefore via a `Criteria` object, the `ProductListingCriteriaEvent` is being fired.

You can use this event to modify the `Criteria` object and therefore add or remove conditions, add or remove associations etc. Of course, the code above is just one example excerpt and there are many more of those events for different entities.

Finding those events can be done by searching for the term `CriteriaEvent`.

INFO

Those "criteria events" are not generated automatically and therefore it is not guaranteed to exist for a given entity.

#### Route Events [​](#route-events)

Symfony provides some general [kernel level routing events](https://symfony.com/doc/current/reference/events.html#kernel-events), e.g `kernel.request` or `kernel.response`. However, those events are thrown on every route, so it's too generic when you only want to react on a specific route. Therefore, we have added fine-grained route events that are thrown for every route:

| Event name | Scope | Event Type | Description |
| --- | --- | --- | --- |
| `{route}.request` | Global | `Symfony\Component\HttpKernel\Event\RequestEvent` | Route specific alias for symfony's `kernel.request` event. |
| `{route}.response` | Global | `Symfony\Component\HttpKernel\Event\ResponseEvent` | Route specific alias for symfony's `kernel.response` event. For storefront routes this contains the already rendered template, for store-api routes this contains the already encoded JSON |
| `{route}.render` | Storefront | `Shopware\Storefront\Event\StorefrontRenderEvent` | Thrown before twig rendering in the storefront. |
| `{route}.encode` | Store-API | `Symfony\Component\HttpKernel\Event\ResponseEvent` | Thrown before encoding the API response to JSON, allowing easy manipulation of the returned data. **Note:** This was only introduced in 6.6.11.0 |
| `{route}.controller` | Global | `\Symfony\Component\HttpKernel\Event\ControllerEvent` | Route specific alias for symfony's `kernel.controller` event. **Note:** This was only introduced in 6.6.11.0 |

To subscribe to a specific event, replace the `{route}` placeholder with the [actual symfony route name](https://symfony.com/doc/current/routing.html), e.g. `store-api.product.listing`.

php

```shiki
public static function getSubscribedEvents(): array
{
    return [
        'store-api.product.listing.request' => 'onListingRequest',
        'store-api.product.listing.encode' => 'onListingEncode'
    ];
}

public function onListingRequest(RequestEvent $event): void
{
}

public function onListingEncode(ResponseEvent $event): void
{
}
```

#### Business events [​](#business-events)

Business events are fired everytime an important business / ecommerce action occurred, such as "A customer registered" or "An order was placed".

Therefore, you can use them to react on those events, most times there even is an event fired **before** an action happened. Have a look at those two example events:

* [CustomerBeforeLoginEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Checkout/Customer/SalesChannel/AccountService.php#L97-L98)
* [CustomerLoginEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Checkout/Customer/SalesChannel/AccountService.php#L109-L110)

The kind of information they contain and which you can modify is different for each event, so you'll have to have a look at the respective event classes to find out about it.

Those business events can be found by either searching for the term `implements BusinessEventInterface` or `implements MailActionInterface`. The latter implement the `MailActionInterface` because they're events which will result in a mail being sent, e.g. when a customer placed an order. Customer login however will obviously not result in a mail being sent and therefore is "only" implement the `BusinessEventInterface`.

### Using the Symfony profiler [​](#using-the-symfony-profiler)

Since Shopware is built upon the Symfony framework, it also grants access to the [Symfony profiler](https://symfony.com/doc/current/profiler.html).

Using the profiler, you can easily find all fired events in the current request. You can do so by opening up the profiler and clicking on the "Events" tab on the left.

![Profiler events](/assets/profiler-events.Bnxjh7QH.png)

There you will find all events that were fired in the current request including their respective name to be used.

## Storefront events [​](#storefront-events)

We're also making use of events in our Storefront javascript plugins. We've already covered Storefront events in this [guide](./../../storefront/reacting-to-javascript-events.html).

However, it's not really explaining how you can find them in the first place. For this case, we're using the same plain method like before: Simply searching for them or by looking through the code.

### Finding events in the code [​](#finding-events-in-the-code)

In the Storefront javascript plugins, you can notice custom events by the following pattern:

javascript

```shiki
this.$emitter.publish('someEvent', additionalData);
```

Therefore, you could subscribe to the event named `someEvent` and gain access to `additionalData` here.

javascript

```shiki
this.$emitter.subscribe('someEvent', (additionalData) => {
    // Do stuff
});
```

### Searching for javascript events [​](#searching-for-javascript-events)

Searching for the said javascript events is done by searching for the following term in either the `<shopware root>/platform/src/Storefront/Resources/app/storefront/src` directory for the [development template](https://github.com/shopwareArchive/development) or the `<shopware root>/vendor/shopware/shopware/src/Storefront/Resources/app/storefront/src` directory for the [production template](https://github.com/shopware/template): `$emitter.publish`. This way, you'll find all occurrences of plugins actually firing a custom event.

## Administration events [​](#administration-events)

In the Administration, most events you can find and deal with are default vue events, which you can learn about [here](https://vuejs.org/guide/essentials/event-handling.html).

However, for the sake of the two-way data-binding, we're sometimes firing events, which looks like this:

javascript

```shiki
this.$emit('some-event', additionalData);
```

Therefore you can also find those occurrences by searching for `$emit` in the `<shopware root>/platform/src/Administration/Resources/app/administration/src` directory for the [development template](https://github.com/shopwareArchive/development) or the `<shopware root>/vendor/shopware/shopware/src/Administration/Resources/app/administration/src` directory for the [production template](https://github.com/shopware/template).

### Vue extension [​](#vue-extension)

One more note here: There's a vue browser extension which can greatly help will development in general, but also with finding events.

[Vue.js devtools for Firefox](https://addons.mozilla.org/de/firefox/addon/vue-js-devtools/)[Vue.js devtools for Google Chrome](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)

## Flow builder events [​](#flow-builder-events)

From Shopware 6.5, all events data in the Flow Builder will be stored in the `StorableFlow`, hence the `getAvailableData` function can no more be used to get data from the Flow Builder. For more information on this refer to [Create a new trigger (event)](./../../../../../guides/plugins/plugins/framework/flow/add-flow-builder-trigger.html#create-a-new-trigger-event) section of this guide.

---

## Extension Points

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/

# Extension Points [​](#extension-points)

Extension Points allow you to **replace core functionality** by intercepting and modifying the execution flow of system processes, unlike traditional events which are only for notifications.

---

## Finding Extension Points

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/finding-extensions.html

# Finding Extension Points [​](#finding-extension-points)

## Overview [​](#overview)

Shopware 6 provides a modern extension system that allows you to intercept and modify core functionality. Unlike traditional events that are primarily for notifications, Extension Points are designed for **replacing and extending** core system processes.

This guide will cover how you can find available Extension Points in the Shopware codebase to use them in your plugin.

## Extension Classes [​](#extension-classes)

Extension Points in Shopware extend the base `Extension` class and are typically located in domain-specific directories. They follow a consistent naming pattern and structure.

### Finding Extension Classes [​](#finding-extension-classes)

You can find Extension classes by searching for the following patterns in the Shopware source code:

#### Search Terms [​](#search-terms)

* `extends Extension`: Find all Extension classes
* `Extension<`: Find typed Extension Points with specific return types
* `ExtensionDispatcher`: Find where Extension Points are dispatched

#### Common Locations [​](#common-locations)

Extension Points are typically located in:

* `src/Core/Content/*/Extension/`
* `src/Core/Checkout/*/Extension/`
* `src/Core/Content/Cms/Extension/`
* `src/Core/Content/Product/Extension/`

### Example Extension Classes [​](#example-extension-classes)

Here are some common Extension Point you might encounter:

#### Product Extensions [​](#product-extensions)

php

```shiki
// Product price calculation
src/Core/Content/Product/Extension/ProductPriceCalculationExtension.php

// Product listing resolution
src/Core/Content/Product/Extension/ResolveListingExtension.php

// Product listing criteria modification
src/Core/Content/Product/Extension/ProductListingCriteriaExtension.php
```

#### Cart Extensions [​](#cart-extensions)

php

```shiki
// Checkout place order
src/Core/Checkout/Cart/Extension/CheckoutPlaceOrderExtension.php

// Cart rule loading
src/Core/Checkout/Cart/Extension/CheckoutCartRuleLoaderExtension.php
```

#### CMS Extensions [​](#cms-extensions)

php

```shiki
// CMS slots data enrichment
src/Core/Content/Cms/Extension/CmsSlotsDataEnrichExtension.php

// CMS slots data resolution
src/Core/Content/Cms/Extension/CmsSlotsDataResolveExtension.php
```

## Extension Naming Convention [​](#extension-naming-convention)

Extension Points follow a consistent naming pattern:

### Event Names [​](#event-names)

Extension Points use a `NAME` constant that defines the event name:

php

```shiki
final class ResolveListingExtension extends Extension
{
    public const NAME = 'listing-loader.resolve';
    
    // ...
}
```

### Event Lifecycle [​](#event-lifecycle)

Extension Points are dispatched with lifecycle suffixes:

* `{name}.pre` - Before the default implementation
* `{name}.post` - After the default implementation
* `{name}.error` - When an error occurs

## Finding Extension Usage [​](#finding-extension-usage)

### In Service Definitions [​](#in-service-definitions)

Services that use Extension Points typically inject the `ExtensionDispatcher`:

xml

```shiki
<service id="Some\Service">
    <argument type="service" id="Shopware\Core\Framework\Extensions\ExtensionDispatcher"/>
</service>
```

### In Constructor Parameters [​](#in-constructor-parameters)

Look for services that inject the `ExtensionDispatcher`:

php

```shiki
public function __construct(
    private readonly ExtensionDispatcher $extensionDispatcher
) {
}
```

### Extension Dispatch Pattern [​](#extension-dispatch-pattern)

Extension Points are typically dispatched using this pattern:

php

```shiki
$extension = new SomeExtension($parameters);
$result = $this->extensionDispatcher->publish(
    SomeExtension::NAME,
    $extension,
    function() use ($parameters) {
        // Default implementation
        return $this->defaultImplementation($parameters);
    }
);
```

## Common Extension Types [​](#common-extension-types)

### Product Extensions [​](#product-extensions-1)

#### ProductPriceCalculationExtension [​](#productpricecalculationextension)

**Purpose**: Intercept and modify product price calculations **Event Name**: `product.calculate-prices`**Return Type**: `void`

php

```shiki
final class ProductPriceCalculationExtension extends Extension
{
    public const NAME = 'product.calculate-prices';
    
    public function __construct(
        public readonly iterable $products,
        public readonly SalesChannelContext $context
    ) {}
}
```

#### ResolveListingExtension [​](#resolvelistingextension)

**Purpose**: Replace product listing resolution logic **Event Name**: `listing-loader.resolve`**Return Type**: `EntitySearchResult<ProductCollection>`

php

```shiki
final class ResolveListingExtension extends Extension
{
    public const NAME = 'listing-loader.resolve';
    
    public function __construct(
        public readonly Criteria $criteria,
        public readonly SalesChannelContext $context
    ) {}
}
```

### Cart Extensions [​](#cart-extensions-1)

#### CheckoutPlaceOrderExtension [​](#checkoutplaceorderextension)

**Purpose**: Intercept order placement process **Event Name**: `checkout.place-order`**Return Type**: `OrderPlaceResult`

php

```shiki
final class CheckoutPlaceOrderExtension extends Extension
{
    public const NAME = 'checkout.place-order';
    
    public function __construct(
        public readonly Cart $cart,
        public readonly SalesChannelContext $context
    ) {}
}
```

### CMS Extensions [​](#cms-extensions-1)

#### CmsSlotsDataEnrichExtension [​](#cmsslotsdataenrichextension)

**Purpose**: Enrich CMS slot data before rendering **Event Name**: `cms.slots.data-enrich`**Return Type**: `CmsSlotCollection`

php

```shiki
final class CmsSlotsDataEnrichExtension extends Extension
{
    public const NAME = 'cms.slots.data-enrich';
    
    public function __construct(
        public readonly CmsSlotCollection $slots,
        public readonly SalesChannelContext $context
    ) {}
}
```

## Using Extensions in Your Plugin [​](#using-extensions-in-your-plugin)

### Event Subscriber [​](#event-subscriber)

Create an event subscriber to listen for Extension Points:

php

```shiki
<?php declare(strict_types=1);

namespace MyPlugin\Subscriber;

use Shopware\Core\Content\Product\Extension\ResolveListingExtension;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ProductListingSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            'listing-loader.resolve.pre' => 'onResolveListing',
        ];
    }
    
    public function onResolveListing(ResolveListingExtension $event): void
    {
        // Custom logic here
        $event->result = $this->customProductLoader->load($event->criteria, $event->context);
        $event->stopPropagation();
    }
}
```

### Service Registration [​](#service-registration)

Register your subscriber in the service configuration:

xml

```shiki
<service id="MyPlugin\Subscriber\ProductListingSubscriber">
    <tag name="kernel.event_subscriber"/>
</service>
```

## Extension Lifecycle [​](#extension-lifecycle)

Extension Points follow a specific lifecycle:

1. **Pre-Event**: `{name}.pre` - Before default implementation
2. **Default Implementation**: Core logic (if not stopped)
3. **Post-Event**: `{name}.post` - After implementation
4. **Error-Event**: `{name}.error` - If an error occurs

### Lifecycle Example [​](#lifecycle-example)

php

```shiki
public function handleExtension(SomeExtension $event): void
{
    // This runs in the .pre phase
    if ($this->shouldReplaceDefault($event)) {
        $event->result = $this->customImplementation($event);
        $event->stopPropagation(); // Prevents default implementation
    }
}

public function handlePostExtension(SomeExtension $event): void
{
    // This runs in the .post phase
    $this->logger->info('Extension completed', ['result' => $event->result]);
}
```

## Best Practices [​](#best-practices)

### 1. Use Type Hints [​](#_1-use-type-hints)

Always use proper type hints for Extension Point parameters:

php

```shiki
public function onResolveListing(ResolveListingExtension $event): void
{
    // Type-safe access to properties
    $criteria = $event->criteria;
    $context = $event->context;
}
```

### 2. Handle Results Properly [​](#_2-handle-results-properly)

Check if a result has already been set:

php

```shiki
public function onExtension(SomeExtension $event): void
{
    if ($event->result !== null) {
        // Another extension already provided a result
        return;
    }
    
    $event->result = $this->myImplementation($event);
}
```

### 3. Use Stop Propagation Wisely [​](#_3-use-stop-propagation-wisely)

Only stop propagation when you're providing a complete replacement:

php

```shiki
public function onExtension(SomeExtension $event): void
{
    if ($this->shouldReplaceDefault($event)) {
        $event->result = $this->completeReplacement($event);
        $event->stopPropagation();
    }
    // If not stopped, default behavior continues
}
```

### 4. Error Handling [​](#_4-error-handling)

Extension Points have built-in error handling, but you can also handle errors gracefully:

php

```shiki
public function onExtension(SomeExtension $event): void
{
    try {
        $event->result = $this->riskyOperation($event);
    } catch (\Exception $e) {
        // Log the error but don't stop the extension
        $this->logger->error('Extension failed', ['error' => $e->getMessage()]);
        // Let the extension system handle the error
    }
}
```

## Debugging Extensions [​](#debugging-extensions)

### Using the Symfony Profiler [​](#using-the-symfony-profiler)

The Symfony profiler shows all dispatched Extension Points in the "Events" tab. Look for events with `.pre`, `.post`, or `.error` suffixes.

### Logging Extension Calls [​](#logging-extension-calls)

You can log Extension Point calls to understand the flow:

php

```shiki
public function onExtension(SomeExtension $event): void
{
    $this->logger->debug('Extension called', [
        'extension' => get_class($event),
        'hasResult' => $event->result !== null,
        'stopped' => $event->isPropagationStopped()
    ]);
}
```

This comprehensive guide should help you find and use Extension Points effectively in your Shopware plugins.

---

## Creating Custom Extension Points

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/creating-custom-extension.html

# Creating Custom Extension Points [​](#creating-custom-extension-points)

## Overview [​](#overview)

While Shopware provides many built-in extension points, you may need to create custom extension points for your specific use cases. This guide will walk you through creating custom extension points that follow Shopware's extension system patterns.

## Extension Class Structure [​](#extension-class-structure)

### Basic Extension Class [​](#basic-extension-class)

All extension points must extend the base `Extension` class and define a typed result:

php

```shiki
<?php declare(strict_types=1);

namespace MyPlugin\Extension;

use Shopware\Core\Framework\Extensions\Extension;
use Shopware\Core\Framework\Log\Package;

/**
 * @extends Extension<MyResultType>
 */
#[Package('my-plugin')]
final class MyCustomExtension extends Extension
{
    public const NAME = 'my-plugin.custom-extension';
    
    public function __construct(
        /**
         * @public
         * @description Input data for processing
         */
        public readonly array $inputData,
        
        /**
         * @public
         * @description Context for the operation
         */
        public readonly Context $context
    ) {
    }
}
```

### Key Components [​](#key-components)

1. **Generic Type**: `@extends Extension<ResultType>` defines the return type
2. **NAME Constant**: Unique identifier for the extension
3. **Public Properties**: Input parameters marked with `@public` for API documentation
4. **Package Attribute**: Identifies the package/plugin

## Example: Custom Product Filter Extension [​](#example-custom-product-filter-extension)

Let's create a custom extension point for filtering products based on custom business logic:

### 1. Define the Extension Class [​](#_1-define-the-extension-class)

php

```shiki
<?php declare(strict_types=1);

namespace MyPlugin\Extension;

use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\Framework\Extensions\Extension;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

/**
 * @extends Extension<EntitySearchResult<ProductCollection>>
 */
#[Package('my-plugin')]
final class CustomProductFilterExtension extends Extension
{
    public const NAME = 'my-plugin.product-filter';
    
    public function __construct(
        /**
         * @public
         * @description The search criteria for products
         */
        public readonly Criteria $criteria,
        
        /**
         * @public
         * @description The sales channel context
         */
        public readonly SalesChannelContext $context,
        
        /**
         * @public
         * @description Custom filter parameters
         */
        public readonly array $filterParams
    ) {
    }
}
```

### 2. Create the Service that Dispatches the Extension [​](#_2-create-the-service-that-dispatches-the-extension)

php

```shiki
<?php declare(strict_types=1);

namespace MyPlugin\Service;

use MyPlugin\Extension\CustomProductFilterExtension;
use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\Framework\Extensions\ExtensionDispatcher;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

#[Package('my-plugin')]
class CustomProductService
{
    public function __construct(
        private readonly ExtensionDispatcher $extensionDispatcher,
        private readonly EntityRepository $productRepository
    ) {
    }
    
    public function filterProducts(
        Criteria $criteria,
        SalesChannelContext $context,
        array $filterParams = []
    ): EntitySearchResult {
        $extension = new CustomProductFilterExtension(
            $criteria,
            $context,
            $filterParams
        );
        
        return $this->extensionDispatcher->publish(
            CustomProductFilterExtension::NAME,
            $extension,
            function() use ($criteria, $context) {
                // Default implementation
                return $this->productRepository->search($criteria, $context->getContext());
            }
        );
    }
}
```

### 3. Create an Event Subscriber [​](#_3-create-an-event-subscriber)

php

```shiki
<?php declare(strict_types=1);

namespace MyPlugin\Subscriber;

use MyPlugin\Extension\CustomProductFilterExtension;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class CustomProductFilterSubscriber implements EventSubscriberInterface
{
    public function __construct(
        private readonly ExternalApiService $apiService,
        private readonly ProductFilterService $filterService
    ) {
    }
    
    public static function getSubscribedEvents(): array
    {
        return [
            'my-plugin.product-filter.pre' => 'onProductFilter',
        ];
    }
    
    public function onProductFilter(CustomProductFilterExtension $event): void
    {
        // Check if we should apply custom filtering
        if (!$this->shouldApplyCustomFilter($event->filterParams)) {
            return;
        }
        
        // Get filtered product IDs from external API
        $filteredIds = $this->apiService->getFilteredProductIds(
            $event->criteria,
            $event->context,
            $event->filterParams
        );
        
        if (empty($filteredIds)) {
            // No products match the filter
            $event->result = new EntitySearchResult(
                'product',
                0,
                new ProductCollection(),
                null,
                $event->criteria,
                $event->context->getContext()
            );
            $event->stopPropagation();
            return;
        }
        
        // Create new criteria with filtered IDs
        $newCriteria = clone $event->criteria;
        $newCriteria->setIds($filteredIds);
        
        // Apply additional filtering
        $filteredProducts = $this->filterService->applyBusinessRules(
            $newCriteria,
            $event->context
        );
        
        $event->result = $filteredProducts;
        $event->stopPropagation();
    }
    
    private function shouldApplyCustomFilter(array $filterParams): bool
    {
        return isset($filterParams['custom_filter']) && $filterParams['custom_filter'] === true;
    }
}
```

### 4. Register Services [​](#_4-register-services)

xml

```shiki
<!-- services.xml -->
<service id="MyPlugin\Service\CustomProductService">
    <argument type="service" id="Shopware\Core\Framework\Extensions\ExtensionDispatcher"/>
    <argument type="service" id="product.repository"/>
</service>

<service id="MyPlugin\Subscriber\CustomProductFilterSubscriber">
    <argument type="service" id="MyPlugin\Service\ExternalApiService"/>
    <argument type="service" id="MyPlugin\Service\ProductFilterService"/>
    <tag name="kernel.event_subscriber"/>
</service>
```

## Advanced Extension Patterns [​](#advanced-extension-patterns)

### 1. Conditional Extension Execution [​](#_1-conditional-extension-execution)

php

```shiki
public function onExtension(MyExtension $event): void
{
    // Only execute under certain conditions
    if (!$this->shouldExecute($event)) {
        return;
    }
    
    $event->result = $this->customImplementation($event);
    $event->stopPropagation();
}

private function shouldExecute(MyExtension $event): bool
{
    return $event->context->getSalesChannelId() === 'special-sales-channel';
}
```

### 2. Extension with Error Handling [​](#_2-extension-with-error-handling)

php

```shiki
public function onExtension(MyExtension $event): void
{
    try {
        $event->result = $this->riskyOperation($event);
        $event->stopPropagation();
    } catch (\Exception $e) {
        // Log the error but don't stop the extension
        $this->logger->error('Custom extension failed', [
            'error' => $e->getMessage(),
            'extension' => get_class($event)
        ]);
        
        // The extension system will handle the error
        // and potentially dispatch error events
    }
}
```

### 3. Extension with Data Enrichment [​](#_3-extension-with-data-enrichment)

php

```shiki
public function onExtension(MyExtension $event): void
{
    // Don't replace the result, just enrich it
    if ($event->result !== null) {
        $enrichedResult = $this->enrichResult($event->result, $event);
        $event->result = $enrichedResult;
    }
}

private function enrichResult($result, MyExtension $event)
{
    // Add custom data to the result
    $result->addExtension('customData', new CustomStruct([
        'processedAt' => new \DateTime(),
        'context' => $event->context->getSalesChannelId()
    ]));
    
    return $result;
}
```

### 4. Multi-Phase Extension [​](#_4-multi-phase-extension)

php

```shiki
public static function getSubscribedEvents(): array
{
    return [
        'my-extension.pre' => 'onPrePhase',
        'my-extension.post' => 'onPostPhase',
        'my-extension.error' => 'onErrorPhase',
    ];
}

public function onPrePhase(MyExtension $event): void
{
    // Prepare data before default implementation
    $event->addExtension('preparedData', $this->prepareData($event));
}

public function onPostPhase(MyExtension $event): void
{
    // Process result after default implementation
    if ($event->result !== null) {
        $event->result = $this->postProcess($event->result, $event);
    }
}

public function onErrorPhase(MyExtension $event): void
{
    // Handle errors gracefully
    if ($event->exception !== null) {
        $event->result = $this->fallbackImplementation($event);
    }
}
```

## Extension Lifecycle Management [​](#extension-lifecycle-management)

### Pre-Phase Extensions [​](#pre-phase-extensions)

Use `.pre` events to:

* Validate input data
* Modify criteria or parameters
* Replace default implementation entirely

### Post-Phase Extensions [​](#post-phase-extensions)

Use `.post` events to:

* Enrich results
* Log completion
* Trigger follow-up actions

### Error-Phase Extensions [​](#error-phase-extensions)

Use `.error` events to:

* Provide fallback implementations
* Log errors
* Recover from failures

## Best Practices [​](#best-practices)

### 1. Naming Conventions [​](#_1-naming-conventions)

* Use descriptive, domain-specific names
* Follow the pattern: `{plugin}.{domain}.{action}`
* Use kebab-case for event names

### 2. Type Safety [​](#_2-type-safety)

* Always define generic types for extension points
* Use proper type hints for parameters
* Validate input data in constructors

### 3. Documentation [​](#_3-documentation)

* Document all public properties with `@public` and `@description`
* Provide clear examples in docblocks
* Include usage examples in plugin documentation

### 4. Error Handling [​](#_4-error-handling)

* Use try-catch blocks for risky operations
* Provide meaningful error messages
* Consider fallback implementations

### 5. Performance [​](#_5-performance)

* Avoid expensive operations in Extensions
* Cache results when appropriate
* Use lazy loading for heavy dependencies

### 6. Testing [​](#_6-testing)

* Write unit tests for extension point classes
* Test event subscribers thoroughly
* Mock external dependencies

## Example: Complete Plugin with Custom Extension Point [​](#example-complete-plugin-with-custom-extension-point)

Here's a complete example of a plugin that creates and uses a custom extension point:

php

```shiki
// 1. Extension class
final class ProductRecommendationExtension extends Extension
{
    public const NAME = 'my-plugin.product-recommendation';
    
    public function __construct(
        public readonly ProductEntity $product,
        public readonly SalesChannelContext $context,
        public readonly int $limit = 5
    ) {}
}

// 2. Service that uses the extension
class ProductRecommendationService
{
    public function getRecommendations(ProductEntity $product, SalesChannelContext $context): ProductCollection
    {
        $extension = new ProductRecommendationExtension($product, $context);
        
        return $this->extensionDispatcher->publish(
            ProductRecommendationExtension::NAME,
            $extension,
            function() use ($product, $context) {
                // Default recommendation logic
                return $this->getDefaultRecommendations($product, $context);
            }
        );
    }
}

// 3. Subscriber that provides custom logic
class ProductRecommendationSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            'my-plugin.product-recommendation.pre' => 'onGetRecommendations',
        ];
    }
    
    public function onGetRecommendations(ProductRecommendationExtension $event): void
    {
        // Custom AI-powered recommendations
        $recommendations = $this->aiService->getRecommendations(
            $event->product,
            $event->context,
            $event->limit
        );
        
        $event->result = $recommendations;
        $event->stopPropagation();
    }
}
```

This comprehensive guide should help you create custom extension points that integrate seamlessly with Shopware's extension system.

---

## Extension Points vs Events

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/extension-vs-events.html

# Extension Points vs Events [​](#extension-points-vs-events)

## Overview [​](#overview)

Shopware 6 provides two different mechanisms for extending functionality: **Extension Points** and **Events**. While they may seem similar, they serve different purposes and have distinct characteristics. Understanding when to use each approach is crucial for effective plugin development.

## Key Differences [​](#key-differences)

### Purpose and Design Philosophy [​](#purpose-and-design-philosophy)

#### Extension Points [​](#extension-points)

* **Purpose**: Replace or extend core functionality
* **Design**: Result-oriented, flow-controlling
* **Philosophy**: "I want to change how this works"

#### Events [​](#events)

* **Purpose**: Notify about actions that occurred
* **Design**: Notification-based, fire-and-forget
* **Philosophy**: "I want to know when this happens"

### Return Values and Flow Control [​](#return-values-and-flow-control)

#### Extension Points [​](#extension-points-1)

php

```shiki
public function onResolveListing(ResolveListingExtension $event): void
{
    // Can return a result that replaces the default behavior
    $event->result = $this->customProductLoader->load($event->criteria, $event->context);
    
    // Can stop the default implementation
    $event->stopPropagation();
}
```

#### Events [​](#events-1)

php

```shiki
public function onProductCreated(ProductCreatedEvent $event): void
{
    // Cannot return values or control flow
    // Can only perform side effects
    $this->logger->info('Product created: ' . $event->getProduct()->getName());
    $this->notificationService->sendNotification($event->getProduct());
}
```

### Execution Timing [​](#execution-timing)

#### Extension Points [​](#extension-points-2)

* **Timing**: Before or during the action
* **Purpose**: Intercept and modify the process
* **Example**: Before product prices are calculated

#### Events [​](#events-2)

* **Timing**: After the action is completed
* **Purpose**: React to completed actions
* **Example**: After a product has been created

### Error Handling [​](#error-handling)

#### Extension Points [​](#extension-points-3)

php

```shiki
// Built-in error handling with recovery
try {
    $extension->result = $function(...$extension->getParams());
} catch (\Throwable $e) {
    $extension->exception = $e;
    $extension->resetPropagation();
    
    // Dispatch error event for recovery
    $this->dispatcher->dispatch($extension, self::error($name));
    
    // If no recovery, rethrow
    if ($extension->result === null) {
        throw $e;
    }
}
```

#### Events [​](#events-3)

php

```shiki
// Basic error handling
public function onProductCreated(ProductCreatedEvent $event): void
{
    try {
        $this->performSideEffect($event);
    } catch (\Exception $e) {
        // Error handling is up to the developer
        $this->logger->error('Failed to process product creation', ['error' => $e->getMessage()]);
    }
}
```

## When to Use Extension Points [​](#when-to-use-extension-points)

Use Extension Points when you need to:

### 1. Replace Core Functionality [​](#_1-replace-core-functionality)

php

```shiki
// Replace default product loading with custom logic
public function onResolveListing(ResolveListingExtension $event): void
{
    $event->result = $this->externalProductService->loadProducts($event->criteria);
    $event->stopPropagation();
}
```

### 2. Modify Data Before Processing [​](#_2-modify-data-before-processing)

php

```shiki
// Filter products before they're displayed
public function onProductListing(ProductListingExtension $event): void
{
    $filteredProducts = $this->filterProducts($event->products, $event->context);
    $event->result = $filteredProducts;
    $event->stopPropagation();
}
```

### 3. Integrate External Systems [​](#_3-integrate-external-systems)

php

```shiki
// Use external pricing service
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    $prices = $this->externalPricingService->calculatePrices($event->products);
    $event->result = $prices;
    $event->stopPropagation();
}
```

### 4. Add Conditional Business Logic [​](#_4-add-conditional-business-logic)

php

```shiki
// Apply special pricing for VIP customers
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    if ($this->isVipCustomer($event->context)) {
        $event->result = $this->applyVipPricing($event->products);
        $event->stopPropagation();
    }
}
```

## When to Use Events [​](#when-to-use-events)

Use Events when you need to:

### 1. Send Notifications [​](#_1-send-notifications)

php

```shiki
public function onOrderPlaced(OrderPlacedEvent $event): void
{
    $this->emailService->sendOrderConfirmation($event->getOrder());
    $this->smsService->sendOrderNotification($event->getOrder());
}
```

### 2. Log Actions [​](#_2-log-actions)

php

```shiki
public function onProductCreated(ProductCreatedEvent $event): void
{
    $this->auditLogger->log('Product created', [
        'productId' => $event->getProduct()->getId(),
        'userId' => $event->getContext()->getUserId()
    ]);
}
```

### 3. Update External Systems [​](#_3-update-external-systems)

php

```shiki
public function onCustomerRegistered(CustomerRegisteredEvent $event): void
{
    $this->crmService->syncCustomer($event->getCustomer());
    $this->analyticsService->trackRegistration($event->getCustomer());
}
```

### 4. Trigger Follow-up Actions [​](#_4-trigger-follow-up-actions)

php

```shiki
public function onOrderCompleted(OrderCompletedEvent $event): void
{
    $this->inventoryService->reserveStock($event->getOrder());
    $this->shippingService->schedulePickup($event->getOrder());
}
```

## Comparison Table [​](#comparison-table)

| Aspect | Extension Points | Events |
| --- | --- | --- |
| **Purpose** | Replace/Extend functionality | Notify about actions |
| **Return Values** | Yes (via `result` property) | No |
| **Flow Control** | Yes (via `stopPropagation()`) | No |
| **Error Handling** | Advanced with recovery | Basic |
| **Timing** | Pre/during action | Post-action |
| **Use Case** | Core functionality | Side effects |
| **Performance Impact** | Can be significant | Usually minimal |
| **Complexity** | Higher | Lower |
| **Backward Compatibility** | Easier to maintain | More complex |

## Real-World Examples [​](#real-world-examples)

### E-commerce Scenarios [​](#e-commerce-scenarios)

#### Product Pricing (Extension Point) [​](#product-pricing-extension-point)

php

```shiki
// Replace default pricing with dynamic pricing from external API
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    $dynamicPrices = $this->pricingApi->getPrices($event->products, $event->context);
    $event->result = $dynamicPrices;
    $event->stopPropagation();
}
```

#### Order Notification (Event) [​](#order-notification-event)

php

```shiki
// Send notifications after an order is placed
public function onOrderPlaced(OrderPlacedEvent $event): void
{
    $this->emailService->sendOrderConfirmation($event->getOrder());
    $this->slackService->notifyTeam($event->getOrder());
}
```

#### Product Search (Extension Point) [​](#product-search-extension-point)

php

```shiki
// Replace default search with AI-powered search
public function onProductSearch(ProductSearchExtension $event): void
{
    $aiResults = $this->aiSearchService->search($event->query, $event->context);
    $event->result = $aiResults;
    $event->stopPropagation();
}
```

#### Inventory Update (Event) [​](#inventory-update-event)

php

```shiki
// Update an external inventory system after a product update
public function onProductUpdated(ProductUpdatedEvent $event): void
{
    $this->inventoryService->syncProduct($event->getProduct());
}
```

## Migration from Events to Extension Points [​](#migration-from-events-to-extension-points)

If you're currently using Events for functionality replacement, consider migrating to Extension Points:

### Before (Event-based) [​](#before-event-based)

php

```shiki
// Old approach - using events for functionality replacement
public function onProductListingCriteria(ProductListingCriteriaEvent $event): void
{
    // Modify criteria
    $event->getCriteria()->addFilter(new EqualsFilter('active', true));
}

public function onProductLoaded(ProductLoadedEvent $event): void
{
    // Post-process products
    foreach ($event->getProducts() as $product) {
        $product->addExtension('customData', $this->getCustomData($product));
    }
}
```

### After (Extension Point-based) [​](#after-extension-point-based)

php

```shiki
// New approach - using extension points for functionality replacement
public function onResolveListing(ResolveListingExtension $event): void
{
    // Replace entire listing resolution
    $event->result = $this->customListingService->resolve($event->criteria, $event->context);
    $event->stopPropagation();
}
```

## Best Practices [​](#best-practices)

### For Extension Points [​](#for-extension-points)

1. **Use sparingly**: Only when you need to replace core functionality
2. **Handle errors gracefully**: Provide fallback implementations
3. **Document thoroughly**: Extension points are part of the public API
4. **Test extensively**: Extension points can break core functionality
5. **Consider performance**: Extension points can impact performance significantly

### For Events [​](#for-events)

1. **Keep side effects minimal**: Don't perform heavy operations
2. **Handle errors gracefully**: Don't let event failures break the main flow
3. **Use async processing**: For heavy operations, use message queues
4. **Document side effects**: Make it clear what the event does
5. **Test in isolation**: Events should be testable independently

---

## Message Queue

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/message-queue/

# Message Queue [​](#message-queue)

The Shopware message queue manages the asynchronous processing of tasks using a message handler, message queue, and middleware, ensuring reliable and efficient execution of background processes within the e-commerce platform. Possible tasks are sending emails, indexing products, or generating the sitemap.

---

## Add message to queue

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/message-queue/add-message-to-queue.html

# Add message to queue [​](#add-message-to-queue)

## Overview [​](#overview)

WARNING

Parts of this guide refer to the `low_priority` queue and the corresponding `LowPriorityMessageInterface`, which is only available in version 6.5.7.0 and above. Configuring the messenger to consume this queue will fail if it does not exist.

In this guide you'll learn how to create a message and add it to the queue.

Shopware integrates with the [Symfony Messenger](https://symfony.com/doc/current/components/messenger.html) component and [Enqueue](https://enqueue.forma-pro.com/). This gives you the possibility to send and handle asynchronous messages.

A [message](https://symfony.com/doc/current/messenger.html#creating-a-message-handler) is a simple PHP object that you want to dispatch over the MessageQueue. It must be serializable and should contain all necessary information that your handlers need to process the message.

It will be wrapped in an [envelope](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes) by the message bus that dispatches the message.

## Prerequisites [​](#prerequisites)

As most guides, this guide is also built upon the [Plugin base guide](./../../plugin-base-guide.html), but you don't necessarily need that. It will use an example service, so if you don't know how to add a custom service yet, have a look at our guide about [Adding a custom service](./../../plugin-fundamentals/add-custom-service.html). Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](./../../plugin-fundamentals/dependency-injection.html), so having this open in another tab won't hurt.

## Create a message [​](#create-a-message)

First, we have to create a new message class in the directory `<plugin root>/MessageQueue/Message`. In this example, we create a `SmsNotification` that contains a string with content. By default, all messages are handled synchronously. To change the behavior to asynchronously, we have to implement the `AsyncMessageInterface` interface. For messages which should also be handled asynchronously but with a lower priority, implement the `LowPriorityMessageInterface` interface.

Here's an example:

php

```shiki
// <plugin root>/src/MessageQueue/Message/SmsNotification.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Message;

use Shopware\Core\Framework\MessageQueue\AsyncMessageInterface;

class SmsNotification implements AsyncMessageInterface
{
    private string $content;

    public function __construct(string $content)
    {
        $this->content = $content;
    }

    public function getContent(): string
    {
        return $this->content;
    }
}
```

## Send a message [​](#send-a-message)

After we've created our notification, we will create a service that will send our `SmsNotification`. We will name this service `ExampleSender`. In this service we need to inject the `Symfony\Component\Messenger\MessageBusInterface`, that is needed to send the message through the desired bus, which is called `messenger.default_bus`.

php

```shiki
// <plugin root>/src/Service/ExampleSender.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Swag\BasicExample\MessageQueue\Message\SmsNotification;
use Symfony\Component\Messenger\MessageBusInterface;

class ExampleSender
{
    private MessageBusInterface $bus;

    public function __construct(MessageBusInterface $bus)
    {
        $this->bus = $bus;
    }

    public function sendMessage(string $message): void
    {
        $this->bus->dispatch(new SmsNotification($message));
    }
}
```

If we want to add metadata to our message, we can dispatch an `Symfony\Component\Messenger\Envelope` in our service instead with the necessary [stamps](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes). In this example below, we use the `Symfony\Component\Messenger\Stamp\DelayStamp`, which tells the queue to process the message later.

php

```shiki
// <plugin root>/src/Service/ExampleSender.php
public function sendMessage(string $message): void
{
    $message = new SmsNotification($message);
    $this->bus->dispatch(
        (new Envelope($message))
            ->with(new DelayStamp(5000))
    );
}
```

## Lower the priority for specific async messages [​](#lower-the-priority-for-specific-async-messages)

You might consider using the new `low_priority` queue if you are dispatching messages that do not need to be handled immediately. To configure specific messages to be transported via the `low_priority` queue, you need to either adjust the routing or implement the `LowPriorityMessageInterface` as already mentioned:

yaml

```shiki
# config/packages/shopware.yaml
shopware:
    messenger:
        routing_overwrite:
            'Your\Custom\Message': low_priority
```

## Override transport for specific messages [​](#override-transport-for-specific-messages)

If you explicitly configure a message to be transported via the `async` (default) queue, even though it implements the `LowPriorityMessageInterface`, which would usually be transported via the `low_priority` queue, the transport is overridden for this specific message.

Example:

php

```shiki
// <plugin root>/src/MessageQueue/Message/LowPriorityMessage.php
<?php declare(strict_types=1);

namespace Your\Custom;

use Shopware\Core\Framework\MessageQueue\LowPriorityMessageInterface;

class LowPriorityMessage implements LowPriorityMessageInterface
{
}
```

yaml

```shiki
# config/packages/shopware.yaml
shopware:
    messenger:
        routing_overwrite:
            'Shopware\Core\Framework\MessageQueue\LowPriorityMessageInterface': low_priority
            'Your\Custom\LowPriorityMessage': async
```

## Next steps [​](#next-steps)

Now that you know how to create a message and add it to the queue, let's create a handler to process our message. To do this, head over to [Add message handler](./add-message-handler.html) guide.

---

## Add message handler

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/message-queue/add-message-handler.html

# Add message handler [​](#add-message-handler)

## Overview [​](#overview)

WARNING

Parts of this guide refer to the `low_priority` queue, which is only available in version 6.5.7.0 and above. Configuring the messenger to consume this queue will fail if it does not exist.

In this guide you'll learn how to create a message handler.

A [handler](https://symfony.com/doc/current/messenger.html#creating-a-message-handler) gets called once the message is dispatched by the `handle_messages` middleware. Handlers do the actual processing of the message.

## Prerequisites [​](#prerequisites)

As most guides, this guide is also built upon the [Plugin base guide](./../../plugin-base-guide.html), but you don't necessarily need that. It will use an example message, so if you don't know how to add a custom message yet, have a look at our guide about [Adding a message to queue](./add-message-to-queue.html). Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](./../../plugin-fundamentals/dependency-injection.html), so having this open in another tab won't hurt.

## Handling messages [​](#handling-messages)

First, we have to create a new class which we will name `SmsHandler` in this example. To mark the class as message handler, we use the php attribute `#[AsMessageHandler]` and implement the method `__invoke`. We can also define multiple handlers for the same message. To register a handler, we have to tag it with the `messenger.message_handler` tag.

php

```shiki
// <plugin root>/src/MessageQueue/Handler/SmsHandler.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Handler;

use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Swag\BasicExample\MessageQueue\Message\SmsNotification;

#[AsMessageHandler]
class SmsHandler
{
    public function __invoke(SmsNotification $message)
    {
        // ... do some work - like sending an SMS message!
    }
}
```

## Next steps [​](#next-steps)

Now that you know how to add a message handler, you may want to add a custom middleware for your bus. To do this, head over to [Add middleware](./add-middleware.html) guide.

If you want to learn more about configuring the message queue, have a look at the [Message queue hosting guide](./../../../../hosting/infrastructure/message-queue.html).

---

## Add middleware

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/message-queue/add-middleware.html

# Add Middleware [​](#add-middleware)

## Overview [​](#overview)

In this guide you will learn how to add a custom middleware.

A [Middleware](https://symfony.com/doc/current/messenger.html#middleware) is called when the message bus dispatches messages. The middleware defines what happens when you dispatch a message. For example the `send_message` middleware is responsible for sending your message to the configured transport and the `handle_message` middleware will actually call your handlers for the given message.

## Prerequisites [​](#prerequisites)

As most guides, this guide is also built upon the [Plugin base guide](./../../plugin-base-guide.html), but you don't necessarily need that. Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](./../../plugin-fundamentals/dependency-injection.html), so having this open in another tab won't hurt.

## Create middleware [​](#create-middleware)

First we need to create a new service that implements the `MiddlewareInterface`. This interface comes with a method `handle`, which should always call the next middleware.

php

```shiki
// <plugin root>/src/MessageQueue/Middleware/ExampleMiddleware.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Middleware;

use Symfony\Component\Messenger\Envelope;
use Symfony\Component\Messenger\Middleware\MiddlewareInterface;
use Symfony\Component\Messenger\Middleware\StackInterface;

class ExampleMiddleware implements MiddlewareInterface
{
    public function handle(Envelope $envelope, StackInterface $stack): Envelope
    {
        // do something here

        // don't forget to call the next middleware
        return $stack->next()->handle($envelope, $stack);
    }
}
```

## Configure middleware [​](#configure-middleware)

After we've created our middleware, we have to add that middleware to the message bus through configuration.

For each defined bus in our `framework.yaml`, we can define the middleware that this bus should use. To add middleware, we simply specify our custom middleware as follows:

yaml

```shiki
// <platform root>/src/Core/Framework/Resources/config/packages/framework.yaml
framework:
    messenger:
        buses:
          messenger.bus.default:
            middleware:
              - 'Swag\BasicExample\MessageQueue\Middleware\ExampleMiddleware'
              - 'Swag\BasicExample\MessageQueue\Middleware\AnotherExampleMiddleware'
```

## More interesting topics [​](#more-interesting-topics)

* [Message Queue](./add-message-to-queue.html)
* [Message Handler](./add-message-handler.html)

---

## Rule

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/rule/

# Rule [​](#rule)

The Rule Builder allows users to add custom rules to create dynamic conditions and actions within the e-commerce platform. Using the Rule Builder, you can define specific criteria based on various attributes, such as customer data, cart contents, order details, or other relevant factors. These custom rules can then trigger specific actions, such as applying discounts, displaying personalized content, or adjusting pricing based on specific conditions. The Rule Builder empowers businesses to create highly tailored and automated experiences for their customers, enhancing the flexibility and customization options within the Shopware framework.

---

## Add custom rules

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/rule/add-custom-rules.html

# Add Custom Rules [​](#add-custom-rules)

## Overview [​](#overview)

In this guide you will learn how to create rules in Shopware. Rules are used by the rule builder.

This example will introduce a new rule, which checks if it is the first monday of the month or not. The shop owner is then able to react on this specific day every month with special prices or dispatch methods.

## Prerequisites [​](#prerequisites)

In order to add your own custom rules for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html).

You also should be familiar with the [Dependency Injection container](./../../plugin-fundamentals/dependency-injection.html) as this is used to register your custom rule.

It might be helpful to gather some general understanding about the concept of [Rules](./../../../../../concepts/framework/rule.html) as well.

## Create custom rule [​](#create-custom-rule)

To create a custom rule, we have to implement both backend (PHP) code and a user interface in the Administration to manage it. Let's start with the PHP part first, which basically handles the main logic of our rule. After that, there will be an example to actually show your new rule in the Administration.

### Creating rule in PHP [​](#creating-rule-in-php)

First of all, we need a new Rule class. In this example, we name it as `FirstMondayOfTheMonthRule`. It will be placed in the directory `<plugin root>/src/Core/Rule`. Our new class has to extend from the abstract class `Shopware\Core\Framework\Rule\Rule`. Below you can find an example implementation.

php

```shiki
// <plugin root>/src/Core/Rule/FirstMondayOfTheMonthRule.php
<?php declare(strict_types=1);

namespace SwagCustomRules\Core\Rule;

use Shopware\Core\Framework\Rule\Rule;
use Shopware\Core\Framework\Rule\RuleScope;
use Symfony\Component\Validator\Constraints\Type;

class FirstMondayOfTheMonthRule extends Rule
{
    protected bool $isFirstMondayOfTheMonth;

    public function __construct()
    {
        parent::__construct();

        // Will be overwritten at runtime. Reflects the expected value.
        $this->isFirstMondayOfTheMonth = false;
    }

    public function getName(): string
    {
        return 'first_monday';
    }

    public function match(RuleScope $scope): bool
    {
        $isFirstMondayOfTheMonth = $this->isCurrentlyFirstMondayOfTheMonth(date("Y-m-d") );

        // Checks if the shop owner set the rule to "First monday => Yes"
        if ($this->isFirstMondayOfTheMonth) {
            // Shop administrator wants the rule to match if there's currently the first monday of the month.
            return $isFirstMondayOfTheMonth;
        }

        // Shop administrator wants the rule to match if there's currently NOT the first monday of the month.
        return !$isFirstMondayOfTheMonth;
    }

    public function getConstraints(): array
    {
        return [
            'isFirstMondayOfTheMonth' => [new Type('bool')]
        ];
    }

    private function isCurrentlyFirstMondayOfTheMonth($dateString)
    {
        $date = new \DateTime($dateString);
        $dayOfWeek = (int) $date->format('w');

        // Check if it's Monday (1 is Monday)
        if ($dayOfWeek !== 1) {
            return false;
        }

        // Check if the date is within the first seven days of the month
        $dayOfMonth = (int) $date->format('j');
        if ($dayOfMonth > 7) {
            return false;
        }

        // If it passed both checks, it's the first Thursday of the month
        return true;
    }
}
```

As you can see, several methods are already implemented:

* `__constructor`: This only defines the default expected value. This is overwritten at runtime with the actual value, that the shop owner set in the Administration.
* `getName`: Returns a unique technical name for your rule.
* `match`: This checks whether the rule applies. Accordingly, a boolean is returned whether the rule applies or not.
* `getConstraints`: This method returns an array of the possible fields and its types. You could also return the `NotBlank` class here, to require this field.

After we've created our rule class, we have to register it in our `services.xml` and tag it as `shopware.rule.definition`. Please keep in mind: The variables to be used in the rule have to be 'protected' and not 'private', otherwise they won't work properly.

WARNING

Never execute database queries or any other time-consuming operations within the `match()` method of your rule, as it will drastically impact the performance of your store. Stick to the rule scope when evaluating whether your rule matches or not.

php

```shiki
// Scope usage: Check if the customer is logged in
$customer = $scope->getSalesChannelContext()->getCustomer();
$loggedIn = $customer !== null;
```

It is possible to add config to our rule. This makes it possible to skip the [Custom rule component](#custom-rule-component) and the [Custom rule Administration template](#custom-rule-administration-template) parts.

php

```shiki
    public function getConfig(): RuleConfig
    {
        return (new RuleConfig())->booleanField('isFirstMondayOfTheMonth');
    }
```

when [Showing rule in the Administration](#showing-rule-in-the-administration) we would not use a custom component but we would render the `sw-condition-generic` component.

### Active rules [​](#active-rules)

You can access all active rules by using the `getRuleIds` method of the context.

php

```shiki
$context->getRuleIds();
```

### Showing rule in the Administration [​](#showing-rule-in-the-administration)

Now we want to implement our new rule in the Administration so that we can manage it. To achieve this, we have to call the `addCondition` method of the [RuleConditionService](https://github.com/shopware/shopware/blob/v6.6.0.0/src/Administration/Resources/app/administration/src/app/service/rule-condition.service.ts), by decorating this service. The decoration of services in the Administration will be covered in our [Adding services](./../../administration/services-utilities/add-custom-service.html#Decorating a service) guide.

Create a new directory called `<plugin root>/src/Resources/app/administration/src/decorator`. In this directory we create a new file called `rule-condition-service-decoration.js`.

javascript

```shiki
// <plugin root>src/Resources/app/administration/src/decorator/rule-condition-service-decoration.js
import '../../core/component/swag-first-monday';

Shopware.Application.addServiceProviderDecorator('ruleConditionDataProviderService', (ruleConditionService) => {
    ruleConditionService.addCondition('first_monday', {
        component: 'swag-first-monday',
        label: 'Is first monday of the month',
        scopes: ['global']
    });

    return ruleConditionService;
});
```

As you can see, this is decorating the `RuleConditionService` by using its name `ruleConditionDataProviderService`. The decoration adds a new condition called `first_monday`. Make sure to match the name we have used in the `getName` method in PHP. Next, we define the component, in our case, `swag-first-monday`, which is responsible for rendering the rule inside the Administration. We will create this component in the next step. Furthermore, we defined a label, which will be displayed in the rule builder selection. The last option is the scope, which in our case is `global`, as we have not specified a specific one in our core class.

We also have to create a `main.js` file in our Administration sources directory and import the decorator file we've created above. The `main.js` file is used as an entry point to load Administration modules from Shopware plugins:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './decorator/rule-condition-service-decoration';
```

INFO

It may be possible that rules, with your newly created condition, aren't selectable in some places inside the Administration — for example, inside the promotion module. That is because rules are "context-aware". To learn more about that feature [click here](#context-awareness)

#### Creating a new group in the administration [​](#creating-a-new-group-in-the-administration)

The rule will now be added to the list of rules in the admin. It might be useful to create a new group for your rules. We can create a new group by using the `upsertGroup` method of the [RuleConditionService](https://github.com/shopware/shopware/blob/v6.6.0.0/src/Administration/Resources/app/administration/src/app/service/rule-condition.service.ts).

javascript

```shiki
  // <plugin root>src/Resources/app/administration/src/decorator/rule-condition-service-decoration.js
  Shopware.Application.addServiceProviderDecorator('ruleConditionDataProviderService', (ruleConditionService) => {
      ruleConditionService.upsertGroup('days_of_the_month', {
        id: 'days_of_the_month',
        name: 'Days of the month',
      });

      return ruleConditionService;
  });
```

Now that we have our group, we have to link this group to our condition. This is easily done by adding the `group` property to our condition.

javascript

```shiki
// <plugin root>src/Resources/app/administration/src/decorator/rule-condition-service-decoration.js
import '../../core/component/swag-first-monday';

Shopware.Application.addServiceProviderDecorator('ruleConditionDataProviderService', (ruleConditionService) => {
    ruleConditionService.addCondition('first_monday', {
        component: 'swag-first-monday',
        label: 'Is first monday of the month',
        scopes: ['global'],
        group: 'days_of_the_month', 
    });

    return ruleConditionService;
});
```

### Custom rule component [​](#custom-rule-component)

Now that you have registered your rule to the Administration, you would still be lacking the actual component `swag-first-monday`. As you have already defined a path for it in your service decoration, create the following directory: `<plugin root>/src/Resources/app/administration/src/core/component/swag-first-monday`. If you are unfamiliar with creating components in Shopware, refer to the [add your own component](./../../administration/module-component-management/add-custom-component.html) section.

Here's an example of what this component could look like:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/core/component/swag-first-monday/index.js
import template from './swag-first-monday.html.twig';

Shopware.Component.extend('swag-first-monday', 'sw-condition-base', {
    template,

    computed: {
        selectValues() {
            return [
                {
                    label: this.$tc('global.sw-condition.condition.yes'),
                    value: true
                },
                {
                    label: this.$tc('global.sw-condition.condition.no'),
                    value: false
                }
            ];
        },

        isFirstMondayOfTheMonth: {
            get() {
                this.ensureValueExist();

                if (this.condition.value.isFirstMondayOfTheMonth == null) {
                    this.condition.value.isFirstMondayOfTheMonth = false;
                }

                return this.condition.value.isFirstMondayOfTheMonth;
            },
            set(isFirstMondayOfTheMonth) {
                this.ensureValueExist();
                this.condition.value = { ...this.condition.value, isFirstMondayOfTheMonth };
            }
        }
    }
});
```

As you can see, our `swag-first-monday` has to extend from the `sw-condition-base` component and has to bring a custom template, which will be explained in the next step. Let's have a look at each property and method. The first computed property is `selectValues`, which returns an array containing the values "true" and "false". Those will be used in the template later on, as they will be the selectable options for the shop administrator. Do not get confused by the call `this.$tc\('global.sw-condition.condition.yes'\)`; it's just loading a translation by its name, in this case, "Yes" and "No".

INFO

When dealing with boolean values, make sure to always return strings here.

The second and last computed property is `isFirstMondayOfTheMonth`, which uses a getter and setter to define the value of the condition.

### Custom rule Administration template [​](#custom-rule-administration-template)

The last step is, creating a template for our condition. We will create a new file called `swag-first-monday.html.twig` in the same directory as the component. In our template, we have to overwrite the block `sw_condition_value_content`. In this example we define a `sw-single-select` in this block.

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/core/component/swag-first-monday/swag-first-monday.html.twig
{% block sw_condition_value_content %}
    <sw-single-select name="first-monday"
                      id="first-monday"
                      size="medium"
                      :options="selectValues"
                      v-model="isFirstMondayOfTheMonth"
                      class="field--main">
    </sw-single-select>
{% endblock %}
```

As you can see, our `sw-single-select` uses the previously created computed property `selectValues` as the `options` prop, and the value is saved into the variable `isFirstMondayOfTheMonth`. That's it; your rule is now fully integrated.

## Context awareness [​](#context-awareness)

INFO

This feature is available in version 6.5.0.0 or above.

Rules in the Shopware Administration are aware of where users assign them. That means that a user can't add a rule to a promotion when the rule contains the condition "Cart amount". That also works the other way around. If the rule is assigned to a promotion, the user can't use the "Cart amount" condition.

![Select component with disabled rules](/assets/rule-restrictions-rule-builder.Drw93hvo.png)

It is possible to define where rules can be assigned inside the Administration.

### Defining restrictions [​](#defining-restrictions)

You have previously added the condition inside `ruleConditionDataProviderService`. This is the place where you define restrictions for the rule. The goal of this example is to restrict the user from adding a rule to advanced prices if the rules contain a specific condition.

First, get the existing definition for the rule relation as below:

javascript

```shiki
// <plugin root>src/Resources/app/administration/src/decorator/rule-condition-service-decoration.js
// Inside the addServiceProviderDecorator method
const restrictions = ruleConditionService.getAwarenessConfigurationByAssignmentName('productPrices');
```

INFO

You can find all possible relations in `Shopware\Core\Content\Rule\RuleDefinition`;

Now, add your `awarenessConfiguration` and call the `addAwarenessConfiguration` method.

javascript

```shiki
type awarenessConfiguration = {
notEquals?: Array<string>,
equalsAny?: Array<string>,
snippet?: string,
}
```

javascript

```shiki
// <plugin root>src/Resources/app/administration/src/decorator/rule-condition-service-decoration.js
Shopware.Application.addServiceProviderDecorator('ruleConditionDataProviderService', (ruleConditionService) => {
    // Your newly added conditions is here

    const restrictions = ruleConditionService.getAwarenessConfigurationByAssignmentName('productPrices');

    ruleConditionService
        .addAwarenessConfiguration('productPrices', {
            notEquals: [
                'first_monday'
            ],
            equalsAny: [ ], // ignore if not needed
            snippet: 'sw-restricted-rules.restrictedAssignment.productPrices',
        });
});
```

What do `notEquals` and `equalsAny` actually mean? With these two properties, you can define the rules you want to assign to a specific relation, i.e., `productPrices` need to have at least one condition inside `equalsAny` or should not have any condition inside of `notEquals`.

Finally, you just need a snippet, and you can choose an existing one or create one yourself. With that said, you successfully defined restrictions for your custom condition. If you now try to assign a rule with your condition to advanced prices, you should see that it is not possible, and the rule is disabled.

### Restricting rule assignments [​](#restricting-rule-assignments)

When you add a new rule-select component to assign rules somewhere in Shopware, you should use the `sw-select-rule-create` component. With that, you can ensure that the rules you don't want to be selectable aren't selectable. For that, we need to write some twig code. The important property here is the `rule-aware-group-key` property which should match the assignment name of the rule-aware group we just extended.

INFO

Refer to [customize administration components](./../../administration/module-component-management/customizing-components.html) to know more about it.

twig

```shiki
{% block example_twig_blog %}
    <sw-select-rule-create
        rule-aware-group-key="productPrices"
        @save-rule="[YOUR SAVE METHOD]">
{% endblock %}
```

That's it! The component automatically fetches rules and marks them as disabled.

## Multi select and other components [​](#multi-select-and-other-components)

The above guide explains the integration of a boolean and no values. If you want to go more in-depth, for example, search your entity, you can extend and use the different components that Shopware comes with. The multi select example can be found in `shopware/administration/Resources/app/administration/src/app/component/form/select/entity/sw-entity-multi-select`.

## Further reading [​](#further-reading)

For more other information you can refer to [Add rule assignment configuration](./../../administration/advanced-configuration/add-rule-assignment-configuration.html) section of the guide.

---

## Store API

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/store-api/

# Store API [​](#store-api)

The Store API plugin in Shopware enables the addition of custom endpoints to the existing Store API and the ability to override or extend the functionality of existing endpoints. This allows developers to customize the API according to their specific requirements, providing additional functionality or modifying the behavior of existing endpoints.

---

## Add store API route

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/store-api/add-store-api-route.html

# Add Store API route [​](#add-store-api-route)

## Overview [​](#overview)

In this guide you will learn how to add a custom store API route. In this example, we will create a new route called `ExampleRoute` that searches entities of type `swag_example`. The route will be accessible under `/store-api/example`.

## Prerequisites [​](#prerequisites)

In order to add your own Store API route for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html).

You also should have a look at our [Adding custom complex data](./../data-handling/add-custom-complex-data.html) guide, since this guide is built upon it.

## Add Store API route [​](#add-store-api-route-1)

As you may already know from the [Adjusting a service](./../../plugin-fundamentals/adjusting-service.html) guide, we use abstract classes to make our routes more decoratable.

WARNING

All fields that should be available through the API require the flag `ApiAware` in the definition.

### Create abstract route class [​](#create-abstract-route-class)

First of all, we create an abstract class called `AbstractExampleRoute`. This class has to contain a method `getDecorated` and a method `load` with a `Criteria` and `SalesChannelContext` as parameter. The `load` method has to return an instance of `ExampleRouteResponse`, which we will create later on.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/AbstractExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

abstract class AbstractExampleRoute
{
    abstract public function getDecorated(): AbstractExampleRoute;

    abstract public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse;
}
```

### Create route class [​](#create-route-class)

Now we can create a new class `ExampleRoute` which uses our previously created `AbstractExampleRoute`.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\Routing\StoreApiRouteScope;
use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
class ExampleRoute extends AbstractExampleRoute
{
    protected EntityRepository $exampleRepository;

    public function __construct(EntityRepository $exampleRepository)
    {
        $this->exampleRepository = $exampleRepository;
    }

    public function getDecorated(): AbstractExampleRoute
    {
        throw new DecorationPatternException(self::class);
    }

    #[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'], defaults: ['_entity' => 'swag_example'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse
    {
        return new ExampleRouteResponse($this->exampleRepository->search($criteria, $context->getContext()));
    }
}
```

As you can see, our class has the attribute `Route` and the defined \_routeScope `store-api`.

In our class constructor we've injected our `swag_example.repository`. The method `getDecorated()` must throw a `DecorationPatternException` because it has no decoration yet and the method `load`, which fetches the data, returns a new `ExampleRouteResponse` with the respective repository search result as argument.

The `_entity` in the defaults of the `Route` attribute just marks the entity that the api will return.

### Register route class [​](#register-route-class)

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" >
            <argument type="service" id="swag_example.repository"/>
        </service>
    </services>
</container>
```

### Route response [​](#route-response)

After we have created our route, we need to create the mentioned `ExampleRouteResponse`. This class should extend from `Shopware\Core\System\SalesChannel\StoreApiResponse`, consequently inheriting a property `$object` of type `Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`. The `StoreApiResponse` parent constructor takes accepts one argument `$object` in order to set the value for the `$object` property (currently we provide this parameter our `ExampleRoute`). Finally, we add a method `getExamples` in which we return our entity collection that we got from the object.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRouteResponse.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\System\SalesChannel\StoreApiResponse;
use Swag\BasicExample\Core\Content\Example\ExampleCollection;

/**
 * Class ExampleRouteResponse
 * @property EntitySearchResult<ExampleCollection> $object
 */
class ExampleRouteResponse extends StoreApiResponse
{
    public function getExamples(): ExampleCollection
    {
        return $this->object->getEntities();
    }
}
```

## Register route [​](#register-route)

The last thing we need to do now is to tell Shopware how to look for new routes in our plugin. This is done with a `routes.xml` file at `<plugin root>/src/Resources/config/` location. Have a look at the official [Symfony documentation](https://symfony.com/doc/current/routing.html) about routes and how they are registered.

xml

```shiki
// <plugin root>/src/Resources/config/routes.xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Core/**/*Route.php" type="attribute" />
</routes>
```

## Check route via Symfony debugger [​](#check-route-via-symfony-debugger)

To check if your route was registered correctly, you can use the [Symfony route debugger](https://symfony.com/doc/current/routing.html#debugging-routes).

bash

```shiki
// 
$ ./bin/console debug:router store-api.example.search
```

## Add a route to the OpenAPI schema [​](#add-a-route-to-the-openapi-schema)

To add the route to the Stoplight page, a JSON file is needed in a specific [format](https://swagger.io/specification/#paths-object). It contains information about the paths, methods, parameters, and more. You must place the JSON file in `<plugin root>/src/Resources/Schema/StoreApi/` so the shopware internal OpenApi3Generator can find it (for Admin API endpoints, use `AdminApi`).

javascript

```shiki
// <plugin root>/src/Resources/Schema/StoreApi/example.json
{
  "openapi": "3.0.0",
  "info": [],
  "paths": {
    "/example": {
      "post": {
        "tags": [
          "Example",
          "Endpoints supporting Criteria "
        ],
        "summary": "Example entity endpoint",
        "description": "Returns a list of example entities.",
        "operationId": "example",
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "allOf": [
                  {
                    "$ref": "#/components/schemas/Criteria"
                  }
                ]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Returns a list of example entities.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Example"
                }
              }
            }
          }
        },
        "security": [
          {
            "ApiKey": []
          }
        ]
      }
    }
  }
}
```

### Check route in Stoplight [​](#check-route-in-stoplight)

To check if your file has the correct format, you'll have to check Stoplight. To do this, go to the following route: `/store-api/_info/stoplightio.html`.

Your generated request and response could look like this:

#### Request [​](#request)

json

```shiki
{
  "page": 0,
  "limit": 0,
  "term": "string",
  "filter": [
    {
      "type": "string",
      "field": "string",
      "value": "string"
    }
  ],
  "sort": [
    {
      "field": "string",
      "order": "string",
      "naturalSorting": true
    }
  ],
  "post-filter": [
    {
      "type": "string",
      "field": "string",
      "value": "string"
    }
  ],
  "associations": {},
  "aggregations": [
    {
      "name": "string",
      "type": "string",
      "field": "string"
    }
  ],
  "query": [
    {
      "score": 0,
      "query": {
        "type": "string",
        "field": "string",
        "value": "string"
      }
    }
  ],
  "grouping": [
    "string"
  ]
}
```

#### Response [​](#response)

json

```shiki
{
  "total": 0,
  "aggregations": {},
  "elements": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "active": true,
      "createdAt": "2021-03-24T13:18:46.503Z",
      "updatedAt": "2021-03-24T13:18:46.503Z"
    }
  ]
}
```

## Make the route available for the Storefront [​](#make-the-route-available-for-the-storefront)

If you want to access the functionality of your route also from the Storefront you need to make it available there by adding a custom [Storefront controller](./../../storefront/add-custom-controller.html) that will wrap your just created route.

php

```shiki
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Swag\BasicExample\Core\Content\Example\SalesChannel\AbstractExampleRoute;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    private AbstractExampleRoute $route;

    public function __construct(AbstractExampleRoute $route)
    {
        $this->route = $route;
    }

    #[Route(path: '/example', name: 'frontend.example.search', methods: ['GET', 'POST'], defaults: ['XmlHttpRequest' => 'true', '_entity' => 'swag_example'])]
    public function load(Criteria $criteria, SalesChannelContext $context): Response
    {
        return $this->route->load($criteria, $context);
    }
}
```

This looks very similar then what we did in the `ExampleRoute` itself. The main difference is that this route is registered for the `storefront` route scope. Additionally, we also use the `'XmlHttpRequest' => true` config option on the route, this will enable us to request that route via AJAX-calls from the Storefronts javascript.

### Register the Controller [​](#register-the-controller)

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" >
            <argument type="service" id="swag_example.repository"/>
        </service>
    
        <service id="Swag\BasicExample\Storefront\Controller\ExampleController" >
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute"/>
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
        </service>
    </services>
</container>
```

### Register Storefront api-route [​](#register-storefront-api-route)

We need to tell Shopware that there is a new API-route for the `storefront` scope by extending the `routes.xml` to also include all Storefront controllers.

xml

```shiki
// <plugin root>/src/Resources/config/routes.xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Core/**/*Route.php" type="attribute" />
    <import resource="../../Storefront/**/*Controller.php" type="attribute" />
</routes>
```

### Requesting your route from the Storefront [​](#requesting-your-route-from-the-storefront)

You can request your new route from the Storefront from inside a [custom javascript plugin](./../../storefront/add-custom-javascript.html). We expect that you have followed that guide and know how to register your custom javascript plugin in the Storefront.

When you want to request your custom route you can use the existing `http-client` service for that.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    async requestCustomRoute() {
        const response = await fetch('/example', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                limit: 10,
                offset: 0,
            }),
        });
        
        if (!response.ok) {
            throw new Error('Request failed');
        }

        const data = await response.json();

        console.log(data);
    }
}
```

---

## Override existing route

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/store-api/override-existing-route.html

# Override Existing Route [​](#override-existing-route)

## Overview [​](#overview)

In this guide you will learn how to override existing Store API routes to add additional data to it.

## Prerequisites [​](#prerequisites)

As most guides, this guide is also built upon the [Plugin base guide](./../../plugin-base-guide.html), but you don't necessarily need that.

Furthermore, you should have a look at our guide about [Adding a Store API route](./add-store-api-route.html), since this guide is built upon it.

## Decorating our route [​](#decorating-our-route)

First, we have to create a new class which extends `AbstractExampleRoute`. In this example we will name it `ExampleRouteDecorator`.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRouteDecorator.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\Routing\StoreApiRouteScope;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
class ExampleRouteDecorator extends AbstractExampleRoute
{
    protected EntityRepository $exampleRepository;

    private AbstractExampleRoute $decorated;

    public function __construct(EntityRepository $exampleRepository, AbstractExampleRoute $exampleRoute)
    {
        $this->exampleRepository = $exampleRepository;
        $this->decorated = $exampleRoute;
    }

    public function getDecorated(): AbstractExampleRoute
    {
        return $this->decorated;
    }
    
    #[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET', 'POST'], defaults: ['_entity' => 'category'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse
    {
        // We must call this function when using the decorator approach
        $exampleResponse = $this->decorated->load();
        
        // do some custom stuff
        $exampleResponse->headers->add([ 'cache-control' => "max-age=10000" ])

        return $exampleResponse;›
    }
}
```

As you can see, our decorated route has to extend from the `AbstractExampleRoute` and the constructor has to accept an instance of `AbstractExampleRoute`. Furthermore, the `getDecorated()` function has to return the decorated route passed into the constructor. Now we can add some additional data in the `load` method, which we can retrieve with the criteria.

## Registering route [​](#registering-route)

Last, we have to register the decorated route to the DI-container. The `ExampleRouteDecorator` has to be registered after the `ExampleRoute` with the attribute `decorated` which points to the `ExampleRoute`. For the second argument we have to use the `ExampleRouteDecorator.inner`.

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        ...

        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRouteDecorator" decorates="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" public="true">
            <argument type="service" id="swag_example.repository"/>
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRouteDecorator.inner"/>
        </service>
    </services>
</container>
```

---

## Filesystem

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/filesystem/

# Filesystem [​](#filesystem)

Plugins often need the ability to read and write files. Thanks to the [Flysystem](https://flysystem.thephpleague.com/docs/) that Shopware uses, this can be managed very easily. It does not matter whether the files are stored on the local file system or at a cloud provider. The read and write access remains the same. If you want to learn more about the configuration of the file system in Shopware, have a look at the [filesystem guide](./../../../../hosting/infrastructure/filesystem.html). For example, you will learn how to outsource the file system to the Amazon cloud. In a plugin, we don't have to worry about the configuration and can use the advantages of the Flysystem directly.

---

## Filesystem - Flysystem

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/filesystem/filesystem.html

# Filesystem - Flysystem [​](#filesystem-flysystem)

## Overview [​](#overview)

Flysystem is a file storage library for PHP. It provides one interface to interact with many types of filesystems. The Flysystem file system in Shopware is flexible, allowing seamless interaction with various file storage systems. It provides a consistent interface to access, manipulate, and manage files across different storage backends.

## Prerequisites [​](#prerequisites)

This guide is built upon both the [Plugin base guide](./../../plugin-base-guide.html) and the [Add custom service guide](./../../plugin-fundamentals/add-custom-service.html).

## Flysystem overview [​](#flysystem-overview)

The Flysystem enables your plugin to read and write files through a common interface. There are several default namespaces/directories that are available, for example:

* One for private files of the shop: invoices, delivery notes
* One for public files: product pictures, media files
* One for theme files
* One for sitemap files
* One for bundle assets files

However, every plugin/bundle gets an own namespace that should be used for private or public plugin files. These are automatically generated during the plugin installation. The namespace is prefixed with the [Snake case](https://en.wikipedia.org/wiki/Snake_case) plugin name followed by `filesystem` `.` `private` or `public`. For our example plugin, this would be

* `swag_basic_example.filesystem.public` for public plugin files
* `swag_basic_example.filesystem.private` for private plugin files

## Use filesystem in a service [​](#use-filesystem-in-a-service)

To make use of the filesystem, we register a new service, which helps to read and write files to the filesystem.

php

```shiki
// <plugin root>/src/Service/ExampleFilesystemService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use League\Flysystem\FilesystemOperator;

class ExampleFilesystemService
{
    /**
     * @var FilesystemOperator
     */
    private FilesystemOperator $fileSystemPublic;
    /**
     * @var FilesystemOperator
     */
    private FilesystemOperator $fileSystemPrivate;

    /**
     * ExampleFilesystemService constructor.
     * @param FilesystemOperator $fileSystemPublic
     * @param FilesystemOperator $fileSystemPrivate
     */
    public function __construct(FilesystemOperator $fileSystemPublic, FilesystemOperator $fileSystemPrivate)
    {
        $this->fileSystemPublic = $fileSystemPublic;
        $this->fileSystemPrivate = $fileSystemPrivate;
    }

    public function readPrivateFile(string $filename) {
        return $this->fileSystemPrivate->read($filename);
    }

    public function writePrivateFile(string $filename, string $content) {
        $this->fileSystemPrivate->write($filename, $content);
    }

    public function listPublicFiles(): array {
        return $this->fileSystemPublic->listContents();
    }
}
```

This service makes use of the private und public filesystem. As you already know, this php class has to be registered as a service in the dependency injection container. This is also the place where we define which filesystem will be handed over to the constructor. To make use of the plugin private and public files, the service definition could look like this:

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleFilesystemService">
            <argument type="service" id="swag_basic_example.filesystem.public"/>
            <argument type="service" id="swag_basic_example.filesystem.private"/>
            <!--
            There are also predefined file system services
            <argument type="service" id="shopware.filesystem.private"/>
            <argument type="service" id="shopware.filesystem.public"/>
            -->
        </service>
    </services>
</container>
```

Now, this service can be used to read or write files to the private plugin filesystem or to list all files in the public plugin filesystem. You should visit the [Flysystem API documentation](https://flysystem.thephpleague.com/docs/usage/filesystem-api/) for more information.

---

## Flow

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/flow/

# Flow [​](#flow)

The flow builder plugin allows businesses to create and manage custom workflows and automation within the e-commerce platform, enhancing efficiency and streamlining processes. The flow builder mainly comprises actions and triggers.

The customizable flow actions allow the automation of various tasks or processes, while the custom flow triggers are the events or conditions that initiate the execution of this flow. These customizations can be defined and executed within the flow builder enabling businesses to respond dynamically to specific events or changes in their e-commerce platform.

---

## Add Flow Builder action

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/flow/add-flow-builder-action.html

# Add custom flow Action [​](#add-custom-flow-action)

## Overview [​](#overview)

In this guide, you'll learn how to create custom flow action in Shopware. The flow builder uses actions to perform business tasks. This example will introduce a new custom action called `create tags`.

## Prerequisites [​](#prerequisites)

In order to add your own custom flow action for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide.](./../../plugin-base-guide.html)

You also should be familiar with the [Dependency Injection container](./../../plugin-fundamentals/dependency-injection.html) as this is used to register your custom flow action and [Listening to events](./../../plugin-fundamentals/listening-to-events.html#creating-your-own-subscriber) to create a subscriber class.

It might be helpful to gather some general understanding about the [concept of Flow Builder](./../../../../../concepts/framework/flow-concept.html) as well.

## Existing triggers and actions [​](#existing-triggers-and-actions)

You can refer to the [Flow reference](./../../../../../resources/references/core-reference/flow-reference.html) to read triggers and actions detail.

## Create custom flow action [​](#create-custom-flow-action)

To create a custom flow action, firstly you have to make a plugin and install it. Refer to the [Plugin Base Guide](./../../plugin-base-guide.html) to do it. For instance, lets create a plugin named `CreateTagAction`. You must implement both backend (PHP) code and a user interface in the Administration to manage it. Let's start with the PHP part first, which handles the main logic of our action. After that, there will be an example to show your new actions in the Administration.

## Creating flow action in PHP [​](#creating-flow-action-in-php)

### Create new Aware interface [​](#create-new-aware-interface)

First of all, we need to define an aware interface for your own action. I intended to create the `CreateTagAction`, so I need to create a related aware named `TagAware`, will be placed in directory `<plugin root>/src/Core/Framework/Event`. Our new interface has to extend from interfaces `Shopware\Core\Framework\Event\FLowEventAware`:

php

```shiki
// <plugin root>/src/Core/Framework/Event/TagAware.php
<?php declare(strict_types=1);
namespace Swag\ExamplePlugin\Core\Framework\Event;
use Shopware\Core\Framework\Event\FlowEventAware;
use Shopware\Core\Framework\Event\IsFlowEventAware;

#[IsFlowEventAware]
interface TagAware extends FlowEventAware
{
    ...

    public const TAG = 'tag';

    public const TAG_ID = 'tagId';

    public function getTag();

    ...
}
```

### Create new action [​](#create-new-action)

In this example, we will name it `CreateTagAction`. It will be placed in the directory `<plugin root>/src/Core/Content/Flow/Dispatching/Action`. Below you can find an example implementation:

php

```shiki
// <plugin root>/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php
<?php declare(strict_types=1);

namespace Swag\CreateTagAction\Core\Content\Flow\Dispatching\Action;

use Shopware\Core\Content\Flow\Dispatching\Action\FlowAction;
use Shopware\Core\Content\Flow\Dispatching\StorableFlow;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Uuid\Uuid;
use Swag\CreateTagAction\Core\Framework\Event\TagAware;

class CreateTagAction extends FlowAction
{
    private EntityRepository $tagRepository;

    public function __construct(EntityRepository $tagRepository)
    {
        // you would need this repository to create a tag
        $this->tagRepository = $tagRepository;
    }

    public static function getName(): string
    {
        // your own action name
        return 'action.create.tag';
    }

    public function requirements(): array
    {
        return [TagAware::class];
    }

    public function handleFlow(StorableFlow $flow): void
    {
        // config is the config data when created a flow sequence
        $config = $flow->getConfig();

        // make sure your tags data exists
        if (!\array_key_exists('tags', $config)) {
            return;
        }

        $tags = $config['tags'];

        // just a step to make sure you're dispatching correct action
        if (!$flow->hasStore(TagAware::TAG_ID) || empty($tags)) {
            return;
        }

        // get tag id
        $tagId = $flow->getStore(TagAware::TAG_ID);

        // get tag
        $tag = $flow->getData(TagAware::TAG);

        $tagData = [];
        foreach ($tags as $tag) {
            $tagData[] = [
                'id' => Uuid::randomHex(),
                'name' => $tag,
            ];
        }

        // simply create tags
        $this->tagRepository->create($tagData, $flow->getContext());
    }
}
```

As you can see, several methods are already implemented:

* `__constructor`: This only defines the default expected value. This is overwritten at runtime with the actual value, that the shop owner set in the Administration.
* `getName`: Returns a unique technical name for your action.
* `requirements`: This defines which interfaces the action belongs to.
* `handleFlow`: Use this method to handle your action stuff.
  + Use `$flow->getStore($key)` if you want to get the data from aware interfaces. E.g: `tag_id` in `TagAware`, `customer_id` from `CustomerAware` and so on.
  + Use `$flow->getData($key)` if you want to get the data from original events or additional data. E.g: `tag`, `customer`, `contactFormData` and so on.

You also need to register this action in the container as a service. Make sure to define a tag `<tag name="flow.action" priority="600">` at `<plugin root>/src/Resources/config/services.xml`. This tag will ensure that your action is included in the response of the *`/api/_info/flow-actions.json`* API. The priority attribute will determine the order of the action in the API response.

XML

```shiki
// <plugin root>/src/Resources/config/services.xml
<service id="Swag\CreateTagAction\Core\Content\Flow\Dispatching\Action\CreateTagAction">
    <argument type="service" id="tag.repository" />
    <tag name="flow.action" priority="600" key="action.create.tag"/>
</service>
```

Great, your own action is created completely. Let's go to the next step.

### Define action scope [​](#define-action-scope)

In this step, you will know how to define your action scope for `CreateTagAction`. There are three scopes for the `CreateTagAction`:

* Available for all *already Events*.
* Available for only one or multiple *already Events.*
* Available for new event (new event from this plugin).

#### `CreateTagAction` available for all *already Events* [​](#createtagaction-available-for-all-already-events)

* Just define the empty array in `CreateTagAction::requirements`

php

```shiki
    // plugin root>/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php
    ...

    public function requirements(): array
    {
        return [];
    }

    ...
```

That means when you define the requirements like the code above, all triggers in the flow builder can define the action `CreateTagAction` for the next progress.

![Flow Builder trigger](/assets/flow-builder-action-available-all-events.C2jvz2S9.png)

Here, the action name is empty as the action name snippet is not yet defined.

#### `CreateTagAction` available for only one or multiple *already Events* [​](#createtagaction-available-for-only-one-or-multiple-already-events)

Make the `CreateTagAction` available for all events related to Order and Customer.

php

```shiki
    // <plugin root>/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php
    ...

    public function requirements(): array
    {
        return [OrderAware::class, CustomerAware::class];
    }

    ...
```

#### `CreateTagAction` available for new event [​](#createtagaction-available-for-new-event)

* For this case, you can define a new event and make the `CreateTagAction` available for this event.
* Event must implement the `TagAware`

php

```shiki
// <plugin root>/src/Core/Content/Flow/Subscriber/BusinessEventCollectorSubscriber.php
<?php declare(strict_types=1);

namespace Swag\CreateTagAction\Core\Content\Event;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\Event\EventData\EntityType;
use Shopware\Core\Framework\Event\EventData\EventDataCollection;
use Shopware\Core\System\Tag\TagDefinition;
use Shopware\Core\System\Tag\TagEntity;
use Swag\CreateTagAction\Core\Framework\Event\TagAware;
use Symfony\Contracts\EventDispatcher\Event;

class BasicExampleEvent extends Event implements TagAware
{
    public const EVENT_NAME = 'example.event';

    private TagEntity $tag;

    private Context $context;

    public function __construct(Context $context, TagEntity $tag)
    {
        $this->tag = $tag;
        $this->context = $context;
    }

    public function getName(): string
    {
        return self::EVENT_NAME;
    }

    public static function getAvailableData(): EventDataCollection
    {
        return (new EventDataCollection())
            ->add('tag', new EntityType(TagDefinition::class));
    }

    public function getContext(): Context
    {
        return $this->context;
    }

    public function getTag(): TagEntity
    {
        return $this->tag;
    }
}
```

* Define the `TagAware` in `CreateTagAction::requirements`

php

```shiki
    // <plugin root>/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php
    ...

    public function requirements(): array
    {
        return [TagAware::class];
    }

    ...
```

* To show the new event in Flow Builder Triggers list

php

```shiki
// <plugin root>/src/Core/Content/Subscriber/BusinessEventCollectorSubscriber.php
<?php declare(strict_types=1);
namespace Swag\CreateTagAction\Core\Content\Subscriber;

use Shopware\Core\Framework\Event\BusinessEventCollector;
use Shopware\Core\Framework\Event\BusinessEventCollectorEvent;
use Swag\CreateTagAction\Core\Content\Event\BasicExampleEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class BusinessEventCollectorSubscriber implements EventSubscriberInterface
{
    private BusinessEventCollector $businessEventCollector;

    public function __construct(BusinessEventCollector $businessEventCollector)
    {
        $this->businessEventCollector = $businessEventCollector;
    }

    public static function getSubscribedEvents()
    {
        return [
            BusinessEventCollectorEvent::NAME => 'onAddExampleEvent',
        ];
    }

    public function onAddExampleEvent(BusinessEventCollectorEvent $event): void
    {
        $collection = $event->getCollection();

        $definition = $this->businessEventCollector->define(BasicExampleEvent::class);

        if (!$definition) {
            return;
        }

        $collection->set($definition->getName(), $definition);
    }
}
```

And don't forget to register your subscriber to the container at `<plugin root>/src/Resources/config/services.xml`.

xml

```shiki
<service id="Swag\CreateTagAction\Core\Content\Subscriber\BusinessEventCollectorSubscriber">
    <argument type="service" id="Shopware\Core\Framework\Event\BusinessEventCollector"/>
    <tag name="kernel.event_subscriber"/>
</service>
```

* Define the Event snippet

json

```shiki
// <plugin root>/src/Resources/app/administration/src/module/sw-flow/snippet/en-GB.json
{
  "sw-flow": {
    "triggers": {
      "example": "Example",
      "event": "Event"
    }
  }
}
```

![Flow Builder trigger](/assets/flow-builder-triggers-list.Dt9s7qhr.png)

Well, you have successfully created your custom action in Backend in PHP.

## Add custom action in Administration [​](#add-custom-action-in-administration)

After we are done with the PHP code, `action.create.tag` is received from the response of `/api/_info/flow-actions.json`. However, the custom action displays in the action list without label. These further steps in Administration will help you show the action label and add configuration for it.

To see the action list, we select a Trigger, for example [example\event], from the Trigger drop-down in the Flow tab. After that, we choose option `ACTION (THEN)`. An action component appears with an action list.

![Flow Builder trigger](/assets/flow-builder-trigger-drop.OnbXERP1.png)

![Flow Builder action then](/assets/flow-builder-action-then.Bz37yhzT.png)

![Flow Builder trigger](/assets/flow-builder-action-no-label.BHkzEubE.png)

### Step 1: Show action label in action list [​](#step-1-show-action-label-in-action-list)

First, we need to define information like `constants`, `snippets` to show on the action list. To be consistent with the custom action defined in our PHP code, create an action name called `CREATE_TAG` to represent `action.create.tag`, which gets from the response of `/api/_info/flow-actions.json`.

![Flow Builder action services list](/assets/flow-builder-action-sevices-list.BLb2H-qy.png)

JS

```shiki
// <plugin root>src/Resources/app/administration/src/constant/create-tag-action.constant.js
export const ACTION = Object.freeze({
    CREATE_TAG: 'action.create.tag',
});

export const GROUP = 'customer'

export default {
    ACTION, GROUP
};
```

And then add snippets for labels:

JS

```shiki
// src/Resources/app/administration/src/snippet/en-GB.json
{
    "create-tag-action": {
        "titleCreateTag": "Create tag",
        "labelTags": "Tags",
        "placeholderTags": "Enter tags",
        "buttonSaveAction": "Save action",
        "buttonAddAction": "Add action",
        "descriptionTags": "Tags: {tags}"
    }
}
```

Do it as the same with `de-DE.json` file for translation of DE language.

After that, we also need to override the `sw-flow-sequence-action` component in the core:

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/extension/sw-flow-sequence-action/index.js
import { ACTION, GROUP } from '../../constant/create-tag-action.constant';

const { Component } = Shopware;

Component.override('sw-flow-sequence-action', {
    computed: {
        // Not necessary if you use an existing group
        // Push the `groups` method in computed if you are defining a new group
        groups() {
            this.actionGroups.unshift(GROUP);

            return this.$super('groups');
        },

        modalName() {
            if (this.selectedAction === ACTION.CREATE_TAG) {
                return 'sw-flow-create-tag-modal';
            }

            return this.$super('modalName');
        },
    },

    methods: {
        getActionDescriptions(sequence) {
            if(sequence.actionName === ACTION.CREATE_TAG){
                return this.getCreateTagDescription(sequence.config)
            }
            return this.$super('getActionDescriptions', sequence)
        },
        
        getCreateTagDescription(config) {
            const tags = config.tags.join(', ');

            return this.$tc('create-tag-action.descriptionTags', 0, {
                tags
            });
        },

        getActionTitle(actionName) {
            if (actionName === ACTION.CREATE_TAG) {
                return {
                    value: actionName,
                    icon: 'regular-tag',
                    label: this.$tc('create-tag-action.titleCreateTag'),
                    group: GROUP,
                }
            }

            return this.$super('getActionTitle', actionName);
        },
    },
});
```

Do not forget to import the file to the entry file `main.js`:

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './extension/sw-flow-sequence-action';
```

**Grouping Actions**

As you can see, we already defined the constant for the group in `create-tag-action.constant.js`

JS

```shiki
export const GROUP = 'customer'
```

The new action `action.create.tag` will be shown on the Customer group.

![Choose a Flow Builder Action](/assets/flow-builder-action-customer-group.DxjPOfO5.png)

It will default on the General group if it is not defined.

Here is a list of group names you should take a look at:

| Group Name | Group Headline |
| --- | --- |
| general | General |
| tag | Tag |
| customer | Customer |
| order | Order |

### Step 2: Add configuration for action [​](#step-2-add-configuration-for-action)

If you click the Create tag action, the below error will be shown on the console. That means we're going the right way.

![Choose a Flow Builder Action](/assets/flow-builder-action-error.C2aRX7Q1.png)

Because in `sw-flow-sequence-action`, we expect that the new modal has the name `sw-flow-create-tag-modal`.

JS

```shiki
modalName() {
    if (this.selectedAction === ACTION.CREATE_TAG) {
        return 'sw-flow-create-tag-modal';
    }

    return this.$super('modalName');
},
```

To define the modal, just create a new folder `sw-flow-create-tag-modal` in `src/Resources/app/administration/src/component` and create some files following:

#### JavaScript file [​](#javascript-file)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/component/sw-flow-create-tag-modal/index.js
import template from './sw-flow-create-tag-modal.html.twig';

const { Data: { Criteria, EntityCollection } } = Shopware;
const { Component, Context } = Shopware;

Component.register('sw-flow-create-tag-modal', {
    template,

    inject: [
        'repositoryFactory',
    ],

    props: {
        sequence: {
            type: Object,
            required: true,
        },
    },

    data() {
        return {
            tagCollection: [],
        };
    },

    computed: {
        tagRepository() {
            return this.repositoryFactory.create('tag');
        },

        tagCriteria() {
            const criteria = new Criteria(1, 25);
            const { config } = this.sequence;
            const tagIds = Object.keys(config.tagIds);
            if (tagIds.length) {
                criteria.addFilter(Criteria.equalsAny('id', tagIds));
            }

            return criteria;
        },
    },

    created() {
        this.createdComponent();
    },

    methods: {
        createdComponent() {
            this.tagCollection = this.createTagCollection();

            const { config } = this.sequence;
            if (this.sequence.id && config?.tagIds) {
                this.getTagCollection();
            }
        },

        getTagCollection() {
            return this.tagRepository.search(this.tagCriteria)
                .then(tags => {
                    this.tagCollection = tags;
                })
                .catch(() => {
                    this.tagCollection = [];
                });
        },

        createTagCollection() {
            return new EntityCollection(
                this.tagRepository.route,
                this.tagRepository.entityName,
                Context.api,
            );
        },

        onClose() {
            this.$emit('modal-close');
        },

        onAddTag(data) {
            this.tagCollection.add(data);
        },

        onRemoveTag(data) {
            this.tagCollection.remove(data);
        },

        getConfig() {
            const tagIds = {};
            this.tagCollection.forEach(tag => {
                Object.assign(tagIds, {
                    [tag.id]: tag.name,
                });
            });

            return {
                tagIds,
            };
        },

        onAddAction() {
            const config = this.getConfig();
            const data = {
                ...this.sequence,
                config,
            };

            this.$emit('process-finish', data);
        },
    },
});
```

#### Twig template file [​](#twig-template-file)

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/component/sw-flow-create-tag-modal/sw-flow-create-tag-modal.html.twig
{% block create_tag_action_modal %}
<sw-modal
    class="create-tag-action-modal"
    :title="$tc('create-tag-action.titleCreateTag')"
    @modal-close="onClose"
>
    {% block create_tag_action_modal_content %}
        <sw-entity-tag-select
            v-model="tagCollection"
            class="sw-flow-create-tag-modal__tags-field"
            required
            :label="$tc('create-tag-action.labelTags')"
            :placeholder="$tc('create-tag-action.placeholderTags')"
            @item-add="onAddTag"
            @item-remove="onRemoveTag"
        />
    {% endblock %}

    {% block create_tag_action_modall_footer %}
        <template #modal-footer>
            {% block create_tag_action_modal_footer_cancel_button %}
                <sw-button
                    class="create-tag-action-modal__cancel-button"
                    size="small"
                    @click="onClose"
                >
                    {{ $tc('global.default.cancel') }}
                </sw-button>
            {% endblock %}

            {% block create_tag_action_modal_footer_save_button %}
                <sw-button
                    class="create-tag-action-modal__save-button"
                    variant="primary"
                    size="small"
                    @click="onAddAction"
                >
                    {{ $tc('create-tag-action.buttonSaveAction') }}
                </sw-button>
            {% endblock %}
        </template>
    {% endblock %}
</sw-modal>
{% endblock %}
```

Please update the file `main.js` like this:

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './extension/sw-flow-sequence-action';
import './component/sw-flow-create-tag-modal';
```

Here is the final result

![Flow Builder create tag](/assets/flow-builder-tag.DyuKRYm7.png)

Click on [Save action] and we will get the result as below screenshot.

![Flow Builder create tag result](/assets/flow-builder-tag-result.CZMVk4rL.png)

#### Custom configuration for action without the modal [​](#custom-configuration-for-action-without-the-modal)

You don't need a modal for the configuration. It can be added automatically.

Imagine, your action is already in the action list after [the first step](#step-1-show-action-label-in-action-list)

![Choose a Flow Builder Action](/assets/flow-builder-trigger-action.DkGxRo5u.png)

First, override the `openDynamicModal` method in the plugin to check if the value matches the desired action. Then, call the `onSaveActionSuccess` directly with the configuration. After the check, call `return`.

#### JavaScript [​](#javascript)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/extension/sw-flow-sequence-action/index.js
const { Component } = Shopware;

Component.register('sw-flow-sequence-action', {
    methods: {
        openDynamicModal(value) {
            if (!value) {
                return;
            }

            const actionName = this.flowBuilderService.getActionName('CREATE_TAG');

            if (value === actionName) {
                this.selectedAction = actionName;
                const config = {
                    tagIds: {
                        'tag_id_1': 'Vip',
                        'tag_id_2': 'New Customer',
                    },
                };

                // Config can be a result from an API.
                this.onSaveActionSuccess({ config });
                return;
            }

            // handle for the rest of actions.
        },
    },
});
```

Now, after you click on the action, the new sequence will automatically be added to the action list like this:

![Flow Builder create tag result](/assets/flow-builder-tag-result.CZMVk4rL.png)

### Demo [​](#demo)

You can view the whole demo for this custom Flow Builder trigger and action below:

![Flow Builder demo](/assets/flow-builder-demo.Cq5_2Ot2.gif)

---

## Add Flow Builder trigger

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/flow/add-flow-builder-trigger.html

# Add custom flow trigger [​](#add-custom-flow-trigger)

INFO

This functionality is available starting with Shopware 6.4.6.0

## Overview [​](#overview)

In this guide, you'll learn how to create a custom flow trigger in Shopware. Triggers are used by the flow builder. This example will introduce a new custom trigger. The shop owner is then able to define what to do with the new trigger.

## Prerequisites [​](#prerequisites)

In order to add your own custom flow trigger for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html).

You also should be familiar with [Add custom event](./../event/add-custom-event.html) to know how to create an event. Please refer to the [Flow Builder concept](./../../../../../concepts/framework/flow-concept.html) for better integration later.

## Existing triggers and actions [​](#existing-triggers-and-actions)

You can refer to the [Flow reference](./../../../../../resources/references/core-reference/flow-reference.html) to read triggers and actions detail.

## Event interfaces and classes [​](#event-interfaces-and-classes)

Any event that implements one of these interfaces will be available in the trigger list of the Flow Builder module in Administration. Besides, the event will have the ability to execute the action that belongs to the interface.

* `FlowEventAware`: This interface is the base for every flow builder trigger. It provides the `availableData` and `name` of the event.
* `MailAware`: This interface provides `MailRecipientStruct` and `salesChannelId`.
* `OrderAware`: This interface provides `orderId`, which is used to add tags, sendmail or generate documents, etc...
* `CustomerAware`: This interface same as `OrderAware` but for customer, which provide `customerId`, used to add tags, remove tags, sendmail, etc...
* `UserAware`: This interface provides `userId` for all actions related to the user.
* `SalesChannelAware`: This interface simply provides `salesChannelId`.

## Create custom flow trigger [​](#create-custom-flow-trigger)

To create a custom flow trigger, firstly you have to create a plugin and install it, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html) to do it. I will create a plugin named `ExamplePlugin`. There will be an example to actually show your new trigger in the Administration.

### Create a new trigger (event) [​](#create-a-new-trigger-event)

In this example, we will name it ExampleEvent to some actions related to customers when dispatching this event. It will be placed in the directory `<plugin root>/src/Core/Checkout/Customer/Event`. Our new event has to implement Shopware\Core\Framework\Event\CustomerAware interface to enable actions requiring this Aware.

Below you can find an example implementation:

php

```shiki
// <plugin root>/src/Core/Checkout/Customer/Event/ExampleEvent.php
<?php declare(strict_types=1);

namespace Swag\ExamplePlugin\Core\Checkout\Customer\Event;

use Shopware\Core\Checkout\Customer\CustomerDefinition;
use Shopware\Core\Checkout\Customer\CustomerEntity;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\Event\CustomerAware;
use Shopware\Core\Framework\Event\FlowEventAware;
use Shopware\Core\Framework\Event\EventData\EntityType;
use Shopware\Core\Framework\Event\EventData\EventDataCollection;
use Symfony\Contracts\EventDispatcher\Event;

class ExampleEvent extends Event implements CustomerAware, FlowEventAware
{
    public const EVENT_NAME = 'example.event';

    private CustomerEntity $customer;

    private Context $context;

    public function __construct(Context $context, CustomerEntity $customer)
    {
        $this->customer = $customer;
        $this->context = $context;
    }

    public function getName(): string
    {
        return self::EVENT_NAME;
    }

    public function getCustomer(): CustomerEntity
    {
        return $this->customer;
    }

    public function getCustomerId(): string
    {
        return $this->customer->getId();
    }

    public static function getAvailableData(): EventDataCollection
    {
        return (new EventDataCollection())
            ->add('customer', new EntityType(CustomerDefinition::class));
    }

    public function getContext(): Context
    {
        return $this->context;
    }
}
```

INFO

Available starting with Shopware 6.5.0.0

From 6.5, in Flow Builder, the original event will be deprecated and we will only use a class `StorableFlow`. All event data will be stored in the `StorableFlow`, hence the `getAvailableData` function can no more be used to get data from the Flow Builder.

We have created many Aware interfaces. These Aware are the conditions to restore event data in Flow Builder via `FlowStorer` respective.

You could read here more about the [Storer](./../../../../../concepts/framework/flow-concept.html#storer-concept) concept.

| Aware interface | Storer respective |
| --- | --- |
| Shopware\Core\Content\Flow\Dispatching\Aware\ScalarValuesAware | Shopware\Core\Content\Flow\Dispatching\Storer\ScalarValuesStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\ConfirmUrlAware | Shopware\Core\Content\Flow\Dispatching\Storer\ConfirmUrlStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\ContactFormDataAware | Shopware\Core\Content\Flow\Dispatching\Storer\ContactFormDataStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\ContentsAware | Shopware\Core\Content\Flow\Dispatching\Storer\ContentsStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\ContextTokenAware | Shopware\Core\Content\Flow\Dispatching\Storer\ContextTokenStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\CustomerGroupAware | Shopware\Core\Content\Flow\Dispatching\Storer\CustomerGroupStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\CustomerRecoveryAware | Shopware\Core\Content\Flow\Dispatching\Storer\CustomerRecoveryStorer |
| Shopware\Core\Framework\Event\CustomerAware | Shopware\Core\Content\Flow\Dispatching\Storer\CustomerStorer |
| Shopware\Core\Framework\Event\MailAware | Shopware\Core\Content\Flow\Dispatching\Storer\MailStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\MessageAware | Shopware\Core\Content\Flow\Dispatching\Storer\MessageStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\NewsletterRecipientAware | Shopware\Core\Content\Flow\Dispatching\Storer\NewsletterRecipientStorer |
| Shopware\Core\Framework\Event\OrderAware | Shopware\Core\Content\Flow\Dispatching\Storer\OrderStorer |
| Shopware\Core\Content\Flow\Dispatching\Aware\OrderTransactionAware | Shopware\Core\Content\Flow\Dispatching\Storer\OrderTransactionStorer |
| Shopware\Core\Framework\Event\ProductAware | Shopware\Core\Content\Flow\Dispatching\Storer\ProductStorer |
| Shopware\Core\Framework\Event\UserAware | Shopware\Core\Content\Flow\Dispatching\Storer\UserStorer |

php

```shiki
<?php declare(strict_types=1);

namespace Swag\ExamplePlugin\Core\Checkout\Customer\Event;

use Shopware\Core\Checkout\Customer\CustomerEntity;
use Shopware\Core\Framework\Event\CustomerAware;
use Shopware\Core\Framework\Event\ShopNameAware;
use Shopware\Core\Framework\Event\EventData\EventDataCollection;
use Symfony\Contracts\EventDispatcher\Event;

class ExampleEvent extends Event implements CustomerAware, ShopNameAware
{
    public const EVENT_NAME = 'example.event';

    private CustomerEntity $customer;

    public function __construct(CustomerEntity $customer, string $shopName)
    {
        $this->customer = $customer;
        $this->shopName = $shopName;
    }

    public function getName(): string
    {
        return self::EVENT_NAME;
    }

    public function getCustomerId(): string
    {
        return $this->customer->getId();
    }

    public static function getAvailableData(): EventDataCollection
    {
        return (new EventDataCollection());
    }

    public function getShopName(): string
    {
        return $this->shopName;
    }
}
```

In the example above, to get the `customerId` and `shopName` data events, you need to store these data via `CustomerStorer` and `ShopNameStorer`.

php

```shiki
class CustomerStorer extends FlowStorer
{
	public function store(FlowEventAware $event, array $stored): array
	{
    		if (!$event instanceof CustomerAware || isset($stored['customerId'])) {
        		return $stored;
    		}

    		$stored['customerId'] = $event->getCustomerId();

    		return $stored;
	}

	public function restore(StorableFlow $storable): void
	{
    		if (!$storable->hasStore('customerId')) {
        		return;
    		}

   		$storable->setData('customer', $this->getCustomer($storable->getStore('customerId')));
	}

	private function getCustomer(string $customerId): Customer
	{
		// load customer via $customerId
		
		return $customer;
	}
}
```

php

```shiki
class ShopNameStorer extends FlowStorer
{
    public function store(FlowEventAware $event, array $stored): array
    {
        if (!$event instanceof ShopNameAware || isset($stored['shopName'])) {
            return $stored;
        }

        $stored['shopName'] = $event->getShopName();

        return $stored;
    }

    public function restore(StorableFlow $storable): void
    {
        if (!$storable->hasStore('shopName')) {
            return;
        }

        $storable->setData('shopName', $storable->getStore('shopName'));
    }
}
```

We already have Aware interfaces, but if you want to use the custom data that is not available, you can define a new Aware interface and a Storer respectively.

php

```shiki
<?php declare(strict_types=1);

namespace Swag\ExamplePlugin\Core\Checkout\Customer\Event;

use Shopware\Core\Framework\Event\CustomExampleDataAware;
use Shopware\Core\Framework\Event\EventData\EventDataCollection;
use Symfony\Contracts\EventDispatcher\Event;

class ExampleEvent extends Event implements CustomExampleDataAware
{
    public const EVENT_NAME = 'example.event';

    private string $customExampleData;

    public function __construct(string $customExampleData)
    {
        $this->customExampleData = $customExampleData;
    }

    public function getName(): string
    {
        return self::EVENT_NAME;
    }

    public function getCustomExampleData(): string
    {
        return $this->customExampleData;
    }

    public static function getAvailableData(): EventDataCollection
    {
        return (new EventDataCollection());
    }
}
```

Aware:

php

```shiki
#[IsFlowEventAware]
interface CustomExampleDataAware extends FlowEventAware
{
    public const CUSTOM_EXAMPLE_DATA = 'customExampleData';

    public function getCustomExampleData(): string;
}
```

Storer respective:

php

```shiki
class CustomExampleDataStorer extends FlowStorer
{
    public function store(FlowEventAware $event, array $stored): array
    {
        if (!$event instanceof CustomExampleDataAware || isset($stored[CustomExampleDataAware::CUSTOM_EXAMPLE_DATA])) {
            return $stored;
        }

        $stored[CustomExampleDataAware::CUSTOM_EXAMPLE_DATA] = $event->getCustomExampleData();

        return $stored;
    }

    public function restore(StorableFlow $storable): void
    {
        if (!$storable->hasStore(CustomExampleDataAware::CUSTOM_EXAMPLE_DATA)) {
            return;
        }

        $storable->setData(CustomExampleDataAware::CUSTOM_EXAMPLE_DATA, $storable->getStore(CustomExampleDataAware::CUSTOM_EXAMPLE_DATA));
    }
}
```

In Flow Actions, you can get the data easily via `getStore` and `getData`.

php

```shiki
class SendMailAction
{
	public function handleFlow(StorableFlow $flow)
	{
		$shopName = $flow->getStore('shopName');
		$customer = $flow->getData('customer');
		$customExampleData = $flow->getData('customExampleData');
	}
}
```

Take a look at the [Add Flow Builder Action](./../../../../../guides/plugins/plugins/framework/flow/add-flow-builder-action.html) section of the guide for how to use data in Flow Actions.

### Add your new event to the flow trigger list [​](#add-your-new-event-to-the-flow-trigger-list)

At this step, you need to add your new event to the flow trigger list, let us see the code below:

php

```shiki
// <plugin root>/src/Core/Checkout/Customer/Subscriber/BusinessEventCollectorSubscriber.php
<?php declare(strict_types=1);

namespace Swag\ExamplePlugin\Core\Checkout\Customer\Subscriber;

use Shopware\Core\Framework\Event\BusinessEventCollector;
use Shopware\Core\Framework\Event\BusinessEventCollectorEvent;
use Swag\ExamplePlugin\Core\Checkout\Customer\Event\ExampleEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class BusinessEventCollectorSubscriber implements EventSubscriberInterface
{
    private BusinessEventCollector $businessEventCollector;

    public function __construct(BusinessEventCollector $businessEventCollector) {
        $this->businessEventCollector = $businessEventCollector;
    }

    public static function getSubscribedEvents()
    {
        return [
            BusinessEventCollectorEvent::NAME => ['onAddExampleEvent', 1000],
        ];
    }

    public function onAddExampleEvent(BusinessEventCollectorEvent $event): void
    {
        $collection = $event->getCollection();

        $definition = $this->businessEventCollector->define(ExampleEvent::class);

        if (!$definition) {
            return;
        }

        $collection->set($definition->getName(), $definition);
    }
}
```

Please note that your subscriber has to have a higher priority point to ensure your event is added before any subscriber `BusinessEventCollectorEvent` to prevent missing awareness or action. I set 1000 for `onAddExampleEvent` action:

php

```shiki
// <plugin root>/src/Core/Checkout/Customer/Subscriber/BusinessEventCollectorSubscriber.php
public static function getSubscribedEvents()
{
   return [
      BusinessEventCollectorEvent::NAME => ['onAddExampleEvent', 1000],
   ];
}
```

And remember to register your subscriber to the container at `<plugin root>/src/Resources/config/services.xml`

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<service id="Swag\ExamplePlugin\Core\Checkout\Customer\Subscriber\BusinessEventCollectorSubscriber">
    <argument type="service" id="Shopware\Core\Framework\Event\BusinessEventCollector"/>
    <tag name="kernel.event_subscriber"/>
</service>
```

Well done, you have successfully created your own flow trigger.

### Let's check the result [​](#let-s-check-the-result)

Go to Administration page -> Settings -> Flow Builder, then click Add flow to create a new flow, search for Example Event. You could see your event is available and having actions related to the Customer likes to Add tag, Remove tag, etc...

![Flow Builder Action Example](/assets/flow-builder-action.CeXFsdNQ.png)

---

## Running actions inside transactions

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/flow/action-transactions.html

# Action transactions [​](#action-transactions)

## Overview [​](#overview)

In this guide, you will learn how to run your action code inside a transaction. This may be important for you if you want to graciously handle rollbacks in certain scenarios. We have implemented various abstractions to ease this process; however, you need to opt in.

For some more background, please see the ADR [Action Transactions](./../../../../../resources/references/adr/2024-02-11-transactional-flow-actions.html).

## Prerequisites [​](#prerequisites)

In order to make your action run inside a database transaction, you will need an existing Flow Action. Therefore, you can refer to the [Add Flow Builder Action Guide.](./add-flow-builder-action.html)

## Run your action inside a transaction [​](#run-your-action-inside-a-transaction)

All you have to do is to implement the `Shopware\Core\Content\Flow\Dispatching\TransactionalAction` interface. It does not have any methods to implement.

When your action implements the interface the Flow Dispatcher will wrap your action in a transaction. If an exception is thrown, it will be caught, the transaction will be rolled back, and an error is logged.

{plugin root}/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\CreateTagAction\Core\Content\Flow\Dispatching\Action;

use Shopware\Core\Content\Flow\Dispatching\Action\FlowAction;
use Shopware\Core\Content\Flow\Dispatching\TransactionalAction;

class CreateTagAction extends FlowAction implements TransactionalAction
{
    public function handleFlow(StorableFlow $flow): void
    {        
        //do stuff - will be wrapped in a transaction
    }  
}
```

## Force a rollback [​](#force-a-rollback)

You can also force the Flow Dispatcher to roll back the transaction by throwing an instance of `\Shopware\Core\Content\Flow\Dispatching\TransactionFailedException`. You can use the static `because` method to create the exception from another one. Eg:

{plugin root}/src/Core/Content/Flow/Dispatching/Action/CreateTagAction.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\CreateTagAction\Core\Content\Flow\Dispatching\Action;

use Shopware\Core\Content\Flow\Dispatching\Action\FlowAction;
use Shopware\Core\Content\Flow\Dispatching\TransactionalAction;

class CreateTagAction extends FlowAction implements TransactionalAction
{
    public function handleFlow(StorableFlow $flow): void
    {        
        try {
            //search for some record
            $entity = $this->repo->find(...);
        } catch (NotFoundException $e) {
            throw TransactionFailedException::because($e);
        }
    }  
}
```

## Under what circumstances will the transaction be rolled back? [​](#under-what-circumstances-will-the-transaction-be-rolled-back)

The transaction will be rollback if either of the following are true:

1. If Doctrine throws an instance of `Doctrine\DBAL\Exception` during commit.
2. If the action throws an instance of `TransactionFailedException` during execution.
3. If another non-handled exception is thrown during the action execution.

If the transaction fails, then an error will be logged.

Also, if the transaction has been performed inside a nested transaction without save points enabled (which is the default in Shopware), the exception will be rethrown. This is because the calling code knows something went wrong and is able to handle it correctly, by rolling back instead of committing. In this scenario, the connection will be marked as rollback only.

---

## Rate Limiter

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/rate-limiter/

# Rate Limiter [​](#rate-limiter)

A rate limiter controls the rate or frequency at which API requests can be made. It sets limits on the number of requests that can be processed within a specified time period, preventing excessive usage. Hence eliminating the chance of brute-force attacks. Rate limiters help maintain system stability, protect against misuse, and ensure fair resource allocation by enforcing predefined limits on the rate of incoming requests.

---

## Add Rate Limiter to API Route

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/rate-limiter/add-rate-limiter-to-api-route.html

# Add Rate Limiter to API Route [​](#add-rate-limiter-to-api-route)

## Overview [​](#overview)

In this guide you'll learn how to secure API routes with a rate limit to reduce the risk against bruteforce attacks. If you want to learn more about the configuration of the rate limiter in Shopware, have a look at the [Rate limiter](./../../../../hosting/infrastructure/rate-limiter.html) guide.

## Prerequisites [​](#prerequisites)

This guide is built upon both the [Plugin base guide](./../../plugin-base-guide.html) as well as the [Dependency injection](./../../plugin-fundamentals/dependency-injection.html) guide.

Furthermore you need an existing API route, to create a new one, head over to our [Add store API route](./../store-api/add-store-api-route.html) guide.

## Creating a new rate limit [​](#creating-a-new-rate-limit)

### Basic configuration for plugins [​](#basic-configuration-for-plugins)

First of all, we have to create a new configuration file for our rate limit. In this example we named it `rate_limiter.yaml` located in `<plugin root>/src/Resources/config/`. The root key of the configuration is the name which has to be a unique key. In this example we named it `example_route`.

Each rate limit configuration needs the following keys:

* `enabled`: Enables / Disables the rate limit for the specific route (default value: true).
* `policy`: Possible policies are `fixed_window`, `sliding_window`, `token_bucket`, `time_backoff`. For more information check the [Symfony documentation](https://symfony.com/doc/current/rate_limiter.html#rate-limiting-policies).

If you plan to configure the `time_backoff` policy, head over to [rate limiter](./../../../../hosting/infrastructure/rate-limiter.html#configuring-time-backoff-policy) guide. Otherwise, check the [Symfony documentation](https://symfony.com/doc/current/rate_limiter.html#configuration) for the other keys you need for each policy.

yaml

```shiki
// <plugin root>/src/Resources/config/rate_limiter.yaml
example_route:
    enabled: true
    policy: 'time_backoff'
```

### Extending rate limit configuration in the DI-container [​](#extending-rate-limit-configuration-in-the-di-container)

In this section we will create a small compiler pass called `RateLimiterCompilerPass`. If you are not very familiar with compiler passes, head over to the [Symfony documentation](https://symfony.com/doc/current/service_container/compiler_passes.html).

### Creating compiler pass [​](#creating-compiler-pass)

php

```shiki
// <plugin root>/src/CompilerPass/RateLimiterCompilerPass.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\CompilerPass;

use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\Yaml\Yaml;

class RateLimiterCompilerPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        /** @var array<string, array<string, string>> $rateLimiterConfig */
        $rateLimiterConfig = $container->getParameter('shopware.api.rate_limiter');

        $rateLimiterConfig += Yaml::parseFile(__DIR__ . '/../Resources/config/rate_limiter.yaml');

        $container->setParameter('shopware.api.rate_limiter', $rateLimiterConfig);
    }
}
```

As you can see, we're getting the current configuration of the rate limit from the DI-container and extend it by our `rate_limiter.yaml` and reassign it with the merged configuration.

### Adding compiler pass to the container [​](#adding-compiler-pass-to-the-container)

Now, we have to add our compiler pass to the container. This will be done by overriding the `build()` method of our `SwagBasicExample` plugin class. Important here is to use `Symfony\Component\DependencyInjection\Compiler\PassConfig::TYPE_BEFORE_OPTIMIZATION` with a higher priority, otherwise it will be built too late.

php

```shiki
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Swag\BasicExample\CompilerPass\RateLimiterCompilerPass;
use Shopware\Core\Framework\Plugin;
use Shopware\Core\Framework\Plugin\Context\InstallContext;
use Symfony\Component\DependencyInjection\Compiler\PassConfig;
use Symfony\Component\DependencyInjection\ContainerBuilder;

class SwagBasicExample extends Plugin
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $container->addCompilerPass(new RateLimiterCompilerPass(), PassConfig::TYPE_BEFORE_OPTIMIZATION, 500);
    }
}
```

## Implementing rate limit in API route [​](#implementing-rate-limit-in-api-route)

### Inject service [​](#inject-service)

After we've configured our rate limit, we want to use it in our API route. For this we need to inject the `Shopware\Core\Framework\RateLimiter\RateLimiter` service.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\Routing\StoreApiRouteScope;
use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\RateLimiter\RateLimiter;
...

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
class ExampleRoute extends AbstractExampleRoute
{
    private RateLimiter $rateLimiter;

    public function __construct(RateLimiter $rateLimiter)
    {
        $this->rateLimiter = $rateLimiter;
    }

    ...
}
```

### Call the rate limiter [​](#call-the-rate-limiter)

After we've injected the service into our API route, we can call the limiter in our route method.

To do this, we call the method `ensureAccepted` of the rate limiter which accepts the following arguments:

* `route`: Unique name of the rate limit, we defined in the configuration.
* `key`: Key we want to use to limit the request e.g., the client IP.

When calling the `ensureAccepted` method it counts the request for the key in the defined cache. If the limit has been exceeded, it throws `Shopware\Core\Framework\RateLimiter\Exception\RateLimitExceededException`.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php

#[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'])]
public function load(Request $request, SalesChannelContext $context): ExampleRouteResponse
{
    // Limit ip address
    $this->rateLimiter->ensureAccepted('example_route', $request->getClientIp());
    
    ...
}
```

### Reset the rate limit [​](#reset-the-rate-limit)

Once we've made a successful request, we want to reset the rate limit for the client. We just have to call the `reset` method as you can see below.

php

```shiki
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php

#[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'])]
public function load(Request $request, SalesChannelContext $context): ExampleRouteResponse
{
    // Limit ip address for example
    $this->rateLimiter->ensureAccepted('example_route', $request->getClientIp());
    
    // if action was successfully, reset limit 
    if ($this->doAction() === true) {
        $this->rateLimiter->reset('example_route', $request->getClientIp());
    }
    
    ...
}
```

---

## System Checks

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/system-check/

# Overview [​](#overview)

In this guide, you will learn about the system health check in Shopware. System health checks are a way to monitor the health of a system and detect failures early.

You can find the core concepts well-defined in the Concepts section of the documentation [System Checks](./../../../../../concepts/framework/system-check.html)

## Triggering System Checks [​](#triggering-system-checks)

The system checks can be invoked either through the CLI or via an HTTP API.

* By calling the endpoint `/api/_info/system-health-check`
  + the HTTP response code only indicates the status of the request, not the status of the checks
* By calling the CLI command `system:check`
  + The command returns status `0` if all checks are healthy, `1` if any check is marked as unhealthy, and `2` if the call is invalid. See [Understanding the Check Results](#understanding-the-check-results)

> The CLI command defaults to using the `cli` execution context. You can change the execution context by passing the `--context` option. The available options are `cli`, `pre-rollout`, and `recurrent`. When calling the HTTP endpoint, the execution context is always `web`

### Shopware default flow [​](#shopware-default-flow)

The default flow of Shopware system checks is done via: `Shopware\Core\Framework\SystemCheck\SystemChecker`

The `SystemChecker` class makes sure the system is working correctly by running all the registered system checks in a series. The following behavior is observed:

* Order of Checks: It runs checks in a specific order, grouped by types.
* Skipping Checks: Some checks are skipped if they aren’t allowed to run or if a major problem is found early on.
* Stopping Early: If a check in the `SYSTEM` type group is marked as `healthy = false`, it stops running more checks.

### Custom flow [​](#custom-flow)

All the system checks in Shopware are tagged with `shopware.system_check`, so you can also fetch all the checks using the Symfony service locator. and run them in your custom flow.

php

```shiki
class CustomSystemChecker
{
   public function __construct(private readonly iterable $checks)
    {
    }

    public function check(): array
    {
       # ... add your custom logic here
    }
}
```

xml

```shiki
<service id="YourNamepace\CustomSystemChecker">
    <argument type="tagged_iterator" tag="shopware.system_check"/>
</service>
```

### Custom triggers [​](#custom-triggers)

For customized triggers, you can also inject the `Shopware\Core\Framework\SystemCheck\SystemChecker` service into your service and trigger the checks programmatically.

php

```shiki
$results = $systemChecker->check(SystemCheckExecutionContext::WEB);
# or also use any custom logic you might have...
$customChecker->check();
```

## Understanding the Check Results [​](#understanding-the-check-results)

The `Shopware\Core\Framework\SystemCheck\Check\Result` class represents the outcome of a system check in Shopware. Helping further diagnosis.

All the properties in the Result class, are objective in nature, so there usually is one clear interpretation. except the `healthy` flag, which is subjective.

In principle, regardless of the actual status of the check, the `healthy` flag should be set to:

* `true` if the system can still function normally
* `false` if the system cannot function normally
* `null` if it cannot be determined

---

## Add custom check

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/framework/system-check/add-custom-check.html

# Overview [​](#overview)

In this guide, we will be building a dummy example of a custom system check that verifies if the local system has enough disk space to operate normally.

## Add a new Custom Check [​](#add-a-new-custom-check)

First, you need to add a new `LocalDiskSpaceCheck` class that extends the `Shopware\Core\Framework\SystemCheck\BaseCheck` and implement the essential categorization methods.

### Fill the categorization methods [​](#fill-the-categorization-methods)

Each check contains a set of categorization methods that help to classify the check, and determine when and where it should be executed.

php

```shiki
class LocalDiskSpaceCheck extends BaseCheck
{
    public function category(): Category
    {
        // crucial for the system to function at all. 
        return Category::SYSTEM;
    }

    public function name(): string
    {
        return 'LocalDiskSpaceCheck';
    }

    protected function allowedSystemCheckExecutionContexts(): array
    {   // a potentially long-running check, because it has an IO operation.
        return SystemCheckExecutionContext::longRunning();
    }
}
```

### Create the check logic [​](#create-the-check-logic)

The next step is to implement the actual check logic. We will check if the disk space is below a certain threshold and return the appropriate result.

php

```shiki
class LocalDiskSpaceCheck extends BaseCheck
{
    public function __construct(
        private readonly string $adapterType,
        private readonly string $installationPath,
        private readonly int $warningThresholdInMb
    )
    {
    }

    public function run(): Result
    {
        if ($this->adapterType !== 'local') {
           return new Result(name: $this->name(), status: Status::SKIPPED, message: 'Disk space check is only available for local file systems.', healthy: true)
        }
        
        $availableSpaceInMb = $this->getFreeDiskSpaceInMegaBytes();
        if ($availableSpaceInMb < $this->warningThresholdInMb) {
            return new Result(name: $this->name(), status: Status::WARNING, message: sprintf('Available disk space is below the warning threshold of %s.', $this->warningThresholdInMb), healthy: true);
        }

        return new Result(name: $this->name(), status: Status::OK, message: 'Disk space is sufficient.', healthy: true);
    }

     private function getFreeDiskSpaceInMegaBytes()
     {
        $freeSpace = disk_free_space($this->installationPath);
        $totalSpace = disk_total_space($this->installationPath);
        $availableSpace = $totalSpace - $freeSpace;

        return $availableSpace / 1024 / 1024;
     }
    ...
    ...
}
```

> An important consideration is the healthy flag, which is subjective and can vary depending on the specific shop's criteria. For example, if the disk space threshold is set high, the system can still function normally, so the healthy flag could be true. Conversely, if the threshold is too low for normal operation, the healthy flag could be false.

### Register the custom check [​](#register-the-custom-check)

Finally, you need to register the custom check as a service resource.

xml

```shiki
        <service id="%YourNameSpace%\LocalDiskSpaceCheck" >
            <argument>%shopware.filesystem.public.type%</argument>
            <argument>%shopware.filesystem.public.config.root%</argument>
            <argument>%warning_threshold_in_mb%</argument>
            <tag name="shopware.system_check"/>
        </service>
```

### Trigger the check [​](#trigger-the-check)

The system check is now part of the system check collection and will be executed when the system check is triggered. Refer to the [System Check](./) guide for more information.

---

## Administration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/

# Administration [​](#administration)

Shopware allows to extend the functionality of the Shopware administration panel, providing additional features and customization options for managing the e-commerce platform. The plugin allows businesses to tailor the administration interface to their specific needs, adding custom sections, modules, services, or functionalities to streamline their workflow and enhance the user experience. The administration plugin offers flexibility in configuring dashboards, menu structures, permissions, and settings, empowering businesses to create a customized and efficient administration experience that aligns with their unique requirements.

---

## Extending Webpack

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/advanced-configuration/extending-webpack.html

# Extending Webpack [​](#extending-webpack)

## Overview [​](#overview)

The Shopware 6 Administration uses [Webpack](https://webpack.js.org/) as a static module bundler. Normally you don't need to change the Webpack configuration, but if you need to here is how to do it.

## Extending the Webpack configuration [​](#extending-the-webpack-configuration)

The Webpack configuration can be extended by creating the file `<plugin root>/src/Resources/app/administration/build/webpack.config.js` and exporting a function from it. This will return a [webpack configuration object](https://webpack.js.org/configuration/), as seen below:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/build/webpack.config.js
const path = require('path');

module.exports = () => {
    return {
        resolve: {
            alias: {
                SwagBasicExample: path.join(__dirname, '..', 'src')
            }
        }
    };
};
```

This way, the configuration is automatically loaded and then merged with the Shopware provided webpack configuration. Configurations of plugins are **not** merged into each other. Merging is done with the [webpackMerge](https://github.com/survivejs/webpack-merge) library.

---

## Add shortcuts

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/advanced-configuration/add-shortcuts.html

# Adding Shortcuts [​](#adding-shortcuts)

## Overview [​](#overview)

Shortcuts in Shopware 6 are defined on a Component basis. This guide will show you how to add your own ones.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module and custom component. Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Configuring the Shortcuts [​](#configuring-the-shortcuts)

The following code sample will show you how to register shortcuts in your components with help of the `shortcuts` attribute.

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
const { Component } = Shopware;

Component.register('swag-basic-example', {
    
    shortcuts: {
        'SYSTEMKEY+S': {
            active() {
                return this.acl.can('product.editor');
            },
            method: 'myEditProductFunction'
        },
        ESCAPE: 'myCancelEditProductFunction'
    },

   
    methods: {
        myEditProductFunction() {
            console.log("myEditProductFunction")
        },
        myCancelEditProductFunction() {
            console.log("myCancelEditProductFunction")
        }
    }
});
```

The first keyboard shortcut reacts to the key combination of `SYSTEMKEY+S`, only if the user has the privilege `product.editor`, with the invocation of the component method with the name `myEditProductFunction`. The second keyboard shortcut defines that, upon the `ESCAPE` key being pressed, the function with the name `myCancelEditProductFunction` should be invoked.

The before mentioned `SYSTEMKEY` is `CTRL` on macOS and `ALT` on Windows, other system-keys like `CTRL` on Windows or `⌥` on macOS are not supported.

Since ACL is used in the first keyboard shortcut, you might want to learn more about ACL and how to add your own ACL rules [here](./../permissions-error-handling/add-acl-rules.html).

## More interesting topics [​](#more-interesting-topics)

* [Writing templates](./../templates-styling/writing-templates.html)
* [Adding styles](./../templates-styling/add-custom-styles.html)

---

## Add rule assignment configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/advanced-configuration/add-rule-assignment-configuration.html

# Add rule assignment configuration [​](#add-rule-assignment-configuration)

INFO

The rule assignment configuration is available from Shopware Version 6.4.8.0

## Overview [​](#overview)

You want to create a custom card in the rule assignment, where you can add or delete assignments? This guide gets you covered on this topic. Based on an example of the configuration of the `Dynamic Access` plugin, you will see how to write your configuration.

![Rule config](/assets/add-rule-assignment-configuration-0.BOZCRF7S.png)

## Prerequisites [​](#prerequisites)

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../../plugin-base-guide)

## Creating the index.js file [​](#creating-the-index-js-file)

The first step is creating a new directory like so `<plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments`. Right afterward, create a new file called `index.js` in there.

Your custom module directory isn't known to Shopware 6 yet. The entry point of your plugin is the `main.js` file. That's the file you need to change now, so that it loads your extended component. For this, simply add the following line to your `main.js` file:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-settings-rule/extension/sw-settings-rule-detail-assignments';
```

Now your module's `index.js` will be executed.

## Override the component [​](#override-the-component)

Your `index.js` is still empty now, so let's override the `sw-settings-rule-detail-assignments` component. This is technically done by calling the method `override` method of our [ComponentFactory](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/core/factory/async-component.factory.ts), which is available through our third party wrapper. This method expects a name, and a configuration for the component you want to override.

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments/index.js
Component.override('sw-settings-rule-detail-assignments', {
    // override configuration here
});
```

## Overriding the computed [​](#overriding-the-computed)

Now your plugin is overriding the `sw-settings-rule-detail-assignments` component, but currently this has no effect. In the `associationEntitiesConfig` computed property the configuration of the rule assignment is built and returned to the method which initiates the component. Because of this, you have to override this computed property, get the computed property of the original component, add your own configuration of the rule assignment and return the whole configuration array.

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments/index.js
Component.override('sw-settings-rule-detail-assignments', {
    computed: {
        associationEntitiesConfig() {
            const associationEntitiesConfig = this.$super('associationEntitiesConfig');
            associationEntitiesConfig.push(/* insert your configuration here */);
            return associationEntitiesConfig;
        },
    }
});
```

## Adding the configuration [​](#adding-the-configuration)

The configuration of the rule assignment is passed as an object and offers a wide range of options. Just have a look onto one example configuration item of the `Dynamic Access` plugin:

javascript

```shiki
// Example of a configuration item
getRuleAssignmentConfig()
{
    return [
        {
            id: 'swagDynamicAccessProducts',
            notAssignedDataTotal: 0,
            entityName: 'product',
            label: 'swag-dynamic-access.sw-settings-rule.detail.associations.productVisibility',
            criteria: () => {
                const criteria = new Criteria();
                criteria.setLimit(this.associationLimit);
                criteria.addFilter(Criteria.equals('swagDynamicAccessRules.id', this.rule.id));
                criteria.addAssociation('options.group');
                criteria.addAssociation('swagDynamicAccessRules');

                return criteria;
            },
            api: () => {
                const api = Object.assign({}, Context.api);
                api.inheritance = true;

                return api;
            },
            detailRoute: 'sw.product.detail.base',
            gridColumns: [
                {
                    property: 'name',
                    label: 'Name',
                    rawData: true,
                    sortable: true,
                    routerLink: 'sw.product.detail.prices',
                    allowEdit: false,
                },
            ],
            deleteContext: {
                type: 'many-to-many',
                entity: 'product',
                column: 'extensions.swagDynamicAccessRules',
            },
            addContext: {
                type: 'many-to-many',
                entity: 'swag_dynamic_access_product_rule',
                column: 'productId',
                searchColumn: 'name',
                criteria: () => {
                    const criteria = new Criteria();
                    criteria.addFilter(
                            Criteria.not('AND', [Criteria.equals('swagDynamicAccessRules.id', this.rule.id)]),
                    );
                    criteria.addAssociation('options.group');

                    return criteria;
                },
                gridColumns: [
                    {
                        property: 'name',
                        label: 'Name',
                        rawData: true,
                        sortable: true,
                        allowEdit: false,
                    },
                    // ...
                ],
            },
        },
    ];
}
```

Let's go through the most important entries, how to configure your rule assignment:

| Option | Description |
| --- | --- |
| id | Required identifier for the assignment, which is arbitrary but unique |
| entityName, criteria, api | Required for data loading of the assignment |
| gridColumns | To define the columns, which are shown in your assignment card. Have a look into the [data grid component](./../data-handling-processing/using-the-data-grid-component.html) for more information. |

### Provide to delete an assignment [​](#provide-to-delete-an-assignment)

If you want to provide to delete an assignment, you have to define the `deleteContext`. There are two types of the `deleteContext`. The first one is the `one-to-many` type, which link to a column of the assignment entity like this:

javascript

```shiki
// Example of a one-to-many deleteContext
deleteContext: {
    type: 'one-to-many',
    entity: 'cms_block',
    column: 'extensions.swagCmsExtensionsBlockRule.visibilityRuleId',
},
```

The other type is `many-to-many`, which has to link to the `ManyToManyAssociationField` of the extension like this:

javascript

```shiki
// Example of a many-to-many deleteContext
deleteContext: {
    type: 'many-to-many',
    entity: 'category',
    column: 'extensions.swagDynamicAccessRules',
},
```

### Provide to add an assignment [​](#provide-to-add-an-assignment)

If you want to provide to add an assignment, you have to define the `addContext`. This context has the same two types as the `deleteContext` (see above), but the `addContext` has more options to fill out, because an add assignment modal has to be configured:

javascript

```shiki
// Example of a one-to-many addContext
addContext: {
    type: 'one-to-many',
    entity: 'shipping_method',
    column: 'availabilityRuleId',
    searchColumn: 'name',
    criteria: () => {
        const criteria = new Criteria();
        criteria.addFilter(Criteria.not(
            'AND',
            [Criteria.equals('availabilityRuleId', ruleId)],
        ));

        return criteria;
    },
    gridColumns: [
        {
            property: 'name',
            label: 'Name',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'description',
            label: 'Description',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'taxType',
            label: 'Tax calculation',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'active',
            label: 'Active',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
    ],
},
```

The `addContext` needs a definition of the `gridColumns`, the `entity` and the `criteria`, like in the general configuration. Also, the context needs the `column` of the assignment and the `searchColumn` of the assigned entity.

A context of the `many-to-many` type would look like this:

javascript

```shiki
// Example of a many-to-many addContext
addContext: {
    type: 'many-to-many',
    entity: 'swag_dynamic_access_category_rule',
    column: 'categoryId',
    searchColumn: 'name',
    association: 'swagDynamicAccessRules',
    criteria: () => {
        const criteria = new Criteria();
        criteria.addFilter(Criteria.equals('parentId', null));

        return criteria;
    },
    gridColumns: [
        // Definition of columns
    ],
},
```

Beside the properties of a `one-to-many` type you have to define the `association` with the name of the `ManyToManyAssociationField`.

## Further reading [​](#further-reading)

For more other information, refer to [Add custom rules](./../../framework/rule/add-custom-rules.html).

---

## Modify dynamic product groups blacklist

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/advanced-configuration/modify-blacklist-for-dynamic-product-groups.html

# Modify dynamic product groups blacklist [​](#modify-dynamic-product-groups-blacklist)

## Overview [​](#overview)

The module "Dynamic product groups" includes a condition builder to properly configure your dynamic product groups. You might have noticed though, that this condition builder does not show all available properties, since some of them are blacklisted in the code, such as e.g. `createdAt`.

In this guide you'll get two quick examples on how to either add new properties to this blacklist or even remove properties from the blacklist, so they're actually shown in the Administration and thus can be used.

## Prerequisites [​](#prerequisites)

This guide **will not** explain in detail how to override an existing component. For this guide you'll have to extend the component [sw-product-stream-field-select](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js) though, since it's the one [actually checking for the properties in the computed property options](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js#L41).

An example on how to override a component can be found [here](./../module-component-management/customizing-components.html).

## Adding properties to blacklist [​](#adding-properties-to-blacklist)

As already mentioned in the prerequisites, the check for properties in the blacklist is done in the computed property `options`. Therefore you'll have to make sure your modifications are done **before** the check happens.

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToGeneralBlacklist(['deliveryTimeId']);
            return this.$super('options');
        }
    }
});
```

This example will simply add the property `deliveryTimeId` to the blacklist, so it's not configurable using the Administration anymore. There are also nested properties, so called 'entity properties', which are selectable once you've chosen a property such as `Categories`. Those entity properties can also be added to the blacklist by using the method `addToEntityBlacklist` instead:

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToEntityBlacklist('category', ['breadcrumb']);
            return this.$super('options');
        }
    }
});
```

This example would forbid the usage of `breadcrumb` from the `category` entity.

## Removing properties from the blacklist [​](#removing-properties-from-the-blacklist)

Most likely you'd want to do the opposite and enable properties by removing entries from the blacklist. This can be done exactly like adding properties to the blacklist:

* Remove a property from the "general blacklist", which is the first dropdown
* Remove from the "entity blacklist" which contains the properties of the previously selected entity.

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.removeFromGeneralBlacklist(['createdAt']);
            this.conditionDataProviderService.removeFromEntityBlacklist('category', ['path']);
            return this.$super('options');
        }
    }
});
```

This example enables both the general `createdAt` property, as well as the category property `path`.

---

## Adding Mixins

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/mixins-directives/add-mixins.html

# Adding Mixins [​](#adding-mixins)

## Overview [​](#overview)

This documentation chapter will cover how to add a new Administration mixin for your plugin. In general, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. If you want an overview over the shopware provided mixins look at them here: [Using Mixins](./using-mixins.html).

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. As stated before mixins in Shopware are basically the same as in Vue, so you should have read their [documentation](https://v2.vuejs.org/v2/guide/mixins.html?redirect=true) on them first.

## Register a new Mixin [​](#register-a-new-mixin)

For this example, we'll just use the example mixin from the [VueJS documentation](https://v2.vuejs.org/v2/guide/mixins.html?redirect=true) and adjust it to be used in Shopware.

Mixins in Shopware have to be registered in the mixin registry via the `Mixin.register` function to be available everywhere in the Administration.

Converting the Vue mixin to be used in Shopware looks like the example seen below:

javascript

```shiki
// <administration root>/mixins/swag-basic-example.js
// get the Mixin property of the shopware object
const { Mixin } = Shopware;

// give the mixin a name and feed it into the register function as the second argument
Mixin.register('swag-basic-mixin', {
    created: function () {
        this.hello()
    },
    methods: {
        hello: function () {
            console.log('hello from mixin!')
        }
    }
});
```

## Importing the Mixin in the Plugin [​](#importing-the-mixin-in-the-plugin)

Now that we have registered the mixin, we need to import it *before importing our components* in the `main.js` file.

javascript

```shiki
// <administration root>/src/main.js
import '<administration root>/mixins/swag-basic-example.js'
    
// importing components...
```

## Using the Mixin [​](#using-the-mixin)

After registering our mixin under a name, we can get it from the registry with the `Mixin.getByName` function and inject it into our component as seen below.

javascript

```shiki
// <administration root>/components/swag-basic-example/index.js
const { Component, Mixin } = Shopware;

Component.register('swag-basic-example', {

    mixins: [
        Mixin.getByName('swag-basic-mixin')
    ],
});
```

This can also be done with Shopware provided mixins, learn more about them here: [Using Mixins](./using-mixins.html)

## More interesting topics [​](#more-interesting-topics)

* [Adding filters](./../services-utilities/add-filter.html)
* [Using utility functions](./../services-utilities/using-utils.html)

---

## Using Mixins

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/mixins-directives/using-mixins.html

# Using Mixins [​](#using-mixins)

## Overview [​](#overview)

This documentation chapter will cover how to use an existing Administration mixin in your plugin. Generally, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. As stated before mixins in Shopware are basically the same as in Vue, so you should have read their [documentation](https://v2.vuejs.org/v2/guide/mixins.html?redirect=true) on them first.

## Finding a mixin [​](#finding-a-mixin)

The Shopware 6 Administration comes with a few predefined [mixins](./../../../../../resources/references/administration-reference/mixins.html)

If you want to learn how to create your own mixin look at this guide: [Creating mixins](./add-mixins.html)

## Using the Mixin [​](#using-the-mixin)

After we've found the mixin we need, we can get it from the registry with the `Mixin.getByName` function and inject it into our component as seen below. In this example we'll use the notification mixin, which is useful for creating notifications visible to the user in the Administration.

javascript

```shiki
// <administration root>/components/swag-basic-example/index.js
const { Component, Mixin } = Shopware;

Component.register('swag-basic-example', {

    mixins: [
        Mixin.getByName('notification')
    ],

    methods: {
        greet: function () {
            this.createNotificationSuccess({ title: 'Greetings' })
        }
    }
});
```

---

## Using Directives

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/mixins-directives/adding-directives.html

# Using Directives [​](#using-directives)

## Overview [​](#overview)

Directives in the Shopware 6 Administration are essentially the same as in any other Vue application. This guide will teach you how to register your directives on a global and on a local scope.

Learn more about Vue Directives in their documentation:

[Custom Directives | Vue.js](https://vuejs.org/v2/guide/custom-directive.html)

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module. Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Registering a directives globally [​](#registering-a-directives-globally)

Directives can be registered globally via the [Shopware Objects](./../data-handling-processing/the-shopware-object.html) `register` helper function as seen below:

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/directive/focus.js
const { Directive } = Shopware;

Directive.register('focus', {
    // when the bound element is inserted into the DOM...
    inserted: function (el) {
        // Focus the element
        el.focus();
    }
});
```

As you might have seen, this is the exact same example as in the [Vue documentation](https://vuejs.org/v2/guide/custom-directive.html). Now, the only thing that's left is importing this file in your `main.js`. Then you can use it in the same way as you would do a normal Vue directive.

## Registering a directives locally [​](#registering-a-directives-locally)

Registering directives locally is exactly the same as you're familiar with in Vue. The code snippet below registers the example from the [Vue documentation](https://vuejs.org/v2/guide/custom-directive.html) locally to the `swag-basic-example` component.

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
Shopware.Component.register('swag-basic-example', {

    directives: {
        focus: {
            // When the bound element is inserted into the DOM...
            inserted: function (el) {
                // Focus the element
                el.focus();
            }
        }
    }

});
```

As mentioned before, directives can be used as in any other Vue application, after they are registered:

html

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/swag-basic-example.html.twig
<input type="text" v-focus="">
```

WARNING

Make sure the directive you are trying to access is actually in your components scope, either by registering the directive globally or locally to a component.

---

## Adding permissions

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/permissions-error-handling/add-acl-rules.html

# Adding permissions [​](#adding-permissions)

## Overview [​](#overview)

This guide will teach you how to add Access Control Lists to the Shopware 6 Administration. Access Control Lists or ACL in Shopware ensure that you can create individual roles. These roles have finely granular rights, which every shop operator can set up for themselves. They can be assigned to users.

As an example, let's take a look at a role called 'Editor'. We would assign this role rights to edit products, categories and manufacturers. Now, every user who is a 'Editor' would be able to see and edit the specific areas which are defined in the role.

This documentation chapter will cover the following topics:

* What is an admin privilege
* How to register new admin privileges for your plugin
* How to protect your plugin routes
* How to protect your menu entries
* How to add admin snippets for your privileges
* How you can check in your module at any place if the user has the required rights

Note: ACL Rules in the Administration can be circumnavigated by making direct API calls to your backend.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. A basic understanding of the [vue router](https://router.vuejs.org/) is also required. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Admin privileges [​](#admin-privileges)

Admin privileges are higher-level permissions that are always determined by an explicit identifier. This is made up of a 'key' and the 'role', connected by a dot: `.`.

A distinction is made here between normal `permissions` and `additional_permissions`. Let's start with the normal permissions.

### Normal permissions [​](#normal-permissions)

![Permissions GUI](/assets/permissions-gui.BZcfBdsu.png)

`permissions`:

* Key: `product`
* Role: `viewer`
* Identifier (Key + Role): `product.viewer`

The key describes the higher-level admin privilege. For normal `permissions` this is usually the module name, `product` in this case. Other keys could be for example `manufacturer`, `shopping_experiences` or `customers`. The key is used to group the admin privileges, as seen in the picture above.

The role indicates which authorization is given for the key. So four predefined roles are available for the normal `permissions`:

* `viewer`: The viewer is allowed to view entities
* `editor`: The editor is allowed to edit entities
* `creator`: The Creator is allowed to create new entities
* `deleter`: The Deleter is allowed to delete entities

It is important to note that these combinations are not API permissions. They are only intended to enable, disable, deactivate or hide certain elements in the Administration.

For each admin privilege, the needed entity privileges need to be assigned. Depending on the admin privileges, these can be much more complex. This means that for example if a user should be allowed to view reviews, then they also have to be allowed to view customers, products and sales channels.

### Additional permissions [​](#additional-permissions)

In addition to the normal `permissions`, which represent CRUD functionality, there are also `additional_permissions`. These are intended for all functions that cannot be represented by CRUD.

![Additional permissions GUI](/assets/additionalPermissions-gui.Db5Cgly7.png)

The `additional_permissions` have their own card below the normal permissions grid. An example for `additional_permissions` would be: "clearing the cache". This is an individual action without CRUD functionalities. The key is still used for grouping. Therefore the role can be individual and does not have to follow the scheme.

`additional_permissions`:

* Key: `system`
* Role: `clear_cache`
* Identifier (Key + Role): `system.clear_cache`

## Register admin privilege [​](#register-admin-privilege)

The privilege service is used to handle privileges in the Administration. Those privileges will then be displayed in the Users & Permissions module under the roles.

Privileges can be added or extended with the Method `addPrivilegeMappingEntry` of the privilege service:

| Property | Description |
| --- | --- |
| category | Where the privilege should be visible in the `permissions` grid or in the `additional_permissions` |
| parent | For nesting and gaining a better overview, you can add a parent key. If the privilege does not have a parent then use `null`. |
| key | All privileges with the same key will be grouped together. For normal `permissions` each role will be in the same row. |
| roles | When category is `permissions`: Use `viewer`, `editor`, `creator` and `deleter`. |
|  | When category is `additional_permissions`: Use a custom key because the additional permissions don´t enforce a structure. |

Each role in roles:

| Property | Description |
| --- | --- |
| privileges | You need to add all API permissions here which are required for an working admin privilege. The structure is `entity_name:operation`, e.g. 'product:read'. |
| dependencies | In some cases it is necessary to automatically check another role. To do this, you need to add the identifier, e.g. `product.viewer`. |

Here's an example how this can look like for the review functionality in the Administration:

javascript

```shiki
Shopware.Service('privileges')
    .addPrivilegeMappingEntry({
        category: 'permissions',
        parent: 'catalogues',
        key: 'review',
        roles: {
            viewer: {
                privileges: [
                    'product_review:read',
                    'customer:read',
                    'product:read',
                    'sales_channel:read'
                ],
                dependencies: []
            },
            editor: {
                privileges: [
                    'product_review:update'
                ],
                dependencies: [
                    'review.viewer'
                ]
            },
            creator: {
                privileges: [
                    'product_review:create'
                ],
                dependencies: [
                    'review.viewer',
                    'review.editor'
                ]
            },
            deleter: {
                privileges: [
                    'product_review:delete'
                ],
                dependencies: [
                    'review.viewer'
                ]
            }
        }
    });
```

### Adding new, normal permissions [​](#adding-new-normal-permissions)

You could use the service at any point in your code. However, it's important that it will be called before the user goes to the roles detail page. For convenience, we recommend this pattern:

text

```shiki
- <plugin root>/src/Resources/app/administration/src/<your-component>/
    - acl
        - index.js -> contains permission
    - ...
    - index.js -> import './acl'
```

Now you can use the method `addPrivilegeMappingEntry` to add a new entry:

To add a new mapping for your custom key use the following approach:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/<your-component>/acl/index.js

Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'your_key',
    roles: {
        viewer: {
            privileges: [],
            dependencies: []
        },
        editor: {
            privileges: [],
            dependencies: []
        },
        creator: {
            privileges: [],
            dependencies: []
        },
        deleter: {
            privileges: [],
            dependencies: []
        }
    }
});
```

### Extending existing normal permissions [​](#extending-existing-normal-permissions)

Adding privileges to an existing key can be done like this:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/acl-override/index.js

Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'product',
    roles: {
        viewer: {
            privileges: ['plugin:read']
        },
        editor: {
            privileges: ['plugin:update']
        },
        newrole: {
            privileges: ['plugin:write']
        }
    }
});
```

Note: This file has to be imported in the `main.js` file which has to be placed in the `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

### Register additional permissions [​](#register-additional-permissions)

To add privileges to the card `additional_permissions` you need to set `additional_permissions` in the property category. The main difference to normal permissions is that you can choose every role key you want.

Here's an example for `additional_permissions`:

javascript

```shiki
Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'additional_permissions',
    parent: null,
    key: 'system',
    roles: {
        clear_cache: {
            privileges: ['system:clear:cache'],
            dependencies: []
        }
    }
});
```

Here, the key is `system` to group the permission together with other system specific permissions. However, you can feel free to add your own names here.

## Get permissions from other privilege mappings [​](#get-permissions-from-other-privilege-mappings)

In case you have many dependencies which are the same as in other modules, you can import them here. This can be useful if you have components in your module which have complex privileges. Some examples can be found in the rule builder or the media module. You can get these privileges with the method `getPrivileges` of the service.

See this example here:

javascript

```shiki
Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'product',
    roles: {
        viewer: {
            privileges: [
                'product.read',
                Shopware.Service('privileges').getPrivileges('rule.viewer')
            ],
            dependencies: []
        }
    }
})
```

Now all users with the privilege `product.viewer` automatically have access to all privileges from the `rule.viewer`.

Important: The user still has no access to the module itself in the Administration. This means that the example above doesn't give a user access to the `rule` module.

## Protect your plugin routes [​](#protect-your-plugin-routes)

It's easy to protect your routes for users without the appropriate privileges. Just add `privilege` to the `meta` property in your route:

javascript

```shiki
Module.register('your-plugin-module', {
    routes: {
        detail: {
            component: 'your-plugin-detail',
            path: 'your-plugin',
            meta: {
                privilege: 'your_key.your_role' // e.g. 'product.viewer'
            }
        }    
    }
});
```

## Protect your plugin menu entries [​](#protect-your-plugin-menu-entries)

Similar to the routes, you can to add the property `privilege` to your navigation settings to hide it:

javascript

```shiki
Module.register('your-plugin-module', {
    navigation: [{
        id: 'your-plugin',
        ...,
        privilege: 'your_key.your_role' // e.g. product.viewer
    }]
});
```

or in the settings item:

javascript

```shiki
Module.register('your-plugin-module', {
    settingsItem: [{
        group: 'system',
        to: 'sw.your.plugin.detail',
        privilege: 'your_key.your_role' // e.g. product.viewer
    }]
});
```

## Add snippets for your privileges [​](#add-snippets-for-your-privileges)

To create translations for the labels of the permissions you need to add snippet translations. The path is created automatically for you:

For group titles:

text

```shiki
sw.privileges.${category}.${key}.label
// e.g. sw.privileges.permissions.product.label
// e.g. sw.privileges.additional_permissions.system.label
```

For specific roles (only needed in `additional_permissions`):

text

```shiki
sw.privileges.${category}.${key}.${role_key} 
// e.g. sw.privileges.additional_permissions.system.clear_cache
```

Just add the snippets to your snippets file:

json

```shiki
{
  "sw-privileges": {
    "permissions": {
      "review": {
        "label": "Reviews"
      }
    },
    "additional_permissions": {
      "system": {
        "label": "System",
        "clear_cache": "Clear cache"
      }
    }
  }
}
```

## Use the privileges in any place in your plugin [​](#use-the-privileges-in-any-place-in-your-plugin)

You can use the `acl` service to check if the user has the correct privileges to view or edit things, regardless of location in your app. The method you need is `acl.can(identifier)`: It checks automatically if the user has admin rights or the privilege for the identifier.

You can use the global Shopware object (`Shopware.Service('acl')`) or inject the service in your component:

javascript

```shiki
Shopware.Component.register('your-plugin-component', {
    template,

    inject: ['acl'],

    ...
});
```

With the injection, you can use the service functionality everywhere in your component.

Example in a method:

javascript

```shiki
Shopware.Component.register('your-plugin-component', {
    template,

    inject: ['acl'],

    methods: {
        allowSaving() {
            return this.acl.can('sales_channel.creator');
        }    
    }
});
```

Below is an example to hide the element if the user has not the right privilege:

html

```shiki
<button v-if="acl.can('review.editor')">
</button>
```

For example you could disable elements if the user has not the right privilege to use them and inform the user with a tooltip that a privilege is missing. To achieve this, you can use the global snippet path:

html

```shiki
<button @click="saveProduct"
        :disabled="!acl.can('review.editor')"
        v-tooltip="{
            message: $tc('sw-privileges.tooltip.warning'),
            disabled: acl.can('review.editor'),
            showOnDisabledElements: true
        }"
></button>
```

## Protect your shortcuts [​](#protect-your-shortcuts)

You can replace the String value with an object which contains the method with the name `active` which then returns a boolean or just the property `active`as boolean. In our case we need a function to check if the user has the privilege required to use the shortcut.

javascript

```shiki
Module.register('your-plugin-module', {
    shortcuts: {
        'SYSTEMKEY+S': {
            active() {
                return this.acl.can('product.editor');
            },
            method: 'onSave'
        },
        ESCAPE: 'onCancel'
    },
});
```

## Add your custom privileges [​](#add-your-custom-privileges)

To make sure your custom privileges are additionally added to existing roles, override the `enrichPrivileges` method and return a list of your custom privileges. This method should return an array with the technical role name as key, while the privileges should be the array value. An event subscriber will add the plugins custom privileges at runtime.

php

```shiki
<?php declare(strict_types=1);

namespace SwagTestPluginAcl;

use Shopware\Core\Framework\Plugin;

class SwagTestPluginAcl extends Plugin
{
    public function enrichPrivileges(): array
    {
        return [
            'product.viewer' => [
                'my_custom_privilege:read',
                'my_custom_privilege:write',
                'my_other_custom_privilege:read',
                // ...
            ],
            'product.editor' => [
                // ...
            ],
        ];
    }
}
```

---

## Adding error handling

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/permissions-error-handling/add-error-handling.html

# Adding error handling [​](#adding-error-handling)

​

## Overview [​](#overview)

The Shopware 6 Administration stores API errors in the [Vuex store](https://vuex.vuejs.org/). There they are centrally accessible to your components, with a flat data structure looking like this:

text

```shiki
(state)
 |- entityNameA
    |- id1
        |- property1
        |- property2
        ...
    |- id2
        |- property1
        |- property2
        ...
 |- entityNameB
   ...
```

In this guide you will learn how to access this error store directly or via one of the provided helper functions. ​

## Read errors from the store [​](#read-errors-from-the-store)

​ Errors can be read from the store by calling the getter method `getApiErrorFromPath`. ​

javascript

```shiki
function getApiErrorFromPath (state) => (entityName, id, path)
```

​ In there, the parameter `path` is an `array` representing the nested property names of your entity.

Also we provide a wrapper which can also handle nested fields in object notation, being much easier to use for scalar fields: ​

javascript

```shiki
function getApiError(state) => (entity, field)
```

​ For example, an empty product name would result in an error with the path `product.name`, instead of having the array `['product', 'name']` present.

In your Vue component, use computed properties to avoid flooding your templates with store calls. ​

javascript

```shiki
computed: {
    propertyError() {
        return this.$store.getters.getApiError(myEntity, 'myFieldName');
    },
    nestedpropertyError() {
        return this.$store.getters.getApiError(myEntity, 'myFieldName.nested');
    }
}
```

Those computed properties can then be used in your templates the familiar way:

html

```shiki
<div>
    <sw-field ... :error="propertyError"></sw-field>
</div>
```

​

### The mapErrors Service [​](#the-maperrors-service)

​ Like every Vuex mapping, fetching the errors from the store may be very repetitive and error-prone. Because of this we provide you an Vuex like mapper function: ​

javascript

```shiki
mapPropertyErrors(subject, properties)
```

​ Here, the `subject` parameter is the entity name (not the entity itself) and `properties` is an array of the properties you want to map. You can spread its result to create computed properties in your component. The functions returned by the mapper are named like a camelCase representation of your input, suffixed with `Error`.

This is an example from the `sw-product-basic-form` component: ​

javascript

```shiki
const { mapPropertyErrors } = Shopware.Component.getComponentHelper();

Component.register('sw-product-basic-form', {
    computed: {
        ...mapPropertyErrors('product', [
            'name',
            'description',
            'productNumber',
            'manufacturerId',
            'active',
            'markAsTopseller'
        ])
    }
})
```

Which then are bound to the inputs like this:

html

```shiki
<sw-field type="text" v-model="product.name" :error="productNameError">
```

​

### Error configuration for pages [​](#error-configuration-for-pages)

​ When working with nested views, you need a way to tell the user that an error occurred on another view, e.g in another `tab`. For this you can write a config for your `sw-page` component which looks like seen below: ​

json

```shiki
{
  "sw.product.detail.base": {
    "product": [
      "taxId",
      "price",
      "stock",
      "manufacturerId",
      "name"
    ]
  },
  "sw.product.detail.cross.selling": {
    "product_cross_selling": [
      "name",
      "type",
      "position"
    ]
  }
}
```

​ This can then directly imported and used in the `mapPageError` computed property:

javascript

```shiki
import errorConfiguration from './error.cfg.json';

const { mapPageErrors } = Shopware.Component.getComponentHelper();

Shopware.Component.register('sw-product-detail', {
    computed: {
        ...mapPageErrors(errorConfiguration),
    }
}
```

This makes it possible to indicate if one or more errors exists, in another view or a tab:

html

```shiki
<sw-tabs
    :hasError="swProductDetailBaseError">
</sw-tabs>
```

---

## Add custom route

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/routing-navigation/add-custom-route.html

# Add custom route [​](#add-custom-route)

Routes in the Shopware 6 Administration are essentially the same as in any other [Vue Router](https://router.vuejs.org). This guide will teach you the basics of creating your very first route from scratch.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Configuring the route [​](#configuring-the-route)

So lets start with configuring our own route. In order to add routes to a module you simply add the `routes` property, which expects an object containing multiple route configuration objects. Each route configuration object needs to have a `name`, which is set using the configuration object's key. Furthermore, we need to set a component and a path: A route points to a [component](https://vuejs.org/guide/essentials/component-basics.html) using the key `component`, which targets the component to be shown when this route is requested. The key `path` represents the actual path, that's going to be used for this route. Do not get confused just because it is equal to the route name in the first route.

Now, our route should look like this:

javascript

```shiki
// routes: {
//     nameOfTheRoute: {
//         component: 'example',
//         path: 'actualPathInTheBrowser'
//     }
// }
routes: {
    overview: {
        component: 'sw-product-list',
        path: 'overview'
    },
},
```

Routes can be matched by name and path. This configuration results in this route's full name being `custom.module.overview` and the URL being `/custom/module/overview` relative to the Administration's default URL. The routes full name is a combination of the module's id and the name of the item inside the `routes` object. In this case the module's id is `custom-module` (Notice that all dashes are automatically replaced by dots in the final route name).

Usually you want to render your custom component here, which is explained [here](./../module-component-management/add-custom-component.html). But that is not all! Routes can have parameters, to then be handed to the components being rendered and much more. Learn more about what the Vue Router can do in its official [Documentation](https://router.vuejs.org/guide/essentials/dynamic-matching.html#reacting-to-params-changes).

## Meta data and dynamic parameters [​](#meta-data-and-dynamic-parameters)

Let's extend this example:

javascript

```shiki
Shopware.Module.register('swag-example', {
    color: '#ff3d58',
    icon: 'default-shopping-paper-bag-product',
    title: 'My custom module',
    description: 'Manage your custom module here.',

    routes: {
        overview: {
            component: 'swag-example-list',
            path: 'overview'
        },
        // This is our second route
        detail: {
            component: 'sw-example-detail',
            path: 'detail/:id',
            meta: {
                parentPath: 'swag.example.list'
            }
        }
    },
});
```

This second route, `detail`, comes with a dynamic parameter as part of the route. When you want to open a detail page of an example, the route also has to contain the ID of the example, in the `path` of `detail`:

javascript

```shiki
path: 'detail/:id'
```

Furthermore, the `detail` route comes with another new configuration, which is called `meta`. As the name suggests, you can use this object to apply more meta information for your route. In this case the `parentPath` is filled. Its purpose is to link the path of the actual parent route. In the Administration, this results in a "back" button on the top left of your module when being on the detail page. This button will then link back to the list route and the icon defined earlier will also be used for this button.

You might want to have a closer look at the `parentPath` value though. Its route follows this pattern: `<bundle-name>.<name of the route>`

See in this example:

javascript

```shiki
...
   meta: {
       parentPath: 'swag.example.list'
   }
...
```

The `bundle-name` is separated by dots instead of dashes here though. The second part is the **name** of the route, the key of the route configuration that is. Thus the path to the `list` route is `swag.example.list`. The same applies for the `create` route.

## More interesting topics [​](#more-interesting-topics)

* [Adding a custom service](./../services-utilities/add-custom-service.html)
* [Customizing a module](./../module-component-management/customizing-modules.html)
* [Adding permissions](./../permissions-error-handling/add-acl-rules.html)

---

## Add menu entry

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/routing-navigation/add-menu-entry.html

# Add menu entry [​](#add-menu-entry)

## Overview [​](#overview)

When it comes to the module configuration, the menu entry is one of the most important things to set up. It serves to open your module.

## Prerequisites [​](#prerequisites)

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../../plugin-base-guide)

Especially if you want to add a new page for an own module, you should consider to look at the process on how to add a custom module first.

[Add custom module](../module-component-management/add-custom-module)

## Creating a simple menu entry [​](#creating-a-simple-menu-entry)

This menu entry can be defined in your module configuration. Remember, your module configuration looks as seen below:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-plugin', {
    // configuration here
});
```

In order to create your own menu entry, you need to use the `navigation` key: It takes an array of objects, each one configuring a route connected to your module.

So let's define a menu entry using the `navigation` key in your module configuration. It takes an array of objects, each one configuring a route connected to your module:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
navigation: [{
    label: 'CustomModule',
    color: '#ff3d58',
    path: 'swag.custommodule.list',
    icon: 'default-shopping-paper-bag-product',
    parent: 'sw-catalogue',
    position: 100
}]
```

As you see, you are able to configure several things in there:

| Configuration | Description |
| --- | --- |
| label | The label to be shown with this menu entry. |
| color | This is the theme color of the module. This color may differ from the module's color itself. |
| path | Which one of your configured routes shall be used when clicking this menu entry? The path is composed of the module id and the path name. Dashes become dots, for example module 'swag-example' and path 'index' become 'swag.example.index'. |
| icon | Also you can set a separate icon, which can make sense e.g. when having multiple menu entries for a single module, such as a special icon for 'Create bundle'. This example does not have this and it's only going to have a single menu entry, so use the icon from the main module here. |
| position | The position of the menu entry. The higher the value, the more likely it is that your menu entry appears in the bottom. |

Of course there's more to be configured here, but more's not necessary for this example.

## Menu entry in category [​](#menu-entry-in-category)

Due to UX reasons, we're not supporting plugin modules to add new menu entries on the first level of the main menu. Please use the "parent" property inside your navigation object to define the category where you want your menu entry will be appended to. Your navigation entry will also have to have an `id` to show up in the rendered navigation:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
navigation: [{
    id: 'swag-custommodule-list',
    label: 'CustomModule',
    color: '#ff3d58',
    path: 'swag.custommodule.list',
    icon: 'default-shopping-paper-bag-product',
    parent: 'sw-catalogue',
    position: 100
}]
```

You can find the parent id at the `index.js` file in each module folder. You can see the property `navigation` in the `Module.register` method. The id here can be used as the parent key.

## Nesting menu entries [​](#nesting-menu-entries)

The parent can be on any level because the menu supports infinite depth nesting. For example, if `sw-manufacturer` were taken as the `parent`, the menu item would be present on the third level. So what's important here is that the configured parent defines where the menu entry will take place.

INFO

If you're planning to publish your plugin to the Shopware Store keep in mind we're rejecting plugins which have created their own menu entry on the first level.

---

## Override existing routes

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/routing-navigation/overriding-routes.html

# Override existing routes [​](#override-existing-routes)

## Overview [​](#overview)

In the `Administration` core code, each module is defined in a directory called `module`. Modules define routes which can be extended with `routeMiddleware`. To see what else you can customize in existing modules, have a look at this [guide](./../module-component-management/customizing-modules.html)

A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) and the [Vue Router](https://router.vuejs.org/). However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further a basic understanding of what modules are is also required, learn more about them [here](./../module-component-management/add-custom-module.html)

## Applying the override [​](#applying-the-override)

At some point you might want to override or change existing routes, for example, to change the privileges required for a route or entirely replace it with your own.

This is done by creating a new module and implementing a `routeMiddleware`. You can add those changes to your `main.js` file, which could then look like this:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
Module.register('my-new-custom-route', {
    routeMiddleware(next, currentRoute) {
        if (currentRoute.name === 'sw.product.detail') {

            const childIndex = currentRoute.children.findIndex(child => child.name === 'sw.product.detail.base');

            currentRoute.children[childIndex] = {
                name: 'sw.product.detail.base',
                component: 'sw-product-detail-base',
                path: 'base',
                meta: {
                    parentPath: 'sw.product.index',
                    privilege: 'product.editor'
                }
            }
        }
        next(currentRoute);
    }
});
```

This `routeMiddleware` changes the required privileges for the `sw.product.detail.base` route from `product.viewer` to `product.editor`. The rest of the route configurations stays the same in this example.

If you want to learn more about ACL take a look at this [guide](./../permissions-error-handling/add-acl-rules.html) and if you want to learn everything about Administration routes, head over to this [guide](./../routing-navigation/add-custom-route.html)

---

## Add tab to existing module

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/routing-navigation/add-new-tab.html

# Add tab to existing module [​](#add-tab-to-existing-module)

## Overview [​](#overview)

You want to create a new tab in the Administration? This guide gets you covered on this subject. A realistic example would be adding a new association for an entity, which you want to configure on a separate tab on the entity detail page.

## Prerequisites [​](#prerequisites)

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our plugin base guide:

[Plugin Base Guide](../../plugin-base-guide)

In the course of this guide, you need to create a custom route. If you want to learn on how to create a custom component, please refer to the guide on it:

[Add custom route](add-custom-route)

Also, we will use a small, custom component to fill our custom tab. In order to get used to that, it might come in handy to read the corresponding guide first:

[Add custom component](../module-component-management/add-custom-component)

INFO

### Please remember [​](#please-remember)

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be found by Shopware 6. So please use the file accordingly and refer to the [plugin base guide](./../../plugin-base-guide.html) for more details.

## Creating a custom tab [​](#creating-a-custom-tab)

### Find the block to extend [​](#find-the-block-to-extend)

For this guide, we'll think about the following example: The product detail page is extended by a new tab, which then only contains a 'Hello world!'. In order to refer to this example, let's have a look at the twig code of the product detail page found here:

[shopware/shopware - sw-product-detailhtml.twig @ GitHub](https://github.com/shopware/shopware/blob/552675ba24284dec2bb01c2107bf45f86b362550/src/Administration/Resources/app/administration/src/module/sw-product/page/sw-product-detail/sw-product-detail.html.twig\#L120)

Let's imagine your first goal is to create a new tab on the product detail page. Having a look at the template, you might find the block `sw_product_detail_content_tabs`, which seems to contain all available tabs. It starts by creating a new `<sw-tabs>` element to contain all the tabs available. Here you can see excerpt of this block:

twig

```shiki
// platform/src/Administration/Resources/app/administration/src/module/sw-product/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs %}
    <sw-tabs class="sw-product-detail-page__tabs" v-if="productId">
        {% block sw_product_detail_content_tabs_general %}
            <sw-tabs-item
                class="sw-product-detail__tab-general"
                :route="{ name: 'sw.product.detail.base', params: { id: $route.params.id } }"
                :hasError="swProductDetailBaseError"
                :title="$tc('sw-product.detail.tabGeneral')">
                {{ $tc('sw-product.detail.tabGeneral') }}
            </sw-tabs-item>
        {% endblock %}

        ...

        {% block sw_product_detail_content_tabs_reviews %}
            <sw-tabs-item
                class="sw-product-detail__tab-reviews"
                :route="{ name: 'sw.product.detail.reviews', params: { id: $route.params.id } }"
                :title="$tc('sw-product.detail.tabReviews')">
                {{ $tc('sw-product.detail.tabReviews') }}
            </sw-tabs-item>
        {% endblock %}
    </sw-tabs>
{% endblock %}
```

Unfortunately, you cannot use the block mentioned above, because then your new tab wouldn't be inside the `<sw-tabs>` element. Instead, you can choose the last available block inside the element, which is `sw_product_detail_content_tabs_reviews` at this moment.

### Create custom tab [​](#create-custom-tab)

Knowing the block you have to override in your plugin, you can now start doing exactly this: Add your custom tab by overriding this block called `sw_product_detail_content_tabs_reviews`.

DANGER

However, please keep in mind that "overriding" doesn't mean we want to replace the block completely with our new one. We want to add our tab, thus only extending the template. This will have some implications on our implementation.

First, please re-create the directory structure from the core code in your plugin. In this case, you'll have to create a directory structure like the following: `<plugin root>/src/Resources/app/administration/src/page/sw-product-detail`

In there you create a new file `index.js`, which then contains the following code:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/index.js
import template from './sw-product-detail.html.twig';

// Override your template here, using the actual template from the core
Shopware.Component.override('sw-product-detail', {
    template
});
```

All this file is doing is to basically override the `sw-product-detail` component with a new template. The new template does not exist yet though, so create a new file `sw-product-detail.html.twig` in the same directory as your `index.js` file. It then has to use the block we figured out earlier and override it by adding a new tab element:

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs_reviews %}

    {# This parent is very important as you don't want to override the review tab completely #}
    {% parent %}

{% endblock %}
```

WARNING

The block gets overridden and immediately the parent block is called, since you do not want to replace the 'Review' tab, you want to add a new tab instead.

After that, we'll create the actual `sw-tabs-item` element, which, as the name suggests, represents a new tab item. We want this tab to have a custom route, so we're also adding this route directly. Don't worry, we'll explain this custom route in a bit. The product detail page's route contain the product's ID, which you also want to have in your custom tab: So make sure to also pass the ID in, like shown in the example above.

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs_reviews %}

    {% parent %}

    <!-- We'll define a custom route here, an explanation will follow later -->
    <sw-tabs-item :route="{ name: 'sw.product.detail.custom', params: { id: $route.params.id } }" title="Custom">
        Custom
    </sw-tabs-item>
{% endblock %}
```

The [route](./../routing-navigation/add-custom-route.html) being used here has the name `sw.product.detail.custom`, this will become important again later on.

### Loading the new tab [​](#loading-the-new-tab)

You've now created a new tab, but your new template is not yet loaded. Remember, that the main entry point for custom javascript for the Administration is the your plugin's `main.js` file. And that's also the file you need to adjust now, so it loads your `sw-product-detail` override.

This is an example of what your `main.js` should look like in order to load your override:

javascript

```shiki
import './page/sw-product-detail';
```

INFO

Don't forget to rebuild the Administration after applying changes to your `main.js`.

## Registering the tab's new route [​](#registering-the-tab-s-new-route)

Your new tab should now already show up on the product detail page, but clicking it should always result in an error. It's basically pointing to a new route, which you never defined yet.

Next step would be the following: Create a new route and map it to your own component. This is done by registering a new dummy module, which then overrides the method `routeMiddleware` of a module. It gets called for each and every route that is called in the Administration. Once the `sw.product.detail` route is called, you want to add your new child route to it.

You can add those changes to your `main.js` file, which could then look like this:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './page/sw-product-detail';
import './view/sw-product-detail-custom';

// Here you create your new route, refer to the mentioned guide for more information
Shopware.Module.register('sw-new-tab-custom', {
    routeMiddleware(next, currentRoute) {
        const customRouteName = 'sw.product.detail.custom';
    
        if (
            currentRoute.name === 'sw.product.detail' 
            && currentRoute.children.every((currentRoute) => currentRoute.name !== customRouteName)
        ) {
            currentRoute.children.push({
                name: customRouteName,
                path: '/sw/product/detail/:id/custom',
                component: 'sw-product-detail-custom',
                meta: {
                    parentPath: 'sw.product.index'
                }
            });
        }
        next(currentRoute);
    }
});
```

As already mentioned, you need to create a dummy module in order to override the `routeMiddleware` method. In there, you're listening for the current route, that got called. If the current route matches `sw.product.detail`, you want to add your new child route to it, and that's what's done here.

WARNING

Your child route defines the routes name, so make sure to use the name you're already defined earlier!

The path should be identical to the default ones, which look like this: `/sw/product/detail/:id/base` Just replace the `base` here with `custom` or anything you like.

It then points to a component, which represents the routes actual content - so you'll have to create [a new component](./../module-component-management/add-custom-component.html) in the next step. Note the new import that's already part of this example: `view/sw-product-detail-custom`

## Creating your new component [​](#creating-your-new-component)

As shown in the previous example, your custom component is expected to be in a directory `view/sw-product-detail-custom`, so create this directory in your plugin now. The directory structure inside of your Administration directory should then look like this:

text

```shiki
administration
├── src
│   └──page
│       └── sw-product-detail
│           ├── index.js
│           └── sw-product-detail.html.twig
|   └──view
│       └── sw-product-detail-custom
│           ├── index.js        
└── main.js
```

Since a component always gets initiated by a file called `index.js`, create such a new file in the `sw-product-detail-custom` directory:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/view/sw-product-detail-custom/index.js
import template from './sw-product-detail-custom.html.twig';

Shopware.Component.register('sw-product-detail-custom', {
    template,

    metaInfo() {
        return {
            title: 'Custom'
        };
    },
});
```

This file mainly registers a new component with a custom title and a custom template. Once more, the referenced template is still missing, so make sure to create the file `sw-product-detail-custom.html.twig` next to your `index.js` file.

Here's what this new template could look like:

html

```shiki
// <plugin root>/src/Resources/app/administration/src/view/sw-product-detail-custom/sw-product-detail-custom.html.twig
<sw-card title="Custom">
    Hello world!
</sw-card>
```

It simply creates a new card with a title, which only contains a 'Hello world!' string. And that's it - your tab should now be fully functional.

---

## Writing templates

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/templates-styling/writing-templates.html

# Writing templates [​](#writing-templates)

## Overview [​](#overview)

The Shopware 6 Administration uses a combination of [twig](https://twig.symfony.com/) and [Vue](https://vuejs.org/) templates in its Administration to provide easy extensibility. This guide will teach you how to use templates to extend the Administration with twig and Vue and how import them into a component.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Writing a template [​](#writing-a-template)

Templates in Shopware are usually defined in a separate `.twig` file, named after the component, in the component's directory. Each module's page should start with the `sw-page` component, because it provides a search bar, a page header and a `content` slot for your content. Components in general should also include twig blocks, in order to be extendable by other plugins.

Let's look at all of this in practice, with the example of a component statically printing `'Hello World'`:

html

```shiki
{% block swag_basic_example_page %}
    <sw-page class="swag-example-list">
        <template #content>
            <h2>Hello world!</h2>
        </template>
    </sw-page>
{% endblock %}
```

## Setting the Template [​](#setting-the-template)

Each component has a template property, which is used to set the template. To use the previously created template file, import it and assign it to the `template` property of the component.

javascript

```shiki
import template from './swag-basic-example.html.twig';

Shopware.Component.register('swag-basic-example', {
    template, // ES6 shorthand for: 'template: template'  

    metaInfo() {
        return {
            title: this.$createTitle()
        };
    },
});
```

Note: The meta info is part of [vue-meta](https://vue-meta.nuxtjs.org/) and is used to set the title of the whole page. The `this.$createTitle()` generates a title.

## Theory: Vue vs Twig [​](#theory-vue-vs-twig)

The Shopware 6 Administration mixes, as mentioned in the beginning, [twig](https://twig.symfony.com/) and [Vue](https://vuejs.org/) to provide extensibility. But for what is twig used and for what is Vue used?

Generally speaking, twig is used for **extending** from another template and adjusting it to your needs. For example overriding a twig block could provide a hook to place your own markup. But be careful overrides apply to all occurrences of this template.

Vue is used to link the data and the DOM to make them reactive. Learn about Vue and its capabilities [here](https://vuejs.org/guide/introduction.html).

## More interesting topics [​](#more-interesting-topics)

* [Add custom styling](./../templates-styling/add-custom-styles.html)
* [Adding shortcuts](./../advanced-configuration/add-shortcuts.html)

---

## Adding snippets

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/templates-styling/adding-snippets.html

# Adding snippets [​](#adding-snippets)

## Overview [​](#overview)

By default Shopware 6 uses the [Vue I18n](https://kazupon.github.io/vue-i18n/started.html#html) plugin in the `Administration` to deal with translation.

## Creating snippet files [​](#creating-snippet-files)

Normally you use snippets in your custom module. To keep things organized, create a new directory named `snippet` inside module directory `<plugin root>/src/Resources/app/administration/src/module/<your-module>/snippet`. For each language you want to support, you need a JSON file inside it, e.g., `de-DE.json`, `en-GB.json`. For more details on selecting a fallback language and structuring your snippet files, see the [Fallback Languages guide](./../../../../../concepts/translations/fallback-language-selection.html).

INFO

Providing snippets for apps works the same as in plugins but it has a more simplistic file structure. Also, unlike plugins, App-Snippets **are not allowed** to override existing snippet keys. So, use the following path for vendor-prefixed app snippet files: `<app root>/Resources/app/administration/snippet`

Each language then receives a nested object of translations, so let's have a look at an example `snippet/en-GB.json`:

json

```shiki
{
    "swag-example": {
        "nested": {
            "value": "example",
            "examplePluralization": "1 Product | {n} Products"
        },
        "foo": "bar"
    }
}
```

In this example you would have access the two translations by the following paths: `swag-example.nested.value` to get the value 'example' and `swag-example.foo` to get the value 'bar'. You can nest those objects as much as you want.

By default, Shopware 6 will collect those files automatically when your plugin is activated.

INFO

When you do not build a module and therefore do not fit into the suggested directory structure, you can still place the translation files anywhere in `<plugin root>/src/Resources/app/administration/src/`.

## Using the snippets in JavaScript [​](#using-the-snippets-in-javascript)

Since snippets are automatically registered in the scope of your module, you can use them directly:

javascript

```shiki
Component.register('my-custom-page', {
    ...

    methods: {
        createdComponent() {
            // call the $tc helper function provided by Vue I18n
            const myCustomText = this.$tc('swag-example.general.myCustomText');

            console.log(myCustomText);
        }
    }
    ...
});
```

Or use `Shopware.Snippet.tc('swag-example.general.myCustomText')` when `this` doesn't point to a component (see also [Vue3 upgrade](./../../../../../resources/references/upgrades/administration/vue3.html))

## Using the snippets in templates [​](#using-the-snippets-in-templates)

The same `$tc` helper function can be used in the templates to access translations.

twig

```shiki
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText') }}
    </p>
{% endblock %}
```

Another feature of `$tc` is pluralization. Use a `|` in snippets to provide translations depending on the number. The first part shows singular expression, while the second takes care of plural cases. Let's have a look at this example of `"examplePluralization": "One Product | {n} Products"` with the following implementation:

twig

```shiki
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.nested.examplePluralization', products.length) }}
    </p>
{% endblock %}
```

If you provide `1` as the second parameter to `$tc()`, the text `One Product` would be rendered. For any other value greater than 1, the number itself is shown — for example, `4 Products`.

## More interesting topics [​](#more-interesting-topics)

* [Learning about the global Shopware object](./../data-handling-processing/the-shopware-object.html)
* [Learning about the VueX state](https://github.com/shopware/docs/blob/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/using-vuex-state.md)

---

## Using assets

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/templates-styling/using-assets.html

# Using assets [​](#using-assets)

## Overview [​](#overview)

When working with an own plugin, the usage of own custom images or other assets is a natural requirement. So of course you can do that in Shopware as well. In this guide we will explore how you can add custom assets in your plugin in order to use them in the Administration.

## Prerequisites [​](#prerequisites)

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the Plugin base guide:

[Plugin Base Guide](../../plugin-base-guide)

Needless to say, you should have your image or another asset at hand to work with.

## Add custom assets [​](#add-custom-assets)

In order to add your own custom assets, you need to save your assets in the `Resources/app/administration/static` folder.

bash

```shiki
# PluginRoot
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │       └── administration
    │             └── static
    │                   └── your-image.png <-- Asset file here
    └── SwagBasicExample.php
```

Similar as in [using custom assets in Storefront](./../../storefront/add-custom-assets.html), you need to execute the following command:

bash

```shiki
// 
bin/console assets:install
```

This way, your plugin assets are copied to the `public/bundles` folder:

bash

```shiki
# shopware-root/public/bundles
.
├── administration
├── framework
├── storefront
└── swagbasicexample
    └── your-image.png <-- Your asset is copied here
```

## Use custom assets in the Administration [​](#use-custom-assets-in-the-administration)

After adding your assets to the `public/bundles` folder, you can start using them in the Administration. Simply utilize the `asset` filter.

Create a computed component to make them easy to use in your template.

javascript

```shiki
computed: {
    assetFilter() {
        return Shopware.Filter.getByName('asset');
    },
}
```

html

```shiki
<img :src="assetFilter('/<plugin root>/administration/static/your-image.png')">
```

You're able to use this line in your `twig`/`html` files as you please and that's basically it. You successfully added your own asset to the Administration.

---

## Add custom styles

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/templates-styling/add-custom-styles.html

# Add custom styles [​](#add-custom-styles)

## Overview [​](#overview)

All components contain own templates and some style. Of course, you may want to use your custom styles in your component or module. In this guide, we got you covered on how to add those custom styles to your components.

## Prerequisites [​](#prerequisites)

However, this guide does not explain how to create a custom component, so head over to the official guide about creating a custom component to learn this first.

[Add custom component](../module-component-management/add-custom-component)

In addition, you need to have a basic knowledge of CSS and SCSS in order to use custom styles. This is though considered a basic requirement and won't be taught in this guide.

### Example: Custom cms block [​](#example-custom-cms-block)

We will base our guide on an example: Let's use a custom component printing out "Hello world!". So first of all, create a new directory for your`sw-hello-world`. As said before, more information about that topic, such as where to create this directory, can be found in [Add a custom component](./../module-component-management/add-custom-component.html).

In your component's directory, create a new `index.js` file and register your custom component `sw-hello-world`:

javascript

```shiki
Shopware.Component.register('sw-hello-world', {
    template
});
```

Just like most components, it has a custom template. First we create the template file named `sw-hello-world.html.twig`:

This template now has to define the basic structure of your component. In this simple case, you only need a parent container and two sub-elements, whatever those are.

html

```shiki
{% block example_block %}
    <div class="sw-hello-world">
        <p>Hello world!</p>
    </div>
{% endblock %}
```

You've got a parent `div` containing the content of your template, an abstract with the text "Hello world!" in this case. Next up, you need to import that template in your `index.js` file of your component:

javascript

```shiki
// Import for your template
import template from './sw-hello-world.html.twig';

Shopware.Component.register('sw-sw-hello-world', {
    template
});
```

## Add custom styles to your component [​](#add-custom-styles-to-your-component)

Your component should come with a custom `.scss` file, which you need to create now. Don't forget to import it in your `index.js` file, if not done yet:

javascript

```shiki
import template from './sw-hello-world.html.twig';

// Import for your custom styles
import './sw-hello-world.scss';

Shopware.Component.register('sw-sw-hello-world', {
    template
});
```

In there, simply use a grid to display your elements next to each other. You set a CSS class for your block, which is named after the component. In there, you can set your styles as you need. To mention an example, we want the text in the `div` with the class `sw-hello-world` to have a blue color:

css

```shiki
.sw-hello-world {
    color: blue;
}
```

That's it for this component! This way, you're able to add your own styles to your component now.

### Import variables [​](#import-variables)

Because of [Sass](https://sass-lang.com/) usage, you are able to import external variables and use them in your classes. Below you see an example which uses Shopware's SCSS variables to color the text of the component in shopware's shade of blue.

css

```shiki
/* Import statement */
@import "~scss/variables";

.sw-hello-world {
  /* Usage of variable */
  color: $color-shopware-brand-500;
}
```

## More interesting topics [​](#more-interesting-topics)

* [Writing templates](./../templates-styling/writing-templates.html)
* [Add shortcuts](https://github.com/shopware/docs/blob/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/add-shortcuts.md)

---

## Adding responsive behavior

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/ui-ux/adding-responsive-behavior.html

# Adding responsive behavior [​](#adding-responsive-behavior)

## Overview [​](#overview)

The Shopware 6 Administration provides two ways of adding classes to elements based on their size, the device helper and the `v-responsive` directive. Alternatively you can use `css` media queries to make your plugin responsive. Learn how to use `css` here:

[Add custom styles](../templates-styling/add-custom-styles)

## DeviceHelper [​](#devicehelper)

The DeviceHelper provides methods to get device and browser information like the current viewport size. The helper methods can be accessed with `this.$device` in every Vue component, since it is bound to the Vue prototype.

It makes it possible to run functions to react to `onResize` events with adding classes or removing them. The example below shows you how to use the `$device.onResize` helper.

javascript

```shiki
const listener = function (ev) {
    // do something on resize with the event, like adding or removing classes to elements   
};

const scope = this;
const component = 'sw-basic-example';

this.$device.onResize({ listener, scope, component });
```

The code snippet before could be placed in the `mounted` [Vue lifecycle](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram) hook to register those listeners automatically. Then you can automatically remove the listeners in the `onDestroy` hook

javascript

```shiki
this.$device.removeResizeListener(component);
```

It also provides many helper functions e.g. to get the screen dimensions. Although there are many more as seen below:

| Function | Description |
| --- | --- |
| `this.$device.getViewportWidth();` | Gets the viewport width |
| `this.$device.getViewportHeight();` | Gets the viewport height |
| `this.$device.getDevicePixelRatio();` | Gets the device pixel ratio |
| `this.$device.getScreenWidth();` | Gets the screen width |
| `this.$device.getScreenHeight();` | Gets screen height |
| `this.$device.getScreenOrientation();` | Gets the screen orientation |

## v-responsive directive [​](#v-responsive-directive)

The `v-responsive` directive can be used to dynamically apply classes based on an element's dimensions.

html

```shiki
<input v-responsive="{ 'is--compact': el => el.width <= 1620, timeout: 200 }">
```

Let's do a small explanation of this directive:

* Apply class (in this case: `is--compact`) when the width of the element is smaller than 1620px.
* `timeout`: Sets the duration on how much the throttle should wait.

---

## API

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/api/

# API [​](#api)

Commercial plugins are pre-built extensions developed by third-party vendors that offer specific features and integrations. In some cases, commercial plugins may expose their own APIs, which developers can use to interact with the plugin's functionalities allowing customization and integration with other systems.

Overall, commercial plugins and APIs work together to expand the capabilities of the Shopware platform. Commercial plugins offer ready-to-use solutions, while APIs provide the flexibility for developers to build custom integrations and extend the functionality of Shopware even further.

---

## Custom Pricing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/api/customer-specific-pricing.html

# Customer-specific Pricing [​](#customer-specific-pricing)

The Customer-specific pricing feature allows massive advances in the pricing model capabilities in the Shopware 6 ecosystem.

The API interface exposed by this module allows the user to operate a set of commands which will enable the granular overriding of prices via an external data repository or ERP system. This is achieved by defining a custom relationship between the current price and the Customer entity.

## Pre-requisites and setup [​](#pre-requisites-and-setup)

Customer-specific pricing is part of the Commercial plugin, requiring an existing Shopware 6 installation and the activated Shopware 6 Commercial plugin. This Commercial plugin can be installed as per the [install instructions](./../../../../guides/plugins/plugins/plugin-base-guide.html#install-your-plugin). In addition, the `Custom Prices` feature needs to be activated within the relevant merchant account.

## Working with the API route [​](#working-with-the-api-route)

To create, alter and/or delete customer-specific prices, you can use the API endpoint `/api/_action/custom-price`. Like with any other admin request in Shopware, you must first authenticate yourself. Therefore, please head over to the [authentication guide](https://shopware.stoplight.io/docs/admin-api/authentication) for details.

Otherwise, the Customer-specific Pricing API interface models itself upon the interface of the [sync API](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide), so you will be able to package your requests similarly.

INFO

You can use the route with single `upsert` and `delete` actions or even combine those in a single request: you can pack several different commands inside one sync API request, and each of them is executed in an independent and isolated way

So, it's not surprising that the request body looks like a familiar sync request. In the payload for the `upsert` action, you pass the following data:

* `productId`: The product whose price should be overwritten.
* `customerId`: The customer for whom we will assign a custom price.
* `price`: The new custom price you want to use.

This way, we come to use a payload as seen in the example below:

json

```shiki
[
  {
    "action": "upsert",
    "payload": [
      {
        "productId": "0001e32041ac451386bf9b7351c540f3",
        "customerId": "02a3c82b5ca842c492f8656029b2e63e",
        "price": [
          {
            "quantityStart": 1,
            "quantityEnd": null,
            "price": [
              {
                "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
                "gross": 682.0,
                "net": 682.0,
                "linked": true
              }
            ]
          }
        ]
      }
    ]
  }
]
```

For the `delete` action, the workflow operation accepts 3 different array of ids: `customerIds`, `productIds`, or `customerGroupIds`. Here, you can specify any combination of these id arrays, with the exception that the API route must have at least one UUID supplied in one of the id arrays (`customerIds`, `productIds`, or `customerGroupIds`)

json

```shiki
[
  {
    "action": "delete",
    "payload": [
      {
        "productIds": [
          "0001e32041ac451386bf9b7351c540f3",
          "363a6985f6434a7493b1ef3dabeed40f"
        ],
        "customerIds": [
          "53fc38877a510a47b0e0c44f1615f0c5"
        ],
        "customerGroupIds": []
      }
    ]
  }
]
```

INFO

In case of an error occurs, the response will not return an error code - which is typical for the sync API; instead, any validation errors will be stored within the `errors` key.

WARNING

When working with this route, one difference sets it apart from the familiar `sync` requests: You cannot specify headers to adapt the endpoint's behavior.

## Known caveats or issues [​](#known-caveats-or-issues)

When working with custom prices, there are currently some caveats or issues to keep in mind:

* Price filtering (within the product listing page) will *currently* not support the overridden prices.
* ElasticSearch product mapping does not currently support Customer-specific Pricing data.
* Optional header flags within the core `sync` API are not supported within the provided endpoint (`indexing-behavior, single-operation`). Indexing of any relevant database (product) data is handled on a per-request basis without the need to specify indexing handling.
* The `customerGroupId` parameter within a Customer-specific Pricing API request body is a stub implementation to avoid breaking changes in future versions and is not currently functional. Any data provided for this parameter will not affect the Storefront.

---

## Multi Inventory

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/api/multi-inventory.html

# Multi-Inventory [​](#multi-inventory)

## Pre-requisites and setup [​](#pre-requisites-and-setup)

### Commercial Plugin [​](#commercial-plugin)

Multi-Inventory is part of the Commercial plugin available along with the Beyond plan. This feature requires:

* Shopware 6 instance
* [Shopware Beyond](https://docs.shopware.com/en/shopware-6-en/features/shopware-beyond) license
* Activated Commercial plugin. Refer to [plugin base guide](./../../../../guides/plugins/plugins/plugin-base-guide.html#install-your-plugin) for installation instructions

### Admin UI [​](#admin-ui)

While this feature is supposed to be used by API first, i.e. by ERP systems, it still comes with an user interface for the Administration. Refer to [My extensions](https://docs.shopware.com/en/shopware-6-en/extensions/myextensions) section of shopware docs to explore more about it.

### Admin API [​](#admin-api)

To create, modify or delete Warehouses, WarehouseGroups etc., related to Multi-Inventory, you can access Admin API endpoints described further.

Meanwhile, refer to the following links regarding the general use of the Admin API:

* [Authentication & Authorization](https://shopware.stoplight.io/docs/admin-api/authentication)
* [Request, Response and Endpoint Structure](https://shopware.stoplight.io/docs/admin-api/request-and-response-structure)

## Data structure [​](#data-structure)

The Multi-Inventory feature implements a specific data structure for its internal stock handling. The following entity-relationship model visually represents the new entities, as well as the relationships between them and platform entities.

## Working with the API [​](#working-with-the-api)

The following examples contain payloads for typical use-cases of this feature. Basically all new entities fully support the Admin API via sync service or their generic entity endpoints.

### Creating or updating a WarehouseGroup and assigning it to an existing Warehouse [​](#creating-or-updating-a-warehousegroup-and-assigning-it-to-an-existing-warehouse)

json

```shiki
// POST /api/warehouse-group
// PATCH /api/warehouse-group/8cf7736855594501aaf86351e147c61e

{
    "id": "8cf7736855594501aaf86351e147c61e",
    "name": "Group A",
    "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore.",
    "priority": 25,
    "ruleId": "93248b220a064424a1f6e90010820ba2",
    "warehouses":  [{
        "id": "4ce2bd36d2824153812fcb6a97f22d22"
    }]
}
```

### Creating or updating a Warehouse and assigning it to an existing WarehouseGroups [​](#creating-or-updating-a-warehouse-and-assigning-it-to-an-existing-warehousegroups)

json

```shiki
// POST /api/warehouse
// PATCH /api/warehouse/4ce2bd36d2824153812fcb6a97f22d22

{
    "id": "4ce2bd36d2824153812fcb6a97f22d22",
    "name": "Warehouse A",
    "groups": [{
        "id": "8cf7736855594501aaf86351e147c61e"
    }, {
        "id": "4154501a3812fcb6a501aaf8c7736855"
    }]
}
```

### Assigning WarehouseGroups to Products, creating ProductWarehouses via association [​](#assigning-warehousegroups-to-products-creating-productwarehouses-via-association)

json

```shiki
// POST /api/_action/sync

[{
    "action": "upsert",
    "entity": "product",
    "payload": [{
        "id": "86d38702be7e4ac9a941583933a1c6f5",
        "versionId": "0fa91ce3e96a4bc2be4bd9ce752c3425",
        "warehouseGroups": [{
            "id": "8cf7736855594501aaf86351e147c61e"
        }],
        "warehouses": [{
            "id": "f5c850109fe64c228377cbd369903b75",
            "productId": "86d38702be7e4ac9a941583933a1c6f5",
            "productVersionId": "0fa91ce3e96a4bc2be4bd9ce752c3425",
            "warehouseId":"4ce2bd36d2824153812fcb6a97f22d22",
            "stock": 0
        }]
    }]
}]
```

### Updating ProductWarehouse stocks [​](#updating-productwarehouse-stocks)

You can update `product_warehouse.stock` in batch via SyncApi, or patch a specific entity directly via entity repository.

json

```shiki
// POST /api/_action/sync

[{
    "action": "upsert",
    "entity": "product_warehouse",
    "payload": [{
        "id": "f5c850109fe64c228377cbd369903b75",
        "stock": 1500
    }, {
        "id": "228377cbd369903b75f5c850109fe64c",
        "stock": 0
    }]
}]

// PATCH /api/product-warehouse/f5c850109fe64c228377cbd369903b75

{
    "id": "f5c850109fe64c228377cbd369903b75",
    "stock": 1500
}
```

## Concept [​](#concept)

INFO

Every described behavior only applies to Products that are assigned to WarehouseGroups and every unrelated Product will use the default Shopware behavior.

### ERP System as Single-Source-of-Truth [​](#erp-system-as-single-source-of-truth)

Multi-Inventory is intended to be used as an interface between Shopware and your resource management software. This means that Shopware will only calculate the availability of Products based on your Warehouse configuration and changes stocks of a Warehouse when an order is created. This prevents oversales while also making your system the single source of truth - making it easier to maintain both systems at the same time.

### Product Availability [​](#product-availability)

Availability of Products is defined in 2 steps:

* WarehouseGroups can be assigned to Rules (Rule builder)
  + If the rule is invalid, this Group will not be considered in calculating Product availability.
  + Products/Warehouses can still be available via other groups.
  + If multiple rules are valid, WarehouseGroups can be prioritized with their own priority, they are not tied to rule priority.
* Products can have a stock per Warehouse
  + All Warehouses inside an active WarehouseGroup are taken into account for calculating the total stock of a specific Product.
  + Warehouses are unique, but can be assigned to multiple Groups (e.g. all Warehouses in the Group "Germany" can also be in the Group "Europe").

If both conditions are true (e.g. "Customer is in a specific customer group" and "requested stock <= total Product stock of all valid Warehouses"), the requested Product is considered available. This calculation also considers other Product properties like `max_purchase`, `min_purchase`, and `purchase_steps`.

## Caveats [​](#caveats)

When working with the Multi-Inventory feature, there are some caveats to keep in mind

* We decided to *not* add the functionality of `product.available_stock` to Multi-Inventory. The stock of Products (or rather ProductWarehouses) will now be reduced immediately after an order was placed. It is no longer necessary to set any order state (for Products assigned to WarehouseGroups) to reduce the stock.
  + Order states are still important for any other workflow, e.g. FlowBuilder triggers, or event subscribers in general.
* Multi-Inventory will not recalculate the stock of Products assigned to WarehouseGroups when editing existing orders in any way. The whole stock handling in this regard is supposed to be done by an external ERP system, the information then need to be pushed to your Shopware instance (e.g. by immediate or daily syncs).
* If you decide to stop using Multi-Inventory for certain products (deleting existing data or deactivating the feature), Shopware will fall back into its default behavior. This is especially important when editing existing orders, since the stocks were taken from ProductWarehouse entities. Shopware will use incorrect data or values to increase/decrease Product stocks, if the order originally included ProductWarehouses.

---

## App Starter Guides

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/starter/

# App Starter Guides [​](#app-starter-guides)

The app starter guide provides a comprehensive approach to extending the platform's functionality. The following section guides you on creating custom API endpoints with App scripts, reading and writing data to/from Shopware, and creating custom admin extensions.

---

## Starter Guide - Read and write data

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/starter/product-translator.html

# Starter Guide - Read and Write Data [​](#starter-guide-read-and-write-data)

This guide will show you how to set up an app server with our [app bundle](https://github.com/shopware/app-bundle-symfony). You will learn how to read and write data to the Shopware Admin API using an example of fetching dynamic translations for products when they are updated.

## Prerequisites [​](#prerequisites)

* Basic CLI usage (creating files, directories, running commands)
* Installed [shopware-cli](./../../../../products/cli/) tools
* Installed [symfony-cli](https://symfony.com/download)
* A running MariaDB or MySQL accessible to your development machine

## Setting up the app template [​](#setting-up-the-app-template)

First, we need to create a new Symfony project using Symfony-CLI

sh

```shiki
symfony new translator-app
```

The app template contains a basic Symfony application.

Now we need to install the Shopware App Bundle with Composer:

sh

```shiki
composer require shopware/app-bundle
```

WARNING

Make sure that you agree to second interaction of the bundle recipe. It will add your routing, register the bundle, and more. If you do not agree to it, you will have to create those manually (check files [here](https://github.com/symfony/recipes-contrib/tree/main/shopware/app-bundle/1.0))

shell

```shiki
-  WARNING  shopware/app-bundle (>=1.0): From github.com/symfony/recipes-contrib:main
   The recipe for this package comes from the "contrib" repository, which is open to community contributions.
   Review the recipe at https://github.com/symfony/recipes-contrib/tree/main/shopware/app-bundle/1.0

    Do you want to execute this recipe?
    [y] Yes
    [n] No
    [a] Yes for all packages, only for the current installation session
    [p] Yes permanently, never ask again for this project
    (defaults to n): n
```

Modify the `SHOPWARE_APP_NAME` and `SHOPWARE_APP_SECRET` in the env to your app name`./.env` to ensure you can install the app in a store later. Also, configure the `DATABASE_URL` to point to your database:

sh

```shiki
// .env
....

###> shopware/app-bundle ###
SHOPWARE_APP_NAME=TestApp
SHOPWARE_APP_SECRET=TestSecret
###< shopware/app-bundle ###
```

You can now start the application with `symfony server:start -v`.

For now, your app server is currently only available locally.

INFO

When you are using a local Shopware environment, you can skip to the [next chapter](#creating-the-manifest)

We need to expose your local app server to the internet. The easiest way to achieve that is using a tunneling service like [ngrok](https://ngrok.com/).

The setup is as simple as calling the following command (after installing ngrok)

sh

```shiki
ngrok http 8000
```

This will expose your Symfony server on a public URL, so the cloud store can communicate with your app.

## Creating the manifest [​](#creating-the-manifest)

The `manifest.xml` is the main interface definition between stores and your app server. It contains all the required information about your app. Let's start by filling in all the meta-information:

xml

```shiki
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>product-translator</name>
        <label>Product translator</label>
        <description>App to translate product descriptions</description>
        <author>shopware AG</author>
        <copyright>(c) by shopware AG</copyright>
        <version>0.1.0</version>
        <license>MIT</license>
    </meta>
   </manifest>
```

WARNING

Take care to use the same `<name>` as in the `.env` file. Otherwise, stores can't install the app.

### Setup hook [​](#setup-hook)

Next, we will define the `<setup>` part of the manifest. This part describes how the store will connect itself with the app server.

xml

```shiki
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
        <registrationUrl>http://localhost:8000/app/lifecycle/register</registrationUrl>
        <secret>TestSecret</secret>
    </setup>
</manifest>
```

The `<registraionUrl>` is already implemented by the app template and is always `/app/lifecycle/register`, unless you modify `config/routes/shopware_app.yaml`. The `<secret>` element is only present in development versions of the app. In production, the extension store will provide the secret to authenticate your app buyers.

### Permissions [​](#permissions)

The manifest needs permissions as this app will read product descriptions and translate them:

xml

```shiki
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
    <!-- ... -->
    </setup>
    <permissions>
        <read>product</read>
        <read>product_translation</read>
        <read>language</read>
        <read>locale</read>
        <update>product</update>
        <update>product_translation</update>
        <create>product_translation</create>
    </permissions>
</manifest>
```

### Webhooks [​](#webhooks)

Finally, your app needs to be notified every time a product description is modified. The app system provides webhooks to subscribe your app server to any changes in the data in its shops:

xml

```shiki
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
    <!-- ... -->
    </setup>
    <permissions>
    <!-- ... -->
    </permissions>
    <webhooks>
        <webhook name="appActivated" url="http://localhost:8000/app/lifecycle/activate" event="app.activated"/>
        <webhook name="appDeactivated" url="http://localhost:8000/app/lifecycle/deactivate" event="app.deactivated"/>
        <webhook name="appDeleted" url="http://localhost:8000/app/lifecycle/delete" event="app.deleted"/>
        <webhook name="productWritten" url="http://localhost:8000/app/webhook" event="product.written"/>
    </webhooks>
</manifest>
```

INFO

The timeout for the requests against the app server is 5 seconds.

The App Bundle provides these four webhooks, so the Bundle does the complete lifecycle and handling of Webhooks for you.

## Handling shop events [​](#handling-shop-events)

To get started, let's write a simple [Symfony event listener](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-listener):

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
#[AsEventListener(event: 'webhook.product.written')]
class ProductWrittenWebhookListener
{
    public function __construct(private readonly ClientFactory $clientFactory, private readonly LoggerInterface $logger)
    {
    }

    public function __invoke(WebhookAction $action): void
    {
    }
}
```

### Creating a shop client [​](#creating-a-shop-client)

The Bundle verifies for you the Request and provides you the Webhook parsed together with the Shop it has requested it. With the Shop, we can create a pre-authenticated PSR-18 Client to communicate with the Shop. In this example, we will use the SimpleHttpClient which simples the usage of the PSR-18 Client.

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        $client = $this->clientFactory->createSimpleClient($action->shop);
    }
```

Now we can inspect the event payload:

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...

        $updatedFields = $action->payload[0]['updatedFields'];
        $id = $action->payload[0]['primaryKey'];

        if (!in_array('description', $updatedFields)) {
            return;
        }
    }
```

### Fetching data from the shop [​](#fetching-data-from-the-shop)

All `$entity.written` events contain a list of fields that a written event has changed. The code above uses this information to determine if someone changed the description of a product. If the change does not affect the description, the listener early returns because there is nothing else to do with this event.

Now that it is certain that someone changed the description of the product, we fetch the description through the API of the shop:

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $response = $client->post(
            sprintf('%s/api/search/product', $action->shop->getShopUrl()),
            [
                'ids' => [$id],
                'associations' => [
                    'translations' => [
                        'associations' => [
                            'language' => [
                                'associations' => [
                                    'locale' => []
                                ]
                            ],
                        ]
                    ],
                ]
            ]
        );
        
        if (!$response->ok()) {
            $this->logger->error('Could not fetch product', ['response' => $response->json()]);
            return;
        }
    }
```

The request contains a criteria that fetches the product for which we received the event `'ids' => [$id]` and all translations and their associated languages `'associations' => 'language'`. Now we can retrieve the English description from the API response:

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $product = $response->json()['data'][0];
        $description = '';
        $name = '';
        foreach ($product['translations'] as $translation) {
            if ($translation['language']['locale']['code'] === 'en-GB') {
                $description = $translation['description'];
                $name = $translation['name'];
            }
        }
    }
```

INFO

A common gotcha with `entity.written` webhooks is that they trigger themselves when you're performing write operations. Updating the description triggers another `entity.written` event. This again calls the webhook, which updates the description, and so on.

Because our goal is to write a French translation of the product, the app needs to take care to avoid endless loops. To determine if the app has already written a translation once, it saves a hash of the original description. We will get to the generation of the hash later, but we need to check it first:

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $lastHash = $product['customFields']['translator-last-translation-hash'] ?? '';
        if (md5($description) === $lastHash) {
            return;
        }
    }
```

### Writing a translated description [​](#writing-a-translated-description)

Now that the app can be sure, the description has not been translated before it can write the new description like so:

php

```shiki
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $response = $client->patch(sprintf('%s/api/product/%s', $action->shop->getShopUrl(), $id), [
            'translations' => [
                'en-GB' => [
                    'name' => $name,
                    'description' => $this->translate($description)
                ],
            ],
            'customFields' => [
                'translator-last-translation-hash' => md5($description)
            ]
        ]);

        if (!$response->ok()) {
            $this->logger->error('Could not update product', ['response' => $response->json()]);
        }
    }
```

Note that the hash of the original description gets saved as a value in the custom fields of the product entity. This is possible without any further config since all custom fields are schema-less.

The implementation of the `translate` method is disregarded in this example. You might perform an additional lookup through a translation API service to implement it.

## Complete Event Listener [​](#complete-event-listener)

php

```shiki
<?php declare(strict_types=1);

namespace App\EventListener;

use Shopware\App\SDK\HttpClient\ClientFactory;
use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
use Shopware\App\SDK\Context\Webhook\WebhookAction;
use Psr\Log\LoggerInterface;

#[AsEventListener(event: 'webhook.product.written')]
class ProductUpdatedListener
{
    public function __construct(private readonly ClientFactory $clientFactory, private readonly LoggerInterface $logger)
    {
    }

    public function __invoke(WebhookAction $action): void
    {
        $client = $this->clientFactory->createSimpleClient($action->shop);

        $updatedFields = $action->payload[0]['updatedFields'];
        $id = $action->payload[0]['primaryKey'];

        if (!in_array('description', $updatedFields)) {
            return;
        }

        $response = $client->post(
            sprintf('%s/api/search/product', $action->shop->getShopUrl()),
            [
                'ids' => [$id],
                'associations' => [
                    'translations' => [
                        'associations' => [
                            'language' => [
                                'associations' => [
                                    'locale' => []
                                ]
                            ],
                        ]
                    ],
                ]
            ]
        );
        if (!$response->ok()) {
            $this->logger->error('Could not fetch product', ['response' => $response->json()]);
            return;
        }

        $product = $response->json()['data'][0];
        $description = '';
        $name = '';
        foreach ($product['translations'] as $translation) {
            if ($translation['language']['locale']['code'] === 'en-GB') {
                $description = $translation['description'];
                $name = $translation['name'];
            }
        }

        $lastHash = $product['customFields']['translator-last-translation-hash'] ?? '';
        if (md5($description) === $lastHash) {
            return;
        }

        $response = $client->patch(sprintf('%s/api/product/%s', $action->shop->getShopUrl(), $id), [
            'translations' => [
                'en-GB' => [
                    'name' => $name,
                    'description' => 'Test English'
                    //'description' => $this->translate($description)
                ],
            ],
            'customFields' => [
                'translator-last-translation-hash' => md5($description)
            ]
        ]);

        if (!$response->ok()) {
            $this->logger->error('Could not update product', ['response' => $response->json()]);
        }
    }
}
```

## Connecting Doctrine to a Database [​](#connecting-doctrine-to-a-database)

The App Bundle ships with a basic Shop entity to store the shop information. You can extend this entity to store more information about your app if needed.

Symfony configures doctrine to use PostgreSQL by default. Change the `DATABASE_URL` environment variable in your `.env` file if you want to use MySQL. You can also use SQLite by setting the `DATABASE_URL` to `sqlite:///%kernel.project_dir%/var/app.db` for development.

After choosing your database engine, you need to require two extra composer packages.

shell

```shiki
composer req symfony/maker-bundle migrations
```

And create your first migration using `bin/console make:migration` (which is using the `AbstractShop` Class) and apply it to your database with `bin/console doctrine:migrations:migrate`.

## Install the app [​](#install-the-app)

In this last step, we will install the app using the Shopware CLI tools.

INFO

If this is your first time using the Shopware CLI, you have to [install](./../../../../products/cli/installation.html) it first. Next, configure it using the `shopware-cli project config init` command.

sh

```shiki
shopware-cli project extension upload ProductTranslator/release --activate --increase-version
```

This command will create a zip file from the specified extension directory and upload it to your configured store. The `--increase-version` parameter increases the version specified in the `manifest.xml` file. The app requires this flag so Shopware picks up changes made to the `manifest.xml` since the last installation. Once successfully installed, you will see the app in the extension manager. And when you save a product, the description will automatically update.

## Where to continue [​](#where-to-continue)

In this example, you have learned how to receive events and modify data through the app system. You can also:

* Add [new payments](./../payment.html) as apps
* Write code that runs during checkout [app scripting](./../app-scripts/cart-manipulation.html)
* Add new endpoints to the API [custom endpoints](./add-api-endpoint.html)

---

## Starter Guide - Add an API endpoint

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/starter/add-api-endpoint.html

# Starter Guide - Add an API Endpoint [​](#starter-guide-add-an-api-endpoint)

INFO

Note that this guide relies on [App scripts](./../app-scripts/), introduced from Shopware 6.4.8.0 version.

This guide shows how you can add a custom API endpoint that delivers dynamic data starting from zero.

After reading, you will be able to:

* Create the basic setup of an app.
* Execute app scripts and use them to model custom logic.
* Fetch, filter, and aggregate data from Shopware.
* Consume HTTP parameters and create responses.

## Prerequisites [​](#prerequisites)

* A Shopware cloud store
* Basic CLI usage (creating files, directories, running commands)
* Installed and configured [shopware-cli](./../../../../products/cli/) tools
* General knowledge of [Twig Syntax](https://twig.symfony.com/)
* A text editor

## Create the app wrapper [​](#create-the-app-wrapper)

We need to create the app "wrapper", the so-called app manifest within a new directory. Let's call that the project directory:

text

```shiki
MyApiExtension/
├─ manifest.xml
```

INFO

When using a self-hosted Shopware version, you can also create the project directory in the `custom/apps` directory of your Shopware installation. However, the descriptions in this guide apply to both Shopware cloud and self-hosted stores.

Next, we will put our basic configuration into the file we just created.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>MyApiExtension</name>
        <label>Topsellers API</label>
        <description>This app adds a Topseller API endpoint</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>1.0.0</version>
        <license>MIT</license>
    </meta>
    <permissions>
        <read>order</read>
        <read>order_line_item</read>
        <read>product</read>
    </permissions>
</manifest>
```

Besides some metadata, like a name, description, or version, this file contains permissions that the app requires. We will need them later on when performing searches.

## Create the script [​](#create-the-script)

We will define our new API endpoint in a script file based on [App Scripts](./../app-scripts/). There are specific directory conventions that we have to follow to register a new API endpoint script. The prefix for our API endpoint is one of the following and cannot be changed:

| API | API consumers / callers | Prefix |
| --- | --- | --- |
| Store API | Customer-facing integrations | `/store-api/script/` |
| Admin API | Backend integrations | `/api/script/` |
| Storefront | Default Storefront | `/storefront/script/` |

INFO

You might wonder why the Storefront shows up in that table. In Storefront endpoints, you can render not only JSON but also twig templates. But use them with care - whenever you create a Storefront endpoint, your app will not be compatible with headless consumers.

Learn more about the different endpoints in [custom endpoints](./../app-scripts/custom-endpoints.html)

### Directory structure [​](#directory-structure)

In this example, we're going to create a Store API endpoint. We want to provide logic that returns the top-selling products for a specific category. So let's use the following endpoint naming:

`/store-api/script/swag/topseller`

You see that we have added a custom subdirectory `swag` in the route. This is a good practice because we can prevent naming collisions between different apps. Slashes (or subdirectories) in the endpoint path are represented by a hyphen in the name of the directory that contains the script.

text

```shiki
MyApiExtension/
├─ Resources/
│  ├─ scripts/
│  │  ├─ store-api-swag-topseller/ <-- /store-api/script/swag/topseller
│  │  │  ├─ topseller-script.twig
├─ manifest.xml
```

This directory naming causes Shopware to expose the script on two routes:

* `/store-api/script/swag/topseller` and
* `/store-api/script/swag-topseller`

### Add custom logic and install [​](#add-custom-logic-and-install)

Let's start with a simple script to see it in action:

twig

```shiki
// Resources/scripts/store-api-swag-topseller/topseller-script.twig
{% block response %}
    {% set response = services.response.json({ test: 'This is my API endpoint' }) %}
    {% do hook.setResponse(response) %}
{% endblock %}
```

Next we will install the App using the Shopware CLI.

INFO

If this is your first time using the Shopware CLI, you have to [install](./../../../../products/cli/installation.html) it first. Next, configure it using the `shopware-cli project config init` command.

Run this command from the root of the project directory.

shell

```shiki
shopware-cli project extension upload . --activate
```

This command will create a zip file from the specified extension directory (the one you are in), upload it to your configured store and activate it.

### Call the endpoint [​](#call-the-endpoint)

You can call the endpoint using this curl command.

INFO

Follow this guide for more information on using the Store API : [Store API Authentication & Authorization](https://shopware.stoplight.io/docs/store-api/ZG9jOjEwODA3NjQx-authentication-and-authorisation)

shell

```shiki
curl --request GET \
  --url http://<your-store-url>/store-api/script/swag/topseller \
  --header 'sw-access-key: insert-your-access-key'
```

which should return something like:

json

```shiki
{"apiAlias":"store_api_swag_topseller_response","test":"This is my API endpoint"}
```

However, instead of using curl, we recommend using visual clients to test the API - such as [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/download).

## Fill in the logic [​](#fill-in-the-logic)

For now, our script is not really doing anything. Let's change that.

twig

```shiki
// Resources/scripts/store-api-swag-topseller/topseller-script.twig
{% block response %}

    {% set categoryId = hook.request.categoryId %}

    {% set criteria = {
        aggregations: [
            {
                name: "categoryFilter",
                type: "filter",
                filter: [{
                    type: "equals",
                    field: "order.lineItems.product.categoryIds",
                    value: categoryId
                }],
                aggregation: {
                    name: "orderedProducts",
                    type: "terms",
                    field: "order.lineItems.productId",
                    aggregation: {
                        name: "quantityItemsOrdered",
                        type : "sum",
                        field: "order.lineItems.quantity"
                    }
                }
            }
        ]
    } %}

    {% set orderAggregations = services.repository.aggregate('order', criteria) %}

    {% set response = services.response.json(orderAggregations.first.jsonSerialize) %}

    {% do hook.setResponse(response) %}

{% endblock %}
```

What happened here?

We wrap everything in a block named `response`. That way, we will get access to useful objects and services, so we can build a response.

### Search criteria and fetching results [​](#search-criteria-and-fetching-results)

We start by reading the requested category id using `hook.request.categoryId`. In general, we can access post body parameters using `hook.request.*`.

In the following lines, we define a search criteria. The criteria contain a description of the data we want to fetch:

1. First, we filter out all products not inside the category that was requested, using a filter aggregation.
2. The following lines contain two further nested aggregations:
   1. The first one groups all products from all orders using their id.
   2. The second one sums up the number of ordered items in each order.

Ultimately, it gives a result of all products that have been ordered and the total ordered.

INFO

To learn more about the structure of search criteria, follow the link below:

[Search Criteria](./../../../integrations-api/general-concepts/search-criteria.html)

We now send a request to the database to retrieve the result using:

twig

```shiki
{% set orderAggregations = services.repository.aggregate('order', criteria) %}
```

### Building the response [​](#building-the-response)

In the final step, we build the response. We use the `services.response.json()` method to convert the serialized json representation of our aggregation into a json response object named `response`.

twig

```shiki
{% set response = services.response.json(orderAggregations.first.jsonSerialize) %}
```

Finally, we just set the response of the hook to the result from above:

twig

```shiki
{% do hook.setResponse(response) %}
```

It is important to do all this within the `response` block of the twig script. Otherwise, you will get errors when calling the script.

### Installing the plugin [​](#installing-the-plugin)

Next, we re-install our plugin using the same command as before:

shell

```shiki
shopware-cli project extension upload . --activate
```

WARNING

Remember, if you made changes to the `manifest.xml` file in the meantime, also pass the `--increase-version` parameter, else Shopware will not pick up the changes:

shell

```shiki
shopware-cli project extension upload . --activate --increase-version
```

We can now call our endpoint again:

shell

```shiki
curl --request GET \
  --url http://<your-store-url>/store-api/script/swag/topseller \
  --header 'sw-access-key: insert-your-access-key'
```

and receive a different result:

json

```shiki
{
  "apiAlias": "store_api_swag_topseller_response",
  "buckets": [
    {
      "key": "0060b9b2b3804244bf8ba98cdad50234",
      "count": 3,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 15
      },
      "apiAlias": "aggregation_bucket"
    },
    {
      "key": "a65d918f883c47778a65b73548f456ea",
      "count": 2,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 3
      },
      "apiAlias": "aggregation_bucket"
    },
    {
      "key": "6b67935063c84bde8e9d86f25a47c69d",
      "count": 3,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 8
      },
      "apiAlias": "aggregation_bucket"
    }
  ]
}
```

## Wrap-Up [​](#wrap-up)

This tutorial covered the basics of app development using app scripts and some filtering and aggregation logic.

In a proper app, you should consider the following points:

* Input parameter validation
* Format and limit the result
* Define an API contract (endpoint structure) first and build after that
* The search result does not show actual top sellers but just the quantity of products ordered

## Where to continue [​](#where-to-continue)

* More on adding [custom endpoints](./../app-scripts/custom-endpoints.html)
* See how you can use [Twig functions](./../app-scripts/#extended-syntax) in app scripts
* Working with [DAL Aggregations](./../../../../resources/references/core-reference/dal-reference/aggregations-reference.html)

---

## Starter Guide - Create Admin Extensions

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/starter/starter-admin-extension.html

# Starter Guide - Create an Admin Extension [​](#starter-guide-create-an-admin-extension)

In this guide, you will learn how to set up an extension for the Administration UI.

![An admin notification](/assets/extension-api-notification.vm1nXy6f.png)

## Prerequisites [​](#prerequisites)

In order to follow this guide, make sure you are familiar with and meet the following requirements:

* Basic CLI usage (creating files, directories, running commands)
* Installed [shopware-cli](./../../../../products/cli/) tools
* We will use the following libraries/software
  + npm
  + live-server (small local development live-reloading server)

## Create the app wrapper [​](#create-the-app-wrapper)

First of all, we need to create the app "wrapper", the so-called app manifest. It is just a single XML file with some basic configuration.

### Create manifest file [​](#create-manifest-file)

First of all, we create the manifest file in a new directory. We'll call that our "project directory".

text

```shiki
SimpleNotification/
├─ manifest.xml
```

INFO

When you are using a self-hosted Shopware version, you can also create the project directory in the `custom/apps` directory of your Shopware installation. However, the descriptions in this guide apply to both Shopware cloud and self-hosted stores.

Next, we will put our basic configuration into the file we just created.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>SimpleNotification</name>
        <label>Hi Developer App</label>
        <description>This app shows a notification in the admin panel</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>1.0.0</version>
        <license>MIT</license>
    </meta>
</manifest>
```

## Set up communication between Shopware and the app [​](#set-up-communication-between-shopware-and-the-app)

Next, we need to set up an entry point, so Shopware and your app can communicate. The entry point is a static `.html` file, which includes the Extension SDK script and defines our extension.

![Communication between the admin panel and your entry point](/assets/extension-api-communication.CSvwJLxt.png)

The file will be rendered as a hidden iFrame within your admin panel. Using `postMessage` requests, the iFrame and your admin panel can communicate and exchange data.

Let's create an `index.html` file in a directory called `src`.

text

```shiki
SimpleNotification/
├─ src/
│  ├─ index.html
├─ manifest.xml
```

html

```shiki
// src/index.html
<!doctype html>
<html>
    <head>
        <script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk/cdn"></script>
    </head>
    <script>
        sw.notification.dispatch({
            title: 'Hi there',
            message: 'Looks like someone sent you a message'
        });
    </script>
</html>
```

This file contains the basic setup for our app to display the notification:

* The HTML is rendered in a hidden iFrame when the Administration panel is loaded.
* The Meteor Admin SDK script is loaded through a CDN and exposed as the `sw` object.
* We use the `notification.dispatch` SDK method to display a simple notification with a title and a message.

### Start the local development server [​](#start-the-local-development-server)

Next, we need to start the live server, so you don't always have to reload the page manually.

bash

```shiki
npm install -g live-server
live-server src
```

Now the file should be available on <http://127.0.0.1:8080>.

### Add the entry point link to your manifest [​](#add-the-entry-point-link-to-your-manifest)

The final step of the setup is to configure your app to use that file as an entry point.

To do that, we have to add an `admin` section to our `manifest.xml` file and pass it into the `base-app-url` tag:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
  <setup>
    <registrationUrl>http://127.0.0.1:8000/app/lifecycle/register</registrationUrl>
    <secret>TestSecret</secret>
  </setup>
    <admin>
        <base-app-url>http://127.0.0.1:8080</base-app-url>
    </admin>
</manifest>
```

Since the URL to your entry point is only available locally, you will only be able to see changes on your own machine. If you want to share it, for development purposes, you need to host the entry point file somewhere or use services to expose local files as public URLs, such as [ngrok](https://ngrok.com/).

For production usage, you should host the entry point file on a public CDN or a static site hosting.

## Install the app [​](#install-the-app)

In this last step, we will install the app using the Shopware CLI tools.

INFO

If this is your first time using the Shopware CLI, you have to [install](./../../../../products/cli/installation.html) it first. Next, configure it using the `shopware-cli project config init` command.

bash

```shiki
shopware-cli project extension upload SimpleNotification --activate --increase-version
```

This command will create a zip file from the specified extension directory and upload it to your configured store. The `--increase-version` parameter increases the version specified in the `manifest.xml` file. This flag is required so Shopware picks up changes made to the `manifest.xml` since the last installation. When the app is successfully installed, you will see the notification pop up once you open the Shopware admin panel - congratulations!

## Where to continue [​](#where-to-continue)

This example showed end-to-end how to create a local dev environment and connect it with your Shopware Store. There is a lot more to learn and try out, so why not move on with one of those topics:

* Did you know, you can add [new sections](/resources/admin-extension-sdk/api-reference/ui/component-section.html) to the UI or even [entire modules](/resources/admin-extension-sdk/api-reference/ui/mainModule.html)?
* The Meteor Admin SDK also offers [TypeScript support](/resources/admin-extension-sdk/getting-started/installation.html#using-npm-require-bundling) (including autocompletion)
* Don't want to extend the admin panel? Have a look at [App Scripts](./../../../../guides/plugins/apps/app-scripts/)

---

## App Scripts

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-scripts/

# App Scripts [​](#app-scripts)

App Scripts allow your app to include logic that is executed inside the Shopware execution stack. It allows you to build richer extensions that integrate more deeply with Shopware.

INFO

Note that app scripts were introduced in Shopware 6.4.8.0 and are not supported in previous versions.

## Script hooks [​](#script-hooks)

The entry point for each script is the so-called "Hooks". You can register one or more scripts inside your app that should be executed whenever a specific hook is triggered. Through the hook, your script gets access to the data of the current execution context and can react to or manipulate the data in some way.

See the [Hooks reference](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html) for a complete list of all available.

## Scripts [​](#scripts)

At the core, app scripts are [twig files](https://twig.symfony.com/) executed in a sandboxed environment. Based on which hook the script is registered to, the script has access to the data of that hook and pre-defined services that can be used to execute your custom logic.

Apps scripts are placed in the `Resources/scripts` directory of your app. For each hook, you want to execute a script on, create a new subdirectory. The name of the subdirectory needs to match the name of the hook.

You can place one or more `.twig` files inside each of these subdirectories, which will be executed when the hook gets triggered.

The file structure of your apps should look like this:

text

```shiki
└── DemoApp
    ├── Resources
    │   └── scripts                         // all scripts are stored in this folder
    │       ├── product-page-loaded         // each script in this folder will be executed when the `product-page-loaded` hook is triggered
    │       │   └── my-first-script.twig
    │       ├── cart
    │       │   ├── first-cart-script.twig
    │       │   └── second-cart-script.twig // you can execute multiple scripts per hook
    │       └── ...
    └── manifest.xml
```

### Including scripts [​](#including-scripts)

Sometimes scripts can become more complex or you want to extract common functionality. Thus it is handy to split your scripts into smaller parts that can later be included in other scripts.

In order to do that you can compose your reusable scripts into [twig macros](https://twig.symfony.com/doc/3.x/tags/macro.html), put them inside a dedicated `include` folder and then import them using the [twig import functionality](https://twig.symfony.com/doc/3.x/tags/import.html).

text

```shiki
└── DemoApp
    ├── Resources
    │   └── scripts                         
    │       ├── include    
    │       │   └── media-repository.twig         // this script may be included into the other scripts
    │       ├── cart
    │       │   ├── first-cart-script.twig
    │       └── ...
    └── manifest.xml
```

Note that app scripts can use the `return` keyword to return values to the caller.

A basic example may look like this:

twig

```shiki
// Resources/scripts/include/media-repository.twig
{% macro getById(mediaId) %}
    {% set criteria = {
        'ids': [ mediaId ]
    } %}
    
     {% return services.repository.search('media', criteria).first %}
{% endmacro %}
```

twig

```shiki
// Resources/scripts/cart/first-cart-script.twig
{% import "include/media-repository.twig" as mediaRepository %}

{% set mediaEntity = mediaRepository.getById(myMediaId) %}
```

### Interface Hooks [​](#interface-hooks)

Some "Hooks" describe interfaces this means that your scripts for that hook need to implement one or more functions. E.g., the `store-api-hook` defines a `cache_key` and a `response` function. Those functions are closely related but are executed separately. To implement the different functions, you use different twig blocks with the name of the function:

twig

```shiki
{% block cache_key %}
    // provide a cacheKey for the incoming request
{% endblock %}

{% block response %}
    // produce the response for the request
{% endblock %}
```

Some functions are optional, whereas others are required. In the above example the `cache_key` function is optional. That means you can omit that block in your script without an error (but caching for the endpoint won't work in that case). The `response` function is required, which means that if your script does not provide a `response` block, it will lead to an error.

Note that for each function, you get access to different input data or services, so in the `cache_key` block, you don't necessarily have access to the same data and services as in the `response` block. The available data and services are described for each hook (or each function in InterfaceHooks) in the [reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html).

### Translation [​](#translation)

Inside the app script, you have access to the [Storefront translation mechanism](./../../plugins/storefront/add-translations.html) by using the `|trans`-filter.

twig

```shiki
{% set translated = 'my.snippet.key'|trans %}

{% do call.something('my.snippet.key'|trans) %}
```

### Extended syntax [​](#extended-syntax)

In addition to the default twig syntax, app scripts can also use a more PHP-flavoured syntax.

#### Equals check with `===` [​](#equals-check-with)

Instead of using the rather verbose `{% if var is same as(1) %}`, you can use the more dense `===` equality checks.

twig

```shiki
{% if var === 1 %}
    ...
{% endif %}
```

Additionally, you can also use the `!==` not equals operator as well.

twig

```shiki
{% if var !== 1 %}
    ...
{% endif %}
```

#### Loops with `foreach` [​](#loops-with-foreach)

Instead of the `for...in` syntax for loops, you can also use a `foreach` tag.

twig

```shiki
{% foreach list as entry %}
    {{ entry }}
    {% break %}
{% endforeach %}
```

#### Instance of checks with `is` [​](#instance-of-checks-with-is)

You can use a `is` check to check the type of a variable.

twig

```shiki
{% if var is string %}
    ...
{% endif %}
```

The following types are supported:

* `true`
* `false`
* `boolean` / `bool`
* `string`
* `scalar`
* `object`
* `integer` / `int`
* `float`
* `callable`
* `array`

#### Type casts with `intval` [​](#type-casts-with-intval)

You can cast variables into different types with the `intval` filter.

twig

```shiki
{% if '5'|intval === 5 %}
    {# always evaluates to true #}
{% endif %}
```

The following type casts are supported:

* `intval`
* `strval`
* `boolval`
* `floatval`

#### conditions with `&&` and `||` [​](#conditions-with-and)

Instead of using `AND` or `OR` in if-conditions, you can use the `&&` or `||` shorthands.

twig

```shiki
{% if condition === true && condition2 === true %}
    ...
{% endif %}
```

#### `return` tag [​](#return-tag)

You can use the `return` tag to return values from inside macros.

twig

```shiki
{% macro foo() %} 
     {% return 'bar' %}
{% endmacro %}
```

## Available services [​](#available-services)

Depending on the hook that triggered the execution of your script, you get access to different services you can use inside your scripts, e.g. to access data inside Shopware or to manipulate the cart. Take a look at the [Hook reference](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html) to get a complete list of all available services per hook.

Additionally, we added a `ServiceStubs`class that can be used as typehint in your script, so you get auto-completion features of your IDE.

twig

```shiki
{# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

{% set configValue = services.config.app('my-app-config') %}
```

INFO

The stub class contains all services, but not all of them are available depending on the hook.

## Example Script - loading media entities [​](#example-script-loading-media-entities)

Assuming your app adds a [custom field set](./../custom-data/custom-fields.html) for the product entity with a custom media entity select field.

When you want to display the file of the media entity in the [Storefront](./../storefront/), it is not easily possible because, in the template's data, you only get the id of the media entity, but not the URL of the media file itself.

For this case, you can add an app script on the `product-page-loaded` hook, which loads the media entity by id and adds it to the page object so the data is available in templates.

twig

```shiki
// Resources/scripts/product-page-loaded/add-custom-media.twig
{# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

{% set page = hook.page %}
{# @var page \Shopware\Storefront\Page\Product\ProductPage #}

{% if page.product.customFields.myCustomMediaField is not defined %}
    {% return %}
{% endif %}

{% set criteria = {
    'ids': [ page.product.customFields.myCustomMediaField ]
} %}

{% set media = services.repository.search('media', criteria).first %}

{% do page.addExtension('swagMyCustomMediaField', media) %}
```

For a more detailed example of how to load additional data, refer to the [data loading guide](./data-loading.html).

Alternatively, take a look at the [cart manipulation guide](./cart-manipulation.html) to get an in-depth explanation of how to manipulate the cart with scripts.

## Developing/debugging scripts [​](#developing-debugging-scripts)

You can get information about what scripts were triggered on a specific Storefront page inside the [Symfony debug toolbar](https://symfony.com/doc/current/the-fast-track/en/5-debug.html#discovering-the-symfony-debugging-tools).

INFO

The debug toolbar is only visible if your Shopware installation is in `APP_ENV = dev`. Ensure to set the correct env, e.g., in your `.env` file, when developing app scripts.

You can find all hooks that are triggered and the scripts that are executed for each by clicking on the `script` icon.

![Symfony Debug Toolbar](/assets/script-debug-toolbar.CWx76Tfs.png)

That will open the Symfony profiler in the script detail view, where you can see all triggered hooks and the count of the scripts executed for each script at the top.

![Script Debug Toolbar](/assets/script-debug-detail.B3HHMmHZ.png)

Additionally, you can use the `debug.dump()` function inside your scripts to dump data to the debug view. A script like this:

twig

```shiki
{% do debug.dump(hook.page) %}
```

Will dump the page object to the debug view.

![Output of debug.dump()](/assets/script-debug-dump.C10DrrYo.png)

---

## Cart manipulation

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-scripts/cart-manipulation.html

# Manipulate the Cart with App Scripts [​](#manipulate-the-cart-with-app-scripts)

If your app needs to manipulate the cart, you can do so by using the [`cart`](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#cart) script hook.

INFO

Note that app scripts were introduced in Shopware 6.4.8.0 and are not supported in previous versions.

## Overview [​](#overview)

The cart manipulation in app scripts expands on the general [cart concept](./../../../../concepts/commerce/checkout-concept/cart.html). In that concept, your cart scripts act as another [cart processor](./../../../../concepts/commerce/checkout-concept/cart.html#cart-processors---price-calculation-and-validation).

Your `cart` scripts run whenever the cart is calculated, this means that the script will be executed when an item is added to the cart, when the selected shipping and payment methods change, etc. You have access to a `cart`-service that provides a [fluent API](https://www.martinfowler.com/bliki/FluentInterface.html) to get data from the cart or to manipulate the cart. For an overview of all data and services that are available, please refer to the [cart hook reference](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#cart).

## Prerequisites [​](#prerequisites)

To get a better understanding of the cart, please make yourself familiar with the [cart concept](./../../../../concepts/commerce/checkout-concept/cart.html) in general. We will expand on that concept and refer to ideas defined there in this guide.

## Calculating the cart [​](#calculating-the-cart)

If you add line items (products, discounts, etc.) in your `cart`-script it may be necessary to manually recalculate the cart. After changing the price definitions in the cart, the total prices of the cart are not recalculated automatically. The recalculation will only happen automatically after your whole script is executed.

But if your script depends on updated and recalculated prices, you can recalculate the entire cart manually.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% do services.cart.products.add(productId) %}

{% do services.cart.calculate() %}
```

The `calculate()` call will recalculate the whole cart and update the total prices, etc. For this the complete [`process`-step](./../../../../concepts/commerce/checkout-concept/cart.html#calculation) is executed again.

WARNING

Note that by executing the `process` step, all properties of the cart (e.g. `products()`, `items()`, `price()`) are recreated and thus will return new instances. This means if your script still holds references to those properties inside variables from before the recalculation, those are outdated after the recalculation.

### Multiple calculations [​](#multiple-calculations)

Your `cart`-script will probably run multiple times per cart whenever the cart is recalculated, e.g., whenever a new product is added to the cart. This means that you have to check that your script works when it is executed multiple times.

The safest way to ensure is to check the cart to see if your script's action was already taken and only execute it if not. For example, you could only add a discount to the cart if it doesn't already exist.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% if not services.cart.has('my-custom-discount') %}
    {% do services.cart.discount('my-custom-discount', 'percentage', 10, 'A custom discount') %}
{% endif %}
```

An alternative solution would be to mark that you already did perform an action by adding a custom state to the cart. This way, you can only perform the action if your custom state is not present and additionally, you can remove the state again when you revert your action.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set isEligable = services.cart.items.count > 3 %}

{% if not services.cart.states.has('swag-my-state') %}

    {% if isEligable %}
        {# perform action #}
    {% endif %}

{% else %}

    {% if not isEligable %}
        {# revert action #}
    {% endif %}

{% endif %}
```

INFO

Note that the state name should be unique, this means you should always use your vendor prefix in the state name.

## Price definitions [​](#price-definitions)

In general, Shopware prices consist of gross and net prices and are currency dependent. If you need price definitions in your app scripts (e.g., to add an absolute discount with a specific price), there are multiple ways to do so.

### Price fields inside custom fields [​](#price-fields-inside-custom-fields)

You can define price fields for [custom fields](./../custom-data/custom-fields.html)

manifest.xml

xml

```shiki
<custom-fields>
    <custom-field-set>
        <name>custom_field_test</name>
        <label>Custom field test</label>
        <label lang="de-DE">Zusatzfeld Test</label>
        <related-entities>
            <product/>
            <customer/>
        </related-entities>
        <fields>
            <price name="test_price_field">
                <label>Test price field</label>
            </price>
        </fields>
    </custom-field-set>
</custom-fields>
```

### Price fields inside app config [​](#price-fields-inside-app-config)

You can define price fields for [app configuration](./../configuration.html).

xml

```shiki
// Resources/config/config.xml
<card>
    <title>Basic configuration</title>
    <title lang="de-DE">Grundeinstellungen</title>
    <name>TestCard</name>
    <input-field type="price">
        <name>priceField</name>
        <label>Test price field</label>
        <defaultValue>null</defaultValue>
    </input-field>
</card>
```

### Manual price definition [​](#manual-price-definition)

The simplest way is to define the price manually and hard code it into your app scripts. We provide a factory method that you can use to create price definitions. You can specify the `gross` and `net` prices for each currency.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set price = services.cart.price.create({
    'default': { 'gross': 19.99, 'net': 19.99},
    'EUR': { 'gross': 19.99, 'net': 19.99},
    'USD': { 'gross': 24.99, 'net': 21.37},
}) %}
```

### Prices inside the app config [​](#prices-inside-the-app-config)

As described above, it is also possible to use price fields inside the [app configuration](./../configuration.html). In your cart scripts, you can access those config values over the [`config` service](./../../../../resources/references/app-reference/script-reference/miscellaneous-script-services-reference.html#SystemConfigFacade) and pass them to the same price factory as the manual definitions.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set priceData = services.config.app('myCustomPrice') %}

{% set discountPrice = services.cart.price.create(priceData) %}
```

Note that if you don't provide a default value for your configuration, you should add a null-check, to verify that the config value you want to use was actually configured by the merchant.

## Line items [​](#line-items)

Inside your cart scripts, you can modify the line items inside the current cart.

### Add product a line item [​](#add-product-a-line-item)

You can add a new product line item simply by providing the product `id` of the product that should be added. Additionally, you may provide a quantity as a second parameter if the product should be added with a quantity higher than 1.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% do services.cart.products.add(productId) %}

{% do services.cart.products.add(productId, 4) %}
```

### Add an absolute discount [​](#add-an-absolute-discount)

To add an absolute discount, you can use the `discount()` function, but you have to define a [price definition](#price-definitions) beforehand. The first argument is the `id` of the line item. You can use that `id`, e.g., to check if the discount was already added to the cart. The fourth parameter is the label of the discount. You can either use a hard-coded string label or use the `|trans` filter to use a Storefront snippet as the label.

Note that you should check if your discount was already added, as your script may run multiple times.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set discountPrice = services.cart.price.create({
    'default': { 'gross': 19.99, 'net': 19.99},
    'EUR': { 'gross': 19.99, 'net': 19.99},
}) %}

{% if not services.cart.has('my-custom-discount') %}
    {% do services.cart.discount('my-custom-discount', 'absolute', discountPrice, 'my.custom.discount.label'|trans) %}
{% endif %}
```

### Add a relative discount [​](#add-a-relative-discount)

Adding a relative discount is very similar to adding an absolute discount. Instead of providing a price definition, you can provide a percentage value that should be discounted, and the absolute value will be calculated automatically based on the current total price of the cart.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% do services.cart.discount('my-custom-discount', 'percentage', 10, 'A custom 10% discount') %}
```

### Remove a line item [​](#remove-a-line-item)

You can remove line items by providing the `id` of the line item that should be removed.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{# first add the product #}
{% do services.cart.products.add(productId) %}
{# then remove it again #}
{% do services.cart.remove(productId) %}

{# first add the discount #}
{% do services.cart.discount('my-custom-discount', 'percentage', 10, 'A custom 10% discount') %}
{# then remove it again #}
{% do services.cart.remove('my-custom-discount') %}
```

## Split line items [​](#split-line-items)

It is also possible to split one line item with a quantity of 2 or more. You can use the `take()` method on the line item that should be split and provide the quantity that should be split from the original line item. Optionally you can provide the new `id` of the new line item as a second parameter.

Note that the `take()` method won't automatically add the new line item to the cart, but instead, it returns the split line item, so you have to add it to the corresponding line item collection manually in your script.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set existingLineItem = services.cart.products.get(productId) %}

{% if existingLineItem and existingLineItem.quantity > 3 %}
    {% set newLineItem = existingLineItem.take(2, newLineItemId) %}
    {% do services.cart.products.add(newLineItem) %}
{% endif %}
```

## Add custom data to line items [​](#add-custom-data-to-line-items)

You can add custom (meta-) data to line items in the cart by manipulating the payload of the cart items.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set lineItem = services.cart.get(lineItemId) %}
{# Add a custom payload value #}
{% do lineItem.payload.set('custom-payload', myValue) %}
{# Access the value #}
{%  set value = lineItem.payload['custom-payload']) %}
```

## Add errors and notifications to the cart [​](#add-errors-and-notifications-to-the-cart)

Your app script can block the cart's checkout by raising an error. As the first parameter you have to provide the [snippet key](./../../plugins/storefront/add-translations.html) of the error message that should be displayed to the user. As the second optional parameter, you can specify a `id` for the error, so you can reference the error later on in your script. Lastly, you can provide an array of parameters as the optional third parameter if you need to pass parameters to the snippet.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% if not cartIsValid %}
    {# add a new error #}
    {% do services.cart.errors.error('my-error-message', 'error-id') %}
{% else %}
    {% do services.cart.errors.remove('error-id') %}
{% endif %}
```

If you only want to display some information to the user during the checkout process, you can also add messages using `warning` and `notice`. Those will be displayed during the checkout process but won't prevent the customer from completing the checkout.

The API is basically the same as for adding errors.

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% do services.cart.errors.notice('my-notice') %}
```

## Rule based cart scripts [​](#rule-based-cart-scripts)

The cart scripts automatically integrate with the [Rule Builder](./../../../../concepts/framework/rule.html) and you can use the full power of the rule builder to only do your cart manipulations if a given rule matches. For example, you can add an entity-single-select field to your [app's config](./../configuration.html) to allow the merchant to choose a rule that needs to match your app script taking effect.

xml

```shiki
// Resources/config/config.xml
<card>
    <title>Basic configuration</title>
    <title lang="de-DE">Grundeinstellungen</title>
    <name>TestCard</name>
    <component name="sw-entity-single-select">
        <name>exampleRule</name>
        <entity>rule</entity>
        <label>Choose a rule that activates the cart script</label>
    </component>
</card>
```

Inside your cart script, you can check if the rule matches by checking if the configured rule id exists in the list of matched rule ids of the context:

twig

```shiki
// Resources/scripts/cart/my-cart-script.twig
{% set ruleId = services.config.app('exampleRule') %}

{% if ruleId and ruleId in hook.context.ruleIds %}
    {# perform action #}
{% else %}
   {# revert action #}
{% endif %}
```

## Further information [​](#further-information)

Take a look at the [cart manipulation script service reference](./../../../../resources/references/app-reference/script-reference/cart-manipulation-script-services-reference.html).

---

## Data loading

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-scripts/data-loading.html

# Load additional data for the Storefront with App Scripts [​](#load-additional-data-for-the-storefront-with-app-scripts)

If your app needs additional data in your [customized Storefront templates](./../../../plugins/plugins/storefront/customize-templates.html), you can load that data with app scripts and make it available to your template.

INFO

Note that app scripts were introduced in Shopware 6.4.8.0 and are not supported in previous versions.

## Overview [​](#overview)

The app script data loading expands on the general [composite data loading concept](./../../../../concepts/framework/architecture/storefront-concept.html#composite-data-handling) of the storefront. For each page that is rendered, a hook is triggered, giving access to the current `page` object. The `page` object gives access to all the available data, lets you add data to it, and will be passed directly to the templates.

For a list of all available script hooks that can be used to load additional data, take a look at the [script hook reference](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#data-loading).

INFO

Note that all hooks that were triggered during a page rendering are also shown in the [Symfony toolbar](./#developing--debugging-scripts). This may come in handy if you are searching for the right hook for your script.

For example, if you want to enrich a storefront detail page with additional data, you just set it within a custom app script and attach it to the `page` object.

twig

```shiki
// Resources/scripts/product-page-loaded/my-example-script.twig
{% set page = hook.page %}
{# @var page \Shopware\Storefront\Page\Product\ProductPage #}

{# the page object if you access to all the data, e.g., the current product #}
{% do page.product ... %}

{% set myAdditionalData = {
    'example': 'just an example'
} %}

{# it also lets you add data to it, that you can later use in your Storefront templates #}
{% do page.addArrayExtension('swagMyAdditionalData', myAdditionalData) %}
```

In your Storefront templates, you can read the data again from the `page` object:

twig

```shiki
// Resources/views/storefront/page/product-detail/index.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}

{% block page_product_detail %}
    <h1>{{ page.getExtension('swagMyAdditionalData').example }}</h1>
    
    {{ parent() }}
{% endblock %}
```

## Loading data [​](#loading-data)

To load data stored inside Shopware, you can use the `read` features of the [Data Abstraction Layer](./../../../../concepts/framework/data-abstraction-layer.html). Therefore, in every hook that may be used to load additional data, the `repository` service is available.

The `repository` service provides methods to load exactly the data you need:

* `search()` to load complete entities
* `ids()` to load only the ids of entities, if you don't need all the additional information of the entities
* `aggregate()` to aggregate data if you don't need any data of individual entities but are only interested in aggregated data

All those methods can be used in the same way. First, you pass the entity name the search should be performed on. Next, you pass the criteria that should be used.

twig

```shiki
{% set mediaEntities = services.repository.search('media', criteria) %}
```

### Search criteria [​](#search-criteria)

The search criteria define how the search is performed and what data is included. The criteria object that is used inside the app scripts behaves and looks the same as the [JSON criteria used for the API](./../../../integrations-api/general-concepts/search-criteria.html).

So please refer to that documentation to get an overview of what features can be used inside a criteria object.

[Search Criteria](../../../integrations-api/general-concepts/search-criteria)

The criteria object can be assembled inside scripts as follows:

twig

```shiki
{% set criteria = {
    'ids': [ 'id1', 'id2' ],
    'associations': {
        'manufacturer': {},
        'cover': {},
    },
    'filter': [
        { 'type': 'equals', 'field': 'active', 'value': true },
    ]
} %}

{% set matchedProducts = services.repository.search('product', criteria) %}
```

### `repository` and `store` services [​](#repository-and-store-services)

Besides the `repository` service, a separate `store` service is also available that provides the same basic functionality and the same interface.

The `store` service is available for all "public" entities (e.g. `product` and `category`) and will return a Storefront optimized representation of the entities. This means that, for example, SEO related data is resolved for `products` and `categories`, loaded over the `store` service, but not over the `repository` service. Additionally, product prices are only calculated using the `store` service.

INFO

The `store` service only loads "public" entities. This means that the entities only include ones that are active and visible for the current sales channel.

One major difference is that when using the `repository` service, your app needs `read` permissions for every entity it reads, whereas you don't need additional permissions for using the `store` service (as that service only searches for "public" data).

Refer to the [App Base Guide](./../app-base-guide.html#permissions) for more information on how permissions work for apps.

The `repository` service exposes the same data as the CRUD-operations of the [Admin API](./../../../integrations-api/#backend-facing-integrations---admin-api), whereas the `store` service gives access to the same data as the [Store API](./../../../integrations-api/#customer-facing-interactions---store-api).

For a full description of the `repository` and `store` service, take a look at the [services reference](./../../../../resources/references/app-reference/script-reference/data-loading-script-services-reference.html).

## Adding data to the page object [​](#adding-data-to-the-page-object)

There are two ways to add data to the page object, either with the `addExtension()` or the `addArrayExtension()` methods. Both methods expect the name under which the extension should be added as the first parameter. Under that name, you can later access the extension in your Storefront template with the `page.getExtension('extensionName')` call.

WARNING

Note that the extension names need to be unique. Therefore always use your vendor prefix as a prefix for the extension name.

The second argument for both methods is the data you want to add as an extension. The `addExtension` method needs to be a `Struct`, meaning you can only add PHP objects (e.g., the collection or entities returned by the `repository` service) directly as extensions. If you want to add scalar values or add more than one struct in your extension, you can wrap your data in a JSON-like twig object and use the `addArrayExtension` method.

In your **scripts** that would look something like this:

twig

```shiki
{% set products = services.repository.search('product', criteria) %}

{# via addExtension #}
{% do page.addExtension('swagCollection', products) %}
{% do page.addExtension('swagEntity', products.first) %}

{# via addArrayExtension #}
{% set arrayExtension = {
    'collection': products,
    'entity': products.first,
    'scalar': 'a scalar value',
} %}
{% do page.addArrayExtension('swagArrayExtension', arrayExtension) %}
```

You can access the extensions again in your **Storefront templates** like this:

twig

```shiki
{# via addExtension #}
{% for product in page.getExtension('swagCollection') %}
    ...
{% endfor %}

{% set product = page.getExtension('swagEntity') %}

{# via addArrayExtension #}
{% for product in page.getExtension('swagArrayExtension').collection %}
    ...
{% endfor %}

{% set product = page.getExtension('swagArrayExtension').entity %}

<h1>{{ page.getExtension('swagArrayExtension').scalar }}</h1>
```

INFO

Note that you can add extensions not only to the page object but to every struct. Therefore you can also add an extension, e.g., to every product inside the page.

---

## Custom endpoints

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/app-scripts/custom-endpoints.html

# Custom Endpoints with App Scripts [​](#custom-endpoints-with-app-scripts)

If you want to execute some logic in Shopware and trigger the execution over an HTTP request or need some special data from Shopware over the API, you can create custom API endpoints in your app that allow you to execute a script when a request to that endpoint is made.

## Manipulate HTTP-headers to API responses [​](#manipulate-http-headers-to-api-responses)

INFO

Note that the `response` hook was added in v6.6.10.4 and is not available in earlier versions.

There is a specific `response` script hook, that allows you to manipulate the HTTP-headers of the response via app scripts. This is especially useful to adjust the security headers to your needs.

To add a custom header to every response, you can do the following:

twig

```shiki
// Resources/scripts/response/response.twig
{% do hook.setHeader('X-Frame-Options', 'SAMEORIGIN') %}
```

Additionally, you can check the current value of a given header and adjust it accordingly:

twig

```shiki
// Resources/scripts/response/response.twig
{% if hook.getHeader('X-Frame-Options') == 'DENY' %}
    {% do hook.setHeader('X-Frame-Options', 'SAMEORIGIN') %}
{% endif %}
```

You also have access to the route name of the current request and to the route scopes to control the headers for specific routes:

twig

```shiki
// Resources/scripts/response/response.twig
{% if hook.routeName == 'frontend.detail.page' and hook.isInRouteScope('store-api') %}
    {% do hook.setHeader('X-Frame-Options', 'SAMEORIGIN') %}
{% endif %}
```

The possible route scopes are `storefront`, `store-api`, `api` and `administration`.

## Custom Endpoints [​](#custom-endpoints)

There are specialized script-execution endpoints for the `api`, `store-api` and `storefront` scopes. Refer to the [API docs](./../../../integrations-api/) for more information on the distinction of those APIs. Those endpoints allow you to trigger the execution of your scripts with an HTTP request against those endpoints.

Custom endpoint scripts need to be located in a folder that is prefixed with the name of the api scope (one of `api-`, `store-api-` or `storefront`). The remaining part of the folder name is the hook name. You can specify which script should be executed by using the correct hook name in the URL of the HTTP request.

This means to execute the scripts under `Resources/scripts/api-test-script` you need to call the `/api/script/test-script` endpoint. Note that all further slashes (`/`) in the route will be replaced by dashes (`-`). To execute the `Resources/scripts/api-test-script` scripts you could also call the `/api/script/test/script` endpoint.

WARNING

To prevent name collisions with other apps, you should always include your vendor prefix or app name as part of the hook name. The best practice is to add your app name after the API scope prefix and then use it as a REST style resource identifier, e.g., `/api/script/swagMyApp/test-script`.

In your custom endpoint scripts, you get access to the JSON payload of the request (and the query parameters for GET-requests) and have access to the read & write functionality of the [Data Abstraction Layer](./../../../../concepts/framework/data-abstraction-layer.html). For a complete overview of the available data and service, refer to the [hook reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#api-hook).

By default, a `204 No Content` response will be sent after your script was executed. To provide a custom response, you can use the [`response`-service](./../../../../resources/references/app-reference/script-reference/custom-endpoint-script-services-reference.html#scriptresponsefactoryfacade) to create a response and set it as the `response` of the hook:

twig

```shiki
// Resources/scripts/api-custom-endpoint/my-example-script.twig
{% set response = services.response.json({ 'foo': 'bar' }) %}
{% do hook.setResponse(response) %}
```

You can execute multiple scripts for the same HTTP request by storing multiple scripts in the same order. Those scripts will be executed in alphabetical order. Remember that later scripts may override the response set by prior scripts. If you want to prevent the execution of further scripts, you can do so by calling `hook.stopPropagation`:

twig

```shiki
// Resources/scripts/api-custom-endpoint/my-example-script.twig
{% do hook.stopPropagation() %}
```

### Admin API endpoints [​](#admin-api-endpoints)

Scripts available over the Admin API should be stored in a folder prefixed with `api-`, so the folder name would be `api-{hook-name}`. The execution of those scripts is possible over the `/api/script/{hook-name}` endpoint.

This endpoint only allows `POST` requests.

Caching of responses is not supported for Admin API responses.

For a complete overview of the available data and services, refer to the [reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#api-hook).

### Store API endpoints [​](#store-api-endpoints)

Scripts that should be available over the Store API should be stored in a folder prefixed with `store-api-`, so the folder name would be `store-api-{hook-name}`. The execution of those scripts is possible over the `/store-api/script/{hook-name}` endpoint.

This endpoint allows `POST` and `GET` requests.

This hook is an [Interface Hook](./#interface-hooks). The execution of your logic should be implemented in the `response` block of your script.

twig

```shiki
// Resources/scripts/store-api-custom-endpoint/my-example-script.twig
{% block response %}
    {% set response = services.response.json({ 'foo': 'bar' }) %}
    {% do hook.setResponse(response) %}
{% endblock %}
```

Caching of responses to `GET` requests is supported, but you need to implement the `cache_key` function in your script to provide a cache key for each response. The cache key you generate should take every permutation of the request, which would lead to a different response into account and should return a unique key for each permutation. A simple cache key generation would be to generate an `md5`-hash of all the incoming request parameters, as well as your hook's name:

twig

```shiki
// Resources/scripts/store-api-custom-endpoint/my-example-script.twig
{% block cache_key %}
    {% set cachePayload = hook.query %}
    {% set cachePayload = cachePayload|merge({'script': 'custom-endpoint'}) %}

    {% do hook.setCacheKey(cachePayload|md5) %}
{% endblock %}
```

For a complete overview of the available data and services, refer to the [reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#store-api-hook).

### Storefront endpoints [​](#storefront-endpoints)

Scripts available for the Storefront should be stored in a folder prefixed with `storefront-`, so the folder name would be `storefront-{hook-name}`. The execution of those scripts is possible over the `/storefront/script/{hook-name}` endpoint. Custom Storefront endpoints can be called by a normal browser request or from JavaScript via ajax.

This endpoint allows `POST` and `GET` requests.

Caching is supported and enabled by default for `GET` requests.

In addition to providing `JsonResponses` you can also render your own templates:

twig

```shiki
// Resources/scripts/storefront-custom-endpoint/my-example-script.twig
{% set product = services.store.search('product', { 'ids': [productId]}).first %}

{% do hook.page.addExtension('myProduct', product) %}

{% do hook.setResponse(
    services.response.render('@MyApp/storefront/page/custom-page/index.html.twig', { 'page': hook.page })
) %}
```

Additionally, it is also possible to redirect to an existing route:

twig

```shiki
// Resources/scripts/storefront-custom-endpoint/my-example-script.twig
{% set productId = hook.query['product-id'] %}

{% set response = services.response.redirect('frontend.detail.page', { 'productId': productId }) %}
{% do hook.setResponse(response) %}
```

For a complete overview of the available data and services, refer to the [reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#storefront-hook).

## Caching [​](#caching)

To improve the end-user experience and provide a scalable system, the customer-facing APIs (i.e., `store-api` and `storefront`) offer a caching mechanism to cache the response to specific requests and return the response from the cache on further requests instead of computing it again and again on each request.

By default, caching is enabled for custom endpoints, but for `store-api` endpoints you have to generate the cache key in the script. For `storefront` requests, however, shopware takes care of it so that responses get automatically cached (if the [HTTP-Cache](./../../../../concepts/framework/http_cache.html) is enabled).

### Cache Config [​](#cache-config)

You can configure the caching behavior for each response on the `response`-object in your scripts.

#### Add custom tags to the cache item [​](#add-custom-tags-to-the-cache-item)

To allow fine-grained [cache invalidation](#cache-invalidation) you can tag the response with custom tags and then invalidate certain tags in a `cache-invalidation` script.

twig

```shiki
{% set response = services.response.json({ 'foo': 'bar' }) %}
{% do response.cache.tag('my-custom-tag') %}

{% do hook.setResponse(response) %}
```

#### Disable caching [​](#disable-caching)

You can opt out of the caching by calling `cache.disable()`. This means that the response won't be cached.

twig

```shiki
{% set response = services.response.json({ 'foo': 'bar' }) %}
{% do response.cache.disable() %}

{% do hook.setResponse(response) %}
```

#### Set the max-age of the cache item [​](#set-the-max-age-of-the-cache-item)

You can specify for how long a response should be cached by calling the `cache.maxAge()` method and passing the number of seconds after which the cache item should expire.

> **Note:** `cache.maxAge()` is deprecated and will be removed in v6.8.0.0. Starting with v6.7.6.0, you can use `sharedMaxAge()` (corresponds to `s-maxage` in the `Cache-Control` header). When the `CACHE_REWORK` feature flag is enabled, you can also use `clientMaxAge()` (corresponds to `max-age` in the `Cache-Control` header).

twig

```shiki
{% set response = services.response.json({ 'foo': 'bar' }) %}
{% do response.cache.sharedMaxAge(120) %}

{% do hook.setResponse(response) %}
```

#### Invalidate cache items for specific states [​](#invalidate-cache-items-for-specific-states)

> **Note:** The cache states feature is deprecated and will be removed in v6.8.0.0. It also does not work when the `CACHE_REWORK` feature flag is enabled.

You can specify that the cached response is not valid if one of the given states is present. For more detailed information on the invalidation states, refer to the [HTTP-cache docs](./../../../../concepts/framework/http_cache.html#sw-states).

twig

```shiki
{% set response = services.response.json({ 'foo': 'bar' }) %}
{% do response.cache.invalidationState('logged-in') %}

{% do hook.setResponse(response) %}
```

### Cache invalidation [​](#cache-invalidation)

To prevent serving stale cache items, the cache needs to be invalidated if the underlying data changes. Therefore, you can add `cache-invalidation` scripts, where you can inspect each write operation in the system and invalidate specific cache items by tag.

In your `cache-invalidation` scripts, you can get the `ids` that were written for a specific entity, e.g., `product_manufacturer`.

twig

```shiki
// Resources/scripts/cache-invalidation/my-invalidation-script.twig
{% set ids = hook.event.getIds('product_manufacturer') %}

{% if ids.empty %}
    {% return %}
{% endif %}
```

To allow even more fine-grained invalidation, you can filter down the list of written entities by filtering for specific actions that were performed on that entity (e.g., `insert`, `update`, `delete`) and filter by which properties were changed.

twig

```shiki
// Resources/scripts/cache-invalidation/my-invalidation-script.twig
{% set ids = hook.event.getIds('product') %}

{% set ids = ids.only('insert') %} // filter by action = insert
{% set ids = ids.with('description', 'parentId') %} // filter all entities were 'description` OR `parentId` was changed
{% if ids.empty %}
    {% return %}
{% endif %}
```

Note that you can also chain the filter operations:

twig

```shiki
// Resources/scripts/cache-invalidation/my-invalidation-script.twig
{% set ids = hook.event.getIds('product') %}

{% set ids = ids.only('insert').with('description', 'parentId') %}
{% if ids.empty %}
    {% return %}
{% endif %}
```

You can then use the filtered-down list of ids to invalidate entity-specific tags:

twig

```shiki
{% set tags = [] %}
{% for id in ids %}
    {% set tags = tags|merge(['my-product-' ~ id]) %}
{% endfor %}

{% do services.cache.invalidate(tags) %}
```

For a complete overview of what data and services are available, refer to the [cache-invalidation hook reference documentation](./../../../../resources/references/app-reference/script-reference/script-hooks-reference.html#cache-invalidation).

---

## Storefront

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/storefront/

# Storefront [​](#storefront)

You can modify the whole appearance of the Storefront within your app. This includes [customizing templates](./../../apps/storefront/customize-templates.html), [adding custom Javascript](./../../plugins/storefront/add-custom-javascript.html) and [custom styling](./../../plugins/storefront/add-custom-styling.html).

As the Shopware server will build the Storefront, you don't have to set up any external servers for this. All you have to do is include your modifications (in form of `.html.twig`, `.js` or `.scss` files) inside the `Resources` folder of your app. The base folder structure of your app may look like this:

text

```shiki
└── DemoApp
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           ├── scss
    │   │           │   └── base.scss
    │   │           └── main.js
    │   ├── views
    │   │   └── storefront
    │   │       └── ...
    │   └── public
    │       └── ... // public assets go here
    └── manifest.xml
```

## Custom Assets in Apps [​](#custom-assets-in-apps)

INFO

Note that this feature was introduced in Shopware 6.4.8.0, and is not supported in previous versions.

You may want to include custom assets inside your app, like custom fonts, etc. Therefore, place the assets you need in the `/Resources/public` folder. All files inside this folder are available over the [asset-system](./../../plugins/storefront/add-custom-assets.html#adding-custom-assets-to-your-plugin).

## Custom Template Priority [​](#custom-template-priority)

INFO

Note that this feature was introduced in Shopware 6.4.12.0, and is not supported in previous versions.

You may want your templates loaded before or after other extensions. To do so, you can define a `template-load-priority` inside your `manifest.xml`. The default value to this is 0, with positive numbers your template will be loaded earlier, and with negative numbers later.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ....
    </meta>
    <storefront>
        <template-load-priority>100</template-load-priority>
    </storefront>    
</manifest>
```

---

## Apps as themes

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/storefront/apps-as-themes.html

# Apps as themes [​](#apps-as-themes)

It is absolutely possible to ship whole [themes](./../../themes/) inside an app. All you have to do is include your theme configuration (in the form of a [theme.json](./../../../plugins/themes/theme-configuration.html) file) inside your app's Resources folder.  
 So the folder structure of a theme may look like this:

text

```shiki
└── DemoTheme
      └── Resources
            └── ...
            └── theme.json
      └── manifest.xml
```

## Themes vs. "ordinary" apps [​](#themes-vs-ordinary-apps)

If your app provides a `theme.json` file, it is considered to be a theme. All the changes you make to the Storefront's appearance inside your theme will be visible only if your theme is assigned to the Storefront. In contrast, if you don't provide a `theme.json` file, your app is an "ordinary" app. The changes will be applied to all sales channels automatically, as long as your app is active.

## Migrating existing themes [​](#migrating-existing-themes)

If you have already created Shopware 6 themes via plugins, it is effortless to migrate them to the app system. Don't worry, you don't have to do all the work twice. Instead of providing a `composer.json` and plugin base class, provide a `manifest.xml` file with the metadata for your app. After you have created a new folder for your app and added the `manifest.xml`, you can copy the `YourThemePlugin/src/Resources` folder from your plugin to the `YourThemeApp/Resources` folder inside your app. It should not be necessary to change anything inside your template or Javascript code.

---

## Customize templates

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/storefront/customize-templates.html

# Customize Templates [​](#customize-templates)

## Overview [​](#overview)

This guide will cover customizing Storefront templates using an app.

## Prerequisites [​](#prerequisites)

Before you begin, make sure you have:

* A basic understanding of [Shopware app development](./../app-base-guide.html).
* Familiarity with the [Twig template](https://twig.symfony.com/) is beneficial.

## Getting started [​](#getting-started)

This guide assumes you have already set up your Shopware app. If not, refer to the [app base guide](./../app-base-guide.html) for the initial setup.

The following sections give you a very short example of how you can extend a storefront block. For simplicity's sake, only the page logo is replaced with a 'Hello world!' text.

### Setting up app's view directory [​](#setting-up-app-s-view-directory)

First of all, in your app's root, register your app's own view path, which basically represents a path in which Shopware 6 is looking for template-files. By default, Shopware 6 is looking for a directory called `views` in your app's `Resources` directory, so the path could look like this: `<app root>/Resources/views`

### Locating the template [​](#locating-the-template)

As mentioned earlier, this guide is only trying to replace the 'demo' logo with a 'Hello world!' text. In order to find the proper template, you can simply search for the term 'logo' inside the `<shopware root>/src/Storefront` directory. This will eventually lead you to [this file](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/views/storefront/layout/header/logo.html.twig).

INFO

There's a plugin out there called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper), that adds hints about template blocks and includes into the rendered HTML. This way, it's easier to actually find the proper template.

### Overriding the template [​](#overriding-the-template)

Now that you have found the proper template for the logo, you can override it.

Overriding this file now requires you to copy the exact same directory structure starting from the `views` directory for your custom file. In this case, the file `logo.html.twig` is located in a directory called `storefront/layout/header`, so make sure to remember this path.

Finally, you have to set up the following directory path in your app: `<app root>/Resources/views/storefront/layout/header`. Next, create a new file called `logo.html.twig`, just like the original file. Once more to understand what's going on here: In the Storefront code, the path to the logo file looks like this: `Storefront/Resources/views/storefront/layout/header/logo.html.twig`. Now have a look at the path being used in your app: `<app root>/Resources/views/storefront/layout/header/logo.html.twig`

Starting from the `views` directory, the path is **exactly the same**, and that's the important part for your custom template to be loaded automatically.

### Customizing the template [​](#customizing-the-template)

First extend from the original file, to override its blocks. Now fill your custom `logo.html.twig` file.

Put this line at the very beginning of your file:

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}
```

This is simply extending the `logo.html.twig` file from the Storefront bundle. If you would leave the file like that, it wouldn't change anything, as you are currently just extending from the original file with no overrides.

To replace the logo with some custom text, take a look at the block called `layout_header_logo_link` in the original file. Its contents create an anchor tag, which is not necessary for our case anymore, so this seems to be a great block to override.

To override it now, just add the very same block into your custom file and replace its contents:

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}

{% block layout_header_logo_link %}
    <h2>Hello world!</h2>
{% endblock %}
```

If you wanted to append your text to the logo instead of replacing it, you could add a line like this to your override: `{{ parent() }}`

And that's it, you are done. However, you might have to clear the cache and refresh your storefront to see your changes in action. This can be done by using the following command:

bash

```shiki
./bin/console cache:clear
```

INFO

Also remember to not only activate your app but also to assign your theme to the correct sales channel by clicking on it in the sidebar, going to the tab Theme and selecting your theme.

### Finding variables [​](#finding-variables)

Of course, this example is very simplified and does not use any variables, even though you most likely want to do that. Using variables is exactly the same as in [Twig](https://twig.symfony.com/doc/3.x/templates.html#variables) in general, so this won't be explained here in detail. However, this is how you use a variable: `{{ variableName }}`

But how do you know which variables are available to use? For this, you can just dump all available variables:

twig

```shiki
{{ dump() }}
```

This `dump()` call will print out all variables available on this page.

INFO

Once again, the plugin called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper) adds all available page data to the Twig tab in the profiler, when opening a request and its details. This might help here as well.

---

## Add cookies to the consent manager

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/storefront/cookies-with-apps.html

# Add cookies to the consent manager [​](#add-cookies-to-the-consent-manager)

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of apps.

[App Base Guide](../app-base-guide)

INFO

For a comprehensive understanding of Shopware's cookie consent system, see the [Cookie Consent Management Concept](./../../../../concepts/commerce/content/cookie-consent-management.html).

## Create a single cookie [​](#create-a-single-cookie)

To add new cookies to the cookie consent manager, you can add a `cookies` section to your `manifest.xml`. Inside this section, you can add new `cookie` elements, as shown in the following example. Note that you don't need a `setup` section in your `manifest.xml` since extending the Storefront doesn't need a registration nor an own server to run.

XML

```shiki
<?XML version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/refs/tags/v6.7.4.0/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <cookie>
            <cookie>my-cookie</cookie>
            <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
            <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
            <value>a static value for the cookie</value>
            <expiration>1</expiration>
        </cookie>
    </cookies>
</manifest>
```

Cookie elements can be configured by adding the following child elements:

* `cookie` (required): The technical name of the cookie. The value is used to store the cookie in the customer's cookie jar.
* `snippet-name` (required): A string that represents the label of the cookie in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.
* `value` (optional): A fixed value that is set as the cookie's value when the customer accepts your cookie. **If unset, the cookie will not be updated (set active or inactive) by Shopware, but passed to the update event.**
* `expiration` (optional): Cookie lifetime in days. **If unset, the cookie expires with the session.**
* `snippet-description` (optional): A string that represents the description of the cookie in the cookie consent manager. To provide translations, this should be the key of a Storefront snippet.

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

## Create a cookie group [​](#create-a-cookie-group)

When adding multiple cookies through your app, it may become handy to group them. This makes it possible for the customer to accept all of your cookies at once and additionally enhances the readability of the cookie consent manager.

To add a cookie group, you can add a `groups` section within your `cookies` section in your `manifest.xml`. In the following example, we use the cookie that we created in the previous section but display it in a cookie group:

XML

```shiki
<?XML version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/refs/tags/v6.7.4.0/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <group>
            <snippet-name>example-app-with-cookies.cookie-group.name</snippet-name>
            <snippet-description>example-app-with-cookies.cookie-group.description</snippet-description>
            <entries>
                <cookie>
                    <cookie>my-cookie</cookie>
                    <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
                    <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
                    <value>a static value for the cookie</value>
                    <expiration>1</expiration>
                </cookie>
            </entries>
        </group>
    </cookies>
</manifest>
```

A `group` element consists of three child elements to configure the cookie group. Here is a description of all of them:

* `snippet-name` (required): A string that represents the label of the cookie group in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.
* `entries` (required): Contains the grouped cookies. It is a collection of `cookie` elements described in the previous section.
* `snippet-description` (optional): A string that represents the description of the cookie group in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

## Assigning Cookies to Standard Cookie Groups [​](#assigning-cookies-to-standard-cookie-groups)

You can assign your app's cookies to Shopware's standard cookie groups by using one of the built-in snippet names in your `manifest.xml`: `cookie.groupRequired`, `cookie.groupComfortFeatures`, `cookie.groupStatistical`, and `cookie.groupMarketing`.

The following example shows how to assign cookies to the **Marketing group**:

XML

```shiki
<?XML version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/refs/tags/v6.7.4.0/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>MyApp</name>
        <label>My App</label>
        <version>1.0.0</version>
        <author>Your Name</author>
    </meta>

    <cookies>
        <!-- Marketing/Tracking cookies go to Marketing group -->
        <group>
            <snippet-name>cookie.groupMarketing</snippet-name>
            <entries>
                <cookie>
                    <cookie>myapp_conversion_tracking</cookie>
                    <snippet-name>myapp.cookie.conversionTracking</snippet-name>
                    <snippet-description>myapp.cookie.conversionTrackingDescription</snippet-description>
                    <value>1</value>
                    <expiration>90</expiration>
                </cookie>
                <cookie>
                    <cookie>myapp_ad_targeting</cookie>
                    <snippet-name>myapp.cookie.adTargeting</snippet-name>
                    <value>1</value>
                    <expiration>365</expiration>
                </cookie>
            </entries>
        </group>
    </cookies>
</manifest>
```

## Snippet handling [​](#snippet-handling)

As already mentioned in the previous sections, both the `cookie` and the `group` elements can contain `snippet-name` and `snippet-description` child elements. Although their values can be strings that will be displayed in the Storefront, the preferred way to set up cookie names and descriptions is to provide Storefront snippets. It gives you and the shop owner the possibility to add translations for your cookie's name and description.

If you are not familiar with setting up Storefront snippets, please refer to our snippet guide.

[Add translations](../../plugins/storefront/add-translations)

## Automatic Configuration Change Detection [​](#automatic-configuration-change-detection)

Any changes made to the cookie definitions in your app's `manifest.xml` are automatically detected by Shopware's consent system. This will trigger a re-consent flow for users, ensuring they are always prompted about the latest cookie settings.

This process is handled by a configuration hash mechanism, which is explained in detail in the [Cookie Consent Management Concept](./../../../../concepts/commerce/content/cookie-consent-management.html#configuration-hash-mechanism).

## Reacting to cookie consent changes [​](#reacting-to-cookie-consent-changes)

As described in the previous section, `cookie` elements without a `value` element will not be set automatically. Instead, you have to react to cookie consent changes within your JavaScript. Find out how to [respond to cookie consent changes](./../../../plugins/plugins/storefront/reacting-to-cookie-consent-changes.html).

---

## Flow Builder

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/flow-builder/

# Flow Builder [​](#flow-builder)

Shopware allows you to extend the functionality of the flow builder by adding custom flow actions from an app. By creating a custom app and defining your own flow actions, you can incorporate unique logic and behavior into the flow builder's workflows. This enables you to create more advanced and tailored automation processes within your online store, enhancing the efficiency and customization of your business operations.

---

## Add custom flow action from app system

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/flow-builder/add-custom-flow-actions-from-app-system.html

# Add custom flow actions [​](#add-custom-flow-actions)

INFO

Custom flow actions in Shopware Apps are available starting with Shopware 6.4.10.0 and are not supported in previous versions.

Besides the default actions, developers can add custom, predefined, and configurable web hook actions to the flow builder.

![Custom flow action in Administration](/assets/flow-builder-app-action-preview.B4KvwLQl.png)

After reading, you will be able to

* Create the basic setup of an app
* Create custom actions for the flow builder
* Use custom actions to interact with third-party services

## Prerequisites [​](#prerequisites)

Please make sure you already have a working Shopware 6 store running (either cloud or self-hosted). Prior knowledge about the Flow Builder feature of Shopware 6 is useful.

Please see the [Flow Builder Concept](./../../../../concepts/framework/flow-concept.html) for more information.

## Create the app wrapper [​](#create-the-app-wrapper)

To get started with your app, create an `apps` folder inside the `custom` folder of your Shopware dev installation. In there, create another directory for your application and provide a `manifest.xml` file, following the structure below:

text

```shiki
└── custom
    ├── apps
    │   └── FlowBuilderActionApp
    │       └── Resources
    │           └── flow-action.xml
    │           └── app-icon.png
    │           └── discord-icon.png
    │       └── manifest.xml
    └── plugins
```

INFO

From 6.5.2.0, you can define the flow action in `flow.xml`. The `flow-action.xml` will be removed from 6.6.0.0.

| File name | Description |
| --- | --- |
| FlowBuilderActionApp | Your app's technical name |
| app-icon.png | The app's icon |
| slack-icon.png | Your action icon will be defined for each action in the `flow-action.xml` file. (optional, icons will default to a fallback) |
| flow-action.xml | Place to define your new actions |
| manifest.xml | Base information about your app |

### Manifest file [​](#manifest-file)

The manifest file is the central point of your app. It defines the interface between your app and the Shopware instance. It provides all the information concerning your app, as seen in the minimal version below:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>FlowBuilderActionApp</name>
        <label>Flow Builder Action App</label>
        <label lang="de-DE">Flow Builder Aktions-App</label>
        <description>This is the example description for app</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>4.14.0</version>
        <icon>Resources/app-icon.png</icon>
        <license>MIT</license>
    </meta>
</manifest>
```

WARNING

The name of your app that you provide in the manifest file needs to match the folder name of your app.

## Define the flow action [​](#define-the-flow-action)

To create a flow action, you need to define a `<flow-action>` block within a file called `flow-action.xml`. Each `<flow-action>` represents one action and you can define an arbitrary number of actions.

Resources/flow-action.xml

xml

```shiki
<flow-actions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-action>
        ... # The first action
    </flow-action>
    <flow-action>
        ... # The second action
    </flow-action>
    <flow-action>
        ... # The third action
    </flow-action>
    ...
</flow-actions>
```

From 6.5.2.0, to create a flow action, you must define a `<flow-actions>` block within a file called `flow.xml`. Each `<flow-action>` in `<flow-actions>` represents one action, and you can define an arbitrary number of actions.

xml

```shiki
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-actions>
        <flow-action>
            ... # The first action
        </flow-action>
        <flow-action>
            ... # The second action
        </flow-action>
        <flow-action>
            ... # The third action
        </flow-action>
    </flow-actions>
    ...
</flow-extensions>
```

A single flow action would look like this:

xml

```shiki
<flow-action>
    <meta>
        <name>slackmessage</name>
        <label>Send slack message</label>
        <label lang="de-DE">Slack-Nachricht senden</label>
        <badge>Slack</badge>
        <description>Slack send message description</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <url>https://hooks.slack.com/services/{id}</url>
        <sw-icon>default-communication-speech-bubbles</sw-icon>
        <icon>slack.png</icon>
        <requirements>orderAware</requirements>
        <requirements>customerAware</requirements>
    </meta>
    ...
</flow-action>
```

| Key | Required | Description |
| --- | --- | --- |
| name | yes | The technical name of your action, unique for all actions |
| label | yes | A name to be shown for your action in the actions list or action modal title |
| badge | no | An attached badge shown behind the label in the action modal title |
| description | yes | Detailed information for your action |
| sw-icon | no | An icon component name from the [icon library](https://shopware.design/icons/) |
| icon | no | Alternatively, a path to your action icon. In the case you define both `<sw-icon>` and `<icon>`, the `<icon>` will be take precedence in this case. |
| requirements | yes | Available action triggers, read more below |
| url | yes | External webhook location. Shopware will call this URL when the action is executed |

**requirements**

Requirements will decide for which trigger events your action is available. Example: The `checkout.order.placed` trigger has an `orderAware` requirement, indicating that your action is allowed to be used in the `checkout.order.placed` event. It is defined using `<requirements>orderAware</requirements>` in your app action definition.

For each value when you define, it'll represent one of the `aware` interfaces from the `core`.

To fulfill the requirements, refer to a subset of action triggers aware:

| Value | Interface |
| --- | --- |
| customerAware | Shopware\Core\Framework\Event\CustomerAware |
| customerGroupAware | Shopware\Core\Framework\Event\CustomerGroupAware |
| delayAware | Shopware\Core\Framework\Event\DelayAware |
| mailAware | Shopware\Core\Framework\Event\MailAware |
| orderAware | Shopware\Core\Framework\Event\OrderAware |
| salesChannelAware | Shopware\Core\Framework\Event\SalesChannelAware |
| userAware | Shopware\Core\Framework\Event\UserAware |

### Header parameters [​](#header-parameters)

xml

```shiki
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        <parameter type="string" name="content-type" value="application/json"/>
    </headers>
    ...
</flow-action>
```

| Key | Description |
| --- | --- |
| type | Parameter type - currently only `string` supported |
| name | The header key |
| value | The header value |

### Parameters [​](#parameters)

xml

```shiki
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        ...
    </headers>
    <parameters>
        <parameter type="string" name="text" value="{{ message }} \n Order Number: {{ order.orderNumber }}"/>
    </parameters>
    ...
</flow-action>
```

Define the `parameter` for the URL body based on your URL webhook services.

| Key | Description |
| --- | --- |
| type | Type of parameter, only support `string` type. |
| name | The body key for your URL. |
| value | The content message for your URL; free to design your content message here. |
| `{{ message }}` | The variable from your `<input-field>` defined in `flow-action.xml`. |
| `{{ order.orderNumber }}` | For each trigger event, the action will have the variables suitable. [Read more variables here](./../../../../resources/references/app-reference/flow-action-reference.html). |

With the parameters configured as described above, an exemplary call of your Webhook Action could look like this:

text

```shiki
    POST https://hooks.slack.com/services/{id} {
        headers:
            content-type: application/json
        body:
            text: {{ message }} \n Order Number: {{ order.orderNumber }}
    }
```

### Action configuration [​](#action-configuration)

You can make your flow action configurable in the Administration by adding input fields. Based on your configuration - similar to the [app configurations](./../../plugins/plugin-fundamentals/add-plugin-configuration.html) - you can later on use these configuration values within flow parameters.

xml

```shiki
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        ...
    </headers>
    <parameters>
        ...
    </parameters>
    <config>
        <input-field type="text">
            <name>message</name>
            <label>Message</label>
            <label lang="de-DE">Gegenstand</label>
            <place-holder>Placeholder</place-holder>
            <place-holder lang="de-DE">Platzhalter</place-holder>
            <required>true</required>
            <helpText>Help Text</helpText>
            <helpText lang="de-DE">Hilfstext</helpText>
        </input-field>
    </config>
</flow-action>
```

Available input field attributes:

| Key | Required |
| --- | --- |
| name | Yes |
| label | Yes |
| place-holder | No |
| required | No |
| helpText | No |

You assemble your configuration from a variety of input fields.

INFO

To get more information on how to create configuration forms, see [Plugin Configurations](./../../plugins/plugin-fundamentals/add-plugin-configuration.html#the-different-types-of-input-field).

| Type | Shopware component |
| --- | --- |
| text | `<sw-text-field/>` |
| textarea | `<sw-textarea-field/>` |
| text-editor | `<sw-text-editor/>` |
| url | `<sw-url-field/>` |
| password | `<sw-password-field/>` |
| int | `<sw-number-field/>` |
| float | `<sw-number-field/>` |
| bool | `<sw-switch-field/>` |
| checkbox | `<sw-checkbox-field/>` |
| datetime | `<sw-datepicker/>` |
| date | `<sw-datepicker/>` |
| time | `<sw-datepicker/>` |
| colorpicker | `<sw-colorpicker/>` |
| single-select | `<sw-single-select/>` |
| multi-select | `<sw-multi-select/>` |

## Install the App [​](#install-the-app)

The app can now be installed by running the following command:

bash

```shiki
bin/console app:install --activate FlowBuilderActionApp
```

## Further steps [​](#further-steps)

* [Flow action example configuration](./../../../../resources/references/app-reference/flow-action-reference.html) page
* [Schema definition for flow actions (GitHub)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd)`

---

## Add custom flow trigger from app system

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/flow-builder/add-custom-flow-triggers-from-app-system.html

# Add custom flow trigger [​](#add-custom-flow-trigger)

INFO

The Shopware app custom flow triggers are only accessible from 6.5.3.0 and later versions.

In addition to the default triggers, you have the option to incorporate custom, pre-defined, and adjustable triggers into the flow builder.

![Custom flow trigger in Administration](/assets/flow-builder-custom-trigger-preview.CZ8aqeNS.png)

After reading, you will be able to :

* Create the basic setup of an app.
* Create custom triggers for the flow builder.
* Use an API to interact with custom triggers.

## Prerequisites [​](#prerequisites)

Please ensure you have a working Shopware 6 store (either cloud or self-hosted). Prior knowledge about the Flow Builder feature of Shopware 6 is useful.

Please see the [Flow Builder Concept](./../../../../concepts/framework/flow-concept.html) for more information.

## Create the app wrapper [​](#create-the-app-wrapper)

To get started with your app, create an `apps` folder inside the `custom` folder of your Shopware dev installation. Next, create another directory inside for your application and provide a `manifest.xml` file following the structure below:

text

```shiki
└── custom
    ├── apps
    │   └── FlowBuilderTriggerApp
    │       └── Resources
    │           └── app
    │               └── administration
    │                   └── snippet
    │                       └── de-DE.json
    │                       └── en-GB.json
    │           └── flow.xml
    │       └── manifest.xml
    └── plugins
```

| File name | Description |
| --- | --- |
| FlowBuilderTriggerApp | Your app's technical name |
| flow.xml | Place to define your new triggers |
| de-DE.json | Snippet to translate your trigger name for Deutsch |
| en-GB.json | Snippet to translate your trigger name for English |
| manifest.xml | Base information about your app |

### Manifest file [​](#manifest-file)

The manifest file is the central point of your app. It defines the interface between your app and the Shopware instance. It provides all the information concerning your app, as seen in the minimal version below:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>FlowBuilderTriggerApp</name>
        <label>Flow Builder Trigger App</label>
        <label lang="de-DE">Flow Builder Abzug-App</label>
        <description>This is the example description for app</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>4.14.0</version>
        <icon>Resources/app-icon.png</icon>
        <license>MIT</license>
    </meta>
</manifest>
```

WARNING

The name of your app that you provide in the manifest file needs to match the folder name of your app.

## Define the flow trigger [​](#define-the-flow-trigger)

To create a flow trigger, you need to define a `<flow-event>` block within a file called `flow.xml`. Each `<flow-event>` represents one trigger, and you can define an arbitrary number of events.

Resources/flow.xml

xml

```shiki
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-events>
        <flow-event>
            ... # The first trigger
        </flow-event>
        <flow-event>
            ... # The second trigger
        </flow-event>
    </flow-events>
    ...
</flow-extensions>
```

A single flow trigger would look like this:

xml

```shiki
<flow-event>
    <name>swag.before.open_the_doors</name>
    <aware>orderAware</aware>
</flow-event>
```

| Key | Required | Description |
| --- | --- | --- |
| name | yes | The technical name of your trigger, unique for all actions. |
| aware | no | Filter actions for your trigger, read more below. |

**aware**

The `aware` will decide which actions are available for your trigger.

***Example***

If you define the `orderAware` in your trigger config `<aware>orderAware</aware>`, the actions related to the Order will be available when the trigger is selected.

* action.add.order.tag,
* action.remove.order.tag,
* action.generate.document,
* action.grant.download.access,
* action.set.order.state,
* action.add.order.affiliate.and.campaign.code,
* action.set.order.custom.field,
* action.stop.flow

If you define the `customerAware` in your trigger config `<aware>orderAware</aware>`, the actions related to Customer will be available when the trigger is selected.

* action.add.customer.tag
* action.remove.customer.tag
* action.change.customer.group
* action.change.customer.status
* action.set.customer.custom.field
* action.add.customer.affiliate.and.campaign.code
* action.stop.flow

Each value defined, it represents one of the `aware` interfaces from the `core`.

To fulfill the `aware`, refer to a subset of action triggers aware:

| Value | Interface |
| --- | --- |
| customerAware | Shopware\Core\Framework\Event\CustomerAware |
| customerGroupAware | Shopware\Core\Framework\Event\CustomerGroupAware |
| delayAware | Shopware\Core\Framework\Event\DelayAware |
| mailAware | Shopware\Core\Framework\Event\MailAware |
| orderAware | Shopware\Core\Framework\Event\OrderAware |
| salesChannelAware | Shopware\Core\Framework\Event\SalesChannelAware |
| userAware | Shopware\Core\Framework\Event\UserAware |

Please refer to the [Schema definition for flow events (GitHub)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd) for more information.

## Trigger API [​](#trigger-api)

We provided an API with the endpoint `POST: /api/_action/trigger-event/{eventName}` to dispatch the custom trigger when you call the API. The app calls the API to trigger the custom event and can provide the data. The API will create a CustomAppEvent object and dispatch it with the data provided. The data given will be saved through `StorableFlow`. This can be utilized for actions or email templates.

Here is an example to define data from the API:

json

```shiki
    {
        "customerId": "d20e4d60e35e4afdb795c767eee08fec",
        "salesChannelId": "55cb094fd1794d489c63975a6b4b5b90",
        "shopName": "Shopware's Shop",
        "url": "https://shopware.com" 
    }
```

Flow actions can retrieve the data from FlowStorer.

php

```shiki
    $salesChanelId = $flow->getData(MailAware::SALES_CHANNEL_ID));
    $customer = $flow->getData(CustomerAware::CUSTOMER_ID));
```

Or we can use the data when defining the email template.

html

```shiki
    <h3>Welcome to {{ shopName }}</h3>
    <h1>Visit us at: {{ url }} </h1>
```

Please see the [StorableFlow Concept](./../../../../resources/references/adr/2022-07-21-adding-the-storable-flow-to-implement-delay-action-in-flow-builder.html) for more information.

## Snippet for translation [​](#snippet-for-translation)

You can define snippets to translate your custom trigger to show the trigger tree and flow list. Refer to the [Adding snippets](./../../plugins/administration/templates-styling/adding-snippets.html) guide for more information.

Snippet keys should be defined based on your trigger name defined at `<name>` in your `flow.xml`.

| Fixed key | Description |
| --- | --- |
| sw-flow-custom-event | All the keys related to the custom trigger will be defined inside |
| event-tree | All the keys used to trigger the tree will be defined inside |
| flow-list | All the keys used to flow list will be defined inside |

***Example***

xml

```shiki
// Resources/flow.xml
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-events>
        <flow-event>
            <name>swag.before.open_the_doors</name>
            ...
        </flow-event>
    </flow-events>
</flow-extensions>
```

javascript

```shiki
// custom/apps/FlowBuilderTriggerApp/Resources/app/administration/snippet/en-GB.json
{
  "sw-flow-custom-event": {
    "event-tree": {
      "swag": "Swag",
      "before": "Before",
      "openTheDoors": "Open the doors"
    },
    "flow-list": {
      "swag_before_open_the_doors": "Before open the doors"
    }
  }
}
```

## Install the App [​](#install-the-app)

The app can now be installed by running the following command:

bash

```shiki
bin/console app:install --activate FlowBuilderTriggerApp
```

---

## Custom Data

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/custom-data/

# Custom data [​](#custom-data)

You are able to store custom data in Shopware which you can use for your apps. You can store simple data types like strings, numbers, booleans, arrays and objects directly in core tables via [custom fields](./custom-fields.html) or define complete new entities with own associations and lifecycle via [custom entities](./custom-entities.html).

---

## Custom fields

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/custom-data/custom-fields.html

# Custom Data [​](#custom-data)

You can add custom fields to Shopware and thus add your own fields to extending data records. The user is able to modify this fields from within the Shopware Administration.  
 To make use of the custom fields, register your custom field sets in your manifest file:

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <custom-fields>
        <custom-field-set>
            <name>swag_example_set</name>
            <label>Example Set</label>
            <label lang="de-DE">Beispiel-Set</label>
            <related-entities>
                <order/>
            </related-entities>
            <fields>
                <text name="swag_code">
                    <position>1</position>
                    <label>Example field</label>
                </text>
            </fields>
        </custom-field-set>
    </custom-fields>
</manifest>
```

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

For the data needed, please refer to the custom fields in general: At first, you need a custom field set, as [custom fields](./../../plugins/framework/custom-field/) in Shopware are organised in sets. Here you need to consider some important fields:

* `name`: A technical name for your set
* `label`: This element provides the label of the text and can be used for defining translations of the label as well.
* `related-entities`: With this element set the entities the custom field set is used in
* `fields`: Finally, the fields are configured in this section.

WARNING

The names of the custom fields are global and therefore should always contain a vendor prefix, like "swag" for "shopware ag", to keep them unique. This holds true for the name of the custom field set, as well as each name of the fields itself.

When defining custom fields in the `<fields>` element, you can configure additional properties of the fields. For example a `placeholder`, `min`, `max` and `step` size of a float field:

html

```shiki
<float name="swag_test_float_field">
    <label>Test float field</label>
    <label lang="de-DE">Test-Kommazahlenfeld</label>
    <help-text>This is an float field.</help-text>
    <position>2</position>
    <placeholder>Enter an float...</placeholder>
    <min>0.5</min>
    <max>1.6</max>
    <steps>0.2</steps>
</float>
```

Refer to the [custom field](./../../plugins/framework/custom-field/) documentation for further details.

---

## Custom entities

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/custom-data/custom-entities.html

# Custom entities [​](#custom-entities)

In addition to [Custom fields](./custom-fields.html), you can create completely own entities in the system, named custom entities. Unlike [Custom fields](./custom-fields.html), you can generate completely custom data structures with custom relations, which can then be maintained by the admin. To make use of the custom entities register your entities in your `entities.xml` file, which is located in the `Resources` directory of your app.

xml

```shiki
// <app root>/Resources/entities.xml
<?xml version="1.0" encoding="utf-8" ?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/CustomEntity/Xml/entity-1.0.xsd">
    <entity name="custom_entity_bundle">
        <fields>
            <string name="name" required="true" translatable="true" store-api-aware="true" />
            <price name="discount" required="true" store-api-aware="true"/>
            <many-to-many name="products" reference="product" store-api-aware="true" />
        </fields>
    </entity>
</entities>
```

For a complete reference of the structure of the entities file take a look at the [Custom entity xml reference](./../../../../resources/references/app-reference/entities-reference.html).

## Functionality [​](#functionality)

All registered entities will get an automatically registered repository. It is also available in the [App scripts](./../app-scripts/) section, in case you are allowed to access the repository service inside the hook.

twig

```shiki
{% set blogs = services.repository.search('custom_entity_blog', criteria) %}
```

Additionally, to the repository you can also access your custom entities via [Admin api](./../../../../concepts/api/admin-api.html).

bash

```shiki
POST /api/search/custom-entity-blog
```

## Using Custom Entities with Custom Fields [​](#using-custom-entities-with-custom-fields)

INFO

The ability to use custom entities with custom fields is available since Shopware 6.5.1.0.

By default, it is not possible to create a custom field of type "Entity Select", which references a custom entity. However, you can opt in to this behavior. You will need to add the `custom-fields-aware` & `label-property` attributes to your entity definition:

xml

```shiki
// Resources/entities.xml
<?xml version="1.0" encoding="utf-8" ?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/CustomEntity/Xml/entity-1.0.xsd">
    <entity name="custom_entity_bundle" custom-fields-aware="true" label-property="name">
        <fields>
            <string name="name" required="true" translatable="true" store-api-aware="true" />
            <price name="discount" required="true" store-api-aware="true"/>
            <many-to-many name="products" reference="product" store-api-aware="true" />
        </fields>
    </entity>
</entities>
```

To enable the usage of custom fields, the `custom-fields-aware` setting should be set to true. Then, it is necessary to indicate a label field for the entity that will be used when selecting via the custom field. In this example, the `name` field is selected as the `label-property` field. It is important to note that this field must be included in the `fields` section of the entity definition and be of type `string`.

Now you will find your entity in the "Entity Type" select when creating a custom field of type "Entity Select". Without a snippet label for the entity, it will display as `custom_entity_bundle.label`. You can create a snippet to add a label like so:

javascript

```shiki
// Resources/app/administration/snippet/en-GB.json
{
  "custom_entity_bundle": {
    "label": "My Custom Entity"
  }
}
```

## Permissions [​](#permissions)

Unlike core entities, your app directly has full access rights to your own custom entities. However, if your entity has associations that reference core tables, you need the appropriate [permissions](./../../../../resources/references/app-reference/manifest-reference.html) to load and write these associations.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
    <permissions>
        <read>product</read>
<!--    <read>custom_entity_blog</read>   < permissions for own entities are automatically set  -->
    </permissions>
</manifest>
```

## Shorthand prefix [​](#shorthand-prefix)

Since v6.4.15.0 it is possible to also use the `ce_` shorthand prefix for your custom entities to prevent problems with length restrictions of names inside the DB.

xml

```shiki
<?xml version="1.0" encoding="utf-8" ?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/CustomEntity/Xml/entity-1.0.xsd">
    <entity name="ce_bundle">
        <fields>
            ...
        </fields>
    </entity>
</entities>
```

If you use the shorthand in the entity definition, you also need to use it if you use the repository or the API.

twig

```shiki
{% set blogs = services.repository.search('ce_blog', criteria) %}
```

bash

```shiki
POST /api/search/ce_blog
```

WARNING

Note that you can't rename existing custom entities as that would lead to the deletion of all existing data.

---

## Content

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/content/

# Content [​](#content)

You can assign content to specific categories, create layouts, and control the visibility of content based on various conditions. It provides a flexible and intuitive system for managing and presenting your store's content, helping you deliver a seamless and engaging customer experience.

---

## CMS

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/content/cms/

# CMS [​](#cms)

Shopware allows you to extend the content management capabilities of the platform by adding a custom CMS block from an app. By creating a custom app, you can define and integrate your own unique CMS blocks. These blocks can contain custom content, such as text, images, or HTML, and can be positioned within the CMS layout according to your requirements. Once the app is installed and activated, the custom CMS block becomes available within the Shopware administration panel, empowering you to create engaging and tailored content for your online store.

---

## Add custom CMS blocks

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/content/cms/add-custom-cms-blocks.html

# Add custom CMS blocks [​](#add-custom-cms-blocks)

INFO

This functionality is available starting with Shopware 6.4.4.0.

Alternatively, you can [add custom CMS blocks](./../../../plugins/content/cms/add-cms-block.html) using the plugin system, however these will not be available in Shopware cloud stores.

Didn't get in touch with Shopware's Shopping Experiences (CMS) yet? Check out the concept behind it first:

[Shopping Experiences (CMS)](../../../../../concepts/commerce/content/shopping-experiences-cms)

## Prerequisites [​](#prerequisites)

This guide is based on our [App Base Guide](./../../app-base-guide.html) and assumes you have already set up an app.

## Overview [​](#overview)

Adding custom CMS blocks from an app works a bit differently than [adding them from a plugin](./../../../plugins/content/cms/add-cms-block.html). Custom CMS blocks are added by providing a `cms.xml` in the `Resources/` directory of your app. The basic directory structure looks as follows:

text

```shiki
├── Resources
│   ├── app
│   │   └── storefront
│   │       └── src
│   │           └── scss
│   │               └── base.scss
│   ├── cms
│   │   └── blocks
│   │       └── swag-image-text-reversed
│   │           ├── preview.html
│   │           └── styles.css
│   ├── views
│   │   └── storefront
│   │       └── block
│   │           └── cms-block-swag-image-text-reversed-component.html.twig
│   └── cms.xml
└── manifest.xml
```

Each CMS block defined within your `cms.xml` must have a directory matching the block's name in `Resources/cms/blocks/`. In those directories you shape your blocks for the CMS module in the Administration by supplying a `preview.html` containing the template used for displaying a preview. Styling the preview in the sidebar and the component in the CMS editor is possible from the `styles.css`.

INFO

Due to technical limitations it's not possible to use templating engines (like Twig) or preprocessors (like Sass) for rendering and styling the preview.

The Storefront representations of your blocks reside in `Resources/views/storefront/block/`.

## Defining blocks [​](#defining-blocks)

As already mentioned above and similar to an app's `manifest.xml`, CMS blocks also require some definition done in the `cms.xml`. In this example we will define a custom CMS block that will extend the default block `image-text` and reverse its elements:

xml

```shiki
// <app root>/Resources/cms.xml
<?xml version="1.0" encoding="utf-8" ?>
<cms xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Cms/Schema/cms-1.0.xsd">
    <blocks>
        <block>
            <!-- A unique technical name for your block. We recommend to use a shorthand prefix for your company, e.g. "Swag" for shopware AG. -->
            <name>swag-image-text-reversed</name>

            <!-- The category your block is associated with. See the XSD for available categories. -->
            <category>text-image</category>

            <!-- Your block's label which will be shown in the CMS module in the Administration. -->
            <label>Two columns, text &amp; boxed image</label>
            <label lang="de-DE">Zwei Spalten, Text &amp; gerahmtes Bild</label>

            <!-- The slots that your block holds which again hold CMS elements. -->
            <slots>
                <!-- A slot requires a unique name and a type which refers to the CMS element it shows. Right now you can only use the CMS elements provided by Shopware but at a later point you will be able to add custom elements too. -->
                <slot name="left" type="text">
                    <!-- The slot requires some basic configuration. The following config-value elements highly depend on which element the slot holds. -->
                    <config>
                        <!-- The following config-value will be interpreted as 'verticalAlign: { source: "static", value: "top"}' in the JavaScript. -->
                        <config-value name="vertical-align" source="static" value="top"/>
                    </config>
                </slot>

                <slot name="right" type="image">
                    <config>
                        <config-value name="display-mode" source="static" value="auto"/>
                        <config-value name="vertical-align" source="static" value="top"/>
                    </config>
                </slot>
            </slots>

            <!-- Each block comes with a default configuration which is pre-filled and customizable when adding a block to a section in the CMS module in the Administration. -->
            <default-config>
                <margin-top>20px</margin-top>
                <margin-right>20px</margin-right>
                <margin-bottom>20px</margin-bottom>
                <margin-left>20px</margin-left>
                <!-- The sizing mode of your block. Allowed values are "boxed" or "full_width". -->
                <sizing-mode>boxed</sizing-mode>
            </default-config>
        </block>
    </blocks>
</cms>
```

Let's have a look at how to configure a CMS block from your app's `cms.xml`:

`<name>` : A **unique** technical name for your block.

`<category>` : Blocks are divided into categories. Available categories can be found in the [plugin guide](./../../../plugins/content/cms/add-cms-block.html#custom-block-in-the-administration).

`<label>` : The **translatable** label will be shown in the Administration.

`<default-config>` : Some default configuration for the block.

`<slots>` : Each block holds slots that configure which element they show.

The full CMS reference is available here:

[CMS Reference](../../../../../resources/references/app-reference/cms-reference)

### Block preview [​](#block-preview)

The preview template for `swag-image-text-reversed` looks like this:

html

```shiki
// <app root>/Resources/cms/blocks/swag-image-text-reversed/preview.html
<div class="sw-cms-preview-swag-image-text-reversed">
    <div>
        <h2>Lorem ipsum dolor</h2>
        <p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr.</p>
    </div>

    <!-- Alternatively you might e.g. also use a base64 encoded preview image instead of an external resource. -->
    <img src="https://example.com/preview.jpg" alt="Preview image">
</div>
```

INFO

For security reasons you can only use pure HTML in the preview template. The template will be sanitized from possibly malicious tags like `<script>` or attributes like `:src="assetFilter('/administration/static/img/cms/preview_mountain_small.jpg')"`.

The styling of the preview looks as follows:

css

```shiki
// <app root>/Resources/cms/blocks/swag-image-text-reversed/styles.css
/* 
 * Styling of your block preview in the CMS sidebar
 */
.sw-cms-preview-swag-image-text-reversed {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-column-gap: 20px;
    padding: 15px;
}

/*
 * Styling of your block in the CMS editor
 * Pattern: sw-cms-block-${block.name}-component
 */
.sw-cms-block-swag-image-text-reversed-component {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
    grid-gap: 40px;
}

/*
 * Each slot will have an additional class
 * Pattern: sw-cms-slot-${slot.name}
 */
.sw-cms-block-swag-image-text-reversed-component .sw-cms-slot-left {
    
}

/*
 * Each slot will have an additional class
 * Pattern: sw-cms-slot-${slot.name}
 */
.sw-cms-block-swag-image-text-reversed-component .sw-cms-slot-right {

}
```

The DOM structure of the block in the CMS editor will look like this:

html

```shiki
<div class="sw-cms-block-swag-image-text-reversed-component">
    <div class="sw-cms-slot sw-cms-slot-left"></div>
    <div class="sw-cms-slot sw-cms-slot-right"></div>
</div>
```

## Defining slots [​](#defining-slots)

Each slot has a **unique** `name` and a `type` that refers to which element it shows. All available elements can be found in [src/Administration/Resources/app/administration/src/module/sw-cms/elements](https://github.com/shopware/shopware/tree/trunk/src/Administration/Resources/app/administration/src/module/sw-cms/elements). At a later point you will also be able to define custom elements but for now you can use the elements shipped by Shopware.

The `config` of a slot is very dynamic as it highly depends on which `type` you have chosen. A good starting point to find out which elements require which configuration is each element's `index.js` in the corresponding directory in [src/Administration/Resources/app/administration/src/module/sw-cms/blocks](https://github.com/shopware/shopware/tree/trunk/src/Administration/Resources/app/administration/src/module/sw-cms/blocks).

## Registering blocks [​](#registering-blocks)

Unlike adding blocks from a plugin, blocks provided from an app will be automatically registered during runtime - so all you need to take care of is to properly define and configure them.

## Storefront representation [​](#storefront-representation)

Providing the Storefront representation of your blocks works very similarly as in the [plugin example](./../../../plugins/content/cms/add-cms-block.html#storefront-representation). In `Resources/views/storefront/block/` a Twig template matching the pattern `cms-block-${block.name}-component.html.twig` is expected.

So in this example, it's sufficient to simply extend the existing `image-text` element:

twig

```shiki
// <app root>/Resources/views/storefront/block/cms-block-swag-image-text-reversed-component.html.twig
{% sw_extends '@Storefront/storefront/block/cms-block-image-text.html.twig' %}
```

Styling of your blocks in the Storefront can then be done in `Resources/app/storefront/src/scss/base.scss`.

## Further reading [​](#further-reading)

You can further take a look at the [CMS references](./../../../../../resources/references/app-reference/cms-reference.html).

---

## Rule Builder

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/rule-builder/

# Rule Builder [​](#rule-builder)

Shopware allows you to enhance the capabilities of the rule builder by adding custom rules from an app. By creating a custom app and defining your own rules, you can incorporate specific conditions and actions based on your business requirements. This empowers you to create dynamic and personalized customer experiences, such as customized promotions, targeted discounts, or advanced product recommendations.

Starting with version 6.4.12.0, apps are able to [add custom rule conditions](./add-custom-rule-conditions.html) for use in the [Rule Builder](./../../../../concepts/framework/rule.html).

---

## Add custom rule conditions

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/rule-builder/add-custom-rule-conditions.html

# Add custom rule conditions [​](#add-custom-rule-conditions)

## Overview [​](#overview)

In this guide, you'll learn how to make your app introduce custom conditions for use in the [Rule Builder](./../../../../concepts/framework/rule/). Custom conditions can be defined with fields to be rendered in the Administration and with their own logic, using the same approach as [App Scripts](./../app-scripts/).

INFO

Note that app rule conditions were introduced in Shopware 6.4.12.0, and are not supported in previous versions.

## Prerequisites [​](#prerequisites)

If you're not familiar with the app system, please take a look at the concept first.

[Apps](../../../../concepts/extensions/apps-concept)

You should also be familiar with the general concept of the Rule Builder.

[Rule system](../../../../concepts/framework/rule-system/)

For the attached logic of your custom conditions, you'll use [twig files](https://twig.symfony.com/). Please refer to the App Scripts guide for a general introduction.

[App Scripts](../app-scripts/)

## Definition [​](#definition)

App Rule Conditions are defined in the `manifest.xml` file of your app:

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
    <rule-conditions>
        <rule-condition>
            <!-- The identifier of the rule condition must be unique should not change. Otherwise a separate rule condition is created and uses of the old one are lost. -->
            <identifier>my_custom_condition</identifier>
            <!-- Translatable, a name of your rule condition -->
            <name>Custom condition</name>
            <name lang="de-DE">Eigene Bedingung</name>
            <!-- A thematic group the condition should be assigned too, available groups are: general, customer, cart, item, promotion, misc -->
            <group>misc</group>
            <!-- The *.twig file that contains the corresponding script for the condition. It must be placed in the directory Resources/scripts/rule-conditions starting from your app's root directory -->
            <script>custom-condition.twig</script>
            <!-- Define the fields you want the user to fill out for use as data within your condition -->
            <constraints>
                <!-- the element type, defines the type of the field -->
                <!-- the elements available here are the same as for custom fields -->
                <single-select name="operator">
                    <placeholder>Choose an operator...</placeholder>
                    <placeholder lang="de-DE">Bitte Operatoren wählen</placeholder>
                    <options>
                        <option value="=">
                            <name>Is equal to</name>
                            <name lang="de-DE">Ist gleich</name>
                        </option>
                        <option value="!=">
                            <name>Is not equal to</name>
                            <name lang="de-DE">Ist nicht gleich</name>
                        </option>
                    </options>
                    <required>true</required>
                </single-select>
                <text name="firstName">
                    <placeholder>Enter first name</placeholder>
                    <placeholder lang="de-DE">Bitte Vornamen eingeben</placeholder>
                    <required>true</required>
                </text>
            </constraints>
        </rule-condition>
    </rule-conditions>
</manifest>
```

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

The following fields are required:

* `identifier`: A technical name for the condition that should be unique within the scope of the app. The name is being used to identify existing conditions when updating the app, so it should not be changed.
* `name`: A descriptive and translatable name for the condition. The name will be shown within the Rule Builder's selection of conditions in the Administration.
* `script`: The file name and extension of the file that contains the script for the condition. All scripts for rule conditions must be placed inside `Resources/scripts/rule-conditions` within the root directory of the app.

### Constraints [​](#constraints)

Constraints are optional and may be used to define fields, whose purpose is to provide data for use within the condition's script.

Constraints are a collection of [custom fields](./../custom-data/), which allows you to provide a variety of different fields for setting parameters within the administration. Fields may be marked as `required`. The `name` attribute of the field is also the variable the field's value will be exposed as within the condition's script. So it is advisable to use a variable-friendly name and to use unique names within the confines of a single condition.

The above example will add the condition shown below for selection in the Administration:

![App Rule Condition](/assets/app-rule-condition.C78HGlsh.png)

## Scripts [​](#scripts)

The corresponding scripts to the defined conditions within `manifest.xml` need to be placed at a specific directory of your app:

text

```shiki
└── DemoApp
    ├── Resources
    │   └── scripts                         // all scripts are stored in this folder
    │       ├── rule-conditions             // reserved for scripts of rule conditions
    │       │   └── custom-condition.twig   // the file name may be freely chosen but must be identical to the corresponding `script` element within `rule-conditions` of `manifest.xml`
    │       └── ...
    └── manifest.xml
```

Scripts for rule conditions are [twig files](https://twig.symfony.com/) that are executed in a sandboxed environment. They offer the same extended syntax and debugging options as [App Scripts](./../app-scripts/).

Within the script you will have access to the `scope` variable which is an instance of `RuleScope` as described in the [Rule Builder concept](./../../../../concepts/framework/rule.html). The scope instance provides you with the current `SalesChannelContext` and, given the right scope, the current cart. Further available variables depend on the existence of constraints within the definition of your conditions.

A script *must* return a boolean value, stating whether the condition is true or false. Anything but a boolean returned as value may lead to unexpected behavior.

### Compare helper [​](#compare-helper)

To keep condition scripts smaller we provide a `compare` helper function which can be used for the most common comparisons of two values.

The function takes three arguments:

text

```shiki
compare(operator, value, comparable)
```

The `operator` *must* be one of the following string values: `=`, `!=`, `>`, `>=`, `<`, `<=`, `empty`

If either one or both of `value` and `comparable` are an array, then only `=` and `!=` should be used as operator. It will then compare whether there is at least one occurrence of the value within the other array and return `true` if that is the case. As an example `value` might be an ID, `comparable` an array of IDs and you could use the function to match whether the ID is included in that array.

### Example [​](#example)

twig

```shiki
// Resources/scripts/rule-conditions/custom-condition.twig
{% if scope.salesChannelContext.customer is not defined %}
    {% return false %}
{% endif %}

{% return compare(operator, scope.salesChannelContext.customer.firstName, firstName) %}
```

In the example above, we first check whether we can retrieve the current customer from the instance of `RuleScope` and return `false` otherwise.

We then use the variables `operator` and `firstName`, provided by the constraints of the condition, to evaluate whether the first name in question matches the first name of the current customer. To do so, we make use of the `compare` helper function.

### Line item condition example [​](#line-item-condition-example)

html

```shiki
// manifest.xml
<!-- ... -->
<rule-condition>
    <identifier>line_item_condition</identifier>
    <name>Custom product multi select</name>
    <group>item</group>
    <script>line-item-condition.twig</script>
    <constraints>
        <single-select name="operator">
            <placeholder>Choose an operator...</placeholder>
            <options>
                <option value="=">
                    <name>Is equal to</name>
                </option>
                <option value="!=">
                    <name>Is not equal to</name>
                </option>
            </options>
            <required>true</required>
        </single-select>
        <multi-entity-select name="productIds">
            <placeholder>Choose products...</placeholder>
            <entity>product</entity>
            <required>true</required>
        </multi-entity-select>
    </constraints>
</rule-condition>
<!-- ... -->
```

twig

```shiki
// Resources/scripts/rule-conditions/line-item-condition.twig
{% if scope.lineItem is defined %}
    {% return compare(operator, lineItem.referenceId, productIds) %}
{% endif %}

{% if scope.cart is not defined %}
    {% return false %}
{% endif %}

{% for lineItem in scope.cart.lineItems.getFlat() %}
    {% if compare(operator, lineItem.referenceId, productIds) %}
        {% return true %}
    {% endif %}
{% endfor %}

{% return false %}
```

In this example we first check if the current scope is `LineItemScope` and refers to a specific line item. If so, we compare that specific line item. Otherwise we check if the scope has a cart and return false if it doesn't. We have a multi select for product selection in the Administration which provides an array of product IDs in the script. We iterate the current cart's line items to check if the product is included and return `true` if that is the case.

### Date condition example [​](#date-condition-example)

html

```shiki
// manifest.xml
<!-- ... -->
<rule-condition>
    <identifier>date_condition</identifier>
    <name>Custom date condition</name>
    <group>misc</group>
    <script>date-condition.twig</script>
</rule-condition>
<!-- ... -->
```

twig

```shiki
// Resources/scripts/rule-conditions/date-condition.twig
{% return compare('=', scope.getCurrentTime()|date_modify('first day of this month')|date_modify('second wednesday of this month')|date('Y-m-d'), scope.getCurrentTime()|date('Y-m-d')) %}
```

For this example, we don't have to define constraints. We retrieve the current date from the scope, calling `getCurrentTime`. We modify the date to set it to the first day of the month, then modify it again to set it to the second wednesday from that point in time. We then compare that date against the current date for a condition that matches only on the second wednesday of each month.

---

## Hosting

**Source:** https://developer.shopware.com/docs/guides/hosting/

# Hosting [​](#hosting)

Setting up an operating environment for Shopware can be hard, but it doesn't have to be if you follow some general guidelines in the subsequent sections.

---

