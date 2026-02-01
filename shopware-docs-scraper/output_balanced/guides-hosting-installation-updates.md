# Guides Hosting Installation Updates

*Scraped from Shopware Developer Documentation*

---

## Installation & Updates

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/

# Installation and Updates [​](#installation-and-updates)

This section will brief you on cluster setup for custom stores, Shopware 6 production template, and deployment to an infrastructure.

---

## Deployments

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/deployments/

# Deployments [​](#deployments)

The following guide explains the fundamental steps to deploy Shopware 6 to a specific infrastructure and how to build assets for Shopware's Administration and Storefront without a database.

---

## Deployment with Deployer

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/deployments/deployment-with-deployer.html

# Deployment with Deployer [​](#deployment-with-deployer)

## Overview [​](#overview)

Automated deployments shouldn't be a pain and have several advantages, like lower failure rates and reproducible builds. Also, they increase overall productivity because actual testing can get more attention.

This article explains the fundamental steps to deploy Shopware 6 to a certain infrastructure, focussing on continuous deployment using [GitLab CI](https://docs.gitlab.com/ci/) or [GitHub Actions](https://github.com/features/actions) and [Deployer](https://deployer.org/) (a deployment tool written in PHP).

## Video [​](#video)

#### Continuous Deployment: Automizing Shopware 6 deployments (Developer Tutorial) - YouTube

## Prerequisites [​](#prerequisites)

Please make sure you already have a working Shopware 6 instance running and that your repository is based on the [Symfony Flex template](./../../../installation/template.html) because this article relies on some scripts to exist in your repository.

### Preparations before the first deployment [​](#preparations-before-the-first-deployment)

[Deployer](https://deployer.org/) has a default directory structure in which it organizes releases, shared files across releases (e.g., certificates, configuration, or media files) and the symlink to the current release.

The structure looks like this:

text

```shiki
├── .dep
├── current -> releases/1
├── releases
│   └── 1
└── shared
    ├── .env
    └── config
    └── ...
```

Suppose you haven't used such a structure yet, it is recommended to move the current document root contents to a different location because you will have to copy some existing files into the `shared` folder after your first deployment with [Deployer](https://deployer.org/).

For more information, refer to [Migrating existing instance to Deployer structure](./deployment-with-deployer.html#migrating-existing-instance-to-deployer-structure).

### Webserver configuration [​](#webserver-configuration)

Ensure to set the document root of the domain to `/var/www/shopware/current/public`, assuming `/var/www/shopware` is the path you are uploading Shopware to, but this can, of course, differ. The most important part of this path is `current`, which is the symlink to the currently active release.

Because `current` is a symlink, please also make sure your web server is configured to resolve/follow symlinks correctly.

### Require Deployer and deployment-helper [​](#require-deployer-and-deployment-helper)

Your project needs to have the following dependencies installed:

bash

```shiki
composer require deployer/deployer shopware/deployment-helper
```

## GitLab runner requirements [​](#gitlab-runner-requirements)

[GitLab pipelines](https://docs.gitlab.com/ci/pipelines/) are processed by [runners](https://docs.gitlab.com/runner/). Once a pipeline job is created, GitLab notifies a registered runner, and the job will then be processed by that runner.

The [GitLab runner](https://docs.gitlab.com/runner/) must have the following packages installed:

* PHP (see supported versions in the [System Requirements](https://docs.shopware.com/en/shopware-6-en/first-steps/system-requirements#environment))
* [NodeJS](https://nodejs.org/en/)
* [Node Package Manager (npm)](https://www.npmjs.com/)
* OpenSSH

This example uses the docker image `ghcr.io/shopware/shopware-cli:latest-php-8.3`. This image meets all requirements.

## Deployment steps [​](#deployment-steps)

### 1. Cloning the repository [​](#_1-cloning-the-repository)

The very first step in the pipeline is cloning the repository into the runner's workspace. GitLab does that automatically for every started job.

### 2. Building the project [​](#_2-building-the-project)

All the dependencies of your project must be installed. Shopware 6 uses [Composer](https://getcomposer.org/) for managing PHP dependencies and [Node Package Manager (NPM)](https://www.npmjs.com/) for frontend related dependencies.

We use Shopware CLI, which simplifies the installation of the dependencies and building the project assets to build a production-ready version of Shopware.

### 3. Transferring the workspace [​](#_3-transferring-the-workspace)

For transferring the files to the target server, please configure at least one host in the [`deploy.php`](./deployment-with-deployer.html#deploy-php):

php

```shiki
host('SSH-HOSTNAME')
    ->setLabels([
        'type' => 'web',
        'env'  => 'prod',
    ])
    ->setRemoteUser('www-data')
    ->set('deploy_path', '/var/www/shopware') // This is the path, where deployer will create its directory structure
    ->set('http_user', 'www-data') // Not needed, if the `user` is the same user, the webserver is running with 
    ->set('writable_mode', 'chmod');
```

This step is defined in the `deploy:update_code` job in the [`deploy.php`](./deployment-with-deployer.html#deploy-php):

php

```shiki
task('deploy:update_code')->setCallback(static function () {
    upload('.', '{{release_path}}', [
        'options' => [
            '--exclude=.git',
            '--exclude=deploy.php',
            '--exclude=node_modules',
        ],
    ]);
});
```

### 4. Applying migrations / install or update plugins [​](#_4-applying-migrations-install-or-update-plugins)

The migrations need to be applied on the target server.

DANGER

If you are deploying to a cluster with multiple web servers, please make sure to run the migrations only on one of the servers.

This step is defined in the `sw:deployment:helper` job in the [`deploy.php`](./deployment-with-deployer.html#deploy-php), which is part of the `sw:deploy` task group:

php

```shiki
task('sw:deployment:helper', static function() {
    run('cd {{release_path}} && vendor/bin/shopware-deployment-helper run');
});
```

### 5. Creating the `install.lock` file [​](#_5-creating-the-install-lock-file)

Before putting the new version live, ensure to create an empty file `install.lock` in the root of the build workspace. Otherwise, Shopware will redirect every request to the Shopware installer because it assumes that Shopware isn't installed yet.

This task is defined in the `sw:touch_install_lock` job in the [`deploy.php`](./deployment-with-deployer.html#deploy-php), which is part of the `sw:deploy` task group:

php

```shiki
task('sw:touch_install_lock', static function () {
    run('cd {{release_path}} && touch install.lock');
});
```

### 6. Running System Checks (Optional) [​](#_6-running-system-checks-optional)

Before putting the new version live, it is recommended to run the system checks to ensure that the new version is working correctly.

php

```shiki
task('sw:health_checks', static function () {
    run('cd {{release_path}} && bin/console system:check --context=pre_rollout');
});
```

> Before incorporating this step into your deployment process, make sure that you are well familiar with the [System Checks Concepts](./../../../../concepts/framework/system-check.html) and how to use and interpret the results [Custom usage](./../../../../guides/plugins/plugins/framework/system-check/), and the command [error codes](./../../../../guides/plugins/plugins/framework/system-check/#triggering-system-checks).

### 7. Switching the document root [​](#_7-switching-the-document-root)

After all the steps are done, Deployer will switch the symlinks destination to the new release.

This task is defined in the `deploy:symlink` default job in the [`deploy.php`](./deployment-with-deployer.html#deploy-php).

## Deployer output [​](#deployer-output)

This is the output of `dep deploy env=prod`:

text

```shiki
$ dep deploy env=prod               

✔ Executing task deploy:prepare
✔ Executing task deploy:lock
✔ Executing task deploy:release
✔ Executing task deploy:update_code
✔ Executing task deploy:shared
✔ Executing task sw:touch_install_lock
✔ Executing task sw:deployment:helper
✔ Executing task deploy:writable
✔ Executing task deploy:clear_paths
✔ Executing task deploy:symlink
✔ Executing task deploy:unlock
✔ Executing task cleanup
Successfully deployed!
```

## Migrating existing instance to Deployer structure [​](#migrating-existing-instance-to-deployer-structure)

After the very first deployment with Deployer, you have to copy some files and directories from your existing Shopware instance into the directory structure, that was created by Deployer.

Let's agree on the following two paths for the examples:

1. You have copied your existing Shopware instance to `/var/www/shopware_backup`.
2. You have set the `deploy_path` in the [`deploy.php`](./deployment-with-deployer.html#deploy-php) to `/var/www/shopware`.

Now, look at the `shared_files` and `shared_dirs` configurations in the [`deploy.php`](./deployment-with-deployer.html#deploy-php). Simply copy all the paths into `/var/www/shopware/shared`. For the configuration of the `deploy.php` the commands would be the following:

bash

```shiki
cp /var/www/shopware_backup/.env.local /var/www/shopware/shared/.env.local
cp -R /var/www/shopware_backup/custom/plugins /var/www/shopware/shared/custom
cp -R /var/www/shopware_backup/config/jwt /var/www/shopware/shared/config
cp -R /var/www/shopware_backup/config/packages /var/www/shopware/shared/config
cp -R /var/www/shopware_backup/files /var/www/shopware/shared
cp -R /var/www/shopware_backup/var/log /var/www/shopware/shared/var
cp -R /var/www/shopware_backup/public/media /var/www/shopware/shared/public
cp -R /var/www/shopware_backup/public/thumbnail /var/www/shopware/shared/public
cp -R /var/www/shopware_backup/public/sitemap /var/www/shopware/shared/public
```

## Generating a new SSH key [​](#generating-a-new-ssh-key)

To deploy your code to a server, you need to have an SSH key. If you don't have one yet, you can generate one with the following command:

bash

```shiki
ssh-keygen -t ed25519
```

It will be used in the above-mentioned GitLab CI/CD pipeline or GitHub Actions.

## Sources [​](#sources)

Have a look at the following files. All steps are provided with helpful comments.

### .gitlab-ci.yml [​](#gitlab-ci-yml)

yaml

```shiki
# This file defines the GitLab CI/CD pipeline.
# For more information, please visit the GitLab CI/CD docs: https://docs.gitlab.com/ee/ci/README.html
variables:
    GIT_STRATEGY: clone

# This variable holds all commands that are needed to be able to connect to the target server via SSH.
# For this you need to define two variables in the GitLab CI/CD variables:
#   - SSH_PRIVATE_KEY: The contents of the SSH private key file. The public key must be authorized on the target server.
#   - DEPLOYMENT_SERVER: Just the hostname of the target server (e.g. shopware.com, don't include schema or paths)
.configureSSHAgent: &configureSSHAgent |-
    eval $(ssh-agent -s)
    echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    mkdir -p ~/.ssh
    ssh-keyscan $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
    chmod 700 ~/.ssh

Deploy:
    stage: deploy
    # Tags are useful to only use runners that are safe or meet specific requirements
    image:
        name: ghcr.io/shopware/shopware-cli:latest
        entrypoint: [ "/bin/sh", "-c" ]
    before_script:
        # First, we need to execute all commands that are defined in the `configureSSHAgent` variable.
        - *configureSSHAgent
    script:
        # This command installs all dependencies and builds the project.
        - shopware-cli project ci .
        # This command starts the workflow that is defined in the `deploy` task in the `deploy.php`.
        # `production` is the stage that was defined in the `host` in the `deploy.php`
        - vendor/bin/dep deploy
```

### .github/workflows/deploy.yml [​](#github-workflows-deploy-yml)

yaml

```shiki
name: Deployment
on:
  push:
    branches: main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - name: Install Shopware CLI
        uses: shopware/shopware-cli-action@v1

      - name: Build
        run: shopware-cli project ci .

      - name: Deploy
        uses: deployphp/action@v1
        with:
          dep: deploy
          private-key: ${{ secrets.SSH_PRIVATE_KEY }}
```

### deploy.php [​](#deploy-php)

php

```shiki
<?php

namespace Deployer;

require_once 'recipe/common.php';
require_once 'contrib/cachetool.php';

set('bin/console', '{{bin/php}} {{release_or_current_path}}/bin/console');

set('cachetool', '/run/php/php-fpm.sock');
set('application', 'Shopware 6');
set('allow_anonymous_stats', false);
set('default_timeout', 3600); // Increase when tasks take longer than that.

// Hosts

host('SSH-HOSTNAME')
    ->setLabels([
        'type' => 'web',
        'env'  => 'production',
    ])
    ->setRemoteUser('www-data')
    ->set('deploy_path', '/var/www/shopware')
    ->set('http_user', 'www-data') // Not needed, if the `user` is the same, the webserver is running with
    ->set('writable_mode', 'chmod')
    ->set('keep_releases', 3); // Keeps 3 old releases for rollbacks (if no DB migrations were executed) 

// These files are shared among all releases.
set('shared_files', [
    '.env.local',
    'install.lock',
    'public/.htaccess',
    'public/.user.ini',
]);

// These directories are shared among all releases.
set('shared_dirs', [
    'config/jwt',
    'files',
    'var/log',
    'public/media',
    'public/plugins',
    'public/thumbnail',
    'public/sitemap',
]);

// These directories are made writable (the definition of "writable" requires attention).
// Please note that the files in `config/jwt/*` receive special attention in the `sw:writable:jwt` task.
set('writable_dirs', [
    'config/jwt',
    'custom/plugins',
    'files',
    'public/bundles',
    'public/css',
    'public/fonts',
    'public/js',
    'public/media',
    'public/sitemap',
    'public/theme',
    'public/thumbnail',
    'var',
]);

task('sw:deployment:helper', static function() {
   run('cd {{release_path}} && vendor/bin/shopware-deployment-helper run');
});

task('sw:touch_install_lock', static function () {
    run('cd {{release_path}} && touch install.lock');
});

task('sw:health_checks', static function () {
    run('cd {{release_path}} && bin/console system:check --context=pre_rollout');
});

desc('Deploys your project');
task('deploy', [
    'deploy:prepare',
    'deploy:clear_paths',
    'sw:deployment:helper',
    "sw:touch_install_lock",
    'sw:health_checks',
    'deploy:publish',
]);

task('deploy:update_code')->setCallback(static function () {
    upload('.', '{{release_path}}', [
        'options' => [
            '--exclude=.git',
            '--exclude=deploy.php',
            '--exclude=node_modules',
        ],
    ]);
});

// Hooks
after('deploy:failed', 'deploy:unlock');
after('deploy:symlink', 'cachetool:clear:opcache');
```

---

## Deployment Helper

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/deployments/deployment-helper.html

# Deployment Helper [​](#deployment-helper)

The Deployment Helper is a tool that unifies the steps executed after the Code has been uploaded to the server. On a traditional deployment, you would run it after the files have been uploaded. When using a Containerized environment, you would run Deployment Helper with the new source code and then switch over the traffic.

## Installing the Deployment Helper [​](#installing-the-deployment-helper)

The Deployment Helper is a composer package and can be installed via composer:

bash

```shiki
composer require shopware/deployment-helper
```

Then the helper can be executed via:

bash

```shiki
vendor/bin/shopware-deployment-helper run
```

## What does the Deployment Helper exactly do? [​](#what-does-the-deployment-helper-exactly-do)

The Deployment Helper checks for you, if Shopware is installed and if not, it will install it for you. It will also check if the database server is accessible, and if not, it will wait until it is.

Besides installing or updating Shopware, it also simplifies common tasks which normally are executed during the deployment like:

* Installing or updating the extensions (apps and plugins)
* Compiling the theme
* Run custom commands
* Run one time commands

## Execution Flow [​](#execution-flow)

## Configuration [​](#configuration)

The Deployment Helper can be configured via a `.shopware-project.yml` file in the root of your project. The following configuration options are available:

INFO

If you have multiple PHP versions locally or on your server, make sure to use `%php.bin%` instead of directly `php` in your custom scripts to use the same PHP version as the Deployment Helper.

yaml

```shiki
deployment:
  hooks:
    pre: |
      echo "Before deployment general"
    post: |
      echo "After deployment general"
    pre-install: |
      echo "Before running system:install"
    post-install: |
      echo "After running system:install"
    pre-update: |
      echo "Before running system:update"
    post-update: |
      echo "After running system:update"

  # Automatically installs and updates all extensions included in custom/plugins and custom/apps and composer
  extension-management:
    enabled: true

    # These extensions are not managed, you should use one-time-tasks to manage them
    exclude:
      - Name

    # These extensions are always updated even if their version does not change
    # This is useful for project-specific plugins that are not versioned
    force-update:
      - Name

    overrides:
      # the key is the extension name (app or plugin)
      MyPlugin:
        # Same as exclude
        state: ignore

      AnotherPlugin:
        # This plugin can be installed, but should be inactive
        state: inactive

      RemoveThisPlugin:
        # This plugin will be uninstalled if it is installed
        state: remove
        # should the extension data of an uninstalled extension be kept
        keepUserData: true

  one-time-tasks:
    - id: foo
      # Runs as last step in deployment. Other options is: first (to run before anything else)
      when: last # defaults to last
      script: |
        # runs one time in deployment, then never again
        ./bin/console --version

  store:
    license-domain: 'example.com'
```

## Environment Variables [​](#environment-variables)

Additionally, you can configure the Shopware installation using the following environment variables:

* `INSTALL_LOCALE` - The locale to install Shopware with (default: `en-GB`)
* `INSTALL_CURRENCY` - The currency to install Shopware with (default: `EUR`)
* `INSTALL_ADMIN_USERNAME` - The username of the admin user (default: `admin`)
* `INSTALL_ADMIN_PASSWORD` - The password of the admin user (default: `shopware`)
* `SALES_CHANNEL_URL` - The URL of the Storefront sales channel (default: `http://localhost`)
* `SHOPWARE_DEPLOYMENT_TIMEOUT` - The timeout allowed for setup commands, that are executed (default: `300`)
* `SHOPWARE_STORE_ACCOUNT_EMAIL` - The email address of the Shopware account
* `SHOPWARE_STORE_ACCOUNT_PASSWORD` - The password of the Shopware account
* `SHOPWARE_STORE_LICENSE_DOMAIN` - The license domain of the Shopware Shop (default: license-domain value in YAML file)
* `SHOPWARE_USAGE_DATA_CONSENT` - Controls Shopware Usage Data sharing (`accepted` or `revoked`), overwrites Administration choice

## One Time Tasks [​](#one-time-tasks)

One time tasks are tasks that should be executed only once during the deployment, like a migration script.

You can check with `./vendor/bin/shopware-deployment-helper one-time-task:list` which tasks were executed and when. To remove a task, use `./vendor/bin/shopware-deployment-helper one-time-task:unmark <id>`. This will cause the task to be executed again during the next update. To manually mark a task as run you can use `./vendor/bin/shopware-deployment-helper one-time-task:mark <id>`.

## Fastly Integration [​](#fastly-integration)

The Deployment Helper can also deploy Fastly VCL Snippets for you and keep them up to date. After installing the Deployment Helper, you can install the Fastly meta package:

bash

```shiki
composer require shopware/fastly-meta
```

After that, make sure that environment variable `FASTLY_API_KEY` and `FASTLY_SERVICE_ID` are set and the Fastly VCL Snippets will be deployed with the regular deployment process of the Deployment Helper.

The deployment helper has also two commands to manage the Fastly VCL Snippets:

* `./vendor/bin/shopware-deployment-helper fastly:snippet:list` - List all VCL snippets that are currently deployed
* `./vendor/bin/shopware-deployment-helper fastly:snippet:remove <name>` - Remove a VCL snippet by name

## Automatic Store Login [​](#automatic-store-login)

The Deployment Helper can automatically log in to the Shopware Store, so you can install Apps from the Store. For this the environment variables: `SHOPWARE_STORE_ACCOUNT_EMAIL` and `SHOPWARE_STORE_ACCOUNT_PASSWORD` need to be set, and a license domain needs to be configured in the `.shopware-project.yml` file. The license domain can be set also by env variable `SHOPWARE_STORE_LICENSE_DOMAIN`, which will overwrite the value from the `.shopware-project.yml` file.

When you open the extension manager, you will see that you are not logged in. This is normal as the Deployment Helper does log you in only for system tasks like extension installation or updates. For the extension manager, every Administration user needs to log in manually.

## Removal of extensions [​](#removal-of-extensions)

To find the name (for example `SwagPlatformDemoData`) of the extension you want to remove, use the `./bin/console plugin:list` command.

shell

```shiki
./bin/console plugin:list

Shopware Plugin Service
=======================

 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ---------------------- 
  Plugin                        Label                                      Composer name                                  Version   Upgrade version   Author              Installed   Active   Upgradeable   Required by composer  
 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ----------------------
  SwagPlatformDemoData          Shopware 6 Demo data                       swag/demo-data                                 2.0.1                       shopware AG         Yes         No       No            No 
 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ----------------------
```

If you want to remove an extension, you need to do it in two steps:

1.) Set the extension to `remove` in the `.shopware-project.yml` file

yaml

```shiki
deployment:
  extension-management:
    enabled: true

    overrides:
      TheExtensionWeWantToGetRidOf:
        # This plugin will be uninstalled if it is installed
        state: remove
        # should the extension data of an uninstalled extension be kept
        keepUserData: true
```

and deploy the changes. The extension will be uninstalled and is inactive.

2.) Remove the extension from source code

After the deployment, you can remove the extension from the source code, remove the entry from the `.shopware-project.yml` file and deploy the changes again.

## Usage examples [​](#usage-examples)

### Container [​](#container)

In a Docker environment, you have a base image with a running PHP Webserver. From that image you make a new image with your Shopware source code. To prepare the Shopware source code, you can run [shopware-cli project ci](./../../../../products/cli/) to install the dependencies and build the assets. On deployment, you spawn a second container or init a container, which runs the Deployment Helper. The Deployment Helper sets up Shopware when it is not installed, installs the extensions and runs the one-time tasks.

### SFTP / Deployer [​](#sftp-deployer)

When using SFTP or Deployer, you clone the repository to the CI/CD server, run the [shopware-cli project ci](./../../../../products/cli/) command to install the dependencies and build the assets. Then you upload the source code to the server and run the Deployment Helper on the server. The Deployment Helper sets up Shopware when it is not installed, installs the extensions and runs the one-time tasks.

---

## Building without Database

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/deployments/build-w-o-db.html

# Building assets of Administration and Storefront without a Database [​](#building-assets-of-administration-and-storefront-without-a-database)

It is common to prebuild assets in professional deployments to deploy the build artifact assets to the production environment. This task is mostly done by a CI job that doesn't have access to the production database. Shopware needs access to the database to look up the installed extensions/load the configured theme variables. To be able to build the assets without a database, we can use static dumped files. All extensions need to be required by Composer to be able to be loaded by the `ComposerPluginLoader`.

WARNING

This guide requires Shopware 6.4.4.0 or higher.

## Compiling the Administration without database [​](#compiling-the-administration-without-database)

By default, Shopware builds the Administration without extensions if there is no database connection. To include the extensions without a database, you will need to use the `ComposerPluginLoader`. This determines the used plugins by looking up the installed project dependencies. To get this working, the plugin needs to be required in the system using `composer req [package/name]`.

There is a file `bin/ci` which uses the `ComposerPluginLoader` and can be used instead of `bin/console`. Using this, you can dump the plugins for the Administration with the new file without a database using the command `bin/ci bundle:dump`. It is recommended to call `bin/ci` instead of `bin/console` in the `bin/*.js` scripts, which can be achieved by setting the environment variable `CI=1`.

## Compiling the Storefront without database [​](#compiling-the-storefront-without-database)

To compile the Storefront theme, you will need the theme variables from the database. To allow compiling it without a database, it is possible to dump the variables to the private file system of Shopware. This file system interacts with the local folder `files/theme-config` by default, but for it to be compiled, it should be shared such that settings are shared across deployments. This can be achieved, for example, by using a [storage adapter like s3](./../../infrastructure/filesystem.html). The configuration can be dumped using the command `bin/console theme:dump`, or it happens automatically when changing theme settings or assigning a new theme.

This means that you still **need a dumped configuration from a system with a working database setup**. You then need to copy these files to your setup without a database and follow the steps below.

By default, Shopware still tries to load configurations from the database. In the next step, you will need to change the loader to `StaticFileConfigLoader`. To change that, you will need to create a new file, `config/packages/storefront.yaml` with the following content:

yaml

```shiki
storefront:
   theme:
       config_loader_id: Shopware\Storefront\Theme\ConfigLoader\StaticFileConfigLoader
       available_theme_provider: Shopware\Storefront\Theme\ConfigLoader\StaticFileAvailableThemeProvider
       theme_path_builder_id: Shopware\Storefront\Theme\MD5ThemePathBuilder
```

This will force the theme compiler to use the static dumped file instead of looking into the database.

INFO

Warnings about Database errors can still occur but will be caught and should be ignored in this case.

The dumped files should be found in the directory `files/theme-config`

### Example [​](#example)

directory (files/theme-config):

text

```shiki
a729322c1f4e4b4e851137c807b4f363.json
index.json
```

index.json

json

```shiki
{"99ef1e95716d43d7be78e9d9921c7163":"a729322c1f4e4b4e851137c807b4f363"}
```

a729322c1f4e4b4e851137c807b4f363.json

### Partially compiling the Storefront [​](#partially-compiling-the-storefront)

You can also build just the Javascript bundle using `CI=1 SHOPWARE_SKIP_THEME_COMPILE=true PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true bin/build-storefront.sh` (without the need for the above loader) in your CI. After that, run `bin/console theme:dump` on your production system when the database is available. This will happen automatically if theme variables are changed via the admin panel.

---

## Cluster Setup

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/cluster-setup.html

# Cluster Setup [​](#cluster-setup)

The setup of high-scaling systems differs from a normal installation of Shopware. They are completely customized stores with individual templates and extensions.

This guide contains information for everyone who intends to start with such a project.

## Shopware configuration [​](#shopware-configuration)

INFO

This configuration is available starting with Shopware version 6.5.6.0

To configure Shopware for a cluster setup, you have to set the following configuration in your shopware.yaml file:

yaml

```shiki
shopware:
    deployment:
        cluster_setup: true
```

This option prevents shopware from running operations locally (meaning only on one node in a cluster), that potentially can corrupt the state of the cluster by having the state of the nodes diverge from each other, e.g. clearing symfony cache files at runtime.

## Symfony Flex template [​](#symfony-flex-template)

Use the [Symfony Flex template](./../../installation/template.html) and pin the Shopware versions in the `composer.json` file. This prevents unwanted updates when deploying (without a composer.lock).

## Sources [​](#sources)

The following folders are available in the production template:

* **/src**: Here, the project-specific bundles and sources can be stored.
* **/config**: Here are the .yaml config files and other possible configurations (routing, admin configs, etc).
* **/config/bundles.php**: In this file, all Symfony bundles are defined, which should be included in the project.

## Third-party sources [​](#third-party-sources)

Most big-scale projects have a development team assigned. It is responsible for the stability and performance of the system. The integration of external sources via apps or plugins can be useful but should always be viewed with a critical eye. By including those sources, the development team relinquishes control over parts of the system. We recommend including the necessary plugins as Composer packages instead of user-managed plugins.

## Composer plugin loader [​](#composer-plugin-loader)

Shopware loads by default all plugins via the database and allows enabling / disabling plugins at runtime. This needs to be fixed in a multi-app server environment. Therefore, we recommend using the Composer plugin loader. The Composer plugin loader loads the plugin state from Composer, so when a plugin is installed using Composer, we assume that it is enabled. That allows you to deploy plugins to all app servers by deploying with installing them using Composer. The plugins must be installed while deployment using `bin/console plugin:install --activate <name>`, so they are ready to use after the deployment. To use the composer plugin loader, add the environment variable `COMPOSER_PLUGIN_LOADER=1` to your `.env` file.

## Redis [​](#redis)

We recommend setting up at least five Redis servers for the following resources:

1. [Session](./../performance/session.html) + [cart](./../infrastructure/database-cluster.html#cart-in-redis)
2. [cache.object](./../performance/caches.html#example-replace-some-cache-with-redis)
3. [Lock](./../performance/lock-store.html) + [Increment storage](./../performance/increment.html)
4. [Number Ranges](./../performance/number-ranges.html)
5. [Message Queue](./../infrastructure/message-queue.html#transport-redis-example) Instead of setting up a Redis server for `messenger`, you can also work directly with [RabbitMQ](./../infrastructure/message-queue.html#transport-rabbitmq-example)

The PHP Redis extension provides persistent Redis connections. Persistent connections can help in high load scenarios as each request doesn't have to open and close connections. Using non-persistent Redis connections can also hit the system's maximum open sockets. Because of these limitations, the Redis extension is preferred over Predis.

When a Redis cluster is in usage, the `php.ini` setting `redis.clusters.cache_slots=1` should be set to skip the cluster node lookup on each connection.

## Database cluster [​](#database-cluster)

We have compiled some best practices and configurations to allow you to operate Shopware in a clustered database environment. Please refer to the guide below.

[Database Cluster](../infrastructure/database-cluster)

## Filesystem [​](#filesystem)

In a multi-app-server system, manage specific directories over a shared filesystem. This includes assets, theme files, and private as well as public filesystems. The recommendation is to use an S3 compatible bucket.

For more information, refer to the [filesystems](./../infrastructure/filesystem.html) section of this guide.

### Shared directories [​](#shared-directories)

Besides the S3 bucket, it is also necessary to create certain directories for the app servers as shared filesystem.

## Shopware updates + security [​](#shopware-updates-security)

To update your project, we always recommend using a staging environment. However, updates for a project should only be obtained if there are critical problems with the system or if essential features have been provided by Shopware. Updates of such systems require a certain amount of effort, as issues often arise during deployments to production systems.

### Security plugin [​](#security-plugin)

For obtaining security fixes, without version upgrades, we provide a dedicated [Security plugin](https://store.shopware.com/de/swag136939272659/shopware-6-sicherheits-plugin.html). This is compatible with all Shopware versions and corresponding hot fixes are only included in versions that are affected.

### Update of composer dependencies [​](#update-of-composer-dependencies)

To ensure the security of your Shopware installation, it's essential to be vigilant about third-party dependencies that might be affected by security vulnerabilities. In that case, a new Shopware version will be released with updated dependencies. If an update to the latest Shopware version in a timely manner is not possible, it is recommended to update the affected dependency manually. This can be done by using the following command:

bash

```shiki
 composer update <dependency-name>
```

To identify any potential security risk in your current dependencies, it's a good practice to regularly run the [`composer audit`](https://getcomposer.org/doc/03-cli.md#audit) command. This command scans your dependencies and alerts you if there are any known vulnerabilities that need to be addressed.

### Disable auto-update [​](#disable-auto-update)

Shopware's integrated auto-update functionality should be disabled to prevent unwanted updates. Also, this feature is not multi-app server compatible and should be controlled via deployment.

yaml

```shiki
shopware:
    auto_update:
        enabled: false
```

## Message queue [​](#message-queue)

On a productive system, the [message queue](./../infrastructure/message-queue.html) should be processed via CLI processes instead of the [Admin worker](./../infrastructure/message-queue.html#admin-worker). This way, messages are completed regardless of logged-in Administration users and CPU load, as messages can be regulated through the amount of worker processes. Furthermore, you can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/).

It is recommended to run multiple `messenger:consume` workers. To automatically start the processes again after they stopped because of exceeding the given limits you can use a process control system like [systemd](https://www.freedesktop.org/wiki/Software/systemd/) or [supervisor](http://supervisord.org/running.html).

### Own queue [​](#own-queue)

It is also recommended to define your own message queue in addition to the standard message queue. This gives you more control over the load distribution and allows you to prioritize your own processes higher than the data indexing of Shopware.

## Monitoring [​](#monitoring)

Likewise, we recommend setting up an appropriate monitoring dashboard with well-known software such as:

* [Blackfire](https://www.blackfire.io/)
* [Tideways](https://tideways.com/)
* [Datadog](https://www.datadoghq.com/)
* [Elastic](https://www.elastic.co/)

## Local machines [​](#local-machines)

It is important to keep the local development environments of the developers similar to the live environments. A development environment without Redis or Elasticsearch is always too far away from reality and often leads to complications after deployment. Therefore, it is advisable to maintain internal documentation on how to deploy the server structure and how to set up local machines.

## Theme compiling [​](#theme-compiling)

The [theme compilation](./deployments/build-w-o-db.html#compiling-the-storefront-without-database) in Shopware by default depends on the settings in the database. However, since a connection to the database is usually not guaranteed during deployment, we recommend configuring static theme compilation.

## Strong CPU [​](#strong-cpu)

For the server setup, pay special attention to CPU speed. This applies to all servers (app, SQL, Elasticsearch, Redis). Usually, it is more optimal to choose a slightly stronger CPU. This has to be determined more precisely depending on the project and load. Experience has shown that systems with powerful CPUs finish processes faster and can release resources sooner.

## Health Check [​](#health-check)

INFO

This feature is available starting with Shopware version 6.5.5.0

Use the Shopware-provided Health Check API (`/api/_info/health-check`) to monitor the health of your Shopware app server. It responds with HTTP status `200` when the Shopware Application is working and `50x` when it is not. For docker, you can use: `HEALTHCHECK CMD curl --fail http://localhost/api/_info/health-check || exit 1`

## Performance tweaks [​](#performance-tweaks)

When setting up big-scale projects, there are some settings and conditions that should be taken into account with regard to performance.

Read more on [performance tweaks](./../performance/performance-tweaks.html).

---

## Docker Image

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/docker.html

# Docker Image [​](#docker-image)

Shopware provides a Docker image to run Shopware 6 in a containerized environment for production intent. The Docker image is based on the official PHP image and includes the required PHP extensions and configurations to run Shopware 6. But it does not contain Shopware itself. It's intended to be used together with your existing Shopware project, copy the project into the image, build it, and run it.

If you don't have a Shopware project yet, you can create a new one with:

INFO

You can create a Project with a specific Shopware version by specifying the version like: `composer create-project shopware/production:6.6.7.0 <folder>`

bash

```shiki
composer create-project shopware/production <folder>
cd <folder>
composer require shopware/docker
```

The typical Dockerfile in your project would look like this:

INFO

You may want to pin the Docker image to a specific sha256 digest to ensure you always use the same image. See [Best Practices](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions) for more information.

dockerfile

```shiki
#syntax=docker/dockerfile:1.4

ARG PHP_VERSION=8.3
FROM ghcr.io/shopware/docker-base:$PHP_VERSION-frankenphp AS base-image
FROM ghcr.io/shopware/shopware-cli:latest-php-$PHP_VERSION AS shopware-cli

FROM shopware-cli AS build

ADD . /src
WORKDIR /src

RUN --mount=type=secret,id=packages_token,env=SHOPWARE_PACKAGES_TOKEN \
    --mount=type=secret,id=composer_auth,dst=/src/auth.json \
    --mount=type=cache,target=/root/.composer \
    --mount=type=cache,target=/root/.npm \
    /usr/local/bin/entrypoint.sh shopware-cli project ci /src

FROM base-image AS final

COPY --from=build --chown=82 --link /src /var/www/html
```

The Dockerfile uses the `shopware-cli` image to build the project and then copies the built project into the `base-image` image. The `base-image` is the Shopware Docker image.

INFO

Instead of copying the Dockerfile to your project, rather run `composer req shopware/docker` to add the Dockerfile to your project. This keeps the Dockerfile up-to-date with the latest changes using Symfony Flex recipes.

## Available Tags / Versioning [​](#available-tags-versioning)

INFO

We recommend using FrankenPHP over Caddy or Nginx, as it does automatic resource allocation and requires just one process to run PHP, which is better suited for containerized environments.

The Docker image is versioned by the PHP Version and the PHP Patch version. The Docker Image is updated daily and contains the latest security patches.

The following tags are available with our recommended FrankenPHP image:

* `ghcr.io/shopware/docker-base:8.3-frankenphp` - PHP 8.3 with FrankenPHP
* `ghcr.io/shopware/docker-base:8.3.12-frankenphp` - PHP 8.3.12 with FrankenPHP (same as above, but much more explicit)
* `ghcr.io/shopware/docker-base:8.3-frankenphp-otel` - PHP 8.3 with FrankenPHP and OpenTelemetry
* `ghcr.io/shopware/docker-base:8.3.12-frankenphp-otel` - PHP 8.3.12 with FrankenPHP and OpenTelemetry (same as above, but much more explicit)

All images (FrankenPHP, Caddy, Nginx, FPM only) are available at Docker Hub and GitHub Container Registry ([ghcr.io](https://github.com/shopware/docker/pkgs/container/docker-base)) with the same names and tags.

## Default installed PHP Extensions [​](#default-installed-php-extensions)

The Docker image contains the following PHP extensions: `bcmath`, `gd`, `intl`, `mysqli`, `pdo_mysql`, `pcntl`, `sockets`, `bz2`, `gmp`, `soap`, `zip`, `ftp`, `ffi`, `opcache`, `redis`, `apcu`, `amqp` and `zstd`

## Environment Variables [​](#environment-variables)

| Variable | Default Value | Description |
| --- | --- | --- |
| `PHP_SESSION_COOKIE_LIFETIME` | 0 | [See PHP FPM documentation](https://www.php.net/manual/en/session.configuration.php) |
| `PHP_SESSION_GC_MAXLIFETIME` | 1440 | [See PHP FPM documentation](https://www.php.net/manual/en/session.configuration.php) |
| `PHP_SESSION_HANDLER` | files | Set to `redis` for redis session |
| `PHP_SESSION_SAVE_PATH` | (empty) | Set to `tcp://redis:6379` for redis session |
| `PHP_MAX_UPLOAD_SIZE` | 128m | See PHP documentation |
| `PHP_MAX_EXECUTION_TIME` | 300 | See PHP documentation |
| `PHP_MEMORY_LIMIT` | 512m | See PHP documentation |
| `PHP_ERROR_REPORTING` | E\_ALL | See PHP documentation |
| `PHP_DISPLAY_ERRORS` | 0 | See PHP documentation |
| `PHP_OPCACHE_ENABLE_CLI` | 1 | See PHP documentation |
| `PHP_OPCACHE_FILE_OVERRIDE` | 1 | See PHP documentation |
| `PHP_OPCACHE_VALIDATE_TIMESTAMPS` | 1 | See PHP documentation |
| `PHP_OPCACHE_INTERNED_STRINGS_BUFFER` | 20 | See PHP documentation |
| `PHP_OPCACHE_MAX_ACCELERATED_FILES` | 10000 | See PHP documentation |
| `PHP_OPCACHE_MEMORY_CONSUMPTION` | 128 | See PHP documentation |
| `PHP_OPCACHE_FILE_CACHE` |  | See PHP documentation |
| `PHP_OPCACHE_FILE_CACHE_ONLY` | 0 | See PHP documentation |
| `PHP_REALPATH_CACHE_TTL` | 3600 | See PHP documentation |
| `PHP_REALPATH_CACHE_SIZE` | 4096k | See PHP documentation |
| `FPM_PM` | dynamic | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MAX_CHILDREN` | 5 | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_START_SERVERS` | 2 | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MIN_SPARE_SERVERS` | 1 | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MAX_SPARE_SERVERS` | 3 | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |

This table contains only the environment variables that are specific to the Shopware Docker image. You can see all Shopware specific environment variables [here](./../configurations/shopware/environment-variables.html)

Additionally, you can use also the [Deployment Helper environment variables](./deployments/deployment-helper.html#environment-variables) to specify default administration credentials, locale, currency, and sales channel URL.

## Possible Mounts [​](#possible-mounts)

INFO

Our recommendation is to store all files in an external storage provider to not mount any volumes. Refer to [official Shopware docs for setup](https://developer.shopware.com/docs/guides/hosting/infrastructure/filesystem.html).

In a very basic setup when all files are stored locally you need 5 volumes:

| Usage | Path |
| --- | --- |
| invoices/private files | `/var/www/html/files` |
| theme files | `/var/www/html/public/theme` |
| images | `/var/www/html/public/media` |
| image thumbnails | `/var/www/html/public/thumbnail` |
| generated sitemap | `/var/www/html/public/sitemap` |

Shopware logs by default to `var/log`, but when `shopware/docker` Composer package is installed, we change it to stdout. This means you can use `docker logs` to see the logs or use logging driver to forward the logs to a logging service.

## Ideal Setup [​](#ideal-setup)

The ideal setup requires an external storage provider like S3. In that way you don't need any mounts and can scale the instances without any problems.

Additionally, Redis is required for the session storage and the cache, so the Browser sessions are shared between all instances and cache invalidations are happening on all instances.

## Typical Setup [​](#typical-setup)

The docker image starts in the entry point PHP-FPM / Caddy. So you will need to start a extra container to run maintenance tasks like to install Shopware, install plugins, or run the update. This can be done by installing the [Deployment Helper](./deployments/deployment-helper.html) and creating one container and running as entry point `/setup`

Here we have an example of a `compose.yaml`, what the services could look like:

INFO

This is just an example compose file to demonstrate what the services could look like. It's not a ready to use compose file. You need to adjust it to your needs.

yaml

```shiki
x-environment: &shopware
  build:
    context: .
  environment:
    DATABASE_URL: 'mysql://shopware:shopware@database/shopware'
    APP_URL: 'http://localhost:8000'
  volumes:
    - files:/var/www/html/files
    - theme:/var/www/html/public/theme
    - media:/var/www/html/public/media
    - thumbnail:/var/www/html/public/thumbnail
    - sitemap:/var/www/html/public/sitemap

services:
    database:
        image: mariadb:11.4

    init-perm:
        <<: *shopware
        user: "root"
        entrypoint: >
          chown 82:82
          /var/www/html/files
          /var/www/html/public/theme
          /var/www/html/public/media
          /var/www/html/public/thumbnail
          /var/www/html/public/sitemap

    init:
        <<: *shopware
        entrypoint: [ "php", "vendor/bin/shopware-deployment-helper", "run" ]
        depends_on:
            database:
                condition: service_started
            init-perm:
                condition: service_completed_successfully
    web:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        ports:
            - 8000:8000

    worker:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        entrypoint: [ "php", "bin/console", "messenger:consume", "async", "low_priority", "--time-limit=300", "--memory-limit=512M" ]
        deploy:
            replicas: 3

    scheduler:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        entrypoint: [ "php", "bin/console", "scheduled-task:run" ]

volumes:
    files:
    theme:
    media:
    thumbnail:
    sitemap:
```

[Example Repository with fully working setup](https://github.com/shopwareLabs/example-docker-repository/)

## Best Practices [​](#best-practices)

* Pin the docker image using a sha256 digest to ensure you always use the same image
  + Set up Dependabot / Renovate to keep the image up to date
* Use an external storage provider for all files to keep all state out of the container
* Use Redis/Valkey for Cache and Session storage so all instances share the same cache and session

## Adding custom PHP extensions [​](#adding-custom-php-extensions)

The Docker image contains the [docker-php-extension-installer](https://github.com/mlocati/docker-php-extension-installer) which allows you to install PHP extensions with the `install-php-extensions` command.

To install a PHP extension, you need to add the following to your Dockerfile:

dockerfile

```shiki
# ...

USER root
RUN install-php-extensions tideways
USER www-data
```

## Adding custom PHP configuration [​](#adding-custom-php-configuration)

Create a new INI file at `/usr/local/etc/php/conf.d/` with the extension `.ini` and add your configuration.

dockerfile

```shiki
COPY custom.ini /usr/local/etc/php/conf.d/
```

## Adding custom Nginx configuration [​](#adding-custom-nginx-configuration)

Create a new config file at `/etc/nginx/conf.d/` with the `.conf` or `.inc` extension.

The `.conf` will be added to the main `http` block.

The `.inc` will be added to the main `server` block.

## Nginx and PHP\_MAX\_UPLOAD\_SIZE [​](#nginx-and-php-max-upload-size)

The default `client_max_body_size` is equal to the default `PHP_MAX_UPLOAD_SIZE`, which is 128M

If you wish to set the `PHP_MAX_UPLOAD_SIZE` higher than 128M, you need to manually adjust the `client_max_body_size`.

dockerfile

```shiki
USER root
RUN sed -i "s/client_max_body_size 128M/client_max_body_size 256M/" /etc/nginx/nginx.conf
USER www-data
```

## FAQ [​](#faq)

### No transport supports the given Messenger DSN for Redis [​](#no-transport-supports-the-given-messenger-dsn-for-redis)

When you are stuck with the error `No transport supports the given Messenger DSN`, you need to install the required package. When the package is already installed, it's mostly a dependency-resolving issue. Make sure that you have also the PHP Redis Extension locally installed.

---

## Extension Management

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/extension-managment.html

# Extension Management [​](#extension-management)

Normally all extensions installed by the Administration will be stored inside `custom/plugins` or `custom/apps`. When you want to update extensions, you have to re-upload the zip file or download the extension from the store using the Extension manager in the administration.

This way of extension management brings many problems:

* It is hard to keep track of which extensions are installed and in which version
* The extensions can be modified live in the Administration without version control
* Extension updates must be downloaded manually for each extension and installed
* Extension updates in the Administration can't be done together with Shopware updates
* Composer class loader cannot be optimized because we need to dynamically look up into `custom/plugins`

## Installing extensions with Composer [​](#installing-extensions-with-composer)

To solve these problems, it is recommended to install all extensions (plugins and apps) with Composer. This way, you can manage all extensions in one place and update them along with Shopware. To get started with Composer, first, you need to authorize your local project with the Shopware Composer Registry. Below are the steps:

* Login to [account.shopware.com](https://account.shopware.com) and go to your Shop (in Merchant or Account area)
* Click on one extension
* Click the button "Install via Composer"
* Generate a token and save it

Now you can add the Shopware Composer Registry to your project:

bash

```shiki
composer config repositories.shopware-packages '{"type": "composer", "url": "https://packages.shopware.com"}'

composer config bearer.packages.shopware.com <your-token>
```

After that, you should have a newly created file `auth.json`, in your project root. This file contains your token and is used by Composer to authenticate against the Shopware Composer Registry.

INFO

The `auth.json` should not be committed to the repository and should be ignored by default with the `.gitignore` file.

Now you can install extensions with Composer:

bash

```shiki
composer require store.shopware.com/{extension-name}
```

This downloads and extracts the extension package into the `vendor` directory. To install and activate the extension in Shopware, execute the following console command:

bash

```shiki
bin/console plugin:install --activate <extension-name>
```

You can also find the Composer package name when you click "Install via Composer" in the Shopware Account.

## Migrating already installed extensions to Composer [​](#migrating-already-installed-extensions-to-composer)

If you already have extensions installed in your project, you can migrate them to Composer. First, you should install the extension with Composer:

bash

```shiki
composer require store.shopware.com/{extension-name}
```

And then delete the source code from `custom/plugins/{extension-name}` or `custom/apps/{extension-name}`.

After that, you must run the below command for Shopware to detect the installed extensions per Composer.

bash

```shiki
bin/console plugin:refresh
```

## Enabling Composer class map authoritative [​](#enabling-composer-class-map-authoritative)

When all extensions are installed with Composer, you can enable the Composer class map authoritative. This will improve the performance of the class loader and is recommended for production environments. [The class map authoritative, disables the live class lookup when it cannot find the class in a dumped class map.](https://getcomposer.org/doc/articles/autoloader-optimization.md#optimization-level-2-a-authoritative-class-maps)

diff

```shiki
{
    "require": {
        "shopware/core": "...",
        // ...
    },
    "config": {
        "optimize-autoloader": true,
+       "classmap-authoritative": true
    }
}
```

And run the below command to re-generate the class loader.

bash

```shiki
composer dump-autoload
```

## Configuring Extension Manager to read-only in Admin [​](#configuring-extension-manager-to-read-only-in-admin)

Since Shopware 6.6.4.0, it has been possible to disable the installation of extensions in the Administration. This is useful when you have a cluster environment or want to use proper deployments to roll out code changes.

To disable the installation of extensions in the Administration, you can set the following configuration in your `config/packages/z-shopware.yaml` file:

yaml

```shiki
shopware:
    deployment:
        runtime_extension_management: false
```

Next clear the cache once. After doing this, the Extension Manager in the Administration will become read-only, allowing access only to the extension configuration. Additionally, the First Run Wizard will no longer download extensions such as PayPal or the Shopware Store.

---

## Performing Shopware Updates

**Source:** https://developer.shopware.com/docs/guides/hosting/installation-updates/performing-updates.html

# Performing Shopware Updates [​](#performing-shopware-updates)

## When to update [​](#when-to-update)

Shopware releases updates every month. It's not necessary to update every month, but you should always install the latest security patches through the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) or update Shopware itself to the latest version. To check if your Shopware version still gets security updates, you can check the [Shopware Release Cycle](https://developer.shopware.com/release-notes/). But generally speaking, the maintenance effort is the same when you wait a long period or update more regularly. So our recommendation would be to update from every major version to the next major version, and stay on a minor version for a longer period of time, if you don't need any new features or encounter issues with the used version.

## Preparations [​](#preparations)

Before any update, check if the installed extensions are compatible with the new version. The easiest way to check this is to open the Update Manager in the Administration. It lists all installed extensions and their compatibility with the new version. If an extension is not compatible, you should check with the extension developer if an update is available.

INFO

If you can't see the info in the admin, please check if [auto\_update](./../installation-updates/cluster-setup.html#disable-auto-update) is set to false.

The next step is to check when the update should be performed. You should always perform updates in a maintenance window to avoid any issues with customers. If you are using a staging environment, you can perform the update there first and then apply it to the production environment.

Before doing the actual update, you should create a backup of your database and files. This is important to ensure that you can restore your Shopware installation in case something goes wrong during the update process.

INFO

If blue-green deployment is enabled, you can rollback to the previous version without restoring the database backup. This is only recommended when you **only updated** Shopware and not any extensions together with it.

Before you start the update process, you should also make sure that you have set the Sales Channels into maintenance mode. This can be done using the Administration or with `bin/console sales-channel:maintenance:enable --all` in the terminal.

### Use Composer to manage all extensions [​](#use-composer-to-manage-all-extensions)

Managing all extensions through Composer is the best way to ensure that they are compatible with the new version. It simplifies the update process as Composer automatically resolves the correct versions of the extensions.

### Use Twig Block Versioning [​](#use-twig-block-versioning)

Twig Block Versioning is a [PHPStorm Plugin](https://plugins.jetbrains.com/plugin/17632-shopware-6-toolbox) only feature. Twig Block Versioning is a feature that allows versioning of the overwritten blocks in your theme. This helps you to show which blocks after a Shopware Update maybe have to be changed. It's recommended to enable "Shopware versioning block comment is missing" in the inspection settings. This will show you a warning if a block is missing the versioning comment. For more information, check the [Twig Block Versioning blog post](https://www.shopware.com/en/news/twig-block-versioning-in-shopware-phpstorm-plugin/).

### Use existing tools to automatically upgrade your extensions [​](#use-existing-tools-to-automatically-upgrade-your-extensions)

There are tools like [Rector](https://github.com/FriendsOfShopware/shopware-rector) for PHP and [Codemods](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/code-mods.js) for Administration JavaScript which can help you to automatically upgrade your extensions. Both tools do the most repeating tasks for you, but you still have to check the results and adapt your code if necessary. It's recommended to use these tools, as they save you a lot of time. Make sure that your code-base is versioned with Git, so you can easily rollback the changes if necessary.

## Update types [​](#update-types)

There are two Shopware update types:

* **Minor/Patch updates**: These are updates that only contain new features, bug fixes and security patches. They are released every month for the active supported versions.
* **Major updates**: These updates are intended to clean up the codebase and introduce breaking changes. They are released once a year.

### Minor/Patch updates [​](#minor-patch-updates)

Minor and patch updates are non-breaking updates. They don't require special attention if your extensions are not using internal/experimental APIs. You can find the Backwards Compatibility Promise [here](./../../../resources/guidelines/code/backward-compatibility.html). Of course, there can be unexpected issues, so we recommend to test the update in a staging environment before applying it to your production environment and [reporting](https://github.com/shopware/shopware/issues) any issues you encounter.

### Major updates [​](#major-updates)

Major updates are breaking updates. They require special attention, as extensions, themes or system configurations might not be compatible with the new version.

First, you should check that all extensions obtained from Shopware Store are compatible with the next version. You can find the compatibility information in the Update Manager in the Administration. Generally speaking, it's recommended to update all extensions before updating Shopware itself to their latest versions, to ensure a smooth transition. After updating Shopware, you should update all extensions again to ensure that you are using the latest versions to the new Shopware version.

For the Hosting environment, it makes sense to update the PHP version to the minimum required version for the new Shopware version before updating Shopware itself. Shopware versions always support an overlapping PHP version, so you can update the PHP version before updating Shopware itself. You can find the minimum required PHP version in the [System Requirements](./../../installation/requirements.html).

For customizations, you should check the [UPGRADE.md](https://github.com/search?q=repo%3Ashopware%2Fshopware+UPGRADE-6+language%3AMarkdown+NOT+path%3A%2F%5Eadr%5C%2F%2F+NOT+path%3A%2F%5Echangelog%5C%2F%2F&type=code&l=Markdown), it contains all breaking changes and migration instructions. Most of the time, it's easier to update to the latest version in a local environment and take a look at what is not working anymore.

## Final Steps [​](#final-steps)

Before you remove the maintenance mode, it is recommended to check the following:

* **Check the Administration**: Make sure the administration is working correctly.
* **Check the Storefront / Sales Channels**: Make sure your main processes are working correctly (e.g., adding products to the cart, checkout, etc.).
* **Check the Extensions**: Make sure that all extensions are working correctly.
* **Check the Performance**: Make sure that there is no major performance degradation.
* **Check the Logs**: Check your error logs for any issues.

After you have checked everything, you can disable the maintenance mode with `bin/console sales-channel:maintenance:disable --all`.

---

