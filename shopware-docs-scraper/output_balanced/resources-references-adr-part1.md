# Resources References Adr Part1

*Scraped from Shopware Developer Documentation*

---

## Implement architecture decision records

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html

# Implement architecture decision records [​](#implement-architecture-decision-records)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-06-25-implement-architecture-decision-records.md)

## Context [​](#context)

We should document architecture and technical decisions for the shopware platform. The documentation should be easy to understand and easy to follow. The workflow for new decisions should add to our existing workflows and should not block the whole development process. One solution could be the form of architecture decision records (ADR) as described in the following articles:

* [Documenting Architecture Decisions](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
* [A Simple but Powerful Tool to Record Your Architectural Decisions](https://medium.com/better-programming/here-is-a-simple-yet-powerful-tool-to-record-your-architectural-decisions-5fb31367a7da)

## Decision [​](#decision)

We will record architecture decisions (ADR) in markdown files directly in the platform repository. The workflow for ADRs will be integrated in the existing merge request workflow. This has the following advantages:

* Decision records are an integral part of the development process
* Decisions remain in sync with the code itself
* The Git history is also the decision history
* Decisions are public available and accessible for every developer
* Also external developers can add new ADRs via GitHub pull requests
* Decision finding can be asynchronous via comments in the corresponding merge request

## Consequences [​](#consequences)

From now on, every architecture decision, affecting the shopware platform or one of its components, has to be recorded in an ADR, following the described workflow.

In the following you find answers to the most important questions about ADRs and the new workflow:

**Who can/must create ADRs?**  
 Every developer working with shopware platform!

**When do you have to create an ADR?**  
 Have you made a significant decision that impacts how developers should write code in the shopware platform? Write an ADR! Here are some cases, which can help you to understand when to write an ADR:

* Introducing new standards
* Large code changes which have a huge impact on the software
* Smaller changes, but which are used very often and would lead to duplicated efforts

If you want a more detailed explanation, we recommend the article "[When should I write an Architecture Decision Record](https://engineering.atspotify.com/2020/04/14/when-should-i-write-an-architecture-decision-record/)".

**How can you create new ADRs?**  
 The ADRs are markdown files inside the platform repository, located in the "adr" directory in the root of the repository. So new ADRs can simply be created via merge requests. The merge request is also the approval process for the ADR. Along with the ADR, all necessary code changes have to be added to the merge request, which are needed to implement the new decision. Add the "ADR" label to your merge request, so everyone can identify merge requests containing an ADR.

**How many people have to approve an ADR?**

* Two additional developers have to review the ADR
  + One developer must be a member of the core development team
  + One developer must be a member of a team, other than the team of the creator
* One product owner or higher role has to approve an ADR \*\* This part of the decision is superseded by [2021-11-05 - Adjust ADR approval rules for the new org structure](./2021-11-05-adjust-adr-approval-rules.html), but the rest of this ADR is untouched.\*\*

**Should counter decisions also be documented?**  
 Not specific, but if there is more than one possible solution, all options should be outlined.

**How does an ADR look like?**  
 You can use this first ADR as an orientation. The filename of the ADR should contain the date and a meaningful title. The content of the ADR should always use the following template:

```shiki
# [Date] - [Title]
## Context
## Decision
## Consequences
```

**Which status can an ADR have?**  
 The status of an ADR is symbolized by the directory. All ADR located in the main `/adr` directory are "accepted" and represent the current decision state of the software. The approval process is done via the merge request. When a new decision outdoes an older decision, the old decision has to be moved to the `/adr/_superseded` directory and a link to the new ADR has to be added.

**Can an ADR be changed?**  
 When an ADR is accepted and merged in to the code, it can no longer be changed. If a decision is outdated or has to be changed, the ADR has to be superseded by a new ADR. Superseded ADRs have to be moved to the `/adr/_superseded` directory.

---

## Get control of association clone behavior as developer

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-07-02-control-clone-behavior.html

# Get control of association clone behavior as developer [​](#get-control-of-association-clone-behavior-as-developer)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-07-02-control-clone-behavior.md)

## Context [​](#context)

The developer should be able to define, if an association has to be considered or skipped during the cloning of an entity.

## Decision [​](#decision)

The current clone behavior is controlled by the `Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\CascadeDelete` flag. All associations which are marked with this flag are considered in the clone process. We will add an optional parameter to the flag constructor to disable this behavior.

I already added this flag to the following associations:

* `product.productReviews`
  + This association is already overwritten by the administration
* `product.searchKeywords`
  + Will be indexed by the product indexer, so we can skip this association in the clone process
* `product.categoriesRo`
  + Will be indexed by the product indexer, so we can skip this association in the clone process

An example looks like the following:

```shiki
(new OneToManyAssociationField('searchKeywords', ProductSearchKeywordDefinition::class, 'product_id'))
    ->addFlags(new CascadeDelete(false)),
```

## Consequences [​](#consequences)

After 6.3 released, the developer can control this behavior by setting `\Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\CascadeDelete::$cloneRelevant` to false

---

## Implement sales channel context token requirement for store-api and sales-channel-api

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-07-02-implement-sales-channel-context-token-requirement.html

# Implement sales channel context token requirement for store-api and sales-channel-api [​](#implement-sales-channel-context-token-requirement-for-store-api-and-sales-channel-api)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-07-02-implement-sales-channel-context-token-requirement.md)

## Context [​](#context)

Some routes for the sales-channel-api and the store-api depend on a sales-channel-context-token to identify the correct context. To ensure these routes cannot be called accidentally or intentionally without a token, a route parameter is in need to distinguish open routes and those that need a token.

## Decision [​](#decision)

Every route that depends on a sales-channel-token will only be callable with such a token provided. To decide whether a route depends on a token or not the following questions should help:

* Will the automatic generation of the token be a security Issue?
* Will the automatic generation of the token lead to an abandoned entity? (e.g. the cart)
* Can every possible caller create or know the needed token beforehand? (e.g. the asynchronous payment provider cannot)

## Consequences [​](#consequences)

From now on, every sales-channel-api and store-api route need to be checked for above question and set the `ContextTokenRequired` annotation (`Shopware\Core\Framework\Routing\Annotation\ContextTokenRequired`).

## Counter decisions [​](#counter-decisions)

Another decision could be to just leave the routes open. There is currently no security issue associated with context-less calls. When a call is made without a sales-channel-token, one will be generated with the default sales-channel-context. The least thing that could happen, is that someone adds an entity (e.g. a cart or a customer) accidentally to the default sales-channel-context instead of a desired custom sales-channel-context.

---

## Document template refactoring

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-12-document-template-refactoring.html

# Document template refactoring [​](#document-template-refactoring)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-12-document-template-refactoring.md)

## Context [​](#context)

Our document templates did not support nested line items. To make this possible, we had to split the document templates into smaller templates. This was necessary, because the logic of how the document is rendered has changed a lot. Previously it worked with a simple loop over the line items, now they are rendered recursively.

In the previous implementation was only one `base.html.twig`, which contained all the template logic. Depending on the document type, there were different templates with smaller overrides: `invoice.html.twig`, `delivery_note.html.twig`. In these specific templates only one or two blocks for headline or other addresses were overwritten.

After refactoring, however, this was no longer possible because the different blocks were moved to different files. There are now two ways how we make the overwrite possible again:

1. set a block around each include and then overwrite the includes in the corresponding templates and include a separate template

* **base.html.twig**

twig

```shiki
{% block include_header %}
    {% sw_include '@Framework/documents/header.html.twig' %}
{% endblock %}
```

* **invoice.html.twig**

twig

```shiki
{% sw_extends '@Framework/documents/base.html.twig' %}

{% block include_header %}
    {% sw_include '@Framework/documents/invoice_header.html.twig' %}
{% endblock %}
```

**Disadvantage**: To exchange a block (depending on the document type), you must first overwrite `base.html.twig`. Then you have to overwrite the corresponding `include` to include another file there `invoice_header.html.twig`. The templates are only included in several places, so for some blocks you have to overwrite several includes. In addition to this, serious errors can occur here if several developers want to overwrite an include. Inheritance would not work because one plugin has its `invoice_footer.html.twig` included and the other plugin has another.

**Advantage**: A developer can still overwrite any template defined by us via `sw_extends`

2. We use the `use` syntax of Twig, which allows to overwrite the blocks of included files

twig

```shiki
{% block include_header %}
    {% sw_include '@Framework/documents/header.html.twig' %}
{% endblock %}
```

* `invoice.html.twig`

twig

```shiki
{% sw_extends '@Framework/documents/base.html.twig' %}

{% block headline %}
    <h1>invoice</h1>
{% endblock %}
```

**Disadvantage** Templates that are rendered per `use` cannot be inherited. This logic is different from the previous storefront template logic and must be clearly documented.

**Advantage** A developer can simply overwrite the `base.html.twig` and directly extend and restructure all blocks. This would even correspond to the current behavior. Furthermore, the developer can make document type specific customizations in a simple `invoice.html.twig` without having to overwrite all the `includes`. If several developers want to overwrite a block, they can't get in each other's way through the different includes.

## Decision [​](#decision)

To keep the extensibility of the document templates simple, we will work with the `use` and `block` pattern from Twig:

* <https://twig.symfony.com/doc/3.x/tags/use.html>
* <https://twig.symfony.com/doc/3.x/functions/block.html>

```shiki
{% use '@Framework/documents/includes/logo.html.twig' %}

{{ block('logo') }}
```

## Consequences [​](#consequences)

* Templates from the folder `/shopware/src/Core/Framework/Resources/views/documents/includes` cannot be extended by the developers via `sw_extends`
* We wrote a new how-to guide, which explains the new behavior
* We have placed a note/comment in the corresponding templates which points out the new behavior.

---

## Implement app system inside platform

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-12-implement-app-system-inside-platform.html

# Implement app system inside platform [​](#implement-app-system-inside-platform)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-12-implement-app-system-inside-platform.md)

## Context [​](#context)

We need a different extension mechanism besides the well known plugins, that works in cloud and on-prem environments in the same way. That's why we envisioned the app system, currently publicly available as a [plugin](https://github.com/shopware/app-system). We were able to quickly develop the app system, gather feedback and iterate over ideas without being bound to the strict release workflow of the shopware platform. That was the reason why we started working on the app system as a plugin in the first place.

Now as the app system matured, it is time to integrate the app system back into the platform. This has the following benefits:

* It sends the signal to partners and potential app manufacturers that the app system is stable
* Partners / app manufacturers can rely on the shopware 6 release cycle and the according upgrade process
* Users don't need to install an extra plugin in order to use apps

### App system concept [​](#app-system-concept)

The app system is designed to run in a multi tenant SaaS system as well as on premise systems. Because of that it has some limitations and some new extension points compared to the plugin system. An app consists of a manifest file, containing meta data about the app, for example what extension points the app uses, etc. and optionally storefront customizations (templates, JS, CSS, snippets, theme configuration).

#### App system limitations [​](#app-system-limitations)

* No PHP code execution: PHP code execution cannot be allowed in a multi tenant system due to security reasons, as we cannot trust third party code, because of that we cannot run third party code on the shopware servers. In the app system third party backend code has to run on third party servers, that communicate over the api with the shopware server.
* No general JS administration extensions: Extending the administration through custom JS like plugins cannot be allowed due to security reasons, too. This is mainly due to the fact that the apps JS code should not run in the context of the systems current user and with his/her permissions (as administration extensions from plugins do), but in the context of the app with only the permissions that app was granted. For this reason custom extension points are created (specifically Action-Buttons and Custom Modules), to allow extending the administration without running JS in the context of the JS administration application.
* Nothing that requires constant file access: In a cloud environment it is not possible to store individual (meaning per tenant) files directly on the local filesystem of the servers. It is possible though to store that information on more distant storages like S3, but that has whole different performance characteristics than storing files on disk. Because of that it is not possible to allow constant file access (meaning reading files on every request for example). That's the reason why the metadata associated with apps (the content of the manifest files) and the template changes are stored in the database of the shop. Additionally, the storefront theme files (JS and CSS) only need to be accessed during theme compilation, after that they are directly served from the CDN, so no constant access to the source files is required.

#### App system extension points [​](#app-system-extension-points)

* [Webhook](https://docs.shopware.com/en/shopware-platform-dev-en/app-system-guide/app-base-guide?category=shopware-platform-dev-en/app-system-guide#webhooks): An app can register to webhooks to be notified on a predefined URL if some events happen inside shopware.
* [Action-Button](https://docs.shopware.com/en/shopware-platform-dev-en/app-system-guide/app-base-guide?category=shopware-platform-dev-en/app-system-guide#buttons): An app can display extra buttons on selected detail & listing pages inside the administration and can perform custom actions for the selected entities.
* [Custom Modules](https://docs.shopware.com/en/shopware-platform-dev-en/app-system-guide/app-base-guide?category=shopware-platform-dev-en/app-system-guide#create-own-module): An app can display it's own UI inside the administration. This is done via iFrames that are embedded in the administration.
* [Custom Fields](https://docs.shopware.com/en/shopware-platform-dev-en/app-system-guide/app-base-guide?category=shopware-platform-dev-en/app-system-guide#custom-fields): An app can register it's own custom fields sets, that are displayed along the other custom fields inside the administration.
* [Storefront Customizations](/docs/guides/plugins/apps/storefront/): An app should be able to customize the storefront in the same way a plugin does. This includes the theme system, custom twig templates and custom JS and CSS. In regard to the theme system apps are treated the same way as plugins are, especially regarding the theme inheritance. Apps can be explicitly set in the inheritance chain via `@TechnicalAppName`, if they are not referenced directly they are part of the fallback `@Plugins` namespace.

Extension points may be added as new features of the app system, but we have to make sure that it does not violate one of the limitations mentioned above. Additionally, it needs to be taken into account that it's possible to deploy and run that feature in the cloud environment.

## Decision [​](#decision)

We will migrate the existing app system from the [plugin](https://github.com/shopware/app-system) into the platform. The app system will be part of the core bundle, analogous to the plugin system. It will be moved to the `Shopware\Core\Framework\App` namespace.

### Migration process [​](#migration-process)

We will try to split up the migration into multiple MRs to ensure that code reviews can be made with the needed care. Therefore, the migration is split in multiple coherent parts that build on each other. Where necessary the changes will be hidden behind a feature flag, so the changes are invisible to the user until the migration process is completely finished. In practice the need for feature flags can be minimized, because the app system currently does not come with an administrative UI and is only usable by CLI. By ensuring that we migrate the CLI commands to install and activate apps as the last step of the migration process we can make sure the changes we made previously don't have any visible effect without the need to use feature flags.

We will release a v0.2.0 of the app system before starting the migration. The app-system will be migrated with that feature set to the platform, and at that point new development in the plugin is stopped and will continue inside the platform after the migration is completed. Apps that work with v0.2.0 of the app system plugin will work in the same way with the app system inside the platform, that means during the migration we won't introduce any breaking changes from the point of view of an app developer. For a plugin developer, who extended the app system itself, this migration will likely be a breaking change, as we will change the internal structure of the app system (e.g. change PHP class names, name spaces, entity names, etc.).

After the migration process is finished we will release a v0.3.0 of the app system plugin. The sole purpose for this update is to migrate the app data from the old plugin data structures to the new platform data structures and make sure that apps that were previously installed (with the app system plugin) continue to work (with the app system in platform). This means that shops on a shopware version prior to the version, in which we will release the app system as part of the platform, can use the app system plugin in v0.2.0 to already use the app system in their shops. Shops that are already on the version where the app system is included as part of the platform can start right away using apps and don't need the plugin. For shops that used apps with the app system plugin and then update to a platform version where the app system is included, need to update the app system plugin to v0.3.0 right after upgrading the platform version, so that the already installed apps continue to work, after that the plugin can safely be deleted and is not necessary anymore.

## Consequences [​](#consequences)

As a consequence the app system is considered stable after the migration process is completed. That means we won't introduce any changes that may break existing apps in minor (6.3.x) or patch (6.3.0.x) versions. This especially includes the following:

* Changes to the manifest schema: Having a strict schema for the manifest file has the two benefits that the manifest files can quickly be validated (e.g at developing time inside IDEs) and that app developers can use autocompletion features from IDEs, which greatly improves developer experience. However schema changes to an existing schema can only be made in a way that won't break existing apps (new stuff can be added, the schema can be loosened, but nothing can be removed or made stricter). For making more radical changes to the schema a new version of the schema can be introduced, but it must be ensured that apps have enough time to adapt to the new schema, that's why it is necessary to have a period in which both versions of the schema are supported.
* Changes to the format of outgoing request: We send multiple requests to third party app backends (e.g. during registration, triggering webhooks, triggering action-buttons, loading custom modules).  
   The format of this requests cannot be changed in a breaking way in minor (6.3.x) and patch (6.3.0.x) versions. This means it is possible to add new parameters to the outgoing requests, but not to remove (or rename) existing parameters. If this is needed it needs to be made in a major version (6.3) and needs to be documented properly, so that app developers can adapt to the changes.

All changes and possible breaks from the point of view of an app developer will be documented in separate `App System` sections inside the changelog and upgrade files.

Additionally, the app system plugin will be deprecated after the migration process is finished and all further development will take place inside the platform.

---

## Implement individual sorting

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-14-implement-individual-sorting.html

# Implement individual sorting [​](#implement-individual-sorting)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-14-implement-individual-sorting.md)

## Context [​](#context)

Shop owners should be able to define custom sorting options for product listings and search result pages out of the administration. It should be possible to define a system default sorting option for product listings. `Top Results` will be the default on search pages and suggest route, which sorts products by `_score`.

Currently, to define a custom sorting option, you need to define it as a service and tag it as `shopware.sales_channel.product_listing.sorting`. This is somewhat tedious and makes it impossible to define individual sortings via the administration.

## Decision [​](#decision)

From now on, it is possible to define custom sortings via the administration.

Individual sortings will be stored in the database in the table `product_sorting` and its translatable label in the `product_sorting_translation` table.

It is possible to define a system default product listing sorting option, which is stored in `system_default`.`core.listing.defaultSorting`. This however has no influence on the default `Top Results` sorting on search pages and the suggest route result.

To define custom sorting options via a plugin, you can either write a migration to store them in the database. This method is recommended, as the sortings can be managed via the administration.

The `product_sorting` table looks like the following:

| Column | Type | Notes |
| --- | --- | --- |
| `id` | binary(16) |  |
| `url_key` | varchar(255) | Key (unique). Shown in url, when sorting is chosen |
| `priority` | int unsigned | Higher priority means, the sorting will be sorted top |
| `active` | tinyint(1) [1] | Inactive sortings will not be shown and will not sort |
| `locked` | tinyint(1) [0] | Locked sortings can not be edited via the DAL |
| `fields` | json | JSON of the fields by which to sort the listing |
| `created_at` | datetime(3) |  |
| `updated_at` | datetime(3) |  |

The JSON for the fields column look like this:

json5

```shiki
[
  {
    "field": "product.name",        // property to sort by (mandatory)  
    "order": "desc",                // "asc" or "desc" (mandatory)
    "priority": 0,                  // in which order the sorting is to applied (higher priority comes first) (mandatory)
    "naturalSorting": 0
  },
  {
    "field": "product.cheapestPrice",
    "order": "asc",
    "priority": 100,
    "naturalSorting": 0
  },
  // ...
]
```

---

Otherwise, you can subscribe to the `ProductListingCriteriaEvent` to add a `ProductSortingEntity` as available sorting on the fly.

php

```shiki
<?php

namespace Shopware\Core\Content\Product\SalesChannel\Sorting\Example;

use Shopware\Core\Content\Product\Events\ProductListingCriteriaEvent;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingCollection;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingEntity;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ExampleListingSubscriber implements EventSubscriberInterface {

    public static function getSubscribedEvents(): array
    {
        return [
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
        $myCustomSorting->setTranslated(['label' => 'My Custom Sorting']);
        $myCustomSorting->setKey('my-custom-sort');
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

## Consequences [​](#consequences)

The old behaviour of defining the custom sorting as a tagged service is deprecated and will be removed in v6.4.0.

---

## Merchant registration

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-14-merchant-registration.html

# Merchant registration [​](#merchant-registration)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-14-merchant-registration.md)

## Context [​](#context)

We have to provide a registration for merchant. The definition of a customer, which is defined as a merchant, we want to realize via customer groups. However, this is not "merchant" specific, because we do not react to "merchant customer groups" in any way in the core. In other words, we implement a customer group registration system.

The process should work as follows:

* The shop owner enables customer group registration for a customer group and generates an url
  + This url must be shared by the shop owner to customers (footer, social media, mails, etc.)
* Customer registers on an individual registration page on an individual url
* The customer will be created with the default customer group
* The shop operator can accept / decline the "merchant" registration in the admin

For this I would suggest the following:

* At the customer we store another Foreign Key (desired customer group)
  + This is then considered in the StoreApiRoute and stored at the customer
* In Administration we extend the current customer module with an accept / decline button
* Upon activation, we switch the customer group of the customer and set "desired customer group" back to zero.

## Decision [​](#decision)

### Headless Frontend [​](#headless-frontend)

* Headless sales channel can resolve the url to get the foreign key using the seo-url store api route
* Call the customer-group-registration config endpoint with the foreign key to get the form configuration
* Sends a registration to customer registration endpoint with the `requestedGroupId`

## Consequences [​](#consequences)

* Registration always creates customer accounts even when the request will be declined.

---

## Notification titles are pre-defined and make use of the global namespace

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-21-unified-notification-titles.html

# Notification titles are pre-defined and make use of the global namespace [​](#notification-titles-are-pre-defined-and-make-use-of-the-global-namespace)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-21-unified-notification-titles.md)

## Context [​](#context)

* Creating notification messages in the administration caused the effort of making up not only a title but a message too. This has led to inconsistent notification appearances. In some cases, the notification message simply duplicated the title; others wore the module's name as a title and so on.
* Now, since it is a set design decision to use the following four types of notification as titles at the same time, it is just logical to make use of the global namespace and manage notification titles centrally.

  + `Success` (green outline)
  + `Error` (red outline)
  + `Info` (blue outline)
  + `Warning` (orange outline)

## Decision [​](#decision)

* Implement a global default title for all notifications types in

`/shopware/src/Administration/Resources/app/administration/src/app/mixin/notification.mixin.js`

* Remove the superfluous title definitions and snippets

## Consequences [​](#consequences)

* By introducing the global namespace as early as in the `notification.mixin.js` it is now unnecessary to define individual titles when implementing notifications within a module.
* Notifications from now on only require a "notification message" and thus the creation of only snippet within each snippet file (en-GB and de-DE).
* Consequently, a bunch of unused snippets have been removed. For more information on snippets deleted in this course see CHANGELOG-6.3.md

### Examples [​](#examples)

* Create error notification

js

```shiki
this.createNotificationError({
    message: this.$tc('sw-module.messageError')
});
```

* Create error message snippets (DE/EN)

json

```shiki
    "messageError": "Meaningful error message.",
```

* Avoid cheap solutions like

js

```shiki
this.createNotificationError({
    message: err
});
```

### Best practice [​](#best-practice)

* Messages should be translatable, precise and not redundant. An error notification's title literally says: "Error" - no need in repeating that. Better find and present information on what exactly went wrong.
* Make use of success notifications, but make them carry useful information, by e.g., including counters.
* Make use of info and warning notifications to keep users informed about things that are ongoing or need a closer look!
* As it is still possible to override the mixin presets with these individual settings, it is theoretically still possible to define individual titles. It would cross the design idea of unified titles though and should only be considered for very good reasons!

## tl;dr [​](#tl-dr)

> *When creating notifications, just decide on the correct type of notification, add a meaningful message, don't waste even a thought on creating a title... And you're done!*

---

## Import ACL privileges from other roles

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-08-28-import-acl-privileges-from-other-roles.html

# Import ACL privileges from other roles [​](#import-acl-privileges-from-other-roles)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-08-28-import-acl-privileges-from-other-roles.md)

## Context [​](#context)

Some modules have components which require many acl privileges. Examples are the rule builder or the media manager. Therefore, you need all privileges in each module which have these components. Also you do not want to add the module to the dependency section because then the user has full access to module in the administration.

## Decision [​](#decision)

To avoid duplication of these privileges we use a helper function. These function returns all privileges from the other module dynamically. You can use it directly in the privileges:

js

```shiki
Shopware.Service('privileges')
    .addPrivilegeMappingEntry({
        category: 'permissions',
        parent: null,
        key: 'promotion',
        roles: {
            viewer: {
                privileges: ['promotion:read',],
                dependencies: []
            },
            editor: {
                privileges: [
                    'promotion:update',
                    Shopware.Service('privileges').getPrivileges('rule.creator')
                ],
                dependencies: [
                    'promotion.viewer'
                ]
            }   
        }
    });
```

## Consequences [​](#consequences)

Each module contains only the relevant privileges for his module. All needed privileges which are not directly mapped to the module can be imported. This has the big benefit if someone changes something in the imported module all other modules will be affected too.

---

## CustomField label loading in storefront

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-09-08-custom-field-label-loading-in-storefront.html

# CustomField label loading in storefront [​](#customfield-label-loading-in-storefront)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-09-08-custom-field-label-loading-in-storefront.md)

## Context [​](#context)

We want to provide the labels of custom fields in the storefront to third party developers. On one hand we could add the labels to every loaded entity, but this will cause a heavy leak of performance and the labels are often not used in the template.

## Decision [​](#decision)

We implemented a subscriber, which listen on the `custom_field.written` event to add also snippets to all snippet sets with the given label translations of the custom field. The `translationKey` of the snippets are prefixed with `customFields.`, followed by the technical name of the custom field. Thus the snippets can be used in the storefront.

## Consequences [​](#consequences)

Inserting a custom field always creates new snippet with the given label translations.

---

## The best-practice to always re-fetch the data after saving

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-09-17-the-best-practice-to-always-re-fetch-the-data-after-saving.html

# The best-practice to always re-fetch the data after saving [​](#the-best-practice-to-always-re-fetch-the-data-after-saving)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-09-17-the-best-practice-to-always-re-fetch-the-data-after-saving.md)

## Context [​](#context)

We should always re-fetch the entity data after saving within admin pages.

## Decision [​](#decision)

Reload the data after each saving progress to ensure the user will work only the latest data.

When you save data without reloading the entity, then you need to re-assign the values. But you can't be sure, that these values are the latest ones, because of possible data inconsistency during the saving process. That's why re-fetching data is always important for further CRUD operations.

For example:

html

```shiki
<!-- we change the status by click to switch for example -->
<sw-switch-field
    v-model="data.status"
    :label="$tc('sw-review.detail.labelStatus')">
</sw-switch-field>

<!-- we will save data with onSave method -->
<sw-button-process @click="onSave">
    {{ $tc('global.default.save') }}
</sw-button-process>
```

javascript

```shiki
// This method for button save
onSave() {
    this.repository.save(this.data, Shopware.Context.api).then(() => {
        // We should add the method to re-fetch the entity data after save success here
        this.loadEntityData();
    });
},

// This method to re-fetch the data
loadEntityData() {
    const criteria = new Criteria();
    const context = { ...Shopware.Context.api, inheritance: true };

    this.repository.get(this.data.id, context, criteria).then((data) => {
        this.data = data;
    });
},
```

## Consequences [​](#consequences)

Consistent and CRUD-ready data in your administration.

---

## Creating events in Shopware

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-11-06-creating-events.html

# Creating events in Shopware [​](#creating-events-in-shopware)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-06-creating-events.md)

## Context [​](#context)

Events throughout Shopware are quite inconsistent. It is not defined which data it must or can contain. This mainly depends on the domain where the events are thrown.

## Decision [​](#decision)

Developers should always have access to the right context of the current request, at least the `Shopware\Core\Framework\Context` should be present as property in events. If the event is thrown in a SalesChannel context, the `Shopware\Core\System\SalesChannel\SalesChannelContext` should also be present as property.

## Consequences [​](#consequences)

From now on every new event must implement the `Shopware\Core\Framework\Event\ShopwareEvent` interface. If a `Shopware\Core\System\SalesChannel\SalesChannelContext` is also available, the `Shopware\Core\Framework\Event\ShopwareSalesChannelEvent` interface must be implemented instead.

---

## DAL join filter

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-11-19-dal-join-filter.html

# DAL join filter [​](#dal-join-filter)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-19-dal-join-filter.md)

## Context [​](#context)

Currently, there are various difficulties with the current implementation of the `anti-join-filter`. Sometimes this does not lead to the correct results or the query cannot be executed due to a PHP exception. Furthermore the counterpart to the `anti-join-filter`, the `join-filter`, is missing. Currently the `anti-join-filter` is automatically assembled in the entity searcher if a `not-filter` exists that points to a field of an association.

### Anti join filter concept [​](#anti-join-filter-concept)

The `anti-join-filter` should make sure that a `to-many` association can be queried negated on multiple values, here is an example:

**Give me all products which do not have "red" or "yellow" as property, but also not "XL" or "L".** On the SQL side, the following query must be generated for this purpose:

sql

```shiki
SELECT product.id

FROM product
    LEFT JOIN property_properties color_filter
        ON color_filter.product_id = product.id
        AND color_filter.id IN ("red", "yellow")

    LEFT JOIN property_properties size_filter
        ON size_filter.product_id = product.id
        AND size_filter.id IN ("XL", "L")

WHERE size_filter.product_id IS NULL
AND color_filter.product_id IS NULL
```

### Join filter concept [​](#join-filter-concept)

The `join-filter` should make sure that a `to-many` association can be queried on multiple values, here is an example:

**Give me all products which do have "red" or "yellow" as property, but also "XL" or "L".** On the SQL side, the following query must be generated for this purpose:

sql

```shiki
SELECT product.id

FROM product
    LEFT JOIN property_properties color_filter
        ON color_filter.product_id = product.id
        AND color_filter.id IN ("red", "yellow")

    LEFT JOIN property_properties size_filter
        ON size_filter.product_id = product.id
        AND size_filter.id IN ("XL", "L")

WHERE size_filter.product_id IS NOT NULL
AND color_filter.product_id IS NOT NULL
```

## Decision [​](#decision)

Whether several joins must be made on an association must be recognized by the DBAL implementation itself. The user of the DAL does not have to pass an extra parameter for this. However, since it is difficult to interpret what exactly is to be determined by the criteria, the algorithm for determination is based on certain rules.

We will form so called `join-groups` in the DAL. These are created per `multi-filter` layer. So a join to an association is only possible once per `multi-filter` layer. So we allow to query several fields within one join. But if an already filtered field is filtered in another or nested `multi-filter`, a separate join is created for this field. It is only necessary to resolve the `to-many` association several times. After the `join-groups` have been formed, the field to be resolved is passed to the `FieldResolver` (which forms the SQL JOIN) and the filter in which this field is located. Resolved filters in the JOIN are then marked and later in the WHERE they are linked with the corresponding AND/OR/NOT logic.

## Consequences [​](#consequences)

Queries against the DAL can now behave differently if multiple filters are set on a to many association. To filter a to many association on multiple fields, where all filters should be related to each other, they must now be wrapped in a multi filter.

Note: If you use filters that filter on a to-many association field, you should check if the results of this query are still correct. It may be that more or less records are returned.

The following example shows how the filter behavior has changed on to-many associations:

```shiki
1: 
$criteria->addFilter(
    new AndFilter([
        new EqualsFilter('product.categories.name', 'test-category'),
        new EqualsFilter('product.categories.active', true)
    ])
);

2:
$criteria->addFilter(
    new EqualsFilter('product.categories.name', 'test-category')
);
$criteria->addFilter(
    new EqualsFilter('product.categories.active', true)
);
```

1: Returns all products assigned to the `test-category` category where `test-category` is also active. 2: Returns all products that are assigned to the `test-category` category AND have a category assigned that is active.

---

## Add the login required annotation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-11-20-add-login-required-annotation.html

# Add the login required annotation [​](#add-the-login-required-annotation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-20-add-login-required-annotation.md)

## Context [​](#context)

Some routes for the `sales-channel-api` and the `store-api/storefront` depend on `SalesChannelContext` to identify whether the Customer is logged or not. For keeping clean code, consistency, and more easy to readable API. We create a new annotation for routing `\Core\Framework\Routing\Annotation\LoginRequired`.

## Decision [​](#decision)

With the `store-api/storefront` routing needs requiring logged in for access, developers need to define annotation `@LoginRequired` for API.

This annotation to the following:

* `@LoginRequired`
  + This annotation is validating the `SalesChannelContext` has Customer return success, otherwise throw `CustomerNotLoggedInException`
* `@LoginRequired(allowGuest=true)`
  + This annotation is validating the `SalesChannelContext` has Customer and allow Guest admits, otherwise throw `CustomerNotLoggedInException`

An example looks like the following:

php

```shiki
/**
 * @Since("6.0.0.0")
 * @LoginRequired()
 * @Route(path="/store-api/v{version}/account/logout", name="store-api.account.logout", methods={"POST"})
 */

/**
 * @Since("6.2.0.0")
 * @LoginRequired(allowGuest=true)
 * @Route("/account/order/edit/{orderId}", name="frontend.account.edit-order.page", methods={"GET"})
 */
```

## Consequences [​](#consequences)

From the moment the `LoginRequired` annotation should be using every new `store-api/storefront` if the routing needs requiring logged in for access. If `LoginRequired` is not using, that means the `store-api/storefront` can accept without a login.

---

## Decoration pattern

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-11-25-decoration-pattern.html

# Decoration pattern [​](#decoration-pattern)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-25-decoration-pattern.md)

## Context [​](#context)

There are currently two different patterns that are applied in the platform to allow the decoration of services. On the one hand there are the interfaces and on the other hand the abstract classes.

With this ADR it should be decided that we don't implement interfaces anymore, because they are too strict.

There are two reasons why we should no longer implement interfaces.

### It is much more complicated to add more parameters for a function of the interface [​](#it-is-much-more-complicated-to-add-more-parameters-for-a-function-of-the-interface)

To add another parameter to a function or interface, proceed as follows:

* The additional parameter is documented in the interface

php

```shiki
interface DataValidationFactoryInterface
{
    /**
     * @param array $data - @deprecated tag:v6.4.0 - Will be introduced in v6.4.0
     */
    public function create(SalesChannelContext $context /* array $data */): DataValidationDefinition;
}
```

* In the implementation, the parameter can be accepted as follows:

php

```shiki
class ContactFormValidationFactory implements DataValidationFactoryInterface
{
    public function create(SalesChannelContext $context  /* array $data */): DataValidationDefinition
    {
        $data = func_get_arg(1) ?? [];
    }
}
```

As you can see, it is possible, but this is more "beautiful" with abstract classes:

php

```shiki
abstract class AbstractCustomerRoute
{
    /**
     * @deprecated tag:v6.4.0 - Parameter $criteria will be mandatory in future implementation
     */
    abstract public function load(Request $request, SalesChannelContext $context/*, Criteria $criteria*/): CustomerResponse;
}

class CustomerRoute extends AbstractCustomerRoute
{
    public function load(Request $request, SalesChannelContext $context, ?Criteria $criteria = null): CustomerResponse
    {
    }
}
```

### It is not possible to provide further functions in the class [​](#it-is-not-possible-to-provide-further-functions-in-the-class)

If we have to implement another function in an interface this is only possible in a very complicated way.

* a new interface is implemented which extends the old one:

php

```shiki
interface DataValidationFactoryInterface
{
    public function create(SalesChannelContext $context /* array $data */): DataValidationDefinition;
}

interface DataValidationFactoryInterfaceV2 extends DataValidationFactoryInterface
{
    public function update(SalesChannelContext $context /* array $data */): DataValidationDefinition;
}
```

* At the appropriate place where the class is called, it is checked if the instance implements the new interface:

php

```shiki
if ($service instanceof DataValidationFactoryInterfaceV2) {
    $service->update(..)
} else {
    $service->create(..)
}
```

However, errors occur here if several plugins decorate this service. If one of the plugins does not yet implement the new interface, there is a PHP error. With the pattern of the abstract classes this looks differently. Here a fallback is provided by the `getDecorated()` method. Plugins which do not support the new function yet, are virtually skipped in the decoration chain.

php

```shiki
abstract class AbstractCustomerRoute
{
    abstract public function load(Request $request, SalesChannelContext $context): CustomerResponse;

    abstract public function getDecorated(): AbstractCustomerRoute; 

    public function loadV2() 
    {
        $this->getDecorated()->loadV2();                               
    }       
}
```

At the appropriate place where the class is called, we can simply use the new function without checking if the current service instance already contains the new method:

php

```shiki
$service->loadV2(..);
```

## Decision [​](#decision)

* In the platform we no longer use interfaces for service definitions. Especially not if this service is intended for decoration.
* For other cases we use abstract classes as well because we can easily extend or change signatures.

## Consequences [​](#consequences)

* We replace, iteratively, the existing interfaces that are marked as not @internal with abstract classes
* The abstract class must implement the interface for backward compatibility
* Once an equivalent for the interface exists, it will be deprecated and removed with the next major version
* The abstract class is always used as type hint for constructors or parameters.

---

## API version removal

**Source:** https://developer.shopware.com/docs/resources/references/adr/2020-12-02-removing-api-version.html

# API version removal [​](#api-version-removal)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2020-12-02-removing-api-version.md)

## Context [​](#context)

Due to the new deprecation strategy and the 6-8 months major cycle, API versioning is no longer reasonable or even possible. Deprecated fields and routes are currently tagged in a minor version and will be removed with the next major version. The API version is currently not increased in a minor version, which would not make sense, because with every second minor version deprecations would have to be removed.

## Decision [​](#decision)

By removing the API versioning within the URL we want to simplify usage and the deprecation strategy of our API. The deprecated fields and routes are shown in the OpenAPI scheme as well as the API changelog and will be removed with the next major version (`6.x`).

## Consequences [​](#consequences)

All route URLs are changed from `/api/v{VERSION}/product` to `/api/product`. Beginning with 6.3.5.0 both route URLs are accessible via `/api/v{VERSION}/product` and `/api/product` before and until the release of 6.4.0.0 in order to enable preparation of connections well in advance.

---

## Processing of nested line items

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-03-24-nested-line-items.html

# Processing of nested line items [​](#processing-of-nested-line-items)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-03-24-nested-line-items.md)

## Context [​](#context)

We want to handle nested order line items. Currently, the line items are available nested, but all cart processors only consider the first level of line items. On one hand, we could implement all cart processors, that they process all levels of line items, but on the other hand, all nested line items are added via plugins, which would implement their own processing logic.

## Decision [​](#decision)

The core cart processors will continue to work with `getFlat()` in enrich. This way the required data for all items in the cart will be fenced and each item could also be processed by its processor. The `process` method on other hand will still not work with `getFlat()`, but will only take care of line items that are on the first level. This way there will be no collisions in the processing of these line items. A plugin that reuses core line items can easily call the other processors to handle the nested line items themselves.

Example:

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Cart;

use Shopware\Core\Checkout\Cart\Error\IncompleteLineItemError;
use Shopware\Core\Checkout\Cart\LineItem\CartDataCollection;
use Shopware\Core\Checkout\Cart\LineItem\LineItem;
use Shopware\Core\Content\Product\Cart\ProductCartProcessor;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

class PluginCartProcessor implements CartProcessorInterface
{
    /**
     * @var CreditCartProcessor
     */
    private $creditCartProcessor;

    /**
     * @var ProductCartProcessor
     */
    private $productCartProcessor;

    public function __construct(CreditCartProcessor $creditCartProcessor, ProductCartProcessor $productCartProcessor)
    {
        $this->creditCartProcessor = $creditCartProcessor;
        $this->productCartProcessor = $productCartProcessor;
    }

    public function process(
        CartDataCollection $data,
        Cart $original,
        Cart $toCalculate,
        SalesChannelContext $context,
        CartBehavior $behavior
    ): void {
        $lineItems = $original->getLineItems()->filterType('plugin-line-item-type');

        /*
         * Structure of the plugin line item:
         * - plugin line item
         *      - product line item(s)
         *      - credit line item(s)
         */
        foreach ($lineItems as $lineItem) {
            $this->calculate($lineItem, $original, $context, $behavior, $data);
            $toCalculate->add($lineItem);
        }
    }

    private function calculate(LineItem $lineItem, Cart $original, SalesChannelContext $context, CartBehavior $behavior, CartDataCollection $data): void
    {
        if (!$lineItem->hasChildren()) {
            $original->remove($lineItem->getId());
            $original->addErrors(new IncompleteLineItemError($lineItem->getId(), 'children'));

            return;
        }

        $tempOriginalCart = new Cart('temp-original', $original->getToken());
        $tempCalculateCart = new Cart('temp-calculate', $original->getToken());

        // only provide the nested products and credit items
        $tempOriginalCart->setLineItems(
            $lineItem->getChildren()
        );

        // first start product calculation - all required data for the product processor is already loaded and stored in the CartDataCollection
        $this->productCartProcessor->process($data, $tempOriginalCart, $tempCalculateCart, $context, $behavior);

        // now calculate the credit, the credit is scoped to the already calculated products - all required data for the credit processor is already loaded and stored in the CartDataCollection
        $this->creditCartProcessor->process($data, $tempOriginalCart, $tempCalculateCart, $context, $behavior);

        // after all line items calculated - use them as new children
        $lineItem->setChildren(
            $tempCalculateCart->getLineItems()
        );
    }
}
```

## Consequences [​](#consequences)

The plugins have to implement their only processing logic or alternatively extend shopware's cart processors, when using a specific implementation of nested line items.

---

## When to use plain SQL or the DAL

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-05-14-when-to-use-plain-sql-or-dal.html

# When to use plain SQL or the DAL [​](#when-to-use-plain-sql-or-the-dal)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-05-14-when-to-use-plain-sql-or-dal.md)

## Context [​](#context)

It is often discussed whether to work with plain SQL or with the Data Abstraction Layer.

## Decision [​](#decision)

In the following application layers, the DAL should be used for the following reasons:

* In the Store API

  + Data selected and returned via Store API must be extensible by third party developers.
  + Requests against the Store API should always allow additional data to be loaded.
  + Data retrieval and encoding must be secured by ACL.
* Storefront page loader and controller

  + Data passed from the storefront to the Twig templates must be extensible by third party developers.
  + Since our templates are customized by many developers, we cannot provide only a minimal offset of the actual data.
* On admin API level

  + Data selected and returned via admin API must be extensible by third party developers.
  + Requests that go against the Store API should always allow additional data to be loaded.
  + Data retrieval and encoding must be secured by ACL.
* When writing data

  + The DAL has a validation, event and indexing system which is used for the write process. Therefore, it is mandatory to ensure data integrity, that write processes take place exclusively via the DAL.
  + The entity indexers are an exception here, see below.

In the following application layers you should work with plain SQL because of the following reasons:

* In the entity indexers

  + The entity indexers are located behind the entity repository layer, so it only makes sense that they do not work with the repositories but with the database connection directly.
  + the entity indexers must be able to re-index all data after a versions update. To avoid as much hydration and event overhead as possible, they should work directly with the connection.
  + The entity indexers are not an extension point of shopware. The queries that are executed there are only used for internal processing of data and should never be rewritten.
* In Core Components

  + Core components like the theme compiler, request transformer, etc. are not places where a third party developer should be able to load additional data. The data loaded here is for pure processing only and should never be rewritten.
  + Deep processes like theme compiling should not be affected by plugin entity schemas, because plugins are an optional part of the system and might be in an unstable state during an update process.

---

## Vue administration app has ESLint support

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-05-28-introduce-eslint-on-vue-admin.html

# Vue administration app has ESLint support [​](#vue-administration-app-has-eslint-support)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-05-28-introduce-eslint-on-vue-admin.md)

## Context [​](#context)

We want to support ESLint of the administration vue app to keep and increase code quality.

By adding ESLint to the administration app, every developer will get instant feedback and best practices on his code by writing.

## Decision [​](#decision)

For the `*.js` linting, we want to get pretty close to a standard vue2 app linting. In the `*.js` linting chapter, we explain where and why we choose to leave the common way.

For the `*.html.twig` linting, we need to create a custom solution, which can handle or circumstance the twig syntax in our templates. We decided to convert all twig syntax to HTML comments within the linting process. This way, the linter ignores the twig parts and can handle the twig files like typical vue templates. The most significant tradeoff with this solution is that the linter cannot take the twig blocks into account on computing indentation levels.

### `*.js` linting [​](#js-linting)

For the `*.js` files we try to follow a standard vue cli linting way, with this adjustments:

* [`'vue/require-prop-types': 'error'`](https://eslint.vuejs.org/rules/require-prop-types.html) - always use proper types definitions for `props`
* [`'vue/require-default-prop': 'error'`](https://eslint.vuejs.org/rules/require-default-prop.html) - always provide a default value for optional `props`
* [`'vue/no-mutating-props': ['off']`](https://eslint.vuejs.org/rules/no-mutating-props.html) - this is a tradeoff to allow mutating properties because it is already heavily used
* [`'vue/component-definition-name-casing': ['error', 'kebab-case']`](https://eslint.vuejs.org/rules/component-definition-name-casing.html) - write component names in kebab-casing

### `*.spec.js` linting [​](#spec-js-linting)

During writing unit test files, we do not want to get a `max-len` warning. A `max-len` rule may lead to hard understandable output in test names only to suit the `max-len` rules. In a test itself, you sometimes have `selector` phrases or something else where you exceed the `max-len` rule without a chance to solve it.

### `*.html.twig` linting [​](#html-twig-linting)

Besides the *twig-to-html-comment* tradeoff, these exceptions are also made:

* `'vue/component-name-in-template-casing': ['error', 'kebab-case']` - write vue component names in kebab-case in templates
* `'vue/no-multiple-template-root': 'off',` - due to external template files and component inheritance
* `'vue/attribute-hyphenation': 'error'` - write `hello-word=""` attributes instead of `helloWorld=""`
* `'vue/no-parsing-error': ['error', {'nested-comment': false}]` - ignore nested html comments, which may be a result of the twig-to-html-comment workflow
* `'vue/valid-template-root': 'off'` - @see `vue/no-multiple-template-root`
* `'vue/valid-v-slot': ['error', { allowModifiers: true }]` - allow `.`s in template slot names
* `'vue/no-unused-vars': 'off'` - the twig parser cannot understand if a scoped slot value is used or not used properly
* `'vue/no-template-shadow': 'off'` - for providing scoped values into another template scope
* `'vue/no-lone-template': 'off'` - in some composition cases lone template tags are used
* `'vue/no-v-html': 'off'` - for i18n and other reasons v-html is often used

### twig block indentation [​](#twig-block-indentation)

To accomplish the twig syntax being able to be linted, we needed to create a custom [`eslint-twig-vue-plugin`](../src/Administration/Resources/app/administration/twigVuePlugin/lib/processors/twig-vue-processor.js) and to accept the following changes in template writing:

*before*

html

```shiki
    …
    <div>
        {% block block_name %}
            <div>
                …
    …
```

*now*

html

```shiki
    …
    <div>
        {% block block_name %}
        <div>
        …
```

To be able to lint the twig templates, we replace the twig syntax with HTML comments during the lint process, and thus every `twig` syntax is treated as an HTML comment and not recognised for indentation.

### self-closing components [​](#self-closing-components)

*before*

html

```shiki
…
    <sw-language-switcher></sw-language-switcher>
…
```

*now*

html

```shiki
…
    <sw-language-switcher />
…
```

### attribute alignment [​](#attribute-alignment)

As soon as more than 1 attribute exists, every attribute gets its own line:

*before*

html

```shiki
    …
    <div v-for="strategy in strategies" class="sw-app-app-url-changed-modal__content-choices">
    …
    <sw-icon small color="#189eff" name="default-basic-shape-circle-filled"></sw-icon>
    …
```

*now*

html

```shiki
    …
    <div
        v-for="strategy in strategies"
        class="sw-app-app-url-changed-modal__content-choices"
    >
    …
    <sw-icon
        small
        color="#189eff"
        name="default-basic-shape-circle-filled"
    />
    …
```

## Linting Pitfalls [​](#linting-pitfalls)

### invalid-x-end-tag [​](#invalid-x-end-tag)

If you stumble upon a *very* red marked file from your linter, please check first that your twig syntax follows this pattern:

twig

```shiki
  {% block block_name %} ✔ <!-- whitespace after and before twig syntax `{% ` and ` %}`. -->
  {% block block_name%} ✘ <!-- missing whitespace after or before twig syntax `{%` or `%}` -->
```

### disabling eslint rules in templates [​](#disabling-eslint-rules-in-templates)

It is possible to disable a specific linting rule in the template by using this syntax:

html

```shiki
    <!-- eslint-disable vue/eslint-rule-to-be-disabled -->
    <div>
    …
```

Please follow the *know the rules, break the rules* approach and not the *dont bug me linter* approach.

## ESLint IDE setup [​](#eslint-ide-setup)

The `*.js` linting should run out of the box with PHPStorm or VSCode. For `*.html.twig` linting have a look at the next chapter.

ESLint is part of the CI pipeline, so a running ESLint environment is mandatory.

### Twig Linting Setup [​](#twig-linting-setup)

#### VSCode [​](#vscode)

Should work out of the box @see [.vscode/settings.json](../.vscode/settings.json).

#### PHPStorm [​](#phpstorm)

Add `html,twig` to `eslint.additional.file.extensions` list in Registry (Help > Find Action..., type registry... to locate it) and re-start the IDE.

---

## Introduce jest-fail-on-console

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-06-14-introduce-jest-fail-on-console.html

# Introduce jest-fail-on-console [​](#introduce-jest-fail-on-console)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-06-14-introduce-jest-fail-on-console.md)

## Context [​](#context)

A jest pipeline run produced previously hundreds of errors and warnings, which made it hard to see why a test failed and if a passing test isn’t just a false positive.

## Decision [​](#decision)

To combat this, we decided to introduce the npm package [jest-fail-on-console](https://github.com/ricardo-ch/jest-fail-on-console#readme), which causes individual unit tests to fail if they log an error or a warning to the console.

## Consequences [​](#consequences)

Jest-fail-on-console makes unit tests a lot more expressive because it prevents easy mistakes, which would previously lead to an error that is hard to find and notice. Like an incorrect key in a `v-for` loop, which could potentially lead to vue update errors, but would have not caused the test to fail.

Jest tests might be a little harder to write, because errors cannot simply be ignored anymore. All needed components have to be provided to the component being tested either by being mocked or built, all API requests need to be mocked, and all needed mixins have to be provided. Although it is a little more work, it makes the jest tests, as previously mentioned, more expressive and as a neat side benefit it keeps the console clean.

---

## Move storefront script to head with defer

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-07-22-move-storefront-scripts-to-head.html

# Move storefront script to head with defer [​](#move-storefront-script-to-head-with-defer)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-07-22-move-storefront-scripts-to-head.md)

## Context [​](#context)

* Currently, our main storefront scripts (inline scripts as well as `all.js`) are located at the bottom of the page near the body end tag.
* The `async` attribute is used for the `all.js` but it isn't really suitable because our own JavaScript plugins depend on DOM elements in order to be initialized, and we have to wait for the document to be finished anyway.
* Additionally, the `DOMContentLoaded` is not compatible with `async` scripts because they might run before this particular event. That's why `document.readystatechange --> complete` is being used at the moment.
* This has the downside, that none of our JavaScript plugins initializes before the entire document is fully loaded including all resources like images.

## Decision [​](#decision)

* In order to improve the script loading all default `<script>` tags are moved to the `<head>` and get a `defer` attribute in favor of `async`.
* To initialize the JavaScript plugins, the `DOMContentLoaded` is being used instead of `document.readystatechange --> complete`.
  + This ensures that the JavaScript plugins initialization must only wait for the document itself but not for additional resources like images.
* This change allows the browser to download/fetch the scripts right away when the `<head>` is parsed instead of when almost the entire document is already parsed.
* Because of `defer` the script execution will wait until the document is parsed (Just right before the `DOMContentLoaded` event).
* `defer` also ensures that the different `<script>`'s are executed in the order in which they are declared.

## Consequences [​](#consequences)

All app/plugin script tags which extended one of the `base_body_script` child blocks must be moved to `Resources/views/storefront/layout/meta.html.twig`

---

## Storefront coding standards

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-08-10-storefront-coding-standards.html

# Storefront coding standards [​](#storefront-coding-standards)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-08-10-storefront-coding-standards.md)

## Context [​](#context)

* The current coding standards are not put into an ADR yet.
* This ADR is to determine the current standards to have a start from where to enhance the storefront concept further more.

## Decision [​](#decision)

### Routes annotations [​](#routes-annotations)

Route annotations respect the following schema: example:

php

```shiki
#[Route(path: '/example/endpoint/{id}', name: 'frontend.example.endpoint', options: ['seo' => false], defaults: ['id' => null, 'XmlHttpRequest' => true, '_loginRequired' => true, '_httpCache' => true], methods: ['GET', 'POST', 'DELETE'])]
```

* `path`: The path of the route. Parameters inside the path will be noted in {} brackets.
* `name`: A unique name for the route beginning with `frontend.`
* `options`: Options for the route to be determined for special cases. Currently `seo` = (true|false) is the only option.
* `defaults`: A set of default parameter for the Route. Either preconfigured parameters or any route query/path parameter can be defined as a default here.
  + `id` (any value): Stands as an example for any path parameter. Can be any noted parameter and the value is used, if it is not set by the request
  + `XmlHttpRequest` (true|false): If the route is an XmlHttpRequest which is normally called by a frontend ajax request. These Routes don't return the `renderStorefront` call.
  + `_loginRrequired` (true|false): Is a logged in user is required to call this route? Otherwise a "permission denied" redirect will be returned.
  + `__httpCache` (true|false): Should this route be cached in the httpCache?
* `methods`: One or more of the HTTP methods ('GET', 'POST', 'DELETE')
  + `GET`: A request which returns data or a html page.
  + `POST`: A request which sends data to the server.
  + `DELETE`: A request which deletes data on the server.

### Controller [​](#controller)

* Each controller requires a Route annotation with a path, name and method: #[Route(path: '/xxx', name: 'frontend.xxx.page', methods: ['GET', 'POST'])]
* The name of the route has to be starting with "frontend"
* Each route has to define the corresponding HTTP Method (GET, POST, DELETE, PATCH)
* Routes which renders pages for the storefront (GET calls) are calling a respective pageloader to get the data it needs.
* The function name should be concise
* Each function has to define a return type hint
* A route only have a single purpose
* Use Symfony flash bags for error reporting to the frontend user
* Each storefront functionality has to be available inside the store-api too
* A storefront controller should never contain business logic
* The controller class requires the annotation: `#[Route(defaults: [\Shopware\Core\PlatformRequest::ATTRIBUTE_ROUTE_SCOPE => [\Shopware\Storefront\Framework\Routing\StorefrontRouteScope::ID]])]`
* Depending services has to be injected over the class constructor. The only exception is the container, which can be injected with the method `setContainer`
* Depending services has to be defined in the DI-Container service definition
* Depending services has to be assigned to a private class property
* Each storefront controller needs to be declared as a public service. (otherwise the routes can be removed from the container)
* A storefront controller has to extend the `\Shopware\Storefront\Controller\StorefrontController`
* Using \_loginRequired=true defaults parameter to identify whether the Customer is logged in or not.
* Each storefront functionality needs to make use of a store-api route service. This is to make sure, this functionality is also available via API

### Operations inside Storefront controllers [​](#operations-inside-storefront-controllers)

A storefront controller should never use a repository directly, It should be injected inside a Route.

Routes which should load a full storefront page, should use a PageLoader class to load all corresponding data that returns a Page-Object.

Pages which contains data which are the same for all customers, should have the \_httpCache=true defaults parameter in the Routes annotation.

#### Write operations inside Storefront controllers [​](#write-operations-inside-storefront-controllers)

Write operations should create their response with the createActionResponse function to allow different forwards and redirects. Each write operation has to call a corresponding store-api route.

### Page-/PageletLoader [​](#page-pageletloader)

* A PageLoader is a class which creates a page-object with the data for the called whole page.
* A PageletLoader is a class which creates a pagelet-object with the data for a part of a page.

The pageLoaders are a specific class to load the data for a given page. The controller calls the pageloader, which collects the needed data for that page via the Store-api. The pageloader can call other pageletloaders to get the data for pagelets(subcontent for a page). The pageloader always returns a page-object.

## Consequences [​](#consequences)

All dependencies in the controllers for routes which render a page have to be moved to the `Loaders` and if still missing, the `Loader` and `Page` has to be created. All direct DAL-dependencies inside the storefront have to be moved to Store-Api routes and respective calls. All other dependencies which are not allowed have to be checked for individual alternatives

---

## Make shopware/shopware stand-alone for development and testing

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-08-11-make-platform-stand-alone.html

# Make shopware/shopware stand-alone for development and testing [​](#make-shopware-shopware-stand-alone-for-development-and-testing)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-08-11-make-platform-stand-alone.md)

## Context [​](#context)

The platform requires some additional config, a console and web entrypoint and additional development tooling for development, tests and running the application. In practice this is provided by one of the templates: `shopware/development` or `shopware/production`. This creates a cyclic dependency, which brings some problems:

* `shopware/development` and `shopware/shopware` need to be updated in lockstep, which makes updating them individually sometimes impossible
* some IDEs have trouble with multi-repository projects
* updating development tooling breaks everything
* auto-detection of git revision and diff is broken because the development template is the root
* for each release branch an additional branch needs to be maintained

## Decision [​](#decision)

* use shopware/shopware directly in the pipeline
* allow development without a template by moving the development tooling into platform
* only advertise this as `shopware/shopware` development setup. Projects should still start with `shopware/production` as a template
* `shopware/development` should continue to work
* allow testing by adding entrypoints for cli and web
* add scripts to composer to ease common tasks
  + these scripts should be kept small and simple
  + essential functionality should be implemented as npm scripts or symfony commands
  + we should improve the symfony commands or npm scripts if they are too complicated
  + if possible, the scripts should allow adding arguments
* use standard convention
  + `.env.dist` provides default environment variables
  + `.env` can be used to define a custom environment (for example, if you use a native setup)
  + `docker-compose.yml` provides a working environment
  + `docker-compose.override.yml` can be used for local overrides to expose ports, for example
* use defaults that work out of the box in most cases
  + don't expose hard coded ports in docker-compose.yml. It's not possible to undo it and may prevent startup of the app service

## Consequences [​](#consequences)

* simplified CI, which also makes errors easier to reproduce locally
* simplified local setup
* no custom scripts that are not available in all setups
* projects may try to use shopware/shopware directly
* yet another shopware setup to choose from

---

## Refactor admin build process to webpack-multi-compiler mode

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-08-31-refactor-admin-build-process-to-webpack-multi-compiler-mode.html

# Refactor admin build process to webpack-multi-compiler mode [​](#refactor-admin-build-process-to-webpack-multi-compiler-mode)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-08-31-refactor-admin-build-process-to-webpack-multi-compiler-mode.md)

## Context [​](#context)

Previously the plugins are not completely independent from the core and other plugins. This has sometimes caused built plugin files to be incompatible with the core. Unless they were rebuilt again with the core.

The reason for this was that dependencies between plugins and the Core were optimized by Webpack. This was because Webpack saw the combination of Core and plugins as one big program. So using tree-shaking, sometimes dependencies were removed or added depending on which plugins were installed.

Also, a custom Webpack configuration in plugins resulted in it unavoidably being applied in core as well. This could sometimes result in the plugin only being compatible with the core if both were built together. If the plugin was then installed on other systems with only the built files, it could cause it not to work.

## Decision [​](#decision)

Webpack is known by many users and already in use. A switch to another builder needs to be deeply analyzed at first and then all plugin devs need to learn this bundler too, which can be frustrating, when you want to write a great plugin but has to learn a new bundler for no reason.

So the isolated compiling and production bundling will be realized with webpack. Webpack also provides a good way how to solve the problem. With the webpack-multi-compiler we can build several independent configurations which do not affect each other. The watch mode also works with this setup so that no developer needs to relearn something.

## Consequences [​](#consequences)

These potential errors are eliminated with the new mode. Each plugin is built completely isolated and cannot modify or affect other plugins or the core. A big advantage is that now plugin developers can customize the Webpack configuration as they wish, without having to worry about being incompatible with the core.

The complete refactoring is implemented in a backward compatible way. Therefore, no plugin developer has to change anything and can continue to develop as before. Only with the advantage that it is now more stable and secure. And with the flexibility to customize its own configuration as they like.

---

## Make Core mail templates independent from Storefront urls

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-09-06-make-core-mail-templates-independent-from-storefront-urls.html

# Make Core mail templates independent from Storefront urls [​](#make-core-mail-templates-independent-from-storefront-urls)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-09-06-make-core-mail-templates-independent-from-storefront-urls.md)

## Context [​](#context)

Some mail templates of the core component (Newsletter, Registration, Password Recovery, Order Status mails) depend on storefront Urls to be included in the mails. Those Urls are not available when shopware is used in "headless" mode, without the storefront bundle being installed.

For some mails (Newsletter subscription, Double Opt-In, Password recovery), the Url was made configurable over the system config and over the settings inside the administration.  
 The default values for those Urls are the ones that the storefront bundle would use. This option does not really scale well as each Url that should be used, needs to be configurable in the administration and this can grow quickly out of hand. Additionally, it is not clear when and where those configs should be used to generate the absolute Urls, as with the BusinessEvent system and the upcoming FlowBuilder, the sending of mails is not necessarily triggered by the same entry point all the times, but different trigger can lead to sending the same mails.

## Decision [​](#decision)

There shouldn't be any links generated on PHP-side as that can be hard to override per sales-channel and can not easily be changed by apps, and links should be generated inside the mailTemplates with string concatenation instead of `raw_url`-twig functions, so the links can still be generated even if the route is not registered in the system. To make generation of urls inside the mail templated easier, we will add a  variable to the twig context, that contains the domain of the current salesChannelContext, of the order in question etc.

The URLs we use in the core mail templates become part of the public API, and custom frontends should adhere to theme and provide routes under the same path, or create redirects so that the default URLs work for their frontend implementation.

The default urls are:

```shiki
/account/order/{deepLinkCode} -> opens the order details of the given order
/account/recover/password?hash={recoverHash} -> start password recovery process
/newsletter-subscribe?em={emailHash}&hash={subscribeHash} -> Subscribe email with given hash to the newsletter (for douple-opt in)
/registration/confirm?em={emailHash}&hash={subscribeHash} -> Confirm registration for user eith the given mail hash (for douple-opt in)
```

If the custom frontends can't or don't want to use our default URLs they can use the possibility to override the existing mail templates to generate custom URLs.

We will deprecate the usage of the system-config configuration values and the events thrown when the links are generated on PHP-side and remove those in the next major version. To be forward compatible we will already pass the necessary data needed for generating the links into the templates, so the urls can be already generated inside the mail templates.

Third party clients (like the PWA) should either adhere to our default URLs or add additional mail templates, that generate the correct urls for their client. In addition to that the third party client could extend the core mail template, rather than providing a new one, and then deciding in an `IF/ELSE` what url needs to be generated based on the salesChannel or domain.

## Consequences [​](#consequences)

The core mail templates work independently from the storefront bundle.

The urls listed in this ADR will become public API, so we cannot easily change those URLs, but have to maintain them in a backward compatible manner.

To ensure this we will add a unit test, that verifies that in our default templates we don't use any `raw_url`-functions. Additionally we ensure that the  variable is present by an unit test. As the Urls we use become public API, we will add a documentation article where we document the public Urls and to ensure that the documentation is up do date we will add another unit test.

---

## Technical concept custom entities

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-09-14-technical-concept-custom-entities.html

# Technical concept custom entities [​](#technical-concept-custom-entities)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-09-14-technical-concept-custom-entities.md)

## Context [​](#context)

It should be possible for apps to define their entities. Furthermore, it should be possible, if desired, that these entities are available via Store API. Later, it should also be possible for store operators to create such entities. The concept is to consider that Apps can not add PHP code into the system under current circumstances. Also, a store operator is, seen from our point of view, not able to write PHP code himself to guarantee logic for his custom entities. Therefore, purely through the definition of a custom entity, certain business logic should be automatically guaranteed.

## Decision [​](#decision)

### Schema [​](#schema)

* Definition
  + An app can include a `config/custom_entity.xml` file.
    - Multiple custom entities can be defined in the XML file.
  + Each custom entity, is registered with the prefix `custom_entity_` or the `ce_` shorthand.
    - App developers can then define that they would like to have `custom_entity_swag_blog` as an entity
    - To prevent naming collisions, app developers should always add their developer prefix to the entity name
    - We then create the `custom_entity_swag_blog` table
* Tables / Properties / Columns:
  + A proper MySQL table is created for each custom entity.
  + For each custom entity field we create a real MySQL table column.
  + We support the following field data types:
    - All scalar fields (int, string, text, float, date, boolean)
    - All JSON fields (JSON, list, price, etc.)
    - All "linking" associations (many-to-one and many-to-many)
      * A bi-directional association will be left out for now.
    - one-to-one and one-to-many will be not supported for now.
* Install & Update
  + When installing and updating an app, the core automatically performs a schema update.
  + Consider running a `dal:validate` on the schema when installing and updating an app.
  + New fields on a custom entity must always be nullable or have a default
  + Changing a field/property data type is not allowed
  + If a field is no longer defined in the .xml file, it will be deleted from the database.
* Identification and representation
  + Each custom entity gets a `IdField(id)`, which serves as primary key
  + Each custom entity gets a field `TranslatedField(label)`, which is required and serves as display name for the admin

### Bootstrapping [​](#bootstrapping)

* At kernel boot we load all custom entities from the database and register them in the registry and di-container.
* For each custom entity, an entity definition is registered
* A generic entity definition is used, which gets the property/column schema injected
* It must be checked how performant this is in case of bad performance we must put a cache in front of it (serialized properties/columns e.g.)
* If no database connection exists, a kernel boot should still be possible
* The loading of the custom entities for the kernel boot should be outsourced to a CustomEntityKernelLoader

### Api availability [​](#api-availability)

For routing, we have to trick a bit, because currently for each entity in the system the routes defined exactly. This is not possible because the API route loader is triggered before the custom entities are registered. Therefore...

* We always register `/api/custom-entity-{entity}` as an API route and point to a custom controller that derives from ApiController.
* A request `/api/custom-entity-swag-blog`, then runs into our controller, and we get for the parameter `entity` the value `swag-blog`. We then pass this value to the parent method and prefetch it
* If the entity was defined with the `ce_` shorthand the API endpoints also use that shorthand, which means the route would be `/api/ce-{entity}`.

### Store api integration [​](#store-api-integration)

* On the schema of the entity, the developer can define if this is `store_api_aware`.
* Entities which are not marked as `store_api_aware` will be removed from the response
* We will provide no automatic generated endpoint for the entities.
* Store api logics will be realized with the app-scripting epic

---

## Refactor theme inheritance

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-09-22-refactor-theme-inheritance.html

# Refactor theme inheritance [​](#refactor-theme-inheritance)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-09-22-refactor-theme-inheritance.md)

## Context [​](#context)

Currently, the themes can only inherit config fields from the default Storefront theme. Also, this inheritance is only a snapshot by activation time of the theme - The configs are copied to the new theme and changes to the default theme config will not appear in the new theme without a re-activation. The different possibilities to inherit different parts of a theme, like scripts, templates and config, can also cause problems on later updates.

## Decision [​](#decision)

To take this points into account, we have decided to add a new inheritance key for the `configFields` in the `theme.json` which allow a theme to inherit its config from other themes in a given order:

json

```shiki
"configInheritance": [
        "@Storefront",
        "@PreviousTheme",
        "@MyDevelopmentTheme"
    ],
```

Complete theme.json with part inheritances

json

```shiki
{
    "name": "MyDevelopmentTheme",
    "author": "Shopware AG",
    "views": [
        "@Storefront",
        "@Plugins",
        "@MyDevelopmentTheme"
    ],
    "style": [
        "app/storefront/src/scss/overrides.scss",
        "@Storefront",
        "app/storefront/src/scss/base.scss"
    ],
    "script": [
        "@Storefront",
        "app/storefront/dist/storefront/js/my-development-theme.js"
    ],
    "asset": [
        "@Storefront",
        "app/storefront/src/assets"
    ],
    "configInheritance": [
        "@Storefront",
        "@PreviousTheme",
        "@MyDevelopmentTheme"
    ],
    "config": {
        "blocks": {
            "exampleBlock": {
                "label": {
                    "en-GB": "Example block",
                    "de-DE": "Beispiel Block"
                }
            }
        },
        "sections": {
            "exampleSection": {
                "label": {
                    "en-GB": "Example section",
                    "de-DE": "Beispiel Sektion"
                }
            }
        },
        "fields": {
            "my-single-test-select-field": {
                "editable": false
            },
            "my-single-select-field": {
                "label": {
                    "en-GB": "Select a font size",
                    "de-DE": "Wähle ein Schriftgröße"
                },
                "type": "text",
                "value": "24",
                "custom": {
                    "componentName": "sw-single-select",
                    "options": [
                        {
                            "value": "16",
                            "label": {
                                "en-GB": "16px",
                                "de-DE": "16px"
                            }
                        },
                        {
                            "value": "20",
                            "label": {
                                "en-GB": "20px",
                                "de-DE": "20px"
                            }
                        },
                        {
                            "value": "24",
                            "label": {
                                "en-GB": "24px",
                                "de-DE": "24px"
                            }
                        }
                    ]
                },
                "editable": true,
                "block": "exampleBlock",
                "section": "exampleSection"
            },
            "usps-positions": {
                "label":
                {
                    "en-GB": "Position",
                    "de-DE": "Position"
                },
                "scss": true,
                "type": "text",
                "value": [
                    "top",
                    "bottom"
                ],
                "custom": {
                    "componentName": "sw-multi-select",
                    "options": [
                        {
                            "value": "bottom",
                            "label":
                            {
                                "en-GB": "bottom",
                                "de-DE": "unten"
                            }
                        },
                        {
                            "value": "top",
                            "label":
                            {
                                "en-GB": "top",
                                "de-DE": "oben"
                            }
                        },
                        {
                            "value": "middle",
                            "label":
                            {
                                "en-GB": "middle",
                                "de-DE": "mittel"
                            }
                        }
                    ]
                },
                "editable": true,
                "tab": "usps",
                "block": "exampleBlock",
                "section": "exampleSection"
            }
        }
    }
}
```

## Consequences [​](#consequences)

The Consequences for the two approaches are described below:

### 1. New config inheritance: [​](#_1-new-config-inheritance)

* The inheritance **can still cause incompatibility errors** because of missing subsets of a dependent theme.
* The current themes will work as always, but one can also add an inheritance for the config fields.
* The inheritance will no longer be a snapshot, but a dynamic copy of the inherited themes (The changes of child themes will be considered by the new theme automatically)
* The admin for the themes will get an inheritance mechanism which allows users to decide if a field will use its inherited or a new value (similar to product variant inherited fields)
* Themes which are dependent on other themes than the default storefront theme, need to add the other themes into there composer.json as `required` to prevent incomplete setups.

json

```shiki
 "require": {
        "swag/previous-theme": "~1.1"
    },
```

Example complete composer.json

json

```shiki
{
    "name": "swag/my-development-theme",
    "description": "My Development Theme",
    "type": "shopware-platform-plugin",
    "version": "1.7",
    "license": "MIT",
    "autoload": {
        "psr-4": {
            "MyDevelopmentTheme\\": "src/"
        }
    },
    "require": {
        "swag/previous-theme": "~1.1"
    },
    "extra": {
        "shopware-plugin-class": "MyDevelopmentTheme\\MyDevelopmentTheme",
        "label": {
            "de-DE": "Theme MyDevelopmentTheme plugin",
            "en-GB": "Theme MyDevelopmentTheme plugin"
        }
    }
}
```

---

## Payment Flow

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-10-01-payment-flow.html

# Payment Flow [​](#payment-flow)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-10-01-payment-flow.md)

## Context [​](#context)

We have to provide a standardized way for Shopware extensions to implement custom payments.

## Decision [​](#decision)

We implement two possible handlers **Synchronous Payment** and **Asynchronous Payment**. Both handlers can optionally implement [Accepting-pre-created-payments](#accepting-pre-created-payments). If a [payment transaction fails](#after-order-payment-error-case), the user can choose an alternative payment method and trigger the flow again.

## Handler [​](#handler)

### Synchronous Payment [​](#synchronous-payment)

The synchronous payment is intended to execute a payment immediately after the order has been created, **without a user interaction**. The client can pass additional data to the handler to process the payment of the order. The handler can throw an exception if an error occurs.

The following diagram shows a happy case sequence of a synchronous payment handling. The error handling is described [here](#after-order-payment-error-case)

![Synchronous Payment](/assets/synchronous-payment.DgbtG1Qv.png)

### Asynchronous Payment [​](#asynchronous-payment)

An asynchronous payment handler has to be implemented, when the client (user) has to be redirected to the payment gateway website. The client will be redirected to the actual payment site and the payment site will later redirect the client back to the success or error page of the shop. The handler is executed when the link is prepared and validates (referred to as "finalize") the redirect back from payment service.

The following diagram shows a happy case sequence of an asynchronous payment handling. The error handling is described [here](#after-order-payment-error-case)

![Asynchronous Payment](/assets/asynchronous-payment.HK78gfLw.png)

### App payments [​](#app-payments)

The app payment flow is similar to the synchronous or asynchronous flow. The app implements one of the flows and can define an external HTTP API endpoint used as a callback. This endpoint will be called instead of executing regular PHP code (custom handlers). The response will define the further payment flow like in the examples above.

## Accepting pre-created payments [​](#accepting-pre-created-payments)

To improve the payment workflow on headless systems or reduce orders without payment, payment handlers can implement an additional interface to support pre-created payments. The client (e.g. a single page application) can prepare the payment directly with the payment service (not through Shopware) and pass a transaction reference (token) to Shopware to complete the payment.

The payment handler **has to verify the given payload with the payment service**, because Shopware cannot ensure that the transaction created by the frontend is valid for the current cart. After successful verification the order will be created and the payment handler will be called again to **charge the payment**.

When the charge was successful the payment will be set to paid and the user will be forwarded to the finish page, but on [failure the after order payment process will be active](#after-order-payment-error-case). It is highly recommended implementing this optional feature, when the creation and the capturing of the payment can be separated.

![Pre created payment](/assets/pre-created-payment.BFJwxuO5.png)

## After order payment (Error case) [​](#after-order-payment-error-case)

Both possible options can produce failed payments. In failure case the after order payment process begins. The client can choose a new payment method and retry the payment and the entire payment loop of a synchronous / asynchronous payment starts again.

![After order payment](/assets/after-order-payment.B24aebC1.svg)

---

## Refund handling

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-10-13-refund-handling.html

# Refund handling [​](#refund-handling)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-10-13-refund-handling.md)

## Context [​](#context)

Shopware offers no way of unified refund handling. This results in every payment extension either implementing it themselves or not at all.

## Decision [​](#decision)

We want to implement the following structure to offer a unified refund handling for all extension types.

## New refund data structure [​](#new-refund-data-structure)

A payment extension will need to persist its actual captures to use the refund handling. Those captures are bound to a specific `OrderTransaction`. The capture has an amount, allows saving an external reference.

### OrderTransactionCapture [​](#ordertransactioncapture)

A capture is directly associated with a transaction. This relation is n `order_transaction_capture`s to 1 `order_transaction`.

#### Database table [​](#database-table)

| Type | Field name | References |
| --- | --- | --- |
| BINARY(16) | id |  |
| BINARY(16) | transaction\_id | order\_transaction.id |
| BINARY(16) | state\_id | state\_machine\_state.id |
| VARCHAR(255) NULL | external\_reference |  |
| LONGTEXT | amount |  |
| LONGTEXT NULL | custom\_fields |  |

#### Entity [​](#entity)

| Type | Property name |
| --- | --- |
| string | id |
| string | transactionId |
| string | stateId |
| string/null | externalReference |
| float | totalAmount |
| CalculatedPrice | amount |
| array/null | customFields |
| OrderTransactionEntity/null | transaction |
| StateMachineStateEntity/null | stateMachineState |
| OrderTransactionRefundCollection/null | refunds |

### OrderTransactionCaptureRefund [​](#ordertransactioncapturerefund)

A refund is directly associated with a capture. This relation is n `order_transaction_capture_refund`s to 1 `order_transaction_capture`.

#### Database table [​](#database-table-1)

| Type | Field name | References |
| --- | --- | --- |
| BINARY(16) | id |  |
| BINARY(16) | capture\_id | order\_transaction\_capture.id |
| BINARY(16) | state\_id | state\_machine\_state.id |
| VARCHAR(255) NULL | reason |  |
| LONGTEXT | amount |  |
| LONGTEXT NULL | custom\_fields |  |
| VARCHAR(255) NULL | external\_reference |  |

#### Entity [​](#entity-1)

| Type | Property name |
| --- | --- |
| string | id |
| string | captureId |
| string | stateId |
| string/null | externalReference |
| string/null | reason |
| float | totalAmount |
| CalculatedPrice | amount |
| array/null | customFields |
| StateMachineStateEntity/null | stateMachineState |
| OrderTransactionCaptureEntity/null | transactionCapture |
| OrderTransactionCaptureRefundPositionCollection/null | positions |

### OrderTransactionCaptureRefundPosition [​](#ordertransactioncapturerefundposition)

Refund positions are optional and only there if a refund is position-specific. They relate n `order_transaction_capture_refund_position`s to 1 `order_transaction_capture_refund`.

#### Database table [​](#database-table-2)

| Type | Field name | References |
| --- | --- | --- |
| BINARY(16) | id |  |
| BINARY(16) | refund\_id | order\_transaction\_capture\_refund.id |
| BINARY(16) | line\_item\_id | order\_line\_item.id |
| INT(11) | quantity |  |
| VARCHAR(255) NULL | reason |  |
| LONGTEXT | refund\_amount |  |
| LONGTEXT NULL | custom\_fields |  |

#### Entity [​](#entity-2)

| Type | Property name |
| --- | --- |
| string | id |
| string | refundId |
| string | lineItemId |
| string/null | reason |
| int | quantity |
| float | refundPrice |
| CalculatedPrice | refundAmount |
| array/null | customFields |
| OrderLineItemEntity/null | lineItem |
| OrderTransactionCaptureRefundEntity/null | orderTransactionCaptureRefund |

## Changes to existing entities [​](#changes-to-existing-entities)

### PaymentMethod [​](#paymentmethod)

* Add `refundHandlingEnabled` computed field if payment method handler implements `RefundHandlerInterface`

#### OrderTransaction [​](#ordertransaction)

* Add OneToManyAssociation OrderTransactionCaptureCollection captures

#### OrderLineItem [​](#orderlineitem)

* Add OneToManyAssociation OrderTransactionCaptureRefundPositionCollection|null refundPositions

## State machine [​](#state-machine)

Add 2 new state machines for OrderTransactionCapture and OrderTransactionCaptureRefund.

### OrderTransactionCapture [​](#ordertransactioncapture-1)

We want to add the following states to a new `order_transaction_capture.state` state machine:

* pending
* completed
* failed

### OrderTransactionCaptureRefund [​](#ordertransactioncapturerefund-1)

We want to add the following states to a new `order_transaction_capture_refund.state` state machine:

* open
* in\_progress
* cancelled
* failed
* completed

## PaymentRefundHandlerInterface [​](#paymentrefundhandlerinterface)

Add an interface as outlined below:

php

```shiki
public function refund(string $orderRefundId, Context $context): void;
```

## PaymentRefundProcessor [​](#paymentrefundprocessor)

The PaymentRefundProcessor gets triggered via a corresponding Admin-API action and contains the method `processRefund` as outlined below:

php

```shiki
public function processRefund(string $refundId, Context $context): Response;
```

## Apps [​](#apps)

The whole refund handling should be available for apps and plugins. The following changes are required to allow apps to handle refunds.

### \Shopware\Core\Framework\App\Manifest\Xml\PaymentMethod [​](#shopware-core-framework-app-manifest-xml-paymentmethod)

Add `refundUrl` to the manifest `PaymentMethod`. Also change the xsd accordingly.

### AppRefundHandler [​](#apprefundhandler)

Add an `AppRefundHandler`, which assembles payloads and talks to the app refund endpoint.

### Captures and apps [​](#captures-and-apps)

Captures are written over the Admin-API endpoint.

---

## App scripts

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-10-21-app-scripting.html

# App scripts [​](#app-scripts)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-10-21-app-scripting.md)

## Context [​](#context)

To improve the abilities of Apps, they should be able to execute code synchronously and hook into familiar places like:

* rules
* cart
* storefront page loading
* shipping method calculation
* flow builder extensions

The app system requires that this code is in some way sandboxed, with no direct access to the database or filesystem, and the code is not saved on the server.

Additionally, such a Scripting feature generally improves the capabilities of the AppSystem, this feature is not bound to the AppSystem exclusively, it should be possible to add standalone scripts.

## Decision [​](#decision)

We use Twig as it brings a secure PHP sandbox and allows interacting directly with objects. The scripts will be saved in the database and mapped to a specific scripting event. Scripting events are placed in many sections in Shopware to be able to adjust them. Apps can subscribe to the scripting events by placing their scripts into the correspondingly named folders.

### Scripting Events [​](#scripting-events)

The data passed to the scripts always has to be an object so that the manipulation from Twig can affect the given value. Given objects must be wrapped into custom objects for app scripting to provide easier access to certain functionality and limit the scripting scope. The twig environment will provide additional functions like `dal_search` globally to all events to fetch other data in a consequent way

#### Which objects can be injected into the hooks and which have to be wrapped [​](#which-objects-can-be-injected-into-the-hooks-and-which-have-to-be-wrapped)

In general, it ok to inject `Struct` classes directly into the hooks, as long as those are rather "dumb" data containers (e.g. our DAL entity classes or the storefront page classes). A notable Exception to this rule are `Struct` classes that provide business logic, besides simple getters and setters (e.g. the Cart struct). Those `Structs` and all other `Services` that provide business logic or function that can lead to side effects (DB access, etc.) need to be wrapped into a facade. This will allow us to closely control the interface we want to provide inside the app scripts, to firstly improve developer experience by tailoring the API to the needs of app developers and secondly to ensure that we don't introduce any security issues with the app scripts.

### Scripting execution [​](#scripting-execution)

Each script has its twig environments to improve execution stability. In failure cases, we will throw our exception. The twig environment is reduced to the only set of functionality that is needed; features like block and many template features are disabled. Script loading can happen in multiple implementations, the default implementation will use the object cache to load the scripts and if missing loading it from the database. The compiled scripts will be cached on the filesystem in a separate folder per app and per appVersion. For development purposes, the scripts can be loaded from the filesystem to allow easier development. The default Twig cache will be used for faster code execution.

### Example pseudo-code of the ScriptEventRegistry [​](#example-pseudo-code-of-the-scripteventregistry)

php

```shiki
class ScriptEventRegistry
{
    public const EVENT_PRODUCT_PAGE_LOADED = 'product-page-loaded';

    private $scripts = [];
    private LoggerInterface $logger;
    
    public function execute(string $hook, array $context)
    {
        $scripts = $this->scripts[$hook] ?? [];
        foreach ($scripts as $script) {
            $this->executeScript($script, $context);
        }
    }
    
    private function executeScript(array $script, array $context) 
    {
        $twig = $this->initEnv($script);

        try {
            $twig->render($script['name'], $context);
        } catch (\Throwable $e) {
            throw new ScriptExecutionFailed('Script execution failed', $e);
            $this->logger->error('Execution of script failed', ['context' => $context, 'error' => $e]));
        }
    }
    
    private function initEnv(array $script) 
    {
        $cache = new ConfigurableFilesystemCache($this->cachePath . '/twig/scripts');
        $cache->setConfigHash($script['appName'] . $script['appVersion']);
        
        $twig = new Environment(
            new ScriptLoader([$script['name'] => $script['source']]),
            [
                'cache' => $cache,
            ]
        );
        
        // Setup some custom twig functions
        
        return $twig;
    }
}
```

### Example pseudo-code [​](#example-pseudo-code)

#### Getting discount for high value order [​](#getting-discount-for-high-value-order)

twig

```shiki
{% if cart.price.totalPrice > 500 %}
    {# get discount for high value orders #}
    {% do cart.discount('percentage', 10, 'my_discount_snippet', cart.lineItems) %}
{% endif %}
```

#### Block cart [​](#block-cart)

twig

```shiki
{% if cart.price.totalPrice < 500 %}
    {# allow only carts with high values #}
    {% do cart.block('you have to pay at least 500€ for this cart') %}
{% endif %}
```

### Data Loading [​](#data-loading)

To allow apps to fetch additional data for the storefront, we will introduce PageLoaded-Hooks. Those hooks will orient themself on the Page and PageLoadedEvents already present in the storefront. So for each PageType and PageLoadedEvent we will create a separate Hook class. We will create separate HookClasses and not just one generic class, so we are able to type hint all the dynamic data that is available for that hook. That will improve the developer experience as it allows for autocompletion in the scripts and allows us to generate documentation for the hooks. The hooks will be instantiated and passed to the HookExecutor from the Controllers where the pages are loaded, so we are able to pass additional data if it is needed or makes sense. Additionally, we explicitly decided to not provide CriteriaEvent-Hooks, as that idea is contrary to the direction we may want to go with a separate and specialized data view for the storefront.

### Documentation [​](#documentation)

To ensure app developers can use the full potential of the app scripts, we need to ensure that we document the features of app scripts extensively and make sure that the documentation is always up-to-date. For this reason we decided to generate as much of the documentation as possible, so it never gets outdated, and it's easier to generate full reference (e.g. all hook points that exist with the associated data and available services).

## Consequences [​](#consequences)

* Added script events with the passed arguments need to be supported for a long time
* We will create a new domain-specific way to interact with shopware core domain logic. This means we have to think of and develop a higher-level description of our core domain logic and represent it through new functions that perform domain-specific tasks. For example, the block cart function in the example above. Those domain objects represent the API of the AppScripts, therefore, breaking changes need to be considered carefully and should definitely follow our general breaking change policy. Additionally, the domain-specific layer may allow us to not break the public interface, when the implementation in the underlying services may break, so we can try to ensure even longer compatibility in the domain layer. However, to make evolvability possible at all, we need to inject the shopware version into the context of the app scripts, so that in the app scripts the version can be detected and new features used accordingly.

---

## Preparing data for rule evaluation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-11-02-preparing-data-for-rule-evaluation.html

# Preparing data for rule evaluation [​](#preparing-data-for-rule-evaluation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-11-02-preparing-data-for-rule-evaluation.md)

## Context [​](#context)

When we are creating new `Rule` definitions, we need to consider how we are retrieving the data necessary for the evaluation. Since rules could possibly be evaluated on any given request, the data for the evaluation must also be present at all times. This circumstance causes us to carefully consider the performance with regards to additional database queries or storing the data beforehand.

## Decision [​](#decision)

Instances of `Rule` should always be able to evaluate based on data retrieved from an instance of `RuleScope`. This instance provides getters for `Context`, `SalesChannelContext` and an instance of `\DateTimeImmutable` as the current time. Everything that needs to be evaluated should be derived from methods of these instances.

When the data necessary for evaluation **can't** already be retrieved by the methods of `Context` and `SalesChannelContext`, the **least** favorable option should be to add additional associations to the `Criteria` of DAL searches, e.g. in the `SalesChannelContextFactory`. Unless an additional association is needed anyways and in a much wider scope, the preferred option should always be to use indexers and updater services. Using the indexers, only the data absolutely necessary for evaluation can be stored as part of the target entity's definition. As the data is persisted asynchronously within the message queue, it should be kept up to date by background processes and we can avoid any additional database queries during storefront requests.

## Consequences [​](#consequences)

### Make sure that the `RuleScope` doesn't already provide you with the necessary data to evaluate the rule [​](#make-sure-that-the-rulescope-doesn-t-already-provide-you-with-the-necessary-data-to-evaluate-the-rule)

* If you're trying to match whether the target entity has a specific "ManyToOne" or a "OneToOne" association, use the corresponding `FkField` of the target's definition to match the id of the association.
* If you're trying to match whether the target entity has a specific "ManyToMany" association, use the corresponding `ManyToManyIdField`. If there is no `ManyToManyIdField` for the the association yet and you can evaluate the rule by matching the id of the association, you should always prefer adding a `ManyToManyIdField` to the definition before seeking alternative solutions. If you are adding a `ManyToManyIdField` make sure that the target entity has an indexer and that it calls the `ManyToManyIdFieldUpdater`.

### Writing indexer/updater services for rule evaluation [​](#writing-indexer-updater-services-for-rule-evaluation)

If you absolutely need data other than the id from an association for the rule evaluation, you should create or use an existing service for indexing said data. Consider the following when writing the service for updating indexed fields:

* If the indexed data contains multiple values per entity use a `JsonField` to store it in.
* The updater service should use plain SQL only.
* Make sure the updater service can handle updating a great number of rows at once at the best possible performance.
* Make sure the updater service is also called and updates accordingly on deletion of data upon which the index data is based on.
* If the indexed data also relies on the state of the target entity, make sure the updater service is also called on changes to the target entity and can update the indexed data accordingly.
* If the data to be indexed can be inherited from a parent make sure to also consider that by involving the parent ids in the plain SQL that updates the field containing pre-indexed data.

---

## Adjust ADR approval rules for the new org structure

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-11-05-adjust-adr-approval-rules.html

# Adjust ADR approval rules for the new org structure [​](#adjust-adr-approval-rules-for-the-new-org-structure)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-11-05-adjust-adr-approval-rules.md)

## Context [​](#context)

When we decided to introduce ADRs we also decided that there need to be special approval rules for those ADRs. The approval rules are now outdated after the reorg, so to continuously ensure that the decisions documented in ADRs work in the long run for us, we want to adapt the approval rules.

## Decision [​](#decision)

The old approval rules for reference:

```shiki
*  Two additional developers have to review the ADR
   *  One developer must be a member of the core development team
   *  One developer must be a member of a team, other than the team of the creator
*  One product owner or higher role has to approve an ADR
```

The new approval rule is the following:

* At least one member of each of the Component Teams for the Core, Admin and Storefront area have to review the ADR.

## Consequences [​](#consequences)

ADRs now need to be approved by the new approval rules.

---

## Introduce increment pattern

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-11-09-increment-pattern.html

# Introduce increment pattern [​](#introduce-increment-pattern)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-11-09-increment-pattern.md)

## Context [​](#context)

The current `message_queue_stats` table records which messages are in the message queue and how often. This is done by a subscriber, which then writes a record to the database via the mysql connection. If this record already exists, a duplicate key is triggered and the `count` value of the record will be updated. Systems with many write operations generate a lot of traffic on the message queue. This in turn generates a lot of traffic on the `message_queue_stats` table, resulting in bottlenecks and/or deadlocks.

On another issue, we also provide a feature called `Frequently Used modules` to increase the count everytime an admin module is visited which faces a similar issue.

## Decision [​](#decision)

We introduce a new table `increment` to store these countable information and deprecated `message_queue_stats` table. We create a possibility to control the access to the `increment` table via Redis or another storage, which is optimized for such scenarios. To do this, however, we need to prevent / extend access via the DAL.

So we implement a new gateway with the following methods:

* `increment(string $cluster, string $key): void`
* `decrement(string $cluster, string $key): void`
* `list(string $cluster, int $limit = 5, int $offset = 0): array`
* `reset(string $cluster, ?string $key = null): array`
* `getPool(): string`
* `getConfig(): array`
* `getDecorated(): self`

This then enables the following functional flow:

![](/assets/message_queue_stats.DMz3pvko.png "Message queue stats gateway")

Furthermore, it should also be possible to completely disable the message queue stats or any pool via config file.

You can easily tweak or define new increment pools in config file with your own pool's configuration. For e.g:

yaml

```shiki
shopware:
    increment:
        user_activity:
            type: 'mysql'

        message_queue:
            type: 'redis'
            config:
                url: 'redis://localhost'
        
        custom_pool:
          type: 'array'
```

By default, we ship a Redis, MySQL and array adapter for the gateway. It should be possible to easily switch the adapter via config. If you want to override the default mysql or redis adapter, you need to register your own incrementer gateway in DI container with the id `shopware.increment.<custom_pool>.gateway.<adapter>`

## Consequences [​](#consequences)

* We deprecate the `message_queue_stats` DAL classes
* We deprecate the current `message_queue_stats` endpoint in the api
* We deprecate the `message_queue_stats` services
* We deprecate the `message_queue_stats` table
* We create a new `increment` table
* We implement a new endpoints to work with the new gateway
* We implement a new node for `increment` configuration
* We use the new gateway in the admin for the notifications
* With the next major we remove all deprecations to the `message_queue_stats`.

---

## Merge E2E projects into a single project

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-11-22-merge-e2e-projects-into-a-single-project.html

# Merge E2E projects into a single project [​](#merge-e2e-projects-into-a-single-project)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-11-22-merge-e2e-projects-into-a-single-project.md)

## Context [​](#context)

It's hard to test components in isolation. Other components are almost always also tested, which is intended because it's the nature of end-to-end tests being workflow-based.

There are currently three E2E projects that are maintained separately. There are a lot of duplicated commands and different variations of them.

## Decision [​](#decision)

We'll merge all cypress e2e projects of platform into a single project.

The projects will be merged by

* creating new project `E2E` in `tests/E2E`
* moving storefront tests to `tests/E2E/cypress/integration/storefront`
* moving administration tests to `tests/E2E/cypress/integration/administration`
* moving recovery tests to `tests/E2E/cypress/integration/recovery`
* moving the new package test scenarios to `tests/E2E/cypress/integration/scenarios`
* merging the commands.js files and removing duplicate code
* merging the setup code
* merging fixtures
* use automatic cleanup in global setup instead of manual calls to `cleanUpPreviousState` in admin tests

## Consequences [​](#consequences)

The command and support code are shared by all tests, therefore the ownership of the project itself is now shared among the component teams. The tests themselves should be written and maintained by the solution teams.

The commands to run the e2e tests, and the pipelines need to be updated.

---

## Add possibility for plugins to add a HTML file

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-11-23-add-possibility-for-plugin-to-add-a-html-file.html

# Add possibility for plugins to add a HTML file [​](#add-possibility-for-plugins-to-add-a-html-file)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-11-23-add-possibility-for-plugin-to-add-a-html-file.md)

## Context [​](#context)

The new ExtensionAPI is based on a iFrame communication architecture. The old App system for the admin relies on the XML file. And the normal plugin architecture in the admin is based on component overriding. The ideal way for developing admin extensions will be the ExtensionAPI.

## Decision [​](#decision)

To provide a smooth transition for plugin developer to the new ExtensionAPI which will be introduced soon we need to make sure that plugin can also behave like Apps in the administration. To fulfill this we need to provide a solution to show their own iFrame views. This is now directly possible when the plugin developer adds a `index.html` file to the plugin in the administration folder.

This file will automatically be used by webpack and can be used like a normal web application.

---

## Admin extension API standards

**Source:** https://developer.shopware.com/docs/resources/references/adr/2021-12-07-admin-extension-api-standards.html

# Admin extension API standards [​](#admin-extension-api-standards)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2021-12-07-admin-extension-api-standards.md)

## Context [​](#context)

We need to provide ways for extension developers to add custom components and views to different places in the administration. Multiple solutions where discussed and tested, this ADR contains a summary of the final solution.

## Decision [​](#decision)

### Word definitions [​](#word-definitions)

For a better understanding of the following text it is good to have a definition for specific words:

#### Location [​](#location)

Extensions can render custom views with the Admin-Extension-API via iFrames. To support multiple views in different places every "location" of the iFrame gets a unique ID. These can be defined by the app/plugin developer itself.

*Example:*

An app wants to render a custom iFrame in a card on the dashboard. The "location" of the iFrame has then a specific "locationID" like `sw-dashboard-example-app-dashboard-card`. The app can also render another iFrames which also get "locationIDs". In our example it is a iFrame in a custom modal: `example-app-example-modal-content`.

The app want to render different views depending on the "location" of the iFrame. So the app developer can render the correct view depending on the "locationID":

js

```shiki
if (sw.location.is('sw-dashboard-example-app-dashboard-card')) {
    renderDashboardCard();
}

if (sw.location.is('example-app-example-modal-content')) {
    renderModalContent();
}
```

#### PositionID (PositionIdentifier) [​](#positionid-positionidentifier)

Developers can extend existing areas or create new areas in the administration with the Admin-Extension-API. To identify the positions which the developer want to extend we need a unique ID for every position. We call these IDs "positionID".

*Example:*

An app wants to add a new tab item to a tab-bar. In the administration are many tab-bars available. So the developer needs to choose the correct "positionID" to determine which tab-bar should be extended. In this example the developer adds a new tab item to the tab-bar in the product detail page.

js

```shiki
sw.ui.tabs('sw-product-detail').addTabItem({ ... })
```

### Solution: [​](#solution)

We use the concept of component sections for providing injection points for extension components.

#### Component Sections [​](#component-sections)

In most cases developers will directly use the extension capabilities of the UI components (e.g. adding tab items, adding button to grid, ...). This will cover most needs of many extensions.

To give them more flexibility we introduce a feature named "Component Sections". These are sections where any extension developer can inject components. These components are prebuilt and they can also contain custom render views with iFrames. The developer needs to use the feature and choose the matching positionID for the component position.

js

```shiki
// Adding a card before the manufacturer card with custom fields entries.
sw.ui.componentSection('sw-manufacturer-card-custom-fields__before').add({
    // The Extension-API provides different components out of the box
    component: 'card', 
    // Props are depending on the type of component
    props: {
        title: 'This is the title',
        subtitle: 'I am the subtitle',
        // Some components can render a custom view. In this case the extension can render custom content in the card.
        locationId: 'example-app-card-before-manufactuer-custom-fields-card'
    }
})
```

#### Vue Devtools Plugin for finding the PositionIDs [​](#vue-devtools-plugin-for-finding-the-positionids)

It is impossible to create a list of all potential position IDs. And they would be hard to manage. To solve this problem we are writing a custom plugin for the Vue Devtools. This plugin will be available for Vue Devtools 6+. It makes identifying the position IDs very easy.

Just open the plugin in the Devtools (It is available directly when you open the Administration). Then you can see all positions at the current administration view which are available for extending. If you click at one position ID you get more information about it. Like the property in the Meteor-Extension-SDK so that you directly know what functionality this position has.

In summary: the Devtool plugin provides a visual way to see which parts can be extended and what are the positionIDs for the extension position.

## Consequences [​](#consequences)

We need to implement the componentSectionRenderer to positions where we want to provide an extension position for apps and plugins. These can be positions like before or after cards, at the top or bottom of a page, at the top or bottom of a tab view and many more.

---

## Add feature flag support for Storefront SCSS

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-01-05-add-feature-flag-support-for-storefront-scss.html

# Add feature flag support for Storefront SCSS [​](#add-feature-flag-support-for-storefront-scss)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-01-05-add-feature-flag-support-for-storefront-scss.md)

## Context [​](#context)

* There is no possibility to check for feature flags inside the Storefront SCSS.
* Altering the SCSS depending on a feature flag will require workarounds like e.g. "making up" and additional class in the template and use the feature toggle in twig instead.
  + The SCSS of a selector which is hidden behind a feature flag will still be in the compiled CSS.
* It is not easily possible to make breaking changes inside SCSS functions, mixins or variables backward-compatible with the use of feature flags.

## Decision [​](#decision)

* Add the possibility to check for feature flags inside SCSS, similar to the twig implementation.
* The feature configuration from `Feature::getAll()` is converted to a SCSS map inside `\Shopware\Storefront\Theme\ThemeCompiler::getFeatureConfigScssMap`.
  + This SCSS map is always added to the SCSS string which gets processed by `\Shopware\Storefront\Theme\ThemeCompiler::compileTheme`.
  + For webpack hot-proxy the `var/config_js_features.json` is used instead.
* The SCSS map looks like this: `$sw-features: ("FEATURE_NEXT_1234": false, "FEATURE_NEXT_1235": true);`
  + See <https://sass-lang.com/documentation/values/maps>
* A globally available function `feature()` is used to read inside the SCSS map if a desired feature is active.

Example:

scss

```shiki
body {
    @if feature('FEATURE_NEXT_1') {
        background-color: #ff0000;
    } @else {
        background-color: #ffcc00;
    }
}
```

## Consequences [​](#consequences)

The feature dump file `var/config_js_features.json` is now used by the Storefront webpack configuration `src/Storefront/Resources/app/storefront/webpack.config.js`. When the feature dump cannot be found, all features will be disabled/false inside `webpack.config.js` and hot-proxy SCSS. A warning is shown in this case with the request to execute `bin/console feature:dump` manually.

---

## Allow apps to define custom api endpoints

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-01-06-custom-app-api-endpoints.html

# Allow apps to define custom api endpoints [​](#allow-apps-to-define-custom-api-endpoints)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-01-06-custom-app-api-endpoints.md)

## Context [​](#context)

Apps should be allowed to provide their own API and Store-API and Storefront endpoints where they can execute different logics that deviate from the automatic entity API.

## Decision [​](#decision)

### API [​](#api)

We implement two new endpoints:

* `/api/script/{hook}`.
* `/store-api/script/{hook}`.

The `{hook}` parameter is used as the script hook name and prefixed with the url prefix (`api-`, `store-api-`).

This hook is then executed, and apps have the possibility to load or even write data in the scripts.

The following data is given to the script:

* [array] request.request.all
* [context/sales channel context] context

By default, multiple scripts can be executed on a single hook; however, we will add a `hook.stopPropagation()` method to all API-Hooks, if that was called no further scripts will be executed. Furthermore, we will document that the hook-name the app developer chooses should contain the vendor-prefix to prevent unwanted overrides from other apps.

### Storefront [​](#storefront)

We implement a new endpoint:

* `/storefront/script/{hook}`

The `{hook}` parameter is used as the script hook name and prefixed with the url prefix (`storefront-`).

In this hook, the app can load or write data and either return a script response or render a twig template as a response.

The following data is given to the script:

* [array] request.request.all
* [array] request.query.all
* [sales channel context] context
* [GenericPage] page

#### Response handling [​](#response-handling)

We will add a new `response` service that provides factory methods to create response objects. The returned Response object is a generic wrapper around one of the following responses: `JsonResponse`, `RedirectResponse`, `StorefrontResponse`.

To output the created response, it has to be assigned to the hook:

twig

```shiki
{% do hook.setResponse(response) %}
```

If no response is set, an empty 204 response will be sent as default.

##### Returning a custom JsonResponse [​](#returning-a-custom-jsonresponse)

The json() method allows to specify the data and the http-status code to be returned:

twig

```shiki
{% set response = services.response.json({'data': data}, statusCode) %}
```

##### Redirecting [​](#redirecting)

The redirect() method allows to specify a route and route params, to which should be redirected, and an optional statusCode (302 is default):

twig

```shiki
{% set response = services.response.redirect('routeName', params, statusCode) %}
```

##### Rendering a template [​](#rendering-a-template)

The render() factory allows to pass the template name and the parameters (the page object and additional params) and will perform the `StorefrontController->renderStorefront()`.

twig

```shiki
{% set response = services.response.render('@myApp/storefront/pages/my-custom-page.html.twig', { 'page': hook.page }) %}
```

If it is called outside of a SalesChannelContext (e.g., from an `/api` endpoint) or called on installations that don't have the storefront-bundle installed it will throw an exception.

#### Login Protection [​](#login-protection)

We will add a helper method to the SalesChannelContext to ensure that a customer is logged in before continuing to execute the script. The helper method will check if there is a customer in the current `SalesChannelContext` and will throw an `CustomerNotLoggedInException` if there is no customer logged in.

twig

```shiki
{% do hook.context.ensureLogin() %}
```

#### Caching [​](#caching)

Our script response wrapper allows modifying the caching strategies for the responses.

twig

```shiki
{% do response.cache.invalidationState('logged-in', 'cart-filled') %}
{% do response.cache.maxAge(7200) %}
{% do response.cache.disable() %}
{% do response.cache.tag('my-manufacturer-tag-' ~ manufacturerId, 'another-tag') %}
```

By default all /storefront and /store-api routes are cached, so caching it is opt-out for those routes. For the /api routes caching is not supported, if you provide cache configuration on the response of those routes, it will be ignored.

For individual cache invalidation, we add a new `cache-invalidation`-hook point. That hook-point is a hook on the general EntityWrittenContainerEvent. The app can analyze the write payload of the event and use a cache-invalidation service to invalid the cache for a given tag.

We will wrap the EntityContainerEvent, so scripts are forced to specify the entity for which they want to inspect the write payload. Instead of providing the raw payload, we will provide a fluid, functional interface which allows to filter for entityIds that match some criteria.

twig

```shiki
{% set ids = hook.event.getIds('manufacturer') %}
{% set ids = ids.only('upated') %} // only update events
{% set ids = ids.with(['name', 'url']) %}  // with name OR url cahnge

{% set ids = hook.event.get('manufacturer').only('upated').with(['name', 'url']) %} // same as above but chained

{% if ids.empty %}
    {% return %}
{% endif %}

{% set tags = [] %}
{% for id in ids %}
    {% set tags = tags|merge(['my-manufacturer-tag-' ~ id]) %}
{% endfor %}

{% do services.cache.invalidate(tags) %}
```

#### No XML-config [​](#no-xml-config)

App-Scripts in general and custom api endpoints in particular work without further configuration inside the manifest.xml file. We prefer solutions inside the scripts over a solution that would require additional configuration in the xml file. The reason is that everything regarding app scripts is in one place inside the app itself, namely the `Resources/scripts` folder. Additionally, the manifest.xml can get outdated which may lead to confusing errors, and in general, the structure of the xml file is more limited than the possibilities we have in the app scripts itself.

#### SEO-Urls [​](#seo-urls)

We won't add seo urls in this iteration, the reason is that that feature is pretty complex, and we don't know yet if the feature would be used at all or not. Additionally, a feature like that would add a heavy maintenance burden because of the tight coupling to the general seo\_url solution, and we just don't know yet if the feature brings more value

We also dropped the idea of custom-routes aka the (static) seo urls light alternative, because it is an overly specific solution

We prefer more general solutions, as we can't anticipate all use cases the app developers may have, and we can't possibly build a custom solution for every use case they may have. Therefore, we will create a separate ticket/ADR to add lifecycle scripts to the app scripts. A script like that could be used to add entries into the seo\_url table with aliases for the script routes but is not limited to that use case. It will greatly simplify the use case that on installation of the app something should be changed/added in the DB of the shop (the current way to go would be to add a webhook on the app\_install event and build an external service that in turn uses the api to change stuff, we would eliminate the need of the external server)

---

## Feature flags for major versions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-01-20-feature-flags-for-major-versions.html

# Feature flags for major versions [​](#feature-flags-for-major-versions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-01-20-feature-flags-for-major-versions.md)

## Context [​](#context)

Feature flags enable the developer to create new code which is hidden behind the flag and merge it into the trunk branch, even when the code is not finalized. We use this functionality to merge breaks into the trunk early, without them already being switched active.

## Decision [​](#decision)

We will use feature flags for major versions to hide new code that will be introduced in the next major version. We have only one feature flag in our core sources: `v6.5.0.0`. This feature flag is used for the breaks mentioned above.

## Consequences [​](#consequences)

We will use the static functions of the Feature class to check if a feature is active or not. And only hide code for the next major version behind the feature flag.

### Activating the flag [​](#activating-the-flag)

To switch flags on and off, you can use the ***.env*** to configure each feature flag. Using dots inside an env variable is not allowed, so we use underscore instead:

bash

```shiki
V6_5_0_0=1
```

### Using flags in PHP: [​](#using-flags-in-php)

The feature flag can be used in PHP to make specific code parts only executable when the flag is active.

### Using flags in methods [​](#using-flags-in-methods)

When there is no option via the container, you can use additional helper functions:

php

```shiki
use Shopware\Core\Framework\Feature;
 
class ApiController
{
  public function indexAction(Request $request)
  {
    // some old stuff
    Feature::ifActive('v6.5.0.0', function() use ($request) {
      // awesome stuff
    });
    // some old stuff
  }
}
```

And you can use it for conditions:

php

```shiki
use Shopware\Core\Framework\Feature;
 
class ApiController
{
  public function indexAction(Request $request)
  {
    // some old stuff
    if (Feature::isActive('v6.5.0.0')) {
      //awesome new stuff
    }
    // some old stuff
  }
}
```

And you can use it simply to throw exceptions:

php

```shiki
use Shopware\Core\Framework\Feature;
 
/**
 * @deprecated tag:v6.5.0 - Class is deprecated, use ... instead
 */
class ApiController
{
  public function indexAction(Request $request)
  {
     Feature::triggerDeprecationOrThrow('v6.5.0.0', 'Class is deprecated, use ... instead');
  }
}
```

### Using flags in tests [​](#using-flags-in-tests)

You can flag a test by using the corresponding helper function. This can also be used in the `setUp()` method.

php

```shiki
use Shopware\Core\Framework\Feature;
 
class ProductTest
{
  public function testNewFeature() 
  {
     Feature::skipTestIfActive('v6.5.0.0', $this);

     // test code
  }
}
```

### Using flags in the administration: [​](#using-flags-in-the-administration)

Also in the JavaScript code of the administration the flags can be used in various ways.

### Using flags for modules [​](#using-flags-for-modules)

You can also hide complete admin modules behind a flag:

javascript

```shiki
Module.register('sw-awesome', {
    flag: 'v6.5.0.0',
    ...
});
```

### Using flags in JavaScript [​](#using-flags-in-javascript)

To use a flag in a VueJS component you can inject the feature service and use it.

```shiki
inject: ['feature'],
...
featureIsActive(flag) {
    return this.feature.isActive(flag);
},
```

### Using flags in templates [​](#using-flags-in-templates)

When you want to toggle different parts of the template you can use the flag in a VueJs condition if you injected the service in the module:

html

```shiki
<sw-field type="text" v-if="feature.isActive('v6.5.0.0')"></sw-field>
```

### Using flags in config.xml [​](#using-flags-in-config-xml)

When you want to toggle config input fields in config.xml like [basicInformation.xml](https://gitlab.shopware.com/shopware/6/product/platform/-/blob/trunk/src/Core/System/Resources/config/basicInformation.xml), you can add a `flag` element like this:

xml

```shiki
<input-field type="bool" flag="v6.5.0.0">
  <name>showTitleField</name>
  <label>Show title</label>
  <label lang="de-DE">Titel anzeigen</label>
  <flag>v6.5.0.0</flag>
</input-field>
```

### Using flags in the storefront: [​](#using-flags-in-the-storefront)

In the Storefront it works nearly similar to the admin.

### Using flags in storefront JavaScript [​](#using-flags-in-storefront-javascript)

```shiki
import Feature from 'src/helper/feature.helper';
...
data() {
   if (Feature.isActive('v6.5.0.0')) {
        console.log('v6.5.0.0 is active')
   }
 };
```

### Using flags in storefront templates [​](#using-flags-in-storefront-templates)

```shiki
{% if feature('v6.5.0.0') %}
    <span>Feature is active</span>
{% endif %}
```

### Using flags in plugins: [​](#using-flags-in-plugins)

Feature flags can also be used in plugins.

### Major feature flag [​](#major-feature-flag)

As mentioned before, we use the major feature flags (`v6.5.0.0`, `v6.6.0.0`) to signal breaks within the code ahead of time. This is an incredible help in the preparation of the next major release, as otherwise all breaks would have to be made within a short period of time.

This procedure can also be applied to plugins, which also use this flag and internally query it to either prepare the plugin for the next major or to support multiple Shopware major versions with one plugin version. Since each major feature flag remains after the corresponding release, they can be used as an alternative version switch to the php equivalent `version_compare`.

---

