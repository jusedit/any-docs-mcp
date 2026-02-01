# Products Extensions B2B Suite Migration

*Scraped from Shopware Developer Documentation*

---

## B2B Suite Migration

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/

# B2B Suite Migration [​](#b2b-suite-migration)

The B2B Suite Migration extension is designed to facilitate the migration of data from the B2B Suite to the B2B Components. This migration process is essential for merchants who want to transition from the legacy B2B Suite to the more modular and flexible B2B Components.

## Purpose [​](#purpose)

This section provides a comprehensive guide for developers to migrate data from B2B Suite to B2B Commercial. It covers the migration process, from high-level concepts to detailed execution and development instructions, ensuring a smooth and reliable transition. The content is structured into focused sections to help you understand, execute, and extend the migration process effectively.

WARNING

B2B Suite will no longer be supported starting Shopware 6.8. Plan your migration promptly to avoid disruptions.

## Prerequisites [​](#prerequisites)

Please refer to the [B2B Suite Migration Prerequisites](./execution/prerequisites.html) section.

---

## Concept

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/concept/

# Concept [​](#concept)

The migration process is designed to handle large datasets while maintaining data integrity. It uses three dedicated tables to track status, map records, and log errors. A message queue ensures scalability, and sequential migration respects entity relationships (e.g., migrating employees before quotes). Understanding these concepts is crucial before proceeding to execution.

## Migration Approach [​](#migration-approach)

The whole migration is executed in a message queue, allowing for scalable processing of large volumes of data. The migration is structured to ensure that all components and entities are migrated in the correct order, respecting their relationships and dependencies. All mappings fields and tables are defined via XML configuration files, which are processed by configurator. This modular approach allows for easy customization and extension of the migration process.

## Key Features [​](#key-features)

* **Message Queue**: Utilizes a message queue to process large volumes of data, ensuring scalability.
* **Sequential Migration**: Components (e.g., Employee, Budget, Quote, Shopping List) are migrated sequentially to respect entity relationships (e.g., employee records before budget).
* **Entity-Level Sequencing**: Within each component, entities (e.g., business partners, employees, roles) are migrated in the correct order.

INFO

Proper sequencing is critical to avoid dependency issues. Verify the migration order for your dataset.

---

## Migration Table

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/concept/migration-table.html

# Migration Tables [​](#migration-tables)

The migration process introduces three tables to manage and track data migration from B2B Suite to B2B Commercial:

1. **`b2b_components_migration_state`**  
    Tracks the status of the migration process for each entity.
2. **`b2b_components_migration_map`**  
    Maps records between B2B Suite and B2B Commercial, ensuring traceability.
3. **`b2b_components_migration_errors`**  
    Logs errors encountered during migration for troubleshooting.

INFO

These tables enable monitoring, verification, and debugging of the migration process.

---

## Technical Terms and Concepts

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/concept/technical-terms-and-concepts.html

# Technical Terms and Concepts [​](#technical-terms-and-concepts)

This section defines key technical terms and concepts used in the migration process from B2B Suite to B2B Commercial, providing clarity for developers navigating the migration.

## Component [​](#component)

A **component** is a distinct module within the B2B Commercial system, such as `B2B Commercial Employee Management`, `B2B Commercial Budget Management`, `B2B Commercial Quote Management`, or `B2B Commercial Shopping List`. Each component encapsulates a specific set of functionalities and associated data structures.

INFO

Components organize related entities and their migrations, ensuring modularity and maintainability.

## Entity [​](#entity)

An **entity** represents a specific type of data within a component. For example, within the `B2B Commercial Employee Management` component, entities include `Employee`, `Role`, and `Permission`. Each entity has its own attributes and behaviors, defined by its schema in the source and target tables.

## Configurator [​](#configurator)

A **configurator** is a PHP class that defines the migration process for a component’s entities. It specifies:

* Technical name of the component (e.g., `employee_management`).
* Field mappings between source and target tables (see [Field Mapping Configuration](./../development/fields-mapping.html)).
* The XML configuration file path for mappings.

Configurator extends classes like `AbstractB2BMigrationConfigurator` or `AbstractB2BExtensionMigrationConfigurator` for base or extended migrations, respectively.

INFO

Configurator provides a structured way to customize and control the migration process for each component.

## Handler [​](#handler)

A **handler** is a PHP class that implements custom logic to transform data for specific fields during migration. Handlers are used when complex transformations are needed beyond simple mappings, ensuring data integrity and compatibility with B2B Commercial’s format. They are defined in the XML configuration and implemented via the `transform` method, as detailed in [Handler-Based Transformation](./../development/handler.html).

INFO

Handlers are critical for handling complex data transformations, such as reformatting or combining multiple source fields.

---

## Execution

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/execution/

# Execution [​](#execution)

Executing the migration involves preparing your environment, running specific commands, and troubleshooting issues. Key steps include backing up data, ensuring the queue worker is active, and using console commands to start and monitor the migration. Detailed instructions ensure you can track progress and handle errors effectively.

---

## Prerequisites

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/execution/prerequisites.html

# Prerequisites [​](#prerequisites)

Before starting the migration, complete the following steps:

## Backup Your Data [​](#backup-your-data)

WARNING

If you are using B2B Commercial and already have data in it, you should back up your Database before initiating the migration. The migration is designed to add data to B2B Commercial and not remove any data from B2B Suite, having a backup ensures you can restore your data in case of any issues.

## Queue Worker [​](#queue-worker)

Ensure the message queue worker is running to process migration tasks.

