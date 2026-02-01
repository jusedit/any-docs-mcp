# Resources References Adr Part2

*Scraped from Shopware Developer Documentation*

---

## Move controller level annotation into Symfony route annotation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-02-09-controller-configuration-route-defaults.html

# Move controller level annotation into Symfony route annotation [​](#move-controller-level-annotation-into-symfony-route-annotation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-02-09-controller-configuration-route-defaults.md)

## Context [​](#context)

Annotations are used to configure controllers in the core currently. The configuration can contain the following as example:

* @LoginRequired
  + Customer needs to be logged in
* @Acl
  + Protects the controller with special acl privileges
* @RouteScope
  + Defines the scope of the route
* and many more

As Annotations are bound to the implementing class, all decorators have to copy and be updated to date with the target class

## Decision [​](#decision)

We replace the Annotations from all controllers and define them in the `defaults` of the Symfony `@Route` annotation. The custom annotation will be deprecated for removal in 6.5.0.

Here is an example of the `@LoginRequired` migration:

### Before [​](#before)

php

```shiki
@LoginRequired
@Route("/store-api/product", name="store-api.product.search", methods={"GET", "POST"})
public function myAction()
```

### After [​](#after)

php

```shiki
@Route("/store-api/product", name="store-api.product.search", methods={"GET", "POST"}, defaults={"_loginRequired"=true})
public function myAction()
```

Symfony passes the defaults to the attribute bag of the Request object, and we can check the attributes in the request cycle of the http kernel.

The following annotations will be replaced:

* `@Captcha` -> `_captcha`
* `@LoginRequired` -> `_loginRequired`
* `@Acl` -> `_acl`
* `@ContextTokenRequired` -> `_contextTokenRequired`
* `@RouteScope` -> `_routeScope`

Extensions can still decorate the controller if it has an abstract class or use events like `KernelEvents::REQUEST` or `KernelEvents::RESPONSE` to execute code before or after the actual controller.

---

## Rule Scripting in apps

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-02-21-rule-scripting-in-apps.html

# Rule Scripting in apps [​](#rule-scripting-in-apps)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-02-21-rule-scripting-in-apps.md)

## Context [​](#context)

Currently rule conditions need to be hard-coded both as PHP classes and in the administration as Vue components. We want to introduce the possibility for apps to provide their own custom rule conditions.

## Decision [​](#decision)

To allow apps to define custom logic for their rule conditions we implement a generic script rule. As with app scripting we use Twig, as it brings a secure PHP sandbox and allows interacting directly with objects. The scripts will be saved in the database and fetched when building a rule's payload or validating a rule.

For storing the scripts in the database we use a new entity `app_script_condition` which not only contains the script that is used for evaluating a condition, but also the constraints used in rule validation. These pre-defined constraints can be configured in the manifest of the app and are also used to render the fields for the parameters of a condition when used in the rule builder within the administration.

### `AppScriptConditionDefinition` and associations [​](#appscriptconditiondefinition-and-associations)

php

```shiki
class AppScriptConditionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'app_script_condition';

    // ...

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new PrimaryKey(), new Required()),
            new TranslatedField('name'),
            (new BoolField('active', 'active'))->addFlags(new Required()),
            new StringField('group', 'group'),
            (new LongTextField('script', 'script'))->addFlags(new Required(), new AllowHtml(false)),
            new JsonField('constraints', 'constraints'),
            (new FkField('app_id', 'appId', AppDefinition::class))->addFlags(new Required()),
            (new OneToManyAssociationField('conditions', RuleConditionDefinition::class, 'script_id', 'id'))->addFlags(new SetNullOnDelete(), new ReverseInherited('script')),
        ]);
    }
}
```

diff

```shiki
// src/Core/Content/Rule/Aggregate/RuleCondition/RuleConditionDefinition.php 

            (new FkField('rule_id', 'ruleId', RuleDefinition::class))->addFlags(new Required()),
+           new FkField('script_id', 'scriptId', AppScriptConditionDefinition::class),
            // ...
            new ManyToOneAssociationField('rule', 'rule_id', RuleDefinition::class, 'id', false),
+           new ManyToOneAssociationField('script', 'script_id', AppScriptConditionDefinition::class, 'id', true),
```

### `ScriptRule` implementation [​](#scriptrule-implementation)

There will be a generic extension of `Rule` named `ScriptRule` which will be used for every condition added by apps.

It has properties for the `script` and the `constraints`, both of which will be set from the corresponding values of `app_script_condition` when the rule's payload is indexed.

The constraints will be used for the validation of the condition and the script is used for the evaluation of the condition. To evaluate the condition we use a Twig macro where the actual script of the app is inserted:

```shiki
{%% macro evaluate(%1$s) %%}
    %2$s
{%% endmacro %%}
```

We use a macro here because we want to allow the use of return statements. Even though return statements may be used outside of macros, Twig won't actually output the returned value. With the macro we can set the returned value to a variable and properly output the variable instead:

```shiki
{%% set var = _self.evaluate(%1$s) %%}
{{ var }}
```

Making use of the macro we can avoid having to write a custom token parser to override return statements.

By calling `setConstraints` with the data stored in a json field of `app_script_condition`, the data will be transformed into actual constraints for the further validation of the condition.

Finally the `values` property contains an array of actual parameters, provided by the user when setting up the condition in the rule builder. Those parameters are passed as part of the context to Twig when rendering the script.

#### Complete draft for `ScriptRule` [​](#complete-draft-for-scriptrule)

php

```shiki
class ScriptRule extends Rule
{
    const CONSTRAINT_MAPPING = [
        'notBlank' => NotBlank::class,
        'arrayOfUuid' => ArrayOfUuid::class,
        'arrayOfType' => ArrayOfType::class,
        'choice' => Choice::class,
        'type' => Type::class,
    ];

    protected string $script = '';

    protected array $constraints = [];

    protected array $values = [];

    public function match(RuleScope $scope): bool
    {
        $context = array_merge(['scope' => $scope], $this->values);
        $script = new Script(
            $this->getName(),
            sprintf('
                {%% apply spaceless %%}
                    {%% macro evaluate(%1$s) %%}
                        %2$s
                    {%% endmacro %%}

                    {%% set var = _self.evaluate(%1$s) %%}
                    {{ var }}
                {%% endapply  %%}
            ', implode(', ', array_keys($context)), $this->script),
            $scope->getCurrentTime(),
            null
        );

        $twig = new TwigEnvironment(
            new ScriptTwigLoader($script),
            $script->getTwigOptions()
        );

        $twig->addExtension(new PhpSyntaxExtension());

        return filter_var(
            trim($twig->render($this->getName(), $context)),
            FILTER_VALIDATE_BOOLEAN
        );
    }

    public function getConstraints(): array
    {
        return $this->constraints;
    }

    public function setConstraints(array $constraints): void
    {
        $this->constraints = [];
        foreach ($constraints as $name => $types) {
            $this->constraints[$name] = array_map(function ($type) {
                $arguments = $type['arguments'] ?? [];
                $class = self::CONSTRAINT_MAPPING[$type['name']];

                return new $class(...$arguments);
            }, $types);
        }
    }

    public function getName(): string
    {
        return 'scriptRule';
    }
}
```

### Changes for building rule payload with scripts [​](#changes-for-building-rule-payload-with-scripts)

When an app script condition is used in a rule, the script from `app_script_condition` is assigned when building the payload. Also there should be an indexer for `app_script_condition`, that calls the `RulePayloadUpdater` for every `rule` the script is used in, to keep the payload up to date on changes made to the scripts, e.g. on lifecycle events of the corresponding app.

diff

```shiki
// src/Core/Content/Rule/DataAbstractionLayer/RulePayloadUpdater.php 

        $conditions = $this->connection->fetchAll(
-           'SELECT LOWER(HEX(rc.rule_id)) as array_key, rc.* FROM rule_condition rc  WHERE rc.rule_id IN (:ids) ORDER BY rc.rule_id',
+           'SELECT LOWER(HEX(rc.rule_id)) as array_key, rc.*, rs.script
+           FROM rule_condition rc
+           LEFT JOIN app_script_condition rs ON rc.script_id = rs.id AND rs.active = 1
+           WHERE rc.rule_id IN (:ids)
+           ORDER BY rc.rule_id',
            ['ids' => Uuid::fromHexToBytesList($ids)],
            ['ids' => Connection::PARAM_STR_ARRAY]
        );
        
        // ...
        
-           if ($rule['value'] !== null) {
+           if ($object instanceof ScriptRule) {
+               $object->assign([
+                   'script' => $rule['script'],
+                   'values' => $rule['value'] ? json_decode($rule['value'], true) : []
+               ]);
+           }
+           elseif ($rule['value'] !== null) {
                $object->assign(json_decode($rule['value'], true));
            }
```

### Defining a rule condition in the manifest [​](#defining-a-rule-condition-in-the-manifest)

The following partial manifest defines a custom rule condition that requires a string value `operator` of either `=` or `!=` and an array `customerGroupIds` of id's for the entity `customer_group`.

The syntax for defining the parameters of a condition follows the same schema of defining config or custom fields.

xml

```shiki
<!-- ExampleApp/manifest.xml -->
<!-- ... -->
<rule-conditions>
    <rule-condition>
        <name>My custom rule condition</name>
        <group>customer</group>
        <script>customer-group-rule-script.twig</script>
        <constraints>
            <single-select name="operator">
                <label>Operator</label>
                <placeholder>Choose an operator...</placeholder>
                <options>
                    <option value="=">
                        <name>Is equal to</name>
                    </option>
                    <option value="!=">
                        <name>Is not equal to</name>
                    </option>
                </options>
                <required>true</required>
            </single-select>
            <multi-entity-select name="cusstomerGroupIds">
                <label>Customer groups</label>
                <placeholder>Choose customer groups...</placeholder>
                <entity>customer_group</entity>
                <required>true</required>
            </multi-entity-select>
        </constraints>
    </rule-condition>
</rule-conditions>
<!-- ... -->
```

The following rule script is logically identical to the hard-coded rule condition for matching that a customer is in a customer group.

```shiki
{# ExampleApp/scripts/rule-conditions/customer-group-rule-script.twig #}

{% if scope.salesChannelContext.customer is not defined %}
    {% return false %}
{% endif %}

{% if operator == "=" %}
    {% return scope.salesChannelContext.customer.groupId in customerGroupIds %}
{% else %}
    {% return scope.salesChannelContext.customer.groupId not in customerGroupIds %}
{% endif %}
```

We also may offer Twig helper functions for evaluation of basic expressions for the more common use cases. So the above construct could be reduced to:

```shiki
{% comparison.compare(operator, scope.salesChannelContext.customer.groupId, customerGroupIds) %}
```

### Implementation in administration [​](#implementation-in-administration)

There will be only a single Vue component for all rule conditions based on scripts. The available fields and the type of each field will be dynamically built from the constraints of a rule script.

The following is a draft for a generic component that gets, sets and validates fields and their values as defined as constraints of an app's custom rule condition.

javascript

```shiki
Component.extend('sw-condition-script', 'sw-condition-base', {
    template,
    inheritAttrs: false,

    computed: {
        constraints() {
            return this.condition.script.constraints;
        },

        values() {
            const that = this;
            const values = {};

            Object.keys(this.constraints).forEach((key) => {
                Object.defineProperty(values, key, {
                    get: () => {
                        that.ensureValueExist();

                        return that.condition.value[key];
                    },
                    set: (value) => {
                        that.ensureValueExist();
                        that.condition.value = { ...that.condition.value, [key]: value };
                    },
                });
            });

            return values;
        },

        currentError() {
            let error = null;

            Object.keys(this.constraints).forEach((key) => {
                if (error) {
                    return;
                }

                const errorProperty = Shopware.State.getters['error/getApiError'](this.condition, `value.${key}`);

                if (errorProperty) {
                    error = errorProperty;
                }
            });

            return error;
        },
    },
    
    // ...
});
```

html

```shiki
<!-- /src/app/component/rule/condition-type/sw-condition-script/sw-condition-script.html.twig -->
{% block sw_condition_value_content %}
<div class="sw-condition-script sw-condition__condition-value">
    {% block sw_condition_script_fields %}
    <sw-arrow-field
        v-for="(constraint, index) in constraints"
        :disabled="disabled"
    >
        <!-- use the specific type of field as need for a constraint -->
        <!-- e.g. sw-entity-multi-select, sw-tagged-field, sw-number-field ... -->
    </sw-arrow-field>
    {% endblock %}
</div>
{% endblock %}
```

## Consequences [​](#consequences)

* Apps will be able to provide their own custom rule conditions, which will consequently be available in the administration's rule builder as any of the hard-coded rule conditions are.
* Rule scripting, first implemented for apps, eventually opens the door for scripting of rule conditions within the administration, e.g. by providing a code editor in the rule builder.

---

## Domain exceptions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-02-24-domain-exceptions.html

# Domain exceptions [​](#domain-exceptions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-02-24-domain-exceptions.md)

## Context [​](#context)

Until now, we have implemented many different exception classes in Shopware to map different exception cases. However, this pattern is very cumbersome for developers to maintain properly, which is why we often fall back on the old \RuntimeException. Another disadvantage of this pattern is that the system is overwhelmed with exception classes and therefore the overview of possible exceptions suffers.

Domain exceptions should be specific in 99% of cases, otherwise, they are no longer clearly identifiable and traceable. If we want to add a generic exception like EntityNotFound exceptions everywhere, it will not help API consumer to identify the root cause. Therefore, it is for a good reason that there are similar exceptions occur again in many places. If something goes wrong from anywhere, there should be a unique code for it. In good software, you have a unique code for each error. This code is then listed in a code list that is publicly available. For each code, there is clear documentation of when and where it occurs and how to fix it.

## Solution [​](#solution)

With the following pattern, we would like to achieve the following goals:

* Developers can **no longer** just throw any **\RuntimeException** that can't be traced.
* Each exception has its **own error code**, which is passed to external APIs
* We **reduce the number of exception classes** we don't react to in the system (e.g. `\InvalidArgumentException`)

### Domain exceptions [​](#domain-exceptions-1)

We implement a separate exception class for each domain. This class is used as a factory for all exceptions within the domain. The \_\_construct of the DomainException is set to `private`, so that only the factory methods can create an instance.

php

```shiki
<?php

namespace Shopware\Core\Content\Cms;

use Shopware\Core\Framework\HttpException;
use Symfony\Component\HttpFoundation\Response;

class CmsException extends HttpException
{
    public const NOT_FOUND_CODE = 'CMS_NOT_FOUND';
    public const SOME_FOO_CODE = 'CMS_SOME_FOO';
    
    public static function notFound(?\Throwable $e = null): void
    {
        return new self(Response::HTTP_NOT_FOUND, self::NOT_FOUND_CODE, 'Cms page not found', [], $e);
    }

    public static function anExceptionIDontCatchAnywhere(?\Throwable $e = null) 
    {
        return new self(Response::HTTP_INTERNAL_SERVER_ERROR, self::SOME_FOO_CODE, 'Some foo', [], $e);
    }
}
```

