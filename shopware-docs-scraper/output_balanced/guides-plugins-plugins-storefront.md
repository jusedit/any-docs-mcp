# Guides Plugins Plugins Storefront

*Scraped from Shopware Developer Documentation*

---

## Storefront

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/

# Storefront [​](#storefront)

Storefront handles the e-commerce platform's front end, including the online store's visual presentation and user interface.

You can customize and enhance the storefront by adding or modifying templates, layouts, styles, and components via plugins. It allows adding custom pages, layouts, dynamic content, filters, media, assets, and styles to create unique and engaging shopping experiences, ensuring a seamless and visually appealing interface for customers. It enables businesses to showcase their products, implement responsive designs, optimize performance, and deliver a personalized shopping journey to online visitors.

---

## Customize templates

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/customize-templates.html

# Customize Templates [​](#customize-templates)

## Overview [​](#overview)

This guide will cover customizing Storefront templates with a plugin.

## Prerequisites [​](#prerequisites)

As most guides, this guide is built upon the [Plugin base guide](./../plugin-base-guide.html), so you might want to have a look at it. Other than that, knowing [Twig](https://twig.symfony.com/) is a big advantage for this guide, but that's not necessary.

## Getting started [​](#getting-started)

In this guide you will see a very short example on how you can extend a storefront block. For simplicity's sake, only the logo is replaced with a 'Hello world!' text.

### Setting up your view directory [​](#setting-up-your-view-directory)

First of all you need to register your plugin's own view path, which basically represents a path in which Shopware 6 is looking for template-files. By default, Shopware 6 is looking for a directory called `views` in your plugin's `Resources` directory, so the path could look like this: `<plugin root>/src/Resources/views`

### Finding the proper template [​](#finding-the-proper-template)

As mentioned earlier, this guide is only trying to replace the 'demo' logo with a 'Hello world!' text. In order to find the proper template, you can simply search for the term 'logo' inside the `<shopware root>/src/Storefront` directory. This will eventually lead you to [this file](https://github.com/shopware/shopware/blob/v6.6.10.2/src/Storefront/Resources/views/storefront/layout/header/logo.html.twig).

Overriding this file now requires you to copy the exact same directory structure starting from the `views` directory. In this case, the file `logo.html.twig` is located in a directory called `storefront/layout/header`, so make sure to remember this path.

INFO

There's a plugin out there called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper), that adds hints about template blocks and includes into the rendered HTML. This way it's easier to actually find the proper template.

### Overriding the template [​](#overriding-the-template)

Now, that you've found the proper template for the logo, you can override it.

This is done by creating the very same directory structure for your custom file, which is also being used in the Storefront core. As you hopefully remember, you have to set up the following directory path in your plugin: `<plugin root>/src/Resources/views/storefront/layout/header`. In there you want to create a new file called `logo.html.twig`, just like the original file. Once more to understand what's going on here: In the Storefront code, the path to the logo file looks like this: `Storefront/Resources/views/storefront/layout/header/logo.html.twig`. Now have a look at the path being used in your plugin: `<plugin root>/src/Resources/views/storefront/layout/header/logo.html.twig`

Starting from the `views` directory, the path is **exactly the same**, and that's the important part for your custom template to be loaded automatically.

### Custom template content [​](#custom-template-content)

It's time to fill your custom `logo.html.twig` file. First of all you want to extend from the original file, so you can override its blocks.

Put this line at the very beginning of your file:

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}
```

This is simply extending the `logo.html.twig` file from the Storefront bundle. If you left the file like that, it wouldn't change anything, as you're currently just extending from the original file with no overrides.

You want to replace the logo with some custom text though, so let's have a look at the original file. In there you'll find a block called `layout_header_logo_link`. Its contents then would create an anchor tag, which is not necessary for our case anymore, so this seems to be a great block to override.

To override it now, just add the very same block into your custom file and replace its contents:

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}

{% block layout_header_logo_link %}
    <h2>Hello world!</h2>
{% endblock %}
```

If you wanted to append your text to the logo instead of replacing it, you could add a line like this to your override: `{{ parent() }}`

And that's it already, you're done. You might have to clear the cache and refresh your storefront to see your changes in action. This can be done by using the command following command inside your command line:

bash

```shiki
./bin/console cache:clear
```

INFO

Also remember to not only activate your plugin but also to assign your theme to the correct sales channel by clicking on it in the sidebar, going to the tab Theme and selecting your theme.

### Finding variables [​](#finding-variables)

Of course this example is very simplified and does not use any variables, even though you most likely want to do that. Using variables is exactly the same as in [Twig](https://twig.symfony.com/doc/3.x/templates.html#variables) in general, so this won't be explained here in detail. Still, this is how you use a variable:

But rather than that, how do you know which variables are available to use? For this case, you can just dump all available variables:

twig

```shiki
{{ dump() }}
```

This `dump()` call will print out all variables available on this page.

INFO

Once again, the plugin called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper) adds all available page data to the Twig tab in the profiler, when opening a request and its details. This might help here as well.

## Next steps [​](#next-steps)

You are able to customize templates now, which is a good start. However, there are a few more things you should definitely learn here:

* [Adding styles](./add-custom-styling.html)
* [Adding translations](./add-translations.html)
* [Using icons](./add-icons.html)
* [Using custom assets](./add-custom-assets.html)

---

## Add custom controller

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-controller.html

# Add Custom Controller [​](#add-custom-controller)

## Overview [​](#overview)

In this guide you will learn how to create a custom Storefront controller.

## Prerequisites [​](#prerequisites)

In order to add your own controller for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

INFO

Refer to this video on **[Common Storefront controller tasks](https://www.youtube.com/watch?v=5eXXNh4cQG0)** explaining the basics about Storefront controllers. Available also on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

## Adding custom Storefront controller [​](#adding-custom-storefront-controller)

### Storefront Controller class example [​](#storefront-controller-class-example)

First of all we have to create a new controller which extends from the `StorefrontController` class. A controller is also just a service which can be registered via the service container. Furthermore, we have to define our `Route` with `defaults` and `_routeScope` via attributes, it is used to define which domain a route is part of and **needs to be set for every route**. In our case the scope is `storefront`.

INFO

Prior to Shopware 6.4.11.0 the `_routeScope` was configured by a dedicated annotation: `@RouteScope`. This way of defining the route scope is deprecated for the 6.5 major version.

Go ahead and create a new file `ExampleController.php` in the directory `<plugin root>/src/Storefront/Controller/`.

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
}
```

Now we can create a new example method with a `Route` attribute which has to contain our route, in this case it will be `/example`. The route defines how our new method will be accessible.

Below you can find an example implementation of a controller method including a route, where we render an `example.html.twig` template file with a template variable `example`.

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'])]
    public function showExample(): Response
    {
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

The name of the method does not really matter, but it should somehow fit its purpose. More important is the `Route` attribute, that points to the route `/example`. Also note its name, which is also quite important. Make sure to use prefixes `frontend`, `widgets`, `payment`, `api` or `store-api` here, depending on what your route does. The first three prefixes are necessary to identify the route as a Storefront route. If you do not want to use the prefixes, you can [add allowed route names via configuration](#allow-custom-route-names-as-storefront-routes). Inside the method, we're using the method `renderStorefront` to render a twig template file in addition with the template variable `example`, which contains `Hello world`. This template variable will be usable in the rendered template file. The method `renderStorefront` then returns a `Response`, as every routed controller method has to.

It is also possible to define the `_routeScope` per route.

INFO

Prior to Shopware 6.4.11.0 the `_routeScope` was configured by a dedicated annotation: `@RouteScope`. This way of defining the route-scope is deprecated for the 6.5 major version.

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
    public function showExample(): Response
    {
        ...
    }
}
```

### Services.xml example [​](#services-xml-example)

Next, we need to register our controller in the DI-container and make it public.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services" 
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Storefront\Controller\ExampleController" public="true">
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
        </service>
    </services>
</container>
```

Please also note the `call` tag, which is necessary in order to set the DI container to the controller.

### Routes.xml example [​](#routes-xml-example)

Once we've registered our new controller, we have to tell Shopware how we want it to search for new routes in our plugin. This is done with a `routes.xml` file at `<plugin root>/src/Resources/config/` location. Have a look at the official [Symfony documentation](https://symfony.com/doc/current/routing.html) about routes and how they are registered.

PLUGIN\_ROOT/src/Resources/config/routes.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Storefront/Controller/*Controller.php" type="attribute" />
</routes>
```

### Adding template [​](#adding-template)

Now we registered our controller and Shopware indexes the route, but the template file, that is supposed to be rendered, is still missing. Let's change that now.

As previously mentioned, the code will try to render an `index.html.twig` file. Thus, we have to create an `index.html.twig` in the `<plugin root>/src/Resources/views/storefront/page/example` directory, as defined in our controller. Below you can find an example, where we extend from the template `base.html.twig` and override the block `base_content`. In our [Customize templates](./customize-templates.html) guide, you can learn more about customizing templates.

PLUGIN\_ROOT/src/Resources/views/storefront/page/example.html.twig

twig

```shiki
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_content %}
    <h1>Our example controller!</h1>
{% endblock %}
```

### Request and Context [​](#request-and-context)

If necessary, we can access the `Request` and `SalesChannelContext` instances in our controller method.

Here's an example:

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{    
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'])]
    public function showExample(Request $request, SalesChannelContext $context): Response
    {
        ...
    }
}
```

### Allow custom route names as Storefront routes [​](#allow-custom-route-names-as-storefront-routes)

INFO

This feature is available since Shopware 6.7.2.0

To allow custom route names without a `frontend`, `widgets` or `payment` prefix, add the following configuration file to your plugin.

PLUGIN\_ROOT]/src/Resources/config/packages/storefront.yaml

yaml

```shiki
storefront:
    router:
        allowed_routes:
            - swag.test.foo-bar
```

Make sure, this file is loaded during the container build process. Overwrite the `build` method in your plugin base class to load the configuration files from the `Resources/config` directory.

PLUGIN\_ROOT/src/SwagBasicExample.php

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

Now you can use the route name `swag.test.foo-bar` in your controller without the need for a prefix.

php

```shiki
#[Route(path: '/example', name: 'swag.test.foo-bar', methods: ['GET'])]
public function showExample(Request $request, SalesChannelContext $context): Response
{
    //...
}
```

## Next steps [​](#next-steps)

Since you've already created a controller now, which is also part of creating a so-called "page" in Shopware, you might want to head over to our guide about [creating a page](./add-custom-page.html).

---

## Add caching to custom controller

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-caching-to-custom-controller.html

# Add Caching to Custom Controller [​](#add-caching-to-custom-controller)

## Overview [​](#overview)

In this guide you will learn how to define a controller route as cacheable for the HTTP cache.

## Prerequisites [​](#prerequisites)

In order to add a cache to an own controller route, you first need a plugin with a controller. Therefore, you can refer to the [Add custom controller guide](./add-custom-controller.html).

## Define the controller as cacheable [​](#define-the-controller-as-cacheable)

To define a controller route as cacheable, the default option of the route attribute `_httpCache` must be set to `true`. Once this option is set, the core takes care of everything else. If the route is called several times in the same state, a response is generated only for the first request and the second request gets the same response as the first one. It is also possible to exclude certain states from the cache. Shopware sets two different user states to which the HTTP cache reacts:

* state: `logged-in` - means that the user is logged in.
* state: `cart-filled` - means that there are products in the shopping cart.

php

```shiki
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{

    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: ['_httpCache' => true])]
    public function showExample(): Response
    {
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

## Cache invalidation [​](#cache-invalidation)

As soon as a controller route has been defined as cacheable, and the corresponding response is written to the cache, it is tagged accordingly. For this purpose, the core uses all cache tags generated during the request or loaded from existing cache entries. The cache invalidation of the Storefront controller routes is controlled by the cache invalidation of the store API routes.

For more information about Store API cache invalidation, you can refer to the [Caching Guide](./../framework/caching/).

This is because all data loaded in a controller route, is loaded in the core via the corresponding Store API routes and provided with corresponding cache tags. So the tags of the HTTP cache entries we have in the core consists of the sum of all store api tags generated or loaded during the request. Therefore the invalidation of a controller route that loads all data via the store API, no additional invalidation needs to be written.

---

## Add dynamic content via AJAX calls

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-dynamic-content-via-ajax-calls.html

# Add Dynamic Content via AJAX Calls [​](#add-dynamic-content-via-ajax-calls)

## Overview [​](#overview)

This guide will show you how to add dynamic content to your Storefront. It combines and builds upon the guides about [adding custom Javascript](./add-custom-javascript.html) and [adding a custom controller](./add-custom-controller.html), so you should probably read them first.

## Setting up the Controller [​](#setting-up-the-controller)

For this guide we will use a very simple controller that returns a timestamp wrapped in the JSON format.

INFO

Refer to this video on **[Creating a JSON controller](https://www.youtube.com/watch?v=VzREUDdpZ3E)** dealing with the creation of a controller that returns JSON data. Available also on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).

As mentioned before this guide builds up upon the [adding a custom controller](./add-custom-controller.html) guide. This means that this article will only cover the differences between returning a template and a `JSON` response and making it accessible to `XmlHttpRequests`.

PLUGIN\_ROOT/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace SwagBasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: ['XmlHttpRequest' => 'true'])]
    public function showExample(): JsonResponse
    {
        return new JsonResponse(['timestamp' => (new \DateTime())->format(\DateTimeInterface::W3C)]);
    }
}
```

As you might have seen, this controller isn't too different from the controller used in the article mentioned before. The route attribute has an added `defaults: ['XmlHttpRequest' => true]` to allow XmlHttpRequest, and it returns a `JsonResponse` instead of a normal `Response`. Using a `JsonResponse` instead of a normal `Response` causes the data structures passed to it to be automatically turned into a `JSON` string.

The following `services.xml` and `routes.xml` are identical as in the before mentioned article, but here they are for reference anyway:

PLUGIN\_ROOT/src/Resources/config/services.xmlPLUGIN\_ROOT/src/Resources/config/routes.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services" 
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="SwagBasicExample\Storefront\Controller\ExampleController" public="true">
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
        </service>
    </services>
</container>
```

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Storefront/Controller/**/*Controller.php" type="attribute" />
</routes>
```

## Preparing the Plugin [​](#preparing-the-plugin)

Now we have to add a `Storefront Javascript plugin` to display the timestamp we get from our controller.

Again this is built upon the [adding custom Javascript](./add-custom-javascript.html) article, so if you don't already know what Storefront `plugins` are, hold on and read it first.

PLUGIN\_ROOT/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js

javascript

```shiki
const { PluginBaseClass } = window;

export default class AjaxLoadPlugin extends PluginBaseClass {
    init() {
        this.button = this.el.children['ajax-button'];
        this.textdiv = this.el.children['ajax-display'];

        this._registerEvents();
    }

    _registerEvents() {
        // fetch the timestamp, when the button is clicked
        this.button.onclick = this._fetch.bind(this);
    }

    async _fetch() {
        const response = await fetch('/example');
        const data = await response.json();
        this.textdiv.innerHTML = data.timestamp;
    }
}
```

and register it in the `main.js`

PLUGIN\_ROOT/src/Resources/app/storefront/src/main.js

javascript

```shiki
import AjaxLoadPlugin from './example-plugin/example-plugin.plugin';

window.PluginManager.register('AjaxLoadPlugin', AjaxLoadPlugin, '[data-ajax-helper]');
```

## Adding the Template [​](#adding-the-template)

The only thing that is now left is to provide a template for the Storefront plugin to hook into:

PLUGIN\_ROOT/src/Resources/views/storefront/page/content/index.html.twig

twig

```shiki
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block cms_content %}
    <div>
        <h1>Swag AJAX Example</h1>

        <div data-ajax-helper>
            <div id="ajax-display"></div>
            <button id="ajax-button">Button</button>
        </div>
    </div>
{% endblock %}
```

## Next steps [​](#next-steps)

The controller we used in this example doesn't do a lot, but this pattern of providing and using data is generally the same. Even if you use it to fetch data from the database, but in that case, you probably want to learn more about the [DAL](./../../../../concepts/framework/data-abstraction-layer.html).

---

## Add custom Javascript

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-javascript.html

# Add Custom Javascript [​](#add-custom-javascript)

## Overview [​](#overview)

If you want to add interactivity to your Storefront you probably have to write your own JavaScript plugin. Here you will be guided through the process of writing and registering your own JavaScript plugins. You will write a plugin that simply checks if the user has scrolled to the bottom of the page and then creates an alert.

## Prerequisites [​](#prerequisites)

You need for this guide a running plugin and therefore a running Shopware 6 instance, with full access to all files. This also includes access to the command line to execute a command, which then builds the Storefront. A general understanding of vanilla JavaScript ES6 is also mandatory. Everything else is explained in this guide itself.

## Writing a JavaScript plugin [​](#writing-a-javascript-plugin)

Storefront JavaScript plugins are vanilla JavaScript ES6 classes that extend from our Plugin base class. For more information, refer to [JavaScript classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) section.

The directory to create custom javascript plugins should be the following, which represents the same structure like the core: `<plugin root>/src/Resources/app/storefront/src/`

In there, you create a new directory, named after your plugin. In this guide, this will be called `example-plugin`, so the full path would look like this: `<plugin root>/src/Resources/app/storefront/src/example-plugin`

Now create an actual file for your JavaScript plugin, in this example it will be called `example-plugin.plugin.js`.

Inside this file create and export an ExamplePlugin class that extends the base Plugin class:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
}
```

