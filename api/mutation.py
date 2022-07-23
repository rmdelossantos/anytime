import graphene
from backend.models import User, Clock
from backend.utils import (is_valid_email, is_valid_password)
from api.fields import UserType, ClockType
from graphql_jwt.decorators import login_required
import graphql_jwt
import json
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
            
            user_instance = User.objects.create_user(**creation_kwargs)
            return CreateUser(user=user_instance)
        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")  

class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType, token=graphene.String(required=True))
    message = graphene.String()

    @staticmethod
    def mutate(root,info):
        try:
            user = info.context.user
            print(user)
            if not user.is_authenticated:
                raise ValueError("Authentication failed.")

            yesterday = date.today() - timedelta(days=1)
            message=None
            # check yesterday's clock 
            try:
                yesterday_clock_obj = Clock.objects.get(user=user , created_at__day=yesterday.day, clocked_in__day=yesterday.day)
                if yesterday_clock_obj and (yesterday_clock_obj.clocked_in and not yesterday_clock_obj.clocked_out):
                    message = "Missing clocked out log from yesterday. System assigned clocked out log equivalent to 8 hours."
                    yesterday_clock_obj.clocked_out = yesterday_clock_obj.clocked_in + timedelta(hours=8)
                    yesterday_clock_obj.save()
            except Clock.DoesNotExist:
                pass
            try:
                clock = Clock.objects.get(user=user,created_at__day=date.today().day, clocked_in__day=date.today().day)
                if clock.clocked_in:
                    message="You have already clocked in."
                    return ClockIn(clock=clock, message=message)

            except Clock.DoesNotExist:
                clocked_in = datetime.now()
                clock = Clock.objects.create(user=user, created_at=clocked_in, clocked_in=clocked_in)
                
            return ClockIn(clock=clock, message=message)

        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")  

class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType, token=graphene.String(required=True))
    message = graphene.String()

    @staticmethod
    def mutate(root,info):
        try:
            user = info.context.user
            print(user)
            if not user.is_authenticated:
                print('went here')
                raise ValueError("Authentication failed.")
            message=''
            try:    
                clocked_out = datetime.now()
                clock = Clock.objects.get(user=user,created_at__day=date.today().day, clocked_in__day=date.today().day)
                if clock.clocked_out:
                    message = "You have already clocked out."
                    return ClockOut(clock=clock, message=message)

            except Clock.DoesNotExist:
                # forgot to clock in today
                clocked_in = clocked_out - timedelta(hours=8)
                clock = Clock.objects.create(user=user,created_at__day=date.today().day, clocked_in=clocked_in)
                message = "Missing clocked in log for today. System assigned clocked in log equivalent to 8 hours."
            clock.clocked_out = clocked_out
            clock.save()
            return ClockOut(clock=clock, message=message)

        except Exception as e:
            print(e)