However, the DomainExceptions are not (necessarily) made to be caught and handled in a try-catch. Therefore, we will continue to implement our own exception classes, for exceptions that we want to catch ourselves in the system via a `try-catch`, which extends the `DomainException`. These exceptions are then stored in an exception subfolder:

php

```shiki
<?php

use Shopware\Core\Framework\ShopwareHttpException;

// src/Core/Content/Cms/ProductException.php
namespace Shopware\Core\Content\Product {

    class ProductException extends ShopwareHttpException
    {
        public static function notFound(?\Throwable $e = null): void
        {
            return new ProductNotFoundException(Response::HTTP_NOT_FOUND, self::NOT_FOUND_CODE, 'Product page not found', [], $e);
        }
    }
}

// src/Core/Content/Product/Exception/ProductNotFoundException.php
namespace Shopware\Core\Content\Product\Exception {
    class ProductNotFoundException extends ProductException { }
}

try {
    throw ProductException::notFound();
} catch (ProductNotFoundException $e) {
    throw $e;
}
```

---

## Consistent deprecation notices in Core

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-02-28-consistent-deprecation-notices-in-core.html

# Consistent deprecation notices in Core [​](#consistent-deprecation-notices-in-core)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-02-28-consistent-deprecation-notices-in-core.md)

## Context [​](#context)

Currently, we use `@deprecated` annotations to warn 3rd party developers that we will introduce some breaking change in the next major version. This annotation instructs the IDE to warn the developer that the method/class is deprecated, but has no consequences at runtime.

PHP/Symfony has also a built-in runtime deprecation mechanism with `trigger_deprecation`. This is only used sparsely in the core in `Feature::triggerDeprecated()`.

## Decision [​](#decision)

In the future we will use both `@deprecated` and runtime deprecation notices over `trigger_deprecation`. This means wherever a `@deprecated` annotation is used we will also throw a deprecation notice.

The deprecation notices can be thrown conditionally, e.g., when a new parameter in a method will become required, we will only throw the deprecation if the method is called in the old/deprecated way. If it is already used in the new way, there is no need to trigger the deprecation.

This has the benefit that 3rd party developers get deprecation notices during runtime with a concrete deprecation message and the stacktrace where the deprecation was triggered. This is useful, e.g., to run the test suite of a plugin against a new shopware version to get a list of all deprecations.

Additionally, we can use this to provide better feedback to 3rd party developers, e.g., if App Scripts use a deprecated method/class or if some private apps in the cloud rely on deprecated functionality.

### Ensuring the correct usage during CI [​](#ensuring-the-correct-usage-during-ci)

To ensure that this guideline is followed, we add a step in the CI (e.g., a custom PHPStan rule or a special unit test) that checks that every method that has a `@deprecated` annotation triggers also a deprecation notice, and vice versa.

There are some special cases where we use a `@deprecated` annotation, but a according triggered deprecation notice makes no sense:

* Classes/methods marked as deprecated, because they will be considered `internal` starting with the next major version.
* Methods are deprecated because the return type will change. For both cases we will add special keywords to the `@deprecated` annotation and our CI-check will skip those annotations.

### Common Implementation [​](#common-implementation)

We will add a common implementation inside the core that should be used everywhere. This makes it easier to change the deprecation handling later on in a single place and makes it possible to provide custom deprecation warnings, e.g., for app scripts inside Symfony's debug toolbar.

The new method will accept the deprecation message as string and the feature flag of the major version, where the deprecation will be removed. The method will then trigger a deprecation notice if the major feature flag is not active. If the flag is active, it will throw an exception instead. This ensures that we inside the core don't rely on deprecated functionality as we have a test-pipeline where the major feature flag is set to true.

A POC implementation in the `Feature`-class can look something like this:

php

```shiki
    public static function triggerDeprecationOrThrow(string $message, string $majorFlag): void
    {
        if (self::isActive($majorFlag) || !self::has($majorFlag)) {
            throw new \RuntimeException('Deprecated Functionality: ' . $message);
        }

        trigger_deprecation('', '', $message);
    }
```

Additionally, we will deprecate the `triggerDeprecated()` method, because it will only trigger deprecation messages if the feature flag is active, but in that case the deprecated code will already be removed and the deprecation message never thrown.

### Consistent deprecation notice format [​](#consistent-deprecation-notice-format)

To be as useful as possible, we should use a consistent format for the deprecation messages.

Most importantly, we should ensure that the following information is present in the deprecation message:

* The name of the method/class that is deprecated
* The version in which the deprecation will be removed and the announced changes will be applied
* What to do instead to get rid of the deprecation, e.g., using another method/class or provide an additional param etc.

As an example:

* **Bad:** Will be removed, use NewFeature::method() instead
* **Good:** Method OldFeature::method() will be removed in v6.5.0.0, use NewFeature::method() instead

---

## Use `ResetInterface` to reset instance state during requests

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-09-reset-class-state-during-requests.html

# Use `ResetInterface` to reset instance state during requests [​](#use-resetinterface-to-reset-instance-state-during-requests)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-09-reset-class-state-during-requests.md)

## Context [​](#context)

