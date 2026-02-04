#CLASES y OBJETOS
#from db (el nombre de tu archivo) import Base (la herramienta que creaste dentro)
from datetime import date

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship, mapped_column, Mapped

import db
#nota: podria ser asi > from db import Base ...class Destino(Base): lo dejo asi x claridad de ver donde sale Base

# NOTA!!!: comento los __init__ manual para no perder la flexibilidad de SQLAlchemy.
# SQLAlchemy ya incluye un constructor init por defecto que acepta cualquier combinación
# de argumentos 'kwargs' y gestiona automaticamente las claves foraneas (IDs)
# cuando le paso los objetos completos.

#CLASES, x cada class una tabla (__tablename__):
class Destino(db.Base):
    __tablename__ = 'destinos'  # se pone nombre a la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Tabla con los destinos'
    }  # esto siempre toda tabla tiene nombre, id tb (autoincrement)

    # EL MAPEO, (NOMBRES de las COLUMNAS), tipo de dato, sera PK
    # se tienen que LLAMAR IGUAL QUE ATRIBUTOS CLASE
    #                                     'Integer' en lenguaje SQLalchemy, orm que luego traduce a la bbdd k sea
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # nullable False > evitar datos nulos
    pais: Mapped[str] = mapped_column(String(50), nullable=False)
    # mapped_column se encarga de pasar al lenguaje de la bbdd que se tenga
    viajes: Mapped[list["Viaje"]] = relationship(back_populates="destino")

    #def __init__(self, nombre, pais):
     #   self.nombre = nombre
      #  self.pais = pais

    def __repr__(self): #esto muestra LISTAS de OBJETOS [destino1,destino2,destino3]
        return f'El destino--> ID: {self.id}, nombre: {self.nombre}, país: {self.pais}'

    def __str__(self): #esto muestra UN solo objeto
        return f'El destino--> ID: {self.id}, nombre: {self.nombre}, país: {self.pais}'
        #el id lo crea la bbdd



class GuiaTuristico(db.Base): #otro atributo UBICACION? conectado con lugar DESTINO?? edad irrelevante?
    __tablename__ = 'guias_turisticos'  # se pone nombre a la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Tabla de guias turisticos'
    }  # esto siempre toda tabla tiene nombre, id tb (autoincrement)

    # EL MAPEO, (NOMBRES de las COLUMNAS), tipo de dato, sera PK, se tienen que LLAMAR IGUAL QUE ATRIBUTOS CLASs
    #                              'Integer' en lenguaje SQLalchemy, orm
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # nullable False > evitar datos nulos
    idioma: Mapped[str] = mapped_column(String(100), nullable=False)
    #                     mapped_column se encarga de pasar al lenguaje de la bbdd que se tenga

    viajes: Mapped[list["Viaje"]] = relationship(back_populates="guia")

#nota: se ve __init__ se genera automáticamente, no es estrictamente necesario...igual lo dejo
    #def __init__(self, nombre, idioma):
     #   self.nombre = nombre
      #  self.idioma = idioma

    def __repr__(self): #esto muestra LISTAS de OBJETOS
        return f'Guia turistico--> ID: {self.id}, nombre: {self.nombre}, idiomas: {self.idioma}'

    def __str__(self): #esto muestra UN solo objeto
        return f'Guia turistico--> ID: {self.id}, nombre: {self.nombre}, idiomas: {self.idioma}'
        #el id lo crea la bbdd



class Cliente(db.Base):
    __tablename__ = 'clientes'  # se pone nombre a la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Tabla de clientes registrados'
    }
    # EL MAPEO, (NOMBRES de las COLUMNAS)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # nullable False > evitar datos nulos
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)

    documento: Mapped['Pasaporte'] = relationship(back_populates='cliente', uselist=False, cascade="all, delete-orphan")
    # es una RELACIÓN. NO ES COLUMNA, es un objeto de "Pasaporte", back_populates busca cliente en Pasaporte
    #uselist=False para que de SOLO UNO, solo un objeto pasaporte, relacion 1:1(1client:1documento: cliente.documento.numero)
    #cascade="all, delete-orphan" es para que al eliminar un cliente tb se eliminen sus datos asociados, aqui su documento, abajo su reserva
    reservas: Mapped[list["Reserva"]] = relationship(back_populates="cliente", cascade="all, delete-orphan") #coenxion a Reservas


    #def __init__(self, nombre, apellido, email, documento):
     #   self.nombre = nombre
      #  self.apellido = apellido
       # self.email = email
        #self.documento = documento

    def __repr__(self): #esto muestra LISTAS de OBJETOS
        return f'Cliente--> ID: {self.id}, nombre: {self.nombre}, apellido: {self.apellido}, email: {self.email}'

    def __str__(self): #esto muestra UN solo objeto
        return f'Cliente--> ID: {self.id}, nombre: {self.nombre}, apellido: {self.apellido}, email: {self.email}'



class Pasaporte(db.Base):
    __tablename__ = 'pasaportes'  # se pone nombre a la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Tabla de nº de pasaportes registrados'
    }
    # EL MAPEO, (NOMBRES de las COLUMNAS) > Nº PASAPORTE STR(casos alfanum o empiecen en 0)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero: Mapped[str] = mapped_column(String(50), nullable=False)  # nullable False > evitar datos nulos
    nacionalidad: Mapped[str] = mapped_column(String(50), nullable=False)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'))
    #la PK de pasaporte se vincula con pk de cliente con ForeignKey('nombretabla.nombrecolumna')

    cliente: Mapped['Cliente'] = relationship(back_populates='documento')
    #es una RELACIÓN. NO ES COLUMNA, es un objeto de "Cliente", back_populates busca pasaporte en Cliente
