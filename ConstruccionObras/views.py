from django.shortcuts import render, redirect
from .models import Obra , Hitos, Cuadrilla_Trabajo, Maquinaria_Pesada, Material, MaterialObra, Subcontratista, Registro_Avances
from decimal import Decimal, InvalidOperation

##Para el DataCalendari
from django.http import JsonResponse

# Create your views here.

def inicio(request):
    return render(request,'principal/inicio.html')


def newobras(request):
    return render(request,'obra/newobras.html')

def showobras(request):
    obras=Obra.objects.all()

    return render(request, 'obra/showobras.html',
                  {'misobras':obras})

def calendario_obras(request):
    return render(request, 'obra/eventos_obras.html')

def guardar_obra(request):
    try:
        presupuesto_raw = request.POST.get('presupuesto')

        if not presupuesto_raw:
            presupuesto = None  # o 0 si quieres
        else:
            presupuesto = Decimal(presupuesto_raw)

    except InvalidOperation:
        presupuesto = None  # o maneja error

    nombre_f=request.POST['nombre']
    descripcion_f=request.POST['descripcion']
    fecha_in_f=request.POST['fecha_in']
    fecha_fin=request.POST['fecha_fin']
    palno=request.FILES.get("plano")
    estadof=request.POST['estado']
    obra=Obra.objects.create(
        nombre_obra = nombre_f,
        descripcion =descripcion_f,
        fecha_inicio = fecha_in_f,
        fecha_fin_estimado = fecha_fin,
        presupuesto_total = presupuesto,
        plano = palno,
        estado = estadof

    )
    return redirect('/showobras/')

def deleteobras(requets,id_obra):
    obradelete=Obra.objects.get(id_obra=id_obra)
    obradelete.delete()
    return redirect('/showobras/')



def updateobras(request,id_obra):
    obra=Obra.objects.get(id_obra=id_obra)
    return render(request,'obra/editobras.html',
                  {'obras':obra})

def procesoupobra(request):
    id=request.POST['id_obra']
    obra=Obra.objects.get(id_obra=id)
    obra.nombre_obra=request.POST['nombre']
    obra.descripcion=request.POST['descripcion']
    obra.fecha_inicio=request.POST['fecha_in']
    obra.fecha_fin_estimado=request.POST['fecha_fin']
    try:
        presupuesto_raw = request.POST.get('presupuesto')
        obra.presupuesto_total = Decimal(presupuesto_raw) if presupuesto_raw else None
    except InvalidOperation:
        obra.presupuesto_total = None
    obra.estado=request.POST['estado']
    plano=request.FILES.get('plano')
    if plano:
        obra.plano=plano
    obra.save()
    return redirect('/showobras/')

def eventos_obras(request):
    obras = Obra.objects.all()

    eventos = []

    for obra in obras:
        eventos.append({

            'id': obra.id_obra,

            'title': obra.nombre_obra,

            'start': obra.fecha_inicio.strftime('%Y-%m-%d'),

            'end': obra.fecha_fin_estimado.strftime('%Y-%m-%d'),

            'color':( 
                'green' if obra.estado == 'Finalizada' 
                else 'blue' if obra.estado == 'Planificada'
                else 'gray' if obra.estado == 'Suspendida'
                else 'orange'),

            'extendedProps': {

                'descripcion': obra.descripcion,

                'presupuesto': str(obra.presupuesto_total),

                'estado': obra.estado,

                'fecha_fin': obra.fecha_fin_estimado.strftime('%Y-%m-%d')

            }

        })

    return JsonResponse(eventos, safe=False)


##HITOS

def newhitos(request):
    obras=Obra.objects.all()
    return render(request,'hitos/newhitos.html',
                  {'miobra':obras})

def showhitos(request):
    hito=Hitos.objects.all()
    return render(request, 'hitos/showhitos.html',
                {'mishitos':hito})


