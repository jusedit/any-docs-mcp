# Resources Guidelines Documentation Guidelines

*Scraped from Shopware Developer Documentation*

---

## Document

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/

# Documentation Guidelines [​](#documentation-guidelines)

As a contributor, you should refer to this section on how to write articles, the language usage, font and formats to be followed, etc. This section also details the step-by-step documentation process.

---

## Fonts & Formats

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/04-fonts-and-formats/

# Fonts and Formats [​](#fonts-and-formats)

This section explains how to format text and code in sentences.

---

## Text

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/04-fonts-and-formats/01-text.html

# Fonts and Format for Text [​](#fonts-and-format-for-text)

Follow the below textual formats for good content visualization.

INFO

Don't override global styles.

* **Bold**

Use bold to signify UI elements, notices (warning, notice, important declaration), API response - status codes, and titles in descriptions lists.

Use double asterisk in Markdown to signify bold format - for example, `**bold**`.

* **Italic**

Use italics to draw attention to a specific word, phrase, parameter values, classes, methods, product versions, and key terms like SQL Database.

Use a single asterisk in Markdown to signify italic format - for example, `*italic*`.

* **Underline**

Don't underline any content.

## List [​](#list)

Use sentence cases for items in all types of lists as below:

* **Numbered list** - Use when you have a fixed number of entities — for example, three varieties, four categories, two types, etc, or sequential steps as shown below:

markdown

```shiki
Follow the below steps to start your project:

1. Create a docker-compose.yml file
2. Start the Docker
3. Prepare Development
4. ...
```

* **Regular bulleted list** - Use this for general enlisting with an asterisk `*` in Markdown to signify bulleted lists.

text

```shiki
You can install Shopware on Mac with the help of tools like:

* Docker
```

However, regular bulleted lists within tables use HTML tags.

text

```shiki
| Who is the audience? | What are their roles? |
| :--- | :--- |
| Fullstack Developer | <ul><li>Plugin Development</li><li>Templates</li><li>Routes/ Controllers</li></ul>|
```

* **Description list** - Use when you need to describe them along with their titles. In such a case, title tags are bolded, followed by a hyphen or new line and a detailed description. For example,

text

```shiki
The Administrations components implement a number of cross-cutting concerns. The most important are:

* **Providing inheritance** - As Shopware 6 offers a flexible extension system to develop your own Apps, Plugins, or Themes.
* **Data management** - The Administration displays entities of the Core component.
* **State management** - Proper state management is key here.
```

The description list can again be a numbered list or a bulleted list based on its sequence or fixed number of entities.

## Date and time [​](#date-and-time)

In general, use the following guidelines to format expressions of date and time:

* Use the 12-hour clock, except if required to use a 24-hour time, such as when documenting features that use 24-hour time.
* Capitalize AM and PM, and leave one space between them and the time.
* Avoid using time zones unless absolutely necessary. If using a specific time zone, spell out the region and include the *UTC or GMT* label.
* Spell out the names of the months. For example, `January 19, 2017`.
* You can also use the numerical date format, `MM-DD-YYYY`, and separate the elements by hyphens.

## Numbers [​](#numbers)

Spell out all ordinal numbers in the text, such as first, fourth, twelfth, and twenty-third for 1st, 4th, 12th, and 23rd, respectively. However, there are exceptions like prices, weight, and quantity which can only be represented as numbers.

## Tables [​](#tables)

* Don't embed a table in the middle of a sentence.
* Use table headings for the first column and the first row only.
* Use tables only when you have more than one row and column to represent.
* Don't end sentences with punctuation, including a period, an ellipsis, or a colon.
* Use sentence case for all the elements in a table - contents, headings, labels, and captions.
* Introduce a table using a complete sentence and try to refer to the table's position, using a phrase such as *the following table or the preceding table*.

## Hyperlinks [​](#hyperlinks)

* Provide meaningful URL text links. Don't use *click here or read this document* phrases.
* Write a complete sentence that refers the reader to another topic. Introduce the link with a phrase such as *For more information, see or For more information about..., see*.
* Keep the link text as short as possible. Do not write lengthy link text such as a sentence or short paragraph.
* Place important words at the beginning of the link text.
* Don't use the exact link text in the same document for different target pages.
* If the hyperlink text includes an abbreviation in parentheses, include the long form and the abbreviation in the link text.

## Heading [​](#heading)

* Use `#` to set the levels of heading.
* Don't skip levels of the heading hierarchy. For example, an `<H3>` heading must fall under `<H2>`.
* Follow camel case for all the `<H1>` headings — for example, *Flow Sequence Evaluation* and sentence case for the rest of the sub-headings that follow - for example, *Flow sequence evaluation*.

