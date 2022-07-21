import re

def is_valid_email(email):
    if len(email) > 7:
        # From https://emailregex.com/
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

