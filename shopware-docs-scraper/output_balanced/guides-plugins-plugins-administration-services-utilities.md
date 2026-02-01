# Guides Plugins Plugins Administration Services Utilities

*Scraped from Shopware Developer Documentation*

---

## Making API requests

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/making-api-requests.html

# Making API Requests [​](#making-api-requests)

## Overview [​](#overview)

In this guide you'll learn how to create a custom API service in your plugin's administration to make HTTP requests to the Shopware API. This is useful when you need to communicate with custom backend endpoints or extend Shopware's API functionality.

## Prerequisites [​](#prerequisites)

In order to add your own custom API service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](./../../plugin-base-guide.html).

You also need to have a custom administration module or component. Refer to [Add custom module](./../module-component-management/add-custom-module.html) to get started.

## Creating the API service [​](#creating-the-api-service)

First, create a new API service class that extends Shopware's `ApiService` class. This provides you with all the necessary methods for authentication and HTTP communication.

Create the service file in your plugin's administration source directory:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/api/my-api-service.js
const { ApiService } = Shopware.Classes;

class MyApiService extends ApiService {
    constructor(httpClient, loginService, apiEndpoint = '_action/my-plugin') {
        super(httpClient, loginService, apiEndpoint);
    }

    // GET request example
    getMyData() {
        const apiRoute = `${this.getApiBasePath()}/my-data`;
        return this.httpClient
            .get(apiRoute, {
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // POST request example with data
    createMyData(data) {
        const apiRoute = `${this.getApiBasePath()}/my-data`;
        return this.httpClient
            .post(
                apiRoute,
                data,
                {
                    headers: this.getBasicHeaders(),
                }
            )
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // DELETE request example
    deleteMyData(id) {
        const apiRoute = `${this.getApiBasePath()}/my-data/${id}`;
        return this.httpClient
            .delete(apiRoute, {
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // GET request with query parameters
    searchMyData(searchTerm, limit = 25) {
        const apiRoute = `${this.getApiBasePath()}/my-data/search`;
        return this.httpClient
            .get(apiRoute, {
                params: {
                    term: searchTerm,
                    limit: limit,
                },
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }
}

export default MyApiService;
```

## Registering the service [​](#registering-the-service)

To make your API service available throughout your plugin's administration, you need to register it as a service provider. Create an index file to handle the registration:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/api/index.js
import MyApiService from './my-api-service';

const { Application } = Shopware;

Application.addServiceProvider('myApiService', (container) => {
    const initContainer = Application.getContainer('init');

    return new MyApiService(
        initContainer.httpClient,
        container.loginService
    );
});
```

Don't forget to import this file in your plugin's main administration entry point:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js
import './api';
// ... other imports
```

## Using the API service in components [​](#using-the-api-service-in-components)

Now you can inject and use your API service in any component within your plugin:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/module/my-module/component/my-component/index.js
import template from './template.twig';

const { Component, Mixin } = Shopware;

Component.register('my-component', {
    template,
    inject: ['myApiService'],
    mixins: [Mixin.getByName('notification')],

    data() {
        return {
            myData: [],
            isLoading: false,
        };
    },

    created() {
        this.loadData();
    },

    methods: {
        async loadData() {
            this.isLoading = true;
            
            try {
                this.myData = await this.myApiService.getMyData();
                
                this.createNotificationSuccess({
                    message: 'Data loaded successfully',
                });
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'An error occurred',
                });
            } finally {
                this.isLoading = false;
            }
        },

        async saveData(data) {
            this.isLoading = true;
            
            try {
                await this.myApiService.createMyData(data);
                
                this.createNotificationSuccess({
                    message: 'Data saved successfully',
                });
                
                // Reload data after saving
                await this.loadData();
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'Failed to save data',
                });
            } finally {
                this.isLoading = false;
            }
        },

        async deleteItem(id) {
            try {
                await this.myApiService.deleteMyData(id);
                
                this.createNotificationSuccess({
                    message: 'Item deleted successfully',
                });
                
                // Reload data after deletion
                await this.loadData();
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'Failed to delete item',
                });
            }
        }
    },
});
```

## Working with authentication [​](#working-with-authentication)

The `ApiService` base class automatically handles authentication by including the necessary headers. The `getBasicHeaders()` method provides:

* Authorization token
* Content-Type headers
* API version headers

If you need custom headers, you can extend them:

javascript

```shiki
getCustomData() {
    const headers = {
        ...this.getBasicHeaders(),
        'X-Custom-Header': 'custom-value'
    };

    return this.httpClient
        .get(`${this.getApiBasePath()}/custom-endpoint`, { headers })
        .then((response) => {
            return ApiService.handleResponse(response);
        });
}
```

## Error handling [​](#error-handling)

The `ApiService.handleResponse()` method automatically handles common HTTP errors. However, you should still implement proper error handling in your components:

javascript

```shiki
async performApiCall() {
    try {
        const result = await this.myApiService.getMyData();
        // Handle success
    } catch (error) {
        // Check for specific error types
        if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Error status:', error.response.status);
            console.error('Error data:', error.response.data);
        } else if (error.request) {
            // The request was made but no response was received
            console.error('No response received:', error.request);
        } else {
            // Something happened in setting up the request
            console.error('Error:', error.message);
        }
    }
}
```

## Advanced usage [​](#advanced-usage)

### File uploads [​](#file-uploads)

For file uploads, you can use FormData:

javascript

```shiki
uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.httpClient.post(
        `${this.getApiBasePath()}/upload`,
        formData,
        {
            headers: {
                ...this.getBasicHeaders(),
                'Content-Type': 'multipart/form-data',
            },
        }
    ).then((response) => {
        return ApiService.handleResponse(response);
    });
}
```

### Accessing standard Shopware APIs [​](#accessing-standard-shopware-apis)

You can also access Shopware's standard APIs using the repository pattern:

javascript

```shiki
Component.register('my-component', {
    inject: ['repositoryFactory'],

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    methods: {
        async loadProducts() {
            const criteria = new Shopware.Data.Criteria();
            criteria.setPage(1);
            criteria.setLimit(25);
            
            const products = await this.productRepository.search(criteria);
            // Use products...
        }
    }
});
```

## Next steps [​](#next-steps)

Now that you've created your API service, you might want to:

* Create the corresponding backend API endpoints
* Add more complex API interactions
* Implement caching strategies for better performance
* Add request interceptors for global error handling

For more information on creating backend API endpoints, refer to the [API documentation](./../../../../../concepts/api/).

---

## Adding Services

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/add-custom-service.html

# Adding Services [​](#adding-services)

## Overview [​](#overview)

This guide will teach you how to add a service to the Shopware 6 Administration, using [BottleJS](https://github.com/young-steveo/bottlejs).

This documentation chapter will cover the following topics:

* What is an Administration service?
* How to register a new Administration service for your plugin

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Register a new service [​](#register-a-new-service)

For this example, we want to use the following service. It's supposed to get random jokes. It is placed in `<administration root>/services/joke.service.js` and looks like the example seen below:

javascript

```shiki
export default class JokeService {
    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    joke() {
        return this.httpClient
            .get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political')
            .then(response => response.data)
    }
}
```

For now this service class is not available in the injection container. To fix this, a new script is placed at `<administration root>/init/joke-service.init.js` and imported in the `main.js` file of our plugin:

javascript

```shiki
import JokeService from '../services/joke.service'

Shopware.Service().register('joker', (container) => {
    const initContainer = Shopware.Application.getContainer('init');
    return new JokeService(initContainer.httpClient);
});
```

## Service injection [​](#service-injection)

A service is typically injected into a vue component and can simply be referenced in the `inject` property:

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['joker'],

    created() {
        this.joker.joke().then(joke => console.log(joke))
    }
});
```

To avoid collision with other properties like computed fields or data fields there is an option to rename the service property using an object:

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: {
        jokeService: 'joker'
    },

    created() {
        this.jokeService.joke().then(joke => console.log(joke))
    }
});
```

## Adding a middleware [​](#adding-a-middleware)

BottleJS also allows us to add middleware to our services.

This code sample is based on the example in the [BottleJS documentation](https://github.com/young-steveo/bottlejs#middlewarename-func). For this we need to change our previously used service, as seen below:

javascript

```shiki
class JokeService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.isActive = false;
    }

    joke() {
        return this.httpClient
            .get(`https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political`)
            .then(response => response.data)
    }
}
```

Now that we've added an `isActive` flag, we can react to it in our middleware and throw an exception if the service is not active.

javascript

```shiki
Shopware.Application.addServiceProviderMiddleware('joker', (service, next) => {
    if(!service.isActive) {
        return next(new Error('Service is inActive'));
    }

    next();
});

Shopware.Service().register('joker', (container) => {
    const initContainer = Shopware.Application.getContainer('init');
    return new JokeService(initContainer.httpClient);
});
```

## Decorating a service [​](#decorating-a-service)

Service decoration can be us in a variety of ways. Services can be initialized right after their creation and single methods can get an altered behavior. Like in the service registration, a script that is part of the `main.js` is needed.

WARNING

Decorators are just simple functions, which intercept a service in the provider phase. This means that a service can only be decorated in the timeframe between it being created and it being accessed for the first time.

If you need to alter a service method return value or add an additional parameter you can also do this using decoration. For this example a `funny` attribute is added to the requested jokes by the previously registered `JokeService`:

javascript

```shiki
Shopware.Application.addServiceProviderDecorator('joker', joker => {
    const decoratedMethod = joker.joke;

    joker.joke = function () {
        return decoratedMethod.call(joker).then(joke => ({
            ...joke,
            funny: joke.id % 2 === 0
        }))
    };

    return joker;
});
```

## Next steps [​](#next-steps)

Now that we have created a service, you might want to create or customize a Administration component:

* [Creating a new administration component](./../module-component-management/add-custom-component.html)
* [Extending an existing administration component](./../module-component-management/customizing-components.html) .

---

## Extending Services

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/extending-services.html

# Extending services [​](#extending-services)

## Overview [​](#overview)

This guide will teach you how to extend a Shopware provided service with middleware and decorators. The Shopware 6 Administration uses [BottleJS](https://github.com/young-steveo/bottlejs) to provide the framework for services. If you want to learn how to create your own services, look at [this guide](./add-custom-service.html).

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Reset Providers [​](#reset-providers)

The [`resetProviders`](https://github.com/young-steveo/bottlejs#resetprovidersnames) function is used to reset providers for the next reference to re-instantiate the provider. You need to do this to add decorators or middleware to Shopware provided services, after they are initially instantiated in the Shopware boot-process.

javascript

```shiki
Shopware.Application.$container.resetProviders()
```

If the `names` param is passed, it will only reset the named providers.

## Adding decorators [​](#adding-decorators)

[BottleJS decorators](https://github.com/young-steveo/bottlejs#decorators) are just simple functions that intercept a service in the provider phase after it has been created, but before it is accessed for the first time. The function should return the service or another object to be used as the service instead.

With Shopware you have to reset the providers before extending Service.

Let's look at an example:

javascript

```shiki
Shopware.Application.$container.resetProviders(['acl']);

Shopware.Application.addServiceProviderDecorator('acl', (aclService) => {
  aclService.foo = 'bar';
  console.log(aclService);
  return aclService;
});
```

## Adding middleware [​](#adding-middleware)

[BottleJS middleware](https://github.com/young-steveo/bottlejs#middleware) are similar to decorators, but they are executed every time a service is accessed from the container. They are passed the service instance and a `next` function:

As mentioned before with Shopware you have to reset the providers, before extending Service.

Let's look at an Example:

javascript

```shiki
Shopware.Application.$container.resetProviders(['acl']);

Shopware.Application.addServiceProviderMiddleware('acl', (service, next) => {
    console.log('ACL service gets called');
    next();
});
```

---

## Using utility functions

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/using-utils.html

# Using utility functions [​](#using-utility-functions)

Utility functions in the Shopware 6 Administration are registered to [the Shopware object](./../data-handling-processing/the-shopware-object.html) and are therefore accessible everywhere in the Administration. They provide many useful [shortcuts](./../../../../../resources/references/administration-reference/utils.html) for common tasks.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance, the files, a registered module, and a good understanding of JavaScript.

## Accessing the utility functions [​](#accessing-the-utility-functions)

Let us see how to use one of the utility functions — for example, `capitalizeString` function. As the name implies, the `capitalizeString` function capitalizes strings by calling the [`lodash capitalize`](https://lodash.com/docs/4.17.15#capitalize) function.

javascript

```shiki
// <extension root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
const { Component, Utils } = Shopware;

Component.register('swag-basic-example', {
    data() {
        return {
            text: 'hello',
            capitalizedString: undefined,
        };
    },

    created() {
        this.capitalize();
    },

    methods: {
        capitalize() {
            this.capitalizedString = Utils.string.capitalizeString(this.string);
        },
    },
});
```

## More, interesting topics [​](#more-interesting-topics)

* [Adding filters](./add-filter.html)
* [Adding mixins](./../mixins-directives/add-mixins.html)

---

## Add filter

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/add-filter.html

# Add filter [​](#add-filter)

## Overview [​](#overview)

In this guide you'll learn, how to create a filter for the Shopware Administration. A filter is just a little helper for formatting text. In this example, we create a filter that converts text into uppercase and adds an underscore at the beginning and end.

## Prerequisites [​](#prerequisites)

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](./../../plugin-base-guide.html).

## Creating the filter [​](#creating-the-filter)

First we create a new file in the directory `<plugin root>/src/Resources/app/administration/src/app/filter`. In this case we name our filter `example`, so our file will be named `example.filter.js`.

Here's an example how your filter could look like:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/app/filter/example.filter.js
const { Filter } = Shopware;

Filter.register('example', (value) => {
    if (!value) {
        return '';
    }

    return `_${value.toLocaleUpperCase()}_`;
});
```

As you can see, it's very simple. We use `Filter` from the `Shopware` object where we can register our filter with the method `register`. The first argument we pass is the name of our filter, which is `example`. The second argument is a function with which we format our text.

If you want to use multiple arguments in your filter function, it could look like this:

javascript

```shiki
Filter.register('example', (value, secondValue, thirdValue) => {
    ...
});
```

Last, import the filter into your plugin's `main.js` file.

## Next steps [​](#next-steps)

Now that you know how to create a filter for the Administration, we want to use it in our code. For this head over to our [using filter](./using-filter.html) guide.

---

## Using filter

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/using-filter.html

# Using filter [​](#using-filter)

## Overview [​](#overview)

In this guide you'll learn how to use filters in the Shopware Administration.

## Prerequisites [​](#prerequisites)

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](./../../plugin-base-guide.html).

Furthermore you should have a look at our [add filter](./add-filter.html) guide, since this guide is built upon it.

## Using the filter [​](#using-the-filter)

In this section we will show you, how to use our `example` filter in JavaScript code and in your Twig template files.

### Filter in components JavaScript [​](#filter-in-components-javascript)

If we want to use the filter in our components JavaScript files, we can access it by using `this.$options.filters` and the name of our filter.

javascript

```shiki
this.$options.filters.example('firstArgument')
```

### Filter in Twig templates [​](#filter-in-twig-templates)

If we want to use our filter in Twig templates, we can easily use it by using a pipe `|` and the name of our filter. It is also possible to use filters in `v-bind` expressions.

Below you can see two example implementations, how it could be done with single argument filters.

twig

```shiki
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText')|example }}
    </p>
{% endblock %}
```

html

```shiki
<example-component :name="$tc('swag-example.general.myCustomText')|example"></example-component>
```

When using multiple arguments, we can pass them as shown below.

twig

```shiki
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText')|example('secondArgument', 'thirdArgument') }}
    </p>
{% endblock %}
```

html

```shiki
<example-component :title="$tc('swag-example.general.myCustomText')|example('secondArgument', 'thirdArgument')"></example-component>
```

---

## Injecting services

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/injecting-services.html

# Injecting services [​](#injecting-services)

## Overview [​](#overview)

This short guide will teach you how to use a service in the Shopware 6 Administration.

Along these lines, this chapter will cover the following topics:

* What is an Administration service?
* How to use a service?

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Definition of an Administration service [​](#definition-of-an-administration-service)

Shopware 6 uses [bottleJS](https://github.com/young-steveo/bottlejs) to inject services. Services are small self-contained utility classes, like the [repositoryFactory](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/core/data-new/repository-factory.data.js), which provides a way to talk to the API.

## Injection of a service [​](#injection-of-a-service)

A service is typically injected into a vue component and can simply be referenced in the `inject` property. This service is then available via its name on the object instance.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    // inject the service
    inject: ['repositoryFactory'],

    created() {
        // insatiate the injected repositoryFactory 
        this.productRepository = this.repositoryFactory.create('product')
    }
});
```

---

## The Sanitizer helper

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/services-utilities/the-sanitizer-helper.html

# The Sanitizer helper [​](#the-sanitizer-helper)

## Overview [​](#overview)

The Shopware 6 Sanitizer Helper is a wrapper around [`DOMPurify`](https://github.com/cure53/DOMPurify), which is used to sanitize HTML in order to prevent `XSS attacks`.

## Where is it registered? [​](#where-is-it-registered)

The Sanitizer Helper is registered to the [Shopware Global Object](./../data-handling-processing/the-shopware-object.html) and therefore can be accessed anywhere in your plugin.

javascript

```shiki
const sanitizer = Shopware.Helper.SanitizerHelper;
```

It also is registered in the Vue prototype as seen [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/app/plugin/sanitize.plugin.js). This means it can also be accessed in your components like this:

javascript

```shiki
const Sanitizer = this.$sanitizer;
const sanitize = this.$sanitize;
```

## Sanitizing HTML [​](#sanitizing-html)

As mentioned before the `SanitizerHelper` is registered to the [Shopware Global Object](./../data-handling-processing/the-shopware-object.html) and therefore can be accessed like this everywhere:

javascript

```shiki
Shopware.Helper.SanitizerHelper.sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

And since it is bound to the Vue prototype it can be used in all Vue components like this:

javascript

```shiki
this.$sanitizer.sanitize('<svg><g/onload=alert(2)//<p>'); // becomes <svg><g></g></svg>
this.$sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

## How to set the config [​](#how-to-set-the-config)

The config can be set with the `setConfig` and cleared with the `clearConfig` function, as seen below:

javascript

```shiki
Shopware.Helper.SanitizerHelper.setConfig({
    USE_PROFILES: { html: true }
});

Shopware.Helper.SanitizerHelper.clearConfig()
```

See all of the configuration options [here](https://github.com/cure53/DOMPurify#can-i-configure-dompurify)

## How to add hooks [​](#how-to-add-hooks)

The aforementioned Wrapper also provides functions to add and remove hooks to DOMPurify. Learn what DOMPurify hooks are in their [documentation](https://github.com/cure53/DOMPurify#hooks).

javascript

```shiki
Shopware.Helper.SanitizerHelper.addMiddleware('beforeSanitizeElements',  function (
        currentNode,
        hookEvent,
        config
    ) {
        // Do something with the current node and return it
        // You can also mutate hookEvent (i.e. set hookEvent.forceKeepAttr = true)
        return currentNode;
    }
);

Shopware.Helper.SanitizerHelper.removeMiddleware('beforeSanitizeElements');
```

---

