import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Clinic.models.clinic import MstFlag
from CustomAuth.utility import get_user_menu
from Patient.models.appointment import Appointment
from Patient.models.patient import MstPatient, MstPatientContact
from Staff.decorators import allowed_group_users, unauthenticated_user
from Staff.models.doctor import TblDoctorSlot
from Staff.models.professional_Onboarding import (
    HealthProfessionalCertificationDetails,
    HealthProfessionalExperienceDetails,
    HealthProfessionalEducationDetails,
    MstHealthProfessional,
)


@login_required(login_url="account_login")
def book_appointment(request):
    menu_items = get_user_menu(request)
    if request.user.is_authenticated:
        patient = MstPatient.get_all_patients(request)
        obj=list(MstHealthProfessional.objects.select_related('HealthProfessionalExperienceDetails__MstHealthProfessionalIDFK').filter(ActiveFlag='A').values('MstHealthProfessionalIDPK','FirstName','LastName','Designation','Gender','healthprofessionalexperiencedetails__ExperienceYears'))

        if request.method == "POST":
            patientId = request.POST.get("patientId")
            slotId = request.POST.get("slotId")
            BookingType = request.POST.get("bookingType")
            AppointmentType = request.POST.get("appointmentType")
            AppointmentBy = request.POST.get("appointmentDoneBy")
            CenterType = request.POST.get("clinicCentreType")
            get_slot = TblDoctorSlot.getSlot_by_id(slotId)
            appointment = Appointment(
                UserIDFK=request.user,
                PatientIDFK=MstPatient.get_patient_by_patientId(patientId),
                Date=get_slot.SlotDate,
                Time=get_slot.StartTime,
                DoctorIDFK=get_slot.DoctorIdFK,
                SlotIDFK=get_slot,
                BookingType=BookingType,
                AppointmentType=AppointmentType,
                AppointmentBy=AppointmentBy,
                CenterType=CenterType,
                CreatedBy=1,
                UpdatedBy=1,
            )
            appointment.save()

            get_slot.AppointmentIdFK = appointment.AppointmentIDPK
            get_slot.Status = "Booked"
            get_slot.save()
            messages.success(
                request, f"Appointment booked successfully for Date {get_slot.SlotDate}"
            )
            return redirect("book-appointment")
        else:
            return render(
                request,
                "book_appointment.html",
                {
                    "patient": patient,
                    "obj": obj,
                    "menu_items": menu_items,
                    "clinicCentreSubType": MstFlag.objects.filter(
                        FlagName="ClinicSubType"
                    ),
                },
            )
    else:
        return redirect("account_login")


@login_required(login_url="account_login")
def book_appointment_for(request, record_id):
    menu_items = None
    if request.user.is_authenticated:
        menu_items = get_user_menu(request)
    if request.user.is_authenticated:
        patient = MstPatient.get_all_patients(request)
        selected_patient = MstPatient.get_patient_by_id(record_id)
        selected_patient_phone = MstPatientContact.objects.get(RecordIDFK=record_id)
        obj=list(MstHealthProfessional.objects.select_related('HealthProfessionalExperienceDetails__MstHealthProfessionalIDFK').filter(ActiveFlag='A').values('MstHealthProfessionalIDPK','FirstName','LastName','Designation','Gender','healthprofessionalexperiencedetails__ExperienceYears'))

        return render(
            request,
            "book_appointment.html",
            {
                "patient": patient,
                "selected_patient": selected_patient,
                "obj": obj,
                "menu_items": menu_items,
                "selected_patient_phone": selected_patient_phone,
                "clinicCentreSubType": MstFlag.objects.filter(FlagName="ClinicSubType"),
            },
        )
    else:
        return redirect("account_login")




def select_doctor(request, doctor_id):
    if request.user.is_authenticated:
      
      
        try:
            selected_doctor = MstHealthProfessional.objects.get(MstHealthProfessionalIDPK=doctor_id)
            doctor_education = HealthProfessionalEducationDetails.objects.filter(MstHealthProfessionalIDFK=selected_doctor)
            doctor_experience = HealthProfessionalExperienceDetails.objects.filter(MstHealthProfessionalIDFK=selected_doctor)
            doctor_certifications = HealthProfessionalCertificationDetails.objects.filter(MstHealthProfessionalIDFK=selected_doctor)    


            doctor_details = {
                'name': f"{selected_doctor.FirstName} {selected_doctor.LastName}",
                'specialties': selected_doctor.Designation,
                'experiences': [{'MedicalInstitute':experience.MedicalInstituteName,
                                 'ExperienceYears':experience.ExperienceYears,
                                 'JobDescription':experience.JobDescription,
                                 'StartDate':experience.StartDate,
                                 'EndDate':experience.EndDate,
                                 }for experience in doctor_experience],
                'registrationNumber': selected_doctor.NationalRegistration,
                'stateRegistrationNumber':selected_doctor.StateRegistration,
                'email': selected_doctor.EmpEmail,
                'education': [{
                    'qualificationType': edu.QualificationType,
                    'qualificationName': edu.QualificationName,
                    'currentStatus': edu.CurrentStatus,
                    'passingYear': edu.PassingYear,
                }for edu in doctor_education],
                'certifications': [{
                    'certificateName': certification.CertificateName,
                    'issueDate': certification.IssueDate,
                    'expiryDate': certification.ExpiryDate,
                } for certification in doctor_certifications],
            }

            return JsonResponse(doctor_details)
        except MstHealthProfessional.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'})
        except HealthProfessionalEducationDetails.DoesNotExist:
            return JsonResponse({'error': 'Education details not found'})
        except HealthProfessionalExperienceDetails.DoesNotExist:
            return JsonResponse({'error': 'Experience details not found'})
        except HealthProfessionalCertificationDetails.DoesNotExist:
            return JsonResponse({'error': 'Certification details not found'}) 
        
                                                  
    else:
        # Handle unauthenticated user case
        return JsonResponse({'error': 'User not authenticated'})


@login_required(login_url="account_login")
def book_appointment_date_slot(request, doc_id, slot_date):
    if request.user.is_authenticated:
        if request.method == "POST":
            date = datetime.datetime.strptime(slot_date, "%Y-%d-%m").date()
            data = TblDoctorSlot.getSlot(doc_id, date)

            serialized_data = [
                {
                    "SlotId": str(slot.DoctorSlotIdPK),
                    "StartTime": str(slot.StartTime),
                    "EndTime": str(slot.EndTime),
                    "Status": str(slot.Status),
                }
                for slot in data
            ]

            return JsonResponse(serialized_data, safe=False)

    else:
        return redirect("account_login")