This is just a basic vanilla JavaScript ES6 class, which extends the `Plugin` class.

Each plugin has to implement the `init()` method. This method will be called when your plugin gets initialized and is the entrypoint to your custom logic. The plugin initialization runs on `DOMContentLoaded` event, so you can be sure, that the dom is already completely loaded. In your case you add a callback to the `scroll` event from the window and check if the user has scrolled to the bottom of the page. If so we display an alert. Your full plugin now looks like this:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        window.addEventListener('scroll', this.onScroll.bind(this));
    }

    onScroll() {
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            alert('Seems like there\'s nothing more to see here.');
        }
    }
}
```

A short explanation what the condition is doing here: The `window.innerHeight` contains the height of the window, as you might have guessed.

This is added to `window.pageYOffset`, which contains the current scroll position on the Y-axis. It represents the **top** value of the current scroll, which basically means: If your website is 5000px high and you scroll to the very bottom, the value would **not** be 5000px, but rather `5000px - window.innerHeight`. Thus, we have to add up the `innerHeight` to actually get the bottom of the website.

Well, and then we check if this sum is bigger or equal the total size of your website, by fetching the height of your website's `body` tag. If it is higher or equal the total height of the website, you reached the end of the website.

## Registering your plugin [​](#registering-your-plugin)

Next you have to tell Shopware that your plugin should be loaded and executed. Therefore you have to register your plugin in the PluginManager.

Shopware is automatically looking for a `main.js` file in a directory `<plugin root>/src/Resources/app/storefront/src`, which then will be loaded automatically. Consider this to be your main storefront JavaScript entrypoint.

Create a `main.js` file inside your `<plugin root>/src/Resources/app/storefront/src` folder and get the PluginManager from the global window object. Then register your own plugin:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
// Import all necessary Storefront plugins
import ExamplePlugin from './example-plugin/example-plugin.plugin';

// Register your plugin via the existing PluginManager
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', ExamplePlugin);
```

Right now, your plugin will automatically be loaded once you load the website.

## Binding your plugin to the DOM [​](#binding-your-plugin-to-the-dom)

You can also bind your plugin to a DOM element by providing a css selector:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
// Import all necessary Storefront plugins
import ExamplePlugin from './example-plugin/example-plugin.plugin';

// Register your plugin via the existing PluginManager
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', ExamplePlugin, '[data-example-plugin]');
```

In this case the plugin just gets executed if the HTML document contains at least one element with the `data-example-plugin` attribute. You can then use `this.el` inside your plugin to access the DOM element your plugin is bound to.

## Registering an async plugin [​](#registering-an-async-plugin)

You can also register an async JS-plugin. Instead of importing a JS-plugin file at the top of your `main.js`, you can provide a dynamic import inside `PluginManager.register()`. The import path can remain the same as the synchronous import.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js

// Register your plugin via the existing PluginManager using a dynamic import
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', () => import('./example-plugin/example-plugin.plugin'), '[data-example-plugin]');
```

If an async/dynamic import is provided, then the JS-plugin will be recognized as async by the PluginManager automatically. This means that, the registered JS-plugin will not be included in the main bundled JavaScript (storefront.js) by default. The JS-plugin will only be downloaded on-demand if the plugin selector (`[data-example-plugin]`) is found on the current page, see [Loading your plugin](#loading-your-plugin).

Using an async JS-plugin can be helpful when the plugin is not supposed to be loaded on every page and should only be loaded when it is actually needed. This can reduce the size of the initially loaded JavaScript in the browser. When using the "normal" import (`import ExamplePlugin from './example-plugin/example-plugin.plugin';`) in comparison, the JS-plugin will always be included in the JavaScript on all pages.

### Loading your plugin [​](#loading-your-plugin)

The following will create a new template with a very short explanation. If you're looking for more information on what's going on here, head over to our guide about [Customizing templates](./customize-templates.html).

You bound your plugin to the css selector `[data-example-plugin]`, so you have to add DOM elements with this attribute on the pages you want your plugin to be active.

Create a `<plugin root>/src/Resources/views/storefront/page/content/` folder and create a `index.html.twig` template. Inside this template, extend from the `@Storefront/storefront/page/content/index.html.twig` and overwrite the `base_main_inner` block. After the parent content of the blog, add a template tag that has the `data-example-plugin` attribute.

A lot of text, here is the respective example:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    {{ parent() }}

    <template data-example-plugin></template>
{% endblock %}
```

With this template extension your plugin is active on every content page, like the homepage or category listing pages.

## Configuring your plugins [​](#configuring-your-plugins)

You can configure your plugins from inside the templates via data-options. First you have to define a static `options` object inside your plugin and assign your options with default values to it. In your case define a `text` option and as a default value use the text you previously directly prompted to the user. And instead of the hard coded string inside the `alert()`, use your new option value.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    static options = {
        /**
         * Specifies the text that is prompted to the user
         * @type string
         */
        text: 'Seems like there\'s nothing more to see here.',
    };

    init() {
        window.addEventListener('scroll', this.onScroll.bind(this));
    }

    onScroll() {
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            alert(this.options.text);
        }
    }
}
```

Now you are able to override the text that is prompted to the user from inside your templates. For this example we're going to display another message on product detail pages.

Therefore create a `product-detail` folder inside your `<plugin root>/src/Resources/views/storefront/page` folder and add an `index.html.twig` file inside that folder. In your template extend from the default `@Storefront/storefront/page/product-detail/index.html.twig` and override the block `page_product_detail_content`.

After the parent content add a template tag with the `data-example-plugin` tag to activate your plugin on product detail pages as well. Next add a `data-{your-plugin-name-in-kebab-case}-options` (in this example: `data-example-plugin-options`) attribute to the DOM element you registered your plugin on (the template tag). The value of this attribute are the options you want to override as a JSON object.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/product-detail/index.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}

{% set examplePluginOptions = {
    text: "Are you not interested in this product?"
} %}

{% block page_product_detail_content %}
    {{ parent() }}

    <template data-example-plugin data-example-plugin-options='{{ examplePluginOptions|json_encode }}'></template>
{% endblock %}
```

It is best practice to use a variable for the options because this is extendable from plugins.

## Modify existing options [​](#modify-existing-options)

We've just mentioned the best practice to use a template variable for setting plugin options, so other plugins can extend those options. This section will explain how to do actually achieve that.

You can use the `replace_recursive` Twig filter for this case.

Imagine the following example can be found in the core:

twig

```shiki
{% set productSliderOptions = {
    productboxMinWidth: sliderConfig.elMinWidth.value ? sliderConfig.elMinWidth.value : '',
    slider: {
        gutter: 30,
        autoplayButtonOutput: false,
        nav: false,
        mouseDrag: false,
        controls: sliderConfig.navigation.value ? true : false,
        autoplay: sliderConfig.rotate.value ? true : false
    }
} %}

{% block element_product_slider_slider %}
    <div class="base-slider"
         data-product-slider="true"
         data-product-slider-options="{{ productSliderOptions|default({})|json_encode|escape('html_attr') }}">
    </div>
{% endblock %}
```

Now you want to overwrite the value `slider.mouseDrag` with your plugin. The variable can be overwritten with `replace_recursive`:

twig

```shiki
{% block element_product_slider_slider %}
    {% set productSliderOptions = productSliderOptions|replace_recursive({
        slider: {
            mouseDrag: true
        }
    }) %}

    {{ parent() }}
{% endblock %}
```

## Plugin script path [​](#plugin-script-path)

For JavaScript you normally would have two locations where your `*.js` files are located. You have your `main.js` as an entry point inside of the following directory: `<plugin root>/src/Resources/app/storefront/src`.

Shopware will then compile the JavaScript and save the compiled version at `<plugin root>/src/Resources/app/storefront/dist/storefront/js/<plugin-name>/<plugin-name>.js`. These files will be recognized automatically by Shopware.

Make sure to ship the compiled file with your plugin as well.

## Testing your changes [​](#testing-your-changes)

To see your changes you have to build the Storefront. Use the following command and reload your Storefront:

If you now scroll to the bottom of your page an alert should appear.

## Next steps [​](#next-steps)

You've got your own first javascript plugin running. You might want to start [listening to javascript events](./reacting-to-javascript-events.html) now, or even [override other javascript plugins](./override-existing-javascript.html) instead.

---

## Override existing Javascript

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/override-existing-javascript.html

# Override Existing Javascript [​](#override-existing-javascript)

## Overview [​](#overview)

If you have to customize the logic of some core JavaScript Storefront plugins you can override them with your own implementations. You will see how this works by extending the cookie permission plugin and showing the cookie notice on every page load and asking the user if he wants to hide cookie bar via a confirm dialogue.

## Prerequisites [​](#prerequisites)

While this is not mandatory, having read the guide about [adding custom javascript plugins](./add-custom-javascript.html) in the first place might help you understand this guide a bit further. Other than that, this guide just requires you to have a running plugin installed, e.g. our plugin from the [Plugin base guide](./../plugin-base-guide.html).

## Extending an existing JavaScript plugin [​](#extending-an-existing-javascript-plugin)

As JavaScript Storefront plugins are vanilla JavaScript classes, you can simply extend them.

INFO

Each JavaScript plugin can only be overridden once. If two Shopware plugins try to override the same plugin, only the last one of them will actually work.

So let's start with creating the proper directory structure. This example will be called `my-cookie-permission`, as it's extending the default `cookie-permission` plugin.

So for this example you create a `<plugin root>/src/Resources/app/storefront/src/my-cookie-permission` directory and put an empty file `my-cookie-permission.plugin.js` in there. The latter will be your main plugin class file.

Next you create a JavaScript class that extends the original CookiePermission plugin inside your previously created file:

javascript

```shiki
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';

export default class MyCookiePermission extends CookiePermissionPlugin {
}
```

The first line just imports the original `cookie-permission` plugin class, so you can extend from it.

If you aren't able to import the original plugin class (for example third-party plugins without an alias) you can make use of the `window.PluginManager` object to get it.

javascript

```shiki
const PluginManager = window.PluginManager
const Plugin = PluginManager.getPlugin('CookiePermission')
const PluginClass = Plugin.get('class')

export default class MyCookiePermission extends PluginClass {
}
```

Now you can override the functions from the parent class.

### Always show the cookie bar [​](#always-show-the-cookie-bar)

Let's start with the function, that the cookie bar should *always* show up, no matter if the user already configured his cookie preferences or not. By having a look at the [original cookie permission plugin](https://github.com/shopware/shopware/blob/v6.3.4.0/src/Storefront/Resources/app/storefront/src/plugin/cookie/cookie-permission.plugin.js#L46-L53), we can see that it's only shown when the item `this.options.cookieName` is set in the `CookieStorage`. The latter is just a neat helper from Shopware 6 itself to simplify dealing with cookies in JavaScript.

So we'll just override the `init()` method and make sure this value is always set to an empty string, which will evaluate to `false`.

After that you call the `init()` method of the original plugin.

javascript

```shiki
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

export default class MyCookiePermission extends CookiePermissionPlugin {
    init() {
        CookieStorage.setItem(this.options.cookieName, '');
        super.init();
    }
}
```

So now the cookie will always be set to an empty string, resulting in the cookie bar always being shown after a page reload.

### Adding confirm dialogue [​](#adding-confirm-dialogue)

Upon clicking the "Accept" or "Deny" button, you want to prompt a confirm dialogue if the user wants to hide the cookie bar. Therefore you override the `_hideCookieBar()` function to show the dialogue and only call the parent implementation if the user clicks "OK" in the confirm dialogue. So your whole plugin now looks like this:

javascript

```shiki
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

export default class MyCookiePermission extends CookiePermissionPlugin {
    init() {
        CookieStorage.setItem(this.options.cookieName, '');
        super.init();
    }

    _hideCookieBar() {
        if (confirm('Do you want to hide the cookie bar?')) {
            super._hideCookieBar();
        }
    }
}
```

Of course, if the user reloads the page, the bar will be back up.

### Register your extended plugin [​](#register-your-extended-plugin)

A few things are now missing to actually register your overridden plugin version. Currently, Shopware doesn't even know your overridden plugin, so let's introduce it to Shopware.

Create a new file called `main.js` in the directory `<plugin root>/src/Resources/app/storefront/src/`, which represents the automatically loaded entry point for javascript files in a plugin.

Next you have to register your extended plugin using the `PluginManager` from the global window object for this. But instead of using the `register()` function to register a new plugin, you use the `override()` function to indicate that you want to override an existing plugin.

javascript

```shiki
import MyCookiePermission from './my-cookie-permission/my-cookie-permission.plugin';

const PluginManager = window.PluginManager;
PluginManager.override('CookiePermission', MyCookiePermission, '[data-cookie-permission]');
```

INFO

If the plugin you want to override is an async plugin, the import of your override plugin has to be async as well. See also [Registering an async plugin](./add-custom-javascript.html#registering-an-async-plugin)

javascript

```shiki
const PluginManager = window.PluginManager;

