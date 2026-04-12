from conexion import conectar
from tkinter import messagebox
from datetime import datetime
import customtkinter as ctk




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
    



def calificar_tareas():
    messagebox.showinfo("Info", "Función calificar tareas (pendiente)")




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

def entregar_tarea(id_tarea, descripcion):
    conexion = conectar()

    if conexion is None or not conexion.is_connected():
        messagebox.showerror("Error", "No hay conexión a la BD")
        return False

    cursor = conexion.cursor()

    try:
        if not id_tarea:
            messagebox.showerror("Error", "Debe seleccionar una tarea")
            return False

        cursor.execute("""
            INSERT INTO entrega (id_tarea, descripcion)
            VALUES (%s, %s)
        """, (id_tarea, descripcion))

        conexion.commit()
        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo entregar tarea:\n{e}")
        return False

    finally:
        conexion.close()