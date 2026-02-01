# Products Extensions Advanced Search

*Scraped from Shopware Developer Documentation*

---

## Advanced Search

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/

# Advanced Search [​](#advanced-search)

INFO

Advanced Search is available starting with Commercial 5.5.0

Shopware Advanced Search is a part of the Commercial plugin available along with the Evolve and Beyond plan.

Advanced search module is based on Elasticsearch. In addition to a high performance product search, it also offers you the possibilities to customize the search experience depending on your needs. So you could also search for manufacturers and categories. The simple Administration module allows quick and easy configuration of the search.

Before continuing, you should make sure you have a basic knowledge of [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/index.html) and the Shopware implementation of it.

---

## Installation

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/installation.html

# Installation [​](#installation)

This module requires the following:

* Advanced Search 2.0 is a licensed feature of the Commercial package. It is available for `Evolve` and `Beyond` plan.
* Opensearch server is up and running.
* `Shopware\Elasticsearch\Elasticsearch` bundle is enabled in `config/bundles.php`.
* On-prem environment configuration:

text

```shiki
OPENSEARCH_URL=http://localhost:9200
ES_MULTILINGUAL_INDEX=1
SHOPWARE_ES_ENABLED=1
SHOPWARE_ES_INDEXING_ENABLED=1
SHOPWARE_ES_INDEX_PREFIX=sw
```

* Commercial plugin version 5.5.0 onward is installed and activated.

---

## Define a custom Elasticsearch Definition

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-define-your-custom-Elasticsearch-definition.html

# Define a custom Elasticsearch Definition [​](#define-a-custom-elasticsearch-definition)

In the previous implementation, the Elasticsearch index was language-based, meaning each system's language would be indexed in a separate index. With the introduction of the multilingual index:

Each index will contain multiple language-based fields; refer to the [ADR](/docs/resources/references/adr/2023-04-11-new-language-inheritance-mechanism-for-opensearch.html) and adjust your custom Elasticsearch definition's configuration mapping to adapt to the new mapping structure.

For instance, to define your custom Elasticsearch definition (this definition will be used for later examples).

php

```shiki
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use Doctrine\DBAL\ArrayParameterType;
use Doctrine\DBAL\Connection;
use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Commercial\AdvancedSearch\Domain\Search\AbstractSearchLogic;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;

class YourCustomElasticsearchDefinition extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly EntityDefinition $definition,
        private readonly Connection $connection,
        private readonly AbstractSearchLogic $searchLogic
    ) {
    }

    /**
     * Define your ES definition's mapping
     */
    public function getMapping(Context $context): array
    {
        $languages = $this->connection->fetchAllKeyValue(
            'SELECT LOWER(HEX(language.`id`)) as id, locale.code
             FROM language
             INNER JOIN locale ON locale_id = locale.id'
        );

        $languageFields = [];

        foreach ($languages as $languageId => $code) {
            $parts = explode('-', $code);
            $locale = $parts[0];

            $languageFields[$languageId] = self::getTextFieldConfig();
            if (\array_key_exists($locale, $this->languageAnalyzerMapping)) {
                $fields = $languageFields[$languageId]['fields'];
                $fields['search']['analyzer'] = $this->languageAnalyzerMapping[$locale];
                $languageFields[$languageId]['fields'] = $fields;
            }
        }

        $properties = [
            'name' => [
                'properties' => $languageFields,
            ],
            'description' => [
                'properties' => $languageFields,
            ],
        ];

        return [
            '_source' => ['includes' => ['id']],
            'properties' => $properties,
        ];
    }

    /**
     * Build a bool query when searching your custom ES definition, by default we use the Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic  
     */
    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->searchLogic->build($this->definition, $criteria, $context);
    }

    /**
    * fetch data from storage to push to elasticsearch cluster when indexing data 
    */
    public function fetch(array $ids, Context $context): array
    {
        $data = $this->fetchData($ids, $context);

        $documents = [];

        foreach ($data as $id => $item) {
            $translations = (array) json_decode($item['translation'] ?? '[]', true, 512, \JSON_THROW_ON_ERROR);

            $document = [
                'id' => $id,
                'name' => $this->mapTranslatedField('name', true, ...$translations),
                'description' => $this->mapTranslatedField('description', true, ...$translations),
            ];

            $documents[$id] = $document;
        }

        return $documents;
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->definition;
    }

    private function fetchData(array $ids, Context $context): array
    {
        $sql = <<<'SQL'
SELECT
    LOWER(HEX(custom_entity.id)) AS id,
    CONCAT(
        '[',
            GROUP_CONCAT(DISTINCT
                JSON_OBJECT(
                    'description', your_custom_entity_translation.description,
                    'name', your_custom_entity_translation.name,
                    'languageId', LOWER(HEX(your_custom_entity_translation.language_id))
                )
            ),
        ']'
    ) as translation
FROM your_custom_entity custom_entity
    LEFT JOIN your_custom_entity_translation ON your_custom_entity_translation.your_custom_entity_id = custom_entity.id
WHERE custom_entity.id IN (:ids)
GROUP BY custom_entity.id
SQL;

        $result = $this->connection->fetchAllAssociativeIndexed(
            $sql,
            [
                'ids' => $ids,
            ],
            [
                'ids' => ArrayParameterType::STRING,
            ]
        );

        return $result;    }
}
```

