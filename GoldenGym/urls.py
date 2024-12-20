
from django.contrib import admin
from django.urls import path
from GoldenGymApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.gestion_clientes, name='gestion_cliente'),
    #----------------------------- VIEWS AUTENTICACIÓN  ---------------------------------

    path('login/', auth_views.LoginView.as_view(template_name='GoldenGymApp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #----------------   VIEWS ENCARGADO --------------------------------------------------------------------------------------------------------
    path('gestion_encargados/', views.gestion_encargados, name='gestion_encargados'),
    path('eliminar_encargado/<int:encargado_id>/', views.eliminar_encargado, name='eliminar_encargado'),
    path('editar_encargado/<int:pk>/', views.editar_encargado, name='editar_encargado'),
    path('registro_encargado/', views.registrar_encargado, name='registro_encargado'),
    #----------------   VIEWS CLIENTE --------------------------------------------------------------------------------------------------------
    
    path('gestion_clientes/',views.gestion_clientes,name='gestion_clientes'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('editar_cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('registro/', views.registrar_cliente, name='registro'),

    #----------------------------- VIEWS INGRESOS Y NOVEDADES
    path('validar_ingreso/', views.validar_ingreso, name='validar_ingreso'),

    path('novedades/', views.novedades, name='novedades'),

    #---------------------------------------- VIEWS REPORTES ---------------------------------
    path('reportes_cliente/<int:cliente_id>/', views.reportes_cliente, name='reportes_cliente'),
    path('crear_reporte/<int:cliente_id>/', views.crear_reporte, name='crear_reporte'),
    path('editar_reporte/<int:reporte_id>/', views.editar_reporte, name='editar_reporte'),
    path('eliminar_reporte/<int:reporte_id>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('generar_pdf_reportes/<int:cliente_id>/', views.generar_pdf_historial_reportes, name='generar_pdf_reportes'),

    #---------------------------------------- VIEWS PLANES ---------------------------------
    path('gestion_planes/', views.gestion_planes, name='gestion_planes'),
    path('eliminar_plan/<int:plan_id>/', views.eliminar_plan, name='eliminar_plan'),
    path('editar_plan/<int:plan_id>/', views.editar_plan, name='editar_plan'),


    #---------------------------------------- VIEWS INSCRIPCIONES ---------------------------------
    path('gestion_inscripciones/', views.gestion_inscripciones, name='gestion_inscripciones'),
    path('editar_inscripcion/<int:id>/', views.editar_inscripcion, name='editar_inscripcion'),
    path('eliminar_inscripcion/<int:id>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
