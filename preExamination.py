from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from CustomAuth.utility import get_user_menu
from Patient.views.manage_patient import calculate_age
from Staff.models.consultation import Vitals, Symptoms, PreExisting, Document
from Patient.models.appointment import Appointment
from Clinic.models.MedicalHistory import (
    ChiefComplaint,
    PastMedicalHistory,
    PersonalHistory,
    FamilyHistory,
    CardiovascularSymptoms,
    NervousSystemSymptoms,
    MusculoskeletalSymptoms,
    GenitourinarySymptoms,
    GastrointestinalSymptoms,
    RespiratorySymptoms,
    EndocrineSymptoms,
    GpeDetails,
    CardiovascularSystem,
    RespiratorySystem,
    GastrointestinalSystem,
    GenitourinarySystem,
    MusculoskeletalSystem,
    NervousSystem,
)


@login_required(login_url="/accounts/login/")
def preExamineList(request):
    if request.method == "GET":
        doc_con_list = Appointment.objects.all()
        menu_items = get_user_menu(request)
        return render(
            request,
            "pre-examine-list.html",
            {"doc_con_list": doc_con_list, "menu_items": menu_items},
        )


@login_required(login_url="/accounts/login/")
def preExamine(request, appointment_id):
    menu_items = None
    if request.user.is_authenticated:
        menu_items = get_user_menu(request)
    try:
        # Retrieve the appointment details or raise a 404 if not found
        appointment_detail = get_object_or_404(
            Appointment, AppointmentIDPK=appointment_id
        )
        # print("appointment_detail", appointment_detail)

        try:
            vitals = Vitals.objects.get(appointment_id=appointment_id)
        except Vitals.DoesNotExist:
            vitals = None  # Set a default value or handle as needed

        try:
            # Assuming you have a ForeignKey relationship between Document and Appointment
            documents = Document.objects.filter(appointment_id=appointment_id)
        except Document.DoesNotExist:
            documents = None  # Set a default value or handle as needed

        try:
            # Assuming you have a ForeignKey relationship between Document and Appointment
            preexistings = PreExisting.objects.get(appointment_id=appointment_id)
        except PreExisting.DoesNotExist:
            preexistings = None  # Set a default value or handle as needed

        try:
            symptoms = Symptoms.objects.get(appointment_id=appointment_id)
        except Symptoms.DoesNotExist:
            symptoms = None  # Set a default value or handle as needed

        # Assuming you have a serializer for your Appointment model
        # Adjust the serializer class based on your actual model structure

        # Calculate age based on date of birth and appointment date
        dob = appointment_detail.PatientIDFK.DOB
        age = calculate_age(dob)

        serializer_data = {
            "patient_name": appointment_detail.PatientIDFK.FirstName
            + " "
            + appointment_detail.PatientIDFK.LastName,
            "contact_number": request.user.phone,
            "gender": appointment_detail.PatientIDFK.Gender,
            "age": age,
            "appointment_date": appointment_detail.Date,
            "patient_image": appointment_detail.PatientIDFK.PatientProfileImage,
            "dob": dob,
            "patient_id": appointment_detail.PatientIDFK.PatientID,
            "appointment_id": appointment_id,
            "appointment_by": appointment_detail.CreatedBy,
            "booking_type": appointment_detail.BookingType,
            "appointment_type": appointment_detail.AppointmentType,
        }

        context = {
            "appointments": Appointment.objects.all(),
            "appointment_detail": serializer_data,
            "vitals": vitals,
            "documents": documents,
            "symptoms": symptoms,
            "preexistings": preexistings,
            "menu_items": menu_items,
        }
        return render(request, "PreExamination.html", context)

    except Appointment.DoesNotExist:
        context = {
            "appointments": Appointment.objects.all(),
            "error_message": "Appointment not found",
            "menu_items": menu_items,
        }
        return render(request, "PreExamination.html", context)

    except Exception as e:
        # Handle other exceptions (e.g., database errors) here
        # print(e)
        context = {
            "appointments": Appointment.objects.all(),
            "error_message": f"Error: {str(e)}",
            "menu_items": menu_items,
        }
        return render(request, "PreExamination.html", context)


