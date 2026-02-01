# Resources References Core Reference

*Scraped from Shopware Developer Documentation*

---

## Core Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/

# Core Reference [​](#core-reference)

The Core reference documents essential components like the DAL, administration panel, flags, filters, Flow Builder, and Rules for efficient platform usage. It details about the classes, methods, commands, events, etc, for your reference. This helps you understand how to use these features to enhance the functionality.

---

## DAL Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/

# DAL Reference [​](#dal-reference)

The DAL reference documents fields, flags, filters, and aggregations for effective data management and querying within the platform.

---

## Fields Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/fields-reference/

# Fields Reference [​](#fields-reference)

| Name | Description | Extends | StorageAware |
| --- | --- | --- | --- |
| AssociationField | Stores a association value | Field |  |
| AutoIncrementField | Stores an integer value | IntField |  |
| BlobField | Stores a blob value | Field | x |
| BoolField | Stores a bool value | Field | x |
| BreadcrumbField | Stores a JSON value | JsonField |  |
| CalculatedPriceField | Stores a JSON value | JsonField |  |
| CartPriceField | Stores a JSON value | JsonField |  |
| CashRoundingConfigField | Stores a JSON value | JsonField |  |
| ChildCountField | Stores an integer value | IntField |  |
| ChildrenAssociationField | Stores a association value | OneToManyAssociationField |  |
| ConfigJsonField | Stores a JSON value | JsonField |  |
| CreatedAtField | Stores a DateTime value | DateTimeField |  |
| CreatedByField | Stores a foreign key value | FkField |  |
| CronIntervalField | Stores a croninterval value | Field | x |
| DateField | Stores a date value | Field | x |
| DateIntervalField | Stores a dateinterval value | Field | x |
| DateTimeField | Stores a datetime value | Field | x |
| EmailField | Stores a string value | StringField |  |
| [EnumField](./enum-field.html) | Stores a enum value | Field | x |
| Field | Stores a value | Struct |  |
| FkField | Stores a fk value | Field | x |
| FloatField | Stores a float value | Field | x |
| IdField | Stores a id value | Field | x |
| IntField | Stores a int value | Field | x |
| JsonField | Stores a json value | Field | x |
| ListField | Stores a JSON value | JsonField |  |
| LockedField | Stores a boolean value | BoolField |  |
| LongTextField | Stores a longtext value | Field | x |
| ManyToManyAssociationField | Stores a association value | AssociationField |  |
| ManyToManyIdField | Stores a manytomanyid value | ListField |  |
| ManyToOneAssociationField | Stores a association value | AssociationField |  |
| ObjectField | Stores a JSON value | JsonField |  |
| OneToManyAssociationField | Stores a association value | AssociationField |  |
| OneToOneAssociationField | Stores a association value | AssociationField |  |
| ParentAssociationField | Stores a association value | ManyToOneAssociationField |  |
| ParentFkField | Stores a foreign key value | FkField |  |
| PasswordField | Stores a password value | Field | x |
| PriceDefinitionField | Stores a JSON value | JsonField |  |
| PriceField | Stores a JSON value | JsonField |  |
| ReferenceVersionField | Stores a foreign key value | FkField |  |
| RemoteAddressField | Stores a remoteaddress value | Field | x |
| SerializedField | Stores a serialized value | Field | x |
| StateMachineStateField | Stores a foreign key value | FkField |  |
| StringField | Stores a string value | Field | x |
| TaxFreeConfigField | Stores a JSON value | JsonField |  |
| TimeZoneField | Stores a string value | StringField |  |
| TranslatedField | Stores a translated value | Field |  |
| TranslationsAssociationField | Stores a association value | OneToManyAssociationField |  |
| TreeBreadcrumbField | Stores a JSON value | JsonField |  |
| TreeLevelField | Stores an integer value | IntField |  |
| TreePathField | Stores a treepath value | LongTextField |  |
| UpdatedAtField | Stores a DateTime value | DateTimeField |  |
| UpdatedByField | Stores a foreign key value | FkField |  |
| VariantListingConfigField | Stores a JSON value | JsonField |  |
| VersionDataPayloadField | Stores a JSON value | JsonField |  |
| VersionField | Stores a foreign key value | FkField |  |

---

## EnumField reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/fields-reference/enum-field.html

# EnumField reference [​](#enumfield-reference)

## Usage [​](#usage)

The `EnumField` can be used to restrict `string` or `int` values to a fixed set.

Define a `\BackedEnum` class, use them in an Entity and restrict the values in your RDBMS.

It's not advisable to use `ENUM` types for integer values, as most RDBMS only support string values and use integers internally. Using a regular `INT` column is recommended in this case. The `BackedEnum` will restrict the possible values, unless the database is modified manually.

## Examples [​](#examples)

### Example 1: Creating an input field from an enum [​](#example-1-creating-an-input-field-from-an-enum)

twig

```shiki
<select name="payment_method">
    {% for method in PaymentMethod::cases() %}
        <option value="{{ method.value }}">{{ method.name }}</option>
    {% endfor %}
</select>
```

### Example 2: Setting an Entity value [​](#example-2-setting-an-entity-value)

php

```shiki
<?php

$batchOrder = new BatchOrderEntity();
$batchOrder->setPaymentMethod(PaymentMethod::PAYPAL);
```

### Example 3: Check if a value is valid [​](#example-3-check-if-a-value-is-valid)

php

```shiki
<?php

$validPaymentMethod = PaymentMethod::tryFrom($userProvidedInput);

// Either check for null
if (is_null($validPaymentMethod)) {
    // The input was not a valid payment method
}

// Or check for the class
if($validPaymentMethod instanceof PaymentMethod) {
    // The input was a valid payment method
}
```

---

## Flags Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/flags-reference.html

# Flags Reference [​](#flags-reference)

