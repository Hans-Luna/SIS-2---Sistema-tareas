import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess
from conexion import conectar
from funciones_paneles import crear_tarea
from funciones_paneles import ver_tareas
from funciones_paneles import entregar_tarea
from datetime import datetime
from funciones_paneles import (
    obtener_cursos_docente,
    obtener_tareas_por_curso,
    obtener_entregas_por_tarea,
    guardar_calificacion
)


class CrearCurso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Crear Curso", font=("Arial", 25)).pack(pady=20)

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre del curso")
        self.nombre.pack(pady=10)

        ctk.CTkButton(self, text="Guardar", command=self.guardar).pack(pady=10)

        ctk.CTkButton(self, text="Volver", command=lambda: master.mostrar_panel("docente")).pack(pady=10)

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

        ctk.CTkButton(self, text="Volver", ommand=lambda: master.mostrar_panel("docente")).pack(pady=10)

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

class VerTareas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Listado de Tareas", font=("Arial", 25)).pack(pady=20)

        tareas = ver_tareas()

        if not tareas:
            ctk.CTkLabel(self, text="No hay tareas disponibles").pack(pady=10)
        else:
            for t in tareas:
                texto = f"{t[1]} | Fecha: {t[2]} | Curso: {t[3]}"
                ctk.CTkLabel(self, text=texto).pack(anchor="w", padx=20)

        ctk.CTkButton(self, text="Volver", command=lambda: master.mostrar_panel("estudiante")).pack(pady=20)

class EntregarTarea(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.ruta_archivo = None
        self.label_archivo = ctk.CTkLabel(self, text="Archivo no seleccionado")
        self.label_archivo.pack(pady=5)

        ctk.CTkLabel(self, text="Entregar Tarea", font=("Arial", 25)).pack(pady=20)

        self.tareas_dict = self.cargar_tareas()

        self.combo_tarea = ctk.CTkOptionMenu(self, values=list(self.tareas_dict.keys()))
        self.combo_tarea.pack(pady=10)

        self.descripcion = ctk.CTkEntry(self, placeholder_text="Descripción")
        self.descripcion.pack(pady=10)

        
        ctk.CTkButton(self, text="Adjuntar archivo", command=self.seleccionar_archivo).pack(pady=10)

        
        self.label_archivo = ctk.CTkLabel(self, text="Ningún archivo seleccionado")
        self.label_archivo.pack(pady=5)

        ctk.CTkButton(self, text="Entregar", command=self.entregar).pack(pady=10)

        ctk.CTkButton(self, text="Volver", command=lambda: master.mostrar_panel("estudiante")).pack(pady=10)

    

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos", "*.pdf *.docx *.doc")]
        )
        if archivo:
            self.ruta_archivo = archivo

            nombre = os.path.basename(archivo)

        
            self.label_archivo.configure(text=f"Archivo: {nombre}")

    def cargar_tareas(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_tarea, titulo FROM tarea")
        datos = cursor.fetchall()

        conexion.close()

        return {titulo: id for id, titulo in datos}

    def entregar(self):
        nombre_tarea = self.combo_tarea.get()
        id_tarea = self.tareas_dict.get(nombre_tarea)

        if not self.ruta_archivo:
            messagebox.showerror("Error", "Debe adjuntar un archivo")
            return

        id_usuario = self.master.usuario_actual[0]

        descripcion = self.descripcion.get()

        exito = entregar_tarea(id_tarea, descripcion, self.ruta_archivo, id_usuario)

        if exito:
            messagebox.showinfo("Éxito", "Tarea entregada")


class SeleccionarCursoCalificar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Seleccionar Curso", font=("Arial", 25)).pack(pady=20)

        id_docente = master.usuario_actual[0]
        cursos = obtener_cursos_docente(id_docente)

        self.cursos_dict = {nombre: id for id, nombre in cursos}

        self.combo = ctk.CTkOptionMenu(self, values=list(self.cursos_dict.keys()))
        self.combo.pack(pady=10)

        ctk.CTkButton(self, text="Ver tareas", command=self.ver_tareas).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=lambda: master.mostrar_panel("docente")).pack(pady=20)
        


    def ver_tareas(self):
        id_curso = self.cursos_dict[self.combo.get()]
        self.master.mostrar_tareas_calificar(id_curso)

    
class ListaTareasCalificar(ctk.CTkFrame):
    def __init__(self, master, id_curso):
        super().__init__(master)

        ctk.CTkLabel(self, text="Tareas", font=("Arial", 25)).pack(pady=20)

        tareas = obtener_tareas_por_curso(id_curso)

        for id_tarea, titulo in tareas:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, fill="x", padx=20)

            ctk.CTkLabel(frame, text=titulo).pack(side="left")

            ctk.CTkButton(frame, text="Ver entregas", command=lambda i=id_tarea: master.mostrar_entregas(i)).pack(side="right")


class ListaEntregas(ctk.CTkFrame):
    def __init__(self, master, id_tarea):
        super().__init__(master)
        self.id_tarea = id_tarea
        ctk.CTkLabel(self, text="Entregas", font=("Arial", 25)).pack(pady=20)

        entregas = obtener_entregas_por_tarea(id_tarea)

        for id_entrega, nombre_archivo, descripcion, usuario in entregas:
            info = f"{usuario}\n{descripcion}\nArchivo: {nombre_archivo}"
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, fill="x", padx=20)

            info = f"{usuario}\n{descripcion}\nArchivo: {nombre_archivo}"
            ctk.CTkLabel(frame, text=info, justify="left").pack(side="left", padx=10)

            ctk.CTkButton(frame, text="Abrir", command=lambda i=id_entrega: self.abrir_archivo(i)).pack(side="right", padx=5)

            ctk.CTkButton(frame, text="Calificar", command=lambda i=id_entrega: master.mostrar_calificar(i, id_tarea)).pack(side="right", padx=5)
        
        ctk.CTkButton(self, text="Volver", command=master.mostrar_calificar_curso).pack(pady=10)

    def abrir_archivo(self, id_entrega):
        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT archivo, nombre_archivo 
                FROM entrega 
                WHERE id_entrega=%s
            """, (id_entrega,))

            resultado = cursor.fetchone()

        
            if not resultado:
                messagebox.showerror("Error", "No se encontró el archivo")
                return

            archivo_binario, nombre = resultado

            if not archivo_binario:
                messagebox.showerror("Error", "El archivo está vacío")
                return

            ruta_temp = f"temp_{nombre}"

            with open(ruta_temp, "wb") as f:
                f.write(archivo_binario)

        
            os.startfile(ruta_temp)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir:\n{e}")

        finally:
            conexion.close()


class CalificarEntrega(ctk.CTkFrame):
    def __init__(self, master, id_entrega, id_tarea):
        super().__init__(master)

        self.id_entrega = id_entrega
        self.id_tarea = id_tarea

        ctk.CTkLabel(self, text="Calificar", font=("Arial", 25)).pack(pady=20)

        self.nota = ctk.CTkEntry(self, placeholder_text="Nota")
        self.nota.pack(pady=10)

        ctk.CTkButton(self, text="Guardar", command=self.guardar).pack(pady=10)

        ctk.CTkButton(self, text="Volver", command=lambda: master.mostrar_entregas(self.id_tarea)).pack(pady=10)

    def guardar(self):
        nota = self.nota.get()

        if guardar_calificacion(self.id_entrega, nota):
            messagebox.showinfo("Éxito", "Nota guardada")
        else:
            messagebox.showerror("Error", "No se pudo guardar")

    