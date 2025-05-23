from django.urls import path, include
from .views import ServiceRequestViewSet, service_request_form_view, confirmation_page
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'service-requests', ServiceRequestViewSet, basename='service-request')

urlpatterns = [
    path('', service_request_form_view, name='home'),
    path('confirmation/', confirmation_page, name='confirmation'),
    path('api/', include(router.urls))
]