| Classname | Description |
| --- | --- |
| AllowEmptyString | Flag a text column that an empty string should not be considered as null |
| AllowHtml | In case a column is allowed to contain HTML-escaped data. Beware of injection possibilities |
| ApiAware | Makes a field available in the Store or Admin API. If no parameter is passed for the flag, the field will be exposed in the both Store and Admin API. By default, all fields are enabled for the Admin API, as the flag is added in the base Field class. However, the scope can be restricted to `AdminApiSource` and `SalesChannelApiSource`. |
| CascadeDelete | In case the referenced association data will be deleted, the related data will be deleted too |
| Computed | The value is computed by indexer or external systems and cannot be written using the DAL. |
| Deprecated | This flag is used to mark the field that has been deprecated and will be removed with the next major version. |
| Extension | Defines that the data of this field is stored in an Entity::$extension and are not part of the struct itself. |
| Immutable | By setting the "Immutable" flag, it indicates that the field is write-once and then read-only |
| Inherited | Defines that the data of this field can be inherited by the parent record |
| PrimaryKey | The PrimaryKey flag defines the field as part of the entity's primary key. Usually, this should be the ID field. |
| Required | Fields marked as "Required" must be specified during the create request of an entity. This configuration is only taken into account during the write process. |
| RestrictDelete | Associated data with this flag, restricts the delete of the entity in case that a record with the primary key exists. |
| ReverseInherited | Flags "ReverseInherited" |
| Runtime | Defines that the data of the field will be loaded at runtime by an event subscriber or other class. Used in entity extensions for plugins or not directly fetchable associations. |
| SearchRanking | Defines the weight for a search query on the entity for this field |
| SetNullOnDelete | In case the referenced association data will be deleted, the related data will be set to null and an Written event will be thrown |
| Since | The "Since" flag defines since which Shopware version the field is available. |
| WriteProtected | By setting the "WriteProtected" flag, write access via API can be restricted. This flag is mostly used to protect indexed data from direct writing via API. |

---

## Filters Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/filters-reference.html

# Filters Reference [​](#filters-reference)

| Name | Notes |
| --- | --- |
| equals | Exact match for the given value |
| equalsAny | At least one exact match for a value of the given list |
| contains | Before and after wildcard search for the given value |
| range | For range compatible fields like numbers or dates |
| not | Allows to negate a filter |
| multi | Allows to combine different filters |
| prefix | Before wildcard search for the given value |
| suffix | After wildcard search for the given value |

## Equals [​](#equals)

The `Equals` filter allows you to check fields for an exact value. The following SQL statement is executed in the background: `WHERE stock = 10`.

## EqualsAny [​](#equalsany)

The `EqualsAny` filter allows you to filter a field where at least one of the defined values matches exactly. The following SQL statement is executed in the background: `WHERE productNumber IN ('3fed029475fa4d4585f3a119886e0eb1', '77d26d011d914c3aa2c197c81241a45b')`.

## Contains [​](#contains)

The `Contains` Filter allows you to filter a field to an approximate value, where the passed value must be contained as a full value. The following SQL statement is executed in the background: `WHERE name LIKE '%Lightweight%'`.

## Range [​](#range)

The `Range` filter allows you to filter a field to a value space. This can work with date or numerical values. Within the `parameter` property the following values are possible:

* `gte` => Greater than equals
* `lte` => Less than equals
* `gt` => Greater than
* `lt` => Less than

The following SQL statement is executed in the background: `WHERE stock >= 20 AND stock <= 30`.

## Not [​](#not)

The `Not` Filter is a container which allows to negate any kind of filter. The `operator` allows you to define the combination of queries within the NOT filter (`OR` and `AND`). The following SQL statement is executed in the background: `WHERE !(stock = 1 OR availableStock = 1) AND active = 1`:

## Multi [​](#multi)

The `Multi` Filter is a container, which allows to set logical links between filters. The `operator` allows you to define the links between the queries within the `Multi` filter (`OR` and `AND`). The following SQL statement is executed in the background: `WHERE (stock = 1 OR availableStock = 1) AND active = 1`.

## Prefix [​](#prefix)

The `Prefix` Filter allows you to filter a field to an approximate value, where the passed value must be the start of a full value. The following SQL statement is executed in the background: `WHERE name LIKE 'Lightweight%'`.

## Suffix [​](#suffix)

The `Suffix` Filter allows you to filter a field to an approximate value, where the passed value must be the end of a full value. The following SQL statement is executed in the background: `WHERE name LIKE '%Lightweight'`.

In general, the storage systems are **case-insensitive**, meaning that when filtering values to search for a string, the casing of the filter values doesn't affect their handling.

---

## Aggregations Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/dal-reference/aggregations-reference.html

# Aggregations Reference [​](#aggregations-reference)

Aggregations allow you to determine further information about the overall result in addition to the actual search results. These include totals, unique values, or the average of a field.

The DAL knows two types of aggregations:

* `metric` aggregation - This type of aggregation applies a mathematical formula to a field. A metric aggregation always has a calculated result. These are aggregations to calculate sums or maximum values.
* `bucket` aggregation - With this type of aggregation, a list of keys is determined. Further aggregations can then be determined for each key.

| Name | Type | Description |
| --- | --- | --- |
| avg | metric | Average of all numeric values for the specified field |
| count | metric | Number of records for the specified field |
| max | metric | Maximum value for the specified field |
| min | metric | Minimal value for the specified field |
| stats | metric | Stats overall numeric values for the specified field |
| sum | metric | Sum of all numeric values for the specified field |
| entity | bucket | Groups the result for each value of the provided field and fetches the entities for this field |
| filter | bucket | Allows to filter the aggregation result |
| terms | bucket | Groups the result for each value of the provided field and fetches the count of affected documents |
| histogram | bucket | Groups the result for each value of the provided field and fetches the count of affected documents. Although allows to provide date interval (day, month, ...) |
| range | bucket | Groups the result for each defined set of ranges into each bucket - bucket of numerical data and a count of items/documents for each bucket |

## Avg aggregation [​](#avg-aggregation)

The `Avg` aggregation makes it possible to calculate the average value for a field. The following SQL statement is executed in the background: `AVG(price)`.

## Count aggregation [​](#count-aggregation)

The `count` aggregation makes it possible to determine the number of entries for a field that are filled with a value. The following SQL statement is executed in the background: `COUNT(DISTINCT(manufacturerId))`.

## Max aggregation [​](#max-aggregation)

The `max` aggregation allows you to determine the maximum value of a field. The following SQL statement is executed in the background: `MAX(price)`.

## Min aggregation [​](#min-aggregation)

The `min` aggregation makes it possible to determine the minimum value of a field. The following SQL statement is executed in the background: `MIN(price)`.

## Sum aggregation [​](#sum-aggregation)

The `sum` aggregation makes it possible to determine the total of a field. The following SQL statement is executed in the background: `SUM(price)`.

## Stats aggregation [​](#stats-aggregation)

The `stats` aggregation makes it possible to calculate several values at once for a field. This includes the previous `max`, `min`, `avg` and `sum` aggregation. The following SQL statement is executed in the background: `SELECT MAX(price), MIN(price), AVG(price), SUM(price)`.

