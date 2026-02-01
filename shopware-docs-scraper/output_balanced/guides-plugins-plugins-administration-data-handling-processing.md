# Guides Plugins Plugins Administration Data Handling Processing

*Scraped from Shopware Developer Documentation*

---

## Using the data handling

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/using-data-handling.html

# Using the data handling [​](#using-the-data-handling)

The Shopware 6 Administration allows you to fetch and write nearly everything in the database. This guide will teach you the basics of the data handling.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line and preferably registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

Considering that the data handling in the Administration is remotely operating the Data Abstraction Layer its highly encouraged to read the articles [Reading data with the DAL](./../../../../../guides/plugins/plugins/framework/data-handling/reading-data.html) and [Writing data with the DAL](./../../../../../guides/plugins/plugins/framework/data-handling/writing-data.html).

## Relevant classes [​](#relevant-classes)

`Repository`: Allows to send requests to the server - used for all CRUD operations `Entity`: Object for a single storage record `EntityCollection`: Enable object-oriented access to a collection of entities `SearchResult`: Contains all information available through a search request `RepositoryFactory`: Allows to create a repository for an entity `Context`: Contains the global state of the Administration (language, version, auth, ...) `Criteria`: Contains all information for a search request (filter, sorting, pagination, ...)

## The repository service [​](#the-repository-service)

Accessing the Shopware API in the Administration is done by using the repository service, which can be injected with a [bottleJs](https://github.com/young-steveo/bottlejs) dependency injection container. In the Shopware Administration, there's a wrapper that makes `bottleJs` work with the [inject / provide](https://vuejs.org/v2/api/#provide-inject) from [`Vue`](https://vuejs.org/). In short: You can use the `inject` key in your component configuration to fetch services from the `bottleJs` DI container, such as the `repositoryFactory`, that you will need in order to get a repository for a single entity.

Add those lines to your component configuration:

javascript

```shiki
inject: [
    'repositoryFactory'
],
```

This way the `repositoryFactory` object is accessible in your component. The `create` function can be used to create a repository for a single entity, like in this example:

javascript

```shiki
const productRepository = this.repositoryFactory.create('product')
```

Note: You can also change some options in the repository, with the third parameter:

javascript

```shiki
Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            repository: undefined
        }
    },

    created() {
        const options = {
            version: 1 // default is the latest api version
        };

        this.repository = this.repositoryFactory.create('product', null, options);
    }
});
```

Note: The version 1 used in the options is just an example, how to select a version. Then again the default would be the newest version. There are no other options.

## Working with the criteria class [​](#working-with-the-criteria-class)

To fetch data from the server, the repository has a `search` function. Each repository function requires the API `context` and `criteria` class, which contains all functionality of the core criteria class. If you want to see all the options take a look at the file [src/Administration/Resources/app/administration/src/core/data/criteria.data.ts](https://github.com/shopware/meteor/blob/main/packages/admin-sdk/src/data/Criteria.ts).

javascript

```shiki
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            result: undefined
        }
    },

    computed: {
        productRepository() {
            // create a repository for the `product` entity
            return this.repositoryFactory.create('product');
        },
    },

    created() {
        const criteria = new Criteria();

        criteria.setPage(1);
        criteria.setLimit(10);
        criteria.setTerm('foo');
        criteria.setIds(['some-id', 'some-id']); // Allows to provide a list of ids which are used as a filter

        /**
            * Configures the total value of a search result.
            * 0 - no total count will be selected. Should be used if no pagination required (fastest)
            * 1 - exact total count will be selected. Should be used if an exact pagination is required (slow)
            * 2 - fetches limit * 5 + 1. Should be used if pagination can work with "next page exists" (fast)
        */
        criteria.setTotalCountMode(2);

        criteria.addFilter(
            Criteria.equals('product.active', true)
        );

        criteria.addSorting(
            Criteria.sort('product.name', 'DESC')
        );

        criteria.addAggregation(
            Criteria.avg('average_price', 'product.price')
        );

        criteria.getAssociation('categories')
            .addSorting(Criteria.sort('category.name', 'ASC'));

        this.productRepository
            .search(criteria, Shopware.Context.api)
            .then(result => {
                this.result = result;
            });
    }
});
```

## How to fetch a single entity [​](#how-to-fetch-a-single-entity)

Since the context of an edit or update form is usually a single root entity, the data handling diverges here from the Data Abstraction Layer and provides loading of a single resource from the Admin API.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entity: undefined
        }
    },
    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        const entityId = 'some-id';

        this.productRepository
            .get(entityId, Shopware.Context.api)
            .then(entity => {
                this.entity = entity;
            });
    }
});
```

## Update an entity [​](#update-an-entity)

The data handling contains change tracking and sends only changed properties to the Admin API endpoint. Please be aware that in order to be as transparent as possible, updating data will not be handled automatically. A manual update is mandatory.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entityId: '1de38487abf04705810b719d4c3e8faa',
            entity: undefined
        }
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        this.productRepository
            .get(this.entityId, Shopware.Context.api)
            .then(entity => {
                this.entity = entity;
            });
    },

    methods: {
        // a function which is called over the ui
        updateTrigger() {
            this.entity.name = 'updated';

            // sends the request immediately
            this.productRepository
                .save(this.entity, Shopware.Context.api)
                .then(() => {
                    // the entity is stateless, the data has be fetched from the server, if required
                    this.productRepository
                        .get(this.entityId, Shopware.Context.api)
                        .then(entity => {
                            this.entity = entity;
                        });
                });
        }
    }
});
```

