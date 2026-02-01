# Guides Plugins Apps Administration

*Scraped from Shopware Developer Documentation*

---

## Administration

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/

# Administration [​](#administration)

You can't extend the Shopware Administration by means of freely overriding and extending Administration components, all js files you provide in the `Resources/administration` namespace will be ignored. Instead, you have more defined extension points and can extend the Administration by other means: You are able to [add your own modules](./add-custom-modules.html), [custom fields](./../custom-data/custom-fields.html) or [action buttons](./add-custom-action-button.html) via manifest file.

Starting with version 6.4.2.0 you can also extend Shopware's CMS module by [adding custom CMS blocks](./../content/cms/add-custom-cms-blocks.html).

---

## Meteor Admin SDK

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/meteor-admin-sdk.html

# Meteor Admin SDK [​](#meteor-admin-sdk)

The [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk) is an NPM library for Shopware 6 apps and plugins that need an easy way to extend or customize the administration.

To write advanced apps, its recommended that you use the [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk). It contains helper functions to communicate with the Administration, execute actions, subscribe to data or extend the user interface. It has many more features and is more flexible.

* 🏗 **Works with Shopware 6 Apps and Plugins:** You can use the SDK for your plugins or apps. API usage is identical.
* 🎢 **Shallow learning curve:** You don't need to have extensive knowledge about the internals of the Shopware 6 Administration. Our SDK hides the complicated stuff behind a beautiful API.
* 🧰 **Many extension capabilities:** Includes throwing notifications, accessing context information, extending the current UI and more. The feature set of the SDK will gradually be extended, providing more possibilities and flexibility for your ideas and solutions.
* 🪨 **A stable API with great backwards compatibility:** Don't fear Shopware updates anymore. Breaking changes in this SDK are an exception. If you use the SDK, your apps and plugins will stay stable for a longer time, without any need for code maintenance.
* 🧭 **Type safety:** The whole SDK is written in TypeScript which provides great autocompletion support and more safety for your apps and plugins.
* 💙 **Developer experience:** Have a great development experience right from the start. And it will become better and better in the future.
* 🪶 **Lightweight:** The whole library is completely tree-shakable and dependency-free. Every functionality can be imported granularly to keep your bundle as small and fast as possible.

