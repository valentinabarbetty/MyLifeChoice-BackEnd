from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from exploration.models import Progress

@api_view(['GET'])
def has_progress(request, user_id):
    """Verifica si el usuario tiene progresos guardados"""
    has_data = Progress.objects.filter(user_id=user_id).exists()
    return Response({'has_progress': has_data})
