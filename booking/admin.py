from django.contrib import admin
from .models import ServiceRequest
# Register your models here.

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bookingId',
        'customerName',
        'customerPhone',
        'vehicleMake',
        'vehicleModel',
        'serviceType',
        'preferredDate',
        'status',
    )
    search_fields = ('bookingId', 'customerName', 'customerPhone', 'registrationNumber')
    list_filter = ('status', 'vehicleMake', 'serviceType', 'preferredDate')
    ordering = ('-bookingDate',)
