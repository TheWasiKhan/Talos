from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages

from CustomAuth.utility import get_user_menu
from Patient.models.appointment import Appointment
from Patient.models.patient import MstPatient, MstPatientMedicalHistory, MstPatientContact, MstPatientPaymentDetails
from django.db import transaction
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage


@login_required(login_url='account_login')
# @allowed_group_users(allowed_group=['Admin'])
def patient_dashboard(request):
    if request.user.is_authenticated:
        menu_items = get_user_menu(request)
        appointments = Appointment.objects.filter(UserIDFK=request.user, )
        return render(request, 'patient_dashboard.html', {'menu_items': menu_items, 'appointments': appointments})
    else:
        return redirect('account_login')


today = datetime.now().date()


def calculate_age(birthdate):
    today = datetime.now().date()
    delta = today - birthdate
    years = delta.days // 365
    months = (delta.days % 365) // 30  # Assuming an average month has 30 days
    days = delta.days % 30

    if years < 1:
        if months < 1:
            return f"{days} days"
        else:
            return f"{months} months and {days} days"
    else:
        return f"{years} years"


def patient_registration(request):
    menu_items = None
    if request.user.is_authenticated:
        menu_items = get_user_menu(request)
    if request.method == 'GET':
        # MstPatientdata=MstPatient.objects.all()
        print('in get')
        obj = list(MstPatient.objects
                   .select_related('mstpatientcontact__RecordIDFK')
                   .filter(ActiveFlag='A')
                   .values('PatientID', 'FirstName', 'MiddleName', 'LastName', 'Gender', 'Age', 'BloodGroup',
                           'mstpatientcontact__PatientEmailId', 'AadharNo', 'MaritalStatus', 'SpouseName',
                           'mstpatientcontact__PatientContactNumber',
                           'Nationality', 'Address', 'City', 'State', 'Country', 'Pin',
                           'mstpatientcontact__EmergencyContactName', 'mstpatientcontact__EmergencyContactNumber',
                           'mstpatientcontact__EmergencyContactRelation'))

        # print(obj)
        if obj:
            return render(request, 'patient_registration.html', {'obj': obj, 'menu_items': menu_items})
        else:
            msg = "No Registerd Patient"
            al = "danger"
            return render(request, 'patient_registration.html', {'msg': msg, 'al': al, 'menu_items': menu_items})
    else:
        fs = FileSystemStorage()
        print('in post')
        profilepic = request.FILES.get('fileInput', None)
        if profilepic:
            profilepicsave = fs.save(profilepic.name, profilepic)
        else:
            profilepicsave = 'https://bootdey.com/img/Content/avatar/avatar7.png'

        DOB_str = request.POST.get('age', None)
        DOB = datetime.strptime(DOB_str, '%Y-%m-%d').date()
        age = calculate_age(DOB)

        preexistingcondition = request.POST.getlist('pretype'),
        description = request.POST.getlist('descrptn'),
        medicalrecordfile = request.FILES.getlist('medrec')

        remarks = request.POST.getlist('remarks')
        print(medicalrecordfile)
        try:
            with transaction.atomic():

                patient = MstPatient(
                    PatientID='P' + str(MstPatient.objects.all().count() + 1).zfill(9),
                    UserIDFK=request.user,
                    FirstName=request.POST.get('firstname', None),
                    MiddleName=request.POST.get('middlename', None),
                    LastName=request.POST.get('lastname', None),
                    City=request.POST.get('city', None),
                    State=request.POST.get('state', None),
                    Country=request.POST.get('country', None),
                    Pin=request.POST.get('pincode', None),
                    Gender=request.POST.get('gender', None),
                    BloodGroup=request.POST.get('patientbloodgroup', None),
                    Nationality=request.POST.get('nationality', None),
                    AadharNo=request.POST.get('aadhar', None),
                    MaritalStatus=request.POST.get('maritals', None),
                    SpouseName=request.POST.get('spousename', None),
                    Address=request.POST.get('address', None),
                    DOB=DOB,
                    Age=age,
                    ActiveFlag='A',
                    PatientProfileImage=profilepicsave)
                patient.save()

                PatientId = patient.PatientID

                contactdetails = MstPatientContact(
                    PatientContactNumber=request.POST.get('patcontactno', None),
                    Occupation=request.POST.get('occupation', None),
                    PatientEmailId=request.POST.get('patemail', None),
                    EmergencyContactNumber=request.POST.get('emgcontact', None),
                    EmergencyContactName=request.POST.get('emgname', None),
                    EmergencyContactRelation=request.POST.get('emgcontactrelation', None),
                    ActiveFlag='A',
                    PatientID=PatientId,
                    UserIDFK=request.user,
                    RecordIDFK=patient

                )
                contactdetails.save()

                # for i in range(len(medicalrecordfile)):
                #     if i < len(description[0]) and i < len(medicalrecordfile[0]) and i < len(remarks):
                #         medicalrecordsave = fs.save(medicalrecordfile[i].name, medicalrecordfile[i])
                #         medicalhistory = MstPatientMedicalHistory(
                #             ActiveFlag='A',
                #             PatientID=PatientId,
                #             UserIDFK=request.user,
                #             RecordIDFK=patient,
                #             PreExistingCondition=preexistingcondition[0][i],
                #             Description=description[0][i],
                #             MedicalRecordFile=medicalrecordsave,
                #             Remarks=remarks[i],
                #             # id=MstPatientMedicalHistory.objects.all().count() + 1,
                #         )
                #         print(i)
                #         medicalhistory.save()
                #         print(medicalhistory, 'mh')
                #
                # paymentdetails = MstPatientPaymentDetails(
                #     PatientID=PatientId,
                #     PaymentType=request.POST.get('paymenttype', None),
                #     PaymentMode=request.POST.get('paymentmode', None),
                #     InsuranceCompanyName=request.POST.get('insurancename', None),
                #     InsuranceNo=request.POST.get('insuranceno', None),
                #     InsuranceType=request.POST.get('typeinsurance', None),
                #     ActiveFlag='A',
                #     UserIDFK=request.user,
                #     RecordIDFK=patient
                #
                # )
                # paymentdetails.save()

                messages.success(request, f'Registration Successful! for {request.POST.get("firstname")}')
                return redirect('patient_registration')
        except Exception as e:
            messages.error(request, {'Not Submitted': str(e)})
            print({'Not Submitted': str(e)})
            return redirect('patient_registration')


