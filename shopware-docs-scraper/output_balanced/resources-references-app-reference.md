# Resources References App Reference

*Scraped from Shopware Developer Documentation*

---

## App Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/

# App Reference [​](#app-reference)

The app reference document gives you an understanding of the app structure, functions, methods, events, variables, responses, and examples for building quality apps in Shopware.

Overall, the app reference document is a valuable resource for creating feature-rich and seamless custom apps that integrate seamlessly with the Shopware platform.

---

## Script Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/

# Script Reference [​](#script-reference)

Script references include detailed explanations of the available functions, methods, arguments, responses, and samples.

This reference gives you an understanding of the various service capabilities, code structure, and functionalities.

---

## Cart Manipulation script services reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/cart-manipulation-script-services-reference.html

# Cart Manipulation script services reference [​](#cart-manipulation-script-services-reference)

## [services.cart (`Shopware\Core\Checkout\Cart\Facade\CartFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/CartFacade.php) [​](#cartfacade)

The `cart` service allows you to manipulate the cart. You can use the cart service to add line-items, change prices, add discounts, etc. to the cart.

### items() [​](#items)

* The `items()` method returns all line-items of the current cart for further manipulation.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemsFacade`](./cart-manipulation-script-services-reference.html#itemsfacade)

  A `ItemsFacade` containing all line-items in the current cart as a collection.

### products() [​](#products)

* The `product()` method returns all products of the current cart for further manipulation.

  Similar to the `items()` method, but the line-items are filtered, to only contain product line items.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ProductsFacade`](./cart-manipulation-script-services-reference.html#productsfacade)

  A `ProductsFacade` containing all product line-items in the current cart as a collection.

### calculate() [​](#calculate)

* The `calculate()` method recalculates the whole cart.

  Use this to get the correct prices after you made changes to the cart. Note that after calling the `calculate()` all collections (e.g. items(), products()) get new references, so if you still hold references to things inside the cart, these are outdated after calling `calculate()`.

  The `calculate()` method will be called automatically after your cart script executed.

### price() [​](#price)

* The `price()` method returns the current price of the cart.

  Note that this price may be outdated, if you changed something inside the cart in your script. Use the `calculate()` method to recalculate the cart and update the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\CartPriceFacade`](./cart-manipulation-script-services-reference.html#cartpricefacade)

  The calculated price of the cart.

### errors() [​](#errors)

* The `errors()` method returns the current errors of the cart.

  You can use it to add new errors or warning or to remove existing ones.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ErrorsFacade`](./cart-manipulation-script-services-reference.html#errorsfacade)

  A `ErrorsFacade` containing all cart errors as a collection (may be an empty collection if there are no errors).

### states() [​](#states)

* `states()` allows you to access the state functions of the current cart.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\StatesFacade`](./cart-manipulation-script-services-reference.html#statesfacade)

  A `StatesFacade` containing all cart states as a collection (maybe an empty collection if there are no states).

### discount() [​](#discount)

* The `discount()` methods creates a new discount line-item with the given type and value.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference.html#discountfacade)

  Returns the newly created discount line-item.
* **Arguments:**

  + *`string`* **key**: The id for the new discount.
  + *`string`* **type**: The type of the discount, e.g. `percentage`, `absolute`
  + *`float|\PriceCollection`* **value**: The value of the discount, a float for percentage discounts or a `PriceCollection` for absolute discounts.
  + *`string`* **label**: The label of the discount line-item.
* **Examples:**

  + Add an absolute discount to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.items.count <= 0 %}
        {% return %}
    {% endif %}

    {% if services.cart.items.has('my-discount') %}
        {% return %}
    {% endif %}

    {% set price = services.cart.price.create({
        'default': { 'gross': -19.99, 'net': -19.99}
    }) %}

    {% do services.cart.discount('my-discount', 'absolute', price, 'Fancy discount') %}
    ```
  + Add a relative discount to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-discount') %}
        {% return %}
    {% endif %}

    {% do services.cart.discount('my-discount', 'percentage', -10, 'Fancy discount') %}
    ```

### count() [​](#count)

* `count()` returns the count of line-items in this collection.

  Note that it does only count the line-items directly in this collection and not child line-items of those.
* **Returns** `int`

  The number of line-items in this collection.

### get() [​](#get)

* `get()` returns the line-item with the given id from this collection.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  The line-item with the given id, or null if it does not exist.
* **Arguments:**

  + *`string`* **id**: The id of the line-item that should be returned.

### has() [​](#has)

* `has()` checks if a line-item with the given id exists in this collection.
* **Returns** `bool`

  Returns true if the given line-item or a line-item with the given id already exists in the collection, false otherwise.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id or a line-item that should be checked if it already exists in the collection.

### remove() [​](#remove)

* `remove()` removes the given line-item or the line-item with the given id from this collection.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id of the line-item or the line-item that should be removed.
* **Examples:**

  + Add and then remove a product line-item from the cart.

    twig

    ```shiki
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% do services.cart.products.remove(hook.ids.get('p1')) %}
    ```

### surcharge() [​](#surcharge)

* The `surcharge()` methods creates a new surcharge line-item with the given type and value.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference.html#discountfacade)

  Returns the newly created surcharge line-item.
* **Arguments:**

  + *`string`* **key**: The id for the new surcharge.
  + *`string`* **type**: The type of the surcharge, e.g. `percentage`, `absolute`
  + *`float|\PriceCollection`* **value**: The value of the surcharge, a float for percentage surcharges or a `PriceCollection` for absolute surcharges.
  + *`string`* **label**: The label of the surcharge line-item.
* **Examples:**

  + Add an absolute surcharge to the cart.#

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}

    {% do services.cart.surcharge('my-surcharge', 'absolute', price, 'Fancy surcharge') %}
    ```
  + Add a relative surcharge to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-surcharge') %}
        {% return %}
    {% endif %}

    {% do services.cart.surcharge('my-surcharge', 'percentage', -10, 'Fancy discount') %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\CartPriceFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/CartPriceFacade.php) [​](#cartpricefacade)

The CartPriceFacade is a wrapper around the calculated price of a cart.

### getNet() [​](#getnet)

* `getNet()` returns the net price of the cart.
* **Returns** `float`

  Returns the net price of the cart as float.

### getTotal() [​](#gettotal)

* `getTotal()` returns the total price of the cart that has to be paid by the customer.

  Depending on the tax settings this may be the gross or net price. Note that this price is already rounded, to get the raw price before rounding use `getRaw()`.
* **Returns** `float`

  The rounded total price of the cart as float.

### getPosition() [​](#getposition)

* `getPosition()` returns the sum price of all line-items in the cart.

  In the position price the shipping costs are excluded. Depending on the tax settings this may be the gross or net price og the line-items.
* **Returns** `float`

  The position price as float.

### getRounded() [​](#getrounded)

* Alias for `getTotal()`.
* **Returns** `float`

  The rounded total price of the cart as float.

### getRaw() [​](#getraw)

* `getRaw() returns the total price of the cart before rounding.
* **Returns** `float`

  The total price before rounding as float.

### create() [​](#create)

* `create()` creates a new `PriceCollection` based on an array of prices.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)

  Returns the newly created `PriceCollection`.
* **Arguments:**

  + *`array`* **price**: The prices for the new collection, indexed by the currency-id or iso-code of the currency.
* **Examples:**

  + Create a new Price in the default currency.

    twig

    ```shiki
    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\ContainerFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ContainerFacade.php) [​](#containerfacade)

The ContainerFacade allows you to wrap multiple line-items inside a container line-item.

### products() [​](#products-1)

* The `product()` method returns all products inside the current container for further manipulation.

  Similar to the `children()` method, but the line-items are filtered, to only contain product line items.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ProductsFacade`](./cart-manipulation-script-services-reference.html#productsfacade)

  A `ProductsFacade` containing all product line-items inside the current container as a collection.

### add() [​](#add)

* Use the `add()` method to add an item to this container.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)

  The item that was added to the container.
* **Arguments:**

  + *[`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)* **item**: The item that should be added.
* **Examples:**

  + Add a product to the container and reduce the quantity of the original line-item.

    twig

### getPrice() [​](#getprice)

* `getPrice()` returns the calculated price of the line-item.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference.html#pricefacade) | `null`

  Returns the price of the line-item as a `PriceFacade` or null if the line-item has no calculated price.

### take() [​](#take)

* `take()` splits an existing line-item by a given quantity.

  It removes the given quantity from the existing line-item and returns a new line-item with exactly that quantity.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  Returns the new line-item as an `ItemFacade` or null if taking is not possible because the line-item has no sufficient quantity.
* **Arguments:**

  + *`int`* **quantity**: The quantity that should be taken.
  + *`string` | `null`* **key**: Optional: The id of the new line-item. A random UUID will be used if none is provided.

    Default: `null`
* **Examples:**

  + Take a quantity of 2 from an existing product line-item and add it to the cart again.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1'), 5) %}

    {% set product = services.cart.products.get(hook.ids.get('p1')) %}

    {% set split = product.take(2, 'new-key') %}

    {% do services.cart.products.add(split) %}
    ```

### getId() [​](#getid)

* `getId()` returns the id of the line-item.
* **Returns** `string`

  Returns the id.

### getReferencedId() [​](#getreferencedid)

* `getReferenceId()` returns the id of the referenced entity of the line-item.

  E.g. for product line-items this will return the id of the referenced product.
* **Returns** `string` | `null`

  Returns the id of the referenced entity, or null if no entity is referenced.

### getQuantity() [​](#getquantity)

* `getQuantity()` returns the quantity of the line-item.
* **Returns** `int`

  Returns the quantity.

### getLabel() [​](#getlabel)

* `getLabel()` returns the translated label of the line-item.
* **Returns** `string` | `null`

  Returns the translated label, or null if none exists.

### getPayload() [​](#getpayload)

* `getPayload()` returns the payload of this line-item.
* **Returns** [`Shopware\Core\Framework\Script\Facade\ArrayFacade`](./miscellaneous-script-services-reference.html#arrayfacade)

  Returns the payload as `ArrayFacade`.

### getChildren() [​](#getchildren)

* `getChildren()` returns the child line-items of this line-item.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemsFacade`](./cart-manipulation-script-services-reference.html#itemsfacade)

  Returns the children as a `ItemsFacade`, that may be empty if no children exist.

### getType() [​](#gettype)

* `getType()` returns the type of this line-item.

  Possible types include `product`, `discount`, `container`, etc.
* **Returns** `string`

  The type of the line-item.

### discount() [​](#discount-1)

* The `discount()` methods creates a new discount line-item with the given type and value.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference.html#discountfacade)

  Returns the newly created discount line-item.
* **Arguments:**

  + *`string`* **key**: The id for the new discount.
  + *`string`* **type**: The type of the discount, e.g. `percentage`, `absolute`
  + *`float|\PriceCollection`* **value**: The value of the discount, a float for percentage discounts or a `PriceCollection` for absolute discounts.
  + *`string`* **label**: The label of the discount line-item.
* **Examples:**

  + Add an absolute discount to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.items.count <= 0 %}
        {% return %}
    {% endif %}

    {% if services.cart.items.has('my-discount') %}
        {% return %}
    {% endif %}

    {% set price = services.cart.price.create({
        'default': { 'gross': -19.99, 'net': -19.99}
    }) %}

    {% do services.cart.discount('my-discount', 'absolute', price, 'Fancy discount') %}
    ```
  + Add a relative discount to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-discount') %}
        {% return %}
    {% endif %}

    {% do services.cart.discount('my-discount', 'percentage', -10, 'Fancy discount') %}
    ```

### count() [​](#count-1)

* `count()` returns the count of line-items in this collection.

  Note that it does only count the line-items directly in this collection and not child line-items of those.
* **Returns** `int`

  The number of line-items in this collection.

### get() [​](#get-1)

* `get()` returns the line-item with the given id from this collection.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  The line-item with the given id, or null if it does not exist.
* **Arguments:**

  + *`string`* **id**: The id of the line-item that should be returned.

### has() [​](#has-1)

* `has()` checks if a line-item with the given id exists in this collection.
* **Returns** `bool`

  Returns true if the given line-item or a line-item with the given id already exists in the collection, false otherwise.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id or a line-item that should be checked if it already exists in the collection.

### remove() [​](#remove-1)

* `remove()` removes the given line-item or the line-item with the given id from this collection.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id of the line-item or the line-item that should be removed.
* **Examples:**

  + Add and then remove a product line-item from the cart.

    twig

    ```shiki
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% do services.cart.products.remove(hook.ids.get('p1')) %}
    ```

### surcharge() [​](#surcharge-1)

* The `surcharge()` methods creates a new surcharge line-item with the given type and value.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference.html#discountfacade)

  Returns the newly created surcharge line-item.
* **Arguments:**

  + *`string`* **key**: The id for the new surcharge.
  + *`string`* **type**: The type of the surcharge, e.g. `percentage`, `absolute`
  + *`float|\PriceCollection`* **value**: The value of the surcharge, a float for percentage surcharges or a `PriceCollection` for absolute surcharges.
  + *`string`* **label**: The label of the surcharge line-item.
