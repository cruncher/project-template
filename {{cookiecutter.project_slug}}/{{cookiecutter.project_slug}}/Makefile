DEBUG=

# Tell make to ignore existing folders and allow overwriting existing files
.PHONY: modules literal

# Must format with tabs not spaces
literal:
    deno run --allow-read --allow-env --allow-net --allow-write --allow-run --unstable ./static/literal/deno/make-literal.js ./static/

modules:
    rm -rf static/build
    deno run --allow-read --allow-env --allow-net --allow-write --allow-run ./static/fn/deno/make-modules.js static/build/ \
        static/project_name/module.js \
        static/project_name/module.css
