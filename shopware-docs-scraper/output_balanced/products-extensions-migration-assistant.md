# Products Extensions Migration Assistant

*Scraped from Shopware Developer Documentation*

---

## Migration Assistant

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/

# Migration Assistant [​](#migration-assistant)

To either migrate data (products, customers, etc.) from the existing shop system to Shopware 6 or to update them, you need to establish a connection between a data source (existing shop, e.g., Shopware 5) and Shopware 6. The Migration Assistant makes it possible to connect these two systems. Once the connection is established, it can be accessed at any time. After the first complete migration, individual datasets can also be migrated or updated as needed.

Let's learn more about this extension in the following sections.

---

## Concept

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/

# Concept [​](#concept)

## Overview [​](#overview)

[Shopware Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) was built with simple but powerful concepts in mind. These enable you to extend the plugin in various ways and migrate data into the Shopware 6 environment. You should have a basic understanding of how to use the migration plugin and its core features before extending it yourself, as this documentation will not explain the usage of the plugin.

We will provide you with a basic introduction to the concepts and structure right here in this chapter. Take a look at the last headline (Extension points) to find out more about the various ways to extend this plugin.

## Profile and connections [​](#profile-and-connections)

Users of the plugin can create connections to different source systems. A connection is used to allow multiple migrations from the same source and update the right data (mapping). Connections require a specific profile indicating the type of source system. Users can, for example, create a connection to a Shopware shop using the Shopware 5.5 profile. Developers can create their own profiles from scratch, connect to different source systems, or just extend existing ones.

For more details, look at [Profile and Connection](./profile-and-connection.html).

## DataSelection and dataSet [​](#dataselection-and-dataset)

These are the fundamental data structures for defining what to migrate. Each `DataSet` represents an entity, for example, a database table. Each `DataSelection` represents an orderly group of `DataSets`. For more information, refer to the articles on [DataSelection and DataSet](./dataselection-and-dataset.html).

## Migration context [​](#migration-context)

This data structure provides all the necessary data for the migration. For more details, refer to the [Migration Context](./migration-context.html).

## Premapping [​](#premapping)

Because the structure of the source system does not always match the structure of the target system, the user may need to map the old structure to the new one. For example, in Shopware 5, we have default salutations like `Mr.`, but the user can also create custom ones. In Shopware 6, there are default salutations like `Mr.` and the user can also create custom ones. So the salutation `Mr.` from Shopware 5 must be mapped to Shopware 6 `Mr.`. In this default case, the mapping can be achieved automatically, but customized salutations will most likely have to be mapped manually. The premapping will be written into the mapping table to associate the old identifier with the new one.

You can look at [Premapping](./premapping.html) section for more details.

## Gateway and reader [​](#gateway-and-reader)

Users will have to specify a gateway for the connection. The gateway defines the way of communicating with the source system. Behind the user interface, we use `Reader` objects to read the data from the source system. For the `shopware55` profile, we have the `api` gateway, which communicates via http/s with the source system, and the `local` gateway, which communicates directly with the source system's database. Thus both systems must be on the same server to successfully use the `local` gateway.

