import customtkinter as ctk
from tkinter import messagebox
from conexion import conectar
from funciones_paneles import crear_tarea
from datetime import datetime


class CrearCurso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Crear Curso", font=("Arial", 25)).pack(pady=20)

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre del curso")
        self.nombre.pack(pady=10)

        ctk.CTkButton(self, text="Guardar", command=self.guardar).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Volver",
            command=lambda: master.mostrar_panel("docente")
        ).pack(pady=10)

    def guardar(self): 
        nombre = self.nombre.get()

        if not nombre:
            messagebox.showerror("Error", "Ingrese nombre")
            return

        conexion = conectar()

        if conexion is None or not conexion.is_connected():
            messagebox.showerror("Error", "No hay conexión a la BD")
            return

        cursor = conexion.cursor()

        try:
            id_docente = self.master.usuario_actual[0]

            cursor.execute("""
                INSERT INTO curso (nombre_curso, id_docente)
                VALUES (%s, %s)
            """, (nombre, id_docente))

            conexion.commit()

            messagebox.showinfo("Éxito", "Curso creado")

            self.nombre.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear curso:\n{e}")

        finally:
            conexion.close()

class CrearTarea(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Crear Tarea", font=("Arial", 25)).pack(pady=20)

        self.titulo = ctk.CTkEntry(self, placeholder_text="Título")
        self.titulo.pack(pady=10)

        self.descripcion = ctk.CTkEntry(self, placeholder_text="Descripción")
        self.descripcion.pack(pady=10)

        self.fecha = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD")
        self.fecha.pack(pady=10)

        
        self.cursos_dict = self.cargar_cursos()
        self.combo_curso = ctk.CTkOptionMenu(self, values=list(self.cursos_dict.keys()))
        self.combo_curso.pack(pady=10)

        ctk.CTkButton(self, text="Guardar", command=self.guardar).pack(pady=15)

        ctk.CTkButton(self, text="Volver",
                      command=lambda: master.mostrar_panel("docente")).pack(pady=10)

    def cargar_cursos(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_curso, nombre_curso FROM curso")
        datos = cursor.fetchall()

        conexion.close()

        return {nombre: id for id, nombre in datos}

    def guardar(self):
        titulo = self.titulo.get()
        descripcion = self.descripcion.get()
        fecha = self.fecha.get()

        
        nombre_curso = self.combo_curso.get()
        id_curso = self.cursos_dict.get(nombre_curso)

        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida (YYYY-MM-DD)")
            return

        exito = crear_tarea(titulo, descripcion, fecha, id_curso)

        if exito:
            messagebox.showinfo("Éxito", "Tarea creada")

        
            self.titulo.delete(0, "end")
            self.descripcion.delete(0, "end")
            self.fecha.delete(0, "end")