And register it in the container with tag `shopware.es.definition` and `advanced_search.supported_definition`

xml

```shiki
# YourPluginNameSpace should be changed to your respectively ElasticsearchDefinition and Definition classes
<service id="YourPluginNameSpace\YourCustomElasticsearchDefinition">
    <argument type="service" id="YourPluginNameSpace\YourCustomDefinition"/>
    <argument type="service" id="Doctrine\DBAL\Connection"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic"/>

    <tag name="shopware.es.definition"/>
    <tag name="advanced_search.supported_definition"/>
</service>
```

---

## Add more fields to product search

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-add-more-fields-to-product-search.html

# Add more Fields to Product Search [​](#add-more-fields-to-product-search)

You can add more searchable fields into your product or any Elasticsearch definition.

In this example, we create a field called `productNumberPrefix` to make it searchable. This requires 3 steps:

**1. Decorate the ElasticsearchDefinition**

xml

```shiki
<service id="YourPluginNameSpace\ElasticsearchProductDefinitionDecorator" decorates="Shopware\Elasticsearch\Product\ElasticsearchProductDefinition">
    <argument type="service" id=".inner"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic"/>
</service>
```

php

```shiki
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;

class ElasticsearchProductDefinitionDecorator extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly AbstractElasticsearchDefinition $decorated
    ) {
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->decorated->getEntityDefinition();
    }

    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->decorated->buildTermQuery($context, $criteria);
    }

    public function getMapping(Context $context): array
    {
        $mappings = $this->decorated->getMapping($context);

        $additionalMappings = [
            // define your new field's type
            'prefixProductNumber' => self::KEYWORD_FIELD,
            // other additional fields
        ];

        $mappings['properties'] = array_merge($mappings['properties'], $additionalMappings);

        return $mappings;
    }

    public function fetch(array $ids, Context $context): array
    {
        $data = $this->decorated->fetch($ids, $context);

        $documents = [];

        foreach ($data as $id => $document) {
            $document = array_merge($document, [
                // get first 5 characters from productNumber to index it
                'prefixProductNumber' => substr($document['productNumber'], 0, 5),
            ]);

            $documents[$id] = $document;
        }

        return $documents;
    }
}
```

**2. Run the commands:**

We need to update these data mapping to the Opensearch's server to make the change effective:

bash

```shiki
// Update the Elasticsearch indices mapping, introduce since 6.5.4.0
bin/console es:mapping:update

// Assume the new field data are already set in products, otherwise you don't need to reindex
bin/console es:index --no-queue
```

**3. Insert new fields to advanced\_search\_config\_field of the search entity**