* **Examples:**

  + Add an absolute surcharge to the cart.#

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}

    {% do services.cart.surcharge('my-surcharge', 'absolute', price, 'Fancy surcharge') %}
    ```
  + Add a relative surcharge to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-surcharge') %}
        {% return %}
    {% endif %}

    {% do services.cart.surcharge('my-surcharge', 'percentage', -10, 'Fancy discount') %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/DiscountFacade.php) [​](#discountfacade)

The DiscountFacade is a wrapper around a newly created discount. Note that this wrapper is independent from the line-item that was added for this discount.

### getId() [​](#getid-1)

* `getId()` returns the id of the line-item that was added with this discount.
* **Returns** `string`

  The id of the discount line-item.

### getLabel() [​](#getlabel-1)

* `getLabel()` returns the translated label of the line-item that was added with this discount.
* **Returns** `string` | `null`

  The translated label of the discount line-item.

---

## [`Shopware\Core\Checkout\Cart\Facade\ErrorsFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ErrorsFacade.php) [​](#errorsfacade)

The ErrorsFacade is a wrapper around the errors of a cart. You can use it to add new errors to the cart or remove existing ones.

### error() [​](#error)

* The `error()` method adds a new error of type `error` to the cart.

  The error will be displayed to the user and the checkout will be blocked if at least one error was added.
* **Arguments:**

  + *`string`* **key**: The snippet-key of the message that should be displayed to the user.
  + *`string` | `null`* **id**: An optional id that can be used to reference the error, if none is provided the $key will be used as id.

    Default: `null`
  + *`array`* **parameters**: Optional: Any parameters that the snippet for the error message may need.

    Default: `array ( )`
* **Examples:**

  + Add a error to the cart.

    twig

    ```shiki
    {% do services.cart.errors.error('NO_PRODUCTS_IN_CART') %}
    ```

### warning() [​](#warning)

* The `warning()` method adds a new error of type `warning` to the cart.

  The warning will be displayed to the user, but the checkout won't be blocked.
* **Arguments:**

  + *`string`* **key**: The snippet-key of the message that should be displayed to the user.
  + *`string` | `null`* **id**: An optional id that can be used to reference the error, if none is provided the $key will be used as id.

    Default: `null`
  + *`array`* **parameters**: Optional: Any parameters that the snippet for the error message may need.

    Default: `array ( )`
* **Examples:**

  + Add a warning to the cart.

    twig

    ```shiki
    {% do services.cart.errors.notice('YOU_SHOULD_REALLY_ADD_PRODUCTS') %}
    ```

### notice() [​](#notice)

* The `notice()` method adds a new error of type `notice` to the cart.

  The notice will be displayed to the user, but the checkout won't be blocked.
* **Arguments:**

  + *`string`* **key**: The snippet-key of the message that should be displayed to the user.
  + *`string` | `null`* **id**: An optional id that can be used to reference the error, if none is provided the $key will be used as id.

    Default: `null`
  + *`array`* **parameters**: Optional: Any parameters that the snippet for the error message may need.

    Default: `array ( )`
* **Examples:**

  + Add a notice to the cart.

    twig

    ```shiki
    {% do services.cart.errors.warning('ADD_PRODUCTS_OR_GO_AWAY') %}
    ```
  + Add a notice to the cart with a custom id.

    twig

    ```shiki
    {% do services.cart.errors.notice('YOU_SHOULD_REALLY_ADD_PRODUCTS', 'add-same-message') %}
    ```
  + Add a notice to the cart with parameters.

    twig

    ```shiki
    {% do services.cart.errors.notice('MESSAGE_WITH_PARAMETERS', null, {'foo': 'bar'}) %}
    ```

### resubmittable() [​](#resubmittable)

* The `resubmittable()` method adds a new error of type `error` to the cart.

  The notice will be displayed to the user, the order will be blocked, but the user can submit the order again.
* **Arguments:**

  + *`string`* **key**: The snippet-key of the message that should be displayed to the user.
  + *`string` | `null`* **id**: An optional id that can be used to reference the error, if none is provided the $key will be used as id.

    Default: `null`
  + *`array`* **parameters**: Optional: Any parameters that the snippet for the error message may need.

    Default: `array ( )`

### has() [​](#has-2)

* The `has()` method, checks if an error with a given id exists.
* **Returns** `bool`

  Returns true if an error with that key exists, false otherwise.
* **Arguments:**

  + *`string`* **id**: The id of the error that should be checked.

### remove() [​](#remove-2)

* The `remove()` method removes the error with the given id.
* **Arguments:**

  + *`string`* **id**: The id of the error that should be removed.

### get() [​](#get-2)

* The `get()` method returns the error with the given id.
* **Returns** [`Shopware\Core\Checkout\Cart\Error\Error`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Error/Error.php) | `null`

  The Error with the given id, null if an error with that id does not exist.
* **Arguments:**

  + *`string`* **id**: The id of the error that should be returned.

---

## [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ItemFacade.php) [​](#itemfacade)

The ItemFacade is a wrapper around one line-item.

### getPrice() [​](#getprice-1)

* `getPrice()` returns the calculated price of the line-item.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference.html#pricefacade) | `null`

  Returns the price of the line-item as a `PriceFacade` or null if the line-item has no calculated price.

### take() [​](#take-1)

* `take()` splits an existing line-item by a given quantity.

  It removes the given quantity from the existing line-item and returns a new line-item with exactly that quantity.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  Returns the new line-item as an `ItemFacade` or null if taking is not possible because the line-item has no sufficient quantity.
* **Arguments:**

  + *`int`* **quantity**: The quantity that should be taken.
  + *`string` | `null`* **key**: Optional: The id of the new line-item. A random UUID will be used if none is provided.

    Default: `null`
* **Examples:**

  + Take a quantity of 2 from an existing product line-item and add it to the cart again.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1'), 5) %}

    {% set product = services.cart.products.get(hook.ids.get('p1')) %}

    {% set split = product.take(2, 'new-key') %}

    {% do services.cart.products.add(split) %}
    ```

### getId() [​](#getid-2)

* `getId()` returns the id of the line-item.
* **Returns** `string`

  Returns the id.

### getReferencedId() [​](#getreferencedid-1)

* `getReferenceId()` returns the id of the referenced entity of the line-item.

  E.g. for product line-items this will return the id of the referenced product.
* **Returns** `string` | `null`

  Returns the id of the referenced entity, or null if no entity is referenced.

### getQuantity() [​](#getquantity-1)

* `getQuantity()` returns the quantity of the line-item.
* **Returns** `int`

  Returns the quantity.

### getLabel() [​](#getlabel-2)

* `getLabel()` returns the translated label of the line-item.
* **Returns** `string` | `null`

  Returns the translated label, or null if none exists.

### getPayload() [​](#getpayload-1)

* `getPayload()` returns the payload of this line-item.
* **Returns** [`Shopware\Core\Framework\Script\Facade\ArrayFacade`](./miscellaneous-script-services-reference.html#arrayfacade)

  Returns the payload as `ArrayFacade`.

### getChildren() [​](#getchildren-1)

* `getChildren()` returns the child line-items of this line-item.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemsFacade`](./cart-manipulation-script-services-reference.html#itemsfacade)

  Returns the children as a `ItemsFacade`, that may be empty if no children exist.

### getType() [​](#gettype-1)

* `getType()` returns the type of this line-item.

  Possible types include `product`, `discount`, `container`, etc.
* **Returns** `string`

  The type of the line-item.

---

## [`Shopware\Core\Checkout\Cart\Facade\ItemsFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ItemsFacade.php) [​](#itemsfacade)

The ItemsFacade is a wrapper around a collection of line-items.

### add() [​](#add-1)

* `add()` adds a line-item to this collection.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)

  Returns the added line-item.
* **Arguments:**

  + *[`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)* **item**: The line-item that should be added.
* **Examples:**

  + Add an absolute discount to the cart.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.items.count <= 0 %}
        {% return %}
    {% endif %}

    {% if services.cart.items.has('my-discount') %}
        {% return %}
    {% endif %}

    {% set price = services.cart.price.create({
        'default': { 'gross': -19.99, 'net': -19.99}
    }) %}

    {% do services.cart.discount('my-discount', 'absolute', price, 'Fancy discount') %}
    ```

### get() [​](#get-3)

* `get()` returns the line-item with the given id from this collection.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  The line-item with the given id, or null if it does not exist.
* **Arguments:**

  + *`string`* **id**: The id of the line-item that should be returned.

### count() [​](#count-2)

* `count()` returns the count of line-items in this collection.

  Note that it does only count the line-items directly in this collection and not child line-items of those.
* **Returns** `int`

  The number of line-items in this collection.

### has() [​](#has-3)

* `has()` checks if a line-item with the given id exists in this collection.
* **Returns** `bool`

  Returns true if the given line-item or a line-item with the given id already exists in the collection, false otherwise.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id or a line-item that should be checked if it already exists in the collection.

### remove() [​](#remove-3)

* `remove()` removes the given line-item or the line-item with the given id from this collection.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id of the line-item or the line-item that should be removed.
* **Examples:**

  + Add and then remove a product line-item from the cart.

    twig

    ```shiki
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% do services.cart.products.remove(hook.ids.get('p1')) %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/PriceFacade.php) [​](#pricefacade)

The PriceFacade is a wrapper around a price.

### getTotal() [​](#gettotal-1)

* `getTotal()` returns the total price for the line-item.
* **Returns** `float`

  The total price as float.

### getUnit() [​](#getunit)

* `getUnit()` returns the unit price for the line-item.

  This is equivalent to the total price of the line-item with the quantity 1.
* **Returns** `float`

  The price per unit as float.

### getQuantity() [​](#getquantity-2)

* `getQuantity()` returns the quantity that was used to calculate the total price.
* **Returns** `int`

  Returns the quantity.

### getTaxes() [​](#gettaxes)

* `getTaxes()` returns the calculated taxes of the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Tax\Struct\CalculatedTaxCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Tax/Struct/CalculatedTaxCollection.php)

  Returns the calculated taxes.

### getRules() [​](#getrules)

* `getRules()` returns the tax rules that were used to calculate the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Tax\Struct\TaxRuleCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Tax/Struct/TaxRuleCollection.php)

  Returns the tax rules.

### change() [​](#change)

* `change()` allows a price overwrite of the current price scope. The provided price will be recalculated over the quantity price calculator to consider quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *[`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)* **price**: The provided price can be a fetched price from the database or generated over the `PriceFactory` statically
* **Examples:**

  + Overwrite prices with a static defined collection

    twig

    ```shiki
    {% do product.calculatedPrices.change([
        { to: 20, price: services.price.create({ 'default': { 'gross': 15, 'net': 15} }) },
        { to: 30, price: services.price.create({ 'default': { 'gross': 10, 'net': 10} }) },
        { to: null, price: services.price.create({ 'default': { 'gross': 5, 'net': 5} }) },
    ]) %}
    ```

### plus() [​](#plus)

* `plus()` allows a price addition of the current price scope. The provided price will be recalculated via the quantity price calculator.

  The provided price is interpreted as a unit price and will be added to the current unit price. The total price is calculated afterwards considering quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *[`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)* **price**: The provided price can be a fetched price from the database or generated over the `PriceFactory` statically
* **Examples:**

  + Plus a static defined price to the existing calculated price

    twig

    ```shiki
    {% set price = services.price.create({
        'default': { 'gross': 1.5, 'net': 1.5}
    }) %}

    {% do product.calculatedPrice.plus(price) %}
    ```

### minus() [​](#minus)

* `minus()` allows a price subtraction of the current price scope. The provided price will be recalculated via the quantity price calculator.

  The provided price is interpreted as a unit price and will reduce to the current unit price. The total price is calculated afterwards considering quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *[`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)* **price**: The provided price can be a fetched price from the database or generated over the `PriceFactory` statically
* **Examples:**

  + Minus a static defined price to the existing calculated price

    twig

    ```shiki
    {% set price = services.price.create({
        'default': { 'gross': 1.5, 'net': 1.5}
    }) %}

    {% do product.calculatedPrice.minus(price) %}
    ```

### discount() [​](#discount-2)

* `discount()` allows a percentage discount calculation of the current price scope. The provided value will be ensured to be negative via `abs(value) * -1`.

  The provided discount is interpreted as a percentage value and will be applied to the unit price and the total price as well.
* **Arguments:**

  + *`float`* **value**: The percentage value of the discount. The value will be ensured to be negative via `abs(value) * -1`.
* **Examples:**

  + Adds a 10% discount to the existing calculated price

    twig

    ```shiki
    {% do product.calculatedPrice.discount(10) %}
    ```

### surcharge() [​](#surcharge-2)

* `surcharge()` allows a percentage surcharge calculation of the current price scope. The provided value will be ensured to be negative via `abs(value)`.

  The provided surcharge is interpreted as a percentage value and will be applied to the unit price and the total price as well.
* **Arguments:**

  + *`float`* **value**: The percentage value of the surcharge. The value will be ensured to be negative via `abs(value)`.
* **Examples:**

  + Adds a 10% surcharge to the existing calculated price

    twig

    ```shiki
    {% do product.calculatedPrice.surcharge(10) %}
    ```

### create() [​](#create-1)

* `create()` creates a new `PriceCollection` based on an array of prices.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)

  Returns the newly created `PriceCollection`.
* **Arguments:**

  + *`array`* **price**: The prices for the new collection, indexed by the currency-id or iso-code of the currency.
* **Examples:**

  + Create a new Price in the default currency.

    twig

    ```shiki
    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}
    ```

---

## [services.price (`Shopware\Core\Checkout\Cart\Facade\PriceFactory`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/PriceFactory.php) [​](#pricefactory)

The PriceFacade is a wrapper around a price.

### create() [​](#create-2)

* `create()` creates a new `PriceCollection` based on an array of prices.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)

  Returns the newly created `PriceCollection`.
* **Arguments:**

  + *`array`* **prices**: The prices for the new collection, indexed by the currency-id or iso-code of the currency.
