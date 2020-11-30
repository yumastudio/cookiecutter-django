import graphene
from graphql_jwt import JSONWebTokenMutation, Verify
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from graphql_jwt.mixins import RefreshMixin
from graphql_social_auth import SocialAuthMutation
from graphql_social_auth.mixins import JSONWebTokenMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from config.errors import GraphQLError
from .types import UserType


User = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        full_name = graphene.String(required=True)

    def mutate(self, info, email, password, full_name, **kwargs):
        user = info.context.user
        email = email.strip()
        if user.is_authenticated:
            raise Exception(GraphQLError.CREATE_USER_NOT_ALLOWED)
        if User.objects.filter(username=email).exists():
            raise Exception(GraphQLError.EMAIL_ALREADY_EXISTS)

        user = User.objects.create_user(
            email,
            email,
            password
        )

        splitted_full_name = full_name.strip().split(" ")
        first_name = splitted_full_name[0]
        last_name = ' '.join(splitted_full_name[1:]).strip()

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return CreateUser(user=user)


class UpdateUserPassword(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user

        if check_password(kwargs['old_password'], user.password):
            user.password = kwargs['new_password']
        else:
            raise Exception(GraphQLError.OLD_PASSWORD_DOESNT_MATCH)

        user.save()

        return UpdateUserPassword(user=user)


class LoginEmail(JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        user.last_login = timezone.now()
        user.save()
        return cls(user=info.context.user)


class LoginSocial(JSONWebTokenMixin, SocialAuthMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        user = social.user
        user.last_login = timezone.now()
        user.save()
        info.context.user = user
        return cls(user=social.user, token=get_token(social.user))


class RefreshToken(RefreshMixin, graphene.Mutation):
    class Arguments(RefreshMixin.Fields):
        """Refresh Arguments"""

    @classmethod
    def mutate(cls, *arg, **kwargs):
        res = cls.refresh(*arg, **kwargs)
        User.objects.filter(username=res.payload['username']).update(last_login=timezone.now())
        return res


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user_password = UpdateUserPassword.Field()
    login_email = LoginEmail.Field()
    login_social = LoginSocial.Field()
    verify_token = Verify.Field()
    refresh_token = RefreshToken.Field()
