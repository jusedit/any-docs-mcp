# Guides Plugins Themes

*Scraped from Shopware Developer Documentation*

---

## Themes

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/

# Themes [​](#themes)

A Shopware theme is an extension (plugin or app) that enables you to customize and modify the appearance and design of your online storefront. You can change the layout, styling, typography, colors, images, and other visual elements to match your brand identity and desired user experience.

text

```shiki
Extensions
├── Plugin
│   └── can include a Theme (not for Cloud)
└── App
    └── can include a Theme (Cloud-ready)
```

Tasks that themes enable include:

* template overrides
* custom styles
* configuration interfaces
* control the order in which styles and templates are loaded

INFO

Note that a plugin can also override templates.

To get started with your first theme, follow our [Theme Base Guide](./theme-base-guide.html).

For more on how themes relate to plugins and apps, see [Plugins and Apps vs Themes](./differences-plugins-and-apps-vs-themes.html).

---

## Theme Base Guide

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/theme-base-guide.html

# Theme Base Guide [​](#theme-base-guide)

A theme gives you the ability to extend/change the visual appearance of the Storefront via styling the SCSS/CSS and adjusting twig templates. You can also provide JavaScript with your theme to change how the Storefront behaves in the browser. For example, JavaScript is used in Shopware to open the offcanvas shopping-cart. Now, as you might know, Shopware comes with a default theme, to make things a bit easier. The default theme in Shopware is built on top of Bootstrap 5, style-wise. So everything you can do with Bootstrap, you can do with the Shopware Storefront as well.

Another handy capability is the theme configuration: As a theme developer you can define variables which can be configured by the shop owner in the Administration. Those variables are accessible in your theme and let you implement powerful features.

## Next steps [​](#next-steps)

Now that you know what you can do with themes, the next steps would be to [create themes](./create-a-theme.html).

---

## Create a first theme

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/create-a-theme.html

# Create a First Theme [​](#create-a-first-theme)

## Overview [​](#overview)

This guide will show you how to create a theme from scratch. You will also learn how to install and activate your theme.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line.

## Create your first plugin theme [​](#create-your-first-plugin-theme)

Let's get started with creating your plugin by finding a proper name for it.

### Name your plugin theme [​](#name-your-plugin-theme)

First, you need to find a name for your theme. We're talking about a technical name here, so it needs to describe your theme appearance as short as possible, written in UpperCamelCase. To prevent issues with duplicated theme names, you should add a shorthand prefix for your company.  
 Shopware uses "Swag" as a prefix for that case.  
 For this example guide we'll use the theme name **SwagBasicExampleTheme.**

INFO

Notice: The name of a theme must begin with a capital letter too!

### Create a plugin-based theme [​](#create-a-plugin-based-theme)

Now that you've found your name, it's time to actually create your plugin.

Open your terminal and run the following command to create a new theme

bash

```shiki
bin/console theme:create SwagBasicExampleTheme

# you should get an output like this:

Creating theme structure under .../development/custom/plugins/SwagBasicExampleTheme
```

After your theme was created successfully Shopware has to know that it now exists. You have to refresh the plugin list by running the following command.

bash

```shiki
bin/console plugin:refresh

# you should get an output like this

[OK] Plugin list refreshed                                                                              

Shopware Plugin Service
=======================

 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 
  Plugin                  Label                                Version       Upgrade version   Author   Installed   Active   Upgradeable  
 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 
  SwagBasicExampleTheme   Theme SwagBasicExampleTheme plugin   9999999-dev                              No          No       No           
 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 

 1 plugins, 0 installed, 0 active , 0 upgradeable
```

Now Shopware recognises your plugin theme. The next step is the installation and activation of your theme. Run the following command in terminal.

bash

```shiki
# run this command to install and activate your plugin
bin/console plugin:install --activate SwagBasicExampleTheme

Shopware Plugin Lifecycle Service
=================================

 Install 1 plugin(s):
 * Theme SwagBasicExampleTheme plugin (vdev-trunk)

 Plugin "SwagBasicExampleTheme" has been installed and activated successfully.

 [OK] Installed 1 plugin(s).
```

Your theme was successfully installed and activated.

The last thing we need to do to work with the theme is to assign it to a sales channel. You can do that by running the `theme:change` command in the terminal and follow the instructions.

bash

```shiki
# run this to change the current Storefront theme
$ bin/console theme:change

# you will get an interactive prompt to change the 
# current theme of the Storefront like this

Please select a sales channel:
[0] Storefront | 64bbbe810d824c339a6c191779b2c205
[1] Headless | 98432def39fc4624b33213a56b8c944d
> 0

Please select a theme:
[0] Storefront
[1] SwagBasicExampleTheme
> 1

Set "SwagBasicExampleTheme" as new theme for sales channel "Storefront"
Compiling theme 13e0a4a46af547479b1347617926995b for sales channel SwagBasicExampleTheme
```

