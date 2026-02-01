# Resources

*Scraped from Shopware Developer Documentation*

---

## References

**Source:** https://developer.shopware.com/docs/resources/references/

# References [​](#references)

The references serve as essential resources for developers, administrators, and testers, providing comprehensive details on implementation parameters. They cover every aspect of the platform, including objects, functions, classes, and more. By consulting these references, you will be able to gain a deep understanding of Shopware's capabilities and utilize its features effectively in your development, administration, and testing tasks.

---

## API Reference

**Source:** https://developer.shopware.com/docs/resources/references/api-reference/

# API Reference [​](#api-reference)

The API references provide detailed information about the available endpoints, methods, parameters, request and response formats, and authentication mechanisms of an API. It provides essential information on how to interact with the API, what data can be sent or received, and how to handle different API responses.

These references guide you to use the correct syntax, understand the expected input and output formats, implement the necessary authentication mechanisms and successful API requests and effectively utilize the functionality provided by the API in your applications.

There are two dedicated API reference documents for your reference:

* [Store API reference](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide) - Focused on customer-facing aspects, the Store API allows you to access and manipulate data related to products, customer interactions, shopping carts, and others that significantly impact the frontend user experience. It caters to both anonymous and authenticated users.
* [Admin API reference](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide) - Primarily for backend and administrative functions, the Admin API enables structured data exchanges, bulk operations, data synchronization, and import-export tasks, addressing the backend needs of the Shopware platform.

---

## Administration Reference

**Source:** https://developer.shopware.com/docs/resources/references/administration-reference/

# Administration Reference [​](#administration-reference)

This section covers concepts on Utils, Mixins and Directives.

---

## Utils

**Source:** https://developer.shopware.com/docs/resources/references/administration-reference/utils.html

# Utils [​](#utils)

This is an overview of all the utility functions bound to the shopware global object. Utility functions provide many useful shortcuts for common tasks, see how to use them in your plugin [here](./../../../guides/plugins/plugins/administration/services-utilities/using-utils.html). Or see the code that registers them [here](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/core/service/util.service.js)

## General functions [​](#general-functions)

