# Guides Plugins Plugins

*Scraped from Shopware Developer Documentation*

---

## Plugins

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/

# Plugins [​](#plugins)

Plugins are Shopware's server-side extension type, giving you deep integration with the e-commerce platform. They allow you to extend, overwrite, and modify Shopware’s core capabilities. Unlike apps and themes, plugins run directly inside the shop environment and can interact tightly with the system.

You will likely create a plugin when you need to make profound changes or require complex functionalities such as:

* Custom price calculation
* Product imports
* Custom content/product logic
* Integrating third-party identity providers
* Dynamic validations
* Customer tracking or behavioral logic

Refer to our [Plugin Base Guide](./plugin-base-guide/) and [Plugin Fundamentals](./plugin-fundamentals/) for guidance on plugin development.

INFO

If your extension focuses only on design changes, a simple template adjustment—typically done through a theme plugin—may be the best choice.

## Types of plugins [​](#types-of-plugins)

Shopware plugins differ in their folder structure and functionality.

### Plugins [​](#plugins-1)

`<shopware project root>/custom/plugins` contains all plugins from the Shopware store. You install and manage these plugins via the Shopware Administration.

### Static plugins [​](#static-plugins)

`<shopware project root>/custom/static-plugins` contains all project-specific plugins that are typically committed to the Git repository.

INFO

The Shopware Administration does not detect static plugins. The project must require them via Composer for them to be installable.

bash

```shiki
# You can find the vendor/package name in the plugin's composer.json file under "name"
composer req <vendor>/<plugin-name>
```

### Symfony bundle / Shopware bundle [​](#symfony-bundle-shopware-bundle)

You can also use Shopware/Symfony bundles instead of plugins. Bundles are a good choice when you want to avoid plugin lifecycle handling or Administration management. You install bundles via Composer. They are not managed by the Shopware Administration.

## Feature comparison [​](#feature-comparison)

TIP

