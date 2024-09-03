from rest_framework import viewsets, permissions
from .models import Medication
from .serializers import MedicationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', None)
        if name is not None:
            medications = self.queryset.filter(name__icontains=name)
        else:
            medications = self.queryset.all()
        serializer = self.get_serializer(medications, many=True)
        return Response(serializer.data)
