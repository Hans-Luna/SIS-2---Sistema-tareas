import customtkinter as ctk
from tkinter import messagebox
from conexion import conectar
import os
from pantallas_paneles import CrearCurso
from pantallas_paneles import CrearTarea
from pantallas_paneles import VerTareas
from pantallas_paneles import EntregarTarea
from pantallas_paneles import MisEntregas
from funciones_paneles import (
    crear_curso,
    crear_tarea,
    ver_tareas,
    entregar_tarea
)
from pantallas_paneles import (
    SeleccionarCursoCalificar,
    ListaTareasCalificar,
    ListaEntregas,
    CalificarEntrega
)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ADMIN_PASSWORD = "admin123"




class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Tareas")
        self.geometry("900x600")
        self.usuario_actual = None
        self.frame_actual = None
        self.mostrar_inicio()
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def limpiar_frame(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    def mostrar_inicio(self):
        self.limpiar_frame()
        self.frame_actual = PantallaInicio(self)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_login(self, tipo):
        self.limpiar_frame()
        self.frame_actual = Login(self, tipo)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_panel(self, tipo):
        self.limpiar_frame()

        if tipo == "estudiante":
            self.frame_actual = PanelEstudiante(self)

        elif tipo == "docente":
            self.frame_actual = PanelDocente(self)

        elif tipo == "admin":
            self.frame_actual = PanelAdmin(self)

        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_crear_curso(self):
        self.limpiar_frame()
        self.frame_actual = CrearCurso(self)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_crear_tarea(self):
        self.limpiar_frame()        
        self.frame_actual = CrearTarea(self)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_ver_tareas(self):
        self.limpiar_frame()        
        self.frame_actual = VerTareas(self)
        self.frame_actual.pack(expand=True, fill="both")
    
    def mostrar_entregar_tarea(self):
        self.limpiar_frame()     
        self.frame_actual = EntregarTarea(self)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_calificar_curso(self):
        self.limpiar_frame()
        self.frame_actual = SeleccionarCursoCalificar(self)
        self.frame_actual.pack(expand=True, fill="both")

    def mostrar_tareas_calificar(self, id_curso):
        self.limpiar_frame()
        self.frame_actual = ListaTareasCalificar(self, id_curso)
        self.frame_actual.pack(expand=True, fill="both")
    
    def mostrar_entregas(self, id_tarea):
        self.limpiar_frame()
        self.frame_actual = ListaEntregas(self, id_tarea)
        self.frame_actual.pack(expand=True, fill="both")


    def mostrar_calificar(self, id_entrega, id_tarea):
        self.limpiar_frame()
        self.frame_actual = CalificarEntrega(self, id_entrega, id_tarea)
        self.frame_actual.pack(expand=True, fill="both")
    
    def al_cerrar(self):
        limpiar_temporales()
        self.destroy()

    def mostrar_mis_entregas(self):
        self.limpiar_frame()
        self.frame_actual = MisEntregas(self)
        self.frame_actual.pack(expand=True, fill="both")


class PantallaInicio(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Sistema de Tareas", font=("Arial", 30)).pack(pady=40)

        ctk.CTkButton(self, text="Ingresar como Estudiante", command=lambda: master.mostrar_login("estudiante")).pack(pady=10)

        ctk.CTkButton(self, text="Ingresar como Docente", command=lambda: master.mostrar_login("docente")).pack(pady=10)

        ctk.CTkButton(self, text="Admin", width=80, command=lambda: master.mostrar_login("admin")).pack(side="bottom", pady=10)




class Login(ctk.CTkFrame):
    def __init__(self, master, tipo):
        super().__init__(master)
        self.tipo = tipo

        ctk.CTkLabel(self, text=f"Login ({tipo})", font=("Arial", 25)).pack(pady=20)

        if tipo == "admin":
            self.password = ctk.CTkEntry(self, placeholder_text="Contraseña Admin", show="*")
            self.password.pack(pady=10)
        else:
            self.email = ctk.CTkEntry(self, placeholder_text="Email")
            self.email.pack(pady=10)

            self.password = ctk.CTkEntry(self, placeholder_text="CI", show="*")
            self.password.pack(pady=10)

        ctk.CTkButton(self, text="Ingresar", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Volver", command=master.mostrar_inicio).pack(pady=5)

    def login(self):

       
        if self.tipo == "admin":
            if self.password.get() == ADMIN_PASSWORD:
                self.master.mostrar_panel("admin")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")

        
        else:
            email = self.email.get()
            password = self.password.get()

            if not email or not password:
                messagebox.showerror("Error", "Completa todos los campos")
                return

            conexion = conectar()
            if conexion is None:
                messagebox.showerror("Error", "Error de conexión")
                return

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT * FROM usuario
                WHERE email=%s AND CI_usuario=%s AND tipo=%s
            """, (email, password, self.tipo))

            resultado = cursor.fetchone()

            if resultado:
                self.master.usuario_actual = resultado 
                self.master.mostrar_panel(self.tipo)
            conexion.close()

            if resultado:
                self.master.mostrar_panel(self.tipo)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")




class PanelEstudiante(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Mis tareas", font=("Arial", 25)).pack(pady=20)

        ctk.CTkButton(self, text="Ver tareas", command=master.mostrar_ver_tareas).pack(pady=10)
        ctk.CTkButton(self, text="Entregar tarea", command=master.mostrar_entregar_tarea).pack(pady=10)
        ctk.CTkButton(self, text="Mis entregas", command=self.master.mostrar_mis_entregas).pack(pady=10)
        ctk.CTkButton(self, text="Cerrar sesión", command=master.mostrar_inicio).pack(side="bottom", pady=10)
        




class PanelDocente(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Gestión de cursos", font=("Arial", 25)).pack(pady=20)

        ctk.CTkButton(self, text="Crear curso", command=master.mostrar_crear_curso).pack(pady=10)
        ctk.CTkButton(self, text="Crear tarea", command=master.mostrar_crear_tarea).pack(pady=10)
        ctk.CTkButton(self, text="Calificar tareas", command=master.mostrar_calificar_curso).pack(pady=10)
        ctk.CTkButton(self, text="Cerrar sesión", command=master.mostrar_inicio).pack(side="bottom", pady=10)




class PanelAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Panel Administrador", font=("Arial", 25)).pack(pady=20)

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.nombre.pack(pady=5)

        self.email = ctk.CTkEntry(self, placeholder_text="Email")
        self.email.pack(pady=5)

        self.ci = ctk.CTkEntry(self, placeholder_text="CI")
        self.ci.pack(pady=5)

        self.tipo = ctk.CTkOptionMenu(self, values=["estudiante", "docente"])
        self.tipo.pack(pady=5)

        ctk.CTkButton(self, text="Crear usuario", command=self.crear_usuario).pack(pady=10)

        
        ctk.CTkButton(self, text="Cerrar sesión", command=master.mostrar_inicio).pack(side="bottom", pady=10)

    def crear_usuario(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuario (nombre, email, CI_usuario, tipo)
            VALUES (%s, %s, %s, %s)
        """, (
            self.nombre.get(),
            self.email.get(),
            self.ci.get(),
            self.tipo.get()
        ))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Usuario creado")

def limpiar_temporales():
    for archivo in os.listdir():
        if archivo.startswith("temp_"):
            try:
                os.remove(archivo)
            except:
                pass




app = App()
app.mainloop()