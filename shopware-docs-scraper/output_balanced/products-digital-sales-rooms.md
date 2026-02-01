# Products Digital Sales Rooms

*Scraped from Shopware Developer Documentation*

---

## Digital Sales Rooms

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/

# Digital Sales Rooms Overview [​](#digital-sales-rooms-overview)

*Digital Sales Rooms* is a state-of-the-art new feature that seamlessly integrates into your Shopware system landscape and co-operates with your existing e-commerce infrastructure.

You can create interactive live video events for your customers straight from your Shopware website without having to switch between a presentation tool, video conferencing system, and store system. It is one sophisticated solution to highlight your products, engage your customers, and reinforce brand loyalty.

![ ](/assets/products-digitalSalesRooms.egDcSICT.png)

WARNING

*Digital Sales Rooms* is a license extension and is not available as open source.

WARNING

*Digital Sales Rooms* application does not belong to *the default Storefront*. It's a standalone Frontend app running with Nuxt instance. This template will be hosted in a separate instance with a new domain, which will be different from the Storefront domain.

To use the Digital Sales Rooms plugin, you must perform **installation** & **3rd parties setup** & **plugin configuration**.

## Prerequisites [​](#prerequisites)

Review the below minimum operating requirements before you install the *Digital Sales Rooms* feature:

