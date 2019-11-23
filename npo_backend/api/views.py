from .serializers import UserProfileSerializer, EventSerializer, DonationSerializer, ExpenseSerializer, UserSerializer
import datetime as datetime
from .serializers import UserProfileSerializer, EventSerializer, DonationSerializer, ExpenseSerializer
from .models import UserProfile, Event, Expense, Donation, FormMetaData, FormResponse, MailingList
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import UserProfile, Event, Expense, Donation, FormMetaData, FormResponse, FormMetaData
from .serializers import UserProfileSerializer, EventSerializer, DonationSerializer, ExpenseSerializer, UserSerializer, FormMetaDataSerializer, FormResponseSerializer, AdminUserSerializer

import datetime
from djqscsv import render_to_csv_response
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from djqscsv import write_csv


def get(self, request):
    content = {'message': 'Hello, World!'}
    return Response(content)


class SignUpView(APIView):
    def post(self, request):
        try:
            import pdb
            user = User.objects.create_user(
                username=request.data['email'], email=request.data['email'], password=request.data['password'],
                first_name=request.data['fname'], last_name=request.data['lname'], is_staff=False,
                is_superuser=False)
            user.save()
            profile = UserProfile(user=user, dob=request.data['dob'],
                                  designation=request.data['designation'], address=request.data['address'],
                                  phone_number=request.data['phno'])
            # pdb.set_trace()
            profile.save()
        except Exception as e:
            return Response(data={'message': 'User creation failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'User Created'}, status=status.HTTP_201_CREATED)


class UpdateDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)

    def post(self, request):
        try:
            print('Current credentials are:')
            print(request.user.userprofile.__dict__)
            user_profile = request.user.userprofile
            data = request.data
            print(data)
            print('*****')
            for key, value in data.items():
                setattr(user_profile, key, value)
            user_profile.save()
            print('New credentials are:')
            print(user_profile.__dict__)
            return Response(status=status.HTTP_200_OK, data={'message': 'Updated'})

        except Exception as e:
            print(e)
            print(type(e))
            return Response(data={'message': 'Update failed'}, status=400)


# To put account id based operations together
'''
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
'''


# using PATCH instead of POST for updating an existing record
class EventView(RetrieveUpdateDestroyAPIView, CreateModelMixin):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CreateEventView(APIView):

    def post(self,request):
        user = request.user
        name = request.data['name']
        description = request.data['description']
        event_begin = request.data['event_begin_date']
        event_end = request.data['event_end_date']

        event = Event(name = name,description = description, event_begin_date = event_begin, event_end_date = event_end,event_created_by = user)
        event.save()
        return Response(data = {'Event' : 'Added'})

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    

class ExpenseView(RetrieveUpdateDestroyAPIView):
    

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class CreateExpenseView(APIView):

    def post(self,request):
        print(request.data)
        print(request.POST)
        user = request.user
        debit = request.data['debit']
        amount = request.data['amount']

        expense = Expense(updated_by=user, debit=debit, amount=amount)
        expense.save()

        return Response(data={'Expense':'Added'},status=200)

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)


class EventDateView(ListAPIView):

    def get_queryset(self):
        start_date = self.request.query_params.get('startDate')
        print(type(start_date))
        print(f'Starting date is: {start_date}')
        end_date = self.request.query_params.get('endDate')
        queryset = Event.objects.filter(event_begin_date__gte=start_date).filter(
            event_end_date__lte=end_date)
        #queryset = Event.objects.filter(event_begin_date__gte = start_date)
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = EventSerializer


class DonationDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = Donation.objects.filter(
            donated_on__range=[intial_date, final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = DonationSerializer


class ExpenseDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = Expense.objects.filter(
            timestamp__range=[intial_date, final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = ExpenseSerializer


class UserDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = UserProfile.objects.filter(
            dob__range=[intial_date, final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = UserProfileSerializer


class DonationCountView(APIView):

    def get(self, request):
        days = request.query_params['days']
        if int(days) == 0:
            count = Donation.objects.all().count()
            return Response(data={'count': count}, status=status.HTTP_200_OK)

        date = datetime.datetime.today() - datetime.timedelta(days=int(days))
        count = Donation.objects.filter(donated_on__gte=date).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class UserCountView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        days = request.query_params['days']
        if int(days) == 0:
            count = User.objects.all().count()
            return Response(data={'count': count}, status=status.HTTP_200_OK)

        date = datetime.datetime.today() - datetime.timedelta(days=int(days))
        count = User.objects.filter(date_joined__gte=date).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class DonationView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date = datetime.datetime.today() - datetime.timedelta(days=30)
        donations = list(Donation.objects.filter(
            donated_on__gte=date).values('donated_on', 'amount'))
        return Response(data=donations, status=status.HTTP_200_OK)


class EventCountView(APIView):

    def get(self, request):
        days = request.query_params['days']
        if int(days) == 0:
            count = Event.objects.all().count()
            return Response(data={'count': count}, status=status.HTTP_200_OK)

        date = datetime.datetime.today() - datetime.timedelta(days=int(days))
        count = Event.objects.filter(event_begin_date__gte=date).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class UpcomingEventCountView(APIView):

    def get(self, request):
        days = request.query_params['days']
        today = datetime.datetime.now()
        if int(days) == 0:
            count = Event.objects.filter(
                event_begin_date__gte=today).count()
            return Response(data={'count': count}, status=status.HTTP_200_OK)

        date = datetime.datetime.today() + datetime.timedelta(days=int(days))
        count = Event.objects.filter(
            event_begin_date__lte=date, event_begin_date__gte=today).count()
        return Response(data={'count': count}, status=status.HTTP_200_OK)


class RegisteredForEventView(ListAPIView):
    def get_queryset(self):
        event_id = self.request.query_params.get('eventId')
        queryset = User.objects.filter(events_registered_for__pk=event_id)
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = UserSerializer


class FillFormView(ListCreateAPIView):

    queryset = FormResponse.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = FormResponseSerializer


class FormView(APIView):
    pass


class FormDetailsView(ListAPIView):
    def get_queryset(self):
        form_id = self.request.query_params.get('formId')
        user_id = self.request.query_params.get('userId')
        forms = FormResponse.objects.filter(form_id=form_id)
        queryset = forms.objects.filter(filled_by__id=user_id)
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = FormResponseSerializer

# Gets all expense records for last 20 days. No. 8 from the New Apis list


class GenericExpenseView(ListAPIView):
    def get_queryset(self):
        queryset = Expense.objects.filter(
            timestamp__date__gte=datetime.date.today() - datetime.timedelta(days=20))
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = ExpenseSerializer


class AdminUserDetailsView(APIView):

    def get(self,request):
        user_details = User.objects.filter(pk = request.user.id).values('first_name','is_staff','is_superuser')
        return Response(data=user_details[0])
    
    '''
    def get_queryset(self):
        users = User.objects.filter(is_superuser=True)
        return users
    '''

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    

class UsersFromPastWeekView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request):
        users = User.objects.filter(
            date_joined__date__gte=datetime.date.today() - datetime.timedelta(days=7))
        users_count = len(users)
        content = {'count': users_count}
        return Response(content)


class CreditDebitCurrentMonthView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request):
        expense_records = Expense.objects.filter(
            timestamp__date__gte=datetime.date.today() - datetime.timedelta(days=30))
        credit_amount, debit_amount = 0, 0
        for record in expense_records:
            if record.debit == 0:
                credit_amount += record.amount
            else:
                debit_amount += record.amount
        content = {'credit': credit_amount, 'debit': debit_amount}
        return Response(content)

class UpcomingEventsView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = EventSerializer

    def get_queryset(self):
        #queryset = Event.objects.all()
        queryset = Event.objects.filter(event_begin_date__gte = datetime.date.today())
        #queryset = Event.objects.filter(event_begin_date__gte = start_date)
        return queryset
    


'''
class PayPalPaymentsView(APIView):
    def get(self,request):
        payment_information = {
            'username' : request.user.username,
            'amount' : 1000,
            
        }
        payment_form = PayPalPaymentsForm(initial = payment_information)
        context = {'form' : payment_form}
'''


class GetExpenseDataAsCSVView(APIView):
    def get(self, request):
        data = Expense.objects.filter(
            timestamp__gte=datetime.datetime.now() - datetime.timedelta(days=30)).values()
        with open('expense.csv', 'wb') as csv_file:
            write_csv(data, csv_file)
        file = open('expense.csv', 'rb')
        return HttpResponse(FileWrapper(file), content_type='text/csv')


class GetDonationDataAsCSVView(APIView):
    def get(self, request):
        data = Donation.objects.filter(donated_on__gte=datetime.datetime.now(
        ) - datetime.timedelta(days=30)).values('amount', 'remark', 'donated_on')
        with open('donation.csv', 'wb') as csv_file:
            write_csv(data, csv_file)
        file = open('donation.csv', 'rb')
        return HttpResponse(FileWrapper(file), content_type='text/csv')


class AddMailingListView(APIView):
    def post(self, request):
        email = request.data['email_id']
        ml = MailingList(email_id=email)
        ml.save()
        return Response(data={'message': 'Added'}, status=status.HTTP_200_OK)


class AddFormView(APIView):
    def post(self, request):
        file = request.FILES['file']
        # formname = request.POST['formname']
        formname = request.POST['formname']
        coords = request.POST['pos']
        form_metadata = FormMetaData(
            form_name=formname,
            created_by=request.user, form_image=file, field_cords=coords
        )
        form_metadata.save()
        return Response(data={'Form': 'Added'}, status=status.HTTP_200_OK)


class GetFormView(APIView):
    def get(self, request):
        form_name = request.get_queryset.get('formname')
        FormMetaData.objects.all()

        