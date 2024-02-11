from django.urls import path

from users.views import *

urlpatterns = [
    path('inicia-sesion', SignInView.as_view(), name="login"),
    path('cerrar-sesion', LogoutView.as_view(), name="logout"),
    path('registrate', SignUpView.as_view(), name="signup"),
    path('verifica-tu-cuenta', TwoFactorAuthView.as_view(), name="two-factor-auth"),
    path('user/mi-cuenta', UserAccountView.as_view(), name="user-account"),
    path('user/mis-reservas', UserAccountBookingView.as_view(), name="user-account-booking"),
    path('user/cambiar-contrasena', UserAccountChangePasswordView.as_view(), name="user-account-change-password"),
]