To use the `ShopwareApiGateway`, you must download the [Shopware Connector](https://github.com/shopware/SwagMigrationConnector) plugin for your Shopware 5.

For more details, look at the [Gateway and Reader](./gateway-and-reader.html) article.

## Converter, mapping, and deltas [​](#converter-mapping-and-deltas)

Data gathered by `Reader` objects is transferred to `Converter` objects that put the data in a format Shopware 6 is able to work with. Simultaneously entries in the underlying mapping table are inserted to map the old identifiers to the new ones for future migrations (Have a look at the `MappingService` for that). The mapping is saved for the current connection. Converted data will be removed after the migration, and the mapping will stay persistent. Also, a checksum is saved to the mapping to identify and skip the same source data (data has not been changed since the last migration).

You can find out more about them in the [Convert and Mapping](./convert-and-mapping.html) section of this guide.

## Logging [​](#logging)

During any migration, especially during the data conversion, there will possibly be errors that should be logged. The users can see these errors and these should be as helpful as possible.

For more information, have a look at the [Logging](./logging.html) section.

## Writer [​](#writer)

The `Writer` objects will receive the converted data and write it to Shopware 6. There is no special magic here; you don't need to worry about error handling because the migration assistant takes care of it.

To learn more about them, take a look at the [Writer](./writer.html) section.

## Media processing [​](#media-processing)

During a typical migration, we download the media files from the source system to Shopware 6. This is the last processing step in the migration and may be done differently for other gateways. For example, the `local` gateway will copy and rename the files directly in the local filesystem.

You can look at the [Media Processing](./media-processing.html) article for more details.

## After migration [​](#after-migration)

All fetched data will be deleted after finishing or aborting a migration run, but the mapping of the identifiers will stay.

## The migration procedure [​](#the-migration-procedure)

The following diagram visualizes how the migration process is executed in the message queue from a high level:

Inside this process it can run through these states:

The following bullet points will give you a general overview of what happens in what classes during a common migration.

1. The user selects/creates a connection (with a profile and gateway specified).
2. The user selects some of the available data (`DataSelections`).
3. Premapping check/execution: The user maps data from the source system to the current system (these decisions are stored with the connection).
4. Fetch data for every `DataSet` in every selected `DataSelection` (mapping is used to store/use the identifiers from the source system).
   1. The corresponding `Reader` reads the data.
   2. The corresponding `Converter` converts the data.
5. Write data for every `DataSet` in every selected `DataSelection` .
   1. The corresponding `Writer` writes the data.
6. Process media, if necessary, for example, to download/copy images.
   1. Data in the `swag_migration_media_file` table will be downloaded/copied.
   2. Files are assigned to media objects in Shopware 6.
7. Finish migration to clean up.

These steps can be done multiple times. Each migration is called a `Run`/`MigrationRun` and will be saved to inform the users about any errors that occurred (in the form of a detailed history).

## Extension points [​](#extension-points)

The recommended way to migrate plugin data from a source system is to extend that profile by a new `DataSelection`. It is also possible to create a new profile in case a migration from a different shop/source system is sought.

Take a look at the following HowTos for your scenario to get a step-by-step tutorial:

* [Extending a Shopware Migration Profile](./../guides/extending-a-shopware-migration-profile.html): Migrating your first basic plugin data (via local gateway).
* [Extending the Migration Connector](./../guides/extending-the-migration-connector.html): Add API support for your migration.
* [Decorating a Shopware Migration Assistant Converter](./../guides/decorating-a-shopware-migration-assistant-converter.html): Implement a premapping and change the behavior of an existing converter.
* [Creating a New Migration Profile](./../guides/creating-a-new-migration-profile.html): Create a new profile from scratch to support a third-party source system (other than Shopware).

---

## Profile and Connection

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/profile-and-connection.html

# Profile and Connection [​](#profile-and-connection)

## Overview [​](#overview)

Users of the plugin can create connections to different source systems. A connection is used to allow multiple migrations from the same source and update the right data (mapping). Connections require a specific profile indicating the type of source system. Users can, for example, create a connection to a Shopware shop using the Shopware 5.5 profile. Developers can create their own profiles from scratch, connect to different source systems, or just build and extend existing ones.

## Profile [​](#profile)

The base of Shopware Migration Assistant is the profile, which enables you to migrate your shop system to Shopware 6. Shopware Migration Assistant comes with the default Shopware 5.5 profile and is located in the `shopware55.xml`:

html

```shiki
<!-- Shopware 5.5 Profile -->
<service id="SwagMigrationAssistant\Profile\Shopware55\Shopware55Profile">
    <tag name="shopware.migration.profile"/>
</service>
```

In order to identify itself, the profile has to implement getter functions like `getName`, which returns the unique name of the profile. The profile is used together with the [Gateway](./gateway-and-reader.html#gateway) to check and apply the right processing during a migration run.

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware55;

use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class Shopware55Profile implements ShopwareProfileInterface
{
    public const PROFILE_NAME = 'shopware55';

    public const SOURCE_SYSTEM_NAME = 'Shopware';

    public const SOURCE_SYSTEM_VERSION = '5.5';

    public const AUTHOR_NAME = 'shopware AG';

    public const ICON_PATH = '/swagmigrationassistant/static/img/migration-assistant-plugin.svg';

    public function getName(): string
    {
        return self::PROFILE_NAME;
    }

    public function getSourceSystemName(): string
    {
        return self::SOURCE_SYSTEM_NAME;
    }

    public function getVersion(): string
    {
        return self::SOURCE_SYSTEM_VERSION;
    }

    public function getAuthorName(): string
    {
        return self::AUTHOR_NAME;
    }

    public function getIconPath(): string
    {
        return self::ICON_PATH;
    }
}
```

## Connection [​](#connection)

To connect Shopware 6 to your source system (e.g., Shopware 5), you will need a connection entity. The connection includes all the important information for your migration run. It contains the credentials for the API or database access, the actual [Premapping](./premapping.html) and the profile, [Gateway](./gateway-and-reader.html) combination which is used for your migration:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Connection;

/*...*/

class SwagMigrationConnectionDefinition extends EntityDefinition
{
    /*...*/

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
             (new IdField('id', 'id'))->setFlags(new PrimaryKey(), new Required()),
             (new StringField('name', 'name'))->setFlags(new Required()),
             (new JsonField('credential_fields', 'credentialFields'))->setFlags(new WriteProtected(MigrationContext::SOURCE_CONTEXT)),
             new JsonField('premapping', 'premapping'),
             (new StringField('profile_name', 'profileName'))->setFlags(new Required()),
             (new StringField('gateway_name', 'gatewayName'))->setFlags(new Required()),
             new CreatedAtField(),
             new UpdatedAtField(),
             new OneToManyAssociationField('runs', SwagMigrationRunDefinition::class, 'connection_id'),
             new OneToManyAssociationField('mappings', SwagMigrationMappingDefinition::class, 'connection_id'),
             new OneToManyAssociationField('settings', GeneralSettingDefinition::class, 'selected_connection_id'),
        ]);
    }
}
```

---

## DataSelection and DataSet

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/dataselection-and-dataset.html

# DataSelection and DataSet [​](#dataselection-and-dataset)

These are the fundamental data structures for defining what to migrate. Each `DataSelection` consists of one or more `DataSets`:

* ProductDataSelection (position: 100)
  + MediaFolderDataSet
  + ProductAttributeDataSet
  + ProductPriceAttributeDataSet
  + ManufacturerAttributeDataSet
  + ProductDataSet
  + PropertyGroupOptionDataSet
  + ProductOptionRelationDataSet
  + ProductPropertyRelationDataSet
  + TranslationDataSet
  + CrossSellingDataSet
* MediaDataSelection (position: 300)
  + MediaFolderDataSet
  + MediaDataSet

The order of the `DataSets` in the `DataSelection` class is important and specifies the processing order. `DataSelection` also holds a position specifying the order applied when migrating (lower numbers are migrated earlier). The `getDataSetsRequiredForCount` method returns an array of all DataSets. Its count should be displayed in the Administration.

Please take a look at the `DataSelection` example:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CrossSellingDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ManufacturerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\MediaFolderDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductOptionRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPriceAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPropertyRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\PropertyGroupOptionDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\TranslationDataSet;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductDataSelection implements DataSelectionInterface
{
    public const IDENTIFIER = 'products';

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getData(): DataSelectionStruct
    {
        return new DataSelectionStruct(
            self::IDENTIFIER,
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            'swag-migration.index.selectDataCard.dataSelection.products', // Snippet name
            100, // The position of the dataSelection
            true, // Is process-media needed (to download / copy images for example),
            DataSelectionStruct::BASIC_DATA_TYPE, // specify the type of data (core data or plugin data)
            false // Is the selection required for every migration? (the user can't unselect this data selection)
        );
    }

    public function getDataSets(): array
    {
        return [
            // The order matters!
            new MediaFolderDataSet(),
            new ProductAttributeDataSet(),
            new ProductPriceAttributeDataSet(),
            new ManufacturerAttributeDataSet(),
            new ProductDataSet(),
            new PropertyGroupOptionDataSet(),
            new ProductOptionRelationDataSet(),
            new ProductPropertyRelationDataSet(),
            new TranslationDataSet(),
            new CrossSellingDataSet(),
        ];
    }

    public function getDataSetsRequiredForCount(): array
    {
        return [
            new ProductDataSet(),
        ];
    }
}
```

Here's a `DataSet` example:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet;

use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductDataSet extends DataSet
{
    public static function getEntity(): string
    {
        return DefaultEntities::PRODUCT;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }
}
```

The `dataSelections` are registered the following way:

html

```shiki
<service id="SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection">
    <tag name="shopware.migration.data_selection"/>
</service>
```

It is also possible to specify the same `DataSets` in multiple `DataSelections` (this should only be done if no other options are available). Have a look at the `ProductReviewDataSelection`:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CrossSellingDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CustomerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CustomerDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ManufacturerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\MediaFolderDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductOptionRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPriceAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPropertyRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductReviewDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\PropertyGroupOptionDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\TranslationDataSet;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductReviewDataSelection implements DataSelectionInterface
{
    public const IDENTIFIER = 'productReviews';

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getData(): DataSelectionStruct
    {
        return new DataSelectionStruct(
            self::IDENTIFIER,
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            'swag-migration.index.selectDataCard.dataSelection.productReviews',
            250,
            true
        );
    }

    /**
     * {@inheritdoc}
     */
    public function getDataSets(): array
    {
        return [
            new MediaFolderDataSet(),
            new ProductAttributeDataSet(),
            new ProductPriceAttributeDataSet(),
            new ManufacturerAttributeDataSet(),
            new ProductDataSet(),
            new PropertyGroupOptionDataSet(),
            new ProductOptionRelationDataSet(),
            new ProductPropertyRelationDataSet(),
            new TranslationDataSet(),
            new CrossSellingDataSet(),
            new CustomerAttributeDataSet(),
            new CustomerDataSet(),
            new ProductReviewDataSet(),
        ];
    }

    public function getDataSetsRequiredForCount(): array
    {
        return [
            new ProductReviewDataSet(),
        ];
    }
}
```

INFO

There are duplicate DataSets from the `ProductDataSelection`, because they are also required if the user does not select the product `DataSelection`. If the user selects both, this `DataSets` will be only migrated once (with their first occurrence).

---

## Migration Context

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/migration-context.html

# Migration Context [​](#migration-context)

The central data structure of Shopware Migration Assistant is the migration context. The migration context contains the following information:

1. The current connection of migration which holds the credentials
2. Current Profile and Gateway instances
3. Identifier of the current run
4. Information on the current processing ([DataSet](./dataselection-and-dataset.html))
5. Offset and limit of the current call

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration;

use Shopware\Core\Framework\Struct\Struct;
use SwagMigrationAssistant\Migration\Connection\SwagMigrationConnectionEntity;
use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\Gateway\GatewayInterface;
use SwagMigrationAssistant\Migration\Profile\ProfileInterface;

class MigrationContext extends Struct implements MigrationContextInterface
{
    /* ... */

    public function getProfile(): ProfileInterface
    {
        return $this->profile;
    }

    public function getConnection(): ?SwagMigrationConnectionEntity
    {
        return $this->connection;
    }

    public function getRunUuid(): string
    {
        return $this->runUuid;
    }

    public function getDataSet(): ?DataSet
    {
        return $this->dataSet;
    }

    public function setDataSet(DataSet $dataSet): void
    {
        $this->dataSet = $dataSet;
    }

    public function getOffset(): int
    {
        return $this->offset;
    }

    public function getLimit(): int
    {
        return $this->limit;
    }

    public function getGateway(): GatewayInterface
    {
        return $this->gateway;
    }

    public function setGateway(GatewayInterface $gateway): void
    {
        $this->gateway = $gateway;
    }
}
```

---

## Premapping

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/premapping.html

# Premapping [​](#premapping)

The premapping will use the normal [Mapping](./convert-and-mapping.html#mapping) to store the old identifier with the equivalent new one. All premapping readers provide the information for the mapping choices and are registered like this:

html

```shiki
<service id="SwagMigrationAssistant\Profile\Shopware\Premapping\SalutationReader">
    <argument type="service" id="salutation.repository" />
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\GatewayRegistry"/>
    <tag name="shopware.migration.pre_mapping_reader"/>
</service>
```

The service will return a `PremappingStruct`, which consists of:

1. Entity of the premapping
2. Choices, representing Shopware 6 equivalents
3. Mapping, representing the source system's structure, including a destination/choice

Here is an example of how the final `PremappingStruct` looks like in the `generate-premapping` json response:

json

```shiki
{
   "entity":"salutation",
   "choices":[
      {
         "uuid":"d4883ea9db2b4a5ca033873903358062",
         "description":"mr",
         "extensions":[

         ]
      },
      {
         "uuid":"7a7ef1e4a9064c46b5f85e28b4d942a9",
         "description":"mrs",
         "extensions":[

         ]
      },
      {
         "uuid":"a6fa00aef9a648d9bd012dbe16c112bf",
         "description":"not_specified",
         "extensions":[

         ]
      }
   ],
   "mapping":[
      {
         "sourceId":"mr",
         "description":"mr",
         "destinationUuid":"d4883ea9db2b4a5ca033873903358062",
         "extensions":[

         ]
      },
      {
         "sourceId":"ms",
         "description":"ms",
         "destinationUuid":"",
         "extensions":[

         ]
      }
   ]
}
```

The `destinationUuid` in the `mapping` array sets the destination for that entity. It will be saved along with the [Connection](./profile-and-connection.html#connection), so the user does not have to make these decisions repeatedly. For more details on how the mapping process works and even more information on automatic assignment, look up more in the `SalutationReader` class.

To get the associated new identifier, you can make use of the `MappingService` similar to the `CustomerConverter`:

php

```shiki
<?php declare(strict_types=1);

/* ... */

protected function getSalutation(string $salutation): ?string
{
    $mapping = $this->mappingService->getMapping(
        $this->connectionId,
        SalutationReader::getMappingName(),
        $salutation,
        $this->context
    );

    if ($mapping === null) {
        $this->loggingService->addLogEntry(new UnknownEntityLog(
            $this->runId,
            DefaultEntities::SALUTATION,
            $salutation,
            DefaultEntities::CUSTOMER,
            $this->oldCustomerId
        ));

        return null;
    }
    $this->mappingIds[] = $mapping['id'];

    return $mapping['entityUuid'];
}

/* ... */
```

The `getMapping` method used in the mapping service looks up the `swag_migration_mapping` table for the combination of the old identifier and entity name stored in the current connection. Then it returns the mapping object containing the new Shopware 6 identifier. This identifier makes it possible to map your converted entity to your premapping choice. If `getMapping` returns null, then no valid mapping is available, and you have to log this with [LoggingService](./logging.html). The mapping object has two keys: `id` and `entityUuid`. The `id` key is the identifier of the `swag_migration_mapping` entry and has to be inserted in the `mappingIds`, if the mapping should be preloaded. The `entityUuid` key is the UUID of the mapped entity.

---

## Gateway and Reader

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/gateway-and-reader.html

# Gateway and Reader [​](#gateway-and-reader)

## Overview [​](#overview)

Users will have to specify a gateway for the connection. The gateway defines the way of communicating with the source system. Behind the user interface, we use `Reader` objects to read the data from the source system. For the `shopware55` profile, we have the `api` gateway, which communicates via http/s with the source system, and the `local` gateway, which communicates directly with the source system's database. Thus both systems must be on the same server to successfully use the `local` gateway.

## Gateway [​](#gateway)

The gateway defines how to communicate from Shopware 6 with your source system, like Shopware 5. Every profile needs to have at least one gateway. Gateways need to be defined in the corresponding service xml using the `shopware.migration.gateway` tag:

html

```shiki
<!-- Shopware Profile Gateways -->
<service id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ShopwareLocalGateway">
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ReaderRegistry" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\EnvironmentReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\TableReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactory" />
    <argument type="service" id="currency.repository"/>
    <tag name="shopware.migration.gateway" />
</service>

<service id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\ShopwareApiGateway">
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry"/>
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\EnvironmentReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\TableReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\TableCountReader" />
    <argument type="service" id="currency.repository"/>
    <tag name="shopware.migration.gateway" />
</service>
```

To use the `ShopwareApiGateway`, you must download the corresponding Shopware 5 plugin [Shopware migration connector](https://github.com/shopware/SwagMigrationConnector) first.

This tag is used by `GatwayRegistry`. This registry loads all tagged gateways and chooses a suitable gateway based on the migration's context and a unique identifier composed of a combination of profile and gateway name:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Gateway;

use SwagMigrationAssistant\Exception\MigrationContextPropertyMissingException;
use SwagMigrationAssistant\Exception\GatewayNotFoundException;
use SwagMigrationAssistant\Migration\MigrationContextInterface;

class GatewayRegistry implements GatewayRegistryInterface
{
    /**
     * @var GatewayInterface[]
     */
    private iterable $gateways;

    /**
     * @param GatewayInterface[] $gateways
    */
    public function __construct(iterable $gateways)
    {
        $this->gateways = $gateways;
    }

    /**
     * @throws GatewayNotFoundException
     *
     * @return GatewayInterface[]
     */
    public function getGateways(MigrationContextInterface $migrationContext): array
    {
        $gateways = [];
        foreach ($this->gateways as $gateway) {
            if ($gateway->supports($migrationContext)) {
                $gateways[] = $gateway;
            }
        }

        return $gateways;
    }

    /**
     * @throws GatewayNotFoundException
     */
    public function getGateway(MigrationContextInterface $migrationContext): GatewayInterface
    {
        $connection = $migrationContext->getConnection();
        if ($connection === null) {
            throw new MigrationContextPropertyMissingException('Connection');
        }

        $profileName = $connection->getProfileName();
        $gatewayName = $connection->getGatewayName();

        foreach ($this->gateways as $gateway) {
            if ($gateway->supports($migrationContext) && $gateway->getName() === $gatewayName) {
                return $gateway;
            }
        }

        throw new GatewayNotFoundException($profileName . '-' . $gatewayName);
    }
}
```

The gateway class has to implement the `GatewayInterface` to support all required methods. As you can see below, the gateway uses the right readers, which internally open a connection to the source system to receive the entity data:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\Gateway\Local;

use Shopware\Core\Defaults;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\Currency\CurrencyEntity;
use SwagMigrationAssistant\Migration\EnvironmentInformation;
use SwagMigrationAssistant\Migration\Gateway\Reader\EnvironmentReaderInterface;
use SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\RequestStatusStruct;
use SwagMigrationAssistant\Profile\Shopware\Exception\DatabaseConnectionException;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactoryInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\ShopwareGatewayInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\TableReaderInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ShopwareLocalGateway implements ShopwareGatewayInterface
{
    public const GATEWAY_NAME = 'local';

    private ReaderRegistry $readerRegistry;

    private EnvironmentReaderInterface $localEnvironmentReader;

    private TableReaderInterface $localTableReader;

    private ConnectionFactoryInterface $connectionFactory;

    private EntityRepository $currencyRepository;

    public function __construct(
        ReaderRegistry $readerRegistry,
        EnvironmentReaderInterface $localEnvironmentReader,
        TableReaderInterface $localTableReader,
        ConnectionFactoryInterface $connectionFactory,
        EntityRepository $currencyRepository
    ) {
        $this->readerRegistry = $readerRegistry;
        $this->localEnvironmentReader = $localEnvironmentReader;
        $this->localTableReader = $localTableReader;
        $this->connectionFactory = $connectionFactory;
        $this->currencyRepository = $currencyRepository;
    }

    public function getName(): string
    {
        return self::GATEWAY_NAME;
    }

    public function getSnippetName(): string
    {
        return 'swag-migration.wizard.pages.connectionCreate.gateways.shopwareLocal';
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function read(MigrationContextInterface $migrationContext): array
    {
        $reader = $this->readerRegistry->getReader($migrationContext);

        return $reader->read($migrationContext);
    }

    public function readEnvironmentInformation(MigrationContextInterface $migrationContext, Context $context): EnvironmentInformation
    {
        $connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
        $profile = $migrationContext->getProfile();

        if ($connection === null) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }

        try {
            $connection->connect();
        } catch (\Exception $e) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }
        $connection->close();
        $environmentData = $this->localEnvironmentReader->read($migrationContext);

        /** @var CurrencyEntity $targetSystemCurrency */
        $targetSystemCurrency = $this->currencyRepository->search(new Criteria([Defaults::CURRENCY]), $context)->get(Defaults::CURRENCY);
        if (!isset($environmentData['defaultCurrency'])) {
            $environmentData['defaultCurrency'] = $targetSystemCurrency->getIsoCode();
        }

        $totals = $this->readTotals($migrationContext, $context);

        return new EnvironmentInformation(
            $profile->getSourceSystemName(),
            $profile->getVersion(),
            $environmentData['host'],
            $totals,
            $environmentData['additionalData'],
            new RequestStatusStruct(),
            false,
            [],
            $targetSystemCurrency->getIsoCode(),
            $environmentData['defaultCurrency']
        );
    }

    public function readTotals(MigrationContextInterface $migrationContext, Context $context): array
    {
        $readers = $this->readerRegistry->getReaderForTotal($migrationContext);

        $totals = [];
        foreach ($readers as $reader) {
            $total = $reader->readTotal($migrationContext);

            if ($total === null) {
                continue;
            }

            $totals[$total->getEntityName()] = $total;
        }

        return $totals;
    }

    public function readTable(MigrationContextInterface $migrationContext, string $tableName, array $filter = []): array
    {
        return $this->localTableReader->read($migrationContext, $tableName, $filter);
    }
}
```

---

## Convert and Mapping

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/convert-and-mapping.html

# Convert and Mapping [​](#convert-and-mapping)

## Overview [​](#overview)

Data gathered by `Reader` objects is transferred to `Converter` objects that put the data in a format Shopware 6 is able to work with. Simultaneously entries in the underlying mapping table are inserted to map the old identifiers to the new ones for future migrations. The mapping is saved for the current connection. After the migration, the converted data will be removed, and the mapping will stay persistent.

## Converter [​](#converter)

All converters are registered in service container like this:

html

```shiki
<service id="SwagMigrationAssistant\Profile\Shopware\Converter\ProductConverter"
         parent="SwagMigrationAssistant\Profile\Shopware\Converter\ShopwareConverter" abstract="true">
    <argument type="service" id="SwagMigrationAssistant\Migration\Media\MediaFileService"/>
</service>
```

The converters have to extend the `ShopwareConverter` class and implement the `convert` method. This method will receive one data entry at a time. It will have to be returned in the right format to be usable for the `writer`.

php

```shiki
<?php declare(strict_types=1);

/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

abstract class ProductConverter extends ShopwareConverter
{
    /* ... */

    /**
     * @throws ParentEntityForChildNotFoundException
     */
    public function convert(
        array $data,
        Context $context,
        MigrationContextInterface $migrationContext
    ): ConvertStruct {
        $this->generateChecksum($data);
        $this->context = $context;
        $this->migrationContext = $migrationContext;
        $this->runId = $migrationContext->getRunUuid();
        $this->oldProductId = $data['detail']['ordernumber'];
        $this->mainProductId = $data['detail']['articleID'];
        $this->locale = $data['_locale'];

        $connection = $migrationContext->getConnection();
        $this->connectionName = '';
        $this->connectionId = '';
        if ($connection !== null) {
            $this->connectionId = $connection->getId();
            $this->connectionName = $connection->getName();
        }

        $fields = $this->checkForEmptyRequiredDataFields($data, $this->requiredDataFieldKeys);
        if (!empty($fields)) {
            $this->loggingService->addLogEntry(new EmptyNecessaryFieldRunLog(
                $this->runId,
                DefaultEntities::PRODUCT,
                $this->oldProductId,
                implode(',', $fields)
            ));

            return new ConvertStruct(null, $data);
        }

        $this->productType = (int) $data['detail']['kind'];
        unset($data['detail']['kind']);
        $isProductWithVariant = $data['configurator_set_id'] !== null;

        if ($this->productType === self::MAIN_PRODUCT_TYPE && $isProductWithVariant) {
            return $this->convertMainProduct($data);
        }

        if ($this->productType === self::VARIANT_PRODUCT_TYPE && $isProductWithVariant) {
            return $this->convertVariantProduct($data);
        }

        $converted = $this->getUuidForProduct($data);
        $converted = $this->getProductData($data, $converted);

        if (isset($data['categories'])) {
            $converted['categories'] = $this->getCategoryMapping($data['categories']);
        }
        unset($data['categories']);

        if (isset($data['shops'])) {
            $converted['visibilities'] = $this->getVisibilities($converted, $data['shops']);
        }
        unset($data['shops']);

        unset($data['detail']['id'], $data['detail']['articleID']);

        if (empty($data['detail'])) {
            unset($data['detail']);
        }

        $returnData = $data;
        if (empty($returnData)) {
            $returnData = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        $mainMapping = $this->mainMapping['id'] ?? null;

        return new ConvertStruct($converted, $returnData, $mainMapping);
    }

    /* ... */
}
```

As you see above, the `convert` method gets the source system data, checks with `checkForEmptyRequiredDataFields` if the necessary data fields are filled, and returns a `ConvertStruct`. The `ConvertStruct` contains the converted value in the structure of Shopware 6 and all source system data which could not be mapped to the Shopware 6 structure. If the required fields are not filled, the convert method returns a `ConvertStruct` without a `converted` value and all of the given source system data as the `unmapped` value.

Also, every `Converter` needs to implement the `getSourceIdentifier` method like the below:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

/**
 * Get the identifier of the source data, which is only known to the converter
 */
public function getSourceIdentifier(array $data): string
{
    return $data['detail']['ordernumber'];
}
```

This is the main identifier of the incoming data, and it will be used to look for already migrated data (which will be covered later in this chapter by the Deltas concept).

## Mapping [​](#mapping)

Many entities rely on other entities, so they have to be converted in a specific order. Because of this and the Shopware Migration Assistant's ability to perform multiple migrations without resetting Shopware 6, source system identifiers must be mapped to their new counterparts. Find a mapping example in the following code snippet:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

private function getUuidForProduct(array &$data): array
{
    $this->mainMapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT,
        $this->oldProductId,
        $this->context,
        $this->checksum
    );

    $converted = [];
    $converted['id'] = $this->mainMapping['entityUuid'];

    $mapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT_MAIN,
        $data['detail']['articleID'],
        $this->context,
        null,
        null,
        $converted['id']
    );
    $this->mappingIds[] = $mapping['id']; // Take a look at the performance section below for details on this.

    return $converted;
}
```

The following function employs the `getOrCreateMapping` function, which is part of the mapping service to acquire a unique identifier for the product that is about to get mapped to the source system's identifier and, at the same time, creating a new mapping entry in the `swag_migration_mapping` table. If there already is a unique identifier for the product, the `getOrCreateMapping` method, instead of creating a duplicate entry, returns the existing identifier:

php

```shiki
/* SwagMigrationAssistant/Migration/Mapping/MappingService.php */

public function getOrCreateMapping(
    string $connectionId,
    string $entityName,
    string $oldIdentifier,
    Context $context,
    ?string $checksum = null,
    ?array $additionalData = null,
    ?string $uuid = null
): array {
    $mapping = $this->getMapping($connectionId, $entityName, $oldIdentifier, $context);

    if (!isset($mapping)) {
        return $this->createMapping($connectionId, $entityName, $oldIdentifier, $checksum, $additionalData, $uuid);
    }

    if ($uuid !== null) {
        $mapping['entityUuid'] = $uuid;
        $this->saveMapping($mapping);

        return $mapping;
    }

    return $mapping;
}
```

Sometimes it is not necessary to create a new identifier, and it may be enough to only get the mapping identifier. In the following example, there is an entity with a premapping and the converter simply uses the mapping service's `getMapping` method:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/CustomerConverter.php */

protected function getDefaultPaymentMethod(array $originalData): ?string
{
    $paymentMethodMapping = $this->mappingService->getMapping(
        $this->connectionId,
        PaymentMethodReader::getMappingName(),
        $originalData['id'],
        $this->context
    );

    if ($paymentMethodMapping === null) {
        $this->loggingService->addLogEntry(new UnknownEntityLog(
            $this->runId,
            DefaultEntities::PAYMENT_METHOD,
            $originalData['id'],
            DefaultEntities::CUSTOMER,
            $this->oldCustomerId
        ));

        return null;
    }
    $this->mappingIds[] = $paymentMethodMapping['id'];

    return $paymentMethodMapping['entityUuid'];
}
```

The `getMapping` method only fetches the identifier from the database and doesn't create a new one:

php

```shiki
/* SwagMigrationAssistant/Migration/Mapping/MappingService.php */

public function getMapping(
    string $connectionId,
    string $entityName,
    string $oldIdentifier,
    Context $context
): ?array {
    if (isset($this->mappings[md5($entityName . $oldIdentifier)])) {
        return $this->mappings[md5($entityName . $oldIdentifier)];
    }

    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('connectionId', $connectionId));
    $criteria->addFilter(new EqualsFilter('entity', $entityName));
    $criteria->addFilter(new EqualsFilter('oldIdentifier', $oldIdentifier));
    $criteria->setLimit(1);

    $result =  $this->migrationMappingRepo->search($criteria, $context);

    if ($result->getTotal() > 0) {
        /** @var SwagMigrationMappingEntity $element */
        $element = $result->getEntities()->first();

        $mapping = [
            'id' => $element->getId(),
            'connectionId' => $element->getConnectionId(),
            'entity' => $element->getEntity(),
            'oldIdentifier' => $element->getOldIdentifier(),
            'entityUuid' => $element->getEntityUuid(),
            'checksum' => $element->getChecksum(),
            'additionalData' => $element->getAdditionalData(),
        ];
        $this->mappings[md5($entityName . $oldIdentifier)] = $mapping;

        return $mapping;
    }

    return null;
}
```

## Deltas [​](#deltas)

One of the parameters for the `getOrCreateMapping` Method is the `checksum`. It is used to identify unchanged data (source system data that has not been changed since the last migration). This will greatly improve the performance of future migrations.

To get this checksum, you can use the `generateChecksum` method of the base `Converter` class:

php

```shiki
/* SwagMigrationAssistant/Migration/Converter/Converter.php */

/**
 * Generates a unique checksum for the data array to recognize changes
 * on repeated migrations.
 */
protected function generateChecksum(array $data): void
{
    $this->checksum = md5(serialize($data));
}
```

This is used in the first line of the converter with the raw data that comes from the `Reader` object:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

public function convert(
    array $data,
    Context $context,
    MigrationContextInterface $migrationContext
): ConvertStruct {
    $this->generateChecksum($data);

    /* ... */

    // This is also important, so the checksum can be saved to the right mapping!
    $this->mainMapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT,
        $this->oldProductId,
        $this->context,
        $this->checksum
    );

    /* ... */

    // Important to put the mainMapping['id'] to the ConvertStruct
    $mainMapping = $this->mainMapping['id'] ?? null;
    return new ConvertStruct($converted, $returnData, $mainMapping);

    /* ... */
}
```

For the checksum to be saved to the right mapping, make sure that you set the `mainMapping` attribute of the base `Converter` class. Internally the checksum of the main mapping of an entity will be compared to the incoming data checksum and if it is the same, it will be skipped by the converter and also by the writer (you will not receive the data with the same checksum in your converter), which increases the performance of repeated migrations massively. For more information, look at the corresponding `filterDeltas` method in the `MigrationDataConverter` class. Important for the delta concept is to return the `mainMapping` with the `ConvertStruct`. This is necessary to map the converted data to the main mapping entry.

## Additional performance tips [​](#additional-performance-tips)

The `Converter` base class also contains an array named `mappingIds`. This can be filled with all mapping IDs related to the current data. Internally the related mappings will be fetched all at once in future migrations, which reduces the performance impact of `getMapping` calls (because not every call needs to query data from the database). So it is advised to add related mapping IDs in the following manner:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

private function getUnit(array $data): array
{
    $unit = [];
    $mapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::UNIT,
        $data['id'],
        $this->context
    );
    $unit['id'] = $mapping['entityUuid'];
    $this->mappingIds[] = $mapping['id']; // Store the mapping id as related mapping

    $this->getUnitTranslation($unit, $data);
    $this->convertValue($unit, 'shortCode', $data, 'unit');
    $this->convertValue($unit, 'name', $data, 'description');

    return $unit;
}
```

To save these mapping IDs in the `mainMapping`, it is necessary to call the `updateMainMapping` before returning the `ConvertStruct`:

php

```shiki
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

public function convert(
    array $data,
    Context $context,
    MigrationContextInterface $migrationContext
): ConvertStruct {
    /* ... */

    $this->updateMainMapping($this->migrationContext, $this->context);

    $mainMapping = $this->mainMapping['id'] ?? null;

    return new ConvertStruct($converted, $returnData, $mainMapping);

    /* ... */
}
```

---

## Logging

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/logging.html

# Logging [​](#logging)

Logging is essential for anyone using the Shopware Migration Assistant. In case of failure, it enables users to find out why part of their data might be missing. Most of the logging takes place in the `Converter` classes each time they detect missing required values. Also, every exception will create a log entry automatically.

We use `LogEntry` objects for our logging, so it's easier to group logs/errors of the same type and get the corresponding amount. Here is an example of how the logging works in the `CustomerConverter`:

php

```shiki
<?php declare(strict_types=1);

abstract class CustomerConverter extends ShopwareConverter
{
    /* ... */

    public function convert(
            array $data,
            Context $context,
            MigrationContextInterface $migrationContext
        ): ConvertStruct
    {
        $this->generateChecksum($data);
        $oldData = $data;
        $this->runId = $migrationContext->getRunUuid();

        $fields = $this->checkForEmptyRequiredDataFields($data, $this->requiredDataFieldKeys);

        if (!empty($fields)) {
            $this->loggingService->addLogEntry(new EmptyNecessaryFieldRunLog(
                $this->runId,
                DefaultEntities::CUSTOMER,
                $data['id'],
                implode(',', $fields)
            ));

            return new ConvertStruct(null, $oldData);
        }

        /* ... */
    }

    /* ... */
}
```

You can get the `LoggingService` from the service container. Use the `addLogEntry` method with a compatible instance of `LogEntryInterface` and save the logging later with `saveLogging`:

php

```shiki
<?php declare(strict_types=1);

interface LoggingServiceInterface
{
    public function addLogEntry(LogEntryInterface $logEntry): void;

    public function saveLogging(Context $context): void;
}
```

Look at the already existing classes, which implement the `LogEntryInterface` to find one that fits your needs, just like the `EmptyNecessaryFieldRunLog` in the `CustomerConverter` example above. All the general LogEntry classes are located under the following namespace `SwagMigrationAssistant\Migration\Logging\Log`.

To create a custom LogEntry make sure you at least implement the `LogEntryInterface` or, if your log happens during a running migration, you can also extend your LogEntry by the `BaseRunLogEntry`.

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Logging\Log;

class EmptyNecessaryFieldRunLog extends BaseRunLogEntry
{
    private string $emptyField;

    public function __construct(string $runId, string $entity, string $sourceId, string $emptyField)
    {
        parent::__construct($runId, $entity, $sourceId);
        $this->emptyField = $emptyField;
    }

    public function getCode(): string
    {
        $entity = $this->getEntity();
        if ($entity === null) {
            return 'SWAG_MIGRATION_EMPTY_NECESSARY_FIELD';
        }

        return sprintf('SWAG_MIGRATION_EMPTY_NECESSARY_FIELD_%s', mb_strtoupper($entity));
    }

    public function getLevel(): string
    {
        return self::LOG_LEVEL_WARNING;
    }

    public function getTitle(): string
    {
        $entity = $this->getEntity();
        if ($entity === null) {
            return 'The entity has one or more empty necessary fields';
        }

        return sprintf('The %s entity has one or more empty necessary fields', $entity);
    }

    public function getParameters(): array
    {
        return [
            'entity' => $this->getEntity(),
            'sourceId' => $this->getSourceId(),
            'emptyField' => $this->emptyField,
        ];
    }

    public function getDescription(): string
    {
        $args = $this->getParameters();

        return sprintf(
            'The %s entity with the source id %s does not have the necessary data for the field(s): %s',
            $args['entity'],
            $args['sourceId'],
            $args['emptyField']
        );
    }

    public function getTitleSnippet(): string
    {
        return sprintf('%s.%s.title', $this->getSnippetRoot(), 'SWAG_MIGRATION__SHOPWARE_EMPTY_NECESSARY_DATA_FIELDS');
    }

    public function getDescriptionSnippet(): string
    {
        return sprintf('%s.%s.description', $this->getSnippetRoot(), 'SWAG_MIGRATION__SHOPWARE_EMPTY_NECESSARY_DATA_FIELDS');
    }
}
```

The important part here is the `getCode` method. It should not contain any details, otherwise, grouping won't work properly. Also, keep in mind to specify the English title and description in the respective `getTitle` and `getDescription` methods. Create corresponding snippets with the same content for both the `getTitleSnippet` and `getDescriptionSnippet` methods.

The English text is used in the international log file. Instead, snippets are used all over in the Administration to inform or guide the user. Parameters for the description should be returned by the `getParameters` method so the English description and snippets can both use them.

---

## Writer

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/writer.html

# Writer [​](#writer)

The `Writer` objects will get the converted data from the `swag_migration_data` table and write it to the right Shopware 6 table. Each `Writer` supports only one entity, which is most likely the target table.

When creating a writer, register it in a manner resembling the following:

html

```shiki
<service id="SwagMigrationAssistant\Migration\Writer\ProductWriter"
         parent="SwagMigrationAssistant\Migration\Writer\AbstractWriter">
    <argument type="service" id="Shopware\Core\Framework\DataAbstractionLayer\Write\EntityWriter"/>
    <argument type="service" id="Shopware\Core\Content\Product\ProductDefinition"/>
    <tag name="shopware.migration.writer"/>
</service>
```

In most cases, you should extend by the `AbstractWriter`, which does most things. You only need to specify the `supports` method.

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Writer;

use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;

class ProductWriter extends AbstractWriter
{
    public function supports(): string
    {
        return DefaultEntities::PRODUCT;
    }
}
```

If you need more control over the writing, you can implement the `WriterInterface` by yourself and the class will receive the data in the `writeData` method. Received data is an array of converted values. The amount depends on the limit of the request. Error handling is already done in the overlying `MigrationDataWriter` class. If writing the entries fails with a `WriteException` from the DAL, it will try to exclude the reported failures and try again. If any other exception occurs, it will retry them one by one to minimize data loss.

---

## Media Processing

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/concept/media-processing.html

# Media Processing [​](#media-processing)

Two steps are necessary to import files to Shopware 6 using the migration. First // todo10 , create a media file object (`MediaDefinition` / `media` table, for more details, take a look at the `MediaConverter`) and create an entry in the `SwagMigrationMediaFileDefinition` / `swag_migration_media_file` table.

Every entry in the `swag_migration_media_file` table of the associated migration run will get processed by an implementation of `MediaFileProcessorInterface`. For the `api` gateway, the `HttpMediaDownloadService` is used and will download the files via HTTP.

To add a file to the table, you can do something like this in your `Converter` class (this example is from the `MediaConverter`):

php

```shiki
<?php declare(strict_types=1);

abstract class MediaConverter extends ShopwareConverter
{
    /* ... */

    public function convert(
        array $data,
        Context $context,
        MigrationContextInterface $migrationContext
    ): ConvertStruct {
        $this->generateChecksum($data);
        $this->context = $context;
        $this->locale = $data['_locale'];
        unset($data['_locale']);

        $connection = $migrationContext->getConnection();
        $this->connectionId = '';
        if ($connection !== null) {
            $this->connectionId = $connection->getId();
        }

        $converted = [];
        $this->mainMapping = $this->mappingService->getOrCreateMapping(
            $this->connectionId,
            DefaultEntities::MEDIA,
            $data['id'],
            $context,
            $this->checksum
        );
        $converted['id'] = $this->mainMapping['entityUuid'];

        if (!isset($data['name'])) {
            $data['name'] = $converted['id'];
        }

        $this->mediaFileService->saveMediaFile(
            [
                'runId' => $migrationContext->getRunUuid(),
                'entity' => MediaDataSet::getEntity(), // important to distinguish between private and public files
                'uri' => $data['uri'] ?? $data['path'],
                'fileName' => $data['name'], // uri or path to the file (because of the different implementations of the gateways)
                'fileSize' => (int) $data['file_size'],
                'mediaId' => $converted['id'], // uuid of the media object in Shopware 6
            ]
        );
        unset($data['uri'], $data['file_size']);

        $this->getMediaTranslation($converted, $data);
        $this->convertValue($converted, 'title', $data, 'name');
        $this->convertValue($converted, 'alt', $data, 'description');

        $albumMapping = $this->mappingService->getMapping(
            $this->connectionId,
            DefaultEntities::MEDIA_FOLDER,
            $data['albumID'],
            $this->context
        );

        if ($albumMapping !== null) {
            $converted['mediaFolderId'] = $albumMapping['entityUuid'];
            $this->mappingIds[] = $albumMapping['id'];
        }

        unset(
            $data['id'],
            $data['albumID'],

            // Legacy data that don't need mapping or there is no equivalent field
            $data['path'],
            $data['type'],
            $data['extension'],
            $data['file_size'],
            $data['width'],
            $data['height'],
            $data['userID'],
            $data['created']
        );

        $returnData = $data;
        if (empty($returnData)) {
            $returnData = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        // The MediaWriter will write this Shopware 6 media object
        return new ConvertStruct($converted, $returnData, $this->mainMapping['id']);
    }

    /* ... */
}
```

`swag_migration_media_files` are processed by the right processor service. This service is different for documents and normal media, but it still is gateway dependent. For example, the `HttpMediaDownloadService` works like this:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware55\Media;

/* ... */

class HttpMediaDownloadService implements MediaFileProcessorInterface
{
    /* ... */

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareApiGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === MediaDataSet::getEntity();
    }

    public function process(MigrationContextInterface $migrationContext, Context $context, array $workload, int $fileChunkByteSize): array
    {
        /* ... */

        //Fetch media from the database
        $media = $this->getMediaFiles($mediaIds, $runId, $context);

        $client = new Client([
            'verify' => false,
        ]);

        //Do download requests and store the promises
        $promises = $this->doMediaDownloadRequests($media, $mappedWorkload, $client);

        // Wait for the requests to complete, even if some of them fail
        /** @var array $results */
        $results = Promise\settle($promises)->wait();

        /* ... handle responses ... */

        $this->setProcessedFlag($runId, $context, $finishedUuids, $failureUuids);
        $this->loggingService->saveLogging($context);

        return array_values($mappedWorkload);
    }
}
```

First, the service fetches all media files associated with the given media IDs and downloads these media files from the source system. After this, it handles the response, saves the media files in a temporary folder and copies them to Shopware 6 filesystem. In the end, the service sets a `processed` status to these media files, saves all warnings that may have occurred and returns the status of the processed files.

---

## Guides

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/guides/

# Guides [​](#guides)

This section guides you on how to migrate from different environments by using a Migration Assistant converter, migration profile, or migration connector.

---

## Extending a Shopware migration profile

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/guides/extending-a-shopware-migration-profile.html

# Extending a Shopware Migration Profile [​](#extending-a-shopware-migration-profile)

## Overview [​](#overview)

In this guide, you will see an example of how you can extend a Shopware migration profile of the [Shopware Migration Assistant](https://store.shopware.com/de/swag257162657297f/migrations-assistent.html). For this example, the Shopware 5 [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) plugin is migrated to the Shopware 6. For simplicity, only the local gateway is implemented.

## Setup [​](#setup)

It is required to have a basic plugin running. You must have installed the [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) plugin in Shopware 5, an own [Plugin](./../../../../guides/plugins/plugins/plugin-base-guide.html#create-your-first-plugin) and [Shopware Migration Assistant](https://store.shopware.com/de/swag257162657297f/migrations-assistent.html) in Shopware 6.

## Enrich existing plugin with migration features [​](#enrich-existing-plugin-with-migration-features)

Instead of creating a new plugin for the migration, you might want to add migration features to your existing plugin. Of course, your plugin should then also be installable without the Migration Assistant plugin. So we have an optional requirement. Have a look at this [section of the guide](./../../../../guides/plugins/plugins/plugin-fundamentals/database-migrations.html) on how to inject the needed migration services only if the Migration Assistant plugin is available. You could also have a look at the example plugin to see how the conditional loading is managed in the plugin base class.

## Creating a new dataSet [​](#creating-a-new-dataset)

First of all, you need to create a new `DataSet` for your bundle entity:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet;

use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class BundleDataSet extends DataSet
{
    public static function getEntity(): string
    {
        return 'swag_bundle'; // Identifier of this entity
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        // This way we support all Shopware profile versions
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getSnippet(): string
    {
        return 'swag-migration.index.selectDataCard.entities.' . static::getEntity();
    }
}
```

The bundle entities must be migrated after the products, because of which you have to extend the `ProductDataSelection` as follows:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet;

class ProductDataSelection implements DataSelectionInterface
{
    private DataSelectionInterface $originalDataSelection;

    public function __construct(DataSelectionInterface $originalDataSelection)
    {
        $this->originalDataSelection = $originalDataSelection;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $this->originalDataSelection->supports($migrationContext);
    }

    public function getData(): DataSelectionStruct
    {
        $dataSelection = $this->originalDataSelection->getData();

        // Add the modified DataSet array to a new DataSelectionStruct
        return new DataSelectionStruct(
            $dataSelection->getId(),
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            $dataSelection->getSnippet(),
            $dataSelection->getPosition(),
            $dataSelection->getProcessMediaFiles(),
            DataSelectionStruct::PLUGIN_DATA_TYPE
        );
    }

    public function getDataSets(): array
    {
        $entities = $this->originalDataSelection->getDataSets();
        $entities[] = new BundleDataSet(); // Add the BundleDataSet to the DataSet array

        return $entities;
    }

    public function getDataSetsRequiredForCount(): array
    {
        return $this->originalDataSelection->getDataSetsRequiredForCount();
    }
}
```

To insert the bundle entity to this `DataSelection`, you have to add this entity to the entities array of the returning `DataSelectionStruct` of the `getData` function.

Both classes have to be registered in the `migration_assistant_extension.xml`:

html

```shiki
<service id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\ProductDataSelection"
         decorates="SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection">
    <argument type="service" id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\ProductDataSelection.inner"/>
</service>

<service id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet">
    <tag name="shopware.migration.data_set"/>
</service>
```

All `DataSets` have to be tagged with `shopware.migration.data_set`. The `DataSetRegistry` fetches all these classes and searches for the correct `DataSet` with the `supports` method.

## Adding entity count snippets [​](#adding-entity-count-snippets)

If you check your current progress in the data selection table of Shopware Migration Assistant in the Administration, you can see that the bundle entities are automatically counted, but the description of the entity count is currently not loaded. To get a correct description of the new entity count, you have to add new snippets for this.

First of all, you create a new snippet file, e.g., `en-GB.json`:

json

```shiki
{
    "swag-migration": {
        "index": {
            "selectDataCard": {
                "entities": {
                    "swag_bundle": "Bundles:"
                }
            }
        }
    }
}
```

All count entity descriptions are located in the `swag-migration.index.selectDataCard.entities` namespace by default, so you have to create a new entry with the entity name of the new bundle entity or you could change the snippet in the `getSnippet` function of the `DataSet`.

At last, you have to create the `main.js` in the `Resources/app/administration` directory like this:

javascript

```shiki
import enGBSnippets from './snippet/en-GB.json';

const { Application } = Shopware;

Application.addInitializerDecorator('locale', (localeFactory) => {
    localeFactory.extend('en-GB', enGBSnippets);

    return localeFactory;
});
```

As you see in the code above, you register your snippet file for the `en-GB` locale. Now the count entity description should display in the Administration correctly.

## Creating a local reader [​](#creating-a-local-reader)

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Gateway\Local\Reader;

use Doctrine\DBAL\Connection;
use Doctrine\DBAL\Driver\ResultStatement;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\TotalStruct;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ShopwareLocalGateway;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class LocalBundleReader extends AbstractReader
{
    public function supportsTotal(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareLocalGateway::GATEWAY_NAME;
    }

    public function readTotal(MigrationContextInterface $migrationContext): ?TotalStruct
    {
        $this->setConnection($migrationContext);

        $query = $this->connection->createQueryBuilder()
            ->select('COUNT(*)')
            ->from('s_bundles')
            ->execute();

        $total = 0;
        if ($query instanceof ResultStatement) {
            $total = (int) $query->fetchColumn();
        }

        return new TotalStruct(BundleDataSet::getEntity(), $total);
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        // Make sure that this reader is only called for the BundleDataSet entity
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareLocalGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === BundleDataSet::getEntity();
    }

    /**
     * Read all bundles with associated product data
     */
    public function read(MigrationContextInterface $migrationContext, array $params = []): array
    {
        $this->setConnection($migrationContext);

        // Fetch the ids of the given table with the given offset and limit
        $ids = $this->fetchIdentifiers('s_bundles', $migrationContext->getOffset(), $migrationContext->getLimit());

        // Strip the table prefix 'bundles' out of the bundles array 
        $bundles = $this->mapData($this->fetchBundles($ids), [], ['bundles']);
        $bundleProducts = $this->fetchBundleProducts($ids);

        foreach ($bundles as &$bundle) {
            if (isset($bundleProducts[$bundle['id']])) {
                $bundle['products'] = $bundleProducts[$bundle['id']];
            }
        }

        return $bundles;
    }

    /**
     * Fetch all bundles by given ids
     */
    private function fetchBundles(array $ids): array
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundles', 'bundles');
        $this->addTableSelection($query, 's_bundles', 'bundles');

        $query->where('bundles.id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_STR_ARRAY);

        $query->addOrderBy('bundles.id');

        return $query->execute()->fetchAll();
    }

    /**
     * Fetch all bundle products by bundle ids
     */
    private function fetchBundleProducts(array $ids): array
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundle_products', 'bundleProducts');
        $this->addTableSelection($query, 's_bundle_products', 'bundleProducts');

        $query->where('bundleProducts.bundle_id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_INT_ARRAY);

        return $query->execute()->fetchAll(\PDO::FETCH_GROUP | \PDO::FETCH_COLUMN);
    }
}
```

In this local reader, you fetch all bundles with associated products and return this in the `read` method. Like the `DataSelection` and `DataSet`, you must register the local reader and tag it with `shopware.migration.reader` in your `migration_assistant_extension.xml`. Also, you have to set the parent property of your local reader to `AbstractReader` to inherit from this class:

html

```shiki
<service id="SwagMigrationBundleExample\Profile\Shopware\Gateway\Local\Reader\LocalBundleReader"
         parent="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader">
    <tag name="shopware.migration.reader"/>
</service>
```

## Creating a converter [​](#creating-a-converter)

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Converter;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\Converter\ConvertStruct;
use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\Converter\ShopwareConverter;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class BundleConverter extends ShopwareConverter
{
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        // Take care that you specify the supports function the same way that you have in your reader
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getDataSet()::getEntity() === BundleDataSet::getEntity();
    }

    public function getSourceIdentifier(array $data): string
    {
        return $data['id'];
    }

    public function convert(array $data, Context $context, MigrationContextInterface $migrationContext): ConvertStruct
    {
        // Generate a checksum for the data to allow faster migrations in the future
        $this->generateChecksum($data);

        // Get uuid for bundle entity out of mapping table or create a new one
        $this->mainMapping = $this->mappingService->getOrCreateMapping(
            $migrationContext->getConnection()->getId(),
            BundleDataSet::getEntity(),
            $data['id'],
            $context,
            $this->checksum
        );
        $converted['id'] = $this->mainMapping['entityUuid'];

        // This method checks if key is available in data array and set value in converted array
        $this->convertValue($converted, 'name', $data, 'name');

        // Set default values for required fields, because these data do not exists in SW5
        $converted['discountType'] = 'absolute';
        $converted['discount'] = 0;

        if (isset($data['products'])) {
            $products = $this->getProducts($context, $migrationContext, $data);

            if (!empty($products)) {
                $converted['products'] = $products;
            }
        }

        // Unset used data keys
        unset(
            // Used
            $data['id'],
            $data['name'],
            $data['products']
        );

        if (empty($data)) {
            $data = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        return new ConvertStruct($converted, $data, $this->mainMapping['id']);
    }

    /** 
     * Get converted products 
    */
    private function getProducts(Context $context, MigrationContextInterface $migrationContext, array $data): array
    {
        $connectionId = $migrationContext->getConnection()->getId();
        $products = [];
        foreach ($data['products'] as $product) {
            // Get associated uuid of product out of mapping table
            $mapping = $this->mappingService->getMapping(
                $connectionId,
                DefaultEntities::PRODUCT . '_mainProduct',
                $product,
                $context
            );

            // Log missing association of product
            if ($mapping === null) {
                continue;
            }

            $productUuid = $mapping['entityUuid'];
            $newProduct['id'] = $productUuid;
            $products[] = $newProduct;
        }

        return $products;
    }

    /** 
     * Called to write the created mapping to the mapping table
    */
    public function writeMapping(Context $context): void
    {
        $this->mappingService->writeMapping($context);
    }
}
```

The converter is the main logic of the migration and converts old Shopware 5 data to new Shopware 6 data structure. If you don't know what the Shopware 6 data structure of your entity looks like, you have to look for the entity definition:

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BundleExample\Core\Content\Bundle;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FloatField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ManyToManyAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\TranslatedField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\TranslationsAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Swag\BundleExample\Core\Content\Bundle\Aggregate\BundleProduct\BundleProductDefinition;
use Swag\BundleExample\Core\Content\Bundle\Aggregate\BundleTranslation\BundleTranslationDefinition;

class BundleDefinition extends EntityDefinition
{
    public function getEntityName(): string
    {
        return 'swag_bundle';
    }

    public function getEntityClass(): string
    {
        return BundleEntity::class;
    }

    public function getCollectionClass(): string
    {
        return BundleCollection::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            new TranslatedField('name'),
            (new StringField('discount_type', 'discountType'))->addFlags(new Required()),
            (new FloatField('discount', 'discount'))->addFlags(new Required()),
            new TranslationsAssociationField(BundleTranslationDefinition::class, 'swag_bundle_id'),
            new ManyToManyAssociationField('products', ProductDefinition::class, BundleProductDefinition::class, 'bundle_id', 'product_id'),
        ]);
    }
}
```

In the `BundleDefinition`, you can see which fields the entity has and which are required. (Hint: Always use the property name of the field.) At the end of this step, you have to register your new converter in the `migration_assistant_extension.xml` and tag it with `shopware.migration.converter`:

html

```shiki
<service id="SwagMigrationBundleExample\Profile\Shopware\Converter\BundleConverter">
    <argument type="service" id="SwagMigrationAssistant\Migration\Mapping\MappingService"/>
    <argument type="service" id="SwagMigrationAssistant\Migration\Logging\LoggingService"/>
    <tag name="shopware.migration.converter"/>
</service>
```

For more general information on converter, mapping, and deltas concept, refer to [Converter and Mapping](./../concept/convert-and-mapping.html) section of the guide.

## Adding a writer [​](#adding-a-writer)

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Migration\Writer;

use SwagMigrationAssistant\Migration\Writer\AbstractWriter;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class BundleWriter extends AbstractWriter
{
    public function supports(): string
    {
        return BundleDataSet::getEntity();
    }
}
```

html

```shiki
<service id="SwagMigrationBundleExample\Migration\Writer\BundleWriter"
         parent="SwagMigrationAssistant\Migration\Writer\AbstractWriter">
    <argument type="service" id="Shopware\Core\Framework\DataAbstractionLayer\Write\EntityWriter"/>
    <argument type="service" id="Swag\BundleExample\Core\Content\Bundle\BundleDefinition"/>
    <tag name="shopware.migration.writer"/>
</service>
```

You only need to implement the `supports` method and specify the right `Definition` in `migration_assistant_extension.xml`. The logic to write the data is defined in the `AbstractWriter` class and should almost always be the same. Look at [writer concept](./../concept/writer.html) for more information.

With that have implemented your first plugin migration. Install your plugin, clear the cache and build the Administration again to see the migration of your bundle entities.

## Source [​](#source)

Check out this [GitHub repository](https://github.com/shopwareArchive/swag-docs-extending-shopware-migration-profile) containing a full example source.

---

## Extending the Migration Connector

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/guides/extending-the-migration-connector.html

# Extending the Migration Connector [​](#extending-the-migration-connector)

In this guide, you will see an example of how you can extend the [Migration connector](https://github.com/shopware/SwagMigrationConnector) plugin to migrate the Shopware 5 [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) to a Shopware 6 plugin via API.

## Setup [​](#setup)

It is required to have a basic Shopware 5 plugin running. You must have installed the [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle), the [Migration connector](https://github.com/shopware/SwagMigrationConnector) plugin in Shopware 5, and an own Shopware 6 [Plugin](./../../../../guides/plugins/plugins/plugin-base-guide.html#create-your-first-plugin), the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) and the [SwagMigrationBundleExample](./extending-a-shopware-migration-profile.html) plugin in Shopware 6. If you want to know how all plugins work together, please look at the [Extending a Shopware Migration Profile](./extending-a-shopware-migration-profile.html) guide.

With this setup, you have the bundle plugin in Shopware 5 and also the bundle plugin in Shopware 6. So you can migrate your Shopware 5 shop to Shopware 6 via local and API gateway, but your bundle data only via a local gateway.

## Creating bundle repository [​](#creating-bundle-repository)

To fetch your data via the Shopware 5 API, you have to create a bundle repository first:

php

```shiki
<?php

namespace SwagMigrationBundleApiExample\Repository;

use Doctrine\DBAL\Connection;
use SwagMigrationConnector\Repository\AbstractRepository;

class BundleRepository extends AbstractRepository
{
    /**
     * Fetch bundles using offset and limit
     *
     * @param int $offset
     * @param int $limit
     *
     * @return array
     */
    public function fetch($offset = 0, $limit = 250)
    {
        $ids = $this->fetchIdentifiers('s_bundles', $offset, $limit);

        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundles', 'bundles');
        $this->addTableSelection($query, 's_bundles', 'bundles');

        $query->where('bundles.id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_STR_ARRAY);

        $query->addOrderBy('bundles.id');

        return $query->execute()->fetchAll();
    }

    /**
     * Fetch all bundle products by bundle ids
     *
     * @param array $ids
     *
     * @return array
     */
    public function fetchBundleProducts(array $ids)
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundle_products', 'bundleProducts');
        $this->addTableSelection($query, 's_bundle_products', 'bundleProducts');

        $query->where('bundleProducts.bundle_id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_INT_ARRAY);

        return $query->execute()->fetchAll(\PDO::FETCH_GROUP | \PDO::FETCH_COLUMN);
    }
}
```

The repository has to inherit from the `AbstractRepository` of the Migration Connector. This provides helper functions like `addTableSelection`, which sets a prefix to all table columns and adds these to the query builder.

You have to register the repository in your `service.xml` with the parent property like this:

html

```shiki
<service id="swag_migration_bundle_api_example.bundle_repository"
         class="SwagMigrationBundleApiExample\Repository\BundleRepository"
         parent="SwagMigrationConnector\Repository\AbstractRepository"
         />
```

## Creating bundle service [​](#creating-bundle-service)

In the next step, you create a new `BundleService`, which uses your new `BundleRepository` to fetch all bundles and products to map them to one result array:

php

```shiki
<?php
/**
 * (c) shopware AG <info@shopware.com>
 * For the full copyright and license information, please view the LICENSE
 * File that was distributed with this source code.
 */

namespace SwagMigrationBundleApiExample\Service;

use SwagMigrationBundleApiExample\Repository\BundleRepository;
use SwagMigrationConnector\Repository\ApiRepositoryInterface;
use SwagMigrationConnector\Service\AbstractApiService;

class BundleService extends AbstractApiService
{
    private BundleRepository $bundleRepository;

    /**
     * @param ApiRepositoryInterface $bundleRepository
     */
    public function __construct(ApiRepositoryInterface $bundleRepository)
    {
        $this->bundleRepository = $bundleRepository;
    }

    /**
     * @param int $offset
     * @param int $limit
     *
     * @return array
     */
    public function getBundles($offset = 0, $limit = 250)
    {
        $bundles = $this->bundleRepository->fetch($offset, $limit);
        $ids = array_column($bundles, 'bundles.id');
        $bundleProducts = $this->bundleRepository->fetchBundleProducts($ids);

        // Strip the table prefix 'bundles' out of the bundles array
        $bundles = $this->mapData($bundles, [], ['bundles']);

        foreach ($bundles as &$bundle) {
            if (isset($bundleProducts[$bundle['id']])) {
                $bundle['products'] = $bundleProducts[$bundle['id']];
            }
        }

        return $this->cleanupResultSet($bundles);
    }
}
```

You have to register the `BundleService` in your `service.xml`:

html

```shiki
<service class="SwagMigrationBundleApiExample\Service\BundleService" id="swag_migration_bundle_api_example.bundle_service">
    <argument type="service" id="swag_migration_bundle_api_example.bundle_repository"/>
</service>
```

## Create a new API controller [​](#create-a-new-api-controller)

At last, you have to create a new API controller, which uses the `BundleService` to get your bundle data:

php

```shiki
<?php
/**
 * (c) shopware AG <info@shopware.com>
 * For the full copyright and license information, please view the LICENSE
 * File that was distributed with this source code
 */

use SwagMigrationBundleApiExample\Service\BundleService;
use SwagMigrationConnector\Service\ControllerReturnStruct;

class Shopware_Controllers_Api_SwagMigrationBundles extends Shopware_Controllers_Api_Rest
{
    public function indexAction()
    {
        $offset = (int) $this->Request()->getParam('offset', 0);
        $limit = (int) $this->Request()->getParam('limit', 250);

        /** @var BundleService $bundleService */
        $bundleService = $this->container->get('swag_migration_bundle_api_example.bundle_service');

        $bundles = $bundleService->getBundles($offset, $limit);
        $response = new ControllerReturnStruct($bundles, empty($bundles));

        $this->view->assign($response->jsonSerialize());
    }
}
```

Now you have to create the `BundleReader` in the [SwagMigrationBundleExample](./extending-a-shopware-migration-profile.html) plugin, which only contains the Shopware 5 API route:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Gateway\Api\Reader;

use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\ApiReader;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Api\ShopwareApiGateway;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class BundleReader extends ApiReader
{
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareApiGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === BundleDataSet::getEntity();
    }

    protected function getApiRoute(): string
    {
        return 'SwagMigrationBundles'; // This defines which API route should called
    }
}
```

After this, you have to register the reader in the Symfony container:

html

```shiki
<service id="SwagMigrationBundleExample\Profile\Shopware\Gateway\Api\BundleReader"
         parent="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\ApiReader">
    <tag name="shopware.migration.reader"/>
</service>
```

With that, you have implemented your first plugin migration via API.

## Source [​](#source)

Check out this [GitHub repository](https://github.com/shopwareArchive/swag-docs-extending-shopware-migration-connector) containing a full example source.

---

## Decorating a Shopware Migration Assistant converter

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/guides/decorating-a-shopware-migration-assistant-converter.html

# Decorating a Shopware Migration Assistant Converter [​](#decorating-a-shopware-migration-assistant-converter)

## Overview [​](#overview)

In this guide, you will learn how to decorate a Shopware migration converter of the [Migration Connector](https://github.com/shopware/SwagMigrationConnector) plugin. Here, the decorated converter will modify the converted products and get data out of a `premapping field`.

## Setup [​](#setup)

It is required to have installed the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) plugin in Shopware 6 and have a running Shopware 5 system running to connect the Migration Assistant via API or local gateway.

## Enrich existing plugin with migration features [​](#enrich-existing-plugin-with-migration-features)

Instead of creating a new plugin for the migration, you might want to add migration features to your existing plugin. Of course, your plugin should then also be installable without the Migration Assistant plugin. So we have an optional requirement. Have a look at this [PLACEHOLDER-LINK: Optional requirements of a plugin] on how to inject the needed migration services only if the Migration Assistant plugin is available. You could also have a look at the example plugin to see how the conditional loading is managed in the plugin base class.

## Creating a premapping reader [​](#creating-a-premapping-reader)

In this example, the user should be able to map the manufacturer while no new manufacturer will be created. You have to create a new premapping reader to achieve this:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationExtendConverterExample\Profile\Shopware\Premapping;

use Shopware\Core\Content\Product\Aggregate\ProductManufacturer\ProductManufacturerEntity;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Sorting\FieldSorting;
use SwagMigrationAssistant\Migration\Gateway\GatewayRegistryInterface;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\Premapping\AbstractPremappingReader;
use SwagMigrationAssistant\Migration\Premapping\PremappingChoiceStruct;
use SwagMigrationAssistant\Migration\Premapping\PremappingEntityStruct;
use SwagMigrationAssistant\Migration\Premapping\PremappingStruct;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection;
use SwagMigrationAssistant\Profile\Shopware\Gateway\ShopwareGatewayInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ManufacturerReader extends AbstractPremappingReader
{
    private const MAPPING_NAME = 'swag_manufacturer';

    private EntityRepository $manufacturerRepo;

    private GatewayRegistryInterface $gatewayRegistry;

    private array $preselectionDictionary;

    private array $preselectionSourceNameDictionary;

    public function __construct(
        EntityRepository $manufacturerRepo,
        GatewayRegistryInterface $gatewayRegistry
    ) {
        $this->manufacturerRepo = $manufacturerRepo;
        $this->gatewayRegistry = $gatewayRegistry;
    }

    public static function getMappingName(): string
    {
        return self::MAPPING_NAME;
    }

    /**
     * Checks whether or not the current profile and DataSelection is supported
     */
    public function supports(MigrationContextInterface $migrationContext, array $entityGroupNames): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && in_array(ProductDataSelection::IDENTIFIER, $entityGroupNames, true);
    }

    public function getPremapping(Context $context, MigrationContextInterface $migrationContext): PremappingStruct
    {
        $this->fillConnectionPremappingDictionary($migrationContext);
        $mapping = $this->getMapping($migrationContext);
        $choices = $this->getChoices($context);
        $this->setPreselection($mapping);

        return new PremappingStruct(self::getMappingName(), $mapping, $choices);
    }

    /**
     * Reads all manufacturers of the source system, looks into connectionPremappingDictionary if a premapping
     * is currently set and returns the filled mapping array
     *
     * @return PremappingEntityStruct[]
     */
    private function getMapping(MigrationContextInterface $migrationContext): array
    {
        /** @var ShopwareGatewayInterface $gateway */
        $gateway = $this->gatewayRegistry->getGateway($migrationContext);

        $preMappingData = $gateway->readTable($migrationContext, 's_articles_supplier');

        $entityData = [];
        foreach ($preMappingData as $data) {
            $this->preselectionSourceNameDictionary[$data['id']] = $data['name'];

            $uuid = '';
            if (isset($this->connectionPremappingDictionary[$data['id']])) {
                $uuid = $this->connectionPremappingDictionary[$data['id']]['destinationUuid'];
            }

            $entityData[] = new PremappingEntityStruct($data['id'], $data['name'], $uuid);
        }

        return $entityData;
    }

    /**
     * Returns all choices of the manufacturer repository
     *
     * @return PremappingChoiceStruct[]
     */
    private function getChoices(Context $context): array
    {
        $criteria = new Criteria();
        $criteria->addSorting(new FieldSorting('name'));

        /** @var ProductManufacturerEntity[] $manufacturers */
        $manufacturers = $this->manufacturerRepo->search($criteria, $context);

        $choices = [];
        foreach ($manufacturers as $manufacturer) {
            $this->preselectionDictionary[$manufacturer->getName()] = $manufacturer->getId();
            $choices[] = new PremappingChoiceStruct($manufacturer->getId(), $manufacturer->getName());
        }

        return $choices;
    }

    /**
     * Loops through mapping and sets preselection, if uuid is currently not set
     *
     * @param PremappingEntityStruct[] $mapping
     */
    private function setPreselection(array $mapping): void
    {
        foreach ($mapping as $item) {
            if (!isset($this->preselectionSourceNameDictionary[$item->getSourceId()]) || $item->getDestinationUuid() !== '') {
                continue;
            }

            $sourceName = $this->preselectionSourceNameDictionary[$item->getSourceId()];
            $preselectionValue = $this->getPreselectionValue($sourceName);

            if ($preselectionValue !== null) {
                $item->setDestinationUuid($preselectionValue);
            }
        }
    }

    /**
     * Only a simple example on how to implement a preselection
     */
    private function getPreselectionValue(string $sourceName): ?string
    {
        $preselectionValue = null;
        $validPreselection = 'Shopware';
        $choice = 'shopware AG';

        if ($sourceName === $validPreselection && isset($this->preselectionDictionary[$choice])) {
            $preselectionValue = $this->preselectionDictionary[$choice];
        }

        return $preselectionValue;
    }
}
```

The created premapping reader fetches all manufacturers of the source system, gets all manufacturer choices out of the Shopware 6 database, and does a simple preselection via the manufacturer name. The `getPremapping` function returns the whole premapping structure. With this structure, the Administration creates a new premapping card and creates for each source system manufacturer a selectbox with all Shopware 6 manufacturers as choices. For more details, have a look at the [Premapping concept](./../concept/premapping.html).

## Adding snippets to premapping card [​](#adding-snippets-to-premapping-card)

Currently, the premapping card has no snippets at all, so you have to create a new snippet file for the title:

json

```shiki
{
     "swag-migration": {
         "index": {
             "premappingCard": {
                 "group": {
                     "swag_manufacturer": "Manufacturer"
                 }
             }
         }
     }
 }
```

This file has to be located in `Resources\administration\snippet` and registered in `Resources\administration\main.js` of the plugin like this:

javascript

```shiki
import enGBSnippets from './snippet/en-GB.json';

const { Application } = Shopware;

Application.addInitializerDecorator('locale', (localeFactory) => {
    localeFactory.extend('en-GB', enGBSnippets);

     return localeFactory;
});
```

Now your new premapping card has a correct title.

## Decorate the product migration converter [​](#decorate-the-product-migration-converter)

After creating your premapping reader, you have a new premapping card, but this premapping is currently not in use. To map the product manufacturers of the source system to your premapping values, you have to decorate one of the Shopware product migration converters. In this example, only the `Shopware55ProductConverter` is decorated, but if you want to decorate all Shopware migration converters, you have to do the same:

php

```shiki
 <?php declare(strict_types=1);

 namespace SwagMigrationExtendConverterExample\Profile\Shopware\Converter;

 use Shopware\Core\Framework\Context;
 use SwagMigrationAssistant\Migration\Converter\ConverterInterface;
 use SwagMigrationAssistant\Migration\Converter\ConvertStruct;
 use SwagMigrationAssistant\Migration\Logging\LoggingServiceInterface;
 use SwagMigrationAssistant\Migration\Mapping\MappingServiceInterface;
 use SwagMigrationAssistant\Migration\Media\MediaFileServiceInterface;
 use SwagMigrationAssistant\Migration\MigrationContextInterface;
 use SwagMigrationAssistant\Profile\Shopware\Converter\ProductConverter;
 use SwagMigrationExtendConverterExample\Profile\Shopware\Premapping\ManufacturerReader;

 class Shopware55DecoratedProductConverter extends ProductConverter
 {
     private ConverterInterface $originalProductConverter;

     public function __construct(
         ConverterInterface $originalProductConverter,
         MappingServiceInterface $mappingService,
         LoggingServiceInterface $loggingService,
         MediaFileServiceInterface $mediaFileService
     ) {
         parent::__construct($mappingService, $loggingService, $mediaFileService);
         $this->originalProductConverter = $originalProductConverter;
     }

     public function supports(MigrationContextInterface $migrationContext): bool
     {
         return $this->originalProductConverter->supports($migrationContext);
     }

     public function getSourceIdentifier(array $data): string
     {
         return $this->originalProductConverter->getSourceIdentifier($data);
     }

     public function getMediaUuids(array $converted): ?array
     {
         return $this->originalProductConverter->getMediaUuids($converted);
     }

     public function writeMapping(Context $context): void
     {
         $this->originalProductConverter->writeMapping($context);
     }

     public function convert(
         array $data,
         Context $context,
         MigrationContextInterface $migrationContext
     ): ConvertStruct
     {
         if (!isset($data['manufacturer']['id'])) {
             return $this->originalProductConverter->convert($data, $context, $migrationContext);
         }

         $manufacturerId = $data['manufacturer']['id'];
         unset($data['manufacturer']);

         $mapping = $this->mappingService->getMapping(
             $migrationContext->getConnection()->getId(),
             ManufacturerReader::getMappingName(),
             $manufacturerId,
             $context
         );

         $convertedStruct = $this->originalProductConverter->convert($data, $context, $migrationContext);

         if ($mapping === null) {
             return $convertedStruct;
         }

         $converted = $convertedStruct->getConverted();
         $converted['manufacturerId'] = $mapping['entityUuid'];

         return new ConvertStruct($converted, $convertedStruct->getUnmapped(), $convertedStruct->getMappingUuid());
     }
 }
```

Your new decorated product migration converter checks if a manufacturer is set and searches for the premapping via the `MappingService`. If a premapping is found, the migration converter uses the converted value of the original converter, adds the manufacturer uuid, and returns the new `ConvertStruct`.

In the end, you have to register your decorated converter in your `services.xml`:

html

```shiki
<service id="SwagMigrationExtendConverterExample\Profile\Shopware\Converter\Shopware55DecoratedProductConverter"
          decorates="SwagMigrationAssistant\Profile\Shopware55\Converter\Shopware55ProductConverter">
    <argument type="service" id="SwagMigrationExtendConverterExample\Profile\Shopware\Converter\Shopware55DecoratedProductConverter.inner"/>
    <argument type="service" id="SwagMigrationAssistant\Migration\Mapping\MappingService"/>
    <argument type="service" id="SwagMigrationAssistant\Migration\Logging\LoggingService"/>
    <argument type="service" id="SwagMigrationAssistant\Migration\Media\MediaFileService"/>
</service>
```

With this, you have decorated your first Shopware migration converter.

## Source [​](#source)

Check out this [GitHub repository](https://github.com/shopwareArchive/swag-docs-decorate-shopware-migration-converter) containing a full example source.

---

## Creating a new migration profile

**Source:** https://developer.shopware.com/docs/products/extensions/migration-assistant/guides/creating-a-new-migration-profile.html

# Creating a New Migration Profile [​](#creating-a-new-migration-profile)

If you want to migrate your data from a different source system than Shopware, create a new migration profile for the Migration Assistant. But if you want to convert your plugin data from a Shopware system to Shopware 6, look at this article on [Extending a Shopware Migration Profile](./extending-a-shopware-migration-profile.html).

## Setup [​](#setup)

First, it is required that you already have installed the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) plugin in Shopware 6 and have created a demo source system database with a `product` table. To create the table, use this SQL statement:

sql

```shiki
CREATE TABLE product
(
  id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  product_number varchar(255) NOT NULL,
  price float NOT NULL,
  stock int NOT NULL,
  product_name varchar(255) NOT NULL,
  tax float NOT NULL
);
```

This table should simulate a simple third-party source system, which should be migrated in the following steps.

## Creating a profile [​](#creating-a-profile)

In the first step, you have to create a new profile for your source system:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample;

use SwagMigrationAssistant\Migration\Profile\ProfileInterface;

class OwnProfile implements ProfileInterface
{
    public const PROFILE_NAME = 'ownProfile';

    public const SOURCE_SYSTEM_NAME = 'MySourceSystem';

    public const SOURCE_SYSTEM_VERSION = '1.0';

    public const AUTHOR_NAME = 'shopware AG';

    public const ICON_PATH = '/swagmigrationassistant/static/img/migration-assistant-plugin.svg';

    public function getName(): string
    {
        return self::PROFILE_NAME;
    }

    public function getSourceSystemName(): string
    {
        return self::SOURCE_SYSTEM_NAME;
    }

    public function getVersion(): string
    {
        return self::SOURCE_SYSTEM_VERSION;
    }

    public function getAuthorName(): string
    {
        return self::AUTHOR_NAME;
    }

    public function getIconPath(): string
    {
        return self::ICON_PATH;
    }
}
```

The profile itself does not contain any logic and is used to bundle the executing classes. To use this profile, you have to register and tag it in the `service.xml` with `shopware.migration.profile`:

html

```shiki
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile">
    <tag name="shopware.migration.profile"/>
</service>
```

## Creating a gateway [​](#creating-a-gateway)

Next, you have to create a new gateway which supports your profile:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\EnvironmentInformation;
use SwagMigrationAssistant\Migration\Gateway\GatewayInterface;
use SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\RequestStatusStruct;
use SwagMigrationAssistant\Profile\Shopware\Exception\DatabaseConnectionException;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactoryInterface;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class OwnLocaleGateway implements GatewayInterface
{
    public const GATEWAY_NAME = 'local';

    private ConnectionFactoryInterface $connectionFactory;

    private ReaderRegistry $readerRegistry;

    public function __construct(
        ReaderRegistry $readerRegistry,
        ConnectionFactoryInterface $connectionFactory
    ) {
        $this->readerRegistry = $readerRegistry;
        $this->connectionFactory = $connectionFactory;
    }

    public function getName(): string
    {
        return self::GATEWAY_NAME;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile;
    }

    public function getSnippetName(): string
    {
        return 'swag-migration.wizard.pages.connectionCreate.gateways.shopwareLocal';
    }

    /**
     * Reads the given entity type from via context from its connection and returns the data
     */
    public function read(MigrationContextInterface $migrationContext): array
    {
        // TODO: Implement read() method.
        return [];
    }

    public function readEnvironmentInformation(
        MigrationContextInterface $migrationContext,
        Context $context
    ): EnvironmentInformation {
        $connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
        $profile = $migrationContext->getProfile();

        try {
            $connection->connect();
        } catch (\Exception $e) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }
        $connection->close();

        $totals = $this->readTotals($migrationContext, $context);

        return new EnvironmentInformation(
            $profile->getSourceSystemName(),
            $profile->getVersion(),
            'Example Host Name',
            $totals,
            [],
            new RequestStatusStruct(),
            false
        );
    }

    public function readTotals(MigrationContextInterface $migrationContext, Context $context): array
    {
        $readers = $this->readerRegistry->getReaderForTotal($migrationContext);

        $totals = [];
        foreach ($readers as $reader) {
            $total = $reader->readTotal($migrationContext);

            if ($total === null) {
                continue;
            }

            $totals[$total->getEntityName()] = $total;
        }

        return $totals;
    }
}
```

As you have seen above, the gateway uses the `ConnectionFactory` to test the connection to the source system. You can also implement your own way to check this, but using this factory is the simplest way for a gateway to connect to a local database. Like the profile, you have to register the new gateway in the `service.xml` and tag it with `shopware.migration.gateway`:

html

```shiki
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway\OwnLocaleGateway">
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry"/>
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactory"/>
    <tag name="shopware.migration.gateway"/>
</service>
```

## Creating a credentials page [​](#creating-a-credentials-page)

If you want to try your current progress in the Administration, you can select the profile and gateway in the migration wizard. If you try to go to the next page, there will be an error message because no credentials page was found. To create a new credentials page, you have to add an `index.js` for your new component into `Resources/app/administration/src/own-profile/profile`:

javascript

```shiki
import { Component } from 'src/core/shopware';
import template from './swag-migration-profile-ownProfile-local-credential-form.html.twig';

Component.register('swag-migration-profile-ownProfile-local-credential-form', {
    template,

    props: {
        credentials: {
            type: Object,
            default() {
                return {};
            }
        }
    },

    data() {
        return {
            inputCredentials: {
                dbHost: '',
                dbPort: '3306',
                dbUser: '',
                dbPassword: '',
                dbName: ''
            }
        };
    },

    watch: {
        credentials: {
            immediate: true,
            handler(newCredentials) {
                if (newCredentials === null) {
                    this.emitCredentials(this.inputCredentials);
                    return;
                }

                this.inputCredentials = newCredentials;
                this.emitOnChildRouteReadyChanged(
                    this.areCredentialsValid(this.inputCredentials)
                );
            }
        },

        inputCredentials: {
            deep: true,
            handler(newInputCredentials) {
                this.emitCredentials(newInputCredentials);
            }
        }
    },

    methods: {
        areCredentialsValid(newInputCredentials) {
            return (newInputCredentials.dbHost !== '' &&
                newInputCredentials.dbPort !== '' &&
                newInputCredentials.dbName !== '' &&
                newInputCredentials.dbUser !== '' &&
                newInputCredentials.dbPassword !== ''
            );
        },

        emitOnChildRouteReadyChanged(isReady) {
            this.$emit('onChildRouteReadyChanged', isReady);
        },

        emitCredentials(newInputCredentials) {
            this.$emit('onCredentialsChanged', newInputCredentials);
            this.emitOnChildRouteReadyChanged(
                this.areCredentialsValid(newInputCredentials)
            );
        },

        onKeyPressEnter() {
            this.$emit('onTriggerPrimaryClick');
        }
    }
});
```

As you can see above, currently, the template does not exist and you have to create this file: `swag-migration-profile-ownProfile-local-credential-form.html.twig`

html

```shiki
{% block own_profile_page_credentials %}
    <div class="swag-migration-wizard swag-migration-wizard-page-credentials"
         @keypress.enter="onKeyPressEnter">
        {% block own_profile_page_credentials_content %}
            <div class="swag-migration-wizard__content">
                {% block own_profile_page_credentials_information %}
                    <div class="swag-migration-wizard__content-information">
                        {% block own_profile_page_credentials_local_hint %}
                            {{ $tc('swag-migration.wizard.pages.credentials.shopware55.local.contentInformation') }}
                        {% endblock %}
                    </div>
                {% endblock %}

                {% block own_profile_page_credentials_credentials %}
                    <div class="swag-migration-wizard__form">
                        {% block own_profile_page_credentials_local_db_host_port_group %}
                            <sw-container columns="1fr 80px"
                                          gap="16px">
                                {% block own_profile_page_credentials_local_dbhost_field %}
                                    <sw-text-field v-autofocus
                                                   name="sw-field--dbHost"
                                                   :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbHostLabel')"
                                                   :placeholder="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbHostPlaceholder')"
                                                   v-model="inputCredentials.dbHost">
                                    </sw-text-field>
                                {% endblock %}

                                {% block own_profile_page_credentials_local_dbport_field %}
                                    <sw-field name="sw-field--dbPort"
                                              :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbPortLabel')"
                                              v-model="inputCredentials.dbPort">
                                    </sw-field>
                                {% endblock %}
                            </sw-container>
                        {% endblock %}

                        {% block own_profile_page_credentials_local_dbuser_field %}
                            <sw-field name="sw-field--dbUser"
                                      :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbUserLabel')"
                                      :placeholder="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbUserPlaceholder')"
                                      v-model="inputCredentials.dbUser">
                            </sw-field>
                        {% endblock %}

                        {% block own_profile_page_credentials_local_dbpassword_field %}
                            <sw-field name="sw-field--dbPassword"
                                      type="password"
                                      :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbPasswordLabel')"
                                      :placeholder="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbPasswordPlaceholder')"
                                      v-model="inputCredentials.dbPassword">
                            </sw-field>
                        {% endblock %}

                        {% block own_profile_page_credentials_local_dbname_field %}
                            <sw-field name="sw-field--dbName"
                                      :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbNameLabel')"
                                      :placeholder="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbNamePlaceholder')"
                                      v-model="inputCredentials.dbName">
                            </sw-field>
                        {% endblock %}
                    </div>
                {% endblock %}
            </div>
        {% endblock %}
    </div>
{% endblock %}
```

Note that the component name isn't random and consists of:

1. The prefix: `swag-migration-profile-`
2. The name of the profile
3. The name of the gateway
4. The suffix: `-credential-form`

To see your credentials page, you have to register this component in your `main.js`:

javascript

```shiki
import './own-profile/profile';
```

## Creating a dataSet and dataSelection [​](#creating-a-dataset-and-dataselection)

Now the credential page is loaded in the Administration and the connection check will succeed. But there is no data selection if you open the data selection table. To add an entry to this table, you have to create a `ProductDataSet` first:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet;

use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class ProductDataSet extends DataSet
{
    /**
     * Returns the entity identifier of this DataSet
     */
    public static function getEntity(): string
    {
        return 'product';
    }

    /**
     * Supports only an OwnProfile
     */
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile;
    }
}
```

Now you have to use this `ProductDataSet` in the new `ProductDataSelection`:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class ProductDataSelection implements DataSelectionInterface
{
    /**
     * Identifier of this DataSelection
     */
    public const IDENTIFIER = 'products';

    /**
     * Supports only an OwnProfile
     */
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile;
    }

    public function getData(): DataSelectionStruct
    {
        return new DataSelectionStruct(
            self::IDENTIFIER,
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            /*
             * Snippet of the original ProductDataSelection, if you
             * want to use your own title, you have to create a new snippet
             */
            'swag-migration.index.selectDataCard.dataSelection.products',
            100
        );
    }

    /**
     * Returns all DataSets, which should be migrated with this DataSelection
     */
    public function getDataSets(): array
    {
        return [
            new ProductDataSet()
        ];
    }

    public function getDataSetsRequiredForCount(): array
    {
        return $this->getDataSets();
    }
}
```

INFO

The order in the `getDataSets` array is important as it determines the order in which the entities are processed. Because of that, the manufacturers, for example, have to be positioned before the products so that the products can use those later on.

To see the created `ProductDataSelection` in the Administration, you have to register it both in the `services.xml` and tag them with `shopware.migration.data_selection` and `shopware.migration.data_set`:

html

```shiki
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\ProductDataSelection">
    <tag name="shopware.migration.data_selection"/>
</service>

<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet">
    <tag name="shopware.migration.data_set"/>
</service>
```

## Creating a product gateway reader [​](#creating-a-product-gateway-reader)

Currently, you can see the `DataSelection` in the Administration, but if you select it and start a migration, no product will be migrated. That is because the gateway `read` function isn't implemented yet. But before you can implement this function, you have to create a new `ProductReader` first:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway\Reader;

use Doctrine\DBAL\Driver\ResultStatement;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\TotalStruct;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ShopwareLocalGateway;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class ProductReader extends AbstractReader
{
    /**
     * Supports only an OwnProfile and the ProductDataSet
     */
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile
            && $migrationContext->getDataSet()::getEntity() === ProductDataSet::getEntity();
    }

    /**
     * Supports only an OwnProfile and the ProductDataSet for totals
     */
    public function supportsTotal(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile
            && $migrationContext->getGateway()->getName() === ShopwareLocalGateway::GATEWAY_NAME;
    }

    /**
     * Creates a database connection and sets the connection class variable
     */
    protected function setConnection(MigrationContextInterface $migrationContext): void
    {
        $this->connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
    }

    public function readTotal(MigrationContextInterface $migrationContext): ?TotalStruct
    {
        $this->setConnection($migrationContext);

        $query = $this->connection->createQueryBuilder()
            ->select('COUNT(*)')
            ->from('product')
            ->execute();

        $total = 0;
        if ($query instanceof ResultStatement) {
            $total = (int) $query->fetchColumn();
        }

        return new TotalStruct(ProductDataSet::getEntity(), $total);
    }

    /**
     * Fetches all entities out of the product table with the given limit
     */
    public function read(MigrationContextInterface $migrationContext, array $params = []): array
    {
        $this->setConnection($migrationContext);

        $query = $this->connection->createQueryBuilder();
        $query->from('product');
        $query->addSelect('*');

        $query->setFirstResult($migrationContext->getOffset());
        $query->setMaxResults($migrationContext->getLimit());

        return $query->execute()->fetchAll(\PDO::FETCH_ASSOC);
    }
}
```

Then you have to register this in `services.xml` and tag it with `shopware.migration.reader`:

html

```shiki
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway\Reader\ProductReader"
    parent="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader">
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactory"/>
    <tag name="shopware.migration.reader"/>
</service>
```

Once the `ProductReader` is created and registered, you can use it in the `read` method of the `OwnLocaleGateway`:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\EnvironmentInformation;
use SwagMigrationAssistant\Migration\Gateway\GatewayInterface;
use SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\RequestStatusStruct;
use SwagMigrationAssistant\Profile\Shopware\Exception\DatabaseConnectionException;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactoryInterface;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class OwnLocaleGateway implements GatewayInterface
{
    public const GATEWAY_NAME = 'local';

    private ConnectionFactoryInterface $connectionFactory;

    private ReaderRegistry $readerRegistry;

    public function __construct(
        ReaderRegistry $readerRegistry,
        ConnectionFactoryInterface $connectionFactory
    ) {
        $this->readerRegistry = $readerRegistry;
        $this->connectionFactory = $connectionFactory;
    }

    public function getName(): string
    {
        return self::GATEWAY_NAME;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile;
    }

    public function getSnippetName(): string
    {
        return 'swag-migration.wizard.pages.connectionCreate.gateways.shopwareLocal';
    }

    public function read(MigrationContextInterface $migrationContext): array
    {
        $reader = $this->readerRegistry->getReader($migrationContext);

        return $reader->read($migrationContext);
    }

    public function readEnvironmentInformation(
        MigrationContextInterface $migrationContext,
        Context $context
    ): EnvironmentInformation {
        $connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
        $profile = $migrationContext->getProfile();

        try {
            $connection->connect();
        } catch (\Exception $e) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }
        $connection->close();

        $totals = $this->readTotals($migrationContext, $context);

        return new EnvironmentInformation(
            $profile->getSourceSystemName(),
            $profile->getVersion(),
            'Example Host Name',
            $totals,
            [],
            new RequestStatusStruct(),
            false
        );
    }

    public function readTotals(MigrationContextInterface $migrationContext, Context $context): array
    {
        $readers = $this->readerRegistry->getReaderForTotal($migrationContext);

        $totals = [];
        foreach ($readers as $reader) {
            $total = $reader->readTotal($migrationContext);

            if ($total === null) {
                continue;
            }

            $totals[$total->getEntityName()] = $total;
        }

        return $totals;
    }
}
```

## Creating a converter [​](#creating-a-converter)

By using the gateway reader, you fetch all products but don't use this data yet. In this step, you implement the logic of the converter:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\Converter;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\Converter\ConvertStruct;
use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\Converter\ShopwareConverter;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class ProductConverter extends ShopwareConverter
{
    private string $connectionId;

    private Context $context;

    public function getSourceIdentifier(array $data): string
    {
        return $data['id'];
    }

    /**
     * Supports only an OwnProfile and the ProductDataSet
     */
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile &&
            $migrationContext->getDataSet()::getEntity() === ProductDataSet::getEntity();
    }

    /**
     * Writes the created mapping
     */
    public function writeMapping(Context $context): void
    {
        $this->mappingService->writeMapping($context);
    }

    public function convert(array $data, Context $context, MigrationContextInterface $migrationContext): ConvertStruct
    {
        $this->generateChecksum($data);
        $this->connectionId = $migrationContext->getConnection()->getId();
        $this->context = $context;

        /**
         * Gets the product uuid out of the mapping table or creates a new one
         */
        $this->mainMapping = $this->mappingService->getOrCreateMapping(
            $migrationContext->getConnection()->getId(),
            ProductDataSet::getEntity(),
            $data['id'],
            $context,
            $this->checksum
        );

        $converted['id'] = $this->mainMapping['entityUuid'];
        $this->convertValue($converted, 'productNumber', $data, 'product_number');
        $this->convertValue($converted, 'name', $data, 'product_name');
        $this->convertValue($converted, 'stock', $data, 'stock', self::TYPE_INTEGER);

        if (isset($data['tax'])) {
            $converted['tax'] = $this->getTax($data);
            $converted['price'] = $this->getPrice($data, $converted['tax']['taxRate']);
        }

        unset(
          $data['id'],
          $data['product_number'],
          $data['product_name'],
          $data['stock'],
          $data['tax'],
          $data['price']
        );

        if (empty($data)) {
            $data = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        return new ConvertStruct($converted, $data, $this->mainMapping['id']);
    }

    private function getTax(array $data): array
    {
        $taxRate = (float) $data['tax'];

        /**
         * Gets the tax uuid by the given tax rate
         */
        $taxUuid = $this->mappingService->getTaxUuid($this->connectionId, $taxRate, $this->context);

        /**
         * If no tax rate is found, create a new one
         */
        if ($taxUuid === null) {
            $mapping = $this->mappingService->createMapping(
                $this->connectionId,
                DefaultEntities::TAX,
                $data['id']
            );
            $taxUuid = $mapping['entityUuid'];
        }

        return [
            'id' => $taxUuid,
            'taxRate' => $taxRate,
            'name' => 'Own profile tax rate (' . $taxRate . ')',
        ];
    }

    private function getPrice(array $data, float $taxRate): array
    {
        $gross = (float) $data['price'] * (1 + $taxRate / 100);

        /**
         * Gets the currency uuid by the given iso code
         */
        $currencyUuid = $this->mappingService->getCurrencyUuid(
            $this->connectionId,
            'EUR',
            $this->context
        );

        if ($currencyUuid === null) {
            return [];
        }

        $price = [];
        $price[] = [
            'currencyId' => $currencyUuid,
            'gross' => $gross,
            'net' => (float) $data['price'],
            'linked' => true,
        ];

        return $price;
    }
}
```

If you don't know which properties or requirements your entity has in Shopware 6, you may check the corresponding `EntityDefinition`. For this example, look at the `ProductEntityDefinition` to know how to convert the data exactly.

To use this converter, you must register it in the `services.xml`:

html

```shiki
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\Converter\ProductConverter">
    <argument type="service" id="SwagMigrationAssistant\Migration\Mapping\MappingService"/>
    <argument type="service" id="SwagMigrationAssistant\Migration\Logging\LoggingService"/>
    <tag name="shopware.migration.converter"/>
</service>
```

To write new entities, you have to create a new writer class, but for the product entity, you can use the `ProductWriter`:

php

```shiki
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Writer;

use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;

class ProductWriter extends AbstractWriter
{
    public function supports(): string
    {
        return DefaultEntities::PRODUCT;
    }
}
```

This writer will be called automatically as the `getEntityName` method of your `ProductDataSet` is compared with the return value of the `supports` method of the writer in the `WriterRegistry`. These values are identical, and so the writer will be used to write your product entities.

## Source [​](#source)

Check out this [GitHub repository](https://github.com/shopwareArchive/swag-docs-create-migration-profile) containing a full example source.

---

