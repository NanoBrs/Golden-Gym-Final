from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from weasyprint import HTML
from GoldenGymApp.models import Cliente, Encargado, Novedad, Reporte, Plan
from GoldenGymApp.forms import ClienteForm,EncargadoForm,NovedadForm,ReporteForm,PlanForm

def gestion_clientes(request):
    if request.method == 'POST':
        if 'cliente_id' in request.POST:
            cliente = get_object_or_404(Cliente, id=request.POST['cliente_id'])
            form = ClienteForm(request.POST, instance=cliente)
        else:
            form = ClienteForm(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            form.save()
            return redirect('gestion_clientes')  # Redirige después de guardar
        else:
            print(form.errors)  # Imprime los errores del formulario para depuración
    else:
        form = ClienteForm()

    clientes = Cliente.objects.all()
    return render(request, 'GoldenGymApp/gestion_cliente.html', {'form': form, 'clientes': clientes})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('gestion_clientes')  # Redirige a la lista de clientes después de guardar
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'GoldenGymApp/gestion_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return HttpResponseRedirect(reverse('gestion_clientes'))

def gestion_encargados(request):
    if request.method == 'POST':
        if 'encargado_id' in request.POST:
            # Editar encargado existente
            encargado = get_object_or_404(Encargado, id=request.POST['encargado_id'])
            form = EncargadoForm(request.POST, instance=encargado)
        else:
            # Crear nuevo encargado
            form = EncargadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('gestion_encargados')  # Redirige para evitar reenvíos de formulario

    else:
        form = EncargadoForm()  # Formulario vacío para crear un nuevo encargado

    # Obtener la lista de todos los encargados
    encargados = Encargado.objects.all()
    return render(request, 'GoldenGymApp/gestion_encargado.html', {'form': form, 'encargados': encargados})

# Vista para eliminar encargado
def eliminar_encargado(request, encargado_id):
    encargado = get_object_or_404(Encargado, id=encargado_id)
    encargado.delete()
    return HttpResponseRedirect(reverse('gestion_encargados'))

def validar_ingreso(request):
    mensaje = None

    if request.method == "POST":
        rut_ingresado = request.POST.get("rut")

        # Buscar al cliente en la base de datos por su RUT
        try:
            cliente = Cliente.objects.get(rut=rut_ingresado)
            # Verificar si tiene una suscripción activa (esto dependerá de tu lógica de negocio)
            if cliente.suscripcion_activa:  # Asegúrate de que tienes este campo en tu modelo
                mensaje = "Ingreso permitido. Bienvenido al gimnasio."
            else:
                mensaje = "Acceso denegado. No tiene una suscripción activa."
        except Cliente.DoesNotExist:
            mensaje = "RUT no registrado. Verifique su información."

    return render(request, "GoldenGymApp/validar_ingreso.html", {"mensaje": mensaje})

def novedades(request):
    # Obtener todas las novedades y ordenarlas por fecha de publicación
    novedades = Novedad.objects.all().order_by('-fecha_publicacion')

    # Reemplazar los saltos de línea por <br> en cada novedad
    for novedad in novedades:
        novedad.contenido_formateado = novedad.contenido.replace('\n', '<br>')

    return render(request, 'GoldenGymApp/novedades.html', {'novedades': novedades})

# Vista para mostrar los reportes de un cliente
def reportes_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    reportes = cliente.reportes.all()  # Obtener todos los reportes de este cliente

    return render(request, 'GoldenGymApp/reportes_cliente.html', {
        'cliente': cliente,
        'reportes': reportes
    })

# Vista para crear un nuevo reporte para un cliente

def crear_reporte(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.cliente = cliente  # Asociamos el reporte al cliente
            reporte.save()
            # Si la solicitud es AJAX, devolver una respuesta JSON
            if request.is_ajax():
                return JsonResponse({'success': True})
            # Si no es AJAX, redirigir como de costumbre
            return redirect('reportes_cliente', cliente_id=cliente.id)
        else:
            # Si el formulario no es válido, devolver error
            if request.is_ajax():
                return JsonResponse({'success': False})
    
    else:
        form = ReporteForm()

    return render(request, 'GoldenGymApp/crear_reporte.html', {
        'form': form,
        'cliente': cliente
    })

def editar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('reportes_cliente', cliente_id=reporte.cliente.id)
    else:
        form = ReporteForm(instance=reporte)

    return render(request, 'GoldenGymApp/editar_reporte.html', {'form': form, 'reporte': reporte})

def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    cliente_id = reporte.cliente.id  # Guardar el ID del cliente para redirigir después
    print(f"Se está eliminando el reporte del cliente con ID: {cliente_id}")
    reporte.delete()
    return redirect('reportes_cliente', cliente_id=cliente_id)

import matplotlib.pyplot as plt
from weasyprint import HTML
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
import base64

from .models import Cliente, Reporte


def generar_pdf_historial_reportes(request, cliente_id):
    # Obtener el cliente usando su ID (o lanzar un 404 si no se encuentra)
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Obtener los reportes del cliente
    reportes = Reporte.objects.filter(cliente_id=cliente_id).order_by('fecha')

    # Generar un gráfico solo si hay más de dos reportes
    grafico_base64 = None
    if len(reportes) > 2:
        fechas = [reporte.fecha.strftime('%Y-%m-%d') for reporte in reportes]
        pesos = [reporte.peso_actual for reporte in reportes]
        imcs = [reporte.imc_actual for reporte in reportes]
        press_banca = [reporte.press_banca for reporte in reportes]
        sentadillas = [reporte.sentadilla for reporte in reportes]

        # Crear el gráfico con Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(fechas, pesos, marker='o', label='Peso Actual [KG]', color='blue')
        plt.plot(fechas, imcs, marker='o', label='IMC', color='green')
        plt.plot(fechas, press_banca, marker='o', label='Press de Banca [KG]', color='red')
        plt.plot(fechas, sentadillas, marker='o', label='Sentadilla [KG]', color='orange')
        
        plt.title(f"Progreso del Cliente: {cliente.nombre} {cliente.apellido}")
        plt.xlabel("Fecha")
        plt.ylabel("Valores")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()

        # Guardar el gráfico como imagen en memoria (sin abrir ventana de GUI)
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

    # Generar el HTML del historial de reportes usando un template
    html = render_to_string('GoldenGymApp/historial_reportes_pdf.html', {
        'reportes': reportes, 
        'cliente': cliente,
        'grafico_base64': grafico_base64,  # Pasar el gráfico al contexto
    })

    # Generar el PDF desde el HTML
    pdf = HTML(string=html).write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historial_reportes_cliente_{cliente.nombre}_{cliente.apellido}.pdf"'
    
    return response

def gestion_planes(request):
    if request.method == 'POST':
        if 'plan_id' in request.POST:
            # Editar plan existente
            plan = get_object_or_404(Plan, id=request.POST['plan_id'])
            form = PlanForm(request.POST, instance=plan)
        else:
            # Crear nuevo plan
            form = PlanForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('gestion_planes')  

    else:
        form = PlanForm()  # Crear un formulario vacío para crear un nuevo plan

    # Obtener la lista de todos los planes
    planes = Plan.objects.all()
    return render(request, 'GoldenGymApp/gestion_planes.html', {'form': form, 'planes': planes})

def eliminar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    plan.delete()
    return HttpResponseRedirect(reverse('gestion_planes'))

def editar_plan(request, plan_id):
    # Obtener el plan que se está editando
    plan = get_object_or_404(Plan, id=plan_id)

    # Si el formulario es enviado
    if request.method == 'POST':
        # Vinculamos el formulario con los datos de la instancia del plan
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            # Guardamos los cambios
            form.save()
            return redirect('gestion_planes')  # Redirigir a la lista de planes o a otra página
    else:
        # Si es un GET, pasamos los datos del plan al formulario
        form = PlanForm(instance=plan)

    # Pasamos el formulario a la plantilla
    return render(request, 'GoldenGymApp/gestion_planes.html', {'form': form, 'plan': plan})

def registro_usuario(request):
    
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir o hacer algo después de guardar
    return render(request, 'GoldenGymApp/registro.html', {'form': form})