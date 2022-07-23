import graphene
from graphene_django import DjangoObjectType
from backend.models import User, Clock
from graphene.types.generic import GenericScalar
from backend.utils import render_dtrange, get_dt_range
from datetime import datetime, date


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
class ClockType(DjangoObjectType):

    class Meta:
        model = Clock
        fields = "__all__"

class ClockedHoursType(DjangoObjectType):

    today = graphene.Int()
    current_week = graphene.Int()
    current_month = graphene.Int()

    class Meta:
        model = Clock
        fields = "__all__" 

    def resolve_today(self, info):
        """
            Queries Clock object created today, with clocked in value, else return 0
        """
        user = info.context.user
        try:
            dtrange = get_dt_range('Today')
            clock_objs = Clock.objects.filter(user=user,created_at__range=dtrange)
            total_hours = 0
            for obj in clock_objs:
                total_hours += obj.calc_hours_worked
            return total_hours   
        except Clock.DoesNotExist:
            return 0    
        except Exception:
            raise Exception("Something went wrong while getting hours worked today.")    
        return clock_obj.calc_hours_worked

    def resolve_current_week(self, info):
        """
            Queries Clock objects created using date range
            Start of the current week is Sunday
            If today is Sunday, function returns only the hours worked on Sunday
        """
        try:
            user = info.context.user
            dtrange = get_dt_range('Week')
            clock_objs = Clock.objects.filter(user=user, created_at__range=dtrange)
            total_hours = 0
            for obj in clock_objs:
                total_hours += obj.calc_hours_worked
            return total_hours   
        except Exception:
            raise Exception("Something went wrong while getting hours worked for this week.")  
    def resolve_current_month(self, info):
        """
            Queries Clock objects created using date range
        """
        try:
            user = info.context.user
            dtrange = get_dt_range('Month')
            clock_objs = Clock.objects.filter(user=user, created_at__range=dtrange)
            total_hours = 0
            for obj in clock_objs:
                total_hours += obj.calc_hours_worked
            return total_hours           
        except Exception:
            raise Exception("Something went wrong while getting hours worked for this month.")  
