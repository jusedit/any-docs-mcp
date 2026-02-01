# Resources References Adr Part3

*Scraped from Shopware Developer Documentation*

---

## Flow storer with scalar values

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-02-flow-storer-with-scalar-values.html

# Flow storer with scalar values [​](#flow-storer-with-scalar-values)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-02-flow-storer-with-scalar-values.md)

## Context [​](#context)

At the moment we have a bunch of different `FlowStorer` implementations. Most of them are used to store scalar values without any restore logic. Each of the Storer class has an own interface which is used to identify if the data of the event should be stored. This leads to much boilerplate code when adding new storer implementations or when plugins want to bypass some for events.

## Decision [​](#decision)

We introduce a generic `ScalarValuesAware` interface which can be used to store simple values which should be simply stored and restored one to one:

php

```shiki
interface ScalarValuesAware
{
    public const STORE_VALUES = 'scalar_values';
    
    /** @return array<string, scalar|null|array> */
    public function getValues(): array;
}
```

This event can be used in different events which needs a simple storage logic:

php

```shiki
class SomeFlowAwareEvent extends Event implements ScalarStoreAware, FlowEventAware
{
    public function __construct(private readonly string $url) { }

    public function getValues(): array
    {
        return ['url' => $this->url];
    }
}
```

To store and restore this data, we provide a simple `FlowStorer` implementation:

php

```shiki
class ScalarValuesStorer extends FlowStorer
{
    public function store(FlowEventAware $event, array $stored): array
    {
        if (!$event instanceof ScalarValuesAware) return $stored

        $stored[ScalarValuesAware::STORE_VALUES] = $event->getValues();

        return $stored;
    }

    public function restore(StorableFlow $storable): void
    {
        $values = $storable->getStore(ScalarValuesAware::STORE_VALUES);
        foreach ($values as $key => $value) {
            $storable->setData($key, $value);
        }
    }
}
```

## Consequences [​](#consequences)

* It is no more necessary to implement storer classes to just store and restore scalar values.
* We deprecate all current `Aware` interface and `Storer` classes which can simply replaced by this new implementation
  + Following storer and interfaces will be deprecated:
    - ConfirmUrlStorer > ConfirmUrlAware
    - ContactFormDataStorer > ContactFormDataAware
    - ContentsStorer > ContentsAware
    - ContextTokenStorer > ContextTokenAware
    - DataStorer > DataAware
    - EmailStorer > Email Aware
    - MailStorer > Mail Aware
    - NameStorer > NameAware
    - RecipientsStorer > RecipientsAware
    - ResetUrlStorer > ResetUrlAware
    - ReviewFormDataStorer > ReviewFormDataAware
    - ShopNameStorer > ShopNameAware
    - SubjectStorer > SubjectAware
    - TemplateDataStorer > TemplateDataAware
    - UrlStorer > UrlAware
* Affected events will be updated to use the new `ScalarStoreAware` interface.
* Existing `*Aware` events will stay in the event implementation and will be marked as deprecated.
* Developers can much easier store and restore values without providing a lot of boilerplate code.
* Deprecated classes will be removed in v6.6.0.0
* All interface and storer logic will remain until the next major and has to be compatible with each other

---

## Follow test pyramid

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-13-follow-test-pyramid.html

# Follow test pyramid [​](#follow-test-pyramid)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-13-follow-test-pyramid.md)

## Context [​](#context)

Since the beginning of the development of shopware 6 we've tried to test as much as possible. Most of the effort went into writing integration or end-to-end tests. This has led to two main issues

### 1. Performance [​](#_1-performance)

E2E tests and integration tests to some degree are slow by nature because they perform a lot of steps to assert required conditions. The e2e test suite has grown over the lifetime of shopware 6 to take more than 6 hours of real-time if executed in serial.

### 2. Flakiness [​](#_2-flakiness)

Because these tests involve a lot of moving parts, most of these tests are not deterministic and behave a little differently on every execution. This leads to flakiness, which is sometimes hard to reproduce because it depends on the performance/load of the machine that is executing the test.

The flakiness in combination with the number of tests, the performance, the complex test matrix, and the merge trains have led to distrust in the test suite and caused a lot of hassle. Especially, when there are many merge requests to be merged, it's very frustrating for pipelines to fail due to flakiness.

## Decision [​](#decision)