def guardar_hito(request):
    nombre_f=request.POST['nombre']
    descripcion_f=request.POST['descripcion']
    fecha_in_f=request.POST['fecha_in']
    fecha_fin=request.POST['fecha_fin']
    avance_f=request.POST.get("avance")
    estadof=request.POST['estado']
    evidencias_f=request.FILES.get('evidencias')
    obra_f=request.POST['obra']
    hito=Hitos.objects.create(
        nombre_hito = nombre_f,
        descripcion =descripcion_f,
        fecha_inicio = fecha_in_f,
        fecha_fin_estimado = fecha_fin,
        estado = estadof,
        avance_porcentaje=avance_f,
        evidencia=evidencias_f,
        obra_id_id=obra_f

    )
    return redirect('/showhitos/')

def deletehitos(requets,id_hito):
    hitodelete=Hitos.objects.get(id_hito=id_hito)
    hitodelete.delete()
    return redirect('/showhitos/')



def updatehitos(request,id_hito):
    hito_f=Hitos.objects.get(id_hito=id_hito)
    obras=Obra.objects.all()
    return render(request,'hitos/edithitos.html',
                  {'hitos':hito_f,
                  'miobra':obras})

def procesouphito(request):
    id=request.POST['id_hito']
    hito=Hitos.objects.get(id_hito=id)
    hito.nombre_hito=request.POST['nombre']
    hito.descripcion=request.POST['descripcion']
    hito.fecha_inicio=request.POST['fecha_in']
    hito.fecha_fin_estimado=request.POST['fecha_fin']
    hito.avance_porcentaje=request.POST['avance']
    hito.estado=request.POST['estado']
    evidencia = request.FILES.get('evidencias')
    if evidencia:
        hito.evidencia = evidencia
    hito.obra_id_id = request.POST['obra']
    hito.save()
    return redirect('/showhitos/')


##Cuadrilla

def newcuadrilla(request):
    obras = Obra.objects.all()
    return render(request, 'cuadrilla_trabajo/newcuadrilla.html', {'obras': obras})


def showcuadrilla(request):
    cuadrillas = Cuadrilla_Trabajo.objects.all()
    return render(request, 'cuadrilla_trabajo/showcuadrilla.html', {'cuadrillas': cuadrillas})


def guardar_cuadrilla(request):
    Cuadrilla_Trabajo.objects.create(
        nombre_cuadrilla=request.POST['nombre'],
        tipo_trabajo=request.POST['tipo'],
        cantidad_trabajadores=request.POST['cantidad'],
        obra_id_id=request.POST['obra']
    )
    return redirect('/showcuadrilla/')


def deletecuadrilla(request, id):
    c = Cuadrilla_Trabajo.objects.get(id_cuadrilla=id)
    c.delete()
    return redirect('/showcuadrilla/')


def updatecuadrilla(request, id_cuadrilla):
    c = Cuadrilla_Trabajo.objects.get(id_cuadrilla=id_cuadrilla)
    obras = Obra.objects.all()
    return render(request, 'cuadrilla_trabajo/editcuadrilla.html', {'c': c, 'obras': obras})


def procesoupcuadrilla(request):
    id=request.POST['id_cuadrilla']
    c = Cuadrilla_Trabajo.objects.get(id_cuadrilla=id)
    c.nombre_cuadrilla = request.POST['nombre']
    c.tipo_trabajo = request.POST['tipo']
    c.cantidad_trabajadores = request.POST['cantidad']
    c.obra_id_id = request.POST['obra']
    c.save()
    return redirect('/showcuadrilla/')


## Maquinaria
def newmaquinaria(request):
    obras = Obra.objects.all()
    hitos = Hitos.objects.all()
    return render(request, 'maquinaria/newmaquinaria.html', {'obras': obras, 'hitos': hitos})


def showmaquinaria(request):
    data = Maquinaria_Pesada.objects.all()
    return render(request, 'maquinaria/showmaquinaria.html', {'maquinaria': data})


def guardar_maquinaria(request):
    Maquinaria_Pesada.objects.create(
        nombre_maquinaria=request.POST['nombre'],
        tipo_maquinaria=request.POST['tipo'],
        estado=request.POST['estado'],
        imagen=request.FILES.get('imagen'),
    )
    return redirect('/showmaquinaria/')


def deletemaquinaria(request, id):
    m = Maquinaria_Pesada.objects.get(id_maquinaria=id)
    m.delete()
    return redirect('/showmaquinaria/')


