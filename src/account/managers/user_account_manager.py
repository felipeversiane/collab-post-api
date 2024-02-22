from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    """
    Custom manager for the UserAccount model.

    This manager provides helper methods for creating user accounts.
    """

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a regular user with the given email and password.

        :param email: The email address of the user.
        :type email: str
        :param password: The password for the user account.
        :type password: str
        :param kwargs: Additional keyword arguments.
        :return: The created user account.
        :rtype: UserAccount
        :raises ValueError: If the email address is not provided.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.

        :param email: The email address of the superuser.
        :type email: str
        :param password: The password for the superuser account.
        :type password: str
        :param kwargs: Additional keyword arguments.
        :return: The created superuser account.
        :rtype: UserAccount
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
