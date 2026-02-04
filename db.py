#aqui configuracion de la BBDD, que tipo de bbdd se quiere? dialecto? la conexion?
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#1-conexion con SQLite3
engine = create_engine('sqlite:///database/agencia_viajes.db', echo=False) #echo muestra el proceso interno ORM
#dialecto(sqlite)///donde se guarda la bbdd (en directorio: database),
# el nombre de la base de datos agencia_viajes.db
#((si tuviera contraseña se pone aqui tb; echo True es para ver-debug las sentencias/INSTRUCCIONES SQL))

#2- session(objeto), con la conexion de la bbdd
Session = sessionmaker(bind=engine) #engine k es la conexion, Session es una clase
session = Session()

#3- DeclarativeBase para modelos, clase de la libreria bbdd, como nivel 1, es la que vincula a los objetos,
#las clases heredan de Base
class Base(DeclarativeBase):
    pass