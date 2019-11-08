from rest_framework import serializers 
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('dob','gender','designation',
        'address','phone_number','pan_no','aadhar_no')
        