@login_required(login_url="/accounts/login/")
def medicalHistory(request, appointment_id):
    if request.method == "GET":
        return render(
            request,
            "MedicalHistory.html",
            {"appointment_id": appointment_id},
        )

    elif request.method == "POST":
            appointment=Appointment.objects.get(AppointmentIDPK=appointment_id)
            try:
                with transaction.atomic():
                    problem = request.POST.getlist("problem")
                    onset = request.POST.getlist("onset")
                    site = request.POST.getlist("site")
                    progression = request.POST.getlist("progression")
                    duration = request.POST.getlist("duration")
                    frequency = request.POST.getlist("frequency")
                    color = request.POST.getlist("color")
                    grade = request.POST.getlist("grade")
                    radiating_to = request.POST.getlist("radiating_to")
                    relieving_factor = request.POST.getlist("relieving_factor")
                    aggravating_factor = request.POST.getlist("aggravating_factor")
                    smell = request.POST.getlist("smell")
                    ChiefComplaint.objects.filter(AppointmentIDFK=appointment).delete()
                    for i in range(len(request.POST.getlist("problem"))):
                        ChiefComplaint.objects.create(
                            Problem=problem[i],
                            AppointmentIDFK=appointment,
                            Onset=onset[i],
                            Site=site[i],
                            Progression=progression[i],
                            Duration=duration[i],
                            Frequency=frequency[i],
                            Color=color[i],
                            Grade=grade[i],
                            RadiatingTo=radiating_to[i],
                            Relieving_Factor=relieving_factor[i],
                            Aggravating_Factor=aggravating_factor[i],
                            Smell=smell[i],
                        )

                    past_disease = request.POST.getlist("past_disease")
                    disease_details = request.POST.getlist("disease_details")
                    PastMedicalHistory.objects.filter(AppointmentIDFK=appointment).delete()
                    for i in range(len(request.POST.getlist("past_disease"))):
                        PastMedicalHistory.objects.create(
                            AppointmentIDFK=appointment,
                            PastDisease=past_disease[i],
                            DiseaseDetails=disease_details[i],
                        )

                    smoking = request.POST.get("smoking")
                    alcohol = request.POST.get("alcohol")
                    sleep = request.POST.get("sleep")
                    allergy = request.POST.get("allergy")
                    bowel_bladder_habits = request.POST.get("bowel_bladder_habits")
                    appetite = request.POST.get("appetite")
                    PersonalHistory.objects.filter(AppointmentIDFK=appointment).delete()
                    PersonalHistory.objects.create(
                        AppointmentIDFK=appointment,
                        Smoking=smoking,
                        Alcohol=alcohol,
                        Sleep=sleep,
                        Allergy=allergy,
                        BowelBladderHabits=bowel_bladder_habits,
                        Appetite=appetite,
                    )

                    past_disease = request.POST.getlist("disease")
                    disease_details = request.POST.getlist("disease_details1")
                    FamilyHistory.objects.filter(AppointmentIDFK_id=appointment.AppointmentIDPK).delete()
                    for i in range(len(request.POST.getlist("disease"))):
                        FamilyHistory.objects.create(
                            AppointmentIDFK_id=appointment.AppointmentIDPK,
                            Disease=past_disease[i],
                            DiseaseDetails=disease_details[i],
                        )

                    breathlessness = request.POST.get("breathlessness1")
                    palpitations = request.POST.get("palpitations")
                    chest_pain = request.POST.get("chest_pain")
                    fainting = request.POST.get("fainting1")
                    ankle_edema = request.POST.get("ankle_edema")
                    CardiovascularSymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    CardiovascularSymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Breathlessness=breathlessness,
                        Palpitations=palpitations,
                        ChestPain=chest_pain,
                        Fainting=fainting,
                        AnkleEdema=ankle_edema,
                    )

                    headache = request.POST.get("headache")
                    dizziness = request.POST.get("dizziness")
                    fainting = request.POST.get("fainting2")
                    tremors = request.POST.get("tremors")
                    seizure = request.POST.get("seizure")
                    tinnitus = request.POST.get("tinnitus")
                    deafness = request.POST.get("deafness")
                    vision_loss = request.POST.get("vision_loss")
                    memory_loss = request.POST.get("memory_loss")
                    NervousSystemSymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    NervousSystemSymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Headache=headache,
                        Dizziness=dizziness,
                        Fainting=fainting,
                        Tremors=tremors,
                        Seizure=seizure,
                        Tinnitus=tinnitus,
                        Deafness=deafness,
                        VisionLoss=vision_loss,
                        MemoryLoss=memory_loss,
                    )

                    joint_pain = request.POST.get("joint_pain")
                    immobility = request.POST.get("immobility")
                    redness = request.POST.get("redness")
                    swelling = request.POST.get("swelling1")
                    MusculoskeletalSymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    MusculoskeletalSymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        JointPain=joint_pain,
                        Immobility=immobility,
                        Redness=redness,
                        Swelling=swelling,
                    )

                    multiple_sexual_partners = request.POST.get("multiple_sexual_partners")
                    libido = request.POST.get("libido")
                    burning_micturition = request.POST.get("burning_micturition")
                    painful_micturition = request.POST.get("painful_micturition")
                    overactive_bladder = request.POST.get("overactive_bladder")
                    incontinence = request.POST.get("incontinence")
                    bloody_urine = request.POST.get("bloody_urine")
                    lmp = request.POST.get("lmp")
                    white_discharge = request.POST.get("white_discharge")
                    foul_smelling_secretions = request.POST.get("foul_smelling_secretions")
                    itching = request.POST.get("itching")
                    periods_duration = request.POST.get("periods_duration")
                    dysmenorrhoea = request.POST.get("dysmenorrhoea")
                    painful_coitus = request.POST.get("painful_coitus")
                    GenitourinarySymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    GenitourinarySymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        MultipleSexualPartners=multiple_sexual_partners,
                        Libido=libido,
                        BurningMicturition=burning_micturition,
                        PainfulMicturition=painful_micturition,
                        OveractiveBladder=overactive_bladder,
                        Incontinence=incontinence,
                        BloodyUrine=bloody_urine,
                        LMP=lmp,
                        WhiteDischarge=white_discharge,
                        FoulSmellingSecretions=foul_smelling_secretions,
                        Itching=itching,
                        PeriodsDuration=periods_duration,
                        Dysmenorrhoea=dysmenorrhoea,
                        PainfulCoitus=painful_coitus,
                    )

                    heartburn = request.POST.get("heartburn")
                    acidity = request.POST.get("acidity")
                    nausea = request.POST.get("nausea")
                    vomiting = request.POST.get("vomiting")
                    pain_abdomen = request.POST.get("pain_abdomen")
                    indigestion = request.POST.get("indigestion")
                    change_in_stool_color = request.POST.get("change_stool_color")
                    GastrointestinalSymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    GastrointestinalSymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Heartburn=heartburn,
                        Acidity=acidity,
                        Nausea=nausea,
                        Vomiting=vomiting,
                        PainAbdomen=pain_abdomen,
                        Indigestion=indigestion,
                        ChangeInStoolColor=change_in_stool_color,
                    )

                    cough = request.POST.get("cough")
                    blood_in_sputum = request.POST.get("blood_sputum")
                    breathlessness = request.POST.get("breathlessness2")
                    painful_breathing = request.POST.get("painful_breathing")
                    RespiratorySymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    RespiratorySymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Cough=cough,
                        BloodInSputum=blood_in_sputum,
                        Breathlessness=breathlessness,
                        PainfulBreathing=painful_breathing,
                    )

                    heat_intolerance = request.POST.get("heat_intolerance")
                    cold_intolerance = request.POST.get("cold_intolerance")
                    heavy_sweating = request.POST.get("heavy_sweating")
                    polydipsia = request.POST.get("polydipsia")
                    polyuria = request.POST.get("polyuria")
                    EndocrineSymptoms.objects.filter(AppointmentIDFK=appointment).delete()
                    EndocrineSymptoms.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        HeatIntolerance=heat_intolerance,
                        ColdIntolerance=cold_intolerance,
                        HeavySweating=heavy_sweating,
                        Polydipsia=polydipsia,
                        Polyuria=polyuria,
                    )

                    mental_state = request.POST.get("mental_state")
                    cyanosis = request.POST.get("cyanosis")
                    clubbing = request.POST.get("clubbing")
                    pallor = request.POST.get("pallor")
                    icterus = request.POST.get("icterus")
                    lymphadenopathy = request.POST.get("lymphadenopathy")
                    edema = request.POST.get("edema")
                    body_built = request.POST.get("body_built")
                    gait = request.POST.get("gait")
                    height = request.POST.get("height")
                    weight = request.POST.get("weight")
                    GpeDetails.objects.filter(AppointmentIDFK=appointment).delete()
                    GpeDetails.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        MentalState=mental_state,
                        Cyanosis=cyanosis,
                        Clubbing=clubbing,
                        Pallor=pallor,
                        Icterus=icterus,
                        Lymphadenopathy=lymphadenopathy,
                        Edema=edema,
                        BodyBuilt=body_built,
                        Gait=gait,
                        Height=height,
                        Weight=weight,
                    )

                    pulse = request.POST.get("pulse2")
                    heart_sounds = request.POST.get("heart_sounds")
                    jvp = request.POST.get("jvp")
                    chest_wall_abnormalities = request.POST.get("chest_wall")
                    engorged_veins = request.POST.get("engorged_veins")
                    cardiovascular_auscultation = request.POST.get("cardiovascular_auscultation")
                    CardiovascularSystem.objects.filter(AppointmentIDFK=appointment).delete()
                    CardiovascularSystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Pulse=pulse,
                        HeartSounds=heart_sounds,
                        JVP=jvp,
                        ChestWallAbnormalities=chest_wall_abnormalities,
                        EngorgedVeins=engorged_veins,
                        CardiovascularAuscultation=cardiovascular_auscultation,
                    )

                    chest_shape = request.POST.get("chest_shape")
                    chest_movement = request.POST.get("chest_movement")
                    auscultation = request.POST.get("auscultation")
                    percussion = request.POST.get("percussion1")
                    trachea_position = request.POST.get("trachea_position")
                    vocal_fremitus = request.POST.get("vocal_fremitus")
                    RespiratorySystem.objects.filter(AppointmentIDFK=appointment).delete()
                    RespiratorySystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        ChestShape=chest_shape,
                        ChestMovement=chest_movement,
                        Auscultation=auscultation,
                        Percussion=percussion,
                        TracheaPosition=trachea_position,
                        VocalFremitus=vocal_fremitus,
                    )

                    palpation = request.POST.get("palpation")
                    percussion = request.POST.get("percussion2")
                    ascites = request.POST.get("ascites")
                    splenomegaly = request.POST.get("splenomegaly")
                    hepatomegaly = request.POST.get("hepatomegaly")
                    tenderness = request.POST.get("tenderness")
                    hernia = request.POST.get("hernia1")
                    skin_changes = request.POST.get("skin_changes")
                    swelling = request.POST.get("swelling2")
                    GastrointestinalSystem.objects.filter(AppointmentIDFK=appointment).delete()
                    GastrointestinalSystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Palpation=palpation,
                        Percussion=percussion,
                        Ascites=ascites,
                        Splenomegaly=splenomegaly,
                        Hepatomegaly=hepatomegaly,
                        Tenderness=tenderness,
                        Hernia=hernia,
                        SkinChanges=skin_changes,
                        Swelling=swelling,
                    )

                    skin_changes = request.POST.get("skin_changes1")
                    phimosis = request.POST.get("phimosis")
                    paraphimosis = request.POST.get("paraphimosis")
                    hypospadias = request.POST.get("hypospadias")
                    undescended_tests = request.POST.get("undescended_tests")
                    hernia = request.POST.get("hernia2")
                    GenitourinarySystem.objects.filter(AppointmentIDFK=appointment).delete()
                    GenitourinarySystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        SkinChanges=skin_changes,
                        Phimosis=phimosis,
                        Paraphimosis=paraphimosis,
                        Hypospadias=hypospadias,
                        UndescendedTests=undescended_tests,
                        Hernia=hernia,
                    )

                    skin_changes = request.POST.get("skin_changes2")
                    joint_swelling = request.POST.get("joint_swelling")
                    tenderness = request.POST.get("tenderness")
                    deformity = request.POST.get("deformity")
                    restricted_mobility = request.POST.get("restricted_mobility")
                    reflexes = request.POST.get("reflexes")
                    MusculoskeletalSystem.objects.filter(AppointmentIDFK=appointment).delete()
                    MusculoskeletalSystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        SkinChanges=skin_changes,
                        JointSwelling=joint_swelling,
                        Tenderness=tenderness,
                        Deformity=deformity,
                        RestrictedMobility=restricted_mobility,
                        Reflexes=reflexes,
                    )

                    speech = request.POST.get("speech")
                    power_limbs = request.POST.get("power_limbs")
                    touch_sensation = request.POST.get("touch_sensation")
                    knee_jerk_reflex = request.POST.get("knee_jerk_reflex")
                    ankle_reflex = request.POST.get("ankle_reflex")
                    cranial_nerves_examination = request.POST.get("cranial_examination")
                    NervousSystem.objects.filter(AppointmentIDFK=appointment).delete()
                    NervousSystem.objects.create(
                        AppointmentIDFK_id=appointment.AppointmentIDPK,
                        Speech=speech,
                        PowerLimbs=power_limbs,
                        TouchSensation=touch_sensation,
                        KneeJerkReflex=knee_jerk_reflex,
                        AnkleReflex=ankle_reflex,
                        CranialNervesExamination=cranial_nerves_examination,
                    )
                
                messages.success(request, 'Medical History saved successfully!')
                return redirect(f"/Clinic/Pre-Examination/{appointment_id}/")
            except Exception as e:
                print("error",e)
                messages.error(request, 'Failed to save Medical History!')
                return redirect(f"/Clinic/Pre-Examination/{appointment_id}/")


    
