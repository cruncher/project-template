import datetime
import hashlib
import logging
import os
import subprocess

from compressor.templatetags.compress import CompressorNode

from django.conf import settings
from django.contrib.staticfiles.storage import (
    StaticFilesStorage as DjangoStaticFilesStorage,
)
from django.core.cache import cache
from django.template.base import Template
from django.utils.timezone import now as utc_now


LAST_MOD_CACHE_KEY = "global-last-mod-js-dt-{{project_name}}"

logger = logging.getLogger("rollup")


def compress(context, data, name):
    """
    Data is the string from the template (the list of js files in this case)
    Name is either 'js' or 'css' (the sekizai namespace)

    We basically just manually pass the string through the compress template tag
    """

    # Handle 'scripts' as js files
    name_ = name
    if name == "scripts":
        name_ = "js"
    return CompressorNode(Template(data).nodelist, name_, "file").render({})


def rollup_compress(context, data, name):
    skip_cache_ = "rollup-skip-cache" in context.get("request").get_full_path()

    # inject some common scripts
    base_data = settings.ROLLUP_BASE + data

    # Sort lines into imports, then actual code.
    imports = []
    code = []

    for line in base_data.split("\n"):
        line = line.strip()
        if line.startswith("//"):
            continue
        elif line.startswith("import"):
            if line not in imports:
                imports.append(line)
        else:
            if line not in code:
                code.append(line)

    safe_base_data = "\n".join(imports) + "\n".join(code)

    # Not compressing? use the non rolled up data
    if not settings.COMPRESS_ENABLED:
        return safe_base_data

    # Fix path of imports so that rollup can find its own
    base_data = "\n".join(imports).replace(settings.STATIC_URL, "./") + "\n".join(code)

    # calculate a hash of last_modified_js_file + aggregated imports + code
    data_hash = hashlib.md5(
        (cache.get(LAST_MOD_CACHE_KEY, "") + base_data).encode()
    ).hexdigest()

    # do we have a compressed version of this?
    cache_key = "js-bunle-{}".format(data_hash)
    if skip_cache_:
        minified_path = None
    else:
        minified_path = cache.get(cache_key)

    if minified_path is not None:
        return "import '{}';".format(minified_path)

    else:
        logger.debug("Base data:\n{}\n".format(base_data))
        logger.debug("Last mod modifier: ")
        logger.debug("--> Ref hash: ")

        # NOTE: We run this in the project static root,
        # treat everything relative to here
        # i.e. /static/asdas -> ./asdas
        tmp_file_name = os.path.join(
            settings.STATIC_ROOT, "tmp.{}.js".format(data_hash)
        )
        rollup_file_name = os.path.join(
            settings.STATIC_ROOT, "rollup.{}.js".format(data_hash)
        )
        minified_file_name = os.path.join(
            settings.STATIC_ROOT, "min.{}.js".format(data_hash)
        )
        config_file_path = os.path.join(settings.BASE_DIR, "static", "rollup.config.js")

        with open(tmp_file_name, "w") as tmp_file:
            tmp_file.write(base_data)

        rollup_command = "{} {} -c {} --format iife --file {}".format(
            settings.ROLLUP_BIN, tmp_file_name, config_file_path, rollup_file_name
        )
        logger.debug("Rolling up: {}".format(rollup_command))
        try:
            res = subprocess.check_output(
                rollup_command, shell=True, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            logger.exception(e.output.decode())
            return safe_base_data
        else:
            if settings.DEBUG:
                print("Rollup:\t\t✅")

            logger.debug(res.decode())

        if os.path.exists(rollup_file_name):
            if settings.MINIFY_BIN:
                minify_command = "{} {} -o {}".format(
                    settings.MINIFY_BIN, rollup_file_name, minified_file_name
                )
            else:
                minify_command = "cp {} {}".format(rollup_file_name, minified_file_name)
            logger.debug("Minifying: {}".format(minify_command))
            env = os.environ.copy()
            env["BABELRC_PATH"] = os.path.join(settings.BASE_DIR, ".babelrc")
            try:
                res = subprocess.check_output(
                    minify_command, shell=True, stderr=subprocess.STDOUT, env=env
                )
            except subprocess.CalledProcessError as e:
                logger.exception(e.output.decode())
                return safe_base_data
            else:
                logger.debug(res.decode())

            if os.path.exists(minified_file_name):
                url = minified_file_name.replace(
                    settings.STATIC_ROOT, settings.STATIC_URL
                ).replace("//", "/")
                cache.set(cache_key, url, None)
                # cleanup
                if os.path.exists(tmp_file_name):
                    os.unlink(tmp_file_name)
                if os.path.exists(rollup_file_name):
                    os.unlink(rollup_file_name)

                if settings.DEBUG:
                    print("Minified:\t✅")
                return "import '{}';".format(url)

        return base_data


class StaticFilesStorage(DjangoStaticFilesStorage):
    def post_process(self, paths, **options):
        last_modified_js_dt = utc_now() - datetime.timedelta(days=10000)

        for name, data in paths.items():
            if name.lower().endswith(".js"):
                storage, _ = data
                last_modified_js_dt = max(
                    last_modified_js_dt, storage.get_modified_time(name)
                )

            yield name, name, False

        cache.set(LAST_MOD_CACHE_KEY, str(last_modified_js_dt), None)
