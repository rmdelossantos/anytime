from multiprocessing.sharedctypes import Value
import re
from datetime import datetime, date, timezone, time, timedelta
import pytz

tz = pytz.timezone('Asia/Manila')

def is_valid_email(email):
    if len(email) > 7:
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_regex, email) != None:
            if len(email.split('@')) == 2:
                domain = email.split('@')[1]
                if len(domain.split('.'))  >= 2:
                    return True
    return False

def is_valid_password(password):
    special_char = ["!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "{", "|", "}" , "~"]
      
    if len(password) < 6:
        return False, 'Password should have at least 6 characters'
          
    elif not any(char.isdigit() for char in password):
        return False, 'Password should have at least 1 number'
          
    elif not any(char.isupper() for char in password):
        return False, 'Password should have at least one uppercase letter'
          
    elif not any(char.islower() for char in password):
        return False, 'Password should have at least one lowercase letter'
          
    elif not any(char in special_char for char in password):
        return False, 'Password should have at least one special character'
    
    else:
        return True, ''

def render_dtrange(start,end):
    curr_date_start= tz.localize(datetime.combine(start, time.min))
    curr_date_end = tz.localize(datetime.combine(end, time.max))
    dtrange = (curr_date_start, curr_date_end)
    return dtrange

def get_dt_range(summary):
    dtrange = None
    if summary == 'Today':
        dtrange = render_dtrange(date.today(), date.today())   
    elif summary == 'Week':
            sunday_index = (date.today().weekday() + 1) % 7 
            start = date.today() - timedelta(days=sunday_index)
            end = date.today()
            dtrange = render_dtrange(start, end)
    elif summary == 'Month':
        # set day to 1st of the current month and year
        start = date(date.today().year, date.today().month, 1)
        # compute last day of the current month (28,29,30,31)
        end = date(start.year + start.month // 12, 
                    start.month % 12 + 1, 1) - timedelta(1)
        dtrange = render_dtrange(start, end)
    else:
        raise ValueError('Invalid timesheet summary type requested.')
  
    return dtrange    