At first, we have to select a sales channel. The obvious choice here is the 'Storefront'. Afterwards enter the number for our theme.

Now your theme is fully installed, and you can start your customization.

### Directory structure of a theme [​](#directory-structure-of-a-theme)

bash

```shiki
# structure of a plugin-based theme
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       ├── dist
    │   │       │   └── storefront
    │   │       │       └── js
    |   |       |           └── swag-basic-example-theme  
    │   │       │               └── swag-basic-example-theme.js
    │   │       └── src
    │   │           ├── assets
    │   │           ├── main.js
    │   │           └── scss
    │   │               ├── base.scss
    │   │               └── overrides.scss
    │   └── theme.json
    └── SwagBasicExampleTheme.php
```

## Next steps [​](#next-steps)

Now that you have created your own theme, the next step is to learn how to make settings and adjustments.

* [Theme configuration](./theme-configuration.html)
* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Add assets to theme](./add-assets-to-theme.html)

---

## Differences Plugins and Apps vs Themes

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/differences-plugins-and-apps-vs-themes.html

# Differences Plugins and Apps vs Themes [​](#differences-plugins-and-apps-vs-themes)

A theme is a special type of Plugin or App, aimed at easily changing the visual appearance of the Storefront. If you want to get more information about plugins and apps you can check out the [Plugin Base Guide](./../plugins/plugin-base-guide.html) and [App Base Guide](./../apps/app-base-guide.html).

There are basically several ways to change the appearance of the Storefront. You can have "regular" plugins or apps whose main purpose is to add new functions and change the behavior of the shop. These plugins / apps might also contain SCSS/CSS and JavaScript to be able to embed their new features into the Storefront.

Technically, a theme is also a plugin / app, but it will be visible in the theme manger once it's activated and can be assigned to a specific sales channel, while plugins / apps are activated globally. To distinguish a theme from a "regular" plugin / app you need to implement the Interface `Shopware\Storefront\Framework\ThemeInterface`. A theme can inherit also from other themes, overwrite the default configuration (colors, fonts, media) and add new configuration options.

You do not need to write any PHP code in a theme. If you need PHP code, you should choose a plugin instead. Another important distinction to themes is this: Themes are specific for a sales channel and have to be assigned to them to take effect, the other way around plugins and apps have a global effect on the Shopware installation.

## Next steps [​](#next-steps)

Now that you have learned the differences between themes, plugins and apps, you can create your first theme.

* [Create a first Shopware theme](./create-a-theme.html)

---

## Theme configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/theme-configuration.html

# Theme Configuration [​](#theme-configuration)

INFO

The `configInheritance` is available from Shopware Version 6.4.8.0

## Overview [​](#overview)

This guide shows you how the theme configuration works and explains the possibilities of the settings in more depth.

## Prerequisites [​](#prerequisites)

This guide is built upon the guide on creating a first theme:

[Create a first theme](create-a-theme)

## Structure of theme configuration [​](#structure-of-theme-configuration)

The theme configuration for a theme is located in the `theme.json` file `<plugin root>/src/Resources` folder. Open up the `<plugin root>/src/Resources/theme.json` file with your favorite code-editor. The configuration looks like this.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "description": {
    "en-GB": "My custom theme",
    "de-DE": "Mein custom thema"
  },
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme"
  ],
  "previewMedia": "app/storefront/dist/assets/defaultThemePreview.jpg",
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/swag-basic-example-theme/swag-basic-example-theme.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ],
  "configInheritance": [
    "@Storefront",
    "@OtherTheme"
    ]
}
```

INFO

If you make changes or additions to the `theme.json` file, you must then execute the `theme:refresh` command to put them into effect. Run `bin/console theme:refresh` in order to update your theme.

Let's have a closer look at each section.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "description": {
    "en-GB": "Just another description",
    "de-DE": "Nur eine weitere Beschreibung"
  },
  ...
}
```

Here change the `name` of your theme and the `author`. It is recommended to choose a name in camel case. The `description` section is optional and as you notice it is also translatable.

The `views` section controls the template inheritance. This will be covered in the [Theme inheritance](./add-theme-inheritance.html) guide.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme"
  ],
  ...
}
```

The `previewMedia` field provides a path `app/storefront/dist/assets/defaultThemePreview.jpg` to an image file that is relative to the root directory of the theme. It serves as a visual preview of the theme. This preview image is typically displayed within the Shopware administration interface or theme marketplace as a thumbnail or preview of the theme's appearance to give users an idea of how the theme will appear on their storefront before they activate it.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "previewMedia": "app/storefront/dist/assets/defaultThemePreview.jpg",
  ...
}
```

