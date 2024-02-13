from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from account.managers.user_account_manager import *
from django.utils.translation import gettext_lazy as _



class UserAccount(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255, verbose_name=_('First Name'),null=False,blank=False)
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'), null=False, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False, max_length=255, verbose_name=_('Email'))

    is_active = models.BooleanField(default=True,null=False, blank=False)
    is_staff = models.BooleanField(default=False,null=False, blank=False)
    is_superuser = models.BooleanField(default=False,null=False, blank=False)

    is_freelancer = models.BooleanField(default=False,null=False, blank=False)
    bio = models.TextField(blank=True,null=False)


    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email