* [node](https://nodejs.org/en) >= v18
* [pnpm](https://pnpm.io/installation) >= 8
* [Shopware Frontends framework](https://frontends.shopware.com/) based on Nuxt 3.
* Instance of [Shopware 6](./../../guides/installation/) (version 6.6.0 and above).
  + Recommend installing with [devenv](./../../guides/installation/setups/devenv.html)
* Third party services:
  + [Daily.co](https://www.daily.co/) - Refer to setup instructions for [realtime video call](./setup-3rd-party/realtime-video-dailyco.html)
  + [Mercure](https://mercure.rocks/)- Refer to setup instructions for [realtime Mercure service](./setup-3rd-party/realtime-service-mercure.html)

---

## Installation

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/installation/

# Digital Sales Rooms Installation [​](#digital-sales-rooms-installation)

WARNING

This section will show how to install **Digital Sales Rooms** plugin into the existing Shopware platform. It will not explain a Shopware platform installation.

INFO

Before we start, lets assume Shopware platform is running at `https://shopware.store` & frontend app will run in `https://dsr.shopware.io`.

This includes installation at admin and at template.

---

## Admin side installation

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/installation/admin-side-installation.html

# Admin Side Installation [​](#admin-side-installation)

INFO

Digital Sales Rooms plugin is a licensed plugin. If you already know how to install a licensed plugin, you can skip this part.

WARNING

As part of the Shopware Beyond plan, the **Digital Sales Rooms** is available to you as an extension. Same with other plugins, you have multiple ways to install the plugin via composer, direct download or through your Shopware Account.

In this part, we will learn how to get and install the **Digital Sales Rooms** plugin into local Shopware instance.

## Get the plugin [​](#get-the-plugin)

If you are a merchant with **Shopware Beyond**, you can access [account.shopware.com](https://auth.shopware.com/login?return_to=https:%2F%2Faccount.shopware.com%2Fportal) and create a [wildcard environment](https://docs.shopware.com/en/account-en/extension-partner/wildcard-environments?category=account-en/extension-partner) with attached plugins.

![ ](/assets/products-digitalSalesRooms-wildcard.Db5qZtUH.png)

By this way, you can get the plugin quickly into Shopware instance in multiple ways (via composer, direct download or through your Shopware Account).

### Via composer [​](#via-composer)

To install a plugin via composer, follow these steps:

* From wildcard environment detail page, click on the plugin and then click on the "Install via composer" button.
* A modal will appear and contain all command lines to install.

### Via download [​](#via-download)

To install a plugin via download, follow these steps:

* From wildcard environment detail page, click on the plugin and then click on the “Download” button.
* Save the zip file to your computer.
* In your Shopware 6 instance source code, go to the `custom/plugins` directory.
* Extract the zip file into the `custom/plugins` directory with name `SwagDigitalSalesRooms`.

## Install & activate the plugin [​](#install-activate-the-plugin)

Once you fetch the plugin, you can run the Symfony commands below for activating the plugin:

bash

```shiki
# refresh the list of available plugins
bin/console plugin:refresh
# find the plugin **name** (first column on the list). In this case, it is "**SwagDigitalSalesRooms"**
bin/console plugin:install **SwagDigitalSalesRooms** --activate
# clear the cache afterward
bin/console cache:clear

# Now it is ready to use
```

---

## Frontend app installation

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/installation/app-installation.html

# Frontend App Installation [​](#frontend-app-installation)

WARNING

After finishing the installation of the plugin in Shopware, we will run and connect the frontend template with Shopware. The frontend template is built based on the Shopware Frontends framework, so it inherits from Shopware Frontends & Nuxt 3 concepts.

## Get the frontend template [​](#get-the-frontend-template)

* From the **Digital Sales Rooms** plugin, you can find the dsr-frontends folder by:

shell

```shiki
cd ./templates/dsr-frontends
```

* This folder contains all the source code for the frontend template. You can copy the entire source code and push it to your own private repository for easy customization in the future.

## How to run? [​](#how-to-run)

### Generate env file [​](#generate-env-file)

shell

```shiki
cp .env.template .env
```

| Key | Required? | Description |
| --- | --- | --- |
| ORIGIN | Yes | This is current frontend app domain. E.g: `https://dsr.shopware.io` |
| SHOPWARE\_STOREFRONT\_URL | Yes | This is default Shopware storefront domain. E.g: `https://shopware.store` |
| SHOPWARE\_ADMIN\_API | Yes | This is Shopware admin-api domain server. E.g: `https://shopware.store/admin-api` |
| SHOPWARE\_STORE\_API | Yes | This is the Shopware store-api domain server. E.g: `https://shopware.store/store-api` |
| SHOPWARE\_STORE\_API\_ACCESS\_TOKEN | Yes | This is the Shopware Access Token to connect to Shopware API. Head to sales channel you assign the *Digital Sales Rooms* domain, find the `API access` section, and copy the `API access key` |
| ALLOW\_ANONYMOUS\_MERCURE | No | This is the flag for development only. When the value = 1, it means your app is running with unsecured Mercure. |

Example .env:

shell

```shiki
ORIGIN=https://dsr.shopware.io
SHOPWARE_STOREFRONT_URL=https://shopware.store
SHOPWARE_ADMIN_API=https://shopware.store/admin-api
SHOPWARE_STORE_API=https://shopware.store/store-api
SHOPWARE_STORE_API_ACCESS_TOKEN=XXXXXXXXXXX
```

### For development [​](#for-development)

* Install pnpm with global scope

shell

```shiki
npm install -g pnpm
```

* Install dependencies

shell

```shiki
pnpm install
```

* Run dev server

shell

```shiki
pnpm dev
```

Usually, port `3000` is the default port so that you can access the domain of the Frontend App `http://localhost:3000/`

### For production [​](#for-production)

* Install pnpm with global scope

shell

```shiki
npm install -g pnpm
```

* Install dependencies

shell

```shiki
pnpm install
```

* Build

shell

```shiki
pnpm build
```

After the build, make the [deployment](./../best-practices/app-deployment/).

The following section guides you to 3rd party setup procedures.

---

## Setup 3rd parties

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/setup-3rd-party/

# Setup 3rd parties [​](#setup-3rd-parties)

This section will show you how to set up 3rd parties of *Digital Sales Rooms*.

* [Daily.co](https://www.daily.co/) - Refer to setup instructions for [realtime video call](./realtime-video-dailyco.html)
* [Mercure](https://mercure.rocks/)- Refer to setup instructions for [realtime Mercure service](./realtime-service-mercure.html)

The following sections give you a detailed setup procedure.

---

## Realtime Video Call - Daily.co

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/setup-3rd-party/realtime-video-dailyco.html

# Realtime Video Call - Daily.co [​](#realtime-video-call-daily-co)

The service is responsible for streaming a video between the attendees.

## Login Daily.co dashboard [​](#login-daily-co-dashboard)

* Go to the dashboard at: <https://dashboard.daily.co/>
* Login or register with the *Daily.co* account.

## Get the API key [​](#get-the-api-key)

* Visit the “developers” section on the left
* Copy the *API KEY* and paste it [here](./../configuration/plugin-config.html#video-and-audio)

![DailyAPIConfig](/assets/products-digitalSalesRooms-videoConfig.DyaS6u6p.png)

---

## Realtime Service - Mercure

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/setup-3rd-party/realtime-service-mercure.html

# Realtime Service - Mercure [​](#realtime-service-mercure)

INFO

Symfony provides a straightforward component, built on top of the [Mercure](https://symfony.com/doc/current/mercure.html) protocol, specifically designed for this class of use cases. [Mercure](https://mercure.rocks/docs/getting-started) is an open protocol designed from the ground up to publish updates from server to client. It is a modern and efficient alternative to timer-based polling and to WebSocket.

## Setup hub [​](#setup-hub)

There are different ways to set up Mercure; we choose the quickest and easiest for you below:

### Setup via Stackhero (Recommended) [​](#setup-via-stackhero-recommended)

INFO

💡 We tested the service provided by [StackHero](https://www.stackhero.io/en/services/Mercure-Hub/pricing). Depending on the expected traffic, you can easily switch between the plans. For a small demo among a few people at the same time, the “Hobby” plan is sufficient.

* Create the Stackhero account.
* Access the dashboard.
* In the **Stacks** menu item, click on **create a new stack** with the **Mercure Hub** service.
* When creating a stack successfully, tap into the Configure button. On this page, you will find the Mercure general settings.
  + *Hub url* - The hub URL.
  + *Hub public url* - The hub public URL, normally it's the same as the hub URL.
  + *Hub subscriber secret* - The JWT key used for authenticating subscribers
  + *Hub publisher secret* - The JWT key used for authenticating publishers

![ ](/assets/products-digitalSalesRooms-mercureConfigExample.D2yzqikn.png)

* Copy all the necessary information, and paste it into [the proper inputs of the configuration page](./../configuration/plugin-config.html#realtime-service).

![Mercure configuration](/assets/products-guidedShopping-mercureConfig.DyWI4VeR.png)

### Setup via Docker [​](#setup-via-docker)

WARNING

For security reasons, use different publisher and subscriber keys in production mode.

You can clone our [local-mercure-sample](https://github.com/shopware/local-mercure-sample) and run it with docker-compose.

## Config Mercure hub [​](#config-mercure-hub)

After init mercure hub, let's make it more secure with your information:

* *Set up CORS allowed origins* - In our case, it would be the domain where the Shopware Frontends is hosted and available. For instance: `https://dsr.shopware.io` (frontend domain).
* *Set up publish allowed origins* - The domains that request the Mercure service must be added to publish allowed origins, else it gets rejected. For instance (HTTP protocol must not be included): `https://dsr.shopware.io` (frontend domain) and `https://shopware.store` (backend API domain).
* *Set up the publisher (JWT) key* - Set whatever you want.
* *Set up the subscriber (JWT) key* - Set whatever you want.

---

## Configuration

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/configuration/

# Digital Sales Rooms Configuration [​](#digital-sales-rooms-configuration)

This section will show how to configure *Digital Sales Rooms* plugin. The following sections will give you a detailed procedure of configuration.

---

## Domain Configuration

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/configuration/domain-config.html

WARNING

Based on the business use case, the merchant can decide to add *Digital Sales Rooms* to their existing sales channel or new sales channel. When you run the frontend app server, you will always have a specific domain (eg: `https://dsr.shopware.io`)

# Domain Configuration for frontend app [​](#domain-configuration-for-frontend-app)

This section will show you how to add these domains to a sales channel.

## Setup domains for Digital Sales Rooms [​](#setup-domains-for-digital-sales-rooms)

WARNING

Please redeploy or rerun your frontend app to apply the domain changes into it.

* After specifying the sales channel, head to the *Domains section* and add appropriate *Digital Sales Rooms* domains with appropriate languages. *Digital Sales Rooms* can switch languages by the path, you can choose your domain path to represent a language. Here is our recommendation:

text

```shiki
https://dsr.shopware.io - English
https://dsr.shopware.io/de-DE - Deutsch
https://dsr.shopware.io/en-US - English (US)
```

![ ](/assets/setup-domain-for-sales-channel-DSR.B4W_CVOE.png)

* These *Digital Sales Rooms* domains should be selected as *Available domains* in [Configuration Page - Appointments](./plugin-config.html#appointments)

![ ](/assets/fill-domain-into-configuration.Bf6e20E0.png)

---

## Plugin Configuration

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/configuration/plugin-config.html

# Plugin Configuration [​](#plugin-configuration)

There are a lot of settings on the configuration page, but most of them are already filled by default. However, there are some settings that need to be set up.

## Navigate to the configuration page [​](#navigate-to-the-configuration-page)

Open Shopware CMS, select **Marketing** > **Digital Sales Rooms** > **Configuration**

![ ](/assets/products-digitalSalesRooms-configuration.tQFVjud6.png)

## Fill the settings [​](#fill-the-settings)

### Appointments [​](#appointments)

* *Available domains* - This select box shows the list of domains of all sales channels. You should choose the *Digital Sales Rooms* domains from [this section](./domain-config.html)

### Video and Audio [​](#video-and-audio)

* *API base url* - use value `https://api.daily.co/v1/`
* *API key* - get the value from [this section](./../setup-3rd-party/realtime-video-dailyco.html#get-the-api-key)

### Realtime service [​](#realtime-service)

* *Hub url*
* *Hub public url*
* *Hub subscriber secret*
* *Hub publisher secret*

Get the value of all these from [this section](./../setup-3rd-party/realtime-service-mercure.html#setup-via-stackhero-recommended)

---

## Configuration with CLI

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/configuration/config-with-cli.html

## Configuration with CLI [​](#configuration-with-cli)

Using the CLI for configuration is significantly faster than performing each setup manually. By executing the below command, you streamline the entire process, ensuring that all necessary configurations are applied efficiently and correctly in one go.

Make sure you are in the root folder of the plugin, run:

bash

```shiki
composer dsr:config
```

This command will automatically execute the following setup commands (If you prefer, you can also execute each setup command separately to configure specific parts individually):

1. **Domain Setup**

   * `composer dsr:domain-setup`
   * This command sets up the necessary domain configurations for **Digital Sales Rooms**.
2. **Daily.co Setup**

   * `composer dsr:daily-setup`
   * This command sets up Daily.co, which is essential for real-time video/audio calling within **Digital Sales Rooms**.
3. **Mercure Setup**

   * `composer dsr:mercure-setup`
   * This command sets up the Mercure hub, which is essential for real-time updates and notifications within **Digital Sales Rooms**.

---

## Customization

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/customization/

# Digital Sales Rooms Customization [​](#digital-sales-rooms-customization)

This section explains how to customize the *Digital Sales Rooms* frontend template. The DSR frontend is built with Nuxt 3 and leverages the [Nuxt Layer concept](https://nuxt.com/docs/getting-started/layers), allowing you to override file content with your own Nuxt layer for easy customization.

## Create a new Nuxt layer [​](#create-a-new-nuxt-layer)

If you look into the `dsr-frontends` template, you'll find the default Nuxt layer named `dsr`. This layer should remain untouched. To apply customizations, you should create a new Nuxt layer and import it in `nuxt.config.ts`. For more details, refer to the [composition guide](https://nuxt.com/docs/guide/going-further/layers). Besides, we’ve also created a customization layer named `example` within the frontend source code. You can rename this layer and modify its contents to suit your needs.

---

## Branding Customization

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/customization/branding.html

WARNING

All customization instructions will refer to changes made within your customization layer folder.

# Branding Customization [​](#branding-customization)

## Favicon [​](#favicon)

* Create `public` folder inside your layer (if missing).
* Place your favicon inside the `public` folder and ensure it is named `favicon.ico`.

## Web application title [​](#web-application-title)

* Create `nuxt.config.ts` inside your layer (if missing).
* Replace "Your app name" with your app's name and add the following code:

js

```shiki
app: {
  head: {
    title: 'Your app name'
  }
}
```

## Theme color [​](#theme-color)

* Create `uno.config.ts` inside your layer (if missing).
* For example, to change the primary color to `#000000`, add the following code:

js

```shiki
theme: {
  colors: {
    primary: {
      DEFAULT: '#000000'
    }
  }
}
```

* Refer to the `uno.config.ts` file in the dsr layer to understand the key structure for overriding colors.

---

## I18n Customization

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/customization/i18n.html

WARNING

All customization instructions will refer to changes made within your customization layer folder.

# I18n Customization [​](#i18n-customization)

This guide will walk you through the process of customizing the internationalization (i18n) setup in your Nuxt 3 project using the Nuxt layer concept. By using this method, you can extend and override the default i18n functionality to meet your specific requirements without modifying the core files.

## Configure i18n [​](#configure-i18n)

Configure the i18n settings in your `nuxt.config.ts` file. This configuration defines the language directory and any specific language configurations you want to override.

Add the following configuration to `nuxt.config.ts`:

js

```shiki
modules: [
  "@nuxtjs/i18n",
],
i18n: {
  langDir: "./i18n/src/langs/",
  ...i18nConfig,
},
```

## Create the i18n Folder in the custom layer [​](#create-the-i18n-folder-in-the-custom-layer)

To customize the i18n functionality, we need to create a new folder structure in your custom layer. You will mirror the default layer's structure, but only create the files you need to override.

Take a look on `example` layer to understand the structure.

---

## Component Customization

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/customization/component.html

WARNING

All customization instructions will refer to changes made within your customization layer folder.

# Component Customization [​](#component-customization)

In this document, we will demonstrate how to customize a component (specifically, the "Wishlist" button) in the DSR frontend template using the Nuxt layer concept. This guide will help you understand the process of extending or modifying the default components in your frontend without altering the core files.

## Understand the component structure of the default layer [​](#understand-the-component-structure-of-the-default-layer)

Before customizing any components, it's essential to understand the structure of the default layer. Navigate to the `dsr/components` directory to view all available components.

In this case, look for the `SwWishlistButton.vue` component inside `dsr/components/shared/molecules/`.

## Create the component in the custom layer [​](#create-the-component-in-the-custom-layer)

Now, inside your custom layer, paste the copied `SwWishlistButton.vue` file. You should now have the same default component in your custom-layer directory, ready for modification. Once you have copied the component to your custom layer, modify the part of the component that you want to change. For instance, you may want to change the style, add new functionality, or update the template. At this point, the frontend app will ignore the `SwWishlistButton` from the default layer and only use the `SwWishlistButton` from the custom layer.

---

## Frontend App Deployment

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/best-practices/app-deployment/

# Frontend App Deployment [​](#frontend-app-deployment)

According to [Shopware Frontends deployment document](https://frontends.shopware.com/best-practices/deployment.html), all the templates which were generated by Shopware Frontends can be deployed in multiple ways, depending on the setup you are using. Most likely you will be using either a static hosting service or a server with a Node.js runtime.

You may find the different approaches as described in [Nuxt instruction](https://nuxt.com/deploy).

Alternatively, we will show some best practices of *Digital Sales Room* frontend app deployment.

---

## Ubuntu Server with PM2

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/best-practices/app-deployment/hosted-with-ubuntu-server.html

# Deploy with Ubuntu Server with PM2 [​](#deploy-with-ubuntu-server-with-pm2)

This guide will walk you through the steps to deploy DSR frontend web application to an Ubuntu server using [PM2](https://nuxt.com/docs/getting-started/deployment#pm2), a process manager for Node.js applications. PM2 will help you keep your app running in the background, restart it automatically when it crashes, and manage logs for easier troubleshooting.

## Prerequisites [​](#prerequisites)

* **Ubuntu Server**: This guide assumes you have an Ubuntu server running, and you can access it via SSH.
* **Node.js & npm**: Make sure Node.js and npm (Node package manager) are installed on your server.
* **PM2**: PM2 should be installed globally.

bash

```shiki
npm install -g pm2
```

* **pnpm**

bash

```shiki
npm install -g pnpm
```

* **Frontend Application**: Clone the frontend source code and push to your GitHub repository.
  + Download the plugin zip. After extracting, you can find it inside `/templates/dsr-frontends`.

## Build code [​](#build-code)

* After you clone the source code into Ubuntu server, please follow the guide to [build env](./../../installation/app-installation.html#generate-env-file) & [build code for production](./../../installation/app-installation.html#for-production)

## Start the Application with PM2 [​](#start-the-application-with-pm2)

Now that your app is built, create a file named `ecosystem.config.cjs` in the root of your project with the following content. Ensure that the script path points to your app's build output directory (e.g., `.output/server/index.mjs` for Nuxt 3)

js

```shiki
module.exports = {
  apps: [
    {
      name: 'DSRNuxtApp',
      port: '3000',
      exec_mode: 'cluster',
      instances: 'max',
      script: './.output/server/index.mjs'
    }
  ]
}
```

Once saved, you can start the app with:

bash

```shiki
pm2 start ecosystem.config.cjs
```

---

## AWS

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/best-practices/app-deployment/aws.html

# Deploy with AWS Amplify [​](#deploy-with-aws-amplify)

In this chapter, you will learn how to deploy the frontend source code to [AWS Amplify](https://aws.amazon.com/amplify/).

## Prerequisites [​](#prerequisites)

* Register an AWS account.
* Clone the frontend source code and push it to your GitHub repository.
  + Download the plugin zip. After extracting it, you will find it inside `/templates/dsr-frontends`.
* Push source code to your Git repository.

## Deploy [​](#deploy)

* Login to the AWS Amplify Hosting Console.
* Create a new app in AWS Amplify.
* Select and authorize access to your Git repository provider and select the main branch (it will auto deploy when there are some changes in the main branch).
* Choose a name for your app and make sure build settings are auto-detected.
* Set Environment variables under the Advanced Settings section.
  + Add `SHOPWARE_STORE_API`, `SHOPWARE_ADMIN_API`, `SHOPWARE_STORE_API_ACCESS_TOKEN`, `SHOPWARE_STOREFRONT_URL`, `ORIGIN` variables with appropriate values.
* Confirm the configuration and click on "Save and Deploy".

## Custom domain [​](#custom-domain)

After deploying your code to AWS Amplify, you may wish to point custom domains (or subdomains) to your site. AWS has an [instruction](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html).

## Configure sales channel domain [​](#configure-sales-channel-domain)

Your website is ready, and you should have a frontend app domain. Please use the current domain to configure [sales channel domain](./../../configuration/domain-config.html).

---

## Cloudflare

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/best-practices/app-deployment/cloudflare.html

# Deploy with Cloudflare [​](#deploy-with-cloudflare)

In this chapter you will learn how to deploy the frontend source code to [Cloudflare Pages](https://pages.cloudflare.com/).

## Prerequisites [​](#prerequisites)

* Register a Cloudflare account.
* Clone the frontend source code and push to your GitHub repository.
  + Download the plugin zip. After extracting, you can find it inside `/templates/dsr-frontends`.

## Deploy from local machine [​](#deploy-from-local-machine)

* Due to this [issue](https://github.com/nuxt/nuxt/issues/28248), just make sure your `.npmrc` file has

bash

```shiki
shamefully-hoist=true
strict-peer-dependencies=false
```

* Install Wrangler

bash

```shiki
pnpm install wrangler --save-dev
```

* Make sure the Frontend app has already [generated .env file](./../../installation/app-installation.html#generate-env-file)
* Build your project for Cloudflare Pages:

bash

```shiki
npx nuxi build --preset=cloudflare_pages
```

* Then deploy. However, for the first time, it will ask you to create a project:

bash

```shiki
wrangler pages deploy dist/
```

## Automation with GitHub Actions [​](#automation-with-github-actions)

### Setup GitHub Secrets & variables [​](#setup-github-secrets-variables)

* In GitHub Secrets, add `CLOUDFLARE_API_TOKEN` with API token value.
  + [Create an API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) in the Cloudflare dashboard with the "Cloudflare Pages — Edit" permission.
* In GitHub environment variables, create new environment named `production`. Add `SHOPWARE_STORE_API`, `SHOPWARE_ADMIN_API`, `SHOPWARE_STORE_API_ACCESS_TOKEN`, `SHOPWARE_STOREFRONT_URL`, `ORIGIN` variables with appropriate values.
  + Besides `production`, we can add new values for the same variable names in multiple environments such as `development`, `staging`.

### Setup pipeline [​](#setup-pipeline)

To trigger the deployment automatically, we can attach the GitHub Actions.

* Create a `.github/workflows/publish.yml` file in your repository with below sample content.

WARNING

Please note that this pipeline is just a sample. There are some points need to update for specific purpose

yml

```shiki
on:
  push:
   # Specify the pipeline trigger
   branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    name: Cloudflare Pages Deployment
    # Specify the environment name
    environment: production
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - uses: pnpm/action-setup@v4
        name: Install pnpm
        with:
          version: 8
          run_install: false

      - name: Install dependencies
        run: |
          pnpm install

      - name: Build env file
        run: |
          touch .env
          # echo ALLOW_ANONYMOUS_MERCURE=${{ vars.ALLOW_ANONYMOUS_MERCURE }} >> .env
          echo SHOPWARE_STORE_API=${{ vars.SHOPWARE_STORE_API }} >> .env
          echo SHOPWARE_ADMIN_API=${{ vars.SHOPWARE_ADMIN_API }} >> .env
          echo SHOPWARE_STORE_API_ACCESS_TOKEN=${{ vars.SHOPWARE_STORE_API_ACCESS_TOKEN }} >> .env
          echo SHOPWARE_STOREFRONT_URL=${{ vars.SHOPWARE_STOREFRONT_URL }} >> .env
          echo ORIGIN=${{ vars.ORIGIN }} >> .env
          cat .env

      - name: Build code
        run: |
          npx nuxi build --preset=cloudflare_pages

      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1.5.0
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: YOUR_ACCOUNT_ID
          projectName: YOUR_PROJECT_NAME
          directory: dist
          wranglerVersion: '3'
```

* Replace `YOUR_ACCOUNT_ID` with your account ID. Get it from the dashboard URL. E.g: `https://dash.cloudflare.com/<ACCOUNT_ID>/pages`.
* Replace `YOUR_PROJECT_NAME` with the appropriate value.

## Custom domain [​](#custom-domain)

When deploying your Pages project, you may wish to point custom domains (or subdomains) to your site. Cloudflare has an [instruction](https://developers.cloudflare.com/pages/configuration/custom-domains/).

## Configure sales channel domain [​](#configure-sales-channel-domain)

Your website is ready, you should have a frontend app domain. Please use the current domain to configure [sales channel domain](./../../configuration/domain-config.html).

---

## SaaS

**Source:** https://developer.shopware.com/docs/products/digital-sales-rooms/best-practices/saas/

# Digital Sales Rooms with SaaS [​](#digital-sales-rooms-with-saas)

If you are a *Beyond merchant* and are using SaaS, the *Digital Sales Rooms* plugin is installed in your SaaS instance. So, you should see the *Digital Sales Rooms* section in the Marketing menu item. However, there are some steps that need to be completed to ensure the DSR functions fully with SaaS:

* [Deploy the frontend app](./../app-deployment/)
* [3rd parties](./../../setup-3rd-party/)
* [Configuration](./../../configuration/)

---

