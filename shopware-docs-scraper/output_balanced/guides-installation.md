# Guides Installation

*Scraped from Shopware Developer Documentation*

---

## Installation

**Source:** https://developer.shopware.com/docs/guides/installation/

# Overview — Shopware 6 Installation [​](#overview-—-shopware-6-installation)

Welcome to the Shopware 6 Developer Installation Guide, which will help you set up a local Shopware 6 development environment whether you’re:

* building a custom shop project
* developing a plugin, app, or theme
* contributing to the Shopware core

You can choose from three supported setup options, each designed for specific use cases and development workflows. All setups start from the [Shopware Project Template](./template.html).

## Shopware project template [​](#shopware-project-template)

Every setup begins with the Project Template. It creates a new Composer project that includes Shopware as a dependency, allowing you to:

* Extend the project with plugins, apps, or themes
* Customize configurations and services
* Align the environment with your development goals

If you have downloaded the [shopware-installer.phar package](https://www.shopware.com/en/download/) instead of using Composer, skip the `composer create-project` step and follow the remaining instructions from the [Project Template](https://developer.shopware.com/docs/guides/installation/template.html) guide.

## Supported setups [​](#supported-setups)

| Setup | Description | Recommended For |
| --- | --- | --- |
| [Docker Setup](./setups/docker.html) | A complete, containerized environment including all required services (database, search engine, cache, etc.). | Most developers — provides production-like conditions, consistent across teams and CI/CD. |
| [Symfony CLI Setup](./setups/symfony-cli.html) | Runs directly on your host system using local PHP and Composer. Lightweight and fast to start. | Quick plugin or theme development, or environments where Docker isn’t available. |
| [Devenv Setup](./setups/devenv.html) | A reproducible, Nix-based setup offering deterministic builds and cross-platform consistency. | Core contributors and advanced users managing multiple Shopware versions. |

INFO

If you’re unsure which setup to choose, start with the Docker setup — it provides the smoothest onboarding experience.

---

## Setups

**Source:** https://developer.shopware.com/docs/guides/installation/setups/

# Setups [​](#setups)

Once your system meets the [requirements](./../requirements.html), you can choose how you want to run your Shopware 6 development environment. This page helps you understand how each setup works in practice: What it’s best at, what to expect in daily use, and how to switch between them.

## Docker setup (recommended) [​](#docker-setup-recommended)

Docker runs your entire Shopware environment in containers, including PHP, MySQL, Redis, Elasticsearch, and Mailhog. It gives you a production-like stack with minimal manual setup.

**What to expect**

* All services run inside containers managed by Docker Compose.
* Great parity between development, CI, and production.
* Easy to reset or rebuild environments (`docker compose down -v`).
* Higher resource usage, but consistent results on any machine.

**When it shines**

* You want zero “works on my machine” issues.
* You collaborate with others or use CI/CD pipelines.
* You need full service parity (e.g. caching, queues, search).

[Docker setup guide →](./docker.html)

## Symfony CLI setup [​](#symfony-cli-setup)

Symfony CLI runs Shopware locally using your host system’s PHP and Composer installation. It’s lightweight, fast, and easy to debug using your local toolchain.

**What to expect**

* Uses your installed PHP, MySQL, and Node.js directly.
* Minimal overhead and startup time.
* Ideal for plugin, theme, or app developers who want rapid iteration.
* You manage local dependencies (e.g. PHP extensions, database) yourself.

**When it shines**

* You’re building or testing extensions, not full stacks.
* You prefer editing and debugging locally.
* You’re on a resource-limited machine.

[Symfony CLI setup guide →](./symfony-cli.html)

## Devenv setup [​](#devenv-setup)

Devenv uses [Nix](https://nixos.org/) to define a reproducible Shopware development environment. It ensures everyone — across macOS, Linux, and CI — gets the same dependency versions and behavior.

**What to expect**

* You define all tools and services in `devenv.yaml`.
* Nix handles installation and version consistency automatically.
* Works well in multi-version or multi-project contexts.
* Slightly steeper learning curve but high reliability.

**When it shines**

* You contribute to Shopware core or maintain multiple versions.
* You want reproducibility between developers and CI.
* You value a declarative, version-controlled environment.

[Devenv setup guide →](./devenv.html)

## Community and alternative Docker tooling [​](#community-and-alternative-docker-tooling)

If you prefer a more automated or GUI-friendly way to run Docker environments, DDEV and Dockware are both popular within the Shopware community. **Note:** DDEV and Dockware are community-maintained and not officially supported by Shopware.

### DDEV setup [​](#ddev-setup)

[DDEV](https://ddev.com/) is a developer-friendly wrapper around Docker that automates environment setup using simple CLI commands.

**Why use DDEV**

* Simplifies Docker configuration: no manual `docker-compose.yml` needed.
* One command (`ddev start`) to start your Shopware environment.
* Easy to switch PHP/MySQL/Node versions per project.
* Integrates well with VS Code and PHPStorm.

**Use it when**

* You want a pre-configured, easy-to-use Docker experience.
* You prefer to focus on code, not container details.

[DDEV with Shopware example →](https://github.com/ddev/test-shopware6)

### Dockware setup [​](#dockware-setup)

[Dockware](https://www.dockware.io/) provides ready-to-run Docker images for quickly spinning up demo stores or full local environments.

**Why use Dockware**

* Pre-built images for Shopware 5, 6, and nightly builds.
* Includes all key services: PHP, DB, Elasticsearch, Mailhog, Adminer, etc.
* Great for testing specific versions or quick evaluation.
* Can be used standalone or integrated into CI pipelines.

**Use it when**

* You need a running Shopware instance in seconds.
* You’re testing multiple Shopware versions or demos.
* You prefer minimal setup over full customization.

[Dockware documentation →](https://docs.dockware.io/)

## Switching between setups [​](#switching-between-setups)

All setups share the same Shopware [Project Template](./../template.html). Only the runtime environment differs. You can safely switch between setups as long as you keep separate environment configurations.

To switch setups:

1. Stop running services (e.g., `docker compose down`, or `symfony server:stop`).
2. Use separate directories for each setup.
3. Reuse the same project template if needed. Each setup has its own configuration files.

You can always migrate between setups later. Your Shopware project remains the same.

## Next step [​](#next-step)

Choose your preferred setup and follow its related guide. Once your setup is running, you can start developing your shop, app, plugin, or theme.

## Installing Shopware CLI [​](#installing-shopware-cli)

Most developers install the [Shopware CLI](./../../../products/cli/), which helps with building, refactoring, validating, and managing Shopware projects and extensions. It works with all setups (Docker, Symfony CLI, Devenv, DDEV, Dockware) and is used in most Shopware upgrade, build, and CI workflows. If you're using the Docker setup, the CLI comes preinstalled and is available in the container shell.

---

## Docker

**Source:** https://developer.shopware.com/docs/guides/installation/setups/docker.html

# Docker [​](#docker)

INFO

This setup is intended for development. If you want to use Docker for production, please check out this [guide](./../../hosting/installation-updates/docker.html).

Docker is a platform that enables developers to develop, ship, and run applications inside containers. These containers are lightweight, standalone, and executable packages that include everything needed to run an application: code, runtime, system tools, libraries, and settings. To get started with Docker, you can follow the official [Docker installation guide](https://docs.docker.com/get-started/get-docker/).

The Docker setup automatically provides all backend services (PHP, MySQL, Elasticsearch, Redis, Mailhog, etc.) so you don’t need to install anything else manually.

In this guide, we will run PHP, Node, and all required services in Docker containers. If you just want to run the services (MySQL/OpenSearch/Redis/...) in Docker, check out the [Docker](./docker.html) guide.

## Prerequisites [​](#prerequisites)

* [Docker](https://docs.docker.com/get-started/get-docker/) or [OrbStack](https://docs.orbstack.dev/quick-start) (macOS) is installed and running. OrbStack is a fast, free (for personal use) alternative to Docker.
* `make` is installed on your machine (`apt install make` on Ubuntu, `brew install make` on macOS)
* `Docker Compose` is installed on your machine. Docker Desktop provides it automatically. If you're using OrbStack or something else, you can follow the official [Docker Compose installation guide](https://docs.docker.com/compose/install/).
* Enough disk and network capacity to pull images (~500MB+ per image depending on tags)

## Pre-pull the image (optional) [​](#pre-pull-the-image-optional)

If you haven’t yet downloaded the Shopware Docker image, pull it now:

bash

```shiki
docker pull ghcr.io/shopware/docker-dev:php8.3-node24-caddy
```

If you skip this step, Docker will automatically download the image during project creation. That’s normal, but pre-pulling makes the process cleaner and enables you to avoid waiting for large image downloads.

## Create a new project [​](#create-a-new-project)

Create a new empty directory and navigate to it:

bash

```shiki
mkdir my-project && cd my-project
```

Then create a new project (required):

bash

```shiki
docker run --rm -it -v $PWD:/var/www/html ghcr.io/shopware/docker-dev:php8.3-node24-caddy new-shopware-setup
```

Or you can use a specific version of Shopware (optional), like so:

bash

```shiki
docker run --rm -it -v $PWD:/var/www/html ghcr.io/shopware/docker-dev:php8.3-node24-caddy new-shopware-setup 6.6.10.0
```

This step creates your new Shopware project in the current directory, along with a `compose.yaml` and a `Makefile`. The difference from regular `composer create-project` is that we run PHP and Composer from within the Docker image. This means you don’t need to have PHP or Composer installed on your local machine.

The project creation currently takes several minutes to complete.

During the process, this prompt will appear: `Do you want to use Elasticsearch? (y/N)`. Elasticsearch improves search performance for large catalogs. We recommend:

* answering "yes" if you expect thousands of products or use Shopware's advanced search features. You'll need an `elasticsearch` container/service. [Go here](https://developer.shopware.com/docs/guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.html) to learn more about Elasticsearch setup.
* answering "no" if you’re just testing locally or have a small dataset. In this case, Shopware will use the MariaDB database for search.

Shopware projects include files that use a combination of Symfony, Composer, Docker, and Shopware-specific conventions.

Project structure explained (click to expand)

| Item | Type | Purpose / what it contains | Notes |
| --- | --- | --- | --- |
| **bin/** | Directory | Executable scripts (e.g., `bin/console` — the main CLI for Shopware/Symfony). | Think of it like `npm run` or `go run` scripts. Use `bin/console` to run commands inside the app. |
| **compose.yaml** | Docker | Defines the Docker services (web, database, mailpit, etc.). | Equivalent to your project’s “infrastructure recipe.” |
| **compose.override.yaml** | Docker | Local overrides for the default Docker Compose stack (e.g., port mappings, extra volumes). | Optional; used to customize or extend services locally. |
| **composer.json** | PHP dependency manifest | Lists PHP dependencies and metadata (like `package.json`). | `composer install` reads this. |
| **composer.lock** | Dependency lock file | Locks exact versions of PHP packages. | Don’t edit manually; committed to git. |
| **config/** | Directory | Symfony configuration files (framework, database, mail, etc.). | Similar to `config/` in many web frameworks. |
| **custom/** | Directory | Your plugins, themes, or app customizations. | This is where you add new extensions — your “src” for Shopware plugins. |
| **files/** | Directory | Uploaded media and temporary files. | Ignored by git; generated at runtime. |
| **Makefile** | Build helper | Shortcuts for Docker tasks (`make up`, `make setup`, etc.). | Replaces long Docker commands with memorable aliases. |
| **public/** | Web root | The actual web-server-accessible directory (contains `index.php`, assets, etc.). | Like `/dist` in JS frameworks or `/public_html`. |
| **src/** | Source code | Shopware’s core application source. | Where the main PHP codebase lives; not usually edited in a project clone. |
| **symfony.lock** | Symfony dependency snapshot | Records Symfony recipes applied during setup. | Used internally by Symfony Flex; no manual editing. |
| **var/** | Runtime data | Cache, logs, temporary files. | Can safely be deleted (Shopware rebuilds it). |
| **vendor/** | Dependency code | All installed PHP libraries from Composer. | Analogous to `node_modules/`. |

You’ll mostly interact with these:

* **Makefile**, which provides convenient shortcuts for common Docker and Shopware commands. It acts as a lightweight wrapper around standard `docker compose` commands. You can still use the underlying Docker commands directly, but it’s recommended to stick with the `make` targets where possible, as they ensure consistent behavior across setups.
* **`custom/`**, to build your own plugins.
* **`bin/console`**, to run Shopware CLI tasks.

Everything else in your project either supports or configures those layers.

## Initial setup [​](#initial-setup)

After creating your project, you still need to install Shopware inside the containers. Run the setup commands below to initialize the database, generate configuration files, and create the default admin user.

First, start the containers:

bash

```shiki
make up
```

This command builds (if needed) and starts all required Docker services (web server, database, Mailpit, etc.) in the background. More details about what each component does:

Components explained (click to expand)

| Name | Type | Purpose |
| --- | --- | --- |
| **Network `my-project_default`** | Docker network | A private virtual network so all containers can communicate (for example, the web container connects to the database). |
| **Volume `my-project_db-data`** | Persistent storage | Stores the MariaDB database files so your data isn’t lost when containers are stopped or rebuilt. |
| **Container `my-project-mailer-1`** | Mailpit service | Captures outgoing emails for local testing. View at <http://localhost:8025>. |
| **Container `my-project-database-1`** | MariaDB service | Runs the Shopware database. Inside the Docker network its host name is `database`. |
| **Container `my-project-web-1`** | PHP + Caddy web service | Runs Shopware itself and serves the storefront and Admin UI at <http://localhost:8000>. |
| **Container `my-project-adminer-1`** | Adminer (DB UI) | Lightweight web interface for viewing and editing your database. Available at <http://localhost:8080>. |

**Tip:** You can check container status anytime with:

bash

```shiki
docker compose ps
```

“Healthy” means the service passed its internal health check and is ready to use.

Once the containers are running, you can install Shopware in one of two ways:

* **Browser installer**: open <http://localhost:8000> to walk through the installation wizard.
* **CLI**: run the following command to perform a quick, non-interactive setup:

bash

```shiki
make setup
```

Both methods install Shopware and prepare your environment. The CLI setup automatically creates the database and an admin user with username `admin`, password `shopware`.

INFO

If you are installing inside the Docker containers (the default when using `make up` and `make setup`), set the database host to `database`. This is the internal service name of the MariaDB container on the Docker network. Inside the containers, `localhost` would refer only to the container itself, not to the database.

If you connect to the database from your host machine (for example, via Adminer or a local MySQL client), use 127.0.0.1 or `localhost` and the exposed port shown in `docker compose ps`.

Access key explained (click to expand)

During setup, you’ll see an output similar to this:

bash

```shiki
Access tokens:
+------------+----------------------------+
| Key | Value |
+------------+----------------------------+
| Access key | `string of capital letters` |
```

This access key is automatically generated for your default Sales Channel (usually *Storefront*). It's used for authenticating requests to the [Store API](./../../../concepts/api/store-api.html)—for example, when fetching product or category data from an external app, headless storefront, or API client.

Example usage:

bash

```shiki
curl -H "sw-access-key: YOUR_ACCESS_KEY" \
     http://localhost:8000/store-api/product
```

You can view or regenerate this key later in the Admin under Sales Channels → [Your Channel] → API Access.

INFO

The access key is not for logging in to the Admin. It’s for programmatic access to your storefront’s data via the Store API.

If you want to stop the setup, run `make stop`.

To start it again, use `make up`.

To stop and remove all containers, run:

bash

```shiki
make down
```

This command removes all containers and associated networks.

If you also want to remove all data and volumes (for example, to perform a full reset of your environment), run:

bash

```shiki
docker compose down -v
```

The `-v` flag will delete the containers, networks, and volumes, meaning all stored data will be lost.

### Known issue on Linux hosts [​](#known-issue-on-linux-hosts)

If you are using Docker on Linux, your host user id (UID) must be **1000** for file permissions to work correctly inside the containers. You can check your user ID with:

bash

```shiki
id -u
```

If it’s not `1000`, you may encounter permission errors when running `make up` or writing to project files.

## Development [​](#development)

To run Shopware CLI commands, first open a shell inside the web container:

bash

```shiki
make shell
```

This command drops you into the container’s terminal (you’ll see the prompt change). From there, you can execute any Shopware CLI command using `bin/console`. For example, to clear the application cache (not required right now):

bash

```shiki
docker compose exec web bin/console cache:clear
```

**Tip**: When you’re inside the container, you only need `bin/console …`. If you prefer to run commands from your host machine instead, use the full Docker prefix: `docker compose exec web bin/console cache:clear`.

You’ll use the following Makefile commands later on, when you modify frontend or admin code, or develop plugins that affect the UI:

bash

```shiki
# Build the administration (admin panel)
make build-administration

# Build the storefront (shop frontend)
make build-storefront

# Start a watcher to rebuild the Administration automatically when files change
make watch-admin

# Start a watcher for Storefront
make watch-storefront
```

These will become part of your everyday development workflow.

## Verify your installation in the browser (optional) [​](#verify-your-installation-in-the-browser-optional)

Now that Shopware is installed, you can confirm the storefront is working by visiting <http://localhost:8000>.

Shopware’s CLI setup automatically installs a complete, preconfigured demo storefront with sample products and categories. It includes local, disposable demo data so you can explore features or test plugins immediately.

You can also check out the Shopware Admin dashboard to verify that the Admin is accessible:

* Log in to the **Admin** at <http://localhost:8000/admin> using `admin / shopware` (default credentials).
* Once logged in, you’ll see the Shopware Admin dashboard and merchant setup wizard.

As a developer, you can skip the wizard and use the Admin to:

* confirm your installation and database are running correctly.
* manage extensions or themes you install later.
* inspect system settings and logs.
* verify that changes from your code (for example, new entities or configuration options) appear in the UI.

## Services [​](#services)

With Shopware running, here are the services in your local stack and how to access them. Understanding what each one does helps you troubleshoot issues and connect external tools if needed:

* **Web service (Caddy + PHP-FPM by default, or Nginx + PHP-FPM)**: serves both the storefront and the admin interface. The default image uses Caddy; you can choose Nginx in image variations.
* Storefront: <http://localhost:8000>
* Admin: <http://localhost:8000/admin> *(default credentials: `admin` / `shopware`)*
* **Database (MariaDB)**: runs on port **3306** inside Docker. The internal hostname is `database`. You can connect from your host using `localhost:3306` if you want to inspect the database directly.
* **Mailpit**: local mail testing tool, available at <http://localhost:8025>. Use this to view emails sent by Shopware (e.g., registration or order confirmations) without needing an external mail server.

### Changing environment variables [​](#changing-environment-variables)

You can create a `.env` file in the project root to override default environment variables. Changes take effect automatically without restarting containers **except for** the `APP_ENV` variable, which requires:

bash

```shiki
make up
```

This command restarts the containers so that the updated environment variable takes effect.

## Production environments [​](#production-environments)

If you're preparing to run Shopware in production using Docker, [this page](./../../hosting/installation-updates/docker.html) covers production images, environment configuration, and deployment workflows.

## Detailed configurations [​](#detailed-configurations)

You can find more detailed configurations for your docker setup in the [Additional Docker Options](./docker-options.html) article.

---

## Devenv

**Source:** https://developer.shopware.com/docs/guides/installation/setups/devenv.html

# Devenv [​](#devenv)

[Devenv](https://devenv.sh) is a Nix-based tool for defining and managing fully reproducible development environments for local workstations or continuous integration (CI) systems. It works like a dependency manager for your entire development stack.

Instead of manually installing and configuring PHP, Node.js, MySQL, Redis, or other services, you describe your setup once in a `devenv.nix` file. Devenv then installs and runs the exact versions you specify, ensuring consistency across every developer’s machine.

Devenv lets you choose specific versions of binaries (e.g., PHP, Node, or npm) and configure and run services like MySQL, Redis, or OpenSearch. All binaries and service states are stored on a per-project basis, providing an isolated yet native development environment.

Unlike Docker or virtual machines, Devenv does not use containerization or virtualization. Instead, all services and binaries run natively on your host system. This makes it an appealing choice for Shopware core contributors or advanced users who want consistent local and CI builds.

## Required on your host [​](#required-on-your-host)

Devenv provides project-local PHP, Node, Composer, and services via Nix, so you don't need to install those runtimes globally for a project that uses Devenv.

On the host you only need a minimal toolchain:

* [Nix package manager](https://nixos.org/download.html)
* Git
* Optional: Docker Engine, only if you plan to run additional containerized services alongside Devenv

See the [Shopware 6 requirements](./../requirements.html) for general system requirements and supported versions. Devenv will provide the exact runtime versions per project.

> **Note:** If you previously installed Nix using an older single-user script or via a package manager (for example, `brew install nix`), remove it first to prevent permission or path conflicts. Removing `/nix` deletes the global Nix store and may require elevated privileges. Use `sudo` if appropriate and double-check before running destructive commands.

## Installation [​](#installation)

### Nix [​](#nix)

Devenv is built on top of [Nix](https://nixos.org/), so you need to [install it](https://nixos.org/download.html) first. The Nix community recommends using the cross-platform [Determinate Systems installer](https://determinate.systems/posts/determinate-nix-installer), which provides a fast, consistent setup across macOS, Linux, and WSL2 that requires no manual configuration:

bash

```shiki
curl -L https://install.determinate.systems/nix | sh -s -- install
```

This installs Nix in multi-user mode and automatically configures your shell. If you prefer, you can still use the [official Nix installer](https://nixos.org/download.html), but it may require additional manual steps, such as updating your shell profile or enabling the Nix daemon.

For CI pipelines, Docker images, or other non-interactive environments, you can skip the Determinate Systems installer and invoke Nix directly using `nix-shell` or [Nix Flakes](https://nixos.wiki/wiki/Flakes). Use `nix-shell` for a simple, one-off environment defined by a `shell.nix` file. Use Nix Flakes for more reproducible builds and shared dependency management across systems or teams.

After installation, restart your terminal to load Nix’s environment variables automatically. Alternatively, to avoid restarting, you can load Nix manually in your current shell session:

bash

```shiki
# Load Nix into your current shell session

. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

The Determinate Systems installer also handles shell integration, including Zsh and [Oh My Zsh](https://ohmyz.sh/), so you don't need to manually copy Nix configuration lines into your shell startup files.

WARNING

If you have previously installed Nix using an older single-user script or via a package manager (for example, `brew install nix`), remove it first to prevent permission or path conflicts:

bash

```shiki
rm -rf ~/.nix-profile ~/.nix-defexpr ~/.nix-channels ~/.local/state/nix
rm -rf /nix
```

Removing `/nix` deletes the global Nix store and may require elevated privileges. Only run these commands if you intend to completely remove previous Nix installations.

If Nix commands aren’t available after installation, restart your terminal or run `source ~/.zshrc`.

### Install Devenv [​](#install-devenv)

Once Nix is installed, install or update Devenv with the Nix profile command:

bash

```shiki
nix profile install github:cachix/devenv/latest
```

You can find the full installation guide and advanced options in the [official Devenv documentation](https://devenv.sh/getting-started/).

## Quick checks (verify host & Devenv) [​](#quick-checks-verify-host-devenv)

Run these to confirm your host environment is ready:

bash

```shiki
# Nix installed and on PATH
nix --version

# Devenv installed and available
devenv --version
which devenv

# Direnv (optional)
direnv --version || echo "direnv not installed"

# Basic sanity: list Devenv commands
devenv help

# Check few common ports (macOS / Linux examples)
lsof -i :8000 -i :3306 -i :6379 || ss -tulpn | grep ':8000\|:3306\|:6379'
```

### Shopware [​](#shopware)

Depending on your goals, you can either create a new Shopware project using the production template or contribute to the Shopware core, which already includes a `devenv.nix` file.

Once your project includes a `devenv.nix` file, you can start the environment:

bash

```shiki
devenv up
```

WARNING

Before starting Devenv, ensure that common service ports (e.g., `8000`, `3306`, `6379`) are not already in use. If they are, Devenv will fail to start the corresponding services.

Check for active services:

## Configure your database connection (optional) [​](#configure-your-database-connection-optional)

Verify your `.env` file points to the correct database:

bash

```shiki
# <PROJECT_ROOT>/.env
DATABASE_URL="mysql://shopware:shopware@127.0.0.1:3306/shopware?sslmode=disable&charset=utf8mb4"
```

If you changed your MySQL port or user in `devenv.local.nix`, update these values here as well.

## Launch Devenv and install Shopware [​](#launch-devenv-and-install-shopware)

Start Devenv in the project directory:

bash

```shiki
devenv up
```

Then open a *new terminal* and enter the Devenv shell, which provides PHP, Composer, Node.js, npm, etc.:

bash

```shiki
devenv shell
```

Inside the Devenv shell, install Shopware:

bash

```shiki
bin/console system:install --basic-setup --create-database --force
```

Once installation completes, open `http://localhost:8000/admin` in your browser. You should see the Shopware Admin interface.

The default credentials are:

* User: `admin`
* Password: `shopware`

INFO

On Windows with WSL2, change the default sales channel domain to `http://localhost:8000`. Use *http*, not https.

To create a full test setup with demo data, run:

bash

```shiki
composer setup && APP_ENV=prod bin/console framework:demodata && APP_ENV=prod bin/console dal:refresh:index
```

If installation completes without schema creation, run `bin/console database:migrate`.

### Direnv (optional) [​](#direnv-optional)

[Direnv](https://direnv.net/) makes it easier to work with multiple Devenv projects by automatically activating the correct environment when you enter a project directory. It's optional but recommended for a smoother workflow.

With Direnv, you don’t have to run `devenv shell` manually every time you use the binaries. The environment loads automatically.

You still need to start the services once with `devenv up`.

First, install Direnv:

Add the Direnv hook to your shell configuration file:

After configuring your shell, reload it or restart your terminal.

### First use [​](#first-use)

When you enter a Devenv project directory for the first time, allow Direnv to load the environment:

bash

```shiki
direnv allow
```

If you change the Devenv configuration or your `.envrc` file after running `direnv allow`, reload the environment with:

bash

```shiki
direnv reload
```

Direnv will now automatically activate the Devenv environment whenever you enter the directory.

See the official [Automatic Shell Activation guide](https://devenv.sh/automatic-shell-activation/) for more details.

## Default services [​](#default-services)

When you start Devenv with `devenv up`, Shopware automatically provides several core services. You can access them using the following addresses:

| Service | Default address | Description |
| --- | --- | --- |
| MySQL | `mysql://shopware:shopware@127.0.0.1:3306` | Primary database for Shopware. |
| Mailhog (SMTP) | `smtp://127.0.0.1:1025` | Local mail capture for testing email. |
| Redis (TCP) | `tcp://127.0.0.1:6379` | Used for caching and sessions. |
| Caddy | `http://127.0.0.1:8000` | Web server. |
| Adminer | `http://127.0.0.1:9080` | Database management tool. |

TIP

The MySQL service listens on port `3306` and stores its data in `<PROJECT_ROOT>/.devenv/state/mysql`. Use `127.0.0.1` instead of `localhost` when connecting to MySQL.

### Redis [​](#redis)

Redis is used for caching and sessions and runs on `tcp://127.0.0.1:6379`.

If Redis fails to start with an error such as `Failed to configure LOCALE for invalid locale name`, set a valid locale before starting Devenv:

bash

```shiki
export LANG=en_US.UTF-8
```

### Caddy [​](#caddy)

[Caddy](https://caddyserver.com/) is an open-source web server written in Go with automatic HTTPS. It serves your local Shopware instance by default at <http://127.0.0.1:8000>.

### Adminer [​](#adminer)

[Adminer](https://www.adminer.org/) is a full-featured, lightweight database management tool written in PHP. You can use it to view and manage your Shopware database: <http://127.0.0.1:9080>.

Default credentials:

* User: `shopware`
* Password: `shopware`

### Mailhog [​](#mailhog)

[MailHog](https://github.com/mailhog/MailHog) is an email testing tool that intercepts outgoing messages so you can preview them in your browser: <http://localhost:8025>.

## Customize your setup [​](#customize-your-setup)

You can customize the predefined Devenv services to match your local needs—for example, changing virtual hosts, database names, or environment variables. You can override defaults to match your local dev setup, e.g., to free ports or change domains.

To override or extend the defaults, create a `devenv.local.nix` file in your project root. This file lets you disable built-in services, adjust configuration, or add new ones that your project requires.

After editing `devenv.local.nix`, reload your environment to apply the changes.

Example:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 # Disable a service
 services.adminer.enable = false;

 # Use a custom virtual host
 services.caddy.virtualHosts."http://shopware.swag" = {
 extraConfig = ''
 root * public
 php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
 file_server
 '';
 };

 # Customize nodejs version
 languages.javascript = {
 package = pkgs.nodejs-18_x;
 };

 # Override an environment variable
 env.APP_URL = "http://shopware.swag:YOUR_CADDY_PORT";
}
```

For a full list of all available services and their configuration options, refer to the official [Devenv documentation](https://devenv.sh/reference/options/).

If you're not using [Direnv](#direnv-optional), remember to reload the environment manually after changing any `*.nix` file:

bash

```shiki
exit
devenv shell
```

All binaries installed by Devenv are located in `<PROJECT_ROOT>/.devenv/profile/bin`.

You can search for available packages on [NixOS package search](https://search.nixos.org/packages).

This comes in handy if you want to configure interpreters in your IDE.

WARNING

Do not commit service tokens or credentials to version control. Store secrets in `.env` or a secret manager.

## Detailed configurations [​](#detailed-configurations)

You can find more detailed configurations for your devenv setup in the [Additional Devenv Options](./devenv-options.html) article.

---

## Symfony CLI

**Source:** https://developer.shopware.com/docs/guides/installation/setups/symfony-cli.html

# Symfony CLI Setup [​](#symfony-cli-setup)

Symfony CLI lets you run Shopware 6 locally without Docker. It's a lightweight option that uses your system’s PHP, Composer, and Node.js installations.

Shopware recommends [Docker](./docker.html) as the default setup for most users because it mirrors production and includes all services out of the box. However, if you already have PHP and a database installed locally, or want a faster, low-overhead workflow, Symfony CLI is a solid alternative.

## Prerequisites [​](#prerequisites)

Before you begin, make sure your system meets the [Shopware 6 requirements](./../requirements.html). You’ll need the following tools installed on your host machine:

* [Symfony CLI](https://symfony.com/download)
* PHP 8.2 or higher with the required extensions; see the [Requirements page](./../requirements.html) for the complete list
* [Composer 2.x](https://getcomposer.org/)
* [Node.js 20+](https://nodejs.org/en/download) and npm
* A running MySQL 8 or MariaDB 11 database (local or remote)

You’ll also need a working web server. The Symfony CLI can provide one automatically for development.

> **macOS note:** If you installed PHP via Homebrew, make sure the `intl` extension is enabled: `brew install php-intl` then verify with `php -m | grep intl`.

Optional tools:

* [Elasticsearch 8](https://www.elastic.co/elasticsearch/) for product search and indexing
* Docker (for running only the database while keeping PHP local)

## Create a New Project [​](#create-a-new-project)

Run this command to create a new Shopware production project:

bash

```shiki
composer create-project shopware/production <project-name>

# or specify a version
composer create-project shopware/production:6.6.10.0 <project-name>
```

During project creation, Symfony Flex asks whether you want to use Docker. Choose **Yes** if you want to run the database in a container, or **No** to use a local MySQL/MariaDB server.

For more details, see the [Shopware Production template documentation](./../template.html).

## Configure database connection [​](#configure-database-connection)

After creating the project, define your database settings in a `.env.local` file in the project root:

dotenv

```shiki
DATABASE_URL=mysql://username:password@localhost:3306/dbname
```

You can define other environment settings (like `APP_URL`, `MAILER_DSN`, or `SHOPWARE_ES_HOSTS`) in `.env.local` as needed.

Git ignores `.env.local`, so you can safely define machine-specific settings here without affecting your team’s shared configuration.

### Using Docker for the database (optional) [​](#using-docker-for-the-database-optional)

Running the database in a Docker container helps keep your local system clean and ensures version consistency with production environments. If you prefer this instead of installing MySQL or MariaDB locally, start Docker with:

bash

```shiki
docker compose up -d
```

This command starts the database container in the background.

To stop and remove the containers, while preserving the database data, run:

bash

```shiki
docker compose down
```

Run `docker compose down -v` to remove the containers and delete all stored data volumes.

INFO

Tip - Use the `-v` flag only if you want to completely reset the database.

## Install Shopware [​](#install-shopware)

INFO

Always prefix commands with `symfony` to ensure the correct PHP version and configuration are used. Skipping this can cause issues such as using the wrong PHP binary or failing to connect to the Docker-based MySQL database.

Run the following command to install Shopware:

bash

```shiki
symfony console system:install --basic-setup
```

The `--basic-setup` flag initializes Shopware with sensible defaults. It automatically creates a database schema, an admin user, and a default sales channel for the specified `APP_URL` so you can start testing immediately without manual configuration. Optional: Add the `--create-database` flag if your database doesn’t already exist.

If you encounter file-permission issues when installing or rebuilding caches, run `symfony console cache:clear` or check directory ownership.

### Default Administration credentials [​](#default-administration-credentials)

Shopware creates a default Administration user during installation:

| Username | Password |
| --- | --- |
| `admin` | `shopware` |

**Tip**: Change these credentials after installation for security.

## Start the webserver [​](#start-the-webserver)

The Symfony local web server automatically uses the correct PHP version, reads your `.env` configuration, and exposes HTTPS by default. This makes it more reliable than the built-in PHP server for local development.

Start the local web server with:

bash

```shiki
symfony server:start
```

By default, this starts the server on port `8000`. Access the Shopware Administration at <http://localhost:8000/admin> and the Storefront at <http://localhost:8000>.

To run the server in the background, add the `-d` flag:

bash

```shiki
symfony server:start -d
```

This frees up your terminal for other commands.

### Stopping the Web Server [​](#stopping-the-web-server)

To stop the server and all running processes, run:

bash

```shiki
symfony server:stop
```

**Tip**: If port 8000 is already in use, start the server on a different port: `symfony server:start --port=8080`

## Set the PHP version (optional, recommended) [​](#set-the-php-version-optional-recommended)

Specify a PHP version to ensure consistent environments across team members.

To change the PHP version used by Symfony CLI, create a `.php-version` file in the project root and specify the desired version. For example, to use PHP 8.3, create `.php-version` and add:

dotenv

```shiki
8.3
```

Symfony CLI will now use PHP 8.3 for all commands in this project. Commit this file to your version control system so everyone on your team uses the same PHP version.

To verify which PHP version is active, run:

bash

```shiki
symfony php -v
```

## Adjust PHP configuration (Optional) [​](#adjust-php-configuration-optional)

Adjusting PHP settings like `memory_limit` or `max_execution_time` can prevent build or cache warm-up processes from failing, especially during large Administration builds or when working on plugins.

You can override PHP settings for this project by adding a `php.ini` file in the project root. For example, to increase the `memory_limit` to 512 MB, add:

ini

```shiki
memory_limit = 512M
```

To confirm your configuration, run:

bash

```shiki
symfony php -i
```

By keeping your `php.ini` in version control, you ensure consistent behavior across development environments and CI pipelines.

Symfony CLI uses PHP’s built-in web server by default. For better performance, you can configure it to use Nginx or Caddy: see the [web server reference](./../../../resources/references/config-reference/server/nginx.html).

## Build and Watch the Administration and Storefront (Optional) [​](#build-and-watch-the-administration-and-storefront-optional)

You only need to run this step if you’re developing or customizing the frontend (Administration or Storefront). It compiles JavaScript and CSS assets so your changes are visible immediately.

[Project Template](../template#building-watching-administration-and-storefront)

---

## Additional Docker Options

**Source:** https://developer.shopware.com/docs/guides/installation/setups/docker-options.html

# Additional Docker Options [​](#additional-docker-options)

## Connecting to a remote database [​](#connecting-to-a-remote-database)

If you want to use a database outside the Docker stack (running on your host or another server, for examples), set `DATABASE_URL` in `.env.local` in the standard form:

bash

```shiki
DATABASE_URL="mysql://user:password@<host>:3306/<database>"
```

Note: containers cannot always reach services bound only to the host's `localhost`. If `localhost` does not work you can try `host.docker.internal`, your host machine’s LAN IP, or add an `extra_hosts` entry in `compose.yaml`.

## Enable profiler/debugging for PHP [​](#enable-profiler-debugging-for-php)

Once your Shopware environment is running, you may want to enable PHP debugging or profiling to inspect code execution, set breakpoints, or measure performance. The default setup doesn’t include these tools, but you can enable them using Docker overrides.

### Enable Xdebug [​](#enable-xdebug)

To enable [Xdebug](https://xdebug.org/) inside the web container, create a `compose.override.yaml` in your project root with the following configuration:

yaml

```shiki
services:
    web:
        environment:
            - XDEBUG_MODE=debug
            - XDEBUG_CONFIG=client_host=host.docker.internal
            - PHP_PROFILER=xdebug
```

After saving the file, apply the changes:

bash

```shiki
docker compose up -d
```

This restarts the containers with Xdebug enabled. You can now attach your IDE (for example, PHPStorm or VS Code) to the remote debugger on the default Xdebug port `9003`.

Shopware’s Docker setup also supports other profilers, like [Blackfire](https://www.blackfire.io/), [Tideways](https://tideways.com/), and [PCOV](https://github.com/krakjoe/pcov). For Tideways and Blackfire, you'll need to run an additional container. For example:

yaml

```shiki
services:
    web:
        environment:
            - PHP_PROFILER=blackfire
    blackfire:
        image: blackfire/blackfire:2
        environment:
            BLACKFIRE_SERVER_ID: XXXX
            BLACKFIRE_SERVER_TOKEN: XXXX
```

## Image variations [​](#image-variations)

The Shopware Docker image is available in several variations, allowing you to match your local setup to your project’s PHP version, Node version, and preferred web server. Use the following pattern to select the right image tag:

`ghcr.io/shopware/docker-dev:php(PHP_VERSION)-node(NODE_VERSION)-(WEBSERVER)`

Here’s the version matrix:

PHP versions:

* `8.4` - PHP 8.4
* `8.3` - PHP 8.3
* `8.2` - PHP 8.2

Node versions:

* `node24` - Node 24
* `node22` - Node 22

Web server:

* `caddy` - Caddy as web server
* `nginx` - Nginx as web server

Example:

* `ghcr.io/shopware/docker-dev:php8.4-node24-caddy` - PHP 8.4, Node 24, Caddy as web server
* `ghcr.io/shopware/docker-dev:php8.3-node24-caddy` - PHP 8.3, Node 24, Caddy as web server
* `ghcr.io/shopware/docker-dev:php8.4-node22-nginx` - PHP 8.4, Node 22, Nginx as web server
* `ghcr.io/shopware/docker-dev:php8.3-node22-nginx` - PHP 8.3, Node 22, Nginx as web server

## Adding Minio for local S3 storage [​](#adding-minio-for-local-s3-storage)

Some projects use Amazon S3 for file storage in production. If you want to mimic that behavior locally—for example, to test uploads or CDN-like delivery—you can add [Minio](https://www.min.io/), an open-source S3-compatible storage server.

### 1. Add the Minio service [​](#_1-add-the-minio-service)

Include a `minio` service in your `compose.yaml`:

yaml

```shiki
services:
  # ....
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      start_period: 20s
      start_interval: 10s
      interval: 1m
      timeout: 20s
      retries: 3
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data

  minio-setup:
    image: minio/mc
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
        set -e;
        mc alias set local http://minio:9000 minioadmin minioadmin;
        mc mb local/shopware-public local/shopware-private --ignore-existing;
        mc anonymous set download local/shopware-public;
        "
    restart: no
  # ...

volumes:
  # ...
  minio-data:
```

### 2. Configure Shopware to use Minio [​](#_2-configure-shopware-to-use-minio)

Create a new YAML file at `config/packages/minio.yaml` with the following content:

yaml

```shiki
# yaml-language-server: $schema=https://raw.githubusercontent.com/shopware/shopware/refs/heads/trunk/config-schema.json

shopware:
  filesystem:
    public: &s3_public
      type: "amazon-s3"
      url: "http://localhost:9000/shopware-public"
      config:
        bucket: shopware-public
        endpoint: http://minio:9000
        use_path_style_endpoint: true
        region: us-east-1
        credentials:
          key: minioadmin
          secret: minioadmin
    theme: *s3_public
    sitemap: *s3_public
    private:
      type: "amazon-s3"
      config:
        bucket: shopware-private
        endpoint: http://minio:9000
        use_path_style_endpoint: true
        region: us-east-1
        credentials:
          key: minioadmin
          secret: minioadmin
```

After adding the Minio service to your `compose.yaml` and creating the configuration file, this will configure Shopware to use Minio as the S3 storage for public and private files.

Run `docker compose up -d` to start the Minio containers. You can access the Minio console at <http://localhost:9001> with the username `minioadmin` and password `minioadmin`.

Finally, regenerate the assets to upload them to S3:

bash

```shiki
make shell
bin/console asset:install
bin/console theme:compile
```

## Using OrbStack routing [​](#using-orbstack-routing)

If you're using [OrbStack](https://orbstack.dev) on macOS, you can take advantage of its built-in routing feature. OrbStack automatically assigns local `.orb.local` URLs to your containers, so you don’t need to manage port mappings manually. This allows running multiple Shopware instances at the same time without port conflicts.

To enable it, create a `compose.override.yaml` in your project root with the following content:

yaml

```shiki
services:
  web:
      ports: !override []
      environment:
          APP_URL: https://web.sw.orb.local
          SYMFONY_TRUSTED_PROXIES: REMOTE_ADDR

###> symfony/mailer ###
  mailer:
    image: axllent/mailpit
    environment:
      MP_SMTP_AUTH_ACCEPT_ANY: 1
      MP_SMTP_AUTH_ALLOW_INSECURE: 1
###< symfony/mailer ###
```

The APP\_URL environment variable follows this pattern: `web.<project-name>.orb.local`. The `<project-folder-name>` comes from your local directory name. For example: a project called `shopware` will have the URL `https://web.shopware.orb.local`. A project called `shopware-6` will have the URL `https://web.shopware-6.orb.local`.

You can also open `https://orb.local` in your browser to view all running containers and their assigned URLs.

## Proxy production images [​](#proxy-production-images)

When you import a production database into your local environment, image URLs in the data may still point to production servers. As a result, your local store might show broken or missing images. You can fix this in two ways:

* **download all production images** and import them locally, or
* **set up a lightweight proxy service** that serves those images directly from the production server (recommended for quick testing).

### 1. Add the image proxy service [​](#_1-add-the-image-proxy-service)

Add a `imageproxy` service to your `compose.override.yaml`:

yaml

```shiki
services:
    imageproxy:
        image: ghcr.io/shopwarelabs/devcontainer/image-proxy
        ports:
          - "8050:80"
        environment:
          # Your production URL.
          REMOTE_SERVER_HOST: shopware.com
```

This starts a proxy server that fetches images from the production environment and caches them locally. For example, a request to `http://localhost:8050/assets/images.png` will be served from `https://[REMOTE_SERVER_HOST]/assets/images.png` and then stored in the local cache for faster reuse.

### 2. Point Shopware to the proxy [​](#_2-point-shopware-to-the-proxy)

Next, we need to configure Shopware to use the proxy server. To do this, create a new YAML file `config/packages/media-proxy.yaml`

yaml

```shiki
shopware:
  filesystem:
    public:
      url: "http://localhost:8050"
```

This tells Shopware to use the proxy server URL for all images.

---

## Additional Devenv Options

**Source:** https://developer.shopware.com/docs/guides/installation/setups/devenv-options.html

# Additional Devenv Options [​](#additional-devenv-options)

## Enable Blackfire [​](#enable-blackfire)

To enable [Blackfire](https://blackfire.io/) profiling in your Devenv setup, add the following configuration to your `devenv.local.nix` file:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.blackfire.enable = true;
 services.blackfire.server-id = "<SERVER_ID>";
 services.blackfire.server-token = "<SERVER_TOKEN>";
 services.blackfire.client-id = "<CLIENT_ID>";
 services.blackfire.client-token = "<CLIENT_TOKEN>";
}
```

## Enable XDebug [​](#enable-xdebug)

To enable [Xdebug](https://xdebug.org/) for debugging or profiling, add the following configuration to your `devenv.local.nix` file:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 # XDebug
 languages.php.extensions = [ "xdebug" ];
 languages.php.ini = ''
 xdebug.mode = debug
 xdebug.discover_client_host = 1
 xdebug.client_host = 127.0.0.1
 '';
}
```

After modifying your `devenv.local.nix` file, reload your environment.

## Use MariaDB instead of MySQL [​](#use-mariadb-instead-of-mysql)

To switch from MySQL to [MariaDB](https://mariadb.org/), update your `devenv.local.nix` file:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.mysql.package = pkgs.mariadb;
}
```

## Use a custom MySQL port [​](#use-a-custom-mysql-port)

You can change the default MySQL port if it conflicts with another service on your system:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.mysql.settings = {
 mysqld = {
 port = 33881;
 };
 };

}
```

After any change, run `devenv reload` to apply updates.

## Customize Caddy ports or virtual hosts [​](#customize-caddy-ports-or-virtual-hosts)

You can adjust the Caddy web server configuration to use a different port or virtual host.

## Use a custom Adminer port [​](#use-a-custom-adminer-port)

If you need to change the default Adminer port (for example, to avoid conflicts with another service), update your `devenv.local.nix` file:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 services.adminer.listen = "127.0.0.1:9084";
}
```

After modifying `devenv.local.nix`, reload your environment.

## Use Varnish [​](#use-varnish)

You can integrate [Varnish](https://varnish-cache.org/) into your local Shopware development setup to test reverse caching behavior. The following example shows how to configure Caddy and Varnish in your `devenv.local.nix` file:

nix

```shiki
# <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
 # caddy config
 services.caddy = {
 enable = true;

 # all traffic to localhost is redirected to varnish
 virtualHosts."http://localhost" = {
 extraConfig = ''
 reverse_proxy 127.0.0.1:6081 {
 # header_up solves this issue: https://discord.com/channels/1308047705309708348/1309107911175176217
 header_up Host sw.localhost
 }
 '';
 };

 # the actual shopware application is served from sw.localhost,
 # choose any domain you want.
 # you may need to add the domain to /etc/hosts:
 # 127.0.0.1       sw.localhost
 virtualHosts."http://sw.localhost" = {
 extraConfig = ''
 # set header to avoid CORS errors
 header {
 Access-Control-Allow-Origin *
 Access-Control-Allow-Credentials true
 Access-Control-Allow-Methods *
 Access-Control-Allow-Headers *
 defer
 }
 root * public
 php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
 encode zstd gzip
 file_server
 log {
 output stderr
 format console
 level ERROR
 }
 '';
 };
 };

 # varnish config
 services.varnish = {
 enable = true;
 package = pkgs.varnish;
 listen = "127.0.0.1:6081";
 # enables xkey module
 extraModules = [ pkgs.varnishPackages.modules ];
 # it's a slightly adjusted version from the [docs](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#configure-varnish)
 vcl = ''
 # ...
 # Specify your app nodes here. Use round-robin balancing to add more than one.
 backend default {
 .host = "sw.localhost";
 .port = "80";
 }
 # ...
 # ACL for purgers IP. (This needs to contain app server ips)
 acl purgers {
 "sw.localhost";
 "127.0.0.1";
 "localhost";
 "::1";
 }
 # ...
 '';
 };
}
```

After updating your `devenv.local.nix`, reload your development environment to apply the changes:

bash

```shiki
devenv reload
```

## Use an older package version [​](#use-an-older-package-version)

Sometimes, you may want to pin a service to an older version to, for example, ensure compatibility with legacy components or reproduce a previous environment state.

Here are examples showing how to use older versions of MySQL and RabbitMQ in your `devenv.local.nix` configuration:

**Example: Use a specific MySQL version**:

nix

```shiki
{
 services.mysql = let
 mysql8033 = pkgs.mysql80.overrideAttrs (oldAttrs: {
 version = "8.0.33";
 # the final url would look like this: https://github.com/mysql/mysql-server/archive/mysql-8.0.33.tar.gz
 # make sure the url exists.
 # alternatively you could use that url directly via pkgs.fetchurl { url = "xyz"; hash="xyz";};
 # for reference see the [different fetchers](https://ryantm.github.io/nixpkgs/builders/fetchers/#chap-pkgs-fetchers)
 src = pkgs.fetchFromGitHub {
 owner = "mysql";
 repo = "mysql-server";
 rev = "mysql-8.0.33";
 # leave empty on the first run, you will get prompted with the expected hash
 sha256 = "sha256-s4llspXB+rCsGLEtI4WJiPYvtnWiKx51oAgxlg/lATg=";
 };
 });
 in
 {
 enable = true;
 package = mysql8033; # use the overridden package
 # ...
 };
}
```

**Example**: Use a specific RabbitMQ version:

nix

```shiki
{
 services.rabbitmq = let
 rabbitmq3137 = pkgs.rabbitmq-server.overrideAttrs (oldAttrs: {
 version = "3.13.7";
 src = pkgs.fetchurl {
 url = "https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.13.7/rabbitmq-server-3.13.7.tar.xz";
 sha256 = "sha256-GDUyYudwhQSLrFXO21W3fwmH2tl2STF9gSuZsb3GZh0=";
 };
 });
 in
 {
 enable = true;
 package = rabbitmq3137; # use the overridden package
 };
}
```

Pinning versions may increase build time; use only when necessary.

## Maintenance [​](#maintenance)

Run `devenv gc` periodically to remove unused packages, services, and caches. This helps free disk space and keeps your environment clean.

Use `devenv down` to stop services first. If processes remain, as a last resort terminate them manually:

bash

```shiki
kill $(ps -ax | grep /nix/store | grep -v "grep" | awk '{print $1}')
```

If you can’t access <http://127.0.0.1:8000> in your browser, try <http://localhost:8000> instead. This issue is common when using WSL2 on Windows.

On macOS or Linux, the app should be available at <http://127.0.0.1:8000>.

---

## Requirements

**Source:** https://developer.shopware.com/docs/guides/installation/requirements.html

# Requirements [​](#requirements)

This page lists the system requirements and supported software versions for developing Shopware 6. Find installation steps for each setup method on their respective pages:

* [Docker setup](./setups/docker.html); recommended for most users
* [Devenv setup](./setups/devenv.html)
* [Symfony CLI](./setups/symfony-cli.html)

## Requirements for all setups [​](#requirements-for-all-setups)

Before setting up your Shopware 6 development environment, make sure your system is ready. Check these basics before installation:

* You’re using a Unix-based system (macOS or Linux), or Windows with WSL 2 or Docker for full compatibility
* You have admin/root privileges (if required in your organization)
* [Git](https://git-scm.com/) installed and available in your `PATH`
* You have at least 8 GB RAM (16 GB recommended) and 10 GB free disk space
* Docker Desktop, PHP, or Nix are not already bound to conflicting ports
* You have a reliable Internet connection for dependency downloads

## Hardware recommendations [​](#hardware-recommendations)

These recommendations ensure smooth local development regardless of setup:

| Component | Recommended |
| --- | --- |
| **CPU** | Quad-core or higher |
| **Memory (RAM)** | 8 GB minimum, 16 GB recommended (especially for Docker) |
| **Disk space** | ~10 GB free for Shopware + services |
| **Operating system** | macOS 13+, Windows 10/11 (Pro with WSL 2), or Linux (64-bit) |

## Permissions and networking [​](#permissions-and-networking)

* Ensure Docker or Symfony CLI has permission to bind to local ports (typically:80 or:8080).
* Allow your system’s firewall to let containers or local web servers communicate internally.
* On Linux, you may need to add your user to the `docker` group:

bash

```shiki
sudo usermod -aG docker $USER
```

## Recommended stack and supported versions [​](#recommended-stack-and-supported-versions)

The following versions and configurations are officially supported for Shopware 6 development:

| Component | Install | Minimum Version | Recommended | Required / Notes |
| --- | --- | --- | --- | --- |
| **PHP** | [PHP installation guide](https://www.php.net/manual/en/install.php) [Composer installation guide](https://getcomposer.org/download/) | 8.2+ | 8.4 | **Required.** `memory_limit ≥ 512M`, `max_execution_time ≥ 30s`. Required extensions: `ctype`, `curl`, `dom`, `fileinfo`, `gd`, `iconv`, `intl`, `mbstring`, `openssl`, `pcre`, `pdo_mysql`, `phar`, `simplexml`, `xml`, `zip`, `zlib`. Optional: `amqp` (for message queues). Composer 2.2+ recommended. **macOS note:** If you install PHP with Homebrew, the `intl` extension may not be included by default. Install it separately: `brew install php-intl` then verify with `php -m |
| **SQL** | [MariaDB installation guide](https://mariadb.com/kb/en/getting-installing-and-upgrading-mariadb/) [MySQL installation guide](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/) | MariaDB ≥ 10.11.6 or MySQL ≥ 8.0.22 | MariaDB 11.4 / MySQL 8.4 | **Required.** `max_allowed_packet ≥ 32M` for optimal performance. |
| **Node.js / npm** | [Node.js downloads](https://nodejs.org/en/download) | Node 20.0.0+ | Node 24 / npm 10 | **Required.** |
| **Search** | [OpenSearch installation guide](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/) | OpenSearch 1.0+ or ElasticSearch 7.8+ | OpenSearch 2.17.1 | **Optional.** Used for product search and indexing.   **Note**: The search preview in the administration requires OpenSearch 2.12+ or Elasticsearch 8.8+.   Support for OpenSearch 3.1 was added in shopware v6.7.3.1 |
| **Cache / KV store** | [Valkey](https://valkey.io/) [Redis](https://redis.io) / [Redict](https://redict.io) / [Dragonfly](https://www.dragonflydb.io) | Redis v7+ | Valkey 8.0 | **Optional.** Used for caching and session storage. Redis-protocol compatible alternatives supported. `maxmemory-policy: volatile-lfu`. |
| **Web server** | [Caddy setup guide](https://developer.shopware.com/docs/resources/references/config-reference/server/caddy.html) [Apache](https://developer.shopware.com/docs/resources/references/config-reference/server/apache.html) [Nginx](https://developer.shopware.com/docs/resources/references/config-reference/server/nginx.html) | Any | Caddy | **Required.** For local development, the [Symfony CLI server](https://symfony.com/doc/current/setup/symfony_cli.html) works out of the box. |
| **Queue** | [RabbitMQ downloads](https://www.rabbitmq.com/download.html) [AWS SQS](https://aws.amazon.com/sqs/) | Any transport supported by the [symfony messenger component](https://symfony.com/doc/current/messenger.html#transport-configuration) | RabbitMQ | **Optional.** By default the SQL database will be used as a queue, however in production setups it is highly recommended to use a dedicated queue system for scalability and observability reasons. |

See also: [PHP performance tweaks guide](https://developer.shopware.com/docs/guides/hosting/performance/performance-tweaks.html#php-config-tweaks)

## Verifying your local environment [​](#verifying-your-local-environment)

Use the following commands to verify your local environment:

INFO

On many systems or hosting environments, multiple PHP versions may be installed. Make sure to use the correct PHP binary, as CLI and FPM often have different `php.ini` files. Ask your hosting provider for the correct PHP binary and how to adjust `php.ini`.

* `php -v`: Show CLI PHP version
* `php -m`: List CLI PHP modules
* `php -i | grep memory_limit`: Show your CLI PHP memory limit
* `composer -V`: Show Composer version
* `node -v`: Show Node version
* `npm -v`: Show npm version

## Next steps [​](#next-steps)

Once your environment meets these requirements, proceed to your preferred installation method:

* [Docker setup](./setups/docker.html)
* [Symfony CLI setup](./setups/symfony-cli.html)
* [Devenv setup](./setups/devenv.html)

---

## Project Template

**Source:** https://developer.shopware.com/docs/guides/installation/template.html

# Project Template [​](#project-template)

The Shopware project template is a Composer project that can be used as a starting point for new Shopware Projects, or if you want to develop extensions or themes for Shopware.

Each official setup option—[Docker](./setups/docker.html), [Symfony CLI](./setups/symfony-cli.html), and [Devenv](./setups/devenv.html)—builds upon this project template, either directly or via a pre-configured environment. See [Installation Overview](./) for a comparison of setup options.

## Alternative: Using the installer package [​](#alternative-using-the-installer-package)

If you have downloaded the [shopware-installer.phar package](https://www.shopware.com/en/download/) instead of using Composer, skip the `composer create-project` step and follow the remaining instructions from the [Project Template](https://developer.shopware.com/docs/guides/installation/template.html) guide.

This method is equivalent to creating a project using Composer but is suited for environments where Composer is not available (for example, shared hosting or limited enterprise servers).

## Set up a new project [​](#set-up-a-new-project)

To create a new Shopware project, run the following command:

bash

```shiki
composer create-project shopware/production <project-name>

# or install a specific version
composer create-project shopware/production:6.6.10.5 <project-name>
```

INFO

Composer `create-project` clones the latest tag from the [Template repository](https://github.com/shopware/template) and installs the dependencies. If you don't have Composer installed, you could also clone the repository itself and run `composer install` in Docker to proceed with the installation.

This creates a new project in the `<project-name>` directory.

The template contains all Shopware bundles like `shopware/administration`, `shopware/storefront` and `shopware/elasticsearch`. If you don't need any, then you can uninstall them with:

bash

```shiki
composer remove shopware/<bundle-name>
```

## Installation [​](#installation)

After you have created the project, you have automatically a `.env` file in your project root. This file contains all the environment variables you need to run Shopware.

If you want to adjust a variable, you should put the variable in a `.env.local` file. This file will override the variables in the `.env` file.

INFO

The `.env` will be overwritten when the Shopware Web Installer is used for Shopware updates, so it's highly recommended to use a `.env.local` file.

After you have adjusted the `.env` file, you can run the following command to install Shopware:

bash

```shiki
bin/console system:install --basic-setup
```

The flag `--basic-setup` will automatically create an admin user and a default sales channel for the given `APP_URL`. If you haven't created a MySQL Database yet, you can pass the `--create-database` flag to create a new database.

The Shopware's default Administration credentials are:

| Username | Password |
| --- | --- |
| `admin` | `shopware` |

Change these credentials after finishing the installation.

### Optional packages [​](#optional-packages)

The template is small and does not contain any dev-tooling or integrations like PaaS or Fastly. You can easily add them to your project with the following commands:

bash

```shiki
# Install profiler and other dev tools, eg Faker for demo data generation
composer require --dev shopware/dev-tools

# Or Install symfony dev tools
composer require --dev symfony/profiler-pack

# Install PaaS integration
composer require paas --ignore-platform-req=ext-amqp

# Install Fastly integration
composer require fastly
```

### Add Shopware packagist [​](#add-shopware-packagist)

Using Shopware Packagist, you can manage all your Shopware Store plugins directly in the `composer.json`. Refer to ["Using Composer for plugin installation in Shopware"](https://www.shopware.com/en/news/using-composer-for-plugin-installation-in-shopware/) blog post for detailed information.

## Building/watching Administration and Storefront [​](#building-watching-administration-and-storefront)

The created project contains Bash scripts in `bin/` folder to build and watch the Administration and Storefront. You can run the following commands:

bash

```shiki
./bin/build-administration.sh
./bin/build-storefront.sh
./bin/watch-administration.sh
./bin/watch-storefront.sh
```

Use these scripts to build the Administration and Storefront. The `watch` commands will watch for changes in the Administration and Storefront and rebuild them automatically.

## Update Shopware [​](#update-shopware)

There are two ways to update Shopware:

* Initially run `bin/console system:update:prepare` to enable the maintenance mode and then update all Composer packages using `composer update --no-scripts`. The `--no-scripts` flag instructs composer to not run any scripts that may reference Shopware CLI commands. They will only be functional after updating the recipes. To disable the maintenance mode, run `bin/console system:update:finish`.
* To force-update all config files, run `composer recipes:update`.

## Migrate from the old zip installation to a new project template [​](#migrate-from-the-old-zip-installation-to-a-new-project-template)

Before Shopware 6.5, we provided a zip file for installation. The zip file contained all dependencies required to run Shopware. This method has been deprecated and replaced with a Composer project template. The Composer project template is way more flexible and allows you to manage extensions together with Shopware itself using Composer.

To migrate from the old zip installation to the new Composer project template, you can use `shopware-cli project autofix flex` command to migrate it automatically, or you can do it manually by following the steps below.

### 1. Backup [​](#_1-backup)

Start with a clean git state, stash everything, or make a backup of your files.

### 2. Adjust root composer.json [​](#_2-adjust-root-composer-json)

First, adjust your root `composer.json`. Add the following lines to your `composer.json`:

json

```shiki
"extra": {
    "symfony": {
        "allow-contrib": true,
        "endpoint": [
            "https://raw.githubusercontent.com/shopware/recipes/flex/main/index.json",
            "flex://defaults"
        ]
    }
}
```

Next, replace all the existing scripts with the following:

json

```shiki
"scripts": {
    "auto-scripts": [],
    "post-install-cmd": [
        "@auto-scripts"
    ],
    "post-update-cmd": [
        "@auto-scripts"
    ]
}
```

Finally, remove the fixed platform as it will now be determined by the required packages.

diff

```shiki
"config": {
    "optimize-autoloader": true,
-    "platform": {
-        "php": "7.4.3"
-    },
    "sort-packages": true,
    "allow-plugins": {
        "composer/package-versions-deprecated": true
    }
},
```

### 3. Cleanup the template [​](#_3-cleanup-the-template)

After having installed the new Composer packages, you can clean up the template by removing the following files:

bash

```shiki
rm -r .dockerignore \
    .editorconfig \
    .env.dist \
    .github \
    .gitlab-ci \
    .gitlab-ci.yml \
    Dockerfile \
    docker-compose.yml \
    easy-coding-standard.php \
    PLATFORM_COMMIT_SHA \
    artifacts \
    bin/deleted_files_vendor.sh \
    bin/entrypoint.sh \
    bin/package.sh \
    config/etc \
    src \
    config/secrets \
    config/services \
    config/services.xml \
    config/services_test.xml \
    license.txt \
    phpstan.neon \
    phpunit.xml.dist \
    psalm.xml

touch .env
```

### 4. Install required Composer packages [​](#_4-install-required-composer-packages)

To install Symfony Flex, you need to have Composer installed. If you don't have Composer installed, please follow the [official documentation](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos).

To install Symfony Flex, you need to run the following commands and allow both new Composer plugins.

bash

```shiki
composer require "symfony/flex:*" "symfony/runtime:*"

composer recipe:install --force --reset
```

### 5. Review changes [​](#_5-review-changes)

Review the changes and commit them to your Git repository. All upcoming config changes can be applied with `composer recipes:update`.

You may need to adjust some environment variables as the names have changed:

| **Old name** | **New name** |
| --- | --- |
| MAILER\_URL | MAILER\_DSN |
| SHOPWARE\_ES\_HOSTS | OPENSEARCH\_URL |

## Known issues [​](#known-issues)

### `APP_ENV=dev` web\_profiler missing extension error [​](#app-env-dev-web-profiler-missing-extension-error)

Prior to Shopware 6.4.17.0, you have to install the Profiler bundle to get `APP_ENV=dev` working with:

bash

```shiki
composer require --dev profiler
```

### framework:demo-data is missing faker classes [​](#framework-demo-data-is-missing-faker-classes)

Prior to Shopware 6.4.17.0, you have to install some packages to get `framework:demo-data` command working:

bash

```shiki
composer require --dev mbezhanov/faker-provider-collection maltyxx/images-generator
```

---

