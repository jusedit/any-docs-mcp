# Guides Plugins Plugins Content

*Scraped from Shopware Developer Documentation*

---

## Content

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/

# Content [​](#content)

Content feature in Shopware encompasses the essential capabilities related to managing and enhancing content within the e-commerce platform, including content management, email management, SEO optimization, sitemap generation, and media management. These functions enhance website content, facilitate effective communication, improve search engine visibility, and streamline media organization within the e-commerce platform. While these functions are typically available within the core Shopware system, plugins offer the flexibility to extend or customize them based on specific business needs and content strategies.

---

## CMS

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/

# CMS [​](#cms)

In general, Shopware CMS creates and manages content using blocks and elements.

The CMS plugin allows you to easily add and organize these CMS blocks, which are reusable sections of content that can be placed on multiple pages. You can customize the appearance and layout of these blocks. To create engaging and visually appealing pages within these blocks, you can add and configure various content elements such as text, images, videos, sliders, and more. Additionally, the CMS plugin enables you to add data to their content elements, such as product information, categories, or dynamic content from APIs.

Furthermore, the CMS feature core functions can be accessed and managed through the Shopware Admin SDK. This provides developers with tools and APIs to interact with the CMS functionality, allowing for more advanced customization.

Overall, the plugin facilitates you to create, customize, and manage engaging content on your website. Through blocks, elements, and the flexibility the Admin SDK provides, businesses can create visually appealing pages with dynamic and relevant content to enhance the user experience.

---

## Add CMS block

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/add-cms-block.html

# Add CMS Blocks [​](#add-cms-blocks)

## What is a Block? [​](#what-is-a-block)

A CMS block in Shopware is a fundamental structural component of the Shopping Experience (CMS) system. Understanding the hierarchy helps clarify what blocks are:

### CMS Hierarchy [​](#cms-hierarchy)

* Page - The top-level container (e.g., category page, shop page, product page)
* Section - Horizontal segments within a page (can be single-column or two-column with sidebar)
* **Block - Units that usually span an entire row with custom layout and styling**
* **Slots - A named container inside a block. Each slot represents a designated area that can hold exactly one CMS element**
* Elements - The actual content primitives (text, image, video, product listing, etc.) placed inside slots

A block represents a reusable layout unit that defines how elements are arranged in slots. For example, Shopware's built-in `image-text` block displays an image on the left and text on the right. Blocks are clustered into categories like Text, Images, Commerce, and Video for organizational purposes in the administration interface.

**Key concept**: Blocks define the structure (layout and slots), while elements provide the actual content. This separation allows the same block to display different types of content in its slots.

