# Guides Plugins Plugins Administration Module Component Management

*Scraped from Shopware Developer Documentation*

---

## Add custom module

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/add-custom-module.html

# Add custom module [​](#add-custom-module)

In the `Administration` core code, each module is defined in a directory called `module`. Inside the `module` directory lies the list of several modules, each having their own directory named after the module itself.

## Prerequisites [​](#prerequisites)

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../../plugin-base-guide)

## Creating the index.js file [​](#creating-the-index-js-file)

The first step is creating a new directory `<plugin root>/src/Resources/app/administration/src/module/swag-example`, so you can store your own modules files in there. Right afterward, create a new file called `index.js` in there. Consider it to be the main file for your custom module.

WARNING

This is necessary, because Shopware 6 is automatically requiring an `index.js` file for each module.

Your custom module directory isn't known to Shopware 6 yet. The entry point of your plugin is the `main.js` file. That's the file you need to change now so that it loads your new module. For this, add the following line to your `main.js` file:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/swag-example';
```

Now your module's `index.js` will be executed.

## Registering the module [​](#registering-the-module)

Your `index.js` is still empty now, so let's get going to actually create a new module. This is technically done by calling the method `registerModule` method of our [ModuleFactory](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/core/factory/module.factory.ts), but you're not going to use this directly.

Instead, you're using the `Shopware.Module.register()` method, but why is that?

`Shopware` is a [global object](./../data-handling-processing/the-shopware-object.html) created for third party developers. It is mainly the bridge between the Shopware Administration and our plugin. The `Module` object comes with a `register` helper method to easily register your module. The method needs two parameters to be set, the first one being the module's name, the second being a javascript object, which contains your module's configuration.

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-example', {
    // configuration here
});
```

## Configuring the module [​](#configuring-the-module)

In this file, you can configure a couple of things, e.g., the color of your module. Each module needs a primary color, which will be used on specific accents and locations throughout your module. To name a few, it's the color of the main icon of the module, the tag in the global search input and the accent color of the smart bar.

