# Products Extensions B2B Components

*Scraped from Shopware Developer Documentation*

---

## B2B Components

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/

# Introduction [​](#introduction)

The B2B components enable you to enhance your shop with essential B2B functionalities. Below are the available components.

In the world of digital B2B commerce, where businesses engage with other companies, we emphasize this vital distinction through these specific features :

* **Employee Management** enables B2B Merchants to create a buyer platform for their business partners.
* **Quote Managements** covers Sales Representative related jobs around negotiating quotes with customers.
* **Order Approval** allows for a more controlled buying process by introducing an approval workflow.
* **Quick Order and Shopping List** takes care of distinctive B2B buying behaviors.
* **Organization Unit** allows for the configuration of more differentiated and specific access rights to meet the needs of businesses with complex structures.
* **Digital Sales Composables** aims to provide a set of composable frontends to cover more complex Sales Representative jobs.

## Configuring custom toggles for B2B components [​](#configuring-custom-toggles-for-b2b-components)

The B2B components allow merchants to selectively choose and configure B2B features according to their needs. They offer merchants the ability to craft a tailored B2B ecommerce experience for their business partners while also allowing agencies to fine-tune Shopware to meet specific requirements. This means that B2B components can be individually activated or deactivated for each business partner within the shop.

The following articles will guide you how to do this by creating custom toggles via a plugin for B2B Components (Customer-specific features).

The **Customer-specific features** section on the Customer detail page allows the shop merchant to turn these B2B features on or off for a specific customer.

![Feature Toggles](/assets/b2b-feature-toggles.Cdi_s3o9.png)

To achieve this, you need to address the following cases where functionality may be hidden:

1. If a merchant has not activated a feature for a particular customer, it should be hidden.
2. If the B2B admin has not granted an employee access to a specific feature, it should not be visible.

Considering these scenarios, we can ensure that the appropriate B2B features are displayed and accessible based on feature toggles and admin-granted permissions.

### Prerequisite [​](#prerequisite)

To improve organization and maintain a clear structure, it is advisable to relocate all B2B Components into the `B2B` folder within the Commercial plugin. By doing so, you can centralize the B2B-related functionality, making it easier to locate, manage, and maintain the codebase. This folder structure promotes better separation of concerns and enhances the overall modularity of the application.

text

```shiki
├── src
│   ├── B2B
│   │   ├── QuickOrder
│   │   ├── AnotherB2BComponent
│   │   │   CommercialB2BBundle.php
...
```

To ensure consistency and clarity, it is recommended to make your B2B Component extend `CommercialB2BBundle` instead of `CommercialBundle` and add the `type` as **B2B** attribute inside the `describeFeatures()` method of each B2B Component. This attribute will help identify and categorize the features specifically related to B2B functionality.

By including `type => 'B2B'` in the `describeFeatures()` method, you can distinguish B2B features from other types of features within your application. This will facilitate easier maintenance, organization, and identification of B2B-related functionalities, ensuring a streamlined development process.

For example, consider the following code snippet:

php

```shiki
namespace Shopware\Commercial\B2B\YourB2BComponent;

class YourB2BComponent extends CommercialB2BBundle
{
    public function describeFeatures(): array
    {
        return [
            [
                ...,
                'type' => self::TYPE_B2B,
            ],
        ];
    }
}
```

## Using feature toggle in Route/API/Controller [​](#using-feature-toggle-in-route-api-controller)

To determine if a customer is allowed to access a specific B2B feature, we will utilize the `isAllowed()` method from the `Shopware\Commercial\B2B\QuickOrder\Domain\CustomerSpecificFeature\CustomerSpecificFeatureService` service. This method accepts two parameters: the customer ID and the technical code of the B2B component.

We will place this check before every route, controller or API as follows:

php

```shiki
use Shopware\Commercial\B2B\QuickOrder\Domain\CustomerSpecificFeature\CustomerSpecificFeatureService;
 
class ApiController
{
    public function __construct(private readonly CustomerSpecificFeatureService $customerSpecificFeatureService)
    {
    }

    #[Route(
        path: '/your/path',
        name: 'path.name',
        defaults: ['_noStore' => false, '_loginRequired' => true],
        methods: ['GET'],
    )]
    public function view(Request $request, SalesChannelContext $salesChannelContext): Response
    {
        if (!$this->customerB2BFeatureService->isAllowed($salesChannelContext->getCustomerId(), 'QUICK_ORDER')) {
            throw CustomerSpecificFeatureException::notAllowed('QUICK_ORDER');
        }

        ...
    }
```

## Using feature toggle in Twig - Storefront [​](#using-feature-toggle-in-twig-storefront)

You can use a new Twig extension called `customerHasFeature()` to implement the functionality of retrieving customer-specific features in Twig templates. This method accepts only one parameter. The parameter is the technical code of the B2B component.

Here is an example implementation:

php

```shiki
namespace Shopware\Commercial\B2B\QuickOrder\Storefront\Framework\Twig\Extension;

class CustomerSpecificFeatureTwigExtension extends AbstractExtension
{
    public function getFunctions(): array
    {
        return [
            new TwigFunction('customerHasFeature', $this->isAllowed(...), ['needs_context' => true]),
        ];
    }

    public function isAllowed(array $twigContext, string $feature): bool
    {
        $customerId = null;
        if (\array_key_exists('context', $twigContext) && $twigContext['context'] instanceof SalesChannelContext) {
            $customerId = $twigContext['context']->getCustomerId();
        }
        
        if (!$customerId) {
            return false;
        }
        
        return $this->customerSpecificFeatureService->isAllowed($customerId, $feature);
    }
}
```

Use it to check if a specific feature is allowed for a given customer in Twig.

html

```shiki
{% if customerHasFeature('QUICK_ORDER') %}
    ...
{% endif %}
```

---

## Employee Management

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/

# Employee Management [​](#employee-management)

A feature of the B2B Components includes employee, role, and permission management. It is implemented into both Storefront and Administration and supports their respective APIs.

## Basic idea [​](#basic-idea)

Employee management, as one of the B2B Components, is a feature that allows you to manage employees and their permissions as an extension to Shopware's account and customer management, but set into a company context. This means that employees are associated with a **company customer** and will act on behalf of that company, e.g., placing orders. Accordingly, employees can make use of addresses that have been defined by administrators of their company.

The **company customer** has the benefit of injecting company managed data into core processes without having to develop new employee processes from scratch or maintain multiple versions of these processes.

## Company customer [​](#company-customer)

The company customer is a regular storefront customer but with a few additional properties. A customer's ID is used to associate employees with a company. Therefore, it is really easy to rely on Shopware's typical order relevant data like addresses. This allows us to keep using most core implementations, while only extending a few B2B related features, e.g., to reference an employee's actions.

## Role management [​](#role-management)

Employees are assigned roles that define their permissions and settings. These permissions can restrict or allow employees to perform certain actions, like ordering without approval or managing roles and employees. Refer to our guides section how permissions can be extended [via app](./../employee-management/guides/creating-own-permissions-via-app.html) or [via plugin](./../employee-management/guides/creating-own-permissions-via-plugin.html).