The `style` section determines the order of the CSS compilation. In the `<plugin root>/app/storefront/src/scss/base.scss` file you can apply your changes you want to make to the `@Storefront` standard styles or add other styles you need. The `<plugin root>/app/storefront/src/scss/overrides.scss` file is used for a special case. Maybe you need to override some defined `variables` or `functions` defined by Shopware or Bootstrap, you can implement your changes here. Checkout the [Override bootstrap variables in a theme](./override-bootstrap-variables-in-a-theme.html) guide for further information.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  ...
}
```

## Assets [​](#assets)

The `asset` option you can configure your paths to your assets like images, fonts, etc. The standard location to put your assets to is the `<plugin root>/app/storefront/src/assets` folder. Checkout the [Add assets to theme](./add-assets-to-theme.html) guide for further information.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "app/storefront/src/assets"
   ]
  ...
}
```

If you need the assets from the default storefront theme for your custom theme, just add `@Storefront` as asset path

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "@Storefront",
     "app/storefront/src/assets"
   ]
  ...
}
```

## Config fields [​](#config-fields)

One of the benefits of creating a theme is that you can overwrite the theme configuration of the default theme or add your own configurations.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ... 
  "asset":[
    ...
  ],
  "config": {
      "fields": {
        "sw-color-brand-primary": {
          "value": "#00ff00"
        }
      }
   }
}
```

In the example above, we change the primary color to green. You always inherit from the storefront config and both configurations are merged. This also means that you only have to provide the values you actually want to change. You can find a more detailed explanation of the configuration inheritance in the section [Theme inheritance](./add-theme-inheritance.html).

WARNING

If you overwrite variables of another theme from a third party provider and these are renamed or removed at a later time, this can lead to issues and the theme can no longer be compiled. So be aware of it.

The `theme.json` contains a `config` property which contains a list of tabs, blocks, sections and fields.

The key of each config field item is also the technical name which you use to access the config option in your theme or scss files. `config` entries will show up in the Administration and can be customized by the end user (if `editable` is set to `true`, see table below).

The following parameters can be defined for a config field item:

| Name | Meaning |
| --- | --- |
| `label` | Array of translations with locale code as key. *(Deprecated for v6.8: Translations are now handled via Administration snippets)* |
| `helpText` | Array of translations with locale code as key. *(Deprecated for v6.8: Translations are now handled via Administration snippets)* |
| `type` | Type of the config. Possible values: color, text, number, fontFamily, media, checkbox, switch and url |
| `editable` | If set to false, the config option will not be displayed (e.g. in the Administration) |
| `tab` | Name of a tab to organize the config options |
| `block` | Name of a block to organize the config options |
| `section` | Name of a section to organize the config options |
| `custom` | The defined data will not be processed but is available via API |
| `scss` | If set to false, the config option will not be injected as a SCSS variable |
| `fullWidth` | If set to true, the Administration component width will be displayed in full width |

### Translations in Theme Manager [​](#translations-in-theme-manager)

Since the translations in `theme.config` are only used by the Theme Manager in the administration, we decided to use snippet keys for translating the configuration in order to ensure inheritance.

Each snippet key begins with `sw-theme`, followed by the theme’s technical name, or its respective parent theme name, since snippets are inherited from the parent theme as well. It then includes the names of the relevant `tab`, `block`, `section`, and `field`. If you're translating field options, a numeric index is added to the snippet path. If any of these elements are unnamed, `default` will be used as the replacement in the key.

At the end of the key, you append `label`. For fields, you may alternatively use `helpText` instead of `label`.

This results in the following key structure:

* **Tab**: `sw-theme.<technicalName>.<tabName>.label`
* **Block**: `sw-theme.<technicalName>.<tabName>.<blockName>.label`
* **Section**: `sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.label`
* **Field**:
  + `sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.<fieldName>.label`
  + `sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.<fieldName>.helpText`
* **Option**: `sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.<fieldName>.<index>.label`

#### Example [​](#example)

