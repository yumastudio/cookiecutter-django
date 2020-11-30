import os
from django.conf import settings
from urllib.request import urlretrieve
from django.utils.html import format_html
from easy_thumbnails.files import generate_all_aliases
from django.core.files import File

AWS_ENABLED = 'storages' in settings.INSTALLED_APPS


def resolve_thumbnails(model, field):
    if not hasattr(model, field) or getattr(model, field).name == '':
        return None

    target = "{app_label}.{model_name}.{field}".format(
        app_label=model.__class__._meta.app_label,
        model_name=model.__class__.__name__,
        field=field
    )
    thumbnail_aliases = settings.THUMBNAIL_ALIASES[target]

    thumbnails = {}
    for key, value in thumbnail_aliases.items():
        width = value['size'][0]
        aspect = value['aspect']

        thumbnails.setdefault(aspect, {})[width] = (
            getattr(model, field)[key].url
        )

    return thumbnails


def get_file(field):
    is_local = not AWS_ENABLED
    if not is_local:
        tempname, _ = urlretrieve(field.url, "/tmp/" + field.name.split("/")[-1])
        file_path = tempname
    else:
        file_path = field.path
    return file_path, is_local


def copy_photo(photo, model, field):
    file_path, is_local = get_file(photo)
    _, file_extension = os.path.splitext(file_path)
    f = open(file_path, 'rb')

    getattr(model, field).save('{filename}{ext}'.format(
        filename=str(model.id),
        ext=file_extension
    ), File(f))
    generate_all_aliases(getattr(model, field), include_global=True)

    if not is_local:
        os.remove(file_path)


def get_photo_preview(photo, aspect, width):
    if photo:
        key = "aspect-%s-width-%s" % (aspect, width)
        return format_html("""
            <div>
                <img src="{src}" />
            </div>
        """.format(
            src=photo[key].url
        ))
    return None
