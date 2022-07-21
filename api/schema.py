import graphene
import graphene_django
from api.fields import UserType
from backend.models import User
from api.mutation import ClockIn, CreateUser
from graphene.types.generic import GenericScalar
import random

import graphene
from graphql_jwt.decorators import login_required
import graphql_jwt


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    me = graphene.Field(UserType, user_id=graphene.Int())

    def resolve_generic(self, info, **kwargs):
        return User.objects.get(pk=0)
        return {}

    def resolve_all_users(self, info, **kwargs):
        print(User.objects.all())
        return User.objects.all()

    def resolve_me(self, info, user_id):
        return User.objects.get(pk=user_id)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    clock_in = ClockIn.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)