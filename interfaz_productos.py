"""
Interfaz Gráfica:
1.- Hay un archivo principal main.py que ejecuta la aplicación.
2.- Muestra la información del estudiante en la pantalla principal.
3.- Tiene un menú con opciones para "Gestión de Productos" y "Salir".
4.- Al abrir "Gestión de Productos", se abre una nueva ventana (Toplevel) con un formulario para gestionar productos.
"""

import tkinter as tk  #  Importa la biblioteca principal para crear interfaces gráficas
from tkinter import ttk, messagebox  #  Importa widgets mejorados y cuadros de mensaje
from producto import Producto  #  Importa la clase Producto desde el archivo producto.py
from PIL import Image, ImageTk  #  Importa biblioteca para manejar imágenes en la interfaz

class InterfazProductos:
    def __init__(self, parent, inventario):  #  Constructor que recibe la ventana padre y el inventario
        self.parent = parent  #  Guarda referencia a la ventana principal
        self.inventario = inventario  #  Guarda referencia al objeto inventario

        self.ventana = tk.Toplevel(parent)  #  Crea una nueva ventana secundaria
        self.ventana.title("Gestión de Productos")  #  Establece el título de la ventana
        self.ventana.geometry("850x550")  #  Define el tamaño de la ventana
        self.ventana.resizable(False, False)  #  Impide que el usuario redimensione la ventana

        # Atajos de teclado
        self.ventana.bind('<Delete>', lambda e: self.eliminar_producto())  #  Asocia tecla Delete para eliminar
        self.ventana.bind('<d>', lambda e: self.eliminar_producto())  #  Asocia tecla D para eliminar

        self.crear_interfaz()  #  Llama al método que construye todos los elementos visuales
        self.listar_productos()  #  Carga y muestra los productos existentes al iniciar

        # Etiqueta de atajos de teclado
        label_atajos = tk.Label(self.ventana,
                               text="Atajos: Doble clic en un producto para cargarlo | Delete o D: Eliminar producto seleccionado",
                               font=('Arial', 8),
                               fg="green")  #  Crea etiqueta informativa sobre atajos
        label_atajos.pack(side=tk.BOTTOM, pady=5)  #  Coloca la etiqueta en la parte inferior

    def crear_interfaz(self):  #  Método principal para construir la interfaz visual
        # Frame para la imagen y título
        frame_titulo = tk.Frame(self.ventana)  #  Crea contenedor para título e imagen
        frame_titulo.pack(pady=10)  #  Empaqueta el frame con espacio vertical

        # Cargar y mostrar imagen Pikachu
        try:
            imagen_original = Image.open("pikachu.png")  #  Abre la imagen desde archivo
            imagen_redimensionada = imagen_original.resize((100, 100), Image.Resampling.LANCZOS)  #  Cambia tamaño imagen
            self.imagen_pikachu = ImageTk.PhotoImage(imagen_redimensionada)  #  Convierte imagen para tkinter

            label_imagen = tk.Label(self.ventana, image=self.imagen_pikachu)  #  Crea etiqueta para mostrar imagen
            label_imagen.place(x=600, y=70)  #  Posiciona la imagen en coordenadas específicas

        except Exception as e:
            print(f"Error cargando imagen: {e}")  #  Maneja errores si la imagen no carga
            self.imagen_pikachu = None  #  Establece imagen como None si hay error

        # Título centrado
        tk.Label(frame_titulo,
                text="GESTIÓN DE PRODUCTOS",
                font=('Arial', 14, 'bold'),
                fg="#2E86AB").pack()  #  Crea y muestra el título principal de la ventana

        # Frame para formulario
        frame_formulario = tk.Frame(self.ventana)  #  Crea contenedor para los campos de entrada
        frame_formulario.pack(pady=10)  #  Empaqueta el frame del formulario

        # Campos de entrada
        self.crear_campo(frame_formulario, "ID:", 0)  #  Crea campo para ID del producto
        self.crear_campo(frame_formulario, "Nombre:", 1)  #  Crea campo para nombre del producto
        self.crear_campo(frame_formulario, "Cantidad:", 2)  #  Crea campo para cantidad del producto
        self.crear_campo(frame_formulario, "Precio:", 3)  #  Crea campo para precio del producto

        # Frame para botones
        frame_botones = tk.Frame(self.ventana)  #  Crea contenedor para los botones
        frame_botones.pack(pady=10)  #  Empaqueta el frame de botones

        botones_info = [  #  Define información de cada botón (texto y función)
            ("Agregar", self.agregar_producto),
            ("Modificar", self.modificar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar", self.limpiar_campos)
        ]

        for texto, comando in botones_info:  #  Itera sobre la lista de botones
            tk.Button(frame_botones, text=texto, command=comando).pack(side=tk.LEFT, padx=5)  #  Crea y empaqueta cada botón

        # Treeview para listado
        frame_listado = tk.Frame(self.ventana)  #  Crea contenedor para la tabla de productos
        frame_listado.pack(pady=10, fill=tk.BOTH, expand=True)  #  Empaqueta expandiéndose

        tk.Label(frame_listado, text="Listado de Productos:").pack()  #  Etiqueta para la sección de listado

        # Crear Treeview (tabla)
        self.tree = ttk.Treeview(frame_listado, columns=('ID', 'Nombre', 'Cantidad', 'Precio'), show='headings')  #  Crea tabla con columnas
        self.tree.heading('ID', text='ID')  #  Define encabezado de columna ID
        self.tree.heading('Nombre', text='Nombre')  #  Define encabezado de columna Nombre
        self.tree.heading('Cantidad', text='Cantidad')  #  Define encabezado de columna Cantidad
        self.tree.heading('Precio', text='Precio')  #  Define encabezado de columna Precio

        # Configurar columnas
        self.tree.column('ID', width=80)  #  Establece ancho de columna ID
        self.tree.column('Nombre', width=150)  #  Establece ancho de columna Nombre
        self.tree.column('Cantidad', width=80)  #  Establece ancho de columna Cantidad
        self.tree.column('Precio', width=80)  #  Establece ancho de columna Precio

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(frame_listado, orient=tk.VERTICAL, command=self.tree.yview)  #  Crea barra de desplazamiento vertical
        self.tree.configure(yscroll=scrollbar.set)  #  Conecta tabla con scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  #  Coloca scrollbar a la derecha
        self.tree.pack(fill=tk.BOTH, expand=True)  #  Empaqueta tabla expandiéndose

        # Etiqueta de instrucciones para el Treeview
        frame_instrucciones = tk.Frame(frame_listado)  #  Crea frame para instrucciones
        frame_instrucciones.pack(fill=tk.X, pady=5)  #  Empaqueta frame de instrucciones

        tk.Label(frame_instrucciones,
                 text="💡 Instrucción: Haz doble clic sobre un producto para cargar sus datos en el formulario",
                 font=('Arial', 8), fg='#7D3C98').pack()  #  Muestra instrucción para usuario

        # Binding para doble clic
        self.tree.bind('<Double-1>', self.cargar_datos_desde_seleccion)  #  Asocia doble clic en tabla a función

    def crear_campo(self, parent, texto, fila):  #  Método para crear campos de entrada etiquetados
        tk.Label(parent, text=texto).grid(row=fila, column=0, padx=5, pady=2, sticky=tk.W)  #  Crea etiqueta del campo
        entry = tk.Entry(parent)  #  Crea campo de entrada de texto
        entry.grid(row=fila, column=1, padx=5, pady=2)  #  Posiciona campo en grid
        setattr(self, f"entry_{texto.lower().replace(':', '')}", entry)  #  Guarda referencia al campo como atributo

    def obtener_datos_formulario(self):  #  Método para extraer y validar datos del formulario
        try:
            return {  #  Retorna diccionario con datos validados
                'id': self.entry_id.get(),  #  Obtiene texto del campo ID
                'nombre': self.entry_nombre.get(),  #  Obtiene texto del campo Nombre
                'cantidad': int(self.entry_cantidad.get()),  #  Convierte cantidad a número entero
                'precio': float(self.entry_precio.get())  #  Convierte precio a número decimal
            }
        except ValueError:  #  Captura error si conversión falla
            raise ValueError("Cantidad y Precio deben ser números válidos")  #  Lanza error descriptivo

    def agregar_producto(self):  #  Método para agregar nuevo producto al inventario
        """
        aqui deviamos preguntar si ya existe ese codigo
        si ya existe deberiaamos decirle que ya no puede ingresar ese codigo
        """

        try:
            datos = self.obtener_datos_formulario()

            productos_existentes = self.inventario.obtener_todos_productos()
            ids_existentes = [p.get_id() for p in productos_existentes]

            if datos['id'] in ids_existentes:
                # Mostrar advertencia si el ID ya está registrado
                messagebox.showwarning("ID duplicado",
                                       f"Ya existe un producto con el ID '{datos['id']}'. Por favor, use otro ID.")
                return  # Detiene el proceso de agregar

            # Si el ID es nuevo, se crea y agrega el producto
            producto = Producto(datos['id'], datos['nombre'], datos['cantidad'], datos['precio'])
            self.inventario.agregar_producto(producto)
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_campos()
            self.listar_productos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {str(e)}")

            #  Obtiene datos validados del formulario
            producto = Producto(datos['id'], datos['nombre'], datos['cantidad'], datos['precio'])  #  Crea objeto Producto
            self.inventario.agregar_producto(producto)  #  Agrega producto al inventario
            messagebox.showinfo("Éxito", "Producto agregado correctamente")  #  Muestra mensaje de confirmación
            self.limpiar_campos()  # Limpia los campos del formulario
            self.listar_productos()  #  Actualiza la lista de productos
        except Exception as e:  #  Captura cualquier error
            messagebox.showerror("Error", f"No se pudo agregar el producto: {str(e)}")  #  Muestra error al usuario

    def modificar_producto(self):  #  Método para modificar producto existente
        try:
            datos = self.obtener_datos_formulario()  #  Obtiene datos del formulario
            if self.inventario.modificar_producto(datos['id'], datos['nombre'], datos['cantidad'], datos['precio']):  #  Intenta modificar
                messagebox.showinfo("Éxito", "Producto modificado correctamente")  #  Mensaje si éxito
                self.limpiar_campos()  #  Limpia formulario
                self.listar_productos()  #  Actualiza lista
            else:
                messagebox.showerror("Error", "Producto no encontrado")  #  Mensaje si producto no existe
        except Exception as e:  #  Captura errores
            messagebox.showerror("Error", f"No se pudo modificar el producto: {str(e)}")  #  Muestra error

    def eliminar_producto(self):  #  Método para eliminar producto seleccionado
        seleccion = self.tree.selection()  #  Obtiene elemento seleccionado en tabla
        if seleccion:  #  Verifica si hay selección
            item = seleccion[0]  #  Obtiene primer elemento seleccionado
            id_producto = self.tree.item(item, 'values')[0]  #  Extrae ID del producto de la tabla
            if self.inventario.eliminar_producto(id_producto):  #  Intenta eliminar del inventario
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")  #  Mensaje de éxito
                self.listar_productos()  #  Actualiza lista
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")  #  Mensaje de error
        else:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar")  #  Mensaje si no hay selección

    def listar_productos(self):  #  Método para mostrar todos los productos en la tabla
        # Limpiar treeview
        for item in self.tree.get_children():  #  Itera sobre todos los elementos de la tabla
            self.tree.delete(item)  #  Elimina cada elemento

        # Cargar productos
        productos = self.inventario.obtener_todos_productos()  #  Obtiene lista de productos del inventario
        for producto in productos:  #  Itera sobre cada producto
            self.tree.insert('', tk.END, values=(  #  Inserta nueva fila en tabla
                producto.get_id(),  #  Valor ID
                producto.get_nombre(),  #  Valor Nombre
                producto.get_cantidad(),  #  Valor Cantidad
                f"${producto.get_precio():.2f}"  #  Valor Precio formateado como dinero
            ))

    def cargar_datos_desde_seleccion(self, event):  # Método para cargar datos de producto seleccionado al formulario
        seleccion = self.tree.selection()  #  Obtiene selección de tabla
        if seleccion:  #  Verifica si hay selección
            item = seleccion[0]  #  Obtiene primer elemento
            valores = self.tree.item(item, 'values')  #  Obtiene valores de la fila
            self.limpiar_campos()  #  Limpia formulario antes de cargar
            self.entry_id.insert(0, valores[0])  #  Inserta ID en campo
            self.entry_nombre.insert(0, valores[1])  #  Inserta Nombre en campo
            self.entry_cantidad.insert(0, valores[2])  #  Inserta Cantidad en campo
            # Remover el símbolo $ del precio si existe
            precio = valores[3].replace('$', '') if isinstance(valores[3], str) else valores[3]  #  Limpia formato de precio
            self.entry_precio.insert(0, precio)  #  Inserta Precio en campo

    def limpiar_campos(self):  #  Método para vaciar todos los campos del formulario
        self.entry_id.delete(0, tk.END)  #  Limpia campo ID
        self.entry_nombre.delete(0, tk.END)  # Limpia campo Nombre
        self.entry_cantidad.delete(0, tk.END)  #  Limpia campo Cantidad
        self.entry_precio.delete(0, tk.END)  #  Limpia campo Precio