---

## Concepts

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/concepts/

# Concepts [​](#concepts)

This section includes the concepts related to Employee Management.

## Additional info [​](#additional-info)

It's important to keep in mind that employees are uniquely identified via their email address. When a new employee gets invited, a check will be performed to ensure that the email address is in use only once.

---

## Entities & Schema

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/concepts/entities-and-schema.html

# Entities and schema [​](#entities-and-schema)

## Entities [​](#entities)

### Business Partner [​](#business-partner)

The business partner entity contains additional B2B company data and therefore extends the basic storefront customer. Business partners are used to pool employees, roles and global settings.

### Employee [​](#employee)

The employee entity represents a separate login within the context of the same business partner. This is to say that, employees operate on behalf of the linked business partner, facilitating actions like order placement. Additionally, these employees can be assigned specific roles.

### Role [​](#role)

The role entity represents a set of permissions that can be assigned to an employee. Permissions can restrict or allow employees to perform certain actions in the shop, like ordering or managing roles as well as employees.

## Schema [​](#schema)

---

## Guides

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/

# Guides [​](#guides)

The following articles gives you an idea of roles. Also it guides you on creating your own permissions via app or plugin for the B2B Employee Management component.

## B2B permissions [​](#b2b-permissions)

Use permissions to restrict access to certain information or functionalities within the B2B Components. For example, the B2B supervisor can restrict which employee can manage the company's employee accounts.

### Groups [​](#groups)

Permissions are divided into individual groups that have a logical relationship to each other.

### Dependencies [​](#dependencies)

A permission can be dependent on another permission, without which this permission cannot be used. For example, if a role is created with the permission to edit employee accounts, this role must also have the permission to view employee accounts. This is because the `employee.edit` permission depends on the `employee.read` permission.

### Shopware base permissions [​](#shopware-base-permissions)

The following permissions are already included and used in the B2B Employee Management component. More "base" permissions will be duly added with future B2B Components.

| Group | Permission | Dependencies |
| --- | --- | --- |
| employee | employee.read |  |
| employee | employee.edit | employee.read |
| employee | employee.create | employee.read, employee.edit |
| employee | employee.delete | employee.read, employee.edit |
| order | order.read.all |  |

---

## API Route Restriction for Employees

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/api-route-restriction-for-employees.html

# API Route Restriction for Employees [​](#api-route-restriction-for-employees)

## Overview [​](#overview)

B2B employees and business partners share the same customer account. This can lead to inconsistency for all users of the shared account because they are allowed to change settings and data (both via Storefront and Store API), which are not related to the B2B permission system. Hence, it is decided to restrict most of the customer account routes by implementing a denylist pattern to prevent the illegal modification of customer data and settings, instead of replicating all customer features for employee accounts. All non-account related routes are still available for B2B employees.

## Denylist [​](#denylist)

The denylist can be found in the employee management config at: `Resources\config\employee_route_access.xml`. All denied routes are inside `<denied>` tags. The routes inside the `<allowed>` tags are not important for third-party developers because they are used for internal integration tests to remind developers to extend the list if new Store API account routes are added.

### Denylist Example [​](#denylist-example)

xml

```shiki
<?xml version="1.0" encoding="utf-8"?>
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../Schema/Xml/employee-route-access-1.0.xsd">
    <denied>store-api.account.change-profile</denied>
    <denied>store-api.account.change-email</denied>
    <denied>...</denied>

    <allowed>store-api.account.login</allowed>
    <allowed>store-api.account.logout</allowed>
    <allowed>...</allowed>
</routes>
```

### How to load the Denylist [​](#how-to-load-the-denylist)

The denylist is loaded by using the `load` function in the `Shopware\Commercial\B2b\Domain\RouteAccess\EmployeeRouteAccessLoader` class. The return result is an associative array that includes arrays of all `allowed` and `denied` routes.

### Where is the Denylist loaded [​](#where-is-the-denylist-loaded)

The denylist is loaded in the `Shopware\Commercial\B2b\Subscriber\B2bRouteBlocker`, which listens to each controller event and validates the route access before the request reaches the controller. Illegal attempts cause an exception to be thrown.

### How to override the Denylist [​](#how-to-override-the-denylist)

It is possible to create additional `employee_route_access.xml` configs, which include new denied routes. After the config is ready, you can decorate the `Shopware\Commercial\B2b\Domain\RouteAccess\EmployeeRouteAccessLoader`, which supports recommended Shopware decoration pattern. Adapt the solution of the decorated `EmployeeRouteAccessLoader::load` function and return your own config.

#### Decoration Example [​](#decoration-example)

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Commercial\B2B\Domain\RouteAccess;

class DecoratedEmployeeRouteAccessLoader extends AbstractEmployeeRouteAccessLoader
{
    private const CONFIG = __DIR__ . '/../../Resources/config/new-custom-employee_route_access.xml';

    public function __construct(
        private readonly AbstractEmployeeRouteAccessLoader $decorated
    ) {
    }

    public function getDecorated(): AbstractEmployeeRouteAccessLoader
    {
        return $this->decorated;
    }

    public function load(): array
    {
        $oldConfig = $this->decorated->load();
        $customConfig = (array) @simplexml_load_file(self::CONFIG);

        // This example merges the old config with the new created custom config.
        // Return the $customConfig variable to override the old completely

        return array_merge_recursive($oldConfig, $customConfig);
    }
}
```

---

## Employee Invitation

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/b2b-employee-invitation.html

# Employee Invitation [​](#employee-invitation)

Employees can be created via Storefront, Store-api, and Administration.

* Storefront - Business partners can invite employees by logging-in to Storefront and navigating to the `employee` page. From there, they can add a new employee.
* Store API - One can utilize the `/store-api/employee/create` endpoint while logged in as a customer to invite employees.
* Administration - Merchants can invite employees by logging in to the administration interface. Selects the business partner customer, navigates to the `company` tab, and adds a new employee account in edit mode.

The invited employee receives an invitation mail that must be confirmed to set a password.

## The URL for the invitation acceptance [​](#the-url-for-the-invitation-acceptance)

Upon invitation, the employee will receive an email requiring confirmation to set a password. This process will also activate the employee for the business partners company. The default URL for the acceptance is `/account/business-partner/employee/invite/%%RECOVERHASH%%`, the recovery hash is used as a unique identifier and is only valid for the invitation of one employee.

### How to override the Invitation URL [​](#how-to-override-the-invitation-url)

The default URL can be replaced with a custom URL. This is helpful if you want to provide a custom endpoint. To override it, you need to insert the URL as a string into the key-value system config with the key `b2b.employee.invitationURL`.

You can find more information about the system config here: [System Config](./../../../../../guides/plugins/apps/configuration.html).

---

## B2B Roles

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/b2b-roles.html

# B2B Roles [​](#b2b-roles)

Roles can be used to bind multiple permission to employees with contexts. Every employee can have one assigned role. Based on that role and the containing permission, the employee will get access to certain information and functionalities.

The business partner has the opportunity to create a **default** role that will be selected by default, when creating a new employee.

---

## Create permissions via App

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/creating-own-permissions-via-app.html

# Create Permissions via App [​](#create-permissions-via-app)

The App needs to use the API to extend and create permissions. Therefore, the apps can send a request to the Store API and pass the required parameters to the `/store-api/permission` route.

After doing that, the already existing permissions created by Shopware or added by plugin, will be merged with the permission created by apps.

It is important to note that permissions have a unique name. So a permission named `employee.read` can neither be added by apps nor by plugins, because this name is already in use. So a new name can better be added by making use of snippets.

## Snippets [​](#snippets)

The Snippet for the new permissions has to be added to the following namespace: `b2b.role-edit.permissions.[name]`. The placeholder has to be replaced by the name of the new permission, e.g., `b2b.role-edit.permissions.order.delete`.

---

## Create permissions via plugin

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/creating-own-permissions-via-plugin.html

# Creating own permissions via plugin [​](#creating-own-permissions-via-plugin)

This article explains how to create custom permissions using a plugin.

To create custom permissions, you will utilize the event subscriber concept in Symfony. Create a new class called `PermissionCollectorSubscriber` that implements the `EventSubscriberInterface`:

php

```shiki
<?php declare(strict_types=1);

