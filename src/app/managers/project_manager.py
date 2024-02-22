from django.db import models

class ProjectManager(models.Manager):
    """
    Custom manager for the Project model wich have any additional methods.

    """

    def get_budgets_by_area(self, area):
        """
        Get budgets by area.

        :param area: The area for which budgets are retrieved.
        :type area: str
        :return: A list of budgets for the specified area.
        :rtype: List

        """
        budgets = self.filter(area=area).values_list('budget', flat=True)
        return list(budgets)
    
    def mean_budget(self, area):
        """
        Calculate the mean budget for the specified area.

        :param area: The area for which the mean budget is calculated.
        :type area: str
        :return: The mean budget for the specified area.
        :rtype: float
        """
        budgets = self.get_budgets_by_area(area)
        if budgets:
            return sum(budgets) / len(budgets)
        return 0
