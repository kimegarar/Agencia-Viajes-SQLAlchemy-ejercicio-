import sys

import db
from models import Destino, Viaje, GuiaTuristico, Cliente, Reserva, Pasaporte
from datetime import date, datetime



#def auxiliar, para no crear cada vez que se ejecute Destinos, Guías o ... repetidos, 'cada ciudad es única'
#buscar el dato que sea, ver si ya existe: sino se crea, si si se avisa y no se crea
#para Destino, GuiaTuristico o Viaje
def obtener_o_crear(modelo, **kwargs): #**kwargs: deja k la def acepte cualquier nº de args que no existan...
    #...captura cualquier filtro que le envíes y lo guarda en un diccionario. modelo: la class
    instancia = db.session.query(modelo).filter_by(**kwargs).first()
#"desempaqueta" el diccionario y crea el filtro x, con first() da el 1º resultado que encuentra, o devuelve None si no
    if instancia: #si esta, ya existe y la devuelve
        #print(f"Recuperando existente: {kwargs}")
        return instancia
    else: #sino existe se añade
        #print(f"Creando nuevo: {kwargs}") #trabaja por detras, no deberia decir nada
        nueva_instancia = modelo(**kwargs)#crear el objeto nuevo: nuevo_objeto = Modelo(**datos)
        db.session.add(nueva_instancia)#añadirlo a la db
        db.session.commit() #guardamos!!!
        return nueva_instancia
    #cada vez se use este def ya hara el add() y commit()


#Nivel 0 (Independientes): Crear Destinos y GuiasTuristicos.
def anyadir_destinos(): #instanciar Destino: (lo hago manualmnt, podria ser con inputs
    print('>>> añadiendo destinos') #nombre, pais
    destino1 = obtener_o_crear(Destino, nombre='Roma', pais='Italia')
    destino2 = obtener_o_crear(Destino, nombre='Málaga', pais='España')
    destino3 = obtener_o_crear(Destino, nombre='Perpiñan', pais='Francia')
    #añadir #guardar destino: en caso de no existir con obtener_o_crear()

    print('...DESTINOS AÑADIDOS CORRECTAMENTE, sin repetidos')

def anyadir_guias():
    print('>>> añadiendo guias turisticos')  # nombre, idioma
    guia1 = obtener_o_crear(GuiaTuristico, nombre='María', idioma='español')
    guia2 = obtener_o_crear(GuiaTuristico, nombre='Peter', idioma='ingles')
    guia3 = obtener_o_crear(GuiaTuristico, nombre='Pietro', idioma='italiano')
    guia4 = obtener_o_crear(GuiaTuristico, nombre='Monique', idioma='frances')
    # añadir destino:
    ##db.session.add_all([guia1, guia2, guia3, guia4]) #esta vez usando add_all([lista, de , objetos])
    # guardar!:

    print('...GUIAS T. AÑADIDOS CORRECTAMENTE, sin repetidos')


def cargar_catalogo(): #combina el añadir los destinos y los guias
    anyadir_destinos()
    anyadir_guias()



#-----------------------------------------------------------------------------------------------------
#Nivel 1 (Dependientes): Crear Viajes (usando los objetos del Nivel 0).
# 1:N (Un Destino (Roma) puede tener muchos Viajes distintos asignados, pero un Viaje va a un solo Destino.),
#     (Un Guía (María) puede llevar muchos Viajes, pero un Viaje tiene un solo Guía principal.)

def crear_viajes(): # titulo, disponible, destino_id, destino, guia_id, guia
    destino_seleccionado1 = db.session.query(Destino).filter_by(nombre='Roma').first() #se busca destino
    guia_seleccionado1 = db.session.query(GuiaTuristico).filter_by(nombre='María').first() #se busca un guia
    viaje1 = obtener_o_crear(Viaje,titulo='SPQR', disponible=True, destino=destino_seleccionado1, guia=guia_seleccionado1)
    #db.session.add(viaje1)

    destino_seleccionado2 = db.session.query(Destino).filter_by(nombre='Málaga').first()
    guia_seleccionado2 = db.session.query(GuiaTuristico).filter_by(nombre='Peter').first()
    viaje2 = obtener_o_crear(Viaje,titulo='The Sunny Sol', disponible=True, destino=destino_seleccionado2, guia=guia_seleccionado2)
    #db.session.add(viaje2)

    destino_seleccionado3 = db.session.query(Destino).filter_by(nombre='Perpiñan').first()  # se busca destino
    guia_seleccionado3 = db.session.query(GuiaTuristico).filter_by(nombre='Monique').first()  # se busca un guia
    viaje3 = obtener_o_crear(Viaje,titulo='le Tour', disponible=False, destino=destino_seleccionado3, guia=guia_seleccionado3)
    #db.session.add(viaje3)

    #db.session.add_all([viaje1, viaje2, viaje3]) #se añaden a la base datos