use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class PermissionCollectorSubscriber implements EventSubscriberInterface
{
    public const OWN_ENTITY_GROUP = 'own_entity';

    // Here you define your custom permissions as constants
    public const OWN_ENTITY_READ = 'own_entity.read';
    
    public const OWN_ENTITY_EDIT = 'own_entity.edit';
    
    public const OWN_ENTITY_CREATE = 'own_entity.create';
    
    public const OWN_ENTITY_DELETE = 'own_entity.delete';

    public static function getSubscribedEvents(): array
    {
        return [
            PermissionCollectorEvent::NAME => [ 'onAddOwnPermissions' , 1000 ]
        ];
    }

    // This method is called when the PermissionCollectorEvent is triggered
    public function onAddOwnPermissions(PermissionCollectorEvent $event): void
    {
        $collection = $event->getCollection();

        // Here you add your custom permissions to the permission collection
        $collection->addPermission(self::EMPLOYEE_READ, self::OWN_ENTITY_GROUP, []);
        $collection->addPermission(self::EMPLOYEE_EDIT, self::OWN_ENTITY_GROUP, [ self::EMPLOYEE_READ ]);
        $collection->addPermission(self::EMPLOYEE_CREATE, self::OWN_ENTITY_GROUP, [ self::EMPLOYEE_READ, self::EMPLOYEE_EDIT ]);
        $collection->addPermission(self::EMPLOYEE_DELETE, self::OWN_ENTITY_GROUP, [ self::EMPLOYEE_READ, self::EMPLOYEE_EDIT ]);
    }
}
```

The `PermissionCollector` collects the permissions of all subscribers and then passes them to the storefront, where they can be attached to the role by the user. If you want to check in the template if the user has this permission, the Twig function `isB2bAllowed` can be used:

twig

```shiki
{% sw_extends '@Storefront/storefront/page/checkout/checkout-item.html.twig' %}

{{ parent() }}

{% if isB2bAllowed(constant('PermissionCollectorSubscriber::EMPLOYEE_READ')) %}
...
{% endif  %}
```

In controllers, the checking of permissions must happen via the employee's role:

php

```shiki
<?php declare(strict_types=1);
public function employeeList(Request $request, SalesChannelContext $context): Response
{
    if (!$context->getCustomer()->getEmployee()->getRole()->can(PermissionCollectorSubscriber::EMPLOYEE_READ)) {
        throw new PermissionDeniedException();
    }
...
}
```

---

## Subscription Integration

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/employee-management/guides/subscription-integration.html

# B2B Employee Integration for Subscriptions [​](#b2b-employee-integration-for-subscriptions)

This guide describes how B2B Employees are integrated with the Subscription module, enabling employee-based subscription management and tracking within a B2B context.

## Overview [​](#overview)

The B2B Employee Integration for Subscriptions extends subscription functionality to support B2B employee workflows without modifying the core Subscription module. All B2B-specific logic is contained within the B2B Employee Management module using decorators, extensions, and event subscribers.

This integration enables:

* **Permission-based subscription access** - Control which subscriptions employees can view
* **Employee tracking** - Track which employee created each subscription
* **Organization context preservation** - Maintain organization data throughout the subscription lifecycle

## Prerequisites [​](#prerequisites)

* Shopware 6.7 with Subscriptions extension
* B2B Components with Employee Management module
* Understanding of [Subscription concepts](./../../../../extensions/subscriptions/concept.html)
* Understanding of [B2B Employee Management concepts](./../concepts/)

## Key Features [​](#key-features)

### Employee-Based Subscription Permissions [​](#employee-based-subscription-permissions)

Employees can view subscriptions based on their assigned permissions:

| Permission | Access Level |
| --- | --- |
| `subscription.read.all` | View all subscriptions in the system |
| `organization_unit.subscription.read` | View subscriptions from assigned organization unit + own subscriptions |
| (no permission) | View only own subscriptions |

These permissions are checked when employees access subscription lists, ensuring data isolation and security in B2B contexts.

### Employee Tracking [​](#employee-tracking)

Subscriptions track which employee created them through the `b2b_components_subscription_employee` association table. This enables:

* **Permission-based filtering** - Filter subscriptions by employee and organization
* **Employee context in orders** - Both initial and renewal orders maintain employee context
* **Audit trails** - Track which employee initiated each subscription

### Organization Context [​](#organization-context)

Organization data is preserved throughout the subscription lifecycle:

* **Initial orders** - Organization data is added when a subscription is created during checkout
* **Renewal orders** - Organization data is maintained in later automated orders
* **Context preservation** - Organization information flows through all subscription-related processes

## Architecture [​](#architecture)

### Core Components [​](#core-components)

The integration is built using several key components in the B2B Employee Management module:

**Decorators:**

* `SubscriptionRouteDecorator` - Decorates `SubscriptionRoute` to apply permission-based filtering
* `SalesChannelContextServiceDecorator` - Adds employee context to subscription sales channel contexts

**Event Subscribers:**

* `SubscriptionTransformedSubscriber` - Adds employee and organization data during subscription creation
* `SubscriptionCartConvertedSubscriber` - Adds employee and organization data to initial orders
* `SubscriptionOrderPlacedSubscriber` - Maintains employee context in renewal orders

**Entity Extension:**

* `SubscriptionExtension` - Extends `SubscriptionDefinition` with `subscriptionEmployee` association
* `SubscriptionEmployeeDefinition` - Defines the subscription-employee relationship

**Filter Service:**

* `SubscriptionEmployeeFilter` - Implements permission-based subscription filtering logic

### Integration Patterns [​](#integration-patterns)

The integration follows Shopware best practices:

**1. Decorator Pattern**

Instead of modifying core Subscription code, the integration uses decorators to extend functionality:

php

```shiki
// SubscriptionRouteDecorator wraps the core SubscriptionRoute
$this->decorated->load($request, $context, $criteria);
// Then applies employee-based filtering
$this->subscriptionEmployeeFilter->applyEmployeeFilter($criteria, $employee);
```

**2. Event-Based Integration**

Key subscription events are used to inject employee data:

* `SubscriptionTransformedEvent` - Fired when subscription is created from cart
* `SUBSCRIPTION_CART_CONVERTED` - Fired when subscription cart is converted to order
* `CheckoutOrderPlacedEvent` - Fired when renewal order is placed

**3. Entity Extension Pattern**

The `SubscriptionExtension` adds the employee association to subscriptions without modifying the core entity:

php

```shiki
new OneToOneAssociationField(
    'subscriptionEmployee',
    'id',
    'subscription_id',
    SubscriptionEmployeeDefinition::class,
    false
);
```

## Database Schema [​](#database-schema)

### b2b\_components\_subscription\_employee Table [​](#b2b-components-subscription-employee-table)

This table links subscriptions to the employees who created them:

| Column | Type | Description |
| --- | --- | --- |
| `id` | BINARY(16) | Primary key |
| `subscription_id` | BINARY(16) | Foreign key to `subscription` (UNIQUE) |
| `employee_id` | BINARY(16) | Foreign key to `b2b_employee` |
| `created_at` | DATETIME(3) | Creation timestamp |
| `updated_at` | DATETIME(3) | Update timestamp |

**Key characteristics:**

* One-to-one relationship between subscription and subscription\_employee
* `subscription_id` has a UNIQUE constraint ensuring one employee per subscription
* Foreign keys maintain referential integrity

## Technical Flows [​](#technical-flows)

### Initial Subscription Order Flow [​](#initial-subscription-order-flow)

When an employee checks out with a subscription product, the following flow occurs:

**Key Points:**

1. `SubscriptionTransformedSubscriber` adds employee and organization data to the subscription being created
2. `SubscriptionCartConvertedSubscriber` ensures the initial order contains employee and organization data
3. The subscription's `convertedOrder` field stores this data for future renewal orders

### Permission-Based Subscription Filtering [​](#permission-based-subscription-filtering)

When an employee views their subscriptions, filtering is applied based on permissions:

**Permission Logic:**

* **No filter** (`subscription.read.all`) - Employee sees all subscriptions
* **OR filter** (`organization_unit.subscription.read`) - Employee sees their own subscriptions or subscriptions from their organization unit
* **Default filter** - Employee sees only subscriptions they created

## Developer Integration Points [​](#developer-integration-points)

### Accessing Employee Data from Subscriptions [​](#accessing-employee-data-from-subscriptions)

To access the employee who created a subscription:

php

```shiki
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

