import os
from tempfile import NamedTemporaryFile

import requests
from filer.models.filemodels import File
from filer.models.imagemodels import Image

from django.core.files import File as BaseFile


IMAGE_TYPES = ("jpg", "jpeg", "png", "tiff", "tif", "gif")


def url_to_filer(url, folder=None, headers=None):
    if any([url.strip().lower().endswith(it) for it in IMAGE_TYPES]):
        cls_ = Image
    else:
        cls_ = File

    name = url.rsplit("/", 1)[-1]

    try:

        inst = cls_.objects.filter(name__exact=name).first()
        inst.file._require_file()
        assert b"DOCTYPE HTML" not in inst.file.read(100)

        return inst
    except Exception:
        pass
    
    with NamedTemporaryFile() as tempfile:
        with requests.get(url, headers=headers, stream=True) as img_res:
            for chunk in img_res.iter_content(chunk_size=1024):
                tempfile.write(chunk)

        tempfile.flush()

        doc_ = cls_.objects.create(folder=folder, name=name)
        doc_.file.save(doc_.name, BaseFile(tempfile))
        doc_.file_data_changed()
        doc_.save()

        return doc_


def local_file_filer(path, folder=None, headers=None):
    assert os.path.exists(path)
    with open(path, "rb") as basefile:
        if path.lower().rsplit(".", 1)[-1] in IMAGE_TYPES:
            cls_ = Image
        else:
            cls_ = File

        doc_ = cls_.objects.create(folder=folder, name=path.rsplit("/", 1)[-1])
        doc_.file.save(doc_.name, BaseFile(basefile))
        doc_.file_data_changed()
        doc_.save()

        return doc_
