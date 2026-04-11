import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Tareas")
        self.geometry("900x600")

        self.frame_actual = None
        self.mostrar_inicio()

    def limpiar_frame(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    def mostrar_inicio(self):
        self.limpiar_frame()
        self.frame_actual = PantallaInicio(self)
        self.frame_actual.pack(expand=True, fill="both")


class PantallaInicio(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Sistema de Tareas", font=("Arial", 30)).pack(pady=40)

        ctk.CTkButton(self, text="Ingresar como Estudiante").pack(pady=10)
        ctk.CTkButton(self, text="Ingresar como Docente").pack(pady=10)

        ctk.CTkButton(self, text="Admin", width=80).pack(side="bottom", pady=10)


app = App()
app.mainloop()