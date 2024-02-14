from django.db import models
from django.utils.translation import gettext_lazy as _
from account.utils.validators import (validate_first_letter,validate_safe_text)
from account.entities.competence import Competence
from django.contrib.auth import get_user_model
import uuid

class EducationalBackground(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name='educational_backgrounds', verbose_name=_('User'),null=False,blank=False)
    institution = models.CharField(max_length=70, verbose_name=_('Institution'), null=False, blank=False,validators=[validate_first_letter,validate_safe_text])
    degree = models.CharField(max_length=50, verbose_name=_('Degree'), null=False, blank=False,validators=[validate_first_letter,validate_safe_text])
    field_of_study = models.CharField(max_length=50, verbose_name=_('Field of Study'), null=False, blank=False,validators=[validate_first_letter,validate_safe_text])
    start_date = models.DateField(verbose_name=_('Start Date'), null=False, blank=False)
    end_date = models.DateField(verbose_name=_('End Date'), null=False, blank=True)
    competences = models.ManyToManyField(Competence, related_name='educational_backgrounds', verbose_name=_('Competences'), blank=True)

    class Meta:
        verbose_name = _('Educational Background')
        verbose_name_plural = _('Educational Backgrounds')

    def __str__(self):
        return "{} - {}".format(self.institution, self.degree)