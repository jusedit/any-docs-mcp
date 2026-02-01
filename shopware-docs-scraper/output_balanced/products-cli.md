# Products Cli

*Scraped from Shopware Developer Documentation*

---

## Shopware CLI

**Source:** https://developer.shopware.com/docs/products/cli/

# Shopware CLI [​](#shopware-cli)

[Shopware CLI](https://github.com/shopware/shopware-cli) is the open-source command-line interface for working with Shopware 6. It's a standalone developer tool that you [install](./installation/) and configure separately from your Shopware instance. Once set up, it helps you automate and speed up common tasks such as:

* managing and configuring Shopware projects
* building, validating, and packaging extensions
* uploading and maintaining extensions in the Shopware Store
* running CI/CD pipelines for Shopware-based solutions

Shopware CLI runs on macOS, Linux, and via Docker. For system-level requirements (PHP, DB, memory, etc.) see the [General Requirements](./../guides/requirements/).

**Supported platforms (short):** macOS (Homebrew), Debian/Ubuntu (APT), other Linux via RPM or manual installation, and Docker. Windows users should use WSL 2 or Docker. (See full [installation](./installation.html) page for Windows details.)

## Quickstart [​](#quickstart)

Select your environment to install or try out the CLI:

**Binary & releases:** Prebuilt packages and archives are published at [shopware/shopware-cli · Releases](https://github.com/shopware/shopware-cli/releases).

## Overview [​](#overview)

Shopware CLI is organized into three main command scopes that cover the most common development and maintenance workflows:

* Project commands: interact with your Shopware project (e.g., build, dump DB, or sync configuration)
* Extension commands: build and validate Shopware extensions
* Store commands: publish or update extensions in the Shopware Store

## Automatic refactoring [​](#automatic-refactoring)

Shopware CLI also includes an automatic refactoring tool for PHP, JavaScript, and Admin Twig files. It uses:

* [Rector](https://getrector.org/) for PHP
* [ESLint](https://eslint.org/) for JavaScript
* Custom rules for Admin Twig

You can run it on an extension or a full project:

bash

```shiki
# Example: refactor an extension
shopware-cli extension fix /path/to/your/extension

# Example: refactor an entire project
shopware-cli project fix /path/to/your/project
```

Always back up or version your code before running refactoring commands, as they will modify files in place. [Learn more here](./automatic-refactoring/).

### Project commands [​](#project-commands)

Work directly with your [Shopware project](./deployment/) to automate setup and maintenance tasks. Available commands include:

bash

```shiki
shopware-cli project create         # Create a new Shopware 6 project
shopware-cli project dump       # Dumps the Shopware database
shopware-cli project ci          # Build Shopware in the CI
```

### Extension commands [​](#extension-commands)

Create, build, and validate Shopware [extensions](./plugins/) and prepare them for the [Store](https://store.shopware.com/de/) or distribution. Available commands include:

bash

```shiki
shopware-cli extension fix   # Fix an extension
shopware-cli extension build    # Builds assets for extensions
shopware-cli extension validate         # Validate an extension
```

### Store commands [​](#store-commands)

Publish and manage your extensions in the [Store](https://store.shopware.com/de/), with commands such as:

bash

```shiki
shopware-cli store login # Login to Shopware Store portal.store
shopware-cli token: Manage tokens for Store authentication
```

Run any command with `--help` to see its available options. Example: `shopware-cli extension --help`

---

## Other Installation Options

**Source:** https://developer.shopware.com/docs/products/cli/installation.html

# Other Installation Options [​](#other-installation-options)

If you haven’t already, see the [Shopware CLI overview](./) for a quick start and the most common installation methods (Homebrew, APT, and Docker). This page covers additional or advanced options for other package managers, CI/CD environments, or building from source.

## Package-manager installs [​](#package-manager-installs)

Shopware CLI is available through several community and distribution channels.

**Fedora, CentOS, openSUSE, RHEL (YUM/DNF)**

bash

```shiki
curl -1sLf \
  'https://dl.cloudsmith.io/public/friendsofshopware/stable/setup.rpm.sh' \
  | sudo -E bash
sudo dnf install shopware-cli
```

**Arch Linux (AUR)**

bash

```shiki
yay -S shopware-cli-bin
```

**Nix / NUR packages**

bash

```shiki
nix profile install nixpkgs#shopware-cli
# or latest from FriendsOfShopware
nix profile install github:FriendsOfShopware/nur-packages#shopware-cli
```

**Devenv (Nix-based)**

Update `devenv.yaml` with:

yaml

```shiki
inputs:
  nixpkgs:
    url: github:NixOS/nixpkgs/nixpkgs-unstable
  froshpkgs:
    url: github:FriendsOfShopware/nur-packages
    inputs:
      nixpkgs:
        follows: "nixpkgs"
```

Then reference the input in `devenv.nix`:

nix

```shiki
{ pkgs, inputs, ... }: {
  packages = [
    inputs.froshpkgs.packages.${pkgs.system}.shopware-cli
  ];
}
```

## Manual installation from releases [​](#manual-installation-from-releases)

Download the appropriate .deb, .rpm, or .apk file from the [GitHub Releases page](https://github.com/shopware/shopware-cli/releases) and install it manually:

bash

```shiki
sudo dpkg -i shopware-cli_<version>_linux_amd64.deb   # Debian/Ubuntu
sudo rpm -i shopware-cli_<version>_linux_arm64.rpm    # Fedora/RHEL
sudo apk add shopware-cli-<version>.apk               # Alpine
```

Alternatively, download the binary and move it into your `$PATH`:

bash

```shiki
curl -L -o shopware-cli https://github.com/shopware/shopware-cli/releases/latest/download/shopware-cli-linux-amd64
chmod +x shopware-cli
sudo mv shopware-cli /usr/local/bin/
```

## CI/CD and development environments [​](#ci-cd-and-development-environments)

These options let you use the CLI automatically in hosted environments. The [main page](./) lists Docker and GitHub Actions, which are popular.

**GitHub Codespaces**

json

```shiki
{
    "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
    "features": {
        "ghcr.io/shyim/devcontainers-features/shopware-cli:latest": {}
    }
}
```

**GitLab CI**

yaml

```shiki
build:
  stage: build
  image:
    name: ghcr.io/shopware/shopware-cli:latest
    entrypoint: [ "/bin/sh", "-c" ]
  script:
    - shopware-cli --version
```

**ddev integration**

Add a file `.ddev/web-build/Dockerfile.shopware-cli`

Dockerfile

```shiki
# .ddev/web-build/Dockerfile.shopware-cli
COPY --from=ghcr.io/shopware/shopware-cli:bin /shopware-cli /usr/local/bin/shopware-cli
```

### Docker image [​](#docker-image)

To copy the binary in your Docker image, add the following line:

Dockerfile

```shiki
# Dockerfile
COPY --from=ghcr.io/shopware/shopware-cli:bin /shopware-cli /usr/local/bin/shopware-cli
```

## Add binary manually [​](#add-binary-manually)

Download the pre-compiled binaries from the [releases](https://github.com/shopware/shopware-cli/releases) page and copy them to the desired location.

## Running with Docker [​](#running-with-docker)

You can also use it within a Docker container. To do that, you will need to execute something more or less like the examples below.

Registries:

* [ghcr.io/shopware/shopware-cli](https://github.com/shopware/shopware-cli/pkgs/container/shopware-cli)

Example usage: Build assets of an extension

bash

```shiki
docker run \
    --rm \
    -v $(pwd):$(pwd) \
    -w $(pwd) \
    -u $(id -u) \
    ghcr.io/shopware/shopware-cli \
    extension build FroshPlatformAdminer
```

## Building from source [​](#building-from-source)

If you prefer to compile the CLI yourself (requires Go 1.20+ and Git):

bash

```shiki
git clone https://github.com/shopware/shopware-cli
cd shopware-cli

go mod tidy

go build -o shopware-cli .

./shopware-cli --version
```

---

## Building extensions and creating archives

**Source:** https://developer.shopware.com/docs/products/cli/extension-commands/build.html

# Building extensions and creating archives [​](#building-extensions-and-creating-archives)

Extensions consist of PHP Changes, JavaScript and CSS. To release an extension to the Shopware Store or upload it to a Shopware 6 instance without having to rebuild Storefront and Administration, your extension needs to provide the compiled assets.

## Building an extension [​](#building-an-extension)

Shopware CLI allows you to easily build the assets of an extension. To build an extension, you can use the following command:

bash

```shiki
shopware-cli extension build <path>
```

Shopware CLI reads the `shopware/core` requirement from `composer.json` or `manifest.xml` and builds the assets using the lowest compatible Shopware version. This ensures the extension remains usable across multiple Shopware versions. If the selected version is incorrect, you can override it using a `.shopware-extension.yml` file.

yaml

```shiki
# .shopware-extension.yml
build:
  shopwareVersionConstraint: '6.6.9.0'
```

This only affects the build process and not on the installation of the extension. For full control you can also specify the environment variable `SHOPWARE_PROJECT_ROOT` pointing to a Shopware 6 project, and it will use that Shopware to build the extension assets.

## Additional bundles [​](#additional-bundles)

If your plugin consists of multiple bundles, usually when you have implemented `getAdditionalBundles` in your `Plugin` class, you have to provide the path to the bundle you want to build in the config:

yaml

```shiki
# .shopware-extension.yml
build:
  extraBundles:
    # Assumes the bundle name is the same as the directory name
    - path: src/Foo
    # Explicitly specify the bundle name
    - path: src/Foo
      name: Foo
```

## Extension as bundle [​](#extension-as-bundle)

If your extension is not a plugin but itself a bundle, make sure your composer type is `shopware-bundle` and that you have set a `shopware-bundle-name` in the `extra` part of the composer definition like this:

json

```shiki
{
    "name": "my-vendor/my-bundle",
    "type": "shopware-bundle",
    "extra": {
        "shopware-bundle-name": "MyBundle"
    }
}
```

Now you can use `shopware-cli extension build <path>` to build the assets and distribute them together with your bundle. Also `shopware-cli project ci` detects know automatically this bundle and builds the assets for it.

## Using `esbuild` for JavaScript bundling [​](#using-esbuild-for-javascript-bundling)

WARNING

Building with esbuild works completely standalone without the Shopware codebase. This means if you import files from Shopware, you have to copy it to your extension.

Esbuild can be used for JavaScript bundling, offering a significantly faster alternative to the standard Shopware bundling process, as it eliminates the need to involve Shopware for asset building.

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    assets:
      # Use esbuild for Administration
      enable_es_build_for_admin: true
      # Use esbuild for Storefront
      enable_es_build_for_storefront: true
```

## Creating an archive [​](#creating-an-archive)

To create an archive of an extension, you can use the following command:

bash

```shiki
shopware-cli extension zip <path>
```

The command copies the extension to a temporary directory, builds the assets, deletes unnecessary files and creates a zip archive of the extension. The archive is placed in the current working directory.

**By default, the command picks the latest released git tag**, use the `--disable-git` flag to disable this behavior and use the current source code. Besides disabling it completely, you can also specify a specific tag or commit using `--git-commit`.

### Bundling composer dependencies [​](#bundling-composer-dependencies)

Before Shopware 6.5, bundling the composer dependencies into the zip file is required. Shopware CLI automatically runs `composer install` and removes duplicate composer dependencies to avoid conflicts.

To disable this behavior, you can adjust the configuration:

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    composer:
      enabled: false
```

This is automatically disabled for plugins targeting Shopware 6.5 and above and `executeComposerCommands` should be used instead.

### Delete files before zipping [​](#delete-files-before-zipping)

Shopware CLI deletes a lot of known files before zipping the extension. If you want to delete more files, you can adjust the configuration:

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    pack:
      excludes:
        paths:
          - <path>
```

### JavaScript build optimization [​](#javascript-build-optimization)

If you bring additional NPM packages, make sure that you added only runtime dependencies to `dependencies` inside `package.json` and tooling to `devDependencies` and enabled `npm_strict` in the configuration:

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    assets:
      npm_strict: true
```

This skips unnecessary `npm install` and `npm ci` commands and only installs the runtime dependencies.

### Checksums [​](#checksums)

When creating an archive using `shopware-cli extension zip`, a `checksum.json` file is automatically generated. This file contains checksums for all files in the extension, which can be used to verify the integrity of the extension after installation.

If you want to exclude certain files or paths from the checksum calculation, you can configure this in your `.shopware-extension.yml` file:

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    checksum:
      ignore:
        - <path>
        - <another_path>
```

For example, to exclude the `src/Resources/config/services.xml` file from checksum calculation:

yaml

```shiki
# .shopware-extension.yml
build:
  zip:
    checksum:
      ignore:
        - src/Resources/config/services.xml
```

To verify the checksum of installed extensions, you can use the [FroshTools](https://github.com/FriendsOfShopware/FroshTools#froshextensionchecksumcheck---check-extension-file-integrity) plugin which provides a checksum verification feature for all extensions.

### Release mode [​](#release-mode)

If you are building an archive for distribution, you can enable the release mode with the flag `--release`. This will remove the App secret from the `manifest.xml` and generate changelog files if enabled.

The changelog generation can be enabled with the configuration:

yaml

```shiki
# .shopware-extension.yml
changelog:
  enabled: true
```

It generates the changelog by utilizing the commits between the last tag and the current commit. Additionally, it can be configured to filter commits and build the changelog differently.

yaml

```shiki
changelog:
  enabled: true
  # only the commits matching to this regex will be used
  pattern: '^NEXT-\d+'
  # variables allow extracting metadata out of the commit message
  variables:
    ticket: '^(NEXT-\d+)\s'
  # go template for the changelog, it loops over all commits
  template: |
    {{range .Commits}}- [{{ .Message }}](https://issues.shopware.com/issues/{{ .Variables.ticket }})
    {{end}}
```

This example checks that all commits in the changelog needs to start with `NEXT-` in the beginning. The `variables` section allows extracting metadata out of the commit message. The `template` is a go template which loops over all commits and generates the changelog. With the combination of `pattern`, `variables` and `template` we link the commit message to the Shopware ticket system.

### Overwrites [​](#overwrites)

Extension configuration can be overwritten during the zipping process, allowing changes to aspects such as the version and app-related settings.

Replaces the version in `composer.json` or `manifest.xml` with the given version:

yaml

```shiki
shopware-cli extension zip --overwrite-version=1.0.0 <path>
```

Replaces all external URLs in `manifest.xml` to that given URL:

yaml

```shiki
shopware-cli extension zip --overwrite-app-backend-url=https://example.com <path>
```

Replaces the App secret in `manifest.xml` with the given secret:

yaml

```shiki
shopware-cli extension zip --overwrite-app-backend-secret=MySecret <path>
```

---

## Standalone Admin Watcher

**Source:** https://developer.shopware.com/docs/products/cli/extension-commands/admin-watcher.html

# Standalone Admin Watcher [​](#standalone-admin-watcher)

INFO

`shopware-cli extension admin-watch` can be different to the regular Admin Watcher. You can start the regular Admin Watcher with `shopware-cli project admin-watch`

Shopware CLI has an integrated Standalone Admin Watcher. This is useful if the regular Admin Watcher struggles with the number of installed extensions, and you only want to watch one single extension. The Standalone Watcher works by using the regular build Administration and injects only the changed files of the extension.

Therefore, the Watcher starts in few milliseconds and is very fast. Additionally, it can be targeted to an external Shopware 6 Instance to debug JavaScript or CSS changes with the external data.

## Starting the standalone Admin Watcher [​](#starting-the-standalone-admin-watcher)

To start the standalone Admin Watcher, you can use the following command:

bash

```shiki
shopware-cli extension admin-watch <path-to-extension> <url-to-shopware>
```

The first parameter is the **path to extension** you want to watch and the last parameter is the URL to the Shopware 6 instance. The URL must be reachable from the machine where the CLI is executed. You can watch also multiple extensions by providing multiple paths, but the last parameter must be the URL to the Shopware 6 instance.

You can also pass **path of a Shopware project** to the command. In this case, the CLI will automatically detect the extensions.

The listing port of the Admin Watcher can be changed with `--listen :<port>`.

## Usage behind a proxy [​](#usage-behind-a-proxy)

If you want to use the Standalone Admin Watcher behind a proxy, for example, SSL, you should set `--external-url` to the URL where the Admin Watcher will be reachable in the Browser.

---

## Extracting Meta Data

**Source:** https://developer.shopware.com/docs/products/cli/extension-commands/extract-meta-data.html

# Extracting Meta Data [​](#extracting-meta-data)

There are helpers in Shopware CLI to extract data of an extension. This is useful in your CI/CD pipeline to get the extension version or the changelog for the automated release.

## Extracting the version [​](#extracting-the-version)

To extract the version of an extension, you can use the following command:

bash

```shiki
shopware-cli extension get-version <path>
```

The path can be absolute or relative to the current working directory. The command will output the version of the extension.

## Extracting the changelog [​](#extracting-the-changelog)

To extract the changelog of an extension, you can use the following command:

bash

```shiki
shopware-cli extension get-changelog <path>
```

The path can be absolute or relative to the current working directory. The command will output the changelog of the extension.

It will output always the English changelog.

---

## Configuration

**Source:** https://developer.shopware.com/docs/products/cli/extension-commands/configuration.html

# Configuration [​](#configuration)

Many configurations can be changed using a `.shopware-extension.yml` file in the root of your extension.

Here is an example of a `.shopware-extension.yml` file:

yaml

```shiki
build:
  extraBundles:
    - path: src/Foo
    - name: OverrideName
      path: src/Override
  shopwareVersionConstraint: '~6.6.0'
  zip:
    assets:
      enabled: false
      before_hooks: []
      after_hooks: []
      disable_sass: false
      enable_es_build_for_admin: false
      enable_es_build_for_storefront: false
      npm_strict: false

changelog:
  enabled: true

store:
  automatic_bugfix_version_compatibility: true
  # ...

validation:
  ignore:
    - 'xx'
```

When you edit that file in an editor, you will get autocompletion and hints for the available options.

## Environment variables [​](#environment-variables)

Additionally, you can set environment variables to change the behavior of the CLI. The following environment variables are available:

| Environment Variable | Description |
| --- | --- |
| CI | Detect CI environment |
| SHOPWARE\_CLI\_PREVIOUS\_TAG | Override previous Git tag detection with a previous tag used for Changelog generation |
| CI\_PROJECT\_URL | GitLab CI project URL used for Changelog generation |
| SHOPWARE\_CLI\_NO\_SYMFONY\_CLI | Disable Symfony CLI usage |
| APP\_ENV | Application environment |
| SHOPWARE\_PROJECT\_ROOT | Use this Shopware project to build the extension instead of setting up a new project |
| SHOPWARE\_CLI\_DISABLE\_WASM\_CACHE | Disable the WASM cache for PHP linting |

---

## Generating MySQL dumps

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/mysql-dump.html

# Generating MySQL dumps [​](#generating-mysql-dumps)

Shopware CLI has built-in support for generating MySQL dumps. The dump command is native implementation and does not use existing tools like `mysqldump`.

Creating a MySQL dump is as simple as running the following command:

bash

```shiki
shopware-cli project dump
```

This will create a `dump.sql` in the current directory. The dump command will use the database credentials from the `.env` file. If you want to use different credentials, you can use the following flags:

bash

```shiki
shopware-cli project dump --host 127.0.0.1 --username root --password root --database sw6
```

It is possible to use `--skip-lock-tables` to skip the lock tables command. This is useful for large databases or when the MySQL user has no rights to lock the table.

## Compressing the dump [​](#compressing-the-dump)

Database dumps can be pretty large, it is possible to compress the dump using `gzip` or `zstd`. Use flag `--compression=gzip` for gzip compression or `--compression=zstd` for zstd compression.

## Table locking [​](#table-locking)

By default, Shopware CLI will try to lock the table before dumping the data. This can fail if the MySQL user has no rights to lock the table. To skip the lock tables command, use the `--skip-lock-tables` flag.

## Anonymizing data [​](#anonymizing-data)

The `--anonymize` flag will anonymize known user data tables. The following tables are anonymized:

[See here for the complete list](https://github.com/shopware/shopware-cli/blob/main/cmd/project/project_dump.go#L74)

It is possible to customize the anonymization process by using the `dump.rewrite` configuration in the `shopware-cli.yml` file.

yaml

```shiki
# .shopware-project.yml
dump:
  rewrite:
    <table-name>:
      # Rewrite column content to new value
      <column-name>: "'new-value'"
      # Use go-faker to generate data
      <column-name>: "faker.Internet().Email()" # See https://github.com/jaswdr/faker for all available functions
```

## Ignoring table content [​](#ignoring-table-content)

Some tables are not relevant for dumps, like log tables. To ignore some default tables, use the `--clean` flag. This will ignore the content of the following tables:

* `cart`
* `customer_recovery`
* `dead_message`
* `enqueue`
* `messenger_messages`
* `increment`
* `elasticsearch_index_task`
* `log_entry`
* `message_queue_stats`
* `notification`
* `payment_token`
* `refresh_token`
* `version`
* `version_commit`
* `version_commit_data`
* `webhook_event_log`

To ignore additional tables, use the `dump.ignore` configuration in the `shopware-project.yml` file.

yaml

```shiki
# .shopware-project.yml
dump:
  nodata:
    - <table-name>
```

## Ignoring entire tables [​](#ignoring-entire-tables)

It is also possible to completely ignore a table **not only the content**.

yaml

```shiki
# .shopware-project.yml
dump:
  ignore:
    - <table-name>
```

## Adding a where clause [​](#adding-a-where-clause)

It is possible to add a where clause to the export of a table. So only rows matching the where clause will be exported.

yaml

```shiki
# .shopware-project.yml
dump:
  where:
    <table-name>: 'id > 5'
```

---

## Build a complete Project

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/build.html

# Build a complete Project [​](#build-a-complete-project)

Usually, when you want to deploy your project, you have to run `composer install` and compile the assets of the project. Shopware CLI provides a single command which does all of this for you.

WARNING

This command modifies the given directory and deletes files. Make sure you have committed all your changes before running this command.

bash

```shiki
shopware-cli project ci <path>
```

## What does it do? [​](#what-does-it-do)

* It runs `composer install` (by default, only installs the production dependencies, use `--with-dev-dependencies` to install the dev dependencies as well)
* Looks for missing assets of extensions and only compiles the missing assets to speed up the build process
* Deletes unnecessary files like `node_modules` and many more to save disk space
* Deletes source code of compiled assets to save disk space
* Merges snippets of extensions to speed up Administration

## Using private Composer repositories [​](#using-private-composer-repositories)

If you want to use `packages.shopware.com` as a private Composer repository, make sure you have set `SHOPWARE_PACKAGES_TOKEN` environment variable to your Composer token. This can be found in your Shopware Account.

For other private Composer repositories, you can use the `auth.json` file in the root of your project or set `COMPOSER_AUTH` environment variable with the content of the `auth.json` file.

For more information, see the [Composer documentation](https://getcomposer.org/doc/articles/authentication-for-private-packages.md).

## Reducing JavaScript in Storefront [​](#reducing-javascript-in-storefront)

Shopware's default `browserlist` still supports older browsers like Internet Explorer 11. If you want to reduce JavaScript polyfill and CSS prefixes, you can adjust the `browserlist` configuration in the `.shopware-project.yml` file.

yaml

```shiki
build:
  # Browserlist configuration for Storefront
  browserslist: 'defaults'
```

You can check [here which browsers would be affected](https://browsersl.ist/#q=defaults).

## MJML Email Template Compilation [​](#mjml-email-template-compilation)

Starting with Shopware CLI 0.6.32, the `project ci` command can compile MJML email templates during the build process for projects using the [FroshPlatformTemplateMail](https://github.com/FriendsOfShopware/FroshPlatformTemplateMail) plugin. [MJML](https://mjml.io) is a markup language designed to reduce the pain of coding responsive emails by providing semantic components that compile to responsive HTML.

### Prerequisites [​](#prerequisites)

This feature is specifically designed for projects using the **FroshPlatformTemplateMail** plugin. The primary purpose of this plugin is to manage email templates as source files in your codebase, rather than storing them in the database. This approach enables:

* **Version control**: Email templates can be tracked in Git alongside your code
* **Deployment consistency**: Templates are deployed with your code, ensuring consistency across environments
* **MJML support**: Optionally write templates in MJML (Mailjet Markup Language) format for responsive emails
* **Build-time compilation**: Since templates are in source files, they can be compiled during the build process

Having email templates in source files is essential for the shopware-cli MJML compilation feature to work, as it processes these files during the build phase.

### Why compile MJML during build-time? [​](#why-compile-mjml-during-build-time)

By default, FroshPlatformTemplateMail compiles MJML templates at runtime when emails are sent. The shopware-cli build-time compilation offers several advantages:

* **Early error detection**: Catch MJML syntax errors during CI/CD instead of when sending emails
* **Better performance**: Eliminate runtime compilation overhead
* **Improved reliability**: Remove potential runtime failures in production
* **Reduced dependencies**: No need for MJML compilation services in production

### Configuration [​](#configuration)

Enable MJML compilation in your `.shopware-project.yml` file:

yaml

```shiki
build:
  mjml:
    # Enable MJML compilation during build-time
    enabled: true
    # Directories to search for MJML templates (defaults to custom/plugins and custom/static-plugins if not specified)
    searchPaths:
      - custom/plugins
      - custom/static-plugins
```

### How it works [​](#how-it-works)

When MJML compilation is enabled:

1. The CLI searches for `html.mjml` files in the configured search paths (defaults to `custom/plugins` and `custom/static-plugins`)
2. Each `html.mjml` file is compiled to HTML and saved as `html.twig`
3. The original `html.mjml` files are removed after successful compilation to prevent runtime re-compilation attempts
4. Any compilation errors are reported and cause the build to fail, ensuring broken templates don't reach production

### Requirements [​](#requirements)

MJML compilation requires the `mjml` package to be installed via NPM in your build environment. The CLI uses local compilation to convert MJML templates to HTML.

## Configuration options [​](#configuration-options)

You can configure the build process with a `.shopware-project.yml` file. The following options are available:

yaml

```shiki
build:
  # Browserlist configuration for Storefront
  browserslist: 'defaults'
  # Paths that should be deleted
  cleanup_paths:
    - 'node_modules'
  # At the end of the process, bin/console asset:install is executed, this can be disabled here
  disable_asset_copy: false
  # Exclude the following extensions from the build process
  exclude_extensions:
    - 'SwagExample'
  # Keep the extension Administration and Storefront source code
  keep_extension_source: false
  # Keep the source maps of the compiled assets
  keep_source_maps: false
  # Delete after bin/console asset:install all assets in the extensions, so only live in public folder.
  # This only works when the assets are served directly from the public folder.
  remove_extension_assets: false
  # Allows to force building an extension even when the assets existing. A use-case could be if you used composer patches for a specific extension.
  force_extension_build:
    - name: 'SomePlugin'
  # MJML compilation configuration (see the MJML section above for details)
  mjml:
    enabled: false
    searchPaths:
      - custom/plugins
      - custom/static-plugins
```

## Supporting bundles [​](#supporting-bundles)

Shopware CLI automatically detects plugins and Apps. Custom bundles (classes that extend bundle class from Shopware) cannot be automatically detected as Shopware CLI does not execute any PHP code. Therefore, you need to add the path of the custom bundle to your project `composer.json`:

json

```shiki
{
    "extra": {
        "shopware-bundles": {
            // The key is the relative path from project root to the bundle
            "src/MyBundle": {}
        }
    }
}
```

If your bundle folder name does not match your bundle name, you can use the `name` key to map the folder to the bundle name.

json

```shiki
{
    "extra": {
        "shopware-bundles": {
            "src/MyBundle": {
                "name": "MyFancyBundle"
            }
        }
    }
}
```

### Bundle packaged in own composer package [​](#bundle-packaged-in-own-composer-package)

If your bundle is an own composer package, make sure your composer type is `shopware-bundle` and that you have set a `shopware-bundle-name` in the extra part of the config like this:

json

```shiki
{
    "name": "my-vendor/my-bundle",
    "type": "shopware-bundle",
    "extra": {
        "shopware-bundle-name": "MyBundle"
    }
}
```

With this Composer type, `shopware-cli extension build` also works for your bundle, if you want to distribute compiled assets.

## Example Docker Image [​](#example-docker-image)

This is an example Dockerfile that builds a Shopware project and copies the source code to the `/var/www/html` folder.

dockerfile

```shiki
#syntax=docker/dockerfile:1.4

# pin versions
FROM ghcr.io/shopware/docker-base:8.3 AS base-image
FROM ghcr.io/shopware/shopware-cli:latest-php-8.3 AS shopware-cli

# build

FROM shopware-cli AS build

ARG SHOPWARE_PACKAGES_TOKEN

ADD . /src
WORKDIR /src

RUN --mount=type=secret,id=composer_auth,dst=/src/auth.json \
    --mount=type=cache,target=/root/.composer \
    --mount=type=cache,target=/root/.npm \
    /usr/local/bin/entrypoint.sh shopware-cli project ci /src

FROM base-image

COPY --from=build --chown=82 --link /src /var/www/html
```

Besides Docker, it is also a perfect fit for any deployment variant.

---

## Remote Extension Management

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/remote-extension-managment.html

# Remote extension management [​](#remote-extension-management)

Shopware CLI has an extension manager to install and manage extensions in your Shopware project through the Shopware API like the Extension Manager in the Shopware 6 Administration panel, but for the CLI.

INFO

This functionality was designed for Shopware SaaS and should not be used for self-hosted installations. [The recommendation is to use the Deployment Helper and install all plugins via Composer](./../../../guides/hosting/installation-updates/deployments/deployment-helper.html)

To use the extension manager, you need a `.shopware-project.yml` or set environment variables. See here for more information about the [Fixture Bundle](./../../../resources/tooling/fixture-bundle/).

WARNING

Make sure you log in using your username and password to the CLI. The extension API can be used **only by users**.

## Commands [​](#commands)

### List all extensions [​](#list-all-extensions)

bash

```shiki
shopware-cli project extension list
```

### Install an extension [​](#install-an-extension)

bash

```shiki
shopware-cli project extension install <extension-name>
```

### Uninstall an extension [​](#uninstall-an-extension)

bash

```shiki
shopware-cli project extension uninstall <extension-name>
```

### Update an extension [​](#update-an-extension)

bash

```shiki
shopware-cli project extension update <extension-name>
```

### Outdated extensions [​](#outdated-extensions)

Shows all extensions that have an update available.

bash

```shiki
shopware-cli project extension outdated
```

### Upload extension [​](#upload-extension)

Uploads an extension to the Shopware instance.

bash

```shiki
shopware-cli project extension upload <path-to-extension-zip>
```

### Delete extension [​](#delete-extension)

Deletes an extension from the Shopware instance.

bash

```shiki
shopware-cli project extension delete <extension-name>
```

---

## Helper Commands

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/helper-commands.html

# Helper Commands [​](#helper-commands)

This is a curated list of helper commands that are useful for your daily work with Shopware CLI in your Shopware project.

## Create a new project [​](#create-a-new-project)

To create a new project, you can use the following command:

bash

```shiki
shopware-cli project create <folder-name>
```

It will ask you for the Shopware version. You can pass the version as second parameter:

bash

```shiki
shopware-cli project create <folder-name> <version>
```

The version parameter can be also `latest` for the latest stable version or `dev-trunk` for the latest development version.

## Replacements to include in shell scripts [​](#replacements-to-include-in-shell-scripts)

Shopware CLI contains replacements for `bin/build-administration.sh` and `bin/build-storefront.sh`.

| Shell Script | Shopware Command |
| --- | --- |
| bin/build-storefront.sh | `shopware-cli project storefront-build` |
| bin/build-administration.sh | `shopware-cli project admin-build` |
| bin/watch-storefront.sh | `shopware-cli project storefront-watch` |
| bin/watch-administration.sh | `shopware-cli project admin-watch` |

Additionally to the replacement, Shopware CLI allows only watching a specific set of extensions or exclude few.

To only watch specific:

bash

```shiki
shopware-cli project admin-watch --only-extensions <name>,<second>....
```

To exclude specific:

bash

```shiki
shopware-cli project admin-watch --skip-extensions <name>,<second>....
```

### Building only custom extensions [​](#building-only-custom-extensions)

When working with a lot of 3rd party extensions, `project storefront-build` and `project admin-build` would become slow, when all extensions are built. This is unnecessary, because store extensions are shipped together with their assets.

Use

bash

```shiki
shopware-cli project storefront-build --only-custom-static-extensions
shopware-cli project admin-build --only-custom-static-extensions
```

to build only extensions in the `custom/static-plugins` folder of your project, which are usually not shipping the assets.

## Worker [​](#worker)

Usually you have to start the worker with `bin/console messenger:consume` in the project root directory. But if you want to have more than one worker at once, it gets a bit tricky. Shopware CLI has a helper command for that:

bash

```shiki
shopware-cli project worker <amount>
```

For production, you should let this handle **supervisord** or **systemd**. But for development, this is a quick way to start multiple workers.

## Clear cache [​](#clear-cache)

It is just a shortcut for `bin/console cache:clear` without having to be in the project root directory.

bash

```shiki
shopware-cli project clear-cache
```

If in the `.shopware-project.yml` a API connection is configured, it will clear the remote instance cache.

## Console [​](#console)

Similar to `clear-cache`, there is also a general shortcut for `bin/console`:

bash

```shiki
shopware-cli project console <command>
```

## Generate JWT secret [​](#generate-jwt-secret)

To generate a new JWT secret, you can use the following command:

bash

```shiki
shopware-cli project generate-jwt
```

It is similar to `bin/console system:generate-jwt-secret`, but requires no Shopware project to be present or PHP to be installed.

## Admin API [​](#admin-api)

If you want to make requests against the Shopware-API using curl, you need to get a JWT token and add it as a header. Shopware CLI has a helper command for that:

bash

```shiki
shopware-cli project admin-api --output-token
```

This will output the JWT token to the console. You can also make directly API requests like:

bash

```shiki
shopware-cli project admin-api GET /_info/version
```

You can also pass more options like `-d` for data or `-H` for headers as you would do with curl.

---

## Autofixer

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/autofix.html

# Autofixer [​](#autofixer)

Shopware-CLI comes with some builtin auto fixers for project migrations.

## Migrate a Project to Symfony Flex [​](#migrate-a-project-to-symfony-flex)

Prior to Shopware 6.5, Shopware didn't use Symfony Flex. This means that the project structure was different, and some configuration files were located in different places. The `shopware-cli project autofix flex` command will migrate your project to Symfony Flex and move all configuration files to the correct locations.

WARNING

Ensure that you have a backup of your project before running this command.

bash

```shiki
shopware-cli project autofix flex
```

The command will delete all unnecessary configuration files. It will also update the `composer.json` file and the `bin/console` file to use the new configuration files.

## Migrate custom/plugins extensions to Composer [​](#migrate-custom-plugins-extensions-to-composer)

It's best practice to manage the store and your custom plugins via Composer. [If you want to learn more about this check out this guide](./../../../guides/hosting/installation-updates/extension-managment.html). Shopware-CLI has a helper for migrating locally installed plugins to Composer through Shopware Packagist for the Shopware Store. Make sure you have a Shopware Packages Token, which can be gathered in the Shopware Account. You can find the token in the Shopware Account under "Shops" > "Licenses" > "..." of one extension and "Install via Composer.

bash

```shiki
shopware-cli project autofix composer-plugins
```

---

## Image Proxy

**Source:** https://developer.shopware.com/docs/products/cli/project-commands/image-proxy.html

# Image Proxy [​](#image-proxy)

The `shopware-cli project image-proxy` command starts a local HTTP server that serves static files from your Shopware project's `public` folder. When a requested file is not found locally, it automatically proxies the request to an upstream server and caches the response for future requests.

This is particularly useful during development when you want to work with a local Shopware installation but need access to media files (images, documents, etc.) from a production or staging environment without downloading the entire media library.

## Usage [​](#usage)

bash

```shiki
# Start the proxy server using configuration from .shopware-project.yml
shopware-cli project image-proxy

# Specify a custom upstream URL
shopware-cli project image-proxy --url https://my-shop.com

# Use a different port
shopware-cli project image-proxy --port 3000

# Clear the cache before starting
shopware-cli project image-proxy --clear

# Use external URL for reverse proxy setups
shopware-cli project image-proxy --external-url https://dev.example.com

# Skip Shopware config file creation
shopware-cli project image-proxy --skip-config
```

## Configuration [​](#configuration)

You can configure the upstream URL in your `.shopware-project.yml` file:

yaml

```shiki
# .shopware-project.yml
image_proxy:
  url: https://production.example.com
```

If no URL is provided via the `--url` flag or configuration file, the command will exit with an error.

## How It Works [​](#how-it-works)

The image proxy follows this request flow:

1. **Check Local Files**: First, it looks for the requested file in your local `public` folder
2. **Check Cache**: If not found locally, it checks the file cache (`var/cache/image-proxy/`)
3. **Proxy Request**: If not cached, it forwards the request to the upstream server
4. **Cache Response**: Successful responses (HTTP 200) are cached to disk for future requests

### Shopware Integration [​](#shopware-integration)

By default, the command creates a Shopware configuration file at `config/packages/zzz-sw-cli-image-proxy.yml` that automatically configures Shopware to use the proxy server for all public filesystem operations. This file is automatically removed when the server stops.

The configuration looks like:

yaml

```shiki
shopware:
  filesystem:
    public:
      type: "local"
      url: 'http://localhost:8080'  # or your configured URL
      config:
        root: "%kernel.project_dir%/public"
```

### Cache Behavior [​](#cache-behavior)

* Files are cached in `var/cache/image-proxy/` within your project directory
* The cache preserves the `Content-Type` header to ensure files are served with correct MIME types
* Cache files are named by replacing `/` with `_` in the request path
* There is no automatic cache expiration - files remain cached until manually cleared
* Cached responses include an `X-Cache: HIT` header when served

## Command Options [​](#command-options)

| Option | Description | Default |
| --- | --- | --- |
| `--url` | Upstream server URL (overrides config) | From config |
| `--port` | Port to listen on | `8080` |
| `--clear` | Clear cache before starting | `false` |
| `--external-url` | External URL for Shopware config (e.g., for reverse proxy setups) | `http://localhost:{port}` |
| `--skip-config` | Skip creating Shopware config file | `false` |

## Example Scenarios [​](#example-scenarios)

### Development with Production Media [​](#development-with-production-media)

When developing locally but needing access to production media files:

bash

```shiki
# Configure once
echo "image_proxy:
  url: https://production.example.com" >> .shopware-project.yml

# Start proxy
shopware-cli project image-proxy

# Access your local Shopware at http://localhost:8080
# Media files will be transparently fetched from production
```

### Testing with Fresh Cache [​](#testing-with-fresh-cache)

To ensure you're working with the latest media files:

bash

```shiki
shopware-cli project image-proxy --clear
```

### Multiple Environments [​](#multiple-environments)

Switch between different upstream servers:

bash

```shiki
# Staging environment
shopware-cli project image-proxy --url https://staging.example.com

# Production environment
shopware-cli project image-proxy --url https://production.example.com
```

### Reverse Proxy Setup [​](#reverse-proxy-setup)

When running behind a reverse proxy (Nginx, Apache, etc.):

bash

```shiki
# Configure external URL for Shopware
shopware-cli project image-proxy --external-url https://dev.example.com
```

### Manual Configuration [​](#manual-configuration)

If you want to manage Shopware configuration manually:

bash

```shiki
# Run proxy without creating config file
shopware-cli project image-proxy --skip-config
```

---

## Authentication

**Source:** https://developer.shopware.com/docs/products/cli/shopware-account-commands/authentication.html

# Authentication [​](#authentication)

To interact with the Shopware Account API, you need to authenticate yourself.

For this, you need to log in using:

bash

```shiki
shopware-cli account login
```

and it will ask you interactively for your credentials.

For CI/CD pipelines, you should pass `SHOPWARE_CLI_ACCOUNT_EMAIL` and `SHOPWARE_CLI_ACCOUNT_PASSWORD` as environment variables and call directly the command you want to use.

INFO

For CI/CD tasks you should create a dedicated Shopware Account with limited access to the Shopware Store.

## Multiple companies [​](#multiple-companies)

A single Shopware Account can be part of multiple companies. You can only interact with one company at a time.

You can use the following commands to list all companies you have access to:

bash

```shiki
shopware-cli account company list
```

Next, select the active company with:

bash

```shiki
shopware-cli account company use <id>
```

---

## Releasing automated extension to Shopware Store

**Source:** https://developer.shopware.com/docs/products/cli/shopware-account-commands/releasing-extension-to-shopware-store.html

# Releasing automated extension to Shopware Store [​](#releasing-automated-extension-to-shopware-store)

## Prerequisites [​](#prerequisites)

* You are logged into the Shopware Store. Checkout the [Authentication](./authentication.html) guide for more information.
* You have a zip file of your extensions with all assets. Checkout the [Creating a zip](./../extension-commands/build.html) guide for more information.
* The zip file contains a `CHANGELOG*.md` file with a Changelog entry for the new version. Having a German changelog is optional.
* You have validated the zip file with `shopware-cli extension validate <zip-path>`. See [Validating the zip](./../validation.html) for more information.

## Releasing the extension [​](#releasing-the-extension)

To release the extension to the Shopware Store, you need to upload the zip file to the store. This can be done with the `shopware-cli account producer extension upload` command.

bash

```shiki
shopware-cli account producer extension upload <zip-path>
```

This command will check first if an extension with the same version already exists in the store. If not, it will upload the extension to the store. For the compatibility of the extension, the command will use the Composer constraint of `composer.json` or `manifest.xml` file.

After the upload, the command will wait for the result of the automatic validation. This can take a few minutes. If the validation fails, the command will output the error message, and you need to fix the issue and upload the extension again. You can skip this check with the `--skip-for-review-result` option.

---

## Updating Store Page of Extension

**Source:** https://developer.shopware.com/docs/products/cli/shopware-account-commands/updating-store-page.html

# Updating store page of extension [​](#updating-store-page-of-extension)

You can use Shopware CLI to version your Store page representation of your extension. This includes the description, images, and all other assets.

## Prerequisites [​](#prerequisites)

* You are logged into the Shopware Store. Checkout the [Authentication](./authentication.html) guide for more information.

## Fetching the current Store page [​](#fetching-the-current-store-page)

It is recommended to start with the current Store page and update only the parts you want to change. You can fetch the current Store page with the following command:

bash

```shiki
shopware-cli account producer extension info pull <path-to-extension-folder>
```

This will download all uploaded Store images and create a `.shopware-extension.yml` with all metadata of the extension.

This file can be checked in into the version control and will be automatically removed when you create a zip file using Shopware CLI.

## Updating the Store page [​](#updating-the-store-page)

To push the changes to the Store page, you can use the following command:

bash

```shiki
shopware-cli account producer extension info push <path-to-extension-folder>
```

This will upload all images and metadata to the Store page.

## Image configuration [​](#image-configuration)

Images can be uploaded in two ways:

Explicitly defined in the configuration like this:

yaml

```shiki
store:
  images:
    - file: <path-to-file>
      # Priority of the image for ordering
      priority: 1
      # In which language the image should be used
      activate:
        de: false
        en: false
      # Is the image a preview image, only one image can be a preview
      preview:
        de: false
        en: false
```

or you can specify a single directory with all images:

yaml

```shiki
store:
  image_directory: <path-to-directory>
```

The images will be sorted by the file name. If you want to separate the images by language, you can create subdirectories with the language code like so:

text

```shiki
src/Resources/store/images/
├── de
│   ├── 0.png
│   ├── 1.png
│   └── 2.png (preview image)
└── en
    ├── 0.png
    ├── 1.png
    └── 2.png (preview image)
```

---

## Configure Composer Repository

**Source:** https://developer.shopware.com/docs/products/cli/shopware-account-commands/configure-composer-repository.html

# Configure composer repository [​](#configure-composer-repository)

To install extensions from the Shopware Store, you need to configure the Composer repository in your `composer.json` file. Shopware CLI can configure this for you automatically.

First, make sure you have access to the given Shop in Shopware Account. You can check this with the following command:

bash

```shiki
shopware-cli account merchant shop list
```

If you don't see the shop you want to use, you need to switch to the correct company with the following command. Check the [Authentication](./authentication.html) guide for more information.

To create a `auth.json` file with the Composer repository configuration, you can use the following command:

INFO

You can also use the tab completion in the terminal to get the domains of the shops you have access to.

bash

```shiki
shopware-cli account merchant shop configure-composer <domain>
```

This will create `auth.json` and append the Composer repository configuration to your `composer.json` file.

---

## Validation

**Source:** https://developer.shopware.com/docs/products/cli/validation.html

## Validation [​](#validation)

Shopware CLI has built-in validation for extensions. This is useful in your CI/CD pipeline to validate the extension before you release it.

## Validating an extension [​](#validating-an-extension)

To validate an extension, you can use the following command:

The path can be absolute or relative to the directory containing the extension or the zip file. The command exits with a non-zero exit code if the validation fails with an error-level message.

## What is validated in basic mode? [​](#what-is-validated-in-basic-mode)

* The `composer.json` has a `shopware/core` requirement and the constraint is parsable
* The extension metadata is filled with:
  + `name`
  + `label` (German and English)
  + `description` (German and English) and longer than 150 characters and shorter than 185 characters
* PHP can be correctly linted with the minimum PHP version
* The `theme.json` can be parsed and included assets can be found
* All snippet files contain the same set of translation keys

## Supported PHP versions for linting [​](#supported-php-versions-for-linting)

The following PHP versions are supported for linting:

* 7.3
* 7.4
* 8.1
* 8.2

These versions don't need to be installed locally; they are downloaded on demand and executed using WebAssembly without any dependencies.

## Running all validation tools [​](#running-all-validation-tools)

By default, only a few tools are run, but you can run all tools by using the `--full` option. This will run all available tools and check your extension against the latest Shopware version.

By default, it will check against the latest allowed Shopware version according to your constraints in `composer.json`. It's recommended to run the check against the lowest and highest allowed version, so you can be sure that your extension is compatible with all versions. You can do this by using the `--check-against` option:

The check command has multiple reporting options, you can use `--reporter` to specify the output format. The following formats are supported:

| Format | Description |
| --- | --- |
| `summary` | default list of all errors and warnings |
| `json` | json output |
| `junit` | junit output |
| `github` | GitHub Actions output |
| `markdown` | markdown output |

## Running Specific Tools [​](#running-specific-tools)

Instead of running all tools, you can choose to run specific tools using the `--only` flag. The following tools are available:

| Tool | Description |
| --- | --- |
| `phpstan` | PHP static analysis |
| `sw-cli` | Shopware CLI validation checks |
| `stylelint` | CSS/SCSS linting |
| `admin-twig` | Admin Twig template checks |
| `php-cs-fixer` | PHP code style fixing |
| `prettier` | Code formatting |
| `eslint` | JavaScript/TypeScript linting |
| `rector` | PHP code refactoring |

You can run a single tool:

This is particularly useful when:

* You want to focus on specific aspects of your code
* You want to run only the relevant tools for the files you've changed
* You want to fix issues one tool at a time

## Validation ignores [​](#validation-ignores)

If you want to ignore errors or warnings, you can create a `.shopware-extension.yaml` file in your extension root with the following content:

yaml

```shiki
validation:
  ignore:
    # Ignore all errors by identifier
    - identifier: 'Shopware.XXXXXX'
    # Ignore all errors by identifier and path
    - identifier: 'Shopware.XXXXXX'
      path: 'path/to/file.php'
    # Ignore all errors by message and path
    - message: 'Some error message'
      path: 'path/to/file.php'
    # Ignore all errors by message
    - message: 'Some error message'
```

## Scanning a project [​](#scanning-a-project)

It's possible to scan an entire project instead of just a single extension. This is useful if you want to check all extensions in your project at once. You can do this by passing the path to the project root instead of the extension path.

All config files like `phpstan.neon` and `.php-cs-fixer.dist.php` should be placed in the project root for proper configuration or to override the default settings. The Verifier will automatically detect the config files and use them for the checks.

Ignoring errors works similarly to extensions; in that case, you can create a `.shopware-project.yaml` file in your project root with the same syntax.

## Common issues [​](#common-issues)

### Fixer does nothing for Shopware 6.7 [​](#fixer-does-nothing-for-shopware-6-7)

The fixers are enabled by the supported Shopware Version in the plugins `composer.json` file. For 6.7, you should change the composer constraint to this:

json

```shiki
{
    "minimum-stability": "dev",
    "require": {
        "shopware/core": "~6.7.0"
    }
}
```

### Missing classes in Storefront/Elasticsearch bundle [​](#missing-classes-in-storefront-elasticsearch-bundle)

Your plugin typically requires only `shopware/core`, but when you use classes from Storefront or the Elasticsearch Bundle and they are required, you have to add `shopware/storefront` or `shopware/elasticsearch` also to the `require` in the composer.json. If those features are optional with `class_exists` checks, you want to add them into `require-dev`, so the dependencies are installed only for development and PHPStan can recognize the files.

---

## Formatter

**Source:** https://developer.shopware.com/docs/products/cli/formatter.html

# Formatter [​](#formatter)

Shopware CLI includes a built-in code formatter for PHP, JavaScript, CSS, SCSS, and Admin Twig files. Use it to apply the Shopware [Coding Standard](https://developer.shopware.com/docs/resources/guidelines/code/) automatically and keep your project consistent. You can format individual extensions or entire projects.

A `--dry-run` mode is also available to preview changes without modifying files.

## Formatting an extension [​](#formatting-an-extension)

## Formatting an entire project [​](#formatting-an-entire-project)

## Configuration [​](#configuration)

By default, the formatting is done by Shopware Coding Standard. You can configure the formatting by creating a `.php-cs-fixer.dist.php` in your extension root or a `.prettierrc` file for JavaScript, CSS, and SCSS files.

---

## Automatic refactoring

**Source:** https://developer.shopware.com/docs/products/cli/automatic-refactoring.html

# Automatic refactoring [​](#automatic-refactoring)

Shopware CLI includes a built-in automatic refactoring tool that helps you automatically update and clean up code in your Shopware projects and extensions.

Use this tool to modernize your codebase when upgrading to a new Shopware version or to apply best-practice changes automatically.

* [Rector](https://getrector.com/) for PHP
* [ESLint](https://eslint.org/) for JavaScript
* Custom rules for Admin Twig files

## Refactoring an extension [​](#refactoring-an-extension)

WARNING

Before you start, make sure you work on a copy or Git-versioned branch, because this command will modify your files in place!

## Refactoring an entire project [​](#refactoring-an-entire-project)

You can also refactor a full Shopware project instead of a single extension.

The CLI runs Rector and ESLint automatically. After completion, review all changes and commit or revert them as needed.

Make sure the `shopware/core` requirement in your `composer.json` file reflects the version you're targeting. Shopware CLI determines which upgrade rules to apply based on that version constraint.

## Experimental Twig upgrade using Large Language Models (LLMs) [​](#experimental-twig-upgrade-using-large-language-models-llms)

Shopware CLI also includes an experimental AI-powered Twig upgrade tool. It can help migrate Twig templates between Shopware versions by using Large Language Models (LLMs) to propose code adjustments.

Because it's experimental, only run this feature on version-controlled (in Git or similar) code. It may generate changes that need manual review.

Run the upgrade:

### Supported providers [​](#supported-providers)

The Twig upgrade tool currently supports multiple providers:

| Provider | Description | Required environment variable |
| --- | --- | --- |
| `gemini` | [Google Gemini](https://ai.google.dev/) LLM | `GEMINI_API_KEY` |
| `openrouter` | [OpenRouter API](https://openrouter.ai/) | `OPENROUTER_API_KEY` |
| `ollama` | Local [Ollama](https://ollama.com/) instance | `OLLAMA_HOST` (optional) |

Recommendations:

* For the most accurate Twig upgrades, use Google Gemini 2.5 Pro (`--provider gemini --model gemini-2.5-pro`).
* If you prefer a fully local setup, use Ollama, but ensure you have pulled a compatible model (e.g., `ollama pull llama3`).

## After running refactoring [​](#after-running-refactoring)

Use Git or your diff tool to review the changes.

Test your extension or project thoroughly.

Commit the accepted changes and discard any unwanted ones.

You can combine automatic refactoring with other Shopware CLI commands (e.g., `project build` or `extension validate`) as part of your upgrade workflow.

---