#comento esta linea ya que me salia esto: (asique hago add individuales
#SAWarning: Object of type <Reserva> not in session, add operation along 'Cliente.reservas' will not proceed
    # (This warning originated from the Session 'autoflush' process, which was invoked automatically in
    # response to a user-initiated operation. Consider using ``no_autoflush`` context manager if this warning
    # happened while initializing objects.)

    #db.session.commit() #y guardar
    print('...VIAJES AÑADIDOS CORRECTAMENTE')


#-----------------------------------------------------------------------------------------------------
#Nivel 2 (Clientes): Crear Cliente y su Pasaporte.
#(relacion 1:1, Un Cliente tiene un solo Pasaporte y ese Pasaporte es solo de ese Cliente.)
#cliente: nombre, apellido, email, documento
#pasaporte: numero, nacionalidad, cliente_id, cliente
def crear_clientes():
    #pasaporte1 = Pasaporte(numero='34657642f', nacionalidad='española') #1º el accesorio que va al obj 'dueño'
    #cliente1 = obtener_o_crear(Cliente, nombre='Pascal', apellido='Perez', email='paspe@algo.es', documento=pasaporte1)
    #db.session.add(cliente1) #ASI LO HICE POR PRIMERA VEZ

    #PASO 1: Asegurar k Cliente existe(sin pasapor aun)# al no pasarle el documento aki, no se lía buscando cosas raras.
    c1 = obtener_o_crear(Cliente, nombre='Pascal', apellido='Perez', email='paspe@algo.es')
    #PASO 2: Asegura k Pasaporte existe y se lo enchufa al cliente, 'cliente=c1' para conectarlos.
    p1= obtener_o_crear(Pasaporte, numero='34657642f', nacionalidad='española', cliente=c1)

    c2 = obtener_o_crear(Cliente, nombre='Rita', apellido='Smith', email='smithzzzz@algo.com')
    p2 = obtener_o_crear(Pasaporte,numero='02957349D', nacionalidad='britanica', cliente=c2)

    c3 = obtener_o_crear(Cliente, nombre='Heinrik', apellido='Dsfeh', email='h_sfeh@algo.org')
    p3 = obtener_o_crear(Pasaporte, numero='99817349D', nacionalidad='alemana', cliente=c3)

    c4 = obtener_o_crear(Cliente, nombre='Jairo', apellido='Rabal', email='jarabal33@algo.com')
    p4 = obtener_o_crear(Pasaporte, numero='33973625A', nacionalidad='boliviana', cliente=c4)

    #db.session.add_all([cliente1, cliente2, cliente3, cliente4])  # se añaden a la base datos

    #db.session.commit()  # y guardar, no ncesario ya lo hace obtener_o_crear()
    print('...CLIENTES AÑADIDOS CORRECTAMENTE')


#-----------------------------------------------------------------------------------------------------
#Nivel 3 (La Unión): Crear la Reserva (uniendo Cliente y Viaje).
#relacion N:N, Un Cliente hace muchas reservas de viajes, y un Viaje recibe muchas reservas de clientes.
# La tabla Reserva es el puente.
def crear_reserva(): #fecha_reserva, cliente y viaje
    print('>>> GENERANDO RESERVAS')
    cliente1 = db.session.query(Cliente).filter_by(nombre='Pascal').first() #se busca cliente
    viaje1 = db.session.query(Viaje).filter_by(titulo='SPQR').first() #y viaje
    reserva1 = obtener_o_crear(Reserva, fecha_reserva=date(2026, 8, 22), cliente=cliente1, viaje=viaje1) #para juntarse en una reserva
    #db.session.add(reserva1)

    cliente2 = db.session.query(Cliente).filter_by(nombre='Pascal').first()
    viaje2 = db.session.query(Viaje).filter_by(titulo='The Sunny Sol').first()
    reserva2 = obtener_o_crear(Reserva, fecha_reserva=date(2026, 9, 22), cliente=cliente2, viaje=viaje2)

    cliente3 = db.session.query(Cliente).filter_by(nombre='Heinrik').first()
    viaje3 = db.session.query(Viaje).filter_by(titulo='SPQR').first()
    reserva3 = obtener_o_crear(Reserva, fecha_reserva=date(2024, 5, 2), cliente=cliente3, viaje=viaje3)

    cliente4 = db.session.query(Cliente).filter_by(nombre='Jairo').first()
    viaje4 = db.session.query(Viaje).filter_by(titulo='le Tour').first()
    reserva4 = obtener_o_crear(Reserva, fecha_reserva=date(2027, 3, 27), cliente=cliente4, viaje=viaje4)

    #db.session.commit()  # y guardar, add y commit ya lo hace obtener_o_crear()
    print('...RESERVAS AÑADIDAS')


