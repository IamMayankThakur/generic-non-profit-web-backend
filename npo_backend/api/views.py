from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from django.contrib.auth.models import User
from api.models import UserProfile
import json


class HelloView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UpdateDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            data = json.loads(request.data)
            #print(request.data)
            print(data)
            user_profile = request.user.userprofile 
            #print(user_profile.__dict__)
            #print(data.values())
            print('*****')
            for key,value in data.values():
                print(key,value)
                user_profile[key] = value
            
            user_profile.save()
            #user_profile.__dict__.update(data)
            #user_profile.save()
            return Response(status = status.HTTP_200_OK, data = {'message' : 'Updated'})

        except Exception as e:
            print(e)
            return Response(data = {'message': 'Update failed'},status = 400)



