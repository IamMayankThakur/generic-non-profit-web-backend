from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps
import api.models as models
# Register your models here.

#Manually registering the models
admin.site.register(models.UserProfile)
admin.site.register(models.Donation)
admin.site.register(models.Event)
admin.site.register(models.Expense)
admin.site.register(models.FormMetaData)
admin.site.register(models.FormResponse)
admin.site.register(models.MailingList)