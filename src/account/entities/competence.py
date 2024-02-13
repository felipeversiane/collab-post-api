from django.db import models
from django.utils.translation import gettext_lazy as _


class Competence(models.Model):
    name = models.CharField(max_length=60, verbose_name=_('Competence Name'), null=False, blank=False)

    class Meta:
        verbose_name = _('Competence')
        verbose_name_plural = _('Competences')

    def __str__(self):
        return self.name