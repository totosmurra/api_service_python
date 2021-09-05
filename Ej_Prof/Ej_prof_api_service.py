from re import S
import traceback
import io
import sys
import os
import base64
import json
import requests
from datetime import datetime, timedelta

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import user
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, session, sessionmaker, relationship

from sqlalchemy import func

from ntpath import join
from os import name

import sqlite3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

engine = sqlalchemy.create_engine("sqlite:///Ej_prof_api_service.db")
base = declarative_base()


class Usuarios(base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=true)
    userId = Column(Integer)
    title = Column(String)
    completed = Column(String)


def clear():

    base.metadata.drop_all(engine)


    base.metadata.create_all(engine)

def fill():
    
    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data = response.json()

    Session = sessionmaker(bind=engine)
    session = Session()
    
    for i in data:
        entry = Usuarios(id = i["id"], userId = i["userId"], title = i["title"], completed = i["completed"])

        session.add(entry)

    session.commit()



def title_completed_count(userId):

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Usuarios).filter(Usuarios.userId == userId).filter(Usuarios.completed == 1).count()

    return (query)



def graph():

    Session = sessionmaker(bind=engine)
    session = Session()

    listadeids = [1,2,3,4,5,6,7,8,9,10]
    listadecompleted = []

    for i in listadeids:
        query = session.query(Usuarios).filter(Usuarios.userId == i).filter(Usuarios.completed == 1).count()

        listadecompleted.append(query)
    
    fig = Figure(figsize=(15,7))
    fig.tight_layout()

    ax = fig.add_subplot()

    ax.bar(listadeids, listadecompleted)
    ax.legend()
    ax.grid()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
        
    return Response(output.getvalue(), mimetype='image/png')


def titles():
    Session = sessionmaker(bind=engine)
    session = Session()

    listadeids = [1,2,3,4,5,6,7,8,9,10]
    listadecompleted = []
    jsonarchivo = []


    for i in listadeids:
        query = session.query(Usuarios).filter(Usuarios.userId == i).filter(Usuarios.completed == 1).count()

        listadecompleted.append(query)

        qwerty = {i:query}

        jsonarchivo.append(qwerty)
    
    return jsonarchivo

    
    