So now the data is mapped and indexed, we need to make it searchable by adding the new field into the search config. Create a new migration and make sure it is run by reinstalling or updating the plugin:

bash

```shiki
bin/console database:create-migration --name AddNewPrefixProductNumberFieldIntoProductAdvancedSearch --plugin YourPlugin
```

php

```shiki
<?php declare(strict_types=1);

namespace YourPluginNameSpace\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\Aggregate\AdvancedSearchConfigFieldDefinition;
use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1692954529AddNewPrefixProductNumberFieldIntoProductAdvancedSearch extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1692954529;
    }

    public function update(Connection $connection): void
    {
        $configSalesChannelIds = $connection->fetchFirstColumn('SELECT id FROM advanced_search_config');

        $createdAt = (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT);

        foreach ($configSalesChannelIds as $configSalesChannelId) {
            $connection->insert(AdvancedSearchConfigFieldDefinition::ENTITY_NAME, [
                'id' => Uuid::randomBytes(),
                'field' => 'prefixProductNumber',
                'config_id' => $configSalesChannelId,
                'entity' => ProductDefinition::ENTITY_NAME,
                'tokenize' => 1,
                'searchable' => 1,
                'ranking' => 500,
                'created_at' => $createdAt,
            ]);
        }
    }
}
```

---

## Configure Searchable Fields

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-configure-searchable-fields.html

# Configure Searchable Fields [​](#configure-searchable-fields)

Search entities and their searchable fields are stored in `advanced_search_config` and `advanced_search_config_field` table respectively.

These configured fields help to build the search query when a search/suggest request is sent from the client.

This approach is very similar to how `product_search_config` and `product_search_config_field` work in the platform. The main difference is you can configure the configuration by sales channel instead of by language (each sales channel now has its own search config).

@Refer:

`\Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\AdvancedSearchConfigDefinition``\Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\Aggregate\AdvancedSearchConfigFieldDefinition`

To have the custom search configuration, you need to add a migration to insert the configuration into the database. In the below example, we add default search configuration for product, manufacturer, and category entities

@Refer: `\Shopware\Commercial\Migration\Migration1680751315SWAGAdvancedSearch_AddAdvancedSearchConfigurationDefaults`

And you might want to add the configuration for newly created saleschannel as well: @Refer: `\Shopware\Commercial\AdvancedSearch\Subscriber\SalesChannelCreatedSubscriber`

---

## Language analyzers

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-add-modify-language-analyzers-stopwords-stemmer.html

# Add / Modify language analyzers, stopwords, stemmer [​](#add-modify-language-analyzers-stopwords-stemmer)

