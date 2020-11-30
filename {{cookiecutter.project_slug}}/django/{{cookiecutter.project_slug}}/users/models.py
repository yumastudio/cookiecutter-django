from django.contrib.auth.models import AbstractUser
from dynamic_filenames import FilePattern
from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    avatar = ThumbnailerImageField(upload_to=FilePattern(
        filename_pattern='{app_label}/{model_name}/{instance.id}{ext}'
    ), blank=True)