def updatemaquinaria(request, id):
    m = Maquinaria_Pesada.objects.get(id_maquinaria=id)
    obras = Obra.objects.all()
    hitos = Hitos.objects.all()
    return render(request, 'maquinaria/updatemaquinaria.html', {'m': m, 'obras': obras, 'hitos': hitos})


def procesoupmaquinaria(request):
    m = Maquinaria_Pesada.objects.get(id_maquinaria=request.POST['id'])
    m.nombre_maquinaria = request.POST['nombre']
    m.tipo_maquinaria   = request.POST['tipo']
    m.estado            = request.POST['estado']
    m.obra_id_id        = request.POST.get('obra') or None
    m.id_hito_id        = request.POST.get('hito') or None
    img = request.FILES.get('imagen')
    if img:
        m.imagen = img
    m.save()
    return redirect('/showmaquinaria/')



## Material
def newmaterial(request):
    return render(request, 'material/newmaterial.html')


def showmaterial(request):
    data = Material.objects.all()
    return render(request, 'material/showmaterial.html', {'material': data})


def guardar_material(request):
    Material.objects.create(
        nombre=request.POST['nombre'],
        unidad=request.POST['unidad']
    )
    return redirect('/showmaterial/')


def deletematerial(request, id):
    m = Material.objects.get(id_material=id)
    m.delete()
    return redirect('/showmaterial/')


def updatematerial(request, id):
    m = Material.objects.get(id_material=id)
    return render(request, 'material/editmaterial.html', {'m': m})


def procesoupmaterial(request):
    m = Material.objects.get(id_material=request.POST['id'])
    m.nombre = request.POST['nombre']
    m.unidad = request.POST['unidad']
    m.save()
    return redirect('/showmaterial/')


## MAterialPrima
def newmaterialobra(request):
    obras = Obra.objects.all()
    materiales = Material.objects.all()
    return render(request, 'materialobra/newmaterialobra.html', {'obras': obras, 'materiales': materiales})


def showmaterialobra(request):
    data = MaterialObra.objects.all()
    return render(request, 'materialobra/showmaterialobra.html', {'data': data})


def guardar_materialobra(request):
    MaterialObra.objects.create(
        obra_id=request.POST['obra'],
        material_id=request.POST['material'],
        cantidad_estimada=request.POST['estimada'],
        cantidad_real=request.POST['real']
    )
    return redirect('/showmaterialobra/')


def deletematerialobra(request, id):
    m = MaterialObra.objects.get(id_material_obra=id)
    m.delete()
    return redirect('/showmaterialobra/')

def updatematerialobra(request, id):
    mo = MaterialObra.objects.get(id_material_obra=id)
    obras = Obra.objects.all()
    materiales = Material.objects.all()

    return render(request, 'materialobra/editmaterialobra.html', {
        'mo': mo,
        'obras': obras,
        'materiales': materiales
    })

def procesoupmaterialobra(request):
    mo = MaterialObra.objects.get(id_material_obra=request.POST['id'])
    mo.obra_id         = request.POST['obra']
    mo.material_id     = request.POST['material']
    mo.cantidad_estimada = request.POST['estimada']
    mo.cantidad_real     = request.POST['real']
    mo.save()
    return redirect('/showmaterialobra/')

## SUBCONTRATISTA
def newsubcontratista(request):
    obras = Obra.objects.all()
    return render(request, 'subcontratista/new.html', {'obras': obras})


def showsubcontratista(request):
    data = Subcontratista.objects.all()
    return render(request, 'subcontratista/show.html', {'data': data})


def guardar_subcontratista(request):
    Subcontratista.objects.create(
        nombre_empresa=request.POST['empresa'],
        especialidad=request.POST['especialidad'],
        telefono=request.POST['telefono'],
        email=request.POST['email'],
        obra_id_id=request.POST['obra']
    )
    return redirect('/showsubcontratista/')


def deletesubcontratista(request, id):
    s = Subcontratista.objects.get(id_subcontratista=id)
    s.delete()
    return redirect('/showsubcontratista/')
def updatesubcontratista(request, id):
    s = Subcontratista.objects.get(id_subcontratista=id)
    obras = Obra.objects.all()

    return render(request, 'subcontratista/edit.html', {
        's': s,
        'obras': obras
    })

