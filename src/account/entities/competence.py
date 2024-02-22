from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Competence(models.Model):
    
    """
    Represents a competence entity.

    :param uuid: The unique identifier for the competence.
    :type uuid: UUID
    :param name: The name of the competence.
    :type name: str
    """

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, verbose_name=_('Competence Name'), null=False, blank=False)

    class Meta:
        verbose_name = _('Competence')
        verbose_name_plural = _('Competences')

    def __str__(self):
        """
        Returns a string representation of the competence.

        :return: A string representation of the competence.
        :rtype: str
        """
        return self.name
