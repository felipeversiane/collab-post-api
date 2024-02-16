from rest_framework import serializers
from app.entities.project import Project

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['uuid', 'title', 'description', 'budget', 'created_at', 'updated_at', 'employer', 'start_date', 'end_date', 'situation', 'payment_type', 'area']


class ReadOnlyProjectSerializer(serializers.ModelSerializer):

    employer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ['uuid', 'title', 'description', 'budget', 'employer', 'created_at', 'start_date', 'end_date','payment_type','area']

    def get_employer(self, obj):
        return {
            "uuid": obj.employer.uuid,
            "name": f"{obj.employer.first_name} {obj.employer.last_name}"
        }