# MOSTRAR-VER
def listar_reservas():
    print('\n>>> LISTADO DE RESERVAS EXISTENTES:')
    todas_las_reservas = db.session.query(Reserva).all()  # all() da lista con todas las reservas

    for reserva in todas_las_reservas:
        print(reserva)

#defs auxiliares para la def crear_nueva_reserva(), antes lo meti en ella y era spagueti
def solicitar_fecha():
    while True:
        fecha_viaje = input('Selecione una fecha (DD/MM/AAAA): ...0 para salir').strip().replace('-', '/')
        if fecha_viaje == '0': #opción de salida
            print('...saliendo de "solicitar fechae"')
            return None
        try:
            fecha_reserva = datetime.strptime(fecha_viaje, "%d/%m/%Y")  # convertir a fecha date
            return fecha_reserva
        except ValueError:
            print(' !!! ocurrio un error con fecha, intentalo de nuevo, formato Día/Mes/Año')

def seleccionar_cliente():
    print('Seleccione un cliente:')
    lista_clientes = db.session.query(Cliente).all()  # da list de todos los clientes registrados
    if not lista_clientes: #si lista esa vacia
        print('no hay clientes registrados!')
        return None #sale de la def devuelve nada
    #si hay clientes en lista se procede
    for i, cliente in enumerate(lista_clientes, 1):  # 1 indica inicio del indice
        print(f"{i}. {cliente.nombre}, {cliente.apellido}")

    while True:
        cliente_seleccionado = input('elige el nº del Cliente (1, 2, 3, ...0 para salir): ').strip()
        if cliente_seleccionado == '0': #opción de salida
            print('...saliendo de "selecionar cliente"')
            return None
        try:
            if cliente_seleccionado.isdigit():  # si es numero
                cliente_seleccionado = int(cliente_seleccionado)  # se formatea
                if cliente_seleccionado > 0 and cliente_seleccionado <= len(lista_clientes):
                    indice_real = cliente_seleccionado - 1  # esto para comensar el indice real base 0
                    cliente_final = lista_clientes[indice_real]  # asignar el objeto de la lista a una variable
                    return cliente_final
                else:
                    print("solo los números de los clientes disponibles")  # si se escribe fuera de rango
            else:
                print("Solo intruduca números, por favor")  # si se meten letras u otra cosa
        except ValueError:
            print('!!! ocurrio un error, intentalo de nuevo')


def seleccionar_viaje():
    print('Seleccione uno de los Viajes:')
    lista_viajes = db.session.query(Viaje).filter_by(disponible=True).all()
    if not lista_viajes: #si lista esa vacia
        print('no hay viajes registrados!')
        return None #sale de la def devuelve nada
    #si hay viajes en lista se procede
    for i, viaje in enumerate(lista_viajes, 1):
        print(f"{i}. {viaje.titulo} --> {viaje.destino}")

    while True:
        viaje_seleccionado = input('elige el nº del Viaje (1, 2, 3, ...0 para salir): ').strip()
        if viaje_seleccionado == '0': #opción de salida
            print('...saliendo de "selecionar viaje"')
            return None
        try:
            if viaje_seleccionado.isdigit():  # si es numero
                viaje_seleccionado = int(viaje_seleccionado)  # se formatea
                if viaje_seleccionado > 0 and viaje_seleccionado <= len(lista_viajes):
                    indice_real = viaje_seleccionado - 1  # esto para comensar el indice real base 0
                    viaje_final = lista_viajes[indice_real]  # asignar el objeto de la lista a una variable
                    return viaje_final

                else:
                    print("solo los números de los viajes disponibles")  # si se escribe fuera de rango
            else:
                print("Solo intruduca números, por favor")  # si se meten letras u otra cosa
        except ValueError:
            print('!!! ocurrio un error, intentalo de nuevo')



