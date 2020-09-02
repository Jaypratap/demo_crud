from django.shortcuts import render

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
# Django library
from django.contrib.auth import authenticate, login, logout
from otp.models import User, firstOTP
from otp.forms import UserRegistrationForm, generateOTPForm
import random

from django.core.mail import EmailMessage, send_mail

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


def home(request):
    return render(request, 'home.html', {})



@api_view(['POST'])
def generateotp(request):
    try:
        email = request.data['email']
        print(email)
        instance = firstOTP()
        form = generateOTPForm(email)
        onetimeotp = random.randrange(000000,999999)
        print(onetimeotp)
        from_mail = 'pratappandey7@gmail.com'
        send_message = "Your one time password is: " + str(onetimeotp)
        try:
            if firstOTP.objects.get(email=email):
                return Response({"message": "email already exists"}, status=HTTP_400_BAD_REQUEST)
        except:
            print("sss")
            instance.email = email
            instance.otp = onetimeotp
            instance.save()
            send_mail("No Reply", send_message, from_mail, email,
                       fail_silently=False)
            return Response({'message': "otp goes to your mail please check!"}, status=HTTP_200_OK)
    except:
        return Response({'message': "something went wrong!"}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verifyotp(request):
    try:
        email = request.data['email']
        otp = request.data['otp']
        original = firstOTP.objects.filter(email=email).values('otp')
        original = int(original[0]['otp'])
        if original==otp:
            instance = firstOTP.objects.get(email=email)
            instance.is_verified=1
            instance.save()
            return Response({"message": "OTP verified successfully"}, status=HTTP_200_OK)
        else:
            return Response({"message": "OTP didn't Match"}, status=HTTP_400_BAD_REQUEST)

    except:
        return Response({'message': 'Something goes wrong!'}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data['email']
        temp = firstOTP.objects.filter(email=email).values('is_verified')
        print("temp", temp[0]['is_verified'])
        if (temp[0]['is_verified']==True):
            form = UserRegistrationForm(request.data)
            if form.is_valid():
                print("In Form")
                form.save()
                email = request.data['email']
                # print(request.data['password2'])
                return_message = "Successfully Register " + email
                return Response({"message": return_message}, status=HTTP_200_OK)
            else:
                return Response({"message": form.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "something wrong"}, status=HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes(['IsAuthenticated'])
def registerfinal(request):
    try:
        email = request.data['email']
        instance = User.objects.get(email=email)
        instance.is_verified = 1
        instance.save()
        return Response({"message":"updated"}, status=HTTP_200_OK)
    except:
        return Response({"message":"Something went wrong"}, status=HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        registerStatus = User.objects.filter(email=email).values('is_verified')
        if registerStatus[0]['is_verified']==False:
            return Response({"message", "User Not Approve by Admin"}, status=HTTP_400_BAD_REQUEST)
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        else:
            message = "Either Email or password is Wrong"
            return Response({'message': message}, status=HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'Either Email or password are wrong'}, status=HTTP_400_BAD_REQUEST)


@permission_classes(['IsAuthenticated'])
def updateuserType(request):
    try:
        print(request.user)
        print(request.data['userType'])
        return Response({"mess":"dfadkf"}, status=HTTP_200_OK)
    except:
        return Response({"mess":"ppppp"}, status=HTTP_400_BAD_REQUEST)

@permission_classes(['IsAuthenticated'])
class updatetype(APIView):
    def put(self, request):
        try:
            new_type = request.data['Type']
            user_email = request.user
            instance = User.objects.get(email=user_email)
            instance.userType = new_type
            instance.save()
            return Response({"message":"Type Updated"}, status=HTTP_200_OK)
        except:
            return Response({"messge":"Something went wrong"}, HTTP_400_BAD_REQUEST)