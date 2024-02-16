from django.db import models

class ProjectManager(models.Manager):
    
    def get_budgets_by_area(self, area):
        budgets = self.filter(area=area).values_list('budget', flat=True)
        return list(budgets)
    
    def mean_budget(self, area):
        budgets = self.get_budgets_by_area(area)
        if budgets:
            return sum(budgets) / len(budgets)
        return 0  
