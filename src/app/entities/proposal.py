from django.db import models
from django.contrib.auth import get_user_model
from app.entities.project import Project
from django.utils.translation import gettext_lazy as _
from app.utils.validators import *
import uuid

SITUATION_CHOICES = [
    ("W",_("Waiting")),
    ("I",_("Interest")),
    ("S",_("Signed")),
]

class Proposal(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project,null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Project'), related_name='proposals')
    freelancer = models.ForeignKey(get_user_model(),null=False, blank=False, on_delete=models.CASCADE,verbose_name=_('Freelancer'), related_name='proposals')
    cover_letter = models.TextField(max_length=200,null=False, blank=True,verbose_name=_('Letter'))
    bid_amount = models.DecimalField(max_digits=10,null=False, blank=False,verbose_name=_('Amount'), decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True,null=False, blank=False,verbose_name=_('Project'))
    situation = models.CharField(max_length=1,default='W',null=False, blank=False,choices=SITUATION_CHOICES,verbose_name=_('Situation'),validators=[validate_first_letter])
    is_paid = models.BooleanField(default=False,null=False, blank=False)
    discounted_value = models.DecimalField(max_digits=10, null=False, blank=False, decimal_places=2, verbose_name=_('Discounted Value'),validators=[validate_value])
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Accepted Date'))
    paid_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Paid Date'))

    def calculate_discounted_value(self):
        discount_percentage = 0.05
        discounted_value = self.budget * (1 - discount_percentage)
        return discounted_value

    def proposal_accepted(self): 
        return self.situation == 'S' and not self.accepted_at;

    def is_paid(self):
        return self.is_paid == True and not self.paid_date;

    def save(self, *args, **kwargs):
        if self.proposal_accepted(self):  
            self.accepted_at = timezone.now()
        if self.is_paid(self):
            self.paid_date = timezone.now()
        self.discounted_value = self.calculate_discounted_value()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')

    def __str__(self):
        return "{}-{}".format(self.project,self.freelancer)
