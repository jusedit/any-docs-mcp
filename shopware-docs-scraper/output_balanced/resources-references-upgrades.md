# Resources References Upgrades

*Scraped from Shopware Developer Documentation*

---

## Upgrades and Migrations

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/

# Upgrades and Migrations [​](#upgrades-and-migrations)

Software projects typically undergo changes and upgrades, for Shopware this is not different. This section provides you with comprehensive update guides for specific technical changes.

---

## Administration

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/administration/

# Administration [​](#administration)

This section contains all upgrade guides related to the Shopware Administration.

---

## Vue 3 upgrade

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/administration/vue3.html

# Vue 3 upgrade [​](#vue-3-upgrade)

## Introduction [​](#introduction)

The Shopware administration uses Vue.js `2`, which will reach its end of life (EOL) **on December 31st 2023**. To deliver up-to-date and maintainable software, the administration will use Vue.js `3` from Shopware version `6.6` and upwards. If you are unfamiliar with the changes from Vue.js `2` to Vue.js `3`, please refer to this [official guide](https://v3-migration.vuejs.org/).

## FAQ [​](#faq)

Let's start with some frequently asked questions. These will also help you figure out if this upgrade affects you.

### Which extensions are affected by the Vue 3 upgrade? [​](#which-extensions-are-affected-by-the-vue-3-upgrade)

App-based extensions aren't affected by these changes. However, if your extension is plugin-based and contains custom administration code, you likely need to do some refactoring.

### Are there any breaking changes I should be aware of? [​](#are-there-any-breaking-changes-i-should-be-aware-of)

Yes, Vue 3 introduced breaking changes. It's crucial to review the migration guide provided by Vue.js and this document for detailed information.

### What steps should I follow to upgrade my Shopware plugin to Vue 3? [​](#what-steps-should-i-follow-to-upgrade-my-shopware-plugin-to-vue-3)

Typically, the process involves updating your project dependencies and modifying your code to adhere to Vue 3's API changes. Consult the Vue 3 documentation and this document's step-by-step instructions.

### Can one plugin version be compatible with Shopware 6.5 and 6.6? [​](#can-one-plugin-version-be-compatible-with-shopware-6-5-and-6-6)

No, your plugin requires a new version in the Store. For instance, version `1.x` is for Shopware `6.5.x`, while version `2.0` is compatible with Shopware `6.6` and newer.

### How can I check if my Shopware extension is compatible with Vue 3? [​](#how-can-i-check-if-my-shopware-extension-is-compatible-with-vue-3)

You can verify compatibility by reviewing the extension's functionality and updating test suites according to this document.

### Do I need to rewrite my extension to upgrade to Vue 3? [​](#do-i-need-to-rewrite-my-extension-to-upgrade-to-vue-3)

While some changes are required, a complete rewrite is not necessary. The amount of effort is dictated by your use of Vue's internal API.

### Are tools or libraries available to facilitate the migration to Vue 3? [​](#are-tools-or-libraries-available-to-facilitate-the-migration-to-vue-3)

Yes, there are tools and migration helpers that can automate certain aspects of the upgrade process. You could start by enabling the Vue 3 rule set of `eslint`.

### Where can I find support and community discussions about updating Shopware plugin to Vue 3? [​](#where-can-i-find-support-and-community-discussions-about-updating-shopware-plugin-to-vue-3)

You can participate in discussions and seek help on the Shopware community Discord. There is a dedicated channel for this topic called `#shopware-development`.

## External resources [​](#external-resources)

Here is a handpicked selection of external resources. This list provides a handy reference, granting you access to all the essential materials you might need.

* [Vue 3 migration guide](https://v3-migration.vuejs.org)
* [Vue 3 breaking changes](https://v3-migration.vuejs.org/breaking-changes/)
* [Vue router migration guide](https://router.vuejs.org/guide/migration/)
* [Vue test utils migration guide](https://test-utils.vuejs.org/migration/)

## Step-by-step guide [​](#step-by-step-guide)

To follow along, you should have the following:

* the latest Shopware `trunk` or an official release candidate
* installed and activated your plugin
* a running administration watcher (`composer run watch:admin`)

### Update your plugin npm dependencies [​](#update-your-plugin-npm-dependencies)

Make sure to align your `package.json` dependencies with the [administration](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/package.json).

### Check your templates [​](#check-your-templates)

For your templates to work correctly, perform the following in no specific order:

* Replace all `sw-field` usages with the corresponding [components](https://github.com/shopware/shopware/blob/6.5.x/src/Administration/Resources/app/administration/src/app/component/form/sw-field/index.js#L16).
* [Check all v-models](https://v3-migration.vuejs.org/breaking-changes/v-model.html)
* [Check event listeners](https://v3-migration.vuejs.org/breaking-changes/v-model.html#_3-x-syntax)
* [Check for deprecated slot syntax](https://eslint.vuejs.org/rules/no-deprecated-slot-attribute.html)
* [Check router-view transition combinations](https://router.vuejs.org/guide/migration/#-router-view-keep-alive-and-transition-)
* [Check your key attributes](https://v3-migration.vuejs.org/breaking-changes/key-attribute.html)
* [Check for filter usages](https://v3-migration.vuejs.org/breaking-changes/filters.html)

### Check your code [​](#check-your-code)

Most of your code should be unaffected by the upgrade. You can start by searching for `this.$`. The usage of `this.$` is an indicator of Vue's internal API. These calls are very likely to break except for `this.$tc`.

If you have a lot of Vue internal API calls, check out the [Known issues section](#known-issues). The best way to find errors is to test your application thoroughly, either by hand or automated.

## Known issues [​](#known-issues)

### Lifecycle hooks [​](#lifecycle-hooks)

Lifecycle hooks such as `@hook:mounted` may be triggered multiple times if the component is loaded asynchronously. Vue 3 will emit the hook for the `AsyncComponentWrapper` and the underlying component. You can only use those hooks if your code allows to be executed multiple times.

### Using slots programmatically [​](#using-slots-programmatically)

It is no longer sufficient to check if `this.$slots` has a property with the slot name to see if that slot exists. Instead, you must verify if your `slotName` contains an actual `v-node`.

### this.$parent [​](#this-parent)

`this.$parent` is prone to errors because Vue 3 wraps the `AsyncWrapperComponent` around asynchronous components. Leading to the virtual dom tree to differ from Vue 2 to Vue 3. Where in Vue 2, a `this.$parent` call was successful, in Vue 3, a `this.$parent.$parent` may be necessary. Try to avoid `this.$parent` communication wherever possible as this is an anti pattern. Use services or event communication instead.

### Vue dev tools performance [​](#vue-dev-tools-performance)

Vue dev tools causes massive performance issues with huge Vue 3 applications. There is an open [issue on Github](https://github.com/vuejs/devtools-v6/issues/1875) with next to no activity from the maintainers.

### v-model changes [​](#v-model-changes)

`v-model` has several breaking changes. Please consider the official [guide](https://v3-migration.vuejs.org/breaking-changes/v-model.html)

### vuex reactivity [​](#vuex-reactivity)

Vuex stores lose reactivity if one or more getters alter state data. For more context, see [here](https://vuejs.org/guide/essentials/reactivity-fundamentals.html#reactivity-fundamentals).

### Form field id's [​](#form-field-id-s)

Fields in the administration no longer have the previous ID almost exclusively used in tests. To fix any failing test, add the `name` attribute to your field with a unique identifier.

### Prop default [​](#prop-default)

Prop default functions no longer have access to the component's `this` scope. You can no longer call `this.$tc` in default functions. Use `Shopware.Snippet.tc` instead.

### Mutating props [​](#mutating-props)

This is an antipattern also for Vue 2. In Vue 2, however, those mutations were not always detected. In Vue 3, this will fail with hard errors. Take a look at this [example](https://eslint.vuejs.org/rules/no-mutating-props.html) to get a basic understanding of how to avoid mutating props directly.

## Conclusion [​](#conclusion)

This document emphasizes the crucial need to upgrade your Shopware extensions to Vue.js 3 as Vue.js 2 reaches its end of life on December 31st 2023. Here's a concise recap of the key points:

* **Transition to Vue 3**: Shopware will adopt Vue.js 3 from version 6.6 onwards.
* **FAQ**: Addressing frequently asked questions:
  + **Extension Compatibility**: Plugin-based extensions with custom administration code are primarily affected. App-based extensions remain unaffected.
  + **Breaking Changes**: Vue 3 introduces significant modifications, necessitating review through the Vue.js migration guide.
  + **Migration Steps**: Adapting your Shopware plugin to Vue 3 involves aligning dependencies and adhering to Vue 3's API changes, following the Vue 3 documentation.
* **Dual Compatibility**: For plugins serving both Shopware 6.5 and 6.6, separate versions are required.
* **Support**: Find support in the Shopware community Discord channel #shopware-development.

---

## Core

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/core/

# Core upgrade and migration guides [​](#core-upgrade-and-migration-guides)

This section contains all upgrade and migration guides related to the Shopware Core.

---

## Translation

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/core/translation/

# Update And Migration Guides For Translations In The Shopware Core [​](#update-and-migration-guides-for-translations-in-the-shopware-core)

This section contains all upgrade and migration guides related to translations in the Shopware Core.

---

## Language Pack Migration

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/core/translation/language-pack-migration.html

# Migration Guide: Language Pack Plugin → Integrated Translation Handling [​](#migration-guide-language-pack-plugin-→-integrated-translation-handling)

Starting with Shopware **6.7.3.0**, translations are managed directly in Shopware. From **6.8.0.0**, the [Language Pack plugin](https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html) will no longer be compatible. Follow this guide to migrate safely.

## What changes [​](#what-changes)

* **From Shopware 6.7.3.0 onward**

  + Translations can be installed via Shopware itself, the [Language Pack plugin](https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html) is not required to fetch the newest [Shopware translations](https://translate.shopware.com).
  + A new CLI command is available:

bash

```shiki
  bin/console translation:install --locales it-IT
```

* The [Language Pack plugin](https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html) still works but is not recommended.
* Languages now have an active flag which can be toggled in the Administration under `Settings → Languages`
* Languages installed/managed from other sources do not need to register their locales in the admin anymore.
* **Other translation plugins or snippets in themes are not affected and can still be used alongside the integrated handling.**
* **Shopware 6.8.0.0 and later**

  + The [Language Pack plugin](https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html) is **not compatible**.
    - The [integrated language handling](./../../../../../concepts/translations/built-in-translation-system.html) should be used to fetch the newest [Shopware translations](https://translate.shopware.com).
  + **Other translation plugins or snippets in themes are not affected and can still be used alongside the integrated handling.**

## Migration paths [​](#migration-paths)

### 1. You are **not using the Language Pack plugin** [​](#_1-you-are-not-using-the-language-pack-plugin)

* Nothing changes.
* To install additional languages, use the CLI command:

bash

```shiki
  bin/console translation:install --locales <locale-code>
```

Example: `bin/console translation:install --locales it-IT,fr-FR` will install Italian and French.

### 2. You are **currently using the Language Pack plugin** [​](#_2-you-are-currently-using-the-language-pack-plugin)

1. Run the translation command and install every language you are using in your shop

   bash

   ```shiki
     bin/console translation:install --locales <locale-code>,<locale-code>
   ```
2. The command uses the **same source ([translate.shopware.com](https://translate.shopware.com))** as the [Language Pack plugin](https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html) but is updated more frequently. So it's essentially identical – or even more up to date!
3. You can safely uninstall and remove the Language Pack plugin. Your **custom snippets** created in the Snippet module remain intact since they are saved in the database.
4. Make sure that all languages you need are **active** in the Administration: `Settings → Languages`

## New installations [​](#new-installations)

* During a fresh Shopware installation, you can select desired languages directly in the installer. They will be downloaded and installed automatically.
* No additional language plugin is required.

## More information [​](#more-information)

* Additional details about the new translation handling are available in the [integrated language handling](./../../../../../concepts/translations/built-in-translation-system.html) guide.

---

## Migrating Extensions

**Source:** https://developer.shopware.com/docs/resources/references/upgrades/core/translation/extension-translation.html

# Migrating Extension Translations to the Country-Independent Snippet Layer [​](#migrating-extension-translations-to-the-country-independent-snippet-layer)

Starting with **Shopware 6.7.3**, a new country-independent snippet layer has been introduced to reduce duplicate translations across similar language variants (e.g., `en-GB`, `en-US`, `en-CA` can share a common "en" base layer).

This change implements a hierarchical fallback system that automatically resolves translations through multiple layers, significantly reducing maintenance overhead for extension developers.

## How the New System Works [​](#how-the-new-system-works)

The snippet loading system now follows this resolution order:

1. **Country-specific layer** (e.g., `en-GB`, `de-DE`) — Highest priority
2. **Language base layer** (e.g., `en`, `de`, `es`) **NEW fallback layer**
3. **British English fallback** (`en-GB`) - Legacy fallback to maximize compatibility
4. **Default fallback** (`en`) - Last resort

When a translation key is requested, Shopware will:

* First check the specific country variant (e.g., `es-AR`)
* If not found, check the base language (e.g., `es`)
* If not found, the legacy fallback will be checked (`en-GB`)
* Finally, fall back to `en` if still not found

**Result**: ~90% reduction in duplicate translations while maintaining full functionality.

## Migrating Your Extensions [​](#migrating-your-extensions)

### Automatic [​](#automatic)

Shipping with Shopware **6.7.3**, there's the command line tool `bin/console translation:lint-filenames` that can be used to check the translation files, or use the `--fix` parameter to even automate the migration process. For more information, see [this migration article](./../../../../../concepts/translations/fallback-language-selection.html#migration-and-linting-via-command).

### Manual [​](#manual)

#### Step 1: Rename your existing files [​](#step-1-rename-your-existing-files)

Rename your existing files from country-specific naming to the language base layer naming.

Generic

```shiki
├── messages.en-GB.base.json ⇒ messages.en.base.json
├── messages.de-DE.base.json ⇒ messages.de.base.json
├── messages.fr-FR.base.json ⇒ messages.fr.base.json
└···
```

#### Step 2: Re-create empty country-specific files [​](#step-2-re-create-empty-country-specific-files)

Re-create empty files with the former names of the country-specific naming.

Generic

```shiki
├── messages.en-GB.base.json
├── messages.de-DE.base.json
├── messages.fr-FR.base.json
└···
```

#### Step 3: Remove duplicates from other country-specific files [​](#step-3-remove-duplicates-from-other-country-specific-files)

Check for duplicate translations across country-specific files and remove them from the country-specific layer.

Here are some example locales that are a dialect to the generic base layer.

Generic

```shiki
├── messages.en-US.base.json (dialect of en-GB with the en base layer)
├── messages.en-IN.base.json (dialect of en-GB with the en base layer)
├── messages.de-AT.base.json (dialect of de-DE with the de base layer)
├── messages.de-CH.base.json (dialect of de-DE with the de base layer)
├── messages.pt-BR.base.json (dialect of pt-PT with the pt base layer)
└···
```

For more details on selecting a fallback language and structuring your snippet files, see the [Fallback Languages guide](./../../../../../concepts/translations/fallback-language-selection.html).

## Testing Your Migration [​](#testing-your-migration)

After the snippet files have been renamed, changing the locale to one of the empty snippet sets should still provide all translated strings. Changing to a country-specific locale should also provide all translated strings with just country-specific terms being replaced.

## Best Practices [​](#best-practices)

### 1. Maintain Backward Compatibility [​](#_1-maintain-backward-compatibility)

Keep existing country-specific files during transition to ensure compatibility with older Shopware versions that don't support the base layer.

## Troubleshooting [​](#troubleshooting)

### Common Migration Issues [​](#common-migration-issues)

#### 1. Translations Not Found After Migration [​](#_1-translations-not-found-after-migration)

**Symptoms**: Missing translations in frontend/backend after restructuring **Solution**:

bash

```shiki
bin/console cache:clear
bin/console snippet:validate
```

---

