from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import MedicationSerializer
from medications.models import Medication

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def create(self, request, *args ,**kwargs):
        medication_name = request.data.get('name')  # Use request.data para obter o corpo da solicitação POST
        if not medication_name:
            return Response({"error": "O campo 'name' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        api_url = f'https://bula.vercel.app/pesquisar?nome={medication_name}'
        response = requests.get(api_url)

        if response.status_code == 200:
            medications_data = response.json()
            
            if medications_data.get('content'):
                first_medication = medications_data['content'][0]
               
                medication_name_from_api = first_medication.get('nomeProduto')
                print(f"MEDICAMENTO API: {medication_name_from_api}")
                
                request.data['name'] = medication_name_from_api
                
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"error": "Nenhum medicamento encontrado com esse nome."}, status=status.HTTP_404_NOT_FOUND)
        else:
            print(f"Falha ao acessar a API externa. Código de status: {response.status_code}")
            return Response({"error": "Não foi possível acessar a API externa."}, status=response.status_code)
