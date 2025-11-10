from rest_framework import routers
from django.urls import path
from .views import UserViewSet, LoginView, AssignPlayerTypeView, AssignGuideByEmailView, GoogleLoginView, UpdateNicknameView


router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('google_login/', GoogleLoginView.as_view(), name='google_login'), 
    path('assign_player_type/', AssignPlayerTypeView.as_view(), name='assign_player_type'),
    path('assign_guide_by_email/', AssignGuideByEmailView.as_view(), name='assign-guide-by-email'),
    path('update_nickname/', UpdateNicknameView.as_view(), name='update_nickname'),  # ✅ nuevo endpoint

]

urlpatterns += router.urls
