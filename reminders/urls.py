from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()
router.register(r'medication-reminder', views.MedicationReminderViewSet)
router.register(r'amount-reminder', views.AmountReminderViewSet)
router.register(r'medication-reminder-record', views.MedicationReminderRecordViewSet)



urlpatterns = [

]

urlpatterns += router.urls