> **Learn more**: For a deeper understanding of the CMS architecture, see the [Shopping Experience fundamental guide](https://developer.shopware.com/docs/concepts/commerce/content/shopping-experiences-cms.html).

## Where to Find Blocks [​](#where-to-find-blocks)

Blocks are located in the Shopping Experience module in the Shopware Administration:

* Navigate to Content → Shopping Experience
* Create a new layout or edit an existing one
* In the layout designer, you'll see a sidebar with available blocks organized by category:
  + Text - Text-only blocks
  + Images - Image-only blocks
  + Text & Images - Combined text and image blocks
  + Commerce - Product sliders, listings, etc.
  + Video - YouTube and Vimeo video blocks
  + Form - Contact and newsletter forms
  + Sidebar - Category navigation and listing filters

Drag and drop blocks from the sidebar into your layout sections.

You can find related block code here:

* Administration: `src/Administration/Resources/app/administration/src/module/sw-cms/blocks/`
* Storefront: `src/Storefront/Resources/views/storefront/block/`
* Core: `\Shopware\Core\Content\Cms\SalesChannel\SalesChannelCmsPageLoader::load`

## How to Create a Block in the Administration [​](#how-to-create-a-block-in-the-administration)

### Directory Structure [​](#directory-structure)

We recommend this structure for CMS blocks:

TEXT

```shiki
<plugin root>/src/Resources/app/administration/src/
├── main.js
└── module/
    └── sw-cms/
        └── blocks/
            └── text-image/              (category)
                └── image-text-reversed/ (block name)
                    ├── index.js
                    ├── component/
                    │   ├── index.js
                    │   ├── cms-block-image-text-reversed.html.twig
                    │   └── cms-block-image-text-reversed.scss
                    └── preview/
                        ├── index.js
                        ├── cms-block-preview-image-text-reversed.html.twig
                        └── cms-block-preview-image-text-reversed.scss
```

### Step 1: Import Your Block in main.js [​](#step-1-import-your-block-in-main-js)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-cms/blocks/text-image/image-text-reversed';
```

### Step 2: Register the Block [​](#step-2-register-the-block)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/image-text-reversed/index.js
import './component';
import './preview';

Shopware.Service('cmsService').registerCmsBlock({
    name: 'image-text-reversed',
    category: 'text-image',
    label: 'cms.blocks.imageTextReversed.label',
    component: 'cms-block-image-text-reversed',
    previewComponent: 'cms-block-preview-image-text-reversed',
    defaultConfig: {
        marginBottom: '20px',
        marginTop: '20px',
        marginLeft: '20px',
        marginRight: '20px',
        sizingMode: 'boxed',
    },
    slots: {
        left: 'text',
        right: 'image',
    },
});
```

| Property | Description |
| --- | --- |
| `name` | Technical name of your block |
| `category` | Which category it appears under (`text`, `image`, `text-image`, `commerce`, `form`, `video`, `sidebar`) |
| `label` | Display name in the UI |
| `component` | Vue component for rendering the block in the designer |
| `previewComponent` | Vue component for the block thumbnail preview |
| `defaultConfig` | Default styling values |
| `slots` | Defines which element types go in which slots (key = slot name, value = element type) |

### Step 3: Create the Block Component [​](#step-3-create-the-block-component)

It's important to include all slots you defined in the block configuration (Step 2). These are used for configuring elements in the administration interface.

JS

```shiki
// image-text-reversed/component/index.js
Shopware.Component.register('cms-block-image-text-reversed', {
    template: `<div style="display: flex; gap: 16px;">
        <slot name="left" />
        <slot name="right" />
    </div>`,
});
```

### Step 4: Create the Preview Component [​](#step-4-create-the-preview-component)

The preview is shown as a thumbnail when selecting a block from the editor sidebar. You could also display a static image of your final Storefront block here.

JS

```shiki
// image-text-reversed/preview/index.js
Shopware.Component.register('cms-block-preview-image-text-reversed', {
    template: `<div style="display: flex; gap: 16px;">
        <h2>Lorem ipsum dolor sit amet</h2>
        <img :src="assetFilter('/administration/administration/static/img/cms/preview_mountain_small.jpg')" />
    </div>`,
    computed: {
        assetFilter() {
            return Shopware.Filter.getByName('asset');
        },
    },
});
```

After this, the block preview should appear in the Shopping Experience block sidebar under the "Text & Images" category and can be added to a layout.

## How to Create a Block in the Storefront [​](#how-to-create-a-block-in-the-storefront)

The Storefront template defines how your element appears on the actual storefront. It is expected to be located in the directory `src/Resources/views/storefront/block`. In there, a twig template file has to follow this naming convention:

* **Prefix**: `cms-block-`
* **Technical name**: `image-text-reversed` (The `name` property in Step 2)
* **Extension**: `.html.twig`

**Shopware is expecting the prefix as part of the full filename in `src/Storefront/Resources/views/storefront/section/cms-section-block-container.html.twig`.**

Full example: `cms-block-image-text-reversed.html.twig`

### Basic Template [​](#basic-template)

You can create your own blocks or extend and reuse existing ones. Don't forget to clear the Storefront cache after adding new templates.

TWIG

```shiki
{# <plugin root>/src/Resources/views/storefront/block/cms-block-image-text-reversed.html.twig #}
<div class="col-md-6">
    {% set element = block.slots.getSlot('left') %}

    {% sw_include '@Storefront/storefront/element/cms-element-' ~ element.type ~ '.html.twig' with {
        'element': element
     } %}
</div>

<div class="col-md-6">
    {% set element = block.slots.getSlot('right') %}

    {% sw_include '@Storefront/storefront/element/cms-element-' ~ element.type ~ '.html.twig' with {
        'element': element
     } %}
</div>
```

The `block` is automatically passed to the template and contains meta data and configuration values. See the `CmsBlockDefinition.php` for a full overview.

### How to Render Slots [​](#how-to-render-slots)

Slots contain elements that need to be rendered. Here are the key methods:

#### 1. Get a Slot by Name [​](#_1-get-a-slot-by-name)

TWIG

```shiki
{% set leftSlot = block.slots.getSlot('left') %}
```

#### 2. Render an Element [​](#_2-render-an-element)

Use `sw_include` to dynamically include the correct element template:

TWIG

```shiki
{% sw_include "@Storefront/storefront/element/cms-element-" ~ leftSlot.type ~ ".html.twig" with {
   'element': leftSlot
} %}
```

This dynamically builds the template path based on the element type. For example:

* If `leftSlot.type` is text, it renders cms-element-text.html.twig
* If `leftSlot.type` is image, it renders cms-element-image.html.twig

#### 3. Loop Through All Slots [​](#_3-loop-through-all-slots)

TWIG

```shiki
{% for slotName, slot in block.slots %}
    {% sw_include "@Storefront/storefront/element/cms-element-" ~ slot.type ~ ".html.twig" with {
        'element': slot
    } %}
{% endfor %}
```

## Next steps [​](#next-steps)

Now you've got your very own CMS block running, what about a custom CMS element? Head over to our guide, which will explain exactly that: [Creating a custom CMS element](./add-cms-element.html)

---

## Add CMS element

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/add-cms-element.html

# Add CMS Elements [​](#add-cms-elements)

## What is an Element? [​](#what-is-an-element)

A CMS element in Shopware is the smallest content unit in the Shopping Experience (CMS) system. Understanding the hierarchy helps clarify what elements are:

### CMS Hierarchy [​](#cms-hierarchy)

* Page - The top-level container (e.g., category page, shop page, product page)
* Section - Horizontal segments within a page (can be single-column or two-column with sidebar)
* Block - Units that usually span an entire row with custom layout and styling
* Slots - A named container inside a block. Each slot represents a designated area that can hold exactly one CMS element
* **Elements - The actual content primitives (text, image, video, product listing, etc.) placed inside slots**

Elements are the "primitives" in the CMS hierarchy. They have no knowledge of their context and contain minimal markup. Elements are always rendered inside slots of their parent blocks.

**Key concept**: Elements provide the actual content, while blocks define the structure and layout. This separation allows different element types to be placed in the same block slot.

> **Learn more**: For a deeper understanding of the CMS architecture, see the [Shopping Experience fundamental guide](https://developer.shopware.com/docs/concepts/commerce/content/shopping-experiences-cms.html).

## Where to Find Elements [​](#where-to-find-elements)

Elements are added to blocks within the Shopping Experience module:

* Navigate to Content → Shopping Experience
* Create a new layout or edit an existing one
* Add a block to your layout (blocks contain slots)
  + Blocks usually contain one or more predefined elements
* Click on the arrow icon on a slot within a block to see available elements
* Select an element to place it in the slot

You can find related element code here:

* Administration: `src/Administration/Resources/app/administration/src/module/sw-cms/elements/`
* Storefront: `src/Storefront/Resources/views/storefront/element/`
* Core: `\Shopware\Core\Content\Cms\SalesChannel\SalesChannelCmsPageLoader::load`

## How to Create an Element in the Administration [​](#how-to-create-an-element-in-the-administration)

We recommend this structure for CMS elements:

TEXT

```shiki
<plugin root>/src/Resources/app/administration/src/
├── main.js
└── module/
    └── sw-cms/
        └── elements/
            └── dailymotion/              (element name)
                ├── index.js
                ├── component/
                │   ├── index.js
                │   ├── cms-el-dailymotion.html.twig
                │   └── cms-el-dailymotion.scss
                ├── config/
                │   ├── index.js
                │   └── cms-el-config-dailymotion.html.twig
                └── preview/
                    ├── index.js
                    ├── cms-el-preview-dailymotion.html.twig
                    └── cms-el-preview-dailymotion.scss
```

### Step 1: Import Your Element in main.js [​](#step-1-import-your-element-in-main-js)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-cms/elements/dailymotion';
```

### Step 2: Register the Element [​](#step-2-register-the-element)

JS

```shiki
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/index.js
import './component';
import './config';
import './preview';

Shopware.Service('cmsService').registerCmsElement({
    name: 'dailymotion',
    label: 'cms.elements.dailymotion.label',
    component: 'cms-el-dailymotion',
    configComponent: 'cms-el-config-dailymotion',
    previewComponent: 'cms-el-preview-dailymotion',
    defaultConfig: {
        url: {
            source: 'static',
            value: '',
        },
    },
});
```

| Property | Description |
| --- | --- |
| name | Technical name of your element |
| label | Display name in the UI (preferably as a snippet key) |
| component | Vue component for rendering the element in the Administration |
| configComponent | Vue component for the configuration panel |
| previewComponent | Vue component for the element thumbnail in the element selector |
| defaultConfig | Default configuration values (key = config property, value = object with source and value) |
| hidden | (Optional) Hides the element in the "replace element" modal |
| removable | (Optional) Prevents the element from being removed from a slot via UI |

### Step 3: Create the Preview Component [​](#step-3-create-the-preview-component)

The preview is shown as a thumbnail when selecting or swapping elements in block slots. You could also display a static image of your final Storefront element here.

JS

```shiki
// dailymotion/preview/index.js
Shopware.Component.register('cms-el-preview-dailymotion', {
    template: `
        <div class="cms-el-preview-dailymotion">
            <h3>Dailymotion Embed</h3>
        </div>
    `,
});
```

### Step 4: Create the Main Component [​](#step-4-create-the-main-component)

The main component is displayed in the editor layout. It should provide a good representation of the final Storefront element.

JS

```shiki
// dailymotion/component/index.js
Shopware.Component.register('cms-el-dailymotion', {
    template: `
        <iframe
            v-if="element.config.url.value"
            class="cms-el-dailymotion"
            :src="embedUrl"
            width="100%"
            height="480"
        />
        <h3 v-else>Dailymotion</h3>
    `,
    mixins: [
        'cms-element'
    ],
    computed: {
        embedUrl() {
            return `https://www.dailymotion.com/embed/video/${this.element.config.url.value}`;
        },
    },
    created() {
        this.initElementConfig('dailymotion');
    },
});
```

**Key points**:

* The `cms-element` mixin provides common props and data-mapping for config objects
* Use fallback content to avoid invisible elements in the editor (for example when missing an `iframe` or `img` `src`)

### Step 5: Create the Configuration Component [​](#step-5-create-the-configuration-component)

This component will be displayed in a modal and should provide form fields for all options defined in Step 2 (`defaultConfig`).

JS

```shiki
// dailymotion/config/index.js
Shopware.Component.register('cms-el-config-dailymotion', {
    template: `<div class="cms-el-config-dailymotion">
        <mt-text-field
            v-model="element.config.url.value"
            label="Dailymotion video ID"
            placeholder="Enter Dailymotion video ID..."
        />
    </div>`,
    mixins: [
        'cms-element'
    ],
    created() {
        this.initElementConfig('dailymotion');
    },
});
```

**Key points**:

* The `cms-element` mixin provides common props and data-mapping for config objects
* Use [Shopware meteor components](https://shopware.design/meteor-components/) for a consistent UI

### Step 6: Inheritance Support For Elements [​](#step-6-inheritance-support-for-elements)

Inheritance in the CMS provides fine-grained control over how content is customized between the base layout and content pages (category, product, landing page, ..) they are assigned to. Similar to how product variants work, content managers can choose to either inherit the content from the base layout or override it with custom content for each page.

By default, configuration will be inherited unless explicitly overridden though the UI may not be as clear.

For an improved user experience when working with inherited fields, we provide a [wrapper component](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/module/sw-cms/component/sw-cms-inherit-wrapper/index.ts) that handles removing and restoring inherited values and displaying proper UI states. To use this is in your own elements, you can add the `sw-cms-inherit-wrapper` component to individual fields in your element.

VUE

```shiki
<!-- src/module/sw-cms/elements/text/config/sw-cms-el-config-text.html.twig -->
<sw-cms-inherit-wrapper
    field="verticalAlign"
    :element="element"
    :label="$t('sw-cms.elements.general.config.label.verticalAlign')"
>
    <template #default="{ isInherited }">
        <mt-select
            v-model:model-value="element.config.verticalAlign.value"
            :placeholder="$t('sw-cms.elements.general.config.label.verticalAlign')"
            :disabled="isInherited"
        />
    </template>
</sw-cms-inherit-wrapper>
```

You can find more references in the standard CMS elements located in `src/Administration/Resources/app/administration/src/module/sw-cms/elements/`.

## How to Create an Element in the Storefront [​](#how-to-create-an-element-in-the-storefront)

The Storefront template defines how your element appears on the actual storefront. It is expected to be located in the directory `src/Resources/views/storefront/element`. In there, a twig template file has to follow this naming convention:

* **Prefix**: `cms-element-`
* **Technical name**: `dailymotion` (the `name` property defined in Step 2)
* **Extension**: `.html.twig`

**Shopware is expecting the prefix as part of the full filename.**

Full example: `cms-element-dailymotion.html.twig`

### Basic Template [​](#basic-template)

You can create your own elements or extend and reuse existing ones. Don't forget to clear the Storefront cache after adding new templates.

TWIG

```shiki
{# <plugin root>/src/Resources/views/storefront/element/cms-element-dailymotion.html.twig #}

<div class="cms-element-dailymotion">
    <iframe
        src="https://www.dailymotion.com/embed/video/{{ element.config.url.value }}"
        frameborder="0"
        type="text/html"
        width="100%"
        height="480"
    />
</div>
```

The `element` is automatically passed to the template and contains meta data and configuration values. See the `CmsSlotDefinition.php` for a full overview.

## Next steps [​](#next-steps)

There are many possibilities to extend Shopware's CMS. If you haven't done so already, consider using your element in a cms block. To learn how to do this, take a look at the guide on [Add custom cms block](./add-cms-block.html).

---

## Add data to CMS element

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/add-data-to-cms-elements.html

# Add Data to CMS Element [​](#add-data-to-cms-element)

## Overview [​](#overview)

When creating custom CMS elements, you sometimes want to use more complex data types than text or boolean values, e.g., other entities such as media or products. In those cases you can implement a custom `CmsElementResolver` to resolve the configuration data.

## Prerequisites [​](#prerequisites)

This guide will not explain how to create custom CMS elements in general, so head over to the official guide about [Adding a custom CMS element](./add-cms-element.html) to learn this first.

## Create a data resolver [​](#create-a-data-resolver)

To manipulate the data of these elements during the loading of the configuration, we create a `DailyMotionCmsElementResolver` resolver in our plugin.

php

```shiki
// <plugin root>/src/DataResolver/DailyMotionCmsElementResolver.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\DataResolver;

use Shopware\Core\Content\Cms\Aggregate\CmsSlot\CmsSlotEntity;
use Shopware\Core\Content\Cms\DataResolver\Element\AbstractCmsElementResolver;
use Shopware\Core\Content\Cms\DataResolver\Element\ElementDataCollection;
use Shopware\Core\Content\Cms\DataResolver\ResolverContext\ResolverContext;
use Shopware\Core\Content\Cms\DataResolver\CriteriaCollection;

class DailyMotionCmsElementResolver extends AbstractCmsElementResolver
{
    public function getType(): string
    {
        return 'dailymotion';
    }

    public function collect(CmsSlotEntity $slot, ResolverContext $resolverContext): ?CriteriaCollection
    {
        return null;
    }

    public function enrich(CmsSlotEntity $slot, ResolverContext $resolverContext, ElementDataCollection $result): void
    {

    }
}
```

Our custom resolver extends from the `AbstractCmsElementResolver` which forces us to implement the methods `getType`, `collect` and `enrich`.

In the previous [example](./add-cms-element.html) we added a CMS element with the name `dailymotion`. As you can see the `getType` method of our custom resolver reflects that name by returning the `dailymotion` string. This resolver is called every time for an element of the type `dailymotion`.

To register our custom resolver to the service container, we have to register it in the `services.xml` file in our plugin.

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\DataResolver\DailyMotionCmsElementResolver">
            <tag name="shopware.cms.data_resolver" />
        </service>
    </services>
</container>
```

### Collect data [​](#collect-data)

The `collect` method prepares the criteria object. This is useful if, for example, you have a media entity `ID` stored in your configuration. As in the following example, you can retrieve the configuration for the current CMS element with the call `$slot->getFieldConfig()` and then have access to the individual fields. In this case we read out `myCustomMedia` field which may contain a mediaId. If a `mediaId` exists, we create a new `CriteriaCollection` for it. Now we are able to use this media object later on. If you want to add data from an [attribute entity](./../../framework/data-handling/entities-via-attributes.html), you do not have an explicit definition class. Instead, you pass `example_entity.defintion` as second parameter to the `CriteriaCollection::add()` method.

PLUGIN\_ROOT/src/DataResolver/DailyMotionCmsElementResolver.php

php

```shiki
<?php declare(strict_types=1);

// ...
use Shopware\Core\Content\Media\MediaDefinition;
use Shopware\Core\Content\Media\MediaEntity;
// ...

    public function collect(CmsSlotEntity $slot, ResolverContext $resolverContext): ?CriteriaCollection
    {
        $config = $slot->getFieldConfig();
        $myCustomMedia = $config->get('myCustomMedia');

        if (!$myCustomMedia) {
            return null;
        }

        $mediaId = $myCustomMedia->getValue();

        $criteria = new Criteria([$mediaId]);

        $criteriaCollection = new CriteriaCollection();
        $criteriaCollection->add('media_' . $slot->getUniqueIdentifier(), MediaDefinition::class, $criteria);

        return $criteriaCollection;
    }

// ...
```

### Enrich data [​](#enrich-data)

Inside the `enrich` you can perform additional logic on the data that has been resolved. Like in the `collect` method, we have access to our configuration fields and their values. Imagine you have stored some information in the element configuration and want to perform an external `Api` call to fetch some additional data. After that you can add the response information to the current slot data by calling `$slot->setData()`.

This could be a possible solution for that:

PLUGIN\_ROOT/src/DataResolver/DailyMotionCmsElementResolver.php

php

```shiki
<?php declare(strict_types=1);

// ...

    public function enrich(CmsSlotEntity $slot, ResolverContext $resolverContext, ElementDataCollection $result): void
    {
        $config = $slot->getFieldConfig();
        $myCustomApiPayload = $config->get('myCustomApiPayload');

        // perform some external api call with the payload `myCustomApiPayload`
        $myCustomAPI = new MyCustomAPI();

        $response = $myCustomAPI->query($myCustomApiPayload);

        if ($response) {
            $slot->setData($response);
        }
    }

// ...
```

### Event-based extensibility [​](#event-based-extensibility)

In Shopware’s CMS flow, CMS Elements are not “live bound” to the original entity (e.g. a product). Instead, during the slot-resolution, resolvers copy values from the entity into internal CMS structs (for example, `ProductNameCmsElementResolver` takes the string `name` from the `product` entity and writes it into the CMS text element). Once that copy is done, the storefront rendering reads from the CMS structs — not from the original entity. Therefore: if you wait until a “page loaded” event (e.g. `ProductPageLoadedEvent`) after the copying happened, changing the underlying entity has no effect on what is displayed in the CMS output. To make modifications effective (e.g. change product name, adjust a field, override some data), you must intervene before or after the resolver runs — i.e. at a point in the CMS resolution pipeline where the entity is still used for populating the CMS slots.

#### Available Extensions / Events [​](#available-extensions-events)

Shopware exposes three CMS extension classes under `Shopware\Core\Content\Cms\Extension`. These extension classes follow the common Extension Point Pattern in Shopware and publish named hooks that you can subscribe to (the classes usually expose a `NAME` constant used as the event identifier). All three extension points are dispatched with lifecycle suffixes such as `.pre` and `.post`, so you will typically see event names like `cms-slots-data.resolve.pre` or `cms-slots-data.resolve.post`. Using the `.pre` hook lets you intervene before the respective phase runs; `.post` runs after the phase finished.

* `CmsSlotsDataCollectExtension` - This event (`cms-slots-data.collect` + suffix) allows interception of the collection process, where a criteria list is populated using the respective CMS resolver. The resulting criteria list is then used to load CMS elements during the CMS page resolution process.
* `CmsSlotsDataEnrichExtension` - This event (`cms-slots-data.enrich` + suffix) allows interception of the enrichment process, during which CMS slots used in a rendered CMS page are populated with data loaded by the respective CMS resolver from the search results.
* `CmsSlotsDataResolveExtension` - This event (`cms-slots-data.resolve` + suffix) enables interception of the resolution process, allowing the collection of CMS slot data and enrichment of slots by their respective CMS resolvers.

#### Example Workflow: Modifying Product Data Before CMS Rendering [​](#example-workflow-modifying-product-data-before-cms-rendering)

Here is a rough outline of how you would implement a subscriber to change some product properties before they end up in CMS elements:

1. Create an event subscriber for the CMS slot resolution event.
2. In the listener method, inspect the `ResolverContext` (or event payload) and check whether the entity is an instance of the type you care about (e.g. `ProductEntity`).
3. Modify the entity (e.g. `$entity->setName(...)`, set custom fields, translations, etc.).
4. Let execution continue, so the built-in resolvers pick up your modified entity and fill CMS elements accordingly.
5. Test frontend — changes should be visible.

#### PHP example (simplified) [​](#php-example-simplified)

PHP

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

// ...

class CmsPreResolveSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            'cms-slots-data.resolve.pre' => 'onCmsSlotsResolvePre',
        ];
    }

    public function onCmsSlotsResolvePre(CmsSlotsDataResolveExtension $event): void
    {
        $resolverContext = $event->getResolverContext();
        $entity = $resolverContext->getEntity();

        if ($entity instanceof ProductEntity) {
            // modify e.g. the name
            $entity->setName('New custom name');
            // optionally modify other fields
        }
    }
}

