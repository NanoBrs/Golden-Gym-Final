from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Encargado(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.username} ({self.rut})"


class Plan(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    duracion_dias = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    suscripcion_activa = models.BooleanField(default=False)
    encargado = models.ForeignKey(Encargado, on_delete=models.SET_NULL, null=True, related_name='clientes')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Inscripcion(models.Model):
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="inscripciones")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="inscripciones")
    encargado = models.ForeignKey(Encargado, on_delete=models.SET_NULL, null=True, related_name="inscripciones_registradas")
    monto_pagado = models.IntegerField()
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.monto_pagado < self.plan.precio:
            raise ValidationError("El monto pagado no puede ser menor al precio del plan.")

        # Validar que el cliente no tenga más de una suscripción activa
        if Inscripcion.objects.filter(cliente=self.cliente, cliente__suscripcion_activa=True).exclude(pk=self.pk).exists():
            raise ValidationError(f"El cliente {self.cliente.nombre} {self.cliente.apellido} ya tiene una suscripción activa.")

        # Activar la suscripción actual
        self.cliente.plan_actual = self.plan
        self.cliente.suscripcion_activa = True
        self.cliente.save()
        super().save(*args, **kwargs)


    def cancelar_suscripcion(self):
        # Cancelar la suscripción activa
        self.cliente.plan_actual = None
        self.cliente.suscripcion_activa = False
        self.cliente.save()

    def __str__(self):
        return f"{self.cliente} - {self.plan.nombre} ({self.metodo_pago} - {self.fecha_transaccion.strftime('%Y-%m-%d')})"


class Novedad(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)
    ruta_video = models.CharField(max_length=300, blank=True, null=True)
    autor = models.ForeignKey(Encargado, on_delete=models.CASCADE, related_name='novedades')

    def __str__(self):
        return self.titulo


class Reporte(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='reportes', on_delete=models.CASCADE)
    fecha = models.DateField(editable=True)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    imc_actual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    press_banca = models.DecimalField(max_digits=5, decimal_places=2)
    sentadilla = models.DecimalField(max_digits=5, decimal_places=2)
    peso_muerto = models.DecimalField(max_digits=5, decimal_places=2)

    def calcular_imc(self):
        if self.altura > 0:
            return round(self.peso_actual / (self.altura ** 2), 2)
        return None

    def save(self, *args, **kwargs):
        self.imc_actual = self.calcular_imc()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reporte de {self.cliente.nombre} {self.cliente.apellido} - {self.fecha.strftime('%d-%m-%Y')}"