* **Examples:**

  + Create a new Price in the default currency.

    twig

    ```shiki
    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\ProductsFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ProductsFacade.php) [​](#productsfacade)

The ProductsFacade is a wrapper around a collection of product line-items.

### get() [​](#get-4)

* `get()` returns the product line-item with the given product id.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade) | `null`

  The line-item associated with the given product id, or null if it does not exist.
* **Arguments:**

  + *`string`* **productId**: The id of the product, of which the line-item should be returned.
* **Examples:**

  + Get a product line-item by id.

    twig

    ```shiki
    {% set product = services.cart.products.get(hook.ids.get('p1')) %}
    ```

### add() [​](#add-2)

* `add()` adds a new product line-item to this collection.

  In the case only a product id is provided it will create a new line-item from type product for the given product id.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)

  The newly added product line-item.
* **Arguments:**

  + *`string|\LineItem|\ItemFacade`* **product**: The product that should be added. Either an existing `ItemFacade` or `LineItem` or alternatively the id of a product.
  + *`int`* **quantity**: Optionally provide the quantity with which the product line-item should be created, defaults to 1.

    Default: `1`
* **Examples:**

  + Add a product to the cart by id.

    twig

    ```shiki
    {% do services.cart.products.add(hook.ids.get('p1')) %}
    ```

### create() [​](#create-3)

* `create()` creates a new product line-item for the product with the given id in the given quantity.

  Note that the created line-item will not be added automatically to this collection, use `add()` for that.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference.html#itemfacade)

  The newly created product line-item.
* **Arguments:**

  + *`string`* **productId**: The product id for which a line-item should be created.
  + *`int`* **quantity**: Optionally provide the quantity with which the product line-item should be created, defaults to 1.

    Default: `1`

### count() [​](#count-3)

* `count()` returns the count of line-items in this collection.

  Note that it does only count the line-items directly in this collection and not child line-items of those.
* **Returns** `int`

  The number of line-items in this collection.

### has() [​](#has-4)

* `has()` checks if a line-item with the given id exists in this collection.
* **Returns** `bool`

  Returns true if the given line-item or a line-item with the given id already exists in the collection, false otherwise.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id or a line-item that should be checked if it already exists in the collection.

### remove() [​](#remove-4)

* `remove()` removes the given line-item or the line-item with the given id from this collection.
* **Arguments:**

  + *`string|\ItemFacade`* **id**: The id of the line-item or the line-item that should be removed.
* **Examples:**

  + Add and then remove a product line-item from the cart.

    twig

    ```shiki
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% do services.cart.products.remove(hook.ids.get('p1')) %}
    ```

---

## [`Shopware\Core\Checkout\Cart\Facade\StatesFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/StatesFacade.php) [​](#statesfacade)

The StatesFacade allows access to the current cart states and functions.

### add() [​](#add-3)

* `add()` allows you to add one or multiple states as string values to the cart.

  This can be useful to check if your script did already run and did some manipulations to the cart.
* **Arguments:**

  + *`string`* **states**: One or more strings that will be stored on the cart.

### remove() [​](#remove-5)

* `remove()` removes the given state from the cart, if it existed.
* **Arguments:**

  + *`string`* **state**: The state that should be removed.

### has() [​](#has-5)

* `has()` allows you to check if one or more states are present on the cart.
* **Returns** `bool`

  Returns true if at least one of the passed states is present on the cart, false otherwise.
* **Arguments:**

  + *`string`* **states**: One or more strings that should be checked.

### get() [​](#get-5)

* `get()` returns all states that are present on the cart.
* **Returns** `array`

  An array containing all current states of the cart.

---

---

## Data Loading script services reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/data-loading-script-services-reference.html

# Data Loading script services reference [​](#data-loading-script-services-reference)

## [services.repository (`Shopware\Core\Framework\DataAbstractionLayer\Facade\RepositoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/RepositoryFacade.php) [​](#repositoryfacade)

The `repository` service allows you to query data, that is stored inside shopware. Keep in mind that your app needs to have the correct permissions for the data it queries through this service.

### search() [​](#search)

* The `search()` method allows you to search for Entities that match a given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/EntitySearchResult.php)

  A `EntitySearchResult` including all entities that matched your criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria used for your search.
* **Examples:**

  + Load a single product.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ]
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```
  + Filter the search result.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```
  + Add associations that should be included in the result.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ],
        'associations': {
            'manufacturer': {}
        }
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    {% do page.addExtension('myManufacturer', product.manufacturer) %}
    ```

### ids() [​](#ids)

* The `ids()` method allows you to search for the Ids of Entities that match a given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\IdSearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/IdSearchResult.php)

  A `IdSearchResult` including all entity-ids that matched your criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria used for your search.
* **Examples:**

  + Get the Ids of products with the given ProductNumber.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set productIds = services.repository.ids('product', criteria).ids %}

    {% do page.addArrayExtension('myProductIds', {
        'ids': productIds
    }) %}
    ```

### aggregate() [​](#aggregate)

* The `aggregate()` method allows you to execute aggregations specified in the given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\AggregationResultCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/AggregationResult/AggregationResultCollection.php)

  A `AggregationResultCollection` including the results of the aggregations you specified in the criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to aggregate data on, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria that define your aggregations.
* **Examples:**

  + Aggregate data for multiple entities, e.g. the sum of the gross price of all products.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'aggregations': [
            { 'name': 'sumOfPrices', 'type': 'sum', 'field': 'price.gross' }
        ]
    } %}

    {% set sumResult = services.repository.aggregate('product', criteria).get('sumOfPrices') %}

    {% do page.addArrayExtension('myProductAggregations', {
        'sum': sumResult.getSum
    }) %}
    ```

---

## [services.store (`Shopware\Core\Framework\DataAbstractionLayer\Facade\SalesChannelRepositoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/SalesChannelRepositoryFacade.php) [​](#saleschannelrepositoryfacade)

The `store` service can be used to access publicly available `store-api` data. As the data is publicly available your app does not need any additional permissions to use this service, however querying data and also loading associations is restricted to the entities that are also available through the `store-api`.

Notice that the returned entities are already processed for the storefront, this means that e.g. product prices are already calculated based on the current context.

### search() [​](#search-1)

* The `search()` method allows you to search for Entities that match a given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/EntitySearchResult.php)

  A `EntitySearchResult` including all entities that matched your criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria used for your search.
* **Examples:**

  + Load a single storefront product.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ]
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```
  + Filter the search result.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```
  + Add associations that should be included in the result.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ],
        'associations': {
            'manufacturer': {}
        }
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    {% do page.addExtension('myManufacturer', product.manufacturer) %}
    ```

### ids() [​](#ids-1)

* The `ids()` method allows you to search for the Ids of Entities that match a given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\IdSearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/IdSearchResult.php)

  A `IdSearchResult` including all entity-ids that matched your criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria used for your search.
* **Examples:**

  + Get the Ids of products with the given ProductNumber.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set productIds = services.store.ids('product', criteria).ids %}

    {% do page.addArrayExtension('myProductIds', {
        'ids': productIds
    }) %}
    ```

### aggregate() [​](#aggregate-1)

* The `aggregate()` method allows you to execute aggregations specified in the given criteria.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\AggregationResultCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/AggregationResult/AggregationResultCollection.php)

  A `AggregationResultCollection` including the results of the aggregations you specified in the criteria.
* **Arguments:**

  + *`string`* **entityName**: The name of the Entity you want to aggregate data on, e.g. `product` or `media`.
  + *`array`* **criteria**: The criteria that define your aggregations.
* **Examples:**

  + Aggregate data for multiple entities, e.g. the sum of the children of all products.

    twig

    ```shiki
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'aggregations': [
            { 'name': 'sumOfChildren', 'type': 'sum', 'field': 'childCount' }
        ]
    } %}

    {% set sumResult = services.store.aggregate('product', criteria).get('sumOfChildren') %}

    {% do page.addArrayExtension('myProductAggregations', {
        'sum': sumResult.getSum
    }) %}
    ```

---

---

## Custom Endpoint script services reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/custom-endpoint-script-services-reference.html

# Custom Endpoint script services reference [​](#custom-endpoint-script-services-reference)

## [services.cache (`Shopware\Core\Framework\Adapter\Cache\Script\Facade\CacheInvalidatorFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Adapter/Cache/Script/Facade/CacheInvalidatorFacade.php) [​](#cacheinvalidatorfacade)

The `cache` service allows you to invalidate the cache if some entity is updated.

### invalidate() [​](#invalidate)

* `invalidate()` allows you to invalidate all cache entries with the given tag.
* **Arguments:**

  + *`array`* **tags**: The tags for which all cache entries should be invalidated as array.
* **Examples:**

  + Invalidate a hard coded tag.

    twig

    ```shiki
    {% do services.cache.invalidate(['my-tag']) %}
    ```
  + Build tags based on written entities and invalidate those tags.

    twig

    ```shiki
    {% set ids = hook.event.getIds('product_manufacturer') %}

    {% if ids.empty %}
        {% return %}
    {% endif %}

    {% set tags = [] %}
    {% for id in ids %}
        {% set tags = tags|merge(['my-manufacturer-' ~ id]) %}
    {% endfor %}

    {% do services.cache.invalidate(tags) %}
    ```
  + Build tags if products with a specific property is created and invalidate those tags.

    twig

    ```shiki
    {% set ids = hook.event.getIds('product') %}

    {% set ids = ids.only('insert').with('description', 'parentId') %}
    {% if ids.empty %}
        {% return %}
    {% endif %}

    {% set tags = [] %}
    {% for id in ids %}
        {% set tags = tags|merge(['my-product-' ~ id]) %}
    {% endfor %}

    {% do services.cache.invalidate(tags) %}
    ```

---

## [services.writer (`Shopware\Core\Framework\DataAbstractionLayer\Facade\RepositoryWriterFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/RepositoryWriterFacade.php) [​](#repositorywriterfacade)

The `writer` service allows you to write data, that is stored inside shopware. Keep in mind that your app needs to have the correct permissions for the data it writes through this service.

### upsert() [​](#upsert)

* The `upsert()` method allows you to create or update entities inside the database.

  If you pass an `id` in the payload it will do an update if an entity with that `id` already exists, otherwise it will be a create.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenContainerEvent.php)

  The WriteEvents that were generated by executing the `upsert()`.
* **Arguments:**

  + *`string`* **entityName**: The name of the entity you want to upsert, e.g. `product` or `media`.
  + *`array`* **payload**: The payload you want to upsert, as a list of associative arrays, where each associative array represents the payload for one entity.
* **Examples:**

  + Create a new entity.

    twig

    ```shiki
    {% do services.writer.upsert('tax', [
        { 'name': 'new Tax', 'taxRate': 99.9 }
    ]) %}
    ```
  + Update an existing entity.

    twig

    ```shiki
    {% do services.writer.upsert('product', [
        { 'id':  hook.productId, 'active': true }
    ]) %}
    ```

### delete() [​](#delete)

* The `delete()` method allows you to delete entities from the database.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenContainerEvent.php)

  The WriteEvents that were generated by executing the `delete()`.
* **Arguments:**

  + *`string`* **entityName**: The name of the entity you want to delete, e.g. `product` or `media`.
  + *`array`* **payload**: The primary keys of the entities you want to delete, as a list of associative arrays, associative array represents the primary keys for one entity.
* **Examples:**

  + Delete an entity.

    twig

    ```shiki
    {% do services.writer.delete('product', [
        { 'id':  hook.productId }
    ]) %}
    ```

### sync() [​](#sync)

