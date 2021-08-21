#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.2

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.2"


import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func

import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import base64
import io


from collections import OrderedDict

from flask_sqlalchemy import SQLAlchemy

from flask import Response

db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    age = db.Column(Integer)
    nationality = db.Column(String)
    
    def __repr__(self):
        return f"Persona:{self.name} con nacionalidad {self.nacionalidad}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(name, age, nationality):
    # Crear una nueva persona
    person = Persona(name=name, age=age, nationality=nationality)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las personas
    query = db.session.query(Persona)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'name': person.name, 'age': person.age, 'nationality': person.nationality}
        json_result_list.append(json_result)

    return json_result_list

def nationality_review():
    
    query = db.session.query(Persona)
    
    fig = Figure(figsize=(15,7))
    fig.tight_layout()
    
    ax = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
   

    lista_nacionalidadesx = [x.nationality for x in query]
    lista_ids = [x.id for x in query]
    lista_edades = [x.age for x in query]
    lista_nacionalidades = list(OrderedDict.fromkeys(lista_nacionalidadesx))
    lenlist = int(len(lista_ids)+1)
    
    numlist = []
    for x in lista_nacionalidades:
        numlist.append(lista_nacionalidadesx.count(x))

    ax.set_title("Nacionalidades",fontsize=20)
    ax.pie(numlist,labels = lista_nacionalidades,autopct='%1.1f%%',shadow=True)
    ax.axis('equal')


    ax2.scatter(lista_ids, lista_edades, c='darkred')
    ax2.legend()
    ax2.grid()
    ax2.set_xlabel('Ids')
    ax2.set_ylabel('Edad')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
        
    return Response(output.getvalue(), mimetype='image/png')
    

    