// If the plugin "CookiePermission" is registered async, you also override it with an async/dynamic import
PluginManager.override('CookiePermission', () => import('./my-cookie-permission/my-cookie-permission.plugin'), '[data-cookie-permission]');
```

### Testing your changes [​](#testing-your-changes)

To see your changes you have to build the Storefront. Use the following command and reload your Storefront.

You should see the cookie notice at the bottom of the page. If you click the "Accept" or the "Deny" button you should be prompted to confirm hiding the bar.

## Next steps [​](#next-steps)

Sometimes you don't have to actually override a javascript plugin, since sometimes you can simply use an event instead. Learn how this is done in our guide about [listening to events](./reacting-to-javascript-events.html).

---

## Add Javascript as script tag

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-javascript-as-script-tag.html

# Add JavaScript as script tag [​](#add-javascript-as-script-tag)

## Overview [​](#overview)

You often want to add your JavaScript to your main entry point `<plugin root>/src/Resources/app/storefront/src/main.js` to automatically compile it alongside the Storefront JavaScript. Please refer to [Add custom Javascript](./add-custom-javascript.html) for more information.

However, you might want to add JavaScript as a separate `<script>` tag in the HTML. For example, to load a script from an external CDN. You will learn how to extend the template to add a `<script>` tag.

## Prerequisites [​](#prerequisites)

For this guide, you need a running plugin, Shopware 6 instance, and full access to all files. You also need a brief understanding of how a [template extension](./customize-templates.html) works.

## Adding JavaScript as a separate script tag [​](#adding-javascript-as-a-separate-script-tag)

You can extend the default template that includes the `<head>` section of the page: `src/Storefront/Resources/views/storefront/layout/meta.html.twig`. While it is possible to add a `<script>` anywhere in the HTML via template extensions, it is recommended to include your script alongside the default scripts by extending the block `layout_head_javascript_hmr_mode`.

twig

```shiki
{# <plugin root>/src/Resources/views/storefront/layout/meta.html.twig #}
{% sw_extends '@Storefront/storefront/layout/meta.html.twig' %}

{% block layout_head_javascript_hmr_mode %}
    {# Renders Storefront script: <script src="https://your-shop.example/theme/747e1c6a73cf4d70f5e831b30554dd15/js/all.js?1698139296" defer></script> #}
    {{ parent() }}

    {# Your script #}
    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
{% endblock %}
```

This will render:

html

```shiki
<head>
    <!-- Other tags are rendered here... -->

    <script src="https://your-shop.example/theme/747e1c6a73cf4d70f5e831b30554dd15/js/all.js?1698139296" defer></script>
    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
</head>
```

DANGER

If you are extending the block `layout_head_javascript_hmr_mode` to add your script, you must always use the `{{ parent() }}` function to render the Storefront JavaScript as well. Otherwise, the core JS functionalities of the Storefront will be overwritten and will stop working. This should only happen when you **explicitly** want this.

### Conditional scripts [​](#conditional-scripts)

Instead of continually rendering your `<script>`, you can also put it behind a condition in Twig. Then the script will only be rendered when the Twig condition is met.

twig

```shiki
{# <plugin root>/src/Resources/views/storefront/layout/meta.html.twig #}
{% sw_extends '@Storefront/storefront/layout/meta.html.twig' %}

{% block layout_head_javascript_hmr_mode %}
    {{ parent() }}

    {# Only add script when condition is met #}
    {% if someCondition %}
        <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
    {% endif %}
{% endblock %}
```

### Script order [​](#script-order)

Should your `<script>` tag come before or after the Storefront core JavaScript? It depends on whether you need to have access to the code added by your `<script>` within the Storefront JavaScript (added by `<plugin root>/src/Resources/app/storefront/src/main.js`).

* If you **don't** need access within the Storefronts JavaScript, you should add the `<script>` **after** the Storefront JavaScript.
* If you **do need** access, your `<script>` should come **before** the Storefront JavaScript.

WARNING

Please consider that non-async `<script src="#">` that are added before the Storefront JavaScript will postpone its execution. Too many scripts can have a negative effect on the shop's performance.

### Script loading behavior [​](#script-loading-behavior)

Using the `defer` attribute is recommended to tell the browser that the script is meant to be executed after the document has been parsed. However, if you add a library as `<script>`, please consult the library documentation. Some libraries are supposed to be loaded with `async` attribute.

WARNING

It should be avoided to add external `<script src="#">` without `defer` or `async` because it will block rendering of the site until the script is executed. This can have a negative effect on the shop's performance.

### Alternative script locations [​](#alternative-script-locations)

You can also add a `<script>` near the body using block `base_body_script` in `src/Storefront/Resources/views/storefront/base.html.twig`. It is possible to add `<script>` at every location the Twig blocks offer.

INFO

Alternative script locations should only be used when there is a technical reason. For example, when the documentation of an external library recommends a specific script location inside the HTML.

---

## Add custom assets

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-assets.html

# Add Custom Assets [​](#add-custom-assets)

## Overview [​](#overview)

When working with an own plugin, the usage of own custom images or other assets is a natural requirement. So of course you can do that in Shopware. In this guide we will discover together how it's possible to add and use custom assets in your Shopware plugin.

## Prerequisites [​](#prerequisites)

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the [Plugin base guide](./../plugin-base-guide.html)

Needless to say, you should have your image or another asset at hand to work with.

## Adding custom assets to your plugin [​](#adding-custom-assets-to-your-plugin)

In order to add custom assets to your theme, you need to create a new folder called public inside the `src/Resources` directory of your plugin. Here you're able to store your assets files, so please feel free to save your image there - we'll do the same thing in our example plugin.

bash

```shiki
# PluginRoot
.
├── composer.json
└── src
    ├── Resources
    │   ├── public
    │   │   └── your-image.png <-- Asset file here
    └── SwagBasicExample.php
```

Afterwards, you need to make sure your plugin assets are copied over to the public/bundles folder. However, don't to this by hand - the command `bin/console assets:install` will take care of it.

text

```shiki
# shopware-root/public/bundles
.
├── administration
├── framework
├── storefront
└── swagbasicexample
    └── your-image.png <-- Your asset is copied here
```

## Linking to assets [​](#linking-to-assets)

### Using custom assets in your template [​](#using-custom-assets-in-your-template)

Let's think about a simple example, displaying our image right in the base template of the Storefront. In there we're able to link our assets by simply using the [asset](https://symfony.com/doc/current/templates.html#linking-to-css-javascript-and-image-assets) function Symfony provides:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/base.html.twig
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_main %}
    <h2>Asset:</h2>

    {# Using asset function to display our custom asset #}
    <img src="{{ asset('bundles/swagbasicexample/image.png', 'asset') }}">
    {{ parent() }}
{% endblock %}
```

That's basically all you need to do to link your plugin's custom assets.

### Using custom assets in your CSS files [​](#using-custom-assets-in-your-css-files)

There's one more interesting possibility though. If you want, you can use your custom asset in your CSS files. Look at the following example:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background-image: url("#{$sw-asset-public-url}/bundles/swagbasicexample/image.png");
}
```

You see, we can use our custom assets by using the asset path provided by the `bundle` directory.

### Adding custom assets in themes [​](#adding-custom-assets-in-themes)

Of course, you're able to use custom assets in themes as well. In this context there's another way on integration custom assets into your theme. Please take a look on the guide about adding assets to a theme for further detail:

[Add assets to a Theme](../../themes/add-assets-to-theme)

## Next steps [​](#next-steps)

One of the said custom assets are medias. For more information on that, refer to [Media and thumbnails](./use-media-thumbnails.html).

---

## Add custom captcha

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-captcha.html

# Add custom captcha [​](#add-custom-captcha)

## Overview [​](#overview)

You can add your custom captcha to the Shopware 6 core. This guide will show you how to do that.

## Prerequisites [​](#prerequisites)

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the [Plugin base guide](./../plugin-base-guide.html)

## Adding custom captcha to your plugin [​](#adding-custom-captcha-to-your-plugin)

In order to add custom captcha to your plugin, create a new folder called `Captcha` inside the `src/Framework` directory of your plugin. This is optional, but it's a good practice to keep your plugin files organized.

Take a look at the AbstractCaptcha class. This class is the base class for all captcha types. It contains the following methods:

* `supports(string $type): bool` - This method is used to check if the captcha type is supported by the plugin.
* `isValid(string $code): bool` - This method is used to check if the captcha code is valid.
* `getName(): string` - This method is used to get the name of the captcha type.
* `shouldBreak(): bool` - This method is used to check if the captcha should break the validation.
* `getData(): array` - This method is used to get the data of the captcha type.
* `getViolations(): ConstraintViolationListInterface` - This method is used to get the violations of the captcha type.

Extend the AbstractCaptcha class and implement the methods isValid and getName. The isValid method should return true if the captcha code is valid, false otherwise. The getName method should return the name of the captcha type.

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Storefront\Framework\Captcha;

use GuzzleHttp\ClientInterface;
use Psr\Http\Client\ClientExceptionInterface;
use Shopware\Core\Framework\Log\Package;
use Symfony\Component\HttpFoundation\Request;

#[Package('storefront')]
class YourCaptcha extends AbstractCaptcha
{
    final public const CAPTCHA_NAME = 'yourCaptchaName';
    final public const CAPTCHA_REQUEST_PARAMETER = '_your_captcha_name';
    private const YOUR_CAPTCHA_ENDPOINT = 'https://www.yourcaptcha.com/verify';

    /**
     * @internal
     */
    public function __construct(private readonly ClientInterface $client)
    {
    }

    /**
     * {@inheritdoc}
     */
    public function isValid(Request $request, array $captchaConfig): bool
    {
        if (!$request->get(self::CAPTCHA_REQUEST_PARAMETER)) {
            return false;
        }
        
        try {
            $response = $this->client->request('POST', self::GOOGLE_CAPTCHA_VERIFY_ENDPOINT, [
                'form_params' => [
                    'response' => $request->get(self::CAPTCHA_REQUEST_PARAMETER),
                    'remoteip' => $request->getClientIp(),
                ],
            ]);

            $responseRaw = $response->getBody()->getContents();
            $response = json_decode($responseRaw, true);

            return $response && (bool) $response['success'];
        } catch (ClientExceptionInterface) {
            return false;
        }
    }

    /**
     * {@inheritdoc}
     */
    public function getName(): string
    {
        return self::CAPTCHA_NAME;
    }
}
```

## Google reCAPTCHA v3 example [​](#google-recaptcha-v3-example)

You might want to check out the example [GoogleReCaptchaV3](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Framework/Captcha/GoogleReCaptchaV3.php) class from the Shopware 6 core. It's a good example of how to implement a custom captcha type.

---

## Add custom styling

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-styling.html

# Add Custom Styling [​](#add-custom-styling)

## Overview [​](#overview)

Quite often your plugin will have to change a few templates for the Storefront. Those might require custom styling to look neat, which will be explained in this guide.

## Prerequisites [​](#prerequisites)

You won't learn to create a plugin in this guide, head over to our [Plugin base guide](./../plugin-base-guide.html) to create a plugin first, if you don't know how it is done yet. Also knowing and understanding [SCSS](https://sass-lang.com/documentation/) will be quite mandatory to fully understand what is going on here.

Other than having those two requirements, nothing else is necessary for this guide.

## Adding (S)CSS files [​](#adding-s-css-files)

By default, Shopware 6 is looking for a `base.scss` file in your plugin. To be precise, this file has to be inside the directory `<plugin root>/src/Resources/app/storefront/src/scss` in order to be properly found and loaded by Shopware.

So just try it out, create a `base.scss` file in the directory mentioned above.

Inside of the `.scss` file, we add some basic styles to see if it's actually working. In this example, the background of the `body` will be changed.

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background: blue;
}
```

### Adding variables [​](#adding-variables)

In case you want to use the same color in several places, but want to define it just one time, you can use variables for this.

Create a `abstract/variables.scss` file inside your `<plugin root>/src/Resources/app/storefront/src/scss` directory and define your background color variable.

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/abstract/variables.scss
// in variables.scss
$sw-storefront-assets-color-background: blue;
```

Inside your `base.scss` file you can now import your previously defined variables and use them:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
@import 'abstract/variables.scss';

body {
    background: $sw-storefront-assets-color-background;
}
```

This comes with the advantage that when you want to change this color for all occurrences, you only have to change this variable once and the hard coded values are not cluttered all over the codebase.

INFO

Refer to the theme guide **[Override Bootstrap Variables in a Theme](./../../themes/override-bootstrap-variables-in-a-theme.html)** if you want to override some of the default Shopware variables.

### Testing its functionality [​](#testing-its-functionality)

Now you want to test if your custom styles actually apply to the Storefront. For this, you have to execute the compiling and building of the `.scss` files first. This is done by using the following command:

If you want to see all style changes made by you live, you can also use our Storefront hot-proxy for that case:

Using the hot-proxy command, you will have to access your store with the port `9998`, e.g. `domainToYourEnvironment.in:9998`.

That's it! Open the Storefront and see it turning blue due to your custom styles!

---

## Add custom icons

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-icons.html

# Add Custom Icons [​](#add-custom-icons)

## Overview [​](#overview)

In this guide you will learn how to use the icon renderer component as well as adding custom icons.

INFO

Even if this is originally a plugin guide, everything will work perfectly in a theme as well. Actually, a theme even is a kind of plugin. So don't get confused by us talking about plugins here.

## Prerequisites [​](#prerequisites)

In order to follow this guide easily, you first need to have a functioning plugin installed. Head over to our [Plugin base guide](./../plugin-base-guide.html) to create a plugin, if you don't know how it's done yet. Also knowing and understanding SCSS will be quite mandatory to fully understand what's going on here. Furthermore, it might be helpful to read the guide on how to [handle own assets](./add-custom-assets.html) in your plugin before you start with this one.

## Adding icon [​](#adding-icon)

In order to add any icons to the Storefront, you use our `sw_icon` twig action. This way, an icon of choice is displayed in the Storefront.

Needless to say, the first step is saving your image somewhere in your plugin where Shopware can find it. The default path for icons is the following:

text

```shiki
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/default
`
```

You can also provide "solid" icons or any other custom pack names which can be configured later with the `pack` parameter. You can do that by creating a folder with the pack name:

text

```shiki
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/<pack-name>
```

By default, Shopware looks inside the "default" folder.

twig

```shiki
{% sw_icon 'done-outline-24px' style {
    'namespace': 'TestPlugin'
} %}
```

INFO

When you want to see all icons available to the Storefront by default, see [here](https://github.com/shopware/shopware/tree/trunk/src/Storefront/Resources/app/storefront/dist/assets/icon). They are available as `default` and `solid` icon pack.

Imagine you want to use the default `checkmark` icon from the `solid` pack. In this case,

You surely want to add your own custom icons. In this case, the `namespace` parameter is the most important one to configure. In there, you need to set the name of the theme in which the icon is searched for by its name.

WARNING

If you configure no deviating namespace, Shopware will display the Storefront's default icons.

However, these are not all of your possibilities of configuration. As you see, you're able to configure even more things. Let's take a look at the `style` object's possible parameters:

| Configuration | Description | Remarks |
| --- | --- | --- |
| `size` | Sets the size of the icon | --- |
| `namespace` | Selection of the namespace of the icon, you can compare it with the source of it | Important configuration if you want to use custom icons. |
| `pack` | Selects the pack of different icons | --- |
| `color` | Sets the color of the icon | --- |
| `class` | Defines a class of the icon | --- |

A simple but fully functional example could look like below:

twig

```shiki
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_body %}

    {# We want to set our own icon here #}
    <h1>Custom icon:</h1>
    {% sw_icon 'done-outline-24px' style {
        'size': 'lg',
        'namespace': 'TestPlugin',
        'pack': 'solid'
    } %}
    {{ parent() }}

{% endblock %}
```

DANGER

Icons or other custom assets are not included in the theme inheritance.

Inside your theme, you cannot put an icon in a directory corresponding the core folder structure and expect the core one to be automatically overwritten by it, as you are used to with themes in general.

---

## Add custom page

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-page.html

# Add Custom Page [​](#add-custom-page)

## Overview [​](#overview)

In this guide, you will learn how to create a custom page for your Storefront. A page in general consists of a controller, a page loader, a "page loaded" event and a page class, which is like a struct and contains the most necessary data for the page.

## Prerequisites [​](#prerequisites)

To add your own custom page for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html). Since you need to load your page with a controller, you might want to have a look at our guide about [creating a controller](./add-custom-controller.html) first. The controller created in the previously mentioned controller guide will also be used in this guide.

## Adding custom page [​](#adding-custom-page)

In the following sections, we'll create each of the necessary classes one by one. The first one will be a controller, whose creation is not going to be explained here again. Have a look at the guide about [creating a controller](./add-custom-controller.html) to see why it works.

### Creating ExampleController [​](#creating-examplecontroller)

Let's have a look at an example controller.

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\PlatformRequest;
use Shopware\Storefront\Framework\Routing\StorefrontRouteScope;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StorefrontRouteScope::ID]])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example-page', name: 'frontend.example.page', methods: ['GET'])]
    public function examplePage(): Response
    {
    }
}
```

It has a method `examplePage`, which is accessible via the route `example-page`. This method will be responsible for loading your page later on, but we'll leave it like that for now.

Don't forget to [register your controller via the DI](./add-custom-controller.html#services-xml-example).

### Creating the pageloader [​](#creating-the-pageloader)

To stick to Shopware's default location for the page loader, we'll have to create a new directory: `<plugin root>/src/Storefront/Page/Example`.

In there, we will proceed to create all page related classes, such as the page loader.

Go ahead and create a new file called `ExamplePageLoader.php`. It's a new service, which doesn't have to extend from any other class. You might want to implement a `ExamplePageLoaderInterface` interface, which is not explained in this guide. You can do that to have a decoratable page loader class.

The page loader is responsible for creating your page class instance (`ExamplePage`, will be created in the next section), filling it with data, e.g. from store api, and firing a `PageLoaded` event, so others can react to your page being loaded. Do not use a repository directly in a page loader. Always get the data for your pages from a store api route instead.

Let's have a look at a full example `ExamplePageLoader`:

PLUGIN\_ROOT/src/Storefront/Page/Example/ExamplePageLoader.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\GenericPageLoaderInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageLoader
{
    private GenericPageLoaderInterface $genericPageLoader;

    private EventDispatcherInterface $eventDispatcher;

    public function __construct(GenericPageLoaderInterface $genericPageLoader, EventDispatcherInterface $eventDispatcher)
    {
        $this->genericPageLoader = $genericPageLoader;
        $this->eventDispatcher = $eventDispatcher;
    }

    public function load(Request $request, SalesChannelContext $context): ExamplePage
    {
        $page = $this->genericPageLoader->load($request, $context);
        $page = ExamplePage::createFrom($page);

        // Do additional stuff, e.g. load more data from store api and add it to page
         $page->setExampleData(...);

        $this->eventDispatcher->dispatch(
            new ExamplePageLoadedEvent($page, $context, $request)
        );

        return $page;
    }
}
```

So first of all, as already mentioned: This is a new class or service, which doesn't have to extend from any other class. The constructor is passed two arguments: The `GenericPageLoaderInterface` and the `EventDispatcherInterface`.

The first one is not necessary, but useful, since it loads all kinds of default page data.

The `EventDispatcherInterface` is of course necessary to fire an event later on.

Every page loader should implement a `load` method, which is not mandatory, but convention. You want your page loader to work like all the other page loaders, right? It should return an instance of your example page, in this case `ExamplePage`. Don't worry, we haven't created that one yet, it will be created in the next sections. So, the first thing it does is basically creating a `Page` instance, containing basic data, like the meta-information.

Afterwards, you're creating your own page instance by using the method `createFrom`. This method is available, since your `ExamplePage` has to extend from the `Page` struct, which in return extends from the `Struct` class. The latter implements the [CreateFromTrait](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Framework/Struct/CreateFromTrait.php) containing this method. In short, this will create an instance of your `ExamplePage`, containing all the data from the generic `Page` object.

Afterwards, you can add more data to your page instance by using a setter. Of course, your example page class then has to have such a setter method, as well as a getter.

As already mentioned, you should also fire an event once your page was loaded. For this case, you need a custom page loaded event class, which is also created in the next sections. It will be called `ExamplePageLoadedEvent`.

The last thing to do in this method is to return your new page instance.

Remember to register your new page loader in the DI container:

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<service id="Swag\BasicExample\Storefront\Page\Example\ExamplePageLoader" public="true">
    <argument type="service" id="Shopware\Storefront\Page\GenericPageLoader" />
    <argument type="service" id="event_dispatcher"/>