## Terms aggregation [​](#terms-aggregation)

The `terms` aggregation belongs to the bucket aggregations. This allows you to determine the values of a field. The result contains each value once and how often this value occurs in the result. The `terms` aggregation also supports the following parameters:

* `limit` - Defines a maximum number of entries to be returned (default: zero)
* `sort` - Defines the order of the entries. By default, the following is not sorted
* `aggregation` - Enables you to calculate further aggregations for each key

The following SQL statement is executed in the background: `SELECT DISTINCT(manufacturerId) as key, COUNT(manufacturerId) as count`.

## Filter aggregation [​](#filter-aggregation)

The `filter` aggregation belongs to the bucket aggregations. Unlike all other aggregations, this aggregation does not determine any result. It can't be used alone. It is only used to further restrict the result of an aggregation in a criterion. Filters defined inside the `filter` property of this aggregation type are only used when calculating this aggregation. The filters have no effect on other aggregations or on the result of the search.

## Entity aggregation [​](#entity-aggregation)

The `entity` aggregation is similar to the `terms` aggregation. It belongs to the bucket aggregations. As with `terms` aggregation, all unique values are determined for a field. The aggregation then uses the determined keys to load the defined entity. The keys are used here as ids.

## Histogram aggregation [​](#histogram-aggregation)

The histogram aggregation is used as soon as the data to be determined refers to a date field. With the histogram aggregation, one of the following date intervals can be given: `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year`, `day`. This interval groups the result and calculates the corresponding count of hits.

## Range aggregations [​](#range-aggregations)

Allows to aggregate data on a predefined range of values for more flexibility in the DAL - for example, it provides faceted filters on a predefined range.

Bound are computed in SQL as in the Elasticsearch native range aggregation:

* `from` will be compared with greater than or equal to
* `to` will be compared with lower than

## Nesting aggregations [​](#nesting-aggregations)

A metric aggregation calculates the value for a specific field. This can be a total or, for example, a minimum or maximum value of the field. Bucket aggregations are different. This determines how often a value occurs in a search result and returns it together with the count. The special thing about bucket aggregation is that it can contain further aggregations. This allows the API to perform complex queries like, for example:

* Calculate the number of manufacturers per category that have a price over 500 Euro. \*

---

## Composer Commands Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/composer-commands-reference.html

# Composer Commands Reference [​](#composer-commands-reference)

INFO

These commands are only available inside `shopware/shopware` GitHub repository, so when you contribute to Shopware. For regular projects, use `./bin/*.sh` scripts.

These composer commands can be executed using composer with your Shopware project.

bash

```shiki
$ composer [command] [parameters]
```

## Commands [​](#commands)

### Setup & build [​](#setup-build)

| Command | Description |
| --- | --- |
| `setup` | Resets and re-installs this Shopware instance - Database will be purged! |
| `build:js` | Builds Administration & Storefront - Combination of `build:js:admin` & `build:js:storefront` |
| `build:js:admin` | Builds the Administration - Includes `bundle:dump`, `feature:dump`, `admin:generate-entity-schema-types` and `assets:install` |
| `build:js:component-library` | Builds the component library |
| `watch:admin` | Build administration with hot module reloading |
| `build:js:storefront` | Builds the Storefront's JavaScript - Includes `bundle:dump`, `feature:dump` and `theme:compile` |
| `check:license` | Check third-party dependency licenses for composer dependencies |
| `reset` | Resets this Shopware instance, without composer and npm install. (Faster reset if no dependencies changed) |

### Administration [​](#administration)

| Command | Description |
| --- | --- |
| `admin:create:test` | Generate a test boilerplate |
| `admin:generate-entity-schema-types` | Convert entity schemas to data types |
| `admin:unit` | Launches the jest unit test-suite for the Admin |
| `admin:unit:watch` | Launches the interactive jest unit test-suite watcher for the Admin |
| `admin:unit:prepare-vue3` | Prepares the jest unit test-suite for the Admin with Vue3 |
| `admin:unit:vue3` | Launches the jest unit test-suite for the Admin with Vue3 |
| `admin:unit:watch:vue3` | Launches the interactive jest unit test-suite watcher for the Admin with Vue3 |
| `npm:admin:check-license` | Check third-party dependency licenses for administration |
| `watch:admin` | Build administration with hot module reloading |

### Storefront [​](#storefront)

| Command | Description |
| --- | --- |
| `build:js:storefront` | Builds the Storefront's JavaScript - Includes `bundle:dump`, `feature:dump` and `theme:compile` |
| `npm:storefront:check-license` | Check third-party dependency licenses for storefront |
| `watch:storefront` | Build storefront with hot module reloading |

### Testsuite & Development [​](#testsuite-development)

| Command | Description |
| --- | --- |
| `bc-check` | Checks for backwards compatibility breaks in the current branch |
| `e2e:setup` | Installs a clean shopware instance for E2E environment and launches `e2e:prepare` |
| `e2e:open` | Launches the Cypress E2E test-suite UI |
| `e2e:prepare` | Installs the Admin Extension SDK test plugin with fixtures and dumps the database |
| `ecs` | Checks all files regarding the Easy Coding Standard |
| `ecs-fix` | Checks all files regarding the Easy Coding Standard and fixes them if possible |
| `eslint` | Codestyle checks all (Administration/Storefront/E2E) JS/TS files |
| `eslint:admin` | Codestyle checks Administration JS/TS files |
| `eslint:admin:fix` | Codestyle checks Administration JS/TS files and fixes them if possible |
| `eslint:e2e` | Codestyle checks all E2E JS/TS files |
| `eslint:e2e:fix` | Codestyle checks all E2E JS/TS files and fixes them if possible |
| `eslint:storefront` | Codestyle checks all Storefront JS/TS files |
| `init:testdb` | Initializes the test database |
| `lint` | Shorthand for the composer commands `stylelint`, `eslint`, `ecs`, `lint:changlog` and `lint:snippets` |
| `lint:changelog` | Validates changelogs |
| `lint:snippets` | Validates existence of snippets in all core-supported languages |
| `phpstan` | runs the PHP static analysis tool |
| `phpunit` | Launches the PHP unit test-suit |
| `phpunit:quarantined` | Launches the PHP unit test-suite for quarantined tests |
| `storefront:unit` | Launches the jest unit test-suite for the Storefront |
| `storefront:unit:watch` | Launches the interactive jest unit test-suite watcher for the Storefront |

---

## Commands Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/commands-reference.html

