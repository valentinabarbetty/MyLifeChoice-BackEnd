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


from .models import Progress

@api_view(['GET'])
def get_user_progress(request, user_id):
    """Retorna las carreras completadas por el usuario"""

    progresses = Progress.objects.filter(user_id=user_id, state='done')

    visited = [p.career.career_id for p in progresses]

    return Response({
        "visited": visited
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Progress
from .serializers import ProgressSerializer


@api_view(['POST'])
def save_progress(request):
    """Guarda progreso de una carrera"""

    user_id = request.data.get("user_id")
    career_id = request.data.get("career_id")
    state = request.data.get("state", "done")
    feedback = request.data.get("feedback")
    progress = request.data.get("progress")

    existing = Progress.objects.filter(
        user_id=user_id,
        career_id=career_id
    ).first()

    if existing:
        return Response(
            {"message": "Ya existe progreso para esta carrera"},
            status=status.HTTP_200_OK
        )

    serializer = ProgressSerializer(data={
        "user": user_id,
        "career": career_id,
        "state": state,
        "feedback": feedback,
        "progress": progress
    })

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)