import ast
import json
from json import JSONDecodeError

from django.db import transaction
from django.views.generic import RedirectView
from CustomAuth.forms import ProfessionalsSignupForm, PatientSignupForm
from CustomAuth.serializers.serializers import APIPermissions, UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from CustomAuth.models import User, ProfessionalType
from django.urls import reverse
from allauth.account.views import SignupView, LoginView

# class ProfessionalsSignupView(SignupView):
#     template_name = 'account/signup.html'
#     form_class = ProfessionalsSignupForm
#
#     def get_success_url(self):
#         return reverse("account_email_verification_sent")
#
#
# class PatientSignupView(SignupView):
#     template_name = 'account/signup.html'
#     form_class = PatientSignupForm
#
#     def get_success_url(self):
#         print("Entered.........")
#         return reverse("account_email_verification_sent")
# accounts/views.py

from rest_framework import status, permissions
from rest_framework.response import Response
from CustomAuth.serializers.serializers import UserSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from CustomAuth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages

from Patient.models.patient import MstPatient, MstPatientContact, MstPatientMedicalHistory, MstPatientPaymentDetails#, MstPatientDocs
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime


# @api_view(['POST'])
def userRegister(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def userLogin(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            print("Token: ", token)
            return Response({'status': "Success", "token": str(token), "userID": user.id, "mobileno": user.phone,
                             "email": user.email, "statusCode": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)

        return Response(
            {'status': "Failure", "errorMessage": "Invalid credentials", "errorDescription": "Invalid credentials",
             "statusCode": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def docUpload(request):
#     if request.method == 'POST':
#         json_data = request.data.get('job')
#         data = json_data[0]
#         print("JSON Data", json_data)
#         print("JSON Type", type(json_data))
#         print("JSON Zero", type(json_data[0]))
#         for i in range(len(json_data)):
#             if (len(json_data) > 0):
#                 data = json_data[i]
#                 # for keys in data:
#                 list_of_the_values = list(data.values())
#                 a = list_of_the_values[0]
#                 b = list_of_the_values[1]
#                 c = list_of_the_values[2]
#                 d = list_of_the_values[3]
#                 patientDocs = MstPatientDocs(
#                     Condition=a,
#                     Description=b,
#                     PatientProfileImage=c,
#                     Remarks=d,
#                 )
#                 patientDocs.save()
#         return Response({'status': "Success", "statusCode": status.HTTP_200_OK},
#                         status=status.HTTP_200_OK)
#     else:
#         return Response(
#             {'status': "Failure", "errorMessage": "Request type", "errorDescription": "Request type is not valid",
#              "statusCode": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes((permissions.AllowAny,))
def userLogout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'status': "Success", "statusCode": status.HTTP_200_OK})
        except Exception as e:
            return Response(
                {'status': "Failure", "errorMessage": "Error", "errorDescription": str(e),
                 "statusCode": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def calculate_age(birthdate):
    today = datetime.now().date()
    delta = today - birthdate
    years = delta.days // 365
    return years


##venaktesh added API
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes((permissions.AllowAny,))
def patientRegister(request):
    print("mobile API")
    fs = FileSystemStorage()
    DOB_str = request.data.get('DOB')
    DOB = datetime.strptime(DOB_str, '%Y-%m-%d').date()
    age = calculate_age(DOB)
    email = request.data.get('email')
    docs = request.FILES.getlist('MedicalRecordFile')
    profileImg = request.FILES.getlist('PatientProfileImage')
    # if 'MedicalRecordFile' in request.FILES else None
    if request.method == 'POST':
        try:
            patient = MstPatient(
                PatientID='P' + str(MstPatient.objects.all().count() + 1).zfill(9),
                UserIDFK=User.objects.get(email=email),
                # PatientProfileImage=request.data.get('PatientProfileImage'),
                PatientProfileImage=profileImg[0],
                FirstName=request.data.get('firstname'),
                MiddleName=request.data.get('middlename'),
                LastName=request.data.get('lastname'),
                City=request.data.get('city'),
                State=request.data.get('state'),
                Country=request.data.get('country'),
                Pin=request.data.get('pincode'),
                Gender=request.data.get('gender'),
                BloodGroup=request.data.get('patientbloodgroup'),
                Nationality=request.data.get('nationality'),
                AadharNo=request.data.get('aadhar'),
                MaritalStatus=request.data.get('maritals'),
                SpouseName=request.data.get('spousename'),
                Address=request.data.get('address'),
                DOB=DOB,
                Age=age,
                ActiveFlag='A',
            )
            patient.save()
            print(patient)

            # Contact information
            PatientId = patient.PatientID
            contactdetails = MstPatientContact(
                PatientContactNumber=request.data.get('patcontactno'),
                AlternatNumber=request.data.get('patalternateno'),
                PatientEmailId=request.data.get('patemail'),
                EmergencyContactNumber=request.data.get('emgcontact'),
                EmergencyContactName=request.data.get('emgname'),
                EmergencyContactRelation=request.data.get('emgcontactrelation'),
                ActiveFlag='A',
                PatientID=PatientId,
                # UserIDFK=request.user,
                UserIDFK=User.objects.get(email=email),
                RecordIDFK=patient
            )
            contactdetails.save()
            print(contactdetails)

            # json_data = request.data.get('medHistoryList')
            medrec_data = request.data.get('medrec')
            medicalrecordfile = ast.literal_eval(medrec_data)
            print(medicalrecordfile)
            # medicalrecordfile = data[0]
            for i in range(len(medicalrecordfile)):
                # to save record in local storage
                # medicalrecordsave=fs.save(docs[i].name,docs[i])
                if (len(medicalrecordfile) > 0):
                    data = medicalrecordfile[i]
                    # for keys in data:
                    list_of_the_values = list(data.values())
                    condition = list_of_the_values[0]
                    description = list_of_the_values[1]
                    medicalRecordFile = list_of_the_values[2]
                    remarks = list_of_the_values[3]
                    patientMedDocs = MstPatientMedicalHistory(
                        PreExistingCondition=condition,
                        Description=description,
                        MedicalRecordFile=docs[i],
                        Remarks=remarks,
                        ActiveFlag='A',
                        PatientID=PatientId,
                        # UserIDFK=request.user,
                        UserIDFK=User.objects.get(email=email),
                        RecordIDFK=patient,
                    )
                    patientMedDocs.save()

            # Payment details
            paymentdetails = MstPatientPaymentDetails(
                PatientID=PatientId,
                PaymentType=request.data.get('paymenttype'),
                PaymentMode=request.data.get('paymentmode'),
                InsuranceCompanyName=request.data.get('insurancename'),
                InsuranceNo=request.data.get('insuranceno'),
                ActiveFlag='A',
                # UserIDFK=request.user,
                UserIDFK=User.objects.get(email=email),
                RecordIDFK=patient
            )
            paymentdetails.save()

            return Response({'status': "Success", "statusCode": status.HTTP_200_OK,"patientID":str(PatientId)},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print({'API error': str(e)})
            return Response(
                {'status': "Failure", "errorMessage": "Exception occured", "errorDescription": str(e),
                 "statusCode": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(
            {'status': "Failure", "errorMessage": "Request type", "errorDescription": "Request type is not valid",
             "statusCode": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