In this example `#ff3d58` is used as a color, which is a soft red. Also, each module has its own icon. You can see [here](https://shopware.design/icons/) which icons are available in Shopware 6 by default. In our case here, let's say we use the icon `regular-shopping-bag`, which will also be used for the module.

DANGER

This is not the icon being used for a menu entry! The icon for that needs to be configured separately. Please refer to the [Add a menu entry](./../routing-navigation/add-menu-entry.html) guide for more information on this topic.

In addition, you're able to configure a title here, which will be used for the actual browser title. Just add a string for the key `title`. This will be the default title for your module, you can edit this for each component later on.

The `description` is last basic information you should set here, which will be shown as an empty-state. That means the description will be shown e.g., when you integrated a list component, but your list is empty as of now. In that case, your module's description will be displayed instead.

Another important aspect is the routes that your module is going to use, such as e.g. `swag-example-list` for the list of your module, `swag-example-detail` for the detail page and `swag-example-create` for creating a new entry. Those routes are configured as an object in a property named `routes`. We will cover that in the next paragraph.

## Setting up menu entry and routes [​](#setting-up-menu-entry-and-routes)

The next steps are covered in their own guides. The first one would be adding a menu entry, so please take a look at the guide regarding:

[Add menu entry](../routing-navigation/add-menu-entry)

The second one refers to setting up custom routes; its guide can be found in the guide on adding custom routes:

[Add custom route](../routing-navigation/add-custom-route)

## Set up additional meta info [​](#set-up-additional-meta-info)

If you have been following that guide, then you should have got a menu entry then. The related routes are also set up already and linked to components, which will be created in the next main step. There's a few more things we need to change in the configurations though that you should add to your module, such as a unique `name` and a `type`. For reference, see this example:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-example', {
    type: 'plugin',
    name: 'Example',
    title: 'swag-example.general.mainMenuItemGeneral',
    description: 'sw-property.general.descriptionTextModule',
    color: '#ff3d58',
    icon: 'regular-shopping-bag',
...
```

The `name` should be technically unique, the `type` would be 'plugin' here. When it comes to this `type`, there are basically two options in Shopware: `core` and `plugin`. So every third-party module should use `plugin`. To give a little context: Looking at `module.factory` inside `registerModule` the plugin type is the only case which is being checked and has some different behavior. So it is more a convention and not a real validation which throws an error when `type` is divergent to these options.

## Implementing snippets [​](#implementing-snippets)

You've already set a label for your module's menu entry. Yet, by default the `Administration` expects the value in there to be a [Vuei18n](https://kazupon.github.io/vue-i18n/started.html#html) variable, a translation key that is. It's looking for a translation key `example` now and since you did not provide any translations at all yet, it can't find any translation for it and will just print the key of a snippet. Now let's implement the translation snippets.

This is done by providing a new object to your module configuration, `snippets` this time. This object contains another object for each language you want to support. In this example `de-DE` and of course `en-GB` will be supported.

Each language then contains a nested object of translations, so let's have a look at an example:

json

```shiki
{
    "swag-example": {
        "nested": {
            "value": "example"
        },
        "foo": "bar"
    }
}
```

In this example you would have access to two translations by the following paths: `swag-example.nested.value` to get the value 'example' and `swag-example.foo` to get the value 'bar'. You can nest those objects as much as you want. Please note that each path is prefixed by the extension name.

Since those translation objects become rather large, you should store them into separate files. For this purpose, create a new directory `snippet` in your module's directory and in there two new files: `de-DE.json` and `en-GB.json`. The snippet files will be loaded automatically based on the folder structure.

Let's also create the first translation, which is for your menu's label. It's key should be something like this: `swag-example.general.mainMenuItemGeneral`

Thus open the `snippet/en-GB.json` file and create the new object in there. The structure here is the same as in the first example, just formatted as json file. Afterward, use this path in your menu entry's `label` property.

To translate the `description` or the `title`, add those to your snippet file as well and edit the values in your module's `description` and `title`. The title will be the same as the main menu entry by default.

This should be your snippet file now:

json

```shiki
{
    "swag-example": {
        "general": {
            "mainMenuItemGeneral": "My custom module",
            "descriptionTextModule": "Manage this custom module here"
        }
    }
}
```

## Build the Administration [​](#build-the-administration)

As mentioned above, Shopware 6 is looking for a `main.js` file in your plugin. Its contents get minified into a new file named after your plugin and will be moved to the `public` directory of Shopware 6 root directory. Given this plugin would be named "AdministrationNewModule", the bundled and minified javascript code for this example would be located under `<plugin root>/src/Resources/public/administration/js/administration-new-module.js`, once you run the command following command in your shopware root directory:

INFO

Your plugin has to be activated for this to work.

Make sure to also include that file when publishing your plugin! A copy of this file will then be put into the directory `<shopware root>/public/bundles/administration/administrationnewmodule/administration/js/administration-new-module.js`.

Your minified JavaScript file will now be loaded in production environments.

## Special: Case Settings [​](#special-case-settings)

### Link your module into settings [​](#link-your-module-into-settings)

If you think about creating a module concerning settings, you might want to link your module in the `settings` section of the Administration. You can add the `settingsItem` option to the module configuration as seen below:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
import './page/swag-plugin-list';
import './page/swag-plugin-detail';
Shopware.Module.register('swag-plugin', {
    ...
    settingsItem: [{
        group: 'plugins',
        icon: 'regular-rocket',
        to: 'swag.plugin.list',
        name: 'SwagExampleMenuItemGeneral', // optional, fallback is taken from module
        id: '', // optional, fallback is taken from module
        label: '', // optional, fallback is taken from module
        iconComponent: YourCustomIconRenderingComponent, // optional, this overrides the component used to render the icon
    }]
});
```

The `group` property determines the tab, the item will be displayed in. Valid options are 'shop', 'system' and 'plugins'.

The `icon` property contains the icon name which will be displayed. Refer to the [Meteor Icon Kit documentation](https://developer.shopware.com/resources/meteor-icon-kit/) for icon names.

The `to` property must contain the name of the route. The route has to be defined in a separate routes section as described [here](./../routing-navigation/add-custom-route.html). Have a look at the `Configuring the route` section in particular to find out about the name of your route.

## Example for the final module [​](#example-for-the-final-module)

Here's your final module:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
import './page/swag-example-list';
import './page/swag-example-detail';
import './page/swag-example-create';
import deDE from './snippet/de-DE';
import enGB from './snippet/en-GB';

Shopware.Module.register('swag-example', {
    type: 'plugin',
    name: 'Example',
    title: 'swag-example.general.mainMenuItemGeneral',
    description: 'sw-property.general.descriptionTextModule',
    color: '#ff3d58',
    icon: 'regular-shopping-bag',

    snippets: {
        'de-DE': deDE,
        'en-GB': enGB
    },

    routes: {
        list: {
            component: 'swag-example-list',
            path: 'list'
        },
        detail: {
            component: 'swag-example-detail',
            path: 'detail/:id',
            meta: {
                parentPath: 'swag.example.list'
            }
        },
        create: {
            component: 'swag-example-create',
            path: 'create',
            meta: {
                parentPath: 'swag.example.list'
            }
        }
    },

    navigation: [{
        label: 'swag-example.general.mainMenuItemGeneral',
        color: '#ff3d58',
        path: 'swag.example.list',
        icon: 'regular-shopping-bag',
        position: 100
    }]
});
```

## Next steps [​](#next-steps)

As you might have noticed, we are just adding a custom module to the module. However, there's a lot more possible when it comes to extending the Administration. In addition, you surely want to customize your module even more. You may want to try the following things:

* [Add custom component](./../module-component-management/add-custom-component.html)
* [Add a menu entry](./../routing-navigation/add-menu-entry.html)
* [Add a custom route](./../routing-navigation/add-custom-route.html)
* [Add a custom service](./../services-utilities/add-custom-service.html)
* [Add translations](./../templates-styling/adding-snippets.html)
* [Customizing another module](./customizing-modules.html)
* [Dealing with data in the Administration](./../data-handling-processing/using-data-handling.html)
* [Adding permissions to your module](./../permissions-error-handling/add-acl-rules.html)

---

## Add custom component

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/add-custom-component.html

# Add custom component [​](#add-custom-component)

## Overview [​](#overview)

Since the Shopware 6 Administration is using [VueJS](https://vuejs.org/) as its framework, it also supports creating custom components. This guide will teach you how to register your own custom component with your plugin.

In this example, you will create a component that will print a 'Hello world!' everywhere it's being used.

## Prerequisites [​](#prerequisites)

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../../plugin-base-guide)

If you want to work with entities in your custom component or page, it might be useful to take a look at how to create a custom entity guide first:

[Adding custom complex data](../../framework/data-handling/add-custom-complex-data)

Especially if you want to add a new page for an own module, you should consider looking at the process on how to add a custom module first.

[Add custom module](add-custom-module)

This way, you're able to start building your own module in the right order.

### Injecting into the Administration [​](#injecting-into-the-administration)

Same as with all custom extensions of the Administration, the main entry point to extend the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be found by Shopware 6.

## Creating a custom component [​](#creating-a-custom-component)

### Path to the component [​](#path-to-the-component)

Usually there's one question you have to ask yourself first: Will your new component be used as a `page` for your plugin's custom route, or is this going to be a component to be used by several other components, such as an element that prints 'Hello world' everywhere it's used? In order to properly structure your plugin's code and to be similar to the core structure, you have to answer this question first. If it's going to be used as page for a module, it should be placed here: `<plugin-root>/src/Resources/app/administration/src/module/<your module's name>/page/<your component name>`

Otherwise, if it's going to be a general component to be used by other components, the following will be the proper path. For this example, this component scenario is used. `<plugin-root>/src/Resources/app/administration/src/component/<name of your plugin>/<name of your component>`

INFO

Using this path is **not** a hard requirement, but rather a recommendation. This way, third party developers having a glance at your code will get used to it real quick, because you stuck to Shopware 6's core conventions.

Since the latter example is being used, this is the path being created in the plugin now: `<plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world`

### Import your custom component via main.js file [​](#import-your-custom-component-via-main-js-file)

In the directory mentioned above, create a new file `index.js`. We will get you covered with more information about it later. Now import your custom component using your plugin's `main.js` file:

### Index.js as main entry point for this component [​](#index-js-as-main-entry-point-for-this-component)

Head back to the `index.js` file, this one will be the most important for your component.

The structure of this file depends on the type of your component. If it loads synchronously, you need to register your component directly in this file. If it loads asynchronously, you can just export the component and register it in the `main.js` file.

A component's template is being defined by using the `template` property. For this short example, the template will be defined inline. An example for a bigger template will also be provided later on this page.

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world
export default Shopware.Component.wrapComponentConfig({
    template: '<h2>Hello world!</h2>'
});
```

That's it. You can now use your component like this `<hello-world></hello-world>` in any other template in the Administration.

### Long template example [​](#long-template-example)

It's quite uncommon to have such a small template example and you don't want to define huge templates inside a javascript file. For this case, just create a new template file in your component's directory, which should be named after your component. For this example `hello-world.html.twig` is used.

Now simply import this file in your component's JS file and use the variable for your property.

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world.html.twig
import template from 'hello-world.html.twig';

export default Shopware.Component.wrapComponentConfig('hello-world', {
    template: template
});
```

In the core code, you will find another syntax for the same result though:

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world.html.twig
import template from 'hello-world.html.twig';

export default Shopware.Component.wrapComponentConfig('hello-world', {
    template
});
```

This is a [shorthand](https://eslint.org/docs/latest/rules/object-shorthand), which can only be used if the variable is named exactly like the property.

## Next steps [​](#next-steps)

You've now added a custom component, including a little template. However, there's more to discover here.

* [More about templates](./../templates-styling/writing-templates.html)
* [Add some styling to your component](./../templates-styling/add-custom-styles.html)
* [Use shortcuts for your component](./../advanced-configuration/add-shortcuts.html)

Furthermore, what about [customizing other components](./customizing-components.html), instead of creating new ones?

---

## Customize modules

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/customizing-modules.html

# Customize modules [​](#customize-modules)

## Overview [​](#overview)

In the `Administration` core code, each module is defined in a directory called `module`. A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with TwigJS, the templating engine, used in the Administration. However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Customizing a module [​](#customizing-a-module)

Module settings like `color`, `icon`, `navigation` are fixed by design and cannot be changed.

A guide for customizing components, which are already defined in existing modules, can be found here - [Customizing components](./../module-component-management/customizing-components.html) ..

However, modules themselves cannot be directly overridden.

At some point you need to add or change the routes of a module. For example when you want to add a tab to the page.

This is done by creating a new module and implementing a `routeMiddleware`. You can add those changes to your `main.js` file, which could then look like this:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
Shopware.Module.register('my-new-custom-route', {
    routeMiddleware(next, currentRoute) {
        if (currentRoute.name === 'sw.product.detail') {
            currentRoute.children.push({
                name: 'sw.product.detail.custom',
                path: '/sw/product/detail/:id/custom',
                component: 'sw-product-detail-custom',
                meta: {
                    parentPath: "sw.product.index"
                }
            });
        }
        next(currentRoute);
    }
});
```

In this example we register a new module which uses the `routeMiddleWare` to scan the routes while the `Vue router` is being set up. If we find the route `sw.product.detail` we just add another child route by pushing it to the `currentRoute.children`.

You can find a detailed example in the [Add tab to existing module](./../routing-navigation/add-new-tab.html) guide.

## More interesting topics [​](#more-interesting-topics)

* [Customizing components](./../module-component-management/customizing-components.html)
* [Adding a route](./../routing-navigation/add-custom-route.html)

---

## Customizing components

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/customizing-components.html

# Customizing components [​](#customizing-components)

The Shopware 6 Administration allows you to override and extend components to change its content and its behavior.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module. Of course, you will have to understand JavaScript, Vue and have a basic familiarity with TwigJS block system, and the templating engine used in the Administration. It is just used for the block extending and overriding. Every other feature of TwigJS is not used in the Administration. However, that is a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## General [​](#general)

To add new functionality or change the behavior of an existing component, you can either override or extend the component.

The difference between the two methods is that with `Component.extend()` a new component is created. With `Component.override()`, on the other hand, the previous behavior of the component is simply overwritten.

## Override a component [​](#override-a-component)

The following example shows how you can override the template of the `sw-text-field` component.

JS

```shiki
// import the new twig-template file
import template from './sw-text-field-new.html.twig';

// override the existing component `sw-text-field` by passing the new configuration
Shopware.Component.override('sw-text-field', {
    template
});
```

## Extending a component [​](#extending-a-component)

To create your custom text-field `sw-custom-field` based on the existing `sw-text-field` you can implement it like the following:

JS

```shiki
// import the custom twig-template file
import template from './sw-custom-field.html.twig';

// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {
    template
});
```

Now you can render your new component `sw-custom-field` in any template like this:

twig

```shiki
    <sw-custom-field></sw-custom-field>
```

## Customize a component template [​](#customize-a-component-template)

To extend a given template you can use the Twig `block` feature.

Imagine, the component you want to extend/override has the following template:

twig

```shiki
{% block card %}
    <div class="sw-card">
        {% block card_header %}
            <div class="sw-card--header">
                {{ header }}
            </div>
        {% endblock %}

        {% block card_content %}
            <div class="sw-card--content">
                {{ content }}
            </div>
        {% endblock %}
    </div>
{% endblock %}
```

Maybe you want to replace the markup of the header section and add an extra block to the content. With the Twig `block` feature you can implement a solution like this:

twig

```shiki
{# override/replace an existing block #}
{% block card_header %}
    <h1 class="custom-header">
        {{ header }}
    </h1>
{% endblock %}

{% block card_content %}

    {# render the original block #}
    {% parent %}

    <div class="card-custom-content">
        ...
    </div>
{% endblock %}
```

Summarized with the `block` feature you will be able to replace blocks inside a template. Additionally, you can render the original markup of a block by using `{% parent %}`

## Extending methods and computed properties [​](#extending-methods-and-computed-properties)

Sometimes you need to change the logic of a method or a computed property while you are extending/overriding a component. In the following example we extend the `sw-text-field` component and change the `onInput()` method, which gets called after the value of the input field changes.

JS

```shiki
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // override the logic of the onInput() method
    methods: {
        onInput() {
            // add your custom logic in here
            // ...
        }
    }
});
```

In the previous example, the inherited logic of `onInput()` will be replaced completely. But sometimes, you will only be able to add additional logic to the method. You can achieve this by using `this.$super()` call.

JS

```shiki
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // extend the logic of the onInput() method
    methods: {
        onInput() {
            // call the original implementation of `onInput()`
            const superCallResult = this.$super('onInput');

            // add your custom logic in here
            // ...
        }
    }
});
```

This technique also works for `computed` properties, for example:

JS

```shiki
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // extend the logic of the computed property `stringRepresentation`
    computed: {
        stringRepresentation() {
            // call the original implementation of `onInput()`
            const superCallResult = this.$super('stringRepresentation');

            // add your custom logic in here
            // ...
        }
    }
});
```

## Real world example for block overriding [​](#real-world-example-for-block-overriding)

### Finding the block to override [​](#finding-the-block-to-override)

In this guide we want to change the heading of the Shopware 6 dashboard to be `Welcome to a customized Administration` instead of `Welcome to Shopware 6`. To do this, we first need to find an appropriate twig block to override. We don't want to replace too much but also to not override too little of the Administration. In this case, we only want to override the headline and not links or anything else on the page. Looking at the twig markup for the dashboard [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/module/sw-dashboard/page/sw-dashboard-index/sw-dashboard-index.html.twig), suggests that we only need to override the twig block with the name `sw_dashboard_index_content_intro_content_headline` to achieve our goal.

### Preparing the override [​](#preparing-the-override)

Now that we know where to place our override, we need to decide what to override it with. In this very simple example it suffices to create a twig file, declare a block with the name we previously found and to insert our new header into the block.

text

```shiki
<!-- <plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/sw-dashboard-index.html.twig -->
{% block sw_dashboard_index_content_intro_content_headline %}
    <h1>
        Welcome to a customized component
    </h1>
{% endblock %}
```

This overrides the entire twig block with our new markup. However, if we want to retain the original content of the twig block and just add our markup to the existing one, we can do that by including a `{% parent %}` somewhere in the twig block. Learn more about the capabilities of twig.js [here](https://github.com/twigjs/twig.js/wiki).

As you might have noticed the heading we just replaced had a `{ $tc() }` [string interpolation](https://vuejs.org/v2/guide/syntax.html#Text) which is used to make it multilingual. Learn more about internationalization in the Shopware 6 Administration and about adding your own snippets to the Administration [here](./../templates-styling/adding-snippets.html).

### Applying the override [​](#applying-the-override)

Registering the override of the Vue component is done by using the override method of our ComponentFactory. This could be done in any `.js` file, which then has to be later imported, but we'll place it in `<plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/index.js`.

javascript

```shiki
import template from './sw-dashboard-index.html.twig';

Shopware.Component.override('sw-dashboard-index', {
    template
});
```

The first parameter matches the component to override, the second parameter has to be an object containing the actually overridden properties for example, the new twig template extension for this component.

### Loading the JavaScript File [​](#loading-the-javascript-file)

The main entry point to customize the Administration via a plugin is the `main.js` file. It has to be placed into the `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

The only thing now left to just add an import for our previously created `./sw-dashboard-index-override/index.js` in the `main.js`:

javascript

```shiki
import './sw-dashboard-index-override/';
```

## Experimental: Composition API extension system [​](#experimental-composition-api-extension-system)

Shopware 6 is introducing a new way to extend components using the Composition API. This system is currently in an experimental state and is needed for the future migration of components from the Options API to the Composition API.

### Current status and future plans [​](#current-status-and-future-plans)

* The existing Options API extension system remains fully supported and functional.
* The new Composition API extension system is introduced as an experimental feature.
* In future versions, components will gradually migrate from Options API to Composition API.
* Plugin developers are encouraged to familiarize themselves with the new system, but should continue using the current Component factory extension system for components written with the Options API.
* For components written with the Composition API, the new extension system should be used.
* In the long term, the Composition API extension system will become the standard way to override components. The Options API extension system will be deprecated and eventually removed when all components are migrated to the Composition API.

### How it works [​](#how-it-works)

The new extension system introduces two main functions:

1. `Shopware.Component.createExtendableSetup`: Used within components to make them extendable. This will mainly be used by the core team to make components extendable.
2. `Shopware.Component.overrideComponentSetup`: Used by plugins to override components.

### Using overrideComponentSetup [​](#using-overridecomponentsetup)

The `overrideComponentSetup` function is a key part of the new Composition API extension system. It allows plugin developers to override or extend the behavior of existing components without directly altering their source code.

### Basic usage [​](#basic-usage)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('componentName', (previousState, props, context) => {
    // Your extension logic here
    return {
        // Return the new or modified properties and methods
    };
});
```

#### Parameters [​](#parameters)

1. `componentName`: A string identifying the component you want to override.
2. Callback function: This function receives three arguments:
   1. `previousState`: The current state of the component, including all its reactive properties and methods.
   2. `props`: The props passed to the component.
   3. `context`: The setup context, similar to what you would receive in a standard Vue 3 setup function.

#### Return value [​](#return-value)

The callback function should return an object containing any new or modified properties or methods you want to add or change in the component.

#### Example: Replacing a Single Property [​](#example-replacing-a-single-property)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-product-list', (previousState) => {
    const newPageSize = ref(50);

    return {
        pageSize: newPageSize // Override the default page size with the new ref
    };
});
```

#### Example: Adding a New Method [​](#example-adding-a-new-method)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-order-list', (previousState) => {
    return {
        newCustomMethod() {
            console.log('This is a new method added to sw-order-list');
        }
    };
});
```

#### Example: Modifying existing data [​](#example-modifying-existing-data)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState) => {
    // Add a new column to the list
    previousState.columns.push({ property: 'customField', label: 'Custom Field' });
    
    return {};
});
```

#### Example: Overwriting a method [​](#example-overwriting-a-method)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState) => {
    // Overwrite the existing method
    const newIncrement = () => {
        // Able to access the previous method
        previousState.increment();
        // Add custom logic
        console.log('Incremented by 1');
    };

    return {
        increment: newIncrement,
    };
});
```

#### Example: Accessing props and context [​](#example-accessing-props-and-context)

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState, props, context) => {
    // Access the props
    console.log(props);

    // Access the context
    console.log(context);

    return {};
});
```

### Important notes [​](#important-notes)

1. Type Safety: The system aims to provide type safety. Make sure your IDE is set up to recognize the types from Shopware's type definitions.
2. Reactive Properties: When modifying reactive properties, ensure you maintain their reactivity. Use Vue's reactive utilities when necessary.
3. Multiple Overrides: Multiple plugins can override the same component. Overrides are applied in the order they are registered.
4. Performance: Be mindful of performance implications when adding complex logic to frequently used components.
5. Compatibility: This method is part of the experimental Composition API system. Ensure your plugin clearly states its dependency on this feature.
6. Testing: Thoroughly test your overrides, especially when modifying core component behavior.

### Example real world usage [​](#example-real-world-usage)

Here is an example of how to create an extendable component and how to override it:

javascript

```shiki
import { defineComponent, reactive } from 'vue';

