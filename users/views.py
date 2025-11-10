from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import User, PlayerType, Guide
from .serializers import UserSerializer
from .auth_serializers import LoginSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from firebase_admin import auth as firebase_auth
# --- Registro de usuarios ---
# --- Registro y gestión de usuarios ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# --- Inicio de sesión ---
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            if check_password(password, user.password):
                return Response({
                    "message": "Inicio de sesión exitoso",
                    "user_id": user.user_id,
                    "nickname": user.nickname,
                    "email": user.email
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AssignPlayerTypeView(APIView):
    def put(self, request):
        try:
            email = request.data.get("email")
            player_type_id = request.data.get("player_type_id")

            if not email:
                return Response({"error": "email es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            if not player_type_id:
                return Response({"error": "player_type_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            player_type = PlayerType.objects.get(pk=player_type_id)

            user.player_type = player_type
            user.save()

            return Response({
                "message": f"Tipo de jugador asignado correctamente a {user.nickname}",
                "player_type": player_type.player_type
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except PlayerType.DoesNotExist:
            return Response({"error": "Tipo de jugador no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class AssignGuideByEmailView(APIView):
    def put(self, request):
        try:
            email = request.data.get("email")
            guide_id = request.data.get("guide_id")

            if not email:
                return Response({"error": "email es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            if not guide_id:
                return Response({"error": "guide_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            guide = Guide.objects.get(pk=guide_id)

            user.guide = guide
            user.save()

            return Response({
                "message": f"Guía asignada correctamente a {user.nickname}",
                "guide": guide.guide
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Guide.DoesNotExist:
            return Response({"error": "Guía no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error asignando guía:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded = firebase_auth.verify_id_token(token)
            email = decoded.get("email")
            name = decoded.get("name", email.split("@")[0])
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"nickname": name, "password": ""}
            )

            serializer = UserSerializer(user)
            return Response({
                "user": serializer.data,
                "created": created,
                "message": "Login con Google exitoso"
            })
        except Exception as e:
            print("Error al verificar token:", e)
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)




class UpdateNicknameView(APIView):
    def put(self, request):
        email = request.data.get("email")
        nickname = request.data.get("nickname")

        # Validaciones básicas
        if not email or not nickname:
            return Response(
                {"error": "email y nickname son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            user.nickname = nickname
            user.save()

            return Response(
                {
                    "message": "✅ Nickname actualizado correctamente",
                    "nickname": user.nickname
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )