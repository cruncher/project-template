import glob
import os

from django.conf import settings
from django.shortcuts import Http404, render
from django.template.exceptions import TemplateDoesNotExist


def template_folder(request, path, document_root="", show_indexes=False):
    if not settings.DEBUG:
        raise Http404

    actual_path = os.path.join(document_root, path)
    try:
        return render(request, actual_path)
    except TemplateDoesNotExist:
        raise Http404
    except IsADirectoryError:
        if show_indexes:
            template_dir = os.path.abspath(settings.TEMPLATES[0].get("DIRS")[0])
            dir = os.path.abspath(os.path.join(template_dir, document_root))

            templates = glob.glob(dir + "/*.html")
            templates.remove(dir + "/_index.html")
            templates = [t.replace(template_dir, "") for t in templates]

            return render(
                request,
                "test/_index.html",
                context={"index_templates": templates, "path": document_root},
            )

        raise Http404
