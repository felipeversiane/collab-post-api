from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from app.utils.validators import *

SITUATION_CHOICES = [
    ("W",_("Waiting")),
    ("O",_("Open")),
    ("B",_("Busy")),
    ("F",_("Finished")),
]

class Project(models.Model):
    title = models.CharField(max_length=60,null=False, blank=False, verbose_name=_('Title'),validators=[validate_first_letter,validate_letters])
    description = models.TextField(max_length=200,null=False, blank=False,verbose_name=_('Description'),validators=[validate_first_letter])
    budget = models.DecimalField(max_digits=10,null=False, blank=False,decimal_places=2,verbose_name=_('Budget'),validators=[validate_value])
    created_at = models.DateTimeField(auto_now_add=True,null=False, blank=False,verbose_name=_('Created Date'),validators=[validate_date])
    updated_at = models.DateTimeField(auto_now=True,null=False, blank=False,verbose_name=_('Updated Date'),validators=[validate_date])
    employer = models.ForeignKey(get_user_model(),null=False, blank=False, on_delete=models.CASCADE, related_name='projects',verbose_name=_('Project Manager'))
    start_date = models.DateField(verbose_name=_('Start Date'),null=False, blank=False)
    end_date = models.DateField(verbose_name=_('End Date'),null=False, blank=False)
    situation = models.CharField(max_length=1,default="W",null=False, blank=False,choices=SITUATION_CHOICES,verbose_name=_('Project Situation'),validators=[validate_first_letter])
    payment_type = models.CharField(max_length=20,null=False,blank=False,verbose_name=_('Payment Type'),validators=[validate_first_letter])
   
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return "{}-{}".format(self.title,self.budget)