* The `sync()` method allows you to execute updates and deletes to multiple entities in one method call.
* **Returns** [`Shopware\Core\Framework\Api\Sync\SyncResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Api/Sync/SyncResult.php)

  The result of the `sync()`.
* **Arguments:**

  + *`array`* **payload**: All operations that should be executed.
* **Examples:**

  + Update an entity and delete another one with one `sync()` call.

    twig

    ```shiki
    {% set payload = [
        {
            'entity': 'product',
            'action': 'upsert',
            'payload': [
                { 'id':  hook.updateProductId, 'active': true }
            ]
        },
        {
            'entity': 'product',
            'action': 'delete',
            'payload': [
            { 'id':  hook.deleteProductId }
        ]
        },
    ] %}

    {% do services.writer.sync(payload) %}
    ```

---

## [services.response (`Shopware\Core\Framework\Script\Api\ScriptResponseFactoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponseFactoryFacade.php) [​](#scriptresponsefactoryfacade)

The `response` service allows you to create HTTP-Responses.

### json() [​](#json)

* The `json()` method allows you to create a JSON-Response.
* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object, remember to assign it to the hook with `hook.setResponse()`.
* **Arguments:**

  + *`array`* **data**: The data that should be sent in the response as array.
  + *`int`* **code**: The HTTP-Status-Code of the response, defaults to 200.

    Default: `200`
* **Examples:**

  + Return hard coded values as JsonResponse.

    twig

    ```shiki
    {% set response = services.response.json({ 'foo': 'bar' }) %}
    {% do hook.setResponse(response) %}
    ```
  + Search for products and return them in a JsonResponse.

    twig

    ```shiki
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% set products = services.repository.search('product', hook.request) %}

    {% set response = services.response.json({ 'products': products }) %}
    {% do hook.setResponse(response) %}
    ```
  + Provide a response to a ActionButtons request from the administration.

    twig

    ```shiki
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

### redirect() [​](#redirect)

* The `redirect()` method allows you to create a RedirectResponse.
* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object, remember to assign it to the hook with `hook.setResponse()`.
* **Arguments:**

  + *`string`* **route**: The name of the route that should be redirected to.
  + *`array`* **parameters**: The parameters needing to generate the URL of the route as an associative array.
  + *`int`* **code**: he HTTP-Status-Code of the response, defaults to 302.

    Default: `302`
* **Examples:**

  + Redirect to an Admin-API route.

    twig

    ```shiki
    {% set response = services.response.redirect('api.product.detail', { 'path': productId }) %}
    {% do hook.setResponse(response) %}
    ```
  + Redirect to a storefront page.

    twig

    ```shiki
    {% set response = services.response.redirect('frontend.detail.page', { 'productId': productId }) %}
    {% do hook.setResponse(response) %}
    ```

### render() [​](#render)

* The `render()` method allows you to render a twig view with the parameters you provide and create a StorefrontResponse.

  Note that the `render()` method will throw an exception if it is called from outside a `SalesChannelContext` (e.g. from an `/api` route) or if the Storefront-bundle is not installed.
* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object with the rendered template as content, remember to assign it to the hook with `hook.setResponse()`.
* **Arguments:**

  + *`string`* **view**: The name of the twig template you want to render e.g. `@Storefront/storefront/page/content/detail.html.twig`
  + *`array`* **parameters**: The parameters you want to pass to the template, ensure that you pass the `page` parameter from the hook to the templates.

    Default: `array ( )`
* **Examples:**

  + Fetch a product, add it to the page and return a rendered response.

    twig

    ```shiki
    {% set product = services.store.search('product', { 'ids': [productId]}).first %}

    {% do hook.page.addExtension('myProduct', product) %}

    {% set response = services.response.render('@MyApp/storefront/page/custom-page/index.html.twig', { 'page': hook.page }) %}
    {% do response.setHeader("Content-Type", "text/plain") %}

    {% do hook.setResponse(response) %}
    ```

---

---

## Miscellaneous script services reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/miscellaneous-script-services-reference.html

# Miscellaneous script services reference [​](#miscellaneous-script-services-reference)

## [services.request (`Shopware\Core\Framework\Routing\Facade\RequestFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Routing/Facade/RequestFacade.php) [​](#requestfacade)

The `request` service allows you to access the current request in the script Examples:

twig

```shiki
{% block response %}
 {% if services.request.method != "POST" %}
     {% set response = services.response.json({
         'error': 'Only POST requests are allowed',
     }, 405) %}
     {% do hook.setResponse(response) %}
     {% return %}
 {% endif %}

 {% set response = services.response.json(services.request.request) %}
 {% do hook.setResponse(response) %}
{% endblock %}
```

### ip() [​](#ip)

* The ip method returns the real client ip address
* **Returns** `string` | `null`

  request client ip address

### scheme() [​](#scheme)

* The scheme method returns the request scheme
* **Returns** `string`

  request scheme

### method() [​](#method)

* The method returns the request method in upper case
* **Returns** `string`

  request method in upper case

### uri() [​](#uri)

* The method `uri` returns the request uri with the resolved url
* **Returns** `string`

  request uri

### pathInfo() [​](#pathinfo)

* The method `pathInfo` returns the request path info. The path info can be also an internal link when a seo url is used.
* **Returns** `string`

  request path info

### query() [​](#query)

* The method `query` returns all query parameters as an array
* **Returns** `array`

  request query parameters

### request() [​](#request)

* The method `request` returns all post parameters as an array.

  On `application/json` requests this contains also the json body parsed as an array.
* **Returns** `array`

  request post parameters

### headers() [​](#headers)

* The method `headers` returns all request headers as an array.

  It is possible to access only the following headers: content-type, content-length, accept, accept-language, user-agent, referer
* **Returns** `array`

  request headers

### cookies() [​](#cookies)

* The method `cookies` returns all request cookies as an array.
* **Returns** `array`

  request cookies

---

## [`Shopware\Core\Framework\Script\Facade\ArrayFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Facade/ArrayFacade.php) [​](#arrayfacade)

The ArrayFacade acts as a wrapper around an array and allows easier manipulation of arrays inside scripts. An array facade can also be accessed like a "normal" array inside twig. Examples:

twig

```shiki
{% do array.push('test') %}

{% do array.foo = 'bar' }

{% do array.has('foo') }

{% if array.foo === 'bar' %}

{% foreach array as key => value %}
```

### set() [​](#set)

* `set()` adds a new element to the array using the given key.
* **Arguments:**

  + *`string|int`* **key**: The array key.
  + *`mixed`* **value**: The value that should be added.
* **Examples:**

  + Add a new element with key `test` and value 1.

    twig

    ```shiki
    {% set product = services.cart.products.get(hook.ids.get('p1')) %}

    {% do product.payload.set('test', 1) %}
    ```

### push() [​](#push)

* `push()` adds a new value to the end of the array.
* **Arguments:**

  + *`mixed`* **value**: The value that should be added.

### removeBy() [​](#removeby)

* `removeBy()` removes the value at the given index from the array.
* **Arguments:**

  + *`string|int`* **index**: The index that should be removed.

### remove() [​](#remove)

* `remove()` removes the given value from the array. It does nothing if the provided value does not exist in the array.
* **Arguments:**

  + *`mixed`* **value**: The value that should be removed.

### reset() [​](#reset)

* `reset()` removes all entries from the array.

### merge() [​](#merge)

* `merge()` recursively merges the array with the given array.
* **Arguments:**

  + *`array&lt;string|int,mixed&gt;|\ArrayFacade`* **array**: The array that should be merged with this array. Either a plain `array` or another `ArrayFacade`.
* **Examples:**

  + Merge two arrays.

    twig

    ```shiki
    {% set my_array = array({'bar': 'foo', 'baz': true}) %}

    {% do product.payload.merge(my_array) %}
    ```

### replace() [​](#replace)

* `replace()` recursively replaces elements from the given array into this array.
* **Arguments:**

  + *`array&lt;string|int,mixed&gt;|\ArrayFacade`* **array**: The array from which the elements should be replaced into this array. Either a plain `array` or another `ArrayFacade`.
* **Examples:**

  + Replace elements in the product payload array.

    twig

    ```shiki
    {% set second = array({'bar': 'baz'}) %}

    {% do product.payload.replace(second) %}
    ```

### count() [​](#count)

* `count()` returns the count of elements inside this array.
* **Returns** `int`

  Returns the count of elements.

### all() [​](#all)

* `all()` function returns all elements of this array.
* **Returns** `array`

  Returns all elements of this array.

---

## [services.config (`Shopware\Core\System\SystemConfig\Facade\SystemConfigFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SystemConfig/Facade/SystemConfigFacade.php) [​](#systemconfigfacade)

The `config` service allows you to access the shop's and your app's configuration values.

### get() [​](#get)

* The `get()` method allows you to access all config values of the store.

  Notice that your app needs the `system_config:read` privilege to use this method.
* **Returns** `array|bool|float|int|string|null`
* **Arguments:**

  + *`string`* **key**: The key of the configuration value e.g. `core.listing.defaultSorting`.
  + *`string` | `null`* **salesChannelId**: The SalesChannelId if you need the config value for a specific SalesChannel, if you don't provide a SalesChannelId, the one of the current Context is used as default.

    Default: `null`
* **Examples:**

  + Read an arbitrary system\_config value.

    twig

    ```shiki
    {% set systemConfig = services.config.get('core.listing.productsPerPage') %}
    ```

### app() [​](#app)

* The `app()` method allows you to access the config values your app's configuration.

  Notice that your app does not need any additional privileges to use this method, as you can only access your own app's configuration.
* **Returns** `array|bool|float|int|string|null`
* **Arguments:**

  + *`string`* **key**: The name of the configuration value specified in the config.xml e.g. `exampleTextField`.
  + *`string` | `null`* **salesChannelId**: The SalesChannelId if you need the config value for a specific SalesChannel, if you don't provide a SalesChannelId, the one of the current Context is used as default.

    Default: `null`
* **Examples:**

  + Read your app's config value.

    twig

    ```shiki
    {% set appConfig = services.config.app('app_config') %}
    ```

---

---

## Script hooks reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/script-hooks-reference.html

# List of all available Hooks for Scripts [​](#list-of-all-available-hooks-for-scripts)

## Data Loading [​](#data-loading)

All available Hooks that can be used to load additional data.

### payment-method-route-request [​](#payment-method-route-request)

|  |  |
| --- | --- |
| **Name** | payment-method-route-request |
| **Since** | 6.5.0.0 |
| **Class** | `Shopware\Core\Checkout\Payment\Hook\PaymentMethodRouteHook` |
| **Description** | Triggered when PaymentMethodRoute is requested |
| **Available Data** | collection: [`Shopware\Core\Checkout\Payment\PaymentMethodCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Payment/PaymentMethodCollection.php) onlyAvailable: `bool` salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) |
| **Stoppable** | `false` |

### shipping-method-route-request [​](#shipping-method-route-request)

|  |  |
| --- | --- |
| **Name** | shipping-method-route-request |
| **Since** | 6.5.0.0 |
| **Class** | `Shopware\Core\Checkout\Shipping\Hook\ShippingMethodRouteHook` |
| **Description** | Triggered when ShippingMethodRoute is requested |
| **Available Data** | collection: [`Shopware\Core\Checkout\Shipping\ShippingMethodCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Shipping/ShippingMethodCollection.php) onlyAvailable: `bool` salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) |
| **Stoppable** | `false` |

### product-reviews-widget-loaded [​](#product-reviews-widget-loaded)

