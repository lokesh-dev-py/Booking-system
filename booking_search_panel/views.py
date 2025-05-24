from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from booking.models import ServiceRequest
from booking.serializers import ServiceRequestSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class BookingSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['bookingDate', 'status']
    search_fields = ['bookingId', 'registrationNumber', 'customerName']

class BookingStatusUpdateAPIView(APIView):
    def patch(self, request, booking_id):
        booking = get_object_or_404(ServiceRequest, bookingId=booking_id)
        serializer = ServiceRequestSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def search_panel(request):
    return render(request, 'booking_search_panel/service-bookings.html')
