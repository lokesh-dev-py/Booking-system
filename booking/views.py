from django.shortcuts import render
from rest_framework import viewsets
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
# Create your views here.

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by('-created_at')
    serializer_class = ServiceRequestSerializer

def service_request_form_view(request):
    return render(request, 'booking/home.html')

def confirmation_page(request):
    return render(request, 'booking/confirmation.html')