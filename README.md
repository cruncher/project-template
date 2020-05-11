A Django project template

* nginx, supervisord, gunicorn configuration
* PostrgreSQL

Usage:

    django-admin.py startproject --template=https://github.com/cruncher/project-template/zipball/master --extension=conf,py,sh,py-template  new_project_name


# {{project_name}}

`https://{{project_name}}.ch/` – prod

`https://{{project_name}}.cruncher.ch/` – staging

`https://{{project_name}}.cruncher.ch/static/index.html` – styleguide


## Project structure

`{{project_name}}/source/`

Contains source files for building front-end assets. The `source/` directory
is only served in local development. It requires `settings/local.py` to contain:

```python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

DEV_STATIC_URLS = {
    r'^static/(?P<path>.*)$': os.path.join(BASE_DIR, 'static'),
    r'^source/(?P<path>.*)$': os.path.join(BASE_DIR, 'source'),
}
```

The `templates/base.html` template contains conditionals that serve source files
when `debug` is true, otherwise static files. To set `debug`, `settings_local.py`
must contain local IPs:

```
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
```

`{{project_name}}/static/`

Static files for production.


## Building front-end resources

From the project directory `{{project_name}}/`...

`npm install`

Installs the node dependencies listed in `package.json`.

`npm run build-css`

Builds CSS assets from `source/style.css` to `static/style.min.css`.

`npm run build-module`

Builds JS modules from `source/module.js` to `static/module.rolled.js`.

`npm run build-docs`

Builds documentation – a component styleguide – from `source/index.template.html`
to `static/index.html`. Front-end documentation is served at `/static/index.html`.

`npm run build-sass`

The project contains very little SASS. It is used only to preprocess a few media
query breakpoints from files in `source/sass/` to `source/components/`. Should
you need to modify the breakpoints found in `source/sass/var.scss` you should
run this command manually and commit prior to the next build/deploy.


## Writing a front-end component

Components live in a flat hierarchy inside `source/components`. Both the CSS
and JS for a component (if your component has both) should share a file
name. If your component is called `my-thingummy`, the files should be named:

```
source/components/my-thingummy.css
source/components/my-thingummy.js
```

Stylesheets are included in the project by listing them as imports in `source/style.css`.

JS modules are included in the project by importing them in `source/module.js`.

There is a CSS component template at `source/components/_component.css`.


## Writing front-end documentation

Comments in both CSS and JS files may be compiled as documentation. Documentation
comments should follow the pattern:

```css
/**
.component-class

```` ```html
<div class="component-class">Example HTML</div>
```` ```

Text description in markdown.
**/
```

The same pattern may be followed in JS:

```js
/**
functionName(param1, param2)

```` ```js
<div class="component-class">Example HTML</div>
```` ```

Text description in markdown.
**/
```

You must add files containing documentation comments to the relevant section
of `source/index.template.html`. It which uses [Sparky](https://stephen.band/sparky)
templates to generate html.
