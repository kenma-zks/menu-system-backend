from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from asyncio.windows_events import NULL

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password = None, is_active = True, is_staff= False, is_admin = False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name:
            raise ValueError('Users must have a first name')
        if phone_number == NULL:
            raise ValueError('Users must have a phone number')
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, phone_number, password = None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone_number,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password = None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone_number,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user

class SubAdmin(AbstractBaseUser):
    id = models.AutoField(primary_key = True)
    email = models.EmailField(max_length = 255, unique = True)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    phone_number = models.CharField(max_length = 255)
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = True)
    admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

