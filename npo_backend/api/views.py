from rest_framework.generics import UpdateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView, CreateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status 
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import UserProfile,Event,Expense,Donation,FormMetaData,FormResponse,FormMetaData
from .serializers import UserProfileSerializer,EventSerializer,DonationSerializer,ExpenseSerializer,UserSerializer,FormMetaDataSerializer,FormResponseSerializer,AdminUserSerializer

import datetime

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class SignUpView(APIView):
    def post(self, request):
        try:
            user = User.objects.create_user(
                username=request.data['email'], email=request.data['email'], password=request.data['password'],
                first_name=request.data['first_name'], last_name=request.data['last_name'], is_staff=False,
                is_superuser=False)
            user.save()
            profile = UserProfile(user=user, dob=request.data['dob'],
                                  designation=request.data['designation'], address=request.data['address'],
                                  phone_number=request.data['phone_number'])
            profile.save()
        except Exception as e:
            return Response(data={'message': 'User creation failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message': 'User Created'}, status=status.HTTP_201_CREATED)

class UpdateDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    def post(self,request):
        try:
            print('Current credentials are:')
            print(request.user.userprofile.__dict__)
            user_profile = request.user.userprofile 
            data = request.data
            print(data)
            print('*****')
            for key,value in data.items():
                setattr(user_profile,key,value)
            user_profile.save()
            print('New credentials are:')
            print(user_profile.__dict__)
            return Response(status = status.HTTP_200_OK, data = {'message' : 'Updated'})

        except Exception as e:
            print(e)
            print(type(e))
            return Response(data = {'message': 'Update failed'},status = 400)

#To put account id based operations together
'''
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
'''
 

#using PATCH instead of POST for updating an existing record
class EventView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ExpenseView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class EventDateView(ListAPIView):

    def get_queryset(self):
        start_date = self.request.query_params.get('startDate')
        print(type(start_date))
        print(f'Starting date is: {start_date}')
        end_date = self.request.query_params.get('endDate')
        queryset = Event.objects.filter(event_begin_date__gte = start_date).filter(event_end_date__lte = end_date)
        #queryset = Event.objects.filter(event_begin_date__gte = start_date)
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = EventSerializer


class DonationDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = Donation.objects.filter(donated_on__range = [intial_date,final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = DonationSerializer

class ExpenseDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = Expense.objects.filter(timestamp__range = [intial_date,final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = ExpenseSerializer

class UserDateView(ListAPIView):
    def get_queryset(self):
        intial_date = self.request.query_params.get('startDate')
        final_date = self.request.query_params.get('endDate')
        queryset = UserProfile.objects.filter(dob__range = [intial_date,final_date])
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = UserProfileSerializer

class RegisteredForEventView(ListAPIView):
    def get_queryset(self):
        event_id = self.request.query_params.get('eventId')
        queryset = User.objects.filter(events_registered_for__pk = event_id)
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
        forms = FormResponse.objects.filter(form_id = form_id)
        queryset = forms.objects.filter(filled_by__id = user_id)
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = FormResponseSerializer

#Gets all expense records for last 20 days. No. 8 from the New Apis list
class GenericExpenseView(ListAPIView):
    def get_queryset(self):
        queryset = Expense.objects.filter(timestamp__date__gte = datetime.date.today() - datetime.timedelta(days = 20))
        return queryset

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = ExpenseSerializer

class AdminUserDetailsView(ListAPIView):
    def get_queryset(self):
        users = User.objects.filter(is_superuser = True)
        return users

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    serializer_class = AdminUserSerializer

class UsersFromPastWeekView(APIView):
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def get(self,request):
        users = User.objects.filter(date_joined__date__gte = datetime.date.today() - datetime.timedelta(days = 7))
        users_count = len(users)
        content = {'count' : users_count}
        return Response(content)

class CreditDebitCurrentMonthView(APIView):
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def get(self,request):
        expense_records = Expense.objects.filter(timestamp__date__gte = datetime.date.today() - datetime.timedelta(days = 30))
        credit_amount,debit_amount = 0,0
        for record in expense_records:
            if record.credit:         
                credit_amount += record.amount
            else:
                debit_amount += record.amount
        content = {'credit' : credit_amount, 'debit' : debit_amount}
        return Response(content)
