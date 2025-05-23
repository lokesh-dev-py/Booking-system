from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['bookingDate']

    def to_internal_value(self, data):
        # Convert list to comma-separated string for 'issueDescription' field
        if isinstance(data.get('issueDescription'), list):
            data['issueDescription'] = ','.join(data['issueDescription'])
        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Convert comma-separated string back to list for 'issueDescription' field
        rep['issueDescription'] = instance.issueDescription.split(',') if instance.issueDescription else []
        return rep