# Commands Reference [​](#commands-reference)

These commands can be executed using the Shopware command line interface (CLI), located within your Shopware project.

bash

```shiki
$ bin/console [command] [parameters]
```

## Commands [​](#commands)

### General [​](#general)

| Command | Description |
| --- | --- |
| `about` | Displays information about the current project |
| `completion` | Dump the shell completion script |
| `help` | Displays help for a command |
| `list` | Lists commands |

### Administration [​](#administration)

| Command | Description |
| --- | --- |
| `administration:delete-extension-local-public-files` | Deletes all files in the local public folder of the extension. This command should run after assets:install so the assets are available in the public folder. |
| `administration:delete-files-after-build` | Deletes all unnecessary files of the administration after the build process |

### App [​](#app)

| Command | Description |
| --- | --- |
| `app:activate` | Activates the app in the folder with the given name |
| `app:create` | Creates an app skeleton |
| `app:deactivate` | Deactivates the app in the folder with the given name |
| `app:install` | Installs the app in the folder with the given name |
| `app:list` | Lists all apps |
| `app:refresh` | [app:update] Refreshes the installed apps |
| `app:uninstall` | Uninstalls the app |
| `app:url-change:resolve` | Resolves changes in the app URL and how the app system should handle it. |
| `app:validate` | Checks manifests for errors |

### Assets [​](#assets)

| Command | Description |
| --- | --- |
| `assets:install` | Installs bundles web assets under a public web directory |

### Bundle [​](#bundle)

| Command | Description |
| --- | --- |
| `bundle:dump` | [administration:dump:plugins|administration:dump:bundles] Creates a JSON file with the configuration for each active Shopware bundle. |

### Cache [​](#cache)

| Command | Description |
| --- | --- |
| `cache:clear` | Clears the cache |
| `cache:clear:all` | Clear all caches/pools, invalidates expired tags, removes old system and twig cache directories |
| `cache:clear:delayed` | Invalidates the delayed cache keys/tags |
| `cache:clear:http` | Clear only the HTTP cache |
| `cache:pool:clear` | Clears cache pools |
| `cache:pool:delete` | Deletes an item from a cache pool |
| `cache:pool:invalidate-tags` | Invalidate cache tags for all or a specific pool |
| `cache:pool:list` | Lists available cache pools |
| `cache:pool:prune` | Prunes cache pools |
| `cache:warmup` | Warms up an empty cache |
| `cache:watch:delayed` | Watches the delayed cache keys/tags |

### Cart [​](#cart)

| Command | Description |
| --- | --- |
| `cart:migrate` | Migrates carts from redis to database |

### Changelog [​](#changelog)

| Command | Description |
| --- | --- |
| `changelog:change` | Returns all changes made in a specific / unreleased version. |
| `changelog:check` | Checks the validation of a given changelog file or of all files in the "changelog/\_unreleased" folder |
| `changelog:create` | Creates a changelog markdown file in `/changelog/_unreleased` |
| `changelog:release` | Creates or updates the final changelog for a new release |

### Config [​](#config)

| Command | Description |
| --- | --- |
| `config:dump-reference` | Dumps the default configuration for an extension |

### Customer [​](#customer)

| Command | Description |
| --- | --- |
| `customer:delete-unused-guests` | Deletes unused guest customers |

### Dal [​](#dal)

| Command | Description |
| --- | --- |
| `dal:create:entities` | Creates the entity classes |
| `dal:create:hydrators` | Creates the hydrator classes |
| `dal:migration:create` | Creates migration for entity schema |
| `dal:create:schema` | Creates the database schema |
| `dal:refresh:index` | Refreshes the index for a given entity |
| `dal:validate` | Validates the DAL definitions |

### Database [​](#database)

| Command | Description |
| --- | --- |
| `database:clean-personal-data` | Cleans personal data from the database |
| `database:create-migration` | Creates a new migration file |
| `database:migrate` | Executes all migrations |
| `database:migrate-destructive` | Executes all migrations |
| `database:refresh-migration` | Refreshes the migration state |

### Debug [​](#debug)

| Command | Description |
| --- | --- |
| `debug:autowiring` | Lists classes/interfaces you can use for autowiring |
| `debug:business-events` | Dumps all business events |
| `debug:config` | Dumps the current configuration for an extension |
| `debug:container` | Displays current services for an application |
| `debug:dotenv` | Lists all dotenv files with variables and values |
| `debug:event-dispatcher` | Displays configured listeners for an application |
| `debug:messenger` | Lists messages you can dispatch using the message buses |
| `debug:router` | Displays current routes for an application |
| `debug:scheduler` | Lists schedules and their recurring messages |
| `debug:serializer` | Displays serialization information for classes |
| `debug:translation` | Displays translation messages information |
| `debug:twig` | Shows a list of twig functions, filters, globals and tests |
| `debug:validator` | Displays validation constraints for classes |

### Dotenv [​](#dotenv)

| Command | Description |
| --- | --- |
| `dotenv:dump` | Compile .env files to .env.local.php |

### Error [​](#error)

| Command | Description |
| --- | --- |
| `error:dump` | Dump error pages to plain HTML files that can be directly served by a web server |

### Es [​](#es)

| Command | Description |
| --- | --- |
| `es:admin:index` | Indexes the elasticsearch for the admin search |
| `es:admin:mapping:update` | Update the Elasticsearch indices mapping |
| `es:admin:reset` | Reset Admin Elasticsearch indexing |
| `es:admin:test` | Allows you to test the admin search index |
| `es:create:alias` | Creates the elasticsearch alias |
| `es:index` | Reindexes all entities to elasticsearch |
| `es:index:cleanup` | Cleans outdated indices |
| `es:mapping:update` | Update the Elasticsearch indices mapping |
| `es:reset` | Resets the elasticsearch index |
| `es:status` | Shows the status of the elasticsearch index |
| `es:test:analyzer` | Allows to test an elasticsearch analyzer |

### Feature [​](#feature)

| Command | Description |
| --- | --- |
| `feature:disable` | Disable feature flags |
| `feature:dump` | [administration:dump:features] Creates a JSON file with feature config for JS testing and hot reloading capabilities |
| `feature:enable` | Enable feature flags |
| `feature:list` | List all registered features |

### Framework [​](#framework)

| Command | Description |
| --- | --- |
| `framework:demodata` | Generates demo data |
| `framework:dump:class:schema` | Dumps the schema of the given entity |
| `framework:schema` | Dumps the api definition to a json file. |

