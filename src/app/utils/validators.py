import datetime
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Regex
PHONE_REGEX = r"^\d{11}$"
DATE_REGEX = r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'


def validate_first_letter(string):
    """
    Validates that the first character of a string is not a digit.

    :param string: The input string.
    :type string: str
    :raises ValidationError: If the first character of the string is a digit.
    """
    if string[0].isdigit():
        raise ValidationError({'message': _("First letter cannot be a number.")}, code='invalid')


def validate_letters(name):
    """
    Validates that the string contains only letters and spaces.

    :param name: The input string.
    :type name: str
    :raises ValidationError: If the string contains characters other than letters and spaces.
    """
    if not re.match(r'^[A-Za-z ]+$', name):
        raise ValidationError({'message': _("Only letters and spaces allowed.")}, code='invalid')


def validate_phone(phone):
    """
    Validates the format of a phone number.

    :param phone: The phone number.
    :type phone: str
    :raises ValidationError: If the phone number does not match the expected format.
    """
    if not re.match(PHONE_REGEX, phone):
        raise ValidationError({'message': _("Invalid phone number format.")}, code='invalid')


def validate_value(value):
    """
    Validates that a value is positive.

    :param value: The input value.
    :type value: int or float
    :raises ValidationError: If the value is not positive.
    """
    if value <= 0:
        raise ValidationError({'message': _("Value must be positive.")}, code='invalid')


def validate_date(date):
    """
    Validates a date against the current date.

    :param date: The input date.
    :type date: datetime.date
    :raises ValidationError: If the date is earlier than the current date.
    """
    if date < timezone.now().date():
        raise ValidationError({'message': _("Invalid date.")}, code='invalid')


def validate_time(time):
    """
    Validates a time against the current time.

    :param time: The input time.
    :type time: datetime.time
    :raises ValidationError: If the time is earlier than the current time.
    """
    if time < timezone.now().time():
        raise ValidationError({'message': _("Invalid time.")}, code='invalid')


def validate_birth_date(value):
    """
    Validates the format of a birth date.

    :param value: The input birth date.
    :type value: str
    :raises ValidationError: If the birth date does not match the expected format.
    """
    if not re.match(DATE_REGEX, value):
        raise ValidationError({'message': _("Invalid date of birth.")}, code='invalid')


def validate_safe_text(value):
    """
    Validates that text does not contain dangerous special characters.

    :param value: The input text.
    :type value: str
    :raises ValidationError: If the text contains dangerous special characters.
    """
    if re.search(r'<|>|&|;|\'|"|\/|\\', value):
        raise ValidationError({'message': _("The text cannot contain dangerous special characters.")}, code='invalid')