|  |  |
| --- | --- |
| **Name** | product-reviews-widget-loaded |
| **Since** | 6.6.9.0 |
| **Class** | `Shopware\Core\Content\Product\SalesChannel\Review\ProductReviewsWidgetLoadedHook` |
| **Description** | Triggered when the ProductReviewsWidget is loaded |
| **Available Data** | reviews: [`Shopware\Core\Content\Product\SalesChannel\Review\ProductReviewResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/SalesChannel/Review/ProductReviewResult.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) |
| **Stoppable** | `false` |

### customer-group-registration-page-loaded [​](#customer-group-registration-page-loaded)

|  |  |
| --- | --- |
| **Name** | customer-group-registration-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\CustomerGroupRegistration\CustomerGroupRegistrationPageLoadedHook` |
| **Description** | Triggered when the CustomerGroupRegistrationPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\CustomerGroupRegistration\CustomerGroupRegistrationPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/CustomerGroupRegistration/CustomerGroupRegistrationPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-guest-login-page-loaded [​](#account-guest-login-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-guest-login-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Login\AccountGuestLoginPageLoadedHook` |
| **Description** | Triggered when the AccountGuestLoginPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Login\AccountLoginPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Login/AccountLoginPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-login-page-loaded [​](#account-login-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-login-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Login\AccountLoginPageLoadedHook` |
| **Description** | Triggered when the AccountLoginPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Login\AccountLoginPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Login/AccountLoginPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-edit-order-page-loaded [​](#account-edit-order-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-edit-order-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Order\AccountEditOrderPageLoadedHook` |
| **Description** | Triggered when the AccountEditOrderPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Order\AccountEditOrderPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountEditOrderPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-order-detail-page-loaded [​](#account-order-detail-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-order-detail-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Order\AccountOrderDetailPageLoadedHook` |
| **Description** | Triggered when the AccountOrderDetailPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Order\AccountOrderDetailPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountOrderDetailPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-order-page-loaded [​](#account-order-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-order-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Order\AccountOrderPageLoadedHook` |
| **Description** | Triggered when the AccountOrderPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Order\AccountOrderPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountOrderPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-overview-page-loaded [​](#account-overview-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-overview-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Overview\AccountOverviewPageLoadedHook` |
| **Description** | Triggered when the AccountOverviewPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Overview\AccountOverviewPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Overview/AccountOverviewPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-profile-page-loaded [​](#account-profile-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-profile-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Profile\AccountProfilePageLoadedHook` |
| **Description** | Triggered when the AccountProfilePage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Profile\AccountProfilePage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Profile/AccountProfilePage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-recover-password-page-loaded [​](#account-recover-password-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-recover-password-page-loaded |
| **Since** | 6.4.13.0 |
| **Class** | `Shopware\Storefront\Page\Account\RecoverPassword\AccountRecoverPasswordPageLoadedHook` |
| **Description** | Triggered when the AccountRecoverPasswordPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\RecoverPassword\AccountRecoverPasswordPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/RecoverPassword/AccountRecoverPasswordPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### account-register-page-loaded [​](#account-register-page-loaded)

|  |  |
| --- | --- |
| **Name** | account-register-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Account\Register\AccountRegisterPageLoadedHook` |
| **Description** | Triggered when the AccountLoginPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Account\Login\AccountLoginPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Login/AccountLoginPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### address-detail-page-loaded [​](#address-detail-page-loaded)

|  |  |
| --- | --- |
| **Name** | address-detail-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Address\Detail\AddressDetailPageLoadedHook` |
| **Description** | Triggered when the AddressDetailPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Address\Detail\AddressDetailPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Address/Detail/AddressDetailPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### address-book-widget-loaded [​](#address-book-widget-loaded)

|  |  |
| --- | --- |
| **Name** | address-book-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Address\Listing\AddressBookWidgetLoadedHook` |
| **Description** | Triggered when the AddressBookWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Address\Listing\AddressListingPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Address/Listing/AddressListingPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### address-listing-page-loaded [​](#address-listing-page-loaded)

|  |  |
| --- | --- |
| **Name** | address-listing-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Address\Listing\AddressListingPageLoadedHook` |
| **Description** | Triggered when the AddressListingPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Address\Listing\AddressListingPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Address/Listing/AddressListingPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-cart-page-loaded [​](#checkout-cart-page-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-cart-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Cart\CheckoutCartPageLoadedHook` |
| **Description** | Triggered when the CheckoutCartPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Cart\CheckoutCartPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Cart/CheckoutCartPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-confirm-page-loaded [​](#checkout-confirm-page-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-confirm-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Confirm\CheckoutConfirmPageLoadedHook` |
| **Description** | Triggered when the CheckoutConfirmPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Confirm\CheckoutConfirmPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Confirm/CheckoutConfirmPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-finish-page-loaded [​](#checkout-finish-page-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-finish-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Finish\CheckoutFinishPageLoadedHook` |
| **Description** | Triggered when the CheckoutFinishPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Finish\CheckoutFinishPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Finish/CheckoutFinishPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-info-widget-loaded [​](#checkout-info-widget-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-info-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Offcanvas\CheckoutInfoWidgetLoadedHook` |
| **Description** | Triggered when the CheckoutInfoWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Offcanvas\OffcanvasCartPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Offcanvas/OffcanvasCartPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-offcanvas-widget-loaded [​](#checkout-offcanvas-widget-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-offcanvas-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Offcanvas\CheckoutOffcanvasWidgetLoadedHook` |
| **Description** | Triggered when the CheckoutOffcanvasWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Offcanvas\OffcanvasCartPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Offcanvas/OffcanvasCartPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### checkout-register-page-loaded [​](#checkout-register-page-loaded)

|  |  |
| --- | --- |
| **Name** | checkout-register-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Checkout\Register\CheckoutRegisterPageLoadedHook` |
| **Description** | Triggered when the CheckoutRegisterPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Checkout\Register\CheckoutRegisterPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Checkout/Register/CheckoutRegisterPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### cms-page-loaded [​](#cms-page-loaded)

|  |  |
| --- | --- |
| **Name** | cms-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Cms\CmsPageLoadedHook` |
| **Description** | Triggered when a CmsPage is loaded |
| **Available Data** | page: [`Shopware\Core\Content\Cms\CmsPageEntity`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Cms/CmsPageEntity.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### landing-page-loaded [​](#landing-page-loaded)

|  |  |
| --- | --- |
| **Name** | landing-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\LandingPage\LandingPageLoadedHook` |
| **Description** | Triggered when the LandingPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\LandingPage\LandingPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/LandingPage/LandingPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### maintenance-page-loaded [​](#maintenance-page-loaded)

|  |  |
| --- | --- |
| **Name** | maintenance-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Maintenance\MaintenancePageLoadedHook` |
| **Description** | Triggered when the MaintenancePage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Maintenance\MaintenancePage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Maintenance/MaintenancePage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### navigation-page-loaded [​](#navigation-page-loaded)

|  |  |
| --- | --- |
| **Name** | navigation-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Navigation\NavigationPageLoadedHook` |
| **Description** | Triggered when the NavigationPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Navigation\NavigationPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Navigation/NavigationPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### product-page-loaded [​](#product-page-loaded)

|  |  |
| --- | --- |
| **Name** | product-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Product\ProductPageLoadedHook` |
| **Description** | Triggered when the ProductPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Product\ProductPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Product/ProductPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### product-quick-view-widget-loaded [​](#product-quick-view-widget-loaded)

|  |  |
| --- | --- |
| **Name** | product-quick-view-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Product\QuickView\ProductQuickViewWidgetLoadedHook` |
| **Description** | Triggered when the ProductQuickViewWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Product\QuickView\MinimalQuickViewPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Product/QuickView/MinimalQuickViewPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### search-page-loaded [​](#search-page-loaded)

|  |  |
| --- | --- |
| **Name** | search-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Search\SearchPageLoadedHook` |
| **Description** | Triggered when the SearchPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Search\SearchPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Search/SearchPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### search-widget-loaded [​](#search-widget-loaded)

|  |  |
| --- | --- |
| **Name** | search-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Search\SearchWidgetLoadedHook` |
| **Description** | Triggered when the SearchWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Search\SearchPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Search/SearchPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### sitemap-page-loaded [​](#sitemap-page-loaded)

|  |  |
| --- | --- |
| **Name** | sitemap-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Sitemap\SitemapPageLoadedHook` |
| **Description** | Triggered when the SitemapPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Sitemap\SitemapPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Sitemap/SitemapPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### suggest-page-loaded [​](#suggest-page-loaded)

|  |  |
| --- | --- |
| **Name** | suggest-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Suggest\SuggestPageLoadedHook` |
| **Description** | Triggered when the SuggestPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Suggest\SuggestPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Suggest/SuggestPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### guest-wishlist-page-loaded [​](#guest-wishlist-page-loaded)

|  |  |
| --- | --- |
| **Name** | guest-wishlist-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Wishlist\GuestWishlistPageLoadedHook` |
| **Description** | Triggered when the GuestWishlistPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Wishlist\GuestWishlistPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Wishlist/GuestWishlistPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### wishlist-page-loaded [​](#wishlist-page-loaded)

|  |  |
| --- | --- |
| **Name** | wishlist-page-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Wishlist\WishlistPageLoadedHook` |
| **Description** | Triggered when the WishlistPage is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Wishlist\WishlistPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Wishlist/WishlistPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### wishlist-widget-loaded [​](#wishlist-widget-loaded)

|  |  |
| --- | --- |
| **Name** | wishlist-widget-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Page\Wishlist\WishlistWidgetLoadedHook` |
| **Description** | Triggered when the WishlistWidget is loaded |
| **Available Data** | page: [`Shopware\Storefront\Page\Wishlist\WishlistPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Wishlist/WishlistPage.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### country-state-data-pagelet-loaded [​](#country-state-data-pagelet-loaded)

|  |  |
| --- | --- |
| **Name** | country-state-data-pagelet-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Pagelet\Country\CountryStateDataPageletLoadedHook` |
| **Description** | Triggered when the CountryStateDataPagelet is loaded |
| **Available Data** | pagelet: [`Shopware\Storefront\Pagelet\Country\CountryStateDataPagelet`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Country/CountryStateDataPagelet.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### footer-pagelet-loaded [​](#footer-pagelet-loaded)

|  |  |
| --- | --- |
| **Name** | footer-pagelet-loaded |
| **Since** | 6.7.0.0 |
| **Class** | `Shopware\Storefront\Pagelet\Footer\FooterPageletLoadedHook` |
| **Description** | Triggered when the FooterPagelet is loaded |
| **Available Data** | page: [`Shopware\Storefront\Pagelet\Footer\FooterPagelet`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Footer/FooterPagelet.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### header-pagelet-loaded [​](#header-pagelet-loaded)

|  |  |
| --- | --- |
| **Name** | header-pagelet-loaded |
| **Since** | 6.7.0.0 |
| **Class** | `Shopware\Storefront\Pagelet\Header\HeaderPageletLoadedHook` |
| **Description** | Triggered when the HeaderPagelet is loaded |
| **Available Data** | page: [`Shopware\Storefront\Pagelet\Header\HeaderPagelet`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Header/HeaderPagelet.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### menu-offcanvas-pagelet-loaded [​](#menu-offcanvas-pagelet-loaded)

|  |  |
| --- | --- |
| **Name** | menu-offcanvas-pagelet-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Pagelet\Menu\Offcanvas\MenuOffcanvasPageletLoadedHook` |
| **Description** | Triggered when the MenuOffcanvasPagelet is loaded |
| **Available Data** | page: [`Shopware\Storefront\Pagelet\Menu\Offcanvas\MenuOffcanvasPagelet`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Menu/Offcanvas/MenuOffcanvasPagelet.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

### guest-wishlist-pagelet-loaded [​](#guest-wishlist-pagelet-loaded)

|  |  |
| --- | --- |
| **Name** | guest-wishlist-pagelet-loaded |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Storefront\Pagelet\Wishlist\GuestWishlistPageletLoadedHook` |
| **Description** | Triggered when the GuestWishlistPagelet is loaded |
| **Available Data** | page: [`Shopware\Storefront\Pagelet\Wishlist\GuestWishlistPagelet`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Wishlist/GuestWishlistPagelet.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `false` |

## Cart Manipulation [​](#cart-manipulation)

All available Hooks that can be used to manipulate the cart.

### cart [​](#cart)

|  |  |
| --- | --- |
| **Name** | cart |
| **Since** | 6.4.8.0 |
| **Class** | `Shopware\Core\Checkout\Cart\Hook\CartHook` |
| **Description** | Triggered during the cart calculation process. |
| **Available Data** | salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) cart: [`Shopware\Core\Checkout\Cart\Cart`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Cart.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [cart](./cart-manipulation-script-services-reference.html#CartFacade) [price](./cart-manipulation-script-services-reference.html#PriceFactory) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) |
| **Stoppable** | `false` |

## Custom API endpoint [​](#custom-api-endpoint)

All available hooks within the Store-API and API

### cache-invalidation [​](#cache-invalidation)

|  |  |
| --- | --- |
| **Name** | cache-invalidation |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\Adapter\Cache\Script\CacheInvalidationHook` |
| **Description** | Triggered whenever an entity is written. |
| **Available Data** | event: [`Shopware\Core\Framework\Adapter\Cache\Script\Facade\WrittenEventScriptFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Adapter/Cache/Script/Facade/WrittenEventScriptFacade.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [cache](./custom-endpoint-script-services-reference.html#CacheInvalidatorFacade) |
| **Stoppable** | `false` |

### api- [​](#api)

|  |  |
| --- | --- |
| **Name** | api- |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\Script\Api\ApiHook` |
| **Description** | Triggered when the api endpoint /api/script/{hook} is called |
| **Available Data** | name: `string` request: `array` context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) scriptResponse: [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php) isPropagationStopped: `bool` |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [response](./custom-endpoint-script-services-reference.html#ScriptResponseFactoryFacade) |
| **Stoppable** | `true` |

#### response [​](#response)

|  |  |
| --- | --- |
| **Name** | response |
| **Since** | 6.6.10.4 |
| **Class** | `Shopware\Core\Framework\Script\Api\ResponseHook` |
| **Description** | Triggered on every response |
| **Available Data** | routeName: `string` routeScopes: `array` context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** |  |
| **Stoppable** | `false` |

### store-api- [​](#store-api)

**Interface Hook**

Triggered when the api endpoint /store-api/script/{hook} is called. Used to execute your logic and provide a response to the request.

#### Function: `cache_key` [​](#function-cache-key)

|  |  |
| --- | --- |
| **Name** | cache\_key |
| **Since** | 6.4.9.0 |
| **Optional** | `true` |
| **Class** | `Shopware\Core\Framework\Script\Api\StoreApiCacheKeyHook` |
| **Description** | Triggered when the api endpoint /store-api/script/{hook} is called. Used to provide a cache-key based on the request. Needs to be implemented when your store-api route should be cached. |
| **Available Data** | cacheKey: `string` name: `string` request: `array` query: `array` salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) isPropagationStopped: `bool` |
| **Available Services** |  |
| **Stoppable** | `true` |

#### Function: `response` [​](#function-response)

|  |  |
| --- | --- |
| **Name** | response |
| **Since** | 6.4.9.0 |
| **Optional** | `false` |
| **Class** | `Shopware\Core\Framework\Script\Api\StoreApiResponseHook` |
| **Description** | Triggered when the api endpoint /store-api/script/{hook} is called. Used to provide the HTTP-Response. This function is only called when no response for the provided cache key is cached, or no `cache_key` function implemented. |
| **Available Data** | name: `string` request: `array` query: `array` salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) scriptResponse: [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php) isPropagationStopped: `bool` |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) [response](./custom-endpoint-script-services-reference.html#ScriptResponseFactoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `true` |

### storefront- [​](#storefront)

|  |  |
| --- | --- |
| **Name** | storefront- |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Storefront\Framework\Script\Api\StorefrontHook` |
| **Description** | Triggered when the storefront endpoint /storefront/script/{hook} is called |
| **Available Data** | script: `string` request: `array` query: `array` page: [`Shopware\Storefront\Page\Page`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Page.php) salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) scriptResponse: [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php) isPropagationStopped: `bool` |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) [response](./custom-endpoint-script-services-reference.html#ScriptResponseFactoryFacade) [request](./miscellaneous-script-services-reference.html#RequestFacade) |
| **Stoppable** | `true` |

## App Lifecycle [​](#app-lifecycle)

All available hooks that can be used to execute scripts during your app's lifecycle.

### app-activated [​](#app-activated)

|  |  |
| --- | --- |
| **Name** | app-activated |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\App\Event\Hooks\AppActivatedHook` |
| **Description** | Triggered when your app is activated. |
| **Available Data** | event: [`Shopware\Core\Framework\App\Event\AppActivatedEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Event/AppActivatedEvent.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) |
| **Stoppable** | `false` |

### app-deactivated [​](#app-deactivated)

|  |  |
| --- | --- |
| **Name** | app-deactivated |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\App\Event\Hooks\AppDeactivatedHook` |
| **Description** | Triggered when your app is deactivated. |
| **Available Data** | event: [`Shopware\Core\Framework\App\Event\AppDeactivatedEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Event/AppDeactivatedEvent.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) |
| **Stoppable** | `false` |

### app-deleted [​](#app-deleted)

|  |  |
| --- | --- |
| **Name** | app-deleted |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\App\Event\Hooks\AppDeletedHook` |
| **Description** | Triggered when your app is deleted. |
| **Available Data** | event: [`Shopware\Core\Framework\App\Event\AppDeletedEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Event/AppDeletedEvent.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) |
| **Stoppable** | `false` |

### app-installed [​](#app-installed)

|  |  |
| --- | --- |
| **Name** | app-installed |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\App\Event\Hooks\AppInstalledHook` |
| **Description** | Triggered when your app is installed. |
| **Available Data** | event: [`Shopware\Core\Framework\App\Event\AppInstalledEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Event/AppInstalledEvent.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) |
| **Stoppable** | `false` |

### app-updated [​](#app-updated)

|  |  |
| --- | --- |
| **Name** | app-updated |
| **Since** | 6.4.9.0 |
| **Class** | `Shopware\Core\Framework\App\Event\Hooks\AppUpdatedHook` |
| **Description** | Triggered when your app is updated. |
| **Available Data** | event: [`Shopware\Core\Framework\App\Event\AppUpdatedEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Event/AppUpdatedEvent.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [writer](./custom-endpoint-script-services-reference.html#RepositoryWriterFacade) |
| **Stoppable** | `false` |

## Product [​](#product)

All available hooks that can be used to manipulate products.

### product-pricing [​](#product-pricing)

|  |  |
| --- | --- |
| **Name** | product-pricing |
| **Since** | 6.5.1.0 |
| **Class** | `Shopware\Core\Content\Product\Hook\Pricing\ProductPricingHook` |
| **Description** | Triggered when product prices are calculated for the store |
| **Available Data** | products: `array` salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php) context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php) |
| **Available Services** | [repository](./data-loading-script-services-reference.html#RepositoryFacade) [price](./cart-manipulation-script-services-reference.html#PriceFactory) [config](./miscellaneous-script-services-reference.html#SystemConfigFacade) [store](./data-loading-script-services-reference.html#SalesChannelRepositoryFacade) |
| **Stoppable** | `false` |

---

## Product script services reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/script-reference/product-script-services-reference.html

# Product script services reference [​](#product-script-services-reference)

## [`Shopware\Core\Content\Product\Hook\Pricing\CheapestPriceFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Hook/Pricing/CheapestPriceFacade.php) [​](#cheapestpricefacade)

The CheapestPriceFacade is a wrapper around the cheapest price of the product.

### reset() [​](#reset)

* `reset()` allows to reset the cheapest price to the original price of the product.
* **Examples:**

  + Reset the product price to default

    twig

    ```shiki
    {% do variant.calculatedCheapestPrice.change(price) %}
    ```

### change() [​](#change)

* `change()` allows to overwrite the cheapest price of the current price scope. The provided price will be recalculated over the quantity price calculator to consider quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *`\PriceFacade|\PriceCollection|\CalculatedPrice|null` | `null`* **price**: You can provide different values to overwrite the cheapest price. In case of null, it uses the original single price of the product.
  + *`bool`* **range**: Allows to switch the `hasRange` attribute of the cheapest price

    Default: `false`
* **Examples:**

  + Overwrite prices with a static defined collection

    twig

    ```shiki
    {% set price = services.price.create({
        'default': { 'gross': 15, 'net': 15}
    }) %}

    {% do variant.calculatedCheapestPrice.change(price) %}
    ```
  + Overwrite the cheapest price with the original price

    twig

    ```shiki
    {% do variant.calculatedCheapestPrice.plus(price) %}
    ```
  + Discount the cheapest price by 10%

    twig

    ```shiki
    {% do variant.calculatedCheapestPrice.discount(10) %}
    ```

### getTotal() [​](#gettotal)

* `getTotal()` returns the total price for the line-item.
* **Returns** `float`

  The total price as float.

### getUnit() [​](#getunit)

* `getUnit()` returns the unit price for the line-item.

  This is equivalent to the total price of the line-item with the quantity 1.
* **Returns** `float`

  The price per unit as float.

### getQuantity() [​](#getquantity)

* `getQuantity()` returns the quantity that was used to calculate the total price.
* **Returns** `int`

  Returns the quantity.

### getTaxes() [​](#gettaxes)

* `getTaxes()` returns the calculated taxes of the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Tax\Struct\CalculatedTaxCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Tax/Struct/CalculatedTaxCollection.php)

  Returns the calculated taxes.

### getRules() [​](#getrules)

* `getRules()` returns the tax rules that were used to calculate the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Tax\Struct\TaxRuleCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Tax/Struct/TaxRuleCollection.php)

  Returns the tax rules.

### plus() [​](#plus)

* `plus()` allows a price addition of the current price scope. The provided price will be recalculated via the quantity price calculator.

  The provided price is interpreted as a unit price and will be added to the current unit price. The total price is calculated afterwards considering quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *[`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)* **price**: The provided price can be a fetched price from the database or generated over the `PriceFactory` statically
* **Examples:**

  + Plus a static defined price to the existing calculated price

    twig

    ```shiki
    {% set price = services.price.create({
        'default': { 'gross': 1.5, 'net': 1.5}
    }) %}

    {% do product.calculatedPrice.plus(price) %}
    ```

### minus() [​](#minus)

* `minus()` allows a price subtraction of the current price scope. The provided price will be recalculated via the quantity price calculator.

  The provided price is interpreted as a unit price and will reduce to the current unit price. The total price is calculated afterwards considering quantity, tax rule and cash rounding configurations.
* **Arguments:**

  + *[`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)* **price**: The provided price can be a fetched price from the database or generated over the `PriceFactory` statically
* **Examples:**

  + Minus a static defined price to the existing calculated price

    twig

    ```shiki
    {% set price = services.price.create({
        'default': { 'gross': 1.5, 'net': 1.5}
    }) %}

    {% do product.calculatedPrice.minus(price) %}
    ```

### discount() [​](#discount)

* `discount()` allows a percentage discount calculation of the current price scope. The provided value will be ensured to be negative via `abs(value) * -1`.

  The provided discount is interpreted as a percentage value and will be applied to the unit price and the total price as well.
* **Arguments:**

  + *`float`* **value**: The percentage value of the discount. The value will be ensured to be negative via `abs(value) * -1`.
* **Examples:**

  + Adds a 10% discount to the existing calculated price

    twig

    ```shiki
    {% do product.calculatedPrice.discount(10) %}
    ```

### surcharge() [​](#surcharge)

* `surcharge()` allows a percentage surcharge calculation of the current price scope. The provided value will be ensured to be negative via `abs(value)`.

  The provided surcharge is interpreted as a percentage value and will be applied to the unit price and the total price as well.
* **Arguments:**

  + *`float`* **value**: The percentage value of the surcharge. The value will be ensured to be negative via `abs(value)`.
* **Examples:**

  + Adds a 10% surcharge to the existing calculated price

    twig

    ```shiki
    {% do product.calculatedPrice.surcharge(10) %}
    ```

### create() [​](#create)

* `create()` creates a new `PriceCollection` based on an array of prices.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)

  Returns the newly created `PriceCollection`.
* **Arguments:**

  + *`array`* **price**: The prices for the new collection, indexed by the currency-id or iso-code of the currency.
* **Examples:**

  + Create a new Price in the default currency.

    twig

    ```shiki
    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}
    ```

---

## [`Shopware\Core\Content\Product\Hook\Pricing\PriceCollectionFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Hook/Pricing/PriceCollectionFacade.php) [​](#pricecollectionfacade)

The PriceCollectionFacade is a wrapper around the calculated price collection of a product. It allows to manipulate the quantity prices by resetting or changing the price collection.

### reset() [​](#reset-1)

* The `reset()` functions allows to reset the complete price collection.

### change() [​](#change-1)

* The `change()` function allows a complete overwrite of the product quantity prices
* **Arguments:**

  + *`array`* **changes**:
* **Examples:**

  + Overwrite the product prices with a new quantity price graduation

    twig

    ```shiki
    {% do product.calculatedPrices.change([
        { to: 20, price: services.price.create({ 'default': { 'gross': 15, 'net': 15} }) },
        { to: 30, price: services.price.create({ 'default': { 'gross': 10, 'net': 10} }) },
        { to: null, price: services.price.create({ 'default': { 'gross': 5, 'net': 5} }) },
    ]) %}
    ```

### count() [​](#count)

* The `count()` function returns the number of prices which are stored inside this collection.
* **Returns** `int`

  Returns the number of prices which are stored inside this collection

---

## [`Shopware\Core\Content\Product\Hook\Pricing\ProductProxy`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Hook/Pricing/ProductProxy.php) [​](#productproxy)

The `ProductProxy` is a wrapper for the `SalesChannelProductEntity`. It provides access to all properties of the product, but also wraps some data into helper facade classes like `PriceFacade` or `PriceCollectionFacade`.

### \_\_get() [​](#get)

* The `__get()` function allows access to all properties of the [SalesChannelProductEntity](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/SalesChannel/SalesChannelProductEntity.php)
* **Returns** `mixed` | `null`

  Returns the value of the property. The value is `mixed` due to the fact that all properties are accessed via `__get()`
* **Arguments:**

  + *`string`* **name**: Name of the property to access
* **Examples:**

  + Access the product properties

    twig

    ```shiki
    { to: 30, price: services.price.create({ 'default': { 'gross': 10, 'net': 10} }) },
        { to: null, price: services.price.create({ 'default': { 'gross': 5, 'net': 5} }) },
    ]) %}
    ```

### calculatedCheapestPrice() [​](#calculatedcheapestprice)

* The `calculatedCheapestPrice` property returns the cheapest price of the product. The price object will be wrapped into a `PriceFacade` object which allows to manipulate the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference.html#pricefacade) | `null`

  Returns a `PriceFacade` if the product has a calculated cheapest price, otherwise `null`

### calculatedPrice() [​](#calculatedprice)

* The `calculatedPrice` property returns the price of the product. The price object will be wrapped into a `PriceFacade` object which allows to manipulate the price.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference.html#pricefacade) | `null`

  Returns a `PriceFacade` if the product has a price, otherwise `null`

### calculatedPrices() [​](#calculatedprices)

* The `calculatedPrices` property returns the price of the product. The price object will be wrapped into a `PriceCollectionFacade` object which allows to manipulate the collection.
* **Returns** [`Shopware\Core\Content\Product\Hook\Pricing\PriceCollectionFacade`](./product-script-services-reference.html#pricecollectionfacade) | `null`

  Returns a `PriceCollectionFacade` if the product has graduated prices, otherwise `null`

---

---

## Manifest Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/manifest-reference.html

# Manifest Reference [​](#manifest-reference)

## Meta information (required) [​](#meta-information-required)

Meta-information about your app.

xml

```shiki
<meta>
    <!-- This is the element for the technical name of your app and must equal the name of the folder your app is contained in -->
    <name>MyExampleApp</name>
    <!-- In this element, you can set a label for your app. To include translations use the `lang` attribute -->
    <label>Label</label>
    <label lang="de-DE">Name</label>
    <!-- Translatable, a description of your app -->
    <description>A description</description>
    <description lang="de-DE">Eine Beschreibung</description>
    
    <author>Your Company Ltd.</author>
    <copyright>(c) by Your Company Ltd.</copyright>
    <version>1.0.0</version>
    <license>MIT</license>
    <compatibility>~6.5.0</compatibility>
    <!-- Optional, you can set the path to an icon that should be shown for your app, the icon needs to a `png` file -->
    <icon>icon.png</icon>
    <!-- Optional, in this element you can link to your privacy policy -->
    <privacy>https://your-company.com/privacy</privacy>
    <!-- Optional, Translatable, in this element you can describe the changes the shop owner needs to apply to his shops privacy policy, e.g. because you process personal information on an external server -->
    <privacyPolicyExtensions>
        This app processes following personal information on servers based in the U.S.:
        - Address information
        - Order positions
        - Order value
    </privacyPolicyExtensions>
    <privacyPolicyExtensions lang="de-DE">
        Diese App verarbeitet folgende personenbezogene Daten auf Servern in den USA:
        - Adress-Informationen
        - Bestellpositionen
        - Bestellsumme
    </privacyPolicyExtensions>
</meta>
```

INFO

The following configurations are all optional.

## Setup [​](#setup)

Can be omitted if no communication between Shopware and your app is needed. For more follow the [app base guide](./../../../guides/plugins/apps/app-base-guide.html#registration-request).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <setup>
        <!-- The URL which will be used for the registration -->
        <registrationUrl>https://my.example.com/registration</registrationUrl>
        <!-- Dev only, the secret that is used to sign the registration request -->
        <secret>mysecret</secret>
    </setup>
</manifest>
```

## Storefront [​](#storefront)

Can be omitted if your app template needs higher load priority than other plugins/apps. For more follow the [storefront guide](./../../../guides/plugins/apps/storefront/index.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ....
    </meta>
    <storefront>
        <template-load-priority>100</template-load-priority>
    </storefront>
</manifest>
```

## Permissions [​](#permissions)

*Optional*, can be omitted if your app does not need permissions. For more follow the [app base guide](./../../../guides/plugins/apps/app-base-guide.html).

You can use individual permission elements (`read`, `create`, `update`, `delete`) or the `<crud>` shortcut element which automatically grants all four CRUD permissions for an entity:

* `<crud>product</crud>` is equivalent to `<read>product</read>`, `<create>product</create>`, `<update>product</update>`, `<delete>product</delete>`

INFO

The `<crud>` shortcut element is available since version 6.7.3.0. If your app needs to support earlier Shopware versions, use the individual permission elements instead.

Granular permissionsFull permissions

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
  <meta>
    ...
  </meta>
  <permissions>
    <read>product</read> 
    <create>product</create> 
    <update>product</update> 
    <delete>product</delete> 

    <!-- Since version 6.4.12.0 your app can request additional non-CRUD privileges-->
    <permission>system:cache:info</permission>
  </permissions>
</manifest>
```

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
  <meta>
    ...
  </meta>
  <permissions>
    <!-- CRUD shortcut - equivalent to read, create, update, delete for product (since 6.7.3.0) -->
    <crud>product</crud> 

    <!-- Since version 6.4.12.0 your app can request additional non-CRUD privileges-->
    <permission>system:cache:info</permission>
  </permissions>
</manifest>
```

## Allowed hosts [​](#allowed-hosts)

A list of all external endpoints your app communicates with (since `6.4.12.0`)

xml

```shiki
<allowed-hosts>
    <host>example.com</host>
</allowed-hosts>
```

## Webhooks [​](#webhooks)

Register webhooks you want to receive, keep in mind that the name needs to be unique. For more follow the [app webhook guide](./../../../guides/plugins/apps/webhook.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <webhooks>
        <webhook name="product-changed" url="https://example.com/event/product-changed" event="product.written"/>
    </webhooks>
</manifest>
```

## Admin extension [​](#admin-extension)

Only needed if the Administration should be extended. For more follow the [add custom module guide](./../../../guides/plugins/apps/administration/add-custom-modules.html).

xml

```shiki
<admin>
    <!-- Optional, entry point for the Admin Extension API (since 6.4.12.0) -->
    <base-app-url>https://app.example.com</base-app-url>
    <!-- Register a custom module that is used as a parent menu entry for other modules -->
    <module name="myAdminModules"
            parent="sw-marketing"
            position="50"
    >
        <label>My modules</label>
        <label lang="de-DE">Meine Module</label>
    </module>
    <!-- Register a custom module (iframe), that should be loaded from the given source -->
    <module name="exampleModule"
            source="https://example.com/promotion/view/promotion-module"
            parent="app-MyExampleApp-myAdminModules"
    >
        <label>Example Module</label>
        <label lang="de-DE">Beispiel Modul</label>
    </module>
    <!-- Register a module that is opened from the app store and your list of installed apps -->
    <main-module source="https://example.com/main-module"/>
    <!-- Register action buttons that should be displayed in the detail and listing pages of the Administration -->
    <!-- view is one of: "list", "detail" -->
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
```

## Custom fields [​](#custom-fields)

Add your custom fields easily via the manifest.xml. For more follow the [custom fields app guide](./../../../guides/plugins/apps/custom-data/custom-fields.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <custom-fields>
        <!-- register each custom field set you may want to add -->
        <custom-field-set>
            <!-- the technical name of the custom field set, needs to be unique, therefor use your vendor prefix -->
            <name>swag_example_set</name>
            <!-- Translatable, the label of the field set -->
            <label>Example Set</label>
            <label lang="de-DE">Beispiel-Set</label>
            <!-- define the entities to which your field set should be assigned -->
            <related-entities>
                <order/>
            </related-entities>
            <!-- define the fields in your set -->
            <fields>
                <!-- the element type, defines the type of the field -->
                <!-- the name needs to be unique, therefore use your vendor prefix -->
                <text name="swag_code">
                    <!-- Translatable, the label of the field -->
                    <label>Example field</label>
                    <!-- Optional, Default = 1, order your fields by specifying the position -->
                    <position>1</position>
                    <!-- Optional, Default = false, mark a field as required -->
                    <required>false</required>
                    <!-- Optional, Translatable, the help text for the field -->
                    <help-text>Example field</help-text>
                </text>
                <float name="swag_test_float_field">
                    <label>Test float field</label>
                    <label lang="de-DE">Test-Kommazahlenfeld</label>
                    <help-text>This is an float field.</help-text>
                    <position>2</position>
                    <!-- some elements allow more configuration, like placeholder, main and max values etc. -->
                    <!-- Your IDE should give you pretty good autocompletion support to explore the configuration for a given type -->
                    <placeholder>Enter an float...</placeholder>
                    <min>0.5</min>
                    <max>1.6</max>
                    <steps>0.2</steps>
                </float>
            </fields>
        </custom-field-set>
    </custom-fields>
</manifest>
```

## Cookies [​](#cookies)

Add a single cookie to the consent manager. For more follow the [cookies with apps guide](./../../../guides/plugins/apps/storefront/cookies-with-apps.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <cookie>
            <cookie>my-cookie</cookie>
            <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
            <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
            <value>a static value for the cookie</value>
            <!-- Expiration in days -->
            <expiration>1</expiration>
        </cookie>
    </cookies>
</manifest>
```

Add a cookie group to the consent manager. For more follow the [cookies with apps guide](./../../../guides/plugins/apps/storefront/cookies-with-apps.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <group>
            <snippet-name>example-app-with-cookies.cookie-group.name</snippet-name>
            <snippet-description>example-app-with-cookies.cookie-group.description</snippet-description>
            <entries>
                <cookie>
                    <cookie>my-cookie</cookie>
                    <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
                    <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
                    <value>a static value for the cookie</value>
                    <!-- Expiration in days -->
                    <expiration>1</expiration>
                </cookie>
            </entries>
        </group>
    </cookies>
</manifest>
```

## Payments [​](#payments)

Add your payment methods via payments and handle your synchronous and asynchronous via an external app-server. For more follow the [app payment guide](./../../../guides/plugins/apps/payment.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise, all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>

    <payments>
        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>asynchronousPayment</identifier>
            <name>Asynchronous payment</name>
            <name lang="de-DE">Asynchrone Zahlung</name>
            <description>This payment method requires forwarding to payment provider.</description>
            <description lang="de-DE">Diese Zahlungsmethode erfordert eine Weiterleitung zu einem Zahlungsanbieter.</description>
            <pay-url>https://payment.app/async/pay</pay-url>
            <finalize-url>https://payment.app/async/finalize</finalize-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>synchronousPayment</identifier>
            <name>Synchronous payment</name>
            <name lang="de-DE">Synchrone Zahlung</name>
            <description>This payment method does everything in one request.</description>
            <description lang="de-DE">Diese Zahlungsmethode arbeitet in einem Request.</description>
            <!-- This URL is optional for synchronous payments (see below). -->
            <pay-url>https://payment.app/sync/pay</pay-url>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>simpleSynchronousPayment</identifier>
            <name>Simple Synchronous payment</name>
            <name lang="de-DE">Einfache synchrone Zahlung</name>
            <description>This payment will not do anything and stay on 'open' after order.</description>
            <description lang="de-DE">Diese Zahlungsmethode wird die Transaktion auf 'offen' belassen.</description>
            <!-- No URL is provided. -->
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>preparedPayment</identifier>
            <name>Payment, that offers everything</name>
            <name lang="de-DE">Eine Zahlungsart, die alles kann</name>
            <validate-url>https://payment.app/validate</validate-url>
            <pay-url>https://payment.app/pay</pay-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>refundPayment</identifier>
            <name>Refund payments</name>
            <name lang="de-DE">Einfache Erstattungen</name>
            <refund-url>https://payment.app/refund</refund-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>recurringPayment</identifier>
            <name>Recurring payments</name>
            <name lang="de-DE">Einfache wiederkehrende Zahlungen</name>
            <recurring-url>https://payment.app/recurring</recurring-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>
    </payments>
</manifest>
```

## Shipping methods [​](#shipping-methods)

Add your shipping methods via shipping-methods and handle your synchronous and asynchronous via an external app-server. For more follow the [shipping methods guide](./../../../guides/plugins/apps/shipping-methods.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- Make sure that the name of your app does not change anymore, otherwise there will be duplicates of your shipping methods -->
        <name>NameOfYourShippingMethodApp</name>
        <!-- ... -->
    </meta>
    <shipping-methods>
        <shipping-method>
            <!-- The identifier should not change after the first release -->
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>

            <delivery-time>
                <!-- Requires a new generated UUID for your new delivery time -->
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
        </shipping-method>
    </shipping-methods>
</manifest>
```

## Rule conditions [​](#rule-conditions)

The identifier of the rule condition must be unique should not change. Otherwise a separate rule condition is created, and uses of the old one are lost. For more follow the [rule conditions guide](./../../../guides/plugins/apps/rule-builder/add-custom-rule-conditions.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
    <rule-conditions>
        <rule-condition>
            <!-- The identifier of the rule condition must be unique should not change. Otherwise a separate rule condition is created and uses of the old one are lost. -->
            <identifier>my_custom_condition</identifier>
            <!-- Translatable, a name of your rule condition -->
            <name>Custom condition</name>
            <name lang="de-DE">Eigene Bedingung</name>
            <!-- A thematic group the condition should be assigned too, available groups are: general, customer, cart, item, promotion, misc -->
            <group>misc</group>
            <!-- The *.twig file that contains the corresponding script for the condition. It must be placed in the directory Resources/scripts/rule-conditions starting from your app's root directory -->
            <script>custom-condition.twig</script>
            <!-- Define the fields you want the user to fill out for use as data within your condition -->
            <constraints>
                <!-- the element type, defines the type of the field -->
                <!-- the elements available here are the same as for custom fields -->
                <single-select name="operator">
                    <placeholder>Choose an operator...</placeholder>
                    <placeholder lang="de-DE">Bitte Operatoren wählen</placeholder>
                    <options>
                        <option value="=">
                            <name>Is equal to</name>
                            <name lang="de-DE">Ist gleich</name>
                        </option>
                        <option value="!=">
                            <name>Is not equal to</name>
                            <name lang="de-DE">Ist nicht gleich</name>
                        </option>
                    </options>
                    <required>true</required>
                </single-select>
                <text name="firstName">
                    <placeholder>Enter first name</placeholder>
                    <placeholder lang="de-DE">Bitte Vornamen eingeben</placeholder>
                    <required>true</required>
                </text>
            </constraints>
        </rule-condition>
    </rule-conditions>
</manifest>
```

## Tax [​](#tax)

Add an external tax provider to your app that is calculating your taxes on the fly for complex tax setups. For more follow the [tax provider guide](./../../../guides/plugins/apps/tax-provider.html).

xml

```shiki
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>
    <tax>
        <tax-provider>
            <!-- Unique identifier of the tax provider -->
            <identifier>myCustomTaxProvider</identifier>
            <!-- Display name of the tax provider -->
            <name>My custom tax provider</name>
            <!-- Priority of the tax provider - can be changed in the administration as well -->
            <priority>1</priority>
            <!-- Url of your implementation - is called during checkout to provide taxes -->
            <process-url>https://tax-provider.app/provide-taxes</process-url>
        </tax-provider>
    </tax>
</manifest>
```

---

## Webhook Events Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/webhook-events-reference.html

# Webhook Event Reference [​](#webhook-event-reference)

| Event | Description | Permissions needed | Payload |
| --- | --- | --- | --- |
| `checkout.customer.before.login` | Triggers as soon as a customer logs in | - | `{"email":"string"}` |
| `checkout.customer.changed-payment-method` | Triggers when a customer changes his payment method in the checkout process | `customer:read` | `{"entity":"customer"}` |
| `checkout.customer.deleted` | Triggers if a customer gets deleted | `customer:read` | `{"entity":"customer"}` |
| `checkout.customer.double_opt_in_guest_order` | Triggers as soon as double opt-in is accepted in a guest order | `customer:read` | `{"entity":"customer","confirmUrl":"string"}` |
| `checkout.customer.double_opt_in_registration` | Triggers when a customer commits to his registration via double opt in | `customer:read` | `{"entity":"customer","confirmUrl":"string"}` |
| `checkout.customer.guest_register` | **EMPTY** | `customer:read` | `{"entity":"customer"}` |
| `checkout.customer.login` | Triggers as soon as a customer logs in | `customer:read` | `{"entity":"customer","contextToken":"string"}` |
| `checkout.customer.logout` | Triggers when a customer logs out | `customer:read` | `{"entity":"customer"}` |
| `checkout.customer.register` | Triggers when a new customer was registered | `customer:read` | `{"entity":"customer"}` |
| `checkout.order.payment_method.changed` | **EMPTY** | `order:read` `order_transaction:read` | `{"entity":"order_transaction"}` |
| `checkout.order.placed` | Triggers when an order is placed | `order:read` | `{"entity":"order"}` |
| `contact_form.send` | Triggers when a contact form is send | - | `{"contactFormData":"object"}` |
| `customer.group.registration.accepted` | **EMPTY** | `customer:read` `customer_group:read` | `{"entity":"customer_group"}` |
| `customer.group.registration.declined` | **EMPTY** | `customer:read` `customer_group:read` | `{"entity":"customer_group"}` |
| `customer.recovery.request` | Triggers when a customer recovers his password | `customer_recovery:read` `customer:read` | `{"entity":"customer","resetUrl":"string","shopName":"string"}` |
| `mail.after.create.message` | **EMPTY** | - | `{"data":"array","message":"object"}` |
| `mail.before.send` | Triggers before a mail is send | - | `{"data":"array","templateData":"array"}` |
| `mail.sent` | Triggers when a mail is send from Shopware | - | `{"subject":"string","contents":"string","recipients":"array"}` |
| `newsletter.confirm` | **EMPTY** | `newsletter_recipient:read` | `{"entity":"newsletter_recipient"}` |
| `newsletter.register` | **EMPTY** | `newsletter_recipient:read` | `{"entity":"newsletter_recipient","url":"string"}` |
| `newsletter.unsubscribe` | **EMPTY** | `newsletter_recipient:read` | `{"entity":"newsletter_recipient"}` |
| `product_export.log` | **EMPTY** | - | `{"name":"string"}` |
| `review_form.send` | Triggers when a product review form is send | `product:read` | `{"reviewFormData":"object","entity":"product"}` |
| `state_enter.order.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.returned` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.returned_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.shipped` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_delivery.state.shipped_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.authorized` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.chargeback` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.paid` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.paid_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.refunded` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.refunded_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.reminded` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction.state.unconfirmed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture.state.pending` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture_refund.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture_refund.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture_refund.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture_refund.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_enter.order_transaction_capture_refund.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.returned` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.returned_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.shipped` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_delivery.state.shipped_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.authorized` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.chargeback` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.paid` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.paid_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.refunded` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.refunded_partially` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.reminded` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction.state.unconfirmed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture.state.pending` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture_refund.state.cancelled` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture_refund.state.completed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture_refund.state.failed` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture_refund.state.in_progress` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `state_leave.order_transaction_capture_refund.state.open` | **EMPTY** | `order:read` | `{"entity":"order"}` |
| `user.recovery.request` | **EMPTY** | `user_recovery:read` | `{"entity":"user_recovery","resetUrl":"string"}` |
| `product.written` | Triggers when a product is written | `product:read` | `{"entity":"product","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `product.deleted` | Triggers when a product is deleted | `product:read` | `{"entity":"product","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `product_price.written` | Triggers when a product\_price is written | `product_price:read` | `{"entity":"product_price","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `product_price.deleted` | Triggers when a product\_price is deleted | `product_price:read` | `{"entity":"product_price","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `category.written` | Triggers when a category is written | `category:read` | `{"entity":"category","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `category.deleted` | Triggers when a category is deleted | `category:read` | `{"entity":"category","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `sales_channel.written` | Triggers when a sales\_channel is written | `sales_channel:read` | `{"entity":"sales_channel","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `sales_channel.deleted` | Triggers when a sales\_channel is deleted | `sales_channel:read` | `{"entity":"sales_channel","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `sales_channel_domain.written` | Triggers when a sales\_channel\_domain is written | `sales_channel_domain:read` | `{"entity":"sales_channel_domain","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `sales_channel_domain.deleted` | Triggers when a sales\_channel\_domain is deleted | `sales_channel_domain:read` | `{"entity":"sales_channel_domain","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `customer.written` | Triggers when a customer is written | `customer:read` | `{"entity":"customer","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `customer.deleted` | Triggers when a customer is deleted | `customer:read` | `{"entity":"customer","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `customer_address.written` | Triggers when a customer\_address is written | `customer_address:read` | `{"entity":"customer_address","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `customer_address.deleted` | Triggers when a customer\_address is deleted | `customer_address:read` | `{"entity":"customer_address","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `order.written` | Triggers when a order is written | `order:read` | `{"entity":"order","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `order.deleted` | Triggers when a order is deleted | `order:read` | `{"entity":"order","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `order_address.written` | Triggers when a order\_address is written | `order_address:read` | `{"entity":"order_address","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `order_address.deleted` | Triggers when a order\_address is deleted | `order_address:read` | `{"entity":"order_address","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `document.written` | Triggers when a document is written | `document:read` | `{"entity":"document","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `document.deleted` | Triggers when a document is deleted | `document:read` | `{"entity":"document","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `media.written` | Triggers when a media is written | `media:read` | `{"entity":"media","operation":"update insert","primaryKey":"array string","payload":"array"}` |
| `media.deleted` | Triggers when a media is deleted | `media:read` | `{"entity":"media","operation":"deleted","primaryKey":"array string","payload":"array"}` |
| `app.activated` |  | - |  |
| `app.deactivated` |  | - |  |
| `app.deleted` |  | - |  |
| `app.installed` |  | - |  |
| `app.updated` |  | - |  |
| `shopware.updated` |  | - |  |

---

## Payment Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/payment-reference.html

# Payment Reference [​](#payment-reference)

WARNING

This feature is only available starting with Shopware 6.4.1.0.

These two requests are executed against your API, the up to two endpoints you define per payment method. All bodies are JSON encoded.

## Pay [​](#pay)

`POST https://payment.app/pay`

This request gets called, when the users hits *Confirm Order* in Shopware.

### Parameters [​](#parameters)

| Parameter | Type | Description |
| --- | --- | --- |
| **Header** |  |  |
| shopware-shop-signature\* | string | The hmac-signature of the JSON encoded body content, signed with the shop secret returned from the registration request |
| **Body** |  |  |
| order\* | OrderEntity | The order entity from Shopware including all necessary associations (like currency, shipping address, billing address, line items). See Shopware for detailed and current structure. |
| orderTransaction\* | OrderTransactionEntity | The order transaction entity from Shopware representing the payment you are supposed to process. See Shopware for detailed and current structure. |
| orderTransaction.id\* | string | This should be used to identify the order transaction on a second finalize request. |
| returnUrl | string | This URL is the URL your app or your payment provider is supposed to redirect back to, once the user has been redirected to the payment provider with the URL you provide in your response. Only supplied on asynchronous payments. |
| source\* | object | Data to identify the shop that sent this request |
| source.url\* | string | The Shop URL sending this request |
| source.shopId\* | string | The shop id you can use to identify the sho that has been registered before with your app. |
| source.appVersion\* | string | The version of the app that is installed in the shop. |

### Responses [​](#responses)

`200`

json5

```shiki
/* Successful redirect */
{
  "redirectUrl": "https://payment.app/user/go/here/068b1ec4d7ff431b95d3b7431cc725aa/"
}
```

json5

```shiki
/* Failure due to missing credentials */
{
  "status": "fail",
  "message": "The shop has not provided all credentials for the payment provider."
}
```

## Finalize [​](#finalize)

`POST https://payment.app/finalize`

This request gets called once the user returns to the `returnUrl` Shopware provided in the first request.

### Parameters [​](#parameters-1)

| Parameter | Type | Description |
| --- | --- | --- |
| **Header** |  |  |
| shopware-shop-signature\* | string | The hmac-signature of the JSON encoded body content, signed with the shop secret returned from the registration request |
| **Body** |  |  |
| orderTransaction\* | OrderTransactionEntity | The order transaction entity from Shopware representing the payment you are supposed to process. See Shopware for detailed and current structure. |
| orderTransaction.id\* | string | This should be used to identify the order transaction on a second finalize request. |
| source\* | object | Data to identify the shop that sent this request |
| source.url\* | string | The Shop URL sending this request |
| source.shopId\* | string | The shop id you can use to identify the sho that has been registered before with your app. |
| source.appVersion\* | string | The version of the app that is installed in the shop. |

### Responses [​](#responses-1)

`200`

json5

```shiki
/* Successful redirect */
{
  "status": "paid"
}
```

json5

```shiki
/* Failure due to missing funds */
{
  "status": "fail",
  "message": "The user did not have adequate funds."
}
```

json5

```shiki
/* Failure if the user has not finished the payment process. */
{
  "status": "cancel",
  "message": "The user did not finish payment."
}
```

---

## CMS Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/cms-reference.html

# CMS Reference [​](#cms-reference)

xml

```shiki
// cms.xml
<?xml version="1.0" encoding="utf-8" ?>
<cms xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Cms/Schema/cms-1.0.xsd">
    <blocks>
        <block>
            <!-- A unique technical name for your block. We recommend to use a shorthand prefix for your company, e.g. "Swag" for shopware AG. -->
            <name>my-first-block</name>
            <!-- The category your block is associated with. See the XSD for available categories. -->
            <category>text-image</category>

            <!-- Your block's label which will be shown in the CMS module in the Administration. -->
            <label>First block from app</label>
            <!-- The label is translatable by providing ISO codes. -->
            <label lang="de-DE">Erster Block einer App</label>

            <!-- The slots that your block holds which again hold CMS elements. -->
            <slots>
                <!-- A slot requires a unique name and a type which refers to the CMS element it shows. Right now you can only use the CMS elements provided by Shopware but at a later point you will be able to add custom elements too. -->
                <slot name="left" type="manufacturer-logo">
                    <!-- The slot requires some basic configuration. The following config-value elements highly depend on which element the slot holds. -->
                    <config>
                        <!-- The following config-value will be interpreted as "displayMode: { source: "static", value: "cover"}" in the JavaScript. -->
                        <config-value name="display-mode" source="static" value="cover"/>
                    </config>
                </slot>
                <slot name="middle" type="image-gallery">
                    <config>
                        <config-value name="display-mode" source="static" value="auto"/>
                        <config-value name="min-height" source="static" value="300px"/>
                    </config>
                </slot>
                <slot name="right" type="buy-box">
                    <config>
                        <config-value name="display-mode" source="static" value="contain"/>
                    </config>
                </slot>
            </slots>

            <!-- Each block comes with a default configuration which is pre-filled and customizable when adding a block to a section in the CMS module in the Administration. -->
            <default-config>
                <margin-bottom>20px</margin-bottom>
                <margin-top>20px</margin-top>
                <margin-left>20px</margin-left>
                <margin-right>20px</margin-right>
                <!-- The sizing mode of your block. Allowed values are "boxed" or "full_width". -->
                <sizing-mode>boxed</sizing-mode>
                <background-color>#000</background-color>
            </default-config>
        </block>

        <block>
            <name>my-second-block</name>
            <category>text-image</category>

            <label>Second block from app</label>
            <label lang="de-DE">Zweiter Block einer App</label>

            <slots>
                <slot name="left" type="form">
                    <config>
                        <config-value name="display-mode" source="static" value="cover"/>
                    </config>
                </slot>
                <slot name="middle" type="image">
                    <config>
                        <config-value name="display-mode" source="static" value="auto"/>
                        <config-value name="background-color" source="static" value="red"/>
                    </config>
                </slot>
                <slot name="right" type="youtube-video">
                    <config>
                        <config-value name="display-mode" source="static" value="contain"/>
                    </config>
                </slot>
            </slots>

            <default-config>
                <margin-bottom>20px</margin-bottom>
                <margin-top>20px</margin-top>
                <margin-left>20px</margin-left>
                <margin-right>20px</margin-right>
                <sizing-mode>boxed</sizing-mode>
                <background-color>#000</background-color>
            </default-config>
        </block>
    </blocks>
</cms>
```

---

## Entities Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/entities-reference.html

# Entities Reference [​](#entities-reference)

xml

```shiki
// entities.xml
<?xml version="1.0" encoding="utf-8" ?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/CustomEntity/Xml/entity-1.0.xsd">
    <entity name="custom_entity_blog">
        <fields>
            <!-- we support different scalar values: int, float, string, text, bool, date -->
            <int name="position" store-api-aware="true" />
            <float name="rating" store-api-aware="true" />
            <string name="title" required="true" translatable="true" store-api-aware="true" />
            <text name="content" allow-html="true" translatable="true" store-api-aware="true" />
            <bool name="display" translatable="true" store-api-aware="true" />
            <date name="my_date" store-api-aware="false" />

            <!-- additionally, to the scalar values, we have support for json fields  -->
            <json name="payload" store-api-aware="false" />
            
            <!-- beside the generic fields, we support different logical fields like email and price -->
            <email name="email"  store-api-aware="false" />
            <price name="price" store-api-aware="false" />
            
            <!--   each field also supports having a default value. This is only supported for scalar types -->
            <bool name="in_stock" store-api-aware="true" default="true" />

            <!-- you may want to define that some fields should not be available in the store-api -->
            <text name="internal_comment" store-api-aware="false" />

            <!-- you can also define relation between entities -->
            <many-to-many name="products" reference="product" store-api-aware="true" />

            <!-- it is also possible to cascading relations between you own custom entities. In this case, we delete all ce_blog_comment records, when the linked custom_entity_blog record deleted -->
            <one-to-many name="comments" reference="ce_blog_comment" store-api-aware="true" on-delete="cascade" reverse-required="true" />
            
            <!-- There are many other cascade cases which we support -->

            <!-- Restrict product deletion when the product is set as `top_seller` -->
            <many-to-one name="top_seller_restrict" reference="product" store-api-aware="true" required="false" on-delete="restrict" />
                <!-- This definition, generates a fk field automatically inside the product table -->

            <!-- when product deleted, delete all custom_entity_blog records where the product is defined as `top_seller_cascade`-->
            <many-to-one name="top_seller_cascade" reference="product" store-api-aware="true" required="true" on-delete="cascade" />

            <!-- when product deleted, set the `top_seller_set_null` column to null -->
            <many-to-one name="top_seller_set_null" reference="product" store-api-aware="true" on-delete="set-null" />

            <!-- restrict product deletion when the product is set as `link_product_restrict`-->
            <one-to-one name="link_product_restrict" reference="product" store-api-aware="false" on-delete="restrict" />

            <!-- when product deleted, delete all custom_entity_blog records where the product is defined as `link_product_cascade`-->
            <one-to-one name="link_product_cascade" reference="product" store-api-aware="false" on-delete="cascade" />

            <!-- when product deleted, set the `link_product_set_null_id` column to null -->
            <one-to-one name="link_product_set_null" reference="product" store-api-aware="false" on-delete="set-null" />

            <!-- restrict custom_entity_blog deletion, when the blog is linked in some category -->
            <one-to-many name="links_restrict" reference="category" store-api-aware="true" on-delete="restrict" />

            <!-- set custom_entity_blog_links_id to null, when the custom_entity_blog record deleted -->
            <one-to-many name="links_set_null" reference="category" store-api-aware="true" on-delete="set-null" />

            <!-- we also support inheritance for product relations  -->
            <many-to-many name="inherited_products" reference="product" store-api-aware="true" inherited="true"/>
            <many-to-one name="inherited_top_seller" reference="product" store-api-aware="true" required="false" inherited="true" on-delete="set-null"/>
            <one-to-one name="inherited_link_product" reference="product" store-api-aware="true" inherited="true" on-delete="set-null" />
        </fields>
    </entity>

    <!-- since shopware v6.5.15.0 you can use the `ce_` shorthand prefix, to make your entity names shorter -->
    <entity name="ce_blog_comment">
        <fields>
            <string name="title" required="true" translatable="true" store-api-aware="true" />
            <!-- <fk name="ce_blog_comments_id" required="true"   <<< defined over the one-to-many association in the custom_entity_blog definition -->
            <text name="content" allow-html="true" translatable="true" store-api-aware="true" />
            <email name="email"  store-api-aware="false" />
            <many-to-one name="recommendation" reference="product" store-api-aware="true" required="false" on-delete="set-null" />
        </fields>
    </entity>
</entities>
```

---

## Flow Action Reference

**Source:** https://developer.shopware.com/docs/resources/references/app-reference/flow-action-reference.html

# Flow Action Reference [​](#flow-action-reference)

xml

```shiki
// flow-action.xml
<flow-actions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-action>
        <meta>
            <name>slack</name>
            <label>Send slack message</label>
            <label lang="de-DE">Slack-Nachricht senden</label>
            <headline>Headline for send slack message</headline>
            <headline lang="de-DE">Überschrift für das Senden einer Slack-Nachricht</headline>
            <description>Slack send message description</description>
            <description lang="de-DE">Beschreibung der Slack-Sendenachricht</description>
            <url>https://hooks.slack.com/services/{id}</url>
            <sw-icon>default-communication-speech-bubbles</sw-icon>
            <icon>slack.png</icon>
            <requirements>orderAware</requirements>
            <requirements>customerAware</requirements>
        </meta>
        <headers>
            <parameter type="string" name="content-type" value="application/json"/>
        </headers>
        <parameters>
            <parameter type="string" name="text" value="{{ subject }} \n {{ message }} \n Order Number: {{ order.orderNumber }}"/>
        </parameters>
        <config>
            <input-field type="text">
                <name>subject</name>
                <label>Subject</label>
                <label lang="de-DE">Gegenstand</label>
                <place-holder>Placeholder</place-holder>
                <place-holder lang="de-DE">Platzhalter</place-holder>
                <required>true</required>
                <helpText>Help Text</helpText>
                <helpText lang="de-DE">Hilfstext</helpText>
            </input-field>
            <input-field type="textarea">
                <name>message</name>
                <label>Message</label>
                <label lang="de-DE">Nachricht</label>
                <place-holder>Placeholder</place-holder>
                <place-holder lang="de-DE">Platzhalter</place-holder>
                <required>true</required>
                <helpText>Help Text</helpText>
                <helpText lang="de-DE">Hilfstext</helpText>
            </input-field>
        </config>
    </flow-action>
    <flow-action>
        <meta>
            <name>telegram</name>
            <label>Send telegram message</label>
            <label lang="de-DE">Telegrammnachricht senden</label>
            <url>https://api.telegram.org/{id}</url>
            <sw-icon>default-communication-speech-bubbles</sw-icon>
            <icon>telegram.png</icon>
            <requirements>orderAware</requirements>
            <requirements>customerAware</requirements>
        </meta>
        <headers>
            <parameter type="string" name="content-type" value="application/json"/>
        </headers>
        <parameters>
            <parameter type="string" name="chat_id" value="{{ chatId }}"/>
            <parameter type="string" name="text" value="{{ content }}"/>
        </parameters>
        <config>
            <input-field type="text">
                <name>chatId</name>
                <label>Chat Room</label>
                <label lang="de-DE">Chatroom</label>
                <required>true</required>
                <defaultValue>Hello</defaultValue>
                <helpText>This is the chat room id, you can get the id via telegram api</helpText>
                <helpText lang="de-DE">Dies ist die Chatroom-ID, Sie können die ID über die Telegramm-API abrufen</helpText>
            </input-field>
            <input-field type="text">
                <name>subject</name>
                <label>Subject</label>
                <label lang="de-DE">Thema</label>
                <required>true</required>
            </input-field>
            <input-field type="textarea">
                <name>content</name>
                <label>Content</label>
                <label lang="de-DE">Inhalt</label>
            </input-field>
        </config>
    </flow-action>
</flow-actions>
```

## Variables [​](#variables)

| Event | Variables |
| --- | --- |
| checkout.order.placed   state\_enter.order.state.cancelled   state\_enter.order.state.completed   state\_enter.order.state.in\_progress  state\_enter.order\_transaction.state.reminded   state\_enter.order\_transaction.state.open   state\_enter.order\_transaction.state.refunded  state\_enter.order\_transaction.state.paid   state\_enter.order\_transaction.state.cancelled   state\_enter.order\_transaction.state.refunded\_partially   state\_enter.order\_transaction.state.paid\_partially   state\_enter.order\_delivery.state.cancelled   state\_enter.order\_delivery.state.shipped   state\_enter.order\_delivery.state.returned\_partially   state\_enter.order\_delivery.state.shipped\_partially   state\_enter.order\_delivery.state.returned | order |
| customer.group.registration.declined   customer.group.registration.accepted | customer   customerGroup |
| user.recovery.request | userRecovery |
| checkout.customer.double\_opt\_in\_registration   checkout.customer.double\_opt\_in\_guest\_order | customer   confirmUrl |
| customer.recovery.request | customerRecovery   customer   resetUrl   shopName |
| contact\_form.send | contactFormData |
| checkout.customer.register | customer |
| newsletter.register | newsletterRecipient   url |
| newsletter.confirm | newsletterRecipient |

---

