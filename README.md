# mkdocs-backlinks

This is a plugin for adding backlinks to your mkdocs generated pages.

Mkdocs is an awesome tool not only for documentation, but also for publishing [digital gardens](https://danodic.dev).
Backlinks are a desirable component when building such digital gardens, as they enable the ability to explore content
based on how the knowledge interconnects instead of just looking at page navigation.

## Setup

Install the plugin using pip:

`pip install mkdocs-backlinks`

Activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - mkdocs-backlinks
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin.
> MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

* `ignored_pages` - A list of page titles that will be excluded from the backlinks.

```yaml
plugins:
  - mkdocs-backlinks:
      ignored_pages: [ 'Tags', 'Home' ] 
```

## Usage

This plugin will add a `backlinks` attribute to the Jinja page context, which can be used to add backlinks at any point
in your template. Here is an example of it:

```html
...

{% if backlinks %}
<h3>Backlinks:</h3>
<ul>
    {% for backlink in backlinks %}
    <li><a href="/{{ backlink.url }}">{{ backlink.title }}</a></li>
    {% endfor %}
</ul>
{% endif %}

...
```

That means **you need to have a template that supports backlinks**, or you can alter the template you are using with the
snippet above.

### Writing Notes

I have been using this to publish my Obsidian vault, and there are some _tricks_ to make it work well:

- Obsidian is smart and will resolve links even if they don´t refer to a valid file path. This is not
  true for mkdocs and the backlinks plugin -- you need to write valid links in your markdown files, either
  absolute or relative links.
- Absolute links are absolute related to the root of the `/docs` folder, not to your computer filesystem.

Following those two rules will allow you to go straight from obsidian to mkdocs with cool backlinks.

## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/

[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables

[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks

## Thanks to

- The creator of this awsome mkdocs plugin template: https://github.com/byrnereese/mkdocs-plugin-template
