DEBUG=

# Tell make to ignore existing folders and allow overwriting existing files
.PHONY: modules literal

# Must format with tabs not spaces
literal:
    deno run --allow-read --allow-env --allow-net --allow-write --allow-run --unstable ./static/literal/deno/make-literal.js ./static/ debug

site:
    rm -rf static/build
    deno run --allow-read --allow-env --allow-net --allow-write --allow-run ./static/fn/deno/make-modules.js static/build/ static/site/module.css static/bolt/elements/slide-show/shadow.css static/bolt/elements/overflow-toggle/shadow.css  static/site/module.js
