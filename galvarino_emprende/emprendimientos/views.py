from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, ProductoForm, EditarPerfilForm, CalificarProductoForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Usuario
from django.contrib import messages
from django.shortcuts import render, redirect

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuario registrado exitosamente")
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('home')
        else:
            messages.error(request, "Error al registrar usuario")
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def home_view(request):
    productos = Producto.objects.all().order_by('-id')
    return render(request, 'home.html', {'productos': productos})


@login_required
def perfil(request):
    # Intentamos obtener el perfil del usuario autenticado extendido (modelo Usuario)
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        # Si no existe el perfil, lo creamos con datos por defecto
        usuario = Usuario.objects.create(
            user=request.user,
            nombre=request.user.first_name,
            apellido=request.user.last_name,
            email=request.user.email,
            telefono='',
            comuna='',
            nombre_emprendimiento=''
        )

    nombre = usuario.user.first_name or usuario.nombre
    apellido = usuario.user.last_name or usuario.apellido

    productos = Producto.objects.filter(usuario=usuario)

    return render(request, 'perfil.html', {
        'usuario': usuario,
        'productos': productos,
        'nombre': nombre,
        'apellido': apellido
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def editar_perfil(request):
    # Obtener el usuario personalizado relacionado con el usuario autenticado
    usuario_actual = Usuario.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Actualizar los datos del usuario
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        
        # Actualizar los datos del usuario personalizado
        usuario_actual.telefono = request.POST['telefono']
        usuario_actual.comuna = request.POST['comuna']
        usuario_actual.nombre_emprendimiento = request.POST['nombre_emprendimiento']
        usuario_actual.save()

        return redirect('perfil')

    return render(request, 'editar_perfil.html', {
        'user': request.user,
        'usuario': usuario_actual
    })


@login_required
def agregar_producto(request):
    usuario = Usuario.objects.get(user=request.user)  # Obtén la instancia del modelo Usuario
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            nuevo_producto.usuario = usuario  # Asigna el usuario correcto
            nuevo_producto.save()
            messages.success(request, 'Producto agregado con éxito.')
            return redirect('perfil')
    else:
        form = ProductoForm()
    
    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    # Obtener el usuario personalizado relacionado con el usuario actual
    usuario_actual = Usuario.objects.get(user=request.user)

    # Obtener el producto relacionado con este usuario
    producto = get_object_or_404(Producto, id=producto_id, usuario=usuario_actual)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('perfil')

    return render(request, 'editar_producto.html', {'producto': producto})

@login_required
def confirmar_eliminacion(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect('perfil')
    return render(request, 'confirmar_eliminacion.html', {'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('perfil')

def calificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    usuario = get_object_or_404(Usuario, user=request.user)  # Asegúrate de obtener el usuario correcto
    
    if request.method == 'POST':
        form = CalificarProductoForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.producto = producto
            calificacion.usuario = usuario  # Usar el usuario correcto
            calificacion.save()
            messages.success(request, "Gracias por tu calificación.")
            return redirect('home')
    else:
        form = CalificarProductoForm()
    
    return render(request, 'calificar_producto.html', {'form': form, 'producto': producto})