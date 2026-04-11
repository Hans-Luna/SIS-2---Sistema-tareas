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
    messagebox.showinfo("Info", "Función ver tareas (pendiente)")


def entregar_tarea():
    messagebox.showinfo("Info", "Función entregar tarea (pendiente)")