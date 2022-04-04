import os

from django.shortcuts import Http404, render


def template_folder(request, path, document_root="", show_indexes=False):
    try:
        return render(request, os.path.join(document_root, path))
    except IsADirectoryError:
        raise Http404