Go to [Installation](/resources/admin-extension-sdk/getting-started/installation.html) to get started. Or check out the [quick start guide](/resources/admin-extension-sdk/#quick-start).

---

## Add custom action button

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/add-custom-action-button.html

# Add custom action button [​](#add-custom-action-button)

INFO

This guide will show you how to add custom action buttons to the Shopware Administration using your manifest file. This works for simple applications; however, if you want to write more advanced applications, the [Meteor Admin SDK](/resources/admin-extension-sdk/) is recommended. It has many more features and is more flexible.

For further details and guidance on custom action buttons, refer to the documentation provided on the Meteor Admin SDK's [action button](/resources/admin-extension-sdk/api-reference/ui/actionButton.html) section.

One extension possibility in the Administration is the ability to add custom action buttons to the smartbar. For now, you can add them in the smartbar of detail and list views:

![Custom action buttons in the Administration](/assets/custom-buttons.0mhLEmNs.png)

To get those buttons, you start in the `admin` section of your manifest file. There you can define `<action-button>` elements in order to add your button, as seen as below:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
        <action-button action="setPromotion" entity="promotion" view="detail" url="https://example.com/promotion/set-promotion">
            <label>set Promotion</label>
        </action-button>
        <action-button action="deletePromotion" entity="promotion" view="detail" url="https://example.com/promotion/delete-promotion">
            <label>delete Promotion</label>
        </action-button>
        <action-button action="restockProduct" entity="product" view="list" url="https://example.com/restock">
            <label>restock</label>
        </action-button>
    </admin>
</manifest>
```

For a complete reference of the structure of the manifest file take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

An action button must have the following attributes:

* `action`: Unique identifier for the action, can be set freely.
* `entity`: Here you define which entity you're working on.
* `view`: `detail`or `list`; to set the view the button should be added to. Currently, you can choose between detail and listing view.

When the user clicks on the action button your app receives a request similar to the one generated by a [webhook](./../app-base-guide.html#webhooks). The main difference is that it contains the name of the entity and an array of ids that the user selected (or an array containing only a single id if the action button was executed on a detail page).

A sample payload may look like the following:

INFO

Starting from Shopware version 6.4.1.0, the current shopware version will be sent as a `sw-version` header.

Again you can verify the authenticity of the incoming request, like with [webhooks](./../app-base-guide.html#webhooks), by checking the `shopware-shop-signature` it too contains the SHA256 HMAC of the request body, that is signed with the secret your app assigned the shop during the [registration](./../app-base-guide.html#setup).

## Providing feedback in the Administration [​](#providing-feedback-in-the-administration)

INFO

This feature was added in Shopware 6.4.3.0, previous versions will ignore the response content.

INFO

Starting from Shopware version 6.4.8.0, the requests of the [tab](#opening-a-new-tab-for-the-user) and [custom modal](#open-a-custom-modal) have the following additional query parameters:

* `shop-id`
* `shop-url`
* `timestamp`
* `sw-context-language`
* `sw-user-language`
* `shopware-shop-signature`

You **must** make sure to verify the authenticity of the incoming request by checking the `shopware-shop-signature`, which is a hash of the request's query part, signed with the shop's secret key.

If you want to trigger an action inside the Administration upon completing the action, the app should return a response with a valid body and the header `shopware-app-signature` containing the SHA256 HMAC of the whole response body signed with the app secret. If you do not need to trigger any actions, a response with an empty body is also always valid.

### Opening a new tab for the user [​](#opening-a-new-tab-for-the-user)

Examples response body: To open a new tab in the user browser you can use the `openNewTab` action type. You need to pass the url that should be opened as the `redirectUrl` property inside the payload.

### Show a notification to the user [​](#show-a-notification-to-the-user)

To send a notification, you can use the `notification` action type. You need to pass the `status` property and the content of the notification as `message` property inside the payload.

### Reload the current page [​](#reload-the-current-page)

To reload the data in the user's current page you can use the `reload` action type with an empty payload.

### Open a custom modal [​](#open-a-custom-modal)

To open a modal with the embedded link in the iframe, you can use the `openModal` action type. You need to pass the url that should be opened as the `iframeUrl` property and the `size` property inside the payload.

### General structure [​](#general-structure)

* `actionType`: The type of action the app want to be triggered, including `notification`, `reload`, `openNewTab`, `openModal`
* `payload`: The needed data to perform the action.
  + `redirectUrl`: The url to open new tab
  + `iframeUrl`: The embedded link in modal iframe
  + `status`: Notification status, including `success`, `error`, `info`, `warning`
  + `message`: The content of the notification
  + `size`: The size of the modal in `openModal` type, including `small`, `medium`, `large`, `fullscreen`, default `medium`
  + `expand`: The expansion of the modal in `openModal` type, including `true`, `false`, default `false`

## Using Custom Endpoints as target [​](#using-custom-endpoints-as-target)

It is also possible to use [custom endpoints](./../app-scripts/custom-endpoints.html) as target for action buttons.

INFO

This feature was added in Shopware 6.4.10.0, previous versions don't support relative target urls for action buttons.

To use custom endpoints as the target url for action buttons you can define the target url as a relative url in your apps manifest.xml:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
      <action-button action="test-button" entity="product" view="list" url="/api/script/action-button">
        <label>test-api-endpoint</label>
      </action-button>
    </admin>
</manifest>
```

And then add the corresponding app script that should be executed when the user clicks the action button.

twig

```shiki
// Resources/scripts/api-action-button/action-button-script.twig
{% set ids = hook.request.ids %}

{% set response = services.response.json({
    "actionType": "notification",
    "payload": {
        "status": "success",
        "message": "You selected " ~ ids|length ~ " products."
    }
}) %}

{% do hook.setResponse(response) %}
```

As you can see it is possible to provide a [`JsonResponse`](./../../../../resources/references/app-reference/script-reference/custom-endpoint-script-services-reference.html#json) to give [feedback to the user in the administration](#providing-feedback-in-the-administration).

---

## Add custom module

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/add-custom-modules.html

# Add custom module [​](#add-custom-module)

INFO

This guide will show you how to add custom modules to the Shopware Administration using your manifest file. This works for simple applications; however, if you want to write more advanced applications, the [Meteor Admin SDK](/resources/admin-extension-sdk/) is recommended. It has many more features and is more flexible.

For further details and guidance on custom modules, refer to the documentation provided on the Meteor Admin SDK's [custom modules](/resources/admin-extension-sdk/api-reference/ui/mainModule.html) section.

## Prerequisites [​](#prerequisites)

You should be familiar with the concept of Apps, especially their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server, as that is required to authenticate the requests coming from the shops and showing the correct content in your modules.

[App Base Guide](../app-base-guide)

## Overview [​](#overview)

In your app, you are able to add your own modules to the Administration. Your custom modules are loaded as iframes which are embedded in the Shopware Administration and within this iframe, your website will be loaded and shown.

Creating custom modules takes place at the `<admin>` section of your `manifest.xml`. Take a look at the [Manifest Reference](./../../../../resources/references/app-reference/manifest-reference.html) You can add any amount of custom modules by adding new `<module>` elements to your manifest.

To configure your module, you can set it up with with some additional attributes.

* `name` (required): The technical name of the module. This is the name your module is referenced with.
* `parent` (required): The Administration navigation id of the menu item that serves as the parent menu item.
* `source` (optional): The URL to your app servers endpoint from which the module is served from. This can be omitted if you want to define a menu item that should serve as a parent menu item for other app modules.
* `parent` (optional): The Administration navigation id from the menu item that serves as the parent menu item. If omitted your module will be listed under the "My apps" menu entry. **This field will be required in future versions as we are going to remove the "My Apps" menu item**
* `position` (optional): A numeric index that sets the position of your menu entry regarding to it's siblings.

Additionally you can define `label` elements inside of your `module` element, to set up how your module will be displayed in the admin menu.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
        <module name="exampleModule"
                source="https://example.com/promotion/view/promotion-module"
                parent="sw-marketing"
                position="50"
        >
            <label>Example module</label>
            <label lang="de-DE">Beispiel Modul</label>
        </module>
    </admin>
</manifest>
```

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](./../../../../resources/references/app-reference/manifest-reference.html).

If the user opens the module in the Administration your app will receive a request to the URL defined in the `source` attribute of your `module` element. Your app can determine the shop that has opened the module through query parameters added to the url:

* `shop-id`: The unique identifier of the shop, where the app was installed
* `shop-url`: The URL of the shop, this can later be used to access the Shopware API
* `timestamp`: The Unix timestamp when the request was created
* `shopware-shop-signature`: SHA256 HMAC of the rest of the query string, signed with the `shop-secret`

## Leave loading state [​](#leave-loading-state)

Because your module is displayed as an iframe in the Administration, Shopware can not easily tell when your module has finished loading. Therefore, your new module will display a loading spinner to signalize your iframe is loading. To leave the loading state, your iframe needs to give a notification when the loading process is done.

javascript

```shiki
function sendReadyState() {
    window.parent.postMessage('sw-app-loaded', '*');
}
```

This has to be done as soon as everything is loaded so that the loading spinner disappears. If your view is not fully loaded after 5 seconds, it will be aborted.

## Structure your modules [​](#structure-your-modules)

With Shopware 6.4.0.0 we added a third level in the admin menu structure. This change was made to give you as a developer the opportunity to group your Administration modules if needed.

When you define a module, it gets automatically loaded by the Administration. Additionally the Administration creates a menu entry for your module. You can reference this menu entry and set it as the parent menu entry for your other modules.

The navigation id of your modules always uses the pattern `app-<appName>-<moduleName>`. So, within your manifest you can add a reference to modules that you just created:

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>myApp</app>
        ...
    </meta>
    <admin>
        <module name="myModules"
                source="https://example.com/promotion/view/promotion-module"
                parent="sw-catalogue"
                position="50"
        >
            <label>My apps modules</label>
            <label lang="de-DE">Module meiner app</label>
        </module>

        <module name="someModule"
                source="https://example.com/promotion/view/promotion-module"
                parent="app-myApp-myModules"
                position="1"
        >
            <label>Module underneath "My apps modules"</label>
            <label lang="de-DE">Modul unterhalb von "Module meiner app"</label>
        </module>
    </admin>
</manifest>
```

Modules that are used as a parent for other modules do not need the `source` attribute to be set, although they can.

## Add main module to your app [​](#add-main-module-to-your-app)

With Shopware 6.4.0.0 You can define a main module for your app. This "special" module will be opened from the list of your installed apps as well as from the app detail page if you bought it from the Shopware store.

Your main module can be defined by adding a `main-module` element within your `administration` section of your manifest file. It's only required attribute is the `source` attribute.

To avoid mixing other modules with your main module, we decided to separate the main module from modules with navigation entries. You can still use the same URL on both, a module that is available through the menu and your main module.

manifest.xml

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>myApp</app>
        ...
    </meta>
    <admin>
        <module name="normalModule"
                source="https://example.com/main"
                parent="sw-catalogue"
                position="50"
        >
            <label>Module in admin menu</label>
            <label lang="de-DE">Modul im Adminmenü</label>
        </module>

        <!-- You can use the same url to open your module from the app store -->
        <main-module source="https://example.com/main"/>
    </admin>
</manifest>
```

This feature is not compatible with themes as they will always open the theme config by default.

## Admin design compatibility [​](#admin-design-compatibility)

As your module page is integrated as an iframe you are not able to use the stylesheet and javascript out of the box. Having the stylesheets that are used in the Administration can be beneficial for the app module to seamlessly integrate into the Administration. You can use the shop version that is passed as `sw-version` within the request query to determine what stylesheets you want to load. The compiled Administration stylesheets for each version can be found within the tagged releases of the `shopware/administration` package within the `Resources/public/static` folder. Combining this information enables your app to look exactly like the Administration, although it is encapsulated within an iframe.

---

## Add CMS element

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/add-cms-element-via-admin-sdk.html

# Add CMS Element [​](#add-cms-element)

## Overview [​](#overview)

This guide explains how to create a new CMS element using the Meteor Admin SDK. The example plugin is named `SwagBasicAppCmsElementExample`, following the naming conventions used in other guides.

## Prerequisites [​](#prerequisites)

* Familiarity with creating [Plugins](./../../plugins/plugin-base-guide.html) or [Apps](./../app-base-guide.html)
* Familiarity with [creating custom admin components](./../../plugins/administration/module-component-management/add-custom-component.html#creating-a-custom-component)
* Understanding of the [Meteor Admin SDK](/resources/admin-extension-sdk/getting-started/installation.html)

INFO

This example uses TypeScript, which is recommended but not required to develop Shopware.

## Creating your custom element [​](#creating-your-custom-element)

Similar to [creating a new custom element via plugin](./../../plugins/content/cms/add-cms-element.html#creating-your-custom-element), this guide describes how to create a new custom element via an app. Creating a new element requires the Meteor Admin SDK.

In this example, you will build a scenario where a shop manager can configure a link to display a Dailymotion video.

### Target structure [​](#target-structure)

You can choose your preferred approach when creating apps, as everything is loaded via iFrame. However, Shopware recommends using a full Vue.js approach.

When the extension is complete, the file structure will look like this:

bash

```shiki
// <plugin root>/src/Resources/app/administration/src
├── base
│   └── mainCommands.ts
├── main.ts
├── viewRenderer.ts
└── views
    └── swag-dailymotion
        ├── swag-dailymotion-config.ts
        ├── swag-dailymotion-element.ts
        └── swag-dailymotion-preview.ts
```

## Initial loading of components [​](#initial-loading-of-components)

The entry point is the `main.ts` file:

javascript

```shiki
// Prior to 6.7
import 'regenerator-runtime/runtime';
import { location } from '@shopware-ag/meteor-admin-sdk';

// Only execute extensionSDK commands when
// it is inside an iFrame
if (location.isIframe()) {
    if (location.is(location.MAIN_HIDDEN)) {
        // Execute the base commands
        import('./base/mainCommands');
    } else {
        // Render different views
        import('./viewRenderer');
    }
}
```

javascript

```shiki
// 6.7 and above (inside meteor-app folder)
import 'regenerator-runtime/runtime';
import { location } from '@shopware-ag/meteor-admin-sdk';

if (location.is(location.MAIN_HIDDEN)) {
    // Execute the base commands
    import('./base/mainCommands');
} else {
    // Render different views
    import('./viewRenderer');
}
```

This is the main file, which is executed first and functions as the entry point.

Use `if(location.is(location.MAIN_HIDDEN))` to **load the main commands**, which are defined in the `mainCommands.ts` file. This will only be used to load logic, but not templates into the Administration.

Lastly, the `else` case will be responsible for specific loading of views via `viewRenderer.ts`. This is where the view templates will be loaded.

### Loading all required templates [​](#loading-all-required-templates)

Next, create the `viewRenderer.ts` file, which loads the three required files for a CMS element:

* `swag-dailymotion-config.ts`, which will handle the content of the CMS element configuration
* `swag-dailymotion-element.ts`, which represents the actual target element in the CMS
* `swag-dailymotion-preview.ts`, which is responsible for the preview, when selecting the CMS element in its selection screen

Observe that every file is named according to the component and prefixed with `swag-dailymotion`, (vendor prefix) to ensure no other developer accidentally chooses the same name.

The following example shows how component loading via `viewRenderer.ts` is implemented:

javascript

```shiki
import Vue from 'vue';
import { location } from '@shopware-ag/meteor-admin-sdk';

// watch for height changes
location.startAutoResizer();

// start app views
const app = new Vue({
    el: '#app',
    data() {
        return { location };
    },
    components: {
        'SwagDailymotionElement':
            () => import('./views/swag-dailymotion/swag-dailymotion-element'),
        'SwagDailymotionConfig':
            () => import('./views/swag-dailymotion/swag-dailymotion-config'),
        'SwagDailymotionPreview':
            () => import('./views/swag-dailymotion/swag-dailymotion-preview'),
    },
    template: `
        <SwagDailymotionElement
            v-if="location.is('swag-dailymotion-element')"
        ></SwagDailymotionElement>
        <SwagDailymotionConfig
            v-else-if="location.is('swag-dailymotion-config')"
        ></SwagDailymotionConfig>
        <SwagDailymotionPreview
            v-else-if="location.is('swag-dailymotion-preview')"
        ></SwagDailymotionPreview>
    `,
});
```

Really straightforward, isn't it? As you probably know from Vue.js's Options API, you just need to load, register and use the Vue.js component to make them work.

What's especially interesting here is the use of the `location` object. This is a main concept of the Meteor Admin SDK, where Shopware provides dedicated `locationIds` to offer you places to inject your templates into. For further information on that, it is recommended to take a look at the documentation of the [Meteor Admin SDK](/resources/admin-extension-sdk/concepts/locations.html) to learn more about its concepts.

In your case, we will get your own **auto-generated** `locationIds`, depending on the name of your CMS element and suffixes, such as `-element`, `-config`, and `-preview`.

Those will be available after **registering the component**, which we will do in the following chapter.

## Registering a new element [​](#registering-a-new-element)

For this step, go to `mainCommands.ts`, as registering CMS elements should be done in a global scope.

javascript

```shiki
import { cms } from '@shopware-ag/meteor-admin-sdk';

const CMS_ELEMENT_NAME = 'swag-dailymotion';
const CONSTANTS = {
    CMS_ELEMENT_NAME,
    PUBLISHING_KEY: `${CMS_ELEMENT_NAME}__config-element`,
};

void cms.registerCmsElement({
    name: CONSTANTS.CMS_ELEMENT_NAME,
    label: 'Dailymotion video',
    defaultConfig: {
        dailyUrl: {
            source: 'static',
            value: '',
        },
    },
});

export default CONSTANTS;
```

At first, you import the Meteor Admin SDK's CMS object used for `cms.registerCmsElement` to register a new element.

That is all about what is required to register your CMS element. As a best practice, it is recommended to create a **constant** for the CMS element name and the publishing key. This makes it easier to maintain and keep track of changes. The publishing key can be predefined since the name must be a combination of CMS element name and the `__config-element` suffix as shown above.

## Templates and communication with the Administration [​](#templates-and-communication-with-the-administration)

The remaining files are the components inside the `views` folder. As with typical CMS element loading, create a folder with the full component name containing three files as shown below:

bash

```shiki
// <plugin root>/src/Resources/app/administration/src
views
└── swag-dailymotion
    ├── swag-dailymotion-config.ts
    ├── swag-dailymotion-element.ts
    └── swag-dailymotion-preview.ts
```

You can vary the structure of `swag-dailymotion`'s contents and create folders for each of the three. However, for simplicity, use single file components.

### The config file [​](#the-config-file)

The following section describes each file, starting with `swag-dailymotion-config.ts`:

javascript

```shiki
import Vue from 'vue'
import { data } from "@shopware-ag/meteor-admin-sdk";
import CONSTANTS from "../../base/mainCommands";

export default Vue.extend({
    template: `
        <div>
          <h2>
            Config!
          </h2>
          Video-Code: <input v-model="dailyUrl" type="text"/><br/>
        </div>
    `,

    data(): Object {
        return {
            element: null
        }
    },

    computed: {
        dailyUrl: {
            get(): string {
                return this.element?.config?.dailyUrl?.value || '';
            },

            set(value: string): void {
                this.element.config.dailyUrl.value = value;

                data.update({
                    id: CONSTANTS.PUBLISHING_KEY,
                    data: this.element,
                });
            }
        }
    },

    created() {
        this.createdComponent();
    },

    methods: {
        async createdComponent() {
            this.element = await data.get({ id: CONSTANTS.PUBLISHING_KEY });
        }
    }
});
```

This file is the config component used to define every type of configuration for the CMS element. Most of the code will be common for experienced Shopware 6 developers, so here are some important highlights:

* Import `data` from the Meteor Admin SDK, which is required for data handling between this app and Shopware
* The `element` variable contains the typical CMS element object and is also used to manage the element configuration you want to edit
* The `publishingKey` is used to tell the Meteor Admin SDK in Shopware what piece of information you want to fetch. In this case, you need the `element` data

So, now you need a simple input field to get a `dailyUrl` for the Dailymotion video to be displayed. For that, first fetch the element via `data.get()` as seen in `createdComponent` and then link it to the computed property `dailyUrl` with getters and setters to mutate it. Using `data.update({ id, data })` you provide the publishing key `id` as a target and `data` for the data you want to save in Shopware.

With these small additions to typical CMS element behavior, you have already done with the config modal.

![Dailymotion config modal](/assets/add-cms-element-via-admin-sdk-config.B-M2NYyP.png)

### The element file [​](#the-element-file)

Now let's have a look at the result of `swag-dailymotion-element.ts`:

javascript

```shiki
import Vue from 'vue'
import { data } from "@shopware-ag/meteor-admin-sdk";
import CONSTANTS from "../../base/mainCommands";

export default Vue.extend({
    template: `
        <div>
            <h2>
              Element!
            </h2>
            <div class="sw-cms-el-dailymotion">
                <div class="sw-cms-el-dailymotion-iframe-wrapper">
                    <iframe
                        frameborder="0"
                        type="text/html"
                        width="100%"
                        height="100%"
                        :src="dailyUrl">
                    </iframe>
                </div>
            </div>
        </div>
    `,

    data(): { element: object|null } {
        return {
            element: null
        }
    },

    computed: {
        dailyUrl(): string {
            return `https://www.dailymotion.com/embed/video/${this.element?.config?.dailyUrl?.value || ''}`;
        }
    },

    created() {
        this.createdComponent();
    },

    methods: {
        async createdComponent() {
            this.element = await data.get({ id: CONSTANTS.PUBLISHING_KEY });
            data.subscribe(CONSTANTS.PUBLISHING_KEY, this.elementSubscriber);
        },

        elementSubscriber(response: { data: unknown, id: string }): void {
            this.element = response.data;
        }
    }
});
```

Here, you have the main rendering logic for the Administration's CMS element. This file shows what your element will look like when it's done. So besides a template and the computed `dailyUrl`, used to correctly load the Dailymotion video player, the only interesting part is the `createdComponent` method.

It initially fetches the `element` data, as you've already seen it in the config file. After that, using `data.subscribe(id, method)` it subscribes to the publishing key, which will update the element data automatically if something changes. It doesn't matter if the changes originate from our config modal outside Shopware or from somewhere else inside Shopware.

![Dailymotion CMS element](/assets/add-cms-element-via-admin-sdk-element.BT8-Wo6W.png)

### The preview file [​](#the-preview-file)

Lastly, have a look at `swag-dailymotion-preview.ts`. In most cases, this file contains minimal logic, as it is only used for the preview when selecting a CMS element for your block. It is common to show an example preview, a skeleton of the result, or just the Dailymotion logo. The following code is sufficient for this example:

javascript

```shiki
import Vue from 'vue'

export default Vue.extend({
    template: `
        <h2>
          Preview!
        </h2>
    `,
});
```

![Dailymotion element preview](/assets/add-cms-element-via-admin-sdk-preview.DSH0LCB7.png)

## Storefront implementation [​](#storefront-implementation)

After completing the admin implementation, you also need a storefront representation of your blocks. This is similar to typical plugin development, except for the path. All storefront templates must follow this pattern: `<app-name>/Resources/views/storefront/element/<elementname>.html.twig`

For more details, see the guide on [CMS element development for plugins](./../../plugins/content/cms/add-cms-element.html#storefront-implementation). Below is an example of how your storefront template (`swag-dailymotion/Resources/views/storefront/element/cms-element-swag-dailymotion.html.twig`) could look:

twig

```shiki
{% block element_swag_dailymotion %}
<div class="cms-element-swag-dailymotion" style="height: 100%; width: 100%">
    {% block element_dailymotion_image_inner %}
    <div class="cms-el-swag-dailymotion">
        <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
            <iframe style="width:100%; height:100%; position:absolute; left:0px; top:0px; overflow:hidden"
                    src="https://www.dailymotion.com/embed/video//{{ element.config.dailyUrl.value }}"
                    frameborder="0"
                    type="text/html"
                    width="100%"
                    height="100%">
            </iframe>
        </div>
    </div>
    {% endblock %}
</div>
{% endblock %}
```

---

## Add translations for apps

**Source:** https://developer.shopware.com/docs/guides/plugins/apps/administration/adding-snippets.html

# Adding translations for apps [​](#adding-translations-for-apps)

Adding snippets to the administration works the same way for plugins and apps. The only difference is the file structure and that apps are not allowed to override existing snippet keys. The only thing to do, therefore, is to create new files in the following directory: `<app root>/Resources/app/administration/snippet` Additionally, you need JSON files for each language you want to support, using the respective language locale (e.g., `de.json`, `en.json`). You can also include patch files for dialects, such as `en-US.json`, to provide country-specific translations.

For more details on selecting a fallback language and structuring your snippet files, see the [Fallback Languages guide](./../../../../concepts/translations/fallback-language-selection.html).

Since everything else works the same, please refer to our [Adding translations for plugins](./../../plugins/administration/templates-styling/adding-snippets.html) guide for more information.

---

