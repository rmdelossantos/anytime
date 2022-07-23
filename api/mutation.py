import graphene
from backend.models import User, Clock
from backend.utils import (is_valid_email, is_valid_password, get_dt_range, render_dtrange)
from api.fields import UserType, ClockType
from graphql_jwt.decorators import login_required
import graphql_jwt
import json
from graphql import GraphQLError
from datetime import date, datetime, timedelta
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
    def mutate(root,info, user=None):
        try:
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
            try:
                user_instance = User.objects.create_user(**creation_kwargs)
            except:
                raise ValueError("There was a problem creating the user")

            return CreateUser(user=user_instance)
        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")  

class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType, token=graphene.String(required=True))

    @staticmethod
    def mutate(root,info):
        user = info.context.user
        clocked_in = datetime.now()
        if not user.is_authenticated:
            raise ValueError("Authentication failed.")


        clock_objs = Clock.objects.filter(user=user)
        if not clock_objs:
            # no clock object
            clock = Clock.objects.create(user=user, created_at=clocked_in, clocked_in=clocked_in)           
            return ClockIn(clock=clock)

        latest_clock = clock_objs.latest('created_at')
        if latest_clock and latest_clock.clocked_in and not latest_clock.clocked_out:
            # if latest clock object is already clocked in and still not clocked out, raise Exception
            raise Exception("Youre trying to clock in with still your previous clock entry not clocked out.")

        elif latest_clock and latest_clock.clocked_in and latest_clock.clocked_out:
            # if latest clock object is already clocked out, user can create another entry
            try:
                clock = Clock.objects.create(user=user, created_at=clocked_in, clocked_in=clocked_in)
                return ClockIn(clock=clock)
            except Exception:
                raise Exception("There was a problem creating a clock entry.")


class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType, token=graphene.String(required=True))

    @staticmethod
    def mutate(root,info):
        user = info.context.user
        clocked_out = datetime.now()

        if not user.is_authenticated:
            print('went here')
            raise ValueError("Authentication failed.")

        clock_objs = Clock.objects.filter(user=user)
        if not clock_objs:
            # if latest clock object has no clock in entry, raise Exception
            raise Exception("You're trying to clock out without a clock entry")

        latest_clock = clock_objs.latest("created_at")    

        if latest_clock and latest_clock.clocked_out:
            # if latest clock object has no clock in entry, raise Exception
            raise Exception("Your latest clock entry has already been clocked out. You need to clock in before clocking out.")
        
        elif latest_clock and (latest_clock.clocked_in and not latest_clock.clocked_out):    
            latest_clock.clocked_out = clocked_out
            latest_clock.save()

        return ClockOut(clock=latest_clock)

