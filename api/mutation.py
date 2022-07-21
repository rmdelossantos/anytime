import graphene
from api.custom_scalar import GenericScalar
from backend.models.user import User
from backend.utils import (is_valid_email, is_valid_password)
from api.fields import UserType
import json

class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)

class ClockEntryInput(graphene.InputObjectType):
    current_time = graphene.DateTime(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        user = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root,info,user=None):

        if not is_valid_email(user.email):
            raise ValueError("The email provided is not valid. Please try again.")
        
        is_email_in_use = User.objects.filter(email=user.email).exists()
        if is_email_in_use:
            raise ValueError("The email provided is already in use. Please try another email.")

        is_pw_valid, error_message = is_valid_password(user.password)
        if not is_pw_valid:
            raise ValueError(error_message)     

        is_username_in_use = User.objects.filter(username=user.username).exists()
        if is_username_in_use:
            raise ValueError("The username provided isn't available. Please try another username")

        creation_kwargs = {
            'username': user.username,
            'email': user.email,
            'password': user.password
        }    
        
        user_instance = User.objects.create_user(**creation_kwargs)
        return CreateUser(user=user_instance)        

class ClockIn(graphene.Mutation):
    class Input:
        time = graphene.DateTime(required=True)

    user = graphene.Field(UserType, token=graphene.String(required=True))

    @staticmethod
    def mutate(root,info,time=None):
        return ClockIn(user=User.objects.get(username='admin'))

        