Assuming your `theme.json` is structured as follows:

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "JustAnotherTheme",
  // ...
  "config": {
    "fields": {
      "my-single-select-field": {
        "type": "text",
        "value": "24",
        "custom": {
          "componentName": "sw-single-select",
          "options": [
            {
              "value": "16"
            },
            {
              "value": "20"
            },
            {
              "value": "24"
            }
          ]
        },
        "editable": true,
        "block": "exampleBlock",
        "section": "exampleSection"
      }
    }
  }
}
```

This would generate the following snippet keys:

* **Tab**: `sw-theme.justAnotherTheme.default.label`
* **Block**: `sw-theme.justAnotherTheme.default.exampleBlock.label`
* **Section**: `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.label`
* **Field**:
  + `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.my-single-select-field.label`
  + `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.my-single-select-field.helpText`
* **Option**:
  + `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.my-single-select-field.0.label`
  + `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.my-single-select-field.1.label`
  + `sw-theme.justAnotherTheme.default.exampleBlock.exampleSection.my-single-select-field.2.label`

## Field types [​](#field-types)

You can use different field types in your theme manager:

A text field example:

A number field example:

Two boolean field examples:

## Examples for custom config fields [​](#examples-for-custom-config-fields)

A custom single-select field example

![Example of a custom single-select field](/assets/example-single-select-config.DjW4J3eH.png)

A custom multi-select field example

![Example of a custom multi-select field](/assets/example-multi-select-config.BRd4WnCe.png)

## Tabs, blocks and sections [​](#tabs-blocks-and-sections)

You can use tabs, blocks and sections to structure and group the config options.

![Example of tabs, blocks and sections](/assets/theme-config.BK_o0FI1.png)

In the picture above are four tabs. In the "Colours" tab there is one block "Theme colours" which contains two sections named "Important colors" and "Other". You can define the block and section individually for each item. Example:

The tab and section property is not required.

You can extend the config to add translated labels for the tabs, blocks and sections:

## Config inheritance [​](#config-inheritance)

The `configInheritance` option lets you configure additional themes from which your theme will inherit its fields configuration and snippets. Every theme will always inherit the fields from the `Storefront` standard theme. With this option you can add additional other themes. For example, you can have a basic theme for your corporate design and special themes for different sales channels with specific changes only needed for a single sales channel.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "configInheritance": [
     "@Storefront", 
     "@BasicTheme"
   ]
  ...
}
```

In this example the `BasicTheme` is a theme that adds all the configurations you need for your corporate design. This configurations will be inherited in your new theme which can add or change some configurations only needed in a special sales channel or for a special time. See [Theme inheritance](./add-theme-inheritance.html) for a more detailed example.

All configuration fields and their values from the mentioned themes in `configInheritance` are available inside the current theme, unless they are explicitly overwritten. This way custom themes can be extended without copying their configuration inside the theme.json. The relationship of the inheritance is only created while installing the theme. For updating the relationship later on, the command `theme:refresh` can be used.

## Next steps [​](#next-steps)

Now that you know how to configure your theme, here is a list of things you can do.

* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Customize Templates](./../plugins/storefront/customize-templates.html)

---

## Add SCSS Styling and JavaScript to a Theme

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/add-css-js-to-theme.html

# Add SCSS Styling and JavaScript to a Theme [​](#add-scss-styling-and-javascript-to-a-theme)

## Overview [​](#overview)

This guide explains how you can add your custom styling via SCSS and add your custom JavaScript to your theme.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which is assigned to a sales channel. Checkout the [Create a first theme](./create-a-theme.html) guide if you have not yet a working theme setup.

## Adding custom SCSS [​](#adding-custom-scss)

When it comes to CSS and SCSS, they are processed by a PHP SASS compiler.

The main entry point to deploy your SCSS code is defined in the `theme.json` file. By default it is the `<plugin root>/app/storefront/src/scss/base.scss` file.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
 {
   ...
   "style": [
     "app/storefront/src/scss/overrides.scss",
     "@Storefront",
     "app/storefront/src/scss/base.scss"
   ],
   ...
 }
```

When the Storefront gets compiled the PHP SASS compiler will look up the files declared in the `style` section of the theme configuration. You can define the SCSS entrypoints individually if you want to.

In order to add some custom SCSS in your theme, you just need to edit the `base.scss` file which in located in `<plugin root>/src/Resources/app/storefront/src/scss` directory.

bash

```shiki
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           └── scss
    │   │               └── base.scss <-- SCSS entry
    └── SwagBasicExampleTheme.php
```

To apply your styles and test them, please use some test code:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background-color: blue;
}
```

Afterwards, you need to compile your theme by running the `bin/console theme:compile` command in terminal.

After your theme was compiled successfully, go and check your changes by opening the Storefront in your browser.

## Adding custom JS [​](#adding-custom-js)

