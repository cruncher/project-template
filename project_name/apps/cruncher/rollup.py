from compressor.templatetags.compress import CompressorNode
from django.contrib.staticfiles.storage import StaticFilesStorage as DjangoStaticFilesStorage
from django.template.base import Template
from django.conf import settings
from django.core.cache import cache
import datetime
import hashlib
import os
import subprocess


LAST_MOD_CACHE_KEY = 'global-last-mod-js-dt-{{project_name}}'


def compress(context, data, name):
    """
    Data is the string from the template (the list of js files in this case)
    Name is either 'js' or 'css' (the sekizai namespace)

    We basically just manually pass the string through the { % compress 'js' % } template tag
    """
    return CompressorNode(Template(data).nodelist, name, 'file').render({})


def rollup_compress(context, data, name):
    # inject some common scripts
    base_data = settings.ROLLUP_BASE + data

    # Sort lines into imports, then actual code.
    imports = []
    code = []

    for line in base_data.split('\n'):
        line = line.strip()
        if line.startswith('//'):
            continue
        elif line.startswith('import'):
            if line not in imports:
                imports.append(line)
        else:
            if line not in code:
                code.append(line)

    base_data = '\n'.join(imports + code)
    # Not compressing? use the non rolled up data
    if not settings.COMPRESS_ENABLED:
        return base_data

    # calculate a hash of last_modified_js_file + aggregated imports + code
    data_hash = hashlib.md5(
        (
            cache.get(LAST_MOD_CACHE_KEY, '') +
            base_data
        ).encode()
    ).hexdigest()

    # do we have a compressed version of this?
    cache_key = 'js-bunle-{}'.format(data_hash)
    minified_path = cache.get(cache_key)
    if minified_path is not None:
        return "import '{}';".format(minified_path)

    else:
        if settings.DEBUG:
            print(base_data)
            print('Last mod modifier', cache.get(LAST_MOD_CACHE_KEY, ''))
            print('-->', data_hash)

        # NOTE: We run this in the project static root, treat everything relative to here
        # i.e. /static/asdas -> ./asdas
        tmp_file_name = os.path.join(settings.STATIC_ROOT, 'tmp.{}.js'.format(data_hash))
        rollup_file_name = os.path.join(settings.STATIC_ROOT, 'rollup.{}.js'.format(data_hash))
        minified_file_name = os.path.join(settings.STATIC_ROOT, 'min.{}.js'.format(data_hash))

        with open(tmp_file_name, 'w') as tmp_file:
            tmp_file.write(base_data.replace(settings.STATIC_URL, './'))

        subprocess.check_output('{} {} --silent --format iife --file {}'.format(
            settings.ROLLUP_BIN,
            tmp_file_name,
            rollup_file_name
        ), shell=True, stderr=subprocess.STDOUT)
        # print(res)

        if os.path.exists(rollup_file_name):
            subprocess.check_output('{} {} -o {}'.format(
                settings.MINIFY_BIN,
                rollup_file_name,
                minified_file_name
            ), shell=True, stderr=subprocess.STDOUT)

            if os.path.exists(minified_file_name):
                url = minified_file_name.replace(settings.STATIC_ROOT, settings.STATIC_URL).replace('//', '/')
                cache.set(cache_key, url, None)
                # cleanup
                if os.path.exists(tmp_file_name):
                    os.unlink(tmp_file_name)
                if os.path.exists(rollup_file_name):
                    os.unlink(rollup_file_name)
                return "import '{}';".format(url)

        return base_data


class StaticFilesStorage(DjangoStaticFilesStorage):
    def post_process(self, paths, **options):
        last_modified_js_dt = datetime.datetime(1970, 1, 1)
        for name, data in paths.items():
            if name.lower().endswith('.js'):
                storage, _ = data
                last_modified_js_dt = max(last_modified_js_dt, storage.modified_time(name))

            yield name, name, False

        cache.set(LAST_MOD_CACHE_KEY, str(last_modified_js_dt), None)
