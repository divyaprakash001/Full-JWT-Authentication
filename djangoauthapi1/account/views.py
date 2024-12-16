from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import status
from .serializers import UserSerializer,UserLoginSerializer,UserProfileSerializer,UserChangeSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request, format=None):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user=serializer.save()
      token = get_tokens_for_user(user)
      return Response({'msg':"Registration Success","token":token},status=status.HTTP_201_CREATED)
    return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    try:
      serializer = UserLoginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email',None)
        password = serializer.data.get('password',None)
        if email is not None and password is not None:
          user = authenticate(email=email, password=password)
          if user is not None:
            token=get_tokens_for_user(user)
            return Response({'msg':'Login Success','token':token}, status=status.HTTP_200_OK)
          else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        else:
          return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as errors:
        return Response({'errors_msg':'Something went wrong','error':errors}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes=[permissions.IsAuthenticated]

  def get(self,request,format=None):
    print(request.user)
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [permissions.IsAuthenticated]

  def post(self,request,format=None):
    serializer  = UserChangeSerializer(data=request.data,context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':"Password Changed Suucessfully"}, status=status.HTTP_200_OK)
    
class SendPasswordPasswordEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data,context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':"Password Reset link send. Please check your email"})

class UserPasswordResetView(APIView):
  renderer_classes=[UserRenderer]
  def post(self,request, uid, token ,format=None):
    serializer=UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':"Password Reset Successfully."},status=status.HTTP_200_OK)
      