| Function | Description | Link |
| --- | --- | --- |
| createId | Returns a uuid string in hex format. Generated with [uuid](https://www.npmjs.com/package/uuid) | [link](https://lodash.com/docs/4.17.15#create) |
| throttle | Creates a `throttled` function that only invokes `func` at most once per every `wait` milliseconds. | [link](https://lodash.com/docs/4.17.15#throttle) |
| debounce | Creates a `debounced` function that delays invoking `func` until after `wait` milliseconds have elapsed since the last time the `debounced` function was invoked. | [link](https://lodash.com/docs/4.17.15#debounce) |
| flow | Creates a function that returns the result of invoking the given functions with the `this` binding of the created function, where each successive invocation is supplied the return value of the previous. | [link](https://lodash.com/docs/4.17.15#flow) |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |

## Object [​](#object)

| Function | Description | Link |
| --- | --- | --- |
| deepCopyObject | Deep copy an object |  |
| hasOwnProperty | Shorthand method for `Object.prototype.hasOwnProperty` |  |
| getObjectDiff | Gets a simple recursive diff of two objects. Does not consider an entity schema or entity related logic. |  |
| getArrayChanges | Check if the compared array has changes. |  |
| cloneDeep | Creates recursively a clone of value. | [link](https://lodash.com/docs/4.17.15#cloneDeep) |
| merge | This method is like \_.assign except that it recursively merges own and inherited enumerable string keyed properties of source objects into the destination object. | [link](https://lodash.com/docs/4.17.15#merge) |
| mergeWith | This method is like \_.merge except that it accepts customizer which is invoked to produce the merged values of the destination and source properties. | [link](https://lodash.com/docs/4.17.15#mergeWith) |
| deepMergeObject | Deep merge two objects |  |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |
| set | Sets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#set) |
| pick | Creates an object composed of the picked `object` properties. | [link](https://lodash.com/docs/4.17.15#pick) |

## Debug [​](#debug)

| Function | Description |
| --- | --- |
| warn | General logging function which provides a unified style of log messages for developers. Please keep the log in mind. Messages will be displayed in the developer console when they're running the application in development mode. |
| debug | The same as `warn` but instead of `console.warn` it uses `console.error`. |

## Format [​](#format)

| Function | Description |
| --- | --- |
| currency | Converts a number to a formatted currency. Especially helpful for template filters. |
| date | Formats a Date object to a localized string with the [native `Intl.DateTimeFormat` method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) |
| fileSize | Formats a number of bytes to a string with a unit |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |

## Dom [​](#dom)

| Function | Description |
| --- | --- |
| getScrollbarHeight | Returns the scrollbar height of an HTML element. |
| getScrollbarWidth | Returns the scrollbar width of an HTML element. |
| copyToClipboard | Uses the browser's copy function to copy a string |

## String [​](#string)

| Function | Description | Link |
| --- | --- | --- |
| capitalizeString | Converts the first character of `string` to upper case and the remaining to lower case. | [link](https://lodash.com/docs/4.17.15#capitalize) |
| camelCase | Converts `string` to camel case. | [link](https://lodash.com/docs/4.17.15#camelCase) |
| kebabCase | Converts `string` to kebab case. | [link](https://lodash.com/docs/4.17.15#kebabCase) |
| snakeCase | Converts `string` to snake case. | [link](https://lodash.com/docs/4.17.15#snakeCase) |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |  |
| isEmptyOrSpaces | Gets if the content of the string is really empty. This does also removes any whitespaces that might exist in the text. |  |
| isUrl | Checks if the provided value is a URL |  |
| isValidIp | Checks if the provided value is an IP with this [Regex](https://regex101.com/r/qHTUIe/1) |  |

## Type [​](#type)

| Function | Description | Link |
| --- | --- | --- |
| isObject | Checks if `value` is the [language type](http://www.ecma-international.org/ecma-262/7.0/#sec-ecmascript-language-types) of `Object`. *(e.g. arrays, functions, objects, regexes, `new Number(0)`, and `new String('')`)* | [link](https://lodash.com/docs/4.17.15#isObject) |
| isPlainObject | Checks if `value` is a plain object, that is, an object created by the `Object` constructor or one with a `[[Prototype]]` of `null`. | [link](https://lodash.com/docs/4.17.15#isPlainObject) |
| isEmpty | Checks if `value` is an empty object, collection, map, or set. | [link](https://lodash.com/docs/4.17.15#isEmpty) |
| isRegExp | Checks if `value` is classified as a `RegExp` object. | [link](https://lodash.com/docs/4.17.15#isRegExp) |
| isArray | Checks if `value` is classified as an `Array` object. | [link](https://lodash.com/docs/4.17.15#isArray) |
| isFunction | Checks if `value` is classified as a `Function` object. | [link](https://lodash.com/docs/4.17.15#isFunction) |
| isDate | Checks if `value` is classified as a `Date` object. | [link](https://lodash.com/docs/4.17.15#isDate) |
| isString | Checks if `value` is classified as a `String` primitive or object. | [link](https://lodash.com/docs/4.17.15#isString) |
| isBoolean | Checks if value is classified as a `boolean` primitive or object. | [link](https://lodash.com/docs/4.17.15#isBoolean) |
| isEqual | Performs a deep comparison between two values to determine if they are equivalent. | [link](https://lodash.com/docs/4.17.15#isEqual) |
| isNumber | Checks if `value` is classified as a Number primitive or object. | [link](https://lodash.com/docs/4.17.15#isNumber) |
| isUndefined | Checks if `value` is `undefined`. | [link](https://lodash.com/docs/4.17.15#isUndefined) |

## FileReader [​](#filereader)

| Function | Description | Link |
| --- | --- | --- |
| readAsArrayBuffer | Reads a `file` as an `ArrayBuffer` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsArrayBuffer) |
| readAsDataURL | Reads a `file` as a `Data-URL` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL) |
| readAsText | Reads a `file` as `text` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsText) |
| getNameAndExtensionFromFile | Gets the `name` and `extension` from a file |  |
| getNameAndExtensionFromUrl | Gets the `name` and `extension` from a URL |  |

## Sort [​](#sort)

| Function | Description |
| --- | --- |
| afterSort | Sorts the elements by their after id property chain |

## Array [​](#array)

| Function | Description | Link |
| --- | --- | --- |
| flattenDeep | Recursively flattens `array`. | [link](https://lodash.com/docs/4.17.15#flattenDeep) |
| remove | Removes all elements from `array` that predicate returns truthy for and returns an array of the removed elements | [link](https://lodash.com/docs/4.17.15#remove) |
| slice | Creates a slice of `array` from `start` up to, but not including, `end`. | [link](https://lodash.com/docs/4.17.15#slice) |
| uniqBy | This method is like [`_.uniq`](https://lodash.com/docs/4.17.15#uniq) except that it accepts `iteratee` which is invoked for each element in `array` to generate the criterion by which uniqueness is computed. | [link](https://lodash.com/docs/4.17.15#uniqBy) |

---

## Mixins

**Source:** https://developer.shopware.com/docs/resources/references/administration-reference/mixins.html

# Mixins [​](#mixins)

This is an overview of all the mixins provided by the Shopware 6 Administration. Mixins in the Shopware 6 Administration are essentially the same in default Vue. They behave generally the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. Learn more about them in the official [Vue documentation](https://vuejs.org/v2/guide/mixins.html).

Also take a look at [how to use them in your plugin](./../../../guides/plugins/plugins/administration/mixins-directives/using-mixins.html) and [how to register your own mixin](./../../../guides/plugins/plugins/administration/mixins-directives/add-mixins.html).

## Overview of all the mixins [​](#overview-of-all-the-mixins)

| Name | Description | Link |
| --- | --- | --- |
| `discard-detail-page-changes` | Mixin which resets entity changes on page leave or if the id of the entity changes. This also affects changes in associations of the entity | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/discard-detail-page-changes.mixin.ts) |
| `form-field` | This mixin is used to provide common functionality between form fields | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/form-field.mixin.ts) |
| `generic-condition` |  | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/generic-condition.mixin.ts) |
| `listing` | Mixin which is used in almost all listing pages to for example keep track of the current page of the administration | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/listing.mixin.ts) |
| `notification` | This mixin is used to create notifications in the administrations more easily | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/notification.mixin.ts) |
| `placeholder` | Provides a function to localize placeholders | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/placeholder.mixin.ts) |
| `position` | A Mixin which contains helpers to work with position integers | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/position.mixin.ts) |
| `remove-api-error` | This mixin removes API errors e.g. after the user corrected a invalid input i.e. leaving the product name field blank | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/remove-api-error.mixin.ts) |
| `rule-container` | Provides common functions between the `sw-condition-or-container` and the `sw-condition-and-container` | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/rule-container.mixin.ts) |
| `salutation` | A common adapter for the `salutation` filter | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/salutation.mixin.ts) |
| `sw-inline-snippet` | Makes it possible to use snippets inline | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/sw-inline-snippet.mixin.ts) |
| `user-settings` |  | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/form-field.mixin.ts) |
| `validation` | Is used to validate inputs in various form fields | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/validation.mixin.ts) |

---

## Directives

**Source:** https://developer.shopware.com/docs/resources/references/administration-reference/directives.html

# Directives reference [​](#directives-reference)

This is an overview of all the directives registered globally to Vue. Directives are the same as normally in Vue. Checkout the [Using directives](./../../../guides/plugins/plugins/administration/mixins-directives/adding-directives.html) article or refer to the [directives](https://github.com/shopware/shopware/tree/trunk/src/Administration/Resources/app/administration/src/app/directive) folder in the GIT repository.

## Overview of directives [​](#overview-of-directives)

| Name | Task |
| --- | --- |
| `autofocus` | Focuses an `<input>` in an element on insertion. |
| `dragdrop` | Enables the drag and drop functionality of the CMS. |
| `popover` | Directive for automatic edge detection of the element place |
| `responsive` | Adds methods to add responsive element classes |
| `tooltip` | Provides utility functions to display tooltips. |

---

## Storefront Reference

**Source:** https://developer.shopware.com/docs/resources/references/storefront-reference/

# Storefront Reference [​](#storefront-reference)

The storefront reference documents functions, filters, and extensions that are available for customizing storefronts. It helps you understand how to use these features to enhance the functionality and appearance of your storefront.

---

## Shopware's twig functions

**Source:** https://developer.shopware.com/docs/resources/references/storefront-reference/twig-function-reference.html

# Shopware's twig functions [​](#shopware-s-twig-functions)

In Shopware, Twig's functionality is extended with custom tags, functions, filters, and extensions.

INFO

Official support for complete Twig multi inheritance using sw\_\* equivalents available since 6.7

WARNING

Templates which are imported via {% sw\_use %} are not allowed to have additional twig statements outside of twig blocks. Therefore, changes in core templates which are imported via {% sw\_use %} might break your app or plugin.

## Tags [​](#tags)

| Function | Description | Notes |
| --- | --- | --- |
| `sw_extends` | Inherits from another file with support for multi inheritance. The API is the same like in Twig's default `extends` | See [Twig 3 documentation for `extends`](https://twig.symfony.com/doc/3.x/tags/extends.html) |
| `sw_include` | Includes template partials with support for multi inheritance. The API is the same like in Twig's default `include` but limited to one file at once | See [Twig 3 documentation for `include`](https://twig.symfony.com/doc/3.x/tags/include.html) |
| `sw_embed` | Includes another file with directly overwriting blocks with support for multi inheritance. The API is the same like in Twig's default `embed` | See [Twig 3 documentation for `embed`](https://twig.symfony.com/doc/3.x/tags/embed.html) |
| `sw_use` | Includes template blocks without rendering them from another file with support for multi inheritance. The API is the same like in Twig's default `use` | See [Twig 3 documentation for `use`](https://twig.symfony.com/doc/3.x/tags/use.html) |
| `sw_import` | Includes all macros from another file with support for multi inheritance. The API is the same like in Twig's default `import` | See [Twig 3 documentation for `import`](https://twig.symfony.com/doc/3.x/tags/import.html) |
| `sw_from` | Includes single macros from another file with support for multi inheritance. The API is the same like in Twig's default `from` | See [Twig 3 documentation for `from`](https://twig.symfony.com/doc/3.x/tags/from.html) |
| `sw_icon` | Displays an icon from a given icon set | See [Add custom icon](./../../../guides/plugins/plugins/storefront/add-icons.html#adding-icon) guide for details. |
| `sw_thumbnails` | Renders a tag with correctly configured “srcset” and “sizes” attributes based on the provided parameters | See [Add thumbnail](./../../../guides/plugins/plugins/storefront/use-media-thumbnails.html) guide for more information. |

## Functions [​](#functions)

| Function | Description | Notes |
| --- | --- | --- |
| `config` | Gets a value from the system config (used by plugins and global settings) for the given sales channel | See [Reading the configuration values](./../../../guides/plugins/apps/configuration.html) |
| `theme_config` | Gets a value from the current theme | See [Theme configuration](./../../../guides/plugins/themes/theme-configuration.html) |
| `sw_block` | Renders a block of the same or another file with support for multi inheritance. The is the same like in Twig's default `block` | See [Twig 3 documentation for `block`](https://twig.symfony.com/doc/3.x/functions/block.html) |
| `sw_source` | Prints the content of a template file with support for multi inheritance. The is the same like in Twig's default `source` | See [Twig 3 documentation for `source`](https://twig.symfony.com/doc/3.x/functions/source.html) |
| `sw_include` | Renders the content of another template file with support for multi inheritance. The is the same like in Twig's default `include` and the new `sw_include` tag | See [Twig 3 documentation for `include`](https://twig.symfony.com/doc/3.x/functions/include.html) |

## Filter [​](#filter)

| Filter | Description | Notes |
| --- | --- | --- |
| `replace_recursive` | Enables recursive replacement in addition to twig's default `replace` filter | To see an example, see the guide on [add custom JavaScript](./../../../guides/plugins/plugins/storefront/add-custom-javascript.html) |
| `currency` | Adopts currency formatting: The currency symbol and the comma setting. | --- |
| `sw_sanitize` | Filters tags and attributes from a given string. By default, twig's auto escaping is on, so this filter explicitly allows basic HTML tags like <i%gt;, <b>,... | --- |
| `sw_convert_unit` | Convert between measurement units | Available since 6.7.1.0, to see examples, see the [adr on the measurement system](./../../../resources/references/adr/2025-05-12-implement-measurement-system.html) |

## Extensions [​](#extensions)

| Extension | Description | Notes |
| --- | --- | --- |
| `sw_breadcrumb_full()` | Returns all categories defined in the breadcrumb as an array | Contains functionalities of `sw_breadcrumb_types` and `sw_breadcrumb_build_types` |
| `sw_breadcrumb()` | Returns the category tree as array. Entry points of the SalesChannel ( e.g. footer, navigation) are filtered out. | Deprecated in 6.5.0 |
| `sw_breadcrumb_types()` | Yields the types of the categories within the breadcrumb | Deprecated in 6.5.0 |
| `sw_breadcrumb_build_types()` | returns the same as sw\_breadcrumb\_types, only without another repository call | Deprecated in 6.5.0 |
| `seoUrl()` | Returns seo URL of given route | --- |
| `searchMedia()` | Resolves media ids to media objects | See [Add media](./../../../guides/plugins/plugins/storefront/use-media-thumbnails.html) guide for details. |
| `rawUrl()` | Returns full URL | --- |

---

## Storefront plugins

**Source:** https://developer.shopware.com/docs/resources/references/storefront-reference/plugin-reference.html

# Storefront plugins and helper [​](#storefront-plugins-and-helper)

This is a list of available javascript plugins and helpers that can be used and extended.

## Plugins [​](#plugins)

| Plugin | Description | Notes |
| --- | --- | --- |
| `AccountGuestAbortButtonPlugin` | Used on the logout button to fire a `guest-logout` event after logging out from a guest session. | --- |
| `AddToCartPlugin` | Submits the form that adds a product to the cart and opens the OffCanvasCart. E.g., used on product buy buttons. | --- |
| `AddToWishlistPlugin` | Adds or removes a product from the wishlist and toggles the indicator (heart icon) that displays if the current product is on the wishlist. Also updates the wishlist counter in the main header. | --- |
| `AddressEditorPlugin` | Opens a modal to edit the billing or shipping address. | --- |
| `AjaxModalPlugin` | This class extends the Bootstrap modal functionality by adding an event listener to modal triggers that contain a special "data-url" attribute which is needed to load the modal content by AJAX. | --- |
| `BaseSliderPlugin` | Provides basic slider functionality to a container with sliding elements. Uses the "tiny-slider" framework in the background. | --- |
| `BaseWishlistStoragePlugin` | Provides basic storage logic to add, remove and get products from the wishlist. Used by the local storage wishlist (if user is guest) and the persisted wishlist (if used is logged in). | --- |
| `BasicCaptchaPlugin` | Provides the JS functionality for the basic captcha that can be activated in storefront sales channel. Only works with a corresponding form. | --- |
| `BuyBoxPlugin` | Refreshes the buy box area on the product detail page after switching to a different product variant. Re-initializes the tax info modal. | --- |
| `CartWidgetPlugin` | Controls the cart widget in the main header that displays the total cart amount. Updates automatically if a product is added to the cart. | --- |
| `ClearInputPlugin` | Adds clear functionality to input fields. | --- |
| `CmsGdprVideoElement` | Shows a consent overlay before rendering an external CMS video element, e.g. from YouTube. Only when the user provides consent, the actual video will be loaded. | --- |
| `CollapseCheckoutConfirmMethodsPlugin` | Displays a "show more" button when too many shipping or payment methods are shown. Used on the checkout page. | --- |
| `CollapseFooterColumnsPlugin` | Enables collapsing containers (accordion) on mobile viewports for the columns in the page footer. | --- |
| `CookieConfiguration` | Controls the detailed cookie configuration (displayed in an OffCanvas). Displays the available cookies with checkboxes and saves the selected user preference. | --- |
| `CookiePermissionPlugin` | Controls the cookie banner at the bottom of the page when no cookie preference is set. Can either save a preference directly via button or open the cookie configuration OffCanvas. | --- |
| `CountryStateSelectPlugin` | Renders an additional select box with country states (e.g. "North-Rhine-Westphalia") if a country was selected. E.g., used in the registration form. | --- |
| `CrossSellingPlugin` | Used to re-initialize the product sliders when toggling between different cross-selling tabs that contain product sliders. | --- |
| `DateFormat` | This plugin formats a date and converts it to the local timezone if the data attribute date-format is set. | --- |
| `DatePickerPlugin` | Controls the date picker component. Shows a datepicker UI when applied to an input field. | --- |
| `EllipsisPlugin` | Used to expand or shrink a text. | Deprecated and removed in v6.6.0 |
| `FadingPlugin` | Collapses or expands a Bootstrap collapse container with additional "more" or "less" links. | Deprecated and removed in v6.6.0 |
| `FilterBasePlugin` | Provides basic functionality for a product listing filter. Communicates with the `ListingPlugin`. Other filters like "multi select" extend from this plugin class. | --- |
| `FlyoutMenuPlugin` | This Plugin handles the subcategory display of the main navigation. | --- |
| `FormAddHistoryPlugin` | Provides an API to push items into the browser history after a form was submitted. Only works on a `<form>` element. | --- |
| `FormAjaxSubmitPlugin` | This plugin submits a form with ajax without reloading the page, instead of performing a regular form submit. | --- |
| `FormAutoSubmitPlugin` | This plugin automatically submits a form, when the element or the form itself has changed. | --- |
| `FormCmsHandler` | Sends forms from the CMS (e.g. contact form) via ajax and renders additional error/success messages. | --- |
| `FormFieldTogglePlugin` | Provides functionality to display or hide additional form fields without reloading the page. E.g., used in the registration form when shipping and billing addresses are different. | --- |
| `FormPreserverPlugin` | This plugin preserves a form, if the element or the form itself has changed. After a reload of the page the form is filled up with the stored values. | --- |
| `FormScrollToInvalidFieldPlugin` | This plugin scrolls to invalid form fields when the form is submitted. | --- |
| `FormSubmitLoaderPlugin` | This plugin shows a loading indicator on the form submit button when the form is submitted. | --- |
| `FormValidation` | This plugin validates fields of a form. Also styles the field elements with the bootstrap style if enabled. | --- |
| `GoogleAnalyticsPlugin` | Adds all events for Google Analytics and configures the `gtag`. Only used when "Analytics" is activated in the sales channel. | --- |
| `GoogleReCaptchaBasePlugin` | Provides basic functionality to apply a Google reCAPTCHA to a `<form>` element. The JS-plugins for reCAPTCHA v2 and v3 extend this plugin. | --- |
| `GuestWishlistPagePlugin` | Used on the `/wishlist` page/route to display the products currently on the wishlist. Displays wishlist items from local storage if the user is a guest. | --- |
| `ImageZoomPlugin` | Enables functionality to zoom into an image, e.g. using the mouse wheel. Used inside the image zoom modal on the product detail page. Works together with `ZoomModalPlugin`. | --- |
| `ListingPlugin` | Provides the filter functionality of the product listing. Gets the current values of each filter, current sorting and pagination. Generates the requests and displays the new results. | --- |
| `MagnifierPlugin` | Handles the magnifier lens functionality on the detail page. | --- |
| `OffCanvasAccountMenu` | Opens the account dropdown menu ("user avatar" icon in header) inside an OffCanvas on mobile viewports. | --- |
| `OffCanvasCartPlugin` | Opens the shopping cart in an OffCanvas. Used on the shopping cart display in the main header. | --- |
| `OffCanvasFilter` | Opens the listing filters inside an OffCanvas when the mobile "Filter" button is clicked. Only used on mobile viewports. | --- |
| `OffCanvasTabs` | Used on mobile viewports to open or show contents in an OffCanvas that are shown in Bootstrap tabs on larger desktop viewports. E.g., used on the product detail page to open the reviews on mobile. | --- |
| `OffcanvasMenuPlugin` | Displays the main category navigation inside an OffCanvas on mobile viewports. Triggered by the mobile "hamburger" menu icon. | --- |
| `QuantitySelectorPlugin` | Enables functionality to select a product's quantity. Controls the increase (+) or decrease (-) buttons. E.g., used on the product detail page or in the checkout. | --- |
| `RatingSystemPlugin` | Controls the rating stars when the user is writing a product review and lets the user select a star rating between 1 and 5. | --- |
| `RemoteClickPlugin` | This plugin is used to remotely click on another element. | --- |
| `ScrollUpPlugin` | Displays a small button with an "arrow up" icon to scroll back to the top of the page. Used on all pages and only displayed when the user has scrolled down the page. | --- |
| `SearchWidgetPlugin` | Renders a dropdown with search result suggestions underneath the main headers search input field, as soon as the user starts to type a search term. | --- |
| `SetBrowserClassPlugin` | Adds CSS classes to the `<body>` element depending on the current device, e.g. `is-ipad`. These classes can be used to add styling for a specific device category. | --- |
| `SpeculationRulesPlugin` | If this javascript plugin is activated via `Admin > Settings > System > Storefront`, it adds speculation rules for the main navigation, the product listing and the header logo. | --- |
| `VariantSwitchPlugin` | This plugin submits the variant form with the correct data option. Used on the product detail page to switch between product variants. | --- |
| `WishlistWidgetPlugin` | Shows how many items are currently on the wishlist. Used by the wishlist "heart" icon inside the main header. | --- |
| `ZoomModalPlugin` | Opens a full-screen modal window with an image gallery. Can contain multiple images that the user can zoom into. Used on the product detail page. | --- |

## Helpers [​](#helpers)

| Helper | Description | Notes |
| --- | --- | --- |
| `ArrowNavigationHelper` | Helper to navigate between different items using the arrow keys. Used by `SearchWidgetPlugin` | --- |
| `CookieStorageHelper` | Provides a nicer API to add or remove cookies. | --- |
| `DateFormatHelper` | Wrapper helper to format a date string or object using `Intl.DateTimeFormat` | --- |
| `Debouncer` | Wait for a defined amount of time. Basically a wrapper around `setTimeout`. | --- |
| `DeviceDetection` | Returns information about the current device, e.g. if it is a touch device. | --- |
| `DomAccess` | Helper function to access DOM elements in a unified way and improved error handling. | --- |
| `ElementReplaceHelper` | Helper to replace a desired DOM element with another DOM element. | --- |
| `FeatureSingleton` | Offers an API to check if specific feature flags are currently activated. | --- |
| `Iterator` | Helper function to iterate over different data types in a unified way (array, objects etc.) | --- |
| `MemoryStorage` | This class is mainly a fallback if the session, local or cookie storage fails. | --- |
| `NativeEventEmitter` | Event Emitter which works with the provided DOM element. The class isn't meant to be extended. | --- |
| `StorageSingleton` | Wrapper API that can use local, session or cookie storage in the background. | --- |
| `StringHelper` | Provides different string formatters, e.g. converting into "UpperCamelCase" | --- |
| `ViewportDetection` | Returns the currently active Bootstrap viewport, e.g. `LG` or `XL` | --- |

---

## Testing Reference

**Source:** https://developer.shopware.com/docs/resources/references/testing-reference/

# Testing Reference [​](#testing-reference)

In this reference, all Shopware commands provided by [E2E-testsuite-platform](https://github.com/shopware/e2e-testsuite-platform) or [Shopware Platform](https://github.com/shopware/shopware) are listed here.

---

## Custom E2E Commands

**Source:** https://developer.shopware.com/docs/resources/references/testing-reference/e2e-custom-commands.html

# Custom E2E Commands [​](#custom-e2e-commands)

## General commands [​](#general-commands)

| Command | Parameter | Description |
| --- | --- | --- |
| setLocaleToEnGb | - | Switches administration UI locale to EN\_GB |
| login | `(userType)` | Logs in to the Administration manually |
| typeAndCheck | `(textToType)` | Types in an input element and checks if the content was correctly typed |
| clearTypeAndCheck | `(textToType)` | Clears field, types in an input element and checks if the content was correctly typed |
| typeMultiSelectAndCheck | `(textToType, { searchTerm: searchTerm })` | Types in a sw-select field and checks if the content was correctly typed (multi select) |
| typeSingleSelect | `(textToType, selector)` | Types in an sw-select field (single select) |
| typeSingleSelectAndCheck | `(textToType, selector)` | Types in an sw-select field and checks if the content was correctly typed (single select) |
| typeLegacySelectAndCheck | `(textToType, { searchTerm: searchTerm })` | Types in an legacy swSelect field and checks if the content was correctly typed |
| typeAndCheckSearchField | `(searchTerm)` | Types in the global search field and verify search terms in url |
| awaitAndCheckNotification | `(message)` | Wait for a notification to appear and check its message |
| clickContextMenuItem | `(actionInMenuSelector, openMenuSelector, scope = '')` | Click context menu in order to cause a desired action |
| clickMainMenuItem | `({ targetPath, mainMenuId, subMenuId })` | Navigate to module by clicking the corresponding main menu item |
| openUserActionMenu | `({ targetPath, mainMenuId, subMenuId })` | Click user menu to open it up |
| dragTo | `(target)` | Drags the previous subject element to a target, performing a drag and drop operation |
| onlyOnFeature | `(feature)` | Only run the test (skip otherwise) if the feature is activated |
| skipOnFeature | `(feature)` | Skip the test if the feature is activated |

## Storefront-related / Sales Channel API commands [​](#storefront-related-sales-channel-api-commands)

| Command | Parameter | Description |
| --- | --- | --- |
| getSalesChannelId | - | Get the sales channel Id via Admin API |
| storefrontApiRequest | `(method, endpoint, header = {}, body = {})` | Performs Storefront API Requests |
| getRandomProductInformationForCheckout | - | Returns random product with id, name and url to view product |

## System Commands [​](#system-commands)

| Command | Parameter | Description |
| --- | --- | --- |
| activateShopwareTheme | - | Activates Shopware theme for Cypress test runner |
| cleanUpPreviousState | - | Cleans up any previous state by restoring database and clearing caches |
| openInitialPage | - | Opens up the administration initially and waits for the "me" call to be successful |

## API commands [​](#api-commands)

| Command | Parameter | Description |
| --- | --- | --- |
| authenticate | - | Authenticate towards the Shopware API |
| loginViaApi | - | Logs in silently using Shopware API |
| searchViaAdminApi | `(data)` | Search for an existing entity using Shopware API at the given endpoint |
| requestAdminApi | `(method, url, requestData)` | Handling API requests |
| updateViaAdminApi | `(endpoint, id, data)` | Updates an existing entity using Shopware API at the given endpoint |

## Fixture commands [​](#fixture-commands)

| Command | Parameter | Description |
| --- | --- | --- |
| setToInitialState | - | Sets Shopware back to its initial state if using platform E2E backup routine |
| createDefaultFixture | `(endpoint, data = {}, jsonPath)` | Create entity using Shopware API via given endpoint |
| createProductFixture | `(userData = {})` | Create product fixture using Shopware API via given endpoint |
| createCategoryFixture | `(userData = {})` | Create category fixture using Shopware API via given endpoint |
| createSalesChannelFixture | `(userData = {}` | Create sales channel fixture using Shopware API via given endpoint |
| setSalesChannelDomain | `(salesChannelName = 'Storefront')` | Create sales channel domain using Shopware API at the given endpoint |
| createCustomerFixture | `(userData = {})` | Create customer fixture using Shopware API via given endpoint |
| createCmsFixture | `(userData = {})` | Create cms fixture using Shopware API at the given endpoint |
| createPropertyFixture | `(options, userData)` | Create property fixture using Shopware API at the given endpoint |
| createLanguageFixture | - | Create language fixture using Shopware API at the given endpoint |
| createShippingFixture | `(userData)` | Create shipping fixture using Shopware API at the given endpoint |
| createSnippetFixture | - | Create snippet fixture using Shopware API at the given endpoint |
| createGuestOrder | `productId, userData)` | Create guest order fixture |
| setProductFixtureVisibility | `(productName, categoryName)` | Sets category and visibility for a product in order to set it visible in the Storefront |

---

## E2E Commands

**Source:** https://developer.shopware.com/docs/resources/references/testing-reference/e2e-commands.html

# E2E Commands [​](#e2e-commands)

| Command | Description |
| --- | --- |
| `bin/console e2e:restore-db` | Sets Shopware back to state of the backup |
| `APP_ENV=e2e bin/console e2e:dump-db` | Creates a backup of Shopware's database |
| `composer run e2e:setup` | Prepares Shopware installation and environment for Cypress usage |
| `composer run e2e:open` | Opens Cypress' e2e tests runner |
| `composer run e2e:prepare` | Install dependencies and prepare database for Cypress usage |
| `composer e2e:cypress -- run --spec="cypress/e2e/administration/**/*.cy.js"` | Runs Cypress' admin e2e tests in CLI |
| `composer e2e:cypress -- run --spec="cypress/e2e/storefront/**/*.cy.js"` | Runs Cypress' storefront e2e tests in CLI |

---

## Security

**Source:** https://developer.shopware.com/docs/resources/references/security.html

# Security [​](#security)

## Overview [​](#overview)

This reference presents a comprehensive compilation of all security measures implemented in Shopware 6, along with instructions on how to configure them.

INFO

If you have found a security vulnerability in Shopware, please report it to us following the instructions in our [Security Advisory Form](https://github.com/shopware/shopware/security/advisories/new).

## ACL in the Administration [​](#acl-in-the-administration)

The Access Control List (ACL) in Shopware ensures that by default, data can only be created, read, updated, or deleted (CRUD), once the user has specific privileges for a module. [ACL in the Administration](./../../concepts/framework/architecture/administration-concept.html#acl-in-the-administration)

## API aware field [​](#api-aware-field)

The `ApiAware` flag allows you to control what fields of your entity are exposed to the Store API. For more information, refer to [Flags Reference](./core-reference/dal-reference/flags-reference.html).

## Captcha [​](#captcha)

Captchas help to verify the user's humanity and prevent automated bots or scripts from gaining access. For more information, refer to [Captcha](https://docs.shopware.com/en/shopware-en/settings/basic-information#captcha) article.

## CSP [​](#csp)

[Content Security Policies](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSPs) are used to prevent Cross-Site-Scripting (XSS) attacks, as well as data injection attacks. This policy specifies the sources from which additional content (e.g., images, scripts, etc.) can be included.

The default policies are configured over the `shopware.security.csp_templates` symfony container parameter and can be adjusted over the container configuration.

## File access [​](#file-access)

Shopware 6 stores and processes a wide variety of files. This goes from product images or videos to generated documents such as invoices or delivery notes. This data should be stored securely, and backups should be generated regularly. For more information, refer to [File system](./../../guides/hosting/infrastructure/filesystem.html)

## Media upload by URL [​](#media-upload-by-url)

Shopware offers a convenience feature to allow media file uploads by directly providing a URL pointing to a third party location containing that file. By default, Shopware validates the URL to ensure that it points to a publicly accessible resource; this prevents attacks where internal networking information might be leaked. You can disable this validation by toggling the `shopware.media.enable_url_validation` to false. However, there is still some security risk in this approach, as your Shopware server makes a request to the external URL and therefore discloses some information about itself (e.g. IP address or user agent). If this is a concern to you, you can disable the whole URL upload feature by setting `shopware.media.enable_url_upload_feature = false`.

## GDPR compliance [​](#gdpr-compliance)

General Data Protection Regulation (GDPR) is a comprehensive European Union (EU) regulation that enhances individuals' privacy rights by imposing strict rules on how organizations collect, process, and protect personal data. For more information, refer to [GDPR](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/gdpr) guide.

Shopware provides a comprehensive [Cookie Consent Management](./../../concepts/commerce/content/cookie-consent-management.html) system with features to help shop owners handle customer privacy preferences, ensure transparent cookie handling, and support GDPR compliance efforts.

## HTML sanitizer [​](#html-sanitizer)

HTML sanitizer improves security, reliability, and usability of the text editor by removing potentially unsafe or malicious HTML code. For more information, refer to [HTML Sanitizer](./../../guides/hosting/configurations/shopware/html-sanitizer.html) guide.

## Rate limiter [​](#rate-limiter)

Shopware 6 provides certain rate limits by default that reduces the risk of brute-force attacks for pages like login or password reset. For more information, refer to [Rate Limiter](./../../guides/hosting/infrastructure/rate-limiter.html) guide.

## Reset sessions when changing password [​](#reset-sessions-when-changing-password)

As soon as a password is changed for a user or customer, the session is invalid and the user or customer must log in again. For more information, refer to:

* [User Changelog](https://github.com/shopware/shopware/commit/5ea99ee5d7a12bab3a01a64c3948eee7c4188ede)
* [Customer Changelog](https://github.com/shopware/shopware/commit/47b4b094c13f62db860be2f431138bb45c0bd0b6)

## SameSite cookie [​](#samesite-cookie)

SameSite prevents the browser from sending cookies along with cross-site requests. For more information on this, refer to [SameSite Protection](./../../guides/hosting/configurations/framework/samesite-protection.html).

## Security plugin [​](#security-plugin)

Obtaining security fixes without version upgrades is possible through the [Security plugin](./../../guides/hosting/installation-updates/cluster-setup.html#security-plugin).

## Storefront IP Whitelisting [​](#storefront-ip-whitelisting)

To enable access even during maintenance mode, IP addresses can be added to [Storefront IP whitelisting](https://docs.shopware.com/en/shopware-6-en/settings/saleschannel#status).

## SQL injection [​](#sql-injection)

SQL injection allows an attacker to execute new or modify existing SQL statements to access information that they are not allowed to access. By mainly using our own [Data Abstraction Layer](/docs/concepts/framework/data-abstraction-layer.html), that does not expose SQL directly, most of the SQL injection attack vectors are prevented. Whenever direct SQL is being used, the [best practices from Doctrine DBAL](https://www.doctrine-project.org/projects/doctrine-dbal/en/current/reference/security.html) are followed to ensure proper escaping of user input.

---

## Guidelines

**Source:** https://developer.shopware.com/docs/resources/guidelines/

# Guidelines [​](#guidelines)

This document is intended for all readers and contributors. We have defined coding, documentation, and testing guidelines.

The code section lays out the coding standards. This helps anyone understand and modify the code at any point while keeping the code consistent.

[Code](./code/)

The test section briefs you about best practices for writing end-to-end tests.

[Test](./testing/)

The document section details you on the language style, grammar, markdown syntax, and documentation process.

[Document](./documentation-guidelines/)

this document serves as a comprehensive resource for both readers and contributors, offering essential coding, testing, and documentation guidelines to maintain consistency, promote best practices, and facilitate effective collaboration.

---

## Troubleshooting

**Source:** https://developer.shopware.com/docs/resources/guidelines/troubleshooting/

# Troubleshooting [​](#troubleshooting)

Use this section to diagnose and resolve common issues you might encounter while working with Shopware projects.

---

## Performance

**Source:** https://developer.shopware.com/docs/resources/guidelines/troubleshooting/performance.html

# Performance [​](#performance)

## Common Performance Considerations [​](#common-performance-considerations)

### Dynamic product groups are slow to load [​](#dynamic-product-groups-are-slow-to-load)

When you use a `contains` filter in dynamic product groups (especially when you use that on a custom field), the loading of that dynamic product group might get slow. The reason is that the underlying SQL query is not and cannot be optimized for this kind of filter. When you use OpenSearch instead of relying on the DB for searching, this issue should be resolved. Alternatively, for using `contains` on custom fields, it should be preferred to create individual bool custom fields for the different values and check those instead. When contains on usual fields is used and slow, it should help to add a [custom field](./../../../guides/plugins/plugins/framework/custom-field/index.html) and manually manage that. Alternatively, [tags](https://docs.shopware.com/en/shopware-6-en/settings/tags) can be used for this purpose.

### Cache is invalided too often [​](#cache-is-invalided-too-often)

It might be that your caching is not effective because the cache is invalidated too often. You should look for the reason why the cache is invalidated that frequently. In general, it means that probably there is a background process running that leads to the cache invalidation. This could be more obvious cases like cron jobs manually clearing the cache or more subtle cases like your ERP system syncing products frequently, which will lead to cache invalidations of all pages where those products are referenced. For cases like the latter, there is the option to only clear the cache delayed and not immediately ([this will be the new default starting with shopware 6.7.0.0](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.7.md#delayed-cache-invalidation)). You might consider [activating this feature](./../../../guides/hosting/performance/performance-tweaks.html#redis-for-delayed-cache-invalidation) in older versions.

### High Memory Usage [​](#high-memory-usage)

While using certain APIs or e.g. the `EntityRepository` it might happen that the memory usage is increasing constantly. First, you should make sure that you have set the `APP_ENV` variable to `prod` in your `.env` file. If the `APP_ENV` is set to `dev` Shopware keeps many objects for debugging purposes, which will lead to high memory usage. If the memory usage issue persists after setting `APP_ENV` to `prod`, check if you are using the [sync API](https://shopware.stoplight.io/docs/admin-api/faf8f8e4e13a0-bulk-payloads). Also consider changing the `indexing-behavior` to your needs if you need to sync many entities. Another reason for high memory usage might be the logging within the application. See the logging section in the [performance guide](./../../../guides/hosting/performance/performance-tweaks.html#logging) for more information. After all, you still can make use of tools like blackfire.io to find the root cause of the memory usage.

---

## PHPStan

**Source:** https://developer.shopware.com/docs/resources/guidelines/troubleshooting/phpstan.html

# PHPStan [​](#phpstan)

## Common PHPStan Issues in Shopware Code [​](#common-phpstan-issues-in-shopware-code)

### EntityRepository Should Define a Generic Type [​](#entityrepository-should-define-a-generic-type)

**Problem**: Repository returns EntityCollection without type information.

php

```shiki
$products = $this->productRepository->search($criteria, $context)->getEntities();
foreach ($products as $product) {
    // PHPStan doesn't know $product is ProductEntity
    $name = $product->getName(); // Call to an undefined method Shopware\Core\Framework\DataAbstractionLayer\Entity::getName()
}
```

**Solution**: Add a PHP doc with a generic type to EntityRepository:

php

```shiki
class Foo
{
    /**
     * @param EntityRepository<ProductCollection> $productRepository
     */
    public function __construct(
        private readonly EntityRepository $productRepository,
    ) {
    }

    public function doSomething(): void
    {
        // ...
        $products = $this->productRepository->search($criteria, $context)->getEntities();
        foreach ($products as $product) {
            $name = $product->getName(); // PHPStan correctly identifies this as ProductEntity
        }
    }
}
```

Be aware that the `EntityRepository` class is a generic class, which gets an EntityCollection as type. This might sound counter-intuitive and different to other well-known repository classes, which take the Entity class as the generic type. But it was the easiest technical solution to get PHPStan to understand the type of the collection returned by the search method.

### Null Safety with First method and Associations [​](#null-safety-with-first-method-and-associations)

**Problem**: Calling `first` could return `null`, also entity associations can be `null` if not loaded.

php

```shiki
$product = $this->productRepository->search($criteria, $context)->first();
$manufacturer = $product->getManufacturer(); // Cannot call method getManufacturer() on Shopware\Core\Content\Product\ProductEntity|null.
$manufacturerName = $manufacturer->getName(); // Cannot call method getName() on Shopware\Core\Content\Product\Aggregate\ProductManufacturer\ProductManufacturerEntity|null.
```

**Solution**: Ensure associations are added before in the criteria and always check for possible `null` returns:

php

```shiki
$criteria = new Criteria();
$criteria->addAssociation('manufacturer');

$product = $this->productRepository->search($criteria, $context)->first();
if ($product === null) {
    throw new ProductNotFoundException();
}

$manufacturer = $product->getManufacturer();
if ($manufacturer === null) {
    throw new ManufacturerNotLoadedException();
}

$manufacturerName = $manufacturer->getName(); // No error
```

Or use the null-safe operators:

php

```shiki
$manufacturerName = $product?->getManufacturer()?->getName() ?? 'Unknown';
```

### Missing Generic Type for EntityCollection [​](#missing-generic-type-for-entitycollection)

**Problem**: Custom EntityCollection does not have a generic type.

php

```shiki
class FooCollection extends EntityCollection
{
    protected function getExpectedClass(): string
    {
        return FooEntity::class;
    }
}

$foo = $fooCollection->first();
if ($foo === null) {
    throw new FooNotFoundException();
}
$foo->bar(); // Cannot call method bar() on Shopware\Core\Framework\DataAbstractionLayer\Entity.
```

**Solution**: Add a generic type to EntityCollection:

php

```shiki
/**
 * @extends EntityCollection<FooEntity>
 */
class FooCollection extends EntityCollection
{
    protected function getExpectedClass(): string
    {
        return FooEntity::class;
    }
}

$foo = $fooCollection->first();
if ($foo === null) {
    throw new FooNotFoundException();
}
$foo->bar(); // No error
```

---

## Elasticsearch

**Source:** https://developer.shopware.com/docs/resources/guidelines/troubleshooting/elasticsearch.html

# Elasticsearch [​](#elasticsearch)

## Common Error Handling [​](#common-error-handling)

### Enabling `SHOPWARE_ES_THROW_EXCEPTION` [​](#enabling-shopware-es-throw-exception)

It is recommended to set the environment variable `SHOPWARE_ES_THROW_EXCEPTION=0` in **production environments** and enable it (`=1`) in **development environments**. This setting helps prevent unexpected interruptions to other processes caused by Elasticsearch or OpenSearch issues.

Some common scenarios include:

* **Search server is not reachable**: If the OpenSearch or Elasticsearch server is temporarily unavailable, keeping this option disabled (`=0`) allows Shopware to automatically fall back to the default MySQL-based search. This ensures that search functionality remains available. A similar fallback also applies when updating products in the Administration, where data synchronization with the search server might fail intermittently.
* **System updates causing expected errors**: During updates—whether through the web UI or via the CLI (`bin/console system:update:finish`)—index mappings may change, requiring a reindex. These expected errors should not block system updates in production, which is why exceptions should remain disabled in such environments.

---

## Adjusting N-gram Settings for Search Precision [​](#adjusting-n-gram-settings-for-search-precision)

When a search field is marked as *searchable* and the **“Split search term”** option is enabled, Shopware uses an **n-gram tokenizer** to index and search that field. By default, Shopware uses the following configuration:

bash

```shiki
SHOPWARE_ES_NGRAM_MIN_GRAM=4
SHOPWARE_ES_NGRAM_MAX_GRAM=5
```

With this configuration, a term like `"shopware"` is tokenized into the following n-grams:

bash

```shiki
["shop", "hopw", "opwa", "pwar", "ware", "shopw", "hopwa", "opwar", "pware"]
```

This allows search results to match even if only part of the search term is entered—for example, searching for `"ware"` will still find `"shopware"`.

If you want to make the search more flexible (fuzzier) or more precise (stricter), you can adjust the environment variables:

bash

```shiki
SHOPWARE_ES_NGRAM_MIN_GRAM=<value>
SHOPWARE_ES_NGRAM_MAX_GRAM=<value>
```

After modifying these values, a full Elasticsearch reindex is required to apply the new configuration:

bash

```shiki
bin/console es:index
```

---

## Test

**Source:** https://developer.shopware.com/docs/resources/guidelines/testing/

# Testing [​](#testing)

Testing ensures software reliability, quality, and optimum performance. Detailed E2E testing and quality guidelines are described in the following sections.

---

## Testing guidelines for extensions

**Source:** https://developer.shopware.com/docs/resources/guidelines/testing/store/

# Testing Guidelines for Shopware Extensions [​](#testing-guidelines-for-shopware-extensions)

This section guides you with the criteria used to test your extension. Detailed information is available on [quality guidelines for apps](./../store/quality-guidelines-apps/) and [quality guidelines for plugins](./../store/quality-guidelines-plugins/)

Check out the points that affect your extension and go through them before submitting it for testing.

We assign three statuses when testing your extension:

TIP

OK: This point was tested and passed

DANGER

Failed: This point was tested, and errors were found

WARNING

Not necessary: This point does not need to be tested

## Test criteria [​](#test-criteria)

Here is what the test criteria include:

* **[Function availability](./../store/quality-guidelines-apps/#every-app-based-on-the-app-system)** - Here, we proceed like a user and check the complete functionality of the app, as well as the logical structure and usability. For instance,

  + Is a general function as described in your extension available?
  + Do the buttons, export, rules, etc., work?
  + Are errors displayed in the console?
* **[Lighthouse audit home/listing/detail](./../store/quality-guidelines-apps/#frontend-apps)** - We check:

  + If your extension affects the Storefront or not? (so that the search engines have no problems with it).
  + If all buttons, labels, etc., are named correctly?

We pay attention to all five audits. The app must not limit these. Like most search engines, we also pay attention to mobile-first.

* **[Rich snippet home/listing/detail](./../store/quality-guidelines-apps/#template-tests)** - We check:

  + If the page can be indexed?
  + Is there any incorrect price information being displayed?

Rich snippets have no influence on the ranking of a website. Thus, they do not count among the ranking factors. Nevertheless, search hits enriched with additional information have various SEO advantages: higher attention, higher click-through rate, and greater relevance.

* **[No errors in the Storefront and 503/404 errors](./../store/quality-guidelines-apps/#error-messages-must-be-entered-in-the-event-log)** - We check:

  + If the app is active in the Storefront?
  + If it involves display errors and errors of any kind?

The end customer should not receive any misleading error messages. It does not matter whether a function causes the error or the customer does not use the function correctly. For example, the customer can upload a picture using a function, but if the customer tries to upload a video, a clear message should be displayed here.

* **[Cookie check storefront/checkout](./../store/quality-guidelines-apps/#register-a-cookie-to-the-cookie-consent-manager)** - Since the GDPR/DSGVO, the classification of cookies is particularly important. We distinguish between three types of cookies.

  + **Technically required**: Only cookies that are really important for the store without which no purchase would be possible.
  + **Comfort functions**: Cookies to display personalized ads as banners, newsletter pop-ups, and content from video and social media platforms.
  + **Statistics and Tracking**: Statistics and everything that has to do with data collection and tracking.
* **[Store description German/English](./../store/quality-guidelines-apps/#app-descriptions-in-your-shopware-account)** - The app store description includes several points if the app can be used only in a specific country, so leave this clearly in the description. The German description is only mandatory if the app is to be offered in the German market. Furthermore, there must always be at least two images of the app in English, e.g., of the Storefront and the Admin. [Here](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to) you can find a guide detailing how to add images and icons to the extensions.
* **[Translations managed admin](./../store/quality-guidelines-apps/#fallback-language)** - We check if the app is available in all languages specified in your account. However, it is important that English is fallback if the app does not support any other language.
* **[API validation](./../store/quality-guidelines-apps/#api-or-payment-apps)** - If access data is required for the app - for example, an API key; a button must be implemented with which the customer can check the data if this is technically possible.

![api access](/assets/guidelines-test-store-apiValidation.C22JOcdJ.png)

* **[Uninstallation process](./../store/quality-guidelines-apps/#extension-manager)** - During the uninstallation process, the app should be able to uninstall and install without any problems. It is also important to check whether the app depends on other apps and whether they must be uninstalled first.
* **Data will be removed from the database after uninstallation** - If the customer selects the option "delete all data" during uninstallation, then all the data has to be removed from the database that was created with the app.
* **Manual code review by a Shopware developer to ensure code quality** - This is the last step. A developer looks at the app's code to ensure it is clean and has no security gaps.

---

## Quality guidelines for apps and themes in the app system

**Source:** https://developer.shopware.com/docs/resources/guidelines/testing/store/quality-guidelines-apps/

# Quality Guidelines for apps and themes based on the app system in the Shopware Store [​](#quality-guidelines-for-apps-and-themes-based-on-the-app-system-in-the-shopware-store)

> **Changelog**
>
> > 09/11/24: Quality guidelines for apps and themes based on app system.
>
> > 23/11/23: [Added - New rules for Checklist for app testing](#every-app-based-on-the-app-system)
>
> > 27/09/23: [Added - Identical name rule](#every-app-based-on-the-app-system)
>
> > 26/07/23: [Added - Name preset according to new naming scheme](#every-app-based-on-the-app-system)

## The way we test apps and themes based on the app system [​](#the-way-we-test-apps-and-themes-based-on-the-app-system)

It is always a good idea to review our test process before submitting your app for review. This ensures the quickest way for your app to be published.

We perform the *first test*, and if successful, we do the *follow-up test* again with the most current Shopware version.

The app is tested with the latest official Shopware 6 CE Version.

INFO

We always test with the [actual SW6 version](https://www.shopware.com/de/download/#shopware-6). So set it to the actual SW6 version e.g., shopware/testenv:6.6.6. Always test with the app`s highest supported Shopware version.

[Test your app for the Shopware Store (DE):](https://www.youtube.com/watch?v=gLb5CmOdi4g) and EN version is coming soon.

**Progressive Web App:** If your app is PWA compatible and you would like the PWA flag, please contact us at [alliances@shopware.com](mailto:alliances@shopware.com).

## Checklist for app testing [​](#checklist-for-app-testing)

Could you be sure to use the most recent testing checklist from Shopware and not any other provider? Please pay attention to every point in this guide. We'll review it before you release your app.

### Every app and theme based on the app system [​](#every-app-and-theme-based-on-the-app-system)

* We pay attention to the automatic code review and look for security issues and shopware coding standards in the manual code review.
* We check the complete functionality of the app (separately sales channel configurations in the config.xml, the uninstallation and reinstallation procedure) and check for styling errors on every viewport.

[Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/extensions?category=account-en/extension-partner#how-can-i-request-a-preview)

INFO

**Safe your app idea and get a preview in the store** If you already have an idea and don't want it to be snatched away, ensure you get it by creating a preview in your account. You can apply for this if you have maintained placeholder images for the store, meaningful use cases, highlight features, a description, and a release month without uploading any binary.

## App / Theme store description [​](#app-theme-store-description)

The release to the English store is standard. As an app / theme will be released in both stores (German and International), the content must accurately translate 1:1 from English to German.

* The mandatory number of characters is set in short and long descriptions. No blank spaces as fillers are allowed (EN/DE).
* Check if the description makes sense and describe the use cases of your app.
* Check if your configuration manual includes step-by-step instructions on how to configure and use your app.
* Check if you have included enough screenshots showing the app in action in the Storefront and administration.
* Check if the display name does not contain the terms "plugin" or "shopware".
* Check if all images for the English store description contain the English language. **Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.**
* Check if you explained the setup of the app / theme and added a configuration manual.

### Display Name [​](#display-name)

According to the new naming scheme, extensions may no longer display the words "plugin" and "shopware" in their names. An extension with a name that directly reflects its functional purpose is permissible, even if it shares the same name as another extension.

Also, the store-display name had to be used for `theme.json` or `manifest.xml`.

### Short description [​](#short-description)

(Min. 150 — max. 185 characters)—The app's short description must be unique and at least 150 characters long. Use the short description wisely, as the text will tease your app in the overview along with the "Customers also bought" and "Customers also viewed" recommendations. The short description is also published as a meta-description.

### Description [​](#description)

(Min. 200 characters)—The app / theme description must be at least 200 characters long and describe the app's/theme's functions in detail.

* Inline styles will be stripped. The following HTML tags are allowed:

markdown

```shiki
<a> <p> <br> <b> <strong> <i> <ul> <ol> <li> <h2> <h3> <h4> <h5>
```

* **Tips:**

  + When it comes to increasing your app / theme sales, it is important that potential customers feel completely informed about your products and services. To this end, you should provide description, highlights, and features that are meaningful, detailed, and easy to understand, even for people with very minimal technical knowledge. Explain step-by-step how your app works and how to use it to achieve the desired result. Of course, your app description should be accompanied by clean HTML source code.
  + Video content increases awareness and trust and has proven to convert potential customers better than other content types. You can help your customers better understand your app or service with explainer videos, product demos, tutorials, etc. You can embed a maximum of 2 YouTube videos in your app description.

INFO

```
You can no longer advertise your Shopware certificates within the app description, in your app images, or in your manufacturer profile. The manufacturer/partner certificates are dynamically loaded at the end of each app description and published by us.
```

### Images [​](#images)

INFO

Screenshots and preview images in English are standard. Only full English screenshots are accepted. Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.

Include several screenshots and descriptive images from the Storefront and backend that represent the app functionality. They must show the app "in action", its configuration options, and how to use it. We recommend uploading screenshots showing the mobile and desktop-view.

Only images that represent or show the function of the extension may be used. Advertising for other extensions or services is not permitted.

[How To - Add images and icons to extensions](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to)

### Link to demoshop [​](#link-to-demoshop)

If you provide a demo shop, the link must be valid (the URL cannot contain `http:` or `https:`). Do not link to your test environments, as we will delete them automatically two weeks after they are created.

### Personal data protection information [​](#personal-data-protection-information)

If necessary, personal data protection information has to be set. If personal data of the customers (store operator and/or his customers) are processed with this extension according to Art. 28 DSGVO, the following information of the data processing company must be stored in the field "Subprocessor".

If other companies are involved in the data processing of personal data, the same information must be stored accordingly for them in the field "Further subprocessors".

### Configuration manual [​](#configuration-manual)

Explain how your app is installed and configured, how it works on a technical base, and how it can be used to achieve the desired result. Of course, your app manual should contain a setup guide and be accompanied by clean HTML source code.

### Manufacturer Profile [​](#manufacturer-profile)

Your manufacturer profile must mandatorily contain accurate English and German descriptions and a manufacturer logo. You can find the manufacturer profile in your account under Shopware Account > Extension Partner > [Extension Partner profile](https://account.shopware.com/producer/profile).

INFO

The source code's descriptions, profiles, and instructions do not allow iframes, external scripts, or tracking pixels. Custom styles may not overwrite the original Shopware styles. External sources must be included via https.

## Basic Guidelines [​](#basic-guidelines)

### Testing functionality [​](#testing-functionality)

Due to our quality assurance, we check the app's / theme's complete functionality and test it wherever it impacts the administration or storefront.

Also, every app / theme will be code-reviewed by one of our core-developer ensuring coding and security standards.

### Extension master data/license [​](#extension-master-data-license)

Please enter the valid license you set in your Shopware account. You have to identify this license in the `manifest.xml` as well.

INFO

The chosen license can't be changed after adding your app / theme to your account. If you want to change the license later, add a new app based on the app system with a new technical name and upload the extension again.

### Fallback language / Translations [​](#fallback-language-translations)

The installation is not always in English or German. Could you make sure that your app works in other languages as well? For example, if the customer has his installation in Spanish and your app is not yet available in this language, you should use the English translation as a fallback.

If your app is available in more than one language (e.g., English, Spanish, French and German), these can be defined using the option "Translations into the following languages are available" (located in the “Description & images” section of your *Account*).

We check for text snippets, `config.xml`, `manifest.xml`, or `theme.json`.

### Valid preview images for the Shopware administration [​](#valid-preview-images-for-the-shopware-administration)

Preview images: There must be a preview image available in the *Extension Manager*. You must upload a valid favicon named plugin.png (png / 112 x 112 pixels) for the app. This favicon will help you identify your app in the Extension Manager module in the administration. The favicon has to be stored under `src/Resources/config/`.

Also, provide a preview image for Themes in the *Theme Manager* and CMS elements in the *Shopping Experiences*.

### Configuration per sales channel [​](#configuration-per-sales-channel)

Apps that appear in the Storefront and use a `config.xml` must be able to be configured separately for each sales channel.

### External links with rel="noopener" [​](#external-links-with-rel-noopener)

Every external link in the administration or Storefront must be marked as *rel="noopener" AND target="\_blank"*.

### Error messages and logging [​](#error-messages-and-logging)

Error or informational messages can only be recorded in the event log of Shopware's log folder (/var/log/). You have to develop your own log service. Never write app exceptions into the Shopware default log or outside the Shopware system log folder. This ensures that the log file can never be accessed via the URL.

### Avoid 400/500 Error [​](#avoid-400-500-error)

*Avoid 500 errors at any time.* Avoid 400 errors unless they are related to an API call.

### Not allowed to extend the Extension Manager [​](#not-allowed-to-extend-the-extension-manager)

The *Extension Manager* must not be extended or overwritten.

### Extension manager [​](#extension-manager)

The Debug Console controls the app's installation, uninstallation, reinstallation, and deletion. No 400 errors or exceptions are allowed to appear. If the app requires special PHP options, it must be queried during installation. If the query is negative, a growl message must appear in the administration.

### Reloading of files not allowed [​](#reloading-of-files-not-allowed)

Apps / Themes may not load other files during and after the installation in the *Extension Manager*.

### Uncompiled JavaScript must be delivered within the binary [​](#uncompiled-javascript-must-be-delivered-within-the-binary)

Compiled JavaScript offers many benefits such as improved performance and code optimization. However, it is difficult to read and understand the compiled code. The uncompiled JavaScript code must be placed in a separate folder to ensure it remains accessible to all developers. This allows other developers to review and understand the code in its original, readable form.

Please build your `main.js` as described in our documentation and create the minified code as described in our developer documentation.

[Loading the JS files](./../../../../../guides/plugins/plugins/administration/module-component-management/add-custom-field.html#loading-the-js-files)

[Injecting into the Administration](./../../../../../guides/plugins/plugins/administration/module-component-management/add-custom-field.html#injecting-into-the-administration)

Shopware reserves the right to publish extensions with minified code after individual consideration and consultation with the developer. For this, the developer must ensure that Shopware has access to the current unminified code of the extension at all times.

### Message queue [​](#message-queue)

If the extension adds messages to the message queue, ensure they are not bigger than 262,144 bytes (256 KB). This limitation is set by common message queue workers and should not be exceeded.

### Note on Shopware technology partner contract for interfaces [​](#note-on-shopware-technology-partner-contract-for-interfaces)

You have now read the complete list of requirements for developing and releasing apps based on our app system in the Shopware Community Store.

If your app is a software app/interface with downstream costs, transaction fees, or service fees for the customer, we need to complete a technology partner agreement in order to activate your app.

If you have any questions regarding the technology partner agreement, please contact our sales team by writing an email to [alliances@shopware.com](mailto:alliances@shopware.com) or calling **+44 (0) 203 095 2445 (UK) / 00 800 746 7626 0 (worldwide) / +49 (0) 25 55 / 928 85-0 (Germany)**.

## Storefront Guidelines [​](#storefront-guidelines)

### Testing the storefront [​](#testing-the-storefront)

Test the frontend and the checkout for new errors throughout the entire Storefront using the Browser Debug Console and also pay attention to JavaScript errors.

### Links must include a title tag [​](#links-must-include-a-title-tag)

Links in the storefront and administration must include a meaningful "title tag".

### Images must include the alt-tag [​](#images-must-include-the-alt-tag)

Links in the storefront and administration must include a meaningful "alt tag" or the original alt tag from the media manager.

### Do not use `<hX>`-Tags [​](#do-not-use-hx-tags)

The utilization of `<hX>`-tags in the storefront templates, which are set to `<meta name="robots" content="index,follow">`, is not permissible, as these tags are reserved exclusively for content purposes. However, you may employ `<span class="h2">`, for instance.

### Do not use inline-css in the storefront templates [​](#do-not-use-inline-css-in-the-storefront-templates)

Use your own classes and let your CSS be compiled by the app.

[Add SCSS variables](./../../../../../guides/plugins/plugins/storefront/add-scss-variables.html#add-scss-variables)

### Prevent `!important` usage [​](#prevent-important-usage)

Please avoid using the `!important` rule whenever possible.

### New controller URLs / XHR requests [​](#new-controller-urls-xhr-requests)

We check for new XHR/Document requests in the storefront as they must be accompanied by an `X-Robots-Tag` in the header request with the directive "noindex, nofollow.". For further details, please refer to the [robots meta tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=de#xrobotstag) article.

If the app creates its own controller URLs set to "index, follow" and the URLs are accessible via the frontend, then these "app URLs" must also appear in the `sitemap.xml`. In addition, these pages must include a valid canonical tag, their own meta description, and a title tag, which can be entered individually via the administration or as a text snippet.

### Lighthouse A/B-Testing [​](#lighthouse-a-b-testing)

Could you do an A/B test with *Lighthouse Audit* to check the performance and quality of your frontend app? There should not be any drastic change in performance, accessibility values, or any new errors when activating the app.

* **Testing tool** for A/B-Testing:
  + [Google Lighthouse](https://developer.chrome.com/docs/lighthouse)

### schema.org/Rich Snippets A/B-Testing [​](#schema-org-rich-snippets-a-b-testing)

Do an A/B-Test with *Scheme.org's Structured Data Testing Tool* and *Google Rich Result Tester* to check the homepage, categories, and various product detail pages (incl. available products, unavailable products, products with no review, single review, many reviews with various ratings, out-of-stock products, products to be released in the future or any other kind of product configuration and products including ean, mpn, width, length, height, weight). Also, could you check for duplicate entries as well as any new bugs?

* **Testing tool** for A/B-Testing:
  + [Schema Markup Validator of schema.org](https://validator.schema.org/)
  + [Google Rich Result Tester] (<https://search.google.com/test/rich-results>)

### Usage of fonts from external sources [​](#usage-of-fonts-from-external-sources)

If you are using external fonts (e.g., Google fonts, Fontawesome) or external services, the app store description must contain this information.

Please be aware that you might have to edit your *data protection information*. This info could be placed as a tooltip near the font settings of the app configuration.

### Register your cookie to the Cookie Consent Manager [​](#register-your-cookie-to-the-cookie-consent-manager)

We expect every cookie set from the store URL to be optional and not technically required for running shopware. Therefore, the cookies had to be [registered in our Cookie Consent Manager](./../../../../../guides/plugins/apps/storefront/cookies-with-apps.html).

We differentiate between "Technically required", ,"Marketing" and "Comfort features". All cookies must appear (unchecked) in the cookie configuration box in the frontend.

## Administration guidelines [​](#administration-guidelines)

### Menu entries in the main menu are not allowed [​](#menu-entries-in-the-main-menu-are-not-allowed)

Menu entries in the main menu of the administration are not allowed because of the look and feel.

### Own media folder [​](#own-media-folder)

Manufacturer must create their own media folders with the right thumbnail settings or use existing ones to upload images, except for upload fields within the `config.xml`.

If you use your own media folder, keep in mind that the folder and the included data had to be removed if selected during the uninstallation.

### Shopping experiences [​](#shopping-experiences)

[Shopping worlds elements](./../../../../../concepts/commerce/content/shopping-experiences-cms.html#elements) must include an element icon. If the app is deleted, *Shopping Worlds* should work flawlessly in the frontend.

### Themes [​](#themes)

[Themes](./../../../../../guides/plugins/themes/) must include its own preview image.

### External technology/ Shopware Technology Partner (STP) apps [​](#external-technology-shopware-technology-partner-stp-apps)

Every external technology app needs to track its commission. Below is an example of implementing the tracking logic in their extensions:

// POST /shopwarepartners/reports/technology - Allows partners to send us the info based on the STP contract

json

```shiki
    {
      "identifier": "8e167662-6bbb-11eb-9439-0242ac130002",
      "reportDate": "2005-08-15T15:52:01",
      "instanceId": "alur24esfaw3ghk",
      "shopwareVersion": "6.3.1",
      "reportDataKeys": [
        {
          "customer": 3
        },
        {
          "turnover": 440
        }
      ]
    }
```

### Automatic code reviews with PhpStan and SonarQube [​](#automatic-code-reviews-with-phpstan-and-sonarqube)

Our most current code review configurations when uploading apps via the Shopware Account can be found on GitHub.

* [Code reviews for Shopware 6 on GitHub](https://github.com/shopwareLabs/store-plugin-codereview)

### Sonarcube Rules status Blocker [​](#sonarcube-rules-status-blocker)

The following statements will be blocked as of 1st Oct. 2022:  
 -die; exit; var\_dump

[Refer to the list of the already existing blockers](https://s3.eu-central-1.amazonaws.com/wiki-assets.shopware.com/1657519735/blocker.txt).

### Useful tool for app development and extension management [​](#useful-tool-for-app-development-and-extension-management)

The [`shopware-cli`](https://github.com/shopware/shopware-cli) is a useful tool for building, validating and uploading new Shopware 6 app releases to the Community Store. It also allows you to manage the store description and images of your apps efficiently.

## Automatic code review - Errors [​](#automatic-code-review-errors)

### The required manifest.xml file was not found [​](#the-required-manifest-xml-file-was-not-found)

**Cause:** Error in manifest.xml

One possible cause is that the technical app name from the Community Store or Account does not match the technical name entered in manifest.xml, or the app is incorrectly zipped. The technical app name must be stored in the first part of manifest.xml. Most of the errors are caused by the wrong technical name. For example, "Swag\MyPlugin\SwagMyPluginSW6" instead of "Swag\MyPlugin\SwagMyPlugin".

[Example of a valid manifest.xml](./../../../../../resources/references/app-reference/manifest-reference.html#manifest-reference)

### Ensure cross-domain messages are sent to the intended domain [​](#ensure-cross-domain-messages-are-sent-to-the-intended-domain)

["Cross-document messaging domains should be carefully restricted"](https://rules.sonarsource.com/javascript/RSPEC-2819)

### Class Shopware\Storefront\* not found [​](#class-shopware-storefront-not-found)

Missing requirements in the theme.json (e.g. "require": {"shopware/frontend": "\*"},)

[Shopware App Development: App Meta Information - Explanation of the properties](./../../../../../guides/plugins/plugins/plugin-base-guide.html#the-composerjson-file)

### Cookies are written safely [​](#cookies-are-written-safely)

Be sure you set cookies as secure. Remember to register your cookie to the *Cookie Consent Manager*.

### The lock file is not up to date with the latest changes in manifest.xml [​](#the-lock-file-is-not-up-to-date-with-the-latest-changes-in-manifest-xml)

You may need to get updated dependencies. Run an update to update them.

The `composer.lock` in the app archive has to be deleted.

### Remove out-commented code from your source-code [​](#remove-out-commented-code-from-your-source-code)

### Unauthorized file formats or folders detected in the app [​](#unauthorized-file-formats-or-folders-detected-in-the-app)

Remove out-commented code, unused files and folders, and all dev-files from your binary.

Here are some examples of not allowed folders and files:

* ./tests
* .DS\_Store
* .editorconfig
* .eslintrc.js
* .git
* .github
* .gitignore
* .gitkeep
* .gitlab-ci.yml
* .gitpod.Dockerfile
* .gitpod.yml
* .phar
* .php-cs-fixer.cache
* .php-cs-fixer.dist.php
* .php\_cs.cache
* .php\_cs.dist
* .prettierrc
* .stylelintrc
* .stylelintrc.js
* .sw-zip-blacklist
* .tar
* .tar.gz
* .travis.yml
* .zip
* .zipignore
* ISSUE\_TEMPLATE.md
* Makefile
* Thumbs.db
* \_\_MACOSX
* auth.json
* bitbucket-pipelines.yml
* build.sh
* composer.lock
* eslint.config.js
* grumphp.yml
* package-lock.json
* package.json
* phpdoc.dist.xml
* phpstan-baseline.neon
* phpstan.neon
* phpstan.neon.dist
* phpunit.sh
* phpunit.xml.dist
* phpunitx.xml
* psalm.xml
* rector.php
* shell.nix
* stylelint.config.js
* webpack.config.js

---

## Quality guidelines for apps in the plugin system

**Source:** https://developer.shopware.com/docs/resources/guidelines/testing/store/quality-guidelines-plugins/

# Quality Guidelines for the Plugin System in the Shopware Store [​](#quality-guidelines-for-the-plugin-system-in-the-shopware-store)

> **Changelog**
>
> > 09/10/24: Quality guidelines for apps in the plugin system.
>
> > 01/08/24: [Added - Message queue](./..//quality-guidelines-plugins/#message-queue)
>
> > 06/09/23: [Added - Rules for own composer dependencies](./../quality-guidelines-plugins/#own-composer-dependencies)
>
> > 26/07/23: [Added - Identical name rule](./../quality-guidelines-plugins/#every-app-based-on-the-plugin-system)

## The way we test apps based on the plugin system [​](#the-way-we-test-apps-based-on-the-plugin-system)

It is always a good idea to review our test process before submitting your app for review. This ensures the quickest way for your app to be published.

We perform the *first test*, and if successful, we do the *follow-up test* again with the most current Shopware version.

The app is tested with the latest official Shopware 6 CE Version.

INFO

We always test with the [actual SW6 version](https://www.shopware.com/de/download/#shopware-6). So set it to the actual SW6 version e.g., shopware/testenv:6.6.6. Always test with the app`s highest supported Shopware version.

Link: [Test your app for the Shopware Store (DE):](https://www.youtube.com/watch?v=gLb5CmOdi4g) and EN version is coming soon.

**Progressive Web App:** If your app is PWA compatible and you would like the PWA flag, please contact us at [alliances@shopware.com](mailto:alliances@shopware.com).

## Checklist for app testing [​](#checklist-for-app-testing)

Could you be sure to use the most recent testing checklist from Shopware and not any other provider? Please pay attention to every point in this guide. We'll review it before you release your app.

### Every app based on the plugin system [​](#every-app-based-on-the-plugin-system)

* We pay attention to the automatic code review and look for security issues and shopware coding standards in the manual code review.
* We check the complete functionality of the app (separately sales channel configurations in the config.xml, the uninstallation and reinstallation procedure) and check for styling errors on every viewport.

Link: [Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/extensions?category=account-en/extension-partner#how-can-i-request-a-preview)

INFO

**Safe your app idea and get a preview in the store** If you already have an idea and don't want it to be snatched away, ensure you get it by creating a preview in your account. You can apply for this if you have maintained placeholder images for the store, meaningful use cases, highlight features, a description, and a release month without uploading any binary.

## App store description [​](#app-store-description)

The release to the English store is standard. As an app will be released in both stores (German and International), the content must accurately translate 1:1 from English to German.

* The mandatory number of characters is set in short and long descriptions. No blank spaces as fillers are allowed (EN/DE).
* Check if the description makes sense and describe the use cases of your app.
* Check if your configuration manual includes step-by-step instructions on how to configure and use your app.
* Check if you have included enough screenshots showing the app in action in the Storefront and administration.
* Check if the display name does not contain the terms "plugin" or "shopware".
* Check if all images for the English store description contain the English language. **Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.**
* Check if you explained the setup of the app and added a configuration manual.

### Display Name [​](#display-name)

According to the new naming scheme, extensions may no longer display the words "plugin" and "shopware" in their names. An extension with a name that directly reflects its functional purpose is permissible, even if it shares the same name as another extension.

Also, the store-display name had to be used for `composer.json` and `config.xml`.

### Short description [​](#short-description)

(Min. 150 — max. 185 characters)—The app's short description must be unique and at least 150 characters long. Use the short description wisely, as the text will tease your app in the overview along with the "Customers also bought" and "Customers also viewed" recommendations. The short description is also published as a meta-description.

### Description [​](#description)

(Min. 200 characters)—The app description must be at least 200 characters long and describe the app's functions in detail.

* Inline styles will be stripped. The following HTML tags are allowed:

markdown

```shiki
<a> <p> <br> <b> <strong> <i> <ul> <ol> <li> <h2> <h3> <h4> <h5>
```

* **Tips:**

  + When it comes to increasing your app sales, it is important that potential customers feel completely informed about your products and services. To this end, you should provide description, highlights, and features that are meaningful, detailed, and easy to understand, even for people with very minimal technical knowledge. Explain step-by-step how your app works and how to use it to achieve the desired result. Of course, your app description should be accompanied by clean HTML source code.
  + Video content increases awareness and trust and has proven to convert potential customers better than other content types. You can help your customers better understand your app or service with explainer videos, product demos, tutorials, etc. You can embed a maximum of 2 YouTube videos in your app description.

INFO

You can no longer advertise your Shopware certificates within the app description, in your app images, or in your manufacturer profile. The manufacturer/partner certificates are dynamically loaded at the end of each app description and published by us.

### Images [​](#images)

INFO

Screenshots and preview images in English are standard. Only full English screenshots are accepted. Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.

Include several screenshots and descriptive images from the Storefront and backend that represent the app functionality. They must show the app "in action", its configuration options, and how to use it. We recommend uploading screenshots showing the mobile and desktop-view.

Only images that represent or show the function of the extension may be used. Advertising for other extensions or services is not permitted.

Link: [How To - Add images and icons to extensions](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to)

### Link to demoshop [​](#link-to-demoshop)

If you provide a demo shop, the link must be valid (the URL cannot contain `http:` or `https:`). Do not link to your test environments, as we will delete them automatically two weeks after they are created.

### Personal data protection information [​](#personal-data-protection-information)

If necessary, personal data protection information has to be set. If personal data of the customers (store operator and/or his customers) are processed with this extension according to Art. 28 DSGVO, the following information of the data processing company must be stored in the field "Subprocessor".

If other companies are involved in the data processing of personal data, the same information must be stored accordingly for them in the field "Further subprocessors".

### Configuration manual [​](#configuration-manual)

Explain how your app is installed and configured, how it works on a technical base, and how it can be used to achieve the desired result. Of course, your app manual should contain a setup guide and be accompanied by clean HTML source code.

### Manufacturer Profile [​](#manufacturer-profile)

Your manufacturer profile must mandatorily contain accurate English and German descriptions and a manufacturer logo. You can find the manufacturer profile in your account under Shopware Account > Extension Partner > [Extension Partner profile](https://account.shopware.com/producer/profile).

INFO

The source code's descriptions, profiles, and instructions do not allow iframes, external scripts, or tracking pixels. Custom styles may not overwrite the original Shopware styles. External sources must be included via https.

## Basic Guidelines [​](#basic-guidelines)

### Testing functionality [​](#testing-functionality)

Due to our quality assurance, we check the app's complete functionality and test it wherever it impacts the administration or storefront.

Also, every app will be code-reviewed by one of our core-developer ensuring coding and security standards.

### Extension master data/license [​](#extension-master-data-license)

Please enter the valid license you set in your Shopware account. You have to identify this license in the `composer.json` as well.

INFO

The chosen license can't be changed after adding your app to your account. If you want to change the license later, add a new app based on the app system with a new technical name and upload the extension again.

### Fallback language / Translations [​](#fallback-language-translations)

The installation is not always in English or German. Could you make sure that your app works in other languages as well? For example, if the customer has his installation in Spanish and your app is not yet available in this language, you should use the English translation as a fallback.

If your app is available in more than one language (e.g., English, Spanish, French and German), these can be defined using the option "Translations into the following languages are available" (located in the "Description & images" section of your *Account*).

We check for text snippets, `config.xml`, and `composer.json`.

### Valid preview images for the Shopware administration [​](#valid-preview-images-for-the-shopware-administration)

Preview images: There must be a preview image available in the *Extension Manager*. You must upload a valid favicon named plugin.png (png / 112 x 112 pixels) for the app. This favicon will help you identify your app in the Extension Manager module in the administration. The favicon has to be stored under `src/Resources/config/`.

Also, provide a preview image for Themes in the *Theme Manager* and CMS elements in the *Shopping Experiences*.

### Configuration per sales channel [​](#configuration-per-sales-channel)

Apps that appear in the Storefront and use a `config.xml` must be able to be configured separately for each sales channel.

### External links with rel="noopener" [​](#external-links-with-rel-noopener)

Every external link in the administration or Storefront must be marked as *rel="noopener" AND target="\_blank"*.

### Error messages and logging [​](#error-messages-and-logging)

Error or informational messages can only be recorded in the event log of Shopware's log folder (/var/log/). You have to develop your own log service. Never write app exceptions into the Shopware default log or outside the Shopware system log folder. This ensures that the log file can never be accessed via the URL.

For payment apps, we check if the "plugin logger" service is used for the debug/error.log and that logs are written in the directory /var/log/. Log files must be used in every circumstance.

The log file had to be named like this: "MyExtension-Year-Month-Day.log"

Another solution is to store them in the database. Try to avoid using your own log tables. Otherwise, you have to implement a scheduled task that regularly empties your log table within the given time of max. 6 months.

### Avoid 400/500 Error [​](#avoid-400-500-error)

*Avoid 500 errors at any time.* Avoid 400 errors unless they are related to an API call.

### With "Install/Uninstall" the user must decide whether the data/table is to be deleted or not [​](#with-install-uninstall-the-user-must-decide-whether-the-data-table-is-to-be-deleted-or-not)

When clicking on the "Install / Uninstall" option in the Extension Manager, the user must be presented with the options "completely delete" or "keep the app data, text snippets, media folder including own media and table adjustments". You can check this using the Adminer-App from *Friends of Shopware* in your provided test-environment.

### Not allowed to extend the Extension Manager [​](#not-allowed-to-extend-the-extension-manager)

The *Extension Manager* must not be extended or overwritten.

### Own composer dependencies [​](#own-composer-dependencies)

Composer dependencies are possible if they are in the `composer.json`. With `executeComposerCommands() === true` in the plugin base class, we provide a dynamic installation of the composer dependencies by default, so they don't have to be included. Everything that is delivered in code should be traceable either directly or via `composer.json`.

[Developer documentation article to add private dependency](./../../../../../guides/plugins/plugins/plugin-fundamentals/using-composer-dependencies.html)

### Extension manager [​](#extension-manager)

The Debug Console controls the app's installation, uninstallation, reinstallation, and deletion. No 400 errors or exceptions are allowed to appear. If the app requires special PHP options, it must be queried during installation. If the query is negative, a growl message must appear in the administration.

### Reloading of files not allowed [​](#reloading-of-files-not-allowed)

Apps may not load other files during and after the installation in the *Extension Manager*.

### Uncompiled JavaScript must be delivered within the binary [​](#uncompiled-javascript-must-be-delivered-within-the-binary)

Compiled JavaScript offers many benefits such as improved performance and code optimization. However, it is difficult to read and understand the compiled code. The uncompiled JavaScript code must be placed in a separate folder to ensure it remains accessible to all developers. This allows other developers to review and understand the code in its original, readable form.

Please build your `main.js` as described in our documentation and create the minified code as described in our developer documentation.

[Loading the JS files](./../../../../../guides/plugins/plugins/administration/module-component-management/add-custom-field.html#loading-the-js-files)

[Injecting into the Administration](./../../../../../guides/plugins/plugins/administration/module-component-management/add-custom-field.html#injecting-into-the-administration)

Shopware reserves the right to publish extensions with minified code after individual consideration and consultation with the developer. For this, the developer must ensure that Shopware has access to the current unminified code of the extension at all times.

### Message queue [​](#message-queue)

If the extension adds messages to the message queue, ensure they are not bigger than 262,144 bytes (256 KB). This limitation is set by common message queue workers and should not be exceeded.

### Note on Shopware technology partner contract for interfaces [​](#note-on-shopware-technology-partner-contract-for-interfaces)

You have now read the complete list of requirements for developing and releasing apps based on our app system in the Shopware Community Store.

If your app is a software app/interface with downstream costs, transaction fees, or service fees for the customer, we need to complete a technology partner agreement in order to activate your app.

If you have any questions regarding the technology partner agreement, please contact our sales team by writing an email to [alliances@shopware.com](mailto:alliances@shopware.com) or calling **+44 (0) 203 095 2445 (UK) / 00 800 746 7626 0 (worldwide) / +49 (0) 25 55 / 928 85-0 (Germany)**.

## Storefront Guidelines [​](#storefront-guidelines)

### Testing the storefront [​](#testing-the-storefront)

Test the frontend and the checkout for new errors throughout the entire Storefront using the Browser Debug Console and also pay attention to JavaScript errors.

### Links must include a title tag [​](#links-must-include-a-title-tag)

Links in the storefront and administration must include a meaningful "title tag".

### Images must include the alt-tag [​](#images-must-include-the-alt-tag)

Links in the storefront and administration must include a meaningful "alt tag" or the original alt tag from the media manager.

### Do not use `<hX>`-Tags [​](#do-not-use-hx-tags)

The utilization of `<hX>`-tags in the storefront templates, which are set to `<meta name="robots" content="index,follow">`, is not permissible, as these tags are reserved exclusively for content purposes. However, you may employ `<span class="h2">`, for instance.

### Do not use inline-css in the storefront templates [​](#do-not-use-inline-css-in-the-storefront-templates)

Use your own classes and let your CSS be compiled by the plugin.

[Add SCSS variables](./../../../../../guides/plugins/plugins/storefront/add-scss-variables.html#add-scss-variables)

### Prevent `!important` usage [​](#prevent-important-usage)

Please avoid using the `!important` rule whenever possible.

[Add SCSS variables](./../../../../../guides/plugins/plugins/storefront/add-scss-variables.html#add-scss-variables)

### New controller URLs / XHR requests [​](#new-controller-urls-xhr-requests)

We check for new XHR/Document requests in the storefront as they must be accompanied by an `X-Robots-Tag` in the header request with the directive "noindex, nofollow.". For further details, please refer to the [robots meta tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=de#xrobotstag) article.

If the app creates its own controller URLs set to "index, follow" and the URLs are accessible via the frontend, then these "app URLs" must also appear in the `sitemap.xml`. In addition, these pages must include a valid canonical tag, their own meta description, and a title tag, which can be entered individually via the administration or as a text snippet.

### Lighthouse A/B-Testing [​](#lighthouse-a-b-testing)

Could you do an A/B test with *Lighthouse Audit* to check the performance and quality of your frontend app? There should not be any drastic change in performance, accessibility values, or any new errors when activating the app.

* **Testing tool** for A/B-Testing:
  + Link: [Google Lighthouse](https://developer.chrome.com/docs/lighthouse)

### schema.org/Rich Snippets A/B-Testing [​](#schema-org-rich-snippets-a-b-testing)

Do an A/B-Test with *Scheme.org's Structured Data Testing Tool* and *Google Rich Result Tester* to check the homepage, categories, and various product detail pages (incl. available products, unavailable products, products with no review, single review, many reviews with various ratings, out-of-stock products, products to be released in the future or any other kind of product configuration and products including ean, mpn, width, length, height, weight). Also, could you check for duplicate entries as well as any new bugs?

* **Testing tool** for A/B-Testing:
  + Link: [Schema Markup Validator of schema.org](https://validator.schema.org/)
  + Link: [Google Rich Result Tester](https://search.google.com/test/rich-results)

### Usage of fonts from external sources [​](#usage-of-fonts-from-external-sources)

If you are using external fonts (e.g., Google fonts, Fontawesome) or external services, the app store description must contain this information.

Please be aware that you might have to edit your *data protection information*. This info could be placed as a tooltip near the font settings of the app configuration.

### Register your cookie to the Cookie Consent Manager [​](#register-your-cookie-to-the-cookie-consent-manager)

We expect every cookie set from the store URL to be optional and not technically required for running shopware. Therefore, the cookies had to be [registered in our Cookie Consent Manager](./../../../../../guides/plugins/plugins/storefront/add-cookie-to-manager.html).

We differentiate between "Technically required", "Marketing" and "Comfort features". All cookies must appear (unchecked) in the cookie configuration box in the frontend.

## Administration guidelines [​](#administration-guidelines)

### Menu entries in the main menu are not allowed [​](#menu-entries-in-the-main-menu-are-not-allowed)

Menu entries in the main menu of the administration are not allowed because of the look and feel.

### Own media folder [​](#own-media-folder)

Manufacturer must create their own media folders with the right thumbnail settings or use existing ones to upload images, except for upload fields within the `config.xml`.

If you use your own media folder, keep in mind that the folder and the included data had to be removed if selected during the uninstallation.

### API test button [​](#api-test-button)

* If your API corresponds via API credentials to external services, we expect an API test button. Apart from that, you can validate the required credentials while saving them in the app settings. In this case, a status message must be displayed in the administration and Shopware log. If the API data is incorrect, an entry must appear in the event log file in the Shopware folder `/var/log/` respectively in the database.
* **Example** for implementing an API Test Button into the System Config form:

  + Link: [GitHub](https://github.com/shyim/ShyimApiTest)

### Shopping experiences [​](#shopping-experiences)

[Shopping worlds elements](./../../../../../concepts/commerce/content/shopping-experiences-cms.html#elements) must include an element icon. If the app is deleted, *Shopping Worlds* should work flawlessly in the frontend.

### Themes [​](#themes)

[Themes](./../../../../../guides/plugins/themes/) must include its own preview image.

### External technology/ Shopware Technology Partner (STP) apps [​](#external-technology-shopware-technology-partner-stp-apps)

Every external technology app needs to track its commission. Below is an example of implementing the tracking logic in their extensions:

// POST /shopwarepartners/reports/technology - Allows partners to send us the info based on the STP contract

json

```shiki
    {
      "identifier": "8e167662-6bbb-11eb-9439-0242ac130002",
      "reportDate": "2005-08-15T15:52:01",
      "instanceId": "alur24esfaw3ghk",
      "shopwareVersion": "6.3.1",
      "reportDataKeys": [
        {
          "customer": 3
        },
        {
          "turnover": 440
        }
      ]
    }
```

### Automatic code reviews with PhpStan and SonarQube [​](#automatic-code-reviews-with-phpstan-and-sonarqube)

Our most current code review configurations when uploading apps via the Shopware Account can be found on GitHub.

* Link: [Code reviews for Shopware 6 on GitHub](https://github.com/shopwareLabs/store-plugin-codereview)

### Sonarcube Rules status Blocker [​](#sonarcube-rules-status-blocker)

The following statements will be blocked as of 1st Oct. 2022:  
 -die; exit; var\_dump

* Link: [Refer to the list of the already existing blockers](https://s3.eu-central-1.amazonaws.com/wiki-assets.shopware.com/1657519735/blocker.txt).

### Automated code tests with Cypress [​](#automated-code-tests-with-cypress)

There are Cypress tests for Shopware 6 on GitHub. The project is driven by the *Friends of Shopware* group. You can contribute at any time:

* Link: [Developer Documentation Cypress Tests for Shopware 6](./../../../../../guides/plugins/plugins/testing/end-to-end-testing/)
* Link: [Cypress Tests for Shopware 6](https://github.com/shopware/shopware/tree/trunk/src/Administration/Resources)

### Useful tool for plugin development and extension management [​](#useful-tool-for-plugin-development-and-extension-management)

The [`shopware-cli`](https://github.com/shopware/shopware-cli) is a useful tool for building, validating and uploading new Shopware 6 plugin releases to the Community Store. It also allows you to manage the store description and images of your plugins efficiently.

## Automatic code review - Errors [​](#automatic-code-review-errors)

### The required composer.json file was not found [​](#the-required-composer-json-file-was-not-found)

**Cause:** Error in composer.json

One possible cause is that the technical app name from the Community Store or Account does not match the technical name entered in composer.json, or the app is incorrectly zipped. The technical app name must be stored in the composer.json, located at `composer.json` > extra > `shopware-plugin-class`. Could you take a look at the bootstrap class? Most of the errors are caused by the wrong technical name. For example, "Swag\MyPlugin\SwagMyPluginSW6" instead of "Swag\MyPlugin\SwagMyPlugin".

Link: [Example of a valid composer.json](https://github.com/FriendsOfShopware/FroshPlatformPerformance/blob/master/composer.json#L20).

### Ensure cross-domain messages are sent to the intended domain [​](#ensure-cross-domain-messages-are-sent-to-the-intended-domain)

Link: ["Cross-document messaging domains should be carefully restricted"](https://rules.sonarsource.com/javascript/RSPEC-2819)

### No bootstrapping file found. Expecting bootstrapping in [​](#no-bootstrapping-file-found-expecting-bootstrapping-in)

The bootstrap cannot be found. The reasons could be that the folder structure in the ZIP file needs to be corrected, a typo, or a case-sensitive error in the app source (e.g., in the technical name).

### Class Shopware\Storefront\* not found [​](#class-shopware-storefront-not-found)

Missing requirements in the composer.json (e.g. "require": {"shopware/frontend": "\*"},)

Link: "[Shopware App Development: App Meta Information - Explanation of the properties](./../../../../../guides/plugins/plugins/plugin-base-guide.html#the-composerjson-file)

### Cookies are written safely [​](#cookies-are-written-safely)

Be sure you set cookies as secure. Remember to register your cookie to the *Cookie Consent Manager*.

### Call to static method jsonEncode() on an unknown class [​](#call-to-static-method-jsonencode-on-an-unknown-class)

Shopware always uses json\_Encode exclusively - there is no other fallback.

### The lock file is not up to date with the latest changes in composer.json [​](#the-lock-file-is-not-up-to-date-with-the-latest-changes-in-composer-json)

You may need to get updated dependencies. Run an update to update them.

The `composer.lock` in the app archive has to be deleted.

### Class Shopware\Core\System\Snippet\Files\SnippetFileInterface not found and could not be autoloaded [​](#class-shopware-core-system-snippet-files-snippetfileinterface-not-found-and-could-not-be-autoloaded)

In the Shopware 6 Early Access (EA) version, the mentioned class did not exist. Therefore, the code review failed. The reason for the problem is the following specification in the composer.json:

xml

```shiki
<pre>"require": {

    "shopware/core": "*",

    "shopware/storefront": "*"

},</pre>
```

The Composer resolves this to "Whatever is the latest from these repositories" and then installs the Early Access version instead of the current Release Candidate. This happens because the Composer does not know an EA as a stability level (like stable or RC) and is, therefore, ultimately considered "stable". The solution is to amend the requirement as follows:

xml

```shiki
<pre>"require": {

    "shopware/core": "~6.1.0",

    "shopware/storefront": "~6.1.0"

},

"minimum-stability": "RC"</pre>
```

This ensures that at least version Shopware 6.1 is installed, even if it is a Release Candidate. It will be preferred as soon as the final 6.1 is released.

### Remove out-commented code from your source-code [​](#remove-out-commented-code-from-your-source-code)

### Unauthorized file formats or folders detected in the app [​](#unauthorized-file-formats-or-folders-detected-in-the-app)

Remove out-commented code, unused files and folders, and all dev-files from your binary.

Here are some examples of not allowed folders and files:

* ./tests
* .DS\_Store
* .editorconfig
* .eslintrc.js
* .git
* .github
* .gitignore
* .gitkeep
* .gitlab-ci.yml
* .gitpod.Dockerfile
* .gitpod.yml
* .phar
* .php-cs-fixer.cache
* .php-cs-fixer.dist.php
* .php\_cs.cache
* .php\_cs.dist
* .prettierrc
* .stylelintrc
* .stylelintrc.js
* .sw-zip-blacklist
* .tar
* .tar.gz
* .travis.yml
* .zip
* .zipignore
* ISSUE\_TEMPLATE.md
* Makefile
* Thumbs.db
* \_\_MACOSX
* auth.json
* bitbucket-pipelines.yml
* build.sh
* composer.lock
* eslint.config.js
* grumphp.yml
* package-lock.json
* package.json
* phpdoc.dist.xml
* phpstan-baseline.neon
* phpstan.neon
* phpstan.neon.dist
* phpunit.sh
* phpunit.xml.dist
* phpunitx.xml
* psalm.xml
* rector.php
* shell.nix
* stylelint.config.js
* webpack.config.js

---

## Storefront Accessibility

**Source:** https://developer.shopware.com/docs/resources/accessibility/storefront-accessibility.html

# Accessibility in the Storefront [​](#accessibility-in-the-storefront)

At Shopware, we are committed to creating inclusive and barrier-free shopping experiences for our merchants and their customers.

## What shopware does to ensure accessibility? [​](#what-shopware-does-to-ensure-accessibility)

* Shopware is committed to fulfill the [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) accessibility guidelines and Barrier-Free Information Technology Regulation (BITV 2.0) in the Storefront.
  + You can find more information on [shopware.design](https://shopware.design/foundations/accessibility.html) and [in our blog post](https://www.shopware.com/en/news/accessible-online-store-by-2025/).
* The Storefront is using [Bootstrap components](https://getbootstrap.com/docs/5.3/getting-started/accessibility/) that already consider good accessibility practices, for example, using aria roles.
* Much of the HTML structure and CSS styling already fulfill accessibility guidelines. However, there are still [open accessibility issues](#Overview-of-known-accessibility-issues) that will be addressed.
* Automated [E2E testing with playwright](https://github.com/shopware/shopware/tree/trunk/tests/acceptance) and axe reporter are used to ensure future accessibility.

## How are core accessibility improvements released? [​](#how-are-core-accessibility-improvements-released)

Starting from **Shopware 6.6+,** accessibility improvements have been introduced, and **6.7+** includes further enhancements. Accessibility improvements are rolled out in regular minor releases, similar to other improvements or bug-fixes. There is no large "accessibility release" planned that ships all accessibility improvements at once.

## How to deal with breaking accessibility changes? [​](#how-to-deal-with-breaking-accessibility-changes)

Ensuring an accessible shop page can require changes in the HTML/Twig structure or the CSS. This can cause unintended behavior for an extension that is modifying an area that is being changed to improve accessibility.

Because of this, breaking accessibility changes are not enabled by default. All accessibility changes that include breaking changes are implemented behind a feature flag:

env

```shiki
ACCESSIBILITY_TWEAKS=1
```

However, breaking accessibility changes are still released regularly inside minor releases. They are just not active by default to not cause a breaking change.

The feature flag `ACCESSIBILITY_TWEAKS` can be activated inside your `.env`, similar to the major feature flags like `V6_7_0_0`. When the feature flag is enabled, all available accessibility improvements are activated. This allows you to check if your project or extension is effected by the change and already prepare an adaptation to the change if it is necessary.

WARNING

With the major version v6.7.0 all accessibility improvements will become the default.

### Example of a breaking accessibility change [​](#example-of-a-breaking-accessibility-change)

Let's say, for example, that a list is not using a proper markup, and it is changed to improve accessibility.

This is what a suboptimal HTML structure could look like:

twig

```shiki
<div class="sidebar-list">
    {% block component_list_items %}
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
    {% endblock %}
</div>
```

Let's assume it should be changed to a proper list. Instead of implementing this right away, it is implemented behind the `ACCESSIBILITY_TWEAKS` flag, including instructions how it should be changed:

twig

```shiki
{# @deprecated tag:v6.7.0 - The list will be changed to `<ul>` and `<li>` to improve accessibility #}
{% if feature('ACCESSIBILITY_TWEAKS') %}
    <ul class="sidebar-list">
        {% block component_list_items_inner %}
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
        {% endblock %}
    </ul>
{% else %}
    <div class="sidebar-list">
        {# @deprecated tag:v6.7.0 - Use `component_list_items_inner` instead with `<li>` #}
        {% block component_list_items %}
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
        {% endblock %}
    </div>
{% endif %}
```

If the block `component_list_items` is being extended, the new accessibility change can already be considered. If the change was rolled out without a feature flag, the extension still assumes a `<div class="list-item">` which would likely result in incorrect HTML:

twig

```shiki
{% sw_extends '@Storefront/storefront/component/list.html.twig' %}

{# Consider the new structure already #}
{% block component_list_items_inner %}
    {{ parent() }}
    <li class="list-item"><a href="#">My item</a></li>
{% endblock %}

{# This can be removed after v6.7.0 #}
{% block component_list_items %}
    {{ parent() }}
    <div class="list-item"><a href="#">My item</a></div>
{% endblock %}
```

## Overview of accessibility issues for iteration 1 [​](#overview-of-accessibility-issues-for-iteration-1)

INFO

With accessibility iteration 1 we have addressed the most critical accessibility problems and implemented multiple improvements.

### Continuous efforts to ensure accessibility [​](#continuous-efforts-to-ensure-accessibility)

We are continuously testing our core Storefront to meet accessibility requirements. This includes screen reader usage, keyboard-operation or color contrast analyzes. We are using the [WCAG 2.1 Level AA](https://www.w3.org/TR/WCAG21/) standard and do our best to solve all issues to meet the WCAG 2.1 requirements.

### Overview of released accessibility improvements [​](#overview-of-released-accessibility-improvements)

* Below, you find a list of recent accessibility improvements. The list includes a changelog and the release versions for each improvement.
* Enable the feature flag `ACCESSIBILITY_TWEAKS` to activate all breaking accessibility changes.

| Topic | Breaking changes | Changelog | Release versions |
| --- | --- | --- | --- |
| Missing semantic markup of form address headings | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-registration-form-fieldset-improvement.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Product image zoom modal keyboard accessibility | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-08-improve-image-zoom-modal-accessibility.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Focused slides in the carousel are not being moved into the visible area | Yes | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-improve-slider-element-accessibility.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Focus jumps to the top of the page after closing a modal | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-01-add-focus-handling-to-storefront.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Ensure that resizing content up to 200% does not cause breaks | Yes | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-Improved-storefront-text-scaling.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Language of each Storefront passage or phrase in the content can be programmatically determined | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-add-language-to-reviews.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Check Lighthouse Accessibility Score | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-21-fix-scroll-up-button-accessibility.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Pagination does not have links | Yes | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2023-08-31-pagination-with-links.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0) |
| Non-informative document title | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.1.0/changelog/release-6-6-1-0/2024-03-12-distinctive-document-titles.md) | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.1.0) |
| The form element quantity selector is not labeled | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.5.0/changelog/release-6-6-5-0/2024-07-15-the-form-element-quantity-selector-is-not-labeled.md) | [v6.6.5.0](https://github.com/shopware/shopware/releases/tag/v6.6.5.0) |
| Slider reports confusing status changes to screen readers | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.4.0/changelog/release-6-6-4-0/2024-05-31-remove-unwanted-aria-live-attributes-from-sliders.md) | [v6.6.4.0](https://github.com/shopware/shopware/releases/tag/v6.6.4.0) |
| The user needs to be able to close triggered, additional content | No | [Changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-6-3-0/2024-05-03-esc-key-for-nav-flyout-close.md) | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0) |
| Improve "Remove Product" button labeling in checkout | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md) | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0) |
| Missing alternative text for product images in the shopping cart | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md) | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0) |
| A closing mechanism for the navigation | No | [Changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-6-3-0/2024-05-03-esc-key-for-nav-flyout-close.md) | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0) |
| Change shipping toggle in OffCanvas cart to button element | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.2.0/changelog/release-6-6-2-0/2024-04-17-change-shipping-costs-toggle-to-button-element.md) | [v6.6.2.0](https://github.com/shopware/shopware/releases/tag/v6.6.2.0) |
| Add heading elements for account login page | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.2.0/changelog/release-6-6-2-0/2024-04-15-heading-elements-on-registration-page.md) | [v6.6.2.0](https://github.com/shopware/shopware/releases/tag/v6.6.2.0) |
| Provide distinctive document titles for each page | No | [Changelog](https://github.com/shopware/shopware/blob/v6.6.1.0/changelog/release-6-6-1-0/2024-03-12-distinctive-document-titles.md) | [v6.6.1.0](https://github.com/shopware/shopware/releases/tag/v6.6.1.0) |
| No empty nav element in top-bar | Yes | [Changelog](https://github.com/shopware/shopware/blob/v6.6.1.0/changelog/release-6-6-1-0/2023-03-05-no-empty-nav.md) | [v6.6.1.0](https://github.com/shopware/shopware/releases/tag/v6.6.1.0) |
| Update the focus states so that they are clearly visible | No | [Multiple changes](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26712&type=commits) | [Multiple releases](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26712&type=code) |
| Increase compatibility of Storefront with future assistance technologies | No | [Multiple changes](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26717&type=commits) | [Multiple releases](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26717&type=code) |
| Content functionality operable through keyboard | Yes | [Multiple changes](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26705&type=commits) | [Multiple releases](https://github.com/search?q=repo%3Ashopware%2Fshopware+NEXT-26705&type=code) |
| No keyboard traps should occur in the Storefront | - | Verification work without released code changes | - |
| Mechanism for the user to pause, stop, or hide moving content | - | Verification work without released code changes | - |
| Add text to components that only work with icons to identify their purpose | - | - |  |
| Check if all non-text content has text alternative and provide if necessary | - | - |  |
| Provide error correction suggestions | - | - |  |
| Text styles needs to be adjusted (line height, paragraph spacing) | - | - |  |
| Keyboard/Tabs should work for nav main-navigation-menu | - | - |  |

### Overview of known accessibility issues [​](#overview-of-known-accessibility-issues)

To report any new accessibility issues, click the New Issue button, select Bug Report, fill out the require fields and make sure to add the area/accessibility label. Here is a reference to the existing [accessibility Issues](https://github.com/shopware/shopware/issues?q=state%3Aopen%20label%3Aarea%2Faccessibility).

## Best practices for accessibility (a11y) in Shopware extensions [​](#best-practices-for-accessibility-a11y-in-shopware-extensions)

Ensuring accessibility in your Shopware extension improves **usability, inclusivity, and compliance** with standards like **WCAG 2.1** and the **EU Web Accessibility Directive**. Below are best practices to help you build accessible extensions and themes.

### 1. Setting up for accessibility testing [​](#_1-setting-up-for-accessibility-testing)

#### Activate the accessibility feature flag [​](#activate-the-accessibility-feature-flag)

Enable the **feature flag** to test changes before release by activating the feature flag in your local environment, modify your `project-root/.env`.

env

```shiki
ACCESSIBILITY_TWEAKS=1
```

Once enabled, the `ACCESSIBILITY_TWEAKS` feature flag, a re-compilation of the theme is needed to enable all styling improvements like adjusted font-sizes.

text

```shiki
bin/console theme:compile
```

Now you can:

* Preview upcoming a11y improvements before they become mandatory.
* Identify potential breaking changes in your theme or extension.
* Ensure your UI remains functional with new [accessibility enhancements](./accessibility-checklist.html).

### 2. Testing for accessibility compliance [​](#_2-testing-for-accessibility-compliance)

#### Automated testing tools [​](#automated-testing-tools)

Use automated tools to **detect common accessibility issues** in your extension:

* **[Google Lighthouse](https://developer.shopware.com/docs/resources/guidelines/testing/store/quality-guidelines-apps/#lighthouse-a-b-testing)** – Run audits in Chrome DevTools.
* **AXE DevTools** – More detailed accessibility testing.
* **WAVE (WebAIM Tool)** – Identifies HTML structure and ARIA misuses.

#### Manual Testing [​](#manual-testing)

While automation helps, **manual checks** ensure real-world usability:

✔ **Keyboard Navigation** – Ensure users can navigate your store using `Tab`, `Enter`, and `Esc`. ✔ **Screen Readers** – Test with **NVDA (Windows)** or **VoiceOver (Mac/iOS)**. ✔ **Color Contrast Checks** – Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to verify readability.

### 3. Validating accessibility in extensions [​](#_3-validating-accessibility-in-extensions)

#### Common a11y issues to fix before release [​](#common-a11y-issues-to-fix-before-release)

* Misuse of **HTML & ARIA roles** (Ensure correct semantic structure).
* Missing **form labels & alt text** for images/icons.
* Improper **focus management** in modals, dropdowns, and popups.
* **Dynamic content updates** not announced to screen readers.

#### Shopware QA and self-certification [​](#shopware-qa-and-self-certification)

* Developers can **self-certify** an extension as a11y-compliant.
* Shopware **QA verification** may be required for listing in the store.

### 4. Accessibility support in Shopware versions [​](#_4-accessibility-support-in-shopware-versions)

| **Shopware version** | **Accessibility support** |
| --- | --- |
| **6.7+** | Full A11y improvements available for testing |
| **6.6+** | Accessibility features introduced (use `ACCESSIBILITY_TWEAKS` feature flag) |
| **Shopware 5** | 🚫 **No accessibility support** |

### 5. Getting help with accessibility [​](#_5-getting-help-with-accessibility)

* Work with **Shopware-certified agencies** for A11y audits.
* Stay updated with Shopware's **developer guidelines**.
* Discuss A11y best practices with other developers in the **Shopware community**.

## Conclusion [​](#conclusion)

Understanding accessibility best-practices is just the beginning. To truly create an inclusive storefront, these ideas must be translated into practice. To help you turn these into action, we have created a comprehensive [Storefront Accessibility Checklist](./accessibility-checklist.html). It outlines the key technical and design practices needed to build accessible interfaces—from semantic HTML to keyboard navigation and ARIA usage.

---

## Accessibility Checklist

**Source:** https://developer.shopware.com/docs/resources/accessibility/accessibility-checklist.html

# Storefront Accessibility [​](#storefront-accessibility)

Creating an accessible storefront ensures that all users can navigate, interact with, and benefit from your site. Accessibility is not only a best practice but a legal and ethical responsibility that contributes to a more inclusive web.

This checklist outlines the key principles and technical requirements for building accessible web interfaces, with a focus on semantic structure, keyboard usability, screen reader compatibility, and inclusive design practices.

## Storefront Accessibility Checklist: Best Practices for Inclusive Web Design [​](#storefront-accessibility-checklist-best-practices-for-inclusive-web-design)

### Use Semantic HTML [​](#use-semantic-html)

Leverage native HTML elements that communicate their purpose effectively:

* Use appropriate tags for actions: `<button>`, `<a>`, `<select>` instead of `<div>` or `<span>`.
* Structure your layout with semantic elements: `<nav>`, `<main>`, `<header>`, `<footer>`.
* Always pair `<label>` elements with form controls using `for` and `id`. Avoid relying solely on `placeholder` text for labeling.

### Set the Correct Document Language [​](#set-the-correct-document-language)

Proper language settings help screen readers use accurate pronunciation and intonation:

* Add `lang="en"` (or the appropriate language code) to the `<html>` tag.

### Ensure Accessible Forms [​](#ensure-accessible-forms)

All form fields must be clearly labeled and error states must be identifiable:

* Use `<label for="input-id">`, `aria-label`, or `aria-labelledby`.
* Provide error messages that are clear and easy to locate.
* Don’t rely solely on color (e.g., red) to indicate errors. You can use icons or text additionally.
* Use `aria-describedby` to connect input fields to help or error messages.

### Manage Focus [​](#manage-focus)

Ensure users know where they are and can move through the interface logically:

* Use `tabindex="0"` for custom interactive elements. Try to not mess around with the tabindex if possible and keep the "natural" tab flow.
* Do not remove focus outlines unless replaced with a clear visible alternative.
* Use `focus()` to direct user attention (e.g. after form errors or modal open).
* Each interactive element that can be clicked or navigated by keyboard (`<a>`, `<button>` etc.) must have a clearly visible focus indication.

### Keyboard Accessibility [​](#keyboard-accessibility)

Users should be able to navigate and interact with all features using only the keyboard:

* Ensure `Enter` and `Space` activate interactive elements.
* Avoid using `onclick` on non-focusable elements without keyboard support.
* Custom widgets must respond to arrow keys and expected keyboard patterns.

### Use ARIA Carefully [​](#use-aria-carefully)

Use ARIA roles and attributes only when native HTML doesn’t work.

* Use `role="alert"` for live error messaging.
* Apply `aria-expanded`, `aria-controls`, and `aria-hidden` for toggleable UI elements.
* Prefer native HTML elements over ARIA whenever possible to reduce complexity.

### Provide Live Region Updates [​](#provide-live-region-updates)

Ensure real-time changes are accessible:

* Use `aria-live="polite"` or `aria-live="assertive"` for real-time updates (e.g. validation messages, chat widgets).

### Manage Page Titles and Headings [​](#manage-page-titles-and-headings)

Headings and titles provide structure and orientation. It helps users understand page structure:

* Always update the `<title>` tag on page load or route change.
* Use one `<h1>` per page, followed by correct heading hierarchy (`<h2>`, `<h3>`, etc.).

### Support Skip Links [​](#support-skip-links)

Help keyboard users skip repetitive content:

* Include a skip link at the top of the page:

  html

  ```shiki
  <a href="#main-content" class="skip-link">Skip to main content</a>
  ```

### Control Focus When Using Modals or Popovers [​](#control-focus-when-using-modals-or-popovers)

Focus should remain within the modal and return to the trigger element after closing:

* Trap focus while the modal is open.
* Return focus to the initiating element once it is closed.

### Avoid Auto-Playing Audio or Video [​](#avoid-auto-playing-audio-or-video)

If unavoidable, make sure users can easily pause or stop it:

* Provide controls on `<video>` or `<audio>` elements.
* Avoid autoplay unless muted and non-disruptive.

### Ensure Unique IDs and ARIA Attributes [​](#ensure-unique-ids-and-aria-attributes)

Avoid duplicated IDs to maintain screen reader reliability:

* Validate that `id` attributes are unique.
* Ensure any referenced IDs in `aria-labelledby` or `aria-describedby` exist and are not duplicated.

### Test with Assistive Technologies [​](#test-with-assistive-technologies)

Test your site with real-world tools and scenarios:

* Use screen readers like NVDA (Windows), VoiceOver (macOS).
* Navigate with only the keyboard (Tab, Shift+Tab, Enter, Space).
* Leverage browser dev tools (Chrome DevTools > Accessibility, Axe Core).

## Conclusion [​](#conclusion)

Following this checklist will help ensure your storefront is usable by everyone, regardless of ability. It also improves SEO, performance, and user satisfaction for all visitors.

Regularly audit your code, test with assistive technologies, and stay updated with evolving accessibility standards. Inclusive design is good design.

---

