from django.urls import path
from .views import home_view, perfil, registro_view, login_view, logout_view, agregar_producto, editar_producto, editar_perfil, calificar_producto, confirmar_eliminacion, eliminar_producto

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('registro/', registro_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil, name='perfil'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('confirmar_eliminacion/<int:producto_id>/', confirmar_eliminacion, name='confirmar_eliminacion'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('calificar_producto/<int:producto_id>/', calificar_producto, name='calificar_producto'),
]