// ...
```

---

## Mail

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/mail/

# Mail [​](#mail)

Shopware Mail offers the ability to add mail data and configure mail templates for various email communications within the e-commerce platform. You can add relevant mail data such as transactional emails, order notifications, customer communication, marketing campaigns, or newsletters. These emails can be tailored to specific events or triggers, ensuring timely and personalized communication with customers.

The plugin provides the functionality to create and customize these mail templates. Users can design and format the content of their emails, including text, images, logos, and dynamic variables, to personalize the messages. This allows for consistent branding and a professional appearance across all outgoing emails.

By utilizing this plugin, businesses can effectively engage with their customers and keep them informed about order updates, promotions, or other relevant information.

---

## Add data to mails

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/mail/add-data-to-mails.html

# Add Data to Mails [​](#add-data-to-mails)

## Overview [​](#overview)

The mail templates in Shopware have access to a given set of data, e.g. the customer data, the order data, etc. Sometimes you want add your custom entity to that data set though, so you can use this data in your mail templates as well.

This guide will teach you how to add new data to the mail templates using your plugin.

## Prerequisites [​](#prerequisites)

This guide is built upon our [plugin base guide](./../../plugin-base-guide.html), whose namespace is going to be used in the examples of this guide. However, you can use those examples with any plugin, you'll just have to adjust the namespace and the directory the files are located in.

Furthermore, you should know how to [decorate a service](./../../plugin-fundamentals/adjusting-service.html).

## Adding data via decorator [​](#adding-data-via-decorator)

In order to add new data to the mail templates, you'll have to decorate the [MailService](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Mail/Service/MailService.php).

To be precise, you have to extend the `send` method, whose last parameter is the `$templateData`, that we want to enrich.

So let's do that, here's an example of a decorated mail service:

PLUGIN\_ROOT/src/Service/AddDataToMails.php

php

```shiki
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Mail\Service\AbstractMailService;
use Shopware\Core\Framework\Context;
use Symfony\Component\Mime\Email;

class AddDataToMails extends AbstractMailService
{
    /**
     * @var AbstractMailService
     */
    private AbstractMailService $mailService;

    public function __construct(AbstractMailService $mailService)
    {
        $this->mailService = $mailService;
    }

    public function getDecorated(): AbstractMailService
    {
        return $this->mailService;
    }

    public function send(array $data, Context $context, array $templateData = []): ?Email
    {
        $templateData['myCustomData'] = 'Example data';

        return $this->mailService->send($data, $context, $templateData);
    }
}
```

If you don't recognise the decoration pattern used here, make sure to have a look at our guide about [decorations](./../../plugin-fundamentals/adjusting-service.html).

As always, we're passing in the original `MailService` as a constructor parameter, so we can return it in the `getDecorated` method, as well as use the original `send` method after having adjusted the `$templateData`.

In this example, we're adding `myCustomData` to the `$templateData`, so that one should be available then.

If we add `{{ myCustomData }}` to any mail template, it should then print "Example data". You can use any kind of data here, e.g. an array of data.

### Register your decorator [​](#register-your-decorator)

Of course you still have to register the decoration to the service container. Beware of the `decorates` attribute of our service.

Here's the respective example `services.xml`:

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\AddDataToMails" decorates="Shopware\Core\Content\Mail\Service\MailService">
            <argument type="service" id="Swag\BasicExample\Service\AddDataToMails.inner" />
        </service>
    </services>
</container>
```

## Adding data via subscriber [​](#adding-data-via-subscriber)

In many cases, adding mail data via an event subscriber is a suitable solution. This way, you avoid the overhead of decorating the mail service. Simply create an event subscriber and listen to the `MailBeforeValidateEvent` event. There, you can safely add template or mail data. Here is a small example:

PLUGIN\_ROOT/src/Subscriber/MyMailSubscriber.php

php

```shiki
<?php

declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\MailTemplate\Service\Event\MailBeforeValidateEvent;

class MyMailSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            MailBeforeValidateEvent::class => 'beforeMailValidate',
        ];
    }

    public function beforeMailValidate(
        MailBeforeValidateEvent $event
    ): void {
        $context = $event->getContext();
        $data = $event->getData(); // Get mail data
        $templateData = $event->getTemplateData(); // Get mail template data

        $event->addTemplateData('key', 'value'); // Example of adding data to the mail template
    }
}
```

### Register your event subscriber [​](#register-your-event-subscriber)

You have to register the subscriber to the service container as well.

Here's the respective example `services.xml`:

PLUGIN\_ROOT/src/Resources/config/services.xml

xml

