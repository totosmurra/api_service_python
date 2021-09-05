import traceback
import io
import sys
import os
import base64
import json
from datetime import datetime, timedelta

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
from sqlalchemy.orm import query
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

from Ej_prof_api_service import db
import Ej_prof_api_service

from config import config

app = Flask(__name__)

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"
# Asociamos nuestro controlador de la base de datos con la aplicacion
db.init_app(app)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>/clearfill para reiniciar la tabla</h3>"
        result += "<h3>[GET] /user/{id}/titles para obtener datos especificos de un id</h3>"
        result += "<h3>[GET] /user/graph para ver un grafico de la cantidad de ids que completaron</h3>"
        result += "<h3>[GET] /user/titles para ver el total de usuarios que lo completaros</h3>"
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/clearfill")
def reset():
    try:
        # Borrar y crear la base de datos
        Ej_prof_api_service.clear()
        Ej_prof_api_service.fill()
        result = "<h3>Base de datos re-generada!"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/user/<id>/titles")
def user_id_titles(id):
    try:

        userId = id

        datarda = Ej_prof_api_service.title_completed_count(userId)

        result = "<h3>El usuario {} completo {}</h3>".format(id, datarda)

        return (result)

    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/user/graph")
def graph():
    try:
        return Ej_prof_api_service.graph()
    
    except:
        return jsonify({'trace': traceback.format_exc()})



@app.route("/user/titles")
def titlesss():
    try:
        rar = Ej_prof_api_service.titles()

        rar = str(rar)

        result = "<h3>Estos son los ids que completaron</h3>"
        result += "<h3>{}</h3>".format(rar)

        return result
    except:
        return jsonify({'trace': traceback.format_exc()})



if __name__ == '__main__':
    print('Servidor arriba!')

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)