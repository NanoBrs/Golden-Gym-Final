
from django.db import models

class Cliente(models.Model):
    PLANES_MEMBRESIA = [
        ('SEMANAL', 'Semanal - $15,000'),
        ('MENSUAL', 'Mensual - $28,000'),
        ('TRIMESTRAL', 'Trimestral - $75,000'),
        ('SEMESTRAL', 'Semestral - $135,000'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    membresia = models.CharField(max_length=10, choices=PLANES_MEMBRESIA)
    suscripcion_activa = models.BooleanField(default=True)  # Suscripción activa

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.membresia}"

class Encargado(models.Model):
    # Nombre del encargado
    nombre = models.CharField(max_length=100)

    # Apellido del encargado
    apellido = models.CharField(max_length=100)

    # RUT (Rol Único Tributario) del encargado
    rut = models.CharField(max_length=12, unique=True)

    # Correo electrónico del encargado
    correo = models.EmailField(max_length=100, unique=True)

    # Nombre de usuario para login
    usuario = models.CharField(max_length=50, unique=True)

    # Contraseña para login (se recomienda usar el sistema de autenticación de Django)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.usuario})"
    
class Novedad(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)  # Usar ImageField
    ruta_video = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.titulo

class Reporte(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='reportes', on_delete=models.CASCADE)
    fecha = models.DateField()
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    imc_actual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    press_banca = models.DecimalField(max_digits=5, decimal_places=2)
    sentadilla = models.DecimalField(max_digits=5, decimal_places=2)
    peso_muerto = models.DecimalField(max_digits=5, decimal_places=2)

    def calcular_imc(self):
        # Calcula el IMC en base al peso y la altura.
        if self.altura > 0:
            return round(self.peso_actual / (self.altura ** 2), 2)
        return None

    def save(self, *args, **kwargs):
        # Calcula el IMC antes de guardar el reporte
        self.imc_actual = self.calcular_imc()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reporte de {self.cliente.nombre} {self.cliente.apellido} - {self.fecha.strftime('%b %Y')}"

class Plan(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    duracion_dias = models.IntegerField()

    def __str__(self):
        return self.nombre