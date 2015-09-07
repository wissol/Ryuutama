from flask import Flask, make_response, render_template, request

#import json

app = Flask(__name__)

# Funciones Auxiliares

def no_favoritas(favorita):
    todas = ["Hojas Cortas", "Hojas Largas", "Armas de Asta", "Hachas",
             "Arcos", "¡Sin Armas!"]
    todas.remove(favorita)
    return todas

def cargar_cookies(lista, x):
    for y in lista:
        try:
            x[y] = request.cookies.get(y)
        except:
            x[y] = 'ErrorErrorErrorErrorError'
    return x

def pg(fue, arquetipo):
    ''' calcula puntos de golpe) '''
    try:
        y = 2*int(fue)
        if arquetipo == "Ofensivo":
            y +=4
        return str(y)
    except:
        return "E"

def pm(esp, arquetipo):
    y = 2*int(esp)
    if arquetipo == "Mágico":
        y += 4
    return str(y)

def carga(fue, arquetipo, clase):
    y = int(fue) + 3
    if arquetipo == "Técnico":
        y += 3
    if clase == "Granjero":
        y += 3
    return str(y)

def cargar_de_request(lista, x):
    for y in lista:
        try:
            x[y] = request.form[y]
        except:
            x[y] = ""
    return x

def leer_caracteristicas(x):
    ''' interpreta el _select_ caracteristicas
    fue en la posición 4, des en la 10, int en la 16 esp en la 22'''
    return (x[4], x[10], x[16], x[22])

def galletitas(x, resp):
    ''' crea cookies '''
    for y in x.keys():
        resp.set_cookie(y, x[y])

# Funciones de route

@app.route('/')
def inicio():
    ''' carga la página de inicio '''
    return render_template('index.html')

@app.route('/detalles', methods=['POST'])
def detalles():
    no_f = []
    x = {} # diccionario con la información del personaje
    conjuros = ["Cristal de Luz Pura", "Campana de Alerta", "Brújula",
                "Mano Roja Mejorada", "Toque Curativo", "Estrella Fugaz",
                "Domador de Animales", "Reflejo Redondeado", "Sabor Sabebueno"]


    lista = ['nombre', 'genero', 'edad', 'color', 'hogar', 'clase', 'arquetipo',
             'caracteristicas', 'objeto', 'favorita']
    x = cargar_de_request(lista, x)

    no_f = no_favoritas(x["favorita"])

    resp = make_response(render_template('detalles.html', x=x, no_f=no_f, conjuros = conjuros))
    galletitas(x, resp)

    return resp

