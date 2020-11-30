from graphene import ObjectType, Field
from .types import UserType
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


class UserQuery(ObjectType):
    user_profile = Field(UserType)

    @login_required
    def resolve_user_profile(self, info, **kwargs):
        return info.context.user
