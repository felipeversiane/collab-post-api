from django.db import models
from django.utils.translation import gettext_lazy as _
from account.entities.competence import Competence
from account.utils.validators import validate_first_letter, validate_safe_text
from django.contrib.auth import get_user_model
import uuid

JOB_TYPE_CHOICES = [
        ("TR", _('Trainee')),
        ("IN", _('Internship')),
        ("FT", _('Full-time')),
        ("PT", _('Part-time')),
        ("FL", _('Free lance')),
        ("AU", _('Autonomous')),
        ("AP", _('Apprentice')),
        ("TP", _('Third Party')),
]

class Job(models.Model):
    """
    Represents a job entity.

    :param uuid: The unique identifier for the job.
    :type uuid: UUID
    :param user: The user associated with the job.
    :type user: class: 'account.models.UserAccount'
    :param title: The title of the job.
    :type title: str
    :param company: The company where the job is located.
    :type company: str
    :param start_date: The start date of the job.
    :type start_date: datetime.date
    :param end_date: The end date of the job.
    :type end_date: datetime.date
    :param competences: The competences required for the job.
    :type competences: List
    :param job_type: The type of the job.
    :type job_type: str
    """

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='jobs', verbose_name=_('User'), null=False, blank=False)
    title = models.CharField(max_length=100, verbose_name=_('Job Title'), null=False, blank=False, validators=[validate_first_letter, validate_safe_text])
    company = models.CharField(max_length=70, verbose_name=_('Company'), null=False, blank=False, validators=[validate_safe_text])
    start_date = models.DateField(verbose_name=_('Start Date'), null=False, blank=False)
    end_date = models.DateField(verbose_name=_('End Date'), null=False, blank=True)
    competences = models.ManyToManyField(Competence, related_name='jobs', verbose_name=_('Competences'), blank=True)
    job_type = models.CharField(max_length=2, default="FT", choices=JOB_TYPE_CHOICES, null=False, blank=False, verbose_name=_('Job Type'))

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def __str__(self):
        """
        Returns a string representation of the job.

        :return: A string representation of the job.
        :rtype: str
        """
        return "{}-{}".format(self.title, self.company)