JavaScript cannot be compiled by PHP, so [webpack](https://webpack.js.org/) is being used for that. All Javascript in Shopware 6 is written in EcmaScript 6. Of course you can write your code in EcmaScript 5 as well.

By default your plugin is using Shopware's default webpack configuration, as you must ship your theme with the JavaScript already compiled.

Since Shopware knows where your style files are located, they are automatically compiled, compressed and loaded into the Storefront. In the case of JavaScript, you have your `main.js` as entry point which has to be located the `src/Resources/app/storefront/src/` directory:

bash

```shiki
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           └── main.js <-- JS entry
    └── SwagBasicExampleTheme.php
```

Add some test code in order to see if it works out:

javascript

```shiki
// <plugin root>/src/Resources/app/storefront/src/js/main.js
console.log('SwagBasicExampleTheme JS loaded');
```

In the end, by running the command `bin/build-storefront.sh` your custom JS plugin is loaded. By default, the compiled JavaScript file is saved as `<plugin root>/src/resources/app/storefront/dist/storefront/js/swag-basic-example-theme/swag-basic-example-theme.js`. It is detected by Shopware automatically and included in the Storefront. So you do not need to embed the JavaScript file yourself.

## Using the hot-proxy (live reload) [​](#using-the-hot-proxy-live-reload)

Of course, the theme compilation with `bin/console theme:compile` will get tedious if you change files a lot and want to check the changes in the browser. So there is a better way while you are developing your theme with the `hot-proxy` option, which will give you the live reload feature.

To activate the hot-proxy, run the following command in your terminal.

This command starts a NodeJS web server on port `9998`. If you open the Storefront of your Shopware installation on `localhost:9998`, this page will be automatically updated when you make changes to your theme.

## Next steps [​](#next-steps)

Now that you know how to customize the styling via SCSS and add JavaScript, here is a list of things you can do.

* [Override Bootstrap variables in a theme](./override-bootstrap-variables-in-a-theme.html)
* [Customize templates](./../plugins/storefront/customize-templates.html)

---

## Override Bootstrap variables in a Theme

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/override-bootstrap-variables-in-a-theme.html

# Override Bootstrap Variables in a Theme [​](#override-bootstrap-variables-in-a-theme)

## Overview [​](#overview)

The storefront theme is implemented as a skin on top of Bootstrap:

[Bootstrap · The most popular HTML, CSS, and JS library in the world.](https://getbootstrap.com/)

Sometimes it is necessary to adjust SCSS variables if you want to change the look of the Storefront for example default variables like `$border-radius` which is defined by Bootstrap. This guide will show how you can override those SCSS variables.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which is assigned to a sales channel. Checkout the [Create a first theme](./create-a-theme.html) guide if you have not yet a working theme setup.

## Override default SCSS variables [​](#override-default-scss-variables)

Bootstrap 4 is using the `!default` flag for it's own default variables. Variable overrides have to be declared beforehand.

More information can be found [here](https://getbootstrap.com/docs/4.0/getting-started/theming/#variable-defaults).

To be able to override Bootstrap variables there is an additional SCSS entry point defined in your `theme.json` which is declared before `@Storefront`.

This entry point is called `overrides.scss`:

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "views": [
        "@Storefront",
        "@Plugins"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss", <-- Variable overrides
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/just-another-theme/just-another-theme.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ]
}
```

In the `<plugin root>/src/Resources/app/storefront/src/scss/overrides.scss` you can now override default variables like `$border-radius` globally and set its value to `0` to reset it in this case:

css

```shiki
// <plugin root>/src/Resources/app/storefront/src/scss/overrides.scss
/*
Override variable defaults
==================================================
This file is used to override default SCSS variables from the Shopware Storefront or Bootstrap.

Because of the !default flags, theme variable overrides have to be declared beforehand.
https://getbootstrap.com/docs/4.0/getting-started/theming/#variable-defaults
*/

$border-radius: 0;

// some other override examples
$icon-base-color: #f00;
$modal-backdrop-bg: rgba(255, 0, 0, 0.5);
$disabled-btn-bg: #f00;
$disabled-btn-border-color: #fc8;
$font-weight-semibold: 300;
```

After saving the `overrides.scss` file and running `bin/console theme:compile` go and check out the Storefront in the browser. The `border-radius` should be removed for every element.

WARNING

Please only add variable overrides in this file. You should not write CSS code like `.container { background: #f00 }` in this file.

INFO

When running `composer run watch:storefront` in platform only setups or `./bin/watch-storefront.sh` in the production template, SCSS variables will be injected dynamically by webpack. When writing selectors and properties in the `overrides.scss` the code can appear multiple times in your built CSS.

## Next steps [​](#next-steps)

Now that you know how to override Bootstrap variables, here is a list of related topics which might be interesting for you.

* [Theme configuration](./theme-configuration.html)
* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Add assets to a theme](./add-assets-to-theme.html)

---

## Add assets to a Theme

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/add-assets-to-theme.html

# Add Assets to a Theme [​](#add-assets-to-a-theme)

## Overview [​](#overview)

Your theme can include custom assets like images. This short guide will show you where to store your custom assets and how you can link them in Twig and SCSS.

## Prerequisites [​](#prerequisites)

This guide is built upon the guide on creating a first theme:

[Create a first theme](create-a-theme)

## Using custom assets [​](#using-custom-assets)

There are basically two ways of adding custom assets to your theme. The first one is using the `theme.json` to define the path to your custom assets, the second being the default way of using custom assets in plugins. We'll take a closer look at them in the following sections.

### Adding assets in theme.json file [​](#adding-assets-in-theme-json-file)

While working with your own theme, you might have already come across the [Theme configuration](./theme-configuration.html). In there, you have the possibility to configure your paths to your custom assets like images, fonts, etc. This way, please configure your asset path accordingly.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "app/storefront/src/assets"
   ]
  ...
}
```

Next, run the command `bin/console theme:compile`. The assets from the path defined in the `theme.json` file will be copied by the `theme:compile` command to `<shopware root>/public/theme/<theme-asset-uuid>` along with the compiled CSS and JS, which are stored in a separate folder.

text

```shiki
// <shopware root>/public
# 
.
└── theme
    ├── <theme-uuid>
    │   ├── css
    │   │   └── all.css
    │   └── js
    │       └── all.js
    └── <theme-asset-uuid>
        └── asset
            └── your-image.png <-- Your asset is copied here
