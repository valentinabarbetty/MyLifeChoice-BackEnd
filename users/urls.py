from rest_framework import routers
from django.urls import path
from .views import UserViewSet, LoginView, AssignPlayerTypeView, AssignGuideByEmailView, GoogleLoginView, UpdateNicknameView, CheckIntroStatusView, CompleteIntroView


router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('google_login/', GoogleLoginView.as_view(), name='google_login'), 
    path('assign_player_type/', AssignPlayerTypeView.as_view(), name='assign_player_type'),
    path('assign_guide_by_email/', AssignGuideByEmailView.as_view(), name='assign-guide-by-email'),
    path('update_nickname/', UpdateNicknameView.as_view(), name='update_nickname'),  
    path('check-intro/<int:user_id>/', CheckIntroStatusView.as_view()),
    path('complete-intro/<int:user_id>/', CompleteIntroView.as_view()),

]

urlpatterns += router.urls
