from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="Correo electrónico", widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingresa tu correo',
            'type': 'email'
        }
    ))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg fakepassword',
            'placeholder': 'Ingresa tu contraseña',
            'type': 'password',
            'required': 'true',
            'id': 'psw-input',
        }
    ))