#Cliente.documento <---> apunta a <---> Pasaporte.cliente
#Pasaporte.cliente <---> apunta a <---> Cliente.documento
    #-podria ir tb fecha de validez...pero lo dejo asi para no complicarlo mas


    #def __init__(self, numero, nacionalidad, cliente_id, cliente):
     #   self.numero = numero
      #  self.nacionalidad = nacionalidad
       # self.cliente_id = cliente_id
        #self.cliente = cliente

    def __repr__(self):  # esto muestra LISTAS de OBJETOS
        return f'Pasaporte--> ID: {self.id}-{self.cliente}, nº: {self.numero}, nacionalidad: {self.nacionalidad}'

    def __str__(self):  # esto muestra UN solo objeto
        return f'Pasaporte--> ID: {self.id}-{self.cliente}, nº: {self.numero}, nacionalidad: {self.nacionalidad}'
#deberia decir de QUIEN es, por eso se vincula el id en cliente_id



class Viaje(db.Base): #es PRODUCTO O PAQUETE
    __tablename__ = 'viajes'  # se pone nombre a la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Viajes disponibles'
    }  # esto siempre toda tabla tiene nombre, id tb (autoincrement)

    # EL MAPEO, (NOMBRES de las COLUMNAS)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] =mapped_column(String(50), nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)#dato BOOL

    #conexion 1:N (Uno a Muchos)
    #CONEXIÓN 1: DESTINO...Foreign Keys apuntan a tabla.col y back_populates a atributo de clase
    destino_id: Mapped[int] = mapped_column(Integer, ForeignKey('destinos.id'))
    destino: Mapped['Destino'] = relationship(back_populates= 'viajes')#apunta a la Clase Destino > viajes

    #CONEXIÓN 2: GUÍATruristico
    guia_id: Mapped[int] = mapped_column(Integer, ForeignKey('guias_turisticos.id')) #apunta a guias_turisticos.id
    guia: Mapped["GuiaTuristico"] = relationship(back_populates="viajes") #Apunta a Clase GuiaTuristico>viajes

    # conexion a Reservas
    reservas: Mapped[list["Reserva"]] = relationship(back_populates="viaje")


    #def __init__(self, titulo, disponible, destino_id, destino, guia_id, guia):
        #self.titulo = titulo
        #self.disponible = disponible
        #self.destino_id = destino_id
        #self.destino = destino
        #self.guia_id = guia_id
        #self.guia = guia


    def __repr__(self):  #  muestra LISTAS de OBJETOS
        return f'''El viaje--> ID: {self.id}, nombre: {self.titulo}, 
        destino: {self.destino}, guiado por: {self.guia}, estado: {self.disponible}'''

    def __str__(self):  #  muestra UN solo objeto
        return f'''El viaje--> ID: {self.id}, nombre: {self.titulo}, 
             destino: {self.destino}, guiado por: {self.guia}, estado: {self.disponible}'''



#asi seria una Tabla de Asociación: NO un Objeto de Asociación que es lo necesario
#cliente_viaje = Table(
 #   'cliente_viaje',
  #  db.Base.metadata,
   # Column('cliente_id', ForeignKey('clientes.id'), primary_key=True),
    #Column('viaje_id', ForeignKey('viajes.id'), primary_key=True)
#)

#Objeto de Asociación:
class Reserva(db.Base): #conectamos Cliente y Viaje, Relación N:N (Muchos a Muchos)
    #Un Cliente puede hacer muchas reservas. Un Viaje puede ser reservado por muchos clientes.
    __tablename__ = 'reservas'  #nombre de la tabla, la clase SINGULAR, tabla plural minusculas
    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Resrvas realizadas'
    }  # esto siempre toda tabla tiene nombre, id tb (autoincrement)

    # EL MAPEO, (NOMBRES de las COLUMNAS)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_reserva: Mapped[date] = mapped_column(Date, nullable=False)#OJO AQUI datetimes COMPLICADO

    #conectamos Cliente y Viaje, Relación N:N (Muchos a Muchos)
    #Dos claves foráneas (una apuntando a clientes.id y otra a viajes.id).
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'))
    id_viaje: Mapped[int] = mapped_column(Integer, ForeignKey('viajes.id'))

    #Dos relaciones (para ver el objeto Cliente y el objeto Viaje).
    cliente: Mapped['Cliente'] = relationship(back_populates='reservas')
    viaje: Mapped['Viaje'] = relationship(back_populates='reservas')

    def __str__(self):
        return f'* Reserva--> ID: {self.id}, cliente: {self.cliente.nombre}, viaje: {self.viaje.titulo} ({self.fecha_reserva})'

    def __repr__(self):
        return f'* Reserva--> ID: {self.id}, cliente: {self.cliente.nombre}, viaje: {self.viaje.titulo} ({self.fecha_reserva})'

#nota: La clase Base (de la que heredan las class) no necesita un __init__,
# ella genera uno automático en segundo plano que acepta todos los nombres de columnas como argumentos.

#mi_reserva = Reserva(fecha_reserva=hoy, cliente=juan, viaje=paris)