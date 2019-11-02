from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'api'

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('update_details/',views.UpdateDetailsView.as_view(),name = 'update'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
