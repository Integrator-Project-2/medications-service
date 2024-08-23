from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()
router.register(r'medication-reminder', views.MedicationReminderViewSet)
router.register(r'amount-reminder', views.AmountReminderViewSet)


urlpatterns = [
    path('take_medication/<int:pk>/', views.TakeMedicationViewSet.as_view({'put': 'update'}), name='take_medication'),
]

urlpatterns += router.urls
