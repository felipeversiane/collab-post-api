import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


#Regex 
PHONE_REGEX = r"^\d{11}$"
DATE_REGEX = r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'

#Functions
def validate_first_letter(str):    
    if str[0].isdigit():        
        raise ValidationError(_("First letter cannot be a number."))

def validate_letters(name):    
    if not re.match(r'^[A-Za-z ]+$', name):      
        raise ValidationError(_("Only letters and spaces allowed."))
        
def validate_phone(phone):
    if not re.match(PHONE_REGEX, phone):
        raise ValidationError(_("Invalid phone number format.")) 

def validate_value(value):
    if value <= 0:
        raise ValidationError(_("Value must be positive."))
        
def validate_date(date): 
    if date < timezone.now().date():  
        raise ValidationError(_("Invalid date."))
        
def validate_time(time):       
    if time < timezone.now().time():   
        raise ValidationError(_("Invalid time."))    
    
def validate_birth_date(value):
    if not re.match(DATE_REGEX, value):
         raise ValidationError(_("Invalid date of birth."))
    
def validate_safe_text(value):
    if re.search(r'<|>|&|;|\'|"|\/|\\', value):
        raise ValidationError(
            _("The text cannot contain dangerous special characters."),
            code='invalid',
        )