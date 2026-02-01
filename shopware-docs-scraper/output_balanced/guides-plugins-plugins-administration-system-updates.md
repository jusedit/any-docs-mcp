# Guides Plugins Plugins Administration System Updates

*Scraped from Shopware Developer Documentation*

---

## Upgrading to Meteor Components

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/meteor-components.html

# Future Development Roadmap: Upgrading to Meteor Components [​](#future-development-roadmap-upgrading-to-meteor-components)

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change. This document serves as a general guideline for our development direction.

## Introduction [​](#introduction)

With the release of Shopware 6.7, we will replace several current administration components with components from the [Meteor Component Library](https://meteor-component-library.vercel.app/).

## Why Meteor Components? [​](#why-meteor-components)

The Meteor Component Library is Shopware's official collection of reusable components used across multiple Shopware projects and built on the Shopware Design System.

Using a shared component library offers several advantages:

* **Consistent Design**: All components follow the Shopware Design System guidelines.
* **Consistent Behavior**: All components share standardized behavior patterns and API conventions.
* **Reusability**: Components can be seamlessly integrated across different projects and apps.
* **Maintenance**: Updates and improvements to components are managed centrally and automatically propagate to all projects using the component library.

## Migration guide [​](#migration-guide)

For each component being replaced, we provide a detailed upgrade guide that explains the migration process from the old component to the new Meteor Component. You can find these guides in the technical upgrade documentation for the release.

## Using Codemods for migration [​](#using-codemods-for-migration)

To simplify the plugin migration process, we provide codemods that automatically replace old components with new Meteor Components.

### Prerequisites [​](#prerequisites)

* A [development installation of Shopware](https://github.com/shopware/shopware) must be installed
* Your plugin must be located in the `custom/plugins` folder

### Running the Migration Tool [​](#running-the-migration-tool)

1. Execute the following composer command:

   bash

   ```shiki
   # Main command which also outputs the help text
   composer run admin:code-mods

   ## Example with arguments
   # composer run admin:code-mods -- --plugin-name example-plugin --fix -v 6.7
   ```
2. Provide your plugin name and target Shopware version for migration
3. The tool will:

   * Automatically replace compatible components with Meteor Components
   * Add guidance comments for components that require manual migration
   * Fixes some other deprecated code where possible

## Supporting Extension Developers [​](#supporting-extension-developers)

To support extension developers and ensure compatibility between Shopware 6.6 and Shopware 6.7, a new prop called `deprecated` has been added to Shopware components.

* **Prop Name**: `deprecated`
* **Default Value**: `false` (uses the new Meteor Components by default)
* **Purpose**:
  + When `deprecated` is set to `true`, the component will render the old (deprecated) version instead of the new Meteor Component.
  + This allows extension developers to maintain a single codebase compatible with both Shopware 6.6 and 6.7 without being forced to immediately migrate to Meteor Components.

Example:

html

```shiki
<!-- Uses mt-button in 6.7 and sw-button-deprecated in 6.6 -->
<template>
  <sw-button />
</template>

<!-- Uses sw-button-deprecated in 6.6 and 6.7 -->
<template>
  <sw-button deprecated />
</template>
```

> **Important:** Although the old components can still be used with the `deprecated` prop, we highly recommend migrating to Meteor Components whenever possible to align with future Shopware development.

---

## Changing from Webpack to Vite

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vite.html

# Future Development Roadmap: Changing from Webpack to Vite [​](#future-development-roadmap-changing-from-webpack-to-vite)

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change. This document serves as a general guideline for our development direction.

## Introduction [​](#introduction)

We are planning substantial changes to the way we build our Vue.js application. The current Webpack build system has been in place for quite some time now, but like everything in tech, it becomes outdated sooner than later. Additionally to Webpack being slow and outdated, we identified a security risk for the future of our application. Many Webpack maintainers have moved on to other projects. Therefore, the Webpack project no longer receives significant updates. The same applies to the Webpack loaders we currently use.

## Introducing Vite [​](#introducing-vite)

The Vue.js ecosystem has built its own bundler: Vite. Vite is fast, easier to configure and the new standard for Vue.js applications. That's why we decided to switch to Vite with Shopware 6.7.

## Consequences for extensions [​](#consequences-for-extensions)

For apps there are no consequences as your build process is already decoupled from Shopware. For plugins you only need to get active if you currently extend the webpack config by providing your own `webpack.config.js` file.

### Migrate the custom webpack config to Vite [​](#migrate-the-custom-webpack-config-to-vite)

If you have a custom webpack config, you need to migrate it to Vite. You need to do the following steps:

1. Create a new config file `vite.config.mts` to your plugin in the `YourApp/src/Resources/app/administration/src` directory. Previously you had a `webpack.config.js` in the following directory: `YourApp/src/Resources/app/administration/build/`
2. Remove the old `webpack.config.js` file
3. Make sure to remove all webpack related dependencies from your `package.json` file
4. Make sure to add the Vite dependencies to your `package.json` file

A basic config migration could look like this:

javascript

```shiki
// Old Webpack config
module.exports = () => {
    return {
        resolve: {
            alias: {
                '@example': 'src/example',
            }
        }
    };
};
```

typescript

```shiki
// New Vite config
import { defineConfig } from 'vite';

export default defineConfig({
    resolve: {
        alias: {
            '@example': 'src/example',
        },
    },
});
```

Of course, this is a very basic example. The Vite config can be much more complex and powerful. You can find more information about the Vite config in the [Vite documentation](https://vite.dev/config/). Depending on your webpack config, the migration can be very individual.

## Implementation details [​](#implementation-details)

In this section we'll document the implementation details of the new Vite setup.

### Feature flag [​](#feature-flag)

The system is already in place and can be tested by activating the feature flag: `ADMIN_VITE`.

### Bundle information [​](#bundle-information)

The information about all active bundles/plugins is written to `<shopwareRoot>/var/plugins.json` by the `Shopware\Core\Framework\Plugin\Command\BundleDumpCommand`. This command can be triggered standalone by running `php bin/console bundle:dump`. It is also part of the composer commands `build:js:admin`, `build:js:storefront`, `watch:admin` and `watch:storefront`. This file is used to load all the Shopware Bundles and custom plugins.

### Building the Shopware Administration [​](#building-the-shopware-administration)

The command responsible for building the Shopware Administration with all extensions remains `composer build:js:admin`.

### Building the core [​](#building-the-core)

The Vite config located under `<shopwareRoot>/src/Administration/Resources/app/administration/vite.config.mts` is only responsible for the core without extensions. Currently there are a few file duplications because Vite requires different module loading order. You can recognize these files, they look like this: `*.vite.ts`. So for example the entry file `<shopwareRoot>/src/Administration/Resources/app/administration/src/index.vite.ts`.

### Building extensions [​](#building-extensions)

The script responsible for building all extensions is located at `<shopwareRoot>/src/Administration/Resources/app/administration/build/plugins.vite.ts`. This script uses the JS API of Vite to build all extensions. As mentioned above, it's still part of the `composer build:js:admin` command and needs no manual execution.

The script will do the following:

1. Get all bundles/plugins from the `<shopwareRoot>/var/plugins.json`
2. Call `build` from Vite for each plugin
3. The `build` function of Vite will automatically load `vite.config` files from the path of the entry file.

### Dev mode/HMR server [​](#dev-mode-hmr-server)

The command responsible for serving the application in dev mode (HMR server) is still `composer watch:admin`. For the core it's just going to take the `vite.config.mts` again and this time the `plugins.vite.ts` script will call `createServer` for each plugin.

### Loading Vite assets [​](#loading-vite-assets)

Once built the right assets need to be loaded somehow into the administration. For the core we use the `pentatrion_vite` Symfony bundle. Loading the correct file(s) based on the `entrypoints.json` file generated by its counterpart `vite-plugin-symfony`. For bundles and plugins the boot process inside the `application.ts` will load and inject the entry files based on the environment.

Production build:

* Information is taken from the `/api/_info/config` call

Dev mode/HMR server:

* Information is served by our own Vite plugin `shopware-vite-plugin-serve-multiple-static` in form of the `sw-plugin-dev.json` file requested by the `application.ts`

## Vite plugins [​](#vite-plugins)

To accomplish all this, we created a few Vite plugins and in this section we'll take the time to explain what they do. All our Vite plugin names are prefixed with `shopware-vite-plugin-`. I'll leave this out of the headlines for better readability.

### asset-path [​](#asset-path)

This plugin manipulates the chunk loading function of Vite, to prepend the `window.__sw__.assetPath` to the chunk path. This is needed for cluster setups, serving the assets from a S3 bucket.

### static-assets [​](#static-assets)

Copies static admin assets from `static` to the output directory so they can get served.

### serve-multiple-static [​](#serve-multiple-static)

Serves static assets in dev mode (HMR server).

### vue-globals [​](#vue-globals)

Replacing all Vue imports in bundles/plugins to destructure from `Shopware.Vue`. This solves the problem of having multiple Vue instances. It does this by creating a temporary file exporting the Shopware.Vue and adding an alias to point every Vue import to that temporary file. This way it will result in bundled code like this:

From this:

vue

```shiki
// From this
<script setup>
import { ref } from 'vue';
</script>

// To this
<script setup>
const { ref } = window['Shopware']['Vue'];
</script>
```

### override-component [​](#override-component)

Registering `*.override.vue` files automatically. It will search for all files matching the override pattern and automatically import them into the bundle/plugin entry file. Additionally, these imports will be registered as override components by calling `Shopware.Component.registerOverrideComponent`. This will make sure that all overrides are loaded at any time as soon as the bundle/plugin script is injected. To learn more about the new overrides take a look at the Vue native docs right next to this file.

### twigjs [​](#twigjs)

Transforming all `*.html.twig` files in a way that they can be loaded by Vite.

## HMR reloading [​](#hmr-reloading)

A quick note on HMR (Hot Module Replacement). Vite is only capable of reloading `*.vue` files. This means that we can only leverage the HMR by the time we transitioned everything to SFC (Single File Components) but once we do the Vite setup will be able to distinguish between changes in a plugin or the core.

## Performance [​](#performance)

Vite is able to build the core Administration in ~18s on my system. This is a saving of over 50% compared to Webpack. In dev mode it's similar but not directly comparable. The Vite dev server starts instantly and moves the loading time to the first request. Webpack on the other hand compiles a long time upfront until the server is ready.

---

## Removing Vue Migration Build

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vue-migration-build.html

# Future Development Roadmap: Removing Vue Migration Build [​](#future-development-roadmap-removing-vue-migration-build)

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change. This document serves as a general guideline for our development direction.

## Introduction [​](#introduction)

Prior to Shopware 6.7, we utilized the Vue migration build to facilitate the transition from Vue 2 to Vue 3 for plugin developers. This approach allowed most public APIs to behave similarly to Vue 2 while enabling gradual migration.

With the release of Shopware 6.7, the Vue migration build will be removed. All plugins must be fully migrated to Vue 3 without relying on the migration build.

## Why remove the Vue migration build? [​](#why-remove-the-vue-migration-build)

The Vue migration build was a temporary solution to help transition from Vue 2 to Vue 3. However, maintaining it indefinitely would introduce complexity, potential performance bottlenecks, and incompatibility with future Vue versions. Removing it ensures that all plugins fully adopt Vue 3, leveraging its improved reactivity system, better TypeScript support, and performance enhancements.

## Migration guide [​](#migration-guide)

Shopware's administration is built using Vue 3, and all plugins should be updated accordingly. We recommend referring to the official [Vue 3 migration guide](https://v3-migration.vuejs.org/) for detailed information on breaking changes and deprecations.

Below are some of the most common changes observed in our codebase. This list is not exhaustive, so always consult the official guide for comprehensive migration steps.

### Common Migration Changes [​](#common-migration-changes)

#### `$listeners` removed [​](#listeners-removed)

In Vue 2, `$listeners` was used to access event listeners passed to a component. In Vue 3, event listeners are now included in `$attrs`.

Before (Vue 2):

vue

```shiki
<template>
    <sw-button v-on="$listeners">Click me</sw-button>
</template>
```

After (Vue 3):

vue

```shiki
<template>
    <sw-button v-bind="$attrs">Click me</sw-button>
</template>
```

More detailed guide about [`$listeners` breaking changes](https://v3-migration.vuejs.org/breaking-changes/listeners-removed.html).

#### `$scopedSlots` removed [​](#scopedslots-removed)

Previously, scoped slots were accessed using `$scopedSlots`. In Vue 3, `$slots` now unifies all slots and exposes them as functions.

Before (Vue 2):

js

```shiki
this.$scopedSlots.header
```

After (Vue 3):

js

```shiki
this.$slots.header()
```

More detailed guide about [`$slots` unification breaking changes](https://v3-migration.vuejs.org/breaking-changes/slots-unification.html).

#### `$children` removed [​](#children-removed)

Vue 2 allowed access to child components using `$children`. In Vue 3, this is no longer supported, and you should use template refs instead.

Before (Vue 2):

js

```shiki
this.$children.childrenMethod();
```

After (Vue 3):

js

```shiki
// <sw-child ref="childrenRef" />

this.$refs.childrenRef.childrenMethod();
```

More detailed guide about [`$children` breaking changes](https://v3-migration.vuejs.org/breaking-changes/children).

#### Some Events API removed [​](#some-events-api-removed)

The methods `$on`, `$off` and `$once` are removed in Vue 3 without a replacement. You can still use `$emit` to trigger event handlers declaratively attached by a parent component.

Alternatively you can use inject/provide to pass down event handlers using a registration pattern.

It is not possible to give a general guide for this change. You need to adjust your code based on your specific use case. Here is an example how you could adjust your code:

Before (Vue 2):

js

```shiki
created() {
  this.$parent.$on('doSomething', this.eventHandler);
},

beforeDestroy() {
  this.$parent.$off('doSomething', this.eventHandler);
}
```

After (Vue 3):

js

```shiki
// The parent component needs to provide the event handler
inject: ['registerDoSomething', 'unregisterDoSomething'],

created() {
  this.registerDoSomething(this.eventHandler);
},

beforeDestroy() {
  this.unregisterDoSomething(this.eventHandler);
}
```

More detailed guide about [Events API breaking changes](https://v3-migration.vuejs.org/breaking-changes/events-api.html).

#### `$set`, `$delete` removed [​](#set-delete-removed)

Vue 2 required `$set` and `$delete` for reactive property modifications. Vue 3’s new reactivity system, based on ES6 Proxies, removes the need for these methods.

Before (Vue 2):

js

```shiki
this.$set(this.myObject, 'key', 'value');
this.$delete(this.myObject, 'key');
```

After (Vue 3):

js

```shiki
this.myObject.key = 'value';
delete this.myObject.key;
```

## Conclusion [​](#conclusion)

With Shopware 6.7, the Vue migration build will be fully removed. To ensure compatibility, all plugins must be updated to Vue 3 following the official migration guide. If you encounter challenges during migration, refer to the official Vue 3 documentation or seek assistance from the Shopware developer community.

---

## Native Vue

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vue-native.html

# Future Development Roadmap: Moving Towards Vue Native [​](#future-development-roadmap-moving-towards-vue-native)

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change. This document serves as a general guideline for our development direction.

## Introduction [​](#introduction)

We are planning a significant shift in our development approach, moving towards a more native Vue.js implementation. This document outlines the reasons for this change and provides an overview of our upgrade path.

## Current status [​](#current-status)

To better understand the changes described in this article, let's recap the current status. The Shopware 6 Administration is built around Vue.js with several custom systems on top to allow for extensions.

### Custom component registration [​](#custom-component-registration)

javascript

```shiki
Shopware.Component.register('sw-component', {
    template,

    //...
});
```

### Custom templates with Twig.Js [​](#custom-templates-with-twig-js)

html

```shiki
{% block sw-component %}
    <sw-card></sw-card>
{% endblock %}
```

## Why Go Native? [​](#why-go-native)

Our transition to a more native Vue.js approach is driven by several key factors:

1. **Improved Developer Experience**

   * Devtool enhancements
   * Easier maintenance
2. **Future-Proofing**

   * Aligning with Vue 3 and potential future versions
   * Preparing for upcoming industry standards
3. **Performance Optimization**

   * Leveraging native Vue.js capabilities for better performance

## Major Changes [​](#major-changes)

### 1. Moving from Options API to Composition API [​](#_1-moving-from-options-api-to-composition-api)

#### Why Make This Change? [​](#why-make-this-change)

We aim to better align with Vue's ecosystem, to minimize the amount of specifications new Developers need to learn. The Composition API has become the new standard for Vue's documentation and projects all over Github. Renowned libraries like `vue-i18n` are dropping support of the Options API, as seen in their [migration guide](https://vue-i18n.intlify.dev/guide/migration/vue3#summary), and we expect similar transitions from other tools in the ecosystem. This also aligns with Vue's best practices, as highlighted in the official [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html#why-composition-api).

#### What Will Change? [​](#what-will-change)

We will gradually transform our components from Options API to Composition API. Together with native blocks, this builds the foundation to use Single File Components (SFC). The transformation will be stretched over multiple major versions to offer enough time for all of us to adapt. Take a look at the estimated timeline below.

#### Upgrade Path [​](#upgrade-path)

| Shopware Version | Options API | Composition API |
| --- | --- | --- |
| 6.7 | Standard | Experimental |
| 6.8 | Still supported for extensions\* | Standard for Core components |
| 6.9 | Removed completely | Standard |

\*Extensions still can register components using the Options API; overwriting Core components needs the Composition API.

### 2. TwigJS to Native Blocks [​](#_2-twigjs-to-native-blocks)

#### Why Make This Change? [​](#why-make-this-change-1)

Vue has no native support for blocks like in Twig.js. Vue has slots, but slots don't work like blocks. Recently, we accomplished the unthinkable and found a way to implement blocks with native Vue components. This will allow us to finally use SFC and keep the extendability of Twig.js. Lowering the learning curve, as the Twig.js syntax is especially unfamiliar to Vue developers. Standard tooling like VSCode, ESLint, and Prettier will work out of the box.

#### What Will Change? [​](#what-will-change-1)

We will gradually transform all component templates from external `*.html.twig` files with Twig.Js into `.vue` files using the native block implementation.

#### Upgrade Path [​](#upgrade-path-1)

| Shopware Version | Twig.Js | Native blocks |
| --- | --- | --- |
| 6.7 | Standard | Experimental |
| 6.8 | Still supported for extensions\* | Standard for Core components |
| 6.9 | Removed completely | Standard |

\*Extensions still can register components using Twig.Js templates; overwriting Core blocks needs the native block implementation.

### 3. Vuex to Pinia [​](#_3-vuex-to-pinia)

#### Why Make This Change? [​](#why-make-this-change-2)

Vuex has been the default State management for Vue 2. For Vue 3 Pinia took it's place.

#### What Will Change? [​](#what-will-change-2)

We will move all core Vuex states to Pinia stores. The public API will change from `Shopware.State` to `Shopware.Store`.

#### Upgrade Path [​](#upgrade-path-2)

| Shopware Version | Vuex | Pinia |
| --- | --- | --- |
| 6.7 | Still supported for extensions\* | Standard for Core components |
| 6.8 | Removed completely | Standard |

\*Extensions still can register Vuex states; Accessing core stores is done via Pinia

## Example: Component Evolution [​](#example-component-evolution)

Now let's take a look how core and extension components will evolve.

### Shopware 6.7 [​](#shopware-6-7)

First we start with the current status which is still compatible with Shopware 6.7.

#### Core component [​](#core-component)

In the core we register a component via `Shopware.Component.register`.

javascript

```shiki
Shopware.Component.register('sw-text-field', {
   template: `
     {% block sw-text-field %}
       <input type=text v-model="value" @change="onChange">
     {% endblock %}
   `,
   
   data() {
       return {
           value: null,
       }
   },
   
   methods: {
       onChange() {
           this.$emit('update:value', this.value);
       }
   },
});
```

#### Extension override [​](#extension-override)

The extension overrides the component via `Shopware.Component.override`.

javascript

```shiki
Shopware.Component.override('sw-text-field', {
   template: `
     {% block sw-text-field %}
       {% parent %}
       
       {{ helpText }}
     {% endblock %}
   `,
   
   props: {
       helpText: {
           type: String,
           required: false,
       }
   }
})
```

#### Extension new component [​](#extension-new-component)

The extension adds additional component via `Shopware.Component.register`.

javascript

```shiki
Shopware.Component.register('your-crazy-ai-field', {
   template: `
     {% block your-crazy-ai-field %}
       {# ... #}
     {% endblock %}
   `,

   // Options API implementation
})
```

### Shopware 6.8 [​](#shopware-6-8)

With Shopware 6.8 the core uses single file components with the composition API.

#### Core component [​](#core-component-1)

The core component is added via a single file component `*.vue` file.

vue

```shiki
<template>
   {# Notice native block comonent instead of twig blocks #}
   <sw-block name="sw-text-field">
    <input type=text v-model="value" @change="onChange">
   </sw-block>
</template>

<script setup>
// Notice Composition API imports
import { ref, defineEmits } from 'vue';

// Notice new extension system Shopware.Component.createExtendableSetup
const {value, onChange, privateExample} = Shopware.Component.createExtendableSetup({
   props,
   context,
   name: 'originalComponent',
}, () => {
   const emit = defineEmits(['update:value']);

   const value = ref(null);
   const onChange = () => {
      emit('update:value', value.value)
   }

   const privateExample = ref('This is a private property');

   return {
      public: {
         value,
         onChange,
      },
      private: {
         privateExample,
      }
   };
});
</script>
```

#### Extension override [​](#extension-override-1)

For overrides we created a new convention. They must match the `*.override.vue` pattern. `*.override.vue` files will be loaded automatically in your main entry file.

vue

```shiki
<template>
{# Notice the native block components #}
<sw-block extends="sw-text-field">
   <sw-block-parent/>
   
   {{ helpText}}
</sw-block>
</template>

<script setup>
// Notice Composition API imports
import { defineProps } from 'vue';

// This file would also use Shopware.Component.overrideComponentSetup
// if it would change the existing public API
const props = defineProps({
   helpText: {
       type: String,
       required: false,
   },
});
</script>
```

#### Extension new component [​](#extension-new-component-1)

javascript

```shiki
// For this you would also have the option to use a `*.vue` file but you don't have to
Shopware.Component.register('your-crazy-ai-field', {
   template: `
     {% block your-crazy-ai-field %}
       {# ... #}
     {% endblock %}
   `,

   // Options API implementation
})
```

### Shopware 6.9 [​](#shopware-6-9)

The only difference for 6.9 is that you can no longer register new components via `Shopware.Component.register`.

## FAQ [​](#faq)

**Will existing extensions built with Options API continue to work in Shopware 6.8?**

When you only use `Shopware.Component.register` yes. If you also use `Shopware.Component.extend/ override` you need to use the composition API extension approach for that.

**How can I prepare my development team for the transition to Composition API?**

I would recommend building a simple Vue application using the Composition API. You can do so by following [official guides](https://vuejs.org/guide/extras/composition-api-faq.html).

**What advantages does the native block implementation offer over the current Twig.js system?**

It works with native Vue.Js components, therefore is compatible with default tooling.

**Can I mix Composition API and Options API components during the transition period?**

Yes as long as you stick to the limitations from the upgrade paths.

**How will the migration from Twig.js templates to .vue files affect my existing component overrides?**

You need to migrate all your overrides with Shopware 6.8.

**What tools or resources will be available to help migrate existing components?**

We'll try to provide a code mod to transition your components into SFC. This will not work for all edge cases, so you need to manually check and transition them.

**Will there be any performance impact during the transition period when both systems are supported?**

During our tests we didn't experience any performance issues.

**How does the new `Shopware.Component.createExtendableSetup` function work with TypeScript?**

It has built in TypeScript support.

**What happens to existing extensions using Twig.js templates after version 6.9?**

They will stop working with Shopware version 6.9.

**Can I start using the native blocks and Composition API in my extensions before version 6.8?**

Yes! You can add new components using SFC and native blocks. But you can't extend core components using the old systems or vise versa.

**Which extensions are affected by these changes?**

* Apps aren't affected at all
* Plugins need to respect the discussed changes

---

## Upgrading to Pinia

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/pinia.html

# Migration from Vuex in Shopware to Pinia [​](#migration-from-vuex-in-shopware-to-pinia)

## Introduction [​](#introduction)

With the release of Shopware 6.7, we will replace Vuex with [Pinia](https://pinia.vuejs.org/) as the state management library for the administration.

## Why Pinia? [​](#why-pinia)

Migrating to Pinia simplifies state management with an intuitive API, no need for mutations, better TypeScript support, and seamless integration with Vue 3 Composition API. It’s lightweight, modular, and offers modern features like devtools support, making it a more efficient alternative to Vuex.

## Migration Guide [​](#migration-guide)

To migrate a Vuex store to Pinia, you need to make some changes to the store definition and how you access it in components.

* First, register it with `Shopware.Store.register` and define the store with `state`, `getters`, and `actions` properties:

**Before (Vuex):**

javascript

```shiki
export default {
    namespaced: true,

    state: {
      // Initial state
      ...
    },
    mutations: {
      ...
    },
    getters: {
       ...
    },
    actions: {
       ...
    },
}
```

**After (Pinia):**

javascript

```shiki
const store = Shopware.Store.register('<storeName>', {
    state: () => ({
        // Initial state
        ...
    }),
    getters: {
       ...
    },
    actions: {
       ...
    },
});
export default store;
```

* You can also register the store with an `id` property in the definition object, for example:

javascript

```shiki
const store = Shopware.Store.register({
    id: '<storeName>',
    state: () => ({
        // Initial state
    }),
    getters: {
       // ...
    },
    actions: {
       // ...
    },
});
```

* If you register a store that already exists, it will be overwritten. You can also unregister a store:

javascript

```shiki
Shopware.Store.unregister('<storeName>');
```

* To register a store from a component or index file, simply import the store file.

**Before (Vuex):**

javascript

```shiki
import productsStore from './state/products.state';

Shopware.State.registerModule('product', productsStore);
```

**After (Pinia):**

javascript

```shiki
import './state/products.state';
```

### Key Changes [​](#key-changes)

#### State [​](#state)

In Pinia, `state` must be a function returning the initial state instead of a static object.

javascript

```shiki
state: () => ({
    productName: '',
})
```

#### Mutations [​](#mutations)

Vuex `mutations` are no longer needed in Pinia, since you can modify state directly in actions or compute it dynamically.

javascript

```shiki
actions: {
    updateProductName(newName) {
        this.productName = newName; // Directly update state
    },
},
```

#### Getters [​](#getters)

* There cannot be getters with the same name as a property in the state, as both are exposed at the same level in the store.
* Getters should be used to compute and return information based on state, without modifying it.

#### TypeScript [​](#typescript)

We recommend migrating JavaScript stores to TypeScript for stricter typing, better autocompletion, and fewer errors during development.

typescript

```shiki
const store = Shopware.Store.register({
  id: 'myStore',
  ...
});

export type StoreType = ReturnType<typeof store>;
```

Then, you can use this type to extend `PiniaRootState`:

typescript

```shiki
import type { StoreType } from './store/myStore';

declare global {
    interface PiniaRootState {
        myStore: StoreType;
    }
}
```

### Composables as a Store [​](#composables-as-a-store)

With Pinia, you can use reactive properties inside a store and define it like a composable. Keep in mind that only variables and functions returned from the store will be tracked by Pinia in devtools.

typescript

```shiki
const store = Shopware.Store.register('<storeName>', function() {
  const count = ref(0);

  const doubled = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, doubled, increment, decrement };
});
```

You can also use a composable function defined outside the store. This allows you to encapsulate and reuse logic across different stores or components, promoting better code organization and modularity:

typescript

```shiki
// composables/myComposable.ts
export function useMyComposable() {
  const count = ref(0);

  const doubled = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, doubled, increment, decrement };
}
```

typescript

```shiki
// store/myStore.ts
import { useMyComposable } from '../composables/myComposable';

const store = Shopware.Store.register('myStore', useMyComposable);
```

### Accessing the Store [​](#accessing-the-store)

To access the store in Vuex, you would typically do:

javascript

```shiki
Shopware.State.get('<storeName>');
```

When migrating to Pinia, it changes to:

javascript

```shiki
Shopware.Store.get('<storeName>');
```

### Testing [​](#testing)

To test your store, just import it so it's registered. You can use `$reset()` to reset the store before each test:

javascript

```shiki
import './store/my.store';

describe('my store', () => {
  const store = Shopware.Store.get('myStore');

  beforeEach(() => {
    store.$reset();
  });

  it('has initial state', () => {
    expect(store.count).toBe(0);
  });
});
```

When testing components that use Pinia stores, register Pinia as a plugin and reset it before each test:

javascript

```shiki
import { createPinia, setActivePinia } from 'pinia';

const pinia = createPinia();

describe('my component', () => {
  beforeEach(() => {
    setActivePinia(pinia);
  });

  it('is a component', async () => {
    const wrapper = mount(await wrapTestComponent('myComponent', { sync: true }), {
      global: {
        plugins: [pinia],
        stubs: {
          // ...
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });
});
```

---

