from rest_framework import serializers
from app.entities.proposal import Proposal

class ProposalViewSet(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'