We commit to following the best practice of the [test pyramid](https://martinfowler.com/articles/practical-test-pyramid.html). Our testing structure currently is a reversed pyramid. We're using too many E2E and too few unit tests to test our code base. To get closer to this ideal, we'll cut all E2E tests that can be covered by jest tests or are better implemented as php integration tests/api tests.

## Consequences [​](#consequences)

*Coverage will decrease*

* some bugs might slip through that might have been caught by a deleted e2e tests. But this is not very likely  
   because most tests that were deleted do not test features as whole but just mostly admin modules that do crud operations.

*Test pyramid*:

* we have to write more unit tests
* we'll delete all e2e tests that just cover things that can be tested by jest or php integration tests
* we'll write jest tests for basic stuff that was covered by the deleted e2e tests (mostly crud stuff)
* we'll only add E2E tests that actually test an important feature end to end

*Quality*:

* we'll only add high quality E2E tests
* we'll test them thoroughly, before merging them (at least 50 times)

*Performance*:

* we'll refactor tests to not require a database reset after each test case. We'll also reconsider moving to playwright
* we'll reduce or disable test retries in e2e, to fight performance creep
* we'll move tests into quarantine as fast as possible

---

## Unstructured ADRs

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-20-unstructured-adrs.html

# Unstructured ADRs [​](#unstructured-adrs)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-20-unstructured-adrs.md)

## Context [​](#context)

Currently, our ADRs are grouped into folders according to different areas. We have added this structure to help people find their way around when they are looking for specific ADRs.

However, there are different approaches when searching for ADRs:

1. I am looking for an ADR and I know the headline.
2. I would like to read the latest ADRs
3. I would like to see ADRs for a specific area.
4. ...

The structuring by areas is good for case 3, but not for the other two. In the first case, the user can easily use the search via the directory to use the appropriate ADR, but will also get duplicate matches. Depending on the keyword the result can be quite long.

In the second case, I would like to read the latest ADRs, the user would have to go to git history, which is only possible via shell or IDE.

## Decision [​](#decision)

We will remove the area structure on directory level and introduce front matter in our ADRs as we already do in our changelog files. This makes it possible to extract metadata from content. Additionally, it can be used as groundwork, if we want to release our ADRs in different front-ends (handbook, dev-docs) and use the front-end's search functionalities. With front matter and the flat file structure, you can solve all three problems described in this ADR. An example of this specific ADR would be:

markdown

```shiki
---
title: Unstructured ADRs
date: 2023-02-23
area: Product Operation #I added prod-ops because this is a workflow topic
tags: [ADR, file structure, workflow]
---
```

We also hope that this will make it easier for people to submit ADRs without being confused about which folder to put the file in.

---

## Native extension system with vue

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-27-native-extension-system-with-vue.html

# Native extension system with vue [​](#native-extension-system-with-vue)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-27-native-extension-system-with-vue.md)

## Context [​](#context)

Our current plugin extension system for the administration is based on our Component Factory. This factory generates native Vue components at runtime based on a base Shopware component which can be extended or overwritten by plugins. This approach offers flexibility to plugin developers to modify every component. For the template part, we use Twig.JS and compile the Vue template in the client at runtime.

However, this approach has its drawbacks. We cannot use the full power of Vue and its ecosystem because everything related to Vue is wrapped with our factories and generated at runtime. We cannot use Vue tools without custom modifications, like linting template files, providing good static analysis, and more. The other downside is that upgrading Vue is challenging, and the performance suffers because we cannot precompile components.

To address these issues, we aimed to test a new idea with Vue 3, which includes all the features of the existing plugin approach, but developed using only native Vue tools. This would offer several benefits, like using the full power of Vue, better performance, better static analysis, and more.

Our main idea for the template part was to use native Vue components named sw-block that can replace the Twig.JS template part. Plugin developers can extend or overwrite the sw-block component as needed.

html

```shiki
<sw-block name="sw-hello-world">
<div>Hello World</div>
</sw-block>
```

For the script and logic part, we aimed to use the Composition API. Before returning all the component data and methods, we would provide a hook point for plugins so they could modify or inject everything they want.

js

```shiki
// The original component
<script setup lang="ts">
// Hook for providing extensibility
useExtensibility();
</script>

// The plugin component
<script lang="ts">
    import SwOrignal from './sw-original.vue';
    // use our extensibility helpers
    import { useComponentExtender, getPropsFromComponent } from 'sw-vue-extensbiles';
    
    const myCustomData = ref('test');
    
    export default {
        name: 'sw-extended-component',
        props: {
            ...getPropsFromComponent(SwOrignal)
        },
        setup(props, context) {
            return {
                ...useComponentExtender(SwOrignal, props, context),
                myCustomData
            }   
        }
}
</script>
```

However, during the evaluation and testing, we realized that this approach was not feasible due to several reasons. The most critical challenges were that it was hard to merge data because the Vue compiler optimizes many parts of the component, and it was not easy to pass all the data of the component to the block system to give plugin developers full access to the original component's data.

To solve these problems, we would need to use internal Vue logic, which is not update-safe and could break with every Vue update.

## Decision [​](#decision)

After considering the challenges we faced with the proposed solution, we concluded that we couldn't find solutions without using internal Vue logic. Given this situation, we did not see any significant benefits to adopting a native Vue solution over our current plugin system, which, despite its challenges, has proven to work well for our use case.

Therefore, we decided to stick with our current plugin system for the administration until new possibilities arise in Vue that solve our problems.

## Consequences [​](#consequences)

We will continue to use the current plugin system for the administration and not switch to a native Vue solution.

---

## Admin text editor evaluation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-03-27-admin-text-editor-evaluation.html

# Admin text editor evaluation [​](#admin-text-editor-evaluation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-03-27-admin-text-editor-evaluation.md)

## Context [​](#context)

The current sw-text-editor in the administration has numerous low-level bugs in basic WYSIWYG features. It is built in a way that is difficult to maintain and understand. Therefore, we require a new text editor that is easy to maintain, has a good feature set, is flexible to extend and more stable.

## Decision [​](#decision)

Building a new text editor from scratch is not a viable option. Therefore, we have evaluated various existing text editors and narrowed down our options to the following:

```
- CKEditor 5
- TinyMCE
- QuillJS
- Prosemirror
- TipTap V2
- Lexical
```

We have decided to skip CKEditor 5 and TinyMCE because they require a license for our use case and are not 100% open source. Prosemirror was also ruled out because it provides only a low-level API and requires much more implementation time than the other editors. Additionally, Lexical is not a valid option for us since it is specialized for React environments and has no official support for VueJS.

The remaining two editors are TipTap V2 and QuillJS. Both have similar feature sets and APIs, but we have found some major differences between them. The first difference is that TipTap is a headless editor, which means that it only provides the editor logic and requires a UI implementation. QuillJS, on the other hand, is a fully featured editor that provides a UI out of the box. In our case, it is better to use a headless editor like TipTap because we can implement the UI to fit our needs, especially for several edge cases that are hard to implement in QuillJS.

The second major difference is in extensibility. TipTap's API is more flexible, allowing us to implement our own features using the existing TipTap and ProseMirror plugins or build our own plugins. In most cases, the powerful main TipTap API can already solve most of our use cases. QuillJS, on the other hand, is not as flexible as TipTap, and its extension system is more complicated to use.

The third big difference is in stability. We found that TipTap is more stable than QuillJS, probably because TipTap is built on top of ProseMirror, which is a very stable and well-tested editor. Although QuillJS is also generally stable, other developers have reported some issues with it in the past.

Our main decision driver was the extensibility of the editor. We want a text editor that is easy to extend and allows us to implement our own features. TipTap provides a powerful extension system that is easy to use, and we can implement our design without overwriting an existing design of other editors. Therefore, we have decided to use TipTap as the base of our new text editor.

## Consequences [​](#consequences)

We need to replace our current sw-text-editor with the new editor. We have chosen TipTap as the base for our new text editor,which means that we need to implement the existing UI to the editor and implement all current features. While some features have already been implemented during the evaluation in a short amount of time, the most challenging part will be to ensure backward compatibility.

---

## Mocking repositories

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-04-01-mocking-repositories.html

# Mocking repositories [​](#mocking-repositories)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-04-01-mocking-repositories.md)

## Context [​](#context)

Right now it is complicated to test classes which have a dependency on a repository. This is because mocking a repository `search` or `searchIds` call requires creating empty `EntitySearchResults` or `IdSearchResults`. This leads to much boilerplate code when writing tests and faking database results. For this reason we should provide a way to mock the `search` and `searchIds` calls in a much easier way.

Faking a search result of a repository looks like this at the moment:

php

```shiki
$result = new EntitySearchResult(
    'my-entity',
    1,
    new EntityCollection([]),
    null,
    new Criteria(),
    Context::createDefaultContext()
);

$entityRepository = $this->createMock(EntityRepository::class);
$entityRepository
    ->expects(static::once())
    ->method('search')
    ->willReturn($result);
```

## Solution [​](#solution)

We created a `\Shopware\Tests\Unit\Common\Stubs\DataAbstractionLayer\StaticEntityRepository` which allows the developer to easily fake repository search results.

### How to use [​](#how-to-use)

php

```shiki
<?php

class SomeCoreClass
{
    public function __construct(private EntityRepository $repository) {}
    
    public function foo() 
    {
        $criteria = new Criteria();
        
        $result = $this->repository->search($criteria, $context);
        
        // ...
    }
}

class SomeCoreClassTest extends TestCase
{
    public function testFoo() 
    {
        $repository = new StaticEntityRepository([
            new UnitCollection([
                new UnitEntity(),
                new UnitEntity(),
            ])
        ]);
        
        $class = new SomeCoreClass($repository);
        
        $class->foo();
        
        // some assertions
    }
}
```

The `StaticEntityRepository` constructor accepts an array of `EntitySearchResults`, `EntityCollections` or `AggregationResultCollection`. The value is the result of the search or one of the supported collections.

### Other configurations [​](#other-configurations)

php

```shiki
<?php

class SomeCoreClassTest extends TestCase
{
    public function testFoo() 
    {
        $repository = new StaticEntityRepository([
            new UnitCollection([
                new UnitEntity(),
            ]),
            new AggregationResultCollection([
                new AvgResult('some-aggregation', 12.0),
            ]),
            new EntitySearchResult(
                'entity', 
                1, 
                new EntityCollection(), 
                new AggregationResultCollection(), 
                new Criteria(), 
                Context::createDefaultContext()
            ),
            [Uuid::randomHex(), Uuid::randomHex(), Uuid::randomHex()]       
            new IdSearchResult(0, [], new Criteria(), Context::createDefaultContext()),
        ]);
        
        $class = new SomeCoreClass($repository);
        
        $class->foo();
        
        // some assertions
    }
}
```

---

## Disable the CSS autoprefixer in the Storefront by default

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-04-03-disable-css-autoprefixer.html

# Disable the CSS autoprefixer in the Storefront by default [​](#disable-the-css-autoprefixer-in-the-storefront-by-default)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-04-03-disable-css-autoprefixer.md)

## Context [​](#context)

The storefront CSS, compiled by `scssphp/scssphp`, is currently automatically prefixed with vendor prefixes using `padaliyajay/php-autoprefixer`. However, the generated prefixes no longer add much value since the browser support has been updated with the Bootstrap v5 update. Most of the prefixes are unnecessary for the supported browsers in .browserslist. Unfortunately, the `theme:compile` process experiences a significant decrease in performance due to the auto-prefixer, which is particularly problematic in our SaaS solution. Moreover, the `padaliyajay/php-autoprefixer` package does not work dynamically and fails to consider `.browserslist` while applying the appropriate vendor-prefixes. This package hard-codes the CSS properties that require prefixing, making it an unsustainable long-term solution. To demonstrate this, a table containing all automatic prefixes generated by `padaliyajay/php-autoprefixer` is provided below.

### Current browser support [​](#current-browser-support)

```shiki
>= 0.5%
last 2 major versions
not dead
Chrome >= 60
Firefox >= 60
Firefox ESR
iOS >= 12
Safari >= 12
not Explorer <= 11
```

### Current auto-prefixes [​](#current-auto-prefixes)

✅ = Fully covered by current browser support. The prefix is not used by the browser.  
 ⚠️ = Not fully covered by current browser support. Please read the notes.

#### Current auto-prefixes for Webkit [​](#current-auto-prefixes-for-webkit)

| CSS property | Vendor prefix | Support | Notes | Can I use |
| --- | --- | --- | --- | --- |
| box-reflect | -webkit-box-reflect | ⚠️ No Firefox support | No cross-browser support was possible using prefixing only | <https://caniuse.com/?search=box-reflect> |
| column-count | -webkit-column-count | ✅ Full support |  | <https://caniuse.com/?search=column-count> |
| column-gap | -webkit-column-gap | ✅ Full support |  | <https://caniuse.com/?search=column-gap> |
| column-rule | -webkit-column-rule | ✅ Full support |  | <https://caniuse.com/?search=column-rule> |
| clip-path | -webkit-clip-path | ⚠️ Partial support | Prefix was needed in Safari 7-13 and iOS 7-12.5 | <https://caniuse.com/?search=clip-path> |
| user-select | -webkit-user-select | ✅ Full support |  | <https://caniuse.com/?search=user-select> |
| appearance | -webkit-appearance | ✅ Full support |  | <https://caniuse.com/?search=appearance> |
| animation | -webkit-animation | ✅ Full support |  | <https://caniuse.com/?search=animation> |
| transition | -webkit-transition | ✅ Full support |  | <https://caniuse.com/?search=transition> |
| transform | -webkit-transform | ✅ Full support |  | <https://caniuse.com/?search=transform> |
| transform-origin | -webkit-transform-origin | ✅ Full support |  | <https://caniuse.com/?search=transform-origin> |
| backface-visibility | -webkit-backface-visibility | ✅ Full support |  | <https://caniuse.com/?search=backface-visibility> |
| perspective | -webkit-perspective | ✅ Full support |  | <https://caniuse.com/?search=perspective> |
| background-clip | -webkit-background-clip | ⚠️ Partial support | Value "text" needs prefix. Non-standard method of clipping a background image to the foreground text | <https://caniuse.com/?search=background-clip> |
| filter | -webkit-filter | ✅ Full support |  | <https://caniuse.com/?search=filter> |
| font-feature-settings | -webkit-font-feature-settings | ✅ Full support |  | <https://caniuse.com/?search=font-feature-settings> |
| flow-from | -webkit-flow-from | ⚠️ No support | Was supported in WebKit and IE, implementing the feature is no longer being pursued by any browser | <https://caniuse.com/?search=flow-from> |
| flow-into | -webkit-flow-into | ⚠️ No support | Was supported in WebKit and IE, implementing the feature is no longer being pursued by any browser | <https://caniuse.com/?search=flow-into> |
| hyphens | -webkit-hyphens | ⚠️ Partial support | Safari and iOs need prefix. Value "auto" has full support | <https://caniuse.com/?search=hyphens> |
| mask-image | -webkit-mask-image | ✅ Full support | Prefixed values for gradients (-webkit-linear-gradient) were needed. Later, support for unprefixed values was added. | <https://caniuse.com/?search=mask-image> |
| mask-repeat | -webkit-mask-repeat | ⚠️ Partial support | Chrome and Edge need prefix. | <https://caniuse.com/?search=mask-repeat> |
| mask-position | -webkit-mask-position | ⚠️ Partial support | Chrome and Edge need prefix. | <https://caniuse.com/?search=mask-position> |
| mask-size | -webkit-mask-size | ⚠️ Partial support | Chrome and Edge need prefix. | <https://caniuse.com/?search=mask-size> |
| display: flex | display: -webkit-flex | ✅ Full support |  | [https://caniuse.com/?search=display%3A flex](https://caniuse.com/?search=display%3A%20flex) |
| display: inline-flex | display: -webkit-inline-flex | ✅ Full support |  | [https://caniuse.com/?search=display%3A inline-flex](https://caniuse.com/?search=display%3A%20inline-flex) |
| position: sticky | position: -webkit-sticky | ⚠️ Partial support | Safari 7.1 - 12.1 needed prefix. Afterwards full unprefixed support | [https://caniuse.com/?search=display%3A inline-flex](https://caniuse.com/?search=display%3A%20inline-flex) |
| ::placeholder | ::-webkit-input-placeholder | ✅ Full support |  | <https://caniuse.com/?search=%3A%3Aplaceholder> |
| ::file-selector-button | ::-webkit-file-upload-button | ✅ Full support |  | <https://caniuse.com/?search=%3A%3Afile-selector-button> |
| keyframes | -webkit-keyframes | ✅ Full support |  | <https://caniuse.com/?search=keyframes> |

#### Current auto-prefixes for Mozilla [​](#current-auto-prefixes-for-mozilla)

| CSS property | Vendor prefix | Support | Notes | Can I use |
| --- | --- | --- | --- | --- |
| column-count | -moz-column-count | ✅ Full support |  | <https://caniuse.com/?search=column-count> |
| column-gap | -moz-column-gap | ✅ Full support |  | <https://caniuse.com/?search=column-gap> |
| column-rule | -moz-column-rule | ✅ Full support |  | <https://caniuse.com/?search=column-rule> |
| user-select | -moz-user-select | ✅ Full support |  | <https://caniuse.com/?search=user-select> |
| appearance | -moz-appearance | ✅ Full support |  | <https://caniuse.com/?search=appearance> |
| font-feature-settings | -moz-font-feature-settings | ✅ Full support |  | <https://caniuse.com/?search=font-feature-settings> |
| hyphens | -moz-hyphens | ✅ Full support |  | <https://caniuse.com/?search=hyphens> |
| ::placeholder | ::-moz-placeholder | ✅ Full support |  | <https://caniuse.com/?search=placeholder> |
| :placeholder-shown | :-moz-placeholder-shown | ✅ Full support |  | <https://caniuse.com/?search=%3Aplaceholder-shown> |

## Decision [​](#decision)

* Due to the above points we have decided to disable the CSS auto-prefixing by default.
* In case it is still needed, to support older browsers or some special CSS property from the table above, it can still be activated via the config key `storefront.theme.auto_prefix_css` in `Storefront/Resources/config/packages/storefront.yaml`. However, we recommend to do a manual prefix inside the SCSS instead.
* We will deprecate the auto-prefixing for v6.6.0 and only use SCSS compiling
* We do not consider the deactivation of the auto-prefixing as a hard breaking change because:
  + Most prefixes are not needed due to current browser support.
  + Some prefixes are for CSS properties which are no longer implemented and developed by browsers.
  + Prefixes which are still valid are primarily cosmetic/appearance properties which are very unlikely to affect the Storefronts functionality.

## Consequences [​](#consequences)

When compiling the themes SCSS with `theme:compile`, the vendor-prefixes are no longer applied by default to the `all.css`.

---

## New language inheritance mechanism for opensearch

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-04-11-new-language-inheritance-mechanism-for-opensearch.html

# New language inheritance mechanism for opensearch [​](#new-language-inheritance-mechanism-for-opensearch)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-04-11-new-language-inheritance-mechanism-for-opensearch.md)

## Context [​](#context)

Currently, when using Elasticsearch for searching on storefront, we are creating multiple indexes of each language. This would be fine till now however there are a few problems with it:

* We need to manage multiple indexes, if the shop's using multilingual, we need to create several indexes for each language, this is a big problem on cloud especially
* "Indices and shards are therefore not free from a cluster perspective, as there is some level of resource overhead for each index and shard."
* Everytime a record is updated, we need to update that record in every language indexes
* There's currently no fallback mechanism when searching, therefor duplicating default language data for each index is needed, but not every field is translatable, this take more storage for each index

## Decision [​](#decision)

### New feature flag [​](#new-feature-flag)

We introduce a new feature flag `ES_MULTILINGUAL_INDEX` to allow people to opt in to the new multilingual ES index immediately.

### New Elasticsearch data mapping structure [​](#new-elasticsearch-data-mapping-structure)

We changed the approach to Multilingual fields strategy following these criteria

1. Each searchable entity now have only one index for all languages (e.g sw\_product)
2. Each translated field will be mapped as an `object field`, each language\_id will be a key in the object
3. When searching for these fields, use multi-match search with <translated\_field>.<context\_lang\_id>, <translated\_field>.<parent\_current\_lang\_id> and <translated\_field>.<default\_lang\_id> as fallback, this way we have a fallback mechanism without needing duplicate data
4. Same logic applied when sorting with the help of a painless script (see 3.Sorting below)
5. When a new language is added or a record is update, we do a partial update instead of replacing the whole document, this will reduce the request update payload and thus improve indexing performance overall

Example:

### 1. Create mapping setting [​](#_1-create-mapping-setting)

**OLD structure**

json

```shiki
// PUT /sw_product
{
    "mappings": {
        "properties": {
            "productNumber": {
                "type": "keyword"
            },
            "name": {
                "type": "keyword",
                "fields": {
                    "text": {
                        "type": "text"
                    },
                    "ngram": {
                        "type": "text",
                        "analyzer": "sw_ngram_analyzer"
                    }
                }
            }
        }
    }
}
```

**NEW structure**

json

```shiki
// PUT /sw_product/_mapping
{
    "mappings": {
        "properties": {
            "productNumber": {
                "type": "keyword"
            },
            "name": {
                "properties": {
                    "en": {
                        "type": "keyword",
                        "fields": {
                            "text": {
                                "type": "text",
                                "analyzer": "sw_english_analyzer"
                            },
                            "ngram": {
                                "type": "text",
                                "analyzer": "sw_ngram_analyzer"
                            }
                        }
                    },
                    "de": {
                        "type": "keyword",
                        "fields": {
                            "text": {
                                "type": "text",
                                "analyzer": "sw_german_analyzer"
                            },
                            "ngram": {
                                "type": "text",
                                "analyzer": "sw_ngram_analyzer"
                            }
                        }
                    }
                }
            }
        }
    }
}
```

### 2. Searching [​](#_2-searching)

Assume we're searching products in german

json

```shiki
// GET /sw_product/_search
{
  "query": {
    "multi_match": {
      "query": "some keyword",
      "fields": [
          "title.de.search", // context languge
          "title.en.search" // fallback language
      ],
      "type": "best_fields" 
    }
  }
}
```

### 3. Sorting [​](#_3-sorting)

We add new painless scripts in `Framework/Indexing/Scripts/translated_field_sorting.groovy` and `Framework/Indexing/Scripts/numeric_translated_field_sorting.groovy`, this script then will be used when sorting

**Example: Sort products by name in DESC**

json

```shiki
// GET /sw_product/_search
{
    "query": {
      ...
    },
    "sort": [
        {
            "_script": {
                "type": "string",
                "script": {
                    "id": "translated_field_sorting",
                    "params": {
                        "field": "name",
                        "languages": [
                            "119317f1d1d1417c9e6fb0059c31a448", // context language
                            "2fbb5fe2e29a4d70aa5854ce7ce3e20b" // fallback language
                        ]
                    }
                },
                "order": "DESC"
            }
        }
    ]
}
```

## Adding a new language [​](#adding-a-new-language)

* When a new language is created, we perform this request to update mapping includes new added language

json

```shiki
// PUT /sw_product/_mapping
{
    "properties": {
        "name": {
            "properties": {
                "<new_language_id>": {
                    "type": "keyword",
                    "fields": {
                        "text": {
                            "type": "text",
                            "analyzer": "<new_language_stop_words_analyzer>"
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": "sw_ngram_analyzer"
                        }
                    }
                }
            }
        }
    }
}
```

## Consequences [​](#consequences)

* From the next major version, old language based indexes will not be used any longer thus could be removed on es cluster
* When the feature is activated, the shop must reindex using command `bin/console es:index` in the next update

---

## Jest test files should be JavaScript only

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-04-14-jest-test-files-should-be-javascript-only.html

# Jest test files should be JavaScript only [​](#jest-test-files-should-be-javascript-only)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-04-14-jest-test-files-should-be-javascript-only.md)

## Context [​](#context)

There is a mix of both JavaScript and TypeScript Jest test files in the Administration. Respectively `*.spec.js` and `*.spec.ts` files. We want to settle on one format, to keep it uniform.

### Current distribution [​](#current-distribution)

There are 46 `*.spec.ts` and 620 `*.spec.js` files.

### Known problems with TypeScript Jest test files [​](#known-problems-with-typescript-jest-test-files)

* The TypeScript eslint `no-unused-vars` rule is broken in Jest test files
* There is no type safety for components, because `vue-test-utils` will just type to `any` Vue component
* Several editors loose the Jest context for `*.spec.ts` files
* The Jest config only adds globals to `*.spec.js` files
* TypeScript linting was disabled for `*.spec.ts` files, therefore they are more like `*.spec.js` files

## Decision [​](#decision)

Accounting the current distribution and the known problems we face with `*.spec.ts` files, we decided to use `*.spec.js` files from now on.

## Consequences [​](#consequences)

All existing `*.spec.ts` where moved to `*.spec.js` files and TypeScript specific code was removed. Additionally to prevent new `*.spec.ts` files an eslint rule was added which prevents new files to be added.

---

## Optimize cart cleanup

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-09-optimise-cart-cleanup.html

# Optimize cart cleanup [​](#optimize-cart-cleanup)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-09-optimise-cart-cleanup.md)

## Context [​](#context)

The existing SQL snippet to delete the outdated cart entries doesn't use any database index to narrow down entries that can be deleted. On high traffic shops this leads to SQL query times larger than 30 seconds to find and remove these database entries.

Running

```shiki
EXPLAIN DELETE FROM cart
WHERE (updated_at IS NULL AND created_at <= '2023-02-01')
   OR (updated_at IS NOT NULL AND updated_at <= '2023-02-01') LIMIT 1000;
```

shows that the original sql query doesn't use an index (`possible_keys` = `NULL`)

## Decision [​](#decision)

Reorder the query parameters so that the relevant cart entries can be narrowed down by an indexed field.

Testing the new SQL snippet by running

```shiki
EXPLAIN DELETE FROM cart
        WHERE created_at <= '2023-02-01'
          AND (updated_at IS NULL OR updated_at <= '2023-02-01') LIMIT 1000;
```

shows that the new query uses an index (`possible_keys` = `idx.cart.created_at`).

## Consequences [​](#consequences)

The logic stays the same but the amount of time needed to find the record drops dramatically, so the change results in a better performance during cart cleanup.

---

## Experimental features

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-10-experimental-features.html

# Experimental features [​](#experimental-features)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-10-experimental-features.md)

## Context [​](#context)

Currently, it is hard to publish features in an early state to gather feedback regarding those features. If they are useful, what needs to be improved etc. One major reason is that everything we publish (that is not marked as internal) is part of our backwards compatibility promise, thus changing foundational parts of features is quite hard after first release. That leads to features being developed over quite some time without getting actual feedback from users or being able to release them, as they need to be implemented to a pretty final state in order to confidently release them in a stable manner, where we will keep backwards compatibility.

This at the same time also means that the current approach is not beneficial to our ecosystem, whom the whole backwards compatibility promise should benefit, because the features are built behind closed curtains they can't chime in with ideas and use cases regarding extendability, etc.

Examples of features that could benefit from an earlier experimental release:

* B2B:
  + We could release the multi account B2B feature with a "simple" employee management system first, and then add the more complex budget management or access control on top of that later.
* Advanced Search:
  + We could release a first version of the new advanced search feature, without all configuration options and customizability that we might envision.

In both cases, releasing the first increments of the features without an "experimental"-flag would mean that we would have to keep backwards compatibility for the whole feature, even if we later decide to change the implementation of the feature, thus making the development of the feature harder. Also in getting feedback from the customers what additional functionalities are needed after we released the first foundational increment of the feature, we can base our further prioritization on real customer feedback. Thus, we can ship business value sooner to our customers and lower the risk of building the wrong thing.

## Decision [​](#decision)

To ship features earlier, we add the concept of "experimental" features, thus giving early access to meaningful increments of features that are still in active development. That means in particular that there is no backwards compatibility promise for experimental features, thus we can change the implementation as is needed, without having to worry about breaking changes. We mark the code for those features with a new `experimental` annotation, to make it clear on code level that the API is **not yet** stable. For code where already expect that it should never become part of the public API we will use the `@internal` annotation directly, to make sure that even if the feature is stable we will continue to tread those parts of the code as internal and not keep backwards compatible. Everything that is marked with `@experimental` is designed to be part of the public API, when the feature is stable.

At the same time, it offers a way for the ecosystem to give early feedback on the feature, as well as to test it in their own projects. Especially, extension developers can check how they might want to integrate and extend the feature being built, and thus suggest the needed extension points during the development process. To make this possible that means that there also will be documentation (API docs, dev docs and user docs) for experimental features

All experimental features are developed with a specific target version, beginning with that version, the feature is considered stable, and the APIs will be kept backwards compatible. This means that `experimental` annotation/attribute have to be removed, before the version can be released. Because it is hard to estimate exactly with which release a feature may be stable (as it also depends on the feedback we get) it makes sense to mark them as being stable with the next major version. That does not mean that the feature won't be finished and stable earlier (we can remove the experimental status with any minor version), it only means that at the latest with that version it is considered stable, this prevents a situation where a lot of features stay in the experimental state for a long time.

### Our experimental promise [​](#our-experimental-promise)

Experimental features don't compromise in terms of quality or any other guidelines we have, that means experimental features are production ready. While the UI and processes and functionalities of a single feature may change considerably during the experimental phase, we won't discard any data that was generated when the feature was actively used in a previous stage, meaning that even if there are changes to the underlying data, we will migrate the existing data. This ensures that customers using an early version of the feature can continue working with that feature.

As said earlier experimental features do not hone our backwards compatibility promise, allowing us to react more flexibly to the feedback we gather based on the earlier iterations of the feature.

### Killing a feature [​](#killing-a-feature)

It may happen that during development of a feature we get the feedback that our feature idea does not provide the value we expected, if that is the case we may kill a feature again. If that is the case, we will mark the feature as deprecated for the next major version, so even if the feature was marked as experimental and does not fall under the backwards compatible promise we will not remove a experimental feature with a minor version. We will only kill the feature for the next major version, and announce the deprecation as soon as possible.

This is also important as features can't stay in the experimental state forever, that means either they are further developed to a stable state, or they are killed to the next major version.

### How does this compare to the "old" feature flag approach? [​](#how-does-this-compare-to-the-old-feature-flag-approach)

With the old feature flag approach work-in-progress code was hidden with a feature flagging mechanism. That meant that code that was not production ready was in the released product, but it was turned off via flag. Experimental features are neither work in progress, nor finished and finalized features. Whatever is included in an experimental feature is production ready and ready to use for customers, but it may mean that not all functionalities we envision for a feature are ready yet, but those that are can be used standalone.

# Do you have to opt-in to experimental features or are they always there? [​](#do-you-have-to-opt-in-to-experimental-features-or-are-they-always-there)

From a technical perspective, experimental features are always there and they can not be deactivated. This reduces the number of permutations of the system and greatly reduces the overall complexity and thus makes testing, etc. a lot easier. From the perspective of an external developer, this makes things also more predictable, as externals can rely on the feature being there in a given version, independent of the specific systems configuration, thus it will help in getting real feedback from the ecosystem.

From a merchants/users perspective, this might not be the case and it might be beneficial for them that some early features are opt-in only. But as already detailed in the [UI section](#UI) this ADR does not focus on the UI and merchants perspective and leaves that open for a future ADR. However when the decision will be made to make certain features opt-in for the user we should always built it in a way that only the UI of the new feature is hidden, but from the technical perspective the whole feature is always there. The opt-in then only makes the entry point to the new feature visible for the user.

## Consequences [​](#consequences)

### Core [​](#core)

We add a `@experimental` annotation, that can be used similar as the `@internal` annotation, to indicate parts of the code (class or method level) that are not yet stable, and thus not covered by the backwards compatibility promise.+ Additionally all `@experimental` annotation need to have a `stableVersion` property when the feature will be made available as stable at the latest, e.g. `@experimental stableVersion:v6.6.0`. This means that at the latest with that major version the feature should be stable (or removed), however the `@experimental` annotation can always be removed earlier. As experimental features can be considered as technical debt, we should strive to stabilize features as soon as possible. When a feature can not be stabilized for the targeted major version, the experimental phase can be extended on a case by case basis.

There will be a static analysis rule / unit test, that checks that every `@experimental` annotation has the stable version property and there are no `@experimental` annotations for a version that is already released (similar to the test case we have for `@deprecated`). Additionally, the BC checker needs to be adapted to handle the `@experimental` annotation in the same way as it handles `@internal`.

We use an annotation here over an attribute because of the following reasons:

* Similarity to other annotations like `@deprecated` and `@internal`
* Symfony also uses an `@experimental` annotation, see [this example](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/Webhook/Client/AbstractRequestParser.php#LL23C5-L23C17) and their [documentation for experimental code](https://symfony.com/doc/current/contributing/code/experimental.html)
* The same annotation can be used for PHP, JS and template code
* We don't need to evaluate the annotation at runtime, so using attributes over annotations won't bring that much benefit

### Database Migrations [​](#database-migrations)

As said earlier data from experimental features needs to be migrated if the underlying structure changes, so that no customer data is lost. But additionally, we also provide a blue/green compatible migration system, this means that all destructive changes to the DB layout (e.g. dropping a table or column) can only be done in a major version and can not happen immediately. As blue/green compatibility is a overall system property we can't exclude `@experimental` features from that.

### API [​](#api)

API routes and also entity definitions (that automatically will be mapped to the auto-generated CRUD-API) can be marked as experimental, meaning that they are also not covered by the backwards compatibility promise. The experimental state then will be reflected in the OpenAPI definition for those routes. To do so add the `Experimental` tag to the OpenApi definition of the route and add a hint that that route currently still is experimental in the summary for that route, and use the `@experimental` annotation on the entity definition class.

### Admin [​](#admin)

Modules, Components, Services, etc. can be marked as experimental, meaning that they are not covered by the backwards compatibility promise.

js

```shiki
/**
 * @experimental stableVersion:v6.6.0
 */
Component.register('sw-new-component', {
    ...
});
```

### Storefront [​](#storefront)

Blocks, SCSS classes, JS plugins etc. can be marked as experimental, meaning that they are not covered by the backwards compatibility promise.

In twig blocks can be wrapped as being experimental:

twig

```shiki
{# @experimental stableVersion:v6.6.0 #}
{% block awesome_new_feature %}
   ...
{% endblock %}
```

In addition to that, we can also mark the whole template as experimental:

twig

```shiki
{# @experimental stableVersion:v6.6.0 #}
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}
```

### UI [​](#ui)

This concept does not deal with how experimental features may be displayed to the merchant on UI level. While the concepts are overlapping, we keep them separate, this ADR only answers the technical side and should enable teams developing features to work in a incremental and iterative way, without being able to revisit early decisions (because they are covered by our BC promise) and without the need to use a long-lived feature branch.

As far as this ADR is concerned the UI part, there is by default no way for a merchant to distinguish between experimental and stable features. If that is needed can be decided individually per feature or in general in a separate ADR. Those considerations should not hinder us from starting to use the `@experimental` annotation as explained here.

### Commercial [​](#commercial)

For commercial the same thing applies as for platform itself. There is no difference in how we handle experimental core features and experimental commercial features.

### Docs [​](#docs)

Experimental features will be documented. This includes Dev docs, API docs and user docs. As we want to encourage the use of the features for end-users, they have to understand how the feature works under the hood. For external developers, documentation for experimental features is also important, as they can check how they might want to integrate and extend the feature being built, and thus suggest the needed extension points during the development process. In the docs it will also be marked that the features are experimental and that the APIs and user interface is not yet stable.

### Roadmap [​](#roadmap)

The experimental status of features should also be reflected in the roadmap. That means that for a given feature, the progress in the roadmap can have a progress of 30% but already released in an experimental state. In that case, the version where it was made available as experimental should be shown in the roadmap. When a feature is completed, it leaves the experimental state and all features that are displayed under "released" in the roadmap are stable.

### Automated checks [​](#automated-checks)

We will add the following automated checks to ensure that the `@experimental` annotation is used correctly:

* Static analysis rule / unit test, that checks that every `@experimental` annotation has the stable version property and there are no `@experimental` annotations for a version that is already released (similar to the test case we have for `@deprecated`).
* The BC checker will be adapted to handle the `@experimental` annotation in the same way as it handles `@internal`.
* The API schema generator will be adapted to add the `Experimental` tag to all auto-generated CRUD-routes if the entity definition is marked as experimental.
* The test that checks that all API routes have OpenApi specification also checks that the route is marked as experimental in the documentation when the route or controller method is marked as experimental.

this ADR was supplemented in [Add Feature property to `@experimental` annotation](./2023-09-06-feature-property-for-experimental-anotation.html)

---

## Stock Manipulation API

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-15-stock-api.html

# Stock Manipulation API [​](#stock-manipulation-api)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-15-stock-api.md)

## Context [​](#context)

The stock handling in Shopware 6 is currently not very flexible and does not support many common use cases.

* It's not possible to easily replace the loading of stocks with a custom implementation, for example one that communicates with an ERP.
* It's not possible to easily modify how stock is increased/decreased throughout the order lifecycle.
* Available stock calculation is very slow on large catalogs.
* Stock is stored as two distinct values: stock and available stock. This is due to the fact that stock is not reduced until an order is set as completed. Therefore, the available stock is calculated as the stock minus all open orders. This is unnecessarily complex.

## Decision [​](#decision)

We have only one field `stock` in the product definition which always has a real time calculated value.

The `stock` value should be correctly updated as an order and its line items transition through the various states. Eg, stock is decremented when an order is placed. If it is cancelled, the stock is increased, and so on.

We have a clear API for manipulating stock which can be extended and supports arbitrary data, which could, for example, support features such as multi warehouse inventory.

We have a way to disable the stock handling behavior of Shopware.

### New feature flag [​](#new-feature-flag)

We introduce a new feature flag `STOCK_HANDLING` to allow people to opt in to the new stock handling behavior immediately. In 6.6 the flag will be removed and the new stock handling will be activated by default.

### Abstract Stock Storage [​](#abstract-stock-storage)

We will introduce a new `AbstractStockStorage`. The API will be as follows:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Product\Stock;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

#[Package('inventory')]
abstract class AbstractStockStorage
{
    abstract public function getDecorated(): self;

    /**
     * This method provides an extension point to augment the stock data when it is loaded.
     *
     * This method is called when loading products via:
     * * \Shopware\Core\Content\Product\SalesChannel\Detail\AvailableCombinationLoader
     * * \Shopware\Core\Content\Product\Stock\LoadProductStockSubscriber
     *
     * This data will be set directly on the products, overwriting their existing values. Furthermore, the keys specified below and any extra data will be added
     * as an array extension to the product under the key `stock_data`.
     */
    abstract public function load(StockLoadRequest $stockRequest, SalesChannelContext $context): StockDataCollection;

    /**
     * This method should be used to update the stock value of a product for a given order item change.
     *
     * @param list<StockAlteration> $changes
     */
    abstract public function alter(array $changes, Context $context): void;

    /**
     * This method is executed when a product is created or updated. It can be used to perform some calculations such as update the `available` flag based on the new stock level.
     *
     * @param list<string> $productIds
     */
    abstract public function index(array $productIds, Context $context): void;
}
```

With a few DTOs:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Product\Stock;

use Shopware\Core\Framework\Log\Package;

#[Package('inventory')]
class StockDataCollection
{
    public function add(StockData $stock): void

    public function getStockForProductId(string $productId): ?StockData

    /**
     * @return array<StockData>
     */
    public function all(): array
    {
    }
}
```

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Product\Stock;

use Shopware\Core\Framework\Log\Package;
use Shopware\Core\Framework\Struct\Struct;

#[Package('inventory')]
final class StockData extends Struct
{
    public function __construct(
        public readonly string $productId,
        public readonly int $stock,
        public readonly bool $available,
        public readonly ?int $minPurchase = null,
        public readonly ?int $maxPurchase = null,
        public readonly ?bool $isCloseout = null,
    ) {
    }

    public static function fromArray(array $info): self
    {
    }
}
```

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Product\Stock;

use Shopware\Core\Framework\Log\Package;

#[Package('core')]
final class StockAlteration
{
    public function __construct(
        public readonly string $lineItemId,
        public readonly string $productId,
        public readonly int $quantityBefore,
        public readonly int $newQuantity
    ) {
    }

    public function quantityDelta(): int
    {
    }
}
```

The `alter` method receives a list of changes. Each change corresponds to a line item change. It contains the line item ID, the product ID and the before and after quantity of the line item.

This API encapsulates all the scenarios an order may transition through.

### Introduce a new `BeforeWriteEvent` event [​](#introduce-a-new-beforewriteevent-event)

We will introduce a new event to the `EntityWriteGateway` service. Much like `BeforeDeleteEvent` it will be dispatched before any commands are written. It allows for subscribers to add success and error callbacks via the methods:

* `public function addSuccess(\Closure $callback): void`
* `public function addError(\Closure $callback): void`

These callbacks will be executed after the writes have been written to the database and if/when an error occurs, respectively.

### Update `\Shopware\Core\Content\Product\DataAbstractionLayer\ProductIndexer` [​](#update-shopware-core-content-product-dataabstractionlayer-productindexer)

We update `\Shopware\Core\Content\Product\DataAbstractionLayer\ProductIndexer` to depend on `\Shopware\Core\Content\Product\DataAbstractionLayer\AbstractStockStorage` as well as `Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdater`.

If `STOCK_HANDLING` is enabled then we call the `\Shopware\Core\Content\Product\DataAbstractionLayer\AbstractStockStorage::index` method with the IDs of the product which have changed.

Otherwise, we call `Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdater::update`

### Deprecate `Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdater` [​](#deprecate-shopware-core-content-product-dataabstractionlayer-stockupdater)

It will be removed with 6.6.

### Introduce `Shopware\Core\Content\Product\Stock\OrderStockSubscriber` [​](#introduce-shopware-core-content-product-stock-orderstocksubscriber)

We introduce a new subscriber which listens to the various required events and interacts with `\Shopware\Core\Content\Product\DataAbstractionLayer\AbstractStockStorage` via it's new API (`alter`).

All of Shopware's internal business rules for handling stock are located in this subscriber.

The subscriber listens to various events and calls `\Shopware\Core\Content\Product\DataAbstractionLayer\AbstractStockStorage::alter` with the appropriate changesets for the following scenarios:

* An order was placed (all items will have a before quantity of 0 and a new quantity reflective of the amount ordered)
* An order was cancelled (all items will have a before quantity of the amount ordered and a new quantity of 0)
* An order was reopened (all items will have a before quantity of 0 and a new quantity reflective of the amount ordered)
* An order item was added (before quantity of 0 and a new quantity reflective of the amount ordered)
* An order item was removed (before quantity of the amount ordered and a new quantity of 0)
* An order item quantity was updated (before and new quantity represent the old and new quantity)
* An order item product was changed (two changes: First: old product with before quantity of the amount ordered and a new quantity of 0. Second: new product with before quantity of 0 and a new quantity reflective of the amount ordered)

It is possible to disable Shopware's internal stock handling by setting the configuration `shopware.stock.enable_stock_management` to false.

### Introduce new core stock storage implementation. [​](#introduce-new-core-stock-storage-implementation)

We introduce a new implementation of `\Shopware\Core\Content\Product\DataAbstractionLayer\AbstractStockStorage` for managing the stock levels. It is responsible for incrementing/decrementing stock values based on the provided changesets.

The new APIs will directly increment and decrement the `stock` column on the `product` table rather than using `available_stock`. Therefore, the `stock` value will always be a realtime representation of the available stock.

The `alter` method will directly update the stock values based on the given deltas in the changesets.

The new implementation solves the issue of the current slow stock calculation process which works like so:

* `stock` vs `available_stock` is the difference between orders in progress and completed orders.
* `available_stock` is calculated from the `stock` value minus open order quantities. This calculation is preformed in `Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdater::updateAvailableStockAndSales`. It is slow because the `SUM` may run over millions of rows.

### Deprecate StockUpdater Filters [​](#deprecate-stockupdater-filters)

We will deprecate all stock update filters. They will be removed in 6.6.

The same behaviour can be implemented with decorators.

The following classes will be deprecated:

* \Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdate\AbstractStockUpdateFilter
* \Shopware\Tests\Unit\Core\Content\Product\DataAbstractionLayer\StockUpdate\TestStockUpdateFilter
* \Shopware\Commercial\MultiWarehouse\Domain\Order\ExcludeMultiWarehouseStockUpdateFilter
* \Shopware\Core\Content\Product\DataAbstractionLayer\StockUpdate\StockUpdateFilterProvider

### `ProductDefinition` updates [​](#productdefinition-updates)

In Shopware version 6.6 or if the `STOCK_HANDLING` feature flag is enabled:

* The `availableStock` field is made write protected and will be updated to directly mirror the `stock` value.

We decide not to remove the `availableStock` field, simply deprecating it with no plan to remove. This is because many integrations rely on this field and it is simple for us to maintain as a mirror of `stock`.

To mirror the value we implement a new listener `AvailableStockMirrorSubscriber` for the `BeforeWriteEvent` event. It simply updates the payload, copying any `stock` value updates to the `available_stock` field.

### Update stock loading to use `AbstractStockStorage::load` [​](#update-stock-loading-to-use-abstractstockstorage-load)

We update the various locations in Shopware where stock is loaded and augment the product with any stock information that is loaded from the stock storage.

This includes:

* \Shopware\Core\Content\Product\Subscriber\ProductSubscriber::salesChannelLoaded
* \Shopware\Core\Content\Product\SalesChannel\Detail\AvailableCombinationLoader::load

Pseudocode for setting the values on the product looks like:

php

```shiki
$product->setStock($stock->stock);
$product->setAvailable($stock->available);

// optional values
$product->setMinPurchase($stock->minPurchase ?? $product->get('minPurchase'));
$product->setMaxPurchase($stock->maxPurchase ?? $product->get('maxPurchase'));
$product->setIsCloseout($stock->isCloseout ?? $product->get('isCloseout'));

// really flexible for projects
$product->addExtension('stock_data', $stock);
```

However, in order to support this API, we must update `\Shopware\Core\Content\Product\SalesChannel\Detail\AvailableCombinationLoader::load` because it currently does not pass along the `SalesChannelContext` which is necessary for `AbstractStockStorage::load`.

Therefore, we deprecate `load` in `AbstractAvailableCombinationLoader` for 6.6 and introduce:

`public function loadCombinations(string $productId, SalesChannelContext $salesChannelContext): AvailableCombinationResult`.

It is introduced as not abstract and throws a deprecation error if called (eg when the method is not implemented in concrete implementations) in 6.6, otherwise it forwards to `load`. It will be made abstract in 6.6.

`AvailableCombinationLoader` implements the new `loadCombinations` method and `load` is deprecated for 6.6.

Finally, `ProductConfiguratorLoader` is updated to call `loadCombinations` instead of `load`.

### Stock changing scenarios [​](#stock-changing-scenarios)

The following table contains all the scenarios that should trigger stock changes. All implementations of `AbstractStockStorage` should be able to handler these scenarios.

| Scenario | Items Before | Items After | Before Stock Values | After Stock Values | Diff |
| --- | --- | --- | --- | --- | --- |
| Order placed | N/A | Product 1: 10 Product 2: 5 | Product 1: 100 Product 2: 55 | Product 1: 90 Product 2: 50 | Product 1: -10 Product 2: -5 |
| Order cancelled | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 5 | Product 1: 90 Product 2: 50 | Product 1: 100 Product 2: 55 | Product 1: +10 Product 2: +5 |
| Cancelled Order -> Open | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 5 | Product 1: 100 Product 2: 55 | Product 1: 90 Product 2: 50 | Product 1: -10 Product 2: -5 |
| Line Item Added -> Product 3 | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 8 Product 3: 1 | Product 1: 90 Product 2: 50 Product 3: 5 | Product 1: 90 Product 2: 47 Product 3: 4 | Product 2: -3 Product 3: -1 |
| Line Item Removed -> Product 3 | Product 1: 10 Product 2: 8 Product 3: 1 | Product 1: 10 Product 2: 8 | Product 1: 90 Product 2: 47 Product 3: 4 | Product 1: 90 Product 2: 50 Product 3: 5 | Product 3: +1 |
| Line Item Updated -> Product 2 qty increased | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 8 | Product 1: 90 Product 2: 50 | Product 1: 90 Product 2: 47 | Product 2: -3 |
| Line Item Updated -> Product 2 qty decreased | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 1 | Product 1: 90 Product 2: 50 | Product 1: 90 Product 2: 54 | Product 2: +4 |
| Line Item Updated -> P2 changed to P3 | Product 1: 10 Product 2: 5 | Product 1: 10 Product 3: 5 | Product 1: 90 Product 2: 50 Product 3: 10 | Product 1: 90 Product 2: 55 Product 3: 5 | Product 2: +5 Product 3: -5 |
| Non cancelled order deleted | Product 1: 10 Product 2: 5 | Product 1: 10 Product 2: 5 | Product 1: 90 Product 2: 50 | Product 1: 100 Product 2: 55 | Product 1: +10 Product 2: +5 |

It is the role of `Shopware\Core\Content\Product\Stock\OrderStockSubscriber` to listen to the required shopware events for these scenarios and then interact with the stock storage implementation.

1. Order placed: The product stock should be reduced by the order line item qties. (`BeforeWriteEvent` -> No items will exist pre insertion, so we know it's a decrement operation)
2. Order cancelled: The product stock should be increased by the order line item qties. (`StateMachineTransitionEvent -> $event->getToPlace()->getTechnicalName() === OrderStates::STATE_CANCELLED`)
3. Order reopened: The product stock should be reduced by the order line item qties. (`StateMachineTransitionEvent -> $event->getFromPlace()->getTechnicalName() === OrderStates::STATE_CANCELLED`)
4. Order item added: The product stock should be reduced by the new order line item qty. (`BeforeWriteEvent` -> filter for order line item writes and diff old and new state)
5. Order item removed (Status: Any non cancelled): The product stock is increased by the old order line item qty. (`BeforeWriteEvent` -> filter for order line item writes and diff old and new state)
6. Order item qty increased (Status: Any non cancelled): The product stock should be decreased by the difference between the old and new qty. (`BeforeWriteEvent` -> filter for order line item writes and diff old and new state)
7. Order item qty decreased (Status: Any non cancelled): The product stock should be increased by the difference between the old and new qty. (`BeforeWriteEvent` -> filter for order line item writes and diff old and new state)
8. Order item product changed (Status: Any non cancelled): The old product stock should be increased by the old qty. The new product stock should be decreased by the new qty. (`BeforeWriteEvent` -> filter for order line item writes and diff old and new state)

## Consequences [​](#consequences)

* By creating an abstract class, we can maintain a consistent interface for stock updating while allowing for different implementations.
* New inventory management strategies can be easily added by creating new concrete classes that extend `AbstractStockStorage`.
* Developers working with the inventory management system can be confident that any concrete implementation of the `AbstractStockStorage` will provide the required methods for handling stock updates.
* Developers wanting to completely remove and rewrite the inventory management logic can completely disable the `OrderStockSubscriber` and implement their own solution.

---

## Use PHP 8.1 Enums

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-16-php-enums.html

# Use PHP 8.1 Enums [​](#use-php-8-1-enums)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-16-php-enums.md)

## Context [​](#context)

As of Shopware 6.5 the minimum version of PHP is 8.1. We would like to promote the usage of PHP Enums.

Enums are useful where we have a predefined list of constant values. It's now not necessary to provide values as constants, and it's not necessary to create arrays of the constants to check validity.

## Decision [​](#decision)

All new code which needs to represent a collection of constant values should now use Enums.

A few examples might be:

* Product Types (Parent, Variant)
* Product Status (Enabled, Disabled)
* Backup Type (Full, Incremental)

Where possible, we should migrate existing constant lists to use Enums. See the following Migration Strategy:

## Backwards Compatibility / Migration Strategy [​](#backwards-compatibility-migration-strategy)

To migrate a list of constant values, where an API accepts a "type" parameter which should exist in the list of constant values we can use the [Expand & Contract pattern](https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html) to migrate in a backwards compatible manner:

Consider the following example:

php

```shiki
class Indexer
{
    public const PARTIAL = 'partial';
    public const FULL = 'full';

    public function product(int $id, string $method): void
    {
        if (!in_array($method, [self::PARTIAL, self::FULL], true)) {
            throw new \InvalidArgumentException();
        }
    
        match ($method) {
            self::PARTIAL => $this->partial($id),
            self::FULL => $this->full($id)
        };
    }
}
```

Step 1: Create the ENUM & Accept in API as well as string. For this step it is necessary to maintain the allowed values in both the constants and the ENUM:

Note: In PHP 8.1 we cannot assign directly an ENUM to a constant. For the future, it is worth noting that this is supported in PHP 8.2 with backed ENUMS: `public const PARTIAL = IndexMethod::PARTIAL->value;`

php

```shiki
enum IndexMethod
{
    case PARTIAL;
    case FULL;
}

class Indexer
{ 
    public function product(int $id, IndexMethod|string $method): void
    {
       ...
    }
}
```

Step 2: Create ENUM from primitive type if string value passed:

Note: If your ENUM is backed with a value you can use `BackedEnum::from` to perform automatic casting and validation. Otherwise you will need to map the values manually.

php

```shiki
class Indexer
{
    public const PARTIAL = 'partial';
    public const FULL = 'full';

    public function product(int $id, IndexMethod|string $method): void
    {
        if (is_string($method)) {
            $method = match ($method) {
                'partial' => IndexMethod::PARTIAL,  
                'full' => IndexMethod::FULL,
                default => throw new \InvalidArgumentException()
            };
        }

        match ($method) {
            IndexMethod::PARTIAL => $this->partial($id),
            IndexMethod::FULL => $this->full($id)
        };
    }
}
```

Step 3: Deprecate the constants and passing primitive values in the method:

php

```shiki
class Indexer
{
    // @deprecated tag:v6.6.0 - Constant will be removed, use enum IndexMethod::PARTIAL
    public const PARTIAL = 'partial';
    // @deprecated tag:v6.6.0 - Constant will be removed, use enum IndexMethod::FULL
    public const FULL = 'full';

    /**
     * @deprecated tag:v6.6.0 - Parameter $method will not accept a primitive in v6.6.0
     */
    public function product(int $id, IndexMethod|string $method): void
    {
        if (is_string($method)) {
            $method = match ($method) {
                'partial' => IndexMethod::PARTIAL,  
                'full' => IndexMethod::FULL,
                default => throw new \InvalidArgumentException()
            };
        }

        match ($method) {
            IndexMethod::PARTIAL => $this->partial($id),
            IndexMethod::FULL => $this->full($id)
        };
    }
}
```

Step 4: Remove deprecations in next major.

Which leaves us with the following, succinct code:

php

```shiki
enum IndexMethod
{
    case PARTIAL;
    case FULL;
}

class Indexer
{
    public function product(int $id, IndexMethod $method): void
    {
        match ($method) {
            IndexMethod::PARTIAL => $this->partial($id),
            IndexMethod::FULL => $this->full($id)
        };
    }
}

(new Indexer())->product(1, IndexMethod::PARTIAL);
```

---

## Switch to UUIDv7

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-22-switch-to-uuidv7.html

# Switch to UUIDv7 [​](#switch-to-uuidv7)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-22-switch-to-uuidv7.md)

## Context [​](#context)

Using UUIDs as primary keys eases the integration of several different data sources, but it also brings some performance issues.

Currently, we're using UUIDv4, which is a random UUID the completely random prefix means that the B-tree indexes of the database are not very efficient.

UUIDv7 time-based prefix is less spread than that of UUIDv4, this helps the database to keep the index more compact. It allows the Index to allocate fewer new pages and to keep the index smaller.

## Decision [​](#decision)

Considering there is little risk to using UUIDv7, as v4 and v7 share the same length and are indistinguishable for shopware, we can switch to v7 without any risk of breaking anything.

The effort is also very low as we only need to change the implementation of the `Uuid` class. As using UUIDv7 will improve the speed of bulk product inserts by about 8 %, we think the effort is worth the measurable and theoretical gain.

## Consequences [​](#consequences)

We will switch to UUIDv7 as default and add performance guides promoting v7.

---

## Exception Log Level configuration

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-05-25-exception-log-levels.html

# Exception Log Level configuration [​](#exception-log-level-configuration)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-05-25-exception-log-levels.md)

## Context [​](#context)

By default, every exception that is thrown in the PHP stack and not caught will be logged by the `symfony/monolog-bridge` on `error` level. But there are some cases where the exception is caused by clients accessing the API wrong (missing fields etc.) and throwing an `ShopwareHttpException` with an HTTP-Status-Code of 40x is our way of handling such situations and returning a correct HTTP-Status-Code to the client. So those cases are in fact no "errors" that need to be analyzed, but are expected given a malformed API request. Logging those cases as "errors" produces a lot of noise, which makes it harder to actually find errors in the logs.

For our cloud product, we already used a configuration list that configures that some Exception classes should only be logged as notices.

## Decision [​](#decision)

We add a configuration to the platform that degrades the error level of specific exceptions to notices. This way, external hosters can also profit from our classification. We use [symfony's `exceptions` configuration](https://symfony.com/doc/current/reference/configuration/framework.html#exceptions) for this.

This has the benefit that for specific projects this configuration could be adjusted, for example, for cases where you also control all clients that access the shop, you may want to log also every client error, just to help debugging the client.

Another solution could be to do the configuration of the log level directly in the exception class either by attributes or a separate method specifying the log level, but that would make overwriting it for a specific project harder, so we stick to the default symfony configuration.

## Consequences [​](#consequences)

We will add the `exceptions` configuration to the platform, that way the error logging in existing projects might change. But in general, we assume that this change is for the better.

Additionally, we will need to extend on the default symfony configuration as that is not compatible with our new [domain exceptions](./2022-02-24-domain-exceptions.html) as there are multiple exception cases in one file/class. Therefore, we will add a similar configuration option, that does not rely on the FQCN, but instead we will use the shopware specific `error code` from the shopware exception as that is unique to the exception case.

On a side note, we should be able to get rid of most of the cloud-specific configuration for the exception logging mapping.

---

## Client side communication to App Server

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-06-27-store-api-to-app-server.html

# Client side communication to App Server [​](#client-side-communication-to-app-server)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-06-27-store-api-to-app-server.md)

## Context [​](#context)

Right now only Shopware Backend is able to communicate with the App Server in a secure way. This is because the App Server is able to verify the origin of the request by checking request signature, and this signature is generated by the Shopware 6 backend application with a shop to app server secret.

When an app wants to communicate directly with the App Server, the App Server is not able to verify the origin of the request and has to trust the client. This works fine for public available data, but not when you reliably need the logged-in customer and other information.

## Decision [​](#decision)

We provide a new endpoint `/store-api/app-system/{appName}/generate-token` (`/app-system/{appName}/generate-token` in Storefront) which generates a JWT token for the given app. This endpoint requires that the customer is logged-in and the app is installed and active.

The JWT token contains claims like:

* `iat` - issued at
* `exp` - expiration time
* `shopId` - the shop id of the current shop
* `salesChannelId` - the sales channel id of the current sales channel
* `customerId` - the customer id of the logged-in customer
* `cartToken` - the cart token of the current cart

The additional claims are bound to app permissions when an app does not have permissions to read a customer, it does not get the `customerId` claim.

The JWT token is signed with the shop to app server secret key which we use already for the signature. So the App Server needs to be able to verify the JWT key and use the claims in a secure way. The request body of the client is still untrusted and has to be properly validated by the app server.

The request cycle would look like this:

The JWT token is valid for 15 minutes and can be used multiple times until expired. The client should save it in the [session storage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) and request it only on expiry again. Additionally, the API route should be rate limited to not generate too often an expensive JWT key.

## Consequences [​](#consequences)

* We add a helper for the Storefront to obtain the token and do the expiry and regenerating
* We add support for JWT token verification in our PHP App SDK to make this process simple as possible

---

## Default handling for non specified salutations

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-06-28-default-handle-for-non-specified-salutations.html

# Default handling for non specified salutations [​](#default-handling-for-non-specified-salutations)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-06-28-default-handle-for-non-specified-salutations.md)

## Context [​](#context)

The current implementation of the salutation in Shopware 6 needs to handle cases where the salutation is not specified by the customer or administrator. To address this requirement and promote inclusivity, we have updated the default salutation to "not\_specified" for unspecified salutations in our Shopware 6 platform.

## Decision [​](#decision)

We have modified the existing salutation handling in Shopware 6 to update the default value to "not\_specified" when the salutation is null. This decision was made based on the following considerations:

* Inclusivity: By offering a default salutation of "not\_specified" for null values, we promote inclusivity and ensure that all customers are appropriately addressed, even when salutation data is missing.
* Customer Experience: Providing a default salutation ensures consistency in customer communications and prevents any confusion or misinterpretation when a salutation is not explicitly specified.
* Non-Deletable Default Salutation: It has been decided that the "not\_specified" salutation, being the default value for unspecified salutations, should not be deletable by the shop owner. This ensures that there is always a fallback option available, guaranteeing a consistent experience for customers.

## Consequences [​](#consequences)

As a result of this decision, the following consequences will occur:

* Improved Default Handling: When a customer or administrator does not specify a salutation, the default value will be automatically set to "not\_specified." This default value itself is configurable by the shop owner. They have the flexibility to customize the "not\_specified" value to their preferred salutation or leave it as it is to use the generic "not\_specified" salutation.
* Enhanced Inclusivity: Customers who have not specified their salutation will be addressed using the default "not\_specified" salutation, reflecting our commitment to inclusivity and respect within our platform.
* Code Changes: The necessary code changes have been implemented to update the default handling of null salutations. This includes validation checks, database updates, and modifications to relevant logic to accommodate the "not\_specified" default value.
* Different Default Values in Specific Locations: The default values used in specific locations within the platform are as follows:
  + Letters and Documents: When generating letters or documents where a salutation is required, the default value will be "Dear Customer" or an appropriate alternative if customization is allowed. This ensures a professional and personalized approach in written communications.
  + Email Communications: In email communications, the default value will be "Hello" or an alternative greeting if customization is allowed. This provides a friendly and welcoming tone in electronic correspondences.
  + User Interfaces: Within the user interfaces of the Shopware 6 platform, the default value will be displayed as "not\_specified" for customers who have not specified a salutation. This allows for a neutral and inclusive representation in the platform's user-facing components.
* Testing and Quality Assurance: Rigorous testing procedures will be conducted to ensure the accuracy and reliability of the updated default handling. Quality assurance measures will be in place to identify and address any potential issues.

---

## Flow Builder Preview

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-07-13-flow-builder-preview.html

# Flow Builder Preview [​](#flow-builder-preview)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-07-13-flow-builder-preview.md)

## Context [​](#context)

In the past merchants had to deal with issues where their custom-built flow did not behave how they intended it to do. An concrete example: We've had a merchant that contacted us (shopware) that their shop did not sent out mails. Debugging the flow turned out to be harder than we thought and honestly harder than it should be. The flow builder should empower users to build reliable flows and not spend their precious time trying to figure out what went wrong.

To improve the experience when using the Flow Builder were taking measures. First, Flow Builder Preview and second Flow Builder Logging. This ADR only discusses the former one, there are plans internally for the latter one, but it won't get much attention for now, as it also addresses different issues (what does my flow do vs what went wrong in the past).

Users should be able to preview a flow and get further understanding on how a flow executes. This preview only displays the steps and decisions happening inside a flow but doesn't execute / simulate the real flow

## Decision [​](#decision)

The whole scope of the Flow Builder Preview is to help merchants *creating* new flows and *update* their existing flows.

Will do:

* Evaluate path of flow by executing rules
* Validating the input data of the actions
* Leave it up to the action how much “real” code is actually executed

Won't do:

* Executing Flow Builder Actions i.e. calling the `handleFlow` method of an action
* Execute one huge transaction to the database and rollback later
  + Mail actions e.g. could render the mail template and send it to a given mail address
  + CRUD actions e.g. could decide, if they only want to check the input data or open a transaction to roll it back

### Preview is optional / We and Third Parties can provide this functionality [​](#preview-is-optional-we-and-third-parties-can-provide-this-functionality)

It is important to note that with this change existing and new actions do *not* need to implement the "preview" functionality and implementing it is completely optional. Actions that do not implement the new feature will be marked as "skipped" inside the administration.

### A new core interface [​](#a-new-core-interface)

The core interface defines the data structure of the output and third party developers could use this to make the flow action previewable. The interface could look like this:

php

```shiki
interface Previewable
{
    public function preview(...): PreviewResponseStruct
}
```

Flow actions are responsible to implement this interface if they want to and execute the necessary steps to generate a preview without actually writing / executing anything real.

### Separation from Flow Logging [​](#separation-from-flow-logging)

The Flow Builder Preview only addresses half of merchants pain points. While it does help with the creation of new flow it does not help merchants to manage incidents in their flows. This is where the Flow Logging feature comes in hand.

## Consequences [​](#consequences)

Though, it is completely optional to implement the "preview" feature for an action, we advice developers to do so. Doing, this will benefit...

1. ... the merchant when previewing their flow,
2. ... the plugin developer because the values the action provides increases

Because, the execution of the flow in a preview mode behaves different compared to when it is actually being executed, developers should make sure that the implementation their action preview stays as close as possible to the implementation of their action. Otherwise the preview could present a wrong impression to the merchant

---

## Collecting and dispatching entity data

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-08-03-collecting-entity-data.html

# Collecting and dispatching entity data [​](#collecting-and-dispatching-entity-data)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-08-03-collecting-entity-data.md)

## Context [​](#context)

*shopware AG* aims to provide data-driven features to its merchants. The foundation for these features are data that our merchants provide to us with their consent. A subset and primary pillar of these data lies within the entities, stored within each and every Shopware shop. This ADR addresses main concepts of extracting the information out of the shops and transferring it to *shopware AG*.

## Decision [​](#decision)

### No data sharing without consent [​](#no-data-sharing-without-consent)

Merchants must explicitly agree and consent to share their data with *shopware AG*. As long as there is no consent, no data will be collected or transferred. The consent to data sharing can be revoked at any time by the merchants.

We will actively prompt Administration users to decide whether they are willing to give their consent to data sharing on the Administration's dashboard. Changing the consent state later is possible via the system settings. To keep track of the consent changes, we will send to and store it on our gateway.

### No collection of sensitive information [​](#no-collection-of-sensitive-information)

Data stored in all types of entities might contain sensitive information including e.g. personal or business critical information. This kind of data is excluded.

### Personally identifiable information (PII) [​](#personally-identifiable-information-pii)

Data that would enable *shopware AG* to identify a person is modified in such a way that it is no longer possible to draw conclusions about the person. A so-called *personal unique identifier (PUID)* is generated to identify users across multiple sources (e.g. entity data, on-site tracking) with the goal of analyzing their behavior which is used for generating insights and making predictions. Again, it is not possible to find out **who** the person is, just that it is the **same** person.

### Transitioning to data pulling [​](#transitioning-to-data-pulling)

The processes described in this ADR can be viewed as an approach of *data pushing*. Data is fetched from the database and prepared on the merchant's servers and infrastructure before it is sent to *shopware AG*.

To be more flexible and to reduce the load on our merchant's infrastructure, we plan to transition to a *data pulling* approach. With this approach we are planning to use Shopware's Admin API to fetch the data, rather than fetching it from the database directly.

### Providing data-driven features via the app system [​](#providing-data-driven-features-via-the-app-system)

The features built upon the data that is collected, will be rolled out as an extension based on the app system. This way, we make feature releases independent of the Shopware 6 release cycle and can provide new features faster.

### Including entities and fields [​](#including-entities-and-fields)

By default, entities are not considered for data collection. Only entities and their fields listed in an allow-list will be included in the data collection.

The format looks as follows:

json

```shiki
{
    "entity_one": [
        "fieldOne",
        "fieldTwo",
        "fieldThree"
    ],
    "entity_two": [
        "fieldOne",
        "fieldTwo"
    ],
    "entity_three": [
        "fieldOne"
    ]
}
```

Example:

json

```shiki
{
    "category": [
        "id",
        "parentId",
        "type"
    ],
    "product": [
        "id",
        "parentId",
        "name"
    ]
}
```

#### Many-to-many associations [​](#many-to-many-associations)

Entities representing many-to-many associations between other entities should not be included in the allow-list. Instead, they are either fetched from the database directly or resolved by querying the associated entity table.

When adding a many-to-many association to the allow-list, the referenced field is the `associationName` instead of the `propertyName`.

Example:

php

```shiki
class ProductDefinition
{
    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            // ...
            (new ManyToManyIdField('category_ids', 'categoryIds', associationName: 'categories'))->addFlags(new ApiAware(), new Inherited()),
            (new ManyToManyAssociationField('categories', CategoryDefinition::class, ProductCategoryDefinition::class, 'product_id', 'category_id'))->addFlags(new ApiAware(), new CascadeDelete(), new Inherited(), new SearchRanking(SearchRanking::ASSOCIATION_SEARCH_RANKING)),
            // ...
            (new ManyToManyAssociationField('tags', TagDefinition::class, ProductTagDefinition::class, 'product_id', 'tag_id'))->addFlags(new CascadeDelete(), new Inherited(), new SearchRanking(SearchRanking::ASSOCIATION_SEARCH_RANKING), new ApiAware()),
            // ...
        ]);
    }
}
```

json

```shiki
{
    "product": [
        "categories",
        "tags"
    ]
}
```

The allow-list contains the `categories` and the `tags` field of the product entity. When the data is queried from the database, the many-to-many associations are resolved as follows:

* Identifiers of many-to-many associations that have a corresponding `ManyToManyIdField` are fetched from the database directly.
* Other many-to-many associations are resolved by fetching the associated entities from the database beforehand and matching them against the currently processed entity.

#### Associations problem: product -> category [​](#associations-problem-product-category)

#### Translated fields [​](#translated-fields)

Translated fields are not resolved automatically. Instead, translation entities must be added to the allow-list explicitly.

## Consequences [​](#consequences)

#### Activating and deactivating the data collecting process [​](#activating-and-deactivating-the-data-collecting-process)

The process will be triggered once a day by a scheduled task as long as the consent is given. It will also be triggered right away when the consent is given. The merchant can revoke the consent at any time, which will prevent the process from starting.

#### Collecting data asynchronously [​](#collecting-data-asynchronously)

Once the process is running, for each entity definition, some messages will be added to a low priority message queue, and so they will be processed asynchronously. The process will create batches of up to 50 entities (configurable) before sending them to the gateway.

#### First run and consecutive runs [​](#first-run-and-consecutive-runs)

Deltas of the data are calculated after the first time the data is sent, so consecutive runs are lighter and faster. In order to achieve this, the process will keep track of the last time the data was sent and will only send the data that was created or updated after that time.

For deletions, an event subscriber will take care of storing the deletions of the entities. These deletions will be sent and deleted when the process is run. No deletion will be stored if the consent for collecting data is revoked or not given in the first place.

#### Remote kill-switch [​](#remote-kill-switch)

A kill-switch on the Gateway enables us to (temporarily) stop shops from sending us data. Messages already dispatched to the queue will still be handled but no new messages will be added by the scheduled task if the kill-switch is enabled.

---

## Media path rewrite

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-08-17-media-path.html

# Media path rewrite [​](#media-path-rewrite)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-08-17-media-path.md)

## Context [​](#context)

In the current media system it is possible to configure different `Shopware\Core\Content\Media\Pathname\PathnameStrategy\PathnameStrategyInterface`.

These strategies are used to store files, which are uploaded for media entity, under a certain path.

The configured strategy is then also used to generate the URL that is used in the frontend/store API to embed the file.

The generation of this URL is currently triggered in an event subscriber which is registered to the `media.loaded` event.

For generating the URL an implementation of the `UrlGeneratorInterface` is used.

php

```shiki
interface UrlGeneratorInterface
{
    public function getAbsoluteMediaUrl(MediaEntity $media): string;

    public function getRelativeMediaUrl(MediaEntity $media): string;

    public function getAbsoluteThumbnailUrl(MediaEntity $media, MediaThumbnailEntity $thumbnail): string;

    public function getRelativeThumbnailUrl(MediaEntity $media, MediaThumbnailEntity $thumbnail): string;
}

interface PathnameStrategyInterface
{
    public function getName(): string;

    /**
     * Generate a hash, missing from url if omitted
     */
    public function generatePathHash(MediaEntity $media, ?MediaThumbnailEntity $thumbnail = null): ?string;

    /**
     * Generate the cache buster part of the path, missing from url if omitted
     */
    public function generatePathCacheBuster(MediaEntity $media, ?MediaThumbnailEntity $thumbnail = null): ?string;

    /**
     * Generate the filename
     */
    public function generatePhysicalFilename(MediaEntity $media, ?MediaThumbnailEntity $thumbnail = null): string;
}
```

## Issues [​](#issues)

* `PathnameStrategyInterface` as well as `UrlGeneratorInterface` have a dependency on the DAL and always need a fully loaded entity to generate the URL. This is a big overhead when you consider what data is (currently) needed for the URL generation in the end.
* The media upload "must" always be done via the shopware application, so that the folder structure stored in the file system and generated in the URL match. So it is only conditionally (or not at all) possible to upload all media directly to a S3 CDN without uploading the files via the shopware stack.
* In theory, the strategy must never be reconfigured after a file has been uploaded. If the file is uploaded to `/foo/test.jpg` and then the strategy is changed to one that would place the same file under `/bar/test.jpg`, the new strategy will take effect when the URL is generated, but the file will never be moved in the filesystem.
* The current strategies use a so called "cache busting" system, where the "uploaded-at" value is included in the file path. However, this does not work if the URL has been statically included in the CMS. Here, replacing the media file always leads to a new file path and the image can no longer be reached under the old file path.

## Decision [​](#decision)

To address the issues listed above, we will make the following changes to the system:

* The file path will be saved directly to the media entity (and thumbnail) when the file is uploaded.
  + This way we don't have to access the strategy when generating the URL, which might have changed in the meantime.
* We allow to change the file path via API and write it directly when creating the entity
  + This way files can be synchronized directly with an external storage and the path only has to be changed in the entity or given during import.
* To generate the strategy we use new location structs, which can be easily created via a service.
  + So we remove the dependency to the DAL to generate the file path.
* For generating the URL, we implement a new service, which can be operated without entities.
  + The URL generation is more resource efficient and can be done without fully loaded entities.
* The new URL generator uses a new "cache busting" system, which writes the updated at timestamp of the media entity as query parameter into the URL.
  + This way the file path can remain the same even if the file is updated. Changes to the entity's meta data will also result in a new URL.

## BC promise [​](#bc-promise)

For the Backwards compatibility we will take the following measures:

* Until 6.6.0 the old URL generator will still be used, which generates the URL with the old strategy.
* From 6.6.0 the new URL generator will be used, which generates the URL based on the `MediaEntity::$path`.
* If a project specific strategy is used, it must be migrated to the new pattern by 6.6.0.
* We provide a `BCStrategy` which converts the new format to the old format.
* For an easy transition between the majors, we make it possible to always use `MediaEntity::$path` for the relative path. We realize this via an entity loaded subscriber, which generates the value at runtime via the URL generator and writes it to the path property.

## Consequences [​](#consequences)

* We need less resources to generate the absolute media URLs
* We can generate the URLs even without fully loaded entities
* The strategy can be changed over time without moving the files in the file system
* We can load the files directly to an external storage and adjust the path in the entity
* We remove the dependency to the DAL from the strategy and the URL generator.

## Example [​](#example)

php

```shiki
<?php 

namespace Examples;

use Shopware\Core\Content\Media\Core\Application\AbstractMediaUrlGenerator;use Shopware\Core\Content\Media\Core\Params\UrlParams;use Shopware\Core\Content\Media\MediaCollection;use Shopware\Core\Content\Media\MediaEntity;use Shopware\Core\Content\Media\Pathname\UrlGeneratorInterface;

class BeforeChange
{
    private UrlGeneratorInterface $urlGenerator;
    
    public function foo(MediaEntity $media) 
    {
        $relative = $this->urlGenerator->getRelativeMediaUrl($media);
        
        $absolute = $this->urlGenerator->getAbsoluteMediaUrl($media);
    }
    
    public function bar(MediaThumbnailEntity $thumbnail) 
    {
        $relative = $this->urlGenerator->getRelativeThumbnailUrl($thumbnail);
        
        $absolute = $this->urlGenerator->getAbsoluteThumbnailUrl($thumbnail);
    }
}

class AfterChange
{
    private AbstractMediaUrlGenerator $generator;
    
    public function foo(MediaEntity $media) 
    {
        $relative = $media->getPath();

        $urls = $this->generator->generate([UrlParams::fromMedia($media)]);
        
        $absolute = $urls[0];
    }
    
    public function bar(MediaThumbnailEntity $thumbnail) 
    {
        // relative is directly stored at the entity
        $relative = $thumbnail->getPath();

        // path generation is no more entity related, you could also use partial entity loading and you can also call it in batch, see below
        $urls = $this->generator->generate([UrlParams::fromMedia($media)]);
        
        $absolute = $urls[0];
    }
    
    public function batch(MediaCollection $collection) 
    {
        $params = [];
        
        foreach ($collection as $media) {
            $params[$media->getId()] = UrlParams::fromMedia($media);
            
            foreach ($media->getThumbnails() as $thumbnail) {
                $params[$thumbnail->getId()] = UrlParams::fromThumbnail($thumbnail);
            }
        }
        
        $urls = $this->generator->generate($paths);

        // urls is a flat list with {id} => {url} for media and also for thumbnails        
    }
}

class ForwardCompatible
{
    // to have it forward compatible, you can use the Feature::isActive('v6.6.0.0') function
    public function foo(MediaEntity $entity) 
    {
        // we provide an entity loaded subscriber, which assigns the url of
        // the UrlGeneratorInterface::getRelativeMediaUrl to the path property till 6.6
        // so that you always have the relative url in the MediaEntity::path proprerty 
        $path = $entity->getPath();
        
        if (Feature::isActive('v6.6.0.0')) {
            // new generator call for absolute url
        } else {
            // old generator call for absolute url
        }
    }
}
```

---

## Post updater

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-08-27-post-updater.html

# Post updater [​](#post-updater)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-08-27-post-updater.md)

## Context [​](#context)

We often need a way between the different Shopware versions to provide a one-time update for data. This is currently done on the way to extend an indexer to this logic and then trigger this via a migration. This is of course a possible way to enable certain migrations of data, but this migration is also executed again and again when the indexer is executed. With certain data this is critical and can lead to system errors. For example, the one-time migration of media path information.

## Decision [​](#decision)

We implement a new `PostUpdateIndexer`. This is an extension of the `EntityIndexer` and the system can be adapted 1:1. Also, the indexing registration via database migration can be adapted 1:1. However, the indexer is not triggered via the `IndexerRegistry` when a full re-index or an entity written event is triggered. These indexers are only included after the update process. In addition to the one-time update of the data, we then often also provide a command that can be used to trigger the migration of the data again.

## Consequences [​](#consequences)

* We allow computationally intensive migrations, which need to be performed only once, to be performed after the update process.
* These one-time migrations do not affect the normal indexer process and cannot be triggered by it.
* Developers can trigger more complex migrations without worrying about the impact on the normal indexer process.
* The transition from one system to the other is very simple and can be adapted 1:1.

## Example [​](#example)

php

```shiki
<?php

class PostUpdateExample extends PostUpdateIndexer
{
    public function getName(): string
    {
        return 'post.update.example';
    }

    public function iterate(?array $offset): ?EntityIndexingMessage
    {
        $iterator = $this->iteratorFactory->createIterator('my_entity', $offset);

        $ids = $iterator->fetch();

        if (empty($ids)) {
            return null;
        }

        return new EntityIndexingMessage(array_values($ids), $iterator->getOffset());
    }
    
    public function handle(EntityIndexingMessage $message): void
    {
        // handle ids
    }
}
```

php

```shiki
<?php

class MigrationExample extends \Shopware\Core\Framework\Migration\MigrationStep
{
    public function update(Connection $connection): void
    {
        $this->registerIndexer($connection, 'post.update.example');
    }
}
```

---

## Add Feature property to `@experimental` annotation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-09-06-feature-property-for-experimental-anotation.html

# Add Feature property to `@experimental` annotation [​](#add-feature-property-to-experimental-annotation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-09-06-feature-property-for-experimental-anotation.md)

## Context [​](#context)

Our current development process uses ['Experimental features'](./2023-05-10-experimental-features.html) to publish features in an early state to gather feedback regarding those features. During the implementation, developers may encounter challenges related to the effective management of extensive code scattered throughout the platform, particularly in connection with specific experimental features. This codebase fragmentation presents impediments to the tracking, maintenance, and comprehensive understanding of each feature's scope, thereby hindering our development progress.

Potential problems:

* Update `stableVersion` property for Prolonged Experiments
  + When a decision is made to extend an experiment, locating all relevant sections of code for updating the property `stableVersion` in `@experimental` annotation becomes a cumbersome task.
* Deprecation of Killed Features
  + Identifying and marking as deprecated the components associated with a deprecated experimental feature is problematic, particularly when multiple experimental features coexist simultaneously within the platform.
  + The ['Experimental features'](./2023-05-10-experimental-features.html) stipulates the "Killing Feature" rule, which mandates that a feature must remain within the platform's codebase until the next major version and be appropriately marked as deprecated. However, it is hardly possible to check with current annotation.

In all the above case main problem is detection to which feature belongs experimental code.

## Decision [​](#decision)

To address the existing challenges, we propose implementing a refined approach to the use of the `@experimental` annotation.

The key modifications are as follows:

* Mandatory `feature` property:
  + Every `@experimental` annotation will now require a mandatory `feature` property. This property is a string that must contain the name of the associated feature.
* Uniform feature Naming:
  + To enhance code organization and traceability, all sections of code related to a particular feature must use the same feature name in the `feature` property of the `@experimental` annotation.
  + Feature names should follow the conventions.
    - Feature names cannot contain spaces
    - Feature names should be written in `ALL_CAPS`.

## Consequences [​](#consequences)

### Core [​](#core)

Implementation of the new `feature` property for the `@experimental` annotation will require the following changes:

* To `@experimental` annotation should be added required string property `feature`. The value of the features should follow the conventions.
* There will be implemented a static analysis rule / unit test, that checks that every `@experimental` annotation has the `feature` property.

Examples of usage: php

php

```shiki
/**
 * @experimental stableVersion:v6.6.0 feature:WISHLIST
 */
class testClass()
{
    //...
}
```

js

js

```shiki
/**
 * @experimental stableVersion:v6.6.0 feature:WISHLIST
 */
Component.register('sw-new-component', {
    ...
});
```

In twig blocks can be wrapped as being experimental:

twig

```shiki
{# @experimental stableVersion:v6.6.0 feature:WISHLIST #}
{% block awesome_new_feature %}
   ...
{% endblock %}
```

In addition to that, we can also mark the whole template as experimental:

twig

```shiki
{# @experimental stableVersion:v6.6.0 feature:WISHLIST #}
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}
```

## Combining `@experimental` annotation and `feature flag` [​](#combining-experimental-annotation-and-feature-flag)

Despite that, the `@experimental` annotation and the `feature flag` are two different concepts. The `@experimental` annotation is used to mark code as experimental and influential only on BC promises regarding this code, while the `feature flag` is used to control the visibility of the experimental code. There might be scenarios where introducing a feature flag (akin to a switch) becomes necessary, for example, in integration points. 'Experimental features' ADR doesn't explicitly prohibit this practice and does not regulate it in any way. Simultaneously, it would be beneficial to ensure a clear linkage between the feature flag and the experimental functionality it enables.

To achieve this linkage, we recommend the following:

1. Ensure that the feature flag's name matches the name used in the @experimental annotation's `feature` property.
2. The description field in the feature flag configuration should include the experimental annotation along with all the required properties, namely 'stableVersion' and 'feature'.

Example:

feature.yaml

yaml

```shiki
shopware:
  feature:
    flags:
      - name: WISHLIST
        default: false
        major: true
        description: "experimental stableVersion:v6.6.0 feature:WISHLIST"
```

New experimental class

php

```shiki
/**
 * @experimental stableVersion:v6.6.0 feature:WISHLIST
 */
class Foo
{
}
```

Connection point

php

```shiki
if (Feature.isActive('WISHLIST') {
        $obj = new Foo();
        // New implementation
} else {
        // Old/current implementation
}
```

---

## Introduction of Unique Identifiers for Checkout Methods

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-10-17-add-unique-identifiers-for-checkout-methods.html

# Introduction of Unique Identifiers for Checkout Methods [​](#introduction-of-unique-identifiers-for-checkout-methods)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-10-17-add-unique-identifiers-for-checkout-methods.md)

## Context [​](#context)

In the current implementation, there exists a challenge for extension developers in uniquely identifying payment and shipping methods using identifiers. This issue is particularly significant for app servers, as it necessitates calls to the Shopware Admin API for the identification of payment and shipping methods based on their respective IDs.

## Decision [​](#decision)

We will introduce a new property called `technicalName` to both the `payment_method` and `shipping_method` entities. This `technicalName` property will serve as a unique identifier for payment and shipping methods, significantly simplifying the identification process.

While the `technicalName` field will be optional within the database and API to ensure backward compatibility, it will be made mandatory in the Administration. This ensures that merchants will update their payment and shipping methods accordingly for the upcoming requirement. An unique index will ensure uniqueness. Starting from version 6.7.0.0, this `technicalName` field will also become required within the database and the API.

As part of the database migration process, the `technicalName` field will be automatically generated for the default payment and shipping methods provided by Shopware, as illustrated below:

| Type | Name | Technical Name |
| --- | --- | --- |
| Payment | Debit | payment\_debitpayment |
| Payment | Invoice | payment\_invoicepayment |
| Payment | Cash on Delivery | payment\_cashpayment |
| Payment | Pre Payment | payment\_prepayment |
| Shipping | Standard | shipping\_standard |
| Shipping | Express | shipping\_express |

Furthermore, all payment and shipping methods provided by apps will also benefit from the automatic generation of their `technicalName`. This generation will be based on the app's name and the `identifier` defined for the payment method in the manifest:

| App Name | Identifier | Technical Name |
| --- | --- | --- |
| MyApp | my\_payment\_method | payment\_MyApp\_my\_payment\_method |
| MyApp | my\_shipping\_method | shipping\_MyApp\_my\_shipping\_method |

## Consequences [​](#consequences)

Plugin developers will be required to supply a `technicalName` for their payment and shipping methods, at least beginning with version 6.7.0.0.

Merchants must review their custom created payment and shipping methods for the new `technicalName` property and update their methods through the administration accordingly.

It is essential to exercise caution when modifying the `technicalName` through the administration, as such changes could potentially disrupt existing integrations.

---

## Make more use of Bootstrap tooling and remove !important from Bootstrap CSS utils

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-10-19-bootstrap-css-utils.html

# Make more use of Bootstrap tooling and remove !important from Bootstrap CSS utils [​](#make-more-use-of-bootstrap-tooling-and-remove-important-from-bootstrap-css-utils)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-10-19-bootstrap-css-utils.md)

## Context [​](#context)

At the moment the Storefront is implementing a lot of custom SCSS inside `app/storefront/src/scss`. Some custom SCSS is not necessary, and it already exists within Bootstrap as a utility. For example default spacing with a custom selector:

scss

```shiki
.register-login-collapse-toogle {
    margin-bottom: $spacer;
}
```

This can be replaced with a Bootstrap [spacing utility](https://getbootstrap.com/docs/5.2/utilities/spacing/) in the HTML and the SCSS can be completely removed:

diff

```shiki
- <div class="register-login-collapse-toogle"><div>
+ <div class="register-login-collapse-toogle mb-3"><div>
```

A class like `register-login-collapse-toogle` should stay in the HTML in case a developer wants to style this specific element. But there is no need to introduce a new CSS rule using a custom selector to apply a default spacing.

If you implement new UI using mostly utility classes, please consider to still add CSS classes that offer the possibility for themes to add individual styling. For example:

html

```shiki
<!-- Classes "shipping-modal-actions", "shipping-abort" and "shipping-submit" are added for better semantics and CSS extensibility, but ship no default CSS. -->
<div class="border p-3 mb-3 shipping-modal-actions">
    <button class="btn btn-light shipping-abort">Abort</button>
    <button class="btn btn-primary shipping-submit">Submit</button>
</div>
```

This principle cannot be applied everywhere. For more complex layouts it can still be valid to use custom SCSS because it is not possible to build with default components and utilities, or it would produce a messy template with too many generic utility classes. However, for simpler stuff like "add a border here, add some spacing there" it's not necessary to implement additional custom styling.

## Decision [​](#decision)

We want to make more use of Bootstrap utilities and get rid of custom SCSS that is not needed.

In order to do so we want to remove unneeded SCSS and add a utility class to the HTML instead (e.g. `mb-3`). However, this can break styling overrides of themes/apps because most Bootstrap utility classes apply `!important` by default.

Let's stick to the example of `.register-login-collapse-toogle`.

* The core Storefront adds a bottom margin of `$spacer` which equals `1rem`.
* Then `CustomTheme` overrides this selector with a margin bottom of `80px`:

diff

```shiki
/* CustomTheme */
.register-login-collapse-toogle {
+    margin-bottom: 80px;
}

/* Storefront */
.register-login-collapse-toogle {
-    margin-bottom: 1rem;
}
```

If the core Storefront would migrate to the utility class it would suddenly overrule the styling of `CustomTheme` because of the `!important` property:

diff

```shiki
/* Utility class from HTML overrules CustomTheme */
.mb-3 {
+    margin-bottom: 1rem !important;
}

/* CustomTheme */
.register-login-collapse-toogle {
-    margin-bottom: 80px;
}

/* Storefront */
.register-login-collapse-toogle {
-    margin-bottom: 1rem;
}
```

The theme developer would have no other choice other than using `!important` as well, or modifying the Twig template.

Because of this, we have decided to remove the `!important` from Bootstrap utility classes by changing the [Importance](https://getbootstrap.com/docs/5.2/utilities/api/#importance) variable `$enable-important-utilities` to `false`. By doing this, we can use more utilities while at the same time allowing themes to override the same CSS property without using `!important` or editing the template.

Since it is currently expected that Bootstrap utilities add `!important` and overrule almost everything, we do not want to change this right away but from `v6.6.0` onwards.

### Bootstrap components first [​](#bootstrap-components-first)

We want to commit more to the standards of our framework and make better use of the default components, especially their configuration.

We should follow this principle:

1. Build something with Bootstrap default components and utilities first.
2. If the appearance does not fully suite our needs, use [component configuration and variables](https://getbootstrap.com/docs/5.2/components/buttons/#variables) for customization whenever possible.
3. Only when there is not enough config available, or in case of complex layouts that cannot be built using default components and utilities, we should rely on custom styling.

## Consequences [​](#consequences)

* In `v6.6.0` Bootstrap CSS utilities like `mb-3` will no longer apply the `!important` property.
* Unneeded custom styling will be removed from the SCSS and migrated to Bootstrap utilities.

---

## Make feature flags toggleable on demand

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-11-29-toggle-feature-flag-on-demand.html

# Make feature flags toggleable on demand [​](#make-feature-flags-toggleable-on-demand)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-11-29-toggle-feature-flag-on-demand.md)

## Context [​](#context)

Feature flags are a great way to enable/disable features in the application. However currently, they are not toggleable on demand. This means that if you want to enable a feature flag, you need to change the environment variables and restart the application. This is not ideal for a production environment.

## Decision [​](#decision)

### Store feature flags in the database [​](#store-feature-flags-in-the-database)

The available features are currently stored in the `feature.yaml` static file and toggleable via environment variables. We want to provide a way, that we can toggle this feature flags also via database and provide an UI for the shop merchant.

#### Example feature flag configuration in `app_config` [​](#example-feature-flag-configuration-in-app-config)

| key | value |
| --- | --- |
| feature.flags | ``` {      EXAMPLE_FEATURE_1:{ name: EXAMPLE_FEATURE_1, default: true, active: true     EXAMPLE_FEATURE_2:{ name: EXAMPLE_FEATURE_2, default: true, active: false } ``` |

All activated feature flags should be registered on `Framework::boot` via `FeatureFlagRegistry::register`:

php

```shiki
class Framework extends Bundle
    public function boot(): void
    {
        ...
        $featureFlagRegistry = $this->container->get(FeatureFlagRegistry::class);
        $featureFlagRegistry->register();
    }
```

`FeatureFlagRegistry::registry`: in this public method, we merge the static feature flags from `feature.yaml` with the stored feature flags from the database, we then activate the feature flags which are marked as active.

php

```shiki
class FeatureFlagRegistry
{
    public function registry(): void
    {
        $static = $this->featureFlags;
        $stored = $this->keyValueStorage->get(self::STORAGE_KEY, []);

        if (!empty($stored) && \is_string($stored)) {
            $stored = \json_decode($stored, true, 512, \JSON_THROW_ON_ERROR);
        }
        
        // Major feature flags cannot be toggled with stored flags
        $stored = array_filter($stored, static function (array $flag) {
            return !\array_key_exists('major', $flag) || !$flag['major'];
        });

        $flags = array_merge($static, $stored);
        
        Feature::registerFeatures($flags);
    }
}
```

### Toggle feature flags on demand [​](#toggle-feature-flags-on-demand)

We introduce new admin APIs so we can either activate/deactivate the feature flags. **Note:** We should only allow toggling feature flags which is not major.

#### Admin API [​](#admin-api)

php

```shiki
class FeatureFlagController extends AbstractController
{
    #[Route("/api/_action/feature-flag/enable/{feature}", name="api.action.feature-flag.toggle", methods={"POST"})]
    public function enable(string $feature, Request $request): JsonResponse
    {        
        $this->featureFlagRegistry->enable($feature);
        
        return new JsonResponse(null, Response::HTTP_NO_CONTENT);
    }
    
    #[Route("/api/_action/feature-flag/disable/{feature}", name="api.action.feature-flag.toggle", methods={"POST"})]
    public function disable(string $feature, Request $request): JsonResponse
    {        
        $this->featureFlagRegistry->disable($feature);
        
        return new JsonResponse(null, Response::HTTP_NO_CONTENT);
    }

    #[Route("/api/_action/feature-flag", name="api.action.feature-flag.load", methods={"GET"})]
    public function load(Request $request): JsonResponse
    {
        $featureFlags = Feature::getRegisteredFeatures();
        
        return new JsonResponse($featureFlags);
    }
}
```

`FeatureFlagRegistry::enable` & `disable` methods: in these public methods, we enable feature flags and store the new state in the database. We also dispatch an event `BeforeFeatureFlagToggleEvent` before toggling the feature flag and `FeatureFlagToggledEvent` after toggling the feature flag. This is helpful for plugins to listen to these events and do some actions before/after toggling the feature flag

php

```shiki
class FeatureFlagRegistry
{
    private function enable(string $feature, bool $active): void
    {
        $registeredFlags = Feature::getRegisteredFeatures();
        
        if (!array_key_exists($feature, $registeredFlags)) {
            return;
        }
        
        if ($registeredFlags[$feature]['major'] === 'true') {
            // cannot toggle major feature flags
            return;
        }
        
        $registeredFlags[$feature] = [
            'active' => $active, // mark the flag as activated or deactivated
            'static' => array_key_exists($feature, $this->staticFlags), // check if the flag is static
            ...$registeredFlags[$feature],
        ];
                
        $this->dispatcher->dispatch(new BeforeFeatureFlagToggleEvent($feature, $active));

        $this->keyValueStorage->set(self::STORAGE_KEY, $registeredFlags);
        Feature::toggle($feature, $active);

        $this->dispatcher->dispatch(new FeatureFlagToggledEvent($feature, $active));
    }
}
```

#### CLI [​](#cli)

We can also toggle the feature flags via CLI

script

```shiki
// to enable the feature FEATURE_EXAMPLE
bin/console feature:enable FEATURE_EXAMPLE 

// to disable the feature FEATURE_EXAMPLE
bin/console feature:disable FEATURE_EXAMPLE

// to list all registered feature flags
bin/console feature:list
```

## Consequences [​](#consequences)

### Ecosystem [​](#ecosystem)

* Before this, Feature flag system was mostly considered as an internal dev-only tool, it's used to hide major breaks or performance boost.
* Now it elevates to be a place where we can introduce new features and hide them behind feature flags. This will allow us to delivery new features even at experimental/beta phase and try them in production on demand without affecting the shop merchants
* But this should not be abused, we could only use the toggle for experimental/beta features and not for major features

### Commercial plans [​](#commercial-plans)

* For commercial licenses, each license's feature should be treated as a feature flag. This way, we can enable/disable features for each license if it's available in the license

### Shop merchants [​](#shop-merchants)

* For shop merchants, they can use the new toggle feature flags API to enable/disable features on demand, this will override the environment variables if the feature flag is available in the database. We can also add a new admin module or an app to allow shop merchants to toggle feature flags on demand or list all available feature flags via new admin APIs

### Developers [​](#developers)

* For internal devs, they can utilize the tool to quickly delivery new experimental/beta features. However, it's important that this should not be a tool to reach deadlines or release "crap". We should still follow standards and guidelines.
* External plugins can also add their own feature flags by adding them to the `feature.flags` key in the key value storage (e.g. `app_config` table if using the default key value storage)
* Feature flags can be toggled via CLI using `bin/console feature:enable <feature>` or `bin/console feature:disable <feature>` this is helpful for testing purposes and for CI/CD pipelines
* We can also add a new CLI command to list all available feature flags and their status using `bin/console feature:list`
* When a feature flag is toggled at run time, we dispatch an event `BeforeFeatureFlagToggleEvent` before toggling the feature flag and `FeatureFlagToggledEvent` after toggling the feature flag. This is helpful for plugins to listen to these events and do some actions before/after toggling the feature flag

---

## New acceptance test suite

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-12-12-acceptance-test-suite.html

# New acceptance test suite [​](#new-acceptance-test-suite)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-12-12-acceptance-test-suite.md)

## Context [​](#context)

For our ambitions to consequently reduce manual testing in favour for test automation the current E2E test suite, based on Cypress, is not sufficient anymore. It has several flaws that have become a big road-blocker. The test suite is tightly coupled to the state of the test environment, which leads to tests that are not very deterministic and tend to be slow and flaky. Tests are often created in different ways and don't follow a specific strategy. In addition, the test suite is currently not able to test against our cloud environment.

Our goal is to create a test suite that fulfills the following requirements:

* Deterministic tests that can run against any environment.
* Fast and reliable tests that follow a certain test strategy.
* Tests that are derived from real product requirements and validate behaviour.
* A test framework that is easy to learn and using a readable syntax that also non-tech people can comprehend.

## Decision [​](#decision)

In order to achieve this goal we decided to not further invest time in the existing test suite, but start from scratch. This offers the opportunity to also switch to another test framework that better fulfills our needs.

After some evaluation we chose Playwright as the new test framework. First benchmarks have shown that it is faster and more stable than Cypress. Additionally, it is easy to learn, has very good documentation and uses a syntax that is easily to understand. It also offers the functionality of creating reusable traces, which come in handy when debugging failing tests from pipelines.

## Consequences [​](#consequences)

We will stop our efforts on the existing E2E test suite based on Cypress and start a new acceptance test suite based on Playwright. The two test suites will co-exist for a certain amount of time until we have created the necessary test coverage with the new test suite. Tests are not just simply transferred from the old to the new test suite, but are also rethought based on a proper test strategy and the defined goals.

The new test suite will be developed in `tests/acceptance`. Please have a look at the `README.md` for more information about the test suite.

---

## Introduce transactional flow actions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-02-11-transactional-flow-actions.html

# Introduce transactional flow actions [​](#introduce-transactional-flow-actions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-02-11-transactional-flow-actions.md)

## Context [​](#context)

1. If flow actions want to interact with the database in a transactional manner, they need to handle it themselves by starting and committing transactions.
2. When there is a problem committing the transaction, the error will be caught and ignored by the flow dispatcher. A vague error message will be logged, but the flows will continue to execute. This is problematic if a transaction was already started before the flow is executed. If the connection is configured without save points (which is the default with Shopware), when a nested commit fails (eg during a flow action) the connection will be marked as rollback only. When the outer transaction attempts to commit, eg the calling code, it will be unaware of the previous inner commit failure and thus will also fail.

## Decision [​](#decision)

We introduce a new marker interface `\Shopware\Core\Content\Flow\Dispatching\TransactionalAction` which flow actions can implement.

The flow executor will wrap any action in a database transaction which implements the interface.

Before:

php

```shiki
class SetOrderStateAction extends FlowAction implements DelayableAction
{
    public function handleFlow(StorableFlow $flow): void
    {
        $this->connection->beginTransaction();
        
        //do stuff
        
        try {
            $this->connection->commit();
        } catch (\Throwable $e) {
                
        }
    }
}
```

After:

php

```shiki
class SetOrderStateAction extends FlowAction implements DelayableAction, TransactionalAction
{
    public function handleFlow(StorableFlow $flow): void
    {        
        //do stuff - will be wrapped in a transaction
    }
}
```

You can also force the flow executor to rollback the transaction by throwing an instance of `\Shopware\Core\Content\Flow\Dispatching\TransactionFailedException`. You can use the static `because` method to create the exception from another one. Eg:

php

```shiki
class SetOrderStateAction extends FlowAction implements DelayableAction, TransactionalAction
{
    public function handleFlow(StorableFlow $flow): void
    {        
        try {
            //search for some record
            $entity = $this->repo->find(...);
        } catch (NotFoundException $e) {
            throw TransactionFailedException::because($e);
        }
    }
}
```

The transaction will be rollback if either of the following are true:

1. If Doctrine throws an instance of `Doctrine\DBAL\Exception` during commit.
2. If the action throws an instance of `TransactionFailedException` during execution.
3. If another non-handled exception is thrown during the action execution. This is to aid debugging.

If the transaction fails, then the error will be logged. Also, if the transaction has been performed inside a nested transaction without save points enabled, the exception will be rethrown. So that the calling code knows something went wrong and is able to handle it correctly, by rolling back instead of committing. As, in this instance, the connection will be marked as rollback only.

## Consequences [​](#consequences)

When developers want to create flows which run inside of a database transaction, they should now implement the interface `\Shopware\Core\Content\Flow\Dispatching\TransactionalAction`, nothing else is required.

When an transaction commit fails and it is inside a nested transaction, the exception will be rethrown, which means that any other scheduled actions will not be executed.

---

## Disable Vue compat mode per component level

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-03-11-disable-vue-compat-mode-per-component-level.html

# Disable Vue compat mode per component level [​](#disable-vue-compat-mode-per-component-level)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-03-11-disable-vue-compat-mode-per-component-level.md)

## Context [​](#context)

Vue 3 introduced a new compatibility mode to ease the migration from Vue 2 to Vue 3. This mode is enabled by default and allows the use of most Vue 2 features in a Vue 3 application. This mode is only recommended for the transition period and should be turned off as soon as possible.

We have kept the compatibility mode enabled in the administration because it makes it easier for plugins to migrate and results in fewer breaking changes during the major release. This splits the work of migrating the administration and the plugins into two separate majors instead of one.

## Decision [​](#decision)

Migrating all components in one by disabling the compatibility mode for the whole administration is a huge task and would make it hard to keep the administration stable during the migration. We decided to disable the compatibility mode per component level. This allows us to migrate components one by one and keep the administration stable during the migration.

This gives all teams and plugin developers the possibility to migrate their components to Vue 3 without waiting for the whole administration to be migrated and for the global removal of the compatibility mode.

To activate the new mode, the `DISABLE_VUE_COMPAT` feature flag must be enabled. Then, it is possible to disable the compatibility mode on a per-component level by setting the `compatConfig` option in the component to our custom configuration. This custom configuration is exposed in `Shopware.compatConfig` and has all compatibility features disabled if the feature flag is activated.

### Example [​](#example)

javascript

```shiki
Shopware.Component.register('your-component', {
    compatConfig: Shopware.compatConfig,
})
```

#### Notice: [​](#notice)

We have a tool which reads all components and creates a list of all components which are still using the compatibility mode. This list is used to track the progress of the migration. This tool checks for the following syntax `compatConfig: Shopware.compatConfig,` inside the component definition. Any other syntax, e.g. `compatConfig: false,` will not be recognized by the tool and will not be tracked.

## Consequences [​](#consequences)

Migration to Vue 3 can be done incrementally, and administration remains stable during migration. Also, it allows us to migrate the admin and plugins separately, making the migration easier for all teams and plugin developers.

To accomplish this task we have to communicate the new feature flag and the new way to disable the compatibility mode to all teams and plugin developers. This will give them the opportunity to migrate their components to Vue 3 over a longer period of time period of time.

---

## Implementation of Meteor Component Library

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-03-21-implementation-of-meteor-component-library.html

# Implementation of Meteor Component Library [​](#implementation-of-meteor-component-library)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-03-21-implementation-of-meteor-component-library.md)

## Context [​](#context)

We have decided to implement the Meteor Component Library within the Shopware platform. They will replace the current base components in the administration.

## Decision [​](#decision)

To ensure a smooth transition, we have thought of a few things to make the implementation easier. Below we describe the solutions in detail.

### 1. Rename components in the Meteor Component Library [​](#_1-rename-components-in-the-meteor-component-library)

To avoid naming conflicts with the current base components, we will rename the components in the Meteor Component Library. The new components will have the prefix `mt-` (Meteor) in their names. This way we can ensure that the components are easily distinguishable from the current components.

The CSS classes will also be renamed to avoid conflicts with the current CSS classes. The new CSS classes will have the prefix `mt-` (Meteor) in their names.

To avoid breaking changes, we will keep the old exports in the Meteor Component Library. This way we can ensure that existing imports will still work. We will console and warn that using the old components is deprecated. Switching to the new components is recommended and can be done by changing the import path.

### 2. Parallel Usage [​](#_2-parallel-usage)

For the current major release phase (6.6), we are implementing the Meteor Component Library in parallel with the current base components. Developers will be able to switch between the two libraries using the major feature flag 6.7. This way, we can ensure that current functionality is not affected by the new implementation.

To have both component implementations working at the same time, we will move each component into a "wrapper" component. This wrapper component will decide which component to render based on the feature flag. You can also use the new components directly with the prefix `mt-`.

Example:

html

```shiki
<!-- Shopware 6.6 -->

<!-- Is working, emit a warning in console that this component usage is deprecated. -->
<sw-example oldProperty="old">Example</sw-example>
<!-- Is NOT working. -->
<sw-example newProperty="new">Example</sw-example>
<!-- Is working. Uses directly the component from the Meteor Component Library. -->
<mt-example newProperty="new">Example</mt-example>

<!-- Shopware 6.7 -->
<!-- Not working anymore. -->
<sw-example oldProperty="old">Example</sw-example>
<!-- Is NOT working. -->
<sw-example newProperty="new">Example</sw-example>
<!-- Is working. -->
<mt-example newProperty="new">Example</mt-example>
```

### 3. Provide automatic code migration tool [​](#_3-provide-automatic-code-migration-tool)

To make the transition as easy as possible, we will provide a code migration tool. This tool will automatically replace the old components with the new ones. The tool will also replace the properties, slot usage, etc. to the new Meteor Component Library. This will save developers a lot of time and make the transition as easy as possible.

We can't guarantee to provide a codemod for every edge case. But the most common use cases will be covered. Developers can also use the codemod as a base and manually modify the code as needed.

### 4. Keeping complicated components in the old implementation [​](#_4-keeping-complicated-components-in-the-old-implementation)

Some components have a lot more differences than others. For example, the `mt-button` component is very similar to the `sw-button` component and can be easily migrated. But the `mt-data-table` component is very different from the `sw-data-grid` component. To avoid breaking changes, we will keep the old implementation of the `sw-data-grid` component with a deprecation note. This way, we can ensure that the functionality is still available, and developers can migrate to the new component in their own time. We will do this for any component that has a more complicated migration path.

If the manual migration contains breaking changes it have to be done behind a feature flag so that it can be released in a major release.

## Consequences [​](#consequences)

The implementation of the Meteor Component Library will provide a better developer experience in the long run. We are relying on a single component library, which will make maintenance easier. The components will be more consistent and development will be faster. They will also be more stable, fully tested, accessible and work and look the same as in the Apps. So it is also easier to switch from the plugin system to the app system because they share the same underlying components.

---

## Checkout gateway

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-04-01-checkout-gateway.html

# Checkout gateway [​](#checkout-gateway)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-04-01-checkout-gateway.md)

# ADR: Enhanced Checkout Gateway Feature [​](#adr-enhanced-checkout-gateway-feature)

## Context [​](#context)

In response to the evolving landscape of checkout decision-making, we propose the introduction of a centralized and opinionated solution. This solution aims to facilitate informed decisions during the checkout process based on both the cart contents and the current sales channel context. The app-system, in particular, stands to benefit significantly, enabling seamless communication with the app server. Presently, achieving such functionality is constrained to app scripts, limiting the capacity for making nuanced decisions during checkout based on app server logic.

Moreover, payment and shipping providers necessitate specific criteria for determining the availability of their respective methods. These criteria include considerations such as risk assessment related to the current customer and cart, unavailability criteria, merchant connection status validation (e.g., checking for correct credentials), and service availability testing (e.g., detecting provider outages). Additionally, these providers require the ability to block carts during checkout based on risk assessment decisions.

While this ADR focuses on the aforementioned features, the implementation is designed to allow for seamless future extensions.

## Decision [​](#decision)

### CheckoutGatewayInterface [​](#checkoutgatewayinterface)

To address the outlined challenges, we propose the introduction of the CheckoutGatewayInterface. This interface will be invoked during the checkout process to determine a response tailored to the current cart and sales channel context.

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Gateway;

use Shopware\Core\Checkout\Gateway\Command\Struct\CheckoutGatewayPayloadStruct;
use Shopware\Core\Framework\Log\Package;

#[Package('checkout')]
interface CheckoutGatewayInterface
{
    /**
    * The input struct consists of the cart, sales channel context and currently available payment and shipping methods.
    */
    public function process(CheckoutGatewayPayloadStruct): CheckoutGatewayResponse;
}
```

Plugin developers are encouraged to create custom implementations of the `CheckoutGatewayInterface` for their specific checkout logic based on decisions from external systems (e.g., ERP, PIM).

The `CheckoutGatewayResponse` will include an `EntityCollection` of payment and shipping methods suitable for the current context, along with a collection of `CartErrors`. The input struct and the response is designed for future extension, allowing for more intricate decision-making during checkout.

#### Store-API [​](#store-api)

A new store API route, `CheckoutGatewayRoute` '/store-api/checkout/gateway', will be introduced. This route will call a `CheckoutGatewayInterface` implementation and respond accordingly, and is integral to `CartOrderRoute` requests, ensuring the cart's validity for checkout during the order process.

#### Storefront [​](#storefront)

The default invocation of the `CheckoutGatewayRoute` will occur during the checkout-confirm page and edit-order page (so-called "after order"). Any changes to the context (e.g., language, currency) will trigger a reload of the payment method selection, calling the app server again.

#### Checkout Gateway Commands [​](#checkout-gateway-commands)

For streamlined response manipulation by plugins and app servers alike, we propose an executable chain of `CheckoutGatewayCommands`. The implementation of the app-system will heavily rely on the command structure. However, it is encouraged, but not mandatory for a custom implementation plugin-system implementation of the `CheckoutGatewayInterface` to follow the command structure.

These commands, chosen from a predefined set, can be responded with by plugins and app servers. The initial release will include the following commands: `add-payment-method`, `remove-payment-method`, `add-shipping-method`, `remove-shipping-method`, and `add-cart-error`. Depending on the command, the payload may differ, necessitating updates to the documentation. We propose the use of a handler pattern, to facilitate the execution of these commands. Commands will be executed in the order provided in the response.

### App-System [​](#app-system)

For the initial release, Shopware will support a single implementation of the `CheckoutGatewayInterface`, provided by the app-system. The `AppCheckoutGateway` will sequentially call active apps, but only if the app has a defined `checkout-gateway-url` in its manifest.xml file.

#### App Manifest [​](#app-manifest)

To address challenges for apps, a new app endpoint can be defined in the manifest.xml. A new key `gateways` will be added to the manifest file, with a sub-key `checkout` to define the endpoint. The `gateways` key signalizes possible future similar endpoints for different purposes. The checkout gateway endpoint is configured using a new element called `checkout`.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <checkout>https://example.com/checkout/gateway</checkout>
    </gateways>
</manifest>
```

#### Checkout Gateway App Payload [​](#checkout-gateway-app-payload)

The app server will receive the current `SalesChannelContext`, `Cart`, and available payment and shipping methods as part of the payload. The `AppCheckoutGateway` will call the app server with this payload.

json

```shiki
{
    "salesChannelContext": SalesChannelContextObject,
    "cart": CartObject,
    "paymentMethods": [
        "payment-method-technical-name-1",
        "payment-method-technical-name-2",
        "payment-method-technical-name-3",
        ...
    ],
    "shippingMethods": [
        "shipping-method-technical-name-1",
        "shipping-method-technical-name-2",
        "shipping-method-technical-name-3",
        ...
    ]
}
```

Note that the paymentMethods and shippingMethods arrays will only contain the technical names of the methods, not the full entities.

#### Checkout Gateway App Response [​](#checkout-gateway-app-response)

json

```shiki
[
  {
    "command": "remove-payment-method",
    "payload": {
      "paymentMethodTechnicalName": "payment-myApp-payment-method"
    }
  },
  {
    "command": "add-cart-error",
    "payload": {
      "reason": "Payment method not available for this cart.",
      "level": 20,
      "blockOrder": true
    }
  }
]
```

#### Event [​](#event)

A new event `CheckoutGatewayCommandsCollectedEvent` will be introduced. This event is dispatched after the `AppCheckoutGateway` has collected all commands from all app servers. It allows plugins to manipulate the commands before they are executed, based on the same payload the app servers retrieve.

## Consequences [​](#consequences)

### App PHP SDK [​](#app-php-sdk)

The app-php-sdk will be enhanced to support the new endpoint and data types, ensuring seamless integration with the command structure. The following adaptations will be made:

Checkout gateway requests with payload will be deserialized into a `CheckoutGatewayRequest` object. Checkout gateway responses will be deserialized into a `CheckoutGatewayResponse` object. Every possible checkout gateway command will have a class representing it, facilitating easy manipulation of its payload.

---

## Add jest runner with disabled compat mode

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-06-12-add-jest-runner-with-disabled-compat-mode.html

# Add jest runner with disabled compat mode [​](#add-jest-runner-with-disabled-compat-mode)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-06-12-add-jest-runner-with-disabled-compat-mode.md)

## Context [​](#context)

Currently, our component tests in Jest are running with enabled compat mode. To remove the compat mode for each component, we need to add a new Jest runner with disabled compat mode to make sure that the tests are running without compat mode.

## Decision [​](#decision)

I added a new runner command in the NPM scripts to run the Jest tests without compat mode. The new runner command is `unit:disabled-compat` and `unit-watch:disabled-compat`. Also, the composer commands are added to run the tests. These commands are `admin:unit:disabled-compat` and `admin:unit-watch:disabled-compat`. These commands are using the environment variable `DISABLE_JEST_COMPAT_MODE` to disable the compat mode.

For the pipeline, I added a new stage to run the Jest tests without compat mode. The stage is `Jest (Administration with disabled compat mode)`.

To mark a test file working without the compat mode you need to add a comment with the `@group` tag. The tag is `@group disabledCompat`.

Example:

javascript

```shiki
/**
 * @package admin
 * @group disabledCompat
 */

import { mount } from '@vue/test-utils';

async function createWrapper() {
...
```

With this tag, the test file is running without compat mode. To make a component working for both modes, you can use the compatUtils helper function from Vue compat:

javascript

```shiki
// Example
import { compatUtils } from '@vue/compat';

...

if (compatUtils.isCompatEnabled('INSTANCE_LISTENERS')) {
    return this.$listeners;
}

return {};

...
```

Important: the test still runs also with compat mode activated in parallel.

## Consequences [​](#consequences)

* Fixing the components and tests to run also without compat mode. This has to be done by removing the compat mode for each component.
* Marking fixed tests with `@group disabledCompat` to run without compat mode.
* When everything is fixed, we can remove the compat mode from the Jest configuration.

---

## Error-code log Level configuration in platform or cloud

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-06-17-error-code-log-level-configuration-in-cloud-and-platform.html

# Error-code log Level configuration in platform or cloud [​](#error-code-log-level-configuration-in-platform-or-cloud)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-06-17-error-code-log-level-configuration-in-cloud-and-platform.md)

## Context [​](#context)

In the configuration files for platform and cloud, specific error codes can be set to the notice level. Some time ago, we decided to configure this in platform ([Exception Log Level configuration](./2023-05-25-exception-log-levels.html)).

As it is still essential for some errors to be logged at the highest level for customers with own servers, we now have to decide which errors we can decrease for all customers and which only for cloud. The key consideration is whether it makes sense for on-premise customers to continue logging these errors at a high level. If it does, the error codes must be added to the cloud configuration file in the SaaS template.

For example, an incorrectly configured flow on the customer side is not an error that needs to be analyzed by us and has to be recorded by our error monitoring, but it is important for the customer to be informed about it at the highest log level.

## Decision [​](#decision)

We have to decide for each error code whether it makes sense for on-premise customers to continue logging these errors at a high level. If so, the error codes have to be added to the cloud configuration file in the SaaS template.

### This could be a small guide for the decision: [​](#this-could-be-a-small-guide-for-the-decision)

* Never decrease critical errors in platform

Errors that shall be configured in cloud:

* all the unexpected stuff that should not happen and a dev should look at this, even though the fix is not in Shopware itself but probably in some calling code/configuration
* like API misuses
* or misconfigurations on the customer side

Errors that shall be configured in platform:

* all the expected stuff, it is totally normal that those things happen and no dev needs to change something
* like 404 errors
* or invalid user credentials at login

## Consequences [​](#consequences)

By implementing this approach, we ensure that critical errors are properly logged and monitored in both on-premise and cloud environments, aligning with the needs and contexts of different customer bases.

---

## Replace Vuex with Pinia

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-06-17-replace-vuex-with-pinia.html

# Replace Vuex with Pinia [​](#replace-vuex-with-pinia)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-06-17-replace-vuex-with-pinia.md)

# ADR: Replace Vuex with Pinia [​](#adr-replace-vuex-with-pinia)

## Context [​](#context)

It was brought to our attention that the latest version of Vuex `4.1.0` contains a bug that destroys getter reactivity under specific circumstances. The proposed fix was to downgrade to `4.0.2`. However, downgrading was not possible as `4.0.2` contains other bugs that caused modules to fail.

## Decision [​](#decision)

Pinia is the new documented standard with Vue 3; therefore, we will switch to Pinia.

## Consequences [​](#consequences)

### Removal of Vuex [​](#removal-of-vuex)

Below you will find an overview of what will be removed on which Shopware Version.

#### 6.7 [​](#_6-7)

For Shopware 6.7 we want to transition all our modules but still leave the possibility for you to use Vuex for your own states.

* All `Shopware.State` functions will cause warnings to appear in the DevTools. For example `Shopware.State.registerModule is deprecated. Use Shopware.Store.register instead!`
* All Vuex state definitions will be transitioned to Pinia:
  + src/module/sw-bulk-edit/state/sw-bulk-edit.state.js
  + src/module/sw-product/page/sw-product-detail/state.js
  + src/module/sw-category/page/sw-category-detail/state.js
  + src/module/sw-extension/store/extensions.store.ts
  + src/module/sw-settings-payment/state/overview-cards.store.ts
  + src/module/sw-settings-seo/component/sw-seo-url/state.js
  + src/module/sw-settings-shipping/page/sw-settings-shipping-detail/state.js
  + src/app/state/notification.store.js
  + src/app/state/session.store.js
  + src/app/state/system.store.js
  + src/app/state/admin-menu.store.js
  + src/app/state/admin-help-center.store.ts
  + src/app/state/license-violation.store.js
  + src/app/state/context.store.ts
  + src/app/state/error.store.js
  + src/app/state/settings-item.store.js
  + src/app/state/shopware-apps.store.ts
  + src/app/state/extension-entry-routes.js
  + src/app/state/marketing.store.js
  + src/app/state/extension-component-sections.store.ts
  + src/app/state/extensions.store.ts
  + src/app/state/tabs.store.ts
  + src/app/state/menu-item.store.ts
  + src/app/state/extension-sdk-module.store.ts
  + src/app/state/modals.store.ts
  + src/app/state/main-module.store.ts
  + src/app/state/action-button.store.ts
  + src/app/state/rule-conditions-config.store.js
  + src/app/state/sdk-location.store.ts
  + src/app/state/usage-data.store.ts
  + src/module/sw-flow/state/flow.state.js
  + src/module/sw-order/state/order.store.ts
  + src/module/sw-order/state/order-detail.store.js
  + src/module/sw-profile/state/sw-profile.state.js
  + src/module/sw-promotion-v2/page/sw-promotion-v2-detail/state.js

#### 6.8 [​](#_6-8)

With Shopware 6.8 we will entirely remove everything Vuex related including the dependency.

* `Shopware.State` - Will be removed. Use `Shopware.Store` instead.
* `src/app/init-pre/state.init.ts` - Will be removed. Use `src/app/init-pre/store.init.ts` instead.
* `src/core/factory/state.factory.ts` - Will be removed without replacement.
* Interface `VuexRootState` will be removed from `global.types.ty`. Use `PiniaRootState` instead.
* Package `vuex` will be removed.

## Transition to Pinia [​](#transition-to-pinia)

Pinia calls its state-holding entities `stores`. Therefore, we decided to hold everything Pinia-related under `Shopware.Store`. The `Shopware.Store` implementation follows the Singleton pattern. The private constructor controls the creation of the Pinia root state. This root state must be injected into Vue before the first store can be registered. The `init-pre/store.init.ts` takes care of this.

### Best practices [​](#best-practices)

1. All Pinia Stores must be written in TypeScript
2. All Stores will export a type or interface like the `cms-page.state.ts`
3. The state property of the exported type must be reused for the state definition.

You can always orientate on the `cms-page.state.ts`. It contains all best practices.

For now, we have decided to limit the public API of `Shopware.Store` to the following:

typescript

```shiki
/**
 * Returns a list of all registered Pinia store IDs.
 */
public list(): string[];

/**
 * Gets the Pinia store with the given ID.
 */
public get(id: keyof PiniaRootState): PiniaStore;

/**
 * Registers a new Pinia store. Works similarly to Vuex's registerModule.
 */
public register(options: DefineStoreOptions): void;

/**
 * Unregisters a Pinia store. Works similarly to Vuex's unregisterModule.
 */
public unregister(id: keyof PiniaRootState): void;
```

The rest of the previous Vuex (`Shopware.State`) public API is implemented into Pinia itself.

typescript

```shiki
// Setup
const piniaStore = Shopware.Store.get('...');

// From Vuex subscribe
Shopware.State.subscribe(...);
// To Pinia $subscribe
store.$subscribe(...);

// From Vuex commit
Shopware.State.commit(...);
// To Pinia action call
store.someAction(...);

// From Vuex dispatch
Shopware.State.dispatch(...);
// To Pinia action call
store.someAsyncAction(...);
```

### Example Implementation [​](#example-implementation)

To prove that Vuex and Pinia can co-exist during the transition period, we picked a private Vuex state and decided to transition it. We chose the `cmsPageState`, which is heavily used in many components. The transition went smoothly without any major disturbances.

How to transition a Vuex module into a Pinia store:

1. In Pinia, there are no `mutations`. Place every mutation under `actions`.
2. `state` needs to be an arrow function returning an object: `state: () => ({})`.
3. `actions` no longer need to use the `state` argument. They can access everything with correct type support via `this`.
4. Point 3 also applies to `getters`.
5. Use `Shopware.Store.register` instead of `Shopware.State.registerModule`.

Let's look at a simple Vuex module and how to transition it:

typescript

```shiki
// Old Vuex implementation
Shopware.State.registerModule('example', {
    state: {
        id: '',
    },
    getters: {
        idStart(state) {
            return state.id.substring(0, 4);
        }
    },
    mutations: {
        setId(state, id) {
            state.id = id;
        }
    },
    actions: {
        async asyncFoo({ commit }, id) {
            // Do some async stuff
            return Promise.resolve(() => {
                commit('setId', id);
                
                return id;
            });
        }
    }
});

// New Pinia implementation
// Notice that the mutation setId was removed! You can directly modify a Pinia store state after retrieving it with Shopware.Store.get.
Shopware.Store.register({
    id: 'example',
    state: () => ({
        id: '',
    }),
    getters: {
        idStart: () => this.id.substring(0, 4),
    },
    actions: {
        async asyncFoo(id) {
            // Do some async stuff
            return Promise.resolve(() => {
                this.id = id;

                return id;
            });
        }
    }
});
```

---

## Transition to an Event-Based Extension System

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-06-18-extended-event-system.html

# Transition to an Event-Based Extension System [​](#transition-to-an-event-based-extension-system)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-06-18-extended-event-system.md)

## Context [​](#context)

In our current architecture, we rely heavily on PHP decoration, Adapter, and Factory patterns to allow for extensions and customizations by third-party developers. While these patterns are effective, they present significant challenges:

1. **Backward and Forward Compatibility:**

   * Maintaining backward and forward compatibility with these patterns is complex and labor-intensive. Each change or update can potentially break existing extensions or require extensive rework to ensure compatibility.
2. **Process Extension Limitations:**

   * These patterns do not inherently allow for the extension of subprocesses unless these subprocesses are extracted into separate classes and interfaces. This extraction often results in a proliferation of interfaces, abstract classes, and their implementations.
3. **Proliferation of Code:**

   * The need to extract subprocesses into separate entities leads to an overwhelming number of interfaces and abstract classes. This proliferation makes the codebase more difficult to understand and maintain, and increases the cognitive load on developers.

## Decision [​](#decision)

To address these challenges, we have decided to transition to an event-based extension system. This new approach will replace the existing decoration, Adapter, and Factory patterns as the primary method for extending and customizing our system.

## Rationale [​](#rationale)

1. **Simplification of Compatibility:**

   * An event-based system inherently simplifies backward and forward compatibility. Events can be introduced, deprecated, or modified with minimal impact on existing extensions, as long as the core event structure remains consistent.
2. **Modular Extension Points:**

   * By leveraging events, we can provide more granular and modular extension points. Developers can hook into specific points of the application flow without needing to manipulate or extend multiple interfaces and classes.
3. **Reduction in Code Proliferation:**

   * The shift to an event-based system will significantly reduce the need for a large number of interfaces and abstract classes. This will streamline the codebase, making it easier to manage and reducing the cognitive load on developers.
4. **Unified Extension Framework:**

   * An event-based system provides a more unified and consistent framework for third-party developers. They can use a standardized method to extend and customize the application, leading to better consistency and reliability in extensions.

## Consequences [​](#consequences)

1. **Initial Refactoring Effort:**

   * Transitioning to an event-based system will require an initial effort to refactor existing code and extensions. This will involve identifying current extension points and replacing them with event triggers.
2. **Learning Curve:**

   * Developers accustomed to the current patterns will need to adapt to the new event-based approach. Training and documentation will be necessary to facilitate this transition.

## Implementation [​](#implementation)

1. **Identify Key Extension Points:**

   * Conduct an audit of the current system to identify key extension points that will be replaced with events.
2. **Define Event Structure:**

   * Develop a standard structure for events, including naming conventions, payload formats, and handling mechanisms.
3. **Refactor Existing Extensions:**

   * Gradually refactor existing extensions to use the new event-based system, ensuring backward compatibility where necessary.
4. **Documentation and Training:**

   * Create comprehensive documentation and training materials to help developers transition to the new system.

## Conclusion [​](#conclusion)

The transition to an event-based extension system represents a strategic shift aimed at simplifying our extension framework, improving maintainability, and providing a more consistent and flexible platform for third-party developers. While this change requires an initial investment in refactoring and training, the long-term benefits of reduced complexity, improved compatibility, and a unified extension approach make it a worthwhile endeavor.

## Example [​](#example)

The following example demonstrates how an event-based extension can be implemented in the context of resolving product listings:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Product\Extension;

use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\Framework\Extensions\Extension;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

/**
 * @extends Extension<EntitySearchResult<ProductCollection>>
 */
#[Package('inventory')]
final class ResolveListingExtension extends Extension
{
    public const NAME = 'listing-loader.resolve';

    /**
     * @internal shopware owns the __constructor, but the properties are public API
     */
    public function __construct(
        /**
         * @public
         *
         * @description The criteria which should be used to load the products. Is also containing the selected customer filter
         */
        public readonly Criteria $criteria,
        /**
         * @public
         *
         * @description Allows you to access to the current customer/sales-channel context
         */
        public readonly SalesChannelContext $context
    ) {
    }
}
```

In this example, the `ResolveListingExtension` class represents an event-based extension point for resolving product listings. Developers can subscribe to this event and provide custom logic for loading product data based on specific criteria and context. This approach allows for more modular and flexible extensions compared to traditional patterns like decoration or Adapter.

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Tests\Examples;

use GuzzleHttp\ClientInterface;
use Shopware\Core\Content\Product\Extension\ResolveListingExtension;
use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

readonly class ResolveListingExample implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            'listing-loader.resolve.pre' => 'replace',
        ];
    }

    /**
     * @param EntityRepository<ProductCollection> $repository
     */
    public function __construct(
        // you can inject your own services
        private ClientInterface $client,
        private EntityRepository $repository
    ) {
    }

    public function replace(ResolveListingExtension $event): void
    {
        $criteria = $event->criteria;

        // building a json aware array for the API call
        $context = [
            'salesChannelId' => $event->context->getSalesChannelId(),
            'currencyId' => $event->context->getCurrency(),
            'languageId' => $event->context->getLanguageId(),
        ];

        // do an api call against your own server or another storage, or whatever you want
        $ids = $this->client->request('GET', 'https://your-api.com/listing-ids', [
            'query' => [
                'criteria' => json_encode($criteria),
                'context' => json_encode($context),
            ],
        ]);

        $data = json_decode($ids->getBody()->getContents(), true);

        $criteria = new Criteria($data['ids']);

        $event->result = $this->repository->search($criteria, $event->context->getContext());

        // stop the event propagation, so the core function will not be executed
        $event->stopPropagation();
    }
}
```

---

## Deprecating Meteor Admin SDK public SDK

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-07-16-deprecating-sdk-public-api.html

# Deprecating Meteor Admin SDK public SDK [​](#deprecating-meteor-admin-sdk-public-sdk)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-07-16-deprecating-sdk-public-api.md)

## Context [​](#context)

Recently, the need arose to deprecate the `Meteor Admin SDK` public API built into the Shopware Core. We need to be able to deprecate the public API, which consists of `component sections` and `data sets`.

### Component sections [​](#component-sections)

The `sw-extension-component-section` component represents component sections in Shopware. This component is added to templates, assigned a `position identifier,` and allows rendering components in place via the SDK.

vue

```shiki
<template>
    <sw-extension-component-section
        position-identifier="sw-chart-card__before"
    />
</template>
```

### Data sets [​](#data-sets)

Data sets can range from whole entities to a subset of such or scalar values. These data sets are published in the component's code like so:

javascript

```shiki
createdComponent() {
    Shopware.ExtensionAPI.publishData({
        id: 'sw-dashboard-detail__todayOrderData',
        path: 'todayOrderData',
        scope: this,
    });
},
```

No mechanisms were in place to mark `component sections` and `data sets` as deprecated. As we promise that the SDK will be our most stable extension tool, we need to ensure that this API is treated as such.

## Decision [​](#decision)

### Monitoring [​](#monitoring)

We decided to monitor the SDK's public API to gain an overview and ensure that it is not diminished by accident. This is achieved by the `meta.spec.ts` file. The test uses committed JSON files containing all `data set ID's` and `component section - position identifiers`. It then checks the committed file against a run-time computed list to determine if any of these were removed.

### Deprecating [​](#deprecating)

Both `component sections` and `data sets` must be able to be deprecated. For `component sections`, we added two props:

* deprecated: Boolean
* deprecationMessage: String

vue

```shiki
<template>
    {# @deprecated tag:v6.7.0 - Will be removed use position XYZ instead #}
    <sw-extension-component-section
        position-identifier="sw-chart-card__before"
        :deprecated="true"
        deprecation-message="Use position XYZ instead."
    />
</template>
```

For `data sets`, we mimicked the same in the publishing options:

* deprecated: Boolean
* deprecationMessage: String

javascript

```shiki
createdComponent() {
    /* @deprecated tag:v6.7.0 - Will be removed, use API instead */ 
    Shopware.ExtensionAPI.publishData({
        id: 'sw-dashboard-detail__todayOrderData',
        path: 'todayOrderData',
        scope: this,
        deprecated: true,
        deprecationMessage: 'No replacement available, use API instead.'
    });
},
```

#### Best practices [​](#best-practices)

It is considered best practice to add a comment with the usual `@deprecated` annotation, so these parts are not missed in a major version update.

## Consequences [​](#consequences)

* Both `component sections` and `data sets` marked as deprecated will throw an error in a dev environment
* Both `component sections` and `data sets` marked as deprecated will publish a warning in a prod environment

The error or warning message will always state which extension used the deprecated `data set` or `component section` and provide the corresponding ID's:

shell

```shiki
# component section
[CORE] The extension "TestApp" uses a deprecated position identifier "foo_bar". Use position identifier "XYZ" instead.

# data set
[CORE] The extension "TestApp" uses a deprecated data set "foo_bar". No replacement available, use API instead.
```

The first sentence containing the app name and the `data set`/ `component section` ID will always be the same format. Any information provided through the `deprecationMessage` will be appended as an addition.

## Conclusion [​](#conclusion)

With all this, we assured that the public API of the Meteor Admin SDK is treated as such, but we have the possibility to properly deprecate.

---

## Telemetry abstraction layer

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-07-30-add-telemetry-abstraction-layer.html

# Telemetry abstraction layer [​](#telemetry-abstraction-layer)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-07-30-add-telemetry-abstraction-layer.md)

## Context [​](#context)

Observability is a key aspect of modern software development. It is essential to have the right tools in place to monitor and analyze runtime statistics of the application.

Many tools and backends are available to enable telemetry and monitoring. The context of this ADR is to provide a streamlined and simple way to enable the integration of any observability tool into the Shopware platform.

## Decision [​](#decision)

To address the need for a unified way to track metrics and performance data, we will introduce a telemetry abstraction layer. This layer will provide a common interface for integrating different monitoring tools into the Shopware platform.

The telemetry abstraction layer will consist of the following components:

### Shopware's abstraction layer [​](#shopware-s-abstraction-layer)

The abstraction layer will provide a common interface for telemetry integration. It will define the methods and data structures required to send telemetry data to the monitoring backend.

### Events subsystem attachment [​](#events-subsystem-attachment)

The telemetry abstraction layer will be integrated with the existing events subsystem. This integration will allow developers to hook into specific events and capture telemetry data related to those events.

### Transport layer (integrations) [​](#transport-layer-integrations)

Vendor specific implementation will not be part of the core. Those would be shipped as external libraries that implement the telemetry abstraction layer specification. The core will provide documentation on how to integrate these libraries into the Shopware platform.

Each transport layer should at least be aware of the following metrics objects:

* `Shopware\Core\Framework\Telemetry\Metrics\Metric\Counter`
* `Shopware\Core\Framework\Telemetry\Metrics\Metric\Gauge`
* `Shopware\Core\Framework\Telemetry\Metrics\Metric\Histogram`
* `Shopware\Core\Framework\Telemetry\Metrics\Metric\UpDownCounter`

Or more generally, should aim to cover all the metric types defined inside the `Shopware\Core\Framework\Telemetry\Metrics\Metric` namespace.

### Implementation and Considerations [​](#implementation-and-considerations)

Each transport should implement the `MetricTransportInterface`. This interface defines a method `emit` that takes a `MetricInterface` object as an argument. The `MetricInterface` object represents a single metric that needs to be sent to the monitoring backend.

If an instance of an unsupported metric type is passed to the transport, it should throw a `MetricNotSupportedException`. This ensures that the transport layer is decoupled from the core and can be extended to support new metric types in the future.

> `MetricNotSupportedException` is gracefully handled, and the application will skip over the unsupported metric type.

php

```shiki
interface MetricTransportInterface
{
    /**
     * @throws MetricNotSupportedException
     */
    public function emit(MetricInterface $metric): void;}
```

The `MetricInterface` is a generic empty interface. This approach provides flexibility for different monitoring tools to define their own metric structures alongside the core ones.

php

```shiki
interface MetricInterface
{
}
```

## Consequences [​](#consequences)

By implementing a telemetry abstraction layer, we provide a unified way to integrate monitoring tools into the Shopware platform. This approach simplifies the process of adding telemetry to the application and ensures consistency across different monitoring tools.

## Usage [​](#usage)

See [README.md](./../src/Core/Framework/Telemetry/) for the implementation and usage details.

---

## Add more unit tests namespaces to FeatureFlag extension

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-07-31-add-more-unit-tests-namespaces-to-featureflag-extension.html

# Add more unit tests namespaces to FeatureFlag extension [​](#add-more-unit-tests-namespaces-to-featureflag-extension)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-07-31-add-more-unit-tests-namespaces-to-featureflag-extension.md)

## Context [​](#context)

The `Shopware\Core\Test\PHPUnit\Extension\FeatureFlag\Subscriber\TestPreparationStartedSubscriber` only allows the `Shopware\Tests\Unit` namespace to be considered when enabling the major feature in the unit tests suite.

## Decision [​](#decision)

To be able to unit test the upcoming major feature in other plugins we will enable the possibility to add other namespaces to the `Shopware\Core\Test\PHPUnit\Extension\FeatureFlag\Subscriber\TestPreparationStartedSubscriber`.

We'll add a static method called `addNamespace()` method to the `Shopware\Core\Test\PHPUnit\Extension\FeatureFlag\FeatureFlagExtension` and by this we are able to add other namespaces to the allowlist of the namespaces to be considered when enabling the major flags in the unit test suite.

This can be useful for plugins that wants to enable the major flags in their unit tests suite.

Therefore, add the extension to the extension list in the `phpunit.xml`:

xml

```shiki
<extensions>
    ...
    <bootstrap class="Shopware\Core\Test\PHPUnit\Extension\FeatureFlag\FeatureFlagExtension"/>
</extensions>
```

And register your test namespace in your test bootstrap file:

php

```shiki
FeatureFlagExtension::addTestNamespace('Your\\Unit\\Tests\\Namespace\\');
```

For example, in the Commercial plugin, we added the following code to the `tests/TestBootstrap.php` file:

php

```shiki
FeatureFlagExtension::addTestNamespace('Shopware\\Commercial\\Tests\\Unit\\');
```

## Consequences [​](#consequences)

If your namespace will be added via the `FeatureFlagExtension::addNamespace()` method, the major flags will be enabled by default in your unit tests suite, and you have to explicitly disable the feature you don't want to be executed with the upcoming major flag turned on. If you want to know the decision why all feature flags are activated by default, please read [this ADR](https://github.com/shopware/shopware/blob/trunk/adr/2022-10-20-deprecation-handling-during-phpunit-test-execution.md#L15-L14).

---

## System Health Checks in Shopware

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-08-02-system-health-check.html

# System Health Checks in Shopware [​](#system-health-checks-in-shopware)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-08-02-system-health-check.md)

## Context [​](#context)

In some instances, a system rollout was completed where an error in certain system functionalities was not detected until the system was live.

A software system is made up of many components that work together to provide a service. The software system can still be healthy even if some of its components are not fully in a healthy state. System health checks are a way to monitor the health of a system and detect failures early.

## Decision [​](#decision)

We will implement system health checks in Shopware to monitor certain parts of the system with the aim to detect failures and issues early. This system should be extensible and allow for custom health checks to be added with ease.

### Abstractions and Core concepts [​](#abstractions-and-core-concepts)

The following abstractions and concepts, are core to the implementation:

1. **Shopware\Core\Framework\SystemCheck\BaseCheck**:

   * Defines a base class for all system checks.
2. **Shopware\Core\Framework\Health\Check\Category**:

   * Represents the category of functionality that the check is covering.
   * Categories:
     + `SYSTEM`: System checks makes sure that the backbone of the software is functioning correctly. Example: Database connection.
     + `FEATURE`: Feature checks make sure that a specific feature of the software is functioning correctly. Example: Payment system.
     + `EXTERNAL`: External checks make sure that external services are responding correctly. Example: SMTP server is online.
     + `AUXILIARY`: Auxiliary checks make sure that auxiliary services are functioning correctly. Example: background tasks are running.
3. **Shopware\Core\Framework\SystemCheck\Check\Result**:

   * Represents the outcome state of a check.
4. **Shopware\Core\Framework\SystemCheck\Check\Status**:

   * Represents the status of a health check result.
   * Statuses (in order of severity):
     + `OK`: The component is functioning correctly.
     + `SKIPPED`: The component check was skipped.
     + `UNKNOWN`: The component status is unknown.
     + `WARNING`: The component is functioning but with some issues that are not errors.
     + `ERROR`: The component has runtime errors, but some parts of it could still be functioning.
     + `FAILURE`: The component has failed with irrecoverable errors.
5. **Shopware\Core\Framework\SystemCheck\Check\SystemCheckExecutionContext**:

   * Represents the context in which a health check is executed.
   * Contexts:
     + `WEB`: The check is running in a web environment.
     + `CLI`: The check is running in a command-line interface environment.
     + `PRE_ROLLOUT`: The check is running before a system rollout.
     + `RECURRENT`: The check is running as part of a scheduled task.

#### System Check Guidelines [​](#system-check-guidelines)

System checks can differ in complexity, purpose, and computational cost. The types are logical categorizations based on the need and cost for the test and is used to determine the appropriate execution context for a check. This distinction is primarily reflected in the `Shopware\Core\Framework\SystemCheck\BaseCheck` class method:

php

```shiki
    protected function allowedSystemCheckExecutionContexts(): array
    {...}
```

##### Readiness Checks [​](#readiness-checks)

Readiness checks are intended to be run by infrastructure teams to determine if a system is ready to be rolled out and accept traffic or run scheduled tasks.

Those checks should typically check critical paths of the system, such as correct configuration and if the storefront indices are correctly opening. There are no requirements for readiness checks to be fast.

Those system checks would have:

php

```shiki
    protected function allowedSystemCheckExecutionContexts(): array
    {
        return \Shopware\Core\Framework\SystemCheck\Check\SystemCheckExecutionContext::readiness();
    }
```

##### Health Checks [​](#health-checks)

Health checks are intended to be run by monitoring systems to determine if a system is healthy and functioning correctly. Those checks should typically check the health of the system, such as database connectivity, cache availability, and other critical components.

A requirement to a typical health-check is that it should be fast, inexpensive, and not block the system.

Those system checks would have:

php

```shiki
    protected function allowedSystemCheckExecutionContexts(): array
    {
        return \Shopware\Core\Framework\SystemCheck\Check\SystemCheckExecutionContext::cases();
    }
```

##### Long Running Checks [​](#long-running-checks)

This type of check is essentially a health check that can take a long time to run. This type of check should be run sparingly and is only allowed to run when on CLI. An example of such test would be a check to verify that there are no issues in log files.

Those system checks would have:

php

```shiki
    protected function allowedSystemCheckExecutionContexts(): array
    {
        return \Shopware\Core\Framework\SystemCheck\Check\SystemCheckExecutionContext::longRunning();
    }
```

##### Other [​](#other)

This type would be any custom check where it needs to be run in a different context other than the templates given above. This could be anything, based on the requirements of the check.

php

```shiki
    protected function allowedSystemCheckExecutionContexts(): array
    {
        # list of contexts
        return [SystemCheckExecutionContext::CRON, SystemCheckExecutionContext::WEB];
    }
```

## Consequences [​](#consequences)

by implementing system health checks, we ensure that the system is monitored and that issues are detected early. This will help to prevent system failures and improve the overall stability of the system. Moreover, it helps detecting issues at the time of deployment and helps to prevent issues from reaching the end-users.

---

## Native Block System in Shopware

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-09-26-native-block-system.html

# Native Block System in Shopware [​](#native-block-system-in-shopware)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-09-26-native-block-system.md)

## Context [​](#context)

The current block system relies on TwigJs for creating reusable and extendable component template. This system allows plugin developers to override or extend content in predefined blocks using TwigJs’s inheritance mechanisms. Vue.js offers a more dynamic and reactive component-based architecture which is better suited for modern frontend development.

To replace TwigJs with a native Vue.js approach we need to introduce two new component `sw-block` and `sw-block-parent`.

The new `sw-block` and `sw-block-parent` components in Vue.js aim to replicate and improve on the TwigJs block system by providing a component-based approach. These components offer enhanced flexibility by allowing dynamic content overriding and extension directly in Vue’s templating and reactivity model.

## Decision [​](#decision)

We have decided to migrate from the TwigJs-based block system to the Vue.js-based `sw-block` system. This decision aligns with the following goals:

1. **Uniform Frontend Stack**: Vue.js is already used for the frontend in Shopware Administration. Moving blocks from TwigJs to Vue.js creates consistency in the technology stack, simplifying development and reducing the cognitive load on developers who previously had to switch between TwigJs and Vue.js.
2. **Improved Flexibility**: With Vue.js blocks we have control over the provided access to the component’s internals, allowing for more granular control over block behavior and content. This allows us to create a public API for any component, making it easier to extend and modify internal behavior, without breaking the public API.

### Architecture Description of the Vue.js Block System [​](#architecture-description-of-the-vue-js-block-system)

This Vue.js block system uses two main components: `sw-block` and `sw-block-parent`, to enable dynamic content overriding and extension, replacing the traditional TwigJs blocks.

1. The `sw-block` defines a block with default content. An overriding component extends this block using the `extends` attribute, optionally accessing the parent content with `sw-block-parent`.
2. The Block Context manages the relationship between blocks.
3. The `sw-block-parent` allows injecting the original block's content into the extended block, enabling partial content overrides.

This architecture streamlines content management, providing a flexible and reusable component system ideal for dynamic UI compositions. ![](/assets/native_block_system.BKrJ9qVv.png "Native Block System Architecture")

## Consequences [​](#consequences)

### Positive Consequences [​](#positive-consequences)

1. **Consistency and Maintainability**: With all frontend logic now centralized in Vue.js, developers will no longer need to manage two separate templating systems. This simplification enhances code maintainability and consistency across the application.
2. **Enhanced Extensibility**: The new `sw-block` system allows blocks to be overridden and extended using native Vue.js slots, making it easier for developers to introduce custom behaviors and content into existing components.
3. **Improved Performance**: Vue.js components are more performant when handling dynamic content updates, reducing the rendering overhead associated with rendering in TwigJs. This will lead to smoother UI updates and potentially lower client load.
4. **Component Reusability**: Since `sw-block` is a Vue.js component, it can be composed with other Vue.js components, enhancing the reusability of UI blocks across different parts of the application.

### Negative Consequences [​](#negative-consequences)

1. **Migration Complexity**: Migrating from TwigJs to Vue.js will require refactoring existing blocks and adjusting the development workflow. This may introduce temporary disruptions as developers need to learn and apply the new system.
2. **Component Structure Breakage**: The insertion of blocks may interfere with existing v-if, v-else, and v-else-if conditions, as blocks can disrupt the flow and logic of these conditionals by placing content between them.
3. **Slot Usage Breakage**: Blocks can disrupt the parent-child slot relationship, leading to issues where a block is inserted between a child slot and its parent, breaking the intended slot composition.

---

## Vue 2 Options API to Vue 3 Composition API Conversion Codemod

**Source:** https://developer.shopware.com/docs/resources/references/adr/2024-10-02-vue-2-options-api-to-vue-3-composition-api-conversion-codemod.html

# Vue 2 Options API to Vue 3 Composition API Conversion Codemod [​](#vue-2-options-api-to-vue-3-composition-api-conversion-codemod)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2024-10-02-vue-2-options-api-to-vue-3-composition-api-conversion-codemod.md)

## Context [​](#context)

Our Vue.js application currently uses the Options API, which is the traditional way of writing Vue components in Vue 2. With the release of Vue 3, the Composition API was introduced, offering improved code organization, better TypeScript support, and enhanced reusability of component logic. For more detailed information about the reasons for migrating to the Composition API, see the [documentation entry](/docs/guides/plugins/plugins/administration/system-updates/vue-native.html).

To modernize our codebase and take advantage of these benefits, we need to migrate our existing Vue 2 Options API components to use the Vue 3 Composition API. Manual conversion of numerous components would be time-consuming and error-prone. Therefore, we need an automated solution to assist in this migration process.

## Decision [​](#decision)

We have decided to implement a Codemod in the form of an ESLint rule to automatically convert Vue 2 Options API components to Vue 3 Composition API. This Codemod will:

1. Identify Vue component definitions in the codebase.
2. Convert the following Options API features to their Composition API equivalents:

   * Convert `data` properties to `ref` or `reactive`.
   * Convert `computed` properties to `computed()` functions.
   * Convert `methods` to regular functions within the `setup()` function.
   * Convert lifecycle hooks to their Composition API equivalents (e.g., `mounted` to `onMounted`).
   * Convert Vue 2 specific lifecycle hooks to their Vue 3 equivalents.
   * Convert `watch` properties to `watch()` functions.
   * Handle `props` and `inject` conversions.
   * Replace `this` references with direct references to reactive variables.
   * Convert writable computed properties.
   * Handle reactive object reassignments using `Object.assign`
   * Handle correct usage of `ref` and replace the access to the value with `.value`.
3. Generate a `setup()` function containing the converted code.
4. Add necessary imports for Composition API functions (e.g., `ref`, `reactive`, `computed`, `watch`).

The Codemod will be implemented as an ESLint rule to leverage the existing ESLint ecosystem and allow for easy integration into our development workflow.

## Consequences [​](#consequences)

### Positive Consequences [​](#positive-consequences)

1. Automated conversion will significantly reduce the time and effort required to migrate components to the Composition API.
2. Consistent conversion patterns will be applied across the codebase, ensuring uniformity.
3. The risk of human error during manual conversion is minimized.
4. Developers can gradually adopt the Composition API, as the Codemod can be run on a per-file or per-component basis.
5. The Codemod can be easily shared and used across different projects within the organization.

### Negative Consequences [​](#negative-consequences)

1. The Codemod may not cover all edge cases or complex component structures, requiring manual intervention in some scenarios.
2. Developers will need to review and potentially refactor the converted code to ensure optimal usage of the Composition API.
3. The Codemod does not handle template changes, such as adjusting `$refs` usage.

### Limitations and Manual Steps [​](#limitations-and-manual-steps)

While the Codemod handles many aspects of the conversion, some parts will still require manual attention:

1. Template modifications: The Codemod doesn't update the component's template. Developers will need to manually adjust template bindings, event handlers, and `ref` usage.
2. Complex data structures: While simple `data` properties are converted to `ref()` or `reactive()`, more complex nested structures might require manual optimization.
3. Vuex store interactions: The Codemod doesn't automatically convert Vuex `mapState`, `mapGetters`, `mapActions`, etc. These will need to be manually converted to use the `useStore` composition function.
4. Mixins: The Codemod doesn't handle the conversion of mixins. These will need to be manually refactored into composable functions.
5. Plugin usage: Certain plugins or third-party libraries that rely on the Options API might require manual updates or replacements.
6. TypeScript annotations: If the project uses TypeScript, type annotations for props, computed properties, and methods will need to be manually added or adjusted in the `setup()` function.
7. Spread operators in computed properties: The Codemod identifies these but doesn't fully convert them. A TODO comment is added for manual attention.
8. Components using render functions or JSX will need manual conversion.
9. Performance optimizations like `shallowRef` or `shallowReactive` are not automatically applied.
10. The converted code may benefit from further refactoring to extract reusable composables.
11. Error handling and edge cases in lifecycle hooks may need manual review.
12. Usage of plugins, etc. in the `this` context may need manual conversion, e.g. `$tc`, `$t`, etc.
13. Sometimes the reassignment of reactive objects over multiple lines may not be handled correctly every time.
14. Usage of `$emit` in the Options API may need manual conversion to `defineEmits` in the Composition API and then using the `emit` function.

By implementing this Codemod, we take a significant step towards modernizing our Vue.js codebase while acknowledging that some manual work will still be required to complete the migration process.

---

