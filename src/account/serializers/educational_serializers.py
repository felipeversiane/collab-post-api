from rest_framework import serializers
from account.entities.education_background import EducationalBackground as Education

class EducationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'