// Add association when loading subscriptions
$criteria = new Criteria();
$criteria->addAssociation('subscriptionEmployee.employee');

$subscription = $subscriptionRepository->search($criteria, $context)->first();

if ($subscription->getSubscriptionEmployee()) {
    $employee = $subscription->getSubscriptionEmployee()->getEmployee();
    // Access employee data
}
```

### Accessing Employee Data from Orders [​](#accessing-employee-data-from-orders)

Employee data is stored in order extensions:

php

```shiki
// For initial or renewal orders
$order = $orderRepository->search($criteria, $context)->first();

// Check if the order has employee context
$orderEmployee = $order->getExtension('orderEmployee');
if ($orderEmployee) {
    $employeeId = $orderEmployee->getEmployeeId();
}

// Check if the order has organization context
$organization = $order->getExtension('organization');
if ($organization) {
    $organizationId = $organization->getId();
}
```

### Event Subscribers [​](#event-subscribers)

The integration provides several event subscribers you can use as reference:

**SubscriptionTransformedSubscriber** - Priority: 0

Listens to: `SubscriptionTransformedEvent`

Use case: Add custom data when a subscription is created from a cart

**SubscriptionCartConvertedSubscriber** - Priority: 0

Listens to: `SUBSCRIPTION_CART_CONVERTED` event

Use case: Modify the initial order data during subscription checkout

**SubscriptionOrderPlacedSubscriber** - Priority: 0

Listens to: `CheckoutOrderPlacedCriteriaEvent` and `CheckoutOrderPlacedEvent`

Use case: Add employee context to renewal orders

### Adding Custom Logic [​](#adding-custom-logic)

To add custom B2B logic to subscriptions:

1. **Create a decorator** for subscription services (follow `SubscriptionRouteDecorator` pattern)
2. **Subscribe to subscription events** to inject your data
3. **Use entity extensions** to add custom associations without modifying core entities
4. **Check context state** instead of relying on event priorities for more robust integration

Example decorator pattern:

php

```shiki
use Shopware\Core\System\SalesChannel\SalesChannelContext;

class CustomSubscriptionServiceDecorator extends AbstractSubscriptionService
{
    public function __construct(
        private readonly AbstractSubscriptionService $decorated,
        private readonly CustomLogicService $customService
    ) {}

    public function getDecorated(): AbstractService
    {
        return $this->decorated;
    }

