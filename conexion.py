import mysql.connector
import os
import sys


def ruta_recurso(relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativa)
    return os.path.join(os.path.abspath("."), relativa)


def conectar():
    try:
        ssl_path = ruta_recurso("certificado/ca.pem")

        conexion = mysql.connector.connect(
            #host="host",
            #user="avnadmin",
            #port=18270,
            #password="password",
            #database="sistema_tareas",
            #ssl_ca=ssl_path
        )

        return conexion

    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None