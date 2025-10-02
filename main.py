"""
Clase AplicacionPrincipal:
1.- Se encuentra en main.py.
2.- Es la aplicación principal del sistema de inventario.
3.- Crea la ventana principal con información del estudiante y menú.
4.- Implementa atajo de teclado Escape para salir.
5.- Maneja la inicialización del inventario y la interfaz gráfica.
"""

import tkinter as tk  #  Importa biblioteca para interfaz gráfica
from interfaz_productos import InterfazProductos  #  Importa clase de interfaz de productos
from inventario import Inventario  #  Importa clase Inventario
from tkinter import PhotoImage  #  Importa para manejar imágenes en tkinter
from PIL import Image, ImageTk  #  Importa para procesamiento de imágenes
from tkinter import ttk, messagebox  #  Importa widgets mejorados y cuadros de mensaje

class AplicacionPrincipal:
    def __init__(self):  #  Constructor de la aplicación principal
        self.inventario = Inventario()  #  Crea objeto Inventario para manejar datos
        self.crear_interfaz()  # Llama método para construir interfaz gráfica

    def crear_interfaz(self):  #  Método para crear la ventana principal
        # Ventana principal
        self.root = tk.Tk()  #  Crea ventana principal de tkinter
        self.root.title("Sistema de Inventario - POO")  #  Establece título de ventana
        self.root.geometry("1200x600")  #  Define tamaño de ventana
        self.root.configure(bg="#E6F2FF")  #  Establece color de fondo azul claro
        self.root.attributes("-alpha", 0.95)

        self.root.resizable(False, False) #  Impide redimensionar ventana

        # Cargar imagen PNG
        icono = PhotoImage(file="fotoventana.png")  #  Carga imagen para ícono
        self.root.iconphoto(True, icono)  #  Establece ícono de ventana

        # Atajo de teclado Escape
        self.root.bind('<Escape>', lambda e: self.salir_aplicacion())  #  Asocia tecla Escape para salir

        # Imagen de fondo
        imagen = Image.open("fondo.jpeg")  #  Abre imagen de fondo
        imagen = imagen.resize((1200, 600))  #  Redimensiona imagen al tamaño de ventana
        self.fondo = ImageTk.PhotoImage(imagen)  #  Convierte imagen para tkinter
        label_fondo = tk.Label(self.root, image=self.fondo)  #  Crea etiqueta con imagen de fondo
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  #  Coloca imagen cubriendo toda ventana

        self.mostrar_informacion_estudiante()  #  Llama método para mostrar información
        self.crear_menu_principal()  #  Llama método para crear menú

    def mostrar_informacion_estudiante(self):  #  Método para mostrar datos del estudiante
        info_estudiante = """UNIVERSIDAD ESTATAL AMAZÓNICA
INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN
ASIGNATURA: 
PROGRAMACIÓN ORIENTADA A OBJETOS (A)
TEMA: 
Sistema de Gestión de Inventario
INTEGRANTES:
Alex David Portero Donoso
Aracely Maribel Quintanilla Rumipamba
DOCENTE:
Mgs. SANTIAGO ISRAEL NOGALES GUERRERO
SEMESTRE: 
Segundo Nivel
FECHA: 
domingo, 5 de octubre de 2025"""

        # Frame con fondo cyan
        frame_info = tk.Frame(self.root, bg="#D0EAFB")  #  Crea frame con fondo azul cielo
        frame_info.pack(pady=20)  #  Empaqueta frame con espacio

        # Título del frame
        tk.Label(frame_info, text="Información del Estudiante",
                 font=('Times New Roman', 14, 'bold'),
                 fg="#003366", bg="#D0EAFB").pack(pady=5)

        # Información del estudiante
        tk.Label(frame_info, text=info_estudiante.strip(),
                 font=('Times New Roman', 11),
                 justify=tk.CENTER,
                 anchor='center',
                 fg="#333333",  #  Color gris oscuro para texto
                 bg="#E6F2FF").pack()  #  Empaqueta información con fondo diferente

    def crear_menu_principal(self):  #  Método para crear menú de opciones
        # Frame del menú con mismo fondo
        frame_menu = tk.Frame(self.root, bg="#E6F2FF")  #  Crea frame para botones
        frame_menu.pack(pady=20)  #  Empaqueta frame

        botones_menu = [  #  Define opciones del menú
            ("Gestión de Productos", self.abrir_gestion_productos),  #  Botón para abrir gestión
            ("Salir", self.salir_aplicacion)  #  Botón para salir
        ]

        for texto, comando in botones_menu:  # Itera sobre opciones del menú
            tk.Button(frame_menu, text=texto, command=comando,
                      width=20, height=2,  # Define tamaño botones
                      fg="white",  # Texto blanco
                      bg="#007ACC",  #  Fondo azul
                      activebackground="#005F99",  #  Color al hacer clic
                      activeforeground="white",  # Texto al hacer clic
                      font=('Arial', 10, 'bold')  # Fuente en negrita
                      ).pack(pady=10)  #  Empaqueta cada botón

        # Etiqueta del atajo de teclado
        tk.Label(frame_menu,
                 text="Presiona Escape para salir de la aplicación",
                 font=('New Times Roman', 8),
                 fg="SpringGreen3",  #  Color verde para texto
                 bg="#E6F2FF").pack(pady=10)  # Empaqueta etiqueta informativa

    def abrir_gestion_productos(self):  # Método para abrir ventana de gestión
        if hasattr(self, 'ventana_gestion') and self.ventana_gestion.ventana.winfo_exists():
            self.ventana_gestion.ventana.lift()
            return

        self.ventana_gestion = InterfazProductos(self.root, self.inventario)

        self.ventana_gestion.ventana.transient(self.root)
        self.ventana_gestion.ventana.grab_set()

    def cerrar_ventana(self):
            self.ventana_gestion.ventana.grab_release()
            self.ventana_gestion.ventana.destroy()
            self.ventana_gestion = None  # Elimina la referencia para permitir abrirla de nuevo

            #  Interceptar el evento de cierre (botón X)
            self.ventana_gestion.ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana())

            self.root.wait_window(self.ventana_gestion.ventana)

    def salir_aplicacion(self, event=None):  #  Método para cerrar aplicación
        self.root.quit()  # Cierra ventana principal y termina aplicación

    def ejecutar(self):  #  Método para iniciar aplicación
        self.root.mainloop()  #  Inicia loop principal de tkinter

if __name__ == "__main__":  #  Verifica si es el archivo principal
    app = AplicacionPrincipal()  #  Crea instancia de aplicación
    app.ejecutar()  #  Ejecuta aplicación