
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.inicio),
        path('newobras/',views.newobras),
        path('showobras/',views.showobras),
        path('guardar_obra/',views.guardar_obra),
        path('deleteobras/<id_obra>',views.deleteobras),
        path('updateobras/<int:id_obra>',views.updateobras),
        path('procesoupobra/',views.procesoupobra),
        path('eventos_obras/', views.eventos_obras),
        path('calendario_obras/', views.calendario_obras),
        path('showhitos/',views.showhitos),
        path('newhitos/',views.newhitos),
        path('guardar_hito/',views.guardar_hito),
        path('deletehitos/<id_hito>',views.deletehitos),
        path('updatehitos/<id_hito>',views.updatehitos),
        path('procesouphito/',views.procesouphito),
        path('showcuadrilla/',views.showcuadrilla),
        path('newcuadrilla/',views.newcuadrilla),
        path('guardar_cuadrilla/',views.guardar_cuadrilla),
        path('deletecuadrilla/<id>',views.deletecuadrilla),
        path('updatecuadrilla/<id_cuadrilla>',views.updatecuadrilla),
        path('procesoupcuadrilla/',views.procesoupcuadrilla),
        path('showmaquinaria/',views.showmaquinaria),
        path('newmaquinaria/',views.newmaquinaria),
        path('guardar_maquinaria/',views.guardar_maquinaria),
        path('deletemaquinaria/<id>',views.deletemaquinaria),
        path('updatemaquinaria/<id>',views.updatemaquinaria),
        path('procesoupmaquinaria/',views.procesoupmaquinaria),
        path('showmaterial/',views.showmaterial),
        path('newmaterial/',views.newmaterial),
        path('guardar_material/',views.guardar_material),
        path('deletematerial/<id>',views.deletematerial),
        path('updatematerial/<id>',views.updatematerial),
        path('procesoupmaterial/',views.procesoupmaterial),
        # Material Obra
        path('showmaterialobra/',views.showmaterialobra),
        path('newmaterialobra/',views.newmaterialobra),
        path('guardar_materialobra/',views.guardar_materialobra),
        path('deletematerialobra/<id>',views.deletematerialobra),
        path('updatematerialobra/<id>',views.updatematerialobra),
        path('procesoupmaterialobra/',views.procesoupmaterialobra),
        # Subcontratista
        path('showsubcontratista/',views.showsubcontratista),
        path('newsubcontratista/',views.newsubcontratista),
        path('guardar_subcontratista/',views.guardar_subcontratista),
        path('deletesubcontratista/<id>',views.deletesubcontratista),
        path('updatesubcontratista/<id>',views.updatesubcontratista),
        path('procesoupsubcontratista/',views.procesoupsubcontratista),
        # Registro Avances
        path('showavance/',views.showavance),
        path('newavance/',views.newavance),
        path('guardar_avance/',views.guardar_avance),
        path('deleteavance/<id>',views.deleteavance),
        path('updateavance/<id>',views.updateavance),
        path('procesoupavance/',views.procesoupavance),
        # Registro de avances por obra (carpeta registro/)
        path('registro/',views.registro_por_obra),
        path('registro/obra/<id_obra>',views.registro_detalle_obra),
        # Dashboard
        path('dashboard/',views.dashboard),
        # Asignacion Maquinaria Drag & Drop
        path('asignar_maquinaria/',views.asignar_maquinaria),
        path('guardar_asignacion_maquinaria/',views.guardar_asignacion_maquinaria),
]
