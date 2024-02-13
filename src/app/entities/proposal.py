from django.db import models
from account.models import UserAccount as User
from app.models import Project
from django.utils.translation import gettext_lazy as _
from app.utils.validators import *

SITUATION_CHOICES = [
    ("W",_("Waiting")),
    ("S",_("Signed")),
]

class Proposal(models.Model):
    project = models.ForeignKey(Project,null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Project'), related_name='proposals')
    freelancer = models.ForeignKey(User,null=False, blank=False, on_delete=models.CASCADE,verbose_name=_('Freelancer'), related_name='proposals')
    cover_letter = models.TextField(max_length=200,null=False, blank=True,verbose_name=_('Letter'))
    bid_amount = models.DecimalField(max_digits=10,null=False, blank=False,verbose_name=_('Amount'), decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True,null=False, blank=False,verbose_name=_('Project'))
    situation = models.CharField(max_length=1,default='W',null=False, blank=False,choices=SITUATION_CHOICES,verbose_name=_('Situation'),validators=[validate_first_letter])
    is_paid = models.BooleanField(default=False,null=False, blank=False)

    def __str__(self):
        return "{}-{}".format(self.project,self.freelancer)
