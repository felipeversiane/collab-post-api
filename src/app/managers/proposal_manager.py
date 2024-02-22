from django.db import models

class ProposalManager(models.Manager):
    """
    Custom manager for the Proposal model wich have any additional methods.

    """

    def proposal_accepted(self):
        """
        Get proposals that have been accepted.

        :return: Queryset containing proposals that have been accepted.
        :rtype: List of Proposal Objects
        """
        return self.filter(situation='S', accepted_at__isnull=False)
    
    def is_paid(self):
        """
        Get proposals that have been paid.

        :return: Queryset containing proposals that have been paid.
        :rtype: List of Proposal Objects
        """
        return self.filter(is_paid=True, paid_date__isnull=False)