</service>
```

#### Adjusting the controller [​](#adjusting-the-controller)

Theoretically, this is all your page loader does - but it's not being used yet. Therefore, you have to inject your page loader to your custom controller and execute the `load` method.

PLUGIN\_ROOT/src/Storefront/Controller/ExampleController.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

...

class ExampleController extends StorefrontController
{
    private ExamplePageLoader $examplePageLoader;

    public function __construct(ExamplePageLoader $examplePageLoader)
    {
        $this->examplePageLoader = $examplePageLoader;
    }

    #[Route(path: '/example-page', name: 'frontend.example.page', methods: ['GET'])]
    public function examplePage(Request $request, SalesChannelContext $context): Response
    {
        $page = $this->examplePageLoader->load($request, $context);

        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world',
            'page' => $page
        ]);
    }
}
```

Note, that we've added the page to the template variables.

#### Adjusting the services.xml [​](#adjusting-the-services-xml)

In addition, it is necessary to pass the argument with the ID of the `ExamplePageLoader` class to the [configuration](./add-custom-controller.html#services-xml-example) of the controller service in the `services.xml`.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<service id="Swag\BasicExample\Storefront\Controller\ExampleController" public="true">
    <argument type="service" id="Swag\BasicExample\Storefront\Page\Example\ExamplePageLoader" />
    <call method="setContainer">
        <argument type="service" id="service_container"/>
    </call>
</service>
```

### Creating the example page [​](#creating-the-example-page)

So now we're going to create the example page class, that was already used in our page loader, `ExamplePage`.

It has to extend from the `Shopware\Storefront\Page\Page` class to contain the meta information, as well as some helper methods.

Let's have a look at an example:

PLUGIN\_ROOT/src/Storefront/Page/Example/ExamplePage.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Storefront\Page\Page;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExamplePage extends Page
{
    protected ExampleEntity $exampleData;

    public function getExampleData(): ExampleEntity
    {
        return $this->exampleData;
    }

    public function setExampleData(ExampleEntity $exampleData): void
    {
        $this->exampleData = $exampleData;
    }
}
```

As explained in the page loader section, your page can contain all kinds of custom data. It has to provide a getter and a setter for the custom data, so it can be applied and read. In this example, the entity from our guide about [creating custom complex data](./../framework/data-handling/add-custom-complex-data.html#entity-class) is being used.

And that's it already. Your page is ready to go.

### Creating the page loaded event [​](#creating-the-page-loaded-event)

One more class is missing, the custom event class. It has to extend from the `Shopware\Storefront\Page\PageLoadedEvent` class.

Its constructor parameter will be the `ExamplePage`, which it has to save into a property and there needs to be a getter to get the example page instance. Additional constructor parameters are the `Request` and the `SalesChannelContext`, which you have to pass to the parent's constructor.

Here's the example:

PLUGIN\_ROOT/src/Storefront/Page/Example/ExamplePageLoadedEvent.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\PageLoadedEvent;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageLoadedEvent extends PageLoadedEvent
{
    protected ExamplePage $page;

    public function __construct(ExamplePage $page, SalesChannelContext $salesChannelContext, Request $request)
    {
        $this->page = $page;
        parent::__construct($salesChannelContext, $request);
    }

    public function getPage(): ExamplePage
    {
        return $this->page;
    }
}
```

And that's it for your `ExamplePageLoadedEvent` class.

Your example page should now be fully functioning.

## Next steps [​](#next-steps)

You've now successfully created a whole new page, including a custom controller, a custom template, and the necessary classes to create a new page, a loader, the page struct and the page loaded event.

In your `load` method, you've used the `GenericPageLoader`, which takes care of the meta-information of the page. There are also "pagelets", basically reusable fractions of a page. Learn how to [create a custom pagelet](./add-custom-pagelet.html).

---

## Add custom pagelet

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-pagelet.html

# Add Custom Pagelet [​](#add-custom-pagelet)

## Overview [​](#overview)

In this guide, you will learn how to create custom pagelets for your Storefront pages.

In short: Pages are exactly that, a fully functioning page of your store with a template loaded by a route. A pagelet is an important and reusable fraction of several pages, such as a footer or the navigation.

## Prerequisites [​](#prerequisites)

To add your own custom pagelet for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html). Since a pagelet is just part of another page, we are going to use the page created in our guide about [adding a custom page](./add-custom-page.html).

## Adding custom pagelet [​](#adding-custom-pagelet)

Basically a pagelet is created exactly like a page: You need a pagelet loader, a pagelet struct to hold the data and a pagelet loaded event.

Since creating this kind of classes is explained in detail in our guide about [adding a custom page](./add-custom-page.html), it is not going to be explained here in detail again. Yet, there's some differences worth mentioning:

* The struct to hold the data has to extend from the `Shopware\Storefront\Pagelet\Pagelet` class instead of `Shopware\Storefront\Page\Page`
* A pagelet doesn't have to be bound to a controller, e.g. with an extra route. It can have a route though!
* A pagelet is mostly loaded by another page or multiple pages, that's their purpose
* The `GenericPageLoaderInterface` is not used, since it is responsible to load the footer or header pagelet. You don't want to load

  a pagelet (footer or header) into your pagelet
* The pagelet instance is not created via `Pagelet::createFrom()`, but rather you just create a new instance yourself. That's because the

  `Pagelet::createFrom()` was only necessary to create a new instance of your page, which already contains the footer & header pagelets.

  Once again: You don't want that in your pagelet.
* The pagelet loaded event class extends from `Shopware\Storefront\Pagelet\PageletLoadedEvent` instead of `Shopware\Storefront\Page\PageLoadedEvent`

Let's now have a look at the example classes. The pagelet is going to be called `ExamplePagelet` in the following examples.

### The ExamplePageletLoader [​](#the-examplepageletloader)

PLUGIN\_ROOT/src/Storefront/Pagelet/Example/ExamplePageletLoader.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\GenericPageLoaderInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageletLoader
{
    private EventDispatcherInterface $eventDispatcher;

    public function __construct(EventDispatcherInterface $eventDispatcher)
    {
        $this->eventDispatcher = $eventDispatcher;
    }

    public function load(Request $request, SalesChannelContext $context): ExamplePagelet
    {
        $pagelet = new ExamplePagelet();

        // Do additional stuff, e.g. load more data from store-api and add it to page
        $pagelet->setExampleData(...);

        $this->eventDispatcher->dispatch(
            new ExamplePageletLoadedEvent($pagelet, $context, $request)
        );

        return $pagelet;
    }
}
```

Note the instance creation without the `::createFrom()` call. The rest is quite equal, you can load your data, set it to the pagelet struct, you fire an event, and you return the pagelet.

### The ExamplePagelet struct [​](#the-examplepagelet-struct)

PLUGIN\_ROOT/src/Storefront/Pagelet/Example/ExamplePagelet.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Storefront\Pagelet\Pagelet;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExamplePagelet extends Pagelet
{
    protected ExampleEntity $exampleData;

    public function getExampleData(): ExampleEntity
    {
        return $this->exampleData;
    }

    public function setExampleData(ExampleEntity $exampleData): void
    {
        $this->exampleData = $exampleData;
    }
}
```

Just like the page struct, this is basically just a class holding data. Note the different `extend` though, you're not extending from `Shopware\Storefront\Page\Page` here.

### The ExamplePageletLoadedEvent [​](#the-examplepageletloadedevent)

PLUGIN\_ROOT/src/Storefront/Pagelet/Example/ExamplePageletLoadedEvent.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Pagelet\PageletLoadedEvent;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageletLoadedEvent extends PageletLoadedEvent
{
    protected ExamplePagelet $pagelet;

    public function __construct(ExamplePagelet $pagelet, SalesChannelContext $salesChannelContext, Request $request)
    {
        $this->pagelet = $pagelet;
        parent::__construct($salesChannelContext, $request);
    }

    public function getPagelet(): ExamplePagelet
    {
        return $this->pagelet;
    }
}
```

Note the different `extends`, which uses the `PageletLoadedEvent` class instead. Also, the getter method is no longer `getPage`, but `getPagelet` instead.

## Loading the pagelet [​](#loading-the-pagelet)

### Loading the pagelet via another page [​](#loading-the-pagelet-via-another-page)

Most times you want to load your pagelet as part of another page. This is simply done by calling the `load` method of your pagelet in another page's `load` method.

Using the example from our [adding a custom page](./add-custom-page.html) guide, this is what the `load` method could look like:

PLUGIN\_ROOT/src/Storefront/Page/Example/ExamplePageLoader.php

php

```shiki
public function load(Request $request, SalesChannelContext $context): ExamplePage
{
    $page = $this->genericPageLoader->load($request, $context);
    $page = ExamplePage::createFrom($page);

    $page->setExamplePagelet($this->examplePageletLoader->load($request, $context));

    // Do additional stuff, e.g. load more data from store-api and add it to page
    $page->setExampleData(...);

    $this->eventDispatcher->dispatch(
        new ExamplePageletLoadedEvent($page, $context, $request)
    );

    return $page;
}
```

Of course, in this example your `ExamplePage` struct needs a method `setExamplePagelet`, as well as the respective getter method `getExamplePagelet`. And then that's it, you've loaded your pagelet as part of another page.

### Loading the pagelet via route [​](#loading-the-pagelet-via-route)

As already mentioned, a pagelet can be loaded via a route if you want it to. For that case, you can add a new route to your controller and load the pagelet via the `ExamplePageletLoader`:

php

```shiki
#[Route(path: '/example-pagelet', name: 'frontend.example.pagelet', methods: ['POST'], defaults: ['XmlHttpRequest' => 'true'])]
public function examplePagelet(Request $request, SalesChannelContext $context): Response
{
    $pagelet = $this->examplePageletLoader->load($request, $context);

    return $this->renderStorefront('@Storefront/storefront/pagelet/example/index.html.twig', [
        'pagelet' => $pagelet
    ]);
}
```

Using the part `defaults: ['XmlHttpRequest' => true]` in the attribute ensures that this pagelet can be loaded using an XML HTTP Request.

---

## Add translations

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-translations.html

# Add translations [​](#add-translations)

## Overview [​](#overview)

In this guide, you'll learn how to add translations to the Storefront and how to use them in your twig templates. To organize your snippets you can add them to `.json` files, so structuring and finding snippets you want to change is very easy.

## Prerequisites [​](#prerequisites)

To add your own custom translations for your plugin or app, you first need a base. Refer to either the [Plugin Base Guide](./../plugin-base-guide.html) or the [App Base Guide](./../../apps/app-base-guide.html) to create one.

## Snippet file structure [​](#snippet-file-structure)

Shopware 6 automatically loads your snippet files when you follow the standard file structure and naming convention. To enable this, store your snippet files in the `<extension root>/src/Resources/snippet/` directory of your plugin or `<extension root>/Resources/snippet/` for your app or theme.

You can also use subdirectories if you prefer, although we recommend keeping a flat structure for better maintainability. Use `<domain>.<locale>.json` as the naming pattern for the file.

The domain can be freely defined (we recommend your extension name in kebab case), while the locale **must** map to the ISO string of the supported locale in this snippet file — for example: `my-app.de.json`. Locales should follow the ISO string of the supported language, such as `de`, `en`, or `es-AR`.  
 This format follows [IETF BCP 47](https://datatracker.ietf.org/doc/html/bcp47), restricted to [ISO 639-1 (2-letter) language codes](https://en.wikipedia.org/wiki/ISO_639-1) as used by [Symfony](https://symfony.com/doc/current/reference/constraints/Locale.html), but with dashes (`-`) instead of underscores (`_`).

For more information on selecting proper locales, see our documentation on [Fallback language selection](./../../../../concepts/translations/fallback-language-selection.html).

In case you want to provide base translations (ship translations for a whole new language), indicate it with the suffix `.base` in your file name. Now the filename convention to be followed looks like this `<name>.<locale>.base.json` - for example, `my-app.de.base.json`.

So your structure could then look like this:

text

```shiki
└── SwagBasicExample
    └── src // Without `src` in apps / themes
        ├─ Resources
        │  └─ snippet
        │     ├─ my-app.de.json
        │     ├─ my-app.en.json
        │     └─ some-directory // optional
        │        └─ some-special-case.en.json
        └─ SwagBasicExample.php
```

## Creating translations [​](#creating-translations)

Now that we know how the structure of snippets should be, we can create a new snippet file. In this example we are creating a snippet file for (British) English called `example.en.json`. If you are using nested objects, you can access the translation values with `exampleOne.exampleTwo.exampleThree`. We can also use template variables, which we can assign values later in the template. There is no explicit syntax for variables in the Storefront. However, it is recommended to enclose them with `%` symbols to make their purpose clear.

Here's an example of an English translation file:

json

```shiki
// <extension root>/src/Resources/snippet/en_GB/example.en-GB.json
{
  "header": {
    "example": "Our example header"
  },
  "soldProducts": "Sold about %count% products in %country%"
}
```

## Using translations in templates [​](#using-translations-in-templates)

Now we want to use our previously created snippet in our twig template, we can do this with the `trans` filter. Below, you can find two examples where we use our translation with placeholders and without.

Translation without placeholders:

twig

```shiki
<div class="product-detail-headline">
    {{ 'header.example' | trans }}
</div>
```

Translation with placeholders:

twig

```shiki
<div class="product-detail-headline">
    {{ 'soldProducts' | trans({'%count%': 3, '%country%': 'Germany'}) }}
</div>
```

## Using translations in controllers [​](#using-translations-in-controllers)

If we want to use our snippet in a controller, we can use the `trans` method, which is available if our class is extending from `Shopware\Storefront\Controller\StorefrontController`. Or use injection via [DI container](#using-translation-generally-in-php).

Translation without placeholders:

php

```shiki
$this->trans('header.example');
```

Translation with placeholders:

php

```shiki
$this->trans('soldProducts', ['%count%' => 3, '%country%' => 'Germany']);
```

## General usage of translations in PHP [​](#general-usage-of-translations-in-php)

If we need to use a snippet elsewhere in PHP, we can use [Dependency Injection](./../plugin-fundamentals/dependency-injection.html) to inject the `translator` service, which implements Symfony's `Symfony\Contracts\Translation\TranslatorInterface`:

xml

```shiki
<service id="Swag\Example\Service\SwagService" public="true" >
    <argument type="service" id="translator" />
</service>
```

php

```shiki
private TranslatorInterface $translator;

public function __construct(TranslatorInterface $translator)
{
    $this->translator = $translator;
}
```

Then, call the `trans` method, which has the same parameters as the method from controllers.

php

```shiki
$this->translator->trans('soldProducts', ['%count%' => 3, '%country%' => 'Germany']);
```

---

## Add custom listing filters

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-listing-filters.html

# Add Custom Listing Filters [​](#add-custom-listing-filters)

## Overview [​](#overview)

In an online shop, filters are an important feature. So you might use filters in your custom plugin. This guide will get you covered on how to implement your own, custom filters in Shopware's Storefront.

## Prerequisites [​](#prerequisites)

Before you start reading this guide, make sure you got an own plugin installed to work with. If you need a starting point for that, see this guide:

[Plugin Base Guide](../plugin-base-guide)

## Create new Filter [​](#create-new-filter)

At first, you need to create a subscriber. In this example, we will call it `ExampleListingSubscriber`. If you are not sure on working with subscribers, please refer to the guide on working with events in Shopware:

[Listening to events](../plugin-fundamentals/listening-to-events)

As usual, we will start by creating this new class in the same path as you're seeing in Shopware's core - `/src/Subscriber/ExampleListingSubscriber.php`.

New listing filters, e.g. for your product listing, can be registered via the event `\Shopware\Core\Content\Product\Events\ProductListingCollectFilterEvent` This event was introduced to enable every developer to specify the metadata for a filter. The handling, meaning if and how a filter is added, is done by Shopware's core:

php

```shiki
    public static function getSubscribedEvents(): array
    {
        return [
            ProductListingCollectFilterEvent::class => 'addFilter'
        ];
    }
```

After that, you can start to actually add your custom filters. Arguably an important step is to define your filter. Therefore, you're able to use the `Filter` class, including the parameters below:

| Parameter | Description |
| --- | --- |
| `name` | Unique name of the filter |
| `filtered` | Set this option to `true` if this filter is active |
| `aggregations` | Defines aggregations behind a filter. Sometimes a filter contains multiple aggregations like properties |
| `filter` | Sets the DAL filter which should be added to the criteria |
| `values` | Defines the values which will be added as `currentFilter` to the result |
| `exclude` | Configure exclusions |

As a result, an example filter could look like this:

php

```shiki
$filter = new Filter(
    // name
    'manufacturer',

    // filtered
    !empty($ids),

    // aggregations
    [new EntityAggregation('manufacturer', 'product.manufacturerId', 'product_manufacturer')],

    // filter
    new EqualsAnyFilter('product.manufacturerId', $ids),

    // values
    $ids
);
```

Inside the `ProductListingCollectFilterEvent`, you get the existing filters, can define your new custom filters and merge them into the existing ones. Here is a complete example implementation, adding a filter on the product information `isCloseout`. Please note the comments for explanation:

php

```shiki
// <plugin root>/src/Subscriber/ExampleListingSubscriber.php
class ExampleListingSubscriber implements EventSubscriberInterface
{
    // register event
    public static function getSubscribedEvents(): array
    {
        return [
            ProductListingCollectFilterEvent::class => 'addFilter'
        ];
    }

    public function addFilter(ProductListingCollectFilterEvent $event): void
    {
        // fetch existing filters
        $filters = $event->getFilters();
        $request = $event->getRequest();

        $filtered = (bool) $request->get('isCloseout');

        $filter = new Filter(
            // unique name of the filter
            'isCloseout',

            // defines if this filter is active
            $filtered,

            // Defines aggregations behind a filter. A filter can contain multiple aggregations like properties
            [
                new FilterAggregation(
                    'active-filter',
                    new MaxAggregation('active', 'product.isCloseout'),
                    [new EqualsFilter('product.isCloseout', true)]
                ),
            ],

            // defines the DAL filter which should be added to the criteria   
            new EqualsFilter('product.isCloseout', true),

            // defines the values which will be added as currentFilter to the result
            $filtered
        );

        // Add your custom filter
        $filters->add($filter);
    }
}
```

## Add your filter to the Storefront UI [​](#add-your-filter-to-the-storefront-ui)

Well, fine - you successfully created a filter via subscriber. However, you want to enable your shop customer to use it, right? Now you need to integrate your filter in the Storefront. Let's start by searching the template file you need to extend in Shopware's Storefront. It's this one - `src/Storefront/Resources/views/storefront/component/listing/filter-panel.html.twig`.

In this template, the existing filters are contained in the block `component_filter_panel_items`. We are going to extend this block with our new filter. If you're not sure on how to customize templates in the Storefront, we got you covered with another guide:

[Customize templates](customize-templates)

INFO

The block `component_filter_panel_items` is available from Shopware Version 6.4.8.0

Including our filter will be done as seen below, please take the comments into account:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/component/listing/filter-panel.html.twig
{% sw_extends '@Storefront/storefront/component/listing/filter-panel.html.twig' %}

{% block component_filter_panel_items %}
    {{ parent() }}

    {# We'll include our filter element here #}
    {% sw_include '@Storefront/storefront/component/listing/filter/filter-boolean.html.twig' with {
        name: 'isCloseout',
        displayName: 'Closeout'
    } %}
{% endblock %}
```

As we want to filter a boolean value, we choose the `filter-boolean` component here. Sure, there are some more you can use - dependent on your filter's values:

| Name | Description |
| --- | --- |
| `filter-boolean` | A filter to display boolean values |
| `filter-multi-select` | Filters with multiple values |
| `filter-property-select` | A filter tailored specifically for properties |
| `filter-range` | Displays a range which can be used for filtering |
| `filter-rating-select` and `filter-rating-select-item` | Filter component for rating |

Extending `component_filter_panel_items` as shown above puts our filter *after* the already existing ones. We could put it at the beginning by moving the `parent()` call to the end of the block.

If we instead want our filter to be placed before or after a specific filter in the middle of the list, we can instead extend the block for that filter. For example, if we want our filter to be displayed after the price filter, we would extend the block `component_filter_panel_item_price`:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/component/listing/filter-panel.html.twig
{% sw_extends '@Storefront/storefront/component/listing/filter-panel.html.twig' %}

{% block component_filter_panel_item_price %}
    {{ parent() }}

    {# We'll include our filter element here #}
    {% sw_include '@Storefront/storefront/component/listing/filter/filter-boolean.html.twig' with {
        name: 'isCloseout',
        displayName: 'Closeout'
    } %}
{% endblock %}
```

## Next steps [​](#next-steps)

To add [custom sorting options](./add-custom-sorting-product-listing.html) to your listing in the Storefront, head over to the corresponding guide.

---

## Fetching data with Javascript

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/fetching-data-with-javascript.html

# Fetching Data with Javascript [​](#fetching-data-with-javascript)

## Overview [​](#overview)

When you develop your own plugin, you might want to fetch necessary data from the API. This guide explains how to achieve that.

## Prerequisites [​](#prerequisites)

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](./../plugin-base-guide.html).

While this is not mandatory, having read the guide about [adding custom javascript](./add-custom-javascript.html) plugins beforehand might help you understand this guide a bit further.

## Fetching data [​](#fetching-data)

We will use the standard [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to gather additional data. The fetch API is a modern replacement for the old `XMLHttpRequest` object. It is a promise-based API that allows you to make network requests similar to XMLHttpRequest (XHR).

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        this.fetchData();
    }

    // ...

    async fetchData() {
        const response = await fetch('/widgets/checkout/info');
        const data = await response.text();

        console.log(data);
    }
}
```

In this example, we fetch the data from the `/widgets/checkout/info` endpoint. The `fetch` method returns a promise that resolves to the `Response` object representing the response to the request. We then use the `text` method of the `Response` object to get the response body as text.

---

## Add data to storefront page

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-data-to-storefront-page.html

# Add Data to Storefront Page [​](#add-data-to-storefront-page)

## Overview [​](#overview)

Pages or pagelets are the objects that get handed to the templates and provide all necessary information for the template to render.

If you make template changes you probably want to display some data that is currently not available in the page. In this case you will have to listen on the page loaded event and then load the additional data and add it to the page object. This guide will show you how to achieve this, by adding the total number of active products to the footer pagelet and displaying them in the Storefront.

## Prerequisites [​](#prerequisites)

This guide is built upon our [Plugin base guide](./../plugin-base-guide.html), so keep that in mind.

Also the following knowledge is necessary, even though some of them are covered here as well:

* Knowing how to [listen to events by using a subscriber](./../plugin-fundamentals/listening-to-events.html)
* Knowing how to [customize storefront templates](./customize-templates.html)
* Knowing how to [read data using our data abstraction layer](./../framework/data-handling/reading-data.html)
* Knowing how to [add a store-api route](./../framework/store-api/add-store-api-route.html)

## Adding data to the Storefront [​](#adding-data-to-the-storefront)

The workflow you need here was already described in the overview:

1. Figure out which page you want to change
2. Register to the event that this page is firing
3. Add a store-api route for your needed data
4. Add data to the page via the event
5. Display this data in the Storefront

### Subscribe to an event [​](#subscribe-to-an-event)

So first of all, you need to know which page or pagelet you actually want to extend. In this example, we're going to extend the [FooterPagelet](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Footer/FooterPagelet.php). All pages or pagelets throw `Loaded` events and this is the right event to subscribe to if you want to add data to the page or pagelet. In our case we want to add data to the `FooterPagelet` so we need to subscribe to the `FooterPageletLoadedEvent`.

php

```shiki
// SwagBasicExample/src/Service/AddDataToPage.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Storefront\Pagelet\Footer\FooterPageletLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class AddDataToPage implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            FooterPageletLoadedEvent::class => 'addActiveProductCount'
        ];
    }

    public function addActiveProductCount(FooterPageletLoadedEvent $event): void
    {

    }
}
```

The next thing we need to do is register our subscriber in the DI-Container and tag it as an event subscriber:

xml

```shiki
// Resources/config/services.xml
<?xml version="1.0" ?>
<service id="Swag\BasicExample\Service\AddDataToPage" >
    <tag name="kernel.event_subscriber" />
