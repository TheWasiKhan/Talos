from django.db import models
from Patient.models.appointment import Appointment

class ChiefComplaint(models.Model):
    ChiefComplaintIDPK=models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Problem = models.CharField(max_length=255, null=True)
    Onset = models.CharField(max_length=255, null=True)
    Site = models.CharField(max_length=255, null=True)
    Progression = models.CharField(max_length=255, null=True)
    Duration = models.CharField(max_length=255, null=True)
    Frequency = models.CharField(max_length=255, null=True)
    Color = models.CharField(max_length=255, null=True)
    Grade = models.CharField(max_length=255, null=True)
    RadiatingTo = models.CharField(max_length=255, null=True)
    Relieving_Factor = models.CharField(max_length=255, null=True)
    Aggravating_Factor = models.CharField(max_length=255, null=True)
    Smell = models.CharField(max_length=255, null=True)


class PastMedicalHistory(models.Model):
    PastMedicalHistoryIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    PastDisease = models.CharField(max_length=255, null=True)
    DiseaseDetails = models.CharField(max_length=255, null=True)


class PersonalHistory(models.Model):
    PersonalHistoryIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Smoking = models.CharField(max_length=50, null=True)
    Alcohol = models.CharField(max_length=50, null=True)
    Sleep = models.CharField(max_length=50, null=True)
    Allergy = models.CharField(max_length=255, null=True)
    BowelBladderHabits = models.CharField(max_length=50, null=True)
    Appetite = models.CharField(max_length=50, null=True)


