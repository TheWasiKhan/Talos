import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Patient.models.appointment import Appointment
from Patient.models.patient import MstPatient
from Staff.decorators import allowed_group_users, unauthenticated_user
from Staff.models.doctor import TblDoctorSlot
from Staff.models.professional_Onboarding import HealthProfessionalPersonalDetails


@login_required(login_url='account_login')
def book_appointment(request):
    if request.user.is_authenticated:
        patient = MstPatient.get_all_patients()
        doctor_list = HealthProfessionalPersonalDetails.get_doctors_list()
        if request.method == 'POST':
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
                CreatedBy=request.user.id,
                UpdatedBy=request.user.id)
            appointment.save()

            get_slot.AppointmentIdFK = appointment.AppointmentIDPK
            get_slot.Status = 'Booked'
            get_slot.save()
            messages.success(request, f'Appointment booked successfully for Date {get_slot.SlotDate}')
            return redirect("book-appointment")
        else:
            return render(request, 'book_appointment.html', {'patient': patient, 'doctor_list': doctor_list})
    else:
        return redirect('account_login')


@login_required(login_url='account_login')
def book_appointment_for(request, record_id):
    if request.user.is_authenticated:
        patient = MstPatient.get_all_patients()
        selected_patient = MstPatient.get_patient_by_id(record_id)
        doctor_list = HealthProfessionalPersonalDetails.get_doctors_list()
        return render(request, 'book_appointment.html',
                      {'patient': patient, 'selected_patient': selected_patient, 'doctor_list': doctor_list})
    else:
        return redirect('account_login')


def select_doctor(request, doctor_id):
    if request.user.is_authenticated:
        selected_doctor = HealthProfessionalPersonalDetails.get_doctor(doctor_id)
        #print("selected_doctor: ", selected_doctor)
    else:
        return redirect('account_login')


@login_required(login_url='account_login')
def book_appointment_date_slot(request, doc_id, slot_date):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #print(slot_date, "---", doc_id)
            date = datetime.datetime.strptime(slot_date, "%Y-%d-%m").date()
            #print(date)
            data = TblDoctorSlot.getSlot(doc_id, date)

            serialized_data = [
                {
                    'SlotId': str(slot.DoctorSlotIdPK),
                    'StartTime': str(slot.StartTime),
                    'EndTime': str(slot.EndTime),
                    'Status': str(slot.Status)
                }
                for slot in data
            ]

            return JsonResponse(serialized_data, safe=False)

    else:
        return redirect('account_login')