For customizing projects, we recommend using [bundles](https://developer.shopware.com/docs/guides/plugins/plugins/bundle.html) instead of plugins. As bundles are not managed via Administration and don't have a lifecycle, they offer full control over the project.

| Feature | Plugin | Static Plugin | Shopware Bundle | Symfony Bundle |
| --- | --- | --- | --- | --- |
| Installation | Via Shopware Admin | Via Composer | Via Composer | Via Composer |
| Repository Location | `custom/plugins` | `custom/static-plugins` | `vendor` or inside `src` folder | `vendor` or inside `src` folder |
| Lifecycle Events (install, update, uninstall) | Yes | Yes | No | No |
| Can be managed in Administration | Yes | No | No | No |
| Can be a Theme | Yes | Yes | Yes | No |
| Can modify Admin / Storefront with JS/CSS | Yes | Yes | Yes | No |

---

## Plugin Base Guide

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugin-base-guide.html

# Plugin Base Guide [​](#plugin-base-guide)

## Overview [​](#overview)

Plugins in Shopware are essentially an extension of [Symfony bundles](./plugins-for-symfony-developers.html). Such bundles and plugins can provide their own resources like assets, controllers, services or tests, which you'll learn in the next guides.  
 A plugin is the main way to extend your Shopware 6 instance programmatically.

This section guides you through the basics of creating a plugin from scratch, which can then be installed on your Shopware 6 instance. Refer to the Guide section to know how to [Install Shopware 6](./../../installation/).

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line.  
 Of course, you'll have to understand PHP, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Create your first plugin [​](#create-your-first-plugin)

Let's get started with creating your plugin by finding a proper name for it.

### Name your plugin [​](#name-your-plugin)

First, you need to find a name for your plugin. We're talking about a technical name here, so it needs to describe your plugins functionality as short as possible, written in UpperCamelCase. To prevent issues with duplicated plugin names, you should add a shorthand prefix for your company.  
 Shopware uses "Swag" as a prefix for that case.  
 For this example guide we'll use the plugin name **SwagBasicExample.**

INFO

Using a prefix for your plugin name is not just a convention we'd recommend, but a hard requirement if you want to publish your plugin in the [Shopware Community Store](https://store.shopware.com/en).

### **Create the plugin** [​](#create-the-plugin)

Now that you've found your name, it's time to actually create your plugin.

Shopware provides a handy command that you can use to generate the plugin structure. Go to your shopware project's root directory and run the following command:

bash

```shiki
bin/console plugin:create SwagBasicExample
```

You can pass an addition flag `-c` or `--create-config` in the above command which would also create a demo configuration file in the `Resources` directory. The command will generate all the basic required files that are needed for an extension to be installed on a Shopware instance. Make sure to adjust the namespace in the files as per your need.

If you want to create the structure manually please follow the instructions below:

For this, please navigate to the directory `custom/plugins`, that you should find in your Shopware 6 installation. Inside the `plugins` directory, create a new directory named after your plugin, so it should look like this: `custom/plugins/SwagBasicExample`

By convention, you'll have another directory in there, which is called `src`. This is not required, but recommended. And that's it for the directory structure for now.

Inside your `src` directory, create a PHP class named after your plugin, `SwagBasicExample.php`.  
 This new class `SwagBasicExample` has to extend from Shopware's abstract Plugin class, which is `Shopware\Core\Framework\Plugin`.

Apart from this, only the namespace is missing. You can freely define it, but we'd recommend using a combination of your manufacturer prefix and the technical name, so in this `guide` this would be: `Swag\BasicExample`

php

```shiki
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;

class SwagBasicExample extends Plugin
{
}
```

Basically that's it for the PHP part, your basic plugin class is already done.

INFO

Refer to this video on **[Creating a plugin](https://www.youtube.com/watch?v=_Tkoq5W7woI)** that shows how to bootstrap a plugin. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

#### The composer.json file [​](#the-composer-json-file)

You've created the necessary plugin structure and the plugin base class. The only thing missing for your plugin to be fully functional, is a `composer.json` file inside your plugin's root directory.  
`custom/plugins/SwagBasicExample/composer.json`

This file consists of basic information, that Shopware needs to know about your plugin, such as:

* The technical name
* The description
* The author
* The used license
* The current plugin version
* The required dependencies
* ... and a few more

This file can also be read by [Composer](https://getcomposer.org/), but that's not part of this guide.  
 Further information you'll have to add in there: The `type` has to be `shopware-platform-plugin`, so Shopware can safely recognize your plugin as such and the `require` field must include at least `shopware/core`, to check for compatibility.

Here's an example `composer.json` for this guide, which will do the trick:

javascript

```shiki
// <plugin root>/composer.json
{
    "name": "swag/basic-example",
    "description": "Description for the plugin SwagBasicExample",
    "version": "1.0.0",
    "type": "shopware-platform-plugin",
    "license": "MIT",
    "authors": [
        {
            "name": "Shopware"
        }
    ],
    "require": {
        "shopware/core": "~6.6.0"
    },
    "extra": {
        "shopware-plugin-class": "Swag\\BasicExample\\SwagBasicExample",
        "label": {
            "de-DE": "Der angezeigte lesbare Name für das Plugin",
            "en-GB": "The displayed readable name for the plugin"
        },
        "description": {
            "de-DE": "Beschreibung in der Administration für das Plugin",
            "en-GB": "Description in the Administration for this plugin"
        }
    },
    "autoload": {
        "psr-4": {
            "Swag\\BasicExample\\": "src/"
        }
    }
}
```

There's another two things that you need to know:

1. The `shopware-plugin-class` information. This has to point to the plugin's base PHP class. The one, that you've previously created.
2. The whole `autoload` part. This has to mention your [PSR-4](https://www.php-fig.org/psr/psr-4/) namespace. So if you'd like to have another namespace for your plugin, this is the place to go.

WARNING

The path you've configured in the configuration `autoload.psr-4`, `src/` in this case, will be referred to as `<plugin root>/src` in almost all code examples. If you're using a custom path here, e.g. just a slash `/`, then the examples would be `<plugin root>/` here instead.

And that's it. The basic structure and all necessary files for your plugin to be installable are done.

INFO

Refer to this video on **[The composer.json plugin file](https://www.youtube.com/watch?v=CY3SlfwkTm8)** that explains the basic structure of the `composer.json` plugin file. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Install your plugin [​](#install-your-plugin)

You can safely install your plugin now and Shopware should easily recognize it like this.

Open up your command line terminal and navigate to your Shopware 6 directory, the one which also contains the `custom` directory.

Once inside there, you need to refresh the list of plugins, that Shopware knows yet. This is done with the following command:

bash

```shiki
php bin/console plugin:refresh
```

There might be a warning appearing regarding the `version` of the `composer.json` file, but you can safely ignore that.  
 You should end up with a list like the following:

bash

```shiki
Shopware Plugin Service
=======================

 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
  Plugin                         Label                                        Version     Upgrade version   Author                       Installed   Active   Upgradeable
 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
  SwagBasicExample               The displayed readable name for the plugin   1.0.0                         Shopware                     No          No       No
 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
```

This output is a **good sign**, because this means Shopware recognized your plugin successfully. But it's not installed yet, so let's do that.

bash

```shiki
php bin/console plugin:install --activate SwagBasicExample
```

This should print the following output:

bash

```shiki
Shopware Plugin Lifecycle Service
=================================

 Install 1 plugin(s):
 * The displayed readable name for the plugin (v1.0.0)

 Plugin "SwagBasicExample" has been installed and activated successfully.
```

And that's basically it.  
**You've just successfully created your Shopware 6 plugin!**

## Next steps [​](#next-steps)

There's many more things to discover when creating your first plugin. Hence, here's a list of important articles, that may be of interest for you.

* [Installing data with your plugin](./plugin-fundamentals/database-migrations.html)
* [Learn more about the plugin lifecycle methods](./plugin-fundamentals/plugin-lifecycle.html)
* [Adding a configuration to your plugin](./plugin-fundamentals/add-plugin-configuration.html)
* [Learning about the service container](./plugin-fundamentals/dependency-injection.html)
* [Adding a custom service](./plugin-fundamentals/add-custom-service.html)
* [Start listening to events](./plugin-fundamentals/listening-to-events.html)

---

## Bundle

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/bundle.html

# Bundle [​](#bundle)

Plugins are based on the Symfony bundle concept, but offer additional features like lifecycle events and the ability to be managed in the Shopware administration. This is maybe unwanted in some cases, like project critical customizations which should not be managed via the Shopware administration. In this case, you can use a Symfony bundle instead of a plugin.

## Project Structure [​](#project-structure)

Here's how a typical Shopware 6 project structure looks like when using bundles:

text

```shiki
project-root/
├── bin/
│   └── console
├── config/
│   ├── bundles.php
│   ├── packages/
│   └── services.yaml
├── public/
│   ├── index.php
│   └── bundles/
├── src/
│   └── YourBundleName/
│       ├── YourBundleName.php
│       ├── Migration/
│       │   └── Migration1234567890YourMigration.php
│       └── Resources/
│           ├── config/
│           │   ├── services.xml
│           │   └── routes.xml
│           ├── views/
│           │   └── storefront/
│           │       └── page/
│           └── app/
│               ├── storefront/
│               │   └── src/
│               └── administration/
│                   └── src/
├── var/
├── vendor/
├── composer.json
├── composer.lock
└── .shopware-project.yaml
```

The Bundle is typically placed in the `src/` folder of your project, which is the standard location for custom code in a Shopware project. You still will need to register the bundle in the `config/bundles.php` file of your project.

## Choosing the right Bundle class [​](#choosing-the-right-bundle-class)

There are two Bundle classes you can choose from:

* `Shopware\Core\Framework\Bundle`
* `Symfony\Component\HttpKernel\Bundle\Bundle`

The first one is the Shopware bundle class and the second one is the Symfony bundle class. The Shopware bundle class extends the Symfony bundle class, but offers additional features like acting as theme, bringing JavaScript/CSS files, Migrations, etc. If you don't need these features, you can use the Symfony bundle class instead.

## Creating a Bundle [​](#creating-a-bundle)

By default, The namespace `App\` is registered to the `src` folder in any Shopware project to be used for customizations. We recommend using this namespace, if you like to change the project structure, you can change the `App\` namespace in the `composer.json` file of your project.

php

```shiki
// <project root>/src/YourBundleName.php
<?php declare(strict_types=1);

namespace App\YourBundleName;

use Shopware\Core\Framework\Bundle;

class YourBundleName extends Bundle
{
}
```

The bundle class needs to be registered in the `config/bundles.php` file of your project.

php

```shiki
// <project root>/config/bundles.php
//...
App\YourBundleName\YourBundleName::class => ['all' => true],
//...
```

## Adding services, twig templates, routes, theme, etc [​](#adding-services-twig-templates-routes-theme-etc)

You can add services, twig templates, routes, etc. to your bundle like you would do in a plugin. Just create `Resources/config/services.xml` and `Resources/config/routes.xml` files or `Resources/views` for twig templates. The bundle will be automatically detected and the files will be loaded.

To mark your bundle as a theme, it's enough to implement the `Shopware\Core\Framework\ThemeInterface` interface in your bundle class. This will automatically register your bundle as a theme and make it available in the Shopware administration. You can also add a `theme.json` file to define the theme configuration like [described here](./../themes/theme-configuration.html).

## Adding migrations [​](#adding-migrations)

Migrations are not automatically detected in bundles. To enable migrations, you need to overwrite the `build` method in your bundle class like this:

php

```shiki
// <project root>/src/YourBundleName.php
<?php declare(strict_types=1);

namespace App\YourBundleName;

use Shopware\Core\Framework\Bundle;

class YourBundleName extends Bundle
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $this->registerMigrationPath($container);
    }
}
```

As Bundles don't have a lifecycle, the migrations are not automatically executed. You need to execute them manually via the console command:

bash

```shiki
bin/console database:migrate <BundleName> --all
```

If you use [Deployment Helper](./../../hosting/installation-updates/deployments/deployment-helper.html), you can add it to the `.shopware-project.yaml` file like this:

yaml

```shiki
deployment:
    hooks:
        pre-update: |
            bin/console database:migrate <BundleName> --all
```

## Integration into Shopware-CLI [​](#integration-into-shopware-cli)

Shopware-CLI cannot detect bundles automatically, therefore the assets of the bundles are not built automatically. You will need to adjust the `composer.json` file of your project to specify the path to the bundle. This is done by adding the `extra` section to the `composer.json` file:

json

```shiki
{
    "extra": {
        "shopware-bundles": {
          "src/<BundleName>": {
            "name": "<BundleName>",
          }
        }
    }
}
```

This will tell Shopware-CLI where the bundle is located and what the name of the bundle is.

---

## Plugins for Symfony developers

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/plugins-for-symfony-developers.html

# Plugins for Symfony Developers [​](#plugins-for-symfony-developers)

## Overview [​](#overview)

This guide serves as an entry point for developers familiar with the concepts of `Symfony bundles`.

INFO

Check out our [Shopware Toolbox PHPStorm extension](./../../../resources/tooling/ide/shopware-toolbox.html) with useful features like autocompletion, code generation or guideline checks.

## Prerequisites [​](#prerequisites)

This guide handles some base concepts of Shopware plugins. Therefore, you may want to have a look at [Plugin base guide](./plugin-base-guide.html) first.

As this guide also references the functionality of Symfony bundles, you should have at least a basic knowledge of it. You may want to have a look or refresh your knowledge on Symfony's [Bundle system](https://symfony.com/doc/current/bundles.html).

## Symfony bundles [​](#symfony-bundles)

A bundle is the Symfony's preferred way to provide additional third-party features to any Symfony application. Those bundles are everywhere: Symfony even outsources many of its core features into external bundles. The template engine `Twig`, the `Security` bundle, the `WebProfiler`, as well as many other third-party bundles can be installed on demand to extend your Symfony application in any way. The Bundle System is Symfony's way of providing an extendable framework with plugin capabilities.

## Shopware plugins [​](#shopware-plugins)

Shopware is building upon the `Symfony Bundle System` to extend its functionality even more. This allows the Shopware Plugin System to function as a traditional plugin system with features like plugin lifecycles and more.

Whenever you create a Shopware plugin, you have to extend the `Shopware\Core\Framework\Plugin` class. If you investigate this class, you will see that this class extends `Shopware\Core\Framework\Bundle`, which in return extends the Symfony's `Bundle` class:

php

```shiki
// 
class YourNamespace\PluginName extends

    // plugin lifecycles
    abstract class Shopware\Core\Framework\Plugin extends

        // adds support for migrations, filesystem, events, themes
        abstract class Shopware\Core\Framework\Bundle extends

            // Symfony base bundle
            abstract class Symfony\Component\HttpKernel\Bundle
```

As you can see, any Shopware plugin is also a Symfony bundle internally as well, and will be handled as such by Symfony. A plugin adds support for some cases, specific to the Shopware environment. These include, for example, handling plugin migrations and registering Shopware business events.

### Plugin lifecycle [​](#plugin-lifecycle)

As mentioned before, Shopware extends the `Symfony Bundle System` with some functionality to adjust its use for the Shopware ecosystem. For you as plugin developer, the most important addition is the extended plugin lifecycle.

A Shopware plugin runs through a lifecycle. Your plugin's base class can implement the following methods to execute any sort of installation or maintenance tasks.

| Lifecycle | Description |
| --- | --- |
| `install()` | Executed on plugin install |
| `postInstall()` | Executed **after** successful plugin install |
| `update()` | Executed on plugin update |
| `postUpdate()` | Executed **after** successful plugin update |
| `uninstall()` | Executed on plugin uninstallation |
| `activate()` | Executed **before** plugin activation |
| `deactivate()` | Executed **before** plugin deactivation |

## Next steps [​](#next-steps)

Now that you know about the differences between a Symfony bundle and a Shopware plugin, you might also want to have a look into the following Symfony-specific topics and how they are integrated in Shopware 6:

* [Dependency Injection](./plugin-fundamentals/dependency-injection.html)
* [Listening to events](./plugin-fundamentals/listening-to-events.html)

INFO

Here are some useful videos explaining:

* **[Bundle Methods in a plugin](https://www.youtube.com/watch?v=cUXcDwQwmPk)**
* **[Symfony services in Shopware 6](https://www.youtube.com/watch?v=l5QJ8EtilaY)**

Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

---

## Redis

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/redis.html

# Redis [​](#redis)

Starting with Shopware v6.6.8.0, Redis support has been improved, giving you more flexibility in how you use it in your projects and plugins.

## Accessing Redis connections [​](#accessing-redis-connections)

Once you've set up your Redis connections as explained in the [Redis configuration](./../../hosting/infrastructure/redis.html) guide, you can access them in your code using the following methods:

1. Inject `Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider` and retrieve connections by name:

   xml

   ```shiki
   <service id="MyCustomService">
       <argument type="service" id="Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider" />
       <argument>%myservice.redis_connection_name%</argument>
   </service>
   ```

   php

   ```shiki
   class MyCustomService
   { 
       public function __construct (
           private RedisConnectionProvider $redisConnectionProvider,
           string $connectionName,
       ) { }

       public function doSomething()
       {
           if ($this->redisConnectionProvider->hasConnection($this->connectionName)) {
               $connection = $this->redisConnectionProvider->getConnection($this->connectionName);
               // use connection
           }
       }
   }
   ```
2. Use `Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider` as factory to define custom services:

   xml

   ```shiki
   <service id="my.custom.redis_connection" class="Redis">
       <factory service="Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider" method="getConnection" />
       <argument>%myservice.redis_connection_name%</argument>
   </service>

   <service id="MyCustomService">
       <argument type="service" id="my.custom.redis_connection" />
   </service>
   ```

   php

   ```shiki
   class MyCustomService
   { 
       public function __construct (
           private object $redisConnection,
       ) { }

       public function doSomething()
       {
           // use connection
       }
   }
   ```

   This approach is especially useful when you want multiple services to share the same Redis connection.
3. Inject connection directly by name:

   xml

   ```shiki
   <service id="MyCustomService">
       <argument type="service" id="shopware.redis.connection.connection_name" />
   </service>
   ```

   Be cautious with this approach! If you change the Redis connection names in your configuration, it will cause container build errors.

## Redis usage tips [​](#redis-usage-tips)

### Connection types [​](#connection-types)

Under the hood, connection service objects are created using the `\Symfony\Component\Cache\Adapter\RedisAdapter::createConnection` method. Depending on the installed extensions/libraries and the provided DSN, this method may return instance of one of the following classes: `\Redis|Relay|\RedisArray|\RedisCluster|\Predis\ClientInterface`

### Reusing connections [​](#reusing-connections)

Connections are cached in a static variable and reused based on the provided DSN. If you use the same DSN for multiple connections, they will share the same connection object. This means you need to be cautious when closing or modifying connection options, as it will affect all services using the same connection.

### Connection initialization [​](#connection-initialization)

The moment actual connection is established depends on the usage model:

* When `RedisConnectionProvider::getConnection` is called.
* When the Redis connection service is requested from the container.
* When a service that depends on Redis connection is instantiated.

### Redis is optional [​](#redis-is-optional)

When developing a plugin, please keep in mind that Redis is an optional dependency in Shopware and might not be available in all installations.

---

## In-App Purchases (IAP)

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/in-app-purchases.html

# In-App Purchases [​](#in-app-purchases)

INFO

In-App Purchase is available since Shopware version 6.6.9.0

In-App Purchases are a way to lock certain features behind a paywall within the same extension. This is useful for developers who want to offer a free version of their extension with limited features, and then offer a paid version with more features.

[In-App purchases concept](../../../concepts/framework/in-app-purchases)[Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/in-app-purchases)

## Allow users to buy an In-App Purchase [​](#allow-users-to-buy-an-in-app-purchase)

In order to enable others to purchase your In-App Purchase, you must request a checkout for it via the `inAppPurchaseCheckout` store in the administration. The checkout process itself is provided by Shopware. As this is purely functional, it is your responsibility to provide a button and hide it if the IAP cannot be purchased more than once.

ts

```shiki
{
    computed: {
        inAppPurchaseCheckout() {
            return Shopware.Store.get('inAppPurchaseCheckout');
        },

        hideButton(): boolean {
            return Shopware.InAppPurchase.isActive('MyExtensionName', 'my-iap-identifier');
        }
    },

    methods: {
        onClick() {
            this.inAppPurchaseCheckout.request({ identifier: 'my-iap-identifier' }, 'MyExtensionName');
        }
    }
}
```

## Check active In-App Purchases [​](#check-active-in-app-purchases)

The `InAppPurchase` class contains a list of all In-App Purchases. Inject this service into your class and you can check against it:

php

```shiki
class Example
{
    public function __construct(
        private readonly InAppPurchase $inAppPurchase,
    ) {}

    public function someFunction() {
        if ($this->inAppPurchase->isActive('MyExtensionName', 'my-iap-identifier')) {
            // ...
        }

        // ...
    }
}
```

If you want to check an in-app purchase in the administration:

js

```shiki
if (Shopware.InAppPurchase.isActive('MyExtensionName', 'my-iap-identifier')) {};
```

## Event [​](#event)

Apps are also able to manipulate the available In-App Purchases as described in

[In App purchase gateway](../apps/gateways/in-app-purchase/in-app-purchase-gateway)

Plugins can listen to the `Shopware\Core\Framework\App\InAppPurchases\Event\InAppPurchasesGatewayEvent`. This event is dispatched after the In-App Purchases Gateway has received the app server response from a gateway and allows plugins to manipulate the available In-App Purchases.

---

