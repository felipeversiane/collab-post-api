from rest_framework import serializers
from account.entities.user_account import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('uuid','email','first_name','last_name')