</service>
```

### Adding data to the page [​](#adding-data-to-the-page)

Now that we have registered our Subscriber to the right event, we first need to fetch the additional data we need and then add it as an extension to the pagelet.

Since we are in a `Pagelet`-event, the DAL should not be called directly to fetch data. Instead, we should check whether a suitable `store-api` route exists.

If we only needed specific product data, we could use the `ProductListRoute`. However, this does not satisfy our use case. While the `ProductListRoute` could provide this data, it would return far more information than necessary.

Therefore, we will create a new `store-api` route tailored to our needs.

First you should read our guide for [adding store-api routes](./../framework/store-api/add-store-api-route.html).

Our new Route should look like this:

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\Routing\StoreApiRouteScope;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
abstract class AbstractProductCountRoute
{
    abstract public function getDecorated(): AbstractProductCountRoute;

    abstract public function load(Criteria $criteria, SalesChannelContext $context): ProductCountRouteResponse;
}
```

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\PlatformRequest;
use Shopware\Core\Framework\Routing\StoreApiRouteScope;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Aggregation\Metric\CountAggregation;
use Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\Metric\CountResult;
use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: [PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [StoreApiRouteScope::ID]])]
class ProductCountRoute extends AbstractProductCountRoute
{
    protected EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }

    public function getDecorated(): AbstractProductCountRoute
    {
        throw new DecorationPatternException(self::class);
    }

    #[Route(
        path: '/store-api/get-active-product-count',
        name: 'store-api.product-count.get',
        methods: ['GET', 'POST'],
        defaults: ['_entity' => 'product']
    )]
    public function load(Criteria $criteria, SalesChannelContext $context): ProductCountRouteResponse
    {
        $criteria = new Criteria();
        $criteria->addFilter(new EqualsFilter('product.active', true));
        $criteria->addAggregation(new CountAggregation('productCount', 'product.id'));

        /** @var CountResult $productCountResult */
        $productCountResult = $this->productRepository
            ->aggregate($criteria, $context->getContext())
            ->get('productCount');
            
        return new ProductCountRouteResponse($productCountResult);
    }
}
```

### Register route class [​](#register-route-class)

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute" >
            <argument type="service" id="product.repository"/>
        </service>
    </services>
</container>
```

The routes.xml according to our guide for [adding store-api routes](./../framework/store-api/add-store-api-route.html) should look like this.

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Core/**/*Route.php" type="attribute" />
</routes>
```

### ProductCountRouteResponse [​](#productcountrouteresponse)

The RouteResponse according to our guide for [adding store-api routes](./../framework/store-api/add-store-api-route.html) should look like this

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\Metric\CountResult;
use Shopware\Core\System\SalesChannel\StoreApiResponse;

/**
 * @extends StoreApiResponse<CountResult>
 */
class ProductCountRouteResponse extends StoreApiResponse
{
    public function __construct(CountResult $countResult)
    {
        parent::__construct($countResult);
    }

    public function getProductCount(): CountResult
    {
        return $this->object;
    }
}
```

So you should know and understand the first few lines if you have read our guide about [Reading data](./../framework/data-handling/reading-data.html) first. Make sure to also understand the usage of aggregations, since this is what is done here. The only main difference you might notice is, that we're using the `aggregate()` method instead of the `search()` method. This will not actually search for any products and return the whole products dataset, but rather just the aggregated data, nothing else.

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Product\SalesChannel\ProductCountRoute;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Storefront\Pagelet\Footer\FooterPageletLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class AddDataToPage implements EventSubscriberInterface
{
    private ProductCountRoute $productCountRoute;

    public function __construct(ProductCountRoute $productCountRoute)
    {
        $this->productCountRoute = $productCountRoute;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            FooterPageletLoadedEvent::class => 'addActiveProductCount'
        ];
    }

    public function addActiveProductCount(FooterPageletLoadedEvent $event): void
    {
        $productCountResponse = $this->productCountRoute->load(new Criteria(), $event->getSalesChannelContext());

        $event->getPagelet()->addExtension('product_count', $productCountResponse->getProductCount());
    }
}
```

The first line should be nothing new as it is only the call for the store-api route, we created. Completely new should only be the last line: `$event->getPagelet()->addExtension('product_count', $productCountResult);`

Basically what you're doing here, is to fetch the actual pagelet instance from the event and add the data to the template. This data will then be available via the name `product_count`, but we'll get to that in the next section.

Now you only have to adjust your service definition to inject the productCountRoute:

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute" public="true">
            <argument type="service" id="product.repository"/>
        </service>
        
        <service id="Swag\BasicExample\Service\AddDataToPage" >
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute"/>
            <tag name="kernel.event_subscriber" />
        </service>
    </services>
</container>
```

### Displaying the data in the Storefront [​](#displaying-the-data-in-the-storefront)

To display the additional data we need to override the footer template and render the data. Refer to the respective section of this guide for detailed information on how to [extend templates and override blocks](./customize-templates.html).

For our case we extend the footer template and add a new column to the navigation block:

twig

```shiki
// Resources/views/storefront/layout/footer/footer.html.twig
{% sw_extends '@Storefront/storefront/layout/footer/footer.html.twig' %}

{% block layout_footer_navigation_columns %}
    {{ parent() }}

    {% if footer.extensions.product_count %}
        <div class="col-md-4 footer-column">
            <p>This shop offers you {{ footer.extensions.product_count.count }} products</p>
        </div>
    {% endif %}
{% endblock %}
```

Note the usage of the variable here. You're accessing the footer object, in which you can now find the path `extensions.product_count.count`.

---

## Add cookie to manager

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-cookie-to-manager.html

# Add Cookie to Manager [​](#add-cookie-to-manager)

## Overview [​](#overview)

Since the GDPR was introduced, every website has to be shipped with some sort of a cookie consent manager. This is also the case for Shopware 6 of course, which comes with a cookie consent manager by default. In this guide you will learn how you can add your own cookies to the cookie consent manager of Shopware 6.

INFO

For a comprehensive understanding of Shopware's cookie consent system, see the [Cookie Consent Management Concept](./../../../../concepts/commerce/content/cookie-consent-management.html).

## Prerequisites [​](#prerequisites)

This guide is built upon the [Plugin base guide](./../plugin-base-guide.html), so take a look at that first if you're lacking a running plugin. Also, you will need to know how to [create your own service](./../plugin-fundamentals/add-custom-service.html) and [subscribe to an event](./../plugin-fundamentals/listening-to-events.html), so you might want to take a look at those guides as well.

## Extend the cookie consent manager [​](#extend-the-cookie-consent-manager)

Adding custom cookies requires you to listen to the `CookieGroupsCollectEvent` and add your custom cookies to the collection.

TIP

It is recommended to use an event listener if you're listening to a single event. If you need to react to multiple events, an event subscriber is the better choice.

### Registering your event listener [​](#registering-your-event-listener)

Start with creating the `services.xml` and registering your event listener.

xml

```shiki
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="PluginName\Listener\CookieListener">
            <tag name="kernel.event_listener" event="Shopware\Storefront\Framework\Cookie\CookieGroupsCollectEvent"/>
        </service>
    </services>
</container>
```

In the next step we'll create the actual listener class.

### Creating the listener [​](#creating-the-listener)

We need to create a class called `CookieListener` with an `__invoke` method. This method will be executed once the `CookieGroupsCollectEvent` is dispatched.

The event object that is passed to our listener method contains the cookie groups collection, which we can use to add our custom cookies.

WARNING

Since Shopware 6.7.3.0, cookies use structured objects (`CookieEntry` and `CookieGroup`) instead of arrays for better type safety and consistency. The array format is deprecated.

Let's have a look at an example:

php

```shiki
// <plugin root>/src/Listener/CookieListener.php
<?php declare(strict_types=1);

namespace PluginName\Listener;

use Shopware\Storefront\Framework\Cookie\CookieGroupsCollectEvent;
use Shopware\Core\Framework\Cookie\CookieEntry;
use Shopware\Core\Framework\Cookie\CookieGroup;

class CookieListener
{
    public function __invoke(CookieGroupsCollectEvent $event): void
    {
        $cookieGroups = $event->getCookieGroups();

        // Create a single cookie
        $singleCookie = new CookieEntry(
            'cookie.name',
            'cookie-key',
            'cookie value',
            30,
            'cookie.description'
        );

        // Create entries collection for cookie group
        $groupEntries = [
            new CookieEntry(
                'cookie.first_child_name',
                'cookie-key-1',
                'cookie value',
                30
            ),
            new CookieEntry(
                'cookie.second_child_name',
                'cookie-key-2',
                'cookie value',
                60
            )
        ];

        // Create a cookie group with multiple cookies
        $cookieGroup = new CookieGroup(
            'cookie.group_name',
            $groupEntries,
            'cookie.group_description'
        );

        $cookieGroups->add($cookieGroup);
        $cookieGroups->add($singleCookie);
    }
}
```

This will eventually lead to a new group being created, containing two new cookies, as well as a new cookie without a group.

And that's basically it already. After loading your Storefront, you should now see your new cookies and the cookie-group.

## Parameter Reference [​](#parameter-reference)

For a complete list of available parameters and their types, refer to the source code:

* [`CookieEntry`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Cookie/Struct/CookieEntry.php) - Individual cookie definition
* [`CookieGroup`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Cookie/Struct/CookieGroup.php) - Cookie group definition

INFO

Cookie groups should not have the `cookie`, `value`, `expiration`, or `isRequired` parameters. These only apply to individual `CookieEntry` objects within the group's `entries`.

## Migrating from CookieProviderInterface (Shopware 6.7.2 and earlier) [​](#migrating-from-cookieproviderinterface-shopware-6-7-2-and-earlier)

If you are upgrading from an older version, you might have used the `CookieProviderInterface` to add custom cookies. This interface is now deprecated and should be replaced with the `CookieGroupsCollectEvent`.

For backward compatibility, you can still use the `CookieProviderInterface` to provide cookies in the old array syntax. However, it is highly recommended to use the new event-based system to provide the new object structure.

## Cookie Configuration Changes and Re-Consent [​](#cookie-configuration-changes-and-re-consent)

Since Shopware 6.7.3.0, cookie configurations include a hash that tracks changes. When you modify cookie configurations through your plugin (add/remove/change cookies), the hash changes automatically, triggering a re-consent flow for users.