// Original component
const originalComponent = defineComponent({
    template: `
        <div>
            <h1>{{ message }}</h1>
            <div>
                <mt-button @click="increment">Increment</mt-button>

                <p>
                    {{ countMessage }}
                </p>

                <p>
                    Notifications are currently: {{ showNotification ? 'enabled' : 'disabled' }}
                </p>
            </div>
        </div>
    `,
    props: {
        showNotification: {
            type: Boolean,
            default: false,
        },
    },
    setup: (props, context) => Shopware.Component.createExtendableSetup({
        props,
        context,
        name: 'originalComponent',
    }, () => {
        const count = ref(0);
        const message = 'Hello from Shopware!';
        const countMessage = computed(() => `The current count is: ${count.value}`);

        const increment = () => {
            count.value++;
        };

        const privateExample = ref('This is a private property');

        return {
            public: {
                count,
                message,
                countMessage,
                increment,
            },
            private: {
                privateExample,
            }
        };            
    }),
});

// Overriding the component with a plugin
Shopware.Component.overrideComponentSetup()('originalComponent', (previousState, props) => { 
    const newMessage = 'Hello from the plugin!';
    const newCountMessage = computed(() => `The new, amazing count is: ${previousState.count.value}`);
    const newIncrement = () => {
        previousState.increment();
        
        if (props.showNotification) {
            Shopware.ServiceContainer.get('notification').dispatch({
                title: 'Incremented!',
                message: `The count has been incremented by the user to ${previousState.count.value}!`,
                variant: 'success',
            });
        }
    };

    return {
        message: newMessage,
        countMessage: newCountMessage,
        increment: newIncrement,
    };
});
```

In this example, `createExtendableSetup` is used to make the `originalComponent` extendable. The `overrideComponentSetup` function is then used to modify the properties of the component. In this case, the message is changed, a new computed property is added, and the increment method is modified to show a notification if the `showNotification` prop is set to `true`.

### Key differences from Options API extension system [​](#key-differences-from-options-api-extension-system)

* Uses Composition API syntax and reactive primitives of Vue 3 instead of Vue 2 options API.
* Extensions are applied using function composition rather than option merging.
* Provides more granular control over what parts of a component can be overridden.
* Only overrides are possible. Extending a component is not supported anymore. This can be done natively with the Composition API.

### Using TypeScript [​](#using-typescript)

To take full advantage of the Composition API extension system, it is recommended to use TypeScript. This will provide better type safety and autocompletion in your IDE and prevent common errors.

For adding type safety to props you need to import the type of the component you want to override and use it in the `overrideComponentSetup` function as a generic type: `<typeof _InternalTestComponent>`. The types for the `previousState` are automatically inferred from the component you are overriding by using the correct component name.

typescript

```shiki
import _InternalTestComponent from 'src/the/path/to/the/exported/component';

