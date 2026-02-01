# Products

*Scraped from Shopware Developer Documentation*

---

## Extensions

**Source:** https://developer.shopware.com/docs/products/extensions/

# Extensions [​](#extensions)

Shopware provides some unique extensions:

* Migration Assistant - An extension that connects the source shop and the target shop to migrate data.
* B2B Suite - The B2B Suite extension equips your store with the most important B2B functions. These include workflows, order lists, budgets, and quick orders.
* B2B Components - B2B components enable you to enhance your shop with essential B2B functionalities.
* Advanced Search - This offers the possibility to customize the search fields.
* Subscriptions - Subscription extension allows you to offer products on a subscription basis.

---

## Commercial

**Source:** https://developer.shopware.com/docs/products/extensions/commercial/

# Commercial [​](#commercial)

The Shopware 6 commercial feature-set comprises myriad features, the sum of which provide additional support for businesses which require extended functionality within the Shopware 6 ecosystem.

## Plugin structure [​](#plugin-structure)

The commercial plugin is structured as a group of nested sub-bundles. [Plugins](./../../../concepts/extensions/plugins-concept.html) concept explains you more about this.

## Setup [​](#setup)

Installation of the commercial plugin does not require special guidance. The installation steps are detailed in our [Plugin Base Guide](./../../../guides/plugins/plugins/plugin-base-guide.html#install-your-plugin).

This plugin contains various features, which are covered in our docs as well.

WARNING

In accordance with a Shopware merchant's active account configuration, features within the plugin will be in *active* or *inactive* (whilst still being installed within the Shopware codebase). Pay close attention to any install information or special conditions for the provided features.

## Licensing [​](#licensing)

On installation, the commercial plugin tries to fetch the license key using the logged-in Shopware Account. If this can't be fetched, the plugin can be installed, but all features are deactivated. If you log into your Shopware Account, you can fetch the license key again using `bin/console commercial:license:update`.

For further debugging you can run the command:

bash

```shiki
bin/console commercial:license:info
```

which will show the current license key, whether it is set, and when it expires.

## Disable Features [​](#disable-features)

INFO

This Feature is available since 6.6.10.0

The commercial plugin consists of multiple features. Since you may not need all the Features included with the plugin, you can specify with the `SHOPWARE_COMMERCIAL_ENABLED_BUNDLES` environment variable all commercial bundles you want to be enabled.

Example environment variable:

text

```shiki
SHOPWARE_COMMERCIAL_ENABLED_BUNDLES=CustomPricing,Subscription
```

You can find all bundle names using this command:

bash

```shiki
./bin/console debug:container --parameter kernel.bundles --format=json
```

---

## SaaS

**Source:** https://developer.shopware.com/docs/products/saas.html

# Cloud [​](#cloud)

With the SaaS platform, Shopware provides updates, hosting, and infrastructure. Also, there are ways to extend it.

The [App system](./../concepts/extensions/apps-concept.html) gives you great freedom to develop extensions for SaaS stores.

---

