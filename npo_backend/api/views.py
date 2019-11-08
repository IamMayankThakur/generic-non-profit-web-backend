from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from rest_framework import status 
from django.contrib.auth.models import User
from api.models import UserProfile,Event,Expense,Donation,FormMetaData,FormResponse
from api.serializers import UserProfileSerializer,EventSerializer
import json


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
            #serializer = UserProfileSerializer(request.user.userprofile)
            #serializer.update(request.data)
            #if serializer.is_valid():
            #    serializer.save() 
            #user_profile.save()
            user_profile.save()
            print('New credentials are:')
            print(user_profile.__dict__)
            return Response(status = status.HTTP_200_OK, data = {'message' : 'Updated'})

        except Exception as e:
            print(e)
            print(type(e))
            return Response(data = {'message': 'Update failed'},status = 400)

class EventView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    def post(self,request):
        data = request.data
        new_event = Event.objects.create(data)
        new_event.save()
        serializer = EventSerializer(new_event)

    