from rest_framework import serializers
from app.entities.proposal import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    discounted_value = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Proposal
        fields = ['uuid', 'project', 'freelancer', 'cover_letter', 'bid_amount', 'submitted_at', 'situation', 'is_paid', 'accepted_at', 'paid_date','discounted_value']
    
    def get_discounted_value(self, obj):
        discount_percentage = 0.05
        bid_amount_float = float(obj.bid_amount)
        discounted_value = bid_amount_float * (1 - discount_percentage)
        return discounted_value
    
