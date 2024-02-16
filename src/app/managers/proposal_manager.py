from django.db import models

class ProposalManager(models.Manager):
    
    def proposal_accepted(self):
        return self.filter(situation='S', accepted_at__isnull=False)
    
    def is_paid(self):
        return self.filter(is_paid=True, paid_date__isnull=False)