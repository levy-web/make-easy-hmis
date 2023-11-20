from django.utils import timezone
from rest_framework import serializers
from .models import (
    InsuranceCompany,
    ContactDetails,
    Patient,
    NextOfKin,
    Appointment,
    Prescription,
    PrescribedDrug,
    PublicAppointment,
    Service,
    Consultation,
    Referral,
    Triage,
)


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ("id", "first_name", "second_name", "date_of_birth",
                  "gender", "insurance", "user_id", "age")

    def get_age(self, obj: Patient):
        if obj.age:
            return obj.age
        return None

    def to_representation(self, instance: Patient):
        data = super().to_representation(instance)
        data["gender"] = instance.get_gender_display()
        if instance.insurance:
            data["insurance"] = instance.insurance.name
        return data


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'


# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = '__all__'

#     def to_representation(self, instance: Appointment):
#         data = super().to_representation(instance)
#         if instance.assigned_doctor:
#             data["assigned_doctor"] = instance.assigned_doctor.get_fullname()

#         if instance.patient:
#             data["first_name"] = instance.patient.first_name
#             data["second_name"] = instance.patient.second_name
#         return data


class PublicAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicAppointment
        fields = [
            "id",
            'service',
            'first_name',
            'second_name',
            'date_of_birth',
            'gender',
            'appointment_date_time',
            'status',
            'reason',
            'date_created',
        ]
        read_only_fields = ("id", "date_created",)

    def to_representation(self, instance: PublicAppointment):
        data = super().to_representation(instance)
        data["gender"] = instance.get_gender_display()
        data["status"] = instance.get_status_display()
        if instance.service:
            data["service"] = instance.service.name
        return data

    def get_service_name(self, obj: PublicAppointment):
        return obj.service.name


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class PrescribedDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribedDrug
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


# get appointments for a specific doctor
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = [
            'patient',
            'assigned_doctor',
            'appointment_date_time',
            'status',
            'reason',
            'date_created',
            'date_changed',
            'id',
        ]
        read_only_fields = ("id",)

    def create(self, validated_data: dict):
        patient = validated_data.pop("patient", None)
        try:
            if patient:
                patient = Patient.objects.create(**patient)
        except Exception as e:
            print(e)
            raise serializers.ValidationError(f"Error occurred {e}")

        try:
            appointment = Appointment.objects.create(
                patient=patient, **validated_data)
            return appointment
        except Exception as e:
            print(e)
            raise serializers.ValidationError(f"Error occurred {e}")

    def update(self, instance: Appointment, validated_data: dict):
        print("update appointment")
        patient_dict = validated_data.get('patient')
        print(patient_dict)
        # try:
        #     patient = Patient.objects.get(id=patient_dict.get('id'),)
        # except Exception as e:
        #     print(e)
        #     raise serializers.ValidationError(f"Error occurred {e}")
        
        instance.patient = validated_data.get('patient', instance.patient)
        instance.assigned_doctor = validated_data.get('assigned_doctor', instance.assigned_doctor)
        instance.appointment_date_time = validated_data.get('appointment_date_time', instance.appointment_date_time)
        instance.status = validated_data.get('status', instance.status)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.date_changed = timezone.now()
        return instance
    
    def to_representation(self, instance: Appointment):
        data = super().to_representation(instance)
        if instance.assigned_doctor:
            data["assigned_doctor"] = instance.assigned_doctor.get_fullname()

        if instance.patient:
            data["first_name"] = instance.patient.first_name
            data["second_name"] = instance.patient.second_name
        return data



class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = '__all__'

