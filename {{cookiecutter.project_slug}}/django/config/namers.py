import os


def alias(thumbnailer, thumbnail_options, source_filename,
            thumbnail_extension, **kwargs):
    """
    Generate filename based on thumbnail alias name (option ``THUMBNAIL_ALIASES``).
    For example: ``source.jpg.medium_large.jpg``
    """
    filename, file_extension = os.path.splitext(source_filename)
    name = "/".join([
        filename,
        "aspect",
        thumbnail_options['aspect'],
        "width",
        str(thumbnail_options['size'][0]) + "." + thumbnail_extension
    ])
    return name
