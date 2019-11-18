from rest_framework import serializers 
from .models import UserProfile,Event,Donation,Expense,FormMetaData,FormResponse
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('dob','gender','designation',
        'address','phone_number','pan_no','aadhar_no')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name','description','created_on',
        'event_begin_date','event_end_date','event_created_by',
        'trash')

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ('donor','amount','remark','event','donated_on')

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class FormMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormMetaData
        fields = ('form_name','created_by','form_image','field_cords')


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponseSerializer
        fields = ('form', 'response', 'filled_by')