This helps maintain transparency by re-prompting users when cookie handling changes, supporting GDPR compliance requirements. The hash is automatically calculated from all cookie configurations provided by the `CookieProvider`.

INFO

While this feature helps with GDPR compliance, shop owners are responsible for ensuring their overall cookie usage, privacy policies, and data handling practices comply with GDPR and other applicable regulations.

### How it works [​](#how-it-works)

1. Your plugin adds/modifies cookies via the `CookieGroupsCollectEvent`
2. Shopware calculates a hash of the entire cookie configuration
3. The hash is stored in the user's browser
4. On the next visit, if the hash differs, the consent banner appears again
5. Users are informed about changes and can make new choices

This automatic re-consent mechanism helps shop owners maintain transparency about cookie changes.

INFO

The configuration hash is exposed via the Store API endpoint `/store-api/cookie/groups`. For API documentation, see [Fetch all cookie groups](https://shopware.stoplight.io/docs/store-api/f9c70be044a15-fetch-all-cookie-groups).

## Video Platform Cookies [​](#video-platform-cookies)

YouTube and Vimeo cookies are now handled separately in Shopware's cookie management. If you're adding video functionality to your plugin, ensure you register the appropriate cookie for your video platform or reuse existing ones.

## Next steps [​](#next-steps)

Those changes will mainly just show your new cookies in the cookie consent manager, but without much function. Head over to our guide about [Reacting to cookie consent changes](./reacting-to-cookie-consent-changes.html) to see how you can implement your custom logic once your cookie got accepted or declined.

---

## Customize Header/Footer

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/customize-header-footer.html

# Customize Header/Footer [​](#customize-header-footer)

## Overview [​](#overview)

With the introduction of ESI loading for the header and footer, the way how to customize the header and footer has changed. E.g. it is no longer possible to customize the header and footer depending on the current page data. This guide will show you how to customize the header and footer in your plugin.

## Prerequisites [​](#prerequisites)

As most guides, this guide is built upon the [Plugin Base Guide](./../plugin-base-guide.html), so you might want to have a look at it. Other than that, knowing [Twig](https://twig.symfony.com/) is a big advantage for this guide, but that's not necessary.

## Customizing by bypassing the ESI loading [​](#customizing-by-bypassing-the-esi-loading)

The ESI loading of header and footer was introduced as they are parts of the page that usually do not change that often and could therefore stay cached for a longer time. The header and footer are now loaded with sub-requests and are therefore no longer dependent on the current page data. It is still possible to add custom data to the header and footer directly, see ["Add data to storefront page"](./add-data-to-storefront-page.html) guide for more information.

But if you need to customize the header or footer depending on the current page data you need to adjust the ESI loading with additional parameters. This happens in the `Storefront/Resources/views/storefront/base.html.twig` [file](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Resources/views/storefront/base.html.twig#L38). The needed block names are `base_esi_header` and `base_esi_footer`. Extend the `base.html.twig` in your plugin and overwrite for example the header block.

PLUGIN\_ROOT/src/Resources/views/storefront/base.html.twig

twig

```shiki
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_esi_header %}
    {% set headerParameters = headerParameters|merge({ 'vendorPrefixPluginName': { 'activeRoute': activeRoute } }) %}
    {{ parent() }}
{% endblock %}
```

The `headerParameters` are passed to the header route as query parameters and after that passed through to the header template. With this change you are now able to access the current route in your header template:

PLUGIN\_ROOT/src/Resources/views/storefront/layout/header.html.twig

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header.html.twig' %}

{% block header %}
    {{ dump(headerParameters.vendorPrefixPluginName.activeRoute) }}
    {{ parent() }}
{% endblock %}
```

This approach works both in plugins and apps. In plugins, you can also use the `StorefrontRenderEvent`, to add custom data to the header and footer:

PLUGIN\_ROOT/src/StorefrontSubscriber.phpPLUGIN\_ROOT/src/Resources/views/storefront/layout/header.html.twig

php

```shiki
class StorefrontSubscriber
{
    public function __invoke(StorefrontRenderEvent $event): void
    {
        if ($event->getRequest()->attributes->get('_route') !== 'frontend.header') {
            return;
        }

        $headerParameters = $event->getParameter('headerParameters') ?? [];
        $headerParameters['vendorPrefixPluginName']['salesChannelId'] = $event->getSalesChannelContext()->getSalesChannelId();

        $event->setParameter('headerParameters', $headerParameters);
    }
}
```

twig

```shiki
{% sw_extends '@Storefront/storefront/layout/header.html.twig' %}

{% block header %}
    {{ dump(headerParameters.vendorPrefixPluginName.salesChannelId) }}
    {{ parent() }}
{% endblock %}
```

WARNING

Please be aware, that `headerParameters` and `footerParameters` can only contain scalar values, as they are also query parameters for the ESI routes.

It is also possible to load your custom header or footer templates. This is also done in the core itself within the checkout process. See e.g. the [checkout confirm page](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Resources/views/storefront/page/checkout/confirm/index.html.twig#L3-L5). Please be aware, that this will overwrite customizations from every other extension. You also need to make sure, that the `header` and `footer` data is available, if your custom template extends from the original header or footer template. See e.g. the [checkout confirm controller](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Controller/CheckoutController.php#L152-L159).

---

## Reacting to cookie consent changes

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/reacting-to-cookie-consent-changes.html

# Reacting to Cookie Consent Changes [​](#reacting-to-cookie-consent-changes)

## Overview [​](#overview)

This guide explains how to react to changes in cookie consent made by the user via JavaScript. This is essential when your plugin needs to load third-party scripts, tracking codes, or other functionality only when users have given their consent.

## Prerequisites [​](#prerequisites)

This guide is built upon both the [Plugin base guide](./../plugin-base-guide.html) and the [Adding a cookie to the consent manager](./add-cookie-to-manager.html) guide, so make sure to know those beforehand. Also, nice to know is the guide about [Reacting to javascript events](./reacting-to-javascript-events.html), since this will be done here, same as how to [create and load a JavaScript](./add-custom-javascript.html) file in the first place.

INFO

For a comprehensive understanding of Shopware's cookie consent system, see the [Cookie Consent Management Concept](./../../../../concepts/commerce/content/cookie-consent-management.html).

## Key Principles [​](#key-principles)

To create a cookie-aware plugin, you need to handle two main scenarios:

1. **Initial Page Load**: When a page loads, you must check if the user has already given consent for your cookie.
2. **Consent Changes**: If the user changes their cookie settings while on the site, your plugin must react to that change in real-time, enabling or disabling its functionality accordingly.
3. **Cleaning Up**: If a user withdraws consent, it's crucial to clean up any resources your plugin has loaded, such as scripts, tracking cookies, or data in local storage.

This guide will walk you through implementing these principles.

## Step 1: Checking for Consent on Page Load [​](#step-1-checking-for-consent-on-page-load)

If you need to check the current state of a cookie on page load, you can do so by checking for the existence of the specific cookie. When a user gives consent, Shopware creates a cookie with the name you defined.

javascript

```shiki
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

// Check for the existence of a specific cookie
function checkCookieConsent(cookieName) {
    const cookieStorage = new CookieStorage();
    return !!cookieStorage.getItem(cookieName);
}

// Usage
if (checkCookieConsent('cookie-key-1')) {
    // Cookie is accepted, load your feature
    loadThirdPartyScript();
}
```

## Step 2: Reacting to Consent Changes [​](#step-2-reacting-to-consent-changes)

Every time a user saves a cookie configuration, Shopware fires a `COOKIE_CONFIGURATION_UPDATE` event. You can listen for this event to react in real-time when a user accepts or declines your cookie.

The event detail contains an object with the names of the cookies that were changed and their new state (`true` for active, `false` for inactive).

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/reacting-cookie/reacting-cookie.js
import { COOKIE_CONFIGURATION_UPDATE } from 'src/plugin/cookie/cookie-configuration.plugin';

document.$emitter.subscribe(COOKIE_CONFIGURATION_UPDATE, eventCallback);

function eventCallback(updatedCookies) {
    if (typeof updatedCookies.detail['cookie-key-1'] !== 'undefined') {
        const cookieActive = updatedCookies.detail['cookie-key-1'];

        if (cookieActive) {
            // Cookie was accepted - load your script/feature
            loadThirdPartyScript();
        } else {
            // Cookie was declined - clean up if necessary
            removeThirdPartyScript();
        }
    }
}

function loadThirdPartyScript() {
    // Example: Load tracking script
    const script = document.createElement('script');
    script.src = 'https://example.com/tracking.js';
    script.id = 'cookie-key-1-script';
    document.head.appendChild(script);
}

function removeThirdPartyScript() {
    // Example: Remove tracking script and clean up related cookies/storage
    const script = document.getElementById('cookie-key-1-script');
    if (script) {
        script.remove();
    }
    // Also clear any cookies set by the script
    document.cookie = 'tracking-session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    // And any storage items
    localStorage.removeItem('tracking-data');
}
```

Notice the `removeThirdPartyScript` function. It's crucial to not only remove the script but also clean up any cookies or storage items it might have created.

## Step 3: Complete Implementation Example [​](#step-3-complete-implementation-example)

Here's a complete example of a plugin that combines both principles: it checks for consent on page load and reacts to changes from the consent manager.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/plugin/cookie-aware-tracking.plugin.js
import Plugin from 'src/plugin-system/plugin.class';
import { COOKIE_CONFIGURATION_UPDATE } from 'src/plugin/cookie/cookie-configuration.plugin';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

export default class CookieAwareTrackingPlugin extends Plugin {
    static options = {
        cookieName: 'my-tracking-cookie',
        trackingUrl: 'https://tracking.example.com/script.js'
    };

    init() {
        this.cookieStorage = new CookieStorage();

        this._registerEvents();

        // Check initial consent on page load
        if (this.hasConsent()) {
            this.enableTracking();
        }
    }

    _registerEvents() {
        this.$emitter.subscribe(COOKIE_CONFIGURATION_UPDATE, this.onConsentChange.bind(this));
    }

    onConsentChange(event) {
        const updatedCookies = event.detail;

        if (typeof updatedCookies[this.options.cookieName] === 'undefined') {
            return;
        }

        if (updatedCookies[this.options.cookieName]) {
            this.enableTracking();
        } else {
            this.disableTracking();
        }
    }

    hasConsent() {
        return !!this.cookieStorage.getItem(this.options.cookieName);
    }

    enableTracking() {
        if (this.isTrackingEnabled) {
            return;
        }

        console.log('Enabling tracking');

        // Load tracking script
        const script = document.createElement('script');
        script.src = this.options.trackingUrl;
        script.id = 'tracking-script';
        script.dataset.trackingScript = 'true';
        document.head.appendChild(script);

        this.isTrackingEnabled = true;
    }

    disableTracking() {
        if (!this.isTrackingEnabled) {
            return;
        }

        console.log('Disabling tracking');

        // Remove tracking script
        const script = document.getElementById('tracking-script');
        if (script) {
            script.remove();
        }

        // Clean up tracking cookies
        document.cookie = 'tracking-session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

        this.isTrackingEnabled = false;
    }
}
```

## Step 4: Loading the JavaScript Plugin [​](#step-4-loading-the-javascript-plugin)

Finally, you have to load your new plugin in your plugin's main entry file, which is the `main.js`. For better performance, it is recommended to load plugins asynchronously using a dynamic import. This ensures the plugin is only loaded on pages where it's actually needed (i.e., where its selector is present).

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
const PluginManager = window.PluginManager;
PluginManager.register('CookieAwareTracking', () => import('./plugin/cookie-aware-tracking.plugin'), '[data-cookie-aware-tracking]');
```

---

## Reacting to javascript events

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/reacting-to-javascript-events.html

# Reacting to Javascript Events on Storefront [​](#reacting-to-javascript-events-on-storefront)

## Overview [​](#overview)

Just like in PHP, there may be useful events in our JavaScript plugins, which you can use to extend the default behavior. This guide will show you how this is done and you can find events, if there's any available for your needs.

## Prerequisites [​](#prerequisites)

As most guides, this one is built upon our [Plugin base guide](./../plugin-base-guide.html), but that one is not necessary, you do need a running plugin though! Also this guide will **not** explain how to create a JavaScript plugin in general, head over to our guide [adding custom javascript](./add-custom-javascript.html) to understand how that's done in the first place.

## JavaScript base class [​](#javascript-base-class)

As already mentioned, this guide will not explain how to create a JavaScript plugin in the first place. For this guide, we'll use the following example JavaScript plugin:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/events-plugin/events-plugin.plugin.js
const { PluginBaseClass } = window;

export default class EventsPlugin extends PluginBaseClass {
    init() {
    }
}
```

This one will be used from now on.

## Finding events [​](#finding-events)

So before you can start reacting and listening to events, you need to find them first. Since not every plugin implements events, they can be hard to find by just looking through the code.

Instead, rather search for `this.$emitter.publish` in the directory `platform/src/Storefront/Resources/app/storefront/src` to find all occurrences of events being published. This way, you may or may not find an event useful for your needs, so you don't have to override other JavaScript plugins.

## Registering to events [​](#registering-to-events)

Now that you possibly found your event, it's time to register to it and execute code once it is fired. For this example, we will listen to the event when the cookie bar is hidden. The respective event can be found via the name [hideCookieBar](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/plugin/cookie/cookie-permission.plugin.js#L71).

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/events-plugin/events-plugin.plugin.js
const { PluginBaseClass } = window;

export default class EventsPlugin extends PluginBaseClass {
    init() {
        const plugin = window.PluginManager.getPluginInstanceFromElement(document.querySelector('[data-cookie-permission]'), 'CookiePermission');
        plugin.$emitter.subscribe('hideCookieBar', this.onHideCookieBar);
    }

    onHideCookieBar() {
        alert("The cookie bar has been hidden!");
    }
}
```

Let's have a look at the code. There's one thing you have to understand first. When a plugin calls `this.$emitter.publish`, this event is fired on the plugin's own `$emitter` instance. This means: Every plugin has its own instance of the emitter. Therefore, you cannot just use `this.$emitter.subscribe` to listen to other plugin's events.

Rather, you have to fetch the respective plugin instance using the `PluginManager` and then you have to use `subscribe` on their `$emitter` instance: `plugin.$emitter.subscribe`

And this is done here. We're fetching the instance of the `CookiePermission` plugin by its [selector](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/main.js#L103) via the `PluginManager` and using that instance to register to the event. Once the event is then fired, our own method `onHideCookieBar` is executed and the `alert` will be shown.

WARNING

This does **not** prevent the execution of the original method. Consider those events to be "notifications".

## Next steps [​](#next-steps)

Everytime you don't find an event to implement the changes you need, you may have to override the plugin itself. For this case, head over to our guide about [Override existing javascript](./override-existing-javascript.html).

---

## Working with media and thumbnails

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/use-media-thumbnails.html

# Working with Media and Thumbnails [​](#working-with-media-and-thumbnails)

## Overview [​](#overview)

In Shopware's Storefront, you can assign media objects to the different entities. To name an example, this is often used for products to show more information with images on the product detail page. This guide should give you a starting point on how to use media and thumbnails in your Storefront plugin.

## Prerequisites [​](#prerequisites)

In order to use your own media files or thumbnails of your plugin in the Storefront, of course you first need a plugin as base. To create an own plugin, you can refer to the Plugin Base Guide:

[Plugin Base Guide](../plugin-base-guide)

Displaying custom images is often done by using custom fields. To take full advantage of this guide, you might want to read the corresponding guide on using custom fields:

[Add custom input field to existing component](../administration/module-component-management/add-custom-field)

## Using searchMedia function [​](#using-searchmedia-function)

You should be able to store media in your shop and to maintain them in your Administration. It is not possible to display such an image in the Storefront with only its media ID though. To achieve that, the function `searchMedia` exists:

php

```shiki
public function searchMedia (array $ids, Context $context): MediaCollection { 
... 
}
```

This `searchMedia` function reads out the corresponding media objects for the given IDs in order to continue working with them afterwards. Here is an example with a custom field (`custom_sports_media_id`) on the product detail page:

twig

```shiki
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

DANGER

Please note that this function performs a query against the database and should therefore not be used within a loop.

The function is already structured in a way that several IDs can be passed. To read the media objects within the product listing we recommend the following procedure:

twig

```shiki
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

## Working with sw\_thumbnail [​](#working-with-sw-thumbnail)

A common issue when developing responsive web pages is resizing images properly for different screen widths. By default, Shopware generates various thumbnails for each uploaded image. Normally you would have to manually write large chunks of HTML code to render the needed images with `img` and `srcset`.

Fortunately, you do not need to define these attributes on your own - For that, Shopware introduced the `sw_thumbnails` Twig function: `sw_thumbnails` automatically generates the `img` and `srcset` code. This is the minimal configuration:

twig

```shiki
{% sw_thumbnails 'my-thumbnails' with {
    media: cover
} %}
```

As you see, `sw_thumbnail` makes use of one required parameter: `media` is required and contains the whole media entity. The string after `sw_thumbnails` is also required but does not render a CSS class. All other parameters are optional.

### Dealing with thumbnail sizes [​](#dealing-with-thumbnail-sizes)

With the `sizes` parameter you can control the `sizes` attribute of the `img` and define which of the thumbnails should be used in a media query / viewport.

You can find more information on those sizes here:

[<img>: The Image Embed element - HTML: HyperText Markup Language | MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img\#attr-srcset)

E.g. if the browser is in Bootstrap viewport `lg` (which is 992px - 1199px) use an image which is closest to 333px. If `sizes` is not set, Shopware will automatically use fallback values from global `shopware.theme.breakpoint`.

Let's think about the snippet below:

twig

```shiki
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    sizes: {
        'xs': '501px',
        'sm': '315px',
        'md': '427px',
        'lg': '333px',
        'xl': '284px',
    }
} %}
```

This example will print out the following output:

html

```shiki
<img 
    src="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg" 
    srcset="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg 1921w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_1920x1920.jpg 1920w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_800x800.jpg 800w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_400x400.jpg 400w" 
    sizes="(max-width: 1920px) and (min-width: 1200px) 284px,
           (max-width: 1199px) and (min-width: 992px) 333px, 
           (max-width: 991px) and (min-width: 768px) 427px, 
           (max-width: 767px) and (min-width: 576px) 315px, 
           (max-width: 575px) and (min-width: 0px) 501px, 100vw">
```

By giving the `default` size you can override the media queries and always refer to a single image source for all viewports. To give an example, think about always using a small thumbnail closest to 100px regardless of the current viewport:

twig

```shiki
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    sizes: {
        'xs': '501px', {# Will be ignored #}
        'sm': '315px', {# Will be ignored #}
        'md': '427px', {# Will be ignored #}
        'lg': '333px', {# Will be ignored #}
        'xl': '284px', {# Will be ignored #}
        'default': '100px'
    }
} %}
```

This example will create the output below:

html

```shiki
<img 
    src="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg" 
    srcset="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg 1921w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_1920x1920.jpg 1920w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_800x800.jpg 800w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_400x400.jpg 400w" 
    sizes="100px">
```

DANGER

Please note that those sizes only work with bootstrap viewports, like xs, sm, md, lg and xl. Custom media queries will not work.

### Additional attributes [​](#additional-attributes)

With the `attributes` param, additional attributes can be applied. Imagine the following example:

twig

```shiki
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    attributes: {
        'class': 'my-custom-class',
        'alt': 'alt tag of image',
        'title': 'title of image'
    }
} %}
```

This will generate the output below:

html

```shiki
<img 
    src="..." 
    sizes="..." 
    class="my-custom-class" 
    alt="Image name" 
    title="My beautiful image">
```

### Native lazy loading [​](#native-lazy-loading)

With the `attributes` param, it is also possible to enable native lazy loading on the thumbnail element:

twig

```shiki
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    attributes: {
        'loading': 'lazy'
    }
} %}
```

This will generate the below output:

html

```shiki
<img 
    src="..." 
    sizes="..." 
    loading="lazy">
```

By default, lazy loading is disabled for newly added `sw_thumbnail` elements. You should consider activating it in the following scenarios:

* When multiple `sw_thumbnail` elements occur on one page while the `sw_thumbnail` s are not in the initial viewport.
* When images rendered by `sw_thumbnail` are within a container hidden by CSS via `display: none`.

## More interesting topics [​](#more-interesting-topics)

* [Use custom assets in general](./add-custom-assets.html)

---

## Remove Javascript plugin

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/remove-unnecessary-js-plugin.html

# Remove Javascript Plugin [​](#remove-javascript-plugin)

## Overview [​](#overview)

When you develop your own plugin, you might want to exclude Javascript plugins at some occasions. For example, if you don't want a Core plugin to interfere, with your own code. This guide will teach you how to remove this Javascript plugin with your own Shopware plugin.

## Prerequisites [​](#prerequisites)

While this is not mandatory, having read the guide about adding custom javascript plugins beforehand might help you understand this guide a bit further:

[Add custom Javascript](add-custom-javascript)

Other than that, this guide just requires you to have a running plugin installed, e.g. our plugin from the plugin base guide:

[Plugin Base Guide](../plugin-base-guide)

## Unregistering Javascript Plugin [​](#unregistering-javascript-plugin)

Imagine we wanted to exclude the `OffCanvasCart` plugin, just to get a test case which can be inspected easily. In order to remove a Javascript plugin, you only need to add the following line to your `main.js` file:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
window.PluginManager.deregister('OffCanvasCart', '[data-off-canvas-cart]');
```

After building the Storefront anew, you shouldn't be able to open the offcanvas cart anymore. Another useful way of testing this is using your browser's devtools. Just open your devtool's console and type in `PluginManager.getPluginList()` in order to get a list of all registered plugins.

In our case, we shouldn't find `OffCanvasCart` in the listed plugins anymore.

## Next steps [​](#next-steps)

Did you already take a look at our other storefront guides? They can give you some neat starting points on how to extend and customize Shopware's storefront.

* [Override existing Javascript in your plugin](./override-existing-javascript.html)
* [Reacting to Javascript events](./reacting-to-javascript-events.html)

---

## Add custom field in the storefront

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/using-custom-fields-storefront.html

# Add Custom Field in the Storefront [​](#add-custom-field-in-the-storefront)

## Overview [​](#overview)

This guide will show you how to use custom fields, e.g., labels in the Storefront.

## Prerequisites [​](#prerequisites)

You won't learn to create a plugin in this guide, head over to our [Plugin base guide](./../plugin-base-guide.html) to create a plugin first, if you don't know how it's done yet.

Needless to say, you need a custom field itself to add to the Storefront via your own plugin. Head over to the guide on [adding custom fields to Shopware](./../framework/custom-field/add-custom-field.html) to be able to prepare your own custom field.

## Use snippets of custom fields [​](#use-snippets-of-custom-fields)

First, if you add a custom field via API or Administration, automatically snippets for all languages are created. The naming of the snippet is like the following template: `customFields.` as prefix and then the name of the custom field. For example, if the name of the created custom field is `my_test_field`, then the created snippet name will be `customFields.my_test_field`.

INFO

In the snippet settings in the Administration you're able to edit and translate the snippet.

## Storefront usage of custom fields [​](#storefront-usage-of-custom-fields)

Adding custom fields in the Storefront is quite simple. You basically use Twig this way:

twig

```shiki
{{ "customFields.my_test_field"|trans|sw_sanitize }}: {{ page.product.translated.customFields.my_test_field }}
```

INFO

Did you notice the Twig function `sw_sanitize`? It's a Twig function we wrote, customized for Shopware's needs. It filters tags and attributes from a given string optimized for Shopware usage.

Imagine you want to add a text field to the product description. If you want to use the snippet in the Storefront, you have to extend a template file first. Let's say we want to add our custom field to the product description's text. The block of this element is `page_product_detail_description_content_text`, so we'll use it in our example. As we want to add our custom field in there, we use `parent` Twig function to keep the original template:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/product-detail/description.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/description.html.twig' %}

{% block page_product_detail_description_content_text %}
    {{ parent() }}
{% endblock %}
```

Now, we finally add our custom field as explained before:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/product-detail/description.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/description.html.twig' %}

{% block page_product_detail_description_content_text %}
    {{ parent() }}

    {# Insert your custom field here, as seen below: #}
    {{ "customFields.my_test_field"|trans|sw_sanitize }}: {{ page.product.translated.customFields.my_test_field }}
{% endblock %}
```

## Custom fields in forms [​](#custom-fields-in-forms)

Let's say you have a custom field for the customer entity through the administration; now, you want the customer to input data into it through a field in the customer register form. This can be done without the need for a subscriber or listener; simply add a field to the form using the correct custom field name.

INFO

For custom fields to work in forms, you must enable the **Modifiable via Store API** option in the custom field configuration. This setting allows the Store API to modify the field, which is required for storing custom data from storefront forms such as registration forms.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/component/address/address-personal.html.twig
{% sw_extends '@Storefront/storefront/component/address/address-personal.html.twig' %}

{% block component_address_personal_fields %}
    {{ parent() }}

	{# custom field #}
	<div class="form-group col-sm-6">
		<label class="form-label" for="customFields[custom_field_name]">
			{{ "customFields.custom_field_name"|trans|sw_sanitize}}*
		</label>
		<input type="text" class="form-control" name="customFields[custom_field_name]" value="{{context.customer.customFields['custom_field_name'] }}" id="customFields[custom_field_name]" required="required">
	</div>
{% endblock %}
```

---

## Add custom sorting for product listing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-sorting-product-listing.html

# Add Custom Sorting for Product Listing [​](#add-custom-sorting-for-product-listing)

## Overview [​](#overview)

Individual sortings are groups of sorting options which you can use to sort product listings. The sortings are available in the Storefront.

This guide will show you how to add individual sorting options using a migration (manageable) or at runtime (non-manageable).

## Prerequisites [​](#prerequisites)

In order to add your own custom sorting for product listings for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

You should also have a look at our [Database migrations](./../plugin-fundamentals/database-migrations.html) guide, as we use one in this guide.

## Create individual sorting with migration [​](#create-individual-sorting-with-migration)

In order to make your sorting manageable in the Administration by the user, you will need to migrate the data to the database.

Create a new Migration in your plugin:

INFO

Note: Do not change an existing migration if your plugin is already in use by someone. In that case, create a new Migration instead! This also means, that you have to re-install or update your plugin if you adjust the migration.

php

```shiki
// <plugin root>/src/Migration/Migration1615470599ExampleSorting.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingDefinition;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1615470599ExampleSorting extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1615470599;
    }

    public function update(Connection $connection): void
    {
        $myCustomSorting = [
            'id' => Uuid::randomBytes(),
            'url_key' => 'my-custom-sort',  // shown in url - must be unique system wide
            'priority' => 5,                // the higher the priority, the further upwards it will be shown in the sortings dropdown in Storefront
            'active' => 1,                  // activate / deactivate the sorting
            'locked' => 0,                  // you can lock the sorting here to prevent it from being edited in the Administration
            'fields' => json_encode([
                [
                    'field' => 'product.name',  // field to sort by
                    'order' => 'desc',          // asc or desc
                    'priority' => 1,            // in which order the sorting is to applied (higher priority comes first)
                    'naturalSorting' => 0       // apply natural sorting logic to this field
                ],
                // ... more fields
            ]),
            'created_at' => (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ];

        // insert the product sorting
        $connection->insert(ProductSortingDefinition::ENTITY_NAME, $myCustomSorting);

        // insert the translation for the translatable label
        // if you use multiple languages, you will need to update all of them
        $connection->executeStatement(
            'REPLACE INTO product_sorting_translation
             (`language_id`, `product_sorting_id`, `label`, `created_at`)
             VALUES
             (:language_id, :product_sorting_id, :label, :created_at)',
            [
                'language_id' => Uuid::fromHexToBytes(Defaults::LANGUAGE_SYSTEM),
                'product_sorting_id' => $myCustomSorting['id'],
                'label' => 'My Custom Sorting',
                'created_at' => (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]
        );
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

## Create individual sorting at runtime [​](#create-individual-sorting-at-runtime)

You can subscribe to the `ProductListingCriteriaEvent` to add a `ProductSortingEntity` as available sorting on the fly. If you don't know how to do this, head over to our [Listening to events](./../plugin-fundamentals/listening-to-events.html) guide.

INFO

While possible, it is not recommended adding an individual sorting at runtime. If you just wish for your individual sorting to be not editable by users in the Administration, create a migration and set the parameter `locked` to be `true`.

Here's an example how your subscriber could look like:

php

```shiki
// <plugin root>/src/Subscriber/ExampleListingSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\Events\ProductListingCriteriaEvent;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingCollection;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingEntity;
use Shopware\Core\Framework\Uuid\Uuid;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ExampleListingSubscriber implements EventSubscriberInterface
{

    public static function getSubscribedEvents(): array
    {
        return [
            // be sure to subscribe with high priority to add you sorting before the default shopware logic applies
            // otherwise storefront will throw a ProductSortingNotFoundException
            ProductListingCriteriaEvent::class => ['addMyCustomSortingToStorefront', 500],
        ];
    }

    public function addMyCustomSortingToStorefront(ProductListingCriteriaEvent $event): void
    {
        /** @var ProductSortingCollection $availableSortings */
        $availableSortings = $event->getCriteria()->getExtension('sortings') ?? new ProductSortingCollection();

        $myCustomSorting = new ProductSortingEntity();
        $myCustomSorting->setId(Uuid::randomHex());
        $myCustomSorting->setActive(true);
        $myCustomSorting->setTranslated(['label' => 'My Custom Sorting at runtime']);
        $myCustomSorting->setKey('my-custom-runtime-sort');
        $myCustomSorting->setPriority(5);
        $myCustomSorting->setFields([
            [
                'field' => 'product.name',
                'order' => 'desc',
                'priority' => 1,
                'naturalSorting' => 0,
            ],
        ]);

        $availableSortings->add($myCustomSorting);

        $event->getCriteria()->addExtension('sortings', $availableSortings);
    }
}
```

## Next steps [​](#next-steps)

To [add a custom filter](./add-listing-filters.html) to your listing in the Storefront head over to the corresponding guide.

---

## Add SCSS variables

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-scss-variables.html

# Add SCSS variables [​](#add-scss-variables)

INFO

The configuration flag `css` is available from Shopware Version 6.4.13.0

## Overview [​](#overview)

In order to add SCSS variables to your plugin, you can configure fields in your `config.xml` to be exposed as scss variables.

We recommend to use the declaration of SCSS variables via the `config.xml` but you can still use a subscriber if you need to be more flexible as described [here](./add-scss-variables-via-subscriber.html).

## Prerequisites [​](#prerequisites)

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin:

[Plugin Base Guide](../plugin-base-guide)

## Setup a default value for a custom SCSS variable [​](#setup-a-default-value-for-a-custom-scss-variable)

Before you start adding your config fields as SCSS variables, you should provide a fallback value for your custom SCSS variable in your plugin `base.scss`:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
// The value will be overwritten when the plugin is installed and activated
$sass-plugin-header-bg-color: #ffcc00 !default;

.header-main {
    background-color: $sass-plugin-header-bg-color;
}
```

## Plugin config values as SCSS variables [​](#plugin-config-values-as-scss-variables)

Now you can declare a config field in your plugin `config.xml` to be available as scss variable. The new tag is `<css>` and takes the name of the scss variable as its value.

xml

```shiki
<input-field>
    <name>sassPluginHeaderBgColor</name>
    <label>Header backgroundcolor</label>
    <label lang="de-DE">Kopfzeile Hintergrundfarbe</label>
    <css>sass-plugin-header-bg-color</css>
    <defaultValue>#eee</defaultValue>
</input-field>
```

This value will now be exposed as SCSS variable and will have the value set in the Administration or the default value if not set. **When this value is changed you still have to recompile the theme manually for the changes to take effect.** Plugin configurations with declared SCSS variable in its config.xml have a notice in the Administration that changes can change the theme.

---

## Add SCSS variables via Subscriber

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-scss-variables-via-subscriber.html

# Add SCSS Variables [​](#add-scss-variables)

## Overview [​](#overview)

In order to add SCSS variables to your plugin, you can configure fields in your `config.xml` to be exposed as scss variables.

We recommend to use the declaration of [SCSS variables](./add-scss-variables.html) via the `config.xml` but you can still use a subscriber if you need to be more flexible as described below.

## Prerequisites [​](#prerequisites)

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin:

[Plugin Base Guide](../plugin-base-guide)

You should also know how to listen to events:

[Listening to events](../plugin-fundamentals/listening-to-events)

## Setup a default value for a custom SCSS variable [​](#setup-a-default-value-for-a-custom-scss-variable)

Before you start adding your subscriber, you should provide a fallback value for your custom SCSS variable in your plugin `base.scss`:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
// The value will be overwritten by the subscriber when the plugin is installed and activated
$sass-plugin-header-bg-color: #ffcc00 !default;

.header-main {
    background-color: $sass-plugin-header-bg-color;
}
```

## Theme variables subscriber [​](#theme-variables-subscriber)

You can add a new subscriber according to the [Listening to events](./../plugin-fundamentals/listening-to-events.html) guide. In this example we name the subscriber `ThemeVariableSubscriber`. The subscriber listens to the `ThemeCompilerEnrichScssVariablesEvent`.

The `ThemeCompilerEnrichScssVariablesEvent` provides the `addVariable()` method which takes the following parameters:

* `$name:` (string): The name of the SCSS variable. In your SCSS, the passed string will be used exactly as its stated here, so please be careful with special characters. We recommend using kebab-case here. The variable prefix `$` will be added automatically. We also recommend prefixing your variable name with your plugin's or company's name to prevent naming conflicts.
* `$value:` (string): The value which should be assigned to the SCSS variable.
* `$sanitize` (bool - optional): Optional parameter to remove special characters from the variables value. The parameter will also add quotes around the variables value. In most cases quotes are not needed e.g. for color hex values. However, there may be situations where you want to pass individual strings to your SCSS variable.

WARNING

Please note that plugins are not sales channel specific. Your SCSS variables are directly added in the SCSS compilation process and will be globally available throughout all themes and Storefront sales channels. If you want to change a variables value for each sales channel you should use plugin config fields and follow the next example.

## Plugin config values as SCSS variables [​](#plugin-config-values-as-scss-variables)

Inside your `ThemeVariableSubscriber` you can also read values from the plugin configuration and assign those to a SCSS variable. This makes it also possible to have different values for each sales channel. Depending on the selected sales channel inside the plugin configuration in the Administration.

First, lets add a new plugin configuration field according to the [Plugin Configurations](./../plugin-fundamentals/add-plugin-configuration.html):

xml

```shiki
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Example configuration</title>
        <input-field type="colorpicker">
            <name>sassPluginHeaderBgColor</name>
            <label>Header background color</label>
        </input-field>
    </card>
</config>
```

As you can see in the example, we add an input field of the type colorpicker for our plugin. In the Administration, the component 'sw-colorpicker' will later be displayed for the selection of the value. You also can set a `defaultValue` which will be pre-selected like the following:

xml

```shiki
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Example configuration</title>
        <input-field type="colorpicker">
            <name>sassPluginHeaderBgColor</name>
            <label>Header background color</label>
            <defaultValue>#fff</defaultValue>
        </input-field>
    </card>
</config>
```

In order to be able to read this config, you have to inject the `SystemConfigService` to your subscriber:

* The `SystemConfigService` provides a `get()` method where you can access the configuration structure in the first parameter with a dot notation syntax like `SwagBasicExample.config.fieldName`. The second parameter is the sales channel `id`. With this `id` the config fields can be accessed for each sales channel.
* You can get the sales channel id through the getter `getSalesChannelId()` of the `ThemeCompilerEnrichScssVariablesEvent`.
* Now your sass variables can have different values in each sales channel.

### All config fields as SCSS variables [​](#all-config-fields-as-scss-variables)

Adding config fields via `$event->addVariable()` for every field individually may be a bit cumbersome in some cases. You could also loop over all config fields and call `addVariable()` for each one. However, this depends on your use case.

php

```shiki
// <plugin root>/src/Subscriber/ThemeVariableSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

// ...
use Symfony\Component\Serializer\NameConverter\CamelCaseToSnakeCaseNameConverter;

class ThemeVariableSubscriber implements EventSubscriberInterface
{
    // ...

    public function onAddVariables(ThemeCompilerEnrichScssVariablesEvent $event): void
    {
        $configFields = $this->systemConfig->get('SwagBasicExample.config', $event->getSalesChannelId());

        foreach($configFields as $key => $value) {
            // convert `customVariableName` to `custom-variable-name`
            $kebabCased = str_replace('_', '-', (new CamelCaseToSnakeCaseNameConverter())->normalize($key));

            $event->addVariable($kebabCased, $value);
        }
    }
}
```

To avoid camelCase variable names when reading from the `config.xml`, we recommend using the `CamelCaseToSnakeCaseNameConverter` to format the variable before adding it.

---

## Using a modal window

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/using-a-modal-window.html

# Using a Modal Window [​](#using-a-modal-window)

## Overview [​](#overview)

This guide explains how you can use a modal window in your plugin in different scenarios.

## Prerequisites [​](#prerequisites)

This guide requires you to already have a basic plugin running. This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../plugin-base-guide)

While this is not mandatory, having read the guide about adding custom JavaScript plugins beforehand might help you understand this guide a bit further:

[Add custom Javascript](./add-custom-javascript)

## Create a modal manually from the DOM using Bootstrap [​](#create-a-modal-manually-from-the-dom-using-bootstrap)

The simples solution to create a modal is by using Bootstrap. More info: [Modal Bootstrap](https://getbootstrap.com/docs/5.3/components/modal/#live-demo) Here is a basic implementation as an example. We override the `base_main_inner` from the `@Storefront/storefront/page/content/index.html.twig` template to insert the modal specific DOM elements.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        Launch demo modal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- insert your content here -->
                    ...
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>

    {{ parent() }}
{% endblock %}
```

## Create a modal using AjaxModalPlugin [​](#create-a-modal-using-ajaxmodalplugin)

When setting `data-ajax-modal="true"` together with `data-url` shopware automatically uses the `PseudoModalUtil` and the pseudo modal template from the `base.html.twig` to render a modal:

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <!-- This uses `AjaxModalPlugin` -->
    <button class="btn btn-primary"
            data-ajax-modal="true"
            data-url="https://example.org/ajax-url">
        Launch ajax modal
    </button>
    {{ parent() }}
{% endblock %}
```

WARNING

This does not work when the trigger selector is being changed via JavaScript, e.g. because of an AJAX call which replaces the content.

## Advanced / manual using Pseudo Modal Utility [​](#advanced-manual-using-pseudo-modal-utility)

To create a modal window you can use the `PseudoModalUtil` in your plugin.

As explained in the guide on [adding custom javascript](./add-custom-javascript.html) we load our JavaScript plugin by creating `index.html.twig` template in the `<plugin root>/src/Resources/views/storefront/page/content/` folder. Inside this template, extend from the `@Storefront/storefront/page/content/index.html.twig` and overwrite the `base_main_inner` block. After the parent content of the blog, add a template tag with the `data-example-plugin` attribute.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    {{ parent() }}

    <template data-example-plugin></template>
{% endblock %}
```

Now we need to register the plugin which should create a modal in the `PluginManager`. To achieve this you can add the following code to the `main.js` file.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/main.js
 // Import all necessary Storefront plugins
 import ExamplePlugin from './example-plugin/example-plugin.plugin';

 // Register your plugin via the existing PluginManager
 const PluginManager = window.PluginManager;
 PluginManager.register('ExamplePlugin', ExamplePlugin, '[data-example-plugin]');
```

Now let's get started with the modal window. First we have to import the `PseudoModalUtil` class in our plugin.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // ...
    }
}
```

Now we create a new modal instance using `new PseudoModalUtil()` and assign to a property of our plugin for later usage. We also call the method `open()` to make it visible.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        this.openModal();
    }
    
    openModal() {
        // create a new modal instance
        this.modal = new PseudoModalUtil();
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

To see your changes you have to build the storefront. Use the following command to build your storefront and reload it afterwards:

You can now see a blank modal which contains `undefined`. This is because we have not added any content to show inside the modal.

The constructor method of `PseudoModalUtil()` expects some HTML `content` to display. To keep this guide simple, we are only including sample code here. Of course, the content can also be generated via an API and inserted via AJAX requests.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

## Closing the modal [​](#closing-the-modal)

The `PseudoModalUtil` class also provide a `close()` method. Same as with opening the modal by calling `this.modal.open()`, you can simply close the modal with `this.modal.close()`.

## Callback when opening a modal [​](#callback-when-opening-a-modal)

The `open()` method of the `PseudoModalUtil` class supports a callback function as an argument. So if you need to perform some action when your modal opens, you can implement a callback like this:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and fire a callback function
        this.modal.open(this.onOpenModal.bind(this));
    }
    
    onOpenModal() {
        console.log('the modal is opened');
    }
}
```

## Updating the modal content [​](#updating-the-modal-content)

To update the content of a modal, `PseudoModalUtil` provides a method `updateContent()` to which you can pass the updated template string. The method also accepts a callback function as a second argument, which is called after the content has been updated. Here is an example how to use it:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
        
        // ... do some stuff

        const updatedContent = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Updated content</div>
            </div>
        `;
        
        this.modal.updateModal(updatedContent, this.onUpdateModal.bind(this));
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and fire a callback function
        this.modal.open(this.onOpenModal.bind(this));
    }
    
    onOpenModal() {
        console.log('the modal is opened');
    }

    onUpdateModal() {
        console.log('the modal was updated');
    }
    
}
```

## Customize the modal appearance [​](#customize-the-modal-appearance)

The constructor method of `PseudoModalUtil` provides optional configuration. If you don't need backdrop of the modal for example just turn it off by instantiating the modal like this

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // disable backdrop
        const useBackrop = false;
        
        // create a new modal instance
        this.modal = new PseudoModalUtil(content, useBackrop);
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

As you can see in the sample code, we are using the `js-pseudo-modal-template-title-element` class to style the title text of the modal. It also tells the `PseudoModalUtil` class that the content of the `div` holds the title text. Furthermore there are two more css selectors `js-pseudo-modal-template` and `js-pseudo-modal-template-content-element` to define the structure of the template string.

If you want to customize your modal by using different style classes, you can do that by overriding the defaults while instantiating `PseudoModalUtil`.

Here is an example which shows how to override the CSS class names.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
// ...
export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // ...
    }

    openModal(content) {
        // enable backdrop
        const useBackrop = true;

        // create a new modal instance
        this.modal = new PseudoModalUtil(
            content,
            useBackrop,
            '.custom-js-pseudo-modal-template',
            '.custom-js-pseudo-modal-template-content-element',
            '.custom-js-pseudo-modal-template-title-element'
        );

        // open the modal window and make it visible
        this.modal.open();
    }
}
```

---

## Using the datepicker plugin

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/using-the-datepicker-plugin.html

# Using the Datepicker Plugin [​](#using-the-datepicker-plugin)

## Overview [​](#overview)

To provide an input field for date and time values, you can use the datepicker plugin. This guide shows you how to use it.

The datepicker plugin uses the `flatpickr` implementation under the hood. So, check out the `flatpickr` documentation, if you need more information about the date picker configuration itself.

[Introduction](https://flatpickr.js.org)

## Prerequisites [​](#prerequisites)

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin:

[Plugin Base Guide](../plugin-base-guide)

You should also know how to customize templates:

[Customize templates](./customize-templates)

## Setup a datepicker input field [​](#setup-a-datepicker-input-field)

To apply the datepicker functionality we have to add a DOM element in a template, e.g. an input field. To keep this example simple for now we just override the `base_main_inner` block of the `storefront/page/content/index.html.twig` template.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

Now you should see an empty input field if you open the storefront in your browser. We need to add the data-attribute `data-date-picker` to activate the datepicker plugin on our input field.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               data-date-picker
        />
    </label>

    {{ parent() }}
{% endblock %}
```

If we check the change in the browser again, thus after reloading the page, we can see that the datepicker plugin is now active on this element.

## Configure the datepicker [​](#configure-the-datepicker)

If you select a date with the datepicker from the example above, you will see that a time is always selected and displayed in the input field. By default, the time selection is activated.

We can change this behaviour by passing more options to the datepicker plugin.

Here you can see how this is done by setting up a local Twig variable `pickerOptions`. We can assign a JSON formatted object to the variable and pass the value to the datepicker plugin through the `data-date-picker-options` attribute.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerOptions = {
        locale: app.request.locale,
        enableTime: true
    } %}
    
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               data-date-picker
               data-date-picker-options="{{ pickerOptions|json_encode|escape('html_attr') }}"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

As you can see, we also pass in the `locale` option which gets its value from `app.request.locale`. As a result, the datepicker plugin now uses the same locale as the current storefront and the date formatting matches active languages accordingly.

## Preselect a date [​](#preselect-a-date)

To preselect the value of the datepicker we can simply set its value in the input field which gets picked up by the datepicker plugin.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerOptions = {
        locale: app.request.locale,
        enableTime: true
    } %}
    
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               value="2021-01-01T00:00:00+00:00"
               data-date-picker
               data-date-picker-options="{{ pickerOptions|json_encode|escape('html_attr') }}"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

## Controlling the datepicker via buttons [​](#controlling-the-datepicker-via-buttons)

To open or close the datepicker by trigger buttons you can pass in DOM selectors. You can also setup a selector to reset the currently selected value. Here is an example which shows all three selectors in action.

twig

```shiki
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerProperties = {
        locale: app.request.locale,
        enableTime: true,
        selectors: {
            openButton: ".openDatePicker",
            closeButton: ".closeDatePicker",
            clearButton: ".resetDatePicker"
        }
    } %}

    <label>
        <input type="text"
               name="foo"
               class="customDate"
               value="2021-04-13T00:00:00+00:00"
               data-date-picker
               data-date-picker-options="{{ pickerProperties|json_encode|escape('html_attr') }}"
        />

        <button class="openDatePicker">Open</button>
        <button class="closeDatePicker">Close</button>
        <button class="resetDatePicker">Reset</button>
    </label>

    {{ parent() }}
{% endblock %}
```

## More options [​](#more-options)

| Option | Default | Description |
| --- | --- | --- |
| `dateFormat` | 'Y-m-dTH:i:S+00:00' | Pattern for the date string representation |
| `altInput` | true | Hides your original input and creates a new one. |
| `altFormat` | 'j. FY, H:i' | Alternative pattern for the date string representation if `altInput` is enabled. The value of the input field gets still formatted by `dateFormat` |
| `time_24hr` | true |  |
| `enableTime` | true |  |
| `noCalendar` | false |  |
| `weekNumbers` | true |  |
| `allowInput` | true |  |
| `minDate` | null | Specifies the minimum/earliest date (inclusively) allowed for selection |
| `maxDate` | null | Specifies the maximum/latest date (inclusively) allowed for selection. |

---

## Use nested line items

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/use-nested-line-items.html

# Use Nested Line Items [​](#use-nested-line-items)

## Overview [​](#overview)

This guide will show you how to use the nested line items in the Storefront.

## Prerequisites [​](#prerequisites)

As most guides, this guide is also built upon the [Plugin base guide](./../plugin-base-guide.html), but you don't necessarily need that. This guide will only extend views and shows how the Custom Product plugin handles this.

## Make nested line item removable [​](#make-nested-line-item-removable)

If the nested line item should be removable in the cart, the `removable` property has to be set, either via view, or in an own controller action. Also, a form with an own path action has to be added:

twig

```shiki
{% block page_checkout_item_remove_icon %}
    {% do nestedLineItem.setRemovable(true) %}
    <form action="{{ path('/mycontroller/nested/remove', { 'id': nestedLineItem.id }) }}" method="post">
        {{ parent() }}
    </form>
{% endblock %}
```

## Make nested line item changeable [​](#make-nested-line-item-changeable)

Most of the time, the root line item defines the nested line items, therefore there is a change button for its root line item in the cart. In the block of the change button, the variable `isChangeable` has to be set, and the button has to be surrounded with a link to the action like this:

twig

```shiki
{% block component_offcanvas_item_children_header_content_change_button %}
    {% set isChangeable = true %}
    {% set seo = seoUrl('frontend.detail.page', {
            'productId': lineItem.children.first.referencedId,
            'swagCustomizedProductsConfigurationEdit': lineItem.extensions.customizedProductConfiguration.id
        })
    %}
    
    <a href="{{ seo }}" class="order-item-product-name" title="{{ label }}">
        {{ parent() }}
    </a>
{% endblock %}
```

## About extended functionality [​](#about-extended-functionality)

Please notice: Nested line items can be implemented in various ways, so there's no telling what a **default handling** could be. Therefore, it is necessary to implement a change or remove handling by yourself.

---

## Add custom twig functions

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/storefront/add-custom-twig-function.html

# Add Custom Twig Functions [​](#add-custom-twig-functions)

## Overview [​](#overview)

Let us consider, for instance, you want to call a PHP script from the twig template during the theme development to create a `MD5-hash`. In such a case, you can create your own twig functions. For this example, pass a string to the `TwigFunction` and return a `MD5-Hash`.

INFO

It is not recommended to use twig functions in order to retrieve data from the database. In such a case, DataResolver could come in handy.

## Prerequisites [​](#prerequisites)

In order to create your own twig function for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../plugin-base-guide.html).

## Creating twig function [​](#creating-twig-function)

In the following sections, we will create and expand all necessary files for the twig function to work. There are two such files:

* PHP file with the twig functions itself and
* Services.xml

### Creating the twig function [​](#creating-the-twig-function)

For clarity, create a folder named `Twig` within the `src` folder. Then create a new php file with desired file name within the `Twig` folder. Refer to the below example :

PLUGIN\_ROOT/src/Twig/SwagCreateMd5Hash.php

php

```shiki
<?php declare(strict_types=1);

namespace SwagBasicExample\Twig;

use Shopware\Core\Framework\Context;
use Twig\Extension\AbstractExtension;
use Twig\TwigFunction;

class SwagCreateMd5Hash extends AbstractExtension
{
    public function getFunctions()
    {
        return [
            new TwigFunction('createMd5Hash', [$this, 'createMd5Hash']),
        ];
    }

    public function createMd5Hash(string $str)
    {
        return md5($str);
    }
}
```

Of course, you can do everything in the `createMd5Hash` function that PHP can do, but the `service.xml` handles registration of the service in the DI container.

PLUGIN\_ROOT/src/Resources/config/services.xmltwig

xml

```shiki
    <services>
        <service id="SwagBasicExample\Twig\SwagCreateMd5Hash" public="true">
            <tag name="twig.extension"/> <!--Required-->
        </service>
    </services>
```

Once done, you can access this `TwigFunction` within your plugin.

### Use twig function in template [​](#use-twig-function-in-template)

The created function is now available in all your templates. You can call it like each other function.

twig

```shiki
{% sw_extends '@Storefront/storefront/page/content/product-detail.html.twig' %}

{% set md5Hash = createMd5Hash('Shopware is awesome') %}

{% block page_content %}
    {{ parent() }}

    {{ md5Hash }}
{% endblock %}
```

---