### Http [​](#http)

| Command | Description |
| --- | --- |
| `http:cache:warm:up` | Warms up the HTTP cache |

### Import [​](#import)

| Command | Description |
| --- | --- |
| `import:entity` | Imports entities from a CSV file |

### Import-export [​](#import-export)

| Command | Description |
| --- | --- |
| `import-export:delete-expired` | Deletes all expired import/export files |

### Integration [​](#integration)

| Command | Description |
| --- | --- |
| `integration:create` | Create an integration and dump the key and secret |

### Lint [​](#lint)

| Command | Description |
| --- | --- |
| `lint:container` | Ensures that arguments injected into services match type declarations |
| `lint:translations` | Lint translations files syntax and outputs encountered errors |
| `lint:twig` | Lints a Twig template and outputs encountered errors |
| `lint:xliff` | Lints a XLIFF file and outputs encountered errors |
| `lint:yaml` | Lints a YAML file and outputs encountered errors |

### Mailer [​](#mailer)

| Command | Description |
| --- | --- |
| `mailer:test` | Tests Mailer transports by sending an email |

### Make plugin [​](#make-plugin)

Generating the skeletons and essential files needed to create and structure a Shopware plugin.

| Command | Description |
| --- | --- |
| `make:plugin:admin-module` | Generate an administration module skeleton |
| `make:plugin:command` | Generate a plugin CLI command skeleton |
| `make:plugin:composer` | Generate a composer configuration for a plugin |
| `make:plugin:config` | Generate a plugin system config skeleton |
| `make:plugin:custom-fieldset` | Generate a custom field set for a plugin |
| `make:plugin:entity` | Generate entity scaffolding for a plugin |
| `make:plugin:event-subscriber` | Generate an event subscriber skeleton |
| `make:plugin:javascript-plugin` | Generate a JavaScript plugin skeleton |
| `make:plugin:plugin-class` | Generate the base plugin class |
| `make:plugin:scheduled-task` | Generate a scheduled task skeleton |
| `make:plugin:store-api-route` | Generate a Store API route skeleton |
| `make:plugin:storefront-controller` | Generate a Storefront controller skeleton |
| `make:plugin:tests` | Generate a plugin tests skeleton |

### Media [​](#media)

| Command | Description |
| --- | --- |
| `media:delete-local-thumbnails` | Deletes all physical media thumbnails when remote thumbnails is enabled. |
| `media:delete-unused` | Deletes all media files that are never used. Use the `--dry-run` flag to see a paginated list of files that will be deleted, without actually deleting them. Use the `--grace-period-days=10` to set a grace period for unused media, meaning only media uploaded before the current date and time minus 10 days will be considered for deletion. The default is 20 and therefore any media uploaded in the previous 20 days will not be considered for deletion even if it is unused. Use the `--folder-entity` flag to target only a specific folder (e.g. `--folder-entity=PRODUCT` to purge all product images) |
| `media:generate-media-types` | Generates the media types for all media entities |
| `media:generate-thumbnails` | Generates the thumbnails for all media entities |
| `media:update-path` | Iterates over the media and updates the path column. |

### Messenger [​](#messenger)

| Command | Description |
| --- | --- |
| `messenger:consume` | Consumes messages |
| `messenger:failed:remove` | Removes given messages from the failure transport |
| `messenger:failed:retry` | Retries one or more messages from the failure transport |
| `messenger:failed:show` | Shows one or more messages from the failure transport |
| `messenger:setup-transports` | Prepares the required infrastructure for the transport |
| `messenger:stats` | Shows the message count for one or more transports |
| `messenger:stop-workers` | Stops workers after their current message |

### Number-range [​](#number-range)

| Command | Description |
| --- | --- |
| `number-range:migrate` | Migrates the increment storage of a number range |

### Plugin [​](#plugin)

| Command | Description |
| --- | --- |
| `plugin:activate` | Activates given plugins |
| `plugin:create` | Creates a plugin skeleton |
| `plugin:deactivate` | Deactivates given plugins |
| `plugin:install` | Installs given plugins |
| `plugin:list` | Lists all plugins |
| `plugin:refresh` | Refreshes the plugins list in the storage from the file system |
| `plugin:uninstall` | Uninstalls given plugins |
| `plugin:update` | Updates given plugins |
| `plugin:update:all` | Install all available plugin updates |
| `plugin:zip-import` | Imports a plugin from a zip file |

### Product-export [​](#product-export)

| Command | Description |
| --- | --- |
| `product-export:generate` | Generates a product export file |

### Router [​](#router)

| Command | Description |
| --- | --- |
| `router:match` | Helps debug routes by simulating a path info match |

### S3 [​](#s3)

| Command | Description |
| --- | --- |
| `s3:set-visibility` | Sets the visibility of all files in the s3 filesystem to public |

### Sales-channel [​](#sales-channel)

| Command | Description |
| --- | --- |
| `sales-channel:create` | Creates a new sales channel |
| `sales-channel:create:storefront` | Creates a new storefront sales channel |
| `sales-channel:list` | Lists all sales channels |
| `sales-channel:maintenance:disable` | Disables maintenance mode for a sales channel |
| `sales-channel:maintenance:enable` | Enables maintenance mode for a sales channel |
| `sales-channel:update:domain` | Updates a sales channel domain |

### Scheduled-task [​](#scheduled-task)

| Command | Description | Version |
| --- | --- | --- |
| `scheduled-task:deactivate` | Deactivate a scheduled task | 6.7.2.0 |
| `scheduled-task:register` | Registers all scheduled tasks |  |
| `scheduled-task:run` | Runs scheduled tasks |  |
| `scheduled-task:run-single` | Runs single scheduled tasks | 6.5.5.0 |
| `scheduled-task:list` | Lists all scheduled tasks | 6.5.5.0 |
| `scheduled-task:schedule` | Schedule a scheduled task | 6.7.2.0 |

### Secrets [​](#secrets)

| Command | Description |
| --- | --- |
| `secrets:decrypt-to-local` | Decrypts all secrets and stores them in the local vault |
| `secrets:encrypt-from-local` | Encrypts all local secrets to the vault |
| `secrets:generate-keys` | Generates new encryption keys |
| `secrets:list` | Lists all secrets |
| `secrets:remove` | Removes a secret from the vault |
| `secrets:reveal` | Reveal the value of a secret |
| `secrets:set` | Sets a secret in the vault |

### Server [​](#server)