    public function someMethod(SalesChannelContext $context): void
    {
        // Your custom logic before
        $this->customService->doSomething($context);

        // Call decorated service
        $this->decorated->someMethod($context);

        // Your custom logic after
    }
}
```

## Related Documentation [​](#related-documentation)

* [Subscription Concept](./../../../../extensions/subscriptions/concept.html) - Core subscription concepts
* [Mixed Checkout](./../../../../extensions/subscriptions/guides/mixed-checkout.html) - Mixed cart checkout flow
* [Separate Checkout](./../../../../extensions/subscriptions/guides/separate-checkout.html) - Separate subscription checkout
* [B2B Employee Management Concepts](./../concepts/) - Employee and role concepts
* [Creating Permissions via Plugin](./creating-own-permissions-via-plugin.html) - How to extend permissions
* [API Route Restriction](./api-route-restriction-for-employees.html) - Route-level permission control

## Summary [​](#summary)

The B2B Employee Integration for Subscriptions provides a clean, maintainable way to add employee context to subscriptions without modifying core code. By using decorators, event subscribers, and entity extensions, the integration:

* Maintains separation of concerns between modules
* Follows Shopware architectural patterns
* Enables permission-based subscription access
* Preserves employee and organization context throughout the subscription lifecycle
* Provides clear extension points for custom logic

---

## Quotes Management

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/quotes-management/

# Quotes Management [​](#quotes-management)

The Quote Management feature streamlines the B2B partnership process by enabling partners to seamlessly request and accept quotes without the need for time-consuming manual negotiations. The process begins with B2B partners populating their cart with desired products, after which they can initiate a quote request based on the contents of their cart. Once the request is submitted, B2B merchants have the ability to review the quote within the administration system. They can also apply discounts to individual product items within the quote to tailor the offer to the partner's needs. Subsequently, the modified quote is sent to the B2B partners for their consideration.

Partners are free to accept or decline the offer, and upon acceptance, they are guided through the seamless checkout process. The system then automatically generates an order based on the accepted quote, optimizing efficiency and ensuring a smooth transition from negotiation to transaction. This feature revolutionizes B2B interactions by reducing the need for extensive manual discussions and fostering a more efficient and collaborative environment for both partners and merchants.

---

## Entities & Schema

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/quotes-management/concepts/entities-and-schema.html

# Entities and schema [​](#entities-and-schema)

## Entities [​](#entities)

### Quote [​](#quote)

The quote entity stores fundamental information about each quote such as state, pricing, discount, associated users, customer and customers.

### Quote Delivery [​](#quote-delivery)

The quote delivery represents the delivery information of a quote. It includes details such as the shipping method, earliest and latest shipping date.

### Quote Delivery Position [​](#quote-delivery-position)

The quote delivery position represents the line items of a quote delivery. It has a quote line item, price, total price, unit price, quantity, and custom fields.

### Quote Line item [​](#quote-line-item)

The quote line item represents the line items of a quote. Only product type is supported currently.

### Quote Transaction [​](#quote-transaction)

The quote transaction entity captures payment amount and also allows saving an external reference.

### Quote Comment [​](#quote-comment)

The quote comment entity stores comments related to a quote.

### Quote Employee [​](#quote-employee)

The quote employee entity represents employees associated with a quote.

### Quote Document [​](#quote-document)

The quote document entity represents documents associated with a quote.

## Schema [​](#schema)

---

## Quotes conversion

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/quotes-management/guides/quotes-conversion.html

# Quotes conversion [​](#quotes-conversion)

Customers can convert their shopping carts into quotes to facilitate seamless processing. There are two new services to handle the conversion process :

## Cart to quote converter [​](#cart-to-quote-converter)

When a customer wants to request a quote for their shopping cart, the process involves converting a cart to an order and then proceeding to enrich the data for the quote. The method `convertToQuote` of class `Shopware\Commercial\B2B\QuoteManagement\Domain\CartToQuote\CartToQuoteConverter` is responsible for this process.

php

```shiki
use Shopware\Core\Checkout\Cart\Order\OrderConversionContext;
use Shopware\Core\Checkout\Cart\Cart;
use Shopware\Core\Checkout\Cart\Order\OrderConverter;

public function convertToQuote(Cart $cart, SalesChannelContext $context, OrderConversionContext $orderContext = null): Quote
    {
        $order = $this->orderConverter->convertToOrder($cart, $context, $orderContext);
        
        $quote = $order;
        
        //enrich quote data
        
        //enrich quote line-items
        
        return $quote;
    }
```

## Quote to cart converter [​](#quote-to-cart-converter)

When a customer wants to place an order based on a quote, a new cart is created based on the quote data. The method `convertToCart` of class `Shopware\Commercial\B2B\QuoteManagement\Domain\QuoteToCart\QuoteToCartConverter` is responsible for this process.

php

```shiki
use Shopware\Core\Checkout\Cart\Cart;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Commercial\B2B\QuoteManagement\Entity\Quote\QuoteEntity;
use Shopware\Commercial\B2B\QuoteManagement\Domain\Transformer\QuoteLineItemTransformer;

public function convertToCart(QuoteEntity $quote, SalesChannelContext $context): Cart
    {
        
        $cart = new Cart(Uuid::randomHex());
        $cart->setPrice($quote->getPrice());

        $lineItems = QuoteLineItemTransformer::transformToLineItems($quote->getLineItems());
        $cart->setLineItems($lineItems);
        
        //enrich the cart
        
        return $cart;
    }
```

---

## Shopping lists

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/shopping-lists/

# Shopping Lists [​](#shopping-lists)

The *Shopping lists* component is designed to help users easily manage their shopping needs. It allows users to create, edit, and organize their shopping lists efficiently. With features such as item categorization, quantity tracking, and the ability to mark items as purchased, the *Shopping lists* ensure that users can shop with ease and never forget essential items. Whether you are planning for a weekly grocery trip or a special event, the *Shopping lists* component provides a simple and intuitive solution to keep track of all your shopping requirements.

---

## Entities & Schema

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/shopping-lists/concepts/entities-and-schema.html

# Entities and schema [​](#entities-and-schema)

## Entities [​](#entities)

### Shopping Lists [​](#shopping-lists)

Shopping lists represent a list of products prepared for a customer or a sales channel. They show basic information about the product list, such as the name, customer, sales channel and so on.

### Line item [​](#line-item)

he Shopping List Line Item represents individual products within a shopping list. Each product in the shopping list is considered a line item.

## Schema [​](#schema)

---

## API & Pricing

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/shopping-lists/guides/api-and-pricing.html

## Store API [​](#store-api)

Here are some of the actions you can perform on *Shopping lists* with Store API.

### Create new shopping list [​](#create-new-shopping-list)

http

```shiki
POST {url}/store-api/shopping-list {
    name: {string}
}
```

### Duplicate shopping list [​](#duplicate-shopping-list)

http

```shiki
POST {url}/store-api/shopping-list/{id}/duplicate {
    name: {string}
}
```

### Get shopping list [​](#get-shopping-list)

http

```shiki
GET {url}/store-api/shopping-list/{id}
```

### Get shopping lists [​](#get-shopping-lists)

http

```shiki
GET {url}/store-api/shopping-lists
```

### Remove shopping lists [​](#remove-shopping-lists)

http

```shiki
DELETE {url}/store-api/shopping-lists {
    ids: {array}
    }