Refer to [Vitepress syntax](https://vitepress.dev/guide/markdown) for more.

This section covers fonts and formats for text, while the following section covers fonts and formats for code.

---

## Code

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/04-fonts-and-formats/02-code.html

# Fonts and Format for Code [​](#fonts-and-format-for-code)

Fonts and formats for inline code, code blocks, non-code items, API reference, classes and methods are detailed below:

## Inline code [​](#inline-code)

* Inline code is a short snippet of code. Use `` backticks (`) `` for single-line code/ inline code.
* The following are examples of inline code:

  + Attribute names and values
  + Command Line (CLI) utility names
  + Class, methods, and function names
  + Enum names
  + Command output
  + Data types
  + Environment variable names
  + File names and paths
  + Folders and directories
  + HTTP methods and status codes
  + HTTP status codes
  + Alias names
  + Parameter values

Below are a few more instances:

### HTTP status codes [​](#http-status-codes)

* In general, put the number and the name of the status code in code font:

  HTTP `400 Bad Request` status code
* To refer to a range of codes, use the following form:

  `HTTP 2xx` or `200` status code
* If you prefer to specify an exact range, use the following form:

  HTTP status code in the `400-499` range

### Command prompt [​](#command-prompt)

* If your CLI instructions show single-line or multi-line input, start each line of input with the `$` prompt symbol.
* Don't show the current directory path before the prompt, even if part of the instruction includes changing directories.

### Placeholders [​](#placeholders)

* In a code output, explain any placeholder that appears in the sample output the first time.
* Mention the placeholders in complete capital and italicized code font.
* In markdown, wrap inline placeholders in `` backticks (`) `` and `asterisk (*)`.

markdown

```shiki
(*`PLACEHOLDER_NAME`*)
```

* Don't use *X* as a placeholder; instead, use an informative placeholder name.

## Code blocks [​](#code-blocks)

* Code blocks are used for code snippets longer than a single line or terminal commands containing sample output when executed.
* In markdown, code blocks are represented using a ```` code fence (```) ````.
* Mention language identifier to enable syntax highlighting in your fenced code block.

markdown

```shiki
 ```markdown
 Language identifier is markdown here.  
 ```
```

* When using code blocks within lists, use correct indention to avoid breaking the list. For example,

TIP

* Payment

  jsx

  ```shiki
  const pay_type = <Payment type=COD />;
  ```
* Transaction

DANGER

* Payment

jsx

```shiki
const pay_type = <Payment type=COD />;
```

* Transaction

* Don't use tabs to indent text within a code block; use two spaces.
* Use three dots (...) on a separate line to indicate that more lines of output are omitted from the sample output.

## Blockquote [​](#blockquote)

* Blockquotes are represented by `>`

text

```shiki
> Added A Name preset according to new naming scheme.
```

* To add blockquotes within a blockquote, use `>>`

## Items to put in ordinary (non-code) font [​](#items-to-put-in-ordinary-non-code-font)

The following list includes items that should not be in code font:

* Email addresses
* Domain names
* URLs
* Names of products, services, and organizations

## API reference [​](#api-reference)

* The API reference code must describe every class, interface, struct, constant, field, enum, and method, with a description for each parameter and the status codes.
* Capitalize the API method names such as `GET`, `PUT`, `PATCH,` etc.
* Provide meaningful information about the request parameters. Link them to other sections of the documentation for more explanations.
* Include any valid and default value at the end of the parameter description. For example, *Valid values are `true` and `false`. The default is `false`.*
* In detailed documentation, elaborate on how to use the API, including invoking or instantiating it, the key features, and best practices or pitfalls.

## Classes and methods [​](#classes-and-methods)

* Describe the class briefly and state the intended function with information that can't be deduced from the class name and signature.
* Describe the method briefly and what action the method performs. In subsequent sentences, state any pre-requisites that must be met before calling it, explain why and how to use the method, give details about exceptions that may occur, and specify any related APIs.
* Method names should be followed by a pair of parentheses `()`.
* You may also cross-link parameters, classes, and methods.

## Deprecations [​](#deprecations)

When something is deprecated, tell the user what to use as a replacement or what to do to make their code work. For example,

WARNING

**Deprecated** - Access it using this getProd() method instead.

The following section deals with asset (files, images, and videos) management.

---

## General

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/01-general.html

# Documentation Guidelines [​](#documentation-guidelines)

Your style, your words, and your tone define you. Correspondingly, this style guide lays out standard editorial instructions that define Shopware documentation.

We recommend that every contributor follows the defined writing standards to maintain uniformity of the documentation. Refer to different sections of this guide to know more.

## Audience [​](#audience)

It is important to consider the background of the potential audience reading your writing. This helps you to adapt your writing to meet their needs and interests.

| Who is the audience? | What are their roles? |
| --- | --- |
| Fullstack developer | * Plugin development * Templates * Routes/ Controllers |
| Frontend developer | * Admin * Themes * PWA |
| Backend developer | * DI/ Service architecture * Message queues * DAL * Action event system * ElasticSearch |
| API developer | * How to consume the API * Create a product/ category import * How to extend the API * API paradigm * Proper API references * Request collection |
| DevOps | * Hosting setup * Deployment * Performance tests |
| Project/ Solution architect | * Hosting * Architecture * Modules/ Extension system * Paradigms/ Patterns * Commonalities app system/ Plugin system |
| Designer | * Component library * Design system |
| Product owner/ Manager | * Responsibilities pertaining to the product life cycle |
| Tech writers | * Document all product details |

## Applicable documents: style guide coverage [​](#applicable-documents-style-guide-coverage)

* [Developer docs](https://developer.shopware.com/docs/)
* [API Reference Guide](https://shopware.stoplight.io/)
* [Composable Frontends docs](https://frontends.shopware.com/)
* [Component library](https://component-library.shopware.com/)

## Word list [​](#word-list)

Choose ecommerce and technical terms from the pre-defined list of terminologies:

* [Shopware terminologies](https://shopware.atlassian.net/wiki/spaces/pr/pages/19249037615/Shopware+terminology)
* [General terms and abbreviations](https://shopware.atlassian.net/wiki/spaces/BGE/pages/735426953/Our+corporate+communications)

INFO

These are internal resources visible to Shopware employees only.

## Use of third-party sources [​](#use-of-third-party-sources)

Third-party sources include websites, books, blogs, videos, images, and more. Ensure to reference these external sources in the documentation only if they are trustworthy. Avoid copying any content directly from other sources like websites, encyclopedias, and Wikipedia.

## Markdown rules [​](#markdown-rules)

Adhere to the [Markdown cheat sheet](https://www.markdownguide.org/cheat-sheet/) while creating the document.

Refer to [Vitepress syntax](https://vitepress.dev/guide/markdown) for features like hint block, emoji, API blocks, etc.

Symbols in Markdown sometimes serve multi-purpose. For example, `*` or `-` can be used to create bulleted lists. However, follow a single pattern to maintain uniformity throughout. Further sections describe the usage of these patterns and let us comply with them.

Also, user-defined rules govern the content quality, such as removing trailing spaces, code fence style, and more. You may refer to these rules in the [Markdown style of Shopware docs](https://github.com/shopware/docs/blob/main/markdown-style-config.yml).

The following section details the conceptual outline structure of our documentation.

---

## Methodize Assets

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/05-methodize-assets.html

# Methodize Assets [​](#methodize-assets)

Maintaining a well-organized repository for all documentation assets, including images, videos, and files, is crucial. This section provides an overview of how assets are represented, managed, and the naming conventions that are adhered to.

INFO

For the creation of a visual representation, either contact the Shopware design team directly or submit a request through the [Issues](https://github.com/shopware/docs/issues) section.

## Visual diagram guidelines [​](#visual-diagram-guidelines)

Our documentation categorizes visuals into different types, including screenshots, diagrams (such as UML and flowcharts), and GIFs. Each of these visual elements shares common quality standards. This section outlines the specific requirements that must be met by all visuals used in technical documentation.

### Diagram specifications [​](#diagram-specifications)

| Image attributes | Specification | Notes |
| --- | --- | --- |
| File type | Only .png, .svg and .gif | Use a lossless image format for screenshots (i.e., PNG) and vector format (i.e., SVG) for drawings (diagram, chart, logos, ...). |
| File size | max. 5 MB | It is best to upload high-quality images. |
| File name | Only use letters and hyphens `<topicName>-<subtopicName>-<meaningfulImageName>.md.` | Use the naming convention documented below in naming conventions for images. |
| Image size | Width: max 768px, Height: max 576px | This is automatically taken care by the inbuilt functions in our docs. |
| Aspect ratio | 4:3 | This is automatically taken care by the inbuilt functions in our docs. |
| Copyright | - | Determine if an image or diagram is protected by copyright. If it is, you must obtain permission and acknowledge credit. |
| Personal identifiable information (PII) | - | Make sure to mask, modify, or remove any PII such as passwords, logins, account details, or other information that could compromise security. |
| Alt tags | `![Alt](/path/to/img.jpg “image title”)` | Make sure to include alt text for every image. The text is used in situations where the image isn’t visible and image SEOs. |
| Borders | - | No borders are added to the images |

### Considerations for Visual Diagrams [​](#considerations-for-visual-diagrams)

* If you add images to illustrate items in a list (typically, steps in a procedure), align these images accordingly:

  + If there is only one image that illustrates the entire procedure, place the image at the end of the procedure or align it with the lead-in paragraph.
  + If you need to provide an image for each step in the procedure, place each image at the end of each step it follows.
* Use the below naming convention for the images:

  + *`<topicName>-<meaningfulImageName>.svg`*. For example,

markdown

```shiki
storefront-pages.svg
```

* If sub-topic exists, *`<topicName>-<subtopicName>-<meaningfulImageName>.svg`*. For example,

markdown

```shiki
storefront-dataHandling-pages.svg
```

* The image names can be serialized if multiple images are under the same topic. For example,

markdown

```shiki
storefront-dataHandling-pages_01.svg
```

* An introductory sentence should precede most images.
* Store all the media in the [assets directory](https://github.com/shopware/docs/tree/main/assets). Once it is loaded, copy the reference to the Markdown file. Test images in a local build.

## Diagrams [​](#diagrams)

### Considerations for Diagrams [​](#considerations-for-diagrams)

Consider creating diagrams to :

* Show architecture
* Show complex relationships
* Define a complex workflow

### Diagram creation tools [​](#diagram-creation-tools)

* [Mermaid](https://mermaid.live/) - Use Mermaid for generating Flowcharts, Sequence Diagrams, State Machine Diagrams, Class Diagrams, etc. Embed the diagram code within a codeblock named `mermaid`.
* [Meteor Diagram Kit](https://www.figma.com/community/file/1339141765099471739) - Apart from UML diagrams, utilize *Meteor Diagram Kit* to create other diagrams. This follows Shopware design and quality standards.

## Screenshots [​](#screenshots)

### Considerations for Diagrams [​](#considerations-for-diagrams-1)

Consider creating screenshots to :

* Provide an example of a visualization
* Show panels populated with query and settings
* Show configurations and settings
* Emphasize a new feature
* Limit the contents of an image to the relevant portion. Do not include distracting or unnecessary content and whitespace.

### Aspects for Capturing Screenshots [​](#aspects-for-capturing-screenshots)

* If the screenshot shows a desktop application interface, you must use the latest OS version supported by the solution to take the screenshot.
* The screenshot must be in focus and show an active window, wizard or dialog box.
* Avoid both horizontal and vertical scroll bars whenever possible.
* The screenshot must show real-world data or at least data that is close to realistic use cases.
* All screenshots you take must be consistent with each other.
* Screenshots can be taken using GIMP, Snipping tools, or any tool you have already worked on.
* Do not use screenshots for Code samples (show code samples in codeblocks).
* Do not take screenshots for a page that is likely to change frequently.

## GIFs [​](#gifs)

### Considerations for GIFs [​](#considerations-for-gifs)

Consider using GIFs when you want to:

* Demonstrate flow of procedures.
* Highlight functionalities visually.
* Aid setup and initial tasks with visual guides.

## File [​](#file)

Every file added to a folder can have a naming convention as:

*`<two_digit_number>-<meaningful_image_name>.md`.* For example,

markdown

```shiki
01-doc-process.md
```

## Video [​](#video)

* Provide captions and transcripts for video content.
* A similar naming pattern to that of images is also followed for videos.

All the previous sections detail how to articulate and format the document. The next section describes the entire process of writing, reviewing, and publishing the documentation.

---

## Conceptual Structure

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/02-conceptual-structure.html

# Conceptual Outline [​](#conceptual-outline)

Our documentation is categorized into the following sections - Concepts, Products, Guides, and Resources. This structure provides different levels of detail, abstraction, and focus.

To give our readers a good experience, we have established writing guidelines for these sections.

## Concepts [​](#concepts)

This section articulates the core concepts of Shopware. It is an entry point to learn about how the platform is organized. This section rather **explains** than **shows** how things work

## Products [​](#products)

This section deals with topics specific to a single product of Shopware. Every product shares at least some aspect and serves as an entry point to other sections. For example, the *catalog* used within our Community Edition and in all commercial plans is technically the same.

## Guides [​](#guides)

This section of the document is home to all the *how-to's*, *examples, cookbooks*, and *tutorials*. In contrast to articles within the *Concepts section*, *Guides* show code, give concrete examples, and provide step-by-step instructions.

It is essential to refer back to the concepts section for related topics from the Guides. For example, *"How to create a custom cart processor"* might contain terms and concepts explained within the "Concepts > Commerce > Checkout > Cart" section and also relate to topics dealt within the "Concepts > Framework > Rules" section. A clear structure allows you to create these cross-references and make the documentation more readable.

## Resources [​](#resources)

Resources contain structured documentation for API references, code references, testing references, tooling, links, SDKs, libraries, etc. It also includes guidelines for contribution and publishing.

Now that you have understood the documentation structure, the following section describes the command over language one needs to use for documentation.

---

## Doc Process

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/06-doc-process.html

# Documentation Process [​](#documentation-process)

You have gone a long way in understanding audience types, language rules, grammar treatment on textual content, and Shopware documentation structure to managing assets.

Now, are you thinking of how to kick-start?

Refer to our [GitHub repository](https://github.com/shopware/docs) for the complete process, from cloning the repository to publishing the content.

Well-defined writing leads to a more consistent, efficient learning experience for readers. We want to establish a common process for writing, reviewing, iterating, and maintaining documentation.

This section guides you on how to ink down your knowledge and publish the article.

## Ideate [​](#ideate)

When you prefer to contribute to an existing article or create a new one, consider yourself the "knowledge lead" for that particular topic while documenting.

Do some research and prepare a rough outline addressing the following points and prompt other maintainers for feedback:

* Who is the audience?
* What article are you going to write?
* What are the prerequisites for readers?
* Which questions are you going to answer?
* Which other topics might be relevant/interesting?

## Write [​](#write)

After you have discussed the abstract and set the objectives, start writing.

It is good to follow a "30/90" rule. This rule suggests creating the first draft when 30% done and taking the first feedback at a high level. When 90% done, schedule a steady review for in-depth validation.

In your first draft:

* Prepare the document structure (flow of topics).
* Jot down the topics of the documentation to be included and describe them.
* Mention all the points briefly that would be part of this article.
* Have a common thread throughout your article.
* Add placeholders for images or code blocks to be added later.
* Work with cross-references (knowledge is a network, not a one-way street ).
* Try to use non-Shopware-specific language when possible or provide a link to its description (e.g., "DAL").

### Guidelines to writing concepts [​](#guidelines-to-writing-concepts)

* **Introduction** - Introduce the concept (for example, cart) by its purpose in such a way that it answers the following general questions:
  + *What is a cart?*
  + *What can it contain?*
  + *How does it relate to users and orders?*
  + *What can the readers expect in the further connected articles?*

Use cross-references to help users fully understand the text — for example, provide a link to *configurable products* or *checkout* articles. Don't use terms like *"custom products"* as these are Shopware-specific, and newcomers may find it difficult to understand.

* **Comprehensive explanation** - Explain the concept in detail with examples, illustrations, tables, graphs, or pseudo-code.

  Don't use any Shopware-specific source code. Using source code within a conceptual article has the following drawbacks:

  + It introduces another dependency that has to be maintained.
  + It builds on the presumption that readers know the given language and context.
  + People tend to copy & paste without context.
* **Conclusions** - If possible add a connective statement to the next article that follows.

## Review [​](#review)

After writing the first 30%, consult a reviewer to give some initial feedback. Discuss the current progress and re-arrange some parts if needed.

If you are the reviewer, check the text's general approach, tone, and wording as per the standard guidelines. Provide the curator with some early direction and feedback. Having multiple reviewers can be beneficial.

This process can be repetitive until the final version is ready.

## Publish [​](#publish)

Before the final version is published, cross-check if the article fulfills all the questions and objectives outlined at the beginning. This must be reviewed, and feedback must be incorporated.

After reviewing the final draft, it will be published on notifying the administrators.

## Maintain Versions [​](#maintain-versions)

All contents are based on Shopware Major versions, such as 6.3, 6.4, 6.5, etc. The current version is reflected by our GitHub repositories' `master` branch, whereas each older version has its respective separate branch.

If a documented feature or functionality is introduced within major versions (and also in cases where you think it is applicable), please include a hint showing the version constraints as below:

INFO

This functionality is available starting with Shopware 6.4.3.0.

**Your contribution is our pride!**

---

## Language & Grammar

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/03-language-and-grammar.html

# Language and Grammar [​](#language-and-grammar)

Basic guidelines for the apt use of language and grammar in the documentation are discussed in this section. In order to create a consistent product solution, Shopware maintains consistent documentation not just in terms of content but also style. A distinctive editorial voice helps create high-quality, readable, and consistent documentation.

Use American English to cater to a global audience. You may refer to the [Cambridge dictionary](https://dictionary.cambridge.org/dictionary/essential-american-english/) for American vocabulary, spell check, and alternate words.

## Voice and tone [​](#voice-and-tone)

Shopware voices a friendly and conversational tone. We are direct, clear, and more human at conveying information.

### Our voice principles [​](#our-voice-principles)

* **Friendly** — Be less formal and more down-to-earth. Developer documentation is technical, but you can vocalize your writing to sound more human than a robot. Occasionally be funny when it is appropriate.
* **Direct and clear** — Be to the point. Write in such a way that just a skim through provides a clear idea to the reader. Make it simple above all.
* **Customer focussed** — Assume that the reader is knowledgeable but has varying proficiency levels. So, understand their real needs and offer help in the right way.

## Active voice and passive voice [​](#active-voice-and-passive-voice)

In general, use the active voice (the subject is the person or thing performing the action) instead of the passive voice (the subject is the person or thing being acted upon). For example,

TIP

**Active Voice** - The user passes the access-key.

DANGER

**Passive Voice** - The access-key is passed by the user.

It is okay to use passive voice in the following cases:

* To emphasize an object over an action — for example, *The file is modified*.
* To de-emphasize a subject — for example, *Over 20 bugs were found in the code*.
* The action doer is not necessarily to be known — for example, *The database was updated in the last week*.

## Second-person over first-person [​](#second-person-over-first-person)

* In general, use the second-person instead of the first-person, such as *you* instead of *we* or *I*. However, first-person usage is an exception for FAQs.
* If you are guiding the reader to perform something, use an imperative form with an implicit *you*. For example:

TIP

**Recommended** - Create a PDF file.

DANGER

**Not recommended** - You need to create a PDF file.

* Avoid the usage of *our* in sentences.

## Gender-neutral reference [​](#gender-neutral-reference)

* Use gender-neutral pronouns, such as *they* rather than *he, she, his, him, her*.
* Use gender-neutral words such as, humankind instead of mankind.

## Abbreviations [​](#abbreviations)

Abbreviations include initialisms, acronyms, shortened words, and contractions. They are intended to save the writer's and the reader's time.

### Initialisms and acronyms [​](#initialisms-and-acronyms)

* An initialism is formed from the first letters of words in a phrase — for example, *API, SQL, DDL*; whereas an acronym is formed from the initial letters of words in a phrase and pronounced as a word — for example, *ASCII, NASA*. Collectively, let's term it as abbreviation itself.
* When an abbreviation is not familiar to the audience, spell out the term followed by the abbreviation in parentheses, for example, *JSON Web Token (JWT)*. For all subsequent mentions, use the abbreviation only.
* Some abbreviations rarely need to be spelled out — for example, *API, HTTPS, SSA,* File formats such as *PDF, XML, PNG, or HTML*.
* Do not create abbreviations for product or feature names. Always spell out Shopware product and feature names.
* Abbreviations in plural form end with “s” — for example, *APIs, SKEs, and IDEs*. However, if the acronym itself ends in s, sh, ch, or x, then add es — for example, *OSes, and SSHes*.
* Don't define your own abbreviations. Use only the recognized industry-standard.

### Shortened words [​](#shortened-words)

* A shortened word is just part of a word or phrase — for example, *etc* for et cetera, *app* for application, *sync* for synchronization.
* Be consistent. Use either the shortened or the full word throughout the document.

### Contractions [​](#contractions)

* Contractions are unique words that are formed as a combination of two or more words with an apostrophe — for example, *it’s, you’re, you’ll, let’s, or we’re*. Such contractions add a more informal and friendly tone. So limit the usage of it.
* On the other hand, negation contractions (such as *isn't, don't, and can't*) are recommended to use as it is easy for a reader to miss the word *not*, whereas it is harder to misread *don't* as *do*.

## Tense [​](#tense)

* In general, use the simple present tense.
* Avoid future or past tense. When you are talking about the future, the reader will be writing or running code in the future. This makes the description look ridiculous. The same holds true for past references.

## Articles [​](#articles)

* Indefinite articles, *A* and *An* represent a singular noun.
* While *The* is a definite article used before singular and plural nouns in particular.
* Use an article with the acronym (an ISP, or a URL), nouns (the product database), etc.

## Capitalization [​](#capitalization)

* Capitalize the first letter of the word immediately following a colon.
* Follow capitalization for the names of companies, software, products, services, features, and terms defined by companies and open-source communities.
* When a hyphenated word is the first word in a sentence, capitalize only the first element in the word unless a subsequent element is a proper noun or proper adjective.

## Spellings [​](#spellings)

* Spellings are based on [Cambridge dictionary](https://dictionary.cambridge.org/dictionary/essential-american-english/).
* It is ideal to use filenames, URLs, and data parameters in words that are not spelled differently by different English dictionaries — for example, color and colour.

## Conjugations [​](#conjugations)

* Don't use */ (slash)* as conjugation. Use *or* instead.
* Don't use *& (ampersands)* as conjunctions. Use *and* instead.

## Punctuations [​](#punctuations)

### Comma [​](#comma)

* In a series of three or more items, use a comma before the sentence's final conjugation (and, or) — for example, *Bundles and plugins can provide their own resources like assets, controllers, services, or tests*.
* Place a comma after an introductory word or phrase — for example, *Also, each plugin is represented as a Composer package*.
* Use a semicolon, a period, or a dash before a conjunctive adverb, such as *otherwise, however*. Place a comma after the conjunctive adverb.
* Conjunction (and, but, or, nor, for, so, or yet) separate two independent clauses. Insert a comma after the first clause (before the conjunction) unless both clauses are very short — for example, *The more time you put into indexing data, the faster it is possible to read it*.

### Dashes and hyphens [​](#dashes-and-hyphens)

To indicate a break in the flow of a sentence, use an em dash (long dash) — for example, *Some programming languages — Pascal, COBOL, Ada are long gone*.

However, use a hyphen (small dash) in the following cases :

* Word prefixes — for example, *self-aware*
* Range of numbers — for example, *25-30 GB*
* Compound nouns — for example, *Mac-specific users*
* To remove ambiguity and clarify the meaning — for example, *logged-in, re-mark*.
* When the prefix ends in a vowel and the word it precedes starts with the same vowel — for example, *co-op, de-energize*.

### Period [​](#period)

* End every sentence with a period.
* Don't end headings with period.
* Don't end a URL with a period. Instead, place the URL in between the description.
* When a sentence ends with quotation marks, place the period inside the quotation marks.
* End every complete sentence with a period in a list. The exception is for phrases. For example,

markdown

```shiki
New cart features:

1. Store-level sales tax
2. Shipping modifier
3. Minimum and maximum order quantities
```

### Slashes [​](#slashes)

* Don't use date formats that rely on slashes.
* Don't use slashes with fractions because they can be ambiguous.
* Don't use slashes to separate alternatives — for example, *blue/red*.

### Parenthesis [​](#parenthesis)

Don't add important information in parentheses to describe it in detail.

## Dos and don'ts [​](#dos-and-don-ts)

* Don't use informal internet slang.
* Avoid usage of buzzwords and jargons.
* Avoid the usage of idioms and phrases.
* Don't start all sentences with the same phrase such as, *In order to, To do, You can*.
* It is good to use polite words such as *may,* and *might* — for example, *That might require you to pass the parameter*.
* Avoid the usage of requesting words such as, please, request — for example, *please use this method, please take a look at the below table*.
* Don't write the way you speak; speaking may be more colloquial and verbose. Instead, add a pinch of formal style with it to convey only enough information to our audience that is sufficient to perform their tasks. This avoids cluttering the page.

Apart from language style, proper fonts and formats must be chosen to promote readers' legibility. The following section covers what fonts and formats need to be used.

---

## Embedding external repositories

**Source:** https://developer.shopware.com/docs/resources/guidelines/documentation-guidelines/07-embedding-external-repositories.html

# Embedding external repositories [​](#embedding-external-repositories)

This guide will explain how to embed project documentation from your repository into the [Developer documentation](https://developer.shopware.com/).

[Developer Portal](https://github.com/shopware/developer-portal) is built using the [`shopware/developer-documentation-vitepress`](https://github.com/shopware/developer-documentation-vitepress) repository (`vitepress-shopware-docs` package). This setup heavily utilizes [Vitepress](https://vitepress.dev/) and incorporates custom Shopware features such as unique design, breadcrumbs, Algolia search, Copilot AI chat and recommendations, auto-built sidebar and more.

This portal serves as a central hub for all developer resources and documentation. However, the actual content is distributed across various repositories but integrated into the developer portal using the [Docs CLI](https://github.com/shopware/developer-documentation-vitepress/blob/main/CLI.md). This approach allows for decentralized content management, enabling the maintainers of each repository to manage their content independently.

## Configure Developer Portal [​](#configure-developer-portal)

To set up your local instance of the developer portal, clone Developer Portal repository and install the dependencies:

bash

```shiki
cd /www/shopware/
git clone https://github.com/shopware/developer-portal.git
cd developer-portal
pnpm i
```

We also want to create a new branch so we can test the integration first in the pull request, then merge it to the `main` branch and do production deployment.

bash

```shiki
git checkout -b feature/embed-meteor-icon-kit
```

### Docs CLI [​](#docs-cli)

Now access `./docs-cli` in the root of the `shopware/developer-portal` repository.

To start embedding a new repository, update `.vitepress/portal.json` and create a new entry in the `repositories` array. Then run the CLI and see if your repository is visible in the list - select it and continue by confirming the default settings.

bash

```shiki
./docs-cli manage
```

You should be able to preview your new content by running the Vitepress dev server and opening your defined URL in the browser using the below command.

bash

```shiki
pnpm dev
```

### Sidebar and main navigation [​](#sidebar-and-main-navigation)

The content is already there and published, but in most cases you will also want to have a sidebar dedicated for your section.

Open `.vitepress/navigation.ts` and update `sublinks` and `ignore` parameters to auto-build the sidebar based on your directory structure and frontmatter config.

If you also want to add it to the top-bar main menu, update the `navigation` accordingly.

### Algolia search [​](#algolia-search)

By default, contents are grouped under `General` section in the Algolia search using Algolia *facets*. You can configure that and group your articles together into a new section, or even create multiple new sections.

Update `sections: SwagSectionsConfig[]` with all the regex matches for your sections and define the title of new section displayed in the Algolia search modal.

javascript

```shiki
const sections: SwagSectionsConfig[] = [
    // ...
    {
        title: 'Meteor Icon Kit',
        matches: [
            '/resources/meteor-icon-kit/',
        ],
    },
];
```

### Edit links [​](#edit-links)

Every article has a `Edit this page on GitHub` link in the bottom left corner. Because we are embedding content from external repositories, we need to make sure that the link points to the correct repository and branch.

You can do that by updating `const embeds: SwagEmbedsConfig[]`.

javascript

```shiki
const embeds: SwagEmbedsConfig[] = [
    // ...
    {
        repository: 'meteor',
        points: {
            '/resources/meteor-icon-kit/': 'main',
        },
        folder: 'packages/icon-kit/docs',
    },
]
```

### Optional [​](#optional)

#### Copilot AI [​](#copilot-ai)

Update `themeConfig.swag.similarArticles.filter` with your settings for recommended articles in Copilot AI. This is only needed for repositories that are embedding multiple branches (versions) so that Copilot only uses articles from one version at the time.

#### Version switcher [​](#version-switcher)

Update `themeConfig.swag.versionSwitcher` with additional settings for your paths when you are embedding multiple branches (versions) from the same repository. This allows users to switch between different versions of the same article.

#### Color coding [​](#color-coding)

Update `themeConfig.swag.colorCoding` with your settings for color coding in the breadcrumbs. This is currently only used for Plugins and Apps in the `docs` repository.

#### Static assets [​](#static-assets)

When you also want to share static assets from your repository such as `.pdf` or `.zip` files (excluding statically linked images in articles), make sure to copy them in the `buildEnd` hook.

javascript

```shiki
export default {
    // ...
    async buildEnd() {
        // ...
        await copyAdditionalAssets([
            // meteor-icon-kit
            {
                src: './resources/meteor-icon-kit/public/icons/regular',
                dst: 'icons/regular',
            }
        ])
    }
}
```

### Production deployment [​](#production-deployment)

While we already added the repository to the Docs CLI, it is not included in the production build by default.

The new repository must be activated in `.github/scripts/mount.sh`. This script is needed to apply correct build config in production build and during PR workflows where custom `branch` or even `org` is used and switched to by overwriting environment variables.

sh

```shiki
# ...
BRANCH_METEOR_ICON_KIT=main
ORG_METEOR_ICON_KIT=shopware

# ...
./docs-cli.cjs clone \
 --ci \
 --repository shopware/meteor \
 --branch ${BRANCH_METEOR_ICON_KIT:-main} \
 --src packages/icon-kit/docs \
 --dst resources/meteor-icon-kit \
 --org ${ORG_METEOR_ICON_KIT:-shopware} \
 --root ../..
```

## Configure your repository [​](#configure-your-repository)

The Last step includes configuring your repository for better developer experience and integration with the Developer Portal. Let's switch to your repository.

bash

```shiki
cd ../docs
# or
cd /www/shopware/docs
```

### Shortcuts [​](#shortcuts)

You will want to create at least 3 scripts in `package.json` of your repository

* `docs:env` - Run this in the context of your repository and the script will either clone the `developer-portal` inside `../developer-portal` or pull changes from the remote, and install latest dependencies.
* `docs:link` - Mount documentation from your repository into your local `developer-portal` instance.
* `docs:preview` - Run Vitepress dev server from your local `developer-portal` instance.

Examples are available in [meteor](https://github.com/shopware/meteor/blob/main/package.json) (monorepo setup), [frontends](https://github.com/shopware/frontends/blob/main/package.json), [release](https://github.com/shopware/release-notes/blob/main/package.json) and [docs](https://github.com/shopware/docs/blob/main/package.json) repositories (all standard repos).

json

```shiki
{
  "scripts": {
    "docs:env": "[ -d \"../developer-portal\" ] && ../developer-portal/docs-cli.cjs pull || (git clone git@github.com:shopware/developer-portal.git ../developer-portal && pnpm i -C ../developer-portal)",
    "docs:link": "../developer-portal/docs-cli.cjs link --src . --dst docs --symlink",
    "docs:preview": "../developer-portal/docs-cli.cjs preview"
  }
}
```

### CI pipelines [​](#ci-pipelines)

Custom GitHub workflows are not needed anymore, but new repos need to be added to the `Shopware Dev Docs connector` app in `shopware` organization on GitHub, so the app can listen for GitHub events. Shopware Dev Docs connector GitHub app takes care of:

* Creating a commit status check in PRs.
* Triggering full integration check in `developer-portal`.
* Updating the status check based on the integration check outcome, with a dedicated preview URL.
* Triggering production deployment when `main` branch is updated.

## Commit changes and create a PR [​](#commit-changes-and-create-a-pr)

Once you have everything set up, commit your changes and create PRs for the `shopware/developer-portal` and your repository.

Usually, you will want to first preview the docs from the feature branch of your repository inside the Developer portal. You can do that by changing the environment variable of the default branch for your repository in the `.github/scripts/mount.sh` inside the `developer-portal`, review changes, and then switch back to `main` branch before merging.

For example, follow the instructions in the article above, and use the feature branch of your repository in production build.

bash

```shiki
BRANCH_METEOR_ICON_KIT=feature/embed-meteor-repo-to-developer-portal
```

shell

```shiki
cd /www/shopware/developer-portal/
git checkout -b feature/embeds-meteor-icon-kit
# apply changes
git commit -m "feat: embedded meteor repo"
```

Make changes in your feature branch of your repository.

shell

```shiki
cd /www/shopware/meteor/
git checkout -b feature/embed-meteor-repo-to-developer-portal
# apply changes
git commit -m "chore: updated shortcuts, set up pipeline for developer portal"
```

Then create a PR and once the Vercel preview inside `developer-portal` is ready and correct, merge feature branch in your repository.

shell

```shiki
cd /www/shopware/meteor/
git checkout main
git merge feature/embed-meteor-repo-to-developer-portal
```

Now switch back production branch for your repository to `main` in the `developer-portal`.

shell

```shiki
cd /www/shopware/developer-portal/
git checkout feature/embeds-meteor-icon-kit
# change BRANCH_METEOR_ICON_KIT=main inside .github/scripts/mount.sh
git commit -m "chore: switched back to main branch for meteor repo"
```

Once the PR is merged, the production build will be triggered and the changes will be live on the Developer Portal.

---

