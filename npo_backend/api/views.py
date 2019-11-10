from rest_framework.generics import UpdateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from rest_framework import status 
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import UserProfile,Event,Expense,Donation,FormMetaData,FormResponse
from .serializers import UserProfileSerializer,EventSerializer,DonationSerializer,ExpenseSerializer

class HelloView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



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
