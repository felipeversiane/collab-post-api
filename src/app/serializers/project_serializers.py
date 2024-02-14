from rest_framework import serializers
from app.entities.project import Project

class ProjectViewSet(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'