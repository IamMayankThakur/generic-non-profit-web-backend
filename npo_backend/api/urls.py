from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'api'

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('update_details/',views.UpdateDetailsView.as_view(),name = 'update'),
    path('event/<pk>/',views.EventView.as_view(),name = 'event'),
    path('get_events/',views.EventDateView.as_view(),name = 'events_by_date'),
    path('get_donations/',views.DonationDateView.as_view(),name = 'donations_by_date'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

'''
event_router = DefaultRouter()
event_router.register('event',EventViewSet,'event')
urlpatterns = event_router.urls
'''