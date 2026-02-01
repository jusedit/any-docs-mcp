# Guides Plugins Plugins Testing

*Scraped from Shopware Developer Documentation*

---

## Testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/

# Testing [​](#testing)

Robust testing is crucial for developing reliable and maintainable Shopware plugins and themes. Shopware provides tooling and guidance for several types of tests, ensuring your code is production-ready and meets community standards.

## Unit Testing [​](#unit-testing)

Unit testing is the base layer of an effective test strategy. Shopware supports both PHP backend logic and JavaScript components (for Storefront and Administration):

Use PHPUnit to write and run backend unit tests for your PHP code.

[PHP unit testing](php-unit)

Use Jest to test Storefront JS and Vue components following modern best practices.

[Jest unit tests in Shopware's storefront](jest-storefront)

Test custom Administration panel modules and components using Jest with the Shopware admin setup.

[Jest unit tests in Shopware's administration](jest-admin)

## End-to-End (E2E) Testing [​](#end-to-end-e2e-testing)

For simulating real user journeys and integration scenarios, Shopware recommends end-to-end (E2E) testing. Playwright is the officially supported tool for automating entire workflows across the application.

Automate browser interactions to verify plugins and customizations work as intended in real-world Shopware environments.

[Playwright E2E testing](playwright/)

Refer to the individual guides for setup, examples, and best practices for each testing type.

---

## Cypress End-to-end testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/

# Cypress End-to-end testing [​](#cypress-end-to-end-testing)

WARNING

Cypress will be deprecated in the future and is no longer maintained. We recommend using [Playwright](./../playwright/) for new projects.

---

## Cypress End-to-end testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/cypress-end-to-end-testing.html

# Cypress End-to-End Testing [​](#cypress-end-to-end-testing)

## Overview [​](#overview)

In end-to-end testing (E2E testing in short) real user workflows are simulated, whereby as many as possible functional areas and parts of the technology stack used in the application should be included. This way, we are able to put our UI under constant stress and ensure that Shopware's main functionalities are always working correctly.

## Prerequisites [​](#prerequisites)

To use Shopware E2E tests, at first you need to have a Shopware 6 installation running. Making sure, that your tests are reliable, you should have a clean installation. Cleanup means no categories, no products, no settings, nothing!

The easiest way to clean up your installation is the initialization. Using the command `composer run init` Shopware 6 gets initialized clean and without demo data. Installation of E2E dependencies can be accomplished separately by running `npm install` in the E2E folder you're using, e.g. for Shopware Administration it's `src/Administration/Resources/app/administration/test/e2e`.

Since our tests should run on an installation that is as close as possible to a release package, we use production mode. If you run the tests on a development environment, the test results may vary.

On top of that, please make sure your shop has a theme assigned. When using `composer run e2e:open` or `run`, this is done automatically.

This guide also won't teach you how to write Cypress tests in general. Please take a look at the official Cypress documentation for further guidance.

[Cypress Documentation](https://docs.cypress.io/)

### Using our testsuite [​](#using-our-testsuite)

The [E2E platform testsuite package](https://github.com/shopwareArchive/e2e-testsuite-platform) contains commands and helpers supporting you while building E2E tests for Shopware 6. On top of that, test data management and custom commands are included as well. More on that here: [Command reference](./../../../../resources/references/core-reference/commands-reference/).

This test suite is built on top of [Cypress](https://www.cypress.io/) as well as the following Cypress plugins:

* [cypress-select-tests](https://github.com/bahmutov/cypress-select-tests)
* [cypress-log-to-output](https://github.com/flotwig/cypress-log-to-output)
* [cypress-file-upload](https://github.com/abramenal/cypress-file-upload)

Here you can find the npm package of our testsuite:

[@shopware-ag/e2e-testsuite-platform - npm](https://www.npmjs.com/package/@shopware-ag/e2e-testsuite-platform)

Please have a look on our [cypress.json](https://github.com/shopwareArchive/e2e-testsuite-platform/blob/3.x/cypress.json), a few of our commands expect some configuration, e.g. viewportHeight and width, because the admin menu only opens if the viewport is wide enough.

## Setup steps [​](#setup-steps)

When you use our [Development template](https://github.com/shopwareArchive/development), we provide you some tooling scripts located in `dev-ops/e2e/actions`, to use E2E tests more comfortably.

The`composer` scripts to run our E2E tests in CLI or in Cypress' test runner are explained in the paragraph [Executing e2e tests](./end-to-end-testing/#executing-e2e-tests).

## Executing E2E tests [​](#executing-e2e-tests)

## Writing your first test [​](#writing-your-first-test)

### Folder structure [​](#folder-structure)

In Shopware platform, you can find the tests in `src/Administration/Resources/app/administration/test/e2e`. There you can find the following folder structure, depending on your environment being Administration or Storefront:

bash

```shiki
`-- e2e
  `-- cypress
    |-- fixtures
        `-- example.json
    |-- integration
        `-- testfile.spec.js
    |-- plugins
        `-- index.js
    |-- support
        |-- commands.js
        `-- index.js
    |--cypress.json
    `--cypress.env.json
```

In the `cypress` folder, all test related folders are located. Most things will take place in these four folders:

* `fixtures`: Fixtures are used as external pieces of static data that can be used by your tests. You can use them

  with the `cy.fixture` command.
* `integration`: By default, the test files are located here. A file with the suffix "\*.spec.js" is a test file that

  contains a sequence of tests, performed in the order defined in it.
* `plugins`: Contains extensions or plugins. By default, Cypress will automatically include the plugins file before

  every single spec file it runs.
* `support`: The support folder is a great place to put reusable behavior such as custom commands or global overrides in,

  that you want to be applied and available to all of your spec files.

These two configuration files are important to mention as well:

* `cypress.json`
* `cypress.env.json`

  These are Cypress configuration files. If you need more information about them, take a look at the

  [Cypress configuration docs](https://docs.cypress.io/app/references/configuration).

If you need to use this structure in a plugin, it is just the path to the `e2e` folder, which is slightly different. You can find the folder structure in the paragraph [Setup](./cypress-end-to-end-testing.html#setup-steps).

If you want to contribute to Shopware platform's tests, please ensure to place your test in one of those folders:

javascript

```shiki
`-- integration
  |-- catalogue
  |-- content
  |-- customer
  |-- general
  |-- media-marketing
  |-- order
  |-- rule-product-stream
  `-- settings
```

WARNING

This is important because otherwise your test is not considered by our CI.

### Test layout and syntax [​](#test-layout-and-syntax)

Cypress tests are written in Javascript. If you worked with Mocha before, you will be familiar with Cypress' test layout. The test interface borrowed from Mocha provides `describe()`, `context()`, `it()` and `specify()`.

To have a frame surrounding your test and provide a nice way to keep your test organized, use `describe()` (or `context()` as its alias):

javascript

```shiki
describe('Test: This is my test file', () => {
    it('test something', () => {
        // This is your first test
    });
    it('tests something else', () => {
        // This is your second test
    });
});
```

The `it()` functions within the `describe()` function are your actual tests. Similar to `describe()` and `context()`, `it()` is identical to `specify()`. However, for writing Shopware tests we focus on `it()` to keep it consistent.

## Commands and assertions [​](#commands-and-assertions)

In Cypress, you use commands and assertions to describe the workflow you want to test.

### Commands [​](#commands)

Commands are the actions you need to do in order to interact with the elements of your application and reproduce the workflow to test in the end.

javascript

```shiki
it('test something', () => {
    ...
    cy.get('.sw-grid__row--0')
        .contains('A Set Name Snippet')
        .dblclick();
    cy.get('.sw-grid__row--0 input')
        .clear()
        .type('Nordfriesisch')
        .click();
    ...
    });
```

You can chain commands by passing its return value to the next one. These commands may contain extra steps to take, e.g. a `click` or `type` operation.

Cypress provides a lot of commands to represent a variety of steps a user could do. On top of that, our E2E testsuite contains a couple of [custom commands](./../../../../../resources/references/testing-reference/e2e-custom-commands/) specially for Shopware.

### Assertions [​](#assertions)

Assertions describe the desired state of your elements, objects and application. Cypress bundles the Chai Assertion Library (including extensions for Sinon and jQuery) and supports both BDD (expect/should) and TDD (assert) style assertions. For consistency reasons, we prefer BDD syntax in Shopware's tests.

javascript

```shiki
it('test something', () => {
    ...
    cy.get('.sw-loader')
        .should('not.exist')
        .should('be.visible')
        .should('not.have.css', 'display', 'none');
    cy.get('div')
        .should(($div) => {
            expect($div).to.have.length(1)
        });
    ...
    });
```

## Hooks [​](#hooks)

You might want to set hooks to run before a set of tests or before each test. At Shopware we use those to e.g. clean up Shopware itself, login to the Administration or to set the admin language.

Cypress got you covered, similar to Mocha, by providing hooks. These can be used to set conditions that you can run before or after a set of tests or each test.

javascript

```shiki
describe('We are using hooks', function() {
  before(function() {
    // runs once before all tests in the block
  })

  beforeEach(function() {
    // runs before each test in the block
  })

  afterEach(function() {
    // runs after each test in the block
  })

  after(function() {
    // runs once after all tests in the block
  })
})
```

### Build up and teardown [​](#build-up-and-teardown)

As we mentioned before, we use these hooks to build up the ideal situation for our test to run. This includes cleaning up the tests' state - based on a clean Shopware installation. According to Cypress' [thoughts on anti-patterns](https://docs.cypress.io/guides/references/best-practices.html#Using-after-or-afterEach-hooks) we clean up the previous state of Shopware beforehand. The reason is pretty simple: You can't be completely sure to reach the `after` hook (sometimes tests may fail), the safer way to cleanup your tests is the `beforeEach` hook. On top of stability advantages, it's possible to stop the tests anytime without manual cleanup.

## Handling test data [​](#handling-test-data)

It's important and necessary the E2E tests are isolated. This means that the test should create itself beforehand, all the data needed for running. Afterwards, state in the database and the browser must be removed completely. This way, the spec avoids dependencies to demo data or data from other tests and cannot be disturbed by those.

One test should only test one workflow, the one it's written for. For example, if you want to test the creation of products, you should not include the creation of categories in your test, although its creation is needed to test the product properly. As best practise we recommend handling everything not related to the test using the [lifecycle hooks](https://docs.cypress.io/guides/core-concepts/writing-and-organizing-tests.html#Hooks) provided by Cypress.

In Shopware platform, we use Shopware's REST API to create the data we need. As a result, our tests are able to focus on one single workflow without having to test the workflows which normally need to be done to provide the data we need. Another aspect of handling it this way is, that creating test data via API is faster than doing it inside the test.

### Cypress' fixtures [​](#cypress-fixtures)

To define the request you send to Shopware and to set first test data, store as `json` file in the folder `e2e/cypress/fixtures`. You can use those files to provide fixed test data which can be used directly to create the desired entity without any further searching or processing. Fortunately, Cypress provides a way to handle those fixtures by default. The command `cy.fixture()` loads this fixed set of data located in a json file.

In the example file below, this file is used in order to define and create a customer. So, it provides data so that the customer can be created in Shopware.

json

```shiki
{
  "customerNumber": "C-1232123",
  "salutation": "Mr",
  "firstName": "Pep",
  "lastName": "Eroni",
  "email": "test@example.com",
  "guest": true,
  "addresses": [
    {
        ...
    }
  ]
}
```

WARNING

Use only fields, which you can access in the UI / Storefront. Keep in mind that all tests in the file may use the fixture. So keep an eye on compatibility.

A small note on ID usage: Using ids may be easier for finding elements, but it isn't a proper way for testing in every case - It depends on your application. You need to be 100% sure that the id is persistent and won't change between builds. Never use ids here if you cannot be 100% sure they will not change at all, e.g. in another build.

INFO

At our case at Shopware, Ids on UUID basis tend to change from one installation to the next, so they are not always suitable to be used as selector in your test.

### API implementation [​](#api-implementation)

Analogue to the Administration itself, the api access of the e2e test is based on [axios](https://www.npmjs.com/package/axios), a promise based HTTP client for the browser and node.js.

Just like the Administration, we use services to access Shopware's REST API. Therefore, we use the ApiService to provide the basic methods for accessing the api. Located in `e2e/cypress/support/service/api.service.js`, ApiService is shared between all repositories and acts as a basis for all your next steps of creating fixtures. That implies that the axios implementation of all important api methods can be found there. This service acts as an interface: Next to the basic functions like get, post etc the request method is specified here as well as some Shopware-related methods which have to be available in all repositories.

INFO

Cypress provides an own axios-based way to handle requests in its command `cy.request`. However, Cypress commands are not real promises, see [Commands are not Promises](https://docs.cypress.io/guides/core-concepts/introduction-to-cypress.html#Commands-Are-Not-Promises). As we aim to parallelize the promises to fetch test data, we use our own implementation instead.

### Services and commands [​](#services-and-commands)

In order to get all test fixture data applied to our Shopware installation, we use services to send the API requests to find, create or update the data we need. To access these services conveniently, we provide custom commands, which we'll cover a bit later. Let's continue with the general things first.

All fixture services can be found in `cypress/support/service/`:

bash

```shiki
service
  |-- administration // this folder stores the Administration channel API services
    `-- <environment>
      `-- test
        `-- e2e
          `-- cypress
            |-- fixture
            |-- admin-api.service.js // Provides all methods which communicate with admin api directly
            `-- fixture.service.js // Provides all methods for general fixture handling
  |-- saleschannel // this one stores the sales channel API services
  `-- api.service.js // axios interface
```

If you want to use all known services, you can access them using custom commands. These commands can be found in `cypress/support/commands/api-commands.js` for general operation and `cypress/support/commands/fixture-commands.js` specifically for fixture handling.

#### Default fixture command [​](#default-fixture-command)

The stationary fixtures mentioned in the paragraph "Cypress' fixtures" can be sent to Shopware's REST API directly: In most cases Shopware does not need any additional data, like IDs or other data already stored in Shopware. That means the request can be sent, and the desired entity can be created immediately: You just need to use the `createDefaultFixture(endpoint, options = [])` command, as seen below:

javascript

```shiki
    beforeEach(() => {
        cy.createDefaultFixture('tax');
    });
```

In this example, a tax rate will be created with the data provided based on the `json` file located in the `fixtures` folder. Let's look at the command in detail:

javascript

```shiki
Cypress.Commands.add('createDefaultFixture', (endpoint, data = {}, jsonPath) => {
    const fixture = new Fixture();
    let finalRawData = {};

    if (!jsonPath) {
        jsonPath = endpoint;
    }

    // Get test data from cy.fixture first
    return cy.fixture(jsonPath).then((json) => {

        // Merge fixed test data with possible custom one
        finalRawData = Cypress._.merge(json, data);

        // Create the fixture using method from fixture service
        return fixture.create(endpoint, finalRawData);
    });
});
```

#### Commands of customised services [​](#commands-of-customised-services)

You will notice soon that some entities need data which has already been created. That means you have to find out specific IDs or employ a completely different handling. In this case, your own service has to be created, located in `e2e/cypress/support/service`. Some examples for these services are:

* Customer
* Sales channel
* Languages
* Products

In most cases, the usage of these services is similar to the basic ones already implemented. There are commands for each of those services provided by our E2E testsuite package. You don't need to define the API endpoint when using those commands. As these services are extending the `FixturesService`, all methods of it can be used in all other services as well.

#### Writing your own customised service [​](#writing-your-own-customised-service)

Let's look at the custom service `shipping.fixture.js`. This service is a rather simple example - It depicts a service in need of some customization for creating a shipping method correctly. With that being said, let's start.

Your `ShippingFixtureService` has to extend the class `AdminFixtureService`. Afterwards, you create a function called `setShippingFixture(userData)` with the parameter `userData` for the data you want to use to create your shipping method. This way, your class should look like this:

javascript

```shiki
const AdminFixtureService = require('../fixture.service.js');

class ShippingFixtureService extends AdminFixtureService {
    setShippingFixture(userData) {
        // Here we're going to create our shipping fixture
    }
}

module.exports = ShippingFixtureService;

global.ShippingFixtureService = new ShippingFixtureService();
```

All custom services hold a distinct method for creating fixtures: First, it's important to collect the necessary data via REST API. This is done by filtering POST requests used in promises. In case of your our `ShippingFixtureService`, you need the ID of the rule you want to use for the availability, and the ID of the delivery time.

javascript

```shiki
 const findRuleId = () => this.search('rule', {
        type: 'equals',
        value: 'Cart >= 0 (Payment)'
    });
 const findDeliveryTimeId = () => this.search('delivery-time', {
    type: 'equals',
    value: '3-4 weeks'
});
```

The responses of these calls are used to provide the missing IDs for your final POST request. At first, we will merge the missing data with the existing data, then create our shipping method:

javascript

```shiki
return Promise.all([
    findRuleId(),
    findDeliveryTimeId()
]).then(([rule, deliveryTime]) => {
    return this.mergeFixtureWithData(userData, {
        availabilityRuleId: rule.id,
        deliveryTimeId: deliveryTime.id
    });
}).then((finalShippingData) => {
    return this.apiClient.post('/shipping-method?_response=true', finalShippingData);
});
```

That's it! There you go: You have successfully created a customised service that sets up a shipping method in Shopware. Actually, we use this service in our platform test to create our shipping method as well. You can find the full service [here](https://github.com/shopwareArchive/e2e-testsuite-platform/blob/master/cypress/support/service/administration/fixture/shipping.fixture.js). So please look at this example to see the whole class.

Below you will find some best practices and tricks we explored to help you with your testing tasks:

* A source of information can be found in FieldCollection of the several EntityDefinition files. All fields belonging to an entity are defined there. For example, if you're searching for customer related data, please search for the `CustomerDefinition` in Shopware platform.
* If you want to extract mandatory data that is not covered by the error message received with the API's response, it's useful to reproduce your workflow manually: E.g. if you need to find out what data is mandatory for creating a customer, try to save an empty one in the Administration. Keep an eye on the developer tools of your browser while doing so, especially on the preview and response section of your request. As you get your response, you can see what data is still missing.
* If you need to set non-mandatory data, reproducing the above mentioned workflow is recommended as well: Even if the error response does not contain a readable error, you can still inspect it: All the relevant information is stored in 'data'. IDs can be found there directly, other relevant data is stored in "attributes".
* Cypress' test runner can help you a lot with inspecting API requests. Just click on the request in the test runner's log to get a full print of it in your console.

## More interesting topics [​](#more-interesting-topics)

* [Unit testing with PHPUnit](./../php-unit.html)
* [Jest unit tests in Shopware's administration](./../jest-admin.html)
* [Jest unit tests in Shopware's storefront](./../jest-storefront.html)

---

## Best practices on writing end-to-end tests

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/cypress-best-practises.html

# Best practices for writing end-to-end tests [​](#best-practices-for-writing-end-to-end-tests)

## Overview [​](#overview)

A typical E2E test can be complex, with many steps that take a lot of time to complete manually. Because of this complexity, E2E tests can be difficult to automate and slow to execute. The following tips can help reduce the cost and pain of E2E testing and still reap the benefits.

Cypress got you covered with their best practices as well: So please also look at their best practices to get to know their patterns:

[Best Practices | Cypress Documentation](https://docs.cypress.io/guides/references/best-practices.html)

WARNING

We strongly recommend following Cypress own best practices as well.

## Amount and prioritization of end-to-end tests [​](#amount-and-prioritization-of-end-to-end-tests)

### Video [​](#video)

When it comes to dividing test types, selecting and prioritizing test cases, and thus designing tests, things get a bit more complicated. We have generally aligned our test strategy with the test pyramid, although not 100%. The pyramid states that end-to-end tests should be written in a few but well chosen test cases because end-to-end tests are slow and expensive.

At [Shopware Community Day](https://scd.shopware.com/en-US/) 2020, we gave a talk on how we approach automated testing in Shopware, how far we have come on this journey, and what we have gained so far:

#### A matter of trust – test - #SCD20 (ENG) - YouTube

To sum it up briefly, the end-to-end tests are slow and thus expensive to maintain. That is why we need a way to prioritize our test cases.

### When should I write an end-to-end test [​](#when-should-i-write-an-end-to-end-test)

DANGER

Cover every possible workflow with E2E tests.

TIP

Use proper prioritization to choose test cases covered by E2E tests.

Due to running times, it is not advisable to cover every single workflow available. The following criteria may help you with that:

* **Cover the most general, most used workflows of a feature**, e.g., CRUD operations. The term "[happy path](https://en.wikipedia.org/wiki/Happy_path)" describes those workflows quite well.
* **Beware the critical path**: Cover those workflows with E2E tests, which are the most vulnerable and would cause the most damage if broken.
* **Avoid duplicate coverage**: E2E tests should only cover what they can, usually big-picture user stories (workflows) that contain many components and views.
  + Sometimes, unit tests are better suited. For example, use an E2E test to test your application's reaction to a failed validation, not the validation itself.

## Workflow-based end-to-end tests [​](#workflow-based-end-to-end-tests)

DANGER

Write the E2E test as you would write unit tests.

TIP

Writing E2E tests in a "workflow-based" manner means writing the test describing a real user's workflow just like a real user would use your application.

A test should be written "workflow-based" - We like to use this word very much because it is simply apt for this purpose. You should always keep your persona and goal of an E2E test in mind. The test is then written from the user's point of view, not from the developer's point of view.

## Structure and scope [​](#structure-and-scope)

### Test scope [​](#test-scope)

DANGER

Write long E2E tests covering lots of workflows and use cases.

TIP

Keep tests as simple as possible. Only test the workflow you explicitly want to test. Ideally, use **one test for one workflow**.

The second most important thing is to test the workflow you explicitly want to test. Any other steps or workflows to get your test running should be done using API operations in the `beforeEach` hook, as we don't want to test them more than once. For example, if you want to test the checkout process, you shouldn't do all the steps, like creating the sales channel, products, and categories, although you need them to process the checkout. Use the API to create these things and let the test just do the checkout.

You need to focus on the workflow to be tested to ensure minimum test runtimes and to get a valid result of your test case if it fails. For this workflow, you have to think like the end-user would do - Focus on the usage of your feature, not technical implementation.

Other examples of steps or workflow to cut off the actual tests are:

* The routines which should only provide the data we need: Just use test fixtures to create this data to have everything available before the test starts.
* Logging in to the Administration: You need it in almost every Administration test, but writing it in all tests is pure redundancy and way more error sensitive.

INFO

This [scope practice](https://docs.cypress.io/guides/references/best-practices.html#Organizing-Tests-Logging-In-Controlling-State) is also mentioned in Cypress best practices as well.

### Focus on stability first [​](#focus-on-stability-first)

DANGER

Design your tests dependent on each other, doing lots of write operations without removing corresponding data.

TIP

Keep tests isolated, enable them to run independently, and restore a clean installation between tests

It is important to focus on stability as the most important asset of a test suite. A flaky test like this can block the continuous deployment pipeline, making feature delivery slower than it needs to be. Moreover, imagine the following case: Tests that fail to deliver deterministic results: Those flaky test is problematic because they won't show valid results anymore, making them useless. After all, you wouldn't trust one any more than you would trust a liar. If you want to find out more on that topic, including solutions, please take a look at this article:

[Flaky tests](https://www.smashingmagazine.com/2021/04/flaky-tests-living-nightmare/)

This was one of the reasons you need stable tests to create value. To achieve that, you have several possibilities. We will introduce you to some of them in the following paragraphs.

Let's start with some easy strategy. Keep tests as simple as possible, and avoid a lot of logic in each one. Think about it this way, the more you do in a test, the more you can go wrong. In addition, by avoiding big tests, you avoid causing load on your application and resource leaks in your environment.

When planning your test cases and structure, always keep your tests isolated from other tests so that they are able to be run in an independent or random order. Don't ever rely on previous tests. You need to test specs in isolation to take control of your application’s state. Every test is supposed to be able to run on its own and independent from any other tests. This is crucial to ensure valid test results. You can realize these using test fixtures to create all data you need beforehand and take care of the cleanup of your application using an appropriate reset method.

## Choosing selectors [​](#choosing-selectors)

DANGER

Choose fuzzy selectors which are prone to change, e.g. xpath.

TIP

Use selectors which won't change often.

XPath selectors are quite fuzzy and rely a lot on the texts, which can change quickly. Please avoid using them as much as possible. If you work in Shopware platform and notice that one selector is missing or not unique enough, just add another one in the form of an additional class.

### Avoid framework specific selectors [​](#avoid-framework-specific-selectors)

DANGER

Choose framework specific syntax as a selector prone to change, e.g. `.btn-primary`.

TIP

Use individual selectors which won't often change, e.g., `.btn-buy`.

Using selectors which rely on a framework specific syntax can be unstable because the framework selectors are prone to change. Instead, you should use individual selectors, which are less likely to change.

html

```shiki
<button class="btn btn-primary btn-buy">Add to cart</button>
```

javascript

```shiki
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('.btn.btn-primary').click();

// ✓ Instead, you should use a shopware specific class like `.btn-buy`.
// (This also remains stable when the button variant is changed to, e.g., `.btn-secondary`.)
cy.get('.btn-buy').click();
```

html

```shiki
<button
    data-toggle="modal"
    data-target="#exampleModal"
    class="btn btn-primary btn-open-settings">
    Open settings modal
</button>
```

javascript

```shiki
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('[data-toggle="modal"]').click();

// ✓ Instead, you should use a shopware specific class like `.btn-open-settings`.
cy.get('.btn-open-settings').click();
```

html

```shiki
<div class="custom-control custom-checkbox">
  <label 
      for="tos" 
      class="checkout-confirm-tos-label custom-control-label">
      I have read and accepted the general terms and conditions.
  </label>
</div>
```

javascript

```shiki
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('.custom-checkbox label').click();

// ✓ Instead, you should use a shopware specific class like `.checkout-confirm-tos-label`.
cy.get('.checkout-confirm-tos-label').click();
```

If there are no suitable selectors available, please add descriptive classes or IDs for your desired elements.

## Waiting in E2E tests [​](#waiting-in-e2e-tests)

DANGER

Waiting for arbitrary time periods, e.g., using `cy.wait(500)`

TIP

Use route aliases or assertions to guard Cypress from proceeding until an explicit condition is met.

Never use fixed waiting times in the form of `.wait(500)` or similar. Using Cypress, you never need to do this. Cypress has a built-in retry-ability in almost every command, so you don't need to wait, e.g., if an element already exists. If you need more than that, we got you covered. Wait for changes in the UI instead, notifications, API requests, etc., via the appropriate assertions. For example, if you need to wait for an element to be visible:

javascript

```shiki
cy.get('.sw-category-tree').should('be.visible');
```

Another useful way for waiting in the Administration is using Cypress possibility to work with [network requests](https://docs.cypress.io/app/guides/network-requests). Here you can let the test wait for a successful API response:

javascript

```shiki
cy.server();

// Route POST requests with matching URL and assign an alias to it
cy.route({
    url: '/api/search/category',
    method: 'post'
}).as('getData');

// Later, you can use the alias to wait for the API response
cy.wait('@getData').then((xhr) => {
    expect(xhr).to.have.property('status', 200);
});
```

INFO

This [best practice](https://docs.cypress.io/guides/references/best-practices#Unnecessary-Waiting) is also mentioned in Cypress best practices as well. Actually, it can be considered a general best practice to avoid flakiness.

## Cypress commands and their queue [​](#cypress-commands-and-their-queue)

DANGER

Using vanilla JavaScript logic alongside cypress commands without further caution

TIP

If you need vanilla Javascript in your test, wrap it in a Cypress `then` or build a custom command to get it queued.

Cypress commands are asynchronous and get queued for execution at a later time. During execution, subjects are yielded from one command to the next, and a lot of helpful Cypress code runs between each command to ensure everything is in order.

This won't happen with Vanilla JS, though. It will be executed immediately. In the worst case, this difference can cause timing issues. So always wrap your vanilla JavaScript code into Cypress commands or `then` in order to make use of Cypress command queue.

WARNING

Concerning Cypress `then`: Even though Cypress commands look like promises, they aren't completely the same. Head over to the [Cypress docs](https://docs.cypress.io/guides/core-concepts/introduction-to-cypress#Commands-Are-Not-Promises) for more information.

---

## Playwright E2E testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/

# Shopware Acceptance Test Suite: Playwright [​](#shopware-acceptance-test-suite-playwright)

[Playwright](https://playwright.dev/) is a powerful tool for end-to-end testing of web applications. It allows you to automate browser interactions, making it ideal for testing the functionality of your [Shopware](https://github.com/shopware/shopware) plugins and themes.

It provides several useful Playwright [fixtures](https://playwright.dev/docs/test-fixtures) to start testing with Shopware right away, including page contexts and [page objects](https://playwright.dev/docs/pom) for Storefront and Administration, API clients, test data creation, and reusable test logic.

---

## Install & Configure

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/install-configure.html

# Overview [​](#overview)

This is a setup guide for the Shopware Acceptance Test Suite (ATS). This section will walk you through initializing a Playwright project, installing the ATS package, and configuring the environment for local testing. Whether you are writing new tests or running existing ones, following these steps ensures your environment is correctly prepared.

## Installation [​](#installation)

Start by creating your own [Playwright](https://playwright.dev/docs/intro) project.

shell

```shiki
npm init playwright@latest
```

Add the package for the Shopware ATS to your project.

shell

```shiki
npm install @shopware-ag/acceptance-test-suite
```

Make sure to install Playwright and its dependencies.

shell

```shiki
npm install
npx playwright install
npx playwright install-deps
```

## Configuration [​](#configuration)

The test suite is designed to test against any Shopware instance with pure API usage. To grant access to the instance under test, you can use the following environment variables. You can choose between two authentication options: **admin user** or **shopware integration** (recommended).

dotenv

```shiki
# .env

APP_URL="<url-to-the-shopware-instance>"

# Authentication via integration
SHOPWARE_ACCESS_KEY_ID="<your-shopware-integration-id>"
SHOPWARE_SECRET_ACCESS_KEY="<your-shopware-integration-secret>"

# Authentication via admin user
SHOPWARE_ADMIN_USERNAME="<administrator-user-name>"
SHOPWARE_ADMIN_PASSWORD="<administrator-user-password>"
```

To ensure Playwright is referencing the correct instance, you can use the same environment variable in your Playwright configuration.

TypeScript

```shiki
// playwright.config.ts

import { defineConfig } from '@playwright/test';

export default defineConfig({
    use: {
        baseURL: process.env['APP_URL'],
 }
});
```

For more information about how to configure your Playwright project, have a look at the [official documentation](https://playwright.dev/docs/test-configuration).

## Mailpit configuration [​](#mailpit-configuration)

Set up your local Mailpit instance by following the instructions at [Mailpit GitHub repository](https://github.com/axllent/mailpit).  
 By default, Mailpit starts a web interface at `http://localhost:8025` and listens for SMTP on port `1025`.  
 Set the `MAILPIT_BASE_URL` environment variable in `playwright.config.ts` to `http://localhost:8025`. You can now run email tests, such as `tests/Mailpit.spec.ts`.

## Usage [​](#usage)

The test suite uses the [extension system](https://playwright.dev/docs/extensibility) of Playwright and can be used as a complete drop-in for Playwright. However, if you also want to add your extensions, the best approach is to create your base test file and use it as the central reference for your test files. Add it to your project root or a specific fixture directory and name it whatever you like.

Make sure to set `"type": "module",` in your `package.json`.

TypeScript

```shiki
// BaseTestFile.ts

import { test as base } from '@shopware-ag/acceptance-test-suite';
import type { FixtureTypes } from '@shopware-ag/acceptance-test-suite';

export * from '@shopware-ag/acceptance-test-suite';

export const test = base.extend<FixtureTypes>({
    
    // Your fixtures 
    
});
```

Within your tests, you can import the necessary dependencies from your base file.

TypeScript

```shiki
// tests/MyFirstTest.spec.ts

import { test, expect } from './../BaseTestFile';

test('My first test scenario.', async ({ AdminApiContext, DefaultSalesChannel }) => {
    
    // Your test logic
    
});
```

In the example above, you can see two Shopware-specific fixtures that are used in the test, `AdminApiContext` and `DefaultSalesChannel`. Every fixture can be used as an argument within the test method. Read more about available [fixtures](./fixtures.html) in the following section.

---

## Deployment

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/deployment.html

# Deployment Process [​](#deployment-process)

To deploy a new version of the ATS, follow the steps below:

1. **Create a Pull Request**  
    Open a new pull request with your changes. Ensure that all commits follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to support automated versioning and changelog generation.
2. **Approval and Merge**  
    Once the pull request has been reviewed and approved, merge it into the main branch.
3. **Automated Deployment PR Creation**  
    After the merge, the [`release-please`](https://github.com/googleapis/release-please) tool will automatically open a new pull request. This deployment PR will include version bumps and a generated changelog.
4. **Review and Approve the Deployment PR**  
    The deployment pull request requires an additional approval before it can be merged.
5. **Merge the Deployment PR**  
    Once the deployment PR is approved and merged, a new release of the ATS will be created in the GitHub repository. This action will also publish a new package version to NPM under [@shopware-ag/acceptance-test-suite](https://www.npmjs.com/package/@shopware-ag/acceptance-test-suite).
6. **Use the New Version**  
    After a short delay, the newly published version will be available on NPM. You can then reference it in your project folders as needed.

## Troubleshooting [​](#troubleshooting)

If you encounter any issues with the automated deployment process, please check the following [troubleshooting page of release-please](https://github.com/googleapis/release-please?tab=readme-ov-file#release-please-bot-does-not-create-a-release-pr-why).

In most cases, the problem is related to the commit messages not following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. Make sure to check your commit messages and rebase your branch if necessary. If your PR is merged with a commit message that does not follow the specification, you can do the following:

* **Create an empty commit to the main branch**

  bash

  ```shiki
      git commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"
  ```

  When a commit to the main branch has Release-As: x.x.x (case-insensitive) in the commit body, Release Please will open a new pull request for the specified version.
* **Push the changes**

  bash

  ```shiki
    git push origin <your-branch>
  ```
* **Adjust the release notes** Remember to adjust the release notes in the deployment PR.

---

## Fixtures

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/fixtures.html

# General fixtures [​](#general-fixtures)

## DefaultSalesChannel [​](#defaultsaleschannel)

We try to encapsulate test execution within the system under test and make tests as deterministic as possible. The idea is to create a separate sales channel for testing purposes within the standard Storefront. The `DefaultSalesChannel` fixture is worker-scoped and is there to achieve exactly that. Using it will provide you with a new sales channel with default settings, including a default Storefront customer.

### Properties [​](#properties)

* `salesChannel`: The Shopware sales channel reference.
* `customer`: A default Storefront customer reference.
* `url`: The url to the sales channel Storefront.

## AdminApiContext [​](#adminapicontext)

This context provides a ready-to-use client for the Admin-API of Shopware. It is based on the standard Playwright [APIRequestContext](https://playwright.dev/docs/api/class-apirequestcontext), but will handle authentication for you, so you can start making API requests to the Shopware instance under test right away. You can use it, for example, for test data creation or API testing. Learn more about the usage of the Shopware Admin-API in the [API documentation](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide).

### Methods [​](#methods)

* `get`
* `post`
* `patch`
* `delete`
* `fetch`
* `head`

### Usage [​](#usage)

TypeScript

```shiki
import { test, expect } from './../BaseTestFile';

test('Property group test scenario', async ({ AdminApiContext }) => {

    const response = await AdminApiContext.post('property-group?_response=1', {
        data: {
            name: 'Size',
            description: 'Size',
            displayType: 'text',
            sortingType: 'name',
            options: [{
                name: 'Small',
 }, {
                name: 'Medium',
 }, {
                name: 'Large',
 }],
 },
 });

    expect(response.ok()).toBeTruthy();
});
```

## StoreApiContext [​](#storeapicontext)

This context provides a ready-to-use client for the Store-API of Shopware and is based on the standard Playwright [APIRequestContext](https://playwright.dev/docs/api/class-apirequestcontext). You can do API calls on behalf of a Storefront user. Learn more about the usage of the Shopware Store-API in the [documentation](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide).

Note that, other than the AdminApiContext, the StoreApiContext won't do an automated login of the shop customer. This is because a Storefront user isn't always a registered user by default, and you might want to test this behaviour explicitly. You can use the `login` method to log in as a registered shop customer.

### Methods [​](#methods-1)

* `login(user)`: Does a login of a customer and stores the login state for future requests.
* `get`
* `post`
* `patch`
* `delete`
* `fetch`
* `head`

### Usage [​](#usage-1)

TypeScript

```shiki
import { test, expect } from './../BaseTestFile';

test('Store customer test scenario', async ({ StoreApiContext, DefaultSalesChannel }) => {

    // Login as the default customer.
    await StoreApiContext.login(DefaultSalesChannel.customer);

    // Create a new cart for the customer.
    const response = await StoreApiContext.post('checkout/cart', {
        data: { name: 'default-customer-cart' },
 });

    expect(response.ok()).toBeTruthy();
});
```

## AdminPage [​](#adminpage)

This fixture provides a Playwright [page](https://playwright.dev/docs/api/class-page) context for the Shopware Administration. It creates a new admin user with an authenticated session. You can start testing within the Administration using this page right away.

### Usage [​](#usage-2)

TypeScript

```shiki
import { test, expect } from './../BaseTestFile';

test('Shopware admin test scenario', async ({ AdminPage }) => {

    await AdminPage.goto('#/sw/product/index');
    await expect(AdminPage.locator('.sw-product-list__add-physical-button')).toBeVisible();
});
```

Note that this is just a very rough example. In most cases, you won't use this page context directly, but maybe a [page-object](#page-objects) using this page.

## StorefrontPage [​](#storefrontpage)

This fixture provides a Playwright [page](https://playwright.dev/docs/api/class-page) context for the Shopware Storefront of the default sales channel.

## Add new fixtures [​](#add-new-fixtures)

To add new general fixtures, create them inside the `src/fixtures` folder. Keep in mind that you need to merge your new fixture inside the `/src/index.ts` file.

---

## Page Objects

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/page-object.html

# Page Objects [​](#page-objects)

Page objects can be helpful to simplify the usage of element selectors and make them available in a reusable way. They help you to organize page-specific locators and provide helpers for interacting with a given page. Within our test suite, we try to keep the page objects very simple and not add too much logic to them. So most of the page objects resemble just a collection of element locators and maybe some little helper methods.

There are several page objects to navigate the different pages of the Administration and Storefront. You can use them as any other fixture within your test. There is also a guide on page objects in the [official Playwright documentation](https://playwright.dev/docs/pom).

## Usage [​](#usage)

TypeScript

```shiki
import { test, expect } from './../BaseTestFile';

test('Storefront cart test scenario', async ({ StorefrontPage, StorefrontCheckoutCart }) => {

    await StorefrontPage.goto(StorefrontCheckoutCart.url());
    await expect(StorefrontCheckoutCart.grandTotalPrice).toHaveText('€100.00*');
});
```

You can get an overview of all available page objects in the [repository](https://github.com/shopware/acceptance-test-suite/tree/trunk/src/page-objects) of this test suite.

## Page Object module [​](#page-object-module)

The `modules` folder is designed to house reusable utility functions that operate on a `Page` object (from Playwright). These functions dynamically interact with different browser pages or contexts using the `page` parameter. For example, utility functions like `getCustomFieldCardLocators` or `getSelectFieldListitem` are used across multiple page objects to handle specific functionality (e.g., managing custom fields or select field list items). Centralizing these utilities in the `modules` folder improves code organization, readability, and reduces duplication. Create a new class inside a module when it helps to streamline the codebase and avoid repetitive logic across page objects.

You can find how `getCustomFieldCardLocators` is defined in the [modules folder](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/page-objects/administration/modules/CustomFieldCard.ts) and used in other [page object classes](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/page-objects/administration/ProductDetail.ts).

## Add new Page Objects [​](#add-new-page-objects)

Page objects are organized mainly by their usage in the Administration or Storefront. To add a new page object, simply add it to the respective subfolder and reference it in `AdministrationPages.ts` or `StorefrontPages.ts`.

### Usage [​](#usage-1)

TypeScript

```shiki
import { test as base } from '@playwright/test';
import type { FixtureTypes } from '../types/FixtureTypes';

import { ProductDetail } from './administration/ProductDetail';
import { OrderDetail } from './administration/OrderDetail';
import { CustomerListing } from './administration/CustomerListing';
// [...]
import { MyNewPage } from './administration/MyNewPage';

export interface AdministrationPageTypes {
    AdminProductDetail: ProductDetail;
    AdminOrderDetail: OrderDetail;
    AdminCustomerListing: CustomerListing;
    // [...]
    AdminMyNewPage: MyNewPage;
}

export const AdminPageObjects = {
    ProductDetail,
    OrderDetail,
    CustomerListing,
    // [...]
    MyNewPage,
}
```

---

## Actor Pattern

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/actor-pattern.html

# Actor pattern [​](#actor-pattern)

The actor pattern is a basic concept that we added to our test suite. It is something not related to Playwright, but similar concepts exist in other testing frameworks. We implemented it to create reusable test logic that can be used in a human-readable form, without abstracting away Playwright as a framework. So you are free to use it or not. Any standard Playwright functionality will still be usable in your tests.

The concept adds two new entities besides the already mentioned [page objects](./page-object.html)

* **Actor**: A specific user with a given context performing actions (tasks) inside the application.
* **Task**: A specific action performed by an actor.
* **Pages**: A page of the application on which an actor performs a task.

## Actors [​](#actors)

The Actor class is a lightweight solution to simplify the execution of reusable test logic or navigate to a specific page.

## Properties [​](#properties)

* `name`: The human-readable name of the actor.
* `page`: A Playwright page context that the actor is navigating.

## Primary methods [​](#primary-methods)

* `goesTo`: Accepts a URL of a page the actor should navigate to.
* `attemptsTo`: Accepts a "task" function with reusable test logic that the actor should perform.
* `expects`: A one-to-one export of the Playwright `expect` method to use it in the actor pattern.

These methods lead to the following pattern:

* The **actor** *goes to* a **page**.
* The **actor** *attempts to* perform a certain **task**.
* The **actor** *expects* a certain result.

Translated into test code, this pattern can look like this:

typescript

```shiki
import { test } from "./../BaseTestFile";

test("Product detail test scenario", async ({
  ShopCustomer,
  StorefrontProductDetail,
  TestDataService,
}) => {
  const product = await TestDataService.createBasicProduct();

  await ShopCustomer.goesTo(StorefrontProductDetail.url(product));
  await ShopCustomer.attemptsTo(AddProductToCart(product));
  await ShopCustomer.expects(
    StorefrontProductDetail.offCanvasSummaryTotalPrice
  ).toHaveText("€99.99*");
});
```

In this example, you can see that this pattern creates very comprehensible tests, even for non-tech people. They also make it easier to abstract simple test logic that might be used in different scenarios into executable tasks, like adding a product to the cart.

The test suite offers two different actors by default:

* `ShopCustomer`: A user that is navigating the Storefront.
* `ShopAdmin`: A user who manages Shopware via the Administration.

## Accessibility methods [​](#accessibility-methods)

* `a11y_checks`: Accepts a locator and verifies if the desired locator is both focused and displays a visible focus indicator. This is automatically called via `presses`, `fillsIn`, and `selectsRadioButton`.
* `presses`: An extension of the Playwright `press` method to include `a11y_checks` as well as automatically apply a keyboard key press per default browser keyboard mappings (which can also be overridden). A keyboard focused alternative to the Playwright `click` method.
* `fillsIn`: An extension of the Playwright `fill` method to include `a11y_checks`.
* `selectsRadioButton`: Selects radio buttons using keyboard navigation in addition to verifying visible focus (via `presses`).

These methods serve as a way to enforce better accessibility practices by using keyboard navigation and checking for visible focus indicators (both of which are WCAG requirements). They can be used both in tests and tasks.

INFO

Be aware that the Playwright `click` method automatically includes a number of [actionability checks](https://playwright.dev/docs/actionability) to combat flakiness. When utilizing the Actor accessibility methods, you may need to adjust your tests to individually assert some of these actionability checks for certain locators yourself.

## Tasks [​](#tasks)

Tasks are small chunks of reusable test logic that can be passed to the `attemptsTo` method of an actor. They are created via Playwright fixtures and have access to the same dependencies. Every executed task will automatically be wrapped in a test step of Playwright, so you get nicely structured reports of your tests.

**Example**

typescript

```shiki
import { test as base } from "@playwright/test";
import type { Task } from "../../../types/Task";
import type { FixtureTypes } from "../../../types/FixtureTypes";
import type { Customer } from "../../../types/ShopwareTypes";

export const Login = base.extend<{ Login: Task }, FixtureTypes>({
  Login: async (
    {
      ShopCustomer,
      DefaultSalesChannel,
      StorefrontAccountLogin,
      StorefrontAccount,
    },
    use
  ) => {
    const task = (customCustomer?: Customer) => {
      return async function Login() {
        const customer = customCustomer
          ? customCustomer
          : DefaultSalesChannel.customer;

        await ShopCustomer.goesTo(StorefrontAccountLogin.url());

        await ShopCustomer.fillsIn(
          StorefrontAccountLogin.emailInput,
          customer.email
        );
        await ShopCustomer.fillsIn(
          StorefrontAccountLogin.passwordInput,
          customer.password
        );
        await ShopCustomer.presses(StorefrontAccountLogin.loginButton);

        await ShopCustomer.expects(
          StorefrontAccount.personalDataCardTitle
        ).toBeVisible();
      };
    };

    await use(task);
  },
});
```

This fixture is the "Login" task and performs a simple Storefront login of the default customer via keyboard navigation (automatically includes `a11y_checks` assertions). Every time we need a logged-in shop customer, we can simply reuse this logic in our test.

typescript

```shiki
import { test } from "./../BaseTestFile";

test("Customer login test scenario", async ({ ShopCustomer, Login }) => {
  await ShopCustomer.attemptsTo(Login());
});
```

**Example**

typescript

```shiki
import type { Page, Locator } from "playwright-core";
import type { PageObject } from "../../types/PageObject";

export class CheckoutConfirm implements PageObject {
  public readonly paymentMethodRadioGroup: Locator;
  public readonly page: Page;

  constructor(page: Page) {
    this.page = page;
    this.paymentMethodRadioGroup = page.locator(".checkout-card", {
      hasText: "Payment Method",
    });
  }

  url() {
    return "checkout/confirm";
  }
}
```

This page object defines the payment method radio group locator.

typescript

```shiki
import { test as base } from "@playwright/test";
import type { Task } from "../../../types/Task";
import type { FixtureTypes } from "../../../types/FixtureTypes";

export const SelectPaymentMethod = base.extend<
  { SelectPaymentMethod: Task },
  FixtureTypes
>({
  SelectPaymentMethod: async (
    { ShopCustomer, StorefrontCheckoutConfirm },
    use
  ) => {
    const task = (paymentOptionName: string) => {
      return async function SelectPaymentMethod() {
        const paymentMethods =
          StorefrontCheckoutConfirm.paymentMethodRadioGroup;
        const paymentOptionRadioButton = paymentMethods.getByRole("radio", {
          name: paymentOptionName,
        });

        await ShopCustomer.selectsRadioButton(
          paymentMethods,
          paymentOptionName
        );
        await ShopCustomer.expects(paymentOptionRadioButton).toBeChecked();
      };
    };

    await use(task);
  },
});
```

This fixture is the "SelectPaymentMethod" task, which selects the desired payment method radio button using keyboard navigation (automatically includes `a11y_checks` assertions).

typescript

```shiki
import { test } from "./../BaseTestFile";

test("Customer successfully orders product", async ({
  ShopCustomer,
  TestDataService,
  Login,
  StorefrontProductDetail,
  AddProductToCart,
  ProceedFromProductToCheckout,
  SelectPaymentMethod,
  ConfirmOrder,
}) => {
  const product = await TestDataService.createBasicProduct();
  await ShopCustomer.attemptsTo(Login());
  await ShopCustomer.goesTo(StorefrontProductDetail.url(product));
  await ShopCustomer.attemptsTo(AddProductToCart(product));
  await ShopCustomer.attemptsTo(ProceedFromProductToCheckout());
  await ShopCustomer.attemptsTo(SelectPaymentMethod("Invoice"));
  await ShopCustomer.attemptsTo(ConfirmOrder());
});
```

To use "SelectPaymentMethod" in a test, you simply pass the name of the desired payment option. Here is a sample scenario for a successful checkout that shows how you can combine multiple tasks to build your test scenarios.

You can create your tasks in the same way to make them available for the actor pattern. Every task is just a simple Playwright fixture containing a function call with the corresponding test logic. Make sure to merge your task fixtures with other fixtures you created in your base test file. You can use the `mergeTests` method of Playwright to combine several fixtures into one test extension. Use `/src/tasks/shop-customer-tasks.ts` or `/src/tasks/shop-admin-tasks.ts` for that.

To keep tests easily readable, use names for your tasks so that in the test itself, the code line resembles the `Actor.attemptsTo(doSomething)` pattern as closely as possible.

**Example**

typescript

```shiki
// Bad example
await ShopCustomer.attemptsTo(ProductCart);

// Better example
await ShopCustomer.attemptsTo(PutProductIntoCart);
```

---

## Test Suite Types

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test-suite-types.html

# Types in the Test Suite [​](#types-in-the-test-suite)

The Shopware Acceptance Test Suite leverages TypeScript’s static typing to ensure that test data structures, API interactions, and test logic are consistent and error-resistant.

## Shopware Types [​](#shopware-types)

The centralized type definition file, [ShopwareTypes.ts](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/types/ShopwareTypes.ts) is tightly coupled with the TestDataService, which defines the shape and default data of all supported Shopware entities. Each supported entity such as Product, Customer, Media, etc is defined with its properties and default values. These types are then referenced throughout the [`TestDataService`](./test-data-service.html) to provide IntelliSense, validation, and consistent data structures.

typescript

```shiki
export type ProductReview = components['schemas']['ProductReview'] & {
 id: string,
 productId: string,
 salesChannelId: string,
 title: string,
 content: string,
 points: number,
}
```

Within that example above, you are importing the auto-generated type for `ProductReview` from the Shopware Admin API OpenAPI schema and extending it with additional or overridden fields using `& { ... }`.

Sometimes, you might want to remove fields from a type. TypeScript provides the `Omit<T, K>` utility to exclude fields from a type:

typescript

```shiki
export type Country = Omit<components['schemas']['Country'], 'states'> & {
 id: string,
 states: [{
 name: string,
 shortCode: string,
 }],
}
```

For custom use cases, simply define a custom type:

typescript

```shiki
export type CustomShippingMethod = {
 name: string;
 active: boolean;
 deliveryTimeId: string;
}
```

---

## Test Suite

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test.html

# Testing within the Test Suite [​](#testing-within-the-test-suite)

The `tests` folder ensures the reliability of the testing framework by validating the functionality of tools and data used in tests. Add tests to verify any new features or changes you introduce:

* **Page Objects**: Ensure they are correctly implemented and interact with the application as expected, including navigation, element visibility, and user interactions.
* **TestDataService Methods**: Verify that methods for creating, getting, and cleaning up test data (e.g., products, customers, orders) work correctly and produce consistent results.

TypeScript

```shiki
//Example for page objects

await ShopAdmin.goesTo(AdminManufacturerCreate.url());
await ShopAdmin.expects(AdminManufacturerCreate.nameInput).toBeVisible();
await ShopAdmin.expects(AdminManufacturerCreate.saveButton).toBeVisible();
```

TypeScript

```shiki
//Example for TestDataService

const product = await TestDataService.createProductWithImage({ description: 'Test Description' });
expect(product.description).toEqual('Test Description');
expect(product.coverId).toBeDefined();
```

## Running tests in the Test Suite [​](#running-tests-in-the-test-suite)

To work on the test suite and execute tests from within this repository, you must run a corresponding Docker image for the specific Shopware version.

We publish pre-built images at the [GitHub container registry](https://github.com/shopware/acceptance-test-suite/pkgs/container/acceptance-test-suite%2Ftest-image). The images are built daily; check to see which versions are available.

To select an image, export the corresponding tag as `SHOPWARE_VERSION` and start the containers:

bash

```shiki
SHOPWARE_VERSION=trunk docker compose up --wait shopware
```

What if the version I would like to test is not available as a pre-built image?

If you want to test with an image that's not available already, you can build it yourself by exporting a few more variables:

bash

```shiki
export PHP_VERSION="8.3" # PHP version of the base image
export SHOPWARE_VERSION="v6.5.8.0" # Shopware version to check out. This may be either a branch or a tag, depending on the value of SHOPWARE_BUILD_SOURCE
export SHOPWARE_BUILD_SOURCE="tag" # Either "branch" or "tag"

docker compose up --attach-dependencies shopware # This will build the image if it's not available
```

Afterwards, you can execute the normal playwright commands:

bash

```shiki
npx playwright test --ui
```

---

## Local development

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/local-development.html

# Local development with ATS [​](#local-development-with-ats)

To work locally with ATS and your development setup, follow these steps:

## Create your Page Objects and TestDataService methods [​](#create-your-page-objects-and-testdataservice-methods)

In the ATS repository ([shopware/acceptance-test-suite](https://github.com/shopware/acceptance-test-suite)), create or modify your custom page objects, `TestDataService` methods, or any related files.

After making your changes, build the project by running the following command in the ATS repository:

bash

```shiki
npm run build
```

This will generate the necessary artifacts in the `dist` folder.

Copy the generated artifacts (e.g., all files in the `dist` folder) from the ATS repository to your local Shopware instance's `node_modules` folder, specifically under the ATS package path:

bash

```shiki
cp -R dist/* <path-to-your-shopware-instance>/tests/acceptance/node_modules/@shopware-ag/acceptance-test-suite/dist
```

### Adjust tests, Page Objects, and methods [​](#adjust-tests-page-objects-and-methods)

In your Shopware instance, adjust any tests, page objects, `TestDataService` methods, or other related files to align them with the changes made in the ATS repository.

### Run the tests [​](#run-the-tests)

Execute the tests to verify your changes. Use the following command from your Shopware project's acceptance test directory:

bash

```shiki
cd tests/acceptance
npx playwright test --ui
```

This will launch the Playwright Test Runner UI, where you can select and run specific tests. By following these steps, you can work locally with the ATS and test your changes in your Shopware instance.

---

## Language Agnostic Testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/language-agnostic-testing.html

# Language Agnostic Testing [​](#language-agnostic-testing)

Language agnostic testing in @shopware-ag/acceptance-test-suite allows you to write acceptance tests that work across different languages without hard-coding text strings. Tests use translation keys instead of hard-coded strings and automatically adapt to different locales via environment variables.

## translate() Function [​](#translate-function)

Use the `translate()` function in page objects to replace hardcoded strings with translation keys.

### Usage in Page Objects [​](#usage-in-page-objects)

typescript

```shiki
import { translate } from '../../services/LanguageHelper';

export class CategoryListing implements PageObject {
    constructor(page: Page) {
        this.createButton = page.getByRole('button', {
            name: translate('administration:category:actions.createCategory'),
        });
    }
}
```

## Translate Fixture [​](#translate-fixture)

The `Translate` fixture provides translation functionality in tests.

### Usage in Tests [​](#usage-in-tests)

typescript

```shiki
import { test, expect } from '@shopware-ag/acceptance-test-suite';

test('Category creation', async ({ AdminPage, Translate }) => {
    const saveText = Translate('administration:category:general.save');
    await AdminPage.getByRole('button', { name: saveText }).click();
});
```

## Environment Control [​](#environment-control)

Switch test language using environment variables:

bash

```shiki
LANG=de-DE npm run test  # German
LANG=en-GB npm run test  # English (default)
```

## Translation Keys [​](#translation-keys)

Translation keys follow the pattern: `area:module:section.key`

### Examples [​](#examples)

typescript

```shiki
'administration:category:general.save';
'administration:category:actions.createCategory';
'storefront:account:fields.firstName';
'storefront:checkout:payment.invoice';
```

### Locale Files [​](#locale-files)

Translations are stored in JSON files organized by language and area:

* `locales/en/administration/category.json`
* `locales/de/administration/category.json`
* `locales/en/storefront/account.json`
* `locales/de/storefront/account.json`

### Example Translation Files [​](#example-translation-files)

**English (`locales/en/administration/category.json`):**

json

```shiki
{
    "general": {
        "save": "Save",
        "cancel": "Cancel"
    },
    "actions": {
        "createCategory": "Create category"
    }
}
```

**German (`locales/de/administration/category.json`):**

json

```shiki
{
    "general": {
        "save": "Speichern",
        "cancel": "Abbrechen"
    },
    "actions": {
        "createCategory": "Kategorie erstellen"
    }
}
```

## Supported Locales [​](#supported-locales)

**Translation Resources**: `en` (English), `de` (German)  
**Browser UI**: `en`, `de`, `fr`, `es`, `it`, `nl`, `pt`

## Common Issues [​](#common-issues)

**Translation key not found:**

* Verify key exists in both EN/DE locale files
* Check import in `locales/index.ts`
* Ensure proper namespace structure

**Tests fail with LANG changes:**

* Move `translate()` calls inside constructors/functions, not at module level
* Ensure translation resources are properly loaded

**JSON import errors:**

* Always use `with { type: 'json' }` import attribute
* Check file paths and naming conventions

**Browser locale not matching:**

* Verify locale mapping in `playwright.config.ts`
* Check browser args configuration
* Ensure language detection is working correctly

## Using in Your Own Project [​](#using-in-your-own-project)

If you want to use the `@shopware-ag/acceptance-test-suite` in your own project with custom translations, you can extend the base test suite with your own translation fixture.

### Installation [​](#installation)

First, install the required dependencies:

bash

```shiki
npm install @shopware-ag/acceptance-test-suite @playwright/test
npm install -D @types/node
```

### Create Custom Translation Fixture [​](#create-custom-translation-fixture)

Create a new fixture file (e.g., `fixtures/CustomTranslation.ts`):

typescript

```shiki
import {
    test as base,
    LanguageHelper,
    TranslationKey,
    TranslateFn,
    BUNDLED_RESOURCES,
    baseNamespaces,
} from '@shopware-ag/acceptance-test-suite';
import { LOCALE_RESOURCES, enNamespaces } from '../locales';

// Merge base BUNDLED_RESOURCES with your custom LOCALE_RESOURCES
const MERGED_RESOURCES = {
    en: { ...BUNDLED_RESOURCES.en, ...LOCALE_RESOURCES.en },
    de: { ...BUNDLED_RESOURCES.de, ...LOCALE_RESOURCES.de },
} as const;

// Merge base and custom namespaces
const mergedNamespaces = {
    ...baseNamespaces,
    ...enNamespaces,
} as const;

type CustomTranslationKey = TranslationKey<typeof mergedNamespaces>;

interface CustomTranslateFixture {
    Translate: TranslateFn<CustomTranslationKey>;
}

export const test = base.extend<CustomTranslateFixture>({
    Translate: async ({}, use) => {
        let lang = process.env.lang || process.env.LANGUAGE || process.env.LANG || 'en';
        let language = lang.split(/[_.-]/)[0].toLowerCase();

        if (!MERGED_RESOURCES[language as keyof typeof MERGED_RESOURCES]) {
            console.warn(
                `⚠️  Translation resources for '${language}' not available. Supported: ${Object.keys(
                    MERGED_RESOURCES
                ).join(', ')}. Falling back to 'en'.`
            );
            language = 'en';
        }

        const languageHelper = await LanguageHelper.createInstance(
            language,
            MERGED_RESOURCES as unknown as typeof BUNDLED_RESOURCES
        );

        const translate: TranslateFn<CustomTranslationKey> = (key, options) => {
            return languageHelper.translate(key as TranslationKey, options);
        };

        await use(translate);
    },
});

export * from '@shopware-ag/acceptance-test-suite';
export type { CustomTranslationKey };
```

### Create Locale Files Structure [​](#create-locale-files-structure)

Organize your translation files by language and area:

text

```shiki
project-root/
├── locales/
│   ├── en/
│   │   ├── administration/
│   │   │   ├── common.json
│   │   │   └── product.json
│   │   └── storefront/
│   │       ├── account.json
│   │       └── checkout.json
│   ├── de/
│   │   ├── administration/
│   │   │   ├── common.json
│   │   │   └── product.json
│   │   └── storefront/
│   │       ├── account.json
│   │       └── checkout.json
│   └── index.ts
├── fixtures/
│   └── CustomTranslation.ts
├── types/
│   └── TranslationTypes.ts
└── tests/
    └── your-test.spec.ts
```

### Create Locales Index [​](#create-locales-index)

Create `locales/index.ts` to import and export your translation files:

typescript

```shiki
// Import all locale files
import enAdministrationCommon from './en/administration/common.json' with { type: 'json' };
import enStorefrontAccount from './en/storefront/account.json' with { type: 'json' };

import deAdministrationCommon from './de/administration/common.json' with { type: 'json' };
import deStorefrontAccount from './de/storefront/account.json' with { type: 'json' };

// Export the bundled resources for i18next
export const LOCALE_RESOURCES = {
    en: {
        'administration/common': enAdministrationCommon,
        'storefront/account': enStorefrontAccount,
    },
    de: {
        'administration/common': deAdministrationCommon,
        'storefront/account': deStorefrontAccount,
    },
} as const;

export const enNamespaces = {
    administration: {
        common: enAdministrationCommon,
    },
    storefront: {
        account: enStorefrontAccount,
    },
} as const;
```

### Create Translation Types [​](#create-translation-types)

Create `types/TranslationTypes.ts` to define your custom translation types. This provides:

* **Type Safety**: Ensures translation keys exist in your locale files
* **IntelliSense**: Auto-completion for available translation keys
* **Compile-time Validation**: Catches typos and missing keys before runtime

typescript

```shiki
import { TranslationKey, TranslateFn } from '@shopware-ag/acceptance-test-suite';
import { enNamespaces } from '../locales';

export type CustomTranslationKey = TranslationKey<typeof enNamespaces>;

export type CustomTranslateFn = TranslateFn<CustomTranslationKey>;
```

### Merge with Base Test Suite [​](#merge-with-base-test-suite)

Create your main test fixture that merges the base test suite with your custom translation:

typescript

```shiki
import { test as ShopwareTestSuite, mergeTests } from '@shopware-ag/acceptance-test-suite';
import { test as CustomTranslation } from './fixtures/CustomTranslation';

export * from '@shopware-ag/acceptance-test-suite';

export const test = mergeTests(ShopwareTestSuite, CustomTranslation);
```

**Note**: Save this as `test.ts` or `index.ts` in your project root and import it in your test files.

### Usage in Your Tests [​](#usage-in-your-tests)

Now you can use the `Translate` fixture in your tests:

typescript

```shiki
import { test } from './your-main-test-fixture';

test('My localized test', async ({ Translate, AdminPage }) => {
    const saveText = Translate('administration:common:button.save');
    await AdminPage.getByRole('button', { name: saveText }).click();
});
```

### Environment Configuration [​](#environment-configuration)

Set up your Playwright configuration to support language switching:

typescript

```shiki
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const LOCALES = { de: 'de-DE', en: 'en-US', fr: 'fr-FR' };

function getLanguage(): string {
    let lang = process.env.lang || process.env.LANGUAGE || process.env.LANG || 'en';
    return lang.split(/[_.-]/)[0].toLowerCase();
}

function getLocaleConfig() {
    const lang = getLanguage();
    const browserLocale = LOCALES[lang as keyof typeof LOCALES] || 'en-US';
    const browserArgs =
        lang !== 'en' && LOCALES[lang as keyof typeof LOCALES]
            ? [`--lang=${browserLocale}`, `--accept-lang=${browserLocale},${lang};q=0.9,en;q=0.8`]
            : [];

    return { lang, browserLocale, browserArgs };
}

export default defineConfig({
    use: {
        locale: getLocaleConfig().browserLocale,
    },
    projects: [
        {
            name: 'Platform',
            use: {
                ...devices['Desktop Chrome'],
                launchOptions: {
                    args: [...getLocaleConfig().browserArgs],
                },
            },
        },
    ],
});
```

### Running Tests with Different Languages [​](#running-tests-with-different-languages)

bash

```shiki
# German
LANG=de-DE npx playwright test

# English (default)
npx playwright test
```

---

## Test Data Service

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test-data-service.html

# Services [​](#services)

The test suite provides several services that can be used to simplify your test code. These services are designed to be reusable and can be easily extended to fit your specific needs.

## Test Data Service [​](#test-data-service)

The `TestDataService` is a powerful utility designed to simplify test data creation, management, and cleanup when writing acceptance and API tests for Shopware. It provides ready-to-use functions for common data needs and ensures reliable, isolated test environments. For detailed documentation of the methods, you can have a look at the [service class](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/services/TestDataService.ts) or use the auto-completion of your IDE.

## When to use the TestDataService in tests [​](#when-to-use-the-testdataservice-in-tests)

You should use the `TestDataService` whenever you need **test data** that matches common Shopware structures, such as:

* Creating a **basic product**, **customer**, **order**, **category**, etc
* Setting up **media** resources like product images or digital downloads
* Creating **promotions**, **rules**, or **payment/shipping methods**
* Fetching existing entities via helper methods (`getCurrency()`, `getShippingMethod()`, etc)
* **Assigning relations** between entities (e.g., linking a product to a category)

### Typical examples [​](#typical-examples)

typescript

```shiki
const product = await TestDataService.createBasicProduct();
const customer = await TestDataService.createCustomer();
const shipping = await TestDataService.createBasicShippingMethod();
```

## When and why to extend the `TestDataService` [​](#when-and-why-to-extend-the-testdataservice)

You should add new functions to the `TestDataService` (or extend it) when:

* Your project or plugin introduces **new entity types** (e.g., `CommercialCustomerGroup`, `CustomProductType`)
* You need a **specialized creation logic** (e.g., a shipping method with multiple rules, a pre-configured product bundle)
* Existing methods require **modifications** that should not affect the core service
* You want to **reuse the same setup across multiple tests** without duplicating logic
* You require **special cleanup handling** for newly created entities

Using and extending the `TestDataService` properly ensures your acceptance tests stay **readable**, **maintainable**, and **scalable** even as your Shopware project grows.

## Available `create*` methods in `TestDataService` [​](#available-create-methods-in-testdataservice)

These methods are designed to streamline the setup of test data, ensuring consistency and efficiency in your testing processes. They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `createBasicProduct(): Promise<Product>`
* `createVariantProducts(parentProduct: Product, propertyGroups: PropertyGroup[]): Promise<Product[]>`
* `createCustomer(): Promise<Customer>`
* `createCustomerGroup(): Promise<CustomerGroup>`
* `createOrder(lineItems: SimpleLineItem[], customer: Customer): Promise<Order>`
* `createCategory(): Promise<Category>`
* `createColorPropertyGroup(): Promise<PropertyGroup>`
* `createBasicPaymentMethod(): Promise<PaymentMethod>`
* `createBasicShippingMethod(): Promise<ShippingMethod>`
* [...]

## Available `assign*` methods in `TestDataService` [​](#available-assign-methods-in-testdataservice)

These methods are designed to establish associations between entities, such as linking products to categories or assigning media to manufacturers, ensuring that your test data reflects realistic scenarios. They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `assignProductCategory(productId: string, categoryIds: string[]): Promise<void>`
* `assignProductManufacturer(productId: string, manufacturerId: string): Promise<void>`
* `assignProductMedia(productId: string, mediaId: string): Promise<void>`
* [...]

## Available `get*` methods in `TestDataService` [​](#available-get-methods-in-testdataservice)

They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `getCountry(iso2: string): Promise<Country>`
* `getCurrency(isoCode: string): Promise<Currency>`
* `getCustomerGroups(): Promise<CustomerGroup[]>`
* `getPaymentMethod(name = 'Invoice'): Promise<PaymentMethod>`
* [...]

## Writing new methods in `TestDataService` [​](#writing-new-methods-in-testdataservice)

If you want to add new functionality to this service such as a new type of entity creation, you can follow this approach:

### 1. Define the purpose [​](#_1-define-the-purpose)

Decide whether you're creating, assigning, or retrieving data. Most methods fall into one of the following patterns:

* `create*`: Creates a new entity (e.g., product, customer, category)
* `assign*`: Links existing entities (e.g., assign media to product)
* `get*`: Retrieves specific or filtered data from the system

### 2. Implement the method [​](#_2-implement-the-method)

Use the `AdminApiContext` to interact with the Shopware Admin API. Here is a simplified example of adding a method to [create a new shipping method](https://github.com/shopware/acceptance-test-suite/blob/e8d2a5e8cee2194b914aa35aa87fe7cf04060834/src/services/TestDataService.ts#L679)

### 3. Follow naming conventions [​](#_3-follow-naming-conventions)

Be consistent in naming:

* Use `createBasic*` for standardized, default setups with predefined values (e.g., `createBasicProduct`)
* Use `create*With*` for variations (e.g. `createProductWithImage`)
* Use `assign*` for methods that associate two entities (e.g., `assignProductMedia`)
* Use `get*` to retrieve specific entities or lists (e.g. `getCurrency`)

### 4. Add a return type [​](#_4-add-a-return-type)

Always define a return type (typically a `Promise<...>`) to improve autocompletion and documentation support.

### 5. Add cleanup logic [​](#_5-add-cleanup-logic)

Make sure to clean up the entity via code after the test run by putting the entity in a record. See the example below:

typescript

```shiki
async createBasicRule(): Promise<Rule> {
        [...]
                
 this.addCreatedRecord('rule', rule.id);

 [...]
 }
```

Explore further info on this in [Automatic Cleanup](#automatic-cleanup-of-test-data-and-system-configurations).

### 6. Test the method [​](#_6-test-the-method)

Once added, use your new method inside a test to verify it works as expected (`/tests/TestDataService.spec.ts`):

typescript

```shiki
test('Verify new shipping method creation', async ({ TestDataService }) => {
    const shippingMethod = await TestDataService.createShippingMethod({
        name: 'Express Delivery'
 });

    expect(shippingMethod.name).toEqual('Express Delivery');
});
```

## Automatic cleanup of test data and system configurations [​](#automatic-cleanup-of-test-data-and-system-configurations)

The `TestDataService` includes a built-in mechanism to ensure that any test data & system configuration entries created during a test run are automatically deleted afterward. This ensures that the Shopware instance remains clean and consistent between tests, helping to maintain **test isolation** and prevent **state leakage**.

### How cleanup works [​](#how-cleanup-works)

When you create an entity using a `create*` method (e.g., `createBasicProduct`, `createCustomer`), the service automatically registers that entity for deletion by calling the `addCreatedRecord()` method:

typescript

```shiki
this.addCreatedRecord('product', product.id);
```

These records are stored in a cleanup queue processed at the end of each test using the Playwright lifecycle.

### Cleanup execution [​](#cleanup-execution)

The `cleanup()` method handles the deletion of all registered entities and system config changes. All created records are grouped into two categories:

* Priority Deletions (`priorityDeleteOperations`) – for entities with dependencies that must be deleted first (e.g., orders, customers)
* Standard Deletions (`deleteOperations`) – for all other entities

This prioritization prevents errors when deleting interdependent data. Any modified system configurations are reset to their previous state after deleting priority records. The priority entities can be found in the `TestDataService` class. If you want to add a new entity to the priority deletion list, you can do so by adding it to the `priorityDeleteOperations` array.

### Skipping cleanup [​](#skipping-cleanup)

In rare scenarios, such as performance testing or debugging, you may want to prevent cleanup for specific entities. You can simply skip the cleanup by calling `TestDataService.setCleanUp(false)` within your test.

## Extending the TestDataService in external projects [​](#extending-the-testdataservice-in-external-projects)

The `TestDataService` is designed to be **easily extendable**. This allows you to add project-specific data generation methods while still benefiting from the existing, standardized base functionality.

### 1. Create a new subclass [​](#_1-create-a-new-subclass)

You can create a new TypeScript class that **extends** the base `TestDataService`.

typescript

```shiki
import { TestDataService } from '@shopware-ag/acceptance-test-suite';

export class CustomTestDataService extends TestDataService {

    constructor(AdminApiContext, DefaultSalesChannel) {
        super(...);
 }
    
    async createCustomCustomerGroup(data: Partial<CustomerGroup>) {
        const response = await this.adminApi.post('customer-group?_response=true', {
            data: {
 ...
 },
 });

        const { data: createdGroup } = await response.json();
        this.addCreatedRecord('customer-group', createdGroup.id);

        return createdGroup;
 }
}
```

### 2. Provide the extended service as a fixture [​](#_2-provide-the-extended-service-as-a-fixture)

Following the Playwright [fixture system](https://playwright.dev/docs/test-fixtures) described, you create a new fixture that initializes your extended service.

Example from `AcceptanceTest.ts`:

typescript

```shiki
import { test as base } from '@shopware-ag/acceptance-test-suite';
import type { FixtureTypes } from './BaseTestFile';
import { CustomTestDataService } from './CustomTestDataService';

export interface CustomTestDataServiceType {
    TestDataService: CustomTestDataService;
}

export const test = base.extend<FixtureTypes & CustomTestDataServiceType>({
    TestDataService: async ({ AdminApiContext, DefaultSalesChannel }, use) => {
        const service = new CustomTestDataService(AdminApiContext, DefaultSalesChannel.salesChannel);
        await use(service);
        await service.cleanUp();
 },
});
```

In this setup:

* The `TestDataService` fixture is **overridden** with your custom `CustomTestDataService`.
* Now, all tests that use `TestDataService` will have access to both the original and your extended methods.
* The automated cleanup is still in place, ensuring that any test data created during the test run is removed afterward.

---

## Best Practices

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/best-practices.html

# Best practices [​](#best-practices)

A good first read about this is the official [playwright best practices page](https://playwright.dev/docs/best-practices). It outlines the essential practices to follow when writing acceptance tests for Shopware.

The most important part is [test isolation](https://playwright.dev/docs/best-practices#make-tests-as-isolated-as-possible), which helps to prevent flaky behavior and enables the test to be run in parallel and on systems with an unknown state.

## Dos [​](#dos)

* Use the [`TestDataService`](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/services/TestDataService.ts) for creating test data
* Create all the data that is required for your test case. That includes sales channels, customers, and users (the page fixtures handle most of the common use cases)
* Clean it up if you don't need it anymore. The `TestDataService` will take care of it if you used it to create the test data
* If you need specific settings for your test, set them explicitly for the `user/customer/sales` channel
* Directly jump to the detail pages with the ID of the entities you have created. If that is not possible, use the search with a unique name to filter lists to just that single entity
* If you need to skip tests, comment any relevant github issues as part of the skip method: `test.skip('Blocked by https://[...])`

## Don'ts [​](#don-ts)

* Do not expect lists/tables only to contain one item; leverage unique IDs/names to open or find your entity instead
* Same with helper functions, do not expect only to get one item back from the API. Always use unique criteria for the API call
* Avoid unused fixtures. If you request a fixture but don't use any data from the fixture, the test or fixture should be refactored
* Do not depend on implicit configuration and existing data. Examples:
  + rules
  + flows
  + categories
* Do not expect the shop to have the defaults `en_GB` and `EUR`
* Do not change global settings (sales channel is ok, because we created it). Everything in "Settings" that is not specific to a sales channel (tax, search, etc.)

## Sensitive Data / Credentials [​](#sensitive-data-credentials)

Sometimes you have to provide sensitive data or credentials for your tests to run, for example, credentials for a sandbox environment for a payment provider. Apart from avoiding having those credentials in the actual code, you should also prevent them from appearing in logs or traces. To achieve this, you should outsource steps involving sensitive data to a separate project that runs before the actual test project and disable traces for it.

**Example**

Typescript

```shiki
projects: [
    // Init project using sensitive data
 {
      name: 'init', 
      testMatch: /.*\.init\.ts/,
      use : {trace : 'off'}
 },

 {
      // actual test project
      // [...]
      dependencies: ['init'],
 }]
```

## Debugging API calls [​](#debugging-api-calls)

Debugging API calls may not be an easy task at first glance, because if the call you made returns an error, it is not directly visible to you. But you can use the `errors[]` array of the response and log that on the console.

**Example**

Typescript

```shiki
const response = await this.AdminApiClient.post('some/route', {
    data: {
        limit: 1,
        filter: [
 {
                type: 'equals',
                field: 'someField',
                value: 'someValue',
 },
 ],
 },
});
const responseData = await response.json();
console.log(responseData.errors[0]);
```

## Code contribution [​](#code-contribution)

You can contribute to this project via its [official repository](https://github.com/shopware/acceptance-test-suite/) on GitHub.

This project uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). Make sure to form your commits accordingly to the spec.

---

## Jest unit tests in Shopware's administration

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/jest-admin.html

# Jest Unit Tests in Shopware's Administration [​](#jest-unit-tests-in-shopware-s-administration)

## Overview [​](#overview)

You should write a unit test for every functional change. It should guarantee that your written code works and that a third developer can't break the functionality with their code.

With a good test coverage we can have the confidence to deploy a stable software without needing to manually test the software in its entirety. This little guide will guide you how to write unit tests for the Administration in Shopware 6.

We are using [Jest](https://jestjs.io) as our testing framework. It's a solid foundation and widely used by many developers. Before you are reading this guide you have to make sure you understand the basics of unit tests and how Jest works.

## Video [​](#video)

Did you know that there's a video available to this topic? Please take a look:

#### Writing unit tests with Jest (Developer Tutorial) - YouTube

## Prerequisites [​](#prerequisites)

This tutorial will have a strong focus on how unit tests should be written when it comes to components in the Administration. So please make sure you already know what a unit test is and why we are doing it. Furthermore, you should know what components tests are and what we want to achieve with them. You can find a good source for best practices in this Github repository:

[Javascript testing - best practices @ GitHub](https://github.com/goldbergyoni/javascript-testing-best-practices)

In addition, you need a running Shopware 6 installation. Your repository used for that should be based on development template, as we need to use some scripts provided by it.

## Test file location [​](#test-file-location)

The test files are placed in the same directory as the file which should be tested. The file name is the same with the suffix `.spec.js` or `spec.ts`.

## Testing services and ES modules [​](#testing-services-and-es-modules)

Services and isolated ECMAScript modules are well testable because you can import them directly without mocking or stubbing dependencies. A service can be used isolated and therefore is easy to test.

Let's have a look at an example:

javascript

```shiki
// sanitizer.helper.spec.js
import Sanitizer from 'src/core/helper/sanitizer.helper';

describe('core/helper/sanitizer.helper.js', () => {
    it('should sanitize the html', () => {
        expect(Sanitizer.sanitize('<A/hREf="j%0aavas%09cript%0a:%09con%0afirm%0d``">z'))
            .toBe('<a href="j%0aavas%09cript%0a:%09con%0afirm%0d``">z</a>');
    });

    it('should remove script functions from dom elements', () => {
        expect(Sanitizer.sanitize('<details open ontoggle=confirm()>'))
            .toBe('<details open=""></details>');
    });

    it('should remove script functions completely', () => {
        expect(Sanitizer.sanitize(`<script y="><">/*<script* */prompt()</script`))
            .toBe('');
    });

    it('should sanitize js in links', () => {
        expect(Sanitizer.sanitize('<a href=javas&#99;ript:alert(1)>click'))
            .toBe('<a>click</a>');
    });

    // ...more tests 
});
```

You see, you are able to write the test the same way you're used to, writing Jest unit tests in general.

## Write tests for components [​](#write-tests-for-components)

After setting up your component test, you need to write your tests. A good way to write them is to test input and output. The most common tests are:

* set Vue Props and check if component looks correctly
* interact with the DOM and check if the desired behaviour is happening

However, when it comes to writing component tests for Shopware's Administration, there are some further steps to go. We will take a look at them in the following paragraphs.

## Setup for testing Vue components [​](#setup-for-testing-vue-components)

We are using the [Vue Test Utils](https://v1.test-utils.vuejs.org/) for easier testing of Vue components. If you don't have experience with testing Vue components it is useful to read some basic guides on this topic. The main part of testing components is similar in Shopware 6.

However, there are some important differences. We can't test components that easily like in other Vue projects because we are supporting template inheritance and extendability for third party developers. This causes overhead which we need to bear in mind.

We are using a global object as an interface for the whole Administration. Every component gets registered to this object, e.g. `Shopware.Component.register()`. Therefore, we have access to Component with the `Shopware.Component.build()` method. This creates a native Vue component with a working template. Every override and extension from another components are resolved in the built component.

## Setup tests with create test command [​](#setup-tests-with-create-test-command)

You can generate a test boilerplate using the create test command. You encountered an untested component or service? Copy the path in your IDE and go to your terminal. In the Shopware root directory run `composer run admin:create:test`. Once prompted paste the path you copied and hit enter.

If everything is correct you should now have a `.spec` file with our newest recommended boilerplate code.

### Executing tests [​](#executing-tests)

Before you are using the commands make sure that you installed all dependencies for your Administration. If you haven't done this already, then you can do it running the following PSH command: `composer run init:js`

In order to run jest unit tests of the Administration, you can use the psh commands provided by our development template.

INFO

This only applies to the Shopware provided Administration! If you use unit tests in your plugin, you might need to write your own scripts for that.

This command executes all unit tests and shows you the complete code coverage.  
`composer run admin:unit`

This command executes only unit tests of changed files. It automatically restarts if a file gets saved. This should be used during the development of unit tests.  
`composer run admin:unit:watch`

### Example test structure [​](#example-test-structure)

typescript

```shiki
import {shallowMount, createLocalVue, Wrapper} from '@vue/test-utils';
import flushPromises from 'flush-promises';

// add additional parameters to change options for the test
async function createWrapper(/* options = {} */): Wrapper {
    // add localVue only if needed
    const localVue = createLocalVue();

    // prefer shallowMount over normal mount
    return shallowMount(await Shopware.Component.build('sw-your-component-for-test'), {
        // localVue only if needed
        localVue,
        // add stubs for missing component
        stubs: {
            'sw-missing-component-one': Shopware.Component.build('sw-missing-component-one'),
            'sw-missing-component-two': Shopware.Component.build('sw-missing-component-two'),
        },
        mocks: {
            // add mocks if needed
        },
        // needed if you interact with elements
        attachTo: document.body,

        // ...options,
    });
}

describe('the/path/to/the/component', () => {
    let wrapper: Wrapper;

    beforeAll(async () => {
        // generate all needed mocks, etc.
    })

    beforeEach(async () => {
        // reset all mocks and state changes to default
        wrapper = await createWrapper();
        
        // wait for created hook etc.
        await flushPromises();
    })

    afterEach(async () => {
        // cleanup everything

        // destroy the existing wrapper
        if (wrapper) {
            await wrapper.destroy();
        }

        // wait until all promises are finished
        await flushPromises();
    })

    it('should be a Vue.js component', () => {
        expect(wrapper.vm).toBeTruthy();
    });

    // Add more component tests
})
```

## First example: Testing sw-multi-select component [​](#first-example-testing-sw-multi-select-component)

For better understanding how to write component tests for Shopware 6 let's write a test. In our example we are using the component `sw-multi-select`.

When you want to mount your component it needs to be imported first:

javascript

```shiki
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-multi-select';
```

You see that we import the `sw-multi-select` without saving the return value. This blackbox import only executes code. However, this is important because this registers the component to the Shopware object:

javascript

```shiki
// src/app/component/form/select/base/sw-multi-select/index.js
Shopware.Component.register('sw-multi-select', {
    // The vue component
});
```

### Mounting components [​](#mounting-components)

In the next step we can mount our Vue component which we get from the global Shopware object:

javascript

```shiki
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-multi-select';

shallowMount(Shopware.Component.build('sw-multi-select'));
```

When we’re testing our vue.js components, we need a way to mount and render the component. Therefore, we use the following methods:

* `mount()`: Creates a Wrapper that contains the mounted and rendered Vue component.
* `shallowMount()`: Like mount, it creates a Wrapper that contains the mounted and rendered Vue component,

  but with stubbed child components.

This way, we create a new `wrapper` before each test. The `build` method resolves the twig template and returns a vue component.

### Test structure [​](#test-structure)

Now you can test the component like any other component. Let's try to write our first test:

javascript

```shiki
// test/app/component/form/select/base/sw-multi-select.spec.js
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/form/select/base/sw-multi-select';

describe('components/sw-multi-select', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(Shopware.Component.build('sw-multi-select'));
    });

    afterEach(() => {
        wrapper.destroy();
    });

    it('should be a Vue.js component', () => {
        expect(wrapper.vm).toBeTruthy();
    });
});
```

This contains our component. In our first test we only check if the wrapper is a Vue instance.

### Running the test [​](#running-the-test)

Now let's start the watcher to see if the test works. You can do this using our PSH command `composer run admin:unit:watch`. You should see a result like this: `Test Suites: 1 passed, 1 total`. You should also see several warnings like this:

* `[Vue warn]: Missing required prop: "options"`
* `[Vue warn]: Missing required prop: "value"`
* `[Vue warn]: Unknown custom element: <sw-select-base> - did you register the component correctly? ...`

The first two warnings are solved easily by providing the required props to our shallowMount:

javascript

```shiki
wrapper = shallowMount(Shopware.Component.build('sw-multi-select'), {
    props: {
        options: [],
        value: ''
    }
});
```

Now you should only see the last warning with an unknown custom element. The reason for this is that most components contain other components. In our case the `sw-multi-select` needs the `sw-select-base` component. Now we have several solutions to solve this. The two most common ways are stubbing or using the component.

javascript

```shiki
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-select-base';

wrapper = shallowMount(Shopware.Component.build('sw-multi-select'), {
    props: {
        options: [],
        value: ''
    },
    stubs: {
        'sw-select-base': Shopware.Component.build('sw-select-base'),
    }
});
```

You need to choose which way is needed: Many tests do not need the real component, but in our case we need the real implementation. You will see that if we import another component that they can create also warnings. Let's look at the code that solve all warnings, then we should have a code like this:

javascript

```shiki
// test/app/component/form/select/base/sw-multi-select.spec.js
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/form/select/base/sw-multi-select';
import 'src/app/component/form/select/base/sw-select-base';
import 'src/app/component/form/field-base/sw-block-field';
import 'src/app/component/form/field-base/sw-base-field';
import 'src/app/component/form/field-base/sw-field-error';
import 'src/app/component/form/select/base/sw-select-selection-list';
import 'src/app/component/form/select/base/sw-select-result-list';
import 'src/app/component/utils/sw-popover';
import 'src/app/component/form/select/base/sw-select-result';
import 'src/app/component/base/sw-highlight-text';
import 'src/app/component/base/sw-label';
import 'src/app/component/base/sw-button';

describe('components/sw-multi-select', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(Shopware.Component.build('sw-multi-select'), {
            props: {
                options: [],
                value: ''
            },
            stubs: {
                'sw-select-base': Shopware.Component.build('sw-select-base'),
                'sw-block-field': Shopware.Component.build('sw-block-field'),
                'sw-base-field': Shopware.Component.build('sw-base-field'),
                'sw-icon': '<div></div>',
                'sw-field-error': Shopware.Component.build('sw-field-error'),
                'sw-select-selection-list': Shopware.Component.build('sw-select-selection-list'),
                'sw-select-result-list': Shopware.Component.build('sw-select-result-list'),
                'sw-popover': Shopware.Component.build('sw-popover'),
                'sw-select-result': Shopware.Component.build('sw-select-result'),
                'sw-highlight-text': Shopware.Component.build('sw-highlight-text'),
                'sw-label': Shopware.Component.build('sw-label'),
                'sw-button': Shopware.Component.build('sw-button')
            }
        });
    });

    afterEach(() => {
        wrapper.destroy();
    });

    it('should be a Vue.js component', () => {
        expect(wrapper.vm).toBeTruthy();
    });
});
```

## Second example: Testing of message inside the sw-alert component [​](#second-example-testing-of-message-inside-the-sw-alert-component)

Of course, the complexity and structure of your test depends on what you are trying to achieve with your component. Here is one little example concerning the component `sw-alert`: Actually, he task of an alert is displaying a message for the user in most cases. So in this example, let's write a test for this text located in a slot. You can find this example in the linked video above as well.

We will start with an already written test similar to the first example:

javascript

```shiki
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/base/sw-alert';

describe('components/base/sw-alert', () => {
    it('should be a Vue.js component', () => {
        const wrapper = shallowMount(Shopware.Component.build('sw-alert'), {
            stubs: ['sw-icon']
        });

        // Assert if our component is a vue instance = mountes correctly
        expect(wrapper.vm).toBeTruthy();
    });
});
```

There we'll add another test case for testing the alert's message:

javascript

```shiki
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/base/sw-alert';

describe('components/base/sw-alert', () => {
    it('should be a Vue.js component', () => {
        // see above
    });

    it('should render the message inside the default slot', () => {
        // New
    });
});
```

### Mounting components [​](#mounting-components-1)

You can set the content of a slot during component mount. See the paragraph "Mounting components" in the first example for details.

javascript

```shiki
    it('should render the message inside the default slot', () => {
        const wrapper = shallowMount(Shopware.Component.build('sw-alert'), {
            slots: {
                default: 'My custom message'
            }
        });
    });
```

Afterwards you can make an assertion that the text passed to the slot will be rendered inside the desired element. In this case we search in the wrapper for the element with the selector `.sw-alert__message` and check if the text is there:

javascript

```shiki
    it('should render the message inside the default slot', () => {
        const wrapper = shallowMount(Shopware.Component.build('sw-alert'), {
            slots: {
                default: 'My custom message'
            }
        });
        expect(wrapper.find('.sw-alert__message').text()).toBe('My custom message');
    });
```

## Stubbing your component [​](#stubbing-your-component)

Vue Test Utils has some advanced features for stubbing components. A stub is actually when you replace an existing implementation of a custom component with a dummy component doing nothing at all, actually. This is necessary for the component to function independently, in an isolated way.

Components in Shopware might also depend on other dependencies like `$tc`, directives or injections. This way, the setup of your test may get more complex. When you are building components then you need to mock their dependencies as well.

To improve the test writing experience we included many mocks, helper methods and even more by default. This will help you to reduce the overhead of setting up a single test with all mocks.

INFO

Everything can be overwritten in the `mount` or `shallowMount` method if you need to have custom implementation.

## Using preconfigured mocks [​](#using-preconfigured-mocks)

### ACL [​](#acl)

You can set the active ACL roles by simply adding values to the global variable `global.activeAclRoles`. By default, the test suite has no ACL rights. If you want, you can change the privileges for each test separately.

Example:

javascript

```shiki
it('should render with ACL rights', async () => {
    // set ACL privileges
    global.activeAclRoles = ['product.editor'];

    const wrapper = await createWrapper();
    expect(wrapper.vm).toBeTruthy();
});
```

### Feature flags [​](#feature-flags)

If you want to enable feature flags you can add the flag to the global variable `global.activeFeatureFlags`. If you want to, you can change the usage of feature flags for each test.

Example:

javascript

```shiki
it('should render with active feature flag', async () => {
    // set feature flag
    global.activeFeatureFlags = ['FEATURE_NEXT_12345'];

    const wrapper = await createWrapper();
    expect(wrapper.vm).toBeTruthy();
});
```

### Repository factory [​](#repository-factory)

The data handling and the repository factory works by default. It will be generated by the entity-schema which will be written to a file before you start the test suite.

Every time the repository factory requests something from a URL, you get a notification in the console. This notification also includes a short guide on how to implement the response. This information may look like this:

javascript

```shiki
// You should implement mock data for this route: "/search/product".

/*
 * ############### Example ###############
*/

const responses = global.repositoryFactoryMock.responses;

responses.addResponse({
    method: 'Post',
    url: '/search/product',
    status: 200,
    response: {
        data: [
            {
                id: YourId,
                attributes: {
                    id: YourId
                }
            }
        ]
    }
});

/*
 * ############### Example ###############
*/

// You can disable this warning with this code:

global.repositoryFactoryMock.showWarning = false;
```

The response value should contain your test data. It needs to match the response from the backend API. An easy way to get the correct response is to inspect the response from the real API when you open the Administration.

If you don't want to use this helper then you can easily overwrite it by setting a custom mock for the repositoryFactory in your mount method.

### Directives [​](#directives)

All global directives are registered by default. You can overwrite them if you want.

### Filters [​](#filters)

All global filters are registered by default. You can overwrite them if you want.

### Services [​](#services)

Some services are registered with a mock alternative. If you want to use a different service, you need to mock it manually. The console will inform you with a warning that the service does not exist.

### Context [​](#context)

The global `Shopware` context is prepared automatically. You can overwrite them in `Shopware.Store` if necessary.

### Global mocks [​](#global-mocks)

For most cases we created automatic mocks, so you don´t need to implement them manually. Some examples are `$tc`, `$device`, `$store` or `$router`.

If you want to override one mock then you can do it in the `mount` method:

javascript

```shiki
mount('dummy-component', {
    mocks: {
        $tc: (...args) => JSON.stringify([...args])
    }
})
```

### Using mocks [​](#using-mocks)

A common warning can occur if you didn't mock functions needed in your component. For example, please look at the warning below:

> [Vue warn]: Error in render: "TypeError: hasError is not a function"

The solution is using mocks while mounting your component. In this case, your mock here is a simple function returning the value "true".

javascript

```shiki
shallowMount(Shopware.Component.build('your-component'), {
    mocks: {
        hasError: () => false // your mock (here a simple function returning the value "true")
    }
});
```

### Stubbing directives [​](#stubbing-directives)

When working with components of Shopware's Administration, you might stumble upon the following warning:

> [Vue warn]: Failed to resolve directive: clipboard

If that happens, you need to use [localVue](https://v1.test-utils.vuejs.org/api/#createlocalvue) to provide the directive mock. `createLocalVue` returns a Vue class for you to add components, mixins and install plugins without polluting the global Vue class. In our context, it looks like this:

javascript

```shiki
import { shallowMount, createLocalVue } from '@vue/test-utils';

const localVue = createLocalVue();
localVue.directive('clipboard', {}); // add directive mock to localVue

shallowMount(Shopware.Component.build('your-component'), {
    localVue
});
```

### Stubbing injections [​](#stubbing-injections)

Another common warning is the one below:

> [Vue warn]: Injection "mediaService" not found

The solution is stubbing this injection. In detail, you need to provide the injected data, services and so on: That means you need to mock the return values for your test's methods used, e.g. `renameMedia` and `uploadMediaById` - Providing the data exactly as needed by the component for running your test case and what the injection actually is. It can be valid to set the injection name equal to an empty object just to mute it when it's not really needed for your test.

javascript

```shiki
provide: {
  mediaService: {}
}
```

Please note that the mediaService has a `renameMedia` method. So in order to stub the `mediaService` in realistic manner, follow the example below:

javascript

```shiki
mediaService: {
    renameMedia: () => Promise.resolve()
}
```

In the context of injections, the next warning can occur sometimes:

> [Vue warn]: Error in foo: "TypeError: Cannot read property 'renameMedia' of undefined"

This can be caused by several reasons. The best way to find out the solution is to look at the source of the code and find out what is missing. This is highly dependent on the component under test, though. In this example the service `mediaService` is missing:

javascript

```shiki
Shopware.Service('mediaService').renameMedia(mediaId, newFileName);
```

To fix this you need to add the mocked service before all tests. In our case we need to register the service:

javascript

```shiki
beforeAll(() => {
  Shopware.Service.register('mediaService', {
    // your service mock
  });
});
```

## Next steps [​](#next-steps)

Do you want to see these examples in practice? Head over to our [video tutorial](https://youtu.be/nWUBK3fjwVg) on how to write component tests in jest for the Shopware Administration.

Furthermore, you might want to have a look at one of the following guides as well:

* [Jest tests for the storefront](./jest-storefront/)
* [PHPUnit tests](./php-unit/)
* [End-to-end tests](./end-to-end-testing/)

---

## Jest unit tests in Shopware's storefront

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/jest-storefront.html

# Jest Unit Tests in Shopware's Storefront [​](#jest-unit-tests-in-shopware-s-storefront)

## Overview [​](#overview)

You should write a unit test for every functional change. Writing tests will ensure that your written code works and that another change can't break your code's functionality with their code.

With a good test coverage you gain confidence to deploy a stable software without the requirement to manually test every change. This little guide will guide you how to write unit tests for the Administration in Shopware 6.

We are using JestJS as our testing framework as it's a solid foundation and widely used by many developers.

[Jest · 🃏 Delightful JavaScript Testing](https://jestjs.io)

## Prerequisites [​](#prerequisites)

Before you are reading this guide you have to make sure you understand the basics of unit tests and how Jest works. You can find a good source for best practices in this Github Repo:

[Javascript testing - best practices @ GitHub](https://github.com/goldbergyoni/javascript-testing-best-practices)

In addition, you need a running Shopware 6 installation. Your repository used for that should be based on development template, as we will to use some scripts provided by it.

For one example, we use a Javascript plugin. In oder to follow this example, you need to know how to build a Javascript plugin in the first place. You can learn about it in the corresponding [guide](./../storefront/add-custom-javascript/).

## Test structure [​](#test-structure)

WARNING

When it comes to the path to the test folder, you are quite free to use your own requirements. You could even build up a separate test suite if you need. There's one limitation though: Please take care you place your tests according your `package.json` file!

The following configuration matches our core configuration in order to give you a starting point. In Shopware's platform repository, you will find the Storefront unit tests in the following directory: `platform/src/Storefront/Resources/app/storefront/test` It may be a good convention to resemble this directory structure, but it's no fixed requirement.

Inside the test directory, you add a test for a file in the same path as the source path. You see: When creating the file, the name should also be the same as the component has with an additional `test`.

The exact test folder structure looks like seen below, starting in `Storefront` bundle:

bash

```shiki
Resources
  `-- app
    `-- <environment>
      `-- test
        `-- plugin
          `-- <plugin-name>
            `-- js-plugin-test.spec.js
```

Please note that in this example, `<environment>` is a placeholder for the environment you are working in. In this context, that should be `storefront`.

## Writing a basic test [​](#writing-a-basic-test)

When writing jest unit tests in the Storefront, you will soon realize that it's not that much different from writing jest unit tests in general. Unlike the [Jest unit tests in the Administration](./jest-admin.html), you basically don't need to go an extra mile to write your unit tests. Services, helper and isolated ECMAScript modules are well testable because you can import them directly without mocking or stubbing dependencies. They can be used isolated and therefore are easy to test.

Let's start from scratch with a simple example: Imagine we want to write a test for a helper class, e.g. the `feature.helper` of our Storefront, handling the feature flag usage. We want to test, if our feature helper can indeed handle active feature flags.

At first, you need to create your test file, e.g. `feature.helper.test.js`. With your new created test file, let's create the test structure for it:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
// describe is meant for grouping and structure
describe('feature.helper.js', () => {

    // This is your actual test
    test('checks the flags', () => {
        // Assertions come here
    });
});
```

Now, let's fill this empty test with life. Our first step is importing the helper under test - the `feature.helper` class. However, there one more step to be done for preparation.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
// Import for the helper to test
import Feature from 'src/helper/feature.helper';

describe('feature.helper.js', () => {
    test('checks the flags', () => {
        // Assertions come here
    });
});
```

In order to be able to test our feature flag integration, we of course need some fixtures to be present - some active and inactive feature flags. So we need to ensure their presence before running the tests, ideally in a setup step. As you might know from other frameworks, it's convenient to use [lifecycle hooks](https://jestjs.io/docs/setup-teardown) for that purpose.

To sum it up, we need a feature flag fixture and the implementation of it in the `beforeEach` hook of our test. In our example, that looks like below:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
import Feature from 'src/helper/feature.helper';

// One flag should be active, the other shouldn't.
const default_flags = {
    test1: true,
    test2: false
};

describe('feature.helper.js', () => {

    // This hook is executed before every test
    beforeEach(() => {
        // Applying the flag fixture
        Feature.init(default_flags);
    });

    test('checks the flags', () => {
        // Assertions come here
    });
});
```

Alright, let's get to the point now, writing the actual test. Remember we want to make sure we have active and inactive feature flags. In addition, it may be useful to check the behavior if a third, non-existent feature flag is introduced. Using [Jest's matchers](https://jestjs.io/docs/using-matchers) for these assertions, we get the following test:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
import Feature from 'src/helper/feature.helper';

const default_flags = {
    test1: true,
    test2: false
};

describe('feature.helper.js', () => {
    beforeEach(() => {
        Feature.init(default_flags);
    });

    test('checks the flags', () => {
        expect(Feature.isActive('test1')).toBeTruthy();
        expect(Feature.isActive('test2')).toBeFalsy();
        expect(Feature.isActive('test3')).toBeFalsy();
    });
});
```

That's basically it! We wrote our first jest unit test in the Storefront.

## Executing the tests [​](#executing-the-tests)

Before you are using the commands make sure that you installed all dependencies for your Storefront. If you haven't done this already, then you can do it running the following PSH command:

bash

```shiki
> composer run build:js:storefront
```

In order to run jest unit tests of the Storefront, you can use the psh commands provided by our development template. This command executes all unit tests and shows you the complete code coverage.

bash

```shiki
> composer run storefront:unit
```

INFO

This only applies to the Shopware provided Storefront! If you use unit tests in your Plugin, you might need to write your own scripts for that.

## Mocking JavaScript plugins [​](#mocking-javascript-plugins)

Now, let's have a look at a intermediate example: As you're writing JavaScript plugins, you may want to test those. As you need to mock some things in this case, this kind of test might be a bit more complex.

INFO

The folder structure, and the corresponding file locations of the following example will resemble the one used in `platform` repository.

Let's start with the plugin we want to test later. For the sake of simplicity, we will use a plugin which returns "Hello world":

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/plugin/hello-world/hello-world.plugin.js
import Plugin from 'src/plugin-system/plugin.class'

export default class HelloWorldPlugin extends Plugin {
    static options = {};

    init() {
        console.log('Hello World!', this.el);
    }

    sayHello() {
        return "Hello World!"
    }
}
```

Of course, you need to make sure that your plugin is registered, more details in the guide on [Javascript plugins](./../storefront/add-custom-javascript/).

In the beginning, writing plugin tests is still similar to other jest unit tests: You import your plugin's class and use the familiar test structure:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

// import your plugin here
import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {

    beforeEach(() => {
        // Here we need to do all the mocking
    });

    afterEach(() => {
        // Teardown
    });

    test('custom plugin exists', () => {
        // your actual test
    });
});
```

You might notice the lifecycle hook we use in this test. These will be important in the next steps where we begin to mock our plugin and clean it up after our tests.

The `beforeEach` hook will be executed before each test. Thus, it's the perfect location for creating our plugin under test. Therefore, we need to get an element first. We'll use it to create our plugin - resembling the usage of a plugin on an element.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {

    // Definition of plugin
    let plugin;

    beforeEach(() => {
        // you need to get an element for the plugin
        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);

    });

    afterEach(() => {
        // Teardown
    });

    test('custom plugin exists', () => {
        // your actual test, temporary filled with a placeholder
        console.log(plugin);
    });
});
```

If you execute your test now, you'll run into an error:

bash

```shiki
      HelloWorldPlugin tests
        ✕ custom plugin exists (32ms)

      ● HelloWorldPlugin tests › custom plugin exists

        TypeError: Cannot read property 'getPluginInstancesFromElement' of undefined

          119 |      */
          120 |     _registerInstance() {
        > 121 |         const elementPluginInstances = window.PluginManager.getPluginInstancesFromElement(this.el);
              |                                                             ^
          122 |         elementPluginInstances.set(this._pluginName, this);
          123 |
          124 |         const plugin = window.PluginManager.getPlugin(this._pluginName, false);
```

This was to be expected because you need to mock some more things required for the plugin to run. To solve this issue, you need to mock the `PluginManager` which holds all plugin instances globally in the Storefront. Because our test is just testing the single plugin class, the actual implementation on the real DOM element in the Storefront isn't too important at this moment.

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {
    let plugin;

    beforeEach(() => {

        // Mocking PluginManager to get the plugin working
        window.PluginManager = {
            getPluginInstancesFromElement: () => {
                return new Map();
            },
            getPlugin: () => {
                return {
                    get: () => []
                };
            }
        };

        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);
    });

    afterEach(() => {
        // Set your plugin to null to clean up afterwards
        plugin = null;
    });

    test('custom plugin exists', () => {
        // your actual test, temporary filled with a placeholder
        console.log(plugin);
    });
});
```

WARNING

Don't forget the cleanup after each test! You need to set your plugin to `null` in your `afterEach` hook to ensure an isolated test.

Finally, we're ready to write our actual test. Write your assertions as you're used to. In this example, we first want to test if our plugin can be instantiated:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {
    let plugin;

    beforeEach(() => {
        window.PluginManager = {
            getPluginInstancesFromElement: () => {
                return new Map();
            },
            getPlugin: () => {
                return {
                    get: () => []
                };
            }
        };

        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);
    });

    afterEach(() => {
        plugin = null;
    });

    test('The HelloWorld plugin can be instantiated', () => {

        // Our assertions will be done here
        expect(plugin).toBeInstanceOf(HelloWorldPlugin);
    });
});
```

Afterwards, we can add more tests as we want to. To give an example, it's useful to rest if our plugin returns the "Hello World" test as expected:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
    test('Shows text', () => {
        expect(plugin.sayHello()).toBe('Hello World!')
    });
```

Now you're ready to go! Below the full example of our test, for reference:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {

    let plugin;

    beforeEach(() => {
        window.PluginManager = {
            getPluginInstancesFromElement: () => {
                return new Map();
            },
            getPlugin: () => {
                return {
                    get: () => []
                };
            }
        };

        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);
    });

    afterEach(() => {
        // Teardown
        plugin = null;
    });

    test('The cookie configuration plugin can be instantiated', () => {
        // your actual test
        expect(plugin).toBeInstanceOf(HelloWorldPlugin);
    });

    test('Shows text', () => {
        expect(plugin.sayHello()).toBe('Hello World!')
    });
});
```

## More interesting topics [​](#more-interesting-topics)

* [PHPUnit tests](./php-unit/)
* [End-to-end tests](./end-to-end-testing/)

---

## PHP unit testing

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/testing/php-unit.html

# PHP Unit Testing [​](#php-unit-testing)

## Overview [​](#overview)

This guide will cover the creation of PHPUnit tests in Shopware 6. Refer to the [official PHPUnit documentation](https://phpunit.de/documentation.html) for a deep dive into PHP unit testing.

## Prerequisites [​](#prerequisites)

In order to create tests for a plugin, you need a plugin as a base. Refer to the [Plugin Base Guide](./../plugin-base-guide.html) for more information.

Furthermore, have a look at our [Execute database queries/migrations](./../plugin-fundamentals/database-migrations.html) guide since this guide will show you how to create a migration test for these examples.

## PHPUnit configuration [​](#phpunit-configuration)

First, to configure PHPUnit, create a file called `phpunit.xml` in the root directory of the plugin. To get more familiar with the configurable options, refer to the [PHPUnit documentation](https://docs.phpunit.de/en/8.5/configuration.html). This example explains configuring PHPUnit to search in the directories `<plugin root>/src/Test` and `<plugin root>/src/Migration/Test` for your tests.

The `phpunit.xml` can be autogenerated for you with the `bin/console plugin:create` command:

xml

```shiki
// <plugin root>/phpunit.xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.3/phpunit.xsd"
         bootstrap="tests/TestBootstrap.php"
         executionOrder="random">
    <coverage>
        <include>
            <directory>./src/</directory>
        </include>
    </coverage>
    <php>
        <ini name="error_reporting" value="-1"/>
        <server name="KERNEL_CLASS" value="Shopware\Core\Kernel"/>
        <env name="APP_ENV" value="test"/>
        <env name="APP_DEBUG" value="1"/>
        <env name="SYMFONY_DEPRECATIONS_HELPER" value="weak"/>
    </php>
    <testsuites>
        <testsuite name="migration">
            <directory>Migration/Test</directory>
        </testsuite>
    
        <testsuite name="Example Testsuite">
            <directory>Test</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

This command will also generate a `TestBootstrap.php` file:

php

```shiki
// <plugin root>/tests/TestBootstrap.php
<?php declare(strict_types=1);

use Shopware\Core\TestBootstrapper;

$loader = (new TestBootstrapper())
    ->addCallingPlugin()
    ->addActivePlugins('BasicExample')
    ->setForceInstallPlugins(true)
    ->bootstrap()
    ->getClassLoader();

$loader->addPsr4('Swag\\BasicExample\\Tests\\', __DIR__);
```

The `setForceInstallPlugins` method ensures that your plugin is installed and active even the test database was already build beforehand.

## Example Tests [​](#example-tests)

### Integration test [​](#integration-test)

After PHPUnit is configured, a first test can be written. In this example, a test simply tries to instantiate every `.php` class to see if any used core classes are missing. In the test, you use the `IntegrationTestBehaviour` trait, which comes with some handy features, such as automatically setting up a database transaction or clearing the cache before starting tests. This is how your test could look like:

php

```shiki
// <plugin root>/src/Test/UsedClassesAvailableTest.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test;

use PHPUnit\Framework\TestCase;
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;
use Symfony\Component\Finder\Finder;

class UsedClassesAvailableTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testClassesAreInstantiable(): void
    {
        $namespace = str_replace('\Test', '', __NAMESPACE__);

        foreach ($this->getPluginClasses() as $class) {
            $classRelativePath = str_replace(['.php', '/'], ['', '\\'], $class->getRelativePathname());

            $this->getMockBuilder($namespace . '\\' . $classRelativePath)
                ->disableOriginalConstructor()
                ->getMock();
        }

        // Nothing broke so far, classes seem to be instantiable
        $this->assertTrue(true);
    }

    private function getPluginClasses(): Finder
    {
        $finder = new Finder();
        $finder->in(realpath(__DIR__ . '/../'));
        $finder->exclude('Test');
        return $finder->files()->name('*.php');
    }
}
```

### Migration test [​](#migration-test)

In order to test the example migration `Migration1611740369ExampleDescription`, create a new test called `Migration1611740369ExampleDescriptionTest`, which extends from the PHPUnit `TestCase`. Use the `KernelTestBehaviour` trait because a database connection from the container is needed.

This is an example for a migration test:

php

```shiki
// <plugin root>/src/Migration/Test/Migration1611740369ExampleDescriptionTest.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration\Test;

use Doctrine\DBAL\Connection;
use PHPUnit\Framework\TestCase;
use Shopware\Core\Framework\Test\TestCaseBase\KernelTestBehaviour;

class Migration1611740369ExampleDescriptionTest extends TestCase
{
    use KernelTestBehaviour;

    public function testNoChanges(): void
    {
        /** @var Connection $conn */
        $conn = $this->getContainer()->get(Connection::class);
        $expectedSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];

        $migration = new Migration1611740369ExampleDescription();

        $migration->update($conn);
        $actualSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];
        static::assertSame($expectedSchema, $actualSchema, 'Schema changed!. Run init again to have clean state');

        $migration->updateDestructive($conn);
        $actualSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];
        static::assertSame($expectedSchema, $actualSchema, 'Schema changed!. Run init again to have clean state');
    }

    public function testNoTable(): void
    {
        /** @var Connection $conn */
        $conn = $this->getContainer()->get(Connection::class);
        $conn->executeStatement('DROP TABLE `swag_basic_example_general_settings`');

        $migration = new Migration1611740369ExampleDescription();
        $migration->update($conn);
        $exists = $conn->fetchColumn('SELECT COUNT(*) FROM `swag_basic_example_general_settings`') !== false;

        static::assertTrue($exists);
    }
}
```

## Mocking services [​](#mocking-services)

In some cases a service should behave differently in a test run. Such a case could be where a service deletes a file or makes a critical api call. To avoid this in a test run it is possible to create a `<plugin root>/Resources/config/services_test.{xml|yml}` file which will override your `<plugin root>/Resources/config/services.{xml|yml}`. But only for the test environment.

In this test-only service config you can override arguments, aliases or parameters to change what the service container injects into services during a test run.

## Executing the test [​](#executing-the-test)

To execute tests, a PHPUnit binary is necessary, which is most likely located in the `vendor/bin` folder. The command below will use the `phpunit.xml` file in the `custom/plugins/SwagBasicExample` folder and execute the testsuite with the name `migration`.

sh

```shiki
// <project root>
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --testsuite "migration"
```

### Executing all tests in the plugin [​](#executing-all-tests-in-the-plugin)

If no testsuite is passed, it will execute all testsuites.

shell

```shiki
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample"
```

### Executing a single class or method [​](#executing-a-single-class-or-method)

To execute a specific test class or method of a testsuite, pass the argument `--filter` with the name of the class or method.

shell

```shiki
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --filter testNoChanges
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --filter Migration1611740369ExampleDescriptionTest
```

## Flex template [​](#flex-template)

In order to run PHPunit tests install the flex template [dev-tools](./../../../../guides/installation/template.html#how-do-i-migrate-from-production-template-to-symfony-flex) package via composer.

shell

```shiki
composer require --dev dev-tools
```

## Next steps [​](#next-steps)

Running unit tests with javascript code is explained in the following two articles:

* [Jest unit tests in Shopware's Administration](./jest-admin.html)
* [Jest unit tests in Shopware's Storefront](./jest-storefront.html)

---

