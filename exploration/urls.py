from django.urls import path
from .views import has_progress

urlpatterns = [
    path('has_progress/<int:user_id>/', has_progress, name='has_progress'),
]
