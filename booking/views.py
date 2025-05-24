from django.shortcuts import render
from rest_framework import viewsets
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from booking.models import ServiceRequest
from booking.serializers import ServiceRequestSerializer
from rest_framework import generics
# Create your views here.

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by('-bookingDate')
    serializer_class = ServiceRequestSerializer

def service_request_form_view(request):
    return render(request, 'booking/form.html')

def confirmation_page(request):
    return render(request, 'booking/confirmation.html')