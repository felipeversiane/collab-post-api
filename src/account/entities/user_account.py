from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.managers.user_account_manager import UserAccountManager
from django.utils.translation import gettext_lazy as _
from account.utils.validators import validate_first_letter, validate_phone
import uuid

class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user account entity.

    :param uuid: The unique identifier for the user account.
    :type uuid: UUID
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The last name of the user.
    :type last_name: str
    :param email: The email address of the user.
    :type email: str
    :param is_active: A boolean indicating whether the user account is active.
    :type is_active: bool
    :param is_staff: A boolean indicating whether the user account has staff privileges.
    :type is_staff: bool
    :param is_superuser: A boolean indicating whether the user account has superuser privileges.
    :type is_superuser: bool
    :param is_freelancer: A boolean indicating whether the user is a freelancer.
    :type is_freelancer: bool
    :param headline: A headline associated with the user.
    :type headline: str
    :param bio: A biography or description of the user.
    :type bio: str
    :param phone_number: The phone number of the user.
    :type phone_number: str
    """

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, verbose_name=_('First Name'), null=False, blank=False)
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'), null=False, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False, max_length=255, verbose_name=_('Email'))

    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    is_superuser = models.BooleanField(default=False, null=False, blank=False)

    is_freelancer = models.BooleanField(default=False, null=False, blank=False)
    headline = models.CharField(max_length=60, null=False, blank=True, verbose_name=_('Headline'), validators=[validate_first_letter])
    bio = models.TextField(blank=True, null=False)
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'), blank=True, null=False, validators=[validate_phone])

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        """
        Returns a string representation of the user account.

        :return: A string representation of the user account.
        :rtype: str
        """
        return "{}-{}".format(self.email, self.headline)
