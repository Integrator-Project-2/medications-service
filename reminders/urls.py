from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationReminderViewSet

router = DefaultRouter()
router.register(r'medication-reminder', MedicationReminderViewSet)

urlpatterns = [

]

urlpatterns += router.urls
