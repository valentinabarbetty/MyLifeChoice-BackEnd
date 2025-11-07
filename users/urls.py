from rest_framework import routers
from django.urls import path
from .views import UserViewSet, LoginView

# Rutas automáticas del CRUD de usuarios
router = routers.DefaultRouter()
router.register(r'', UserViewSet)

# Rutas personalizadas
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Endpoint para iniciar sesión
]

# Agregamos también las rutas del router
urlpatterns += router.urls
