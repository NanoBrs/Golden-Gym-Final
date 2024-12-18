"""GoldenGym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GoldenGymApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.gestion_clientes,name='gestion_clientes'),
    path('encargado/',views.gestion_encargados,name='gestion_encargado'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('validar_ingreso/', views.validar_ingreso, name='validar_ingreso'),
    path('novedades/', views.novedades, name='novedades'),
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
