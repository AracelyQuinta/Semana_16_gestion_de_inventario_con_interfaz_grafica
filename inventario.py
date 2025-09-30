"""
Clase Inventario:
1.-Se encuentra en inventario.py.
2.-Utiliza un diccionario para almacenar los productos (clave: id, valor: objeto Producto).
3.-Tiene métodos para agregar, eliminar, modificar y mostrar productos.
4.-Guarda y carga el inventario desde un archivo de texto."""

from producto import Producto  #  Importa la clase Producto para crear objetos producto

class Inventario:
    def __init__(self, archivo="inventario.txt"):  #  Constructor con nombre de archivo por defecto
        self._productos = {}  #  Inicializa diccionario vacío para almacenar productos
        self._archivo = archivo  #  Guarda nombre del archivo de persistencia
        self.cargar_desde_archivo()  #  Carga productos existentes al crear inventario

    def agregar_producto(self, producto):  #  Método para agregar producto al inventario
        self._productos[producto.get_id()] = producto  #  Agrega producto al diccionario usando ID como clave
        self.guardar_en_archivo()  #  Guarda cambios en archivo

    def eliminar_producto(self, id):  #  Método para eliminar producto por ID
        if id in self._productos:  #  Verifica si el ID existe en el inventario
            del self._productos[id]  #  Elimina producto del diccionario
            self.guardar_en_archivo()  #  Guarda cambios en archivo
            return True  #  Retorna True indicando éxito
        return False  #  Retorna False si producto no existe

    def modificar_producto(self, id, nombre, cantidad, precio):  #  Método para modificar producto existente
        if id in self._productos:  #  Verifica si producto existe
            producto = self._productos[id]  #  Obtiene referencia al producto
            producto.set_nombre(nombre)  #  Actualiza nombre del producto
            producto.set_cantidad(cantidad)  #  Actualiza cantidad del producto
            producto.set_precio(precio)  #  Actualiza precio del producto
            self.guardar_en_archivo()  #  Guarda cambios en archivo
            return True  #  Retorna True indicando éxito
        return False  #  Retorna False si producto no existe

    def obtener_producto(self, id):  #  Método para obtener producto específico por ID
        return self._productos.get(id)  #  Retorna producto o None si no existe

    def obtener_todos_productos(self):  #  Método para obtener todos los productos
        return list(self._productos.values())  #  Retorna lista con todos los objetos Producto

    def mostrar_productos(self):  #  Método para obtener representación en texto de productos
        return [producto.to_string() for producto in self._productos.values()]  #  Retorna lista de strings formateados

    def guardar_en_archivo(self):  #  Método para guardar inventario en archivo
        try:
            with open(self._archivo, 'w') as f:  #  Abre archivo en modo escritura
                for producto in self._productos.values():  #  Itera sobre todos los productos
                    f.write(producto.to_file_string() + "\n")  #  Escribe cada producto en una línea
        except Exception as e:  #  Captura errores de escritura
            print(f"Error guardando archivo: {e}")  #  Muestra error en consola

    def cargar_desde_archivo(self):  # Método para cargar inventario desde archivo
        self._productos = {}  # Reinicia diccionario de productos
        try:
            with open(self._archivo, 'r') as f:  #  Abre archivo en modo lectura
                for linea in f:  # Itera sobre cada línea del archivo
                    datos = linea.strip().split(',')  #  Divide línea por comas
                    if len(datos) == 4:  #  Verifica que línea tenga 4 campos
                        id, nombre, cantidad, precio = datos  #  Desempaqueta datos
                        producto = Producto(id, nombre, int(cantidad), float(precio))  #  Crea objeto Producto
                        self._productos[id] = producto  #  Agrega producto al inventario
        except FileNotFoundError:  #  Captura error si archivo no existe
            # Si el archivo no existe, se inicia con un inventario vacío
            self._productos = {}  #  Mantiene inventario vacío