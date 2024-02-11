from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from rest_framework.views import APIView

from users.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({"status": True, "message": "Usuario creado con éxito."},
                                status=status.HTTP_201_CREATED, headers=headers)
            except IntegrityError as e:
                if 'email' in str(e):
                    return Response({"status": False, "message": "Correo electrónico ya existe."},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif 'phone_number' in str(e):
                    return Response({"status": False, "message": "Número de teléfono ya existe."},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = serializer.errors
            if 'email' in errors:
                return Response({"status": False, "message": "Correo electrónico ya existe."},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'phone_number' in errors:
                return Response({"status": False, "message": "Número de teléfono ya existe."},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'photo' in errors:
                return Response({"status": False,
                                 "message": "Sube una imagen válida. El archivo subido no era una imagen o estaba corrupto."},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'password' in errors:
                return Response({"status": False, "message": "Ingresa una contraseña e intenta de nuevo."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()


class UserNewApiView(APIView):
    def post(self, request):
        print(request.data)
        data = request.data

        if (data.get("email") and data.get("first_name") and data.get("last_name")
                and data.get("password") and data.get("role")):

            if User.objects.filter(email=data.get("email")).first():
                error_message = "Correo electrónico ingresado ya esta registrado. Intente de nuevo o inicia sesión."
                return Response(data={"success": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)

            user = User()
            user.email = data.get("email")
            user.username = data.get("email")
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.role = data.get("role")
            user.set_password(data.get("password"))
            user.save()
            return Response(
                data={
                    "status": True,
                    "message": "Usuario registrado con éxito",
                    "email": user.email
                },
                status=status.HTTP_200_OK
            )

        else:
            error_message = "Complete todos los campos correctamente"
            return Response(data={"status": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)