```

### Adding assets the plugin way [​](#adding-assets-the-plugin-way)

This way of adding custom assets refers to the default way of dealing with assets. For more details, please check out the article that specifically addresses this topic:

[Add custom assets](../plugins/storefront/add-custom-assets)

## Linking to assets [​](#linking-to-assets)

You can link to the asset with the twig [asset](https://symfony.com/doc/current/templates.html#linking-to-css-javascript-and-image-assets) function:

html

```shiki
<img src="{{ asset('/assets/your-image.png', 'theme') }}">
```

In SCSS, you can link to the asset like the following:

css

```shiki
body {
    background-image: url('#{$app-css-relative-asset-path}/your-image.png');
}
```

## Next steps [​](#next-steps)

Now that you know how to use your assets in a theme, here is a list of other related topics where assets can be used.

* [Customize templates](./../plugins/storefront/customize-templates.html)

---

## Add custom icons

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/add-icons.html

# Add Custom Icons [​](#add-custom-icons)

## Overview [​](#overview)

In this guide, you will learn how to use the icon renderer component as well as adding custom icons.

INFO

Even if this is originally a plugin guide, everything will work perfectly in a theme as well. Actually, a theme even is a kind of plugin. So don't get confused by us talking about plugins here.

## Prerequisites [​](#prerequisites)

To follow this guide easily, you first need to have a functioning plugin installed. Head over to our [Plugin base guide](./../plugins/plugin-base-guide.html) to create a plugin, if you don't know how it's done yet. Also, knowing and understanding SCSS will be quite mandatory to fully understand what's going on here. Furthermore, it might be helpful to read the guide on how to [handle own assets](./../plugins/storefront/add-custom-assets.html) in your plugin before you start with this one.

## Adding icon [​](#adding-icon)

To add any icons to the Storefront, you use our `sw_icon` twig action. This way, an icon of choice is displayed in the Storefront.

Needless to say, the first step is saving your image somewhere in your plugin where Shopware can find it. The default path for icons is the following:

text

```shiki
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/default
`
```

You can also provide "solid" icons or any other custom pack names that can be configured later with the `pack` parameter. You can do that by creating a folder with the pack name:

text

```shiki
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/<pack-name>
```

By default, Shopware looks inside the "default" folder.

twig

```shiki
{% sw_icon 'done-outline-24px' style {
    'namespace': 'TestPlugin'
} %}
```

INFO

