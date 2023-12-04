from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
import datetime

from Staff.decorators import allowed_role_users
from Staff.models.clinic import Clinic
from Staff.models.doctor import TblDoctorSchedule, TblDoctorSlot
from Staff.models.professional_Onboarding import HealthProfessionalPersonalDetails
from Staff.utility import generate_slots, generate_selected_dates


@login_required(login_url="/accounts/login/")
# @allowed_role_users(allowed_roles='1001')
# @permission_required('Doctor_dashboard')
def manage_slot(request):
    if request.method == 'POST':
        # different
        start_date = datetime.datetime.strptime(request.POST.get('slot_start_date'), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.POST.get('slot_end_date'), "%Y-%m-%d")
        SlotDuration = request.POST.get('time_slot')

        # same
        start_time_all = request.POST.get('start_time')
        start_time_same_for_all_days = request.POST.get('start_time_same_for_all_days')
        number_slot_for_all = int(request.POST.get('number_slot'))
        slots_same_for_all_days = request.POST.get('slots_same_for_all_days')
        all_days = request.POST.get('all_days')
        #print("start_time_all", start_time_all)

        # Days of the week44
        monday = request.POST.get('weekday_mon')
        tuesday = request.POST.get('weekday_tue')
        wednesday = request.POST.get('weekday_wed')
        thursday = request.POST.get('weekday_thu')
        friday = request.POST.get('weekday_fri')
        saturday = request.POST.get('weekday_sat')
        sunday = request.POST.get('weekday_sun')

        # Slot start times and numbers
        mon_start_time = request.POST.get('mon_start_time')
        tue_start_time = request.POST.get('tus_start_time')
        wed_start_time = request.POST.get('wed_start_time')
        thu_start_time = request.POST.get('thu_start_time')
        fri_start_time = request.POST.get('fri_start_time')
        sat_start_time = request.POST.get('sat_start_time')
        sun_start_time = request.POST.get('sun_start_time')

        mon_slot_number = request.POST.get('mon_slot_number')
        tue_slot_number = request.POST.get('tus_slot_number')
        wed_slot_number = request.POST.get('wed_slot_number')
        thu_slot_number = request.POST.get('thu_slot_number')
        fri_slot_number = request.POST.get('fri_slot_number')
        sat_slot_number = request.POST.get('sat_slot_number')
        sun_slot_number = request.POST.get('sun_slot_number')

        if all_days:
            no_of_days = (end_date - start_date).days + 1
            #print("no_of_days: ", no_of_days)
            weekdays = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
            #print("weekdays: ", weekdays)
            if slots_same_for_all_days:
                no_of_slots_of_the_day = number_slot_for_all
                if start_time_same_for_all_days:
                    start_time_of_the_day = start_time_all
                    for i in range(7):
                        #print(weekdays[i])
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                            current_date += datetime.timedelta(days=1)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")
                else:  # different start_time_of_the_day
                    start_time_of_the_day = [mon_start_time, tue_start_time, wed_start_time, thu_start_time, fri_start_time, sat_start_time, sun_start_time]
                    for i in range(7):
                        #print(weekdays[i])
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day[i],
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                                #print("----slot_date []----------", slot_date)
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(
                                        schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")

            else:  # different slots_for_all_days
                slots_number = [mon_slot_number, tue_slot_number, wed_slot_number, thu_slot_number, fri_slot_number, sat_slot_number, sun_slot_number]
                if start_time_same_for_all_days:
                    for i in range(7):
                        #print(weekdays[i])
                        start_time_of_the_day = start_time_all
                        no_of_slots_of_the_day = slots_number[i]
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()

                        slot_date = []
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                                #print("----slot_date []----------", slot_date)
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        # slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(
                                        schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")

                else:   # different slots different Time for all days
                    start_time = [mon_start_time, tue_start_time, wed_start_time, thu_start_time, fri_start_time, sat_start_time, sun_start_time]
                    for i in range(7):
                        #print(weekdays[i])
                        start_time_of_the_day = start_time[i]
                        no_of_slots_of_the_day = slots_number[i]
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        # slot_date = generate_selected_dates(start_date, end_date, weekdays)
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        # slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")
        else:  # not for all_days
            weekdays_code = []
            weekdays = []
            if monday:
                weekdays_code.append(0)
                weekdays.append(monday)
            if tuesday:
                weekdays_code.append(1)
                weekdays.append(tuesday)
            if wednesday:
                weekdays_code.append(2)
                weekdays.append(wednesday)
            if thursday:
                weekdays_code.append(3)
                weekdays.append(thursday)
            if friday:
                weekdays_code.append(4)
                weekdays.append(friday)
            if saturday:
                weekdays_code.append(5)
                weekdays.append(saturday)
            if sunday:
                weekdays_code.append(6)
                weekdays.append(sunday)
            #print("different weekdays list: ", weekdays)

            if slots_same_for_all_days:
                no_of_slots_of_the_day = number_slot_for_all
                if start_time_same_for_all_days:
                    start_time_of_the_day = start_time_all
                    for i in range(len(weekdays_code)):
                        #print(weekdays[i])
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        #print(current_date)
                        #print(start_date)
                        #print(end_date)
                        #print("------")
                        #print(current_date.weekday())
                        #print(": ", weekdays.index(weekdays[i]))
                        while current_date <= end_date:
                            #print("i:", current_date)
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                #print("if ..")
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                                #print("slot_date:, ", slot_date)
                            current_date += datetime.timedelta(days=1)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        #print(slot_date)
                        #print(slots)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")
                else:  # different start_time_of_the_day
                    start_time_of_the_day = [mon_start_time, tue_start_time, wed_start_time, thu_start_time,
                                             fri_start_time, sat_start_time, sun_start_time]
                    for i in range(len(weekdays_code)):
                        #print(weekdays[i])
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day[i],
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                                #print("----slot_date []----------", slot_date)
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(
                                        schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")

            else:  # differ slots_for_all_days
                slots_number = []
                if mon_slot_number:
                    slots_number.append(int(mon_slot_number))
                if tue_slot_number:
                    slots_number.append(int(tue_slot_number))
                if wed_slot_number:
                    slots_number.append(int(wed_slot_number))
                if thu_slot_number:
                    slots_number.append(int(thu_slot_number))
                if fri_slot_number:
                    slots_number.append(int(fri_slot_number))
                if sat_slot_number:
                    slots_number.append(int(sat_slot_number))
                if sun_slot_number:
                    slots_number.append(int(sun_slot_number))
                if start_time_same_for_all_days:
                    for i in range(len(weekdays_code)):
                        #print(weekdays[i])
                        start_time_of_the_day = start_time_all
                        no_of_slots_of_the_day = slots_number[i]
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                                #print("----slot_date []----------", slot_date)
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        # slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(
                                        schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")
                else:   # different slots different Time for all days
                    start_time = []
                    if mon_start_time:
                        start_time.append(mon_start_time)
                    if tue_start_time:
                        start_time.append(tue_start_time)
                    if wed_start_time:
                        start_time.append(wed_start_time)
                    if thu_start_time:
                        start_time.append(thu_start_time)
                    if fri_start_time:
                        start_time.append(fri_start_time)
                    if sat_start_time:
                        start_time.append(sat_start_time)
                    if sun_start_time:
                        start_time.append(sun_start_time)
                    for i in range(len(weekdays_code)):
                        #print(weekdays[i])
                        start_time_of_the_day = start_time[i]
                        no_of_slots_of_the_day = slots_number[i]
                        schedule = TblDoctorSchedule(DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                                     UserIdFK=request.user,
                                                     ClinicIdFK=Clinic.get_clinic_id(),
                                                     StartDate=start_date,
                                                     EndDate=end_date,
                                                     SlotDuration=SlotDuration,
                                                     Day=weekdays[i],
                                                     StartTime=start_time_of_the_day,
                                                     NoofSlots=no_of_slots_of_the_day)
                        schedule.save()
                        slot_date = []
                        current_date = start_date
                        # slot_date = generate_selected_dates(start_date, end_date, weekdays)
                        while current_date <= end_date:
                            if current_date.weekday() == weekdays.index(weekdays[i]):
                                slot_date.append(current_date.strftime('%Y-%m-%d'))
                            current_date += datetime.timedelta(days=1)
                        #print("slot_date: ", slot_date)
                        slots = generate_slots(start_time_of_the_day, SlotDuration, no_of_slots_of_the_day)
                        # slots = generate_slots(start_time_of_the_day[i], SlotDuration, no_of_slots_of_the_day)
                        for j in range(len(slot_date)):
                            for k in range(no_of_slots_of_the_day):
                                slot = TblDoctorSlot(
                                    DoctorScheduleIdFK=TblDoctorSchedule.get_schedule_by_id(
                                        schedule.DoctorScheduleIdPK),
                                    DoctorIdFK=HealthProfessionalPersonalDetails.get_doctor_id(request.user),
                                    UserIdFK=request.user,
                                    ClinicIdFK=Clinic.get_clinic_id(),
                                    SlotDate=slot_date[j],
                                    Day=weekdays[i],
                                    StartTime=slots[k][0],
                                    EndTime=slots[k][1],
                                    Status='Available',
                                    AppointmentIdFK=0)
                                slot.save()
                                #print("slots: ", slots)
                                #print("----------------------------------------------------")

        return render(request, 'slot_management.html', {'msg': 'Slot created...'})
    else:
        return render(request, 'slot_management.html')