def procesoupsubcontratista(request):
    s = Subcontratista.objects.get(id_subcontratista=request.POST['id'])

    s.nombre_empresa = request.POST['empresa']
    s.especialidad = request.POST['especialidad']
    s.telefono = request.POST['telefono']
    s.email = request.POST['email']
    s.obra_id_id = request.POST['obra']

    s.save()

    return redirect('/showsubcontratista/')


##Registro Avances
def newavance(request):
    hitos = Hitos.objects.all()
    return render(request, 'avances/new.html', {'hitos': hitos})


def showavance(request):
    data = Registro_Avances.objects.all()
    return render(request, 'avances/show.html', {'data': data})


def guardar_avance(request):
    Registro_Avances.objects.create(
        fecha=request.POST['fecha'],
        avance=request.POST['avance'],
        reporte=request.FILES.get('reporte'),
        hito_id_id=request.POST['hito']
    )
    return redirect('/showavance/')


def deleteavance(request, id):
    a = Registro_Avances.objects.get(id_registro=id)
    a.delete()
    return redirect('/showavance/')

def updateavance(request, id):
    a = Registro_Avances.objects.get(id_registro=id)
    hitos = Hitos.objects.all()

    return render(request, 'avances/edit.html', {
        'a': a,
        'hitos': hitos
    })



def procesoupavance(request):
    a = Registro_Avances.objects.get(id_registro=request.POST['id'])

    a.fecha = request.POST['fecha']
    a.avance = request.POST['avance']

    # SOLO si suben nuevo archivo
    if request.FILES.get('reporte'):
        a.reporte = request.FILES.get('reporte')

    a.hito_id_id = request.POST['hito']

    a.save()

    return redirect('/showavance/')


## Dashboard
def dashboard(request):
    from django.db.models import Sum
    import json

    # ── Datos para S-Curve presupuestario ──────────────────────────────────
    # Todas las obras con presupuesto
    obras = Obra.objects.filter(presupuesto_total__isnull=False).order_by('fecha_inicio')

    # Presupuesto acumulado estimado por fecha de inicio de obra
    presupuesto_labels = [str(o.fecha_inicio) for o in obras]
    presupuesto_acumulado = []
    acum = 0
    for o in obras:
        acum += float(o.presupuesto_total or 0)
        presupuesto_acumulado.append(round(acum, 2))

    # Gasto real aproximado: suma de cantidad_real * (precio_unitario simulado = 1)
    # Usamos MaterialObra como proxy de consumo
    gasto_real_labels = presupuesto_labels
    gasto_real_acumulado = []
    acum_real = 0
    for o in obras:
        consumo = MaterialObra.objects.filter(obra=o).aggregate(total=Sum('cantidad_real'))['total'] or 0
        acum_real += float(consumo)
        gasto_real_acumulado.append(round(acum_real, 2))

    # ── Datos para S-Curve de cronograma ───────────────────────────────────
    # Usa los registros reales de Registro_Avances agrupados por fecha
    from django.db.models import Avg as DjAvg
    hitos = Hitos.objects.filter(obra_id__isnull=False).order_by('fecha_inicio')
    hitos_labels = [str(h.fecha_inicio) for h in hitos]
    avance_planificado = []
    avance_real = []
    n_hitos = len(hitos)
    for i, h in enumerate(hitos):
        avance_planificado.append(round(100 * (i + 1) / n_hitos if n_hitos else 0, 2))
        # Promedio de registros reales para este hito
        prom = Registro_Avances.objects.filter(hito_id=h).aggregate(
            p=DjAvg('avance')
        )['p']
        avance_real.append(float(prom or h.avance_porcentaje or 0))

    # ── Datos para reporte materiales vs estimado ──────────────────────────
    mat_obra = MaterialObra.objects.select_related('material', 'obra').all()
    mat_labels = [f"{m.material.nombre} ({m.obra.nombre_obra})" for m in mat_obra]
    mat_estimado = [float(m.cantidad_estimada) for m in mat_obra]
    mat_real = [float(m.cantidad_real) for m in mat_obra]

    # ── KPIs simples ───────────────────────────────────────────────────────
    total_obras = Obra.objects.count()
    obras_en_ejecucion = Obra.objects.filter(estado='En ejecucion').count()
    hitos_completados = Hitos.objects.filter(estado='Completado').count()
    total_subcontratistas = Subcontratista.objects.count()

    context = {
        'presupuesto_labels': json.dumps(presupuesto_labels),
        'presupuesto_acumulado': json.dumps(presupuesto_acumulado),
        'gasto_real_acumulado': json.dumps(gasto_real_acumulado),
        'hitos_labels': json.dumps(hitos_labels),
        'avance_planificado': json.dumps(avance_planificado),
        'avance_real': json.dumps(avance_real),
        'mat_labels': json.dumps(mat_labels),
        'mat_estimado': json.dumps(mat_estimado),
        'mat_real': json.dumps(mat_real),
        'total_obras': total_obras,
        'obras_en_ejecucion': obras_en_ejecucion,
        'hitos_completados': hitos_completados,
        'total_subcontratistas': total_subcontratistas,
    }
    return render(request, 'dashboard/dashboard.html', context)


