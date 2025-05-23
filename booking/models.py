from django.db import models

class ServiceRequest(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)

    # Vehicle Information
    TATA_MODELS = [
        ('nexon', 'Nexon'),
        ('harrier', 'Harrier'),
        ('punch', 'Punch'),
        ('altroz', 'Altroz'),
        ('tiago', 'Tiago'),
        ('tigorev', 'Tigor EV'),
        ('safari', 'Safari'),
        ('sumo', 'Sumo'),
    ]
    tata_model = models.CharField(max_length=20, choices=TATA_MODELS)
    reg_year = models.PositiveIntegerField()
    reg_number = models.CharField(max_length=20)
    odometer_reading = models.PositiveIntegerField()

    # Service Details
    SERVICE_TYPES = [
        ('regularMaintenance', 'Regular Maintenance'),
        ('repairService', 'Repair Service'),
        ('warrantyService', 'Warranty Service'),
        ('amcService', 'AMC Service'),
    ]
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)

    # Common issues (multi-select stored as comma-separated values)
    common_issues = models.TextField(blank=True, help_text="Comma-separated list of selected issues")

    additional_details = models.TextField(blank=True, null=True)

    # Appointment Details
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=20)

    # Additional Preferences (stored as comma-separated values)
    service_pref = models.TextField(blank=True, help_text="Comma-separated list of preferences")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"ServiceRequest({self.full_name}, {self.tata_model}, {self.preferred_date})"
