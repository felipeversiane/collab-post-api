from django.contrib import admin
from account.entities.user_account import UserAccount
from account.entities.job import Job
from account.entities.education_background import EducationalBackground as Education
from account.entities.competence import Competence

admin.site.register(UserAccount)
admin.site.register(Competence)
admin.site.register(Job)
admin.site.register(Education)


