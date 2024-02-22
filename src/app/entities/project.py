from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from app.utils.validators import *
import uuid
from app.managers.project_manager import ProjectManager

SITUATION_CHOICES = [
    ("W",_("Waiting")),
    ("O",_("Open")),
    ("B",_("Busy")),
    ("F",_("Finished")),
]

AREA_CHOICES = [
    ("FS",_("Full-Stack")),
    ("FE",_("Front-End")),
    ("BE",_("Back-End")),
    ("GM",_("Gaming")),
]

class Project(models.Model):
    """
    This is a project model

    :param uuid: A unique identification for project
    :type uuid: UUID
    :param title: A title of the project
    :type title: str  
    :param description: A description of the project
    :type description: str  
    :param budget: A budget of the project
    :type budget: float
    :param created_at: The date and time when the project was created
    :type created_at: datetime.datetime  
    :param updated_at: The date and time when the project was last updated
    :type updated_at: datetime.datetime  
    :param employer: The user who manages the project
    :type employer: class:'account.models.UserAccount'  
    :param start_date: The start date of the project
    :type start_date: datetime.date  
    :param end_date: The end date of the project
    :type end_date: datetime.date  
    :param situation: The situation of the project. Can be one of "Waiting", "Open", "Busy", "Finished"
    :type situation: str  
    :param payment_type: The payment type for the project
    :type payment_type: str  
    :param area: The area of the project. Can be one of "Full-Stack", "Front-End", "Back-End", "Gaming"
    :type area: str
    """

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=60, null=False, blank=False, verbose_name=_('Title'), validators=[validate_first_letter, validate_letters, validate_safe_text])
    description = models.TextField(max_length=200, null=False, blank=False, verbose_name=_('Description'), validators=[validate_first_letter, validate_safe_text])
    budget = models.DecimalField(max_digits=10, null=False, blank=False, decimal_places=2, verbose_name=_('Budget'), validators=[validate_value])
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name=_('Created Date'), validators=[validate_date])
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False, verbose_name=_('Updated Date'), validators=[validate_date])
    employer = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='projects', verbose_name=_('Project Manager'))
    start_date = models.DateField(verbose_name=_('Start Date'), null=False, blank=False)
    end_date = models.DateField(verbose_name=_('End Date'), null=False, blank=False)
    situation = models.CharField(max_length=1, default="W", null=False, blank=False, choices=SITUATION_CHOICES, verbose_name=_('Project Situation'), validators=[validate_letters])
    payment_type = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Payment Type'), validators=[validate_first_letter])
    area = models.CharField(max_length=2, choices=AREA_CHOICES, null=False, blank=False, verbose_name=_("Project Area"), validators=[validate_letters])

    objects = ProjectManager()

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = 'created_at'

    def __str__(self):

        """
        Returns a string representation of the object.

        :return: Return a string representation of the object
        :rtype: string
        """

        return "{}-{}".format(self.title, self.budget)