| Command | Description |
| --- | --- |
| `server:dump` | Start a dump server that collects and displays dumps in a single place |
| `server:log` | Start a log server that displays logs in real time |

### Services [​](#services)

| Command | Description |
| --- | --- |
| `services:install` | Install all services |

### Sitemap [​](#sitemap)

| Command | Description |
| --- | --- |
| `sitemap:generate` | Generates sitemaps for a given shop (or all active ones) |

### Snippets [​](#snippets)

| Command | Description |
| --- | --- |
| `snippets:validate` | Validates snippets |

### State-machine [​](#state-machine)

| Command | Description |
| --- | --- |
| `state-machine:dump` | Dumps a state machine to a graphviz file |

### Store [​](#store)

| Command | Description |
| --- | --- |
| `store:download` | Downloads a plugin from the store |
| `store:login` | Login for the store |

### System [​](#system)

| Command | Description |
| --- | --- |
| `system:check` | Check the shopware application system health |
| `system:config:get` | Gets a config value |
| `system:config:set` | Sets a config value |
| `system:configure-shop` | Configures the shop |
| `system:generate-app-secret` | Generates a new app secret |
| `system:generate-jwt-secret` | Generates a new JWT secret |
| `system:install` | Installs the Shopware 6 system |
| `system:is-installed` | Checks if the system is installed and returns exit code 0 if Shopware is installed |
| `system:setup` | Setup the system |
| `system:setup:staging` | Installs the Shopware 6 system in staging mode |
| `system:update:finish` | Finishes the update process |
| `system:update:prepare` | Prepares the update process |

### Theme [​](#theme)

| Command | Description |
| --- | --- |
| `theme:change` | Changes the active theme for a sales channel |
| `theme:compile` | Compiles the theme |
| `theme:create` | Creates a theme skeleton |
| `theme:dump` | Dumps the theme configuration |
| `theme:prepare-icons` | Prepares the theme icons |
| `theme:refresh` | Refreshes the theme configuration |

### Translation [​](#translation)

| Command | Description |
| --- | --- |
| `translation:extract` | Extract missing translations keys from code to translation files |
| `translation:install` | Downloads and installs translations from the translations GitHub repository for the specified locales or all available locales |
| `translation:pull` | Pull translations from a given provider. |
| `translation:push` | Push translations to a given provider. |

### User [​](#user)

| Command | Description |
| --- | --- |
| `user:change-password` | Changes the password of a user |
| `user:create` | Creates a new user |
| `user:list` | List current users |

---

## Flow Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/flow-reference.html

# Flow Reference [​](#flow-reference)

INFO

This functionality is available starting with Shopware 6.4.6.0

