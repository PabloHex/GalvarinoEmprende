from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Usuario, Producto, Calificacion


class RegistroForm(UserCreationForm):
    nombre_emprendimiento = forms.CharField(max_length=100, required=True)
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=15, required=True)
    comuna = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'nombre_emprendimiento', 'nombre', 'apellido', 'email', 'telefono', 'comuna', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Usuario.objects.create(
                user=user,
                nombre_emprendimiento=self.cleaned_data['nombre_emprendimiento'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data['telefono'],
                comuna=self.cleaned_data['comuna']
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'telefono', 'comuna']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class CalificarProductoForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['calificacion']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[(i, f'{i} estrellas') for i in range(1, 6)])
        }