## Delete an entity [​](#delete-an-entity)

The `delete` method sends a `delete` request for a provided id. To delete multiple entities at once use the `syncDeleted` method by passing an array of `ids`.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        this.productRepository.delete('1de38487abf04705810b719d4c3e8faa', Shopware.Context.api);
    }
});
```

## Create an entity [​](#create-an-entity)

Although entities are detached from the data handling once retrieved or created they still must be set up through a repository. You can create an entity by using the `this.repositoryFactory.create()` method, fill it with data and save it as seen below:

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entity: undefined
        }
    },

    computed: {
        manufacturerRepository() {
            return this.repositoryFactory.create('product_manufacturer');
        }
    },

    created() {
        this.entity = this.manufacturerRepository.create(Shopware.Context.api);

        this.entity.name = 'test';

        this.manufacturerRepository.save(this.entity, Shopware.Context.api);
    }
});
```

## Working with associations [​](#working-with-associations)

Each association can be accessed via normal property access:

javascript

```shiki
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined
        }
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        productCriteria() {
            return new Criteria()
                .addAssociation('manufacturer')
                .addAssociation('categories')
                .addAssociation('prices');
        }
    },

    created() {
        this.repository = this.repositoryFactory.create('product');

        const entityId = '66338d4e19f749fd90b59032134ecb74';

        this.repository
            .get(entityId, Shopware.Context.api, this.productCriteria)
            .then(product => {
                this.product = product;

                // ManyToOne: contains an entity class with the manufacturer data
                console.log(this.product.manufacturer);

                // ManyToMany: contains an entity collection with all categories.
                // contains a source property with an api route to reload this data (/product/{id}/categories)
                console.log(this.product.categories);

                // OneToMany: contains an entity collection with all prices
                // contains a source property with an api route to reload this data (/product/{id}/prices)            
                console.log(this.product.prices);
            });
    }
});
```

### Set a ManyToOne [​](#set-a-manytoone)

If you have a ManyToOne association, you can write changes as seen below:

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined,
        };
    },

    computed: {

        productRepository() {
            return this.repositoryFactory.create('product');
        },
        manufacturerRepository() {
            return this.repositoryFactory.create('product_manufacturer');
        }
    },

    created() {
        this.productRepository
            .get('some-product-id', Shopware.Context.api)
            .then((product) => {
                this.product = product;

                this.product.manufacturerId = 'some-manufacturer-id'; // manually set the foreign key y

                this.productRepository.save(this.product, Shopware.Context.api);
            });
    },
});
```

### Working with lazy loaded associations [​](#working-with-lazy-loaded-associations)

In most cases, *ToMany* associations can be loaded by adding a the association with the `.addAssociation()` method of the Criteria object.

javascript

```shiki
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        productCriteria() {
            const criteria = new Criteria();
            criteria.addAssociation('prices');

            return criteria;
        }
    },

    created() {
        this.productRepository
            .get('some-id', Shopware.Context.api, this.productCriteria)
            .then((product) => {
                this.product = product;
            });
    }

});
```

### Working with OneToMany associations [​](#working-with-onetomany-associations)

The following example shows how to create a repository based on associated data. In this case the `priceRepository` contains associated `prices` to the product with the `id` 'some-id'.

javascript

```shiki
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined,
            prices: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        priceRepository() {
            if (!this.product) {
                return undefined;
            };

            return this.repositoryFactory.create(
                // `product_price`
                this.product.prices.entity,
                // `product/some-id/priceRules`
                this.product.prices.source
            );
        }
    },

    created() {
        this.productRepository
            .get('some-product-id', Shopware.Context.api)
            .then((product) => {
                this.product = product;
            });
    },

    methods: {
        loadPrices() {
            this.priceRepository
                .search(new Criteria(), Shopware.Context.api)
                .then((prices) => {
                    this.prices = prices;
                });
        },

        addPrice() {
            const newPrice = this.priceRepository.create(Shopware.Context.api);

            newPrice.quantityStart = 1;
          // Note: there are more things required than just the quantityStart

            this.priceRepository
                .save(newPrice, Shopware.Context.api)
                .then(this.loadPrices);
        },

        deletePrice(priceId) {
            this.priceRepository
                .delete(priceId, Shopware.Context.api)
                .then(this.loadPrices);
        },

        updatePrice(price) {
            this.priceRepository
                .save(price, Shopware.Context.api)
                .then(this.loadPrices);
        }
    }
});
```

### Working with ManyToMany associations [​](#working-with-manytomany-associations)

The following example shows how to create a repository based on associated data. In this case the `categoryRepository` contains associated categories to the product with the `id` 'some-id'.

javascript

```shiki
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined,
            categories: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        categoryRepository() {
            if (!this.product) {
                return undefined;
            };

            return this.repositoryFactory.create(
                // `product_categories`
                this.product.categories.entity,
                // `product/some-id/categories`
                this.product.categories.source
            );
        }
    },

    created() {
        this.productRepository
            .get('some-product-id', Shopware.Context.api)
            .then((product) => {
                this.product = product;
            });
    },

    methods: {
        loadCategories() {
            this.categoryRepository
                .search(new Criteria(), Shopware.Context.api)
                .then((categories) => {
                    this.categories = categories;
                });
        },

        addCategoryToProduct(category) {
            this.categoryRepository
                .assign(category.id, Shopware.Context.api)
                .then(this.loadCategories);
        },

        removeCategoryFromProduct(categoryId) {
            this.categoryRepository
                .delete(categoryId, Shopware.Context.api)
                .then(this.loadCategories);
        }
    }
});
```

### Working with local associations [​](#working-with-local-associations)

In case of a new entity, the associations can not be sent directly to the server using the repository, because the parent entity isn't saved yet. For example: You can not add prices to a product which is not even saved in the database yet.

For this case the association can be used as storage as well and will be updated with the parent entity. In the following examples, `this.productRepository.save(this.product, Shopware.Context.api)` will send the prices and category changes.

Notice: It is mandatory to `add` entities to collections in order to get reactive data for the UI.

#### Working with local OneToMany associations [​](#working-with-local-onetomany-associations)

The following example shows how to create a repository based on associated data. In this case the `priceRepository` contains associated `prices` to the product with the `id` 'some-id'.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        priceRepository() {
            if (!this.product) {
                return undefined;
            };

            this.priceRepository = this.repositoryFactory.create(
                // `product_price`
                this.product.prices.entity,
                // `product/some-id/priceRules`
                this.product.prices.source
            );
        }
    },

    created() {
        this.productRepository
            .get('some-id', Shopware.Context.api)
            .then(product => {
                this.product = product;

            });
    },
    methods: {
        loadPrices() {
            this.prices = this.product.prices;
        },

        addPrice() {
            const newPrice = this.priceRepository
                .create(Shopware.Context.api);

            newPrice.quantityStart = 1;
            // update some other fields

            this.product.prices.add(newPrice);
        },

        savePrice() {
            this.productRepository.save(this.product)
        },

        deletePrice(priceId) {
            this.product.prices.remove(priceId);
        },

        updatePrice(price) {
            // price entity is already updated and already assigned to product, no sources needed 
        }
    }
});
```