Shopware.Component.overrideComponentSetup<typeof _InternalTestComponent>()('_internal_test_compponent', (previousState, props) => {
    const newBaseValue = ref(5);
    const newMultipliedValue = computed(() => {
        // Props are now correctly typed
        return newBaseValue.value * props.multiplier!;
    });

    // Previous state is now correctly typed
    previousState.baseValue.value = 2;

    return {
        baseValue: newBaseValue,
        multipliedValue: newMultipliedValue,
    };
});
```

### Accessing private properties [​](#accessing-private-properties)

In some cases, you may need to access private properties of a component. This is not recommended, as it can lead to unexpected behavior and breakages when the component is updated. However, if you need to access private properties for debugging or testing purposes, you can do so using the `_private` property of the `previousState` object where all private properties are stored.

Note: overriding and accessing private properties has no TS support and is not recommended for production use.

javascript

```shiki
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState, props, context) => {
    // Access the private properties
    console.log(previousState._private.thePrivateProperty);
});
```

## More interesting topics [​](#more-interesting-topics)

* [Customizing templates](./../templates-styling/writing-templates.html)
* [Customizing via custom styles](./../templates-styling/add-custom-styles.html)
* [Using base components](./../module-component-management/using-base-components.html)

---

## Add custom input field to existing component

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/add-custom-field.html

# Add custom input field to existing component [​](#add-custom-input-field-to-existing-component)

## Overview [​](#overview)

If you were wondering how to add a new input field to an existing module in the Administration via plugin, then you've found the right guide to cover that subject. In the following examples, you'll add a new input field to the product's detail page, to display and configure some other product data not being handled by default.

## Prerequisites [​](#prerequisites)

This guide **does not** explain how you can create a new plugin for Shopware 6. Head over to our plugin base guide to learn how to create a plugin at first:

[Plugin Base Guide](../../plugin-base-guide)

## Injecting into the Administration [​](#injecting-into-the-administration)

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

Your `main.js` file then needs to override the [Vue component](https://vuejs.org/guide/essentials/component-basics.html) using the `override` method of our `ComponentFactory`.

The first parameter matches the component to override, the second parameter has to be an object containing the actually overridden properties , e.g. the new twig template extension for this component.

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import template from './extension/sw-product-settings-form/sw-product-settings-form.html.twig';

Shopware.Component.override('sw-product-settings-form', {
    template
});
```

