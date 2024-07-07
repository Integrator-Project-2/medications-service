from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationReminderViewSet, AmountReminderViewSet

router = DefaultRouter()
router.register(r'medication-reminder', MedicationReminderViewSet)
router.register(r'amount-reminder', AmountReminderViewSet)

urlpatterns = [

]

urlpatterns += router.urls
