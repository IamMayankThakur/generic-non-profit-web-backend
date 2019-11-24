from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'api'

urlpatterns = [
    # path('hello/', views.HelloView.as_view(), name='hello'),
    path('signup/', views.SignUpView.as_view(), name='sign up'),
    path('donations_count/', views.DonationCountView.as_view(),
         name='count donation by date'),
    path('users_count/', views.UserCountView.as_view(), name='count user by date'),
    path('get_donations_value/', views.DonationView.as_view(),
         name='Donations for past 30 days'),
    path('upcoming_events_count/',
         views.UpcomingEventCountView.as_view(), name='Upcoming Events'),
    path('events_count/', views.EventCountView.as_view(), name='Past Events'),

    path('event/',views.CreateEventView.as_view(),name = 'post-event'),
    path('event/<pk>/', views.EventView.as_view(), name='event'),
    path('update_details/',views.UpdateDetailsView.as_view(),name = 'update'),

    path('get_upcoming_events/',views.UpcomingEventsView.as_view(), name = 'upcoming-events'),
    
    path('expense/',views.CreateExpenseView.as_view(),name = 'expense'),
    path('expense/<pk>/',views.ExpenseView.as_view(),name = 'expense'),
    path('get_expenses/',views.ExpenseDateView.as_view(),name ='expenses_by_date'),
    
    path('get_events/',views.EventDateView.as_view(),name = 'events_by_date'),

    path('get_users/', views.UserDateView.as_view(), name = 'users_by_date'),
    path('get_donations/', views.DonationDateView.as_view(),
         name='donations_by_date'),
    path('get_users_last_week/', views.UsersFromPastWeekView.as_view(),
         name='last-week-users'),
    path('get_user_details/', views.AdminUserDetailsView.as_view(),
         name='get-user-details'),
    path('get_cd/', views.CreditDebitCurrentMonthView.as_view(),
         name='get-credit-debit'),
    path('get_expenditure/', views.GenericExpenseView.as_view(),
         name='get-expenditure'),
    path('get_registered_users/', views.RegisteredForEventView.as_view(),
         name='registered_users'),
    path('fill_form/', views.FillFormView.as_view(), name='fill-form'),
    path('get_form_data/', views.FormDetailsView.as_view(), name='form-data'),
    path('get_expense_csv/', views.GetExpenseDataAsCSVView.as_view(), name='get csv expense data'),
    path('get_donation_csv/', views.GetDonationDataAsCSVView.as_view(), name='get csv donation data'),
    path('add_mailing_list/', views.AddMailingListView.as_view(), name='add user to mailing list'),
    path('add_form/', views.AddFormView.as_view(), name='add Form to database'),
    path('get_form/', views.GetFormView.as_view(), name='Get Form from database'),
    path('get_all_forms/', views.GetAllFormsView.as_view(), name='Get All Forms from database'),
    path('get_form_image/', views.GetFormImageView.as_view(), name='Get Image for the given file'),
    path('get_filled_forms_name/', views.GetFilledFormsNameView.as_view(), name='Get Filled Forms name for current user'),
    path('get_filled_forms_data/', views.GetFilledFormsDataView.as_view(), name='Get Filled Forms data for current user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

'''
event_router = DefaultRouter()
event_router.register('event',EventViewSet,'event')
urlpatterns = event_router.urls
'''