```

### Get summary price shopping list [​](#get-summary-price-shopping-list)

The shopping list price will be included in the API for getting the shopping list. However, if you want to directly get the shopping list summary price, you can use this API.

http

```shiki
GET {url}/store-api/shopping-list/{id}/summary
```

For more details, refer to [B2B Shopping Lists](https://shopware.stoplight.io/docs/store-api/c9849725606fd-create-new-shopping-list) from Store API docs.

## Admin API [​](#admin-api)

Shopping lists do not provide any special APIs. The Admin API offers CRUD operations for every entity within Shopware, and you can use it to work with shopping lists.

### Shopping lists price [​](#shopping-lists-price)

A shopping list shows a list of products. The prices of these products may change depending on the time, customers, and sales channels. Therefore, the price of each product and the total price of the shopping list will not be saved in the database but will be calculated when loading the shopping list.

The `Shopware\Commercial\B2B\ShoppingList\Subscriber\ShoppingListSubscriber` listens to any loading of a shopping list.

php

```shiki
class ShoppingListSubscriber implements EventSubscriberInterface
{
    ...
    public static function getSubscribedEvents(): array
    {
        return [
            self::SHOPPING_LIST_LOADED => 'adminLoadedForSpecificCustomer',
            self::SALES_CHANNEL_SHOPPING_LIST_LOADED => 'salesChannelLoaded',
            self::SALES_CHANNEL_SHOPPING_LIST_LINE_ITEM_LOADED => 'salesChannelLineItemLoaded',
        ];
    }
    ...
}
```

The `Shopware\Commercial\B2B\ShoppingList\Domain\Price\ShoppingListPriceCalculator::calculate` will process calculations for entities:

php

```shiki
class ShoppingListPriceCalculator extends AbstractShoppingListPriceCalculator
{
    ...
    public function calculate(iterable $shoppingLists, SalesChannelContext $context): void
    {
        $productIds = $this->getProductIds($shoppingLists);
        $products = $this->productRepository->search(new Criteria($productIds), $context)->getEntities();

        foreach ($shoppingLists as $entity) {
            $listPrices = new PriceCollection();

            if (!$entity->getLineItems() instanceof ShoppingListLineItemCollection) {
                $entity->setPrice($this->calculatedPrices($listPrices, $context));
                continue;
            }

            $this->processCalculatedLineItems($entity->getLineItems(), $products, $context);

            foreach ($entity->getLineItems() as $lineItem) {
                if (!$lineItem->getPrice()) {
                    continue;
                }

                $listPrices->add($lineItem->getPrice());
            }

            $entity->assign([
                'price' => $this->calculatedPrices($listPrices, $context),
            ]);
        }
    }
    ...
}
```

For loading a shopping list in the admin, to include the price of the shopping list and the price of the products, it is necessary to ensure that all shopping lists have the same customer. If not, the price will not be calculated.

Also, products can also be activated or deactivated at any time. The shopping lists will still store deactivated products, but they will not be included in the calculations when loading the shopping lists.

---

## Order Approval

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/order-approval/

# Order approval component [​](#order-approval-component)

Order approval component is a part of the B2B Employee Management. It allows you to define rules that determine which orders require approval and which employees can approve them. It also allows you to view all pending orders and approve or decline them.

## Requirements [​](#requirements)

* You need to have Employee Management component installed and activated (see [Employee Management](./../employee-management/)).

---

## Entities and workflow

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/order-approval/concepts/01-entities-and-workflow.html

# Entities and workflow [​](#entities-and-workflow)

## Entities [​](#entities)

### Approval Rule [​](#approval-rule)

The approval rule entity represents a set of conditions that need to be met for an order to be approved. These conditions might be based on the order's total value, the order's currency or orders placed by employees with a specific role. Each approval rule can be assigned to a reviewer with specific role, which means that only employees that only employees possessing that role are authorized to approve orders meeting the rule's conditions. Additionally, it can be assigned to a particular role, requiring employees with that role to seek approval for orders meeting the rule's criteria. The rule also includes a priority, dictating the sequence in which the rules are evaluated.

### Pending Order [​](#pending-order)

The pending order entity represents an order that has been placed by an employee that requires approval. It contains the order's data, the employee that placed the order and the approval rule that matched the order.

## Workflow [​](#workflow)

The following diagram shows the workflow of the order approval component:

## Who can request approval? [​](#who-can-request-approval)

* Employees holding the role designated as the "Effective role" in the approval rule corresponding to the order are authorized to request approval.

## Who can view pending orders? [​](#who-can-view-pending-orders)

* Employees with the "Can view all pending orders" permission can view all pending orders.
* Employees who requested approval for the order can view their pending orders.
* Business Partners can view all pending orders of their employees.

## Who can approve or decline pending orders? [​](#who-can-approve-or-decline-pending-orders)

* Employees with the "Can approve/decline all pending orders" permission can approve or decline all pending orders.
* Employees with the "Can approve/decline pending orders" permission can approve or decline pending orders that assigned to them.
* Business Partners can approve or decline all pending orders of their employees.

---

## Order approval permissions

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/order-approval/guides/02-order-approval-permissions.html

# Order approval permissions [​](#order-approval-permissions)

Below, you can find a list of all the order approval rules that are available in the order approval component. You can utilize these rules for assigning roles to your employees.

## Approval rule permissions [​](#approval-rule-permissions)

| Permission | Description |
| --- | --- |
| `Can create approval rules` | Allows the employee to create approval rules |
| `Can update approval rules` | Allows the employee to update approval rules |
| `Can delete approval rules` | Allows the employee to delete approval rules |
| `Can read approval rules` | Allows the employee to view approval rules |

## Pending order Permissions [​](#pending-order-permissions)

| Permission | Description |
| --- | --- |
| `Can approve/decline all pending orders` | Allows the employee to approve or decline all pending orders |
| `Can approve/decline pending orders` | Allows the employee to approve or decline assigned pending orders |
| `Can view all pending orders` | Allows the employee to view all pending orders |

---

## Payment Process

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/order-approval/guides/03-payment-process.html

# Order approval's payment process [​](#order-approval-s-payment-process)

The payment process of the order approval component is the same as the payment process of the order component. You can select the payment method that you want to use for your orders; however unlike the standard order component, the payment process will be executed only after the order has been approved in case of the online payment method (Visa, PayPal, etc.).

## Customization [​](#customization)

### Storefront [​](#storefront)

The payment process of the order approval component can be customized by extending or overriding this page `@OrderApproval/storefront/pending-order/page/pending-approval/detail.html.twig`

### Payment process [​](#payment-process)

Normally, after reviewer approves the order, the payment process will be executed automatically. However, if you just want to approve the order without executing the payment process, you can subscribe to the `PendingOrderApprovedEvent` event and set the `PendingOrderApprovedEvent::shouldProceedPlaceOrder` to `false`. This event is dispatched in the `Shopware\Commercial\B2B\OrderApproval\Storefront\Controller\ApprovalPendingOrderController::order` method.

php

```shiki
use Shopware\Commercial\B2B\OrderApproval\Event\PendingOrderApprovedEvent;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            PendingOrderApprovedEvent::class => 'onPendingOrderApproved'
        ];
    }

    public function onPendingOrderApproved(PendingOrderApprovedEvent $event): void
    {
        $event->setShouldProceedPlaceOrder(false);
    }
}
```

---

## How to add a new approval condition

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/order-approval/guides/04-add-new-approval-condition.html

# How to add a new approval condition [​](#how-to-add-a-new-approval-condition)

The order approval component provides a set of conditions for defining your approval rules. However, if you need to add a new condition, you can do so via an app or a plugin.

## Plugin [​](#plugin)

To add a custom rule, following this document [Add custom rule](./../../../../../guides/plugins/plugins/framework/rule/add-custom-rules.html)

Example:

php

```shiki
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use Shopware\Core\Framework\Rule\Rule;
use Shopware\Core\Framework\Rule\RuleComparison;
use Shopware\Core\Framework\Rule\RuleConfig;
use Shopware\Core\Framework\Rule\RuleConstraints;
use Shopware\Core\Framework\Rule\RuleScope;

class CartAmountRule extends Rule
{
    final public const RULE_NAME = 'totalCartAmount';

    public const AMOUNT = 1000;

    protected float $amount;