#### Working with local ManyToMany associations [​](#working-with-local-manytomany-associations)

The following example shows how to create a repository based on associated data. In this case the `categoryRepository` contains associated categories to the product with the `id` 'some-id'.

javascript

```shiki
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined,
            prices: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        priceRepository() {
            if (!this.product) {
                return undefined;
            };

            return this.repositoryFactory.create(
                // `product_price`
                this.product.prices.entity,
                // `product/some-id/priceRules`
                this.product.prices.source
            );
        }
    },

    created() {
        this.productRepository
            .get('some-id', Shopware.Context.api)
            .then(product => {
                this.product = product;
            });
    },
    methods: {
        loadPrices() {
            this.prices = this.product.prices;
        },

        addPrice() {
            const newPrice = this.priceRepository
                .create(Shopware.Context.api);

            newPrice.quantityStart = 1;
            // update some other fields

            this.product.prices.add(newPrice);
        },

        savePrice() {
            this.productRepository.save(this.product)
        },

        deletePrice(priceId) {
            this.product.prices.remove(priceId);
        },

        updatePrice(price) {
            // price entity is already updated and already assigned to product, no sources needed 
        }
    }
});
```

#### Working with entity extensions [​](#working-with-entity-extensions)

The following example shows how to pass on and save data of entity extensions.

javascript

