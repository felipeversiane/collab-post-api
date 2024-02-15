import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#Regex 
PHONE_REGEX = r"^\d{11}$"
DATE_REGEX = r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'


def validate_first_letter(str):    
    if str[0].isdigit():        
        raise ValidationError({'message': _("First letter cannot be a number.")}, code='invalid')

def validate_letters(name):    
    if not re.match(r'^[A-Za-z ]+$', name):      
        raise ValidationError({'message': _("Only letters and spaces allowed.")}, code='invalid')
        
def validate_phone(phone):
    if not re.match(PHONE_REGEX, phone):
        raise ValidationError({'message': _("Invalid phone number format.")}, code='invalid') 

def validate_value(value):
    if value <= 0:
        raise ValidationError({'message': _("Value must be positive.")}, code='invalid')
        
def validate_date(date): 
    if date < timezone.now().date():  
        raise ValidationError({'message': _("Invalid date.")}, code='invalid')
        
def validate_time(time):       
    if time < timezone.now().time():   
        raise ValidationError({'message': _("Invalid time.")}, code='invalid')    
    
def validate_birth_date(value):
    if not re.match(DATE_REGEX, value):
         raise ValidationError({'message': _("Invalid date of birth.")}, code='invalid')
    
def validate_safe_text(value):
    if re.search(r'<|>|&|;|\'|"|\/|\\', value):
        raise ValidationError({'message': _("The text cannot contain dangerous special characters.")}, code='invalid')
