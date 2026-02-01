# Concepts Framework

*Scraped from Shopware Developer Documentation*

---

## Framework

**Source:** https://developer.shopware.com/docs/concepts/framework/

# Framework [​](#framework)

Shopware 6 is not only an ecommerce platform but also a **framework** for developing highly customized shop infrastructures. This section will introduce some of the core concepts that will help you fully understand and leverage Shopware 6's capabilities.

---

## Architecture

**Source:** https://developer.shopware.com/docs/concepts/framework/architecture/

# Architecture [​](#architecture)

On a high level, Shopware consists of multiple modules that separate the entire code base into logical units. Some modules are independent, and some depend on others.

---

## Storefront

**Source:** https://developer.shopware.com/docs/concepts/framework/architecture/storefront-concept.html

# Storefront [​](#storefront)

In this article, you will get to know the Storefront component and learn a lot of its main concepts. Along the way, you will find answers to the following questions:

* What is the Storefront component & what is its main purpose?
* What technologies are being used?
* How is the Storefront structured?
* Which parts of other Platform components are being used?
* How does the composite data handling work?
* What is the definition and main purpose of Pages, Pagelets, Controllers, and their corresponding Templates?
* How is the Storefront handling translations?

## Introduction [​](#introduction)

The Storefront component is a frontend written in PHP. It conceptually sits on top of the Core, similar to the [Administration](./administration-concept.html) component. As the Storefront can be seen as a classical PHP application, it makes use of HTML rendering, JavaScript, and a CSS preprocessor. The Storefront component uses Twig as the templating engine and SASS for styling purposes. The foundation of the Storefront template is based on the Bootstrap framework and, therefore, fully customizable.

## Main concerns [​](#main-concerns)

The main concerns that the Storefront component has are listed below. Furthermore, we are diving deeper into these in the following chapters.

* Creating Pages and Pagelets
* Mapping requests to the Core
* Rendering templates
* Provide theming

Contrary to API calls that result in single resource data, a whole page in the Storefront displays multiple different data sets on a single page. Think of partials, which lead to a single page being displayed. Imagine a page that displays the order overview in the customer account environment. There are partials that are generic and will be displayed on almost every Page. These partials include - for example, Header and Footer information wrapped into a `GenericPage` as `Pagelets` (`HeaderPagelet`, `FooterPagelet`). This very generic Page will later be enriched with the specific information you want to display through a separate loader (e.g. a list of orders).

To achieve getting information from a specific resource, the Storefront's second concern is to map requests to the Core. Internally, the Storefront makes use of the [Store API](./../../api/store-api.html) routes to enrich the Page with additional information, e.g., a list of orders, which is being fetched through the order route. Once all needed information is added to the Page, the corresponding page loader returns the Page to a Storefront controller.

