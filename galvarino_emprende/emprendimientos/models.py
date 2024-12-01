from django.db import models
from django.contrib.auth.models import User

# Modelo para el perfil del usuario
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_emprendimiento = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo para los productos que suben los usuarios
class Producto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relaciona con el modelo Usuario
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def calificacion_promedio(self):
        total_calificaciones = self.calificaciones.count()
        if total_calificaciones > 0:
            suma_calificaciones = sum(cal.calificacion for cal in self.calificaciones.all())
            return round(suma_calificaciones / total_calificaciones, 1)
        return 0

# Modelo para las calificaciones de los productos
class Calificacion(models.Model):
    producto = models.ForeignKey(Producto, related_name='calificaciones', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Cambiado a Usuario
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Valor entre 1 y 5
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Calificación de {self.usuario.user.username} para {self.producto.nombre}: {self.calificacion}'