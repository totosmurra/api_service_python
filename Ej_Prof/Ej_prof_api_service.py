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
from sqlalchemy.orm import session, sessionmaker, relationship

from ntpath import join
from os import name

import sqlite3


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