Contrary to the Core, which can almost completely omit templating in favor of JSON responses, the Storefront contains a rich set of Twig templates to display a fully functional shop. Another concern of the Storefront is to provide templating with Twig. The page object, which was enriched beforehand, will later be passed to a specific Twig page template throughout a controller. A more detailed look into an example can be found in [Composite data handling](./storefront-concept.html#composite-data-handling).

Last but not least, the Storefront not only contains static templates but also includes a theming engine to modify the rendered templates or change the default layout programmatically with your own [Themes](./../../../guides/plugins/themes/) or [Plugins](./storefront-concept.html).

## Structure [​](#structure)

Let's have a look at the Storefront's general component structure. When opening this directory, you will find several sub-directories, and a vast part of the functionality of the Storefront component includes templates (`./Resources`). But besides that, there are other directories worth having a look at:

bash

```shiki
<Storefront>
|- Controller
|- DependencyInjection
|- Event
|- Framework
|- Migration
|- Page
|- Pagelet
|- Resources
|- Test
|- Theme
|- .gitignore
|- composer.json
|- phpunit.xml.dist
|- README.md
|- Storefront.php
```

Starting at the top of this list, you will find all Storefront controllers inside the `Controller` directory. As said beforehand, a page is being built inside that controller with the help of the corresponding page loaders, Pages, Pagelets, and events, which you will find in the directories: `Pages`, `Pagelets`, and their sub-directories. Each controller method will also give detailed information about its routing with the help of attributes. The directory `DependencyInjection` includes all dependencies which are used in the specific controllers, whereas the `Event` directory includes route request events, and the `Framework` directory, amongst other things, also includes the Routing, Caching, and furthermore. `Migration` and `Test` obviously include migrations and tests for the Storefront component (e.g., tests for each Storefront controller).

As the Storefront theme uses Bootstrap, the template structure inside `./Resources` is a derivative of the Bootstrap starter template. Besides using Twig as the templating engine and SASS as the CSS preprocessor, we are also using Webpack for bundling and transpiling purposes. This templating directory structure is considered the best practice. If you are interested in developing your own themes or plugins, this section will give more information.

## Composite data handling [​](#composite-data-handling)

Composite data loading describes the process of preparing and fetching data for a whole template page worth of content. As a web application, the page rendering process is a central concern of the Storefront. Contrary to solutions through `postDispatch`-Handling or `lazy loading` from templates, the controller actions of the Storefront do a full lookup and handle data loading transparently and fully. The Storefront provides a general solution for this problem - the Page System.

### Pages and Pagelets [​](#pages-and-pagelets)

The pages in the Storefront component can roughly be categorized into Pages and Pagelets. Although functionally identical, they represent different usages of Page's data. A Page is generally rendered into a full template, whereas a Pagelet is either a part of a Page or accessible through an XHR route, sometimes even both.

A single Page is always a three class namespace:

* The Page-Struct (`GenericPage`) - represents the data
* The PageLoader (`PageLoaderInterface`) - handles the creation of page structs
* The PageEvent (`NestedEvent`) - adds a clean extension point to the pages

### Example: Composition of the account order page [​](#example-composition-of-the-account-order-page)

Referring to the example described in the [main concerns chapter](./storefront-concept.html#main-concerns), have a detailed look at the composition of the Storefronts `AccountOrderPage` with Header and Footer information. The composition is handled through the page loaders themselves by triggering the loading of associated data internally. The following example will also be used for any other Page being displayed on the Storefront.

To describe how the composition of the Page works, first get to know what the result of the composition should be.

* By calling a specific route (e.g. `/account/order`), one should receive a specific page in the Storefront.
* This page consists of generic information (e.g. Header, Footer) and detailed information (e.g. a list of orders).
* Detailed information should be fetched throughout the Core component to make use of the [Store API routes](./../../api/store-api.html).

The best entry point to give you a good understanding of how the composition works is the corresponding controller. In our case, it is the `AccountOrderController`. The main and only task of the controller is to assign a page struct to a variable, which will later be passed to a Twig template. The Page is received by the specific `AccountOrderPageLoader`. Additionally, the method attributes of the controller also set routing information like path, name, options, and methods.

Speaking of the page loader (`AccountOrderPageLoader`), which returns the page (`AccountOrderPage`), you will see that we are doing the composition here. At first, a generic page is created by using the `GenericPageLoader`. As described above, this generic Page includes information, which is generic like Header, Footer, and Meta information. This information is wrapped inside our `Pagelets` and displays a specific part of the Page.

Later, the `AccountOrderPage` is created from the generic Page because we also would like to add more information to this Page. Per definition, the `AccountOrderPage` can set and get a list of orders we can receive by calling a Store API route through the `OrderRoute` of our Core component. That said, we make sure that our Storefront uses the same data as we would use by calling the API directly, which is a big advantage.

Once we have set all the necessary information to our page (`AccountOrderPage`) in our page loader (`AccountOrderPageLoader`), we are making usage of our event dispatcher to throw a `PageLoadedEvent`. For each Page, there should be a specific event, which will be thrown to ensure extensibility throughout plugins (`AccountOrderPageLoadedEvent`).

To summarize the composition of a page, have a look at this diagram:

![Composition of a Storefront page](/assets/framework-storefront-comnpositeData.-p9I9rFM.svg)

## Translations [​](#translations)

Extending or adjusting a **translation** in Shopware 6 can be done by adding your own snippets inside a plugin. Besides that, there is also a set of translations inside our default Storefront component. We have decided to save snippets as JSON files, so it is easy to structure and find snippets you want to change. However, when using pluralization and/or variables, you can expect slight differences between snippets in the Administration and the Storefront. In theory, you can place your snippets anywhere as long as you load your JSON files correctly. However, we recommend that you mirror the core structure of Shopware.

INFO

Storefront snippets can be found in `platform/src/Storefront/Resources/snippet`.

Inside that directory, you will find a specific sub-directory for each language, e.g., `de_DE` following the ISO standard. The localization is done via the exact ISO. In addition to the language, the country of destination is also supplied. By default, two Storefront translations are provided: `de_DE` and `en_GB`. There are, of course, language plugins for other locales available. Inside these JSON files, you will find a simple translation and the possibility to work with variables and pluralization, which are wrapped with the `%` character. The reference of a translated value is used inside our Twig templates by calling the Twig function `trans` and working with interpolations ( e.g. `0`).

---

## Administration

**Source:** https://developer.shopware.com/docs/concepts/framework/architecture/administration-concept.html

# Administration [​](#administration)

In this article, you will get to know the Administration component and learn a lot of its main concepts. Along the way, you will find answers to the following questions:

* What is the Administration, and what is its main purpose?
* Which technologies are being used?
* How is the Administration structured?
* How is the Administration implemented inside the Platform?
* How is the Administration connected to other components?
* Which parts of the Core are being used?
* What are Modules, Pages, and Components?
* How is the Administration handling Inheritance & ACL?

## Introduction [​](#introduction)

The Administration component is a Symfony bundle that contains a Single Page Application (SPA) written in JavaScript. It conceptually sits on top of the Core - similar to the [Storefront](./storefront-concept.html) component. The SPA itself provides a rich user interface on top of REST-API-based communication. It communicates with the Core component through the Admin API and is an headless application build on custom components written in [Vue.js](https://vuejs.org/). Similar to the frameworks being used in the Storefront component, the Administration component uses SASS for styling purposes and [Twig.js](https://github.com/twigjs/twig.js/wiki) to offer templating functionalities. By default, Shopware 6 uses the [Vue I18n plugin](https://kazupon.github.io/vue-i18n/) in the Administration to deal with translation. Furthermore, [Webpack](https://webpack.js.org/) is being used to bundle and compile the SPA.

## Main concerns [​](#main-concerns)

As mentioned previously, the Administration component provides a SPA that communicates with the Core through the [Admin API](./../../../concepts/api/admin-api.html). To summarize, its main concern is to provide a UI for all administrative tasks for a shop owner in Shopware. To be more precise, it does not contain any business logic. Therefore, there is no functional layering but a flat list of modules structured along the Core component and containing Vue.js web components. Every single communication with the Core can, e.g., be inspected throughout the network activities of your browser's developer tools.

Apart from the arguably most central responsibility of creating the UI itself, which can be reached through `/admin`. The Administration components implement a number of cross-cutting concerns. The most important are:

* **Providing inheritance**: As Shopware 6 offers a flexible extension system to develop own apps, plugins, or themes, one can override or extend the Administration to fit needs. More information can be found in the [inheritance](./administration-concept.html#inheritance) chapter of this article.
* **Data management**: The Administration displays entities of the Core component and handles the management of this data. So, of course, REST-API access is an important concern of [Pages and views](./administration-concept.html#modules-and-their-components) where necessary. You will find many components working with in-memory representations of API-Data.
* **State management**: In contrast to the Core (Backend), the Administration is a long-running process contained in the browser. Proper state management is key here. There is a router present handling the current page selection. View and component rendering is done locally in relation to their parents. Therefore, each component manages the state of its subcomponents.

## Structure [​](#structure)

The main Vue.js application is wrapped inside a Symfony bundle. You will find the specific SPA sources inside the Administration component in a specific sub-directory of `shopware/src/Administration`. Therefore, the SPA's main entry point is: `./Resources/app/administration`. Everything else inside `shopware/src/Administration` can be seen as a wrapped configuration around the SPA. This bundle's main concern is to set up the initial Routing (`/admin`) and the Administration's main template file, which initializes the SPA (`./Resources/views/administration/index.html.twig`) and to provide translation handling.

The `src` directory of the SPA below is structured along the three different use cases the Administration faces - provide common functionality, an application skeleton, and modules.

bash

```shiki
<shopware/src/Administration/Resources/app/administration/src/>
|- app
|- core
|- module
```

* `app`: Contains the application basis for the Administration. Generally, you will find framework dependant computational components here.
* `core`: Contains the binding to the Admin API and services.
* `module`: UI and state management of specific view pages, structured along the Core modules. More information on this is detailed below.

## Modules and their components [​](#modules-and-their-components)

One module represents a navigation entry in the Administrations main menu. Since the Administration is highly dependent on the Shopware ecommerce Core, the module names reappear in the Administration, though in a slightly different order. The main building block, which the Administration knows, is called `component`, adjacent to web components.

A `component` is the combination of styling, markup, and logic. What a component does will not surprise you if you are already familiar with the [MVC pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). The role of the model and controller collapses into a single class. The components Twig.js template is generally rendered by a JavaScript (`index.js`) file and includes styling from an SCSS file. A template file also notifies the JavaScript, which then reacts to specific (user) interactions. Furthermore, components can be and often are nested. Our [Component library](https://component-library.shopware.com/) will also give you an overview of our default components.

### General module structure [​](#general-module-structure)

A `page` represents the entry point or the page that needs to be rendered and encapsulates views. A `view` is a subordinate part of the page that encapsulates components. A `component` can itself encapsulate different components. From this level on, there is no distinction in the directory structure made.

At least one `page` is mandatory in each module. Though views and components can be present in the module, a vast default component library is present to help with default cases.

bash

```shiki
|- page1
  |- view1
    |- component1
    |- component2
      |- subcomponent1
      |- …
  |- view2
    |- component3
    |- …
```

### Order module [​](#order-module)

Having a look at a more practical example, one can look closer at the order module. Typically, you will find this structure alongside other modules, especially when creating pages or views for creating/editing, listing, or viewing a specific entity. Refer to the [Add custom module](./../../../guides/plugins/plugins/administration/module-component-management/add-custom-module.html) article if you want to learn more about adding your custom module with a Shopware plugin.

bash

```shiki
<shopware/src/Administration/Resources/app/administration/src/module/sw-order/>
|- acl
|- component
  |- sw-order-address-modal
  |- …
|- page
  |- sw-order-create
  |- sw-order-detail
  |- sw-order-list
|- snippet  
|- state  
|- view
  |- sw-order-create-base
  |- sw-order-details-base
|- index.js
```

## Inheritance [​](#inheritance)

To add new functionality or change the behavior of an existing component through plugins, you can either override or extend a component. The difference between the two methods is `Component.extend()` method creates a new component and `Component.override()` method overwrites the previous behavior of the component.

Within plugins, you do have the following options when it comes to adjusting existing components:

* Override a component's logic
* Extend a component's logic
* Customize a component template with Twig.js
* Extending methods and computed properties

You will find more information about [customizing components](./../../../guides/plugins/plugins/administration/module-component-management/customizing-components.html) of the Administration in the guide.

## ACL in the Administration [​](#acl-in-the-administration)

The Access Control List (ACL) in Shopware ensures that by default, data can only be created, read, updated, or deleted ( CRUD), once the user has specific privileges for a module. Additionally, one can set up custom roles in the Administrations UI or develop individual privileges with plugins. These roles have finely granular rights, which every shop operator can set up himself and be assigned to users. By default, a module of the Administration has a directory called `acl` included. In this directory, one will find a specific mapping of privileges (permissions for roles; additional permissions) for the default roles: `viewer`, `editor`, `creator`, and `deleter`.

For more information, refer to [Adding permissions](./../../../guides/plugins/plugins/administration/permissions-error-handling/add-acl-rules.html) article.

---

## Rule system

**Source:** https://developer.shopware.com/docs/concepts/framework/rule-system/

# Rule system [​](#rule-system)

Shopware provides a generic **rule system** that allows you to describe business conditions as composable rules. These rules are evaluated against a specific context, such as a cart, an order, or a customer and are used across multiple domains like checkout, promotions, and flows.

On top of this rule system, the **Rule Builder** is the Administration feature that lets users configure and combine rule conditions visually.

## Example scenario [​](#example-scenario)

The power of the rule system can be illustrated with a simple scenario:

**"If a customer orders a car, a pair of sunglasses will be free in the same order."**

This relies on multiple different data points:

* A product called "car"
* A product called "sunglasses"

Both are independent, separately buyable, and stored in the database.

* The whole state of a single cart
* The quantity of a line item

This is a runtime concept in memory, resulting in the adjustment of a single line item's price, which in turn changes the whole calculation of the cart.

The rule system sits right in the middle of this scenario, providing the necessary mapping information to get from point A (`car` is in the cart) to point B (`sunglasses` are free), without embedding this logic directly into the cart.

## Where rules are used [​](#where-rules-are-used)

The rule system is cross-domain and used in multiple parts of Shopware, including among others:

* **Checkout and cart:** Controlling availability and behavior of shipping methods, payment methods, and product prices based on the current cart and customer.
* **Promotions:** Applying or restricting promotions depending on the customer, cart content, or other criteria.
* **Flow Builder:** Defining rule conditions, controlling flow behavior and outcome, based on order, checkout, customer or product context.

---

## Rule concepts

**Source:** https://developer.shopware.com/docs/concepts/framework/rule-system/rule-concepts.html

# Rule concepts [​](#rule-concepts)

## Rule [​](#rule)

A **rule** represents a single condition that can be evaluated to either `true` or `false`.

Rules can represent very different things (customer attributes, cart content, dates, tags, and more), but they follow the same contract: they evaluate against a given scope and return a boolean.

![Rule scope](/assets/framework-rules-rulesScope.Sve3OTTX.svg)

### Responsibilities [​](#responsibilities)

A rule answers a specific question, such as "Does the customer belong to the standard customer group?" or "Is the cart total greater than 50?".

### Input [​](#input)

A rule does not fetch the data needed for the evaluation on its own. Instead, it receives all required data through a **rule scope**.

### Output [​](#output)

A rule always returns a boolean result and has no side effects. It does not modify the cart, orders, or any other state.

## Rule scopes [​](#rule-scopes)

A **rule scope** defines the context in which a rule is evaluated and provides the data that is available for the evaluation.

### Context carrier [​](#context-carrier)

The scope provides access to the technical context (`Context`, `SalesChannelContext`) and, depending on the use case, domain-specific data, such as the current cart, customer, order, or products.

### Specialization [​](#specialization)

Different parts of the system use different scopes. For example:

* `CheckoutRuleScope` provides access to the `SalesChannelContext` (customer, sales channel, currency, etc.).
* `CartRuleScope` extends `CheckoutRuleScope` and adds access to the current cart.
* `FlowRuleScope` includes checkout information plus the related order.

Rules depend only on what the scope exposes to them. This keeps rule implementations focused and makes them reusable across features that share the same scope.

## Container rules [​](#container-rules)

Rules can be **combined into trees** using special rules called **container rules**. Container rules do not evaluate any conditions on their own, but instead combine the results of other rules using logical operators.

### Logical composition [​](#logical-composition)

Container rules implement logical behavior such as:

* "All of these conditions must match" (`AndRule`)
* "At least one of these conditions must match" (`OrRule`)
* "This condition must not match" (`NotRule`)

### Tree structure [​](#tree-structure)

A complete rule definition is represented as a tree:

* Container nodes (AND, OR, NOT, etc.)
* Leaf nodes (concrete rule conditions that check a single condition)

The following diagram shows an example rule tree with an `OrRule` container and two leaf conditions:

This tree structure allows for complex rule definitions that can express a wide variety of conditions with the same building blocks.

## Operators and comparisons [​](#operators-and-comparisons)

Most rules compare values (for example, a number, string or date) against a given input using standardized **operators**.

Conceptually, a rule can be read as: "Compare **this input value** from the scope with **this configured value** using **this operator**".

### Standard operator set [​](#standard-operator-set)

Common operators include:

* Equality or inequality (`=`, `!=`)
* Ranges (`<`, `<=`, `>`, `>=`)
* Emptiness checks (`empty`)

### Consistent semantics [​](#consistent-semantics)

Rules that compare similar types of values (numbers, strings, dates, IDs) share consistent comparison semantics (`RuleComparison`). This makes behavior predictable across different rules, contexts, and domains.

## Rule configuration [​](#rule-configuration)

Each rule condition defines which operators it supports in **the rule config** (`RuleConfig`). The Rule Builder uses this information to present the correct operator choices and fields in the administration UI. You can think of the rule config as the **UI contract** for a rule: it defines what users can enter and how it is presented. The rule config declares:

### Operator set [​](#operator-set)

A rule defines which operators are valid for its comparison. For example, a numeric rule might support range operators (`<`, `>`, etc.), while string-based rules might only support equality checks (`=`, `!=`).

### Field definitions [​](#field-definitions)

A rule describes each configurable field by:

* **Name:** Identifier of the field (for example `amount` or `customerGroupId`).
* **Type:** How the field is represented in the UI (for example `number`, `text`, `date`).
* **Additional config:** Extra information the UI needs (for example, available options for select fields, a unit for number fields, or a placeholder for text fields).

## Rule constraints [​](#rule-constraints)

To ensure that rules are configured correctly, each rule also defines **rule constraints** (`RuleConstraints`). These constraints describe what counts as a valid configuration for a rule. They are used to validate rule payloads before evaluating them.

### Value constraints [​](#value-constraints)

A rule can specify which kinds of values are allowed for each property, for example:

* A number field must be present and must contain a numeric value.
* A string field must not be blank.
* A list of IDs must contain valid identifiers.

### Operator constraints [​](#operator-constraints)

A rule can also restrict which operator values are allowed. For example, a rule might only allow equality checks (`=`, `!=`) and disallow range comparisons (`<`, `>`).

---

## Rule evaluation

**Source:** https://developer.shopware.com/docs/concepts/framework/rule-system/rule-evaluation.html

# Rule evaluation [​](#rule-evaluation)

The lifecycle of rule evaluation from UI to decision-making can be summarized as follows:

1. The Rule Builder lets a user create a rule tree (containers and conditions).
2. The rule system validates each condition against the corresponding rule class from the registry.
3. Valid rule and rule condition records are stored in the database.
4. At runtime, a domain builds an appropriate rule scope and, if needed, computes matching rules for that scope in advance.
5. Features either filter by rule IDs exposed on the context or evaluate a specific rule tree directly by calling it.

The sections below explain the individual steps in more detail.

## 1. From Rule Builder to stored rule definition [​](#_1-from-rule-builder-to-stored-rule-definition)

### 1.1. Rule trees and conditions [​](#_1-1-rule-trees-and-conditions)

When a user configures a rule in the Rule Builder:

* The **visual tree** is mapped to a `rule` entity representing the whole rule and multiple `rule_condition` records representing both container nodes and leaf conditions.
* The tree structure is stored via `parent_id` references between `rule_condition` records.
* Each `rule_condition` has a **type** that maps to a rule class (implementing `Rule`) and stores its configured values (operator, thresholds, IDs, etc.) in a `value` JSON field.

So the Rule Builder is building the **structure and configuration** that will later be hydrated into a tree of `Rule` objects for evaluation.

### 1.2. Validation [​](#_1-2-validation)

Before writes are accepted, `RuleValidator` validates each condition. It subscribes to write events and inspects commands targeting `RuleConditionEntity`. For each condition, it:

* Resolves the condition type to a rule class via the `RuleConditionRegistry`.
* Instantiates the rule and uses its constraints to understand which fields and operators are valid.

If the payload does not match what the rule class declares (wrong fields, types, operators), the write is rejected.

## 2. Preparing evaluation [​](#_2-preparing-evaluation)

Rules do not fetch data themselves, they always evaluate against a provided **rule scope**.

### 2.1. Rule scope specification [​](#_2-1-rule-scope-specification)

The abstract `RuleScope` defines the minimal contract for evaluation. Domains extend it to add domain-specific data.

* `CheckoutRuleScope` - base for checkout-related rules.
* `CartRuleScope` - adds access to cart data.
* `FlowRuleScope` - adds access to order data.
* `LineItemScope` - focuses on a single line item.

### 2.2. Scope owners [​](#_2-2-scope-owners)

Different parts of the system are responsible for constructing scopes:

* **Cart / Checkout:** `CartRuleLoader` is the main entry point for cart and checkout rule evaluation, building the necessary scopes and evaluating rules against them.
* **Flows:** `FlowRuleScopeBuilder` is responsible for building `FlowRuleScope`. It reconstructs a cart-like context from an order and runs data collectors so rules see realistic checkout data.
* **Line items:** Classes like `AnyRuleLineItemMatcher` construct `LineItemScope` when they need to test rules against individual line items.

The important point is: rules themselves are pure functions that depend only on the scope they receive. They do not depend on a global state.

## 3. Matching rules [​](#_3-matching-rules)

For some domains (checkout), the system evaluates all rules upfront and exposes the IDs of matching rules in the context so features can filter by them.

### 3.1. Candidate loading [​](#_3-1-candidate-loading)

`CartRuleLoader` is central for checkout. It uses the `AbstractRuleLoader` to load a collection of rules and narrows these to context-relevant rules before evaluating anything.

### 3.2. Iterative matching [​](#_3-2-iterative-matching)

To determine which of these candidates actually match the current cart context, `CartRuleLoader` builds the scope and uses `RuleCollection::filterMatchingRules(...)` to keep only rules whose payload rule tree evaluates to `true` for that scope. The matching rule IDs are then exposed on the `SalesChannelContext`.

Because the set of matching rules can affect cart processors (promotions, shipping, etc.) which in turn change the cart, the loader may need to iterate:

The result is a **self-consistent pair** of (cart, matching rule IDs) in the context.

## 4. Rules at runtime [​](#_4-rules-at-runtime)

Once rules are validated and the context knows which rules match, features can consume them in two ways.

### 4.1. ID-based decisions [​](#_4-1-id-based-decisions)

Features that only need to know "is this entity available in the current context?" attach a rule ID then filter by IDs exposed on the context. For example:

* Entities like `shipping_method`, `payment_method` or `tax_provider` have an `availability_rule_id` field.
* Items with availability rules are allowed if their rule ID is in `SalesChannelContext::getRuleIds()`.

### 4.2. Direct evaluation [​](#_4-2-direct-evaluation)

Other features need to evaluate a particular rule against a specific scope (flow, cart calculation, etc.). In these cases, the feature fetches the rule tree from the database, builds the appropriate scope for the current need and calls `Rule::match(RuleScope $scope)` on the root rule.

The following sequence shows how a container rule delegates to its children:

Since the `OrRule` requires at least one child to match, and both return `false`, the entire rule evaluates to `false`.

---

## Data Abstraction Layer

**Source:** https://developer.shopware.com/docs/concepts/framework/data-abstraction-layer.html

# Data Abstraction Layer [​](#data-abstraction-layer)

## Database access [​](#database-access)

### Database guide [​](#database-guide)

In contrast to most Symfony applications, Shopware uses no ORM, but a thin abstraction layer called the data abstraction layer (DAL). The DAL is implemented with the specific needs of Shopware in mind and lets developers access the database via pre-defined interfaces. Some concepts used by the DAL, like Criteria, may sound familiar to you if you know [Doctrine](https://symfony.com/doc/current/doctrine.html) or other ORMs. A reference to more in-depth documentation about the DAL can be found below.

Refer to [Shopware 6.6.5.0 entity relationship model](../../../assets/shopware6-erd.pdf) that depicts different tables and their relationships.

Alternatively, you can export a fresh ER model, using [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-reverse-engineering.html), [PHPStorm Database Tools](https://www.jetbrains.com/help/phpstorm/creating-diagrams.html), or similar tool.

INFO

Mysql Workbench → File → Import → Reverse Engineer Mysql Script → Select Db → ER diagram is created. If you want to have it as an image: File → Export → Export as PNG

### CRUD operations [​](#crud-operations)

An EntityRepository is used to interact with the DAL. This is the recommended way for developers to interface with the DAL or the database in general.

### Provisioning code to use the repositories [​](#provisioning-code-to-use-the-repositories)

Before using the repositories, you will need to get them from the [Dependency Injection Container (DIC)](./../../guides/plugins/plugins/plugin-fundamentals/dependency-injection.html). This is done with [Constructor injection](https://symfony.com/doc/current/service_container/injection_types.html#constructor-injection), so you will need to extend your services constructor by expecting an EntityRepository:

php

```shiki
// <plugin root>/src/Service/DalExampleService.php
public function __construct (EntityRepository $productRepository)
{
    $this->productRepository = $productRepository;
}
```

If you are using [Service autowiring](https://symfony.com/doc/current/service_container/autowiring.html) with the correct type and argument variable names, the repository will be injected automatically.

Alternatively, configure the `product.repository` service to be injected explicitly:

html

```shiki
// <plugin root>src/Resources/config/service.xml
<service id="Swag\ExamplePlugin\Service\DalExampleService">
    <argument type="service" id="product.repository"/>
</service>
```

You can read more about dependency injection and service registration in Shopware in the services guides:

[Add custom service](../../guides/plugins/plugins/plugin-fundamentals/add-custom-service)

### Translations [​](#translations)

The DAL was designed, among other things, to enable the special requirements of Shopware's translation system. When a record is read or searched, three language levels are searched.

1. **Current language**: The first level is the current language that is set and displayed to the user.
2. **Parent language**: the second level is an optional parent language that can be configured. So it is possible to translate certain dialects faster.
3. **System language**: The third and last level is the system language that is selected during the installation. Each entity in the system has a translation in this language. This serves as a final fallback to ensure only one label for the entity in the end.

The translations for a record are stored in a separate table. The name of this table is always the same as the table for which the records are translated, with the additional suffix `_translation`.

### Versioning [​](#versioning)

Another feature that the DAL offers is versioning. This makes it possible to store multiple versions of a single entity. All data assigned to an entity is duplicated and made available under the new version. Multiple entities or changes to different entities can be stored for one version. The versioning was designed for previews, publishing, or campaign features, to prepare changes that are not yet live and to be able to view them in the store. Currently, it is not possible (yet) to create a completely new entity with another version than the default live version. Means, you cannot "draft" the entity first and then update it into the live version. A live version of your entity is always required, before deriving a new version from it.

The versioning is also reflected in the database. Entities that are versionable always have a compound foreign key: `id`, `version_id`. Also, the foreign keys, which point to a versioned record, always consist of two columns, e.g.: `product_id` and `product_version_id`.

### Context [​](#context)

The context `core/Framework/Context.php` defines important configuration of the shop system and is instantiated once per request. Depending on the passed parameters it can change the CRUD behavior of the DAL. For example when using the currency toggle in the storefront and selecting Dollar instead of Euro, the context currency ID is changed accordingly and all operations now refer to Dollar.

### Inheritance [​](#inheritance)

Another reason why the DAL was designed is to meet the requirements of the product and variant system. For this purpose, a parent-child inheritance system was implemented in the DAL. This allows variants to inherit records, properties, or even whole associations from the parent or container product. For example, if a variant has not been assigned any categories or images, those of the parent product are used.

### Indexing [​](#indexing)

The DAL was designed to be optimized for use in ecommerce. One principle has proven to be very effective so far: "The more time you put into indexing data, the faster it is possible to read it". This is reflected in Shopware as follows:

* A product is written once every X minutes
* A product is called X times every X seconds by a customer.

This varies depending on the store, but the ratio is always the same. Data records are read way more often than they are written. Therefore, it is worthwhile to spend a little more time on the writing process in order to minimize the effort required for the reading process. This is done in the DAL via the Entity Indexer pattern. As soon as a product record is written, the corresponding Product Indexer is triggered, which pre-selects certain aggregations and writes them away optimized for the later reading process.

---

## Messaging

**Source:** https://developer.shopware.com/docs/concepts/framework/messaging.html

# Messaging [​](#messaging)

Shopware integrates with the [Symfony Messenger](https://symfony.com/doc/current/components/messenger.html) component and [Enqueue](https://enqueue.forma-pro.com/). This gives you the possibility to send and handle asynchronous messages.

## Components [​](#components)

### Message Bus [​](#message-bus)

The [Message bus](https://symfony.com/doc/current/components/messenger.html#bus) is used to dispatch your messages to your registered handlers. While dispatching your message it loops through the configured middleware for that bus. The message bus used inside Shopware can be found under the service tag `messenger.default_bus`. It is mandatory to use this message bus if your messages should be handled inside Shopware. However, if you want to send messages to external systems, you can define your custom message bus for that.

### Middleware [​](#middleware)

A [Middleware](https://symfony.com/doc/current/messenger.html#middleware) is called when the message bus dispatches messages. It defines what happens when you dispatch a message. For example, the `send_message` middleware is responsible for sending your message to the configured [Transport](./messaging.html#transport), and the `handle_message` middleware will actually call your handlers for the given message. You can add your own middleware by implementing the `MiddlewareInterface` and adding that middleware to the message bus through configuration.

### Handler [​](#handler)

A [Handler](https://symfony.com/doc/current/messenger.html#registering-handlers) gets called once the message is dispatched by the `handle_messages` middleware. A message handler is a PHP callable, the recommended way to create it is to create a class that has the `AsMessageHandler` attribute and has an `__invoke()` method that's type-hinted with the message class (or a message interface)

### Message [​](#message)

A [Message](https://symfony.com/doc/current/messenger.html#message) is a simple PHP class you want to dispatch over the MessageQueue. It must be serializable and should contain all the necessary information that a [handler](./messaging.html#handler) needs to process the message.

### Envelope [​](#envelope)

A message will be wrapped in an [Envelope](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes) by the message bus that dispatches the message.

### Stamps [​](#stamps)

While the message bus is processing the message through its middleware, it adds [Stamps](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes) to the envelope that contain metadata about the message. If you need to add metadata or configuration to your message, you can either wrap your message in an envelope and add the necessary stamps before dispatching your message or create your own custom middleware.

### Transport [​](#transport)

A [Transport](https://symfony.com/doc/current/messenger.html#transports) is responsible for communicating with your 3rd party message broker. You can configure multiple Transports and route messages to multiple or different Transports. Supported are all Transports that are either supported by [Symfony](https://symfony.com/doc/current/messenger.html#transports) itself or by [Enqueue](https://github.com/php-enqueue/enqueue-dev/tree/master/docs/transport). If you don't configure a Transport, messages will be processed synchronously, like in the Symfony event system.

### Sending Messages [​](#sending-messages)

To send messages, the Shopware messenger bus is used, which can be injected through DI and populated with metadata. Optionally, there is also a message bus for sensitive data that offers encryption.

### Consuming Messages [​](#consuming-messages)

Consuming messages can be done via both a [Console command](./../../guides/hosting/infrastructure/message-queue.html#cli-worker) and via an API endpoint. The console command starts a worker that will receive incoming messages from your Transport and dispatch them. The API can be communicated via a POST, which will consume messages for 2 seconds, and then you get the count of the handled messages in the response.

---

## Migrations

**Source:** https://developer.shopware.com/docs/concepts/framework/migrations.html

# Migrations [​](#migrations)

Migrations are PHP classes containing database schema changesets. These changesets can be applied or reverted to bring the database into a certain state. You might know the concept of migrations from other Frameworks or Symfony as well.

## Adding migrations to a plugin [​](#adding-migrations-to-a-plugin)

For Shopware to recognize additional plugin migrations, they need to be placed in the `Migration` directory under your plugin's source code root directory.

Each migration filename follows a specific pattern. To ease plugin development, Shopware provides a console command which can be used to generate a correctly named migration file with the default methods needed.

[Create migration](../../guides/plugins/plugins/plugin-fundamentals/database-migrations.html#create-migration)

## Modifying the database [​](#modifying-the-database)

Each migration can have two methods. The `update` and `updateDestructive`. The `update` method must contain only non-destructive changes which can be rolled back at any time. The `updateDestructive` method can contain destructive changes, like dropping columns or tables, which cannot be reversed. For examples of database migrations, refer to the below guide:

[Database migration](../../guides/plugins/plugins/plugin-fundamentals/database-migrations.html)

---

## HTTP Cache

**Source:** https://developer.shopware.com/docs/concepts/framework/http_cache.html

# HTTP Cache [​](#http-cache)

The HTTP cache allows you to cache responses of the shop system. This means that the next time the same page is requested, the answer can be returned much faster. While the general concept of a cache is quite simple, there are many details to think of in a complex system like a shopping cart. For that reason, the following overview might come in handy for you.

## HTTP cache setup [​](#http-cache-setup)

If you think about a simple web page, you will usually have a setup like this:

* A user that requests a page
* The web application generates a result

So whenever a user requests a page, Shopware will create a result page individually. If you have many users requesting the same pages, it makes sense to have an additional instance in between:

* A user that requests a page
* A reverse proxy cache
* The web application generates a result

![Http cache concept](/assets/concepts-framework-httpCache.DuIsfKY2.svg)

The reverse proxy is located between the user and the web application and takes care of any requests to the web application. If a user requests a page that has been requested before, chances are that the reverse proxy can just hand out the same result as before, so the web application will not even be asked.

So a reverse proxy is basically a thin layer between the user and the web application that will try to avoid load on the web application by caching the results. Whenever the web application generates a response for a request, the reverse proxy will save the request and the response to cache storage. The next time the same request comes in, the response will most probably be the same.

## How does it work? [​](#how-does-it-work)

Caching is always about questions like:

* Did I return the same page before?
* Did the content of the page change meanwhile?
* Is this page the same for all customers, or will the current customer get another result (e.g. price)?

The Shopware HTTP cache has a variety of mechanisms to answer these questions.

## When will the page be cached? [​](#when-will-the-page-be-cached)

Set the defaults value of the `_httpCache` key to `true`. Examples for this can be found in the [ProductController](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Controller/ProductController.php#L62). Only `GET` requests are considered cacheable.

php

```shiki
#[Route(path: '/detail/{productId}', name: 'frontend.detail.page', methods: ['GET'], defaults: ['_httpCache' => true])]
public function index(SalesChannelContext $context, Request $request): Response
```

### Determining the cache key [​](#determining-the-cache-key)

Determining the cache key is one of the most important tasks of the HTTP cache. The cache key is used to identify a request and its corresponding response. If the same request comes in again, the cache key will be used to look up the corresponding response in the cache storage. For a dynamic system like Shopware, the cache key needs to take the application state into account, as the response to the same request might differ e.g., based on the tax state of the currently logged-in customer. At the same time, it needs to be possible to generate the cache key directly from the request to support reverse proxy caches, where the caching is handled by a standalone application that has no access to Shopware's internal application state. Shopware generates a `cache-hash` that encodes the application state and this hash is passed alongside every request and response, the caching component will then generate the exact cache key based on the `cache-hash`.

Concretely Shopware uses Cookies to store the `cache-hash` as part of the request/response structure. The `cache-hash` describes the current state of the customer "session", every parameter that leads to different responses being generated (e.g., tax-states, matched rules) should be taken into account for the `cache-hash` to ensure that every user sees the correct page. However, it is equally important to keep the number of different cache entries/permutations as low as possible to maximize the cache hits. The reason the `cache-hash` is stored as a cookie is that it needs to be sent with every request and can change on any response sent from shopware. The client needs to send the latest value back to shopware on every request to ensure the correct cache entry is used. This is needed as the cache is resolved before the request is handled by shopware itself. To allow reverse proxies to cache based on the application state, the information needs to be present on every request. The reverse proxies (e.g., Fastly or Varnish) or the symfony cache component use the provided `cache-hash` as part of the cache key they generate for every request, thus they can differentiate the cache entries for the same request based on the application state.

#### sw-cache-hash [​](#sw-cache-hash)

This cookie contains the hash of all cache-relevant information (e.g. is the user logged-in, what tax state and what currency do they use, which cache-relevant rules have matched). This is the cookie that stores the `cache-hash` mentioned above. This cookie will be set as soon as the application state differs from the default, which is: no logged-in customer, the default currency and an empty cart.

If you want to know how to manipulate and control the `cache-hash`, you can refer to the [Plugin caching guide](./../../guides/plugins/plugins/framework/caching/#http-cache).

#### sw-currency [​](#sw-currency)

**Note:** The currency cookie is deprecated and will be removed in v6.8.0.0, as the currency information is already part of the `sw-cache-hash` cookie. This cookie will be set when the non-logged-in customer with an empty cart changes the current currency. Why does Shopware need a separate cookie for currency? It allows us to maximize the cache hits for non-logged-in customers as we separate the cache as less as possible.

#### sw-states [​](#sw-states)

**Note:** The states cookie is deprecated and will be removed in v6.8.0.0, as the state information is already part of the `sw-cache-hash` cookie and different caches are used for the different states. If you want to disable the cache in certain circumstances, you can do so via the `sw-cache-hash` cookie as well. This cookie describes the current session in simple tags like `cart-filled` and `logged-in`. When the client tags fit the response `sw-invalidation-states` header, the cache will be skipped.

An example of usage for this feature is to save the cache for logged-in customers only.

### Determining TTL and other cache parameters [​](#determining-ttl-and-other-cache-parameters)

The TTL and other cache parameters are determined via [caching policies](./../../guides/hosting/performance/caches.html#http-caching-policies). The feature is experimental and will become the default behavior in Shopware v6.8.0.0.

## Cache invalidation [​](#cache-invalidation)

As soon as a response has been defined as cacheable and the response is written to the cache, it is tagged accordingly. For this purpose, the core uses all cache tags generated during the request or loaded from existing cache entries. The cache invalidation of a Storefront controller route is controlled by the cache invalidation of the Store API routes.

For more information about Store API cache invalidation, you can refer to the [Caching Guide](./../../guides/plugins/plugins/framework/caching/).

This is because all data loaded in a Storefront controller is loaded in the core via the corresponding Store API routes and provided with corresponding cache tags. So the tags of the HTTP cache entries we have in the core consist of the sum of all Store API tags generated or loaded during the request. Therefore, the invalidation of a controller route is controlled over the Store API cache invalidation.

List-type routes are not tagged with all entities returned in the response. This applies to Store API endpoints such as product listings or search results, category listings, or SEO URL listings. These routes instead rely on their TTL as defined by the active HTTP Caching Policy. If the default TTLs are not appropriate for your use case, configure a [custom caching policy](./../../guides/hosting/performance/caches.html#fine-tuning-per-route-or-app-hook) for those routes. The reason is that, while it would be technically possible to try to invalidate all affected listings when a single entity changes, doing this at scale is very costly in terms of performance and resources. One entity can appear in many different listings (with different filters, sorting, pagination, etc.). It is also not possible to catch all cases where a change would cause an entity to newly appear in or disappear from a cached listing. Because of this, listing pages cannot guarantee strict, immediate consistency under caching; instead, we accept a small amount of staleness in exchange for predictable performance and stability.

Since v6.7.7.0, cache invalidations logging at info level can be enabled or disabled via the `tag_invalidation_log_enabled` configuration option. It is disabled by default.

yaml

```shiki
# <shopware-root>/config/packages/shopware.yaml
shopware:
  cache:
    invalidation:
      tag_invalidation_log_enabled: false
```

## HTTP Cache workflow [​](#http-cache-workflow)

**Note:** Workflow described here applies since v6.8.0.0 or since 6.7.6.0 when the `CACHE_REWORK` feature flag is enabled.

When a response is generated and about to be sent to the client, the `CacheResponseSubscriber` executes the following logic to determine caching behavior:

* Header application: The system applies `sw-language-id` and `sw-currency-id` headers. The `Vary` header is expanded to include these IDs and the `sw-context-hash`, ensuring proxies store separate cache entries for different contexts.
* Early exits: Basic checks are performed (e.g., is HTTP cache enabled?) to potentially skip further processing.
* Context hash calculation: The `sw-context-hash` is calculated based on the current state (cart, customer, rules, etc.). Extensions can hook into this process to add their own parameters (see [Plugin Caching Guide](./../../guides/plugins/plugins/framework/caching/#http-cache)).
* Cacheability assessment: The request is evaluated if it can be cached. It must be a `GET` request and the route must be marked with the `_httpCache` attribute.
* Validation: The system compares the client's `sw-context-hash` with the server-calculated hash. If they mismatch, a no-cache policy is applied to prevent cache poisoning. The `sw-dynamic-cache-bypass` header is added to hint proxies to apply shorter TTLs for ["hit-for-pass"](https://info.varnish-software.com/blog/hit-for-pass-varnish-cache) objects (custom configuration needed).
* Policy application: The appropriate [caching policy](./../../guides/hosting/performance/caches.html#http-caching-policies) is resolved for the route and applied to the response, setting the correct `Cache-Control` headers.

---

## Elasticsearch

**Source:** https://developer.shopware.com/docs/concepts/framework/elasticsearch.html

# Elasticsearch [​](#elasticsearch)

Elasticsearch is a NoSQL Database focused on search capabilities to act as a search engine. The Shopware implementation of Elasticsearch provides an integrated way to improve the performance of product and category searches. To use Elasticsearch for your shop, take a look at our [Elasticsearch guide](./../../guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.html)

## Concept [​](#concept)

### Enabling Elasticsearch for your search [​](#enabling-elasticsearch-for-your-search)

Elasticsearch is only used in searches that are explicitly defined. This is by default set to the `ProductSearchRoute`, `ProductListingRoute`, and `ProductSuggestRoute`. To use Elasticsearch on your own searches, make sure to add the Elasticsearch aware state to your criteria.

INFO

If the Elasticsearch query fails, the data is loaded using MySQL. You can disable this behavior by setting the environment variable `SHOPWARE_ES_THROW_EXCEPTION=1`

php

```shiki
$criteria = new \Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria();
$context = \Shopware\Core\Framework\Context::createDefaultContext();
// Enables Elasticsearch for this search
$context->addState(\Shopware\Core\Framework\Context::STATE_ELASTICSEARCH_AWARE);

$repository->search($criteria, $context);
```

### ElasticsearchDefinition [​](#elasticsearchdefinition)

To provide Elasticsearch for an entity, a corresponding `ElasticsearchDefinition` needs to be added. Shopware has a definition for the product entity called `ProductElasticsearchDefinition`. This definition defines the fields provided to Elasticsearch and how they are aggregated.

### ElasticsearchEntitySearcher [​](#elasticsearchentitysearcher)

The `ElasticsearchEntitySearcher` decorates the `EntitySearcher` to map the entity search to the Elasticsearch structure. The `ElasticsearchEntitySearcher` returns an `IdSearchResult` hydrated by the `ElasticsearchEntitySearchHydrator` as the `EntitySearcher` does, and this result is used to read the found ids from the database.

### ElasticsearchEntityAggregator [​](#elasticsearchentityaggregator)

The `ElasticsearchEntityAggregator` does the same as the `ElasticsearchEntitySearcher` for aggregations.

### CriteriaParser [​](#criteriaparser)

The `CriteriaParser` parses the criteria to an Elasticsearch specific notation.

### ProductSearchBuilder [​](#productsearchbuilder)

The product search has a special `ProductSearchBuilder` in the core, and so has the Elasticsearch extension, a corresponding extension for the `ProductSearchBuilder`. This extension matches the queries of the core `ProductSearchBuilder` to the Elasticsearch notation.

### ProductUpdater [​](#productupdater)

The `ProductUpdater` listens to the `ProductIndexerEvent` and triggers the `ElasticsearchIndexer` on changes to a `ProductEntity`.

## Commands [​](#commands)

### es:index:cleanup [​](#es-index-cleanup)

The command `es:index:cleanup` deletes outdated Elasticsearch indexes. The parameter `-f` will skip the confirmation.

### es:create:alias [​](#es-create-alias)

The command `es:create:alias` refreshes the current Elasticsearch index and sets the alias to the index name without the timestamp (which will make this index the active index). This will happen automatically when a new index is published, so this command can force the alias creation for testing purposes or if something goes wrong.

### es:index [​](#es-index)

The command `es:index` re-indexes all configured entities to Elasticsearch.

### es:reset [​](#es-reset)

The `es:reset` command resets all active indices with their respective prefix (`SHOPWARE_ES_INDEX_PREFIX`) in the .env file and clears the queue. This command should only be used if an index is corrupted or needs to be set up from scratch. If multiple Shopware instances are accessing the same Elasticsearch Host, you should consider changing the prefix.

### es:status [​](#es-status)

The command `es:status` returns the status of all current Elasticsearch indices.

### es:test:analyzer [​](#es-test-analyzer)

The command `es:test:analyzer` runs an Elasticsearch analyzer on your indices. For more details on Elasticsearch analyzers, take a look at this [external link](https://www.elastic.co/docs/reference/text-analysis/analyzer-reference).

## Customize the Elasticsearch integration [​](#customize-the-elasticsearch-integration)

To customize the Elasticsearch integration or add your own fields and entities, refer to the [Elasticsearch extension guide](./../../guides/plugins/plugins/elasticsearch/add-product-entity-extension-to-elasticsearch.html)

---

## Flow

**Source:** https://developer.shopware.com/docs/concepts/framework/flow-concept.html

# Flow Builder [​](#flow-builder)

Flow Builder is a Shopware automation solution for shop owners with great adaptability and flexibility. With Flow Builder, you can build workflows to automate tasks tailored to your business needs without programming knowledge.

## Flow [​](#flow)

A flow is an automation process in your business. From here, you can specify which actions are triggered by a trigger. Additionally, you can define conditions for these actions under which the actions are to be executed. If multiple flows with the same trigger exist, the priority point will decide which flow will perform first.

## Trigger [​](#trigger)

A trigger is an event that starts the flow and detects the event from the Storefront or the application. A trigger could have multiple actions.

## Condition [​](#condition)

A condition is a business rule to determine whether the action should be executed.

## Action [​](#action)

An action is a task that executes on a trigger or when certain conditions are met.

A special action called "Stop flow" stops any further action in the flow sequence.

## Flow Templates [​](#flow-templates)

A flow template is a pre-created [flow](#flow).

The flow library contains the flow template listing shipped with Shopware. Two main ways to create a flow template in the template library are by [apps](./../../guides/plugins/plugins/framework/flow/) and [plugins](./../../guides/plugins/apps/flow-builder/).

We can help merchants reduce the complexity of creating an automation process in their business by using a flow template rather than building a flow. As a merchant, you may design a flow more easily by using the flow templates. So you don't have to create complicated flows on your own.

You can view the details of a flow template just like a regular flow. However, flow templates can't be modified.

## How a flow sequence is evaluated [​](#how-a-flow-sequence-is-evaluated)

In Shopware, you have multiple interfaces and classes for different types of events. For Flow Builder, those triggers mentioned above are implements from the *Aware* interface.

Once the action on the Storefront or from the app happens, the FlowDispatcher will dispatch FlowEventAware to the FlowExecutor. From here, the FlowExecutor will check the condition to decide whether to execute the action.

Here is an example flow of what happens in the system when an order is placed on the Storefront.

## Storer concept [​](#storer-concept)

Every flow can have data stored and associated with it. This data can be used in the actions when the flow is triggered (for example, for fetching the order that triggered the flow).

There are many storer classes (`ProductStorer`, `OrderStorer`, `MailStorer` etc.) that extend an abstract `FlowStorer` class. They have the methods `store` and `restore`. These are called when the flow (`StorableFlow`) is created in the `FlowFactory` class. The `restore` method can either directly or in some cases lazy load the data that was stored in the `store` method.

Usually the storer classes are linked to different `*Aware` interfaces and store data relevant to these interfaces. The triggering events can implement multiple `*Aware` interfaces. For example, the `CheckoutOrderPlacedEvent` implements the `OrderAware` interface and when the flow object is created, the `OrderStorer` will be used to store and then restore the order data.

By default, the flow data is not persisted in the database because it's restored already in the same request cycle for actions that are triggered instantly. Only in the case of delayed flows, the data is persisted so that it can be later retrieved when the delayed flow is executed.

---

## System Check

**Source:** https://developer.shopware.com/docs/concepts/framework/system-check.html

# System Checks [​](#system-checks)

System checks are a way to ensure that your Shopware installation is operating normally, where each check verifies a specific aspect of functionality. If a check fails, it can be an indicator that something is wrong with your system.

## Concepts [​](#concepts)

### System Check [​](#system-check)

Shopware is composed of many components that work together to provide the full experience. A component can be an internal piece of code that achieves a functionality, an external provider, or a plugin.

Each system check verifies a specific aspect of the system. For example, one system check might verify that the database connection is working, another that the payment system is functioning correctly, or that the SMTP server is online.

And to ensure clear terminology, we have defined the following logical concepts that defines a guideline for a System Check type.

#### Types [​](#types)

* `Readiness Checks`: Checks that are executed before the system is ready to serve traffic.
* `Health Checks`: Checks that are executed periodically to ensure the system is healthy. Those are usually invoked either manually or by monitoring systems.
* `Long running Checks`: These are a subset of `Health Checks` but the main difference is that they can take a long time to execute, and they should always be executed in the background.

> [System Execution Context](#system-check-execution-context) plays a vital role in determining the type of the check

### Category [​](#category)

The category aims to cluster what the check is verifying rather than to categorize the type of check itself. Each component logically falls into a certain category. Functional categories are used to group checks together. The following categories are available:

* `SYSTEM`: System checks make sure that the backbone of the software is functioning correctly. For example, a database connection.
* `FEATURE`: Feature checks make sure that a specific feature of the software is functioning correctly. For example, the payment system.
* `EXTERNAL`: External checks make sure that external services are responding correctly. For example, the SMTP server is online.
* `AUXILIARY`: Auxiliary checks make sure that auxiliary services are functioning correctly. For example, Shopware background tasks are running.

### Status [​](#status)

A component is not always in a failing or working state. For example, sometimes it can be degraded and not fully operational while still providing some functionality. The status of a check is used to represent the outcome of the check:

* `OK`: The component is functioning correctly.
* `SKIPPED`: The component check was skipped. Which could mean that some criteria for the check were not met. (e.g. the check is not applicable to the current environment)
* `UNKNOWN`: The component status is unknown.
* `WARNING`: The component is functioning but with some issues that are not errors.
* `ERROR`: The component has runtime errors, but some parts of it could still be functioning.
* `FAILURE`: The component has failed with irrecoverable errors.

### System Check Execution Context [​](#system-check-execution-context)

System checks may be unnecessary in certain contexts but crucial in others. For instance, in an immutable environment, a check verifying runtime configuration is not needed after the system has been deployed to customers, as the configuration is not expected to change. However, this check is vital before a roll-out.

The context in which a check is executed is represented by the `SystemCheckExecutionContext`. The following contexts are available:

* `WEB`: The check is running in a web environment.
* `CLI`: The check is running in a command-line interface environment.
* `PRE_ROLLOUT`: The check is running before a system roll-out.
* `RECURRENT`: The check is running as part of a scheduled task.

---

## In-App Purchases

**Source:** https://developer.shopware.com/docs/concepts/framework/in-app-purchases.html

# In-App purchases (IAP) [​](#in-app-purchases-iap)

INFO

In-App Purchase is available since Shopware version 6.6.9.0

In-App Purchases are a way to lock certain features behind a paywall within the same extension. This is useful for developers who want to offer a free version of their extension with limited features and a paid version with more features.

## Creation [​](#creation)

In-App Purchases can be created in the Shopware Account. You can find out how to do this in the [Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/in-app-purchases).

## Token [​](#token)

Each in-app purchase is represented by a signed JSON Web Token (JWT), issued per extension. This JWT ensures that purchase data cannot be tampered with or spoofed and allows verification of its authenticity. All bought In-App Purchases are part of the JWT claims.

To verify the JWT signature, you can use the JSON Web Key Set (JWKS) available at [`https://api.shopware.com/inappfeatures/jwks`](https://api.shopware.com/inappfeatures/jwks) Shopware automatically verifies the signature for the use within the Core and Admin.

Tokens are retrieved when a new purchase is made and during periodic updates. You can also manually trigger an update by running the command `bin/console scheduled-task:run-single in-app-purchase.update` or by calling the `/api/_action/in-app-purchases/refresh` endpoint.

## Extensions [​](#extensions)

In-app purchases are optimized for use with app servers.

Whenever Shopware sends a request to the app server, it includes the [IAP JWT](#token). The app server can use this token to validate active purchases and unlock related features accordingly.

Plugins are inherently less secure, as their open nature makes them more vulnerable to spoofing or tampering.

[In-App purchases for Apps](../../guides/plugins/apps/in-app-purchases)[In-App purchases for Plugins](../../guides/plugins/plugins/in-app-purchases)

## Checkout Process [​](#checkout-process)

When integrating In-App Purchases, Shopware handles the entire checkout process for you—including payment processing and subscription management.

To initiate a purchase, simply provide the identifier of the desired In-App Purchase. This will trigger a modal window where the user can complete the transaction.

---