In many places, we use [memoization](https://en.wikipedia.org/wiki/Memoization) to store data inside an instance variable to cache the data and reuse it during the same request without needing to recompute/fetch it again.

Currently, we do not reset that data and rely on the fact that for every request, the kernel will be rebooted and each request will have new instances of those services (like PHP-FPM does). With modern php application servers (e.g., roadrunner, swoole) that is not the case anymore and service instances maybe shared and reused for multiple requests.

## Decision [​](#decision)

Symfony provides a way to reset data in between requests with the [`kernel.reset`](https://symfony.com/doc/current/reference/dic_tags.html#kernel-reset)-tag. A class that holds memoized data in an instance variable, needs to provide a method to reset that data, and the service has to be tagged accordingly in the DI-container.

For consistency, we implement the `\Symfony\Contracts\Service\ResetInterface` which will add a `public function reset(): void`, where the reset is performed. The only exceptions to this rule are services that already implement a `reset`-method, and thus we cannot add one, in that case we will add a method with a different suitable name to reset the internal state, and configure that method to be used to reset data in the service tag.

This way we can build part of shopware already in a way that is compatible with modern PHP applications servers, and we are future-proof. This reset is especially important in the cloud environment, as there the next request may be for different shop/tenant, so if we won't reset the data, we would not just serve stale data, but we wil instead data from a different instance! Additionally, it makes unit testing easier, as PHPUnit already reuses service instances between execution of each test cases which already made trouble in the past.

## Consequences [​](#consequences)

Wherever we have a class that holds some memoized data in an instance variable e.g.

php

```shiki
class FooService
{
    private array $data = [];
    
    public function getData(): array
    {
        if ($this->data) {
            return $this->data;
        }
        
        return $this->data = $this->fetchDataFromSomewhere();
    }
}
```

We will implement the `ResetInterface` and provide a `reset()` method, to reset that internal state between requests:

php

```shiki
use Symfony\Contracts\Service\ResetInterface;

class FooService implements ResetInterface
{
    private array $data = [];
    
    public function getData(): array
    {
        if ($this->data) {
            return $this->data;
        }
        
        return $this->data = $this->fetchDataFromSomewhere();
    }

    public function reset(): void
    {
        $this->data = [];
    }
}
```

And additionally we will tag the service with the `kernel.reset` tag:

xml

```shiki
<service id="FooService">
    <tag name="kernel.reset" method="reset"/>
</service>
```

That way, symfony will reset the data between requests automatically.

Additionally, we've added a hook to our `IntegrationTestBehaviour`, that will also reset that state between the execution of test cases.

This makes it unnecessary to reset the internal state manually by using `Reflection` to overwrite and reset the internal/private instance variable. If you need to do this in your test case it clearly shows that you should go with the `ResetInterface` and `kernel.reset` tag instead! Having to rely on `Reflection` in your test cases to reset data is a major red flag now!

---

## Extract data handling classes to extension sdk

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-15-extract-data-handling-classes-to-extension-sdk.html

# Extract data handling classes to extension sdk [​](#extract-data-handling-classes-to-extension-sdk)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-15-extract-data-handling-classes-to-extension-sdk.md)

## Context [​](#context)

* The package `@shopware-ag/meteor-extension-sdk` will be referred to as sdk
* The ts/js implementation of the Administration is referred to as administration

Previously the administration held the implementation of the classes `Entity`, `EntityCollection` and `Criteria`. This led to the problem, that the sdk was unable to identify instances of these classes easily. Since the administration is not a standalone package that could be imported in the sdk. Also, the sdk would need to copy the implementation since we want to copy the administration data handling in the sdk.

## Decision [​](#decision)

Move the implementation of `Entity`, `EntityCollection` and `Criteria` to the sdk. The corresponding files in the administration simply forward the default export of the sdk.

## Consequences [​](#consequences)

This will result in the same behaviour for current implementations. On the other hand, it provides the benefit of having these basic classes in an external package anybody can use.

---

## New templates for line items and nested line items

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-17-new-nested-line-items.html

# New templates for line items and nested line items [​](#new-templates-for-line-items-and-nested-line-items)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-17-new-nested-line-items.md)

## Context [​](#context)

In the storefront there are multiple templates, which display line items in different areas of the shop. Line items can be products, discounts, container items or custom line item types added by apps/extensions.

Currently, there are over ten different templates which are used to render line items in different situations. This current implementation has a few downsides we want to address with the next major version.

* Templates are sometimes written as independent templates, while copying over chunks of code from other line item templates.
* Sometimes the templates extend other line item templates instead.
* Inconsistent naming, templates are named `checkout-item` while the CSS-classes/markup inside the template itself is named `cart-item`
* Additional templates are needed to display nested line items.
* Nested line items only displayed as bullet points with text, not as "real" line items.
* Large templates files with many if-else conditions to distinguish between product, discount etc.

## Decision [​](#decision)

To address the issues mentioned above, we decided to refactor the different line item templates into a single line item base template: `Resources/views/storefront/component/line-item/line-item.html.twig`.

* All shop areas will be able to use the new template. The appearance (e.g. offcanvas) can be toggled via configuration variables.
* The naming will be changed to `line-item` for more consistency. A line item has not always to be inside a shopping cart.
* No more additional templates needed for children (nested line items), the base template includes itself recursively now.
* All known line item types (product, container, discount) get their own template to future-proof for more line item types and better readability.
* Less maintenance effort for extensions which may want to include custom line item types.

## Consequences [​](#consequences)

* All storefront line items in platform will use the new base template `Resources/views/storefront/component/line-item/line-item.html.twig`.
* The appearance of line items displayed inside the offcanvas will be unified with the mobile appearance of line items in the regular cart.
* If you are extending one if the line item templates listed below, you will need to use the line item base template `Resources/views/storefront/component/line-item/line-item.html.twig` instead.
  + `Resources/views/storefront/page/checkout/checkout-item.html.twig`
  + `Resources/views/storefront/page/checkout/checkout-item-children.html.twig`
  + `Resources/views/storefront/page/checkout/confirm/confirm-item.html.twig`
  + `Resources/views/storefront/page/checkout/finish/finish-item.html.twig`
  + `Resources/views/storefront/component/checkout/offcanvas-item.html.twig`
  + `Resources/views/storefront/component/checkout/offcanvas-item-children.html.twig`
  + `Resources/views/storefront/page/account/order/line-item.html.twig`
  + `Resources/views/storefront/page/account/order-history/order-detail-list-item.html.twig`
  + `Resources/views/storefront/page/account/order-history/order-detail-list-item-children.html.twig`
  + `Resources/views/storefront/page/checkout/checkout-aside-item.html.twig`
  + `Resources/views/storefront/page/checkout/checkout-aside-item-children.html.twig`

---

## Available stock improvements

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-available-stock.html

# Available stock improvements [​](#available-stock-improvements)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-available-stock.md)

Currently, the available stock calculation is performed on every update of a product. This is true if the product is updated via the API but also if it is ordered via the store api route. When an order is placed, this is triggered by `StockUpdater::lineItemWritten` and performs an update of the available stock by subtracting the stock with the quantity of open orders. If there are many open orders in the storage, this can lead to a bottleneck if many orders are executed at the same time, with the same products.

We have solved this problem by updating the available stock directly in the `CheckoutOrderPlaced` event with the ordered quantity:

php

```shiki
public function orderPlaced(CheckoutOrderPlacedEvent $event): void
{
    $ids = [];
    foreach ($event->getOrder()->getLineItems() as $lineItem) {
        if ($lineItem->getType() !== LineItem::PRODUCT_LINE_ITEM_TYPE) {
            continue;
        }

        if (!\array_key_exists($lineItem->getReferencedId(), $ids)) {
            $ids[$lineItem->getReferencedId()] = 0;
        }

        $ids[$lineItem->getReferencedId()] += $lineItem->getQuantity();
    }

    // order placed event is a high load event. Because of the high load, we simply reduce the quantity here instead of executing the high costs `update` function
    $query = new RetryableQuery(
        $this->connection,
        $this->connection->prepare('UPDATE product SET available_stock = available_stock - :quantity WHERE id = :id')
    );

    foreach ($ids as $id => $quantity) {
        $query->execute(['id' => Uuid::fromHexToBytes((string) $id), 'quantity' => $quantity]);
    }

    $this->updateAvailableFlag(\array_keys($ids), $event->getContext());
}
```

To prevent executing the `lineItemWritten` logic in addition to the `CheckoutOrderPlaced` logic, we set a context state within the `CartOrderRoute`, which we can then query in the event listener and skip the process:

php

```shiki
public function lineItemWritten(EntityWrittenEvent $event): void
{
    $ids = [];

    // we don't want to trigger to `update` method when we are inside the order process
    if ($event->getContext()->hasState('checkout-order-route')) {
        return;
    }
    
    //...
}
```

In addition to this optimization, we only perform a stock update if one of the three relevant fields (`stock`, `minPurchase`, `isCloseout`) has changed. This is checked in the `ProductIndexer` within the `update` method:

php

```shiki
$stocks = $event->getPrimaryKeysWithPropertyChange(ProductDefinition::ENTITY_NAME, ['stock', 'isCloseout', 'minPurchase']);
$this->stockUpdater->update($stocks, $event->getContext());
```

---

## Base sales channel context factory

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-base-context-factory.html

# Base sales channel context factory [​](#base-sales-channel-context-factory)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-base-context-factory.md)

Within each store api request (and storefront), the sales channel context must be built. Building the sales channel context is a very resource consuming task for the database, since many DAL objects are now included in the sales channel context. Therefore, a cache for the corresponding service (`Shopware\Core\System\SalesChannel\Context\SalesChannelContextFactory`) has already been implemented in the past: `Shopware\Core\System\SalesChannel\Context\CachedSalesChannelContextFactory`. However, since the context also contains the customer and the selected shipping address as well as billing address, the context cannot be cached once a customer is logged in:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\System\SalesChannel\Context;

class CachedSalesChannelContextFactory extends AbstractSalesChannelContextFactory
{
    public function create(string $token, string $salesChannelId, array $options = []): SalesChannelContext
    {
        if (!$this->isCacheable($options)) {
            return $this->getDecorated()->create($token, $salesChannelId, $options);
        }

        // ...
    }

    private function isCacheable(array $options): bool
    {
        return !isset($options[SalesChannelContextService::CUSTOMER_ID])
            && !isset($options[SalesChannelContextService::BILLING_ADDRESS_ID])
            && !isset($options[SalesChannelContextService::SHIPPING_ADDRESS_ID]);
    }
}
```

However, since there is also data in the context that is independent of a customer's data, it is possible to cache some of this resource-costing data across customers, even if the customer is logged in, has selected a different payment method, shipping method or address. For this we have implemented the `Shopware\Core\System\SalesChannel\Context\BaseSalesChannelContextFactory`, which is responsible for creating the `Shopware\Core\System\SalesChannel\BaseSalesChannelContext`. Only data that belongs to the sales channel or is independent of the customer account is loaded into the `BaseSalesChannelContext`:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\System\SalesChannel;

class BaseSalesChannelContext
{
    protected CustomerGroupEntity $currentCustomerGroup;

    protected CustomerGroupEntity $fallbackCustomerGroup;

    protected CurrencyEntity $currency;

    protected SalesChannelEntity $salesChannel;

    protected TaxCollection $taxRules;

    protected PaymentMethodEntity $paymentMethod;

    protected ShippingMethodEntity $shippingMethod;

    protected ShippingLocation $shippingLocation;

    protected Context $context;

    private CashRoundingConfig $itemRounding;

    private CashRoundingConfig $totalRounding;
}
```

The `BaseSalesChannelContextFactory` as well as the `BaseSalesChannelContext` are both marked as `@internal` and are not intended for extensions. Any intervention in the loading of the `BaseSalesChannelContext` can quickly lead to cache misses and is therefore not supported.

In addition to the corresponding `$salesChannelId`, the current session parameters are passed to the service, which contains a list of changed parameters. The `BaseSalesChannelContextFactory` takes into account the following parameters, which also have an effect on the corresponding cache permutation of the service:

* `shippingMethodId` - Contains the id of the selected shipping method.
* `paymentMethodId` - Contains the id of the selected payment method
* `countryId` - Contains the id of the selected shipping country
* `countryStateId` - Contains the id of the selected shipping state
* `currencyId` - Contains the id of the selected currency
* `languageId` - Contains the id of the selected language

In addition to the `Shopware\Core\System\SalesChannel\Context\BaseSalesChannelContextFactory` the `Shopware\Core\System\SalesChannel\Context\CachedBaseSalesChannelContextFactory` was implemented, which is responsible for caching the base context. It assembles the cache key based on the parameters listed above and loads the base context from the cache if it has already been loaded once.

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\System\SalesChannel\Context;

class CachedBaseSalesChannelContextFactory extends AbstractBaseSalesChannelContextFactory
{
    public function create(string $salesChannelId, array $options = []): BaseContext
    {
        ksort($options);

        $keys = \array_intersect_key($options, [
            SalesChannelContextService::CURRENCY_ID => true,
            SalesChannelContextService::LANGUAGE_ID => true,
            SalesChannelContextService::DOMAIN_ID => true,
            SalesChannelContextService::PAYMENT_METHOD_ID => true,
            SalesChannelContextService::SHIPPING_METHOD_ID => true,
            SalesChannelContextService::VERSION_ID => true,
            SalesChannelContextService::COUNTRY_ID => true,
            SalesChannelContextService::COUNTRY_STATE_ID => true,
        ]);

        $key = implode('-', [$name, md5(json_encode($keys, \JSON_THROW_ON_ERROR))]);
        
        //...
    }
}
```

So now the caching of the Sales Channel context is handled on two levels:

* `CachedSalesChannelContextFactory`: Is responsible for global caching and provides a fast hit rate and load time for customers who are not logged in.
* `CachedBaseSalesChannelContextFactory`: Is responsible for caching generic objects that do not relate to the customer account. Once a customer has created the context for another payment or shipping method, it will be shared with all logged-in users.

---

## Cache stampede protection

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-cache-stampede-protection.html

# Cache stampede protection [​](#cache-stampede-protection)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-cache-stampede-protection.md)

The Cache Stampede protection is a mechanism to prevent several users try to update this cache entry at the same time if a cache entry is no longer hot. This mechanism is very useful if there is a lot of load on the store and a cache entry is expired or invalidated. If there is no cache stampede protection on the system, and several users call a category listing at the same time, which is no longer in the cache, then all users would be let through to the database and the server could collapse under the load.

We have now integrated such a protection into all our services using the [`\Symfony\Contracts\Cache\CacheInterface` of symfony](https://symfony.com/blog/new-in-symfony-4-2-cache-stampede-protection). This mechanic is mainly used in our cached store api routes. Another positive side effect is that the code has become much more concise, since much is done within symfony:

## `CachedRuleLoader` before [​](#cachedruleloader-before)

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Cart;

use Psr\Log\LoggerInterface;
use Shopware\Core\Content\Rule\RuleCollection;
use Shopware\Core\Framework\Context;
use Symfony\Component\Cache\Adapter\TagAwareAdapterInterface;

class CachedRuleLoader extends AbstractRuleLoader
{
    public const CACHE_KEY = 'cart_rules';

    private AbstractRuleLoader $decorated;

    private TagAwareAdapterInterface $cache;

    private LoggerInterface $logger;

    public function __construct(AbstractRuleLoader $decorated, TagAwareAdapterInterface $cache, LoggerInterface $logger)
    {
        $this->decorated = $decorated;
        $this->cache = $cache;
        $this->logger = $logger;
    }

    public function getDecorated(): AbstractRuleLoader
    {
        return $this->decorated;
    }

    public function load(Context $context): RuleCollection
    {
        $item = $this->cache->getItem(self::CACHE_KEY);

        try {
            if ($item->isHit() && $item->get()) {
                $this->logger->info('cache-hit: ' . self::CACHE_KEY);

                return $item->get();
            }
        } catch (\Throwable $e) {
            $this->logger->error($e->getMessage());
        }

        $this->logger->info('cache-miss: ' . self::CACHE_KEY);

        $rules = $this->getDecorated()->load($context);

        $item->set($rules);
        $this->cache->save($item);

        return $rules;
    }
}
```

## `CachedRuleLoader` after [​](#cachedruleloader-after)

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Cart;

use Shopware\Core\Content\Rule\RuleCollection;
use Shopware\Core\Framework\Context;
use Symfony\Contracts\Cache\CacheInterface;

class CachedRuleLoader extends AbstractRuleLoader
{
    public const CACHE_KEY = 'cart_rules';

    private AbstractRuleLoader $decorated;

    private CacheInterface $cache;

    public function __construct(AbstractRuleLoader $decorated, CacheInterface $cache)
    {
        $this->decorated = $decorated;
        $this->cache = $cache;
    }

    public function getDecorated(): AbstractRuleLoader
    {
        return $this->decorated;
    }

    public function load(Context $context): RuleCollection
    {
        return $this->cache->get(self::CACHE_KEY, function () use ($context): RuleCollection {
            return $this->decorated->load($context);
        });
    }
}
```

However, since the service itself does not recognize whether it is a cache hit or miss, we have removed the corresponding logging.

---

## Initial state id loader

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-initial-state-id-loader.html

# Initial state id loader [​](#initial-state-id-loader)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-initial-state-id-loader.md)

During the performance optimizations, it was noticed that the determination of the initial state, for a state machine, is currently associated with a quite high database load, although only one ID must be determined. This has the consequence that during the checkout unnecessarily much load on the database is caused, in order to determine the initial state id, because this must be determined for the `order.state`, `order_delivery.state` as well as the `order_transaction.state` machine. Responsible for the load were the `\Shopware\Core\System\StateMachine\StateMachineRegistry::getInitialState` method, which is usually used as follows:

php

```shiki
$this->stateMachineRegistry->getInitialState(OrderStates::STATE_MACHINE, $context->getContext())->getId(),
//...
$this->stateMachineRegistry->getInitialState(OrderDeliveryStates::STATE_MACHINE, $context->getContext())->getId(),
//...
$this->stateMachineRegistry->getInitialState(OrderTransactionStates::STATE_MACHINE, $context->getContext())->getId(),
//...
```

Inside the `getInitialState`, the complete `StateMachine` object is loaded, including all `transitions` and their `from` and `to` states:

```shiki
$criteria = new Criteria();
$criteria
    ->addFilter(new EqualsFilter('state_machine.technicalName', $name))
    ->setLimit(1);

$criteria->getAssociation('transitions')
    ->addSorting(new FieldSorting('state_machine_transition.actionName'))
    ->addAssociation('fromStateMachineState')
    ->addAssociation('toStateMachineState');

$criteria->getAssociation('states')
    ->addSorting(new FieldSorting('state_machine_state.technicalName'));
```

Since this means unnecessary load for the database, we have `@deprecated` this method for `v6.5.0.0` and provided a new smaller and faster service. Furthermore, all usages in the core have been removed and replaced with the new service:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\System\StateMachine\Loader;

class InitialStateIdLoader implements ResetInterface
{
    public const CACHE_KEY = 'state-machine-initial-state-ids';

    public function get(string $name): string
    {
        if (isset($this->ids[$name])) {
            return $this->ids[$name];
        }

        $this->ids = $this->load();

        return $this->ids[$name];
    }

    private function load(): array
    {
        return $this->cache->get(self::CACHE_KEY, function () {
            return $this->connection->fetchAllKeyValue(
                'SELECT technical_name, LOWER(HEX(`initial_state_id`)) as initial_state_id FROM state_machine'
            );
        });
    }
}
```

With the help of this service we were able to reduce the determination of the initial state under load by a multiple. The cache shown here is invalidated by a DAL written event on the state\_machine entity.

---

## Prevent mail updates

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-prevent-mail-updates.html

# Prevent mail updates [​](#prevent-mail-updates)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-prevent-mail-updates.md)

In order to guarantee an autocompletion for the different mail templates in the administration UI, we currently have a mechanism, which writes the current mail into the database when sending a mail:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Content\Flow\Dispatching\Action;

class SendMailAction extends FlowAction
{
    public function handle(Event $event): void
    {
        // ...
        
        if ($data->has('templateId')) {
            $this->updateMailTemplateType($event, $mailEvent, $mailTemplate);
        }
        
        // ...
    }

    private function updateMailTemplateType(
        FlowEvent $event, 
        MailAware $mailAware, 
        MailTemplateEntity $mailTemplate
        ): void {
        if (!$mailTemplate->getMailTemplateTypeId()) {
            return;
        }

        if (!$this->updateMailTemplate) {
            return;
        }

        $this->mailTemplateTypeRepository->update([[
            'id' => $mailTemplate->getMailTemplateTypeId(),
            'templateData' => $this->getTemplateData($mailAware),
        ]], $mailAware->getContext());
    }
}
```

This allows us to also support plugin extensions out of the box. However, the disadvantage of this mechanism is a rather high load on the database when there are many orders and registrations in the store. It creates unnecessary load due to the mail templates in the database.

To avoid this load, we have implemented the configuration `shopware.mail.update_mail_variables_on_send`, which overrides this mechanism. We recommend, to set this configuration as soon as all mail templates in the store are configured correctly. You can simply set this configuration in your `config/packages/*.yaml` file:

yaml

```shiki
shopware:
    mail:
        update_mail_variables_on_send: false
```

This is only a temporary solution. We will create an alternative for this feature in the future, which will have no impact on the database due to high order numbers.

---

## Profiler integrations

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-profiler-integrations.html

# Profiler integrations [​](#profiler-integrations)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-profiler-integrations.md)

## Context [​](#context)

During the last performance benchmarks we have intensively dealt with profiling tools like Blackfire, Tideways and datadog. We often encountered the difficulty of getting detailed trace information when the server is under high load.

Tideways gave us very good monitoring tools, but in contrast to Blackfire it was difficult to detect bottlenecks by interpreting the timeline. We used Blackfire for single traces, but it turned out to be difficult to catch a "bad trace".

Therefore, we created a profiler integration, where we provide tools like Tideways or datadog with additional information, directly from our application. This will be triggered via a static method call, which can be used within the application. This profiler signals the integrations to create a span for the code that will be executed within a given closure:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Profiling;

use Shopware\Core\Profiling\Integration\ProfilerInterface;

/**
 * @internal experimental atm
 */
class Profiler
{
    /**
     * Profilers will be activated over the shopware.yaml file
     *
     * All enabled profilers will be added here
     *
     * @var ProfilerInterface[]
     */
    private static array $profilers = [];

    /**
     * Tags will be added to each trace
     *
     * @var string[]
     */
    private static array $tags = [];

    /**
     * @param string[] $activeProfilers
     */
    public function __construct(\Traversable $profilers, array $activeProfilers)
    {
        $profilers = iterator_to_array($profilers);
        self::$profilers = array_intersect_key($profilers, array_flip($activeProfilers));
        self::$tags = [];
    }

    /**
     * @return mixed
     */
    public static function trace(string $name, \Closure $closure, string $category = 'shopware', array $tags = [])
    {
        $pointer = static function () use ($closure) {
            return $closure();
        };

        $tags = array_merge(self::$tags, $tags);
        
        // we have to chain the profilers here: `return Stopwatch::trace(Tideways::trace(...));`
        foreach (self::$profilers as $profiler) {
            $pointer = static function () use ($profiler, $name, $pointer, $category, $tags) {
                return $profiler->trace($name, $pointer, $category, $tags);
            };
        }

        return $pointer();
    }

}
```

The corresponding calls of this profiler can be found everywhere in the application and can also be used in plugins:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Cart;

use Shopware\Core\Profiling\Profiler;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

class CartCalculator
{
    /**
     * @var CartRuleLoader
     */
    private $cartRuleLoader;

    public function __construct(CartRuleLoader $cartRuleLoader)
    {
        $this->cartRuleLoader = $cartRuleLoader;
    }

    public function calculate(Cart $cart, SalesChannelContext $context): Cart
    {
        return Profiler::trace('cart-calculation', function () use ($cart, $context) {
            // validate cart against the context rules
            return $this->cartRuleLoader
                ->loadByCart($context, $cart, new CartBehavior($context->getPermissions()))
                ->getCart();
        });
    }
}
```

These spans are then displayed in the timeline of the corresponding profilers: ![](/assets/tideways_benchmark.Dq_Mbr-t.png "Tideways benchmark")

Which profiler should be used in the system can be configured via `config/packages/*.yaml`:

yaml

```shiki
shopware:
    profiler:
        integrations: ['Symfony', 'Tideways', 'Datadog']
```

---

## Redis cart persister

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-25-redis-cart-persister.html

# Redis cart persister [​](#redis-cart-persister)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-25-redis-cart-persister.md)

With the last benchmarks it became clear how cost intensive the loading and saving of the shopping cart to and from the database is. A detailed analysis revealed two problems:

1. Every time the shopping cart is loaded, it is written back to the database after validation. However, this leads to a write on the connection which causes us to lose support for master-slave database setups.
2. To ensure the best possible performance, the shopping cart is written to the database as a serialized object. However, this in turn leads to rather high amounts of data having to be sent through the internal network.

To solve these problems, we implemented the `Shopware\Core\Checkout\Cart\RedisCartPersister`:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Cart;

class RedisCartPersister extends AbstractCartPersister
{
    /**
     * @var \Redis|\RedisCluster
     */
    private $redis;

    private EventDispatcherInterface $eventDispatcher;

    private bool $compress;

    public function load(string $token, SalesChannelContext $context): Cart {}

    public function save(Cart $cart, SalesChannelContext $context): void {}

    public function delete(string $token, SalesChannelContext $context): void {}

    public function replace(string $oldToken, string $newToken, SalesChannelContext $context): void {}
}
```

This stores the cart inside redis, which can be configured via the config in `config/packages/*.yaml`:

yaml

```shiki
shopware:
    cart:
        redis_url: 'redis://redis'
```

If no redis connection is configured, the redis cart persister is removed from the DI container. This is done inside the `\Shopware\Core\Checkout\DependencyInjection\CompilerPass\CartRedisCompilerPass`:

php

```shiki
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\DependencyInjection\CompilerPass;

class CartRedisCompilerPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        if (!$container->getParameter('shopware.cart.redis_url')) {
            $container->removeDefinition('shopware.cart.redis');
            $container->removeDefinition(RedisCartPersister::class);

            return;
        }

        $container->removeDefinition(CartPersister::class);
        $container->setAlias(CartPersister::class, RedisCartPersister::class);
    }
}
```

In addition, to reduce network traffic, we used cache compression, which significantly reduces the amount of data to be sent. However, the compression can be deactivated again via `config/packages/*.yaml`:

yaml

```shiki
shopware:
    cart:
        compress: false
```

**Notice:** Currently there is no migration path to transfer shopping carts from one storage to the other.

---

## Specify priority of translations in DAL write payloads

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-03-29-specify-priority-of-translations-in-dal-write-payloads.html

# Specify priority of translations in DAL write payloads [​](#specify-priority-of-translations-in-dal-write-payloads)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-03-29-specify-priority-of-translations-in-dal-write-payloads.md)

## Context [​](#context)

The DAL allows to write translated values in multiple ways:

* directly on the translated field
  + as a plain string (in the language of the current context)
  + as an array indexed either by language id or iso-code indicating the language of the value
* on the `translations` association as an indexed array

The current priority of those overwrites was accidental and never formally specified. This lead to unexpected behaviour in some cases.

## Decision [​](#decision)

We will formally specify the priority of those translations overwrites, so the DAL works as expected and developers can rely on that priority. In general we encourage to use `iso-codes` when writing translations for multiple languages at once. This has the following advantages:

* The payload itself is either to understand, and errors are easier to catch by just looking at the payload.
* The payload is compatible with multiple system (where the ids for each language will be different)

Besides that the common understanding when providing a translation value on the translated field itself, was that it should be treated as "default" value, and all values that are further specified in the associations should take precedence.

From those two observations we deduced the following rules for the priority of translation overwrites:

1. Translations indexed by `iso-code` take precedence over values indexed by `language-id`
2. Translations specified on the `translations`-association take precedence over values specified directly on the translated field.

**Note:** Rule 1 is more important than rule 2, therefore a translation value indexed by `iso-code` on the field directly, will overwrite a value in the `translations`-association, if that is indexed by `language-id`.

## Consequences [​](#consequences)

We will update the DAL to handle translation overwrites as specified above and will add test cases to ensure that our implementation adheres to this specification.

---

## Add default cms pages to products and categories

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-04-06-add-default-cms-layouts-to-products-and-categories.html

# Add default cms pages to products and categories [​](#add-default-cms-pages-to-products-and-categories)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-04-06-add-default-cms-layouts-to-products-and-categories.md)

## Context [​](#context)

We want to provide a way to set a default cms page.  
 Currently, if a product has no cms page assigned to it, there is a hardcoded fallback twig-template but no default. This does not apply to categories.

Products and categories should both get a default cms page if none is assigned which can be configured by the user.  
 The default should only be used when the corresponding entity is marked to use a default.

## Decision [​](#decision)

In order to implement this functionality, we needed a way to mark a product or category, which should use the default. This affects the following entities:

* category
  + `category.cmsPageId` will be set to null if the defined default is given,
  + this only applies to cms pages of type `product_list`
* product
  + `product.cmsPageId` will be set to null if the defined default `\Shopware\Core\Defaults::CMS_PRODUCT_DETAIL_PAGE` is given.

In order to set the default cms page, we simply provide the corresponding cms page id in the system config.

* `\Shopware\Core\Content\Product\ProductDefinition::CONFIG_KEY_DEFAULT_CMS_PAGE_PRODUCT` for the default cms page for products
* `\Shopware\Core\Content\Category\CategoryDefinition::CONFIG_KEY_DEFAULT_CMS_PAGE_CATEGORY` for the default cms page for categories of type `product_list`

This fallback is loaded at the `entity.loaded` event of the corresponding entity, where we check if the foreign key is set to NULL and inject the corresponding system config as default.

## Consequences [​](#consequences)

For all related entities, the `cmsPageId` will be set to `null` if the default is given. The corresponding cms page id will then be set by subscribers. Therefore, the cms page id, which is stored in the database, might differ from the cms page id which can be received via repository.  
 To use the default functionality, an entity must not have a cms page id assigned to it.

---

## Integrate an app into flow action

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-04-19-integrate-app-into-flow-action.html

# Integrate an app into flow action [​](#integrate-an-app-into-flow-action)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-04-19-integrate-app-into-flow-action.md)

We want to offer apps the possibility to deliver their own flow actions. Each app should be able to deliver multiple flow actions. The implementation should be done via webhooks and XML configuration. The information will be stored in the database as usual. If the app is uninstalled, all data will be deleted.

## Webhooks [​](#webhooks)

Actions within a flow are currently realized via the event system. If the user has configured certain flow actions for a flow trigger (a business event within Shopware, e.g. `CheckoutOrderPlaced`), an event is triggered in the background for each configured action. Each action defines a listener for this event, which then executes the corresponding logic. However, since apps cannot include PHP code, we want to give apps the ability to automatically call a configurable webhook in the background.

To identify these flow actions, we store an `app_id` at each `flow_sequence` record in the database. In the `FlowExecutor`, we can thus identify that it is a flow action and automatically call the corresponding webhook for that app.

## Configuration [​](#configuration)

For flow actions, configuration parameters may be necessary that can be stored individually for each action. This should also be possible for apps. The flow actions are configured in a new `Resources/flow-action.xml` file. The following information can be stored for a flow action:

1. `<meta>` - Meta information for identification and UI.
2. `<headers>` - header information for the webhook
3. `<parameters>` - parameter information for the webhook
4. `<config>` - configuration information for the admin UI

A complete XML structure looks like this:

xml

```shiki
<flow-actions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://test-flow.com/flow-action-1.0.xsd">
    <flow-action>
        <meta>
            <name>telegram.send.message</name>
            <badge>Telegram</badge>
            <label>Telegram send message</label>
            <description>Telegram send message description</description>
            <url>https://test-flow.com</url>
            <sw-icon>default-communication-speech-bubbles</sw-icon>
            <requirements>orderAware</requirements>
        </meta>
        <headers>
            <parameter type="string" name="content-type" value="application/json"/>
        </headers>
        <parameters>
            <parameter type="string" name="message" value="{{ subject }} \n {{ customer.lastName }} some text here"/>
        </parameters>
        <config>
            <input-field type="text">
                <name>subject</name>
                <label>Subject</label>
                <required>true</required>
            </input-field>
        </config>
    </flow-action>
</flow-actions>
```

---

## Introducing tax providers

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-04-28-tax-providers.html

# Introducing tax providers [​](#introducing-tax-providers)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-04-28-tax-providers.md)

## Context [​](#context)

In other countries like the USA, there are different tax rates for different states and counties you are shipping to, leading to thousands of different tax rates in the USA alone. For this purpose, *tax providers* exist like `TaxJar`, `Vertex` or `AvaTax` that output the tax rate depending on the customer and cart details.

## Decision [​](#decision)

We want to implement a possibility (interface / hook), which is called after the cart is calculated and is able to overwrite the taxes. Then, when a customer is logged in (therefore information about the shipping / billing is available), we can call the interface to receive all necessary information about the tax rates.

## Implementation details [​](#implementation-details)

### New entity `tax_provider` [​](#new-entity-tax-provider)

We want to create a new entity called `tax_provider` which registers the available tax providers and defines rules.

The following fields should therefore be required:

* IdField `id`
* TranslatedField `name`
* IntField `priority` (default 1)
* FkField `availabilityRuleId`
* StringField `providerIdentifier` (unique)
* TranslatedField `customFields`

### Location and prioritization of *tax providers* [​](#location-and-prioritization-of-tax-providers)

The `TaxProviderProcessor` is called in the `CartRuleLoader`, after the whole cart has been calculated (so all the promotions and deliveries are calculated). Therefore, if any rules may change due to the changed taxes (e.g. gross price), they will not be validated anymore.

The *tax provider* will only be called, if:

* A customer is logged in
* The availability rule matches

The highest priority defines, which *tax provider* is called first. If no parameter is filled or the `TaxProviderNotAvailableException` is thrown, the next *tax provider* by priority is called.

### Calling the *tax provider* [​](#calling-the-tax-provider)

The `TaxProviderProcessor` will call a class that is tagged `shopware.tax.provider`, named in the `providerIdentifier` and implements the `TaxProviderInterface`. If the class does not exist, the Processor will throw a `TaxProviderHook`, that has the identifier and the return struct as additional parameters, so it can be filled via app scripting, if the identifier matches with the app. To allow for app scripting to call the provider, we need to add a possibility to do requests to the app, e.g. via Guzzle.

php

```shiki
interface TaxProviderInterface
{
    /**
     * @throws TaxProviderOutOfScopeException|\Throwable
     */
    public function provideTax(Cart $cart, SalesChannelContext $context): TaxProviderStruct;
}
```

If a *tax provider* throws any other Exception than the `TaxProviderOutOfScopeException` (e.g. due to connection issues), we proceed to the next tax provider. If no other provider can provide taxes, we will throw the first Exception since we then don't want any invalid taxes.

### Return & Processing [​](#return-processing)

If any of the values of the TaxProviderStruct is filled by the class / hook, we do not call any more TaxProviders. Afterwards, the line items / shipping costs / total tax are respectively overwritten, before the cart is persisted.

php

```shiki
class TaxProviderStruct extends Struct 
{
    /**
     * @param null|array<string, CalculatedTaxCollection> key is line item id
     */
    protected ?array $lineItemTaxes = null;

    /**
     * @param null|array<string, CalculatedTaxCollection> key is delivery id
     */
    protected ?array $deliveryTaxes = null;

    protected ?CalculatedTaxCollection $cartPriceTaxes = null;
}
```

---

## Remove static analysis with psalm

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-05-12-remove-static-analysis-with-psalm.html

# Remove static analysis with psalm [​](#remove-static-analysis-with-psalm)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-05-12-remove-static-analysis-with-psalm.md)

## Context [​](#context)

Currently, we are running static analysis over the php code with both `phpstan` and `psalm`. This slows down our pipeline and may lead to weird effects where `phpstan` and `psalm` report errors that are incompatible with each other.

## Decision [​](#decision)

There is not much need anymore to run both tools, as they pretty much converged to a common feature set. This was different when we started with shopware 6 where both tools had some different features, but most of the differences are gone by now. Therefore, we won't run both tools anymore in the CI.

We decided to stick with `phpstan` and remove `psalm` because:

* It's easier to write custom `phpstan` rules than to extend `psalm`
* We already have custom `phpstan` rules
* There are more extension for `phpstan`, e.g. for `symfony` or `phpunit`

## Consequences [​](#consequences)

`psalm` will be completely removed from the repository and the CI.

---

## Rule condition field abstraction

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-05-23-rule-condition-field-abstraction.html

# Rule condition field abstraction [​](#rule-condition-field-abstraction)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-05-23-rule-condition-field-abstraction.md)

## Context [​](#context)

Conditions for the Rule Builder consist of a `shopware.rule.definition` tagged service and a corresponding Vue component. Many of these Vue components follow a common scheme, so it is possible to use an abstracted single component for all of these.

## Decision [​](#decision)

We want to reduce the number of rule condition components in the administration and use a single abstracted component instead. This would also decrease the number of necessary steps when introducing a new rule condition and would require writing less JavaScript.

Conditions will still be able to register and use their own custom components, as it used to be, in cases where the needed functionality is beyond the capabilities of the generic abstracted component.

To make use of the generic abstracted component, rule conditions, whose component may be abstracted, may implement a new method `getConfig` and return an instance of `RuleConfig`. Via `RuleConfig` the appropriate set of operators and a number of corresponding fields can be defined:

php

```shiki
public function getConfig(): RuleConfig
{
    return (new RuleConfig())
        ->operatorSet(RuleConfig::OPERATOR_SET_STRING, false, true)
        ->entitySelectField('customerGroupIds', CustomerGroupDefinition::ENTITY_NAME, true)
        ->selectField('customSelect', ['foo', 'bar', 'baz'])
        ->numberField('amount', ['unit' => RuleConfig::UNIT_DIMENSION])
        ->booleanField('active')
        ->dateTimeField('creationDate');
}
```

Within the administration, the configurations for the different types of conditions are being requested and stored. The new generic condition component then makes use of the configurations to render the various fields.

## Consequences [​](#consequences)

Starting from now, newly introduced rule conditions will make use of the `Rule::getConfig()` implementation whenever possible and hence no longer require a new Vue component. If the new condition cannot be abstracted, as it may need special functionality within the administration, it may still introduce its own custom component.

The original components of conditions are being deprecated and marked to be removed by the next major release.

If you used or extended any of these components, use/extend `sw-condition-generic` or `sw-condition-generic-line-item` instead and refer to `this.condition.type` to introduce changes for a specific type of condition.

---

## Integrate an app into the flow event

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-06-17-integrate-app-into-flow-event.html

# Integrate an app into the flow event [​](#integrate-an-app-into-the-flow-event)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-06-17-integrate-app-into-flow-event.md)

# 2022-10-11 - Integrate an app into the flow event [​](#_2022-10-11-integrate-an-app-into-the-flow-event)

## Context [​](#context)

Currently, apps can not extend the list of available events in the flow builder.

## Decision [​](#decision)

We update the flow builder so the apps can expand the list of available trigger events in the flow builder UI.

### Flow aware [​](#flow-aware)

We define flow aware classes to detect which data will be available in the event and a function to get them.

**Problems:**

* We are unsure which data will the app event provide

**Solution:**

* We create an interface CustomAppAware that will use as implementation for the custom event from the app.

**Example pseudocode**

php

```shiki
interface CustomAppAware
{
    public const APP_DATA = 'customAppData';

    public function getCustomAppData(): array;
}
```

### Flow storer [​](#flow-storer)

Flow data storer saves the data from the event as the [StorableFlow](./../adr/2022-07-21-adding-the-storable-flow-to-implement-delay-action-in-flow-builder.html), and we use them in flow actions.

**Problems:**

* Currently, we keep the event data in the core but do not store any personalized event data from the application.

**Solution:**

* We create a CustomAppStorer, which is used to store the data from custom app event.
* When the API triggers a custom trigger, the data in the body will be stored in FlowStore by their keys.

*Example to define data from the API:*

json

```shiki
    {
        "customerId": "d20e4d60e35e4afdb795c767eee08fec",
        "salesChannelId": "55cb094fd1794d489c63975a6b4b5b90",
        "shopName": "Shopware's Shop",
        "url": "https://shopware.com" 
    }
```

*After that, at actions we can get data thought FlowStorer.*

php

```shiki
    $salesChanelId = $flow->getData(MailAware::SALES_CHANNEL_ID));
    $customer = $flow->getData(CustomerAware::CUSTOMER_ID));
