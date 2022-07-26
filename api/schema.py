import graphene
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphql_jwt
from django.views.decorators.csrf import csrf_exempt

from backend.models import User, Clock

from api.fields import ClockType, UserType, ClockedHoursType
from api.mutation import ClockIn, ClockOut, CreateUser

import random
from datetime import datetime, date, timedelta


class Query(graphene.ObjectType):
    # authenticated queries
    me = graphene.Field(UserType, token=graphene.String(required=True))
    current_clock = graphene.Field(ClockType, token=graphene.String(required=True))
    clocked_hours = graphene.Field(ClockedHoursType, token=graphene.String(required=True))
    
    @login_required
    def resolve_me(self, info, **kwargs):
        try:
            user = info.context.user

            if not user.is_authenticated:
                raise Exception("Authentication credentials were not provided.")

            if user.is_anonymous:
                raise Exception('Authentication failed.')

            return User.objects.get(pk=user.id)

        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")
            
    @login_required
    def resolve_current_clock(self, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication failed.")

            if user.is_anonymous:
                raise Exception('Authentication failed.')
            try:    
                clock = Clock.objects.filter(user=user, clocked_out=None).latest("created_at")
            except Clock.DoesNotExist:
                return None    
                
            return clock
        
        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")
                

    @login_required
    def resolve_clocked_hours(self, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication failed.")
            if user.is_anonymous:
                raise Exception('Authentication failed.')

            yesterday = date.today() - timedelta(days=1)
            test = ClockedHoursType()
            return test
        
        except Exception as e:
            print(e)
            raise Exception("Something went wrong.")    

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)