from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .constants import Gender
from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    # Other attributes are in the default User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=255, choices=[(
        gender, gender.value) for gender in Gender], blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    pan_no = models.TextField(blank=True, null=True)
    aadhar_no = models.TextField(blank=True, null=True)

    def __str__(self):
        return super().__str__() + f': {self.user.username}'


class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    event_begin_date = models.DateField(blank=True, null=True)
    event_end_date = models.DateField(blank=True, null=True)
    event_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    trash = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__() + str(self.name)


class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(blank=False)
    remark = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)
    donated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Donation by {self.donor} of {self.amount} ' + super().__str__() 

class FormMetaData(models.Model):
    form_name = models.CharField(
        max_length=255, default="Default", blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    form_image = models.ImageField(blank=False)
    field_cords = JSONField()


class FormResponse(models.Model):
    form = models.ForeignKey(FormMetaData, on_delete=models.CASCADE)
    response = JSONField()
    filled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    filled_on = models.DateTimeField(default=timezone.now)


class Expense(models.Model):
    credit = models.BooleanField(default=True)
    debit = models.BooleanField(default=False)
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
