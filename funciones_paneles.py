from conexion import conectar
from tkinter import messagebox
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog
import os



def crear_curso():
    conexion = conectar()

    if conexion is None or not conexion.is_connected():
        messagebox.showerror("Error", "No hay conexión a la BD")
        return

    cursor = conexion.cursor()

    try:
        
        cursor.execute("INSERT INTO curso (nombre_curso, id_docente) VALUES (%s, %s)", (nombre, id_docente))
        conexion.commit()

        messagebox.showinfo("Éxito", "Curso creado")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear curso:\n{e}")

    finally:
        conexion.close()


def crear_tarea(titulo, descripcion, fecha_limite, id_curso):
    conexion = conectar()

    if conexion is None or not conexion.is_connected():
        messagebox.showerror("Error", "No hay conexión a la BD")
        return False

    cursor = conexion.cursor()

    try:
        if not titulo or not fecha_limite or not id_curso:
            messagebox.showerror("Error", "Campos obligatorios vacíos")
            return False

        cursor.execute("""
            INSERT INTO tarea (titulo, descripcion, fecha_limite, id_curso)
            VALUES (%s, %s, %s, %s)
        """, (titulo, descripcion, fecha_limite, id_curso))

        conexion.commit()
        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear tarea:\n{e}")
        return False

    finally:
        conexion.close()
    



def obtener_cursos_docente(id_docente):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_curso, nombre_curso FROM curso WHERE id_docente=%s",
        (id_docente,)
    )

    datos = cursor.fetchall()
    conexion.close()

    return datos


def obtener_tareas_por_curso(id_curso):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_tarea, titulo FROM tarea WHERE id_curso=%s",
        (id_curso,)
    )

    datos = cursor.fetchall()
    conexion.close()

    return datos


def obtener_entregas_por_tarea(id_tarea):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id_entrega, nombre_archivo, descripcion, id_usuario
    FROM entrega
    WHERE id_tarea=%s""", (id_tarea,))

    datos = cursor.fetchall()
    conexion.close()

    return datos


def guardar_calificacion(id_entrega, nota):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "UPDATE entrega SET nota=%s WHERE id_entrega=%s",
            (nota, id_entrega)
        )

        conexion.commit()
        return True

    except Exception:
        return False




def ver_tareas():
    conexion = conectar()

    if conexion is None or not conexion.is_connected():
        return None

    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT t.id_tarea, t.titulo, t.fecha_limite, c.nombre_curso
            FROM tarea t
            JOIN curso c ON t.id_curso = c.id_curso
        """)
        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        conexion.close()

def entregar_tarea(id_tarea, descripcion, ruta_archivo, id_usuario):
    conexion = conectar()

    if conexion is None or not conexion.is_connected():
        return False

    cursor = conexion.cursor()

    try:
        with open(ruta_archivo, "rb") as f:
            archivo_binario = f.read()

        nombre_archivo = os.path.basename(ruta_archivo)

        cursor.execute("""
            INSERT INTO entrega (archivo, nombre_archivo, descripcion, id_tarea, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (archivo_binario, nombre_archivo, descripcion, id_tarea, id_usuario))

        conexion.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        conexion.close()