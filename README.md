# Project for AnyMind Group Application

Repo of the Python technical project for AnyMind Group application process \
I called this AnyTime (pun intended 😉)

## Setup

Clone repo\
`git clone <repo>`

Create virtual env

- I used virtualenv, but feel free to use what suits you.

`python -m venv venv`

Activate venv\
`source venv/bin/activate`

Install dependencies\
`pip install -r requirements`

Create database

- Make a file named db.sqlite3 in the project root directory.

Run the migrations

`python manage.py migrate`

Run the server

`python manage.py runserver`


Try the queries in GraphiQL by going to http://localhost:port_number/graphql/ (default port_number = 8000)
## Queries

Get current user

```graphql
query{
  me (token: $token) {
    id
    username
    email
  }
}
```

Get clock details for the current day

```graphql
query{
  currentClock(token: $token){
    clockedIn
    clockedOut
  }
}
```

Get clocked hours for the current day, week, and month

```graphql
query{
  clockedHours (token: $token) {
    today
    currentWeek
    currentMonth
  }
}
```

## Mutations

Create a user

```graphql
mutation createMutation {
    createUser(user: {username: $username, password: $password, email: $email}) {
        user{
            id
        } 
    }
}

```
Obtain JWT token
```graphql
mutation createMutation {
    obtainToken(username :$username, password: $password) {
        token
        payload
        refreshExpiresIn
    }
}
```
Obtain JWT Token
```graphql
mutation createMutation {
    obtainToken(username :$username, password: $password) {
        token
        payload
        refreshExpiresIn
    }
}
```
Clock in
```graphql
mutation createMutation {
 	clockIn {
        clock(token: $token) {
            id
            clockedIn
            clockedOut
        }
        message
}
```
Clock out
```graphql
mutation createMutation {
 	clockOut {
        clock(token: $token) {
            id
            clockedIn
            clockedOut
        }
        message
}
```

## Create Superuser
I assigned user roles in the User model. Superuser has a user_role ADMIN in the model.\
Normal user has a user_role EMPLOYEE.\
To create a super user and view the Django admin dashboard,

Run createsuperuser, then input the creds\
`python manage.py createsuperuser`

Run the shell
`python manage.py shell`

Run the following in the shell
```ipython
from backend.models import User
user = User.objects.get(username=<username>)
user.user_role="AD"
user.save()
```

User and Clock models are available in Django admin

## Applicant Notes
- I added validation to email format and password requirements
- I don't know the other rules for clocking in  or out so I filled in the gaps:
    - If user clocks in today without a clock out yesterday, yesterdays Clock entry will have full 8 hours of work.
    - If user clocks out today without a clock in entry, Clock entry will have full 8 hours of work.
- Wanted to add design a frontend, I overthought a Figma design. Will just continue in another branch, some other time.