def crear_nueva_reserva(): #primero buscar-selec cliente, luego viaje
    print('\nPara registrar un NUEVA RESERVA introduzca los sigueintes datos:')

    cliente_final = seleccionar_cliente() #se selecciona cliente
    if cliente_final == None:
        print('no hay cliente seleccionado')
        return None

    viaje_final = seleccionar_viaje() #se selecciona viaje
    if viaje_final == None:
        print('no hay Viaje seleccionado')
        return None

    fecha_reserva = solicitar_fecha() #se llama a def y se genera fecha valida
    if fecha_reserva == None:
        print('no hay fecha seleccionada')
        return None

    #instacia de objeto Reserva
    nueva_reserva = Reserva(fecha_reserva=fecha_reserva, cliente=cliente_final, viaje=viaje_final)
    db.session.add(nueva_reserva)
    db.session.commit()  # y guardamos!!!
    print(f'Reserva número {nueva_reserva.id} creada con éxito!')




def ver_viajes():
    print('\n>>> CATÁLOGO VIAJES:')
    catalogo_viajes = db.session.query(Viaje).all()

    for viaje in catalogo_viajes:
        if viaje.disponible == False:
            print('X ¡No disponible! X: ', viaje)
        else:
            print('\t-', viaje)


def crear_viaje_nuevo():
    print('>>> CREANDO NUEVO VIAJE')
    nombre_destino = input('Nombre del destino (ej. Paris): ').capitalize()
    #buscar si ya existe un destino con ese nombre
    posible_destino = db.session.query(Destino).filter_by(nombre=nombre_destino).first()

    if not posible_destino: #si no esta ya en la lista de destinos, es un lugar nuevo
        nombre_pais = input('Nombre del pais del destino (ej. Francia): ').capitalize()
        nuevo_destino = Destino(nombre=nombre_destino, pais=nombre_pais)

        #db.session.add(nuevo_destino)ESTO AQUI NO, lo pase abajo
        destino_final = nuevo_destino
        print(f"Se ha creado el nuevo destino: {nombre_destino}")
    else:
        destino_final = posible_destino
        print(f"Destino encontrado: {nombre_destino}")

    print('Elige el Guia turistico por idioma: ')
    posible_guia = db.session.query(GuiaTuristico).all() #lista completa de guías
    for i, guia in enumerate(posible_guia, 1):  #1 indica inicio del index
        print(f"{i}. {guia.nombre} - {guia.idioma}")

    guia_seleccionado = input('elige el nº del guia (1, 2, 3, ...): ').strip()
    if guia_seleccionado.isdigit(): # si es numero
        guia_seleccionado = int(guia_seleccionado) #se formatea
        #y si es mayo 0 y uno de los nº de la lista
        if guia_seleccionado > 0 and guia_seleccionado <= len(posible_guia):
            indice_real = guia_seleccionado - 1 #esto para comensar el indice real base 0
            guia_final = posible_guia[indice_real] #asignar el objeto de la lista a una variable
            #no necesario add, se elige entre los que ya hay

            # pedir titulo del viaje
            nuevo_titulo = input('por ultimo pon TITULO al viaje: ').title().strip()

            #Instanciar clase Viaje con los datos
            nuevo_viaje = Viaje(titulo=nuevo_titulo, disponible=True, destino=destino_final, guia=guia_final)

            db.session.add(destino_final) #se añaden si esta bien lo de mas
            db.session.add(nuevo_viaje)
            db.session.commit()  # y guardamos!!!

        else:
            print("solo los números de los guias disponibles") #si se escribe fuera de rango
    else:
        print("Solo intruduca números, por favor")  #si se meten letras u otra cosa




def ver_clientes():
    print('\n>>> CLIENTES REGISTRADOS:')
    todos_los_clientes = db.session.query(Cliente).all()

    for cliente in todos_los_clientes:
        print('\t-', cliente)


def crear_cliente_completo(): #dar de alta a cliente
    print('--> añadiendo cliente, introduzca sus datos:') # hay que pedir args de class Pasaporte y Cliente

    nacionalidad = input('-Escriba la NACIONALIDAD del cliente: ').strip()#1º objeto hijo Pasaporte
    num_pasaporte = input('-Escriba el Nº de PASAPORTE del cliente: ').strip()
    nuevo_pasaporte = Pasaporte(numero=num_pasaporte, nacionalidad=nacionalidad) #se crea el pasaporte, luego se pasa a cliente

    nombre = input('-Escriba el NOMBRE del cliente: ').strip() #despeus ojteto cliente
    apellido = input('-Escriba el APELLIDO del cliente: ').strip()
    email = input('-Escriba el e-mail del cliente: ').strip()

    nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, email=email, documento=nuevo_pasaporte) #se crea obj
    #como pasar el obj a la bbdd:
    db.session.add(nuevo_cliente)  #tb se podria hacer directamente aki: db.session.add(Persona(nombre, edad)
    db.session.commit() #y guardamos!!!
    print('CLIENTE AÑADIDO CORRECTAMENTE!')