## Extension Version [​](#extension-version)

Ensure your B2B Suite version is `4.9.3` or above.

## Component Requirements [​](#component-requirements)

### Budget Management [​](#budget-management)

* Requires B2B Commercial version `7.6.0` or above.
* Note: The Organization Unit of the budget will be empty after migration and needs to be manually assigned in B2B Commercial.

---

## Running Migration

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/execution/running-migration.html

# Running Migration [​](#running-migration)

This section describes how to execute and monitor the migration process.

## Commands [​](#commands)

In this section, we will introduce two helpful commands:

* `b2b:migrate:commercial`: Start the migration process.
* `b2b:migrate:progress`: Check migration status.

For an optimal experience, we recommend running both commands simultaneously in separate terminal windows rather than sequentially. See details below.

### Start the Migration [​](#start-the-migration)

#### 1. How to run the migration command [​](#_1-how-to-run-the-migration-command)

This command initiates the migration process, transferring all components and entities as defined in the configuration

bash

```shiki
bin/console b2b:migrate:commercial
```

#### 2. How to run the migration command with specific components [​](#_2-how-to-run-the-migration-command-with-specific-components)

You could also specify which component to migrate. This is useful for testing or when you want to migrate specific components without affecting others. The name of the component should match the technical name defined in the [configurator](./../concept/technical-terms-and-concepts.html#configurator).

bash

```shiki
bin/console b2b:migrate:commercial component_name_1 component_name_2
```

**Example**: To migrate only the `shopping_list` and `quote_management` components:

bash

```shiki
bin/console b2b:migrate:commercial quote_management shopping_list
```

**Note**: The `employee_management` component is a prerequisite for all other B2B components and is migrated first by default, regardless of the specified order. For instance, executing `bin/console b2b:migrate:commercial quote_management shopping_list` will migrate `employee_management` first, followed by `quote_management`, and then `shopping_list`. The order of components listed in the command does not affect the migration sequence. The order of migration is determined by the priority of the configurators, which is defined in the service definition file. The configurator with the highest priority will be executed first.

#### 3. How to run the migration command with a specific batch size [​](#_3-how-to-run-the-migration-command-with-a-specific-batch-size)

To control the number of records processed in each batch, you can specify a batch size using the `--batch-size` option. This is useful for managing memory usage and performance during migration.

bash

```shiki
bin/console b2b:migrate:commercial --batch-size=100
```

**Note**: Adjust the batch size according to your system's capabilities and the size of the data being migrated.

INFO

This command utilizes the message queue system to process the migration in the background. Even after the command execution completes, the migration may still be ongoing. To monitor the migration status in real-time, run the `bin/console b2b:migrate:progress` command in a separate terminal window.

## Component-Specific Notes [​](#component-specific-notes)

### Budget Management [​](#budget-management)

WARNING

The Organization Unit of the budget will be empty after migration. This is expected behavior and you will need to manually assign each budget to organization units in B2B Commercial after the migration is complete.

**Note**: Budget Management feature is available from Commercial 7.6.0 and above.

### Check Migration Status [​](#check-migration-status)

This command provides real-time insights into the migration process, displaying progress and statistics in a table format.

The output includes the following columns:

* **Total**: Total records in the source table.
* **Valid**: Records meeting migration criteria.
* **Newly**: Records added post-migration start.
* **Migrated**: Successfully migrated records.
* **Pending**: Records awaiting migration.
* **Error**: Records that failed to migrate.

And the **Status** column will indicate the current state of the migration:

* `Complete`: Migration completed successfully.
* `Pending`: Waiting to start.
* `In progress`: Migration in progress.
* `Complete with error`: Errors occurred (check `b2b_components_migration_errors`).
* `Has new records`: New records detected in B2B Suite.

  bash

  ```shiki
    bin/console b2b:migrate:progress
  ```

To monitor the migration process effectively, it is recommended to run this command in a separate terminal window while the migration is ongoing. This allows you to see real-time updates on the migration status. You could also add `--watch` option to automatically refresh the output every 5 seconds:

bash

```shiki
bin/console b2b:migrate:progress --watch
```

---

## Troubleshooting

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/execution/troubleshooting.html

# Troubleshooting [​](#troubleshooting)

Address issues during migration with the following steps:

* **Check Errors**: Review the `b2b_components_migration_errors` table for detailed error logs if the status is `Complete with error`. This error is logged when the migration process encounters issues that prevent it from completing successfully.
* **New Records**: If `Has new records` appears in the output of the watch progress command, it indicates that new records were added during the migration process. This can happen if there are changes in the B2B Suite while the migration is running.

## Rollback Migration [​](#rollback-migration)

If you need to revert the migration, you can roll back the changes made by the migration process. This will remove all migrated data from B2B Commercial and restore the state before migration.

What is this command doing?

* Deletes all records from the B2B Commercial tables that were migrated.
* Resets the migration state, mapping, and error tables to their initial state.
* Delete all messages from the message queue related to the migration.
* All data from B2B Suite will remain intact.

  bash

  ```shiki
  bin/console b2b:migrate:rollback
  ```

### 1. Rollback Specific Components [​](#_1-rollback-specific-components)

Additionally, you can specify which component to roll back. This is useful if you want to revert specific components without affecting others. The name of the component should match the technical name defined in the [configurator](./../concept/technical-terms-and-concepts.html#configurator).

bash

```shiki
bin/console b2b:migrate:rollback component_name_1 component_name_2
```

* **Example**: To roll back only the `shopping_list` and `quote_management` components:

  bash

  ```shiki
  bin/console b2b:migrate:rollback quote_management shopping_list
  ```

**Note**: The `employee_management` component is a prerequisite for all other B2B components. Therefore, if you specify `employee_management` in the rollback command, it will roll back all other components as well.

INFO

The order of components listed in the command does not matter for rollback. The command will process all specified components in the reverse order of their migration sequence.

### 2. Force Rollback [​](#_2-force-rollback)

If you want to force the rollback command without confirming the deletion of data, you can use the `--force` or `-f` option:

bash

```shiki
bin/console b2b:migrate:rollback --force
```

### 3. Batch Size [​](#_3-batch-size)

Just like the migration command, you can specify a maximum batch size for the rollback operation. This is useful for managing memory usage and performance during the rollback.

bash

```shiki
bin/console b2b:migrate:rollback --batch-size=500
```

## Error Troubleshooting [​](#error-troubleshooting)

If you encounter errors during migration, follow these steps to troubleshoot:

1. **Check Migration Errors**: Review the `b2b_components_migration_errors` table for detailed error logs. This table contains information about any issues encountered during the migration process, including the component, entity, and specific error messages.
2. Because the migration process executes in a batch mode, it is possible that some records were migrated successfully while others failed. In this case, all records that belong to this batch will be marked as `Error` and will not be migrated. All of them will be logged in the `b2b_components_migration_errors` table and link to the `b2b_components_migration_map` table. You can use this information to indicate which records were not migrated and why.

---

## Development

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/

# Development [​](#development)

For developers looking to customize or extend the migration, this section provides guidance on adding new components, extending existing entities, and validating configurations. It includes detailed steps for creating configurator, defining XML mappings, and setting conditions or default values, enabling you to tailor the migration to your needs.

---

## Adding Component

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/adding-component.html

# Adding a New Component [​](#adding-a-new-component)

This section guides developers on adding a new component to the migration process.

## Register a Migration Configurator [​](#register-a-migration-configurator)

* Create a class extending `Shopware\Commercial\B2B\B2BSuiteMigration\Core\Domain\MappingConfigurator\AbstractB2BMigrationConfigurator`.
* Define the component name in lowercase snake\_case in `getName()`.
* Specify the [XML mapping](#create-xml-mapping-file) path in `configPath()`.
* Tag the class with `b2b.migration.configurator`. **Example**:

  XML

  ```shiki
  <service id="Shopware\Commercial\B2B\B2BSuiteMigration\Components\EmployeeManagement\EmployeeManagementMigrationConfigurator">
     <tag name="b2b.migration.configurator" priority="9000"/>
  </service>
  ```

  PHP

  ```shiki
  class EmployeeManagementMigrationConfigurator extends AbstractB2BMigrationConfigurator
  {
    public function getName(): string
    {
        return 'employee_management';
    }

    public function configPath(): string
    {
        return 'path/to/your/xml/mapping/file.xml';
    }
    ...
  }
  ```

  + The `priority` attribute in the tag determines the order of execution among multiple configurator. Higher values execute first.

    INFO

    You can run this command to see the order of execution:

    bash

    ```shiki
    php bin/console debug:container --tag=b2b.migration.configurator
    ```

    The default priorities for existing configurator are:

    - `EmployeeManagementMigrationConfigurator` has a priority of `9000`.
    - `QuoteB2BMigrationConfigurator` has a priority of `8000`.
    - `ShoppingListMigrationConfigurator` has a priority of `7000`.
    - `BudgetManagementMigrationConfigurator` has a priority of `5000`.

## Create XML Mapping File [​](#create-xml-mapping-file)

### Entity Definition [​](#entity-definition)

XML

```shiki
<migration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../Core/Resources/Schema/Xml/migration-1.0.xsd">
 <entity>
   <name>migration_b2b_component_business_partner</name>
   <source>b2b_customer_data</source>
   <source_primary_key>customer_id</source_primary_key>
   <target>b2b_business_partner</target>
   <target_primary_key>id</target_primary_key>
   <conditions>
     <condition>foo = bar</condition>
   </conditions>
   <fields>
     ...
   </fields>
 </entity>
</migration>
```

* **name**: Unique migration process identifier.
* **source**: Source table name.
* **source\_primary\_key**: Source table primary key (default: `id`).
* **target**: Target table name.
* **target\_primary\_key**: Target table primary key (default: `id`).
* **conditions**: Optional conditions to filter source records (see [Conditions](#conditions)).
* **fields**: Field mappings between source and target tables (see [Field Mapping Configuration](./fields-mapping.html)).

## Conditions [​](#conditions)

XML

```shiki
<conditions>
    <condition>foo = bar</condition>
</conditions>
```

* Conditions allow you to filter which records from the source table are included in the migration process. They are defined in `<condition>` elements within the `<conditions>` block of the XML configuration for each entity.

**Example**:

XML

```shiki
<entity>
  <name>migration_b2b_component_business_partner</name>
  <source>b2b_customer_data</source>
  <target>b2b_business_partner</target>
  ...
  <conditions>
    <condition>is_debtor = 1</condition>
  </conditions>
  ...
</entity>
```

* **Explanation**: This filters the records from the `b2b_customer_data` source table (as specified in the XML configuration) to include only entries where the `is_debtor` field is set to `1`.
* **Key Points**:
  + Conditions are written as SQL-like expressions (e.g., `is_debtor = 1`, `status != 'inactive'`).
  + Multiple conditions can be specified, and they are combined with `AND` logic.

INFO

Ensure conditions are valid for the source table schema to avoid runtime errors.

---

## Fields Mapping

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/fields-mapping.html

# Fields Mapping [​](#fields-mapping)

This section guides developers on how to create and configure field mappings for migrating data from B2B Suite to B2B Commercial.

## Fields [​](#fields)

In the previous sections, we discussed how to create a component and its entities. Now, we will focus on how to define field mappings between source tables in B2B Suite and target tables in B2B Commercial. **Example**:

XML

```shiki
<fields>
  <field source="customer_id" target="customer_id"/>
  <field source="created_at" target="created_at"/>
</fields>
```

## Field Mapping Configuration [​](#field-mapping-configuration)

Field mappings define how data is transferred from source tables in B2B Suite to target tables in B2B Commercial. These mappings are specified in the XML configuration within the `<fields>` element. This section explains the different mapping types and their syntax.

### One-to-One Mapping [​](#one-to-one-mapping)

A one-to-one mapping directly maps a field from the source table to a field in the target table.

**Example**:

XML

```shiki
<field source="customer_id" target="customer_id"/>
```

* **source**: The field name in the source table (e.g., `customer_id` in `b2b_customer_data`).
* **target**: The field name in the target table (e.g., `customer_id` in `b2b_business_partner`).

INFO

Use one-to-one mappings for straightforward field transfers where no transformation is needed.

### Relational Mapping [​](#relational-mapping)

Relational mappings allow you to map a field from a related table by joining through foreign keys. This is useful when the source table references data in another table.

**Example**:

XML

```shiki
<field source="context_owner_id.b2b_store_front_auth.customer_id" target="business_partner_customer_id"/>
```

**Explanation**:

Joins the source table to `b2b_store_front_auth` using `context_owner_id = b2b_store_front_auth.id`, then retrieves `customer_id` from `b2b_store_front_auth` and maps it to `business_partner_customer_id` in the target table.

#### 1. Basic Format [​](#_1-basic-format)

This is the example on how to define a basic relational mapping in the XML configuration:

XML

```shiki
<field source="foreign_field.foreign_table.field_of_foreign_table" target="target_field"/>
```

**Explanation**:

* `foreign_field`: The field in the source table used to join to the foreign table.
* `foreign_table`: The related table to join.
* `field_of_foreign_table`: The field to retrieve from the foreign table.

#### 2. Multiple Joins [​](#_2-multiple-joins)

Chain joins for deeper relationships

XML

```shiki
<field source="foo_id.foo.bar_id.bar.name" target="target_field"/>
```

**Explanation**:

Joins `source_table.foo_id` to `foo.id`, then `foo.bar_id` to `bar.id`, and retrieves `bar.name`.

#### 3. Custom Join Field [​](#_3-custom-join-field)

By default, joins use the `id` field of the foreign table. To use a different field, specify it in square brackets:

XML

```shiki
<field source="foreign_field.foreign_table[custom_field].field_of_foreign_table" target="target_field"/>
```

**Explanation**:

Joins `source_table.foo_id` to `foo.custom_field` instead of `foo.id`.

INFO

Ensure the foreign key relationships are valid to avoid errors during migration.

### Handler-Based Mapping [​](#handler-based-mapping)

In some cases, you may need to apply custom logic to transform data before mapping it to the target field(s). This is where **handlers** come into play. Let's continue with the next [section](./handler.html) to understand how handlers work and how to implement them in your migration process.

---

## Handlers

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/handler.html

# Handlers [​](#handlers)

This section guides developers on how to create and configure handlers for transforming data during the migration from B2B Suite to B2B Commercial. Handlers allow for custom logic to be applied to source data before it is mapped to target fields, enabling complex transformations and data processing.

## Handler-Based Transformation [​](#handler-based-transformation)

As you notice, the previous examples of field mappings are straightforward. However, in some cases, you may need to apply custom logic to transform data before mapping it to the target field(s). This is where **handlers** come into play.

Handlers allow custom logic to transform data before mapping it to the target field(s). Handlers are PHP classes that process source data (if provided) and return values for the target field(s). A handler is specified in the XML configuration using the `handler` attribute within a `<field>` element, the value of which is the technical name of the handler class(It would be described in the section [How Handlers Work](#how-handlers-work)).

### 1. Options [​](#_1-options)

* **With Source Field**:

  XML

  ```shiki
  <field source="foo" target="permissions" handler="b2b.employee.employee_status_transformer"/>
  ```

  The handler takes the value of `foo` from the source table, applies transformation logic, and maps the result to `permissions`.
* **Without Source Field**:

  XML

  ```shiki
  <field target="permissions" handler="b2b.employee.employee_status_transformer"/>
  ```

  The handler generates the value for `permissions` without requiring a source field, using custom logic.

### 2. Multiple Sources or Targets [​](#_2-multiple-sources-or-targets)

* **Multiple Source Fields to One Target**:

  XML

  ```shiki
  <field target="quote_number" handler="b2b.employee.employee_status_transformer">
      <source>currency_factor</source>
      <source>auth_id.b2b_store_front_auth.customer_id.customer.sales_channel_id.sales_channel.language_id</source>
      <source>auth_id.b2b_store_front_auth.customer_id.customer.sales_channel_id</source>
  </field>
  ```

  The handler processes multiple source fields (e.g., `currency_factor`, relational fields) to compute a single target value (`quote_number`).
* **Multiple Source Fields to Multiple Targets**:

  XML

  ```shiki
  <field handler="b2b.employee.employee_status_transformer">
      <source>currency_factor</source>
      <source>auth_id.b2b_store_front_auth.customer_id.customer.sales_channel_id.sales_channel.language_id</source>

      <target>state_id</target>
      <target>expiration_date</target>
  </field>
  ```

  The handler processes multiple source fields and maps the results to multiple target fields (`state_id`, `expiration_date`).
* **Single Source Field to Multiple Targets**:

  XML

  ```shiki
  <field source="converted_at" handler="b2b.employee.employee_status_transformer">
      <target>order_version_id</target>
      <target>order_id</target>
  </field>
  ```

  The handler transforms a single source field (`converted_at`) into multiple target fields (`order_version_id`, `order_id`).

## Handler Registration [​](#handler-registration)

To use a handler, implement a PHP class (e.g., `RolePermissionsTransformer`) that extends `Shopware\Commercial\B2B\B2BSuiteMigration\Core\Domain\DataTransformer\AbstractFieldTransformer` and tag it with `b2b.migration.transformer` in your service configuration.

XML

```shiki
<service id="Shopware\Commercial\B2B\B2BSuiteMigration\Components\QuoteManagement\DataTransformer\QuoteComment\StateTransformer" lazy="true">
    <argument type="service" id="Shopware\Core\Framework\Extensions\ExtensionDispatcher"/>

    <tag name="b2b.migration.transformer" />
</service>
```

The best practice is to mark this service as `lazy="true"` to improve performance by loading it only when needed.

## Handler Implementation [​](#handler-implementation)

### Constructor [​](#constructor)

* Each handler must extend `AbstractFieldTransformer` and implement the required methods.
* Each handler's constructor must inject the `ExtensionDispatcher` service to allow for extension points and event handling.

PHP

```shiki
class StateTransformer extends AbstractFieldTransformer
{
    public function __construct(
        ExtensionDispatcher $extensions
    ) {
        parent::__construct($extensions);
    }
}
```

### Technical Name [​](#technical-name)

Each handler must have to define a technical name in the `getName()` method, which is used in the XML configuration (`field` element's `handler` attribute). This name should be unique and descriptive. The `FieldTransformerRegistry` will use this name to identify and instantiate the handler during the migration process.

PHP

```shiki
...
public function getName(): string
{
    return 'b2b.employee.employee_status_transformer';
}
```

### Required Fields [​](#required-fields)

Each handler must implement the `requiredFields` method to specify which source fields are required for the transformation.

PHP

```shiki
protected function requiredSourceFields(): array
{
  return ['foo', 'bar'];
}
```

**Example**:

1. If just one source field is required:

   XML

   ```shiki
   <field source="foo" target="permissions" handler="b2b.employee.employee_status_transformer"/>
   ```

   PHP

   ```shiki
   protected function requiredSourceFields(): array
   {
     return ['foo'];
   }
   ```
2. If multiple source fields are required:

   XML

   ```shiki
   <field handler="b2b.employee.employee_status_transformer">
       <source>foo</source>
       <source>bar</source>
     
       <target>permissions</target>
   </field>
   ```

   PHP

   ```shiki
   protected function requiredSourceFields(): array
   {
     return ['foo', 'bar'];
   }
   ```

### Transform Method [​](#transform-method)

* Each handler must implement the `_transform` method with the following signature:

PHP

```shiki
protected function _transform(
    Field $field,
    array $sourceRecord,
): mixed
```

* **Parameters**:

  + **Field `$field`**: Represents the field configuration from the XML mapping. Use:
    - `$field->getSource()`: Retrieves the single source field name (if specified).
    - `$field->getSourceElements()`: Retrieves an array of source field names for multiple sources.
  + **array `$sourceRecord`**: Contains the data of the current record being migrated, with keys corresponding to source field names or relational paths.
* **Return Value**:

  + For a single target field: Return a single value (e.g., string, integer, or JSON-encoded string).
  + For multiple target fields: Return an associative array where keys are target field names and values are the corresponding transformed values.

#### Examples [​](#examples)

***Example 1: Single Source to Single Target***

Transform a source field to determine an employee's status based on an `active` flag.

XML

```shiki
<entity>
  <name>migration_b2b_component_employee</name>
  <source>b2b_debtor_contact</source>
  <target>b2b_employee</target>
  <fields>
    <field source="active" target="status" handler="b2b.employee.employee_status_transformer"/>
  </fields>
</entity>
```

PHP

```shiki
public function transform(Field $field, array $sourceRecord): mixed
{
    $active = $sourceRecord[$field->getSource()] ?? 0;

    return $active ? EmployeeStatus::ACTIVE->value : EmployeeStatus::INACTIVE->value;
}
```

**Explanation**:

* The value of `$field->getSource()` is the plain string `active` - the column 'active' in the source table `b2b_debtor_contact`
* The value of this column `active` is retrieved from the `$sourceRecord` by using `$sourceRecord[$field->getSource()]`
* Checks if `$active` is truthy; returns `EmployeeStatus::ACTIVE->value` if true, or `EmployeeStatus::INACTIVE->value` if false.
* The handler returns a single value for the target field `status`.

***Example 2: Multiple Sources to multiple Target*** Transform multiple source fields to multiple target fields, such as generating an order ID and version ID.

XML

```shiki
<entity>
  <name>migration_b2b_component_quote_line_item</name>
  <source>b2b_line_item_reference</source>
  <target>quote_line_item</target>
  <fields>
    <field handler="b2b.quote_line_item.line_item_price_transformer">
      <source>list_id</source>
      <source>mode</source>
  
      <target>order_id</target>
      <target>order_version_id</target>
    </field>
  </fields>
</entity>
```

PHP

```shiki
public function transform(Field $field, array $sourceRecord): mixed
{
    ...
    if (!isset($field->getSourceElements()['list_id']) || !isset($field->getSourceElements()['mode'])) {
        // Handle missing required source fields
    }
    
    $listId = $sourceRecord['list_id'];
    $mode = $sourceRecord['mode'];
    // Perform transformation logic based on listId and mode
    return [
        'order_id' => $orderId,
        'order_version_id' => Uuid::fromHexToBytes(Defaults::LIVE_VERSION),
    ];
}
```

**Explanation**:

* `$field->getSourceElements()` retrieves the source fields `list_id` and `mode` which are present in the XML configuration - these are the columns in the source table `b2b_line_item_reference`.
* The handler retrieves values of 2 columns `list_id` and `mode` from source record of table `b2b_line_item_reference`.
* Returns an associative array with multiple target fields (`order_id`, `order_version_id`).

### Extending Handlers Transformation Logic [​](#extending-handlers-transformation-logic)

By default, handlers are designed to handle specific transformations. However, you can extend their functionality by subscribing to the corresponding event. We will publish the extension `B2BMigrationFieldTransformerExtension` (which is extended from `Shopware\Core\Framework\Extensions\Extension`) with the name is the technical name of the handler. This allows you to add custom logic to the transformation process without modifying the original handler code.

---

## Extending Migration

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/extending-migration.html

# Extending an Existing Migration [​](#extending-an-existing-migration)

This section explains how to add new fields to an existing entity or introduce new entities to an existing component.

## Registering a New Extension Configurator [​](#registering-a-new-extension-configurator)

* Create a class extending `Shopware\Commercial\B2B\B2BSuiteMigration\Core\Domain\Extension\ExtensionConfigurator\AbstractB2BExtensionMigrationConfigurator`.
* Tag the class with `b2b.migration.configurator.extension` in the service definition.
* Specify the component to extend in the `getName` method.
* Provide the directory path to your XML configuration file in the `configPath` method.

  **Example**:

  XML

  ```shiki
  <service id="MigrationExtension\B2BMigration\B2BExtensionMigrationConfigurator">
      <tag name="b2b.migration.configurator.extension"/>
  </service>
  ```

  PHP

  ```shiki
  class B2BExtensionMigrationConfigurator extends AbstractB2BExtensionMigrationConfigurator
  {
    public function getName(): string
    {
        return 'employee_management';
    }

    public function configPath(): string
    {
        return __DIR__ . '/../../src/Resources/employee.xml';
    }
    ...
  }
  ```

## Adding new conditions to an existing entity [​](#adding-new-conditions-to-an-existing-entity)

To add new conditions to an existing migration entity, you need to update the XML configuration.

### Update XML Configuration [​](#update-xml-configuration)

Define the new conditions in an XML file using the `<conditions>` element. **Example**:

XML

```shiki
<migration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../SwagCommercial/src/B2B/B2BSuiteMigration/Core/Resources/Schema/Xml/migration-extension-1.0.xsd">
    <entity>
        <name>migration_b2b_component_business_partner</name>
        <source>b2b_customer_data</source>
        <target>b2b_business_partner</target>
        <conditions>
          <condition>new_condition = value</condition>
          <condition>new_condition2 != value</condition>
        </conditions>
        <fields>
            ...
        </fields>
    </entity>
</migration>
```

**Note**: The `<conditions>` element allows you to specify additional filtering criteria for the migration entity. Each `<condition>` can be a simple SQL condition that will be applied to the source data. All of these conditions will be merged with the existing conditions defined in the base migration entity and applied together with `AND` logic.

## Adding New Fields to an Existing Entity [​](#adding-new-fields-to-an-existing-entity)

To add new fields to an existing migration entity, you need to update the XML configuration.

### Update XML Configuration [​](#update-xml-configuration-1)

Define the new fields in an XML file using the `<entity-extension>` element. **Example**:

XML

```shiki
<migration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../SwagCommercial/src/B2B/B2BSuiteMigration/Core/Resources/Schema/Xml/migration-extension-1.0.xsd">
    <entity-extension>
        <name>migration_b2b_component_business_partner</name>
        <fields>
            <field source="new_column" target="target_column"/>
        </fields>
    </entity-extension>
</migration>
```

* **name**: Must match the entity name defined in the base migration (e.g., `migration_b2b_component_business_partner`).
* **fields**: Follow the same mapping logic as described in [Field Mapping Configuration](./adding-component.html#field-mapping-configuration) (e.g., one-to-one, relational, or handler-based mappings).

INFO

Adding fields extends the existing entity without altering its original mappings.

## Adding a New Entity to an Existing Component [​](#adding-a-new-entity-to-an-existing-component)

To introduce a new entity to an existing component, define the entity in the XML configuration and update the extension configurator.

### Update XML Configuration [​](#update-xml-configuration-2)

Define the new entity in the XML file using the `<entity>` element, similar to the base migration setup for [Entity](./adding-component.html#entity-definition).

**Example**:

XML

```shiki
<migration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../SwagCommercial/src/B2B/B2BSuiteMigration/Core/Resources/Schema/Xml/migration-extension-1.0.xsd">
    <entity>
        <name>migration_b2b_component_customer_specific_features</name>
        <source>customer</source>
        <target>customer_specific_features</target>
        <fields>
            <field source="id.b2b_business_partner[customer_id].customer_id" target="customer_id"/>
            <field target="features" handler="Shopware\Commercial\B2B\B2BSuiteMigration\Components\EmployeeManagement\DataTransformer\CustomerSpecificFeature\CustomerSpecificFeaturesTransformer"/>
        </fields>
    </entity>
</migration>
```

---

## Validation and Run

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/development/validation-and-run.html

# Configuration Validation and Migration Execution [​](#configuration-validation-and-migration-execution)

After configuring your migration, follow these steps:

1. Validate the configuration: Validate your migration configuration to ensure correctness before running the migration.

   bash

   ```shiki
   bin/console b2b:migrate:validate
   ```

   * Checks the configuration for errors. Ensure the XML is well-formed and adheres to a valid schema. It will also verify if the fields and tables exist in the database; otherwise, it will throw an exception.
   * Provides hints to resolve issues if validation fails.

   INFO

   Validation helps catch configuration errors early, saving time during migration.
2. Monitor progress (should be run in a separate terminal):

   bash

   ```shiki
   bin/console b2b:migrate:progress --watch
   ```
3. Start the migration (ensure the queue worker is running):

   bash

   ```shiki
   bin/console b2b:migrate:commercial
   ```
4. Review logs and errors in `b2b_components_migration_errors` to ensure a successful migration.
5. In case you want to roll back the migration, use:

   bash

   ```shiki
   bin/console b2b:migrate:rollback
   ```

---

## References

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/references/

# References [​](#references)

This section provides additional resources and references to help you understand the B2B Suite Migration process better. It includes links to related documentation, command references for executing migration tasks, and other relevant materials.

---

## References

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/references/references.html

# References [​](#references)

This section consolidates key command-line commands used throughout the migration process and provides instructions for configuring the batch size (`Chunk_size`) for message queues. It serves as a quick reference for developers executing or customizing the migration from B2B Suite to B2B Commercial.

## Command-Line Commands [​](#command-line-commands)

The following table lists all console commands used in the migration process, along with their purpose and relevant handbook sections.

| Command | Purpose | Reference |
| --- | --- | --- |
| `bin/console b2b:migrate:commercial` | Starts the migration process, transferring data from B2B Suite to B2B Commercial. - `--batch-size` to set batch size for deletion.  - Arguments: `component_name_1 component_name_2` to specify components to migrate. | [Running the Migration](./../execution/running-migration.html) |
| `bin/console b2b:migrate:validate` | Validates the migration configuration (XML and configurator classes) for correctness. | [Configuration Validation](./../development/validation-and-run.html) |
| `bin/console b2b:migrate:progress` | Displays the current migration status.  - Use `--watch` for real-time updates. | [Running the Migration](./../execution/running-migration.html#check-migration-status) |
| `bin/console b2b:migrate:rollback` | Reverts the migration, clearing migrated data from target tables while preserving source data. - `-f --force` to skip confirmation  - `--batch-size` to set batch size for deletion.  - Arguments: `component_name_1 component_name_2` to specify components to roll back. | [Troubleshooting](./../execution/troubleshooting.html#rollback-migration) |

INFO

Ensure the message queue worker is running before executing migration commands, as described in [Prerequisites](./../execution/prerequisites.html)

## Configuring Batch Size (Chunk size) [​](#configuring-batch-size-chunk-size)

A **batch size** is a configuration parameter that determines how many records are processed in a single migration operation. It helps manage memory usage and performance during the migration process, allowing for efficient handling of large datasets.

### Current Configuration [​](#current-configuration)

The default batch size is set to 100, but it can be adjusted in several ways:

* By setting the `SHOPWARE_B2B_MIGRATION_BATCH_SIZE` environment variable in the `.env` file.
* By passing the `--batch-size` option when executing the migration command.

### Considerations [​](#considerations)

* **Smaller Batch Size (e.g., 50)**:
  + Reduces memory usage and load on the database and queue.
  + Suitable for environments with limited resources or when debugging.
  + Increases total migration time due to more frequent batch processing.
* **Larger Batch Size (e.g., 500)**:
  + Speeds up migration for large datasets by processing more records per batch.
  + May increase memory and CPU usage, risking timeouts in constrained environments.
* **Testing**: Test the new batch size in a staging environment to ensure stability.

WARNING

Changing the batch size without testing may lead to performance issues or timeouts. Always validate the configuration after modifications.

---

## Role and Permission Mapping

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-suite-migration/references/role-permission-mapping.html

# Role and Permission Mapping [​](#role-and-permission-mapping)

This section documents the role mappings from B2B Suite to B2B Commercial, detailing how permissions and roles are transformed during the migration. Roles define the permissions assigned to employees within the B2B Commercial, and dependencies ensure that related permissions are included to maintain functionality. This reference is essential for developers to understand how roles and permissions are structured in the new system.

## Permission Mapping [​](#permission-mapping)

Below is the mapping of permissions from B2B Suite to B2B Commercial. Each permission from B2B Suite is mapped to a corresponding permission in B2B Commercial.

INFO

Some permissions in B2B Suite do not actually exist in B2B Commercial, because some features are not available in B2B Commercial. In this case, the permission would be mapped to nearest equivalent permission in B2B Commercial.

| B2B Suite Role | B2B Commercial Role | Dependencies | Category |
| --- | --- | --- | --- |
| `address_assign` | `organization_unit.shipping_address.create` | `organization_unit.billing_address.create`, `organization_unit.create`, `organization_unit.update` | Address |
| `address_create` | `organization_unit.shipping_address.create` | `organization_unit.billing_address.create`, `organization_unit.create`, `organization_unit.update` | Address |
| `address_delete` | `organization_unit.shipping_address.delete` | `organization_unit.billing_address.delete` | Address |
| `address_detail` | `organization_unit.shipping_address.update` | `organization_unit.billing_address.update`, `organization_unit.create`, `organization_unit.update` | Address |
| `address_list` | `organization_unit.read` | `organization_unit.create`, `organization_unit.update` | Address |
| `address_update` | `organization_unit.shipping_address.update` | `organization_unit.create`, `organization_unit.update` | Address |
| `budget_assign` | `approval_rule.create` | None | Budget |
| `budget_create` | `approval_rule.create` | None | Budget |
| `budget_delete` | `approval_rule.delete` | None | Budget |
| `budget_detail` | `approval_rule.read` | None | Budget |
| `budget_list` | `approval_rule.read` | None | Budget |
| `budget_update` | `approval_rule.update` | None | Budget |
| `company_list` | `organization_unit.read` | None | Company |
| `contact_create` | `employee.create` | `employee.read`, `employee.edit`, `role.read` | Contact |
| `contact_delete` | `employee.delete` | `employee.read`, `employee.edit`, `role.read` | Contact |
| `contact_detail` | `employee.read` | None | Contact |
| `contact_list` | `employee.read` | None | Contact |
| `contact_update` | `employee.edit` | `employee.read`, `role.read` | Contact |
| `contingent_assign` | `approval_rule.create` | None | Contingent |
| `contingent_create` | `approval_rule.create` | None | Contingent |
| `contingent_delete` | `approval_rule.delete` | None | Contingent |
| `contingent_detail` | `approval_rule.read` | None | Contingent |
| `contingent_list` | `approval_rule.read` | None | Contingent |
| `contingent_update` | `approval_rule.update` | None | Contingent |
| `contingentrule_create` | `approval_rule.create` | None | Contingent Rule |
| `contingentrule_delete` | `approval_rule.delete` | None | Contingent Rule |
| `contingentrule_detail` | `approval_rule.read` | None | Contingent Rule |
| `contingentrule_list` | `approval_rule.read` | None | Contingent Rule |
| `contingentrule_update` | `approval_rule.update` | None | Contingent Rule |
| `fastorder_create` | `quote.request` | None | Order |
| `offer_create` | `quote.request` | None | Order |
| `offer_delete` | `quote.decline` | None | Order |
| `offer_detail` | `quote.read.all` | None | Order |
| `offer_list` | `quote.read.all` | `organization_unit.quote.read` | Order |
| `offer_update` | `quote.request_change` | `quote.accept` | Order |
| `order_create` | `organization_unit.order.read` | None | Order |
| `order_delete` | `pending_order.approve_decline_all` | `pending_order.read_all`, `pending_order.approve_decline` | Order |
| `order_detail` | `order.read.all` | None | Order |
| `order_list` | `order.read.all` | None | Order |
| `order_update` | `order.read.all` | None | Order |
| `role_assign` | `role.create` | `role.read`, `role.edit` | Role |
| `role_create` | `role.create` | `role.read`, `role.edit` | Role |
| `role_delete` | `role.delete` | `role.read`, `role.edit` | Role |
| `role_detail` | `role.edit` | `role.read` | Role |
| `role_list` | `role.read` | None | Role |
| `role_update` | `role.edit` | `role.read` | Role |
| `route_assign` | `role.create` | `role.read`, `role.edit` | Route |
| `route_detail` | `role.edit` | `role.read` | Route |
| `route_list` | `role.read` | None | Route |

INFO

In case you want to override the default mapping, either to add new permissions or change existing ones, you can do so by subscribing to the `Shopware\Commercial\B2B\B2BSuiteMigration\Core\Domain\Event\B2BMigrationPermissionEvent` event. This allows you to customize permission mapping according to your specific requirements.

## Role Mapping [​](#role-mapping)

B2B Suite and B2B Commercial have different approaches to role assignments, impacting how roles are migrated:

* **B2B Suite**: An employee can be assigned multiple roles, each with specific permissions, and may also have individual permissions not tied to a role.
* **B2B Commercial**: An employee is assigned a single role that contains all their permissions.

To handle this difference, the migration process uses the following cases to assign roles to employees in B2B Commercial:

1. **Single Role in B2B Suite**  
    If an employee in B2B Suite has only one role, that role is migrated to B2B Commercial as is, retaining its permissions and dependencies as defined in the role mapping table below.
2. **Multiple Roles in B2B Suite**  
    If an employee has multiple roles, these roles are merged into a single role in B2B Commercial. The new role includes all permissions from the original roles (including their dependencies). The role name is a combination of the original role names, joined with underscores.  
   **Example**: An employee with roles `role1`, `role2`, and `role3` will have a new role named `role1_role2_role3` in B2B Commercial, containing all permissions from these roles.
3. **Multiple Roles with Specific Permissions in B2B Suite**  
    If an employee has multiple roles and additional specific permissions not tied to a role, these are merged into a single role in B2B Commercial. The new role includes all permissions from the roles and the specific permissions. The role name is a combination of the original role names and the employee’s email address, joined with underscores.  
   **Example**: An employee with email `foo@gmail.com`, roles `role1` and `role2`, and specific permissions will have a new role named `role1_role2_foo@gmail.com` in B2B Commercial.

INFO

After migration, you can rename roles in B2B Commercial to more meaningful names, but the permissions will remain unchanged.

---

