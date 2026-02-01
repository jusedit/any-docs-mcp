# Products Paas

*Scraped from Shopware Developer Documentation*

---

## PaaS

**Source:** https://developer.shopware.com/docs/products/paas/

# Introduction to PaaS [​](#introduction-to-paas)

While both [Shopware PaaS Native](./shopware/) and [Shopware PaaS](./shopware-paas/) offer cloud-based environments for development, they differ in specialization and flexibility:

* **Shopware PaaS**: A generic PaaS provider, [Shopware PaaS](./shopware-paas/) supports various applications and multiple cloud providers, giving developers the flexibility to define their infrastructure as code. However, this requires customers to manage more aspects of infrastructure and setup.
* **Shopware PaaS Native**: Optimized solely for Shopware, this platform provides a tightly integrated and controlled environment on AWS. This focus ensures higher stability, with Shopware managing all underlying configurations, enabling developers to concentrate on application development.

By using [Shopware PaaS Native](./shopware/), teams benefit from a unified, robust platform that simplifies the development lifecycle, enhances performance, and enables faster innovation.

---

## Shopware PaaS Native

**Source:** https://developer.shopware.com/docs/products/paas/shopware/

# Introduction to Shopware PaaS Native [​](#introduction-to-shopware-paas-native)

**Shopware PaaS Native (Platform-as-a-Service)** is a fully managed, cloud-native environment dedicated to hosting and developing Shopware applications. Built with an opinionated infrastructure, Shopware PaaS Native enables developers to focus on custom development without the overhead of managing scalability or infrastructure. This platform is optimized for efficiency, scalability, and rapid iteration, helping developers streamline Shopware project workflows.

## Key technical features [​](#key-technical-features)

* **Kubernetes and AWS-Powered Infrastructure:** Shopware PaaS Native is built on a Kubernetes-based architecture running on AWS. This setup provides managed resources—such as servers, storage, networking, and databases—optimized to scale automatically based on application demands, ensuring high availability and stability without manual intervention.
* **Developer-Centric Tools and Workflows:** The platform includes preconfigured tools and standardized workflows specifically designed for Shopware development. These tools enable seamless integration with CLI, APIs, and other familiar development resources, streamlining deployment, testing, and monitoring processes.
* **Efficient Build and Deployment Pipelines:** Developers benefit from a ready-to-use environment optimized for continuous integration and deployment (CI/CD), reducing the need to manage complex infrastructure configurations. This setup accelerates development lifecycles and minimizes error rates.

## Shopware PaaS Native Architecture [​](#shopware-paas-native-architecture)

The architecture of Shopware PaaS Native includes two primary layers:

1. **Infrastructure Layer:** A robust, cloud-based foundation powered by Kubernetes and AWS. Resources are configured to scale based on project needs, ensuring high availability and stability.
2. **Platform Layer:** A preconfigured environment with integrated best practices and tools, streamlining the development and deployment of Shopware applications. This layer accelerates workflows and reduces operational complexity by providing a consistent and managed setup.

## Comparison with Self-Hosted and SaaS Models [​](#comparison-with-self-hosted-and-saas-models)

| **Model** | **Self-Hosted** | **Shopware PaaS Native** | **SaaS** |
| --- | --- | --- | --- |
| **Infrastructure Responsibility** | Fully managed by the customer | Managed by Shopware (customer manages application) | Fully managed by Shopware |
| **Control Over Customization** | Complete control | High control with opinionated best practices | Limited; customization possible only through apps |
| **Setup and Maintenance Effort** | High | Moderate, with most infrastructure tasks automated | Low |
| **Ideal Use Case** | Full control, advanced custom setups | Balance of control and managed scalability | Ease of use with minimal setup |

---

## Get Started

**Source:** https://developer.shopware.com/docs/products/paas/shopware/get-started/

# Get Started with Shopware PaaS Native [​](#get-started-with-shopware-paas-native)

This section will introduce how to get started with Shopware PaaS Native, including setting up the CLI, preparing your code base, and providing a step-by-step guide to creating your first application.

---

## Prepare Shopware codebase

**Source:** https://developer.shopware.com/docs/products/paas/shopware/get-started/prepare-codebase.html

# Prepare Shopware codebase [​](#prepare-shopware-codebase)

## Prerequisite [​](#prerequisite)

**macOS** and **Linux** are the recommended environments for local development. On **Windows**, it's advisable to use [Docker](https://www.youtube.com/watch?v=5XYFRDlT9WI) or **WSL2** (Windows Subsystem for Linux) for a consistent development experience.

To develop and customize your Shopware project effectively, certain operations must be performed in a local environment. This is especially important for tasks that directly interact with the file system, such as Installing or upgrading plugins, adjusting system-level configuration (e.g., language, environment) or applying custom code changes.

Plugin management via the Shopware Administration interface is **not supported**. This is because the platform operates in a **high-availability (HA), clustered setup**, where all application instances must remain **stateless and identical**.

