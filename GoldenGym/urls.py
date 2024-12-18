
from django.contrib import admin
from django.urls import path
from GoldenGymApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.gestion_clientes,name='gestion_clientes'),
    path('eliminar_encargado/<int:id>/', views.eliminar_encargado, name='eliminar_encargado'),
    
    path('gestion_encargado/',views.gestion_encargados,name='gestion_encargado'),


    
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('validar_ingreso/', views.validar_ingreso, name='validar_ingreso'),
    path('novedades/', views.novedades, name='novedades'),


    path('login/', auth_views.LoginView.as_view(template_name='GoldenGymApp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Ruta para ver los reportes de un cliente
    path('reportes_cliente/<int:cliente_id>/', views.reportes_cliente, name='reportes_cliente'),
    
    path('crear_reporte/<int:cliente_id>/', views.crear_reporte, name='crear_reporte'),
    path('editar_reporte/<int:reporte_id>/', views.editar_reporte, name='editar_reporte'),
    path('eliminar_reporte/<int:reporte_id>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('generar_pdf_reportes/<int:cliente_id>/', views.generar_pdf_historial_reportes, name='generar_pdf_reportes'),

    #Planes
    path('gestion_planes/', views.gestion_planes, name='gestion_planes'),
    path('eliminar_plan/<int:plan_id>/', views.eliminar_plan, name='eliminar_plan'),
    path('editar_plan/<int:plan_id>/', views.editar_plan, name='editar_plan'),

    #registro
    path('registro/', views.registro_usuario, name='registro'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
