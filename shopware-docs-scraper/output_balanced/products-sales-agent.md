# Products Sales Agent

*Scraped from Shopware Developer Documentation*

---

## Sales Agent

**Source:** https://developer.shopware.com/docs/products/sales-agent/

# Sales Agent Overview [​](#sales-agent-overview)

This project is designed to streamline the communication and sales processes between sales representatives and their customers. By integrating Shopware, it enables sales representatives to handle various tasks in an optimized environment, without the overhead added by the Shopware Administration.

![ ](/assets/sales-agent-overview.D8XPCgkf.jpg)

INFO

**Sales Agent** is a licensed application and not available as open source.

INFO

The **Sales Agent** application does not belong to the *default Storefront*. It is a standalone Frontend app running with Nuxt instance. This template will be hosted in a separate instance with a new domain, which will be different from the Storefront domain.

To get access to the private Gitlab repository, create a support ticket in your [Shopware Account](https://account.shopware.com). Access is granted after a short validation or a purchase of the Beyond or the Evolve license.

## Prerequisites [​](#prerequisites)

Review the below minimum operating requirements before you install *Sales Agent* on your infrastructure:

* [node](https://nodejs.org/en) >= v18
* [pnpm](https://pnpm.io/installation) >= 8
* [Shopware Frontends framework](https://frontends.shopware.com/) based on [Nuxt 3](https://nuxt.com/).
* Instance of [Shopware 6](./../../guides/installation/) (version 6.7.3 and above).
* Database: MySQL
* Beyond or Evolve license needed for the Shopware instance.

## API Documentation [​](#api-documentation)

[API documentation](https://shopware.stoplight.io/docs/swag-sales-agent/) provides detailed information about the available endpoints and their functionalities.

## Architecture [​](#architecture)

![ ](/assets/sales-agent-architecture.BFEICDVe.jpg)

The architecture depicted in the image shows a system with the following components:

* **Frontend**: Using Vue.
* **Backend**: Nuxt uses Nitro as its server engine.
* **Database**: Uses MySQL. Nuxt interacts with the backend through [Prisma](https://www.prisma.io/).
* **Cache Layer**: Uses Redis. Nitro provides a caching system built on top of the storage layer.

---

## Customization

**Source:** https://developer.shopware.com/docs/products/sales-agent/customization/

# Sales Agent Customization [​](#sales-agent-customization)

This section explains how to customize the *Sales Agent* frontend. It is built with Nuxt 3 and leverages the [Nuxt Layer concept](https://nuxt.com/docs/getting-started/layers), allowing you to override file content with your own Nuxt layer for easy customization.

## Create a new Nuxt layer [​](#create-a-new-nuxt-layer)

If you look into the source code, you'll find the default Nuxt layer named `sales-agent`. This layer should remain untouched. To apply customizations, you should create a new Nuxt layer and import it in `nuxt.config.ts`. For more details, refer to the [composition guide](https://nuxt.com/docs/guide/going-further/layers). Besides, we’ve also created a customization layer named `example` within the frontend source code. You can rename this layer and modify its contents to suit your needs.

---

## Branding Customization

**Source:** https://developer.shopware.com/docs/products/sales-agent/customization/branding.html

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

Sales Agent utilizes the Shopware [Meteor Component Library](https://shopware.design/get-started/installation.html), which provides a comprehensive CSS variable system to manage themes. The default theme is aligned with their design system, ensuring consistency across applications. This package offers both a [light theme](https://github.com/shopware/meteor/blob/main/packages/tokens/deliverables/administration/light.css) and a [dark theme](https://github.com/shopware/meteor/blob/main/packages/tokens/deliverables/administration/dark.css), allowing you to explore and utilize the CSS variable system effectively.

### Customizing Theme Colors [​](#customizing-theme-colors)

To tailor the theme to your brand's identity, you can override the default CSS variables. By defining custom values in your own CSS file, you can seamlessly adapt the visual aspects of the application:

css

```shiki
/* main.css */
:root {
  --color-interaction-primary-default: #80A1BA; /* Add your primary color */
  /* Add more customizations as needed */
}
```

### Integrating Custom Styles in Nuxt.js [​](#integrating-custom-styles-in-nuxt-js)

To apply these customizations in your application, import the CSS file into your Nuxt configuration. This will ensure that your branding colors take effect across the app:

javascript

```shiki
// nuxt.config.ts
export default defineNuxtConfig({
  css: ["./main.css"], // Include your custom CSS file
});
```

By doing so, you maintain the flexibility of the Shopware system while aligning it with your unique brand style, providing a cohesive user experience.

---

## I18n Customization

**Source:** https://developer.shopware.com/docs/products/sales-agent/customization/i18n.html

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
  locales: [
    {
      code: "en-GB",
      iso: "en-GB",
      file: "en-GB.ts",
    },
    {
      code: "de-DE",
      iso: "de-DE",
      file: "de-DE.ts",
    },
  ],
},
```

## Create the i18n Folder in the custom layer [​](#create-the-i18n-folder-in-the-custom-layer)

To customize the i18n functionality, we need to create a new folder structure in your custom layer. You will mirror the default layer's structure, but only create the files you need to override.

Take a look on `example` layer to understand the structure.

---

## Component Customization

**Source:** https://developer.shopware.com/docs/products/sales-agent/customization/component.html

WARNING

All customization instructions will refer to changes made within your customization layer folder.

# Component Customization [​](#component-customization)

In this document, we will demonstrate how to customize a component (e.g, the login page) in the Sales Agent frontend using the Nuxt layer concept. This guide will help you understand the process of extending or modifying the default components in your frontend without altering the core files.

## Understand the component structure of the default layer [​](#understand-the-component-structure-of-the-default-layer)

Before customizing any components, it's essential to understand the structure of the default layer. Navigate to the `~/layers/sales-agent` directory to view all available components.

In this case, look for the `login.vue` component inside `sales-agent/pages/auth`.

## Create the component in the custom layer [​](#create-the-component-in-the-custom-layer)

Now, inside your custom layer, paste the copied `login.vue` file. You should now have the same default component in your custom-layer directory, ready for modification. Once you have copied the component to your custom layer, modify the part of the component that you want to change. For instance, you may want to change the style, add new functionality, or update the template. At this point, the frontend app will ignore the `login.vue` from the default layer and only use the `login.vue` from the custom layer.

See example in the layer `example` of source code.

---

## Frontend App Deployment

**Source:** https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/

# Frontend App Deployment [​](#frontend-app-deployment)

According to [Shopware Frontends deployment document](https://frontends.shopware.com/best-practices/deployment.html), all the templates which were generated by Shopware Frontends can be deployed in multiple ways, depending on the setup you are using. Most likely you will be using either a static hosting service or a server with a Node.js runtime.

You may find the different approaches as described in [Nuxt instruction](https://nuxt.com/deploy).

Alternatively, we will show some best practices of *Sales Agent* frontend app deployment.

---

## Ubuntu Server with PM2

**Source:** https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/hosted-with-ubuntu-server.html

# Deploy with Ubuntu Server with PM2 [​](#deploy-with-ubuntu-server-with-pm2)

This guide will walk you through the steps to deploy Sales Agent frontend web application to an Ubuntu server using [PM2](https://nuxt.com/docs/getting-started/deployment#pm2), a process manager for Node.js applications. PM2 will help you keep your app running in the background, restart it automatically when it crashes, and manage logs for easier troubleshooting.

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

## Setup Redis [​](#setup-redis)

Redis is required for caching. You can either install Redis locally on your Ubuntu server or use a managed Redis service.

### Option 1: Install Redis locally [​](#option-1-install-redis-locally)

Install Redis using the package manager:

bash

```shiki
sudo apt update
sudo apt install redis-server
```

Configure Redis for production by editing the configuration file:

bash

```shiki
sudo nano /etc/redis/redis.conf
```

Key settings to consider:

* Set `supervised systemd` to integrate with systemd.
* Configure `bind` to restrict access (e.g., `bind 127.0.0.1` for local only).
* Set a password with `requirepass your_secure_password`.

Enable and start the Redis service:

bash

```shiki
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Verify Redis is running:

bash

```shiki
# If you configured a password with requirepass
redis-cli -a your_secure_password ping

# If no password is set
redis-cli ping
```

You should see `PONG` as a response.

### Option 2: Use a managed Redis service [​](#option-2-use-a-managed-redis-service)

Alternatively, you can use managed Redis services such as:

* [Upstash](https://upstash.com/) - Serverless Redis with pay-per-request pricing.
* [Redis Cloud](https://redis.com/cloud/overview/) - Managed Redis by Redis Ltd.

These services provide connection details (host, port, password) that you configure in your `.env` file.

### Configure Redis environment variables [​](#configure-redis-environment-variables)

Add these Redis environment variables to your `.env` file:

bash

```shiki
REDIS_CACHE=true
REDIS_HOST=127.0.0.1  # For local installation, or your managed service endpoint
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_password  # If configured with requirepass
REDIS_TLS=false  # Set to true for managed services that require TLS
```

For managed Redis services like Upstash, use the connection details provided by the service (host, port, password, and set `REDIS_TLS=true` for secure connections).

## Build code [​](#build-code)

* Please follow instructions here to [set up all necessary things and build the code](./../../installation.html#setup-app-server)

## Start the Application with PM2 [​](#start-the-application-with-pm2)

Now that your app is built, create a file named `ecosystem.config.cjs` in the root of your project with the following content. Ensure that the script path points to your app's build output directory (e.g., `.output/server/index.mjs` for Nuxt 3)

js

```shiki
module.exports = {
  apps: [
    {
      name: "SalesAgentApp",
      port: "3000",
      exec_mode: "cluster",
      instances: "max",
      script: "./.output/server/index.mjs",
    },
  ],
};
```

Once saved, you can start the app with:

bash

```shiki
pm2 start ecosystem.config.cjs
```

---

## AWS

**Source:** https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/aws.html

# Deploy with AWS Amplify [​](#deploy-with-aws-amplify)

In this chapter, you will learn how to deploy the frontend source code to [AWS Amplify](https://aws.amazon.com/amplify/).

## Prerequisites [​](#prerequisites)

* Register an AWS account.
* Clone the frontend source code and push it to your Git repository (for example, GitHub).

## Setup Redis with Amazon ElastiCache [​](#setup-redis-with-amazon-elasticache)

AWS Amplify does not include Redis by default. To use Redis for caching, you need to set up [Amazon ElastiCache](https://aws.amazon.com/elasticache/) or use an external Redis provider.

### Option 1: Amazon ElastiCache [​](#option-1-amazon-elasticache)

Amazon ElastiCache is a fully managed in-memory data store service compatible with Redis.

1. Navigate to the [ElastiCache Console](https://console.aws.amazon.com/elasticache/).
2. Click "Create" and select "Redis OSS" as the cluster engine.
3. Configure your cluster settings (node type, number of replicas, etc.).
4. Configure security groups to allow access from your Amplify application.
5. Once created, note the **Primary Endpoint** for your Redis connection.

WARNING

ElastiCache runs within a VPC. Connecting from AWS Amplify (which runs outside VPC by default) requires additional configuration such as VPC peering or using a public endpoint. For serverless applications, consider using Option 2.

### Option 2: Serverless Redis providers [​](#option-2-serverless-redis-providers)

For easier integration with serverless deployments like AWS Amplify, consider using:

* [Upstash](https://upstash.com/) - Serverless Redis with REST API support, ideal for edge/serverless environments.
* [Redis Cloud](https://redis.com/cloud/overview/) - Managed Redis with public endpoints.

These providers offer public endpoints that work seamlessly with AWS Amplify without VPC configuration.

### Configure Redis environment variables [​](#configure-redis-environment-variables)

After setting up Redis (ElastiCache or a serverless provider), configure these environment variables in AWS Amplify:

bash

```shiki
REDIS_CACHE=true
REDIS_HOST=your-redis-endpoint.cache.amazonaws.com  # Or your provider's endpoint
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_TLS=true  # Recommended for production
```

Add these variables in the AWS Amplify Console under "Environment variables" in your app settings, or include them in your `.env.template` file.

## Deploy [​](#deploy)

* Login to the AWS Amplify Hosting Console.
* Create a new app in AWS Amplify.
* Select and authorize access to your Git repository provider and select the main branch (it will auto-deploy when there are some changes in the main branch).
* Choose a name for your app and make sure build settings are auto-detected.
* Set Environment variables which are declared in `.env.template` under the Advanced Settings section.
* Confirm the configuration and click on "Save and Deploy".

## Custom domain [​](#custom-domain)

After deploying your code to AWS Amplify, you may wish to point custom domains (or subdomains) to your site. AWS has an [instruction](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html).

---

## Cloudflare

**Source:** https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/cloudflare.html

# Deploy with Cloudflare [​](#deploy-with-cloudflare)

In this chapter you will learn how to deploy the frontend source code to [Cloudflare Pages](https://pages.cloudflare.com/).

## Prerequisites [​](#prerequisites)

* Register a Cloudflare account.
* Clone the frontend source code and push to your GitHub repository.

## Setup Redis with Upstash [​](#setup-redis-with-upstash)

Cloudflare Pages/Workers do not include a built-in Redis service. [Upstash](https://upstash.com/) is the recommended serverless Redis provider that integrates natively with Cloudflare.

### Create an Upstash Redis database [​](#create-an-upstash-redis-database)

1. Sign up at [Upstash Console](https://console.upstash.com/).
2. Click "Create Database" and select a region close to your users.
3. Once created, navigate to the database details page.
4. Copy the connection details:
   * **REDIS\_HOST**: The endpoint URL (e.g., `xxx.upstash.io`)
   * **REDIS\_PORT**: Usually `6379` or the TLS port `6380`
   * **REDIS\_PASSWORD**: The password from the database details
   * **REDIS\_TLS**: Set to `true` for secure connections

### Configure environment variables [​](#configure-environment-variables)

Add these Redis environment variables to your `.env` file:

bash

```shiki
REDIS_CACHE=true
REDIS_HOST=your-database.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your_upstash_password
REDIS_TLS=true
```

### Cloudflare integration (optional) [​](#cloudflare-integration-optional)

You can also set up the Upstash integration directly in Cloudflare:

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) → Workers & Pages → Your project.
2. Navigate to Settings → Integrations.
3. Find and add the Upstash integration.
4. Follow the prompts to connect your Upstash account.

## Deploy from a local machine [​](#deploy-from-a-local-machine)

* Due to this [issue](https://github.com/nuxt/nuxt/issues/28248), just make sure your `.npmrc` file has the following content:

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

* Make sure the Frontend app has already [generated an .env file](./../../installation.html#create-a-env-file)
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
* In GitHub environment variables, create new environment named `production` and fill it with all environment variables in `.env.template`.
  + Besides `production`, we can add new values for the same variable names in multiple environments such as `development`, `staging`.

### Setup pipeline [​](#setup-pipeline)

To trigger the deployment automatically, we can attach the GitHub Actions.

* Create a `.github/workflows/publish.yml` file in your repository with the below sample content.

WARNING

Please note that this pipeline is just a sample. There are some points need to update for a specific purpose

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
          echo COMPANY_NAME=${{ vars.COMPANY_NAME }} >> .env
          echo ORIGIN=${{ vars.ORIGIN }} >> .env
          echo REDIS_CACHE=${{ vars.REDIS_CACHE }} >> .env
          echo REDIS_HOST=${{ vars.REDIS_HOST }} >> .env
          echo REDIS_PORT=${{ vars.REDIS_PORT }} >> .env
          echo REDIS_PASSWORD=${{ vars.REDIS_PASSWORD }} >> .env
          echo REDIS_TLS=${{ vars.REDIS_TLS }} >> .env
          echo APP_NAME=${{ vars.APP_NAME }} >> .env
          echo APP_SECRET=${{ vars.APP_SECRET }} >> .env
          echo DATABASE_URL=${{ vars.DATABASE_URL }} >> .env

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
          wranglerVersion: "3"
```

* Replace `YOUR_ACCOUNT_ID` with your account ID. Get it from the dashboard URL. E.g: `https://dash.cloudflare.com/<ACCOUNT_ID>/pages`.
* Replace `YOUR_PROJECT_NAME` with the appropriate value.

## Custom domain [​](#custom-domain)

When deploying your Pages project, you may wish to point custom domains (or subdomains) to your site. Cloudflare has an [instruction](https://developers.cloudflare.com/pages/configuration/custom-domains/).

---

## Local installation

**Source:** https://developer.shopware.com/docs/products/sales-agent/installation.html

# Local installation [​](#local-installation)

## Prepare [​](#prepare)

Obtain all the credentials to connect to the following services:

* Database (MySQL).
* Cache layer (Redis).

## Setup App Server [​](#setup-app-server)

### Clone the Repository [​](#clone-the-repository)

shell

```shiki
git clone https://github.com/shopware/swagsalesagent.git
cd swagsalesagent
```

### Create a `.env` File [​](#create-a-env-file)

* Use the provided `.env.template` file as an example.

shell

```shiki
cp .env.template .env
```

Fill in the required details in the `.env` file. All detailed explanations of the properties are written in the `.env.template`.

### Install dependencies [​](#install-dependencies)

shell

```shiki
pnpm install --frozen-lockfile --prefer-offline
```

### Migrate Database [​](#migrate-database)

Choose one of the following commands based on your needs:

* Execute existing migrations without creating new files:

bash

```shiki
  pnpm db:migration:deploy
```

* Execute & create new migration files if there are schema changes:

bash

```shiki
  pnpm db:migration:dev
```

### Run the Development Server [​](#run-the-development-server)

shell

```shiki
pnpm dev
```

### Build code for Production [​](#build-code-for-production)

shell

```shiki
pnpm build
```

## Connect App to Shopware Instance [​](#connect-app-to-shopware-instance)

* Build zip

bash

```shiki
pnpm app:build
```

* Upload zip from `bundle/swagsalesagent.zip` into Shopware Extensions.
* Verify the Installed App: after installation, you should see the Sales Agent menu item appear in the Settings.

![ ](/assets/sales-agent-item.B06K2eVc.png)

---

## Testing

**Source:** https://developer.shopware.com/docs/products/sales-agent/testing.html

# Testing [​](#testing)

## Unit Tests [​](#unit-tests)

[Vitest](https://vitest.dev/) is used for unit testing. The tests are located in the `tests` directory.

## Running Tests [​](#running-tests)

**Unit Tests**

bash

```shiki
pnpm run test
```

**Coverage**

bash

```shiki
pnpm run test:coverage
```

---

