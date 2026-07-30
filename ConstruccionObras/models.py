from django.db import models
import os
# Create your models here.


class Obra(models.Model):
    id_obra=models.AutoField(primary_key=True)
    nombre_obra=models.CharField(max_length=50, unique=True)
    descripcion=models.TextField()
    fecha_inicio=models.DateField()
    fecha_fin_estimado=models.DateField()
    presupuesto_total=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    plano = models.FileField(upload_to='planos/', null=True, blank=True)
    ESTADO_CHOICES = [
    ('Planificada', 'Planificada'),
    ('En ejecucion', 'En Ejecucion'),
    ('Finalizada', 'Finalizada'),
    ('Suspendida', 'Suspendida')
    ]
    estado=models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Planificada')

    def __str__(self):
        return f"{self.nombre_obra} | {self.descripcion} | {self.fecha_inicio} | {self.fecha_fin_estimado}"

## Funcion para eliminar archivos multimedia y que se refleje el cambio en la carpeta media   
    
    def delete(self, *args, **kwargs):
        if self.plano and os.path.isfile(self.plano.path):
            os.remove(self.plano.path)
        super().delete(*args, **kwargs)
## Funcion para cuando actualicemos el archivo multimedia se elimine el archivo anterior de la carpeta media
    def save(self, *args, **kwargs):
        try:
            old = Obra.objects.get(id_obra=self.id_obra)
            
            # Si cambian la imagen
            if old.plano and old.plano != self.plano:
                if os.path.isfile(old.plano.path):
                    os.remove(old.plano.path)

        except Obra.DoesNotExist:
            pass

        super().save(*args, **kwargs)



class Hitos(models.Model):
    id_hito=models.AutoField(primary_key=True)
    nombre_hito=models.CharField(max_length=50, unique=True)
    descripcion=models.TextField()
    fecha_inicio=models.DateField()
    fecha_fin_estimado=models.DateField()
    ESTADO_CHOICES = [
    ('Pendiente', 'Pendiente'),
    ('En progreso', 'En progreso'),
    ('Completado', 'Completado')
    ]
    estado=models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    avance_porcentaje=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    evidencia = models.FileField(upload_to='hitos/', null=True, blank=True)
    obra_id=models.ForeignKey('Obra', on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.nombre_hito} | {self.descripcion}"
## Funcion para eliminar archivos multimedia y que se refleje el cambio en la carpeta media   
    
    def delete(self, *args, **kwargs):
        if self.evidencia and os.path.isfile(self.evidencia.path):
            os.remove(self.evidencia.path)
        super().delete(*args, **kwargs)
## Funcion para cuando actualicemos el archivo multimedia se elimine el archivo anterior de la carpeta media
    def save(self, *args, **kwargs):
        try:
            old = Hitos.objects.get(id_hito=self.id_hito)
            if old.evidencia and old.evidencia != self.evidencia:
                if os.path.isfile(old.evidencia.path):
                    os.remove(old.evidencia.path)
        except Hitos.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class Cuadrilla_Trabajo(models.Model):
    id_cuadrilla=models.AutoField(primary_key=True)
    nombre_cuadrilla=models.CharField(max_length=50, unique=True)
    tipo_trabajo=models.CharField(max_length=50, unique=True)
    cantidad_trabajadores=models.IntegerField()
    obra_id=models.ForeignKey('Obra', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_cuadrilla} | {self.tipo_trabajo} | {self.cantidad_trabajadores}"

class Maquinaria_Pesada(models.Model):
    id_maquinaria=models.AutoField(primary_key=True)
    nombre_maquinaria=models.CharField(max_length=50, unique=False)
    tipo_maquinaria=models.CharField(max_length=50, unique=False)
    ESTADO_CHOICES = [
    ('disponible', 'Disponible'),
    ('en_uso', 'En Uso'),
    ('mantenimiento', 'Mantenimiento')
    ]
    estado=models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    imagen = models.ImageField(upload_to='maquinaria/', null=True, blank=True)
    obra_id=models.ForeignKey('Obra',on_delete=models.SET_NULL,
        null=True,
        blank=True)
    id_hito=models.ForeignKey('Hitos',on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return f"{self.nombre_maquinaria} | {self.tipo_maquinaria} | {self.estado}"
    
    def delete(self, *args, **kwargs):
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)
## Funcion para cuando actualicemos el archivo multimedia se elimine el archivo anterior de la carpeta media
    def save(self, *args, **kwargs):
        try:
            old = Maquinaria_Pesada.objects.get(id_maquinaria=self.id_maquinaria)
            
            # Si cambian la imagen
            if old.imagen and old.imagen != self.imagen:
                if os.path.isfile(old.imagen.path):
                    os.remove(old.imagen.path)

        except Maquinaria_Pesada.DoesNotExist:
            pass

        super().save(*args, **kwargs)
    

##Entidad Material
class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    unidad = models.CharField(max_length=20)  # kg, m3, unidades

    def __str__(self):
        return f"{self.nombre} ({self.unidad})"

##Rompemos la relacion  N:M
class MaterialObra(models.Model):
    id_material_obra = models.AutoField(primary_key=True)
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    
    cantidad_estimada = models.FloatField()
    cantidad_real = models.FloatField(default=0)

    def __str__(self):
        return f"{self.material.nombre} - {self.obra.nombre_obra}"

class Subcontratista(models.Model):
    id_subcontratista = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    obra_id = models.ForeignKey('Obra', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_empresa} | {self.especialidad}"


class Registro_Avances(models.Model):
    id_registro = models.AutoField(primary_key=True)
    fecha = models.DateField()
    avance = models.DecimalField(max_digits=5, decimal_places=2)
    reporte = models.FileField(upload_to='avances/', null=True, blank=True)
    hito_id = models.ForeignKey('Hitos', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.fecha} | {self.avance}"