from django.contrib import admin
from app.entities.project import Project
from app.entities.proposal import Proposal


admin.site.register(Project)
admin.site.register(Proposal)

