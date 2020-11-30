from graphene import Field
from graphene_django.types import DjangoObjectType
from config.types import CustomJSON
from {{cookiecutter.project_slug}}.utils.functions import resolve_thumbnails
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password', )

    avatar = Field(CustomJSON)

    def resolve_avatar(self, info):
        return resolve_thumbnails(model=self, field='avatar')