@app.route('/personaje', methods=['POST'])
def personaje():
    x = {}
    cookies = ['nombre', 'genero', 'edad', 'color', 'hogar', 'clase', 'arquetipo',
             'caracteristicas', 'objeto', 'favorita']

    x = cargar_cookies(cookies, x)

    datos_formulario = ['sarma', 'conjuro1', 'conjuro2', 'estacion', 'oficio', 'militar']

    x = cargar_de_request(datos_formulario, x)

    estacional = { "Primavera":["Levántate y Anda", "Manto de Flores", "Curar Plus Plus", "Un Poco de Belleza"],
                    "Verano":["Manto de Brezos", "Vitalidad de las Vacaciones", "Coro Min-Min de las Cigarras", "Bonita Hoja Koro-pok-kuru"],
                    "Otoño":["Hojas Caídas", "Luna de la Cosecha", "Mar de Lágrimas", "Botella de Mermelada Mágica"],
                    "Invierno":["Cubo de Hielo", "Máscara de Indiferencia", "Tormenta de Bolas de Nieve", "Sueño de Invierno"],
                    }

    habilidades =  {"Trovador":["Trotamundos", "Tradiciones", "Música"],
                    "Mercader":["Elocuencia", "Adiestrar", "Comerciar"],
                    "Cazador":["Rastrear", "Matarife", "Cazar"],
                    "Sanador":["Curar", "Primeros Auxilios", "Forrajear"],
                    "Granjero":["Robusto", "Adiestrar"],
                    "Artesano":["Matarife", "Artesanía", "Reparar"],
                    "Noble":["Etiqueta", "Cultura"]
                    }

    efectos =  {"Trotamundos":"+1 a Viaje",
                "Tradiciones":"Puedes obtener información adicional sobre algo que has visto o escuchado",
                "Música":"Todos los miembros del grupo tienen +1 a su siguiente tirada. Crítico +3. Pifia: Todos los PJs con Salud de 6 o menos sufren la Condición[Mareado]",
                "Elocuencia":"+1 a Negociación (INT+ESP) Siempre activo.",
                "Adiestrar":"2 animales adicionales no necesitan comida ni agua, para un total de 3",
                "Comerciar":"Puedes comprar o vender a mejor precio (ver pág 37)",
                "Rastrear":"Encuentras un monstruo. +1 al Daño contra el monstruo que hayas encontrado",
                "Matarife":"Consigues materiales a partir de un monstruo derrotado",
                "Cazar":"Consigues tantas raciones como Tirada - Número Objetivo. No puedes participar en la tirada de acampada. Crítico razones sabrosas. Pifia: Condición[Herido: 6]",
                "Curar":"El personaje tratado recupera tanto como una tirada de INT+DES, en combate sólo se tira INT (1 dado)",
                "Primeros Auxilios":"Cura una Condición de un personaje durante 1 hora. Además reduce la severidad de una Condición en una cantidad igual al nivel del Sanador",
                "Forrajear":"Encuentra 1 planta medicinal. Crítico: Encuentras 3. Pifia: Envenenado:6",
                "Robusto":"+1 a las tiradas de Salud, todos los días. +3 a carga (ya sumado)",
                "Artesanía":"Fabricas un objeto de tu especialidad",
                "Reparar":"Reparas un objeto haciendo que su durabilidad vuelva a su valor original",
                "Etiqueta":"Dejas una impresión positiva de ti mismo ante alguien de alto rango o estatus social elevado",
                "Cultura":"Conoces información detallada sobre algo que has visto o escuchado",
                }

    prerrequisitos =  {"Trotamundos":"-",
                "Tradiciones":"Ves o escuchas algo",
                "Música":"Sólo con Terreno o Clima adecuado, cada uso reduce los PG en 1",
                "Elocuencia":"Realizar una tirada de Negociación",
                "Adiestrar":"-",
                "Comerciar":"Comprar o vender 4 o más objetos del mismo tipo",
                "Rastrear":"Encontrar las huellas del monstruo",
                "Matarife":"Derrotar a un monstruo",
                "Cazar":"Antes de la tirada de Acampada, una vez al día.",
                "Curar":"Gastar 1 planta medicinal y 1 ración de agua",
                "Primeros Auxilios":"Un personaje que no ha recibido Primeros Auxilios hoy",
                "Forrajear":"Por la mañana, antes de la tirada de Movimiento, una vez al día",
                "Robusto":"-",
                "Artesanía":"Debes disponer del tiempo (1 día por tamaño) y los materiales (la mitad del coste del objeto en oro)",
                "Reparar":"Debes disponer del tiempo (1 día por tamaño) y los materiales (10% del coste del objeto en oro)",
                "Etiqueta":"-",
                "Cultura":"Ves o escuchas algo",
                }

    cars =     {"Trotamundos":"-",
                "Tradiciones":"INT + INT",
                "Música":"DES + ESP",
                "Elocuencia":"-",
                "Adiestrar":"-",
                "Comerciar":"INT + ESP",
                "Rastrear":"FUE + INT",
                "Matarife":"DES + INT",
                "Cazar":"DES + INT.",
                "Curar":"INT + ESP, durante el combate INT",
                "Primeros Auxilios":"INT + ESP",
                "Forrajear":"FUE + INT",
                "Robusto":"-",
                "Artesanía":"FUE + DES",
                "Reparar":"FUE + DES",
                "Etiqueta":"DES + INT",
                "Cultura":"INT + INT",
                }

    nobj =     {"Trotamundos":"-",
                "Tradiciones":"A elección del DJ",
                "Música":"Topografía",
                "Elocuencia":"-",
                "Adiestrar":"-",
                "Comerciar":"ver página 36",
                "Rastrear":"Topografía",
                "Matarife":"Nivel del monstruo x 2",
                "Cazar":"Topografía",
                "Curar":"-",
                "Primeros Auxilios":"Severidad de la Condición",
                "Forrajear":"Topografía",
                "Robusto":"-",
                "Artesanía":"Según el precio cien o menos: 6; 101 a mil: 8; mil a diezmil: 10; diezmil a cienmil: 14, más 18",
                "Reparar":"Según el precio cien o menos: 6; 101 a mil: 8; mil a diezmil: 10; diezmil a cienmil: 14, más 18",
                "Etiqueta":"Tirada enfrentada",
                "Cultura":"A elección del DJ",
                }


    x["fue"], x["des"], x["int"], x["esp"] = leer_caracteristicas(x['caracteristicas'])
    x['pg'] = pg(x['fue'], x['arquetipo'])
    x['pm'] = pm(x['esp'], x['arquetipo'])
    x['carga'] = carga(x['fue'], x['arquetipo'], x['clase'])
    x['salud'] = int(x['fue']) + int(x['esp'])
    x['iniciativa'] = int(x['des']) + int(x['int'])

    if x['arquetipo'] == "Mágico":
        x['estacional'] = estacional[x['estacion']]


    x['habilidades'] = habilidades[x['clase']]

    if x['clase'] == 'Granjero':
        if x['oficio'] == "Hojas Largas" or x['oficio'] == "Arcos" or x["oficio"] == "Armas de Asta":
            x['militar'] = x['oficio']
        else:
            x['habilidades'].append(x['oficio'])

    if x['militar']:
        if x['militar'] == x['favorita']:
            x['favorita'] += " +1"
        elif x['sarma']:
            if x['sarma'] == x['militar']:
                x['sarma'] += " +1"
    else:
        x['militar'] = 'nada'



    return render_template('personaje.html', x=x, efectos = efectos, pre = prerrequisitos, cars = cars, nobj = nobj)

