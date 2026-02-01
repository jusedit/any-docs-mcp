# Guides Plugins Plugins Plugin Fundamentals

*Scraped from Shopware Developer Documentation*

---

## Plugin fundamentals

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/

# Plugin Fundamentals [​](#plugin-fundamentals)

Shopware plugins are PHP-based extensions that enhance the functionality of the Shopware e-commerce platform. They follow a specific directory structure and have a lifecycle for installation, activation, deactivation, and uninstallation. Plugins can utilize hooks and events to interact with core functionality, and they can have controllers, services, and models to handle specific tasks. Plugin configuration options can be defined, and integration with various parts of Shopware is possible.

You will learn more about it in depth in the following sections.

---

## Add plugin configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/add-plugin-configuration.html

# Add Plugin Configuration [​](#add-plugin-configuration)

The `Shopware plugin system` provides you with the option to create a configuration page for your plugin without any knowledge of templating or the `Shopware Administration`.

## Prerequisites [​](#prerequisites)

To build your own configuration page for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

## Create your plugin configuration [​](#create-your-plugin-configuration)

#### Backend Development - Adding a plugin configuration - YouTube

INFO

This video is part of the online training ["Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma) available on Shopware Academy for **free**.

All you need to do is create a `config.xml` file inside a `Resources/config` directory in your plugin root. The content of the `config.xml` will be dynamically rendered in the Administration. Below you'll find an example structure:

text

```shiki
└── plugins
    └── SwagBasicExample
        ├── src
        │   ├── Resources
        │   │   └── config
        │   │       └── config.xml 
        │   └── SwagBasicExample.php
        └── composer.json
```

## Fill your plugin configuration with settings [​](#fill-your-plugin-configuration-with-settings)

As you now know how to create configurations, you can start to fill it with life using various configuration options.

### Cards in your configuration [​](#cards-in-your-configuration)

The `config.xml` follows a simple syntax. You can organize the content in `<card>` elements. Every `config.xml` must contain a minimum of one `<card>` element and each `<card>` must contain one `<title>` and at least one `<input-field>`. See the minimum `config.xml` below:

xml

```shiki
<!--<plugin root>/src/Resources/config/config.xml-->
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">
    <card>
        <title>Minimal configuration</title>
        <input-field>
            <name>example</name>
        </input-field>
    </card>
</config>
```

Please make sure to specify the `xsi:noNamespaceSchemaLocation` as shown above and fetch the external resource into your IDE if possible. This enables auto-completion and suggestions for this XML file and will therefore help you to prevent issues and bugs.

### Card Titles [​](#card-titles)

A `<card>` `<title>` is translatable, this is managed via the `lang` attribute. By default, the `lang` attribute is set to `en-GB`, to change the locale of a `<title>` just add the attribute as follows:

html

```shiki
    ...
    <card>
        <title>English Title</title>
        <title lang="de-DE">German Titel</title>
    </card>
    ...
```

### Input fields [​](#input-fields)

As you can see above, every `<input-field>` has to contain at least a `<name>` element. The `<name>` element is not translatable and has to be unique, since it will be used as the technical identifier for the config element. The field `<name>` must at least be 4 characters long and consist of only lower and upper case letters. It can contain numbers, but not at first place - see this RegEx pattern: `[a-zA-Z][a-zA-Z0-9]*`

### The different types of input field [​](#the-different-types-of-input-field)

Your `<input-field>` can be of different types, this is managed via the `type` attribute. Unless defined otherwise, your `<input-field>` will be a text field. Below you'll find a list of all available `<input-field type="?">`.

| Type | Configuration settings | Renders | Default value example |
| --- | --- | --- | --- |
| text | [copyable](./add-plugin-configuration.html#copyable), [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text), [length](./add-plugin-configuration.html#text-length-restrictions) | Text field | Some text |
| textarea | [copyable](./add-plugin-configuration.html#copyable), [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text) | Text area | Some more text |
| text-editor | [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text) | HTML editor | Some text with HTML `<div>`tags`</div>` |
| url | [copyable](./add-plugin-configuration.html#copyable), [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text), [length](./add-plugin-configuration.html#text-length-restrictions) | URL field | <https://example.com> |
| password | [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text), [length](./add-plugin-configuration.html#text-length-restrictions) | Password field | \*\*\*\*\*\*\*\* |
| int | [length](./add-plugin-configuration.html#number-length-restrictions) | Number field | 42 |
| float | [length](./add-plugin-configuration.html#number-length-restrictions) | Number field | 42.42 |
| bool |  | Switch | `true` or `false` |
| checkbox |  | Checkbox | `true` or `false` |
| datetime |  | Date-time picker | 2024-04-04T12:00:00.000Z |
| date |  | Date picker | 2024-04-05T00:00:00 |
| time |  | Time picker | 11:00:00 |
| colorpicker |  | Color picker | #189EFF |
| single-select | [options](./add-plugin-configuration.html#options), [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text) | Single-Select box | option\_id |
| multi-select | [options](./add-plugin-configuration.html#options), [placeholder](./add-plugin-configuration.html#label-placeholder-and-help-text) | Multi-Select box | [option\_id1, option\_id2] |

### Input field settings [​](#input-field-settings)

These settings are used to configure your `<input-field>`. **Every `<input-field>` has to start with the `<name>` element.** After the `<name>` element you can configure any of the other settings mentioned above. Beside these settings, they have the following in common: [label](./add-plugin-configuration.html#label-placeholder-and-help-text), [helpText](./add-plugin-configuration.html#label-placeholder-and-help-text), [defaultValue](./add-plugin-configuration.html#defaultvalue), [disabled](./add-plugin-configuration.html#disabled), and [required](./add-plugin-configuration.html#required).

#### Label, placeholder and help text [​](#label-placeholder-and-help-text)

The settings `<label>`, `<placeholder>` and `<helpText>` are used to label and explain your `<input-field>` and are translatable. You define your `<label>`, `<placeholder>` and `<helpText>` the same way as the `<card><title>`, with the `lang` attribute. Please remember, that the `lang` attribute is set to `en-GB` per default.

#### defaultValue [​](#defaultvalue)

Add the `defaultValue` setting to your `<input-field>` to define a default value for it. This value will be imported into the database on installing and updating the plugin. We use [Symfony\Component\Config\Util\XmlUtils](https://github.com/symfony/config/blob/7.1/Util/XmlUtils.php#L211) for casting the values into the correct PHP types.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field type="text">
    <name>textField</name>
    <label>Test field with default value</label>
    <defaultValue>test</defaultValue>
</input-field>
```

#### disabled [​](#disabled)

You can add the `<disabled>` setting to any of your `<input-field>` elements to disable it.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field>
    <name>email</name>
    <disabled>true</disabled>
</input-field>
```

*Please note, `<disabled>` only accepts boolean values.*

#### required [​](#required)

You can add the `<required>` setting to any of your `<input-field>` elements to mark it accordingly.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field>
    <name>email</name>
    <required>true</required>
</input-field>
```

*Please note, `<required>` only accepts boolean values.*

#### copyable [​](#copyable)

You can add the `<copyable>` setting to your `<input-field>` which are of type `text` or extensions of it. This will add a button at the right, which on click copies the content of your `<input-field>` into the clipboard.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field>
    <name>email</name>
    <copyable>true</copyable>
</input-field>
```

*Please note, that `<copyable>` only accepts boolean values*

#### Text length restrictions [​](#text-length-restrictions)

You can add the `<minLength>`/`<maxLength>` settings to your `<input-field>` which are of type `text`, `url` or `password`. With those you can restrict the length of the input.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field type="password">
    <name>token</name>
    <minLength>5</minLength>
    <maxLength>20</maxLength>
</input-field>
```

#### Number length restrictions [​](#number-length-restrictions)

You can add the `<min>`/`<max>` settings to your `<input-field>` which are of type `int` or `float`. With those you can restrict the minimum and maximum value of the input.

Below, you'll find an example of how to use this setting.

html

```shiki
<input-field type="int">
    <name>token</name>
    <min>5</min>
    <max>20</max>
</input-field>
```

#### options [​](#options)

You can use `<options>` to add settings to a `<input-field>` of the types `single-select` and `multi-select`. Each `<option>` represents one setting you can select.

Below you'll find an example.

html

```shiki
<input-field type="single-select">
    <name>mailMethod</name>
    <options>
        <option>
            <id>smtp</id>
            <name>English label</name>
            <name lang="de-DE">German label</name>
        </option>
        <option>
            <id>pop3</id>
            <name>English label</name>
            <name lang="de-DE">German label</name>
        </option>
    </options>
</input-field>
```

Each `<options>` element must contain at least one `<option>` element. Each `<option>` element must contain at least one `<id>` and one `<name>` element. As you can see above, `<name>` elements are translatable via the `lang` attribute.

### Advanced custom input fields [​](#advanced-custom-input-fields)

For more complex and advanced configurations it is possible to declare a `<component name="componentName">` element. This element can render many admin components. It is also possible to render your own admin component which you could deliver with your plugin. The name of the component has to match the components name in the Administration, for example `sw-entity-single-select`. The component also needs a `<name>` element first. All other elements within the component element will be passed to the rendered admin component as properties. For some components you could also use [`label` and `placeholder`](./add-plugin-configuration.html#label-placeholder-and-help-text).

Here are some examples:

### Entity single select for products [​](#entity-single-select-for-products)

html

```shiki
<component name="sw-entity-single-select">
    <name>exampleProduct</name>
    <entity>product</entity>
    <label>Choose a product for the plugin configuration</label>
</component>
```

Stores the ID of the selected product into the system config.

### Entity multi ID select for products [​](#entity-multi-id-select-for-products)

html

```shiki
<component name="sw-entity-multi-id-select">
    <name>exampleMultiProductIds</name>
    <entity>product</entity>
    <label>Choose multiple products IDs for the plugin configuration</label>
</component>
```

Stores an array with IDs of the selected products into the system config.

### Media selection [​](#media-selection)

html

```shiki
<component name="sw-media-field">
    <name>pluginMedia</name>
    <label>Upload media or choose one from the media manager</label>
</component>
```

### Text editor [​](#text-editor)

html

```shiki
<component name="sw-text-editor">
    <name>textEditor</name>
    <label>Write some nice text with WYSIWYG editor</label>
</component>
```

### Snippet field [​](#snippet-field)

html

```shiki
<component name="sw-snippet-field">
    <name>snippetField</name>
    <label>Description</label>
    <snippet>myPlugin.test.snippet</snippet>
</component>
```

Allows you to edit snippet values within the configuration page. This component does not store values in the system config, but changes the translations for the snippet key. **Note: This field is only available from 6.3.4.0 onward.**

### Supported component types [​](#supported-component-types)

Please Note: It is impossible to allow every component in the `config.xml`, due to their complexities. If you can't efficiently resolve your plugin's necessities with, it is probably better to create an own module instead. Therefore, Shopware supports the following components by default (also to be found in the [ConfigValidator class](https://github.com/shopware/shopware/blob/v6.6.7.0/src/Core/Framework/App/Validation/ConfigValidator.php#L18)):

* sw-entity-single-select
* sw-entity-multi-id-select
* sw-media-field
* sw-text-editor
* sw-snippet-field

## Example [​](#example)

Now all that's left to do is to present you a working example `config.xml` and show you the result.

xml

```shiki
<!--<plugin root>/src/Resources/config/config.xml-->
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Basic Configuration</title>
        <title lang="de-DE">Grundeinstellungen</title>

        <input-field>
            <name>email</name>
            <copyable>true</copyable>
            <label>eMail address</label>
            <label lang="de-DE">E-Mailadresse</label>
            <placeholder>you@example.com</placeholder>
            <placeholder lang="de-DE">du@beispiel.de</placeholder>
            <helpText>Please fill in your personal eMail address</helpText>
            <helpText lang="de-DE">Bitte trage deine persönliche E-Mailadresse ein</helpText>
        </input-field>

        <input-field type="single-select">
            <name>mailMethod</name>
            <options>
                <option>
                    <id>smtp</id>
                    <name>English smtp</name>
                    <name lang="de-DE">German smtp</name>
                </option>
                <option>
                    <id>pop3</id>
                    <name>English pop3</name>
                    <name lang="de-DE">German pop3</name>
                </option>
            </options>
            <defaultValue>smtp</defaultValue>
            <label>Mail method</label>
            <label lang="de-DE">Versand-Protokoll</label>
        </input-field>
    </card>

    <card>
        <title>Advanced Configuration</title>
        <title lang="de-DE">Erweiterte Einstellungen</title>

        <input-field type="password">
            <name>secret</name>
            <label>Secret token</label>
            <label lang="de-DE">Geheimschlüssel</label>
            <helpText>Your secret token for xyz...</helpText>
            <helpText lang="de-DE">Dein geheimer Schlüssel für xyz...</helpText>
        </input-field>
    </card>
</config>
```

## Add values to your configuration [​](#add-values-to-your-configuration)

After adding your input fields to the `config.xml`, you can add values to your configuration. To do so, navigate from the sidebar to the `Extensions` > `My extensions` > `Apps` tab and click `Configure`. Now you can see the `Configuration` tab and fill in the values for your input fields.

## Next steps [​](#next-steps)

Now you've added your own plugin configuration. But how do you actually read which configurations the shop owner used? This will be covered in our guide about [Using the plugin configuration](./use-plugin-configuration.html).

---

## Use plugin configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/use-plugin-configuration.html

# Use Plugin Configuration [​](#use-plugin-configuration)

In our guide on how to [add a plugin configuration](./add-plugin-configuration.html), you can learn how to provide this possibility to use configuration options in your plugins. This guide will aid you on how to then use this configuration in your plugin.

## Prerequisites [​](#prerequisites)

In order to add a plugin configuration, you sure need to provide your plugin first. However, you won't learn to create a plugin in this guide. Head over to our [plugin base guide](./../plugin-base-guide.html) to create your plugin first. It is also recommended to know how to setup a [plugin configuration](./add-plugin-configuration.html) in the first instance. In this example, the configurations will be read inside of a subscriber, so knowing the [Listening to events](./listening-to-events.html) guide will also be helpful.

## Overview [​](#overview)

The plugin in this example already knows a subscriber, which listens to the `product.loaded` event and therefore will be called every time a product is loaded.

php

```shiki
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded'
        ];
    }

    public function onProductsLoaded(EntityLoadedEvent $event): void
    {
        // Do stuff with the product
    }
}
```

For this guide, a very small plugin configuration file is available as well:

xml

```shiki
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Minimal configuration</title>
        <input-field>
            <name>example</name>
        </input-field>
    </card>
</config>
```

Just a simple input field with the technical name `example`. This will be necessary in the next step.

## Reading the configuration [​](#reading-the-configuration)

Let's get to the important part. Reading the plugin configuration is based on the `Shopware\Core\System\SystemConfig\SystemConfigService`. This service is responsible for reading all configs from Shopware 6, such as the plugin configurations.

Inject this service into your subscriber using the [DI container](https://symfony.com/doc/current/service_container.html).

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\MySubscriber">
            <argument type="service" id="Shopware\Core\System\SystemConfig\SystemConfigService" />
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Note the new `argument` being provided to your subscriber. Now create a new field in your subscriber and pass in the `SystemConfigService`:

php

```shiki
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

...
use Shopware\Core\System\SystemConfig\SystemConfigService;

class MySubscriber implements EventSubscriberInterface
{
    private SystemConfigService $systemConfigService;

    public function __construct(SystemConfigService $systemConfigService)
    {
        $this->systemConfigService = $systemConfigService;
    }

    public static function getSubscribedEvents(): array
    {
        ...
    }
    ...
}
```

So far, so good. The `SystemConfigService` is now available in your subscriber.

This service comes with a `get` method to read the configurations. The first idea would be to simply call `$this->systemConfigService->get('example')` now, wouldn't it? Simply using the technical name you've previously set for the configuration.

But what would happen, if there were more plugins providing the same technical name for their very own configuration field? How would you access the proper field, how would you prevent plugin conflicts?

That's why the plugin configurations are always prefixed. By default, the pattern is the following: `<BundleName>.config.<configName>`. Thus, it would be `SwagBasicExample.config.example` here.

php

```shiki
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

...

class MySubscriber implements EventSubscriberInterface
{
    ...
    public function onProductsLoaded(EntityLoadedEvent $event): void
    {
        $exampleConfig = $this->systemConfigService->get('SwagBasicExample.config.example', $salesChannelId);
    }
}
```

INFO

Set the `saleschannelId` to `null` for the plugin configuration to be used by all Sales Channels else set to the corresponding Sales Channel ID.

## Reading configuration in JavaScript [​](#reading-configuration-in-javascript)

While the above examples show how to read plugin configuration in PHP, you might also need to access these values in JavaScript for Administration extensions or Storefront functionality.

### Administration API access [​](#administration-api-access)

To access your plugin's configuration from JavaScript in the Administration, you should use the `systemConfigApiService` which wraps the system-config endpoints.

#### Using injection in Vue components [​](#using-injection-in-vue-components)

javascript

```shiki
// Example: Reading plugin configuration in Administration Vue component
export default Shopware.Component.wrapComponentConfig({
    inject: ['systemConfigApiService'],
    
    async created() {
        await this.loadPluginConfig();
    },
    
    methods: {
        async loadPluginConfig() {
            try {
                const config = await this.systemConfigApiService.getValues('SwagBasicExample.config');
                const exampleValue = config['SwagBasicExample.config.example'];
                
                console.log('Plugin configuration value:', exampleValue);
                return exampleValue;
            } catch (error) {
                console.error('Error fetching plugin configuration:', error);
            }
        }
    }
});
```

#### Using direct service access [​](#using-direct-service-access)

javascript

```shiki
// Example: Reading plugin configuration using direct service access
async function getPluginConfig() {
    try {
        const systemConfigApiService = Shopware.ApiService.getByName('systemConfigApiService');
        const config = await systemConfigApiService.getValues('SwagBasicExample.config');
        const exampleValue = config['SwagBasicExample.config.example'];
        
        console.log('Plugin configuration value:', exampleValue);
        return exampleValue;
    } catch (error) {
        console.error('Error fetching plugin configuration:', error);
    }
}
```

WARNING

Your plugin needs the `system_config:read` permission to access this API endpoint.

### Storefront template access [​](#storefront-template-access)

In Storefront templates, you can use the `config()` twig function to access plugin configuration values directly without making API calls:

twig

```shiki
{# Example: Reading plugin configuration in Storefront templates #}
{% set exampleValue = config('SwagBasicExample.config.example') %}

{% if exampleValue %}
    <div class="plugin-config-value">{{ exampleValue }}</div>
{% endif %}
```

### Storefront JavaScript access [​](#storefront-javascript-access)

For Storefront JavaScript plugins, you can pass configuration values from Twig templates to your JavaScript code:

twig

```shiki
{# In your Storefront template #}
<script>
    window.pluginConfig = {
        example: {{ config('SwagBasicExample.config.example')|json_encode|raw }}
    };
</script>
```

javascript

```shiki
// In your Storefront JavaScript plugin
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // Access the configuration value passed from Twig
        const exampleConfig = window.pluginConfig?.example;
        
        if (exampleConfig) {
            console.log('Plugin configuration:', exampleConfig);
            // Use the configuration value in your plugin logic
        }
    }
}
```

---

## Database migrations

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/database-migrations.html

# Database Migrations [​](#database-migrations)

## Overview [​](#overview)

In this guide, you'll learn what migrations are and how to use them. Migrations are PHP classes used to manage incremental and reversible database schema changes. Shopware comes with a pre-built Migration System, to take away most of the work for you. Throughout this guide, you will find the `$` symbol representing your command line.

## Prerequisites [​](#prerequisites)

To add your own database migrations for your plugin, you first need a plugin as a base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

INFO

Refer to this video on **[Database migrations](https://www.youtube.com/watch?v=__pWwaK6lxw)**. Also, available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## File structure [​](#file-structure)

By default, Shopware 6 is looking for migration files in a directory called `Migration` relative to your plugin's base class.

text

```shiki
└── plugins
    └── SwagBasicExample
        └── src
            ├── Migration
            │   └── Migration1546422281ExampleDescription.php
            └── SwagBasicExample.php
```

As you can see there is one file in the `<plugin root>/src/Migration` directory. Below you find a break down of what each part of its name means.

| File Name Snippet | Meaning |
| --- | --- |
| Migration | Each migration file has to start with Migration |
| 1546422281 | A Timestamp used to make migrations incremental |
| ExampleDescription | A descriptive name for your migration |

### Customizing the migration path / namespace [​](#customizing-the-migration-path-namespace)

You are also able to change the migration directory. This is done by choosing another namespace for your migrations, which can be changed by overwriting your plugin's `getMigrationNamespace()` method in the plugin base class:

php

```shiki
public function getMigrationNamespace(): string
{
    return 'Swag\BasicExample\MyMigrationNamespace';
}
```

Since the path is read from the namespace, your Migration directory would have to be named `MyMigrationNamespace` now.

## Generate migration skeleton [​](#generate-migration-skeleton)

To generate the boilerplate code for your migration, you have to open your Shopware root directory in your terminal and execute the command `database:create-migration`. Below you can see the command used in this example to create the migration seen above in the file structure.

bash

```shiki
$ ./bin/console database:create-migration -p SwagBasicExample --name ExampleDescription
```

Below you'll find a breakdown of the command.

| Command Snippet | Meaning |
| --- | --- |
| ./bin/console | Calls the executable Symfony console application |
| database:create-migration | The command to create a new migration |
| -p your\_plugin\_name | -p creates a new migration for the plugin with the name provided |
| --name your\_descriptive\_name | Appends the provided string after the timestamp |

*Note: If you create a new migration yourself, the timestamp will vary.*

If you take a look at your created migration, it should look similar to this:

php

```shiki
// <plugin root>/src/Migration/Migration1611740369ExampleDescription.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1611740369ExampleDescription extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1611740369;
    }

    public function update(Connection $connection): void
    {
        // implement update
    }

    public function updateDestructive(Connection $connection): void
    {
        // implement update destructive
    }
}
```

As you can see, your migration contains three methods:

* getCreationTimestamp()
* update()
* updateDestructive()

There is no need to change `getCreationTimestamp()`, it returns the timestamp that's also part of the file name. In the `update()` method you implement non-destructive changes which should always be **reversible**. The `updateDestructive()` method is the follow up step, that is run after `update()` and used for **destructive none reversible changes**, like dropping columns or tables. Destructive migrations are only executed explicitly.

INFO

You do not add instructions to revert your migrations within the migration class itself. `updateDestructive` is not meant to revert instructions in `update`. Reverting changes in the database is done explicitly in plugin lifecycle method `uninstall`. Read more about [it here](./plugin-lifecycle.html#uninstall).

Here's an example of a non-destructive migration, creating a new table:

php

```shiki
// <plugin root>/src/Migration/Migration1611740369ExampleDescription.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1611740369ExampleDescription extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1611740369;
    }

    public function update(Connection $connection): void
    {
        $query = <<<SQL
CREATE TABLE IF NOT EXISTS `swag_basic_example_general_settings` (
    `id`                INT             NOT NULL,
    `example_setting`   VARCHAR(255)    NOT NULL,
    PRIMARY KEY (id)
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;
SQL;

        $connection->executeStatement($query);
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

## Generating a complete migration for an entity [​](#generating-a-complete-migration-for-an-entity)

Shopware can also generate the complete migration, including the SQL statements for you, based on the entity definitions.

bash

```shiki
$ ./bin/console dal:migration:create --bundle=SwagBasicExample --entities=your_entity,your_other_entity
```

This command will generate a new migration file including the `CREATE TABLE` or `ALTER TABLE` statements to get the DB schema into a state that matches the entity definitions.

| Option | Meaning |
| --- | --- |
| --bundle | The name of the plugin, when not provided the command will generate a migration in the core |
| --entities | Comma-seperated list of the entities it should create migrations for, it will generate one migration file per entity |

*Note: Your plugin has to be activated, otherwise your custom entity definition cannot be found.*

## Execute migration [​](#execute-migration)

When you install your plugin, the migration directory is added to a MigrationCollection and all migrations are executed. Also, when you update a plugin via the Plugin Manager, all **new** migrations are executed. If you want to perform a migration manually as part of your development process, simply create it after installing your plugin. This way, your plugin migration directory will already be registered during the installation process and you can run any newly created migration by hand using one of the following commands.

WARNING

When updating a plugin, do not change a migration that was already executed, since every migration is only run once.

| Command | Arguments | Usage |
| --- | --- | --- |
| database:migrate | identifier (optional) | Calls the update() methods of unhandled migrations |
| database:migrate-destructive | identifier (optional) | Calls the updateDestructive() methods of unhandled migrations |

The identifier argument is used to decide which migrations should be executed. Per default, the identifier is set to run Shopware Core migrations. To run your plugin migrations, set the identifier argument to your plugin's bundle name, in this example `SwagBasicExample`.

bash

```shiki
$ ./bin/console database:migrate SwagBasicExample --all
```

## Advanced migration control [​](#advanced-migration-control)

Once you have become familiar with the migration process and the development flow, you may want to have finer control over the migrations performed during the installation and update. In this case the `MigrationCollection` which is only filled with your specific migrations, can be accessed via the `InstallContext` and all its subclasses (UpdateContext, ActivateContext, ...). A plugin must reject the automatic execution of migrations in order to have control over the migrations that are executed.

Therefore, a typical update method might look more like this:

php

```shiki
    public function update(UpdateContext $updateContext): void
    {
        $updateContext->setAutoMigrate(false); // disable auto migration execution

        $migrationCollection = $updateContext->getMigrationCollection();

        // execute all DESTRUCTIVE migrations until and including 2019-11-01T00:00:00+00:00
        $migrationCollection->migrateDestructiveInPlace(1572566400);

        // execute all UPDATE migrations until and including 2019-12-12T09:30:51+00:00
        $migrationCollection->migrateInPlace(1576143014);
    }
```

If you don't use the Shopware migration system, an empty collection (NullObject) will be in the context.

---

## Dependency injection

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/dependency-injection.html

# Dependency Injection [​](#dependency-injection)

## Overview [​](#overview)

In this guide you'll learn how to inject services into other services. You can read more about injecting services in the [Symfony documentation](https://symfony.com/doc/current/service_container.html#injecting-services-config-into-a-service).

## Prerequisites [​](#prerequisites)

To add your own custom service for your plugin, you first need a plugin as a base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

Furthermore, you need a working service. Therefore, you can refer to [Adding a custom service](./add-custom-service.html) guide.

INFO

Refer to this video on **[Injecting services into a command](https://www.youtube.com/watch?v=Z4kyx9J1xaQ)** explaining DI based on the example of a custom CLI command. It is also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Injecting another service [​](#injecting-another-service)

This example will be about injecting the `SystemConfigService` into our `ExampleService`. First, we are preparing the `ExampleService` PHP class. Add the `SystemConfigService` as parameter to the constructor of the service class.

PLUGIN\_ROOT/src/Service/ExampleService.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\System\SystemConfig\SystemConfigService;

class ExampleService
{
    public function __construct(
        private SystemConfigService $systemConfigService
    ) {
    }

    public function getShopname(SalesChannelContext $context): string
    {
        return $this->systemConfigService->getString('core.basicInformation.shopName', $context->getSalesChannel()->getId());
    }
}
```

### Using autowire and autoconfigure [​](#using-autowire-and-autoconfigure)

If you previously declared `autowire` and `autoconfigure` in your `services.xml` file, you do not need to do anything else. The `SystemConfigService` will be injected into the `ExampleService` automatically.

### Explicit declaration [​](#explicit-declaration)

If you declared the service explicitly, you need to add the `SystemConfigService` as argument to the service.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService">
            <argument type="service" id="Shopware\Core\System\SystemConfig\SystemConfigService"/>
        </service>
    </services>
</container>
```

---

## Listening to events

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/listening-to-events.html

# Listening to Events [​](#listening-to-events)

A way to listen to events in Symfony projects is via an [event subscriber,](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-subscriber) which is a class that defines one or more methods that listen to one or various events. It is thus the same in Shopware, so this article will guide you on how to create event subscriber in your Shopware extension.

## Prerequisites [​](#prerequisites)

In order to build your own subscriber for your plugin, of course you first need a plugin as base. To create an own plugin, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

INFO

Refer to this video on **[Live coding example with product.loaded event.](https://www.youtube.com/watch?v=cJDaiuyjKJk)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Creating your own subscriber [​](#creating-your-own-subscriber)

### Plugin base class [​](#plugin-base-class)

Registering a custom subscriber requires to load a `services.xml` file with your plugin. This is done by either placing a file with name `services.xml` into a directory called `src/Resources/config/`.

Basically, that's it already if you're familiar with [Symfony subscribers](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-subscriber). Don't worry, we got you covered here as well.

### Creating your new subscriber class [​](#creating-your-new-subscriber-class)

To start creating a subscriber, we need to create a class first implementing EventSubscriberInterface. As mentioned above, such a subscriber for Shopware 6 looks exactly the same as in Symfony itself.

Therefore, this is how your subscriber could then look like:

php

```shiki
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        // Return the events to listen to as array like this:  <event to listen to> => <method to execute>
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded'
        ];
    }

    public function onProductsLoaded(EntityLoadedEvent $event)
    {
        // Do something
        // E.g. work with the loaded entities: $event->getEntities()
    }
}
```

In this example, the subscriber would be located in the `<plugin root>/src/Subscriber` directory.

The subscriber is now listening for the `product.loaded` event to trigger.

Some entities, like orders or products, are versioned. This means that some events are dispatched multiple times for different versions, but they belong to the same entity. Therefore, you can check the version of the context to make sure you're only reacting to the live version.

php

```shiki
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_WRITTEN_EVENT => 'onProductWritten'
        ];
    }

    public function onProductWritten(EntityWrittenEvent $event)
    {
        if ($event->getContext()->getVersionId() !== Defaults::LIVE_VERSION) {
            return;
        }
        // Do something
    }
}
```

Unfortunately, your subscriber is not even loaded yet - this will be done in the previously registered `services.xml` file.

### Registering your subscriber via services.xml [​](#registering-your-subscriber-via-services-xml)

Registering your subscriber to Shopware 6 is also as simple as it is in Symfony. You're simply registering your (subscriber) service by mentioning it in the `services.xml`. The only difference to a normal service is that you need to add the `kernel.event_subscriber` tag to your subscriber for it to be recognized as such.

php

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\MySubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

That's it, your subscriber service is now automatically loaded at runtime, and it should start listening to the mentioned events to be dispatched.

---

## Add custom service

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/add-custom-service.html

# Add Custom Service [​](#add-custom-service)

## Overview [​](#overview)

In this guide you'll learn how to create a custom service using the Symfony [DI Container](https://symfony.com/doc/current/service_container.html).

## Prerequisites [​](#prerequisites)

To add your own custom service for your plugin, you first need a plugin as a base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

## Adding service [​](#adding-service)

For adding a custom service, you need to provide a `services.xml` file in your plugin. Place a file with name `services.xml` into a directory called `src/Resources/config/`.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
    </services>
</container>
```

Now you have two possibilities to add a service to your plugin.

### Using autowire and autoconfigure [​](#using-autowire-and-autoconfigure)

Set `autowire` and `autoconfigure` to `true` in your `services.xml` file. Symfony will then automatically register your service. Read more about it in the [Symfony docs](https://symfony.com/doc/current/service_container.html#creating-configuring-services-in-the-container).

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <defaults autowire="true" autoconfigure="true"/>
        <prototype namespace="Swag\BasicExample\" resource="../../" exclude="../../{Resources,Migration,*.php}"/>
    </services>
</container>
```

Now every PHP class in the `src` directory of your plugin will be registered as a service. The directory `Resources` and `Migration` are excluded, as they usually should not contain services.

### Explicit declaration [​](#explicit-declaration)

Instead of autowiring and autoconfiguring, you can also declare your service explicitly. Use this option if you want to have more control over your service.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService"/>
    </services>
</container>
```

### Actual service class [​](#actual-service-class)

Then this is what your service could look like:

PLUGIN\_ROOT/src/Service/ExampleService.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

class ExampleService
{
    public function doSomething(): void
    {
        ...
    }
}
```

INFO

By default, all services in Shopware 6 are marked as *private*. Read more about [private and public services](https://symfony.com/doc/current/service_container.html#public-versus-private-services).

## Alternatives to XML [​](#alternatives-to-xml)

Symfony offers two other file formats to define your services: YAML and PHP. In Shopware, it is also possible to use one of these. Choose the one that suits you best.

## Next steps [​](#next-steps)

You have now created your own custom service. In the same manner, you can create other important plugin classes, such as [commands](./add-custom-commands.html), [scheduled tasks](./add-scheduled-task.html) or a [subscriber to listen to events](./listening-to-events.html).

Furthermore, we also have a guide explaining how to [customize an existing service](./adjusting-service.html) instead.

---

## Adjusting a service

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/adjusting-service.html

# Adjusting a Service [​](#adjusting-a-service)

## Overview [​](#overview)

In this guide you'll learn how to adjust a service. You can read more about service decoration in the [Symfony documentation](https://symfony.com/doc/current/service_container/service_decoration.html).

## Prerequisites [​](#prerequisites)

In order to add your own custom service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

INFO

Refer to this video on **[Decorating services](https://www.youtube.com/watch?v=Rgf4c9rd1kw)** explaining service decorations with an easy example. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Decorating the service [​](#decorating-the-service)

First of all we have to create a new service for this example which gets decorated in the next step. Then we have to add a new service to our `services.xml` with the attribute `decorates` pointing to our service we want to decorate. Next we have to add our service decorator as argument, but we append an `.inner` to the end of the service to keep the old one as reference.

Here's our example `services.xml`:

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService" />

        <service id="Swag\BasicExample\Service\ExampleServiceDecorator" decorates="Swag\BasicExample\Service\ExampleService">
            <argument type="service" id="Swag\BasicExample\Service\ExampleServiceDecorator.inner" />
        </service>
    </services>
</container>
```

Now we have to define an abstract class because it's more beautiful and not so strict like interfaces. With an abstract class we can add new functions easier, you can read more about this at the end of this article. The abstract class has to include an abstract function called `getDecorated()` which has the return type of our instance.

INFO

To avoid misunderstandings: The abstract service class and the implementation of it is not part of the decoration process itself and most of the times comes either from the Shopware core or from a plugin you want to extend. They are added here to have an example to decorate.

Therefore, this is how your abstract class could then look like:

php

```shiki
// <plugin root>/src/Service/AbstractExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

abstract class AbstractExampleService
{
    abstract public function getDecorated(): AbstractExampleService; 

    abstract public function doSomething(): string;
}
```

Now we have our abstract class, but no service which uses it. So we create our `ExampleService` which extends from our `AbstractExampleService`. In our service the `getDecorated()` function has to throw an `DecorationPatternException` because it has no decoration yet.

Therefore, your service could then look like this:

php

```shiki
// <plugin root>/src/Service/ExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;

class ExampleService extends AbstractExampleService
{
    public function getDecorated(): AbstractExampleService
    {
        throw new DecorationPatternException(self::class);
    }

    public function doSomething(): string
    {
        return 'Did something.';
    }
}
```

The last step is creating our decorated service called `ExampleServiceDecorator` in this example. Our decorated service has to extend from the `AbstractExampleService` and the constructor has to accept an instance of `AbstractExampleService`. Furthermore, the `getDecorated()` function has to return the decorated service passed into the constructor.

Your service could then look like below:

php

```shiki
// <plugin root>/src/Service/ExampleServiceDecorator.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

class ExampleServiceDecorator extends AbstractExampleService
{
    private AbstractExampleService $decoratedService;

    public function __construct(AbstractExampleService $exampleService)
    {
        $this->decoratedService = $exampleService;
    }

    public function getDecorated(): AbstractExampleService
    {
        return $this->decoratedService;
    }

    public function doSomething(): string
    {
        $originalResult = $this->decoratedService->doSomething();

        return $originalResult . ' Did something additionally.';
    }
}
```

## Adding new functions to an existing service [​](#adding-new-functions-to-an-existing-service)

If you plan to add new functions to your service, it is recommended to add them as normal public functions due to backwards compatibility, if you decorate the service at several places. In this example we add a new function called `doSomethingNew()` which first calls the `getDecorated()` and then our new function `doSomethingNew()` because if our decorator does not implement it yet, it will call it from the parent. The advantage of adding it as normal public function is that you can implement it step by step into your other services without any issues. After you have implemented the function in every service decorator, you can make it abstract for the next release. If you add it directly as an abstract function, you will get errors because the function is required for every service decorator.

Here's our example abstract class:

php

```shiki
// <plugin root>/src/Service/AbstractExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

abstract class AbstractExampleService
{
    abstract public function getDecorated(): AbstractExampleService; 

    abstract public function doSomething(): string;

    public function doSomethingNew(): string
    {
        return $this->getDecorated()->doSomethingNew();
    }
}
```

After we have implemented our new function in the abstract class, we implement it in our service too.

php

```shiki
// <plugin root>/src/Service/ExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;

class ExampleService extends AbstractExampleService
{
    public function getDecorated(): AbstractExampleService
    {
        throw new DecorationPatternException(self::class);
    }

    public function doSomething(): string
    {
        return 'Did something.';
    }

    public function doSomethingNew(): string
    {
        return 'Did something new.';
    }
}
```

---

## Add plugin dependencies

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/add-plugin-dependencies.html

# Add Plugin Dependencies [​](#add-plugin-dependencies)

New in Shopware 6 is the possibility to properly require on other plugins to be in the system. This is done using the `require` feature from composer. Further information about this can be found in the [official composer documentation](https://getcomposer.org/doc/04-schema.md#package-links).

## Setup [​](#setup)

Each plugin for Shopware 6 has to own a `composer.json` file for it to be a valid plugin. Creating a plugin is not explained here, make sure to read our [Plugin base guide](./../plugin-base-guide.html) first.

Since every plugin has to own a `composer.json` file, you can simply refer to this plugin by its technical name and its version mentioned in the respective plugin's `composer.json`.

So, those are example lines of the `SwagBasicExample` plugin's `composer.json`:

json

```shiki
{
    "name": "swag/swag-basic-example",
    "description": "Plugin quick start plugin",
    "version": "v1.0.0",
    ...
}
```

Important to note is the `name` as well as the `version` mentioned here, the rest of the file is not important for this case here. You're going to need those two information to require them in your own plugin.

In order to require the `SwagBasicExample` plugin now, you simply have to add these two information to your own `composer.json` as a key value pair:

javascript

```shiki
// <plugin root>/composer.json
{
    "name": "swag/plugin-dependency",
    "description": "Plugin requiring other plugins",
    "version": "v1.0.0",
    "type": "shopware-platform-plugin",
    "license": "MIT",
    "authors": [
        {
            "name": "shopware AG",
            "role": "Manufacturer"
        }
    ],
    "require": {
        "shopware/core": "6.1.*",
        "swag/SwagBasicExample": "v1.0.0"
    },
    "extra": {
        "shopware-plugin-class": "Swag\\PluginDependency\\PluginDependency",
        "label": {
            "de-DE": "Plugin mit Plugin-Abhängigkeiten",
            "en-GB": "Plugin with plugin dependencies"
        },
        "description": {
            "de-DE": "Plugin mit Plugin-Abhängigkeiten",
            "en-GB": "Plugin with plugin dependencies"
        }
    },
    "autoload": {
        "psr-4": {
            "Swag\\PluginDependency\\": "src/"
        }
    }
}
```

Have a detailed look at the `require` keyword, which now requires both the Shopware 6 version, which **always** has to be mentioned in your `composer.json`, as well as the previously mentioned plugin and its version. Just as in composer itself, you can also use version wildcards, such as `v1.0.*` to only require the other plugin's minor version to be 1.1, not taking the patch version into account when it comes to find the matching plugin version.

Now your plugin isn't installable anymore, until that requirement is fulfilled.

## More interesting topics [​](#more-interesting-topics)

* [Using Composer dependencies](./using-composer-dependencies.html)
* [Using NPM dependencies](./using-npm-dependencies.html)

---

## Add custom CLI commands

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/add-custom-commands.html

# Add Custom CLI Commands [​](#add-custom-cli-commands)

To ease development tasks, Shopware contains the Symfony commands functionality. This allows (plugin-) developers to define new commands executable via the Symfony console at `bin/console`. The best thing about commands is, that they're more than just simple standalone PHP scripts - they integrate into Symfony and Shopware, so you've got access to all the functionality offered by both of them.

Creating a command for Shopware 6 via a plugin works exactly like you would add a command to Symfony. Make sure to have a look at the Symfony commands guide:

[Console Commands (Symfony Docs)](https://symfony.com/doc/current/console.html\#registering-the-command)

## Prerequisites [​](#prerequisites)

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../plugin-base-guide)

The main requirement here is to have a `services.xml` file loaded in your plugin. This can be achieved by placing the file into a `Resources/config` directory relative to your plugin's base class location.

INFO

Refer to this video on custom **[Creating a CLI command](https://www.youtube.com/watch?v=OL_qNVLLyaI)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Registering your command [​](#registering-your-command)

From here on, everything works exactly like in Symfony itself. Commands are recognised by Shopware, once they're tagged with the `console.command` tag in the [dependency injection](./dependency-injection.html) container. So to register a new command, just add it to your plugin's `services.xml` and specify the `console.command` tag:

html

```shiki
<services>
   <!-- ... -->

   <service id="Swag\BasicExample\Command\ExampleCommand">
       <tag name="console.command"/>
   </service>
</services>
<!-- ... -->
```

Here's a full example `services.xml` which registers your custom command:

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Command\ExampleCommand">
            <tag name="console.command"/>
        </service>
    </services>
</container>
```

Your command's class should extend from the `Symfony\Component\Console\Command\Command` class, here's an example:

php

```shiki
// <plugin root>/src/Command/ExampleCommand.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Attribute\AsCommand;

// Command name
#[AsCommand(name: 'swag-commands:example')]
class ExampleCommand extends Command
{
    // Provides a description, printed out in bin/console
    protected function configure(): void
    {
        $this->setDescription('Does something very special.');
    }

    // Actual code executed in the command
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $output->writeln('It works!');

        return Command::SUCCESS;
    }
}
```

This command is of course only a basic example, so feel free to experiment. As stated above, you now have access to all the functionality offered by Symfony and Shopware.

INFO

For inspiration, maybe have a look at the Symfony documentation - you may for example use [tables](https://symfony.com/doc/current/components/console/helpers/table.html), [progress bars](https://symfony.com/doc/current/components/console/helpers/progressbar.html), or [custom formats](https://symfony.com/doc/current/components/console/helpers/formatterhelper.html).

### Running commands [​](#running-commands)

Commands are run via the `bin/console` executable. To list all available commands, run `bin/console list`:

text

```shiki
$: php bin/console list
Symfony 4.4.4 (env: dev, debug: true)

Usage:
  command [options] [arguments]

Options:
  -h, --help            Display this help message
  -q, --quiet           Do not output any message
  -V, --version         Display this application version
      --ansi            Force ANSI output
      --no-ansi         Disable ANSI output
  -n, --no-interaction  Do not ask any interactive question
  -e, --env=ENV         The Environment name. [default: "dev"]
      --no-debug        Switches off debug mode.
  -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

Available commands:
  about                                   Displays information about the current project
  help                                    Displays help for a command
  list                                    Lists commands
 feature
  feature:dump                            Creating json file with feature config for js testing and hot reloading capabilities.
 assets
  assets:install                          
 bundle
  bundle:dump                             Creates a json file with the configuration for each active Shopware bundle.
 cache
  cache:clear                             Clears the cache
  cache:pool:clear                        Clears cache pools
  cache:pool:delete                       Deletes an item from a cache pool
  cache:pool:list                         List available cache pools
  cache:pool:prune                        Prunes cache pools
  cache:warmup                            Warms up an empty cache
 [...]
```

Each command usually has a namespace like `cache`, so to clear the cache you would execute `php bin/console cache:clear`. If you would like to learn more about commands in general, have a look at [this article](https://symfony.com/doc/current/console.html) in the Symfony documentation.

## More interesting topics [​](#more-interesting-topics)

* [Adding a scheduled task](./add-scheduled-task.html)

---

## Add scheduled task

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/add-scheduled-task.html

# Add Scheduled Task [​](#add-scheduled-task)

## Overview [​](#overview)

Quite often one might want to run any type of code on a regular basis, e.g. to clean up very old entries every once in a while, automatically. Usually known as "Cronjobs", Shopware 6 supports a `ScheduledTask` for this.

## Prerequisites [​](#prerequisites)

This guide is built upon our [plugin base guide](./../plugin-base-guide.html), but that one is not mandatory. Knowing how the `services.xml` file in a plugin works is also helpful, which will be taught in our guides about [Dependency Injection](./dependency-injection.html) and [Creating a service](./add-custom-service.html). It is shortly explained here as well though, so no worries!

INFO

Refer to this video on **[Adding scheduled tasks](https://www.youtube.com/watch?v=88S9P3x6wYE)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Registering scheduled task in the DI container [​](#registering-scheduled-task-in-the-di-container)

A `ScheduledTask` and its respective `ScheduledTaskHandler` are registered in a plugin's `services.xml`. For it to be found by Shopware 6 automatically, you need to place the `services.xml` file in a `Resources/config/` directory, relative to the location of your plugin's base class. The path could look like this: `<plugin root>/src/Resources/config/services.xml`.

Here's an example `services.xml` containing a new `ScheduledTask` as well as a new `ScheduledTaskHandler`:

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">
    <services>
        <service id="Swag\BasicExample\Service\ScheduledTask\ExampleTask">
            <tag name="shopware.scheduled.task" />
        </service>
        <service id="Swag\BasicExample\Service\ScheduledTask\ExampleTaskHandler">
            <argument type="service" id="scheduled_task.repository" />
            <argument type="service" id="logger"/>
            <tag name="messenger.message_handler" />
        </service>
    </services>
</container>
```

Note the tags required for both the task and its respective handler, `shopware.scheduled.task` and `messenger.message_handler`. Your custom task will now be saved into the database once your plugin is activated.

## ScheduledTask and its handler [​](#scheduledtask-and-its-handler)

As you might have noticed, the `services.xml` file tries to find both the task itself as well as the new task handler in a directory called `Service/ScheduledTask`. This naming is up to you, Shopware 6 decided to use this name though.

Here's the an example `ScheduledTask`:

php

```shiki
// <plugin root>/src/Service/ScheduledTask/ExampleTask.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service\ScheduledTask;

use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTask;

class ExampleTask extends ScheduledTask
{
    public static function getTaskName(): string
    {
        return 'swag.example_task';
    }

    public static function getDefaultInterval(): int
    {
        return 300; // 5 minutes
    }
}
```

Your `ExampleTask` class has to extend from the `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTask` class, which will force you to implement two methods:

* `getTaskName`: The technical name of your task. Make sure to add a vendor prefix to your custom task, to prevent collisions with other plugin's scheduled tasks. In this example this is `swag`.
* `getDefaultInterval`: The interval in seconds at which your scheduled task should be executed.

And that's it for the `ExampleTask` class.

Following will be the respective task handler:

php

```shiki
// <plugin root>/src/Service/ScheduledTask/ExampleTaskHandler.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service\ScheduledTask;

use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskHandler;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler(handles: ExampleTask::class)]
class ExampleTaskHandler extends ScheduledTaskHandler
{
    public function run(): void
    {
        // ...
    }
}
```

The task handler, `ExampleTaskHandler` as defined previously in your `services.xml`, will be annotated with `AsMessageHandler` handling the `ExampleTask` class. In addition, the `ScheduledTaskHandler` has to extend from the class `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskHandler`. This also comes with one method that you need to implement first:

* `run`: This method is executed once your scheduled task is executed. Do everything, that your task is supposed to do here. In this example, it will just create a new file.

Now every five minutes, your task will be executed and it will print an output every time now.

## Executing the scheduled task [​](#executing-the-scheduled-task)

Usually scheduled tasks are registered when installing or updating your plugin. If you don't want to reinstall your plugin in order to register your scheduled task, you can also use the following command to achieve this: `bin/console scheduled-task:register`

In order to properly test your scheduled task, you first have to run the command `bin/console scheduled-task:run`. This will start the `ScheduledTaskRunner`, which takes care of your scheduled tasks and their respective timings. It will dispatch a message to the message bus once your scheduled task's interval is due.

Now you still need to run the command `bin/console messenger:consume` to actually execute the dispatched messages. Make sure, that the `status` of your scheduled task is set to `scheduled` in the `scheduled_task` table, otherwise it won't be executed. This is not necessary, when you're using the admin worker.

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

## More interesting topics [​](#more-interesting-topics)

* [Adding a custom command](./add-custom-commands.html)

---

## Using custom fields of type media

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/custom-fields-of-type-media.html

# Using Custom Fields of Type Media [​](#using-custom-fields-of-type-media)

After you have added a custom field of type media, with the Administration or via plugin, you can assign media objects to the different entities. This is often used for products to add more images to the product detail page. If you want to learn more about custom fields you might want to take a look at this guide: [Adding custom fields](./../framework/custom-field/add-custom-field.html).

## Overview [​](#overview)

In the product detail page template, the key `page.product.translated.customFields.xxx` with the `xxx`, which is replaced with the corresponding custom field, contains the UUID of the media. Now the ID has just to be resolved with the function [searchMedia](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Framework/Adapter/Twig/Extension/MediaExtension.php#L31-L45):

php

```shiki
// platform/src/Core/Framework/Adapter/Twig/Extension/MediaExtension.php
public function searchMedia(array $ids, Context $context): MediaCollection { ... }
```

This function resolves out the corresponding media objects for the given IDs in order to continue working with them afterwards. Here is an example with a custom field (`custom_sports_media_id`) on the product detail page:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/product-detail.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}

{% block page_product_detail_media %}
    {# simplify ID access #}
    {% set sportsMediaId = page.product.translated.customFields.custom_sports_media_id %}

    {# fetch media as batch - optimized for performance #}
    {% set mediaCollection = searchMedia([sportsMediaId], context.context) %}

    {# extract single media object #}
    {% set sportsMedia = mediaCollection.get(sportsMediaId) %}

    {{ dump (sportsMedia) }}
{% endblock %}
```

text

```shiki
//dump() output
Shopware\Core\Content\Media\MediaEntity {#5302 ▼
  #extensions: array:1 [▶]
  #_uniqueIdentifier: "f69ab8ae42d04e17b2bab5ec2ff0a93c"
  #versionId: null
  #translated: array:3 [▶]
  #createdAt: DateTimeImmutable @1691755154 {#7298 ▶}
  #updatedAt: DateTimeImmutable @1691755154 {#6848 ▶}
  -_entityName: "media"
  -_fieldVisibility: Shopware\Core\Framework\DataAbstractionLayer\FieldVisibility {#4511 ▶}
  #userId: "0189e47673a671198c21a14f15cf563e"
  #mimeType: "image/jpeg"
  #fileExtension: "jpg"
  #fileSize: 21914
  #title: null
  #metaDataRaw: null
  #mediaTypeRaw: "O:47:"Shopware\Core\Content\Media\MediaType\ImageType":3:{s:13:"\x00*\x00extensions";a:0:{}s:7:"\x00*\x00name";s:5:"IMAGE";s:8:"\x00*\x00flags";a:0:{}}"
  #metaData: array:3 [▶]
  #mediaType: Shopware\Core\Content\Media\MediaType\ImageType {#6626 ▶}
  #uploadedAt: DateTimeImmutable @1691755154 {#7376 ▶}
  #alt: null
  #url: "http://YOUR_SHOP_URL.TEST/media/f5/d3/45/1691755154/shirt_red_600x600.jpg"
  #fileName: "shirt_red_600x600"
  #user: null
  #translations: null
  #categories: null
  #productManufacturers: null
  #productMedia: null
  #avatarUsers: null
  #thumbnails: Shopware\Core\Content\Media\Aggregate\MediaThumbnail\MediaThumbnailCollection {#7086 ▶}
  #mediaFolderId: "0189e474eda5709fb8ef632219dd6fc0"
  #mediaFolder: null
  #hasFile: true
  #private: false
  #propertyGroupOptions: null
  #mailTemplateMedia: null
  #tags: null
  #thumbnailsRo: "O:77:"Shopware\Core\Content\Media\Aggregate\MediaThumbnail\MediaThumbnailCollection":2:{s:13:"\x00*\x00extensions";a:0:{}s:11:"\x00*\x00elements";a:4:{s:32:"018 ▶"
  #documentBaseConfigs: null
  #shippingMethods: null
  #paymentMethods: null
  #productConfiguratorSettings: null
  #orderLineItems: null
  #cmsBlocks: null
  #cmsSections: null
  #cmsPages: null
  #documents: null
  #appPaymentMethods: null
  #productDownloads: null
  #orderLineItemDownloads: null
  #customFields: null
  #id: "f69ab8ae42d04e17b2bab5ec2ff0a93c"
}
```

## Avoid loops [​](#avoid-loops)

This function performs a query against the database on every invocation and should therefore not be used within a loop. To resolve multiple ID's at once just pass it an array of ID's instead.

To read the media objects within the product listing we recommend the following procedure:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/component/product/listing.html.twig
{% sw_extends '@Storefront/storefront/component/product/listing.html.twig' %}

{% block element_product_listing_col %}
    {# initial ID array #}
    {% set sportsMediaIds = [] %}

    {% for product in searchResult %}
        {# simplify ID access #}
        {% set sportsMediaId = product.translated.customFields.custom_sports_media_id %}

        {# merge IDs to a single array #}
        {% set sportsMediaIds = sportsMediaIds|merge([sportsMediaId]) %}
    {% endfor %}

    {# do a single fetch from database #}
    {% set mediaCollection = searchMedia(sportsMediaIds, context.context) %}

    {% for product in searchResult %}
        {# simplify ID access #}
        {% set sportsMediaId = product.translated.customFields.custom_sports_media_id %}

        {# get access to media of product #}
        {% set sportsMedia = mediaCollection.get(sportsMediaId) %}

        {{ dump(sportsMedia) }}
    {% endfor %}
{% endblock %}
```

## Display image [​](#display-image)

Use a direct html `img` tag to load the original image.

twig

```shiki
<img src="{{ sportsMedia.url }}" alt="{{ sportsMedia.alt }}">
```

You can also use the `sw_thumbnails` twig function to load viewport specific images.

twig

```shiki
{% sw_thumbnails 'my-sportsMedia-thumbnails' with {
media: sportsMedia
} %}
```

---

## Adding NPM dependencies

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/using-npm-dependencies.html

# Adding NPM Dependencies [​](#adding-npm-dependencies)

In this guide, you'll learn how to add NPM dependencies to your project.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further, a basic understanding of Node and NPM is required.

## Video [​](#video)

This guide is also available as a video:

#### Shopware 6: Your custom NPM dependencies (Developer Tutorial) - YouTube

WARNING

This video shows how to resolve the NPM package name as an alias. We recommend resolving all node\_modules instead like shown in the code example below.

## Adding a npm package to the Administration or the Storefront [​](#adding-a-npm-package-to-the-administration-or-the-storefront)

Presuming you have `npm` installed, run `npm init -y` in the `<plugin root>src/Resources/app/administration/` folder or the `<plugin root>src/Resources/app/storefront/` folder. This command creates a `package.json` file in the respective folder, depending on the environment you're working in. To add a package to the `package.json` file simply run the `npm install` command. In this example we will be installing [`missionlog`](https://www.npmjs.com/package/missionlog).

So in order to install `missionlog`, run `npm install missionlog` in the folder you have created your `package.json` file in.

## Registering a package in the build system [​](#registering-a-package-in-the-build-system)

Shopware's storefront as well as administration is based on the build system [Webpack](https://webpack.js.org/). Webpack is a source file bundler: In essence it bundles all the source files into a single `bundle.js` to be shipped to a browser. So in order to make Webpack aware of the new dependency, we have to register it and give it an alias/pseudonym so that the package can be bundled correctly.

To do this, we create a new folder called "build" under either `Resources/app/storefront` or `Resources/app/administration`. In this build folder we create a new file with the name `webpack.config.js`. We thereby make it possible to extend the Webpack configuration of Shopware.

javascript

```shiki
module.exports = (params) => {
    return { 
        resolve: { 
            modules: [
                `${params.basePath}/Resources/app/storefront/node_modules`,
            ],
       } 
   }; 
}
```

Let us take a closer look at the code. In the first line, we export a so-called arrow function. The build system from Shopware calls this function when either the Administration or Storefront is being built.

Now we add the `node_modules` folder from our extension. `resolve.modules` tells webpack what directories should be searched when resolving modules. By default, the shopware webpack config only considers the `node_modules` folder of the platform. By accessing `params.basePath` we get the absolute path to our extension. We then add the rest of the path to our extensions `node_modules`. Now webpack will also search for modules in our `node_modules` folder.

## Using the dependency [​](#using-the-dependency)

Once we have installed all the dependencies and registered the package in the build system, we can use the package in our own code.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example.plugin.js
const { PluginBaseClass } = window;

// Import logger
import { log } from 'missionlog';

// Initializing the logger
log.init({ initializer: 'INFO' }, (level, tag, msg, params) => {
    console.log(`${level}: [${tag}] `, msg, ...params);
});

// The plugin skeleton
export default class ExamplePlugin extends PluginBaseClass {
    init() {
        console.log('init');

        // Use logger
        log.info('initializer', 'example plugin got started', this);
    }
}
```

We import the function log as well as the constants tag via `destructuring` in the specified code and register our above plugin in our main.js file, so it can be loaded by the plugin system.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
import ExamplePlugin from './example.plugin';

PluginManager.register(
    'ExamplePlugin',
    ExamplePlugin
);
```

The final step in this process is to build your Storefront or Administration so that your changes are processed by Webpack.

bash

```shiki
# Build the Storefront
./bin/build-storefront.sh

# Build the Administration
./bin/build-administration.sh
```

## Next steps [​](#next-steps)

Now that you know how to include new `npm` dependencies you might want to create a service with them. Learn how to do that in this guide: [How to add a custom-service](./../administration/services-utilities/add-custom-service.html)

If you want to add [Composer dependencies](./using-composer-dependencies.html), or even other [plugin dependencies](./add-plugin-dependencies.html), we've got you covered as well.

---

## Adding Composer dependencies

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/using-composer-dependencies.html

# Adding Composer Dependencies [​](#adding-composer-dependencies)

In this guide you'll learn how to add Composer dependencies to your project.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand PHP, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further a basic understanding of Node and NPM is required.

## Adding a Composer plugin to the `composer.json` file [​](#adding-a-composer-plugin-to-the-composer-json-file)

In this guide we will install [`exporter`](https://github.com/sebastianbergmann/exporter), which provides the functionality to export PHP variables for visualization.

Now we can simply install the `exporter` package by adding `"sebastian/exporter": "*"` to the list in `require` section of the `composer.json` of our plugin.

Now we can simply install `exporter` by running `composer require sebastian/exporter` in your plugin directory.

After that we have to add our dependency to shopware back in.

WARNING

The `vendor` directory, where the Composer saves the dependencies, has to be included in the plugin bundle. The plugin bundle size is not allowed to exceed 5 MB.

## Executing composer commands during plugin installation [​](#executing-composer-commands-during-plugin-installation)

In order that the additional package our plugin requires are installed as well when our plugin is installed, shopware need to execute composer commands to do so. Therefore, we need to overwrite the `executeComposerCommands` method in our plugin base class and return true.

php

```shiki
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;

class SwagBasicExample extends Plugin
{
    public function executeComposerCommands(): bool
    {
        return true;
    }

}
```

## Using the Composer plugin [​](#using-the-composer-plugin)

PHP doesn't require a build system, which means that we can just add `use` statements and then use the Composer dependency directly.

The following code sample imports `SebastianBergmann\Exporter\Exporter` and logs `hello, world!` to the Symfony profiler logs whenever the `NavigationPageLoadedEvent` is fired. Learn how to [register this listener](./listening-to-events.html).

php

```shiki
// <plugin root>/src/SwagBasicExample.php
<?php
namespace SwagBasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Storefront\Page\Navigation\NavigationPageLoadedEvent;

use Psr\Log\LoggerInterface;
use SebastianBergmann\Exporter\Exporter;

class MySubscriber implements EventSubscriberInterface
{
     private LoggerInterface $logger;

    public function __construct(
        LoggerInterface $logger
    ) {
        $this->logger = $logger;
    }

    public static function getSubscribedEvents(): array
    {
        // Return the events to listen to as array like this:  <event to listen to> => <method to execute>
        return [
            NavigationPageLoadedEvent::class => 'onNavigationPage'
        ];
    }

    public function onNavigationPage(NavigationPageLoadedEvent $event)
    {
        $exporter = new Exporter;
        $this->logger->info($exporter->export('hello, world!'));
    }
}
```

## Adding private Composer dependencies [​](#adding-private-composer-dependencies)

You can bundle Composer dependencies with your plugin by adding them to the `/packages/` folder of your plugin.

Example structure:

text

```shiki
SwagBasicExample
├── packages
│   └── my-private-dependency/
│       ├── composer.json
│       └── src/
│           └── SomeCoolService.php
├── src/
│   └── SwagBasicExample.php
└── composer.json
```

You can then require them like other dependencies:

text

```shiki
"require": {
    "my-vendor-name/my-private-dependency": "^1.2.3",
}
```

## More interesting topics [​](#more-interesting-topics)

* [Using NPM dependencies](./using-npm-dependencies.html)
* [Adding plugin dependencies](./add-plugin-dependencies.html)

---

## Plugin lifecycle methods

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/plugin-lifecycle.html

# Plugin Lifecycle Methods [​](#plugin-lifecycle-methods)

## Overview [​](#overview)

A Shopware plugin can be installed, activated, deactivated and then again uninstalled. Those are some plugin lifecycle methods, which will be covered a bit more in this guide.

## Prerequisites [​](#prerequisites)

This guide is built upon our [plugin base guide](./../plugin-base-guide.html), which explains the basics of a plugin as a whole. Make sure to have a look at it to get started on building your first plugin.

## Lifecycle methods [​](#lifecycle-methods)

Each of the followings methods are going to be part of the plugin bootstrap, in this example the file will be `<plugin root>/src/SwagBasicExample.php`, which is the bootstrap file of the previously mentioned plugin base guide.

Throughout all of the lifecycle methods, you have access to the [service container](./dependency-injection.html) via `$this->container`.

### Install [​](#install)

The install method of a plugin is executed when the plugin is installed. You can use this method to install all the necessary requirements for your plugin, e.g. a new payment method.

php

```shiki
// <plugin root>/src/SwagBasicExample
public function install(InstallContext $installContext): void
{
    // Do stuff such as creating a new payment method
}
```

In your install method, you have access to the `InstallContext`, which provides information such as:

* The current plugin version
* The current Shopware version
* The `Context`, which provides a lot more of system information, e.g. the currently used language
* A collection of the [plugin migrations](./database-migrations.html)
* If the migrations should be executed (`isAutoMigrate` or `setAutoMigrate` to prevent the execution)

INFO

You maybe don't want to create new data necessary for your plugin in the `install` method, even though it seems to be the perfect place. That's because an installed plugin is not automatically active yet - hence some data changes would have an impact on the system before the plugin is even active and therefore functioning. A good rule of thumb is: Only install new data or entities, that can be activated or deactivated themselves, such as a payment method. This way you can create a new payment method in the `install` method, but keep it inactive for now.

### Uninstall [​](#uninstall)

The opposite of the `install` method. It gets executed once the plugin is uninstalled. You might want to remove the data, that your plugin created upon installation.

WARNING

You can't simply remove everything that your plugin created previously. Think about a new payment method, that your plugin created and which was then used for actual orders. If you were to remove this payment method when uninstalling the plugin, all the orders that used this payment method would be broken, since the system wouldn't find the used payment method anymore. In this case, you most likely just want to deactivate the respective entity, if possible. Be careful here!

php

```shiki
// <plugin root>/src/SwagBasicExample
public function uninstall(UninstallContext $uninstallContext): void
{
    // Remove or deactivate the data created by the plugin
}
```

The `uninstall` method comes with the `UninstallContext`, which offers the same information as the `install` method. There's one more very important information available with the `UninstallContext`, which is the method `keepUserData`.

#### Keeping user data upon uninstall [​](#keeping-user-data-upon-uninstall)

When uninstalling a plugin, the user is asked if he really wants to delete all the plugin data. The method `keepUserData` of the `UninstallContext` will provide the users decision. If `keepUserData` returns `true`, you should **not** remove important data of your plugin, the user wants to keep them.

php

```shiki
// <plugin root>/src/SwagBasicExample
public function uninstall(UninstallContext $uninstallContext): void
{
    parent::uninstall($uninstallContext);

    if ($uninstallContext->keepUserData()) {
        return;
    }

    // Remove or deactivate the data created by the plugin
}
```

INFO

Refer to this video on **[Uninstalling a plugin](https://www.youtube.com/watch?v=v9OXrUJzC1I)** dealing with plugin uninstall routines. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

### Activate [​](#activate)

The `activate` method is executed once the plugin gets actually activated. You most likely want to do one of the following things here:

* Activate entities that you created in the install method, e.g. such as a payment method
* Create new entities or data, that you couldn't create in the install method

php

```shiki
// <plugin root>/src/SwagBasicExample
public function activate(ActivateContext $activateContext): void
{
    // Activate entities, such as a new payment method
    // Or create new entities here, because now your plugin is installed and active for sure
}
```

The `ActivateContext` provides the same information as the `InstallContext`.

### Deactivate [​](#deactivate)

The opposite of the `activate` method. It is triggered once the plugin deactivates the plugin. This method should mostly do the opposite of the plugin's `activate` method:

* Deactivate entities created by the `install` method
* Maybe remove entities, that cannot be deactivated but would harm the system, if they remained in the system while the plugin is inactive

php

```shiki
// <plugin root>/src/SwagBasicExample
public function deactivate(DeactivateContext $deactivateContext): void
{
    // Deactivate entities, such as a new payment method
    // Or remove previously created entities
}
```

The `DeactivateContext` provides the same information as the `InstallContext`.

### Update [​](#update)

The `update` method is executed once your plugin gets updated to a new version. You do not need to update database entries here, since this should be done via [plugin migrations](./database-migrations.html). Otherwise you'd have to check if this specific update to an entity was already done in a previous `update` method execution, mostly by using plugin version conditions.

However, of course you can still do that if necessary. Also, non-database updates can be done here.

php

```shiki
// <plugin root>/src/SwagBasicExample
public function update(UpdateContext $updateContext$context): void
{
    // Update necessary stuff, mostly non-database related
}
```

The `UpdateContext` provides the same information as the `InstallContext`, but comes with one more method. In order to get the new plugin version, you can use the method `getUpdatePluginVersion` in contrast to the `getCurrentPluginVersion`, which will return the currently installed plugin version.

### PostInstall and PostUpdate methods [​](#postinstall-and-postupdate-methods)

There are two more lifecycle methods, that are worth mentioning: `PostUpdate` and `PostInstall`, which are executed **after** the respective process of installing or updating your plugin is fully and successfully done.

php

```shiki
// <plugin root>/src/SwagBasicExample
public function postInstall(InstallContext $installContext): void
{
}

public function postUpdate(UpdateContext $updateContext): void
{
}
```

---

## Logging

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-fundamentals/logging.html

# Logging [​](#logging)

## Overview [​](#overview)

As a plugin developer, you may want to log certain actions or errors to a log file to aid in debugging or to simply keep a record of performed actions.

## Prerequisites [​](#prerequisites)

This guide is built upon our [plugin base guide](./../plugin-base-guide.html), which explains the basics of a plugin as a whole. Make sure to have a look at it to get started on building your first plugin.

## Configuring Monolog [​](#configuring-monolog)

First, you must make sure that your plugin loads package configuration from the `/Resources/config/packages` folder:

[plugin root]/src/SwagBasicExample.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;
use Symfony\Component\Config\FileLocator;
use Symfony\Component\Config\Loader\DelegatingLoader;
use Symfony\Component\Config\Loader\LoaderResolver;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Loader\DirectoryLoader;
use Symfony\Component\DependencyInjection\Loader\GlobFileLoader;
use Symfony\Component\DependencyInjection\Loader\YamlFileLoader;

class SwagBasicExample extends Plugin
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $locator = new FileLocator('Resources/config');

        $resolver = new LoaderResolver([
            new YamlFileLoader($container, $locator),
            new GlobFileLoader($container, $locator),
            new DirectoryLoader($container, $locator),
        ]);

        $configLoader = new DelegatingLoader($resolver);

        $confDir = \rtrim($this->getPath(), '/') . '/Resources/config';

        $configLoader->load($confDir . '/{packages}/*.yaml', 'glob');
    }
}
```

This is a Symfony Bundle requirement, the same can also be achieved using Bundle Extensions. Please refer to the [Symfony Documentation](https://symfony.com/doc/current/bundles/extension.html).

We will now use monolog configuration to create a channel for your log messages; the channel should be a unique name identifying your plugin. See below for an example:

[plugin root]/src/Resources/config/packages/monolog.yaml

yaml

```shiki
monolog:
  channels: ['my_plugin_channel']
```

Monolog automatically registers a logger service that you can inject in to your services, which is scoped to your channel. You can access the logger with the service ID: `monolog.logger.my_plugin_channel`.

With your newly created channel, you can create a handler, directing your new channel to it.

[plugin root]/src/Resources/config/packages/monolog.yaml

yaml

```shiki
monolog:
  channels: ['my_plugin_channel']

  handlers:
    myPluginLogHandler:
        type: rotating_file
        path: "%kernel.logs_dir%/my_plugin_%kernel.environment%.log"
        level: error
        channels: [ "my_plugin_channel"]
```

Following this approach allows project owners to redirect your channel to a different one to better suit their needs.

---

