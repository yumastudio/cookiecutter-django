from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            from easy_thumbnails.signals import saved_file
            from easy_thumbnails.signal_handlers import generate_aliases_global

            saved_file.connect(generate_aliases_global)
        except ImportError:
            pass