When you want to see all icons available to the storefront by default, see [here](https://github.com/shopware/shopware/tree/trunk/src/Storefront/Resources/app/storefront/dist/assets/icon). They are available as `default` and `solid` icon pack.

Imagine you want to use the default `checkmark` icon from the `solid` pack. In this case,

You surely want to add your own custom icons. In this case, the `namespace` parameter is the most important one to configure. In there, you need to set the name of the theme in which the icon is searched for by its name.

WARNING

If you configure no deviating namespace, Shopware will display the Storefront's default icons.

However, these are not all of your possibilities of configuration. As you see, you're able to configure even more things. Let's take a look at the `style` object's possible parameters:

| Configuration | Description | Remarks |
| --- | --- | --- |
| `size` | Sets the size of the icon | --- |
| `namespace` | Selection of the namespace of the icon, you can compare it with the source of it | Important configuration if you want to use custom icons. |
| `pack` | Selects the pack of different icons | --- |
| `color` | Sets the color of the icon | You can either use pre-defined variants similar to bootstrap (eg: primary , danger etc) or manually style the icon with any color with CSS. |
| `class` | Defines a class of the icon | --- |

A simple but fully functional example could look like below:

twig

```shiki
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_body %}

    {# We want to set our own icon here #}
    <h1>Custom icon:</h1>
    {% sw_icon 'done-outline-24px' style {
        'size': 'lg',
        'namespace': 'TestPlugin',
        'pack': 'solid'
    } %}
    {{ parent() }}

{% endblock %}
```

DANGER

Icons or other custom assets are not included in the theme inheritance.

Inside your theme, you cannot put an icon in a directory corresponding to the core folder structure and expect the core one to be automatically overwritten by it, as you're used to with themes in general.

## Load icons from custom locations [​](#load-icons-from-custom-locations)

Since Shopware 6.4.1.0 it is possible to define custom locations of your custom icons inside your theme.json file. You can define the name of the icon pack and the path to those icons under the `iconSets`-key:

json

```shiki
{
  /* ... */
  "iconSets": {
    "custom-icons": "app/storefront/src/assets/icon-pack/custom-icons"
  }
}
```

You can use your custom icons by specifying your icon pack:

twig

```shiki
{% sw_icon 'done-outline-24px' style {
    'pack': 'custom-icons'
} %}
```

WARNING

This setup is mandatory if you ship your Theme as an App, because otherwise your custom icons can't be loaded.

---

## Theme inheritance

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/add-theme-inheritance.html

# Theme Inheritance [​](#theme-inheritance)

## Overview [​](#overview)

This guide explains how you can extend an existing theme. What are use cases to inherit from another theme? Maybe you already use a specific theme for a sales channel and you want to use it in another sales channel for a different project with slight changes.

For example, imagine you want to use a dark version of the theme, so you have different looks for different sales channels. Or maybe you own a store-bought theme and only need to change the appearance of it without changing the code of the theme itself. Sometimes it could be useful to develop some kind of base theme and customize it for different clients.

## Prerequisites [​](#prerequisites)

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which you want to extend. Let's imagine we already have an installed and activated theme called `SwagBasicExampleTheme`.

## Extending an existing theme with a new theme [​](#extending-an-existing-theme-with-a-new-theme)

The first step is to create a new theme which will extend the existing `SwagBasicExampleTheme`. Checkout the [Create a first theme](./create-a-theme.html) guide if you don't know how to create a new theme. In this guide we call the extending theme `SwagBasicExampleThemeExtend`. After `SwagBasicExampleTheme` was installed, activated and assigned to a sales channel we need to set up the inheritance.

## Set up the inheritance [​](#set-up-the-inheritance)

To set up the inheritance we need to edit the theme configuration file called `theme.json` and it is located in the `<plugin root>/src/Resources` folder.

The content of the `theme.json` file looks like this:

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleThemeExtend",
  "author": "Shopware AG",
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleThemeExtend"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/swag-example-plugin-theme-extended/swag-example-plugin-theme-extended.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ]
}
```

As you can see each section `views`, `style`, `script` and `asset` contains the `@Storefront` placeholder. This means that inheritance is already taking place here. Every theme inherits the default theme of Shopware called `@Storefront`.

Now it is easy to see how we can inherit from our base theme `SwagBasicExampleTheme`. We just need to add it in the inheritance chain.

Here is an example:

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleThemeExtend",
  "author": "Shopware AG",
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme",
     "@SwagBasicExampleThemeExtend"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@SwagBasicExampleTheme",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "@SwagBasicExampleTheme",
    "app/storefront/dist/storefront/js/swag-example-plugin-theme-extended/swag-example-plugin-theme-extended.js"
  ],
  "asset": [
    "@Storefront",
    "@SwagBasicExampleTheme",
    "app/storefront/src/assets"
  ],
  "configInheritance": [
    "@Storefront",
    "@SwagBasicExampleTheme"
  ]
}
```

Let's walk over each section and have a closer look.

### `views` section [​](#views-section)

In the `views` section we added the placeholder `@SwagBasicExampleTheme` right before our current theme. This means that when a view gets rendered, the Storefront template is first used as the basis. The extensions of the installed plugins are applied to this. Next, the changes to the `@SwagBasicExampleTheme` theme are taken into account in the rendering process. Finally, the changes to our current theme are applied.

### `script` section [​](#script-section)

The same applies to the JavaScript `script` section. The javascript of the Storefront serves as the basis. On top of this come the extensions of the theme `@SwagBasicExampleTheme`. Finally, the JavaScript that we can implement in the current theme is applied.

### `style` section [​](#style-section)

