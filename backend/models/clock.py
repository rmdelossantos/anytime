from django.db import models    
from django.utils import timezone
from datetime import datetime, date

class Clock(models.Model):
    user = models.ForeignKey("User", related_name="user_clock",
                            on_delete=models.CASCADE,
                            null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    clocked_in = models.DateTimeField(null=True, blank=True)
    clocked_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "backend"

    def __repr__(self):
        return "<Clock [%s]: %s %s>" % (
            self.user, self.clocked_in, self.clocked_out)

    def __str__(self):
        return "[%s]: %s - %s" % (
            self.user, self.clocked_in_str, self.clocked_out_str)

    def __unicode__(self):
        return "[%s] %s: %s" % (self.user, self.clock_in, self.clock_out)

    @property
    def clocked_in_str(self):
        if self.clocked_in:
            t = timezone.localtime(self.clocked_in)
            return t.strftime("%B %d %Y, %I:%M %p")
        return ''

    @property
    def clocked_out_str(self):
        if self.clocked_out:
            t = timezone.localtime(self.clocked_out)
            return t.strftime("%B %d %Y, %I:%M %p")
        return ''

    @property
    def today(self):
        return 1

    @property
    def calc_hours_worked(self):
        if not self.clocked_in and not self.clocked_out:
            return 0
        elif self.clocked_in and not self.clocked_out:
            """
                case 1:
                    - if self.created_at__day < today => missing clockout log
                    - return 8 hours
                case 2: still no clock out for today, compute hours    
            """
            if self.created_at.day < date.today().day:
                return 8
            hour = self.clocked_out - datetime.now()
            return round(hour.total_seconds() / (60 * 60))
        else:
            hour = self.clocked_out - self.clocked_in
            return round(hour.total_seconds() / (60 * 60))
                     
