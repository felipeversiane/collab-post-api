from rest_framework import serializers
from app.entities.project import Project
from app.entities.proposal import Proposal  

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'