```

*Or we can use the data when defining the email template.*

html

```shiki
    <h3>Welcome to {{ shopName }}</h3>
    <h1>Visit us at: {{ url }} </h1>
```

**Example pseudocode**

php

```shiki
class CustomAppStore extends FlowStorer
{
    public function store(FlowEventAware $event, array $stored): array
    {
        //check if $event is an instance of CustomAppAware
        foreach ($event->getCustomAppData() as $key => $data) {
            $stored[ScalarValuesAware::STORE_VALUES][$key] = $data;
            $stored[$key] = $data;
        }
    }

    public function restore(StorableFlow $storable): void
    {
        return;
    }
}
```

### Flow Events [​](#flow-events)

Events must implement FlowEventAware to be able to available in the flow builder triggers.

**Problems:**

* We do not possess any `FlowEventAware` event instances that app developers can utilize for custom triggers to be dispatched or triggered from an app.

**Solution:**

* We create a new CustomAppEvent class that can be triggered by the App system.

**Example pseudocode**

php

```shiki
class CustomAppEvent extends Event implements CustomAppAware, FlowEventAware
{
    private string $name;

    private array $data;
    
    // __construct()
    //getters
}
```

### BusinessEventCollector [​](#businesseventcollector)

BusinessEventCollector collects events that implemented FlowEventAware and output to flow builder.

**Problems:**

* We currently collect events that implemented FlowEventAware. So the collector does not contain the events from the activated app.

**Solution:**

* We will collect all `CustomAppEvent` events from activated apps.

**Example pseudocode**

php

```shiki
public function collect(Context $context): BusinessEventCollectorResponse
{
    //fetch app event
    $this->fetchAppEvents(new BusinessEventCollectorResponse)
}

