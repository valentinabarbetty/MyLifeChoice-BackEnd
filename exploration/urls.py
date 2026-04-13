from django.urls import path
from .views import has_progress, get_user_progress, save_progress, get_user_feedback


urlpatterns = [
    path('has_progress/<int:user_id>/', has_progress, name='has_progress'),
    path('progress/<int:user_id>/', get_user_progress),
    path('progress/', save_progress),  
    path('feedback/<int:user_id>/', get_user_feedback)
]
