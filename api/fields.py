import graphene
from graphene_django import DjangoObjectType
from backend.models import User
from graphene.types.generic import GenericScalar


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