The `style` section behaves similarly to the others. The only difference here is the `override.css` can affect SCSS variables e.g. `$border-radius`. That's why it's at the top of the list. To find out more about overriding variables check out the [Override Bootstrap variables in a theme](./override-bootstrap-variables-in-a-theme.html) guide.

### `asset` section [​](#asset-section)

If you want to use assets from the `@SwagBasicExampleTheme` you have add it to the list here as well.

### `configInheritance` section [​](#configinheritance-section)

Finally, the `configInheritance` section will use the field configuration from the given themes and defines the last of the themes, that is different from the current theme, as the parent theme. The configuration values are inherited from the themes mentioned in `configInheritance`. The Storefront theme configuration will always be inherited, even if no `configInheritance` is given. See [Theme inheritance configuration](./theme-inheritance-configuration.html) for a more detailed example.

## Next steps [​](#next-steps)

Now that you know how the theme inheritance works you can start with own customizations. Here is a list of other related topics where assets can be used.

* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Customize templates](./../plugins/storefront/customize-templates.html)

---

## Theme with Bootstrap styling

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/add-theme-inheritance-without-resources.html

# Theme with Bootstrap Styling [​](#theme-with-bootstrap-styling)

## Overview [​](#overview)

The Shopware default theme is using [Bootstrap](https://getbootstrap.com/) with additional custom styling. But sometimes you want to develop a theme without the Shopware default styling.

## Theme without Shopware default styling [​](#theme-without-shopware-default-styling)

If you want to build your theme only upon the Bootstrap SCSS you can use the `@StorefrontBootstrap` placeholder instead of the `@Storefront` bundle in the `style` section of your `theme.json`. This gives you the ability to use the Bootstrap SCSS without the Shopware Storefront "skin". Therefore all the SCSS from `<plugin root>src/Storefront/Resources/app/storefront/src/scss/skin` will not be available in your theme.

javascript

```shiki
// <plugin root>/src/Resources/theme.json
{
  ...
  "style": [
    "@StorefrontBootstrap",
    "@Plugins",
    "app/storefront/src/scss/base.scss"
  ]
}
```

INFO

* This option can only be used in the `style` section of the `theme.json`. You must not use it in `views` or `script`.
* All theme variables like `$sw-color-brand-primary` are also available when using the Bootstrap option.
* You can only use either `@StorefrontBootstrap` or `@Storefront`. They should not be used at the same time. The `@Storefront` bundle **includes** the Bootstrap SCSS already.
* `@StorefrontBootstrap` does not include `@Plugins`, you have to add it yourself.

## Next steps [​](#next-steps)

Here is a list of related topics which might be interesting for you.

* [Theme configuration](./theme-configuration.html)
* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Add assets to theme](./add-assets-to-theme.html)

---

## Theme inheritance configuration

**Source:** https://developer.shopware.com/docs/guides/plugins/themes/theme-inheritance-configuration.html

# Theme Inheritance Configuration [​](#theme-inheritance-configuration)

INFO

The `configInheritance` is available from Shopware Version 6.4.8.0

## Overview [​](#overview)

This guide explains how you can use a theme as a basic corporate design theme and create inherited themes for special purposes like holiday time or a sales week.

Imagine you have a theme that is applying your corporate design to the storefront. With your colors, your logo and other configuration fields. But on a special week in the year, you have additional requirements for a special design, like a discount counter or an advent calendar.

## Setup [​](#setup)

### Create two themes [​](#create-two-themes)

Create the two themes like described in [Theme inheritance](./add-theme-inheritance.html).

### Configure your themes [​](#configure-your-themes)

Add some configuration fields you need in your basic theme inside the `theme.json` of the `SwagBasicExampleTheme`

## Extending an existing theme configuration with a new theme [​](#extending-an-existing-theme-configuration-with-a-new-theme)

Add configurations to your extended theme

In this theme (`SwagBasicExampleThemeExtend`) all the configuration fields from the themes `Storefront` and `SwagBasicExampleTheme` will be used as inherited values. They will be shown in the Administration with an inherit anchor and will use the value of the parent themes as long as they are not set to a different value. In the `theme.json` the `sw-brand-icon` field value will be overwritten with a different default value. So this field will not be inherited regardless that it is already defined in the `SwagBasicExampleTheme`. This theme also adds a new field for the background color of the advent calendar (`sw-advent-calendar-background-color`) because this is only needed in this special theme which will only be used for 4-6 weeks a year.

## Next steps [​](#next-steps)

Now that you know how the theme inheritance works you can start with own customizations. Here is a list of other related topics where assets can be used.

* [Add SCSS Styling and JavaScript to a theme](./add-css-js-to-theme.html)
* [Customize templates](./../plugins/storefront/customize-templates.html)

---

