from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'api'

urlpatterns = [
    # path('hello/', views.HelloView.as_view(), name='hello'),
    path('signup/', views.SignUpView.as_view(), name='sign up'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('update_details/',views.UpdateDetailsView.as_view(),name = 'update'),
    path('event/<pk>/',views.EventView.as_view(),name = 'event'),
    path('expense/<pk>/',views.ExpenseView.as_view(),name = 'expense'),
    path('get_expenses/',views.ExpenseDateView.as_view(),name ='expenses_by_date'),
    path('get_events/',views.EventDateView.as_view(),name = 'events_by_date'),
    path('get_donations/',views.DonationDateView.as_view(),name = 'donations_by_date'),
    path('get_users/', views.UserDateView.as_view(), name = 'users_by_date'),
    path('donations_count/', views.DonationCountView.as_view(), name = 'count donation by date'),
    path('users_count/', views.UserCountView.as_view(), name = 'count user by date'),
    path('get_donations_value/', views.DonationView.as_view(), name = 'Donations for past 30 days'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

'''
event_router = DefaultRouter()
event_router.register('event',EventViewSet,'event')
urlpatterns = event_router.urls
'''