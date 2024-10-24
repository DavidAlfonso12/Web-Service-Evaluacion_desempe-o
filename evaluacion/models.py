from django.db import models

# Create your models here.
class Unidades(models.Model):
    id_unidad = models.AutoField(primary_key=True)  # Campo AUTO_INCREMENT
    nombre_unidad = models.CharField(max_length=250)  # varchar(250)
    jefe_unidad = models.CharField(max_length=250)  # varchar(250)

    def __str__(self):
        return self.nombre_unidad
    
    class Meta:
        managed = False  # No permitir que Django gestione la tabla
        db_table = 'unidades'

class Empleados(models.Model):
    codigo_empleado = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre_empleado
    
    class Meta:
        managed = False
        db_table = 'empleados'

class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre_rol
    
    class Meta:
        managed = False
        db_table = 'roles'

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    foto = models.CharField(max_length=150)

    def __str__(self):
        return f'Imagen {self.id_imagen}'
    class Meta:
        managed = False
        db_table = 'imagenes'

class Empleados_roles(models.Model):
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='roles', db_column='id_rol')
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, related_name='roles', db_column='id_empleado')
    
    def __str__(self):
        return self.id_empleado
    
    class Meta:
        managed = False
        db_table = 'empleados_roles'

class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    componente2 = models.CharField(max_length=250)
    valor = models.FloatField()
    vinculo = models.IntegerField()
    evaluado = models.IntegerField()
    fecha = models.DateField(null=True, blank=True)
    componente = models.ForeignKey(Empleados, on_delete=models.CASCADE, related_name='competencias', db_column='componente')
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name='competencias', db_column='id_unidad')
    id_imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='competencias', db_column='id_imagen')
    cargo = models.CharField(max_length=250, null=True, blank=True)
    fortaleza = models.CharField(max_length=500, null=True, blank=True)
    capacitado = models.IntegerField()
    fecha_capacitacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.componente2
    class Meta:
        managed = False
        db_table = 'competencia'