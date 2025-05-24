from django.db import models
import datetime

# Service Details
SERVICE_TYPES = [
    ('generalService', 'General Service'),
    ('majorRepair', 'Major Repair'),
    ('accidentalRepair', 'Accidental Repair'),
    ('breakService', 'Break Service'),
    ('engineCheckup', 'Engine Check-Up'),
    ('other', 'Other'),
]

# Make choices
MAKE_CHOICE = [
    ('honda', 'Honda'),
    ('royalEnfield', 'Royal Enfield'),
    ('tvs', 'TVS'),
    ('marutiSuzuki', 'Maruti Suzuki'),
    ('hyundai', 'Hyundai'),
    ('mahindra', 'Mahindra'),
    ('other', 'Other'),
]

#Group names 
GROUPS = ['A', 'B', 'C', 'D']

#Status choices
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

class ServiceRequest(models.Model):
    # Personal Information
    customerName = models.CharField(max_length=100)
    customerPhone = models.CharField(max_length=15)
    customerEmail = models.EmailField()
    customerAddress = models.TextField(max_length=255, blank=True, null=True)

    # Vehicle Information
    
    vehicleMake = models.CharField(max_length=20, choices=MAKE_CHOICE)
    vehicleModel = models.CharField(max_length=255)
    vehicleYear = models.PositiveIntegerField()
    registrationNumber = models.CharField(max_length=20)

    
    serviceType = models.CharField(max_length=30, choices=SERVICE_TYPES)
    preferredDate = models.DateField()
    preferredTime = models.CharField(max_length=20)

    # Common issues (multi-select stored as comma-separated values)
    issueDescription = models.TextField(blank=True, help_text="Comma-separated list of selected issues")
    bookingDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="Pending", choices=STATUS_CHOICES)

    class Meta:
        ordering = ['bookingDate']

    bookingId = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.bookingId:
            # Assign group based on a simple logic, e.g. last digit of phone modulo groups count
            group_index = int(self.customerPhone[-1]) % len(GROUPS)
            group = GROUPS[group_index]

            # Use registrationNumber cleaned and uppercase
            vehicle_number = self.registrationNumber.upper().replace(" ", "")

            # Format bookingDate (use current datetime if not set)
            date_str = datetime.datetime.now().strftime('%Y%m%d')

            # Compose bookingId
            self.bookingId = f"{group}{vehicle_number}{date_str}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"ServiceRequest({self.customerName}, {self.vehicleModel}, {self.preferredDate})"
