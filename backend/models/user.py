from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin )
from django.db import models    

class UserManager(BaseUserManager):

    def create_user(self, username, password, email, role='ME'):

        is_superuser = False


        user = self.model(username=username, email=email)
        if role == 'AD':
            print('went here')
            user.is_superuser = True
            user.user_role=role

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **extra_fields):
        return self.create_user(username, password, '', 'AD')

class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'AD'
    EMPLOYEE = 'ME'

    USER_ROLES = (
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee')
    )

    email = models.EmailField(null=True)
    username = models.CharField(max_length=32, unique=True)
    user_role = models.CharField(
        max_length=5, choices=USER_ROLES, default='ME')

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        app_label = "backend"

    def __repr__(self):
        return "<User [%d]: %s %s>" % (
            self.id, self.email, self.username)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return "[%d] %s: %s" % (self.id, self.email, self.username)

    def has_perm(self, perm, obj=None):
        """"
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm_list, obj=None):
        """"
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True      

    @property
    def is_staff(self):
        return self.user_role == 'AD'       