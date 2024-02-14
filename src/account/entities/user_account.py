from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from account.managers.user_account_manager import *
from django.utils.translation import gettext_lazy as _
from account.utils.validators import (validate_first_letter,validate_phone)
import uuid

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, verbose_name=_('First Name'),null=False,blank=False)
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'), null=False, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False, max_length=255, verbose_name=_('Email'))

    is_active = models.BooleanField(default=True,null=False, blank=False)
    is_staff = models.BooleanField(default=False,null=False, blank=False)
    is_superuser = models.BooleanField(default=False,null=False, blank=False)

    is_freelancer = models.BooleanField(default=False,null=False, blank=False)
    headline = models.CharField(max_length=60,null=False,blank=True,verbose_name=_('Headline'),validators=[validate_first_letter])
    bio = models.TextField(blank=True,null=False)
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'), blank=True, null=False,validators=[validate_phone])

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return "{}-{}".format(self.email,self.headline)