private function fetchAppEvents(BusinessEventCollectorResponse $result): BusinessEventCollectorResponse
{
    //check valid app events from the database
    return $this->createCustomAppEvent();
}

private function createCustomAppEvent(): CustomAppEvent
{
   // return new CustomAppEvent
}
```

### Trigger app custom events API [​](#trigger-app-custom-events-api)

We will provide an APIs to trigger CustomAppEvent.

**Problems:**

* Currently, the events are provided and triggered from the core when the user performs specific actions from the storefront or admin, like checkout order or user recovery. 3rd parties can not add custom triggers and trigger them by themself.

**Solution:**

* We will provide an API. The app calls the API to trigger the custom event and needs to provide the event name and the data. The API will create a CustomAppEvent object and dispatch it with the information provided.

**Example pseudocode**

php

```shiki
    /**
     * @Since("6.5.2.0")
     */
    #[Route(path: '/api/_action/trigger-event/{eventName}', name: 'api.action.trigger_event', methods: ['POST'])]
    public function flowCustomTrigger(string $eventName, Request $request, Context $context): JsonResponse
    {
        $data = $request->request->all();
        
        $criteria = new Criteria([$data['flowAppEventId']])
        $criteria->addFilter(new EqualsFilter('appId', $data['flowId']));
        $criteria->addFilter(new EqualsFilter('app.active', 1));

        $flowEvent = $flowAppEventRepository->search($criteria);
        //return http status code 404 if $flowEvent is empty
        
        $this->eventDispatcher->dispatch(new CustomAppEvent($flowEvent->getName(), $data));
        //return http status code 200 and success message
    }
```

## Defining an App flow event in Xml [​](#defining-an-app-flow-event-in-xml)

The flow events are configured in a `<appRoot>/src/Resources/flow.xml` file. We can store the following information for a flow event, Also, we can define more than one event in one app:

1. `<name>` - The technical name - is unique and should be prefixed with the app vendor prefix, used when dispatching CustomAppEvent.php.
2. `<aware>` - Use for deciding what flow actions will be allowed to show after the event.

   * The list of aware supported following:

     + `orderAware`
     + `customerAware`
     + `mailAware`
     + `userAware`
     + `salesChannelAware`
     + `productAware`
     + `customerGroupAware`
   * *Example:*

   *`<aware>orderAware</aware>`*

   *We will have a list of actions related to Order that can be selected at the flow below:*

   * action.add.order.tag,
   * action.remove.order.tag,
   * action.generate.document,
   * action.grant.download.access,
   * action.set.order.state,
   * action.add.order.affiliate.and.campaign.code,
   * action.set.order.custom.field,
   * action.stop.flow

   *`<aware>customerAware</aware>`*

   *We will have a list of actions related to Customer that can be selected at the flow below:*

   * action.add.customer.tag
   * action.remove.customer.tag
   * action.change.customer.group
   * action.change.customer.status
   * action.set.customer.custom.field
   * action.add.customer.affiliate.and.campaign.code
   * action.stop.flow

A complete XML structure looks like this:

xml

```shiki
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://test-flow.com/flow-1.0.xsd">
    <flow-events>
        <flow-event>
            <name>swag.before.open.the.doors</name>
            <aware>customerAware</aware>
            <aware>orderAware</aware>
        </flow-event>
        <flow-event>
            ...
        </flow-event>
    </flow-events>
</flow-extensions>
```

## Defining translated [​](#defining-translated)

We support defining translation for custom trigger events to show in the trigger tree and the trigger's name in the flow list.

* We will create the snippet file in folder `<appRoot>/src/Resources/app/administration/snippet/`. The structure of the snippet should follow some principles below:
  + `sw-flow-custom-event` is a fixed key instance for snippets using at the trigger event.
  + `event-tree` is a fixed key. The keys are defined inside this key based on the specified trigger name at `name` in `flow.xml` used to translate in trigger tree.
  + `flow-list` is a fixed key, The keys defined inside the key based on the trigger name defined at `name` in `flow.xml` used to translate in the trigger tree. **Example pseudocode**

    json

    ```shiki
    {
    "sw-flow-custom-event": {
      "event-tree": {
        "swag": "Swag",
        "before": "Before",
        "openTheDoors": "Open the doors"
      },
      "flow-list": {
        "swag_before_open_the_doors": "Before open the doors"
      }
    }
    ```

}

```shiki
## Database migration
* We will create a new table `app_flow_event` to save defined data from the `<appRoot>/src/Resources/flow.xml` file.
* The table will have columns like bellow:
  * `id` BINARY(16) NOT NULL,
  * `app_id` BINARY(16) NOT NULL,
  * `name` VARCHAR(255) NOT NULL UNIQUE,
  * `aware` JSON NOT NULL,
  * `created_at` DATETIME(3) NOT NULL,
  * `updated_at` DATETIME(3) NULL,
```

---

## Add typescript support for storefront javascript

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-06-24-add-typescript-support-for-storefront-js.html

# Add typescript support for storefront javascript [​](#add-typescript-support-for-storefront-javascript)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-06-24-add-typescript-support-for-storefront-js.md)

## Context [​](#context)

* We want to add TypeScript support to the Storefront, to make use of all of it's features increasing the overall developer experience, quality and maintainability.
* The main concern is the compatibility to existing Storefront plugins, which have been built in previous versions without TypeScript support.
* TypeScript files need to be compatible with JavaScript files and vice versa, for both the Storefront internally, and also for plugins.

## Decision [​](#decision)

* To prevent any breaks in our current Storefront stack, we will add TypeScript language support to the current babel chain, using the preset `@babel/preset-typescript`.
* To prevent any breaks for existing Storefront plugins, we won't replace any publicly used .js files with .ts files, without proper deprecation.

## Consequences [​](#consequences)

* TypeScript (.ts and .tsx) files are now supported by the Storefront.
* Storefront plugins can now be developed using TypeScript and the actual Storefront JavaScript can be incrementally converted to .ts files from now on.
* TypeScript files and JavaScript files are compatible and can be imported to each other.

---

## Providing the admin extension SDK

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-06-27-providing-the-admin-extension-sdk.html

# Providing the admin extension SDK [​](#providing-the-admin-extension-sdk)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-06-27-providing-the-admin-extension-sdk.md)

WARNING

The Admin Extension SDK has been renamed to Meteor Extension SDK.

## Context [​](#context)

The Admin Extension SDK is a toolkit for plugin and app developers to extend or modify the administration via their plugins or apps. The SDK contains easy to use methods which interact with the administration in the background via the PostMessage API for iFrames.

## Decision [​](#decision)

We created the SDK in a separate repository on GitHub instead of creating it in the platform repository. This decision has several reasons.

### Faster development [​](#faster-development)

The main reason for the separate repository is the development speed. We can develop much faster. The whole, large pipeline does not need to run for small changes. Also the pipeline for the SDK runs extremely fast and provides all necessary features like testing, creating of the documentation and many more things. The experiences we made in the past showed that working with SDK works very flawless, fast and agile.

### Independent deployment [​](#independent-deployment)

The SDK is not hard-bound to Shopware version like plugins. This dependency will be included directly in the apps and also supports newer Shopware versions. This allows us to provide separate releases independent of the administration. Example: A small bug can be fixed and released in minutes. A similar deployment in the platform would take much more time.

### SDK is just a convenience layer for the PostMessage API [​](#sdk-is-just-a-convenience-layer-for-the-postmessage-api)

Similar as the previous reason the SDK is not hard-bound to the Shopware releases and is a completely separate package. And if we would add it into the monorepo we would be bound to the Shopware release cyclus. With a separate repository we can work independent and react faster.

### Independent documentation [​](#independent-documentation)

Documentation has a really high priority for the SDK. Everything should be documented very well. To make sure that nothing gets merged without documentation we include the documentation in the same repository. Then we can directly see if documentation was written and if not, we wouldn't merge the feature.

### PHP monorepo mixed with JS packages is difficult [​](#php-monorepo-mixed-with-js-packages-is-difficult)

The behavior of JS and PHP monorepos is different. Things like nested packages should be avoided in the context of JS. The current platform structure doesn't match the structure of JS monorepos. For example the plugin folder, the component library inside the administration package, etc... This structure leads to difficulties in build systems, dependency resolution behavior (e.g. even if a dependency is not defined in the package.json in can be loaded because it looks traversal for a node\_modules folder which can lead to different dependency versions which than can lead to further problems. This already happened in the past in the current component library.) To avoid all these problems at the first place we created a separate repository.

### No need for a monorepo management tool like Lerna [​](#no-need-for-a-monorepo-management-tool-like-lerna)

Managing monorepos is not that simple for most developers. We had the experience in the past with Lerna as a monorepo tool. The dependency resolution between packages was not that trivial (also because of the folder structure). This led to broken package-lock files, not working npm installs and many more problems. You need to know how this tooling works to modify things in the separate packages. Even if it is now easier with Yarn or other tools it is still unnecessary complicated. Working with multi repositories is in this case less error prone. You just do the change in the repository and bump up the version in the package.json. And if you also need the new changes in a different place, then you also need to bump up the dependency version. No magic tooling required for this.

### Monorepo has no real advantage in the SDK case and would make things just more complicated [​](#monorepo-has-no-real-advantage-in-the-sdk-case-and-would-make-things-just-more-complicated)

Monorepos have several advantages over multi repos. But in the case of the SDK almost none of these advantages comes to fruition. Things like deployment, separate testing, documentation, independent versions and many more things would be much more difficult.

## Consequences [​](#consequences)

If you want to add something to the SDK you need to checkout the GitHub repository and publish the changes to this repository. If the change is also relevant for the administration side - then this version also needs to be bumped up there.

---

## Concept for blogs using Shopping Experiences

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-07-19-blog-concept.html

# Concept for blogs using Shopping Experiences [​](#concept-for-blogs-using-shopping-experiences)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-07-19-blog-concept.md)

## Context [​](#context)

A highly requested feature & expected for the CMS of Shopware 6 is the blog. In addition, this is an ideal use case and example for the use of [Custom Entities](./../adr/2021-09-14-technical-concept-custom-entities.html).

## Decision [​](#decision)

We want to implement blogs as part of the CMS. Since Custom Entities offers a good chance to implement such a feature, the blog is supposed to show the community how to handle Custom Entities in the Shopping Experiences. Therefore, we decided on the following:

### Blog posts & Content types [​](#blog-posts-content-types)

Multiple types of content should be available in the future for our CMS and be directly accessible in the Content section of the administration. Using `admin-ui` as a flag in its specific xml file, Shopware will create a listing and a detail page into the Content section automatically for types of content (Custom Entities). In addition, the `cms-aware` flag also will bring some pre-defined fields, used as defaults in the CMS elements, to our entity. Those are always prefixed with `sw_` to avoid duplicates by the user:

* `sw_title`
* `sw_content`
* `sw_media_id`
* `sw_cms_page_id`
* `sw_cms_page_version_id`
* `sw_seo_meta_title`
* `sw_seo_meta_description`
* `sw_seo_keywords`

To keep everything tidy, we decided to implement using two different files `admin-ui.xml` and `cms-aware.xml` and keep a distinct separation of schema and UI. This flag will also result in new component types, so that for example the `cms-aware` property's `sw_cms_page_id` can be rendered as a CMS page selection, like known from the categories.

![Category menu with Content types](/assets/example-cms-aware-admin-menu.CU7QkDNc.png)

#### Example `admin-ui.xml` [​](#example-admin-ui-xml)

xml

```shiki
<admin-ui>
    <entity name="custom_entity_example"
            navigation-parent="sw-content"
            position="50"
            icon="regular-tools-alt"
            color="#f00">
        <listing>
            <columns>
                <column ref="name"/>
                <column ref="my_description"/>
                <column ref="position" hidden="true" />
                <column ref="rating"/>
            </columns>
        </listing>
        <detail>
            <tabs>
                <tab name="main">
                    <card name="general">
                        <field ref="name"/>
                        <field ref="position"/>
                        <field ref="rating"/>
                    </card>
                    <card name="cardClone">
                        <field ref="name"/>
                        <field ref="my_description"/>
                    </card>
                </tab>
                <tab name="tabClone">
                    <card name="generalSecond">
                        <field ref="name"/>
                        <field ref="position"/>
                        <field ref="rating"/>
                    </card>
                    <card name="cardClone">
                        <field ref="name"/>
                        <field ref="my_description"/>
                    </card>
                </tab>
                <!-- cms-aware tabs will always be rendered last, if defined -->
            </tabs>
        </detail>
    </entity>
    <entity name="custom_entity_example_second"
            navigation-parent="sw-content"
            position="50"
            icon="regular-tools-alt"
            color="#f00">
        <!-- Like above -->
    </entity>
</admin-ui>
```

#### Example `cms-aware.xml` [​](#example-cms-aware-xml)

xml

```shiki
<?xml version="1.0" encoding="utf-8" ?>
<cms-aware xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:noNamespaceSchemaLocation="../../../../../../../../src/Core/System/CustomEntity/Xml/Config/CmsAware/cms-aware-1.0.xsd">
    <entity name="custom_entity_example"/>
    <entity name="custom_entity_example_second"/>
</cms-aware>
```

### Category type as blogs [​](#category-type-as-blogs)

A blog is defined as a collection of blog posts, some additional metadata, SEO data and an associated CMS page. With this in mind, we decided upon using categories and create a new type `blog` for those, since the category itself has everything we need for a blog feature, even in terms of UI. The only change would be to replace assigned products with assigned posts, or custom entity entries when speaking generally. The CMS page template assigned to the category will contain a post listing.

With content types in mind, this will be an additional step to be auto generated via the `cms-aware` flag of Custom Entities.

### Basic blog structure [​](#basic-blog-structure)

### Snippet structure [​](#snippet-structure)

Modules generated via `admin-ui.xml` are automatically referring to the following snippet structure:

json

```shiki
{
   "custom_entity_bundle": {
       "moduleTitle": "Blog posts",
       "moduleDescription": "Blog is colorful and has pics",
       "tabs": {
           "main": "Main settings",
           "tabClone": "Optional stuff"
       },
       "cards": {
           "general": "General stuff",
           "cardClone": "Just a clone",
           "generalSecond": "More general stuff"
       },
       "fields": {
           "swTitle": "Title",
           "swContent": "Product description",
           "swContentHelpText": "Help text!",
           "swContentPlaceholder": "Enter description...",
           "position": "Positioning"
       }
   }
}
```

---

## Adding the `StorableFlow` instead of the `FlowEvent` for implementing the flow DelayAction in flow builder

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-07-21-adding-the-storable-flow-to-implement-delay-action-in-flow-builder.html

# Adding the `StorableFlow` instead of the `FlowEvent` for implementing the flow DelayAction in flow builder [​](#adding-the-storableflow-instead-of-the-flowevent-for-implementing-the-flow-delayaction-in-flow-builder)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-07-21-adding-the-storable-flow-to-implement-delay-action-in-flow-builder.md)

## Context [​](#context)

The actions in Flow Builder are listening for Business Events. We want to implement the flow DelayAction in Flow Builder, that means the actions can be delayed, and will be executed after a set amount of time. But we have some problems after the action was delayed:

* Events may contain old data, that data may be updated during the delay, and currently we don't have any way to restore the data.
* After a delay the rules have to be re-evaluated, but the data in the rules could be outdated or changed, so the rules have to be reloaded as well. Or the rules do not exist anymore.

## Decision [​](#decision)

We would need to detach the Event System and the Flow System from each other, thus removing the dependency on the runtime objects within an event. Meaning the Actions must not have access to the original Events.

We would create a class `StorableFlow`, that can store the data in the original event as scalar values, and restore the original data based on this stored data.

php

```shiki
class StorableFlow
{
    // contains the scalar values based on the original events
    // $store can be serialized and used to restore the object data
    protected array $store = [];
    
    // contains the restored object data like the data we defined in the `availableData` in original events 
    // $data can not be serialized, but can be restored from $store
    protected array $data = [];
      
    public function __construct(array $store = [], array $data = [])
    {
        $this->store = $store;
        $this->data = $data;
    }
    
    // This method will be called in each `Storer` to store the representation of data
    public function setStore(string $key, $value) {
        $this->store[$key] = $value;
    }
    
    public function getStore(string $key) {
        return $this->store[$key];
    }
    
    // After we restored the data in `Storer`, we can set the data, we'll use `$this->data` instead getter data on original event
    public function setData(string $key, $value) {
        $this->data[$key] = $value;
    }
    
    public function getData(string $key) {
        return $this->data[$key];
    }
}
```

The `StorableFlow` class will be use on Flow Builder:

Before:

php

```shiki
class FlowDispatcher 
{
    public function dispatch(Event $event) {
        ...
        // Currently, dispatch on Flow Builder use the original event to execute the Flow 
        $this->callFlowExecutor($event);
        ...
    }
}
```

After:

php

```shiki
class FlowDispatcher 
{
    public function dispatch(Event $event) {
        ...
        // The `FlowFactory` will create/restore the `StorableFlow` from original event
        $flow = $this->flowFactory->create($event);
        // use the `StorableFlow` to execute the flow builder actions instead of the original events
        $this->execute($flow);
        ...
    }
}
```

* Flow Builder actions may no longer access the original event.
* Each Aware Interface gets its own `Storer` class to restore the data of Aware, so we have many `Storer` like `OrderStorer`, `MailStorer`, `CustomerStorer` ...
* The main task of a `Storer` is to restore the data from a scalar storage.
* The `Storer` provides a store function, in order to store itself the data, in order restore the object
* The `Storer` provides a restore function to restore the object using the store data.

php

```shiki
interface FlowStorer {}
```

Example for `OrderStorer`:

php

```shiki
class OrderStorer implements FlowStorer
{
    // This function to check the original event is the instanceof Aware interface, and store the representation.
    public function store(FlowEventAware $event, array $storedData): array 
    {
        if ($event instanceof OrderAware) {
            $storedData['orderId'] = $event->getOrderId();
        }
        
        return $storedData;
    }
    
    // This function is restore the data based on representation in `storedData`
    public function restore(StorableFlow $flow): void
    {
        if ($flow->hasStore('orderId')) {
            // allows to provide a closure for lazy data loading
            // this opens the opportunity to have lazy loading for big data
            // When we load the entity, we need to add the necessary associations for each entity
            $flow->lazy('order', [$this, 'load']);    
        }
        ...
    }
}
```

About the additional data defined in `availableData` in original events, that aren't defined in any Aware Interfaces and we can't restore that data in the `Storer`. To cover the additional data from original events, we will have another `store` `AdditionalStorer` to store those data.

php

```shiki
class AdditionalStorer extends FlowStorer
{
    public function store(FlowEventAware $event, array $storedData)
    {
        ...
        // based on the `getAvailableData` in the original event to get the type of additional data
        $additionalDataTypes = $event::getAvailableData()->toArray();
        
        foreach ($additionalDataTypes as $key => $eventData) {
            // Check if the type of data is Entity or EntityCollection
            // in the $storedData, we only store the presentation like ['id' => id, 'entity' => entity], we'll restore the data in `AdditionalStorer::restore`
            if ($eventData['type'] === 'Entity' || 'EntityCollection') {
                $storedData[$key] = [
                    'id' => $event->getId(),
                    'entity' => Entity                 
                ];
            }
            
            // Check if the type of data is ScalarValueType
            if ($eventData['type'] === ScalarValueType) {
                $storedData[$key] = value
            }
            
            // start to implement /Serializable for ObjectType
            if ($eventData['type'] === ObjectType) {
                $storedData[$key] = value->serialize()
            }
            
            ...
        }
        
        ... 
        
        return $storedData;
    }
      
    // this function  make sure we can restore the additional data from original data are not covered in `Storer`
    // The additional data can be other entity, because the entities we defined in Aware interface like `order`, `customer` ... covered be `Storer`
    public function restore(StorableFlow $flow): void
    {
        if (type === entity) {
            // About the associations for entity data, mostly the additional entity data is the base entity, we don't need to add associations for this
            $flow->setData($key, $this->load());
        } else {
            $flow->setData($key, $flow->getStore($key));
        }
        ...
    }
}
```

About the associations for entity data, mostly the additional entity data is the base entity, we don't need to add associations for this. About the `ObjectType` data, we enforce all values used in ObjectType implement /Serializable, and serialize the object before store to `$storedData`.

* Flow Builder actions only work with the `StorableFlow` instead of the `FlowEvent`. The `StorableFlow` will restore the data from original events via `Storer`, and the Actions can get the data via `getData($key)` from `StorableFlow` instead of `getAvailableData` from original events.

Before, in the flow actions still dependency Aware interfaces:

php

```shiki
    public function handle(StorableFlow $event) {
        ...
        $baseEvent = $event->getEvent();
    
        if ($baseEvent instanceof CustomerAware) {
            $customerId= $baseEvent->getCustomerId();
        }
        ...
    }
```

After in the flow actions:

php

```shiki
    public function handle(StorableFlow $event) {
        ...
        if ($event->hasStore('customerId') {
            $customerId= $event->getStore('customerId');
        }
        ...
    }
```

* `getAvailableData` must NOT be responsible for the access of the data.
* To create new or restore the `StorableFlow` by on the existing stored data, we need to provider the `FlowFactory`.

php

```shiki
class FlowFactory
{    
    ...
    public function create(FlowEventAware $event)
    {
        $storedData = [];
        foreach ($this->storer as $storer) {
            // Storer are responsible to move the corresponding 
            // data from the original event 
            $storer->store($event, $storedData);
        }
        
        return $this->restore($storedData);
    }
  
    public function restore(array $stored = [], array $data = [])
    {
        $flow = new StorableFlow($stored, $data);
      
        foreach ($this->storer as $storer) {
            $storer->restore($flow);
        }
  
        return $flow;
    }
    ...
}
```

But when executing a delayed actions, we won't have a `StorableFlow`, we just have the `$stored` from the previously stored `StorableFlow`, and based on the `$stored`, we can restore a new `StorableFlow`.

Example in Delay Actions:

php

```shiki
// In handler delay actions -> put the actions to `queue`
$stored = json_encode($flow->stored());

$connection->executeStatement('INSERT INTO `swag_delay_action` (store) VALUES (:stored)...', ['stored' => $stored]);
```

php

```shiki
// In handler execute delay actions
$stored = 'SELECT store FROM `swag_delay_action` .... ';

$flow = $this->flowFactory->restore(json_decode($stored));
```

## Consequences [​](#consequences)

Because we use the new class `StorableFlow` instead of the `FlowEvent` class in the Flow Builder, we cannot use the original events or aware interfaces anymore, but about the symfony event was listeners the `FlowEvent`, those can continue to use the interfaces as the store is not yet filled during we'll remove it in next major version.

* In symfony event listeners: only use the interfaces as the store is not yet filled
* In the flow builder: Only use the store functionality as the interfaces might not be implemented

---

## Add bootstrap JS-plugin initialization utility to storefront JS

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-09-23-add-bootstrap-util.html

# Add bootstrap JS-plugin initialization utility to storefront JS [​](#add-bootstrap-js-plugin-initialization-utility-to-storefront-js)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-09-23-add-bootstrap-util.md)

## Context [​](#context)

* Some Bootstrap JavaScript plugins have to be initialized manually to the desired DOM elements, see: <https://getbootstrap.com/docs/4.3/components/tooltips/#example-enable-tooltips-everywhere>
* This is not needed for all Bootstrap plugins. Modals for example work out of the box without extra initialization.
* Currently, we only initialize Tooltips using `src/utility/tooltip/tooltip.util.js`
* On dynamic content changes (listing pagination, ajax OffCanvas cart, etc.) Bootstrap plugins like Tooltip are no longer working.
* For example: It is not possible to show Tooltips in the OffCanvas cart without extra/manual work in JavaScript.

## Decision [​](#decision)

* Add a new module `src/utility/bootstrap/bootstrap.util` in favor of `TooltipUtil` to consider more Bootstrap plugins in the future.
* Currently, it initializes `Tooltip` and `Popover` because those are the only Bootstrap plugins which have a documented manual initialization.
* We use the "selector" option in order to initialize Bootstrap plugins on selectors, which are added dynamically to the HTML. See: <https://getbootstrap.com/docs/4.3/components/tooltips/#options>

## Consequences [​](#consequences)

* In the main.js, `BootstrapUtil.initBootstrapPlugins()` is used instead of `new TooltipUtil()` to initialize Popovers as well.
* `TooltipUtil` is deprecated.
* Since we use event delegation ("selector" option) inside `BootstrapUtil` we don't need to manually re-initialize the Bootstrap plugins after dynamic content changes, so it works automatically for all `[data-toogle="tooltip"]` and `[data-toogle="popover"]` selectors.

---

## Vue 2.7 update

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-09-27-vue-2.7-update.html

# Vue 2.7 update [​](#vue-2-7-update)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-09-27-vue-2.7-update.md)

## Context [​](#context)

Vue released a new version for Vue 2. This update contains some new backported features of Vue 3 like the new Composition API. This ADR explains why we don't upgrade to Vue 2.7 in the next major.

## Decision [​](#decision)

We skip the version 2.7 and will jump directly to Vue 3 in the next year. The reason for this is that the amount of work need to be put into the update out weights the benefits the update delivers.

Following things need to be done to update to Vue 2.7:

* Fix and update the Component Factory to support the new Composition API. This also means that we need a decision if we want to make this API extendable and if yes, we need to create a concept how the extensibility should look like and implement this.
* Fix many runtime errors which freezes the whole admin. The reasons for this are several things, like using internal Vue code and more.
* Rewrite the TypeScript definitions for our components to support the improved TypeScript definitions of Vue 2.7. They are now supporting also Mixins, Extend and more. The main problem here is that we have wrapper around all these things like the Mixin Factory. And they need to return the correct types otherwise the component will not work with TypeScript

To solve all issues it will take much work. And this work will be done only for one major version, and then we go directly to Vue 3. So in general: much work for a short time and no real benefits (if we don't want to allow the Composition API yet).

## Consequences [​](#consequences)

We don't update to Vue 2.7 and jump directly to Vue 3.

---

## Mapping of product area

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-09-28-mapping-of-product-area.html

# Mapping of product area [​](#mapping-of-product-area)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-09-28-mapping-of-product-area.md)

## Context [​](#context)

We have a lot of teams working on different parts of the Shopware 6 platform. We want to have a clear mapping of the teams to the source code, so that we can easily assign the right area to a ticket. This allows us also to map automatically errors reported in our SaaS application to the right area.

## Decision [​](#decision)

We decided to add a `@package <area>` annotation to all files in the `src` and `tests` directory of the `platform`, `rufus` and `commercial` repository. This annotation will be used to map the files to the product areas.

The areas are:

* admin
* storefront
* core
* inventory
* checkout
* content
* customer-order
* services-settings
* buyers-experience

## Consequences [​](#consequences)

We will add a PHP-doc/JavaScript comment to any file with `@package <area>`

---

## Hide and show CMS content

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-10-17-hide-and-show-cms-content.html

# Hide and show CMS content [​](#hide-and-show-cms-content)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-10-17-hide-and-show-cms-content.md)

## Context [​](#context)

Many merchants reached out to us, that the possibility to customize content per device is important for them. Therefore, we would like to provide a solution to allow merchants to hide and show cms sections or blocks per devices.

## Decision [​](#decision)

Blocks and sections should be displayed or hidden per viewports, so we decided to do this on the client side via CSS media queries. We won't do this on the server side, because we don't want a full-page reload in order to hide/show blocks or sections. We also won't do an ajax call because for each block, and section this could cause too many requests on one page.

### Cms section and Cms block config [​](#cms-section-and-cms-block-config)

Merchants can use the cms sections and blocks to customize their storefront.

### Problems: [​](#problems)

* The shop merchant wants to configure sections or blocks to display them depending on the respective device.

### Solution: [​](#solution)

* We want more flexibility in the future by adding more options to configure the visibility of blocks and sections. That is why we will add visibility as a JSON column to `cms_section`, and `cms_block` table to save config for that section or block.

**Example in pseudocode:**

json

```shiki
{
    'mobile': true,
    'tablet': true,
    'desktop': true
}
```

### Administration [​](#administration)

Blocks and sections are visible on all viewports by default. In the administration, we add a new visibility section under block and section settings to allow merchants to hide or show blocks or sections by device.

**Example in pseudocode:**

html

```shiki
<sw-checkbox-field
    v-model="visibility.mobile"
    class=sw-cms-visibility-config__checkbox-input
    :label="$tc('sw-cms.sidebar.contentMenu.visibilityMobile')"
/>

<sw-checkbox-field
    v-model="visibility.tablet"
    class="sw-cms-visibility-config__checkbox-input"
    :label="$tc('sw-cms.sidebar.contentMenu.visibilityTablet')"
/>

<sw-checkbox-field
    v-model="visibility.desktop"
    class="sw-cms-visibility-config__checkbox-input"
    :label="$tc('sw-cms.sidebar.contentMenu.visibilityDesktop')"
/>
```

### Storefront [​](#storefront)

Based on the settings set in the administration, in the storefront we will add css classes in `src/Storefront/Resources/views/storefront/section/cms-section-default.html.twig` & `src/Storefront/Resources/views/storefront/section/cms-section-block-container.html.twig` to hide blocks or sections using CSS media queries.

**Example in pseudocode:**

html

```shiki
{% if block.visibility is null %}
    {% set block = {
        visibility: {
            mobile: true,
            tablet: true,
            desktop: true
        }
    } %}
{% endif %}

{% if not block.visibility.mobile %}
    {% set blockClasses = ['hidden-mobile']|merge(blockClasses) %}
{% endif %}
{% if not block.visibility.tablet %}
    {% set blockClasses = ['hidden-tablet']|merge(blockClasses) %}
{% endif %}
{% if not block.visibility.desktop %}
    {% set blockClasses = ['hidden-desktop']|merge(blockClasses) %}
{% endif %}
```

---

## Deprecation handling during PHPUnit test execution

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-10-20-deprecation-handling-during-phpunit-test-execution.html

# Deprecation handling during PHPUnit test execution [​](#deprecation-handling-during-phpunit-test-execution)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-10-20-deprecation-handling-during-phpunit-test-execution.md)

## Context [​](#context)

To stay innovative and on the bleeding edge of technology it is important, that we don't rely on deprecated functionality, as it prevents us from using the latest and greatest versions of libraries, that may include important bug fixes, performance improvements or new features. Relying on deprecated functionality makes continuously upgrading the dependencies harder, as you have a lot of work to remove the deprecated usages before being able to do the upgrades. This is not just important for external dependencies, but also for internal deprecations, that is we still rely on some deprecated functionality it makes removing the deprecation very hard.

One opportunity is to rely on our PHPUnit test suite to detect usages of deprecated functionality, so we can continuously remove them as they appear and ensure that the code base is always forward compatible.

## Solution [​](#solution)

Because the handling for internal and external deprecations is quite different we probably need different solutions for those cases. Especially as for internal deprecations we still want to ensure that they continue to work and that those deprecated code paths are also covered by tests.

### Using Symfony's Deprecation Helper for external deprecations [​](#using-symfony-s-deprecation-helper-for-external-deprecations)

Symfony offers a tool to report all deprecations that are encountered when running the test inside their [PHPUnit Bridge](https://symfony.com/doc/current/components/phpunit_bridge.html). With enabling the [`SYMFONY_DEPRECATIONS_HELPER`](https://symfony.com/doc/current/components/phpunit_bridge.html#trigger-deprecation-notices) for our testsuite we can ensure that no deprecations are triggered while executing the tests. Previously we could not enable this as it also reported all deprecation usages for internal deprecations and also reported on deprecations that were triggered from inside external dependencies that we could not fix from inside shopware.

But since lately a feature was added to use a [`ignoreFile`](https://symfony.com/doc/current/components/phpunit_bridge.html#ignoring-deprecations), in order to ignore specific deprecations by regex.

We leverage this feature by using it in a way to ignore all deprecations that we can't fix immediately. Those cases especially include:

1. Ignoring all internal deprecations (as they are handled differently, see next section)
2. Ignoring all deprecations from inside external dependencies (those ignores should be commented by the package that is triggering them, so we can remove them once we are able to update the dependency that is triggering them)
3. Ignoring all deprecations that would be too much to fix immediately. E.g. if in a library update a lot of new deprecations are added (say DBAL renaming a big portion of it's public API), that would be too much work to fix immediately we can ignore those deprecations **temporarily** and create a ticket to remove those deprecations.

### Using our Feature Flag system for internal deprecations [​](#using-our-feature-flag-system-for-internal-deprecations)

Internally we use the feature flag system to trigger deprecation messages, or throw exceptions if the major feature flag is activated as explained in the [deprecation handling ADR](./../adr/2022-02-28-consistent-deprecation-notices-in-core.html). We already use that system in our new unit test suite with a custom `@ActiveFeatures()` annotations, that allows us to run single test cases with a specific set of feature flags. But the current implementation has the big drawback that feature flags have to be actively enabled, this leads to following problems:

1. There are already tests that are not passing after all deprecations are removed, because they rely on deprecated behaviour.
2. We can't check automatically that our implementation is forward compatible, as the default way of executing tests is without any major flag activated.
3. It is hard to directly see which test cases are there only to cover legacy/deprecated functionality and can safely be removed after the deprecations are removed.

Therefore, the workflow is updated in the following way:

1. All unit tests get executed with all major feature flags activated.
2. The `@ActiveFeatures()` will be removed, and we introduce a `@DisableFeatures` annotation, that works in the exact opposite way => disabling all feature flags that are passed.

This has the upside that now the default behaviour of our test suite is the new/not-deprecated behaviour, and the deprecated code paths are treated as the exceptional case instead the other way around. Additionally, all tests that are relying on deprecated behaviour are marked with the `@DisableFeatures` annotations, so it is easy to detect them and simply remove them, if the underlying deprecation was removed.

---

## Test structure

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-10-20-test-structure.html

# Test structure [​](#test-structure)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-10-20-test-structure.md)

## Context [​](#context)

Currently, all tests are in the same folder: `src/Administration/Resources/app/administration/test`. This approach has some disadvantages:

* While changing a component, you have to search for the corresponding test file
* You can't see which components are tested and which are not

## Decision [​](#decision)

We will move the tests to the same folder as the components they test. This approach is standard in the Vue community and solves the problems mentioned above.

### Example [​](#example)

The test for the `sw-cms-el-config-image` component will be moved to `src/Administration/Resources/app/administration/src/module/sw-cms/component/sw-cms-el-config-image/sw-cms-el-config-image.spec.js`. The test file should contain the same name as the component it tests. So a valid test file name would be `[component name].spec.js|ts`. The `[` and `]`are not part of the name. Additionally test files are either `.js` or `.ts` files. Typescript is preferred.

## Consequences [​](#consequences)

Test files will no longer be loaded from the test folder.

---

## Composer-based web updater

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-11-09-composer-based-web-updater.html

# Composer-based web updater [​](#composer-based-web-updater)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-11-09-composer-based-web-updater.md)

## Context [​](#context)

Currently, we are using a Slim Framework 2 based web updater which downloads the zip file from our server and unpacks it. This is a very old approach and blocks us implementing new features like using Composer to install additional composer packages.

So our main problems are:

### Outdated stack of the updater itself [​](#outdated-stack-of-the-updater-itself)

The Slim Framework 2 is outdated and is not supported anymore. We also don't have any good knowledge about the framework itself.

### Dangerous update process [​](#dangerous-update-process)

* We assume that the shop files are in the same state as after the installation or the latest update. So we only apply the changeset to the latest update
* If the user runs Composer commands, the generated and dumped autoloader can differ and break the entire shop

### No Composer support [​](#no-composer-support)

* Due to the simple unpacking of a changeset of the Shopware update, the user cannot use Composer to install additional packages
* Extensions have to package their own dependencies inside their extension zip and overwrite dependencies of Shopware or other extensions which can cause problems

## Decision [​](#decision)

We will build a new Symfony based web updater which is packaged as an single phar file. The Phar file will be downloaded from our server for each update and runs the newest web updater for the process of the update. This allows us to react faster on bugs and implement new features, without having to wait for a new Shopware release.

The new web updater will use the same update process as the CLI update using composer.

So the process will be:

* The Shopware Admin will do a basic update check that all extensions are compatible with the next Shopware version
* If the user clicks on the update button the web updater will be downloaded and executed
* If the project is still based on the old structure, it will migrate it to Symfony Flex.
* Enable the maintenance mode using `bin/console`
* Run `composer update` to update Shopware
* Run `bin/console` to update the database
* Disable the maintenance mode
* Delete the Phar and Redirect the user to the Shopware Admin

The new way of managing a Shopware project will also allow us to setup a new project with the new tool. So in the same way, we can provide an installer for new projects by utilising the `create-project` command of Composer.

## Consequences [​](#consequences)

The System requirements will change. We need access to functions like `proc_open` and `proc_close` in PHP and a PHP-CLI binary.

For updating config files Symfony Flex requires the `git` binary to be installed on the server and a git repository to be initialised. This is a requirement for reviewing all the changes that have been made to the config files. To avoid this we will backup the `.env` and the `.htaccess` file and overwrite all config files from a fresh installation and restore the backup.

To merge the upcoming changes of the `.htaccess` file we will use our already existing [UpdateHtaccess](https://github.com/shopware/shopware/blob/6.4.17.0/src/Core/Framework/Update/Services/UpdateHtaccess.php) which is using the Markers to update only our own changes. For the `.env` files we will make use of `.env.local` to be able to update the normal `.env` file.

The normal CLI update way will require a git repository to be initialised and uses the normal Symfony update flow.

---

## Deprecate the storefront CSRF implementation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-11-16-deprecate-csrf.html

# Deprecate the storefront CSRF implementation [​](#deprecate-the-storefront-csrf-implementation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-11-16-deprecate-csrf.md)

## Context [​](#context)

* With browsers evolving and dropping support for older browser in 6.5 we have wide support for SameSite cookies.
* The current CSRF implementation adds a lot of complexity to all forms and ajax calls in the Storefront.
* The CSRF protection does not add a great improvement in security due to the SameSite strategy.

## Decision [​](#decision)

* We remove the CSRF protection in favor of SameSite cookies which are used and prevent CSRF attacks already.

## Consequences [​](#consequences)

* All CSRF implementations in the Storefront will be removed.

---

## Replace drop-shadow with box-shadow

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-11-21-replace-drop-shadow-with-box-shadow.html

# Replace drop-shadow with box-shadow [​](#replace-drop-shadow-with-box-shadow)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-11-21-replace-drop-shadow-with-box-shadow.md)

## Context [​](#context)

Safari has drastic performance issues with drop-shadow.

## Decision [​](#decision)

Changing it to box-shadow solves all the performance issues.

## Consequences [​](#consequences)

The design and optic of the drop-shadow is slightly different. It is not as perfect as before. But it looks almost the same and is much faster.

---

## Run Lighthouse tests in E2E env

**Source:** https://developer.shopware.com/docs/resources/references/adr/2022-11-25-run-lighthouse-test-ine2e-env.html

# Run Lighthouse tests in E2E env [​](#run-lighthouse-tests-in-e2e-env)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2022-11-25-run-lighthouse-test-ine2e-env.md)

## Context [​](#context)

The Lighthouse test ran in the `APP_ENV=prod`, this meant that also AdminQueueWorker was active, which is recommended to not be used in real prod setups.

## Decision [​](#decision)

Use `APP_ENV=e2e` for lighthouse tests, to deactivate the admin worker. After removing enqueue lighthouse ran int o timeouts when the admin worker was used, this solves this problem also. Besides that it should lead to much more realistic results.

## Consequences [​](#consequences)

This means that the lighthouse tests won't run in the real `prod` env anymore, but the main difference between the two envs is that in `e2e` env the admin worker is deactivated, which is probably closer to "real" production setups. The only other difference is that all rate limits are deactivated in the `e2e` env, but this is not relevant for the lighthouse tests.

---

## Atomic theme compilation

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-01-10-atomic-theme-compilation.html

# Atomic theme compilation [​](#atomic-theme-compilation)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-01-10-atomic-theme-compilation.md)

## Context [​](#context)

The theme compilation could result in a broken storefront, when there is some error during theme compilation (e.g. because of wrongly configured values in the theme configuration by the customer). The reason is that the theme is always compiled into the same physical folder/location and at the start of the compilation this folder will be deleted and recreated, but when the compilation crashes due to errors, not all needed files are present in the theme folder and the storefront UI is broken.

Another issue was that there were edge cases when you hit a shop where the theme compilation was in progress, the storefront also may look broken as not all required compiled files are present in the theme folder (yet).

## Decision [​](#decision)

Instead of compiling the theme always in the same folder we will compile the theme always in a new folder with a generated seed. Until the theme compilation is completed and successful the old theme will be used in the storefront UI, only when the theme compilation is finished we will use the new theme folder in the storefront.

This will also open up the possibility for further new features where the customer may manually rollback to previous theme compiled version. But for now we will delete the old theme folder one hour (see [caching](#caching)) after the theme was compiled successfully to the new location and we use the theme from the new location in the storefront.

### Discarded Alternatives [​](#discarded-alternatives)

An alternative solution would be to always use the same folder location for the live version of the theme, but the theme compile process will not directly write into this folder, but in a temporary folder. When the theme compilation finished we then copy the whole temp folder over to the live folder.

This approach works well under the assumptions that moving a whole folder is a fast and a atomic operation, which it is on most local filesystems. But the theme assets can also be stored on external storage (e.g. S3, Google Cloud storage), especially for more dedicated setups it is common to store the asset files on a external filesystem/CDN. And we can't assume that copying a whole folder is an atomic operation there, and in fact for S3 and Google Cloud Storage moving a folder means that we need to manually empty the target folder and move each file individually as both storages don't really support the concept of `folders`. Even though this alternative fixed the issue when theme compilation errored, it does not fix the edge case when you hit a store where the current theme asset folder does not contain all needed folders yet. And as the files have to be copied one by one it would probably exaggerate that problem further.

Additionally, from a cost perspective the solution has some downsides, as on some (especially S3) external storages you not only pay for the storage itself, but also for file operations. And using a temporary folder and then moving the folders will result in a lot more file operations, compared to directly compiling into the new folder.

Because of the aforementioned issues we decided to discard this approach.

## Consequences [​](#consequences)

We will expand the abstract class `AbstractThemePathBuilder` to allow for a `seeding` mechanism that allows to change the active theme folder path based on a randomly generated seed.

We add the two following methods that should be implemented in custom implementations of the `AbstractThemePathBuilder`.

php

```shiki
    public function generateNewPath(string $salesChannelId, string $themeId, string $seed): string
    {
    }

    public function saveSeed(string $salesChannelId, string $themeId, string $seed): void
    {
    }
```

During a theme compilation the theme compiler will generate a new random seed and call the `generateNewPath()` method with that seed, to get the location of the theme folder where the compiled files of that compilation will be stored. After the theme compilation is finished successfully the compiler will call the `saveSeed()` method with the seed that was used for the compilation, after that subsequent calls to the existing `assemblePath()` method should take into account the new seed and thus the new theme folder should be used in the storefront.

### Backwards Compatibility [​](#backwards-compatibility)

Those methods will be added as concrete methods in the abstract class with a default implementation, to not break backwards compatibility. But both new methods are marked as `@deprecated`, because they will be abstract in the 6.6 major version, so custom implementations have to implement those methods for 6.6. The default implementation to keep backwards compatibility will ignore the seed, so the `saveSeed()` method will be a no-op, and the `generateNewPath()` will just call the existing `assemblePath()` method, thus the behaviour for existing implementations will be the same as before this change. This means that the old implementations also don't use the seeding mechanism, so the problems with the theme compilation will still be present in those implementations, unless the custom implementations also implement the seeding mechanism, by implementing the two new methods.

### Performance [​](#performance)

The current `seed` has to be saved somewhere where it is fast to retrieve, as the `seed` value will be needed on every storefront request. Therefore, we will store the `seed` in `system_config` table as the system config is already heavily cached and should not be a performance issue. Additionally it already allows saving values per sales channel which we need in this case.

We also considered storing the seed in an additional column in the `theme_sales_channel` mapping table and reading it in the `RequestTransformer` and then adding it as a `request attribute` for further usage. This idea was discarded, because the DAL does not allow additional columns in mapping definitions, and in fact it will reset values in additional columns on every write as it uses `REPLACE INTO` queries to update the mappings.

### Caching [​](#caching)

As the url to the assets now change this means that the cache for all storefront requests needs to be invalidated. This was already the case previously as a new theme compilation would add a cache-buster query param to the url, to prevent the serving of stale theme files cached on the browser side.

But with the theme compilation, we can't delete the old theme folder immediately after the new theme compilation finished successfully, as the cache invalidation can take some time especially if you use external CDNs like fastly. This means that we expect for a short time that clients still will request the old theme folder, because they are served stale content from the CDN. To ensure that the site renders normally for those clients we won't delete the old theme folder immediately, but instead dispatch a queue message with a configurable delay (default 15 min / max SQS delay) that the old theme folder should be deleted. So the old theme files will still be accessible for one hour after a new theme was compiled.

We can expand on this deletion strategy, once we implement further features like manual rollback to previous theme versions.

### Theme Assets [​](#theme-assets)

Previously the theme assets were stored in the same folder as the compiled theme files, that meant, that for every saleschannel where a theme was used the theme assets were duplicated, even though the assets are always the same, regardless of the theme configuration. This does not scale, when we create new folders for the compiled theme files on the fly on every theme compile. So the asset files are now stored in a separate folder, that is not dependent on the sales channel or the theme configuration. We use the `themeId` as the folder name, so the assets are still unique per theme, but they are not duplicated for every sales channel.

### PaaS / Upsun [​](#paas-upsun)

Upsun currently does not offer to store the theme assets on an internal storage, therefore the assets need to be stored locally. Additionally, Upsun uses `immutable deploys`, meaning that once a version is deployed the file system is read-only and no changes can be made to the local files.

The theme compile is executed on PaaS during the `build` step, where there is no DB connection, so we can't use the new default implementation of the `AbstractThemePathBuilder`, which stores the new `seed` in the DB during the theme compile. But because of the `immutable deploys` it is not possible to recompile the theme at runtime, a new deployment is needed to recompile the theme. So PaaS was not affected by the issues during the theme compilation, and instead of rollbacking to a backup theme folder you would rollback to the last deployment instead.

That means that PaaS does not need the seeding mechanism, so we add a implementation for the `AbstractThemePathBuilder` that ignores the seed and will always return the same path for a given theme and sales channel combination (like the old default implementation).

Once Upsun allows to store the theme assets externally we can move the theme compile from the `build` to the `deploy` step and can then use the default `seeding` implementation, as we have access to the DB in the deploy step. Then you can also recompile the theme at runtime and PaaS will also benefit from the new theme compile mechanism.

---

## Npm packages pre-release versions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-01-16-npm-packages-pre-release-versions.html

# Npm packages pre-release versions [​](#npm-packages-pre-release-versions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-01-16-npm-packages-pre-release-versions.md)

## Context [​](#context)

A pre-release package version is a version followed by a hyphen and an alphanumeric string.

Imagine the following scenario:

* An imaginary package is marked as insecure with version 1.8.7
* The issue is fixed with 2.0.0
* We use version `1.9.0-alpha1`
* Any pre-release package version like `1.9.0-alpha1` is interpreted as `<0.0.0` by npm

Why is this problematic?

The insecurity introduced with version `1.8.7` would never get reported to us by npm, unless we switch to a none pre-release version.

## Decision [​](#decision)

Using pre-release package versions is prohibited. This will be checked via a npm `preinstall` script.

## Consequences [​](#consequences)

Bug fix releases only available as a preview in a pre-release package can't be used.

---

## Add native lazy loading for images to the storefront

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-01-30-image-lazy-loading.html

# Add native lazy loading for images to the storefront [​](#add-native-lazy-loading-for-images-to-the-storefront)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-01-30-image-lazy-loading.md)

## Context [​](#context)

* Currently, the images/thumbnails inside the Storefront are not making use of any lazy loading mechanism.
* Without a third-party extension which includes something like "lazysizes" it is not possible to get lazy loading images.
* Native lazy loading of images is available in current browsers, see: <https://caniuse.com/?search=loading>

## Decision [​](#decision)

* We want to make use of native lazy loading for images in the Storefront without adding additional JavaScript logic.

## Consequences [​](#consequences)

* We pass a new attribute `loading="lazy"` to several usages of the thumbnail component `Resources/views/storefront/utilities/thumbnail.html.twig`. This enables native lazy loading.
* By default, the thumbnail component uses `loading="eager"` which is the default behaviour and has the same effect as not setting the attribute.
* The default is not `lazy` in order to avoid unexpected behaviour for extensions which might have added the thumbnail component while using a JavaScript solution for lazy loading.
* We add native lazy loading in appropriate areas to reduce the initial network load:
  + Main menu flyout: Category preview images will only load when flyout is being opened.
  + Product boxes: Product images will only load when they appear in the viewport inside the listing. This also affects product sliders with horizontal scrolling, e.g. cross-selling.
  + CMS image elements: CMS layouts will only load images which appear in the viewport (e.g., when scrolling down the page).
  + Line item images: Product images in line items (e.g., cart page) will only load when they appear in the viewport.

### Why don't we just add `loading="lazy"` everywhere? [​](#why-don-t-we-just-add-loading-lazy-everywhere)

* Even though this would technically work, there are a few pitfalls that need to be considered.
* For example, it is not recommended to add lazy loading to images which are very likely inside the initial viewport when loading the page aka "above-the-fold". Further reading: <https://web.dev/browser-level-lazy-loading-for-cmss/#avoid-lazy-loading-above-the-fold-elements>
* For a system like shopware, where the content is almost entirely dynamic, it is not easy to determine where a generic image component will be rendered. It could have any position on any CMS page.
* Even "guesses" like "only add lazy loading after the 8th product in a listing" can be invalid as soon as a monitor is in portrait mode or the viewport changes to mobile.
* Therefore, we live with the small drawback that, e.g., all product boxes have lazy loading. Some of them will appear "above-the-fold". However, we still have the benefit of loading images later when scrolling down a page or scrolling in product sliders.
* Implementing a JavaScript solution for this would contradict the usage of native lazy loading.

#### Areas without loading="lazy"` [​](#areas-without-loading-lazy)

* Image gallery on product detail page: This is very likely "above-the-fold" and the gallery already uses JavaScript lazy loading for the image zoom as well.
* Image sliders (CMS): When sliding to the next image, the lazy loading can lead to a bad user experience because the image can appear too late.

#### How to activate lazy loading? [​](#how-to-activate-lazy-loading)

When using the thumbnail component, pass the `loading` attribute with value `lazy`:

diff

```shiki
{% sw_thumbnails 'my-thumbnail' with {
    media: category.media,
    attributes: {
        'class': 'my-css-class'
+        'loading': 'lazy'
    }
} %}
```

---

## App script product pricing

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-01-app-script-product-pricing.html

# App script product pricing [​](#app-script-product-pricing)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-01-app-script-product-pricing.md)

## Context [​](#context)

We want to provide the opportunity to manipulate the price of a product inside the cart and within the store. For the cart manipulation we already have a hook integrated which allows accessing and manipulating the cart. Right now we are not allowing to manipulate prices directly but just creating discounts or new price objects and add them as new line items into the cart.

However, there are different business cases which require a direct price manipulation like `get a sample of the product for free`

The following code can be used for manipulating the prices in the product-pricing hook:

php

```shiki
{% foreach hook.products as product %}
    {# allow resetting product prices #}
    {% do product.calculatedCheapestPrice.reset %}
    {% do product.calculatedPrices.reset %}
    {# not allowed to RESET the default price otherwise it is not more valid
    
    {# get control of the default price calculation #}
    {% set price = services.prices.create({
       'default': { 'gross': 20, 'net': 20 },
       'USD': { 'gross': 15, 'net': 15 },
       'EUR': { 'gross': 10, 'net': 10 }
    }) %}
    
    {# directly changes the price to a fix value #}
    {% do product.calculatedPrice.change(price) %}
    
    {# manipulate the price and subtract the provided price object #}
    {% do product.calculatedPrice.minus(price) %}
    
    {# manipulate the price and add the provided price object #}
    {% do product.calculatedPrice.plus(price) %}
    
    {# the following examples show how to deal with percentage manipulation #}
    {% do product.calculatedPrice.discount(10) %}
    {% do product.calculatedPrice.surcharge(10) %}
    
    {# get control of graduated prices #}
    {% do product.calculatedPrices.reset %}
    {% do product.calculatedPrices.change([
        { to: 20, price: services.prices.create({ 'default': { 'gross': 15, 'net': 15} }) },
        { to: 30, price: services.prices.create({ 'default': { 'gross': 10, 'net': 10} }) },
        { to: null, price: services.prices.create({ 'default': { 'gross': 5, 'net': 5} }) },
    ]) %}
    
    {# after hook => walk through prices and fix "from/to" values #}
    
    {% do product.calculatedCheapestPrice.change(price) %}
    {% do product.calculatedCheapestPrice.minus(price) %}
    {% do product.calculatedCheapestPrice.plus(price) %}
    {% do product.calculatedCheapestPrice.discount(10) %}
    {% do product.calculatedCheapestPrice.surcharge(10) %}

{% endforeach %}
```

The following code can be used to manipulate the prices of a product inside the cart:

php

```shiki
{# manipulate price of a product inside the cart #}
{% set product = services.cart.get('my-product-id') %}

{% set price = services.prices.create({
   'default': { 'gross': 20, 'net': 20 }
}) %}

{% do product.price.change(price) %}

{% do product.price.discount(10) %}
{% do product.price.surcharge(10) %}
```

---

## Deprecate autoloading associations in DAL entity definitions

**Source:** https://developer.shopware.com/docs/resources/references/adr/2023-02-02-deprecate-autoload-true-in-dal-associations.html

# Deprecate autoloading associations in DAL entity definitions [​](#deprecate-autoloading-associations-in-dal-entity-definitions)

INFO

This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository. You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/2023-02-02-deprecate-autoload-true-in-dal-associations.md)

## Context [​](#context)

When using the `OneToOneAssociationField` & `ManyToOneAssociationField` associations it is possible to specify the parameter `autoload` as `true`. This causes the association to be loaded with every query, regardless of whether the data is used or not.

This is a performance issue due to unnecessary data transfer, it slows down SQL queries with extra joins, slows the application down with hydrating and data processing and finally, API payloads are larger than they need to be.

## Decision [​](#decision)

We will deprecate the usage of autoload === true in the core codebase in version 6.5. All usages in entity definitions should be removed by the time 6.6 is released.

We have introduced a new PHPStan rule which will check for any usages of autoload === true and fail if it finds any. The failures are currently ignored in the `phpstan.neon.dist` file until they can be fixed by the respective teams.

## Migration Strategy [​](#migration-strategy)

In order to safely migrate core code away from using autoload === true, the following steps should be followed:

1. Document all deprecations in the changelog
2. All internal APIs that rely on data that is autoloaded should now specify the association in the criteria objects.
3. All entity definitions should be updated to add the association conditionally based on the 6.6 feature flag, see below for an example.
4. In the run-up to the 6.6 release the feature conditional should be removed.

```shiki
public function defineFields(): FieldCollection
{
   $fields = new FieldCollection(...);

  if (Feature::isActive('v6.6.0.0') {
     $fields->add(new ManyToOneAssociationField(..., autoload: false);
  } else {
     $fields->add(new ManyToOneAssociationField(..., autoload: true);
  }
}
```

## Breaking changes [​](#breaking-changes)

For external consumers of the API who are relying on data which is autoloaded, removing the autoloaded entities will indeed be a BC break. However, this break should be minimal since it is not documented anywhere which associations are autoloaded. They would have found the data only by manually inspecting the responses.

External consumers will have to change their code to specifically request any associations they are using once 6.6 is released. They can of course specify the association, before 6.6 is released and it will continue to work as it did.

---

