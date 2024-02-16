from rest_framework import serializers
from account.entities.competence import Competence

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'