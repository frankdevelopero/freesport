from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout, authenticate, login as django_login, update_session_auth_hash, login
from users.forms import LoginForm


def _redirect_url(user):

    if user.role == 1:
        return 'user-account'
    elif user.role == 2:
        return 'agent_dashboard'
    else:
        return 'dashboard'


class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'users/sign-in.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm(request.POST)
        if not form.is_valid():
            context = {
                'errors': ["Ingresa un correo electrónico y contraseña válida"],
                'form': form
            }
            return render(request, 'users/sign-in.html', context)
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                'errors': ["Correo electrónico o contraseña inválida. Por favor revisa tus accesos."],
                'form': form
            }
            return render(request, 'users/sign-in.html', context)
        if not user.status:
            error_message = ["Tu cuenta está bloqueado. Por favor contacta con nosotros."]
            if user.role == 2:
                error_message = [
                    "Tu cuenta ha sido suspendida, contacta a tu administrador para habilitar tu cuenta de vendedor"]
            context = {
                'errors': error_message,
                'form': form
            }
            return render(request, 'users/sign-in.html', context)
        django_login(request, user)
        next_url = request.GET.get('next', '')

        if next_url:
            return redirect(next_url)
        return redirect(_redirect_url(user))


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(_redirect_url(request.user))

        context = {
        }
        return render(request, 'users/sign-up.html', context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')


class TwoFactorAuthView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        context = {
        }
        return render(request, 'users/two-factor-auth.html', context)


class UserAccountView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {
        }
        return render(request, 'users/user_account.html', context)


class UserAccountChangePasswordView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {
        }
        return render(request, 'users/user_account_change_password.html', context)


class UserAccountBookingView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {
        }
        return render(request, 'users/user_account_bookings.html', context)
