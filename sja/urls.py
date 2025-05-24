from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('booking.urls')),
    path('', include('booking_search_panel.urls')),
]
