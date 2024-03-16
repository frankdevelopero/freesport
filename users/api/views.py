from django.contrib.auth import authenticate, login
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from booking.models import Booking
from users.models import User


class RegisterView(APIView):
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

            user = authenticate(email=data.get("email"), password=data.get("password"))
            login(request, user)

            return Response(
                data={
                    "status": True,
                    "message": "Usuario registrado y logueado con éxito",
                    "email": user.email
                },
                status=status.HTTP_200_OK
            )

        else:
            error_message = "Complete todos los campos correctamente"
            return Response(data={"status": False, "message": error_message}, status=status.HTTP_400_BAD_REQUEST)

def get_token(request):
    if request.user.is_authenticated:
        user = request.user
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        })
    else:
        raise Http404("La página no existe")