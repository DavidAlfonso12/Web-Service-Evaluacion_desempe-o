from django.urls import path, include
from evaluacion import views
from .views import LoginView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'unidades', views.lista_unidades, 'unidades')
router.register(r'empleados', views.lista_empleados, 'empleados')
router.register(r'imagenes', views.lista_imagenes, 'imagenes')
router.register(r'competencia', views.lista_empleados_unidad, 'competencia')
router.register(r'detalleEmpleado', views.Detalle_empleado, 'detalleEmpleado')
router.register(r'competencias_unidad', views.competencias_unidad, 'competencias_unidad')
router.register(r'resultados_empleados', views.resultado_empleados_unidad, 'resultados_empleados')
router.register(r'resumen_equipo', views.resumen_equipo, 'resumen_equipo')
router.register(r'Empleados_evaluados', views.Empleados_evaluados, 'Empleados_evaluados')
router.register(r'promedio', views.EmpleadosPromedioAPIView, 'promedio')
router.register(r'Apreciaciones', views.MejoresCompetenciasViewSet, 'Apreciaciones')
router.register(r'capacitados_mes', views.CapacitandoceView, 'capacitados_mes')
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]