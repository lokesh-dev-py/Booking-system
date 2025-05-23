from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = [
            'id',
            'full_name',
            'phone_number',
            'email_address',
            'address',
            'tata_model',
            'reg_year',
            'reg_number',
            'odometer_reading',
            'service_type',
            'common_issues',
            'additional_details',
            'preferred_date',
            'preferred_time_slot',
            'service_pref',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def to_internal_value(self, data):
        # Convert lists to comma-separated strings if needed
        if isinstance(data.get('common_issues'), list):
            data['common_issues'] = ','.join(data['common_issues'])
        if isinstance(data.get('service_pref'), list):
            data['service_pref'] = ','.join(data['service_pref'])

        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Convert stored comma-separated string back to list
        rep['common_issues'] = instance.common_issues.split(',') if instance.common_issues else []
        rep['service_pref'] = instance.service_pref.split(',') if instance.service_pref else []
        return rep