```shiki
import template from './swag-paypal-pos-wizard.html.twig';
import './swag-paypal-pos-wizard.scss';
import {
    PAYPAL_POS_SALES_CHANNEL_EXTENSION,
    PAYPAL_POS_SALES_CHANNEL_TYPE_ID,
} from '../../../../../constant/swag-paypal.constant';

const { Component, Context } = Shopware;
const { Criteria } = Shopware.Data;

Component.extend('swag-paypal-pos-wizard', 'sw-first-run-wizard-modal', {
    template,

    inject: [
        'SwagPayPalPosApiService',
        'SwagPayPalPosSettingApiService',
        'SwagPayPalPosWebhookRegisterService',
        'salesChannelService',
        'repositoryFactory',
    ],

    mixins: [
        'swag-paypal-pos-catch-error',
        'notification',
    ],

    data() {
        return {
            showModal: true,
            isLoading: false,
            salesChannel: {},
            cloneSalesChannelId: null,
            stepperPages: [
                'connection',
                'connectionSuccess',
                'connectionDisconnect',
                'customization',
                'productSelection',
                'syncLibrary',
                'syncPrices',
                'finish',
            ],
            stepper: {},
            currentStep: {},
        };
    },

    metaInfo() {
        return {
            title: this.wizardTitle,
        };
    },

    computed: {

        paypalPosSalesChannelRepository() {
            return this.repositoryFactory.create('swag_paypal_pos_sales_channel');
        },

        salesChannelRepository() {
            return this.repositoryFactory.create('sales_channel');
        },

        salesChannelCriteria() {
            return (new Criteria(1, 500))
                .addAssociation(PAYPAL_POS_SALES_CHANNEL_EXTENSION)
                .addAssociation('countries')
                .addAssociation('currencies')
                .addAssociation('domains')
                .addAssociation('languages');
        },
    },

    watch: {
        '$route'(to) {
            this.handleRouteUpdate(to);
        },
    },

    mounted() {
        this.mountedComponent();
    },

    methods: {
        //...
        
        createdComponent() {
            //...
            this.createNewSalesChannel();
        },

        save(activateSalesChannel = false, silentWebhook = false) {
            if (activateSalesChannel) {
                this.salesChannel.active = true;
            }

            return this.salesChannelRepository.save(this.salesChannel, Context.api).then(async () => {
                this.isLoading = false;
                this.isSaveSuccessful = true;
                this.isNewEntity = false;

                this.$root.$emit('sales-channel-change');
                await this.loadSalesChannel();

                this.cloneProductVisibility();
                this.registerWebhook(silentWebhook);
            }).catch(() => {
                this.isLoading = false;

                this.createNotificationError({
                    message: this.$tc('sw-sales-channel.detail.messageSaveError', 0, {
                        name: this.salesChannel.name || this.placeholder(this.salesChannel, 'name'),
                    }),
                });
            });
        },

        createNewSalesChannel() {
            if (Context.api.languageId !== Context.api.systemLanguageId) {
                Context.api.languageId = Context.api.systemLanguageId;
            }

            this.previousApiKey = null;
            this.salesChannel = this.salesChannelRepository.create(Context.api);
            this.salesChannel.typeId = PAYPAL_POS_SALES_CHANNEL_TYPE_ID;
            this.salesChannel.name = this.$tc('swag-paypal-pos.wizard.salesChannelPrototypeName');
            this.salesChannel.active = false;

            this.salesChannel.extensions.paypalPosSalesChannel
                = this.paypalPosSalesChannelRepository.create(Context.api);

            Object.assign(
                this.salesChannel.extensions.paypalPosSalesChannel,
                {
                    mediaDomain: '',
                    apiKey: '',
                    imageDomain: '',
                    productStreamId: null,
                    syncPrices: true,
                    replace: 0,
                },
            );

            this.salesChannelService.generateKey().then((response) => {
                this.salesChannel.accessKey = response.accessKey;
            }).catch(() => {
                this.createNotificationError({
                    message: this.$tc('sw-sales-channel.detail.messageAPIError'),
                });
            });
        },

        loadSalesChannel() {
            const salesChannelId = this.$route.params.id || this.salesChannel.id;
            if (!salesChannelId) {
                return new Promise((resolve) => { resolve(); });
            }

            this.isLoading = true;
            return this.salesChannelRepository.get(salesChannelId, Shopware.Context.api, this.salesChannelCriteria)
                .then((entity) => {
                    this.salesChannel = entity;
                 this.previousApiKey = entity.extensions.paypalPosSalesChannel.apiKey;
                    this.isLoading = false;
                });
        },
        //...
    },
});
```

## Next steps [​](#next-steps)

As this is very similar to the DAL it might be interesting to learn more about that. For this, head over to the section about the [data handling](./../../../../../guides/plugins/plugins/framework/data-handling/) in PHP.

---

## Using the data grid component

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/using-the-data-grid-component.html

# Using the data grid component [​](#using-the-data-grid-component)

## Overview [​](#overview)