| Event | Description |
| --- | --- |
| checkout.customer.before.login | Triggers as soon as a customer logs in |
| checkout.customer.deleted | Triggers if a customer gets deleted |
| checkout.customer.double\_opt\_in\_guest\_order | Triggers as soon as double opt-in is accepted in a guest order |
| checkout.customer.double\_opt\_in\_registration | Triggers when a customer commits to his registration via double opt-in |
| checkout.customer.guest\_register | Triggers when a new guest customer was registered |
| checkout.customer.login | Triggers as soon as a customer logs in |
| checkout.customer.logout | Triggers when a customer logs out |
| checkout.customer.register | Triggers when a new customer was registered |
| checkout.order.payment\_method.changed | Triggers when a user changed payment method during checkout process |
| checkout.order.placed | Triggers when an order is placed |
| contact\_form.send | Triggers when a contact form is send |
| customer.group.registration.accepted | Triggers when admin accepted a user who register to join a customer group |
| customer.group.registration.declined | Triggers when admin declined a user who register to join a customer group |
| customer.recovery.request | Triggers when a customer recovers his password |
| mail.after.create.message | Triggers when a mail message/ content is created |
| mail.before.send | Triggers before a mail is send |
| mail.sent | Triggers when a mail is send from Shopware |
| newsletter.confirm | Triggers when newsletter was confirmed by a user |
| newsletter.register | Triggers when user registered to subscribe to a sales channel newsletter |
| newsletter.unsubscribe | Triggers when user unsubscribe from a sales channel newsletter |
| product\_export.log | Triggers when product export is executed |
| review\_form.send | Triggers when a product review form is submitted by a customer |
| state\_enter.order.state.cancelled | Triggers when an order enters status "Cancelled" |
| state\_enter.order.state.completed | Triggers when an order enters status "Completed" |
| state\_enter.order.state.in\_progress | Triggers when an order enters status "In progress" |
| state\_enter.order.state.open | Triggers when an order enters status "Open" |
| state\_enter.order\_delivery.state.cancelled | Triggers when an order delivery enters status "Cancelled" |
| state\_enter.order\_delivery.state.open | Triggers when an order delivery enters status "Open" |
| state\_enter.order\_delivery.state.returned | Triggers when an order delivery enters status "Returned" |
| state\_enter.order\_delivery.state.returned\_partially | Triggers when an order delivery enters status "Return partially" |
| state\_enter.order\_delivery.state.shipped | Triggers when an order delivery enters status "Shipped" |
| state\_enter.order\_delivery.state.shipped\_partially | Triggers when an order delivery enters status "Shipped partially" |
| state\_enter.order\_transaction.state.authorized | Triggers when an order payment enters status "Authorized" |
| state\_enter.order\_transaction.state.cancelled | Triggers when an order payment enters status "Cancelled" |
| state\_enter.order\_transaction.state.chargeback | Triggers when an order payment enters status "Chargeback" |
| state\_enter.order\_transaction.state.failed | Triggers when an order payment enters status "Failed" |
| state\_enter.order\_transaction.state.in\_progress | Triggers when an order payment enters status "In progress" |
| state\_enter.order\_transaction.state.open | Triggers when an order payment enters status "Open" |
| state\_enter.order\_transaction.state.paid | Triggers when an order payment enters status "Paid" |
| state\_enter.order\_transaction.state.paid\_partially | Triggers when an order payment enters status "Paid partially" |
| state\_enter.order\_transaction.state.refunded | Triggers when an order payment enters status "Refunded" |
| state\_enter.order\_transaction.state.refunded\_partially | Triggers when an order payment enters status "Refunded partially" |
| state\_enter.order\_transaction.state.reminded | Triggers when an order payment enters status "Reminded" |
| state\_enter.order\_transaction.state.unconfirmed | Triggers when an order payment enters status "Unconfirmed" |
| state\_enter.order\_transaction\_capture.state.completed | Triggers when a payment capture is fully completed |
| state\_enter.order\_transaction\_capture.state.failed | Triggers when a payment capture attempt fails |
| state\_enter.order\_transaction\_capture.state.pending | Triggers when a payment capture is initiated and waiting for completion |
| state\_enter.order\_transaction\_capture\_refund.state.cancelled | Triggers when a capture refund request is cancelled |
| state\_enter.order\_transaction\_capture\_refund.state.completed | Triggers when a capture refund is completed |
| state\_enter.order\_transaction\_capture\_refund.state.failed | Triggers when a capture refund fails |
| state\_enter.order\_transaction\_capture\_refund.state.in\_progress | Triggers when a capture refund is currently being processed |
| state\_enter.order\_transaction\_capture\_refund.state.open | Triggers when a capture refund enters status "Open" |
| state\_leave.order.state.cancelled | Triggers when an order leaves status "Cancelled" |
| state\_leave.order.state.completed | Triggers when an order leaves status "Completed" |
| state\_leave.order.state.in\_progress | Triggers when an order leaves status "In progress" |
| state\_leave.order.state.open | Triggers when an order leaves status "Open" |
| state\_leave.order\_delivery.state.cancelled | Triggers when an order delivery leaves status "Cancelled" |
| state\_leave.order\_delivery.state.open | Triggers when an order delivery leaves status "Open" |
| state\_leave.order\_delivery.state.returned | Triggers when an order delivery leaves status "Returned" |
| state\_leave.order\_delivery.state.returned\_partially | Triggers when an order delivery leaves status "Return partially" |
| state\_leave.order\_delivery.state.shipped | Triggers when an order delivery leaves status "Shipped" |
| state\_leave.order\_delivery.state.shipped\_partially | Triggers when an order delivery status is changed from “Shipped partially” |
| state\_leave.order\_transaction.state.authorized | Triggers when an order payment leaves status "Authorized" |
| state\_leave.order\_transaction.state.cancelled | Triggers when an order payment leaves status "Cancelled" |
| state\_leave.order\_transaction.state.chargeback | Triggers when an order payment leaves status "Chargeback" |
| state\_leave.order\_transaction.state.failed | Triggers when an order payment leaves status "Failed" |
| state\_leave.order\_transaction.state.in\_progress | Triggers when an order payment leaves status "In progress" |
| state\_leave.order\_transaction.state.open | Triggers when an order payment leaves status "Open" |
| state\_leave.order\_transaction.state.paid | Triggers when an order payment leaves status "Paid" |
| state\_leave.order\_transaction.state.paid\_partially | Triggers when an order payment leaves status "Paid partially" |
| state\_leave.order\_transaction.state.refunded | Triggers when an order payment leaves status "Refunded" |
| state\_leave.order\_transaction.state.refunded\_partially | Triggers when an order payment leaves status "Refunded partially" |
| state\_leave.order\_transaction.state.reminded | Triggers when an order payment leaves status "Reminded" |
| state\_leave.order\_transaction.state.unconfirmed | Triggers when an order payment leaves status "Unconfirmed" |
| state\_leave.order\_transaction\_capture.state.completed | Triggers when a payment capture leaves status "Completed" |
| state\_leave.order\_transaction\_capture.state.failed | Triggers when a payment capture leaves status "Failed" |
| state\_leave.order\_transaction\_capture.state.pending | Triggers when a payment capture leaves "Pending" status |
| state\_leave.order\_transaction\_capture\_refund.state.cancelled | Triggers when a capture refund leaves status "Cancelled" |
| state\_leave.order\_transaction\_capture\_refund.state.completed | Triggers when a capture refund leaves status "Completed" |
| state\_leave.order\_transaction\_capture\_refund.state.failed | Triggers when a capture refund leaves status "Failed" |
| state\_leave.order\_transaction\_capture\_refund.state.in\_progress | Triggers when a capture refund leaves "In progress" status |
| state\_leave.order\_transaction\_capture\_refund.state.open | Triggers when a capture refund leaves status "Open" |
| user.recovery.request | Triggers when a user created a password recovery request at admin |

## B2B [​](#b2b)

### Trigger interfaces [​](#trigger-interfaces)

| Name | Provided |
| --- | --- |
| EmployeeAware | employeeId |

### Events [​](#events)

| Class | Description | Component |
| --- | --- | --- |
| collect.permission-events | Triggers when base permissions are created | Employee Management |
| employee.invite.sent | Triggers when an employee invitation has been sent | Employee Management |
| employee.invite.accepted | Triggers when an employee invitation has been accepted | Employee Management |
| employee.recovery.request | Triggers when an employee requests password recovery | Employee Management |
| employee.status.changed | Triggers when the status of an employee changes | Employee Management |
| employee.role.changed | Triggers when the role of an employee changes | Employee Management |
| employee.order.placed | Triggers when an employee places an order | Employee Management |

---

## Rules Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/rules-reference.html

# Rules Reference [​](#rules-reference)

List of all rule classes across Shopware 6.

## Checkout [​](#checkout)

