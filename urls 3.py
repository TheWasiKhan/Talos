from django.urls import path
from Clinic.views import clinic_onboarding, clinic_dashboard,clinic_book_appointment,preExamination

urlpatterns = [
    path('Clinic-onboarding/', clinic_onboarding.clinic_onboarding, name='clinic_onboarding'),
    path('', clinic_dashboard.clinic_dashboard, name='clinic_dashboard'),
    path('Clinic-Book-Appointment/', clinic_book_appointment.clinic_book_appointment, name='clinic_book_appointment'),
    path('Clinic-Book-Appointment-For/<int:record_id>/', clinic_book_appointment.clinic_book_appointment_for, name='clinic_book_appointment_for'),
    path('Clinic-Book-Appointment/<int:doc_id>/<str:slot_date>/', clinic_book_appointment.clinic_book_appointment_date_slot, name='clinic_book_appointment_date_slot'),
    path('Pre-Examination/', preExamination.preExamineList, name='preExamineList'),
    path('Pre-Examination/<int:appointment_id>/', preExamination.preExamine, name='preExamine'),
    path('Medical-History/<int:appointment_id>/', preExamination.medicalHistory, name='medicalHistory'),

    ]