```shiki
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\MyMailSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

---

## Add mail templates

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/mail/add-mail-template.html

# Add Mail Templates [​](#add-mail-templates)

## Overview [​](#overview)

You can add new mail templates to Shopware by using the Administration. However, you might want to ship a mail template with your plugin, so using the Administration is no option.

This guide will cover how to add a custom mail template with your plugin.

## Prerequisites [​](#prerequisites)

The namespaces used in the examples of this guide are the same as the namespace from our [Plugin base guide](./../../plugin-base-guide.html), so you might want to have a look at it first.

Furthermore, this guide will use [Database migrations](./../../plugin-fundamentals/database-migrations.html) in order to add a custom mail template, which is not explained in depth here. Make sure to understand those first!

## Adding a mail template via migration [​](#adding-a-mail-template-via-migration)

As already mentioned, adding a mail template is done by using a plugin database migration. To be precise, those are the steps necessary:

* Create a new mail template type or fetch an existing mail template type ID
* Add an entry to `mail_template` using the said template type ID
* Add an entry to `mail_template_translation` for each language you want to support

The following example will create a new template of type "contact form", which is already available. There will be an example to create a custom mail template type though.

Let's have a look at an example, which will:

* Use the "contact form" type
* Add a mail template entry
* Add a mail template translation for en\_GB and de\_DE

php

```shiki
// <plugin root>/src/Migration/Migration1616418675AddMailTemplate.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use DateTime;
use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1616418675AddMailTemplate extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1616418675;
    }

    public function update(Connection $connection): void
    {
        $mailTemplateTypeId = $this->getMailTemplateTypeId($connection);

        $this->createMailTemplate($connection, $mailTemplateTypeId);
    }

    public function updateDestructive(Connection $connection): void
    {
    }

    private function getMailTemplateTypeId(Connection $connection): string
    {
        $sql = <<<SQL
            SELECT id
            FROM mail_template_type
            WHERE technical_name = "contact_form"
        SQL;

        return Uuid::fromBytesToHex($connection->fetchOne($sql));
    }

    private function getLanguageIdByLocale(Connection $connection, string $locale): ?string
    {
        $sql = <<<SQL
        SELECT `language`.`id`
        FROM `language`
        INNER JOIN `locale` ON `locale`.`id` = `language`.`locale_id`
        WHERE `locale`.`code` = :code
        SQL;

        $languageId = $connection->executeQuery($sql, ['code' => $locale])->fetchOne();

        if (empty($languageId)) {
            return null;
        }

        return $languageId;
    }

    private function createMailTemplate(Connection $connection, string $mailTemplateTypeId): void
    {
        $mailTemplateId = Uuid::randomHex();

        $enGbLangId = $this->getLanguageIdByLocale($connection, 'en-GB');
        $deDeLangId = $this->getLanguageIdByLocale($connection, 'de-DE');

        $connection->executeStatement("
        INSERT IGNORE INTO `mail_template`
            (id, mail_template_type_id, system_default, created_at)
        VALUES
            (:id, :mailTemplateTypeId, :systemDefault, :createdAt)
        ",[
            'id' => Uuid::fromHexToBytes($mailTemplateId),
            'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
            'systemDefault' => 0,
            'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ]);

        if (!empty($enGbLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_translation`
                (mail_template_id, language_id, sender_name, subject, description, content_html, content_plain, created_at)
            VALUES
                (:mailTemplateId, :languageId, :senderName, :subject, :description, :contentHtml, :contentPlain, :createdAt)
            ",[
                'mailTemplateId' => Uuid::fromHexToBytes($mailTemplateId),
                'languageId' => $enGbLangId,
                'senderName' => '{{ salesChannel.name }}',
                'subject' => 'Example mail template subject',
                'description' => 'Example mail template description',
                'contentHtml' => $this->getContentHtmlEn(),
                'contentPlain' => $this->getContentPlainEn(),
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        if (!empty($deDeLangId)) {            
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_translation`
                (mail_template_id, language_id, sender_name, subject, description, content_html, content_plain, created_at)
            VALUES
                (:mailTemplateId, :languageId, :senderName, :subject, :description, :contentHtml, :contentPlain, :createdAt)
            ",[
                'mailTemplateId' => Uuid::fromHexToBytes($mailTemplateId),
                'languageId' => $deDeLangId,
                'senderName' => '{{ salesChannel.name }}',
                'subject' => 'Beispiel E-Mail Template Titel',
                'description' => 'Beispiel E-Mail Template Beschreibung',
                'contentHtml' => $this->getContentHtmlDe(),
                'contentPlain' => $this->getContentPlainDe(),
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

    }

    private function getContentHtmlEn(): string
    {
        return <<<MAIL
        <div style="font-family:arial; font-size:12px;">
            <p>
                Example HTML content!
            </p>
        </div>
        MAIL;
    }

    private function getContentPlainEn(): string
    {
        return <<<MAIL
        Example plain content!
        MAIL;
    }

    private function getContentHtmlDe(): string
    {
        return <<<MAIL
        <div style="font-family:arial; font-size:12px;">
            <p>
                Beispiel HTML Inhalt!
            </p>
        </div>
        MAIL;
    }

    private function getContentPlainDe(): string
    {
        return <<<MAIL
        Beispiel Plain Inhalt!
        MAIL;
    }
}
```

First of all, let's have a look at the small `update` method. It's mainly just fetching the mail template type ID using a short SQL statement and afterwards it executes the method `createMailTemplate`, which will cover all the other steps.

Now on to the `createMailTemplate` method, which looks big, but isn't that scary. First of all, we're fetching the language IDs for both `en-GB` and `de-DE`.

We then create the entry for the `mail_template` table. Make sure to set `system_default` to 0 here!

Afterwards we're inserting the entries into the `mail_template_translation` table. For compatibility reasons we have to check whether the languages exist in the database so we can insert our translations for these languages. The same principle applies to other ISO languages.

The variables for the English and the German subject and description, may be changed to fit your needs.

Each of those calls uses a little helper method `getContentHtml` or `getContentPlain` respectively, where you can use your template.

And that's it, once your plugin is installed, the mail template will be added to Shopware.

WARNING

Do not remove e-mail templates in your plugin, e.g. when it is uninstalled. This may lead to data inconsistency, since those templates can be associated to other entities. Beware to use `IGNORE` before `INTO` Statements so no exception will be thrown upon uninstallation and reinstallation of your plugin.

### Creating a custom mail type [​](#creating-a-custom-mail-type)

In order to not only use an existing mail template type, but to create a custom one, you have to adjust the `update` method and create a new method.

Let's have a look:

php

```shiki
// <plugin root>/src/Migration/Migration1616418675AddMailTemplate.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use DateTime;
use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1616418675AddMailTemplate extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1616418675;
    }

    public function update(Connection $connection): void
    {
        $mailTemplateTypeId = $this->createMailTemplateType($connection);

        $this->createMailTemplate($connection, $mailTemplateTypeId);
    }

    private function createMailTemplateType(Connection $connection): string
    {
        $mailTemplateTypeId = Uuid::randomHex();

        $enGbLangId = $this->getLanguageIdByLocale($connection, 'en-GB');
        $deDeLangId = $this->getLanguageIdByLocale($connection, 'de-DE');

        $englishName = 'Example mail template type name';
        $germanName = 'Beispiel E-Mail Template Name';

        $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type`
                (id, technical_name, available_entities, created_at)
            VALUES
                (:id, :technicalName, :availableEntities, :createdAt)
        ",[
            'id' => Uuid::fromHexToBytes($mailTemplateTypeId),
            'technicalName' => 'custom_mail_template_type',
            'availableEntities' => json_encode(['product' => 'product']),
            'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ]);

        if (!empty($enGbLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type_translation`
                (mail_template_type_id, language_id, name, created_at)
            VALUES
                (:mailTemplateTypeId, :languageId, :name, :createdAt)
            ",[
                'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
                'languageId' => $enGbLangId,
                'name' => $englishName,
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        if (!empty($deDeLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type_translation`
                (mail_template_type_id, language_id, name, created_at)
            VALUES
                (:mailTemplateTypeId, :languageId, :name, :createdAt)
            ",[
                'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
                'languageId' => $deDeLangId,
                'name' => $germanName,
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        return $mailTemplateTypeId;
    }

    // ...
}
```

First of all we changed the `getMailTemplateTypeId` method call to `createMailTemplateType`, a new method which we will create afterwards. Again, this method then has to return the ID of the newly created mail template ID.

So having a look at the `createMailTemplateType` method, you will see some similarities:

* First of all we're fetching the language IDs for `en-GB` and `de-DE`
* Then we define the translated names for the mail template type
* And then the respective `mail_template_type` entry, as well as the translated `mail_template_type_translation` entries are created

Note the `available_entities` column when creating the mail template type itself though. In here, you define which entities should be available for the respective mail template, in this example we'll just provide the `ProductEntity`.

## Next steps [​](#next-steps)

Now that you know how to add custom mail templates, you might wonder how you can actually add new mail template data to existing mail templates.

For that case, we've created a separate guide about [adding data to mail templates](./add-data-to-mails.html).

---

## Media

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/media/

# Media [​](#media)

Shopware Media offers the ability to add media file extensions and prevent the deletion of media files within the e-commerce platform.

With the Media plugin, users can specify and configure new media file extensions. This allows businesses to define different types of media files, such as images, videos, or documents, that can be uploaded and used within the Shopware platform.

Furthermore, the plugin helps prevent the deletion of media files that are not used in your application.

---

## Prevent Deletion of Media Files Referenced in your Plugins

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/media/prevent-deletion-of-media-files-referenced-in-your-plugins.html

# Prevent Deletion of Media Files Referenced in your Plugins [​](#prevent-deletion-of-media-files-referenced-in-your-plugins)

INFO

The ability to prevent Media entities from being deleted is available since Shopware 6.5.1.0.

## Overview [​](#overview)

The Shopware CLI application provides a `media:delete-unused` command which deletes all media entities and their corresponding files which are not used in your application. Not used means that it is not referenced by any other entity. This works well in the simple case that all your entity definitions store references to Media entities with correct foreign keys.

However, this does not cover all the possible cases, even for many internal Shopware features. For example the CMS entities store their configuration as JSON blobs with references to Media IDs stored in a nested data structure.

In order to fix the case of Media references that cannot be resolved without knowledge of the specific entity and its features, an extension point is provided via an event.

If you are developing an extension which references Media entities, and you cannot use foreign keys, this guide will detail how to prevent shopware deleting the Media entities your extension references.

## Prerequisites [​](#prerequisites)

As most of our plugin guides, this guide was also built upon our [Plugin base guide](./../../plugin-base-guide.html). Furthermore, you'll have to know about adding classes to the [Dependency injection](./../../plugin-fundamentals/dependency-injection.html) container and about using a subscriber in order to [Listen to events](./../../plugin-fundamentals/listening-to-events.html).

## The deletion process [​](#the-deletion-process)

The `\Shopware\Core\Content\Media\UnusedMediaPurger` service first searches for Media entities that are not referenced by any other entities in the system via foreign keys. Then it dispatches an event containing the Media IDs it believes are unused.

The event is an instance of `\Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent`. A subscriber can then cross-reference the Media IDs scheduled to be deleted and mark any of them as *used*.

The remaining Media IDs will then be deleted by the `\Shopware\Core\Content\Media\UnusedMediaPurger` service.

Please note that this process is completed in small batches to maintain stability, so the event may be dispatched multiple times when an installation has many unused Media entities.

## Adding a subscriber [​](#adding-a-subscriber)

In this section, we're going to register a subscriber for the `\Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent` event.

Have a look at the following code example:

php

```shiki
// <plugin root>/src/Subscriber/UnusedMediaSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class UnusedMediaSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            UnusedMediaSearchEvent::class => 'removeUsedMedia',
        ];
    }

    public function removeUsedMedia(UnusedMediaSearchEvent $event): void
    {
        $idsToBeDeleted = $event->getUnusedIds();
    
        $doNotDeleteTheseIds = $this->getUsedMediaIds($idsToBeDeleted);
    
        $event->markAsUsed($doNotDeleteTheseIds);
    }
    
    private function getUsedMediaIds(array $idsToBeDeleted): array
    {
        // do something to get the IDs that are used
        return [];
    }
}
```

You can use the method `getUnusedIds` of the `$event` variable to get the current an array of Media IDs scheduled for removal.

You can use these IDs to query whatever storage your plugin uses to store references to Media entities, to check if they are currently used.

If any of the IDs are used by your plugin, you can use the method `markAsUsed` of the `$event` variable to prevent the Media entities from being deleted. `markAsUsed` accepts an array of string IDs.

If your storage is a relational database such as MySQL you should, when possible, use direct database queries to check for references. This saves memory and CPU cycles by not loading unnecessary data.

Imagine an extension which provides an image slider feature. An implementation of `getUsedMediaIds` might look something like the following:

php

```shiki
// <plugin root>/src/Subscriber/UnusedMediaSubscriber.php
private function getUsedMediaIds(array $idsToBeDeleted): array
{
    $sql = <<<SQL
    SELECT JSON_EXTRACT(slider_config, "$.images") as mediaIds FROM my_slider_table
    WHERE JSON_OVERLAPS(
        JSON_EXTRACT(slider_config, "$.images"),
        JSON_ARRAY(?)
    );
    SQL;

    $usedMediaIds = $this->connection->fetchFirstColumn(
        $sql,
        [$event->getUnusedIds()],
        [ArrayParameterType::STRING]
    );

    return array_map(fn (string $ids) => json_decode($ids, true, \JSON_THROW_ON_ERROR), $usedMediaIds);
}
```

In the above example, `$this->connection` is an instance of `\Doctrine\DBAL\Connection` which can be injected in to your subscriber. We use the MySQL JSON functions to query the table `my_slider_table`. We check if there are any references to the Media IDs from the event, in the `slider_config` column which is a JSON blob. The `JSON_EXTRACT` function looks into the `images` key of the data. We use the where condition in combination with the `JSON_OVERLAPS` function to only query rows that have references to the Media IDs we are interested in.

Finally, we return all the IDs of Media which are used in the slider config so that they are not deleted.

Make sure to register your event subscriber to the [Dependency injection container](./../../plugin-fundamentals/dependency-injection.html) by using the tag `kernel.event_subscriber`.

---

## Add custom media extension

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/media/add-custom-file-extension.html

# Add Custom Media File Extension [​](#add-custom-media-file-extension)

## Overview [​](#overview)

You might have come across the fact, that you cannot just upload any type of media to Shopware by using the Media module in the Administration. If that's the case for you, this guide will be the solution. It will provide an explanation on how you can add new allowed file extensions to Shopware using a plugin.

## Prerequisites [​](#prerequisites)

As most of our plugin guides, this guide was also built upon our [Plugin base guide](./../../plugin-base-guide.html). Furthermore, you'll have to know about adding classes to the [Dependency injection](./../../plugin-fundamentals/dependency-injection.html) container and about using a subscriber in order to [Listen to events](./../../plugin-fundamentals/listening-to-events.html).

## Adding a custom extension [​](#adding-a-custom-extension)

In this section, we're going to take care of allowing a new extension to Shopware first, without letting Shopware know exactly what kind of file this new extension represents (Images, videos, documents, ...).

For this to work, all you have to do is to register to the `MediaFileExtensionWhitelistEvent` event, which can be found [here](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Media/File/FileSaver.php#L397-L398). This is of course done via a [subscriber](./../../plugin-fundamentals/listening-to-events.html).

Have a look at the following code example:

php

```shiki
// <plugin root>/src/Service/Subscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Media\Event\MediaFileExtensionWhitelistEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class Subscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            MediaFileExtensionWhitelistEvent::class => 'addEntryToFileExtensionWhitelist'
        ];
    }

    public function addEntryToFileExtensionWhitelist(MediaFileExtensionWhitelistEvent $event): void
    {
        $whiteList = $event->getWhitelist();
        $whiteList[] = 'img';

        $event->setWhitelist($whiteList);
    }
}
```

You can use the method `getWhitelist` of the `$event` variable to get the current whitelist, which is just a plain array of extensions. Therefore you can add new array entries and then set the array back to the `$event` instance by using the respective setter method `setWhitelist`.

And that's it already! Shopware will now allow uploading files with the extension `.img`.

## Recognising the new extension [​](#recognising-the-new-extension)

There is another thing you most likely want to do here. While you can add new extensions like mentioned above, Shopware does not automatically recognise which kind of extension it is dealing with. Is it a new image extension and should be displayed as such? Is it a video file extension? Maybe a new kind of document?

In order to let Shopware know which kind of type we're dealing with, you can add a new `TypeDetector` class to let Shopware know about your new extension.

In the following example we'll imagine that we've added a new **image** extension called `img`, like we did above, and we're going to let Shopware know about it.

What we'll be doing now, is to add a custom `TypeDetector` class which returns an `ImageType` if the extension of the file to be checked matches our type detector. Have a look at the following example:

You will have to create a new class which implements from the interface `TypeDetectorInterface`. This will come with the requirement of having a `detect` method, which will return the respective media type.

Inside of the `detect` method, we're first checking if the file extension matches our allowed extensions, in this case only `img`. If that's not the case, just return the `$previouslyDetectedType`, which most likely comes from the `DefaultTypeDetector` and which tried to detect the type already by analysing the file's MIME-type.

If the extension does indeed match, we're for sure going to return `ImageType` here. Make sure to add flags to your media type, e.g. the `transparent` flag, or if it's an animated image.

You can find all available flags in their respective media type classes, e.g. [here](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Media/MediaType/ImageType.php#L7-L10) for the image media type.

Make sure to register your new type detector to the [Dependency injection container](./../../plugin-fundamentals/dependency-injection.html) by using the tag `shopware.media_type.detector`.

Shopware will now recognise your new image extension and handle your new file like an image.

---

## Remote Thumbnail Generation

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/media/remote-thumbnail-generation.html

# Remote Thumbnail Generation [​](#remote-thumbnail-generation)

INFO

This feature is available starting with Shopware version 6.6.4.0

In certain scenarios, you might want to disable the filesystem thumbnail generation in Shopware and use an external CDN service to handle the thumbnails. This can be beneficial for performance and scalability reasons. When the remote thumbnail configuration is enabled, the thumbnail images and thumbnail records in the database are not generated by Shopware, but by the external service.

## Configuration [​](#configuration)

To use remote thumbnails, you need to adjust the following parameters in your `config/packages/shopware.yaml`:

yaml

```shiki
shopware:
  media:
    remote_thumbnails:
      enable: true
      pattern: '{mediaUrl}/{mediaPath}?width={width}&ts={mediaUpdatedAt}'
```

1. `shopware.media.remote_thumbnails.enable`: Set this parameter to `true` to enable remote thumbnails.
2. `shopware.media.remote_thumbnails.pattern`: This parameter defines the URL pattern for your remote thumbnails. Replace it with your actual URL pattern.

The pattern supports the following variables:

* `mediaUrl`: The base URL of the media file.
* `mediaPath`: The media file path relative to the `mediaUrl`.
* `width`: The width of the thumbnail.
* `height`: The height of the thumbnail.
* `mediaUpdatedAt`: The timestamp of the last media change.

For example, by default, the pattern was set as `{mediaUrl}/{mediaPath}?width={width}&ts={mediaUpdatedAt}`, the thumbnail URL would be generated as `https://yourshop.example/abc/123/456.jpg?width=80&ts=1718954838`.

## Usage [​](#usage)

Once the configuration is set, Shopware will automatically use the defined pattern to generate thumbnail URLs. These URLs will point to the external CDN service, which should handle generating and delivering the thumbnail images.

Please note that the external service needs to be able to handle the URL pattern and generate the appropriate thumbnails based on the provided parameters.

## Invalidating Thumbnails with Fastly [​](#invalidating-thumbnails-with-fastly)

If you are using Fastly as your CDN, you can let Shopware invalidate the cached thumbnails when the media is updated. To do this, you need to configure your Fastly API key in your `config/packages/shopware.yaml`:

yaml

```shiki
shopware:
  cdn:
    fastly:
      api_key: YOUR_FASTLY_API_KEY
```

## Conclusion [​](#conclusion)

By using remote thumbnails, you can offload the task of thumbnail generation to an external service, potentially improving the performance and scalability of your Shopware installation.

---

## SEO

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/seo/

# SEO [​](#seo)

The Shopware SEO feature offers comprehensive tools to optimize the search engine visibility of your e-commerce platform.

## SEO URLs [​](#seo-urls)

You can create custom SEO URLs for product pages, categories, content pages, and other relevant sections of the website. The plugin allows businesses to customize meta tags for each page, including meta titles, descriptions, and keywords. This enables users to optimize the on-page SEO elements, providing search engines with relevant information about the content of the page.

[Add custom SEO URLs](add-custom-seo-url)

## Robots configuration [​](#robots-configuration)

Shopware provides full support for `robots.txt` configuration, including all standard directives, user-agent blocks, and extensibility through events. You can customize how search engine crawlers interact with your shop by extending the `robots.txt` parsing and generation.

[Extend robots configuration](extend-robots-txt)

---

## Add custom SEO URLs

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/seo/add-custom-seo-url.html

# Add custom SEO URLs [​](#add-custom-seo-urls)

## Overview [​](#overview)

Every good website had to deal with it at some point: SEO URLs. Of course Shopware supports the usage of SEO URLs, e.g. for products or categories.

This guide however will cover the question on how you can define your own SEO URLs, e.g. for your own custom entities. This will include both static SEO URLs, as well as dynamic SEO URLs.

## Prerequisites [​](#prerequisites)

As every almost every guide in the plugins section, this guide as well is built upon the plugin base guide.

[Plugin Base Guide](../../plugin-base-guide)

Furthermore, we're going to use a [Custom storefront controller](./../../storefront/add-custom-controller.html) for the static SEO URL example, as well as [Custom entities](./../../framework/data-handling/add-custom-complex-data.html) for the dynamic SEO URLs. Make sure you know and understand those two as well before diving deeper into this guide. Those come with two different solutions:

* Using [plugin migrations](./../../plugin-fundamentals/database-migrations.html) for static SEO URLs
* Using [DAL events](./../../framework/data-handling/using-database-events.html) to react on entity changes and therefore generating a dynamic SEO URL

## Custom SEO URLs [​](#custom-seo-urls)

As already mentioned in the overview, this guide will be divided into two parts: Static and dynamic SEO URLs.

### Static SEO URLs [​](#static-seo-urls)

A static SEO URL doesn't have to change every now and then. Imagine a custom controller, which is accessible via the link `yourShop.com/example`.

Now if you want this URL to be translatable, you'll have to add a custom SEO URL to your controller route, so it is accessible using both `Example-Page` in English, as well as e.g. `Beispiel-Seite` in German.

#### Example controller [​](#example-controller)

For this example, the controller from the [Add custom controller guide](./../../storefront/add-custom-controller.html) is being used. It creates a controller with a route like the example mentioned above: `/example`

Let's now have a look at our example controller:

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
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'])]
    public function showExample(): Response
    {
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

The important information you'll need here is the route name, `frontend.example.example`, as well as the route itself: `/example`. Make sure to remember those for the next step.

#### Example migration [​](#example-migration)

Creating a SEO URL in this scenario can be achieved by creating a [plugin migration](./../../plugin-fundamentals/database-migrations.html).

The migration has to insert an entry for each sales channel and language into the `seo_url` table. For this case, we're making use of the `ImportTranslationsTrait`, which comes with a helper method `importTranslation`.

Don't be confused here, we'll just treat the `seo_url` table like a translation table, since it also needs a `language_id` and respective translated SEO URLs. You'll have to pass a German and an English array into an instance of the `Translations` class, which is then the second parameter for the `importTranslation` method.

Let's have a look at an example:

php

```shiki
// <plugin root>/src/Migration/Migration1619094740AddStaticSeoUrl.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Core\Migration\Traits\ImportTranslationsTrait;
use Shopware\Core\Migration\Traits\Translations;

class Migration1619094740AddStaticSeoUrl extends MigrationStep
{
    use ImportTranslationsTrait;

    public function getCreationTimestamp(): int
    {
        return 1619094740;
    }

    public function update(Connection $connection): void
    {
        $this->importTranslation('seo_url', new Translations(
            // German array
            array_merge($this->getSeoMetaArray($connection), ['seo_path_info' => 'Beispiel-Seite']),
            // English array
            array_merge($this->getSeoMetaArray($connection), ['seo_path_info' => 'Example-Page']),

        ), $connection);
    }

    public function updateDestructive(Connection $connection): void
    {
    }

    private function getSeoMetaArray(Connection $connection): array
    {
        return [
            'id' => Uuid::randomBytes(),
            'sales_channel_id' => $this->getStorefrontSalesChannelId($connection),
            'foreign_key' => Uuid::randomBytes(),
            'route_name' => 'frontend.example.example',
            'path_info' => '/example',
            'is_canonical' => 1,
            'is_modified' => 0,
            'is_deleted' => 0,
        ];
    }

    private function getStorefrontSalesChannelId(Connection $connection): ?string
    {
        $sql = <<<SQL
            SELECT id
            FROM sales_channel
            WHERE type_id = :typeId
SQL;
        $salesChannelId = $connection->fetchOne($sql, [
            ':typeId' => Uuid::fromHexToBytes(Defaults::SALES_CHANNEL_TYPE_STOREFRONT)
        ]);

        if (!$salesChannelId) {
            return null;
        }

        return $salesChannelId;
    }
}
```

You might want to have a look at the `getSeoMetaArray` method, that we implemented here. Most important for you are the columns `route_name` and `path_info` here, which represent the values you've defined in your controller's route attributes.

By using the default PHP method `array_merge`, we're then also adding our translated SEO URL to the column `seo_path_info`.

And that's it! After installing our plugin, you should now be able to access your controller's route with the given SEO URLs.

INFO

You can only access the German SEO URL if you've configured a German domain in your respective sales channel first.

### Dynamic SEO URLs [​](#dynamic-seo-urls)

Dynamic SEO URLs are URLs, that have to change every now and then. Yet, there's another separation necessary.

If you're going to generate custom SEO URLs for your custom entities, you'll have to follow the section about [Dynamic SEO URLs for entities](./add-custom-seo-url.html#dynamic-seo-urls-for-entities). For all other kinds of dynamic content, that are not DAL entities, the section about [Dynamic SEO URLs for other content](./add-custom-seo-url.html#dynamic-seo-urls-for-custom-content) is your way to go.

#### Dynamic SEO URLs for entities [​](#dynamic-seo-urls-for-entities)

This scenario will be about a custom entity, to be specific we're going to use the entity from our guide about [adding custom complex data](./../../framework/data-handling/add-custom-complex-data.html), which then would have a custom Storefront route for each entity.

Each entity comes with a name, which eventually should be the SEO URL. Thus, your entity named `Foo` should be accessible using the route `yourShop.com/Foo` or `yourShop.com/Entities/Foo` or whatever you'd like. Now, everytime you create a new entity, a SEO URL has to be automatically created as well. When you update your entities' name, guess what, you'll have to change the SEO URL as well.

For this scenario, you can make use of the Shopware built-in `SeoUrlRoute` classes, which hold all necessary information about your dynamic route and will then create the respective `seo_url` entries automatically.

Let's first have a look at such an example class:

Okay, so let's look through this step by step.

Your custom "SeoUrlRoute" class has to implement the `SeoUrlRouteInterface`, which comes with three necessary methods:

* `getConfig`: Here you have to return an instance of `SeoUrlRouteConfig`, containing your entity's definition,

  the technical name of the route to be used, and the desired SEO path.
* `prepareCriteria`: Here you can adjust the criteria instance, which will be used to fetch your entities.

  Here you can e.g. narrow down which entities may be used for the SEO URL generation. For example you could add a filter

  on an `active` field and therefore only generate SEO URLs for active entities. Also you can add associations here,

  which will then be available with the entity provided in the `getMapping` method.
* `getMapping`: In this method you have to return an instance of `SeoUrlMapping`. It has to contain the actually

  available data for the SEO URL template. If you're using a variable `example.name` in the SEO URL template, you have to

  provide the data for the key `example` here.

Make sure to check which kind of entity has been applied to the `getMapping` method, since you don't want to provide mappings for other entities than your custom one.

It then has to be registered to the container using the tag `shopware.seo_url.route`.

Now that you've set up this class, there are two more things to be done, which are covered in the next sections.

**Example subscriber**

Every time your entity is written now, you have to let Shopware know, that you want to generate the SEO URLs for those entities now. This is done by reacting to the [DAL events](./../../framework/data-handling/using-database-events.html) of your custom entity, to be specific we're going to use the `written` event. Everytime your entity is written, you then have to execute the `update` method of the `Shopware\Core\Content\Seo\SeoUrlUpdater` class.

Once again, let's have a look at an example subscriber here:

As already said, we're using the `written` event of our custom entity by providing the entities' technical name with the `.written` suffix. Everytime it is executed, we're just using the said `update` method of the `SeoUrlUpdater`. Here you'll have to provide the technical route name and the IDs of the entities, that need to be updated. And that's it for the subscriber.

The `SeoUrlUpdater` will need one more thing in order to work properly: An entry in the table `seo_url_template`, which is done in the next step.

**Example SeoUrlTemplate migration**

Now we need to add an entry to the `seo_url_template` table for our new dynamic SEO URL template. This is done by adding a [database migration](./../../plugin-fundamentals/database-migrations.html) to our plugin.

The most important values you'll have to set in the migration are:

* `route_name`: We've defined this multiple times already. Use the constant from your `ExamplePageSeoUrlRoute` class
* `entity_name`: The technical name of your custom entity. In this guide it's `swag_example`
* `template`: Once again use the constant `DEFAULT_TEMPLATE` from your `ExamplePageSeoUrlRoute` class

Now here is the said example migration:

php

```shiki
// <plugin root>/src/Migration/Migration1619514731AddExampleSeoUrlTemplate.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;
use Swag\BasicExample\Storefront\Framework\Seo\SeoUrlRoute\ExamplePageSeoUrlRoute;

class Migration1619514731AddExampleSeoUrlTemplate extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1619514731;
    }

    public function update(Connection $connection): void
    {
        $connection->insert('seo_url_template', [
            'id' => Uuid::randomBytes(),
            'sales_channel_id' => null,
            'route_name' => ExamplePageSeoUrlRoute::ROUTE_NAME,
            'entity_name' => 'swag_example',
            'template' => ExamplePageSeoUrlRoute::DEFAULT_TEMPLATE,
            'created_at' => (new \DateTimeImmutable())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ]);
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

And that's it! Every time your entity is written now, you'll automatically generate a SEO URL for it.

INFO

This guide will not cover creating an actual controller with the used example route. Learn how that is done in our guide about [creating a storefront controller](./../../storefront/add-custom-controller.html).

**Reacting to entity deletion**

If your entity is deleted, you want the SEO URL to be updated as well. In detail, the column `is_deleted` of the respective entry in the `seo_url` table has to be set to `1`.

This can be achieved by using the DAL event `.deleted` and then executing the `update` method again.

php

```shiki
// <plugin root>/src/Service/DynamicSeoUrlPageSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Seo\SeoUrlUpdater;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityDeletedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent;
use Swag\BasicExample\Storefront\Framework\Seo\SeoUrlRoute\ExamplePageSeoUrlRoute;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class DynamicSeoUrlPageSubscriber implements EventSubscriberInterface
{
    // ...

    public static function getSubscribedEvents(): array
    {
        return [
            'swag_example.written' => 'onEntityWritten',
            'swag_example.deleted' => 'onEntityDeleted'
        ];
    }

    // ...

    public function onEntityDeleted(EntityDeletedEvent $event): void
    {
        $this->seoUrlUpdater->update(ExamplePageSeoUrlRoute::ROUTE_NAME, $event->getIds());
    }
}
```

#### Dynamic SEO URLs for custom content [​](#dynamic-seo-urls-for-custom-content)

This section is specifically about dynamic content other than custom entities. This could be e.g. data from an external resource, maybe external APIs.

You'll need some kind of event or some other way to execute code once your dynamic content changes, like once a new instance of that content is created or once it is updated.

In this example, we'll assume you've got a class called `DynamicSeoUrlsService` with a method `writeSeoEntries`. This method will get an array of entries to be written, including their respective payload, such as a name for the SEO URL. It also needs the current context.

Calling this method is up to you, depending on your set up and the type of "dynamic content" you're having.

This method will then use the `SeoUrlPersister` and its method `updateSeoUrls` in order to write entries to the `seo_url` table.

Here's an example of such a class:

php

```shiki
// <plugin root>/src/Service/DynamicSeoUrlsService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Cocur\Slugify\SlugifyInterface;
use Shopware\Core\Content\Seo\SeoUrlPersister;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter;

class DynamicSeoUrlsService
{
    public const ROUTE_NAME = 'example.route.name';

    private SeoUrlPersister $seoUrlPersister;

    private EntityRepository $salesChannelRepository;

    private SlugifyInterface $slugify;

    public function __construct(
        SeoUrlPersister $seoUrlPersister,
        EntityRepository $salesChannelRepository,
        SlugifyInterface $slugify
    ) {
        $this->seoUrlPersister = $seoUrlPersister;
        $this->salesChannelRepository = $salesChannelRepository;
        $this->slugify = $slugify;
    }

    public function writeSeoEntries(array $entries, Context $context): void
    {
        $urls = [];

        $salesChannelId = $this->getStorefrontSalesChannelId($context);
        if (!$salesChannelId) {
            // Might want to throw an error here
            return;
        }

        foreach ($entries as $entry) {
            $urls[] = [
                'salesChannelId' => $salesChannelId,
                'foreignKey' => $entry->getId(),
                // The name of the route in the respective controller
                'routeName' => self::ROUTE_NAME,
                // The technical path of your custom route, using a given parameter
                'pathInfo' => '/example-path/' . $entry->getId(),
                'isCanonical' => true,
                // The SEO URL that you want to use here, in this case just the name
                'seoPathInfo' => '/' . $this->slugify->slugify($entry->getName()),
            ];
        }

        // You might have to create a new context using another specific language ID
        $this->seoUrlPersister->updateSeoUrls($context, self::ROUTE_NAME, array_column($urls, 'foreignKey') , $urls);
    }

    private function getStorefrontSalesChannelId(Context $context): ?string
    {
        $criteria = new Criteria();
        $criteria->addFilter(new EqualsFilter('typeId', Defaults::SALES_CHANNEL_TYPE_STOREFRONT));

        return $this->salesChannelRepository->searchIds($criteria, $context)->firstId();
    }
}
```

The method `writeSeoEntries` will look for a Storefront sales channel and return its ID. It's then iterating over each provided entry, which in this example will need a method called `getId` and method called `getName`. Using this data, an array of URLs to be written is created. Make sure to change the values of the following keys:

* `routeName`: The technical name of your route, configured in your controller
* `pathInfo`: The technical, non-SEO, path of your route, also configured in your controller
* `seoPathInfo`: The actual SEO path you want to use - in this case the name of the said content

INFO

This guide will not cover creating an actual controller with the used example route. Learn how that is done in our guide about [creating a storefront controller](./../../storefront/add-custom-controller.html).

It will then use the built array and all of the other information like the context, the route name and an array of foreign keys for the method `updateSeoUrls` of the `SeoUrlPersister`. And that's it for your dynamic content.

#### Reacting to deletion of the content [​](#reacting-to-deletion-of-the-content)

If your custom dynamic content is deleted, you have to set the column `is_deleted` to `1` of the respective `seo_url` entry. This can be achieved with a new method, in this example we'll call it `deleteSeoEntries`. It will receive an array of IDs to be deleted. Those IDs have to match the value of the column `foreign_key` in the `seo_url` table. Also it needs the current context. It will take care of setting the generated SEO URLs to `deleted`. It will **not** delete an entry from the table `seo_url`.

php

```shiki
public function deleteSeoEntries(array $ids, Context $context): void
{
    $this->seoUrlPersister->updateSeoUrls($context, self::ROUTE_NAME, $ids, []);
}
```

This way the respective SEO URLs will be marked as `is_deleted` for the system. However, this SEO route will remain accessible, so make sure to implement a check whether or not the content still exists in your controller.

#### Writing SEO URLs for another language [​](#writing-seo-urls-for-another-language)

In the example mentioned above, we're just using a `Context` instance, for whichever language that is. You can be more specific here though, in order to properly define the language ID yourself here and therefore ensuring it is written for the right language.

php

```shiki
$context = new Context(
    $event->getContext()->getSource(),
    $event->getContext()->getRuleIds(),
    $event->getContext()->getCurrencyId(),
    [$languageId]
);
```

You can then pass this context to the `updateSeoUrls` method.

---

## Extend robots.txt configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/seo/extend-robots-txt.html

# Extend robots.txt configuration [​](#extend-robots-txt-configuration)

## Overview [​](#overview)

Since Shopware 6.7.1, the platform provides full `robots.txt` support with all standard directives and user-agent blocks. This feature was developed as an open-source contribution during Hacktober 2024 ([learn more](https://www.shopware.com/en/news/hacktoberfest-2024-outcome-a-robots-txt-for-shopware/)). For general configuration, refer to the [user documentation](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/creation-of-robots-txt).

INFO

The events and features described in this guide are available since Shopware 6.7.5.

You can extend the `robots.txt` functionality through events to:

* Add custom validation rules during parsing
* Modify or generate directives dynamically
* Support custom or vendor-specific directives
* Prevent warnings for known non-standard directives

## Prerequisites [​](#prerequisites)

This guide requires you to have a basic plugin running. If you don't know how to create a plugin, head over to the plugin base guide:

[Plugin Base Guide](../../plugin-base-guide)

You should also be familiar with [Event listeners](./../../plugin-fundamentals/listening-to-events.html).

INFO

This guide uses EventListeners since each example listens to a single event. If you need to subscribe to multiple events in the same class, consider using an [EventSubscriber](./../../plugin-fundamentals/listening-to-events.html#listening-to-events-via-subscriber) instead.

## Modifying parsed directives [​](#modifying-parsed-directives)

The `RobotsDirectiveParsingEvent` is dispatched after `robots.txt` content is parsed. You can modify the parsed result, add validation, or inject dynamic directives.

This example shows how to dynamically add restrictions for AI crawlers:

## Handling custom directives [​](#handling-custom-directives)

The `RobotsUnknownDirectiveEvent` is dispatched when an unknown directive is encountered. Use this to support vendor-specific directives or prevent warnings for known non-standard directives:

## Validation and parse issues [​](#validation-and-parse-issues)

You can add validation warnings or errors during parsing using the `ParseIssue` class. This example shows common validation scenarios:

Issues are automatically logged when the `robots.txt` configuration is saved in the Administration. Use `WARNING` for recommendations and `ERROR` for critical problems that prevent proper generation.

---

## Sitemap

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/sitemap/

# Sitemap [​](#sitemap)

Shopware Sitemap offers the ability to add sitemaps and modify sitemap entries within the e-commerce platform.

With the Sitemap plugin, you can create custom sitemaps to provide search engines with a structured overview of the website's content. These sitemaps can be tailored to specific requirements, allowing businesses to include relevant pages, categories, products, or other content sections based on their needs.

Additionally, the plugin enables users to modify sitemap entries. This means they can customize the information included in the sitemap, such as URLs change or overriding SEO URLs.

With this flexibility, businesses can ensure their website's content is efficiently crawled and indexed by search engines. Custom sitemaps and modified sitemap entries help improve the visibility and discoverability of the website, leading to better search engine rankings and increased traffic.

---

## Add custom sitemap entries

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/sitemap/add-custom-sitemap-entries.html

# Add Custom Sitemap Entries [​](#add-custom-sitemap-entries)

## Overview [​](#overview)

Shopware includes built-in sitemap generation for products, categories, and other core URLs. This guide explains how to extend it by adding your own custom URLs to the sitemap.

## Ways to add custom URLs to the sitemap [​](#ways-to-add-custom-urls-to-the-sitemap)

There are two approaches to adding custom URLs to the sitemap, depending on your use case. For static URLs that rarely change, use the configuration method. For dynamic URLs based on custom entities or database content, implement a custom URL provider.

### By using the configuration [​](#by-using-the-configuration)

To add a custom URL to the sitemap, use the configuration setting `shopware.sitemap.custom_urls`

yaml

```shiki
shopware:
    sitemap:
        custom_urls:
            -   url: 'custom-url'
                salesChannelId: '98432def39fc4624b33213a56b8c944d'
                changeFreq: 'weekly'
                priority: 0.5
                lastMod: '2024-09-19 12:19:00'
            -   url: 'custom-url-2'
                salesChannelId: '98432def39fc4624b33213a56b8c944d'
                changeFreq: 'weekly'
                priority: 0.5
                lastMod: '2024-09-18 12:18:00'
```

The `salesChannelId` is the ID of the sales channel you want to add the URL to.

### By adding a URL provider [​](#by-adding-a-url-provider)

This part of the guide is mainly built upon the guide about [Adding a custom SEO URL](./../seo/add-custom-seo-url.html#dynamic-seo-urls-for-entities), so you might want to have a look at that. The said guide comes with a custom entity, a controller with a technical route to display each entity, and a custom SEO URL. All of this will be needed for this guide, as we're going to add the custom entity SEO URLs to the sitemap here.

So let's get started. Adding custom URLs to the sitemap is done by adding a so-called "URL provider" to the system.

This is done by adding a new class, which is extending from `Shopware\Core\Content\Sitemap\Provider\AbstractUrlProvider`. It then has to be registered to the [service container](./../../plugin-fundamentals/dependency-injection.html) using the tag `shopware.sitemap_url_provider`.

It has to provide three methods:

* `getDecorated`: Just throw an exception of type `DecorationPatternException` here. This is done for the sake of extending a class via decoration. Learn more about this [here](./../../plugin-fundamentals/adjusting-service.html).
* `getName`: A technical name for your custom URLs
* `getUrls`: The main method to take care of. It has to return an instance of `Shopware\Core\Content\Sitemap\Struct\UrlResult`, containing an array of all URLs to be added.

Let's have a look at the example class:

Let's go through this step by step. Start by creating a new class `CustomUrlProvider`, which is extending from the `AbstractUrlProvider`. Following are the constants `CHANGE_FREQ` and `priority` - you don't have to add those values as constants of course. They're going to be used later in the generation of the sitemap URLs.

Passed into the constructor are the repository for our [custom entity](./../../framework/data-handling/add-custom-complex-data.html), the DBAL connection used for actually fetching SEO URLs from the database, and the Symfony router to generate SEO URLs that have not yet been written to the database.

Now let's get to the main method `getUrls`. We start off by fetching all custom entities, using the provided `$limit` and `$offset` values. Make sure to always use those values, as the sitemap supports "paging" and therefore you do not want to simply fetch all of your entities. If there aren't any entities to be fetched, there is nothing more to be done here.

Afterward we fetch all already existing SEO URLs for our custom entities. Once again, have a look at our guide about [adding a custom SEO URL](./../seo/add-custom-seo-url.html#dynamic-seo-urls-for-entities) if you don't know how to add custom SEO URLs in the first place.

We're then iterating over all of our fetched entities, and we create an instance of `Shopware\Core\Content\Sitemap\Struct\Url` for each iteration. This struct requests each of the typical sitemap information:

* `lastMod`: The last time this entry was modified. Use the `updatedAt` value here, if available
* `changeFreq`: How often will the entry most likely change? Possible values are `always`, `hourly`, `daily`, `weekly`, `monthly`, `yearly` and `never`
* `priority`: Has to have a value between 0 and 1. URLs with higher priority are considered to be "more important" by common search engines.
* `resource`: Just a name for your entry, in this example we're just using the entity class name
* `identifier`: The ID of the entry, if available

The most important entry is set afterward, which is the `location`: The actual SEO URL to be indexed. We're setting this value by checking if the SEO URL for the given entity was already generated, and if not, we're generating it on the fly.

All of those instances are then stored in an array, which in return is passed to the `UrlResult`. This completes the implementation. Your custom URLs will now be included in the generated sitemap.

---

## Modifying sitemap entries

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/sitemap/modify-sitemap-entries.html

# Modify Sitemap Entries [​](#modify-sitemap-entries)

## Overview [​](#overview)

You might have had a look at our guide about [adding custom sitemap entries](./add-custom-sitemap-entries.html), e.g. for a custom entity. However, you might not want to add new URLs, but rather modify already existing ones. This guide will cover modifying e.g. the product URLs for the sitemap.

## Prerequisites [​](#prerequisites)

This guide is built upon the [Plugin base guide](./../../plugin-base-guide.html), like most guides.

Modifying the sitemap entries is done via decoration, so should know how that's done as well. Also, knowing how the URL providers work, like it's explained in our guide about [adding custom sitemap entries](./add-custom-sitemap-entries.html), will come in handy.

## Modifying the sitemap [​](#modifying-the-sitemap)

There's two ways of actually modifying the sitemap entries, but both ways are done by decorating the respective `UrlProvider`, e.g. the `Shopware\Core\Content\Sitemap\Provider\ProductUrlProvider` for products.

Hence, let's start with creating the basic decorated class for the `ProductUrlProvider`. We'll call this class `DecoratedProductUrlProvider`:

Now let's get on to the two possible ways and its benefits.

### Adjusting the getUrls method [​](#adjusting-the-geturls-method)

By adjusting the `getUrls` method, you can execute the parent's `getUrls` method and modify its return value, which is an instance of the `UrlResult`. On this instance, you can use the method `getUrls` to actually get the `Url` instances and make adjustments to them - or even remove them.

php

```shiki
// <plugin root>/src/Core/Content/Sitemap/Provider/DecoratedProductUrlProvider.php
public function getUrls(SalesChannelContext $context, int $limit, ?int $offset = null): UrlResult
{
    $urlResult = $this->getDecorated()->getUrls($context, $limit, $offset);
    $urls = $urlResult->getUrls();

    /* Change $urls, e.g. removing entries or updating them by iterating over them. */

    return new UrlResult($urls, $urlResult->getNextOffset());
}
```

You could iterate over the `$urls` array and modify each entry - or even create a new array with less entries, if you want to fully remove some.

There is one main downside to this way: You don't have access to a lot of information about the entity itself, that was used for this `Url` instance. E.g. if you'd like to filter all products with a given name, you can't do that here, since the name itself isn't available. The only reliable information you have here, is the ID of the entity by using the method `getIdentifier` on the `Url` instance.

Also, it's not the best way in terms of performance to read all SEO URLs from the database, only to filter them afterwards.

### Overriding the getSeoUrls method [​](#overriding-the-getseourls-method)

The available SEO URLs are read in the protected method `getSeoUrls` of the `AbstractUrlProvider`. Since it's a protected method, you can override it and create a custom SQL in order to only read the data you really want.

For this you'll most likely want to copy the original method's code and paste it into your overridden method. You can then add new lines to the SQL statement in order to do the necessary filtering or customising.

php

```shiki
// <plugin root>/src/Core/Content/Sitemap/Provider/DecoratedProductUrlProvider.php
protected function getSeoUrls(array $ids, string $routeName, SalesChannelContext $context, Connection $connection): array
{
    /* Make adjustments to this SQL */
    $sql = 'SELECT LOWER(HEX(foreign_key)) as foreign_key, seo_path_info
                FROM seo_url WHERE foreign_key IN (:ids)
                 AND `seo_url`.`route_name` =:routeName
                 AND `seo_url`.`is_canonical` = 1
                 AND `seo_url`.`is_deleted` = 0
                 AND `seo_url`.`language_id` =:languageId
                 AND (`seo_url`.`sales_channel_id` =:salesChannelId OR seo_url.sales_channel_id IS NULL)';

    return $connection->fetchAll(
        $sql,
        [
            'routeName' => $routeName,
            'languageId' => Uuid::fromHexToBytes($context->getSalesChannel()->getLanguageId()),
            'salesChannelId' => Uuid::fromHexToBytes($context->getSalesChannelId()),
            'ids' => Uuid::fromHexToBytesList(array_values($ids)),
        ],
        [
            'ids' => Connection::PARAM_STR_ARRAY,
        ]
    );
}
```

Now you could adjust the SQL statement to fit your needs, e.g. by adding a `JOIN` to the respective entities' table.

However, there is a downside here as well: Overriding the method like this is not really update-compatible. If the original method is changed in a future update, those changes will not apply for your modification, hence you might not receive a performance update or a bugfix for those few lines of code.

---

## Remove sitemap entries

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/sitemap/remove-sitemap-entries.html

# Remove Sitemap Entries [​](#remove-sitemap-entries)

## Overview [​](#overview)

This guide covers how to remove URLs from the sitemap.

## By using the configuration [​](#by-using-the-configuration)

To remove a URL from the sitemap, use the configuration setting `shopware.sitemap.excluded_urls`

yaml

```shiki
shopware:
    sitemap:
        excluded_urls:
            -   salesChannelId: '98432def39fc4624b33213a56b8c944d'
                resource: 'Shopware\Core\Content\Product\ProductEntity'
                identifier: 'd20e4d60e35e4afdb795c767eee08fec'
```

The `salesChannelId` is the ID of the sales channel from which you want to exclude the URL. The `resource` is the full class name of the entity from which you want to exclude the URL, for example, `Shopware\Core\Content\Product\ProductEntity`. The `identifier` is the entity's ID for which you want to exclude the URL.

---

## Stock

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/stock/

# Stock [​](#stock)

INFO

The stock management system is available from Shopware 6.5.5.0. It is only enabled if the shop owner has enabled the `\STOCK_HANDLING\` feature flag.

The stock management system allows the allocation of stocks to products. Stock is incremented and decremented as orders are placed, modified, canceled, and refunded.

In order to accommodate for the various use cases, the stock management system has been kept as simple as possible. The shop owner can deactivate it entirely if not required.

To enable or disable this feature, refer to [stock configuration](./../../../../../guides/hosting/configurations/shopware/stock.html) section.

---

## Implementing your own stock storage

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/stock/implementing-your-own-stock-storage.html

# Implementing your own stock storage [​](#implementing-your-own-stock-storage)

## Overview [​](#overview)

Shopware stores stock as simple integer values in the `product` table. If you need a more advanced stock management system or would like to write the stock alterations to a different system, you can implement your own stock storage.

## Prerequisites [​](#prerequisites)

Here you will be decorating a service; therefore, it will be helpful to familiarize yourself with the [Adjusting a Service](./../../../../../guides/plugins/plugins/plugin-fundamentals/adjusting-service.html) guide.

## Add a decorator to load the stock [​](#add-a-decorator-to-load-the-stock)

First, to communicate stock alterations to a third-party service, you will have to decorate `\Shopware\Core\Content\Product\Stock\AbstractStockStorage` and implement the `alter` method. This method is triggered with an array of `StockAlteration`'s, which contains:

* the Product and Line Item IDs,
* the old quantity and
* the new quantity.

The alter method will be called when the stock of a product should be updated. The `$changes` array contains a list of `StockAlteration` instances. These objects contain the following properties/methods:

| Property/Method | Type | Description |
| --- | --- | --- |
| lineItemId | string | The ID of the line item that triggered the stock update |
| productId | string | The ID of the product that should be updated |
| quantityBefore | int | The old product stock level |
| newQuantity | int | The new product stock level |
| quantityDelta() | int | The difference between the old and new stock level |

## Stock changing scenarios [​](#stock-changing-scenarios)

The following list contains all the scenarios that trigger stock alterations. All implementations of `AbstractStockStorage` should be able to handle these scenarios.

* Order placed
* Order canceled
* Order deleted
* Cancelled order, reopened
* Line item added to the order
* Line item removed from an order
* Line item updated (Product qty increased)
* Line item updated (Product qty decreased)
* Line item updated (Product sku changed)

All of these scenarios are handled by the event subscriber `Shopware\Core\Content\Product\Stock\OrderStockSubscriber`.

## Further extension points for advanced customization [​](#further-extension-points-for-advanced-customization)

1. If you need to listen to more events to trigger stock alterations, you can create an event subscriber for the required events and call the `\Shopware\Core\Content\Product\Stock\AbstractStockStorage::alter` method with a `StockAlteration` instance representative of the alteration.
2. If you don't want to use Shopware's default events and stock storage, you can implement your own system and recommend that the project owner disables the Shopware stock management system. Refer them to [Configuration guide](./../../../../../guides/hosting/configurations/shopware/stock.html).

---

## Loading Stock Information from a different Source

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/stock/loading-stock-information-from-different-source.html

# Loading Stock Information from a Different Source [​](#loading-stock-information-from-a-different-source)

## Overview [​](#overview)

If Shopware is not the source of truth for your stock data, you can customize the stock loading process and provide your data from a third-party source.

## Prerequisites [​](#prerequisites)

Here again, you will be decorating a service; therefore, it will be helpful to familiarize yourself with the [Adjusting a Service](./../../../../../guides/plugins/plugins/plugin-fundamentals/adjusting-service.html) guide.

## Add a decorator to load the stock [​](#add-a-decorator-to-load-the-stock)

For example, to load stock from a third-party API, you need to decorate `\Shopware\Core\Content\Product\Stock\AbstractStockStorage` and implement the `load` method. When products are loaded in Shopware the `load` method will be invoked with the loaded product IDs.

In your `load` method, you can access the product IDs from the `StockLoadRequest` instance and perform a request to your system to retrieve the data.

You then construct and return a `StockDataCollection` full of `StockData` instances. Each `StockData` instance represents a product.

You can use the static method `Shopware\Core\Content\Product\Stock::fromArray()` to construct an instance, passing in an array of the stock attributes.

There are several required values and some optional values.

| Attribute | Type | Description | Optional/Required |
| --- | --- | --- | --- |
| productId | string | The product ID | Required |
| stock | int | The stock amount | Required |
| available | boolean | Whether the product is considered available | Required |
| minPurchase | int | The minimum purchase value for this product | Optional |
| maxPurchase | int | The maximum purchase value for this product | Optional |
| isCloseout | boolean | Whether the product can be ordered if there is not enough stock | Optional |

For example:

php

```shiki
$stockData = \Shopware\Core\Content\Product\Stock\StockData::fromArray([
    'productId' => 'product-1',
    'stock' => 5,
    'available' => true,
    'minPurchase' => 1,
    'maxPurchase' => 10,
    'isCloseout' => false,
]);
```

It is also possible to provide arbitrary data via extensions:

php

```shiki
$stockData = \Shopware\Core\Content\Product\Stock\StockData::fromArray([
    'productId' => 'product-1',
    'stock' => 5,
    'available' => true,
]);

$stockData->addArrayExtension('extraData', ['foo' => 'bar']);
```

The values in the `StockData` instance will be used to update the loaded product instance. Furthermore, fetching the `StockData` instance from the product via the `stock_data` extension is possible. For example:

php

```shiki
$stockData = $product->getExtension('stock_data');
```

---

## Reading and Writing Stock

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/content/stock/reading-writing-stock.html

# Reading and Writing Stock [​](#reading-and-writing-stock)

## Overview [​](#overview)

Shopware stores the current stock level alongside the product, this guide will help you when you want to read and write that value.

## Reading Stock [​](#reading-stock)

The `product.stock` field should be used to read the current stock level. When building extensions that need to query a product's stock, use this field. It is always a real-time calculated value of the available product stock.

php

```shiki
// <plugin root>/src/Swag/Example/ServiceReadingData.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class ReadingStock
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }
    
    public function read(Context $context): void
    {
        $product = $this->productRepository
            ->search(new Criteria([$productId]), $context)
            ->first();
            
        $stock = $product->getStock();
    }
}
```

## Writing Stock [​](#writing-stock)

The `product.stock` field should be used to write the current stock level.

php

```shiki
// <plugin root>/src/Swag/Example/ServiceReadingData.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class WritingStock
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }
    
    public function write(string $productId, int $stock, Context $context): void
    {
        $this->productRepository->update(
            [
                [
                    'id' => $productId,
                    'stock' => $stock
                ]
            ],
            $context
        );
    }
}
```

---

