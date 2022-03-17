from django.conf.urls.static import static
from django.urls import path

from measurement.views import SensorListCreateView, SensorRetrieveUpdateView, \
    MeasurementCreateView
from smart_home import settings

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdateView.as_view()),
    path('measurements/', MeasurementCreateView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
