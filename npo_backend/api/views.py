from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile


# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


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