| Class | Description |
| --- | --- |
| [Shopware\Core\Checkout\Cart\Rule\AlwaysValidRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/AlwaysValidRule.php) | Matches always |
| [Shopware\Core\Checkout\Cart\Rule\CartAmountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartAmountRule.php) | Matches a specific number to the carts total price. |
| [Shopware\Core\Checkout\Cart\Rule\CartHasDeliveryFreeItemRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartHasDeliveryFreeItemRule.php) | Matches if the cart has a free delivery item. |
| [Shopware\Core\Checkout\Cart\Rule\CartWeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartWeightRule.php) | Matches a specific number to the current cart's total weight. |
| [Shopware\Core\Checkout\Cart\Rule\GoodsCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/GoodsCountRule.php) | Matches a number to the current cart's line item goods count. |
| [Shopware\Core\Checkout\Cart\Rule\GoodsPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/GoodsPriceRule.php) | Matches a specific number to the carts goods price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemClearanceSaleRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemClearanceSaleRule.php) | Matches a specific line item which is on clearance sale |
| [Shopware\Core\Checkout\Cart\Rule\LineItemCreationDateRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemCreationDateRule.php) | Matches if a line item has a specific creation date. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemCustomFieldRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemCustomFieldRule.php) | Matches if a line item has a specific custom field. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionHeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionHeightRule.php) | Matches a specific line item's height. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionLengthRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionLengthRule.php) | Matches a specific line item's length. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionWeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionWeightRule.php) | Matches a specific line item's weight. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionWidthRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionWidthRule.php) | Matches a specific line item's width. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemGroupRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemGroupRule.php) | Matches if a line item has a specific group. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemInCategoryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemInCategoryRule.php) | Matches if a line item is in a specific category. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemIsNewRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemIsNewRule.php) | Matches if a line item is marked as new. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemListPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemListPriceRule.php) | Matches a specific line item has a specific list price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemOfManufacturerRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemOfManufacturerRule.php) | Matches a specific line item has a specific manufacturer. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemOfTypeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemOfTypeRule.php) | Matches a specific type name to the line item's type. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPromotedRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPromotedRule.php) | Matches if a line item is promoted. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPropertyRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPropertyRule.php) | Matches if a line item has a specific property. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPurchasePriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPurchasePriceRule.php) | Matches if a line item has a specific purchase price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemReleaseDateRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemReleaseDateRule.php) | Matches a specific line item's release date. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemRule.php) | Matches multiple identifiers to a line item's keys. True if one identifier matches. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTagRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTagRule.php) | Matches multiple tags to a line item's tag. True if one tag matches. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTaxationRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTaxationRule.php) | Matches if a line item has a specific tax. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTotalPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTotalPriceRule.php) | Matches a number to the current cart's line item total price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemUnitPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemUnitPriceRule.php) | Matches a specific number to a line item's price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemWithQuantityRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemWithQuantityRule.php) | Matches a specific line item's quantity to the current line item's quantity. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemWrapperRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemWrapperRule.php) | Internally handled scope changes. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemsInCartCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemsInCartCountRule.php) | Matches a number to the current cart's line item count. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemsInCartCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemsInCartCountRule.php) | Matches multiple identifiers to a carts line item's identifier. True if one identifier matches. |
| [Shopware\Core\Checkout\Cart\Rule\PaymentMethodRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/PaymentMethodRule.php) | Matches if a specific payment method is used |
| [Shopware\Core\Checkout\Cart\Rule\ShippingMethodRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/ShippingMethodRule.php) | Matches if a specific shipping method is used |
| [Shopware\Core\Checkout\Customer\Rule\BillingCountryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingCountryRule.php) | Matches multiple countries to the customer's active billing address country. |
| [Shopware\Core\Checkout\Customer\Rule\BillingStreetRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingStreetRule.php) | Matches multiple street names to the customer's active billing address street name. |
| [Shopware\Core\Checkout\Customer\Rule\BillingZipCodeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingZipCodeRule.php) | Matches multiple zip codes to the customer's active billing address zip code. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerGroupRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerGroupRule.php) | Matches multiple customer groups to the current customers group. True if one customer group matches. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerNumberRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerNumberRule.php) | Matches multiple numbers to the active customers number. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerTagRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerTagRule.php) | Matches a tag set to customers |
| [Shopware\Core\Checkout\Customer\Rule\DaysSinceLastOrderRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/DaysSinceLastOrderRule.php) | Matches a specific number of days to the last order creation date. |
| [Shopware\Core\Checkout\Customer\Rule\DifferentAddressesRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/DifferentAddressesRule.php) | Matches if active billing address is not the default. |
| [Shopware\Core\Checkout\Customer\Rule\IsCompanyRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/IsCompanyRule.php) | Matches if the customer is a company |
| [Shopware\Core\Checkout\Customer\Rule\IsNewCustomerRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/IsNewCustomerRule.php) | Matches if a customer is new, by matching the `firstLogin` property with today. |
| [Shopware\Core\Checkout\Customer\Rule\LastNameRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/LastNameRule.php) | Exactly matches a string to the customer's last name. |
| [Shopware\Core\Checkout\Customer\Rule\OrderCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/OrderCountRule.php) | Matches a specific number to the number of orders of the current customer. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingCountryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingCountryRule.php) | Matches multiple countries to the customer's active shipping address country. True if one country matches. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingStreetRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingStreetRule.php) | Matches multiple street names to the customer's active shipping address street name. True if one street name matches. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingZipCodeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingZipCodeRule.php) | Matches multiple zip codes to the customer's active shipping address zip code. True if one zip code matches. |

## Framework [​](#framework)

| Class | Description |
| --- | --- |
| [Shopware\Core\Framework\Rule\Container\AndRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/Container/AndRule.php) | Composition of rules. Matches if all match. |
| [Shopware\Core\Framework\Rule\Container\NotRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/Container/NotRule.php) | Negates one rule. |
| [Shopware\Core\Framework\Rule\Container\OrRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/Container/OrRule.php) | Composition of rules. Matches if at least one rule matches. |
| [Shopware\Core\Framework\Rule\Container\XorRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/Container/XorRule.php) | Composition of rules. Matches if exactly one matches. |
| [Shopware\Core\Framework\Rule\DateRangeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/DateRangeRule.php) | Match a fixed date range to now. |
| [Shopware\Core\Framework\Rule\SalesChannelRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/SalesChannelRule.php) | Match a specific sales channel to the current context. |
| [Shopware\Core\Framework\Rule\TimeRangeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/TimeRangeRule.php) | Matches a fixed time range to now. |
| [Shopware\Core\Framework\Rule\WeekdayRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Rule/WeekdayRule.php) | Matches a fixed day of the week to now. |

## System [​](#system)

| Class | Description |
| --- | --- |
| [Shopware\Core\System\Currency\Rule\CurrencyRule](https://github.com/shopware/shopware/blob/trunk/src/Core/System/Currency/Rule/CurrencyRule.php) | Match a specific currency to the current context. |

## B2B [​](#b2b)

| Class | Description | Component |
| --- | --- | --- |
| EmployeeOrderRule | Matches if the order was placed by an employee | Employee Management |
| EmployeeOfBusinessPartnerRule | Matches if the customer is an employee of a specific business partner | Employee Management |
| EmployeeRoleRule | Matches if a specific role is assigned to an employee | Employee Management |
| EmployeeStatusRule | Matches if the employee as a specific status | Employee Management |
| IsEmployeeRule | Matches if the customer is an employee | Employee Management |

---

## Actions Reference

**Source:** https://developer.shopware.com/docs/resources/references/core-reference/actions-reference.html

# Actions Reference [​](#actions-reference)

## B2B [​](#b2b)

| Class | Description | Component |
| --- | --- | --- |
| ChangeEmployeeStatusAction | Assigns the configured status to the employee | Employee Management |
| ChangeCustomerSpecificFeaturesAction | Adds or removes the configured b2b components for the customer | Employee Management |

---