With the introduction of the multi-language index, support for built-in [Elasticsearch language analyzers](https://www.elastic.co/docs/reference/text-analysis/analysis-lang-analyzer) was also introduced.

This would help language-based fields have different analyzers for each language's specific features, like stopwords, stemmers, and normalization, out of the box.

You can also add more or customize the language analyzer by overriding the analyzer parameter in `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/config/packages/advanced_search.yaml`

For example:

yaml

```shiki
advanced_search:
    analysis:
        analyzer:
            sw_your_custom_language_analyzer:
                type: custom
                tokenizer: standard
                filter: ['lowercase', 'my_stopwords_filter', 'my_stemmer_filter']
    filter:
        my_stopwords_filter:
            type: 'stop'
            stopwords: ['foo', 'bar']
        my_stemmer_filter:
            type: 'stemmer'
            language: 'english'
    # It's important to map your analyzer with the language iso code
    language_analyzer_mapping:
        custom_iso: sw_your_custom_language_analyzer
```

---

## Cross search

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/Cross-search.html

# Cross Search [​](#cross-search)

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\CrossSearch\CrossSearchLogic`

At times, the need arises to search for categories using product names. To enable Elasticsearch with this capability, it becomes essential to index associated data across different indexes. However, it's important to note that this operation leads to a notable increase in the overall size of the index.

To solve this problem, an **experimental** feature called Cross Search has been introduced. You can configure which associations could be cross-searched:

yaml

```shiki
# config/packages/advanced_search.yaml
advanced_search:
    # When searching for `manufacturer.product.name`, if `product_manufacturer.product` cross_search is enabled, the `product` index will be used for search field `name`
    cross_search:
        product.product_manufacturer: false
        product.category: false
        category.product: true
        product_manufacturer.product: true
```

By default, only `category - product` and `product_manufacturer - product` associations are enabled, but you can change this behavior in the parameter. This way, we don't need to index product's data inside category and manufacturer indexes.

You can add your own Cross Search mapping to the parameter. If the mapping is not defined or is false, you need to index the associated data accordingly.

Be aware that this comes with a downside: when Cross Search is enabled, we need an extra aggregated Elasticsearch query to accomplish the desired search behavior.

---

## Extending search template

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-extend-the-search-and-suggest-template.html

# Extend Search Template [​](#extend-search-template)

To show the results in the search overview, you have to extend the `search/index.html.twig` and then apply the results in your desired styling. You can take a look at an example of `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/views/storefront/page/search/index.html.twig`.

The manufacturers and categories or your custom search result could be realized in the template as:

twig

```shiki
{% set searchResult = page.listing.extensions.multiSearchResult %}
{% set products = page.listing %}
{% set manufacturers = searchResult.getResult('product_manufacturer') %}
{% set categories = searchResult.getResult('category') %}
{% set customEntities = searchResult.getResult('custom_entity') %}
```

## How to extend the suggest template [​](#how-to-extend-the-suggest-template)

To show the results in the suggest dropdown, you have to extend `Storefront/storefront/layout/header/search-suggest.html.twig` like the Advanced Search does in `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/views/storefront/layout/header/search-suggest.html.twig`.

The completion, manufacturers and categories or your custom search result could be realized in the template as:

twig

```shiki
{% set suggestResult = page.searchResult.extensions.multiSuggestResult %}
{% set products = page.searchResult %}
{% set completions = page.searchResult.extensions.completionResult %}
{% set manufacturers = suggestResult.getResult('product_manufacturer') %}
{% set categories = suggestResult.getResult('category') %}
{% set customEntities = suggestResult.getResult('custom_entity') %}
```

---

## Modify search logic

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-modify-search-logic.html

# Modify Search Logic [​](#modify-search-logic)

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic`

This class is the central place to build the Elasticsearch query:

* Load all searchable fields of the wanted search entity and the current context's sales channel.
* The search term will be tokenized and filtered into a list of "token". For e.g., `The 2 QUICK Brown-Foxes jumped over the lazy dog's bone` will be tokenized to `[ The, 2, QUICK, Brown, Foxes, jumped, over, the, lazy, dog's, bone ]`.
* Each search token will form a bool query to check whether the token matches any of the loaded searchable fields. This step is when `\Shopware\Commercial\AdvancedSearch\Domain\Search\TokenQueryBuilder::build` takes place, it will help to build a `token query`.
* These built queries will be combined into a single query by `AND` or `OR` operators, depending on the search behavior configured at the first step.
* This query will be used by `\Shopware\Elasticsearch\Framework\DataAbstractionLayer\ElasticsearchEntitySearcher` to search.

To modify the search logic, you can decorate the search logic class and add your own logic into it:

xml

```shiki
<service id="YourPluginNameSpace\Domain\Search\SearchLogicDecorator" decorates="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic">
    <argument type="service" id=".inner"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Configuration\ConfigurationLoader"/>
</service>
```

php

```shiki
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Commercial\AdvancedSearch\Domain\Configuration\ConfigurationLoader;
use Shopware\Commercial\AdvancedSearch\Domain\Search\AbstractSearchLogic;
use Shopware\Core\Framework\Api\Context\SalesChannelApiSource;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class SearchLogicDecorator extends AbstractSearchLogic
{
    public function __construct(
        private readonly AbstractSearchLogic $decorated,
        private readonly ConfigurationLoader $configurationLoader
    ) {
    }

    public function build(EntityDefinition $definition, Criteria $criteria, Context $context): BoolQuery
    {
        if (!$context->getSource() instanceof SalesChannelApiSource) {
            return new BoolQuery();
        }

        $salesChannelId = $context->getSource()->getSalesChannelId();
        // you probably want get the search configs of the context's sales channel but it's optional
        $searchConfig = $this->configurationLoader->load($salesChannelId);

        // you probably want to add extra logic into existing logic but it's optional
        $bool = $this->getDecorated()->build($definition, $criteria, $context);

        // Add your own logic
        return $bool;
    }

    public function getDecorated(): AbstractSearchLogic
    {
        return $this->decorated;
    }
}
```

---

## Search and suggest routes

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/Search-and-suggest-routes.html

# Search and Suggest Routes [​](#search-and-suggest-routes)

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Search\ProductSearchRouteDecorator`

`ProductSearchRoute` is decorated, so when searching for products from the Storefront, a `multiSearchResult` extension is added to the search product listing result. This extension includes all the search results for each Elasticsearch definition with the tag `advanced_search.supported_definition` with the given search term.

The same approach applies to `ProductSuggestRoute`. The only difference is that we added the completion search result as another extension `completionResult` to the search product listing result.

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Suggest\ProductSuggestRouteDecorator`

You can also subscribe to the event `\Shopware\Commercial\AdvancedSearch\Event\MultiContentSearchCriteriaEvent` or `\Shopware\Commercial\AdvancedSearch\Event\MultiContentSuggestCriteriaEvent` to adjust the search criteria.

This decoration approach comes with the benefit that the caching mechanism already works for the decorated search routes.

---

## Completion

**Source:** https://developer.shopware.com/docs/products/extensions/advanced-search/How-to-modify-completion.html

# Add / Modify Completion [​](#add-modify-completion)

The Advanced Search does not use the default Elasticsearch completion because it only supports a fixed order and the storage size is high. As an alternative, Advanced Search uses aggregations to find the most important word combinations for your search input.

## Adding completion to your definition mapping [​](#adding-completion-to-your-definition-mapping)

To index our own completion keywords, we need to inject `Shopware\Commercial\AdvancedSearch\Domain\Completion\CompletionDefinitionEnrichment` into your ES definition and call enrich methods in `getMapping` and `fetch` as following example:

Example:

*The definition is from the [previous example](./How-to-define-your-custom-Elasticsearch-definition.html):*

php

```shiki
<?php declare(strict_types=1);

class YourCustomElasticsearchDefinition extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly EntityDefinition $definition,
        private readonly Connection $connection,
        private readonly AbstractSearchLogic $searchLogic,
        private readonly CompletionDefinitionEnrichment $completionDefinitionEnrichment,
        private readonly array $languageAnalyzerMapping
    ) {
    }

    public function getMapping(Context $context): array
    {
        // ...
        
        return [
            '_source' => ['includes' => ['id']],
            // to add the mapping of completion field in your definition
            'properties' => array_merge($properties, $this->completionDefinitionEnrichment->enrichMapping()),
        ];
    }

    public function fetch(array $ids, Context $context): array
    {
        // ...

        // to add the completion keywords to the existing data
        return $this->completionDefinitionEnrichment->enrichData($this->getEntityDefinition(), $documents);
    }
}
```

## Add/modify completion keywords [​](#add-modify-completion-keywords)

By default, each of Shopware's ES definitions has a set of `string` fields to be considered as completion keywords. This configuration is realized via the parameter `%advanced_search.completion%`, if the configured fields for your definition are not set, all StringFields of the definition will be used as completion keywords.

For example, you can add or modify this configuration in `config/packages/advanced_search.yaml`:

yaml

```shiki
advanced_search:
    completion:
        your_custom_entity:
            - email
            - company
```

If you want to have more control over the completion, such as using static texts from files or parsing a field from another data source as completion keywords, you might want to decorate the service `\Shopware\Commercial\AdvancedSearch\Domain\Completion\CompletionDefinitionEnrichment::enrichData` instead.

---

