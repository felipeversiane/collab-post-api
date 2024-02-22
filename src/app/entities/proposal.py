from django.db import models
from django.contrib.auth import get_user_model
from app.entities.project import Project
from django.utils.translation import gettext_lazy as _
from app.utils.validators import *
import uuid
from app.managers.proposal_manager import ProposalManager

SITUATION_CHOICES = [
    ("W", _("Waiting")),
    ("I", _("Interest")),
    ("S", _("Signed")),
]

class Proposal(models.Model):
    """
    Represents a proposal entity.

    :param uuid: A unique identifier for the proposal.
    :type uuid: UUID
    :param project: The project associated with the proposal.
    :type project: class: 'app.entities.project.Project'
    :param freelancer: The freelancer who submitted the proposal.
    :type freelancer: class: 'account.models.UserAccount'
    :param cover_letter: The cover letter submitted with the proposal.
    :type cover_letter: str
    :param bid_amount: The bid amount for the proposal.
    :type bid_amount: float
    :param submitted_at: The date and time when the proposal was submitted.
    :type submitted_at: datetime.datetime
    :param situation: The situation of the proposal. Can be one of "Waiting", "Interest", "Signed".
    :type situation: str
    :param is_paid: Indicates if the proposal is paid.
    :type is_paid: bool
    :param accepted_at: The date and time when the proposal was accepted.
    :type accepted_at: datetime.datetime
    :param paid_date: The date and time when the proposal was paid.
    :type paid_date: datetime.datetime
    """

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Project'), related_name='proposals')
    freelancer = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('Freelancer'), related_name='proposals')
    cover_letter = models.TextField(max_length=200, null=False, blank=True, verbose_name=_('Letter'))
    bid_amount = models.DecimalField(max_digits=10, null=False, blank=False, verbose_name=_('Amount'), decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name=_('Project'))
    situation = models.CharField(max_length=1, default='W', null=False, blank=False, choices=SITUATION_CHOICES, verbose_name=_('Situation'), validators=[validate_first_letter])
    is_paid = models.BooleanField(default=False, null=False, blank=False)
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Accepted Date'))
    paid_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Paid Date'))

    objects = ProposalManager()

    def save(self, *args, **kwargs):
        """
        Saves the proposal object.

        If the situation is 'Signed' and accepted_at is not set, sets accepted_at to current time.
        If is_paid is True and paid_date is not set, sets paid_date to current time.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        if self.situation == 'S' and not self.accepted_at:
            self.accepted_at = timezone.now()
        if self.is_paid and not self.paid_date:
            self.paid_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')

    def __str__(self):
        """
        Returns a string representation of the proposal.

        :return: A string representation of the proposal.
        :rtype: str
        """
        return "{}-{}".format(self.project, self.freelancer)
