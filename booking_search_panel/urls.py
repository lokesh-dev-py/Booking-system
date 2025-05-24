from django.urls import path, include
from .views import BookingSearchViewSet, search_panel, BookingStatusUpdateAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookings', BookingSearchViewSet, basename='bookings')

urlpatterns = [
    path('search/', search_panel, name='service-search'),
    path('api/', include(router.urls)),
    path('api/bookings/<str:booking_id>/status/', BookingStatusUpdateAPIView.as_view(), name='booking-status-update'),

]