The data grid component makes it easy to render tables with data. It also supports hiding columns or scrolling horizontally when many columns are present. This guide shows you how to use it.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line and preferably registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Creating a template for the data grid component [​](#creating-a-template-for-the-data-grid-component)

Let's create the simplest template we need in order to use the [`sw-data-grid`](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/component/data-grid/sw-data-grid/index.js).

html

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-example/swag-example.html.twig
<div>
    <sw-data-grid :data-source="dataSource" :columns="columns">
    </sw-data-grid>
</div>
```

This template will be used in a new component. Learn how to override existing components [here](./../module-component-management/customizing-components.html) .

## Declaring the data [​](#declaring-the-data)

Since this is a very basic example the following code will just statically assign data to the `dataSource` and `columns` data attribute. If you want to load data and render that instead, please consult the guide [How to use the data handling](./using-data-handling.html)

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-example/index.js
import template from 'swag-example.html.twig';

Shopware.Component.register('swag-basic-example', {
    template,

    data: function () {
        return {
            dataSource: [
                { id: 'uuid1', company: 'Wordify', name: 'Portia Jobson' },
                { id: 'uuid2', company: 'Twitternation', name: 'Baxy Eardley' },
                { id: 'uuid3', company: 'Skidoo', name: 'Arturo Staker' },
                { id: 'uuid4', company: 'Meetz', name: 'Dalston Top' },
                { id: 'uuid5', company: 'Photojam', name: 'Neddy Jensen' }
            ],
            columns: [
                { property: 'name', label: 'Name' },
                { property: 'company', label: 'Company' }
            ],
        };
    }
});
```

## More interesting topics [​](#more-interesting-topics)

* [Using base components](./../module-component-management/using-base-components.html)

---

## The Shopware object

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/the-shopware-object.html

# The Shopware object [​](#the-shopware-object)

## Overview [​](#overview)

The global `Shopware` object is the bridge between the Shopware Administration and your plugin as third party code. It provides utility functions to interface to the rest of the Administration.

WARNING

Don't try to access other parts of the Administration directly, always use the `Shopware` object.

It is bound to a window object in order to be accessible everywhere and can therefore be inspected with the browser console in the developer tools. To take a look at it, open the `Administration` in your browser and run this in the dev-tools console:

javascript

```shiki
// run this command in the dev-tools of your browser
console.log(Shopware);
```

There are lots of things bound to this object. So here is a short overview of the most commonly used parts.

## Component [​](#component)

The `Component` property of the global `Shopware` contains the component registry, which is responsible for handling the VueJS components. If you want to write your own components you have to register them with the `Component.register()` method. Those components are small reusable building blocks which you can use to implement your features.

javascript

```shiki
const { Component } = Shopware;

Component.register('sw-dashboard-index', {
    template,
});
```

Learn more about them here: [Creating administration component](./../module-component-management/add-custom-component.html)

## Module [​](#module)

The `Module` property of the global `Shopware` contains the module registry. A `Module` is an encapsulated unit of routes and pages, which implements a whole feature. For example there are modules for customers, orders, settings, etc.

javascript

```shiki
const { Module } = Shopware;

Module.register('your-module', {});
```

Learn more about them here: [Creating administration module](./../module-component-management/add-custom-module.html)

## A more general overview [​](#a-more-general-overview)

We now have discussed the most commonly used parts of the `Shopware` object, but there is much more to discover. Take a look at all these options in a brief overview below:

| Property | Description |
| --- | --- |
| ApiService | Registry which holds services to fetch data from the api |
| Component | A registry for VueJS `components` |
| Context | A set of contexts for the `app` and the `api` |
| Defaults | A collection of default values |
| Directive | A registry for [VueJS `directives`](https://vuejs.org/guide/reusability/custom-directives.html) |
| Filter | A registry for [VueJS template `filters`](https://v2.vuejs.org/v2/guide/filters.html?redirect=true) |
| Helper | A collection of helpers, e.g. the `DeviceHelper` where you can listen on the `resize` event |
| Locale | A registry for `locales` |
| Mixin | A registry for `mixins` |
| Module | A registry for `modules` |
| Plugin | An interface to add `promise`based hooks to run when the Administration launches |
| Service | A helper to get quick access to service, e.g. `Shopware.Service('snippetService')` |
| Shortcut | A registry for keyboard shortcuts |
| State | A wrapper for the [VueX](https://vuex.vuejs.org/) store to manage state |
| Utils | A collection of utility methods like `createId` |

## TypeScript declarations [​](#typescript-declarations)

INFO

TypeScript declarations are available from Shopware Version 6.4.4.0

The Shopware Administration is written in pure JavaScript. To provide you with the benefits of TypeScript and the best possible developer experience while working in JavaScript files we're providing TypeScript declaration files within the Administration. These files are helping you to understand how the Shopware object works and what arguments you have to provide for example when you're creating a new module or registering a new component.

![TypeScript declarations example](/assets/typescript-declaration-shopware-module.BcXrXxfh.gif)

In the example above you can see how the TypeScript declarations are helping you to register a module. It automatically marks your code and points out what is missing.

## Next steps [​](#next-steps)

As you might have noticed, the `Shopware` object can be used in a lot of cases. Besides registering components and modules, here are some guides about [adding filters](./../services-utilities/add-filter.html), about [adding mixins](./../mixins-directives/add-mixins.html) and about [using our utils](./../services-utilities/using-utils.html) - all by using the Shopware object.

---

## Using custom fields

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/using-custom-fields.html

# Using custom fields [​](#using-custom-fields)

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module in your own plugin. Don't know how to create an own plugin yet? Head over to the following guide:

[Plugin Base Guide](../../plugin-base-guide)

In order to craft your module, you will need to create lots on own components. If you're not sure about how to do that, take a look at the corresponding guide:

[Add custom component](../module-component-management/add-custom-component)

In addition, of course you need an entity with custom fields to be able to add those custom fields to your module to begin with. Here you can learn how to add your custom fields:

[Add custom input field to existing component](../module-component-management/add-custom-field)

## Using custom fields in your module [​](#using-custom-fields-in-your-module)

In Shopware, we provide an own component called `sw-custom-field-set-renderer` for your template, being tailored specifically to display custom field sets.

As a consequence, you're able to use this component to display your custom fields. See here:

html

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/swag-basic-example.html.twig
<sw-card title="Custom fields">
    <sw-custom-field-set-renderer
        :entity="customEntity"
        showCustomFieldSetSelection
        :sets="sets">
    </sw-custom-field-set-renderer>
</sw-card>
```

For further details on the `sw-custom-field-set-renderer` component, feel free to refer to its page in our component library:

[Homepage - Shopware Component library](https://component-library.shopware.com/components/sw-custom-field-set-renderer)

The next step is loading your custom fields. First things first, create a variable for your custom fields in `data`:

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
    data() {
        return {
            ...
            customFieldSets: null
        };
    }
```

Afterwards, you can start to integrate the custom field data into your component. Therefore, you need to create a `customFieldSetRepository` first as `computed` property. In this context, it may come in handy to already set the `customFieldSetCriteria`. Both steps can be seen in the example below:

javascript

```shiki
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
computed: {
    // Using the repository to work with customFields
    customFieldSetRepository() {
        return this.repositoryFactory.create('custom_field_set');
    },

    // sets the criteria used for your custom field set
    customFieldSetCriteria() {
        const criteria = new Criteria();

        // restrict the customFieldSets to be associated with products
        criteria.addFilter(Criteria.equals('relations.entityName', 'product'));

        // sort the customFields based on customFieldPosition
        criteria
            .getAssociation('customFields')
            .addSorting(Criteria.sort('config.customFieldPosition', 'ASC', true));

        return criteria;
    }
}
```

Now you can access your custom fields, e.g. within a `method`. In order to achieve that, you can use the `search` method as you're used to working with repositories:

javascript

```shiki
    // this will fetch the customFieldSets
    this.customFieldSetRepository.search(this.customFieldSetCriteria, Shopware.Context.api)
        .then((customFieldSets) => {
            this.customFieldSets = customFieldSets;
        });
```

---

## Add custom data to the search

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/search-custom-data.html

# Add custom data to the search [​](#add-custom-data-to-the-search)

## Overview [​](#overview)

When developing a customization that has a frequently visited entity listing, you're able to make use of an interesting opportunity: You can enable the user to take a shortcut finding his desired entry using the global search.

There are two different ways how the global search works:

* Global search without type specification
* Typed global search

They only differ in the API they use and get displayed in a slightly different way.

WARNING

Think twice about adding this shortcut because if every plugin adds their own search tag, it gets cluttered.

## Prerequisites [​](#prerequisites)

For this guide, it's necessary to have a running Shopware 6 instance and full access to both the files and a running plugin. See our plugin page guide to learn how to create your own plugins.

[Plugin Base Guide](../../plugin-base-guide)

In addition, you need a custom entity to add to the search to begin with. Head over to the following guide to learn how to achieve that:

[Adding custom complex data](../../framework/data-handling/add-custom-complex-data)

## Support custom entity via search API [​](#support-custom-entity-via-search-api)

To support an entity in the untyped global search, the entity has to be defined in one of the Administration Modules.

[Add custom module](../module-component-management/add-custom-module.md)

Add the `entity` and `defaultSearchConfiguration` values to your module to make it available to the search bar component.

javascript

```shiki
Shopware.Module.register('swag-plugin', {
    entity: 'swag_example',
    defaultSearchConfiguration: {
        _searchable: true,
        name: {
            _searchable: true,
            _score: 500,
        },
        description: {
            name: {
                _searchable: true,
                _score: 500,
            },
        },
    },
});
```

## Support in the Administration UI [​](#support-in-the-administration-ui)

### Add search tag [​](#add-search-tag)

The search tag displays the entity type used in the typed search and is a clickable button to switch from the untyped to the typed search. To add the tag, a service decorator is used to add a type to the `searchTypeService`:

javascript

```shiki
const { Application } = Shopware;

Application.addServiceProviderDecorator('searchTypeService', searchTypeService => {
    searchTypeService.upsertType('foo_bar', {
        entityName: 'foo_bar',
        placeholderSnippet: 'foo-bar.general.placeholderSearchBar',
        listingRoute: 'foo.bar.index',
        hideOnGlobalSearchBar: false,
    });

    return searchTypeService;
});
```

Let's take a closer look at how this decorator is used:

* The key and `entityName` is used as the same to change also existing types.
* This service can be overridden with an own implementation for customization.
* The `placeholderSnippet` is a translation key that is shown when no search term is entered.
* The `listingRoute` is used to show a link to continue the search in the module-specific listing view.
* The `hideOnGlobalSearchBar` is used to determine whether the entity should be searched when searching globally untyped.

### Add the search result item [​](#add-the-search-result-item)

By default, the search bar does not know how to display the result items, so a current search request will not show any result. In order to declare a search result view the `sw-search-bar-item` template has to be altered as seen below, starting with the template:

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-bar-item/sw-search-bar-item.html.twig
{% block sw_search_bar_item_cms_page %}
    {% parent %}

    <router-link v-else-if="type === 'foo_bar'"
                 v-bind:to="{ name: 'foo.bar.detail', params: { id: item.id } }"
                 ref="routerLink"
                 class="sw-search-bar-item__link">
        {% block sw_search_bar_item_foo_bar_label %}
            <span class="sw-search-bar-item__label">
                <sw-highlight-text v-bind:searchTerm="searchTerm"
                                   v-bind:text="item.name">
                </sw-highlight-text>
            </span>
        {% endblock %}
    </router-link>
{% endblock %}
```

Here you see the changes in the `index.js` file:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js

Shopware.Component.override('sw-search-bar-item', () => import('./app/component/structure/sw-search-bar-item'));
```

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-bar-item/index.js
import template from './sw-search-bar-item.html.twig';

export default {
    template
};
```

The `sw_search_bar_item_cms_page` block is used as it is the last block, but it is not important which shopware type is extended as long as the vue else-if structure is kept working.

### Add custom show more results link [​](#add-custom-show-more-results-link)

By default, the search bar tries to resolve to the registered listing route. If your entity can be searched externally you can edit the `sw-search-more-results` or `sw-search` components as well:

twig

```shiki
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-more-results/sw-search-more-results.html.twig
{% block sw_search_more_results %}
    <template v-if="result.entity === 'foo_bar'">
        There are so many hits.
        <a :href="'https://my.erp.localhost/?q=' + searchTerm"
           class="sw-search-bar-item__link"
           target="_blank">
             Look it directly up
        </a>
        in the ERP instead.
    </template>
    <template v-else>
        {% parent %}
    </template>
{% endblock %}
```

See for the changes in the `index.js` file below:

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/main.js

Shopware.Component.override('sw-search-more-results', () => import('./app/component/structure/sw-search-more-results'));
```

javascript

```shiki
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-more-results/index.js
import template from './sw-search-more-results.html.twig';

export default {
    template
};
```

### Potential pitfalls [​](#potential-pitfalls)

In case of a tag with a technical name with a missing translation, proceed like this:

json

```shiki
{
    "global": {
        "entities": {
            "my_entity": "My entity | My entities"
        }
    }
}
```

To change the color of the tag, or the icon in the untyped global search, a module has to be registered with an entity reference in the module:

javascript

```shiki
Shopware.Module.register('any-name', {
    color: '#ff0000',
    icon: 'default-basic-shape-triangle',
    entity: 'my_entity',
})
```

---

## Handling media

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/handling-media.html

# Handling media [​](#handling-media)

## Overview [​](#overview)

The Shopware 6 Administration provides many components to work with, when it comes to handle media. For example, imagine you want to provide an opportunity to upload files. This guide will show you how to use the most important of them.

## The media upload component [​](#the-media-upload-component)

The Shopware 6 Administration media upload component makes it relatively easy to upload media of various kinds such as images, videos and audio files. This is done through the `sw-media-upload-v2` component as seen below:

html

```shiki
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        :autoUpload="true"
        label="My image-upload">
    </sw-media-upload-v2>
</div>
```

As you can see in the code sample below, the `sw-media-upload-v2` is pretty configurable through properties. To get an overview of all the options, here is a list:

| Property | Function |
| --- | --- |
| `source` | The source that will be used for the internal `sw-media-preview-v2` if the component is not used in the `allowMultiSelect` mode |
| `variant` | This can be used to choose between the `regular` and the `compact` variants |
| `uploadTag` | This is used to coordinate with the `sw-upload-listener` component |
| `allowMultiSelect` | Sets whether multiple files can be uploaded at once |
| `label` | The text that is displayed in the header |
| `defaultFolder` | The path where the file will be put |
| `targetFolderId` | The `targetFolderId` that will be used as a backup to the `defaultFolder` |
| `helpText` | Sets the `helpText` displayed in the header of the component |
| `fileAccept` | Sets what the underlying `<input>`, accepts standard is `image/*` |
| `disabled` | Disables the whole component |

## Keeping track of uploads [​](#keeping-track-of-uploads)

As seen below, the `sw-upload-listener` component can be used in conjunction with an `sw-media-upload-v2` component.

html

```shiki
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        label="My image-upload">
    </sw-media-upload-v2>
    <sw-upload-listener
        @media-upload-finish="onUploadFinish" 
        uploadTag="my-upload-tag">
    </sw-upload-listener>
</div>
```

Notice that the `uploadTag` needs to be the same in the `sw-media-upload-v2` and the `sw-upload-listener` for them to communicate properly. Beyond the `media-upload-finish` event there are a few more events:

| Event | Description |
| --- | --- |
| `media-upload-add` | This event is triggered when an upload is added |
| `media-upload-finish` | This event is triggered when an upload finishes |
| `media-upload-fail` | This event is triggered on an upload failing |
| `media-upload-cancel` | This event is triggered when an upload is canceled |

## Previewing Media [​](#previewing-media)

Media can be previewed with the `sw-media-preview-v2` component as seen below:

html

```shiki
<sw-media-preview-v2
    :source="some-id">
</sw-media-preview-v2>
```

As previously mentioned this component is already embedded within the `sw-media-upload-v2`. However, using it as a separate component you get access to the following configuration options:

| Property | Function |
| --- | --- |
| `source` | The `id` or alternately the path to the media to be previewed |
| `showControls` | Controls whether media such as videos or audio shows controls |
| `autoplay` | Controls whether media such as videos or audio auto-plays |
| `hideTooltip` | Hides the the filename tooltip of the media in at the bottom of the component |
| `mediaIsPrivate` | If set to true displays various lock symbols |

---

## Using Vuex Stores

**Source:** https://developer.shopware.com/docs/guides/plugins/plugins/administration/data-handling-processing/using-vuex-state.html

# Using Vuex Stores [​](#using-vuex-stores)

## Overview [​](#overview)

The Shopware 6 Administration uses [Vuex](https://vuex.vuejs.org/) stores to keep track of complex state, while just adding a wrapper around it. Learn what Vuex is, how to use it and when to use it from their great [documentation](https://vuex.vuejs.org/). This guide will show you how to use Vuex as you normally would, through the interfaces provided by the Shopware 6 Administration.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module. Of course, you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) the framework used in the Administration, and it's flux library [Vuex](https://vuex.vuejs.org/).

## Creating a store [​](#creating-a-store)

Creating a store works the same way as it would in standard Vuex with the only limitation being, that all stores have to be `namespaced` in order to prevent collisions with other third party plugins or the Shopware 6 Administration itself.

The following code snippet is the `namespaced` store we will register later through Shopware to the underlying Vuex. It is admittedly rather short and has only one variable called `content` and a setter for it, but again this all the same as in Vuex. Beware of the property `namespaced`, though.

PLUGIN\_ROOT/src/Resources/app/administration/app/src/component/store-example/store.js

javascript

```shiki
export default {
    namespaced: true,

    state() {
        return {
            // the state we want to keep track of
            content: ''
        };
    },

    mutations: {
        // a mutation to change the state
        setContent(state, content) {
            state.content = content;
        },
    }
};
```

## Registering the store [​](#registering-the-store)

The store can be registered in two scopes, on a module scope and on a per component scope. Both ways use the same functions from the [Shopware object](./the-shopware-object.html) to register and unregister the `namespaced store modules`.

Registering in a module scope is done by simply calling the function `Shopware.State.registerModule` in the `main.js` file.

ADMINISTRATION\_ROOT/src/main.js

javascript

```shiki
import swagBasicState from './store';

Shopware.State.registerModule('swagBasicState', swagBasicState);
```

In the component scope `Namespaced` store modules can be registered in the `beforeCreate` [Vue lifecycle hook](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram), with the previously mentioned `Shopware.State.registerModule` function. But then they also need to be `unregistered` in the `beforeDestroy` Vue lifecycle hook, in order to not leave unused stores behind after a component has been destroyed.

All of this can be seen in the following code sample:

PLUGIN\_ROOT/src/Resources/app/administration/app/src/component/store-example/index.js

javascript

```shiki
    beforeCreate() {
        // registering the store to vuex through the Shopware objects helper function
        // the first argument is the name the second the imported namespaced store
        Shopware.State.registerModule('swagBasicState', swagBasicState);
    },

    beforeDestroy() {
        // unregister the store before the component is destroyed
        Shopware.State.unregisterModule('swagBasicState');
    },
```

Both methods make the store on the given name everywhere available, regardless of where it has been registered.

## Using the store in a component [​](#using-the-store-in-a-component)

The Shopware object also makes the native Vuex helper functions available, like [`mapState`](https://vuex.vuejs.org/guide/state.html#the-mapstate-helper), [`mapGetters`](https://vuex.vuejs.org/guide/getters.html#the-mapgetters-helper), [`mapMutations`](https://vuex.vuejs.org/guide/mutations.html#committing-mutations-in-components) and [`mapActions`](https://vuex.vuejs.org/guide/actions.html#dispatching-actions-in-components). The `namespaced` store itself can be accessed through the `Shopware.State.get()` function.

PLUGIN\_ROOT/src/Resources/app/administration/app/src/component/store-example/index.js

javascript

```shiki
// import the template
import template from './store-example.html.twig';

const { Component } = Shopware;

// Access the normal Vuex helper functions through the Shopware Object
const { 
    mapState,
    mapMutations,
} = Shopware.Component.getComponentHelper();

Component.register('swag-basic-state', {
    template,

    computed: {
        // the native mapState vuex helper function 
        ...mapState('swagBasicState', [
            'content',
        ])
    },

    methods: {
        // the native mapMutations vuex helper function
        ...mapMutations('swagBasicState', [
            'setContent',
        ]),
    }
});
```

## Adding a template [​](#adding-a-template)

After we have registered our `namespaced` store, mapped state and mutations, we can now use them in our components or templates. The component below displays the previously mapped state `content` in a `div` and a `sw-text-field`, mutating the state on the `changed` event of the `sw-text-field`.

PLUGIN\_ROOT/src/Resources/app/administration/app/src/component/store-example/store-example.html.twig

html

```shiki
<div>
    <h1>SW-6 State</h1>
    <sw-text-field
            :value="content"
            @update:value="value => setContent(value)">
    </sw-text-field>
    <div>
        {{ content }}
    </div>
</div>
```

## More interesting topics [​](#more-interesting-topics)

* [The Shopware object](./the-shopware-object.html)

---