# UPPDATE, editar-actualizar
def editar_email_cliente():
    cliente_id = int(input('escribe el id del cliente a EDITAR: '))
    # filtramos pedimos a la bbdd y k de el objeto Persona, filter_by(col=lo k buscas) filtra x 1a colum concreta
    cliente = db.session.query(Cliente).filter_by(id=cliente_id).first()  # .first() se queda el 1º
    # print(cliente) #esto muestra el __str__ de Cliente
    if cliente:  # si el cliente existe, se cambia el email
        print(f'persona encontrada: {cliente.nombre}')
        nuevo_email = input('introduce el nuevo email de la persona: (en blanco para no cambiar)')

        if nuevo_email:  # si el nuevo str existe, se sustituye, sino nada
            cliente.email = nuevo_email

        db.session.commit()  # y guardamos-actualizamos!!!
        print('Email de cliente editado OK')
    else:
        print('no se encontró a la persona con ese ID')


# DELETE, eliminar
# gracias al relationship(back_populates='cliente', uselist=False, cascade="all, delete-orphan") al borrar...
# cliente se borran su documento y reservas asociados a el (eso esta en models en su clase)
def eliminar_cliente():  # al eliminar tb se elimina el id
    cliente_id = int(input('escribe el id del cliente a EDITAR: '))
    # filtramos pedimos a la bbdd y k de el objeto Persona, filter_by(col=lo k buscas) filtra x 1a colum concreta
    cliente = db.session.query(Cliente).filter_by(id=cliente_id).first()
    if cliente:  # si el cliente existe, se procede a eliminar
        print(f'persona encontrada: {cliente.nombre}')
        db.session.delete(cliente)  # Eliminado cliente
        db.session.commit()  # y guardamos-actualizamos!!!
        print('persona eliminada!')
    else:
        print('no se encontro a cliente con ese ID')



if __name__ == '__main__':
    print('--->>>>> *** ·Bienvenido al sistema de AGENCIA DE VIAJES· *** <<<<<---')

    # si existe bbdd BORRA, sino nada !!! SE DEBERIA DE BORRAR/COEMNTAR EL drop_all()
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)  # ...fuerza borrado de bbdd al ppio ejecutar
    # se crea bbdd, si ya esta no hace nada
    db.Base.metadata.create_all(bind=db.engine)  # esto crea la BBDD atraves del conector(engine)
    # si ya estaba creada no hace nada; para puebas mejor borrar y crearla de nuevo ...

    #llamado a las funciones, de CREAR datos
    #primero se cargan datos: OJO DEBEN SER LLAMADAS EN ESTE ORDEN

    cargar_catalogo() #(Cimientos). anyadir_destinos() y anyadir_guias()
    crear_viajes() #(Estructura).
    crear_clientes() #(Habitantes).
    crear_reserva() #(Acción).

    print('··· DATOS CARGADOS ···')

    print("\n" + "=" * 30)
    print("   AGENCIA DE VIAJES - MENÚ")
    print("=" * 30)

    #MENU, dict: listar_reservas(), ver_viajes(), ver_clientes(), editar_email_cliente(), eliminar_cliente()
    opciones = {
        1: listar_reservas,
        2: crear_nueva_reserva,
        3: ver_viajes,
        4: crear_viaje_nuevo,
        5: ver_clientes,
        6: crear_cliente_completo,
        7: editar_email_cliente,
        8: eliminar_cliente

    }
    #mostramos menu y entramos en loop while true
    while True:

        print("1. ver Reservas\n"
              "2. Crear nueva Reserva\n"
              "3. ver Viajes\n"
              "4. Crear nuevo Viaje\n"
              "5. ver Clientes Registrados\n"
              "6. Crear Cliente\n"
              "7. Editar email de cliente\n"
              "8. Eliminar Cliente\n"
              "9. Salir\n")

        try:
        #se elige opcion
            opcion = int(input("elije una opcion (1-9)"))
            if opcion == 9:
                print('...Saliendo, HASTA OTRA.')
                sys.exit() #SALIDA

            funcion = opciones.get(opcion) #funcion ES una REFERENCIA del dict opciones se le pide la opcion(input) y
            #opciones.get(opcion) devuelve la funcion elegida, DEFS se hacen antes del if main
            funcion() #es como que le pone los () al valor elegido del dict k pasa a ser def. INVOCA

        except ValueError:
            print('solo numeros entre 1 y 9')
        except TypeError:
            print('funcion no valida')
        except Exception as e:
            print(f'ocurrio un error {e}')