In this case, the `sw-product-settings-form` component is overridden, which reflects the settings form on the product detail page. As mentioned above, the second parameter has to be an object, which includes the actual template extension.

## Adding the custom template [​](#adding-the-custom-template)

Time to create the referenced twig template for your plugin now.

INFO

We're dealing with a [TwigJS](https://github.com/twigjs/twig.js/wiki) template here.

Create a file called `sw-product-settings-form.html.twig` in the following directory: `<plugin root>/src/Resources/app/administration/src/extension/sw-product-settings-form`

INFO

The path starting from 'src' is fully customizable, yet we recommend choosing a pattern like this one.

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/extension/sw-product-settings-form/sw-product-settings-form.html.twig
{% block sw_product_settings_form_content %}
    {% parent %}

    <sw-container columns="repeat(auto-fit, minmax(250px, 1fr))" gap="0px 30px">
        <sw-text-field label="Manufacturer ID" v-model="product.manufacturerId" disabled></sw-text-field>
    </sw-container>
{% endblock %}
```

Basically the twig block `sw_product_settings_form_content` is overridden here. Make sure to have a look at the [Twig documentation about the template inheritance](https://twig.symfony.com/doc/3.x/templates.html#template-inheritance), to understand how blocks in Twig work.

This block contains the whole settings form of the product detail page. In order to add a new input field to it, you need to override the block, call the block's original content (otherwise we'd replace the whole form), and then add your custom input field to it. Also, the input field is "disabled", since it should be readable only. This should result in a new input field with the label 'Manufacturer ID', which then contains the ID of the actually chosen manufacturer.

## Loading the JS files [​](#loading-the-js-files)

As mentioned above, Shopware 6 is looking for a `main.js` file in your plugin. Its contents get minified into a new file named after your plugin and will be moved to the `public` directory of Shopware 6 root directory. Given this plugin would be named "AdministrationNewField", the minified javascript code for this example would be located under `<plugin root>/src/Resources/public/administration/js/administration-new-field.js`, once you run the command following command in your shopware root directory:

INFO

Your plugin has to be activated for this to work.

Make sure to also include that file when publishing your plugin! A copy of this file will then be put into the directory `<shopware root>/public/bundles/administration/newfield/administration/js/administration-new-field.js`.

Your minified javascript file will now be loaded in production environments.

---

## Using base components

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/module-component-management/using-base-components.html

# Using base components [​](#using-base-components)

The Shopware 6 Administration comes with a bunch of tailored Vue components, already accessible in all of your templates via the `component registry`. This guide will show you how you can use Shopware-made components in your templates, if you want to learn more about the `component registry` and how you can register your own components to it have a look at the [corresponding guide](./../module-component-management/add-custom-component.html)

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module. Of course you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/), the framework used in the Administration. However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Finding the base component needed [​](#finding-the-base-component-needed)

All Shopware 6 Administration components can be found in the [Component Library](https://component-library.shopware.com/). There you can see what each of the components does and looks like, it also shows you what props they can work with and which slots they have.

## Using the base component [​](#using-the-base-component)

As mentioned before in the introduction, all components used in the Shopware 6 Administration are first registered to the `component registry`. This `component registry` is just a map of all components, which then get registered to Vue during the `Administrations boot process`. Since all of the components are registered as [global `Vue` components](https://vuejs.org/v2/guide/components-registration.html#Global-Registration), they are accessible in all templates of the Administration.

Using base components in your own Administration templates is rather simple. In the example below we will use the `sw-text-field` in our template, which simply renders a `text` input tag, but also supports some fancy functionality, like inheritance, etc:

html

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/example-component/example.html.twig
<div>
    <sw-text-field />
</div>
```

That's basically it. To continue building beautiful custom components, learn how to write templates and how to include them in your components [here](./../templates-styling/writing-templates.html)

---