    /**
     * @internal
     */
    public function __construct(
        protected string $operator = self::OPERATOR_GTE,
        ?float $amount = self::AMOUNT
    ) {
        parent::__construct();
        $this->amount = (float) $amount;
    }

    /**
     * @throws UnsupportedOperatorException
     */
    public function match(RuleScope $scope): bool
    {
        if (!$scope instanceof CartRuleScope) {
            return false;
        }

        return RuleComparison::numeric($scope->getCart()->getPrice()->getTotalPrice(), $this->amount, $this->operator);
    }

    public function getConstraints(): array
    {
        return [
            'amount' => RuleConstraints::float(),
            'operator' => RuleConstraints::numericOperators(false),
        ];
    }

    public function getConfig(): RuleConfig
    {
        return (new RuleConfig())
            ->operatorSet(RuleConfig::OPERATOR_SET_NUMBER)
            ->numberField('amount');
    }
}
```

Then, we have to register it in our `services.xml` and tag it as `shopware.approval_rule.definition`

xml

```shiki
 <service id="YourPluginNameSpace\CartAmountRule" public="true">
    <tag name="shopware.approval_rule.definition"/>
 </service>
```

## App [​](#app)

INFO

Note that the approval rule conditions for app is introduced in Commercial plugin 6.4.0, and are not supported in previous versions.

### Overview [​](#overview)

Following the same methodology as [Add custom rule conditions](./../../../../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html) in the Administration Rule Builder, approval custom conditions is configured with fields displayed on the Storefront Approval Rule detail page and the logic is defined within [App Scripts](./../../../../../guides/plugins/apps/app-scripts/).

### Concepts [​](#concepts)

#### Folder structure [​](#folder-structure)

The folder structure is similar to [Add custom rule conditions](./../../../../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html). An App Approval Rule Condition is defined in the `manifest.xml` file of your app and its condition logic is defined in app script file. The difference is all scripts for rule conditions must be placed inside `Resources/scripts/approval-rule-conditions` within the root directory of the app.

text

```shiki
└── DemoApp
    ├── Resources
    │   └── scripts                         // all scripts are stored in this folder
    │       ├── approval-rule-conditions    // reserved for scripts of approval rule conditions
    │       │   └── custom-condition.twig   // the file name may be freely chosen but must be identical to the corresponding `script` element within `rule-conditions` of `manifest.xml`
    │       └── ...
    └── manifest.xml
```

#### Manifest file [​](#manifest-file)

Similar to [Add custom rule conditions](./../../../../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html), a condition's manifest file has `identifier`, `name` and `script`.

The `name` is a descriptive and translatable name for the condition. The name will be shown within the Condition's selection in the Storefront Approval Rule detail or create page.

Within the script tag, the path of the twig script file must include the `/approval-rule-conditions/` prefix.

Let's create a custom condition that compares the total price of the current shopping cart.

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>

    <rule-conditions>
        <rule-condition>
            <identifier>total_cart_amount</identifier>
            <name>Total cart amount</name>
            <group>approval</group>
            <script>/approval-rule-conditions/custom-condition.twig</script>
            <constraints>
                <single-select name="operator">
                    <placeholder>Choose an operator...</placeholder>
                    <options>
                        <option value="=">
                            <name>Is equal to</name>
                        </option>
                        <option value="!=">
                            <name>Is not equal to</name>
                        </option>
                        <option value=">">
                            <name>Is greater than</name>
                        </option>
                        <option value=">=">
                            <name>Is greater than or equal to</name>
                        </option>
                    </options>
                    <required>true</required>
                </single-select>
                <float name="amount">
                    <placeholder>Enter an amount...</placeholder>
                </float>
            </constraints>
        </rule-condition>
    </rule-conditions>
</manifest>
```

The fields in `constraints` tag are used for rendering `operators` and `value` fields.

INFO

Note that the value field is only supported with number fields (`float`, `int`), text fields (`text`), single-selection fields (`single-select`), and multi-selection fields (`multi-select`).

This is how the custom condition appears on the Approval Rule detail page, the `Total cart amount` condition in added to condition selection list. In this case, the value is displayed as a number field that allows decimals, with each increment being 0.01. This is because the `float` tag is defined in the manifest file.

![App Approval Rule Condition](/assets/approval-rule-condition.DbLxCWRX.png)

#### Scripts [​](#scripts)

Script logic is similar to [Add custom rule conditions](./../../../../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html). Let's continue with our example by creating a script file that compares the current shopping cart's total price with the pre-established value in the approval rule.

twig

```shiki
// Resources/scripts/approval-rule-conditions/custom-condition.twig
{% if scope.cart is not defined %}
    {% return false %}
{% endif %}

{% return compare(operator, scope.cart.price.totalPrice, amount) %}
```

In the example above, we first check whether we can retrieve the current cart from the instance of `RuleScope` and return `false` otherwise.

We then use the variables `operator` and `totalPrice`, provided by the constraints of the condition, to evaluate whether the total price in question matches the total price of the cart.

### Other examples [​](#other-examples)

#### Text field [​](#text-field)

![App Approval Rule Condition Text](/assets/approval-rule-condition-text-field-example.C4YLgBMt.png)

xml

```shiki
<!-- manifest.xml -->
<!-- ... -->
<rule-condition>
    <identifier>cart_tax_status_rule_script</identifier>
    <name>Customer's first name</name>
    <group>customer</group>
    <script>/approval-rule-conditions/custom-condition.twig</script>
    <constraints>
        <single-select name="operator">
            <options>
                <option value="=">
                    <name>Is equal to</name>
                </option>
                <option value="!=">
                    <name>Is not equal to</name>
                </option>
            </options>
        </single-select>
        <text name="firstName">
            <placeholder>Enter customer's first name</placeholder>
        </text>
    </constraints>
</rule-condition>
<!-- ... -->
```

twig

```shiki
// Resources/scripts/approval-rule-conditions/custom-condition.twig
{% if scope.salesChannelContext.customer is not defined %}
    {% return false %}
{% endif %}

{% return compare(operator, scope.salesChannelContext.customer.firstName, firstName) %}
```

#### Single-select [​](#single-select)

![App Approval Rule Condition Single Select](/assets/approval-rule-condition-single-select-example.CVH_fdLI.png)

xml

```shiki
<!-- manifest.xml -->
<!-- ... -->
<rule-condition>
    <identifier>cart_tax_status_rule_script</identifier>
    <name>Cart tax status</name>
    <group>cart</group>
    <script>/approval-rule-conditions/custom-condition.twig</script>
    <constraints>
        <single-select name="operator">
            <options>
                <option value="=">
                    <name>Is equal to</name>
                </option>
                <option value="!=">
                    <name>Is not equal to</name>
                </option>
            </options>
        </single-select>
        <single-select name="taxStatus">
            <options>
                <option value="net">
                    <name>Net</name>
                </option>
                <option value="gross">
                    <name>Gross</name>
                </option>
            </options>
        </single-select>
    </constraints>
</rule-condition>
<!-- ... -->
```

twig