To ensure consistency and reproducibility across deployments, plugins must be installed or updated **via Composer** as part of the project’s codebase. Follow the official guidance on [managing extensions with Composer](https://developer.shopware.com/docs/guides/hosting/installation-updates/extension-managment.html#installing-extensions-with-composer).

Additionally, before installation, verify that each plugin supports **S3-based storage**, as not all extensions are compatible with external file systems.

## How to uninstall plugins [​](#how-to-uninstall-plugins)

To uninstall plugins in the PaaS environment, use the [Deployment Helper](./../../../../guides/hosting/installation-updates/deployments/deployment-helper.html#removal-of-extensions) which provides a streamlined process for extension management.

The uninstallation process involves two steps:

1. **Set the extension to remove**: Configure the extension state as `remove` in your `.shopware-project.yml` file and deploy the changes to uninstall the extension.
2. **Remove from source code**: After the deployment, remove the extension from your source code and deploy again.

For detailed instructions and configuration examples, refer to the [Removal of extensions](./../../../../guides/hosting/installation-updates/deployments/deployment-helper.html#removal-of-extensions) section in the Deployment Helper documentation.

## Generating the required files [​](#generating-the-required-files)

Whether you're starting from scratch or working with an existing Shopware project, the following steps will ensure your setup is ready for deployment on Shopware PaaS Native.

### For New Projects [​](#for-new-projects)

To create a new Shopware project from the official production template, run:

sh

```shiki
composer create-project shopware/production <folder-name>
```

Then navigate into the project directory and proceed with the next steps.

### For Existing Projects [​](#for-existing-projects)

If you're working with an already created Shopware project, simply navigate into the project directory:

sh

```shiki
cd <your-project-folder>
```

Ensure the required Kubernetes metadata package is installed to enable compatibility with the [Shopware Operator](https://github.com/shopware/shopware-operator):

sh

```shiki
composer require shopware/k8s-meta --ignore-platform-reqs
```

INFO

The `--ignore-platform-reqs` flag ensures that all necessary recipes are installed, even if your local PHP version differs from the required platform version.

This package installs essential configuration files, including those required for deploying your shop via the Shopware Operator. After installation, verify that the file `config/packages/operator.yaml` has been created.

### Create the `application.yaml` File [​](#create-the-application-yaml-file)

At the root of your project, create a file named `application.yaml`. This file defines key deployment parameters, such as the PHP version and any environment-specific configuration needed for your shop.

#### Basic Example [​](#basic-example)

yaml

```shiki
app:
  php:
    version: "8.3"
  environment_variables: []
services:
  mysql:
    version: "8.0"
```

#### Advanced Example (with Custom Environment Variables) [​](#advanced-example-with-custom-environment-variables)

yaml

```shiki
app:
  php:
    version: "8.3"
  environment_variables:
    - name: INSTALL_LOCALE
      value: fr-FR
      scope: RUN # Supports RUN or BUILD
services:
  mysql:
    version: "8.0"
```

## Hooks Configuration [​](#hooks-configuration)

Shopware PaaS Native uses the deployment helper to execute custom hooks for your application. To see how these hooks are configured, refer to the [Deployment Helper documentation](./../../../../guides/hosting/installation-updates/deployments/deployment-helper.html#configuration).

---

## CLI

**Source:** https://developer.shopware.com/docs/products/paas/shopware/get-started/cli.html

The Shopware PaaS Native CLI makes it easy to manage your shops and resources in the cloud.

## Prerequisites [​](#prerequisites)

Before you start, you'll need a Shopware account. Shopware uses AWS Cognito for identity management. Currently, you must be invited to join our platform before you can access any resources.

Once your organization is onboarded to the Shopware Business Platform (SBP) and users are added to Shopware PaaS Native, the first user gets the admin role. This admin can then assign roles to other users in your organization.

For more on managing users, see our [Organization Guide](./../fundamentals/organization.html).

## Installation [​](#installation)

To install the CLI, run:

sh

```shiki
curl -L https://install.sw-paas-cli.shopware.systems | sh
```

The installation script will download the latest version (or specified version) from GitHub releases, install the binary to ~/.sw-paas/bin/sw-paas and add the installation directory to your PATH (if not already present). You can set `SW_PAAS_DIR` environment variable to customize the installation directory, which defaults to `~/.sw-paas`

To install a specific version:

sh

```shiki
curl -L https://install.sw-paas-cli.shopware.systems | sh -s 0.0.30
```

INFO

Soon, you'll also be able to install the CLI using popular package managers.

## Authentication [​](#authentication)

After installing, you'll need to log in to use the CLI.

Run the following command to open a browser window and log in to your Shopware PaaS Native account. Your authentication token will be saved automatically.

sh

```shiki
sw-paas auth
```

For more details on managing your account and creating machine tokens for CI/CD, see the [account command](./../fundamentals/account.html) guide.

## Authorization [​](#authorization)

To access resources, you need the right roles in your organization. Only users with the **Account Admin** role can assign roles to others.

To check your current role:

sh

```shiki
sw-paas account whoami
```

If you are an Account Admin and want to add more users, ask the new user to get their user ID:

sh

```shiki
sw-paas account whoami --output json
```

Add the user to your organization and assign a role:

sh

```shiki
sw-paas account user add --sub "<user-id of the new user>"
```

## Available commands [​](#available-commands)

To view all available commands with supported flags:

sh

```shiki
sw-paas
```

## Need help or found a bug? [​](#need-help-or-found-a-bug)

If you find a bug or have feedback, please let us know in our [issue tracker](https://github.com/shopware/sw-paas/issues).

---

## Quickstart

**Source:** https://developer.shopware.com/docs/products/paas/shopware/get-started/quickstart.html

# Quickstart [​](#quickstart)

Get started with Shopware PaaS Native in just a few minutes. This guide will walk you through the essential steps to deploy your first Shopware application.

## Prerequisites [​](#prerequisites)

Before you begin, ensure you have:

* A Git repository with your Shopware application prepared for PaaS. You can follow [this guide](./) for preparation.
* Access to the terminal / command line
* Git installed on your local machine. You can follow [this guide](https://github.com/git-guides/install-git).

## Step 1: Install the PaaS CLI [​](#step-1-install-the-paas-cli)

First, install the Shopware PaaS Native CLI tool:

sh

```shiki
curl -L https://install.sw-paas-cli.shopware.systems | sh
```

Verify the installation:

sh

```shiki
sw-paas version
```

## Step 2: Connect Your Git Repository [​](#step-2-connect-your-git-repository)

To connect your private git repository with our backend, you need to add an SSH key to your repository. This key is used to clone your repository and deploy your code to the cluster.

### 2.1 Generate and Store SSH Key [​](#_2-1-generate-and-store-ssh-key)

Run the following command to create an SSH key and store it securely in your organization's vault:

sh

```shiki
sw-paas vault create --type ssh
```

This command will generate a new SSH key pair and store the private key securely.

INFO

Organization vs Project Level

* **Organization level**: All projects can use the key
* **Project level**: Only a specific project can use the key (add `--project` flag)

Project-level keys override organization-level keys.

### 2.2 Add Public Key to Repository [​](#_2-2-add-public-key-to-repository)

After running the command, the CLI will display the generated public key. Copy this public key and add it to your repository settings:

* **GitHub**: Go to `Settings` → `Deploy keys` → `Add deploy key`
* **GitLab**: Go to `Settings` → `Repository` → `Deploy Keys`
* **Bitbucket**: Go to `Repository settings` → `Access keys`

Ensure the key has **read access** to the repository.

## Step 3: Create Your First Project [​](#step-3-create-your-first-project)

Initialize a new PaaS project:

sh

```shiki
sw-paas project create --name "my-shopware-app" --repository "git@github.com:username/repo.git"
```

## Step 4: Create and deploy an Application Instance of the project [​](#step-4-create-and-deploy-an-application-instance-of-the-project)

Create your application:

sh

```shiki
sw-paas application create
```

Then, deploy your application:

sh

```shiki
sw-paas application deploy create
```

Monitor the deployment progress:

sh

```shiki
sw-paas watch
```

---

## Fundamentals

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/

# Fundamentals [​](#fundamentals)

This section will introduce the fundamental pieces of Shopware PaaS Native.

---

## Organizations

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/organization.html

# Organizations [​](#organizations)

An organization serves as the top-level container representing a company or an entity in Shopware PaaS Native. It acts as the primary organizational unit that encompasses all resources, projects, and users associated with a particular business entity. By default, the initial admin user is added to an Organization and can further add more users.

To create additional organizations via CLI, run;

sh

```shiki
sw-paas organization create
```

## Organization Members [​](#organization-members)

Organization members are users who have been granted access to an organization and its resources.

### Roles [​](#roles)

Organization members can be assigned different roles that determine their level of access and permissions:

* `read-only`: Access to projects and applications. Only actions allowed are `get` and `list`.
* `developer`: Access to projects and applications. All actions are allowed.
* `project-admin`: Access to projects and applications. All actions are allowed.
* `account-admin`: Access to account management. Actions for managing users are allowed.

### User Management [​](#user-management)

If you already have the `project-admin` role and wish to add additional users to your organization, they can share their **user ID (sub-id)** with you. You can instruct them to retrieve it using the following command:

sh

```shiki
sw-paas account whoami --output json
```

Or, if they have `jq` installed for easier parsing:

sh

```shiki
sw-paas account whoami --output json | jq ".sub"
```

Once you receive their `sub` (subject ID), you can proceed to add them to your organization with the appropriate role.

sh

```shiki
sw-paas organization user add
```

To remove a user from the organization:

sh

```shiki
sw-paas organization user remove
```

---

## Projects

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/project.html

# Projects [​](#projects)

Projects represent a codebase in a GitHub, Bitbucket, or GitLab repository that is deployed to Shopware PaaS Native. Projects can contain many applications.

## Creating a New Project [​](#creating-a-new-project)

Initialize a new project in your organization by specifying its name, repository, and type.

sh

```shiki
sw-paas project create
```

Ensure that Shopware PaaS Native has access to the repository by following [this guide](./../guides/setting-up-repository-access.html).

## List All Projects [​](#list-all-projects)

Displays all projects associated with your user or organization, along with key metadata such as project name, type, and repository.

**Usage:**

sh

```shiki
sw-paas project list
```

---

## Applications

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/applications.html

# Applications [​](#applications)

Shopware PaaS Native supports multiple applications within a project, such as environments for production, staging, or temporary feature testing.

Each application has its own compute resources, infrastructure, and deployment configuration, so you can tailor each environment to its specific needs.

For instance, you might allocate smaller, hibernating compute instances for staging while reserving larger, always-on resources for production.

## Creating an Application [​](#creating-an-application)

Create a new application to a project:

sh

```shiki
sw-paas application create
```

## Build your application [​](#build-your-application)

To trigger a new build for the application via CLI, use the following command:

sh

```shiki
sw-paas application build start
```

This command initiates the build process, packaging your application and preparing it for deployment. While the build is running, you can monitor its progress and view real-time output by following the logs:

sh

```shiki
sw-paas application build logs
```

## Update your application [​](#update-your-application)

To update your application, you need to run the following command and provide the commit SHA:

sh

```shiki
sw-paas application update
```

This command initiates the build process, waits until it's done, and runs the deployment for you.

## Deploy a specific build of your application [​](#deploy-a-specific-build-of-your-application)

To create a deployment with a specific build, use the following command:

sh

```shiki
sw-paas application deploy create
```

It will let you choose which build you want to deploy. This is very handy, since you can choose any successful build to deploy: the latest one to bring your change live, or a previous one to fix an issue that arose.

## Deployments management [​](#deployments-management)

To list all past deployments:

sh

```shiki
sw-paas application deploy list
```

To get details about a given deployment:

sh

```shiki
sw-paas application deploy get
```

## Plugin Management [​](#plugin-management)

Plugin management is done [via Composer](./../../../../guides/hosting/installation-updates/extension-managment.html#installing-extensions-with-composer) because the platform runs in a high-availability and clustered environment.

In such setups, local changes aren't feasible, as all instances must remain identical and stateless. This ensures consistency across all deployments.

### Using Privately Hosted Packages [​](#using-privately-hosted-packages)

To pull privately hosted Composer packages, you need to provide authentication credentials. Create a `COMPOSER_AUTH` secret using the CLI:

sh

```shiki
sw-paas vault create
```

Follow the prompts to enter your Composer authentication JSON as a `buildenv`. This secret will be used during builds to access private repositories.

## Executing Commands [​](#executing-commands)

Shopware PaaS Native provides two primary ways to run commands in your application environments via CLI: `exec` and `command`.

### `exec` Command [​](#exec-command)

The `exec` command allows you to execute commands in a remote terminal session for your applications. This is useful for running commands directly on your application's environment, such as debugging, maintenance, or running one-off commands interactively.

sh

```shiki
sw-paas exec --new
```

This opens an interactive shell session inside your application's container.

#### Note [​](#note)

Please check the [known issues](./../known-issues.html) regarding network considerations when running this command.

### `command` Command [​](#command-command)

The `command` command lets you create and manage commands that are executed in dedicated containers. This is particularly useful for CI/CD environments, asynchronous command execution, automated processes, or situations where you don't need to wait for command completion.

Unlike `exec`, which provides an interactive shell, `command` runs your specified command in a new, isolated container and does not require you to wait for its completion.

The default execution directory is `/var/www/html` and the container has a time-to-live (TTL) of 1 hour, so your command must complete within that timeframe.

sh

```shiki
sw-paas command create
```

For a complete list of available commands, refer to the [Shopware console commands documentation](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/shopware-cli).

## Domain Management [​](#domain-management)

### Shopware Domain [​](#shopware-domain)

When you deploy an application for the first time, it automatically receives a complimentary `shopware.shop` domain. This allows you to access and test your application right away, even before setting up a custom domain.

The assigned domain is generated based on your application's name and unique identifier.

### Custom Domain [​](#custom-domain)

You can configure custom domains for your applications using the `sw-paas` CLI domain command. This allows you to attach multiple domains to a single application and route traffic through the Fastly CDN for optimal performance.

#### Creating Custom Domains [​](#creating-custom-domains)

To create a custom domain for your application:

sh

```shiki
sw-paas domain create
```

Follow the prompts to specify your domain name and application. You can attach multiple domains to a single application.

#### DNS Configuration [​](#dns-configuration)

After creating a custom domain, you must configure your DNS settings to point to the PaaS CDN endpoint:

**Configure your custom domain's DNS to point to:**

dns

```shiki
cdn.shopware.shop
```

This configuration ensures that all traffic to your custom domain is routed through the Fastly CDN for optimal performance and caching.

#### Application Deployment [​](#application-deployment)

Following domain creation, you must redeploy your application. You can do it by using:

sh

```shiki
sw-paas application deploy create
```

#### Shopware Configuration [​](#shopware-configuration)

Subsequently, you can configure the domain within Shopware and associate it with a storefront. Status update functionality is currently under development and should be considered a beta feature.

For more detailed information about CDN configuration and best practices, refer to the [CDN documentation](./../cdn/).

---

## Environment variables

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/environment-variables.html

# Setting environment variables [​](#setting-environment-variables)

This page explains how to configure environment variables in Shopware PaaS Native.

Please only use this to configure non-sensitive environment variables. For sensitive variables, please use [secrets](./secrets.html). There is a detailed guide [here](./../guides/secrets-vault-guide.html).

## Configure environment variables [​](#configure-environment-variables)

Environment variables are defined in the `application.yaml` file, in the following array `app.environment_variables`.

Environment variables need to be scoped, they can be configured either for `RUN` or `BUILD`

| Scope | Description |
| --- | --- |
| `RUN` | The value is passed to Shopware application (runtime) |
| `BUILD` | Build-time environment variables |

Once the `application.yaml` is updated as usual, run the following:

sh

```shiki
sw-paas application update
```

## Configure an environment variable for runtime [​](#configure-an-environment-variable-for-runtime)

Update the `application.yaml` file like this:

yaml

```shiki
app:
  environment_variables:
    - name: MY_RUNTIME_VARIABLE
      value: my-value
      scope: RUN
```

## Configure an environment variable for build-time [​](#configure-an-environment-variable-for-build-time)

Update the `application.yaml` file like this:

yaml

```shiki
app:
  environment_variables:
    - name: MY_BUILDTIME_VARIABLE
      value: my-value
      scope: BUILD
```

## Complete example [​](#complete-example)

Here is a full example of environment variables. They can be used for both build-time and runtime, and you can have multiple variables with the same name but different scopes.

yaml

```shiki
app:
  # ... Other application settings
  environment_variables:
    - name: MY_BUILDTIME_VARIABLE
      value: bar
      scope: BUILD
    - name: MY_RUNTIME_VARIABLE
      value: foo
      scope: RUN
    - name: MY_VARIABLE_WITH_THE_SAME_NAME
      value: my-value
      scope: RUN
    - name: MY_VARIABLE_WITH_THE_SAME_NAME
      value: my-value
      scope: BUILD
```

---

## Secrets

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/secrets.html

# Secrets [​](#secrets)

Shopware PaaS Native allows you to securely store and retrieve sensitive information like passwords or API tokens.

Secrets stored in Vault are reusable, which means that you can reuse a secret value in different applications. Secrets are global to the organization, so all applications can access the same values.

## Creating a New Secret [​](#creating-a-new-secret)

A secret is composed of a type, a key, and a value. Once created, it is assigned a unique `secret-id`, which is required for retrieving or deleting the secret.

The supported types are `env`, `buildenv`, and `ssh`. `env` is available at runtime in the application, `buildenv` is accessible during build processes, and `ssh` keys are for secure connections.

To create a secret, use the following command:

sh

```shiki
sw-paas vault create
```

## Listing all Vault secrets [​](#listing-all-vault-secrets)

sh

```shiki
sw-paas vault list
```

## Retrieving a Secret [​](#retrieving-a-secret)

To retrieve an existing secret from the Vault, you **must specify the secret ID** using the `--secret-id` flag:

sh

```shiki
sw-paas vault get --secret-id SECRET-ID
```

---

## Deleting a Secret [​](#deleting-a-secret)

To delete a secret from the Vault, also use the `--secret-id` flag:

sh

```shiki
sw-paas vault delete --secret-id SECRET-ID
```

WARNING

Deleting a secret is permanent. Ensure the secret is no longer in use before removing it.

---

## Account

**Source:** https://developer.shopware.com/docs/products/paas/shopware/fundamentals/account.html

# Account [​](#account)

An account represents your access to resources within the Shopware PaaS Native backend environment which includes context management, token handling, and role identification.

## Roles [​](#roles)

To find what resources you have access to via the CLI:

sh

```shiki
sw-paas account whoami
```

## Context [​](#context)

To avoid repetitive prompts for `organization-id` and `project-id`, you can set a context and the CLI will automatically use these values without asking.

Setting your context streamlines your workflow by eliminating the need to specify these parameters with every command.

sh

```shiki
sw-paas account context set
```

The context is saved as `context-production.yaml` and stored alongside the main configuration file in the following locations:

|  | Unix | macOS | Windows |
| --- | --- | --- | --- |
| XDG\_CONFIG\_HOME | ~/.config/sw-paas | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |
| XDG\_STATE\_HOME | ~/.local/state/sw-paas | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |

## Authentication Tokens [​](#authentication-tokens)

The `token` command manages personal access tokens, enabling secure authentication for both API and CLI operations without exposing your main account credentials. Personal access tokens are especially useful for automating workflows, such as authenticating in CI/CD pipelines or integrating with external systems.

### Creating a Token [​](#creating-a-token)

Generate a new access token:

sh

```shiki
sw-paas account token create --name "ci-token"
```

### Using a Token [​](#using-a-token)

To use a token you have multiple options:

sh

```shiki
token=<your-token-here>
sw-paas --token $token account whoami
sw-paas --token "<your-token-here>" account whoami

# Set it for the current terminal session
export SW_PAAS_TOKEN=<your-token-here>
sw-paas account whoami
```

### Revoking a Token [​](#revoking-a-token)

Remove a specific token by ID:

sh

```shiki
sw-paas account token revoke --token-id abcd-1234
```

---

## Resources

**Source:** https://developer.shopware.com/docs/products/paas/shopware/resources/

# Resources [​](#resources)

This section guides you through the resources that support your application, such as the database and object storage.

---

## Databases

**Source:** https://developer.shopware.com/docs/products/paas/shopware/resources/databases.html

# Databases [​](#databases)

## Introduction [​](#introduction)

Shopware PaaS Native provides a managed MySQL cluster for each application created where we handle: automatic backups and recovery, high availability, performance monitoring and metrics, resource scaling (CPU, RAM, storage), automatic encryption of data at rest and in transit.

## Connecting to Database Cluster [​](#connecting-to-database-cluster)

To connect to your database via CLI:

sh

```shiki
sw-paas open service --service database --port 3306
```

### Note [​](#note)

Please check the [known issues](./../known-issues.html) regarding network considerations when running this command.

---

## Object Storage

**Source:** https://developer.shopware.com/docs/products/paas/shopware/resources/object-storage.html

# Object Storage [​](#object-storage)

## Introduction [​](#introduction)

Applications in Shopware PaaS Native are created by default with two S3-compatible object storage buckets. A public bucket and a private bucket.

You can learn more about [shopware filesystem here](./../../../../guides/hosting/infrastructure/filesystem.html).

---

## Monitoring

**Source:** https://developer.shopware.com/docs/products/paas/shopware/monitoring/

# Monitoring [​](#monitoring)

Shopware PaaS Native provides comprehensive monitoring capabilities to help you track the health and performance of your applications. With built-in monitoring tools, you can observe your application's behavior, troubleshoot issues, and ensure optimal performance in your cloud environment. This section introduces 3 key components used in monitoring: Logs, Traces and Events.

---

## Logs

**Source:** https://developer.shopware.com/docs/products/paas/shopware/monitoring/logs.html

# Logs [​](#logs)

## Application Logs [​](#application-logs)

Shopware PaaS Native allows you to view your application’s logs for a given environment via Grafana.

To access Grafana, run the following command:

bash

```shiki
sw-paas open grafana
```

This command will provide you with the Grafana URL, username, and password.

Once logged in to Grafana:

1. Open the **Explore** tab.
2. Select **Loki** as the data source.
3. Filter logs by setting the `component` label to the service you want to inspect.
4. Run the query to view the logs for that component.

![PaaS log search in Grafana](/assets/paas-monitoring-log-search.qfXjO1mV.png "PaaS monitoring log search")

## Tips [​](#tips)

In the Explore view, you can refine results using the search box:

* Line contains — matches the exact string.
* Line contains case-insensitive — recommended, as it matches the string regardless of the letter case.

A predefined dashboard named `Logs Dashboard` is available. It displays the log ingestion volume and includes a built-in case-insensitive search box.

![PaaS log filter in Grafana](/assets/paas-monitoring-log-filter.i6mHtsVz.png "PaaS monitoring log filter")

## Log retention [​](#log-retention)

Shopware PaaS Native keeps your latest logs available for review. Logs older than 14 days are automatically removed.

---

## Traces

**Source:** https://developer.shopware.com/docs/products/paas/shopware/monitoring/traces.html

# Traces [​](#traces)

## Application Traces [​](#application-traces)

Shopware PaaS Native allows you to view your application's traces for a given environment via Grafana.

To access Grafana, run the following command:

bash

```shiki
sw-paas open grafana
```

This command will provide you with the Grafana URL, username, and password.

Once logged in to Grafana:

1. Go to the **Explore** tab.
2. Select **Tempo** as the data source.
3. Ensure the query type is **Search**
4. Filter traces by setting the Service Name to the value `shopware`.
5. Run the query to view your application traces.

## Trace Retention [​](#trace-retention)

Shopware PaaS Native keeps your latest traces available for review. Traces older than 14 days are automatically removed.

---

## Monitor events

**Source:** https://developer.shopware.com/docs/products/paas/shopware/monitoring/watch.html

# Monitor events [​](#monitor-events)

## Real-time Event Monitoring [​](#real-time-event-monitoring)

Shopware PaaS Native provides real-time event monitoring for your applications, allowing you to track deployments, application status changes, and other important events as they happen.

To start monitoring events, run the following command:

bash

```shiki
sw-paas watch
```

This command will start streaming events in real-time to your terminal.

## Monitoring Specific Applications [​](#monitoring-specific-applications)

You can monitor events for specific applications within your project:

bash

```shiki
sw-paas watch --application-ids app1,app2
```

This is particularly useful in multi-application projects where you only want to focus on certain services.

## Filtering Event Types [​](#filtering-event-types)

To reduce noise and focus on specific types of events, you can filter by event type:

bash

```shiki
sw-paas watch --event-types "EVENT_TYPE_DEPLOYMENT_STARTED,EVENT_TYPE_DEPLOYMENT_FINISHED"
```

Common event types include:

* `EVENT_TYPE_DEPLOYMENT_STARTED` - When a deployment begins
* `EVENT_TYPE_DEPLOYMENT_FINISHED` - When a deployment completes

The event stream will continue running until you stop it with `Ctrl+C`. All events are displayed in real-time with timestamps and detailed information about what's happening in your project.

## Understanding different Event Types [​](#understanding-different-event-types)

Events are generally linked to a preceding action. Each action is connected to a specific event type, which is emitted when a state change occurs. The type of each event is indicated in the output of the `sw-paas watch` command and can help to understand what is happening in your project.

Especially for deployments, the history of the events can be used to understand what happened during a deployment. To list all events of a specific deployment, use the following command:

bash

```shiki
sw-paas application deploy get
```

The output of the `DEPLOYMENT STATUS HISTORY` shows all events that were emitted during the deployment. This contains events from the underlying PaaS infrastructure as well as events from the shop itself.

The following table lists the most common event types and their descriptions:

| Event | Description |
| --- | --- |
| `UNSPECIFIED` | Default or unspecified deployment status |
| `PENDING` | Deployment is queued and waiting to start |
| `BASE` | Infrastructure: Base infrastructure components are being deployed |
| `BASE_FAILED` | Infrastructure: Base infrastructure deployment has failed |
| `BASE_SUCCESS` | Infrastructure: Base infrastructure deployment completed successfully |
| `SHOP` | Infrastructure: Shop-specific infrastructure components are being deployed |
| `SHOP_FAILED` | Infrastructure: Shop infrastructure deployment has failed |
| `SHOP_SUCCESS` | Infrastructure: Shop infrastructure deployment completed successfully |
| `DEPLOYING_STORE` | Store: Shopware store application is being deployed |
| `DEPLOYING_STORE_FAILED` | Store: Shopware store deployment has failed |
| `DEPLOYING_STORE_SUCCESS` | Store: Shopware store deployment completed successfully |
| `DEPLOYMENT_SUCCESS` | Complete deployment finished successfully |
| `DEPLOYMENT_FAILED` | Complete deployment has failed |

---

## CDN

**Source:** https://developer.shopware.com/docs/products/paas/shopware/cdn/

# CDN [​](#cdn)

This section provides comprehensive information about Content Delivery Network (CDN) solutions for Shopware PaaS Native, with a focus on Fastly integration and optimization strategies.

## Fastly CDN [​](#fastly-cdn)

Fastly serves as the primary CDN solution for Shopware PaaS Native, delivering edge caching capabilities that significantly enhance your shop's performance and user experience. By storing HTTP cache at the nearest edge server to your customers, Fastly reduces response times globally while minimizing resource consumption on your application servers.

### Key Benefits [​](#key-benefits)

* **Global Performance**: Cached responses are served from edge locations worldwide, drastically reducing latency
* **Resource Optimization**: Reduces load on your application servers by serving cached content from the edge
* **Redis Cache Relief**: Minimizes Redis cache usage by handling HTTP cache at the CDN level
* **Automatic Scaling**: Seamlessly handles traffic spikes without impacting your application performance

### Integration [​](#integration)

Fastly is fully integrated into Shopware PaaS Native. The integration includes:

* Pre-configured VCL snippets for optimal Shopware performance
* Automatic cache invalidation mechanisms
* Soft purge capabilities to maintain performance during cache updates
* Deployment helper integration for seamless VCL snippet management

### Configuration [​](#configuration)

Fastly is automatically configured and enabled by default in Shopware PaaS Native environments. No additional Shopware configuration is required - the PaaS platform handles all Fastly setup, VCL snippets, and cache management automatically.

#### Custom Domain DNS Configuration [​](#custom-domain-dns-configuration)

To configure your custom domain with the Fastly CDN, you must configure a DNS record. Depending of the type of your record, the DNS configuration is different.

If you have multiple custom domains, you need to create a record per domain.

**None APEX record**

Configure a `CNAME` record with your custom domain's DNS to point to:

dns

```shiki
cdn.shopware.shop
```

**APEX record**

Configure a `A` with your custom domain's DNS to point to:

dns

```shiki
151.101.3.52
151.101.67.52
151.101.131.52
151.101.195.52
```

This configuration ensures that all traffic to your custom domain is routed through the Fastly CDN for optimal performance and caching.

#### Managing Custom Domains [​](#managing-custom-domains)

Custom domain management is handled through the `sw-paas` CLI domain command. You can attach multiple domains to a single shop. Following domain creation, you must update the application using `sw-paas application update`. You may use the same commit to trigger a deployment. This process will be automated in future releases.

Subsequently, you can configure the domain within Shopware and associate it with a storefront. Status update functionality is currently under development.

---

## Guides

**Source:** https://developer.shopware.com/docs/products/paas/shopware/guides/

# Guides [​](#guides)

This section provides a collection of common guides and best practices for working with Shopware PaaS Native. Here, you will find step-by-step instructions, helpful tips, and resources to assist you in setting up, configuring, and optimizing your Shopware PaaS Native environment.

---

## How to set up repository access

**Source:** https://developer.shopware.com/docs/products/paas/shopware/guides/setting-up-repository-access.html

## Setting Up Repository Access via Deploy Keys [​](#setting-up-repository-access-via-deploy-keys)

To enable Shopware PaaS Native to access your private Git repository, you must configure an **SSH deploy key**. This key allows the platform to securely clone your code during deployments.

Regardless of whether you use the CLI or set things up manually, you must **add the public SSH key to your repository**.

### Option 1: Automated Setup via PaaS CLI [​](#option-1-automated-setup-via-paas-cli)

For a quicker setup, you can use the PaaS CLI to automatically generate and register the key:

sh

```shiki
sw-paas vault create --type ssh
```

By default, this command stores the key at the **organization level**, making it available to all projects within the org. To limit the key to a specific project, use the `--project` flag:

sh

```shiki
sw-paas vault create --type ssh --project <project-id>
```

After running the command, copy the generated public key and add it to your Git repository's **Deploy keys** section (see instructions below).

### Option 2: Manual Setup [​](#option-2-manual-setup)

If you prefer full control over the SSH key creation process, follow these steps:

#### 1. Generate a Passwordless SSH Key Pair [​](#_1-generate-a-passwordless-ssh-key-pair)

Run the following command to generate an RSA key pair in PEM format:

bash

```shiki
ssh-keygen -t rsa -b 4096 -m PEM -f ./sw-paas
```

INFO

Alternative algorithms like **ED25519** and **ECDSA** are also supported, provided the key is **passwordless** and the **private key is in PEM format**.

#### 2. Add the Public Key to Your Repository [​](#_2-add-the-public-key-to-your-repository)

Open the file `sw-paas.pub`, copy its contents, and add it as a **read-only deploy key** in your Git repository:

* **GitHub**: Go to your repository `Settings` → `Deploy keys`
* **GitLab**/**Bitbucket**: Look for the equivalent "Deploy keys" section in your repository settings Be sure to enable **read-only access**.

#### 3. Store the Private Key in the Vault [​](#_3-store-the-private-key-in-the-vault)

Once the public key is added to your repo, store the corresponding private key in the Shopware PaaS Native Vault:

bash

```shiki
cat sw-paas | sw-paas vault create --type ssh --password-stdin
```

You can store the key at either:

* **Organization level**: Shared across all projects.
* **Project level**: Dedicated to a single project (takes precedence over the org-level key).

WARNING

Only one SSH key can be stored per level (organization or project). You may name the key freely, but keep in mind that a project-level key **overrides** an organization-level one during deployments.

---

## Using the Vault

**Source:** https://developer.shopware.com/docs/products/paas/shopware/guides/secrets-vault-guide.html

# Guide: Using the Shopware PaaS Vault [​](#guide-using-the-shopware-paas-vault)

This guide explains how to securely manage secrets using the Shopware PaaS CLI Vault. You’ll learn how to create, retrieve, and delete secrets — including SSH keys — with practical examples.

## What is the Vault? [​](#what-is-the-vault)

The Vault is a secure, centralized location to store sensitive data such as:

* Environment variables
* Build-time secrets
* SSH keys for accessing private Git repositories

Secrets stored in the Vault are reusable across all applications in your organization.

## Secret Types [​](#secret-types)

| Type | Description |
| --- | --- |
| `env` | Runtime environment variables for your app |
| `buildenv` | Build-time environment variables |
| `ssh` | SSH keys for secure Git access |

## Creating a Secret [​](#creating-a-secret)

To create a secret interactively:

sh

```shiki
sw-paas vault create
```

You will be prompted to select a secret type, key, and value.

### Creating an SSH Key Secret [​](#creating-an-ssh-key-secret)

To generate and store an SSH key for deployments:

sh

```shiki
sw-paas vault create --type ssh
```

After generation, the CLI will output the public key. Add this to your Git hosting provider (e.g., GitHub under **Deploy Keys**).

## Retrieving a Secret [​](#retrieving-a-secret)

Secrets are accessed by their unique `secret-id`. You can retrieve a secret using:

sh

```shiki
sw-paas vault get --secret-id SECRET-ID
```

To list all secrets and find their IDs:

sh

```shiki
sw-paas vault list
```

## Deleting a Secret [​](#deleting-a-secret)

To delete a secret from the Vault:

sh

```shiki
sw-paas vault delete --secret-id SECRET-ID
```

WARNING

This action is permanent. Ensure the secret is not in use before deleting it.

## Example Workflow: Using SSH Keys [​](#example-workflow-using-ssh-keys)

### Step 1: Generate and store an SSH key [​](#step-1-generate-and-store-an-ssh-key)

sh

```shiki
sw-paas vault create --type ssh
```

### Step 2: Add the public key to GitHub as a deploy key [​](#step-2-add-the-public-key-to-github-as-a-deploy-key)

Navigate to your GitHub repository → Settings → Deploy Keys → Add Key.

### Step 3: List all secrets to verify [​](#step-3-list-all-secrets-to-verify)

sh

```shiki
sw-paas vault list
```

### Step 4: Retrieve a specific secret [​](#step-4-retrieve-a-specific-secret)

sh

```shiki
sw-paas vault get --secret-id ssh-abc123xyz
```

### Step 5: Delete a secret (when no longer needed) [​](#step-5-delete-a-secret-when-no-longer-needed)

sh

```shiki
sw-paas vault delete --secret-id ssh-abc123xyz
```

---

## Frequently Asked Questions

**Source:** https://developer.shopware.com/docs/products/paas/shopware/faq.html

# Frequently Asked Questions [​](#frequently-asked-questions)

## Can I roll back my deployment if I lose my git history? [​](#can-i-roll-back-my-deployment-if-i-lose-my-git-history)

For now, no rollback is possible when you do a force push and lose your git history

## Is it possible to write to the local filesystem? [​](#is-it-possible-to-write-to-the-local-filesystem)

No, all containers are stateless, and local file writes are discouraged. Persistent storage must use S3 buckets or other external storage solutions. Changes to the filesystem and Shopware code must be made directly in the Git repository.

## How can I connect my already deployed application to a new branch? [​](#how-can-i-connect-my-already-deployed-application-to-a-new-branch)

The application that you create is linked to a commit SHA and not to a branch. You can change the existing application commit SHA by running `sw-paas application update`. What matters is the commit configured for a given application.

## Can I run different applications like Node.js? [​](#can-i-run-different-applications-like-node-js)

No, currently PaaS is limited to Shopware projects.

## How are secrets managed in PaaS? [​](#how-are-secrets-managed-in-paas)

Secrets are stored in the PaaS secret store and can be applied at the organization, project, or application level. They are encrypted in the database and decrypted only when accessed via the CLI.

## Can I access the database directly? [​](#can-i-access-the-database-directly)

Yes. Follow the guide on [databases](./resources/databases.html).

## Can I customize the infrastructure (e.g., change web server configurations)? [​](#can-i-customize-the-infrastructure-e-g-change-web-server-configurations)

No, the infrastructure is opinionated and pre-configured. Customizations at the server level are not allowed.

## Are CDN or database configurations customizable? [​](#are-cdn-or-database-configurations-customizable)

No, PaaS uses Fastly as the CDN and provides a fixed database configuration at the moment. Customizations to these resources are currently under development.

## Can I host my custom applications? [​](#can-i-host-my-custom-applications)

Custom applications and decoupled storefront hosting will be evaluated based on customer needs but are not currently supported.

## What is the difference between `exec` and `command` ? [​](#what-is-the-difference-between-exec-and-command)

1. **Container Management**:

   * `exec`: Uses an existing container and provides an interactive shell
   * `command`: Spins up a new container specifically for the command execution
2. **Execution Mode**:

   * `exec`: Interactive and synchronous
   * `command`: Non-interactive and can be asynchronous
3. **Use Cases**:

   * `exec`: Best for debugging, maintenance, and interactive work
   * `command`: Best for automation, CI/CD, and scheduled tasks

## Can I connect to my PaaS instance via SSH [​](#can-i-connect-to-my-paas-instance-via-ssh)

Yes, you can connect to your PaaS instance — but not via traditional SSH. Instead, we provide a remote terminal session through the `sw-paas exec` CLI command. This command allows you to execute shell commands inside your PaaS environment remotely, effectively giving you SSH-like access for troubleshooting, deployments, or interactive sessions.

## Where can I see the status of my PaaS application update? [​](#where-can-i-see-the-status-of-my-paas-application-update)

You can see the status of your PaaS application by running `sw-paas application list`. This command shows the current status of your application, including whether the update was successful or if it's still in progress. To monitor all real-time events associated with the project and its applications run `sw-paas watch` this provides a live stream of events and is especially useful for tracking the progress of an ongoing update.

---

## Known issues

**Source:** https://developer.shopware.com/docs/products/paas/shopware/known-issues.html

# Known Issues [​](#known-issues)

This document outlines acknowledged issues with Shopware PaaS Native, including workarounds if known.

## Size of messages for the message queue [​](#size-of-messages-for-the-message-queue)

Currently, Shopware does not prevent bigger messages, but will do so with the next major version 6.7. Ensure the messages you are sending do not exceed this limit. Check your local log files for this [critical log message](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/MessageQueue/Subscriber/MessageQueueSizeRestrictListener.php#L48)

## Plugins should support S3 compatible storage [​](#plugins-should-support-s3-compatible-storage)

Some third-party plugin providers may not currently support S3 compatible storage solutions. Such plugins cannot be used in Shopware PaaS Native since we use S3 compatible storage as the media storage backend. If you encounter such a situation, consider visiting the plugin’s documentation or contact the developer directly to verify whether the plugin supports remote storage via S3 or a compatible service and if there are any known workarounds or planned updates for S3 support.

## Network Considerations [​](#network-considerations)

Some commands do not support certain network configurations in the environment where they are executed.

The following commands — `exec` and `service` — establish mTLS tunnels, which are not compatible with **NAT** (Network Address Translation).

If you run these commands in environments such as a Virtual Machine (VM) or Windows Subsystem for Linux (WSL), ensure that the network mode is configured to `Host` or `Mirrored` mode.

---

## Shopware PaaS

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/

# Shopware PaaS [​](#shopware-paas)

INFO

Shopware PaaS is available at request for Shopware merchants. Please approach the [Shopware Sales](https://www.shopware.com/en/#contact-sales) to get more information on Shopware PaaS

Shopware PaaS is a platform-as-a-service to host, deploy and scale for your individual Shopware project. It comes with full flexibility and code ownership of a self-hosted Shopware project, but takes away the complexity of building custom infrastructure, build and testing pipelines, or deployment automation.

Get started by installing the PaaS CLI on your local development machine.

## Getting started with Shopware PaaS - How to deploy your first project [​](#getting-started-with-shopware-paas-how-to-deploy-your-first-project)

INFO

Prerequisites:

* Having a Shopware PaaS account (Select Register now on the authentication form when accessing <https://console.shopware.com>)
* Having the project\_id of an empty project created on Shopware PaaS
* Having the Shopware PaaS CLI installed, see <https://developer.shopware.com/docs/products/paas/shopware-paas/cli-setup.html>
* Having PHP ext-amqp installed (PaaS uses RabbitMQ instead of the regular DB to manage messages)

Steps:

1.) Create a local Shopware project on your laptop

sh

```shiki
composer create-project shopware/production demo --no-interaction --ignore-platform-reqs
```

2.) Enter the folder newly created

sh

```shiki
cd /demo
```

3.) Install the PaaS composer package

sh

```shiki
composer req paas
```

4.) Initialize your local Git repository

sh

```shiki
git init
```

5.) Add all the existing files to Git

sh

```shiki
git add .
```

6.) Create your first commit

sh

```shiki
git commit -am "initial commit"
```

7.) Configure the PaaS CLI with your project\_id

sh

```shiki
shopware project:set-remote PROJECT_ID
```

Where PROJECT\_ID is the project\_id of your empty project.

8.) Push the code to Shopware PaaS

sh

```shiki
git push shopware
```

## Step-by-step guide [​](#step-by-step-guide)

The sub-pages describe a more detailed step-by-step guide that you can follow to set up your PaaS project.

First, make sure your [PaaS CLI is set up correctly](./cli-setup.html). Once your PaaS CLI is up and running, it is time to [set up your project repository](./repository.html).

When your repository is set up correctly, you are ready to [push and deploy your project](./build-deploy.html) to the PaaS environment.

You can look into setting up [Elasticsearch](./elasticsearch.html), [RabbitMQ](./rabbitmq.html) and/or [Fastly](./fastly.html) to further enhance the performance of your PaaS project.

Finally, do not forget each PaaS project comes with [Blackfire](./blackfire.html) which will help you to monitor the response time and investigate performance issues of your project.

---

## PaaS CLI Setup

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/cli-setup.html

# PaaS CLI Setup [​](#paas-cli-setup)

The PaaS CLI is your tool to connect with your PaaS environment, push changes, trigger deployments, etc.

## Download and install [​](#download-and-install)

To install PaaS CLI, run the following command:

sh

```shiki
curl -sfS https://cli.shopware.com/installer | php
```

When you run the PaaS CLI for the first time, it will ask you to log in via your browser.

You can also generate an SSH key manually and add it in the **My profile > SSH Keys** section of your [PaaS Console](https://console.shopware.com/).

INFO

**Set up SSH keys**

If you are unsure of how to create SSH keys, please follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) provided by GitHub.

## Authenticate [​](#authenticate)

Next, you need to authenticate your PaaS CLI. This can be done through your browser. Just run the following command and follow the instructions:

sh

```shiki
shopware
```

---

## Repository

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/repository.html

INFO

**Platform.sh** is now **Upsun**. You may still encounter references to Platform.sh in code, documentation, or older materials. These references are equivalent to Upsun.

# Repository [​](#repository)

The source code of your project will reside in a git-based VCS repository. You can start with a plain project. However, we suggest starting with a new Composer create-project. You will learn more about the setup template in the [Setup Template](./setup-template.html) section.

INFO

This guide explains the repository setup using **GitHub**. You can also integrate Bitbucket or GitLab-based version control environments with Shopware PaaS. Refer to [Source Integrations](https://fixed.docs.upsun.com/integrations/source.html) for more information.

## Create a Shopware project [​](#create-a-shopware-project)

Firstly, create a new project with `composer create-project shopware/production <folder-name>` using the [Symfony Flex](./../../../guides/installation/template.html) template.

This will create a brand new Shopware 6 project in the given folder. Now, change it into the newly created project and require the PaaS configuration with `composer req paas`.

Secondly, create a new Git repository and push it to your favourite Git hosting service.

### Updating the PaaS template recipe [​](#updating-the-paas-template-recipe)

You can update the recipe to the latest version using the `composer recipes:update` [command](https://symfony.com/blog/fast-smart-flex-recipe-upgrades-with-recipes-update).

However, the template may receive breaking changes. For example, when making certain changes to file mounts (like using a "service mount" instead of a "local mount"), there is no way to migrate your existing data into the updated mount automatically. Due to this, we always recommend manually checking all changes in the `recipes:update` command provided for the PaaS package, as some updates to the `.platform-yaml` files might need extra manual actions. Every PaaS recipe update should be deemed a **breaking** update and thus be validated before applying it to your project.

## Add PaaS remote [​](#add-paas-remote)

Lastly, add a second remote, which allows us to push code towards the PaaS environment and trigger a deployment.

We first need the project ID, so we display all projects using

bash

```shiki
$ shopware projects

Your projects are:
+---------------+-----------+------------------+--------------+
| ID            | Title     | Region           | Organization |
+---------------+-----------+------------------+--------------+
| 7xasjkyld189e | paas-env  | <region-domain>  | shopware     |
+---------------+-----------+------------------+--------------+

Get a project by running: platform get [id]
List a projects environments by running: platform environments -p [id]
```

To add the project remote to your local repository, just run

bash

```shiki
shopware project:set-remote 7xasjkyld189e # Replace with your project ID
```

## Conclusion [​](#conclusion)

Now your repository is configured - you should have two remotes

sh

```shiki
$ git remote -v

origin	git@github.com:<project-repository>.git (fetch)
origin	git@github.com:<project-repository>.git (push)
shopware	<paas-url>.git (fetch)
shopware	<paas-url>.git (push)
```

| Remote | Function | Description |
| --- | --- | --- |
| `origin` | Project Code | This remote contains all your project specific source code |
| `shopware` | PaaS Environment | Changes pushed to this remote will be synced with your PaaS environment |

## Migrating from the old template to the new template [​](#migrating-from-the-old-template-to-the-new-template)

If you have already used the [Shopware PaaS old template](https://github.com/shopwareArchive/paas), please follow the guide to [migrate it to the new structure](./../../../guides/installation/template.html#how-to-migrate-from-production-template-to-symfony-flex).

The following tasks have to be done additionally to the flex migration:

* The root `.platform.app.yml` has been moved to `.platform/applications.yaml`
* The following services has been renamed:
  + `queuerabbit` to `rabbitmq`
  + `searchelastic` to `opensearch`

As the services are renamed, a completely new service will be created. Here are three possible options available:

* Rename the services back again
* Start with a new service and re-index Elasticsearch
* [Perform the transitional upgrade of two services in parallel for some time](https://fixed.docs.upsun.com/add-services/opensearch.html#upgrading)

---

## Build & Deploy

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/build-deploy.html

# Build and Deploy [​](#build-and-deploy)

Now that we have set up the repository, we are ready to push changes to your PaaS environment.

The key concept is that your PaaS project is a git repository. Every time you push to that repository, a new version of your store will be created from the source code and deployed. Different environments (e.g., dev-previews, staging, and production) are mapped by corresponding branches.

## Push main branch [​](#push-main-branch)

To push your latest changes, run the following commands from your terminal:

bash

```shiki
git add .
git commit -m "Applied new configuration"
git push -u shopware main
```

First, we stage all changes and then add them as a new commit. Then, we push them to our `shopware` origin (remember, the one for our PaaS environment) on the `main` branch.

This will trigger a new build with a subsequent deploy consisting of the following steps:

| Build | Deploy |
| --- | --- |
| Configuration validation | Hold app requests |
| Build container image | Unmount live containers |
| Installing dependencies | Mount file systems |
| Run [build hook](./setup-template.html#build-hook) | Run [deploy hook](./setup-template.html#deploy-hook) |
| Building app image | Serve requests |

After both steps have been executed successfully (you will get extensive logging about the process), you will be able to see the deployed store on a link presented at the end of the deployment.

## First deployment [​](#first-deployment)

The first time the site is deployed, Shopware's command line installer will run and initialize Shopware. It will not run again unless the `install.lock` file is removed. **Do not remove that file unless you want the installer to run on the next deploy.**

The installer will create an administrator account with the default credentials.

| username | password |
| --- | --- |
| `admin` | `shopware` |

Make sure to change this password immediately in your Administration account settings. Not doing so is a security risk.

## Composer authentication [​](#composer-authentication)

You must authenticate yourself to install extensions from the Shopware store via composer. In your local development environment, this is possible by creating an `auth.json` file that contains your auth token. However, this file shouldn't be committed to the repository.

The following command adds your authentication token to the secure environment variable storage of Shopware Paas. This variable (contains the content which would otherwise be in `auth.json`) will be available during the build step and be automatically picked up by the composer.

bash

```shiki
shopware variable:create --level project --name env:COMPOSER_AUTH --json true --visible-runtime false --sensitive true --visible-build true --value '{"bearer": {"packages.shopware.com": "%place your key here%"}}'
```

Make sure to replace `%place your key here%` with your actual token. You can find your token by clicking 'Install with Composer' in your Shopware Account.

## Extending Shopware - plugins and apps [​](#extending-shopware-plugins-and-apps)

The PaaS recipe uses the [Composer plugin loader](./../../../guides/hosting/installation-updates/cluster-setup.html#composer-plugin-loader), which expects all extensions being installed via Composer.

## Manually trigger rebuilds [​](#manually-trigger-rebuilds)

Sometimes, you might want to trigger a rebuild and deploy of your environment without pushing new code to your project. To do this for your main environment, create a `REBUILD_DATE` environment variable. This triggers a build right away to propagate the variable.

bash

```shiki
shopware variable:create --environment main --level environment --prefix env --name REBUILD_DATE --value "$(date)" --visible-build true
```

To force a rebuild at any time, update the variable with a new value:

bash

```shiki
shopware variable:update --environment main --value "$(date)" "env:REBUILD_DATE"
```

This forces your application to be built even if no code has changed.

---

## Setup Template

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/setup-template.html

# Setup Template [​](#setup-template)

The setup template is installed automatically using Symfony Flex when requiring the `paas` package as described in the [Repository](./repository.html). It contains build and deployment logic for Shopware PaaS as well as configuration for the underlying infrastructure and services. In this chapter, we will have a look at these customizations.

Below is an overview of the files and directories added by the PaaS meta-package:

text

```shiki
./
├─ .platform/
│  ├─ applications.yaml
│  ├─ routes.yaml
│  ├─ services.yaml
├─ bin/
│  ├─ prestart_cacheclear.sh
├─ config/
│  ├─ packages/
│  │  ├─ paas.yaml
├─ files/
│  ├─ theme-config/
```

## [.platform/applications.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/applications.yaml) [​](#platform-applications-yaml)

This file contains Shopware PaaS specific configuration and can be customized as needed for your individual project.

### name [​](#name)

It is the name of your app. It is used in commands like:

bash

```shiki
shopware ssh -A app 'bin/console theme:dump'
```

Unless there is a specific need for it, leave it as `app`.

### type [​](#type)

This section contains the base image used for your build process. This is also where you configure the PHP version used in your PaaS environment.

### variables [​](#variables)

This section contains configuration for environment variables or server settings. General store settings and configurations are set here. Here you can inject custom environment variables or enable feature flags.

Variables in the `env` section are automatically injected as environment variables. If a variable is also set in your .env file, the variables set in the `applications.yaml` file will overwrite these.

### hooks [​](#hooks)

Lifecycle hooks are custom scripts that are called during your build and deploy processes. See more on the [deployment process](./build-deploy.html#push-main-branch).

#### build hook [​](#build-hook)

This script is called during the build process and builds your application's assets (composer dependencies, javascript- and css- assets of Shopware core and extensions) and disables the UI installer. You can customize this script if you need. During the execution, you may perform write operations on the file system, which are prohibited in the proceeding steps unless the corresponding directory is [mounted](#mounts).

You do not have access to any of the services (like the database or Redis) configured, as the application is not running yet. You should ensure to perform as much of your entire building procedure during the build step, as web traffic is blocked during the execution of the deploy step.

#### deploy hook [​](#deploy-hook)

WARNING

The environment will be cut off from web traffic during the execution of the deploy hook. The shorter this script is, the shorter the downtime will be.

This script is called during the deployment process. Theme configuration is copied, the install scripts are executed and secrets are generated.

* Copy theme configuration
* Run database migrations
* Set sales channel domains for non-production environments
* Clear cache

If this is the first deployment, the following operations are performed:

* Setup script is executed
* Theme is set
* Secrets are generated
* `install.lock` file is created

You can also customize this script, however, make sure to keep operations to a minimum, as your store will not be exposed to web traffic during the execution. Connections made during the meantime will be queued in a suspended state and not necessarily fail but will take longer than usual (i.e., until the deployment has finished).

#### post\_deploy [​](#post-deploy)

Analogous to the two preceding hooks, the post\_deploy hook provides an entry point for custom scripts. However, this hook is executed after the application container accepts connections.

### relationships [​](#relationships)

This section defines the mapping between services created in the [services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml) and the application itself.

### mounts [​](#mounts)

By default, the entire storage of your application is read-only. Mounts define directories that are writable after the build is complete. They aren’t available during the build.

Every mount has one of two types: `local` or `service`. A local mount is unique to the service that is accessing it. For example `/var/cache` is a good local mount because the Symfony cache should not be shared between different app servers. A service mount references to another service (of the type `network-storage`). These mounts are shared between other services and between the different app servers. For example the `/public/media` folder is a good shared mount because the [workers](#workers) that consume the Messenger queue should be able to read and write to the media directory.

### web [​](#web)

The public root of your application `public/index.php` is configured so the server knows where to route dynamic requests.

### workers [​](#workers)

Workers are copies of your application instance after the [build hook](#build-hook) has been executed. They are usually configured with a start command. By default, there are two configured workers - one for message queues and one for scheduled tasks.

## [.platform / routes.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/routes.yaml) [​](#platform-routes-yaml)

This file configures incoming HTTP requests routed to the `app` instance.

## [.platform / services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml) [​](#platform-services-yaml)

This file contains services that are used by the `app` instances. Depending on your setup, uncomment or add services that you need, and they will be created and scaled automatically.

In our template there are 4 different services enabled by default:

* `db`
* `cacheredis`
* `rabbitmq`
* `fileshare`

## [files / theme-config](https://github.com/shopware/recipes/tree/main/shopware/paas-meta/6.4/files/theme-config) [​](#files-theme-config)

We suggest checking in your theme configuration to version control in this directory. Read more on the concept of [builds without database](./../../../guides/hosting/installation-updates/deployments/build-w-o-db.html).

## Automatic Environment Variables [​](#automatic-environment-variables)

Shopware PaaS automatically sets environment variables based on the services configured in your `services.yaml` and linked via `relationships` in your `applications.yaml`. This eliminates the need to manually configure connection strings.

### Global Variables [​](#global-variables)

These variables are set automatically for every deployment:

| Variable | Example Value |
| --- | --- |
| `APP_SECRET` | `a3c45d78e91f2b3c4d5e6f7a8b9c0d1e` |
| `APP_ENV` | `prod` |
| `APP_URL` | `https://main-abc123.eu-5.platformsh.site` |
| `MAILER_DSN` | `smtp://localhost:25` |

### Database (`database`) [​](#database-database)

| Variable | Example Value |
| --- | --- |
| `DATABASE_URL` | `mysql://user:password@database.internal:3306/main` |

### Database Replica (`database-replica`) [​](#database-replica-database-replica)

| Variable | Example Value |
| --- | --- |
| `DATABASE_REPLICA_0_URL` | `mysql://user:password@database-replica.internal:3306/main` |

### RabbitMQ (`rabbitmqqueue`) [​](#rabbitmq-rabbitmqqueue)

| Variable | Example Value |
| --- | --- |
| `MESSENGER_TRANSPORT_DSN` | `amqp://guest:guest@rabbitmq.internal:5672/%2f/messages` |
| `MESSENGER_TRANSPORT_DSN_PREFIX` | `amqp://guest:guest@rabbitmq.internal:5672/%2f/` |

### Redis Cache (`rediscache`) [​](#redis-cache-rediscache)

| Variable | Example Value |
| --- | --- |
| `CACHE_DSN` | `redis://rediscache.internal:6379` |
| `CACHE_URL` | `redis://rediscache.internal:6379` |

### Redis Session (`redissession`) [​](#redis-session-redissession)

| Variable | Example Value |
| --- | --- |
| `SESSION_REDIS_HOST` | `redissession.internal` |
| `SESSION_REDIS_PORT` | `6379` |
| `SESSION_REDIS_URL` | `redis://redissession.internal:6379` |

### OpenSearch (`opensearch`) [​](#opensearch-opensearch)

| Variable | Example Value |
| --- | --- |
| `OPENSEARCH_URL` | `http://opensearch.internal:9200` |
| `ADMIN_OPENSEARCH_URL` | `http://opensearch.internal:9200` |

### Elasticsearch (`elasticsearch`) [​](#elasticsearch-elasticsearch)

| Variable | Example Value |
| --- | --- |
| `ELASTICSEARCH_HOST` | `elasticsearch.internal` |
| `ELASTICSEARCH_PORT` | `9200` |
| `ELASTICSEARCH_URL` | `http://elasticsearch.internal:9200` |

### MongoDB (`mongodatabase`) [​](#mongodb-mongodatabase)

| Variable | Example Value |
| --- | --- |
| `MONGODB_SERVER` | `mongodb.internal:27017` |
| `MONGODB_DB` | `main` |
| `MONGODB_USERNAME` | `user` |
| `MONGODB_PASSWORD` | `password` |

---

## Elasticsearch

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/elasticsearch.html

# Elasticsearch [​](#elasticsearch)

Perform the following steps to activate Elasticsearch in your environment.

## Enable service [​](#enable-service)

Add (or uncomment) the Elasticsearch service configuration.

yaml

```shiki
// .platform/services.yaml
elasticsearch:
   type: opensearch:2
   disk: 256
```

## Add relationship [​](#add-relationship)

Add (or uncomment) the relationship for the app configuration.

yaml

```shiki
// .platform.app.yaml
relationships:
    elasticsearch: "elasticsearch:opensearch"
```

## Configure instance [​](#configure-instance)

Follow the setup and indexing steps to prepare your instance as described in the [setup Elasticsearch](./../../../guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.html#prepare-shopware-for-elasticsearch).

After that, the following environment variables are provided by the Composer package `shopware/paas-meta:

* `SHOPWARE_ES_HOSTS`

## Enable Elasticsearch [​](#enable-elasticsearch)

Ultimately, activate Elasticsearch by setting the environment variable `SHOPWARE_ES_ENABLED` to `1`. You can either do that by uncommenting the corresponding line in `platformsh-env.php` or setting it in the [variables](./setup-template.html#variables) section of the app configuration.

---

## RabbitMQ

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/rabbitmq.html

# RabbitMQ [​](#rabbitmq)

RabbitMQ is enabled by default in the template. This service is optional but recommended. It can be disabled and replaced by an SQL-backed queue.

## Disable service [​](#disable-service)

Comment out the RabbitMQ service configuration.

yaml

```shiki
// .platform/services.yaml
#rabbitmq:
#   type: rabbitmq:3.8
#   disk: 1024
```

## Remove relationship [​](#remove-relationship)

Comment out the relationship for the app configuration.

yaml

```shiki
// .platform.app.yaml
#relationships:
#   rabbitmqqueue: "rabbitmq:rabbitmq"
```

## Push changes [​](#push-changes)

Push the changes to your git repository and wait for the deployment to finish.

---

## Fastly

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/fastly.html

# Fastly [​](#fastly)

Fastly allows Shopware to store the HTTP Cache at the nearest edge server to the end customer. This saves a lot of resources as the cached responses don't reach the actual application, and it decreases the response time drastically worldwide. Another benefit is that the Redis cache is not used anymore and will have less cache items.

## Setup [​](#setup)

INFO

Fastly is supported in Shopware versions 6.4.11 or newer.

1. Make sure `FASTLY_API_TOKEN` and `FASTLY_SERVICE_ID` are set in the environment or contact the support when they are missing.
2. Install the Fastly Composer package using `composer req fastly`.
3. Disable caching in the `.platform/routes.yaml`.
4. Push the new config and Fastly gets enabled.

INFO

**Enable Fastly Soft Purges**

Make sure your Fastly configuration has [soft purges](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#fastly-soft-purge) enabled to mitigate the impact of large-scale cache invalidations.

---

## Blackfire

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/blackfire.html

INFO

**Platform.sh** is now **Upsun**. You may still encounter references to Platform.sh in code, documentation, or older materials. These references are equivalent to Upsun.

# Blackfire Continuous Observability Solution [​](#blackfire-continuous-observability-solution)

Blackfire is bundled with every Enterprise Shopware PaaS project without any additional fees.  
 All the people invited to the project can access Blackfire, and all environments can be monitored.

The APM will show you when, where, and why performance issues happen.

Here are the main Blackfire features:

* Monitoring (Live metrics from your app): identify slow transactions, background jobs, services or third-party calls
* Deterministic Profiling (Deep, runtime code analysis): get function-call level metrics and spot root causes of bottlenecks
* Continuous Profiling (Combines profiling and monitoring with minimal overhead): easily identify hotspots, optimize resource usage, and compare timeframes to visually identify the flaky parts of your application
* Testing (Performance budget control): verify code behavior and performance
* Alerting (Warnings upon abnormal behaviors)
* Recommendations (Actionable insights and expert advice): benefit from unique, cutting-edge issue detection with documented resolution recommendations
* CI/CD integration (Automated testing and regression prevention): add Blackfire to any testing pipeline and existing tests, or start from scratch with our Open-Source crawler, tester, and scraper

## Access [​](#access)

You'll find the link to access Blackfire on the Shopware PaaS Console at the environment level. Once you click on the link, you'll be redirected to the Upsun authentication portal.

If this is your first authentication, please use your usual Shopware PaaS email and follow the "reset password" workflow so you can set your Upsun password.

## Onboarding Guide [​](#onboarding-guide)

We encourage you to look at our [self-onboarding guide](https://docs.blackfire.io/onboarding/index). It includes extensive documentation and videos to help use and understand Blackfire.

## Deterministic Profiling [​](#deterministic-profiling)

We recommend you install the [Firefox Blackfire extension](https://addons.mozilla.org/en-US/firefox/addon/blackfire/) or the [Chrome Blackfire extension](https://chromewebstore.google.com/detail/blackfire-profiler/miefikpgahefdbcgoiicnmpbeeomffld?hl=en) so you can trigger profiles of targeted transactions or group of transactions.

![Blackfire profile](/assets/blackfire-profile.DByio_gV.png)

---

## Composable-Frontends Performance

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/composable-frontends/performance.html

# Composable-Frontends Performance [​](#composable-frontends-performance)

## Shopware Backend caching [​](#shopware-backend-caching)

The current versions of Shopware rely heavily on `POST` requests for `/store-api/`.  
`POST` requests are by design not cacheable, so Fastly simply passes them to the backend cluster without even trying to cache them.

A temporary [plugin](https://github.com/shopwareLabs/SwagStoreApiCache) has been developed. With this workaround, Fastly can cache some of the `/store-api/` `POST` requests.

This plugin includes new Fastly snippets that must be used instead of the usual ones.

The plugin includes [a few routes](https://github.com/shopwareLabs/SwagStoreApiCache/blob/trunk/src/Listener/StoreAPIResponseListener.php#L57) which will become automatically cacheable.

If you need to cache additional routes, it can be done via the admin config: `SwagStoreAPICache.config.additionalCacheableRoutes`.

As usual, ensure [soft-purges](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#fastly-soft-purge) are enabled.

Please note that we're actively working on moving the `store-api` requests from `POST` to `GET` to make them cacheable, so the use of this plugin would no longer be required.  
 More details in the [Epic](https://github.com/shopware/shopware/issues/7783).

## Composable Frontend caching [​](#composable-frontend-caching)

To get the best performance, Frontend caching must be enabled.

There are a few steps to get there:

1. Configure a Fastly service on top of each Frontend. It can be one Fastly service per Frontend, or it can be a single Fastly service with multiple domains and hosts configured.
2. Update `nuxt.config.ts` so `routesRules`, using Incremental Static Regeneration (`ISR`), have the required cache headers. Example:

ts

```shiki
'/': {
      		isr: 60 * 60 * 24,
      		headers: {
        		'cache-control': 'public, s-maxage=3600, stale-while-revalidate=1800'
      		}
    	},
'/**': {
      		isr: 60 * 60 * 24,
      		headers: {
        		'cache-control': 'public, s-maxage=3600, stale-while-revalidate=1800'
      		}
    	},
```

`s-maxage` and `stale-while-revalidate` can be adjusted.  
`s-maxage` represents how long in seconds the content will be cached on Fastly.  
`stale-while-revalidate` represents how long a stale page (aka an expired page) can be kept and served, so when a client requests this page, the stale object is served while a request to update it is done in the background, so the next client will have an updated version of the page.

::: Note

The cache invalidation process is only on the Fastly Backend service. The Shopware instance is not "aware" of the Frontend instance. It cannot trigger cache invalidation. Items will remain in cache for the `s-maxage` duration.

:::

## Get rid of the OPTIONS requests (CORS) [​](#get-rid-of-the-options-requests-cors)

When using a different domain for backend requests, browsers are forced to send `OPTIONS` requests. Those requests, also named `preflight` requests, are due to `CORS` checks. Every time the browser needs to send a request to the backend, it must first confirm it's authorized to do so.

`OPTIONS` requests are by default not cacheable as the responses may vary depending on the request's headers. There is a possibility to include an `Access-Control-Max-Age` header in the `OPTIONS` responses, so it forces the browser to cache the answer for a longer period than the default 5 seconds.

But the recommended action is to remove those `CORS` checks completely. To do so, all the requests to the Shopware backend must be sent on the same domain as the Frontend, so the browser only sees one single domain.

For this, the Frontend Fastly service can be configured to serve both the Frontend and the Backend requests.

The config is pretty simple. With the additional host, the logic is only four lines of code:

vcl

```shiki
if (req.url.path ~ "^/store-api/") { 
  set req.http.host = "backend.mydomain.com"; 
  set req.backend = F_Backend__Shopware_instance_; 
  return (pass);
}
```

The `return (pass)` is very important. We must not add a cache layer on the Frontend Fastly service to avoid invalidation issues. The Backend Fastly service remains the one responsible for caching.

## Optimize the Fastly Backend hit-ratio [​](#optimize-the-fastly-backend-hit-ratio)

Once an item has been set into the cart, a new cookie named `sw-cache-hash` is sent. The default VCL hash snippet includes the content of this cookie in the hash (aka the cache key). It means that the first backend request that was cached will no longer be cached when requested once an item has been added to the cart.

If rules based pricing is not used in the Shopware instance, the following section can be commented out in the VCL hash snippet:

vcl

```shiki
# Consider Shopware http cache cookies
#if (req.http.cookie:sw-cache-hash) {
#	set req.hash += req.http.cookie:sw-cache-hash;
#} elseif (req.http.cookie:sw-currency) {
#	set req.hash += req.http.cookie:sw-currency;
#}
```

## Check the results using the Developer Tools [​](#check-the-results-using-the-developer-tools)

Once everything is configured, check for the `Age` header to confirm the responses are cached.

---

## Blackfire Continuous Profiling of Nuxt.js

**Source:** https://developer.shopware.com/docs/products/paas/shopware-paas/composable-frontends/blackfire.html

# Blackfire Continuous Profiling of Nuxt.js [​](#blackfire-continuous-profiling-of-nuxt-js)

It's possible to enable [Blackfire Continuous Profiling](https://www.blackfire.io/continuous-profiler/) on a frontend based on Nuxt.js.

1. Install the Blackfire Node.js Lib: `npm install @blackfireio/node-tracing`
2. Add the environment variable `BLACKFIRE_ENABLE=1`
3. Add `./server/plugins/blackfire.ts`:

ts

```shiki
// server/plugins/blackfire.ts
export default defineNitroPlugin(async () => {
  if (process.env.BLACKFIRE_ENABLE !== '1') return;

  try {
    // Works in ESM: dynamically import and handle both default/named exports
    const mod = await import('@blackfireio/node-tracing');
    const Blackfire: any = (mod as any).default || mod;

    Blackfire.start({
      appName:
        process.env.BLACKFIRE_APP_NAME || 'shopware-frontend',
      // durationMillis: 45000,
      // cpuProfileRate: 100,
      // labels: { service: 'frontend', framework: 'nuxt3' },
    });

    console.info('[blackfire] node-tracing started');
  } catch (e) {
    console.error('[blackfire] failed to start node-tracing', e);
  }
});
```

---