def edit_patient_details(request):
    if request.method == 'POST':
        fullname = request.POST.get('mfullname').split()
        first_name = fullname[0] if fullname else ''
        middle_name = fullname[1] if len(fullname) > 1 else ''
        last_name = ' '.join(fullname[2:]) if len(fullname) > 2 else ''

        DOB_str = request.POST.get('mage')
        DOB = datetime.strptime(DOB_str, '%Y-%m-%d').date()
        age = calculate_age(DOB)

        try:
            with transaction.atomic():
                PatientID = request.POST.get('patientid')
                MstPatient.objects.filter(PatientID=PatientID, ActiveFlag='A').update(ActiveFlag='I')

                patient = MstPatient(
                    PatientID=request.POST.get('patientid'),
                    UserIDFK=request.user,
                    FirstName=first_name,
                    MiddleName=middle_name,
                    LastName=last_name,
                    City=request.POST.get('mcity', None),
                    State=request.POST.get('mstate', None),
                    Country=request.POST.get('mcountry', None),
                    Pin=request.POST.get('mpin', None),
                    Gender=request.POST.get('mGender', None),
                    BloodGroup=request.POST.get('mbloodgroup', None),
                    Nationality=request.POST.get('mnationality', None),
                    AadharNo=request.POST.get('maadhar', None),
                    MaritalStatus=request.POST.get('mmaritalstatus', None),
                    SpouseName=request.POST.get('mspousename', None),
                    Address=request.POST.get('maddress', None),
                    DOB=DOB,
                    Age=age,
                    ActiveFlag='A',
                    PatientProfileImage="https://encrypted-tbn0.gstatic.com")
                patient.save()

                MstPatientContact.objects.filter(PatientID=PatientID, ActiveFlag='A').update(ActiveFlag='I')

                contactdetails = MstPatientContact(
                    PatientID=request.POST.get('patientid'),
                    PatientContactNumber=request.POST.get('mcontactno'),

                    PatientEmailId=request.POST.get('memailid'),
                    EmergencyContactNumber=request.POST.get('emcontactno'),
                    EmergencyContactName=request.POST.get('memergencypersonname'),
                    EmergencyContactRelation=request.POST.get('mrelation'),
                    ActiveFlag='A',
                    UserIDFK=request.user,
                    RecordIDFK=patient
                )
                contactdetails.save()

                messages.info(request, 'Updated Successfully!')
                return redirect('patient_registration')

        except Exception as e:
            print(e)
            messages.warning(request, "Not Submitted edited ", e)
            return (request, {'error_message': str(e)})


def call_patient(request):
    menu_items = None
    if request.user.is_authenticated:
        menu_items = get_user_menu(request)
    return render(request, 'call.html', {'menu_items': menu_items})