class FamilyHistory(models.Model):
    FamilyHistoryIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Disease = models.CharField(max_length=255, null=True)
    DiseaseDetails = models.CharField(max_length=50, choices=[
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('GrandFather', 'Grand Father'),
        ('GrandMother', 'Grand Mother'),
        ('Husband', 'Husband'),
        ('Wife', 'Wife'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    ], null=True)


class CardiovascularSymptoms(models.Model):
    CardiovascularSymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Breathlessness = models.CharField(max_length=255, null=True)
    Palpitations = models.CharField(max_length=255, null=True)
    ChestPain = models.CharField(max_length=255, null=True)
    Fainting = models.CharField(max_length=255, null=True)
    AnkleEdema = models.CharField(max_length=255, null=True)


class NervousSystemSymptoms(models.Model):
    NervousSystemSymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Headache = models.CharField(max_length=255, null=True)
    Dizziness = models.CharField(max_length=255, null=True)
    Fainting = models.CharField(max_length=255, null=True)
    Tremors = models.CharField(max_length=255, null=True)
    Seizure = models.CharField(max_length=255, null=True)
    Tinnitus = models.CharField(max_length=255, null=True)
    Deafness = models.CharField(max_length=255, null=True)
    VisionLoss = models.CharField(max_length=255, null=True)
    MemoryLoss = models.CharField(max_length=255, null=True)


class MusculoskeletalSymptoms(models.Model):
    MusculoskeletalSymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    JointPain = models.CharField(max_length=255, null=True)
    Immobility = models.CharField(max_length=255, null=True)
    Redness = models.CharField(max_length=255, null=True)
    Swelling = models.CharField(max_length=255, null=True)


class GenitourinarySymptoms(models.Model):
    GenitourinarySymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    MultipleSexualPartners = models.CharField(max_length=255, null=True)
    Libido = models.CharField(max_length=255, null=True)
    BurningMicturition = models.CharField(max_length=255, null=True)
    PainfulMicturition = models.CharField(max_length=255, null=True)
    OveractiveBladder = models.CharField(max_length=255, null=True)
    Incontinence = models.CharField(max_length=255, null=True)
    BloodyUrine = models.CharField(max_length=255, null=True)
    LMP = models.CharField(max_length=255, null=True)
    WhiteDischarge = models.CharField(max_length=255, null=True)
    FoulSmellingSecretions = models.CharField(max_length=255, null=True)
    Itching = models.CharField(max_length=255, null=True)
    PeriodsDuration = models.CharField(max_length=255, null=True)
    Dysmenorrhoea = models.CharField(max_length=255, null=True)
    PainfulCoitus = models.CharField(max_length=255, null=True)


class GastrointestinalSymptoms(models.Model):
    GastrointestinalSymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Heartburn = models.CharField(max_length=255, null=True)
    Acidity = models.CharField(max_length=255, null=True)
    Nausea = models.CharField(max_length=255, null=True)
    Vomiting = models.CharField(max_length=255, null=True)
    PainAbdomen = models.CharField(max_length=255, null=True)
    Indigestion = models.CharField(max_length=255, null=True)
    ChangeInStoolColor = models.CharField(max_length=255, null=True)


class RespiratorySymptoms(models.Model):
    RespiratorySymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Cough = models.CharField(max_length=255, null=True)
    BloodInSputum = models.CharField(max_length=255, null=True)
    Breathlessness = models.CharField(max_length=255, null=True)
    PainfulBreathing = models.CharField(max_length=255, null=True)


class EndocrineSymptoms(models.Model):
    EndocrineSymptomsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    HeatIntolerance = models.CharField(max_length=255, null=True)
    ColdIntolerance = models.CharField(max_length=255, null=True)
    HeavySweating = models.CharField(max_length=255, null=True)
    Polydipsia = models.CharField(max_length=255, null=True)
    Polyuria = models.CharField(max_length=255, null=True)


class GpeDetails(models.Model):
    GpeDetailsIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    MentalState = models.CharField(max_length=255, null=True, blank=True)
    Cyanosis = models.CharField(max_length=255, null=True, blank=True)
    Clubbing = models.CharField(max_length=255, null=True, blank=True)
    Pallor = models.CharField(max_length=255, null=True, blank=True)
    Icterus = models.CharField(max_length=255, null=True, blank=True)
    Lymphadenopathy = models.CharField(max_length=255, null=True, blank=True)
    Edema = models.CharField(max_length=255, null=True, blank=True)
    BodyBuilt = models.CharField(max_length=255, null=True, blank=True)
    Gait = models.CharField(max_length=255, null=True, blank=True)
    Height = models.CharField(max_length=255, null=True, blank=True)
    Weight = models.CharField(max_length=255, null=True, blank=True)


class CardiovascularSystem(models.Model):
    CardiovascularSystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Pulse = models.CharField(max_length=255, null=True)
    HeartSounds = models.CharField(max_length=255, null=True)
    JVP = models.CharField(max_length=255, null=True)
    ChestWallAbnormalities = models.CharField(max_length=255, null=True)
    EngorgedVeins = models.CharField(max_length=255, null=True)
    CardiovascularAuscultation = models.CharField(max_length=255, null=True)


class RespiratorySystem(models.Model):
    RespiratorySystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    ChestShape = models.CharField(max_length=255, null=True)
    ChestMovement = models.CharField(max_length=255, null=True)
    Auscultation = models.CharField(max_length=255, null=True)
    Percussion = models.CharField(max_length=255, null=True)
    TracheaPosition = models.CharField(max_length=255, null=True)
    VocalFremitus = models.CharField(max_length=255, null=True)


class GastrointestinalSystem(models.Model):
    GastrointestinalSystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Palpation = models.CharField(max_length=255, null=True)
    Percussion = models.CharField(max_length=255, null=True)
    Ascites = models.CharField(max_length=255, null=True)
    Splenomegaly = models.CharField(max_length=255, null=True)
    Hepatomegaly = models.CharField(max_length=255, null=True)
    Tenderness = models.CharField(max_length=255, null=True)
    Hernia = models.CharField(max_length=255, null=True)
    SkinChanges = models.CharField(max_length=255, null=True)
    Swelling = models.CharField(max_length=255, null=True)


class GenitourinarySystem(models.Model):
    GenitourinarySystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    SkinChanges = models.CharField(max_length=255, null=True)
    Phimosis = models.CharField(max_length=255, null=True)
    Paraphimosis = models.CharField(max_length=255, null=True)
    Hypospadias = models.CharField(max_length=255, null=True)
    UndescendedTests = models.CharField(max_length=255, null=True)
    Hernia = models.CharField(max_length=255, null=True)


class MusculoskeletalSystem(models.Model):
    MusculoskeletalSystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    SkinChanges = models.CharField(max_length=255, null=True)
    JointSwelling = models.CharField(max_length=255, null=True)
    Tenderness = models.CharField(max_length=255, null=True)
    Deformity = models.CharField(max_length=255, null=True)
    RestrictedMobility = models.CharField(max_length=255, null=True)
    Reflexes = models.CharField(max_length=255, null=True)


class NervousSystem(models.Model):
    NervousSystemIDPK = models.AutoField(primary_key=True)
    AppointmentIDFK = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Speech = models.CharField(max_length=255, null=True)
    PowerLimbs = models.CharField(max_length=255, null=True)
    TouchSensation = models.CharField(max_length=255, null=True)
    KneeJerkReflex = models.CharField(max_length=255, null=True)
    AnkleReflex = models.CharField(max_length=255, null=True)
    CranialNervesExamination = models.CharField(max_length=255, null=True)