## Asignacion de maquinaria a frentes de trabajo (drag & drop)
def asignar_maquinaria(request):
    maquinaria_disponible = Maquinaria_Pesada.objects.filter(estado='disponible')
    maquinaria_en_uso = Maquinaria_Pesada.objects.filter(estado='en_uso')
    obras = Obra.objects.exclude(estado='Finalizada')
    return render(request, 'maquinaria/asignar_maquinaria.html', {
        'disponible': maquinaria_disponible,
        'en_uso': maquinaria_en_uso,
        'obras': obras,
    })


def guardar_asignacion_maquinaria(request):
    if request.method == 'POST':
        maquinaria_ids = request.POST.getlist('maquinaria_ids[]')
        obra_id = request.POST.get('obra_id')
        if obra_id and maquinaria_ids:
            for mid in maquinaria_ids:
                try:
                    m = Maquinaria_Pesada.objects.get(id_maquinaria=int(mid))
                    m.obra_id_id = int(obra_id)
                    m.estado = 'en_uso'
                    m.save()
                except Maquinaria_Pesada.DoesNotExist:
                    pass
    return redirect('/asignar_maquinaria/?ok=1')


## Registro de Avances agrupado por Obra (carpeta registro/)
def registro_por_obra(request):
    from django.db.models import Avg

    obras = Obra.objects.all().order_by('fecha_inicio')
    resumen = []

    for obra in obras:
        hitos_obra   = Hitos.objects.filter(obra_id=obra)
        registros    = Registro_Avances.objects.filter(
            hito_id__in=hitos_obra
        ).order_by('-fecha')
        subcontratistas = Subcontratista.objects.filter(obra_id=obra)

        # Avance promedio de los REGISTROS de avance (dato real diario)
        avance_registros = registros.aggregate(prom=Avg('avance'))['prom'] or 0

        # Avance promedio de los HITOS (porcentaje asignado al hito)
        avance_hitos = hitos_obra.aggregate(prom=Avg('avance_porcentaje'))['prom'] or 0

        resumen.append({
            'obra'              : obra,
            'hitos'             : hitos_obra,
            'registros'         : registros,
            'subcontratistas'   : subcontratistas,
            'avance_registros'  : round(float(avance_registros), 2),
            'avance_hitos'      : round(float(avance_hitos), 2),
            'total_registros'   : registros.count(),
        })

    return render(request, 'registro/resumen.html', {'resumen': resumen})


def registro_detalle_obra(request, id_obra):
    from django.db.models import Avg

    obra            = Obra.objects.get(id_obra=id_obra)
    hitos_obra      = Hitos.objects.filter(obra_id=obra)
    registros       = Registro_Avances.objects.filter(
        hito_id__in=hitos_obra
    ).order_by('-fecha')
    subcontratistas = Subcontratista.objects.filter(obra_id=obra)

    avance_registros = registros.aggregate(prom=Avg('avance'))['prom'] or 0
    avance_hitos     = hitos_obra.aggregate(prom=Avg('avance_porcentaje'))['prom'] or 0

    return render(request, 'registro/detalle.html', {
        'obra'            : obra,
        'hitos'           : hitos_obra,
        'registros'       : registros,
        'subcontratistas' : subcontratistas,
        'avance_registros': round(float(avance_registros), 2),
        'avance_hitos'    : round(float(avance_hitos), 2),
    })