```shiki
// Resources/scripts/approval-rule-conditions/custom-condition.twig
{% if scope.cart is not defined %}
    {% return false %}
{% endif %}

{% return compare(operator, scope.cart.price.taxStatus, taxStatus) %}
```

#### Multi-select [​](#multi-select)

![App Approval Rule Condition Multi Select](/assets/approval-rule-condition-multi-select-example._ApET8pn.png)

xml

```shiki
<!-- manifest.xml -->
<!-- ... -->
<rule-condition>
    <identifier>cart_currency_rule_script</identifier>
    <name>Cart currency</name>
    <group>cart</group>
    <script>/approval-rule-conditions/cart-currency.twig</script>
    <constraints>
        <single-select name="operator">
            <options>
                <option value="=">
                    <name>Is one of</name>
                </option>
                <option value="!=">
                    <name>Is none of</name>
                </option>
            </options>
             <required>true</required>
        </single-select>
        <multi-select name="isoCode">
            <options>
                <option value="EUR">
                    <name>Euro</name>
                </option>
                <option value="USD">
                    <name>US-Dollar</name>
                </option>
                <option value="GBP">
                    <name>Pound</name>
                </option>
            </options>
            <required>true</required>
        </multi-select>
    </constraints>
 </rule-condition>
<!-- ... -->
```

twig

```shiki
// Resources/scripts/approval-rule-conditions/custom-condition.twig
{% if scope.salesChannelContext.currency is not defined %}
    {% return false %}
{% endif %}
{% return compare(operator, scope.salesChannelContext.currency.isoCode, isoCode) %}
```

---

## Organization unit

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/organization-unit/

# Organization unit component [​](#organization-unit-component)

Organization unit component is a part of the B2B Employee Management. Each unit can have its own set of employees, and use specific payment and shipping methods. It will allow for the configuration of more differentiated and specific access rights to meet the needs of businesses with complex structures.

## Requirements [​](#requirements)

* You need to have Employee Management component installed and activated (see [Employee Management](./../employee-management/)).

---

## Entities & Schema

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/organization-unit/concepts/entities-and-schema.html

# Entities and schema [​](#entities-and-schema)

## Entities [​](#entities)

### Organization [​](#organization)

The organization entity represents a structural unit within a customer account. Each organization has a name, belongs to a specific customer, and defines both a default billing address and a default shipping address, selected from the customer's addresses. An organization can have multiple employees assigned to it and can also be assigned specific payment and shipping methods. These assignments define which options are available to employees of the organization during checkout.

### Organization Customer Address [​](#organization-customer-address)

The organization customer address entity defines a customer address that is assigned to a specific organization. It links a customer address to an organization and specifies whether the address is used for billing or shipping purposes.

## Schema [​](#schema)

---

## Store API

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/organization-unit/guides/store-api.html

## Store API [​](#store-api)

Here are some of the actions you can perform on *Organization Unit* using the Store API.

### Create new organization unit [​](#create-new-organization-unit)

http

```shiki
POST {url}/store-api/organization-unit {
    name: {string},
    defaultShippingAddressId: {uuid},
    defaultBillingAddressId: {uuid},
    employeeIds: {array of uuid},
    shippingAddressIds: {array of uuid},
    billingAddressIds: {array of uuid},
    paymentMethodIds: {array of uuid},
    shippingMethodIds: {array of uuid}
}
```

### Update organization unit [​](#update-organization-unit)

http

```shiki
POST {url}/store-api/organization-unit/{id} {
    name: {string},
    defaultShippingAddressId: {uuid},
    defaultBillingAddressId: {uuid},
    employeeIds: {array of uuid},
    shippingAddressIds: {array of uuid},
    billingAddressIds: {array of uuid},
    paymentMethodIds: {array of uuid},
    shippingMethodIds: {array of uuid}
}
```

### Get organization unit [​](#get-organization-unit)

http

```shiki
GET|POST {url}/store-api/organization-unit/{id}
```

### Get organization units [​](#get-organization-units)

http

```shiki
GET|POST {url}/store-api/organization-units
```

### Remove organization units [​](#remove-organization-units)

http

```shiki
DELETE {url}/store-api/organization-unit {
    ids: {array}
}
```

For more details, refer to [B2B Organization Unit](https://shopware.stoplight.io/docs/store-api/branches/main/b286c1f43d395-shopware-store-api) from Store API docs.

---

## Extending the Organization entity

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/organization-unit/guides/extending-organization-entity.html

# What is an Attribute Entity [​](#what-is-an-attribute-entity)

An Attribute Entity uses PHP attributes (e.g. `#[Entity(...)]`, `#[Field(...)]`) to describe the structure of the entity instead of the traditional EntityDefinition and EntityCollection. Unlike normal entities, attribute entities do not have a corresponding EntityDefinition class, which changes how you need to write extensions for them.

You can read more about using Attribute entities here: [Entities via attributes](./../../../../../guides/plugins/plugins/framework/data-handling/entities-via-attributes.html).

## How to extend the Organization entity [​](#how-to-extend-the-organization-entity)

When extending a normal entity, you usually refer to its EntityDefinition class in your extension. However, attribute entities like `OrganizationEntity` don't have such classes, you must reference them by their entity name string.

The entity name is the value provided in the #[Entity(...)] attribute. For `OrganizationEntity`, that name is:

php

```shiki
#[Entity('b2b_components_organization')]
```

Even though `OrganizationEntity` does not have a traditional EntityDefinition class, Shopware still generates the definition and repository using the entity name.

| Type | Service name |
| --- | --- |
| Definition | `b2b_components_organization.definition` |
| Repository | `b2b_components_organization.repository` |

An example of an organization extension

php

```shiki
class OrganizationExtension extends EntityExtension
{
    public function extendFields(FieldCollection $collection): void
    {
        $collection->add(
            (new OneToManyAssociationField(
                'yourEntities',
                YourEntityDefinition::class,
                'organization_id'
            ))->addFlags(new CascadeDelete())
        );
    }

    public function getEntityName(): string
    {
        return 'b2b_components_organization';
    }
}
```

---

## How to identify the organization unit from the context

**Source:** https://developer.shopware.com/docs/products/extensions/b2b-components/organization-unit/guides/how-to-identify-organization-from-context.html

# How to identify the organization unit from the context [​](#how-to-identify-the-organization-unit-from-the-context)

To determine the organization unit linked to an employee, you can retrieve the employee entity from the sales channel context. This entity includes a reference to the organization the employee belongs to.

Here’s an example:

php

```shiki
...
$employee = $context->getCustomer()?->getExtension(SalesChannelContextFactoryDecorator::CUSTOMER_EMPLOYEE_EXTENSION);

if (!$employee instanceof EmployeeEntity) {
    return;
}

$organizationId = $employee->get('organizationId');
...
}
```

This code checks whether the current customer has an employee extension. If it does, it retrieves the employee entity and then accesses the `organizationId` property to get the ID of the organization unit associated with that employee. You can use this `organizationId` to load data related to the organization or to control what the employee is allowed to access.

---

