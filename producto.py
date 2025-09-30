"""
Clase Producto:
1.-Se encuentra en producto.py.
2.-Tiene los atributos: _id, _nombre, _cantidad, _precio.
3.-Tiene getters y setters para cada atributo.
4.-Tiene dos métodos de representación: to_string() para mostrar en la interfaz y to_file_string() para guardar en archivo."""

class Producto:
    def __init__(self, id, nombre, cantidad, precio):  #  Constructor que inicializa atributos del producto
        self._id = id  #  Atributo privado para identificador único
        self._nombre = nombre  #  Atributo privado para nombre del producto
        self._cantidad = cantidad  #  Atributo privado para cantidad en stock
        self._precio = precio  #  Atributo privado para precio unitario

    # Getters - métodos para obtener valores de atributos privados
    def get_id(self):  #  Getter para ID
        return self._id  #  Retorna valor del ID

    def get_nombre(self):  #  Getter para nombre
        return self._nombre  #  Retorna nombre del producto

    def get_cantidad(self):  #  Getter para cantidad
        return self._cantidad  #  Retorna cantidad disponible

    def get_precio(self):  #  Getter para precio
        return self._precio  #  Retorna precio unitario

    # Setters - métodos para modificar valores de atributos privados
    def set_nombre(self, nombre):  #  Setter para nombre
        self._nombre = nombre  #  Actualiza nombre del producto

    def set_cantidad(self, cantidad):  #  Setter para cantidad
        self._cantidad = cantidad  #  Actualiza cantidad en stock

    def set_precio(self, precio):  #  Setter para precio
        self._precio = precio  #  Actualiza precio unitario

    def to_string(self):  #  Método para representación legible del producto
        return f"ID: {self._id} | {self._nombre} | Cant: {self._cantidad} | Precio: ${self._precio}"  #  String formateado

    def to_file_string(self):  #  Método para representación en archivo (CSV)
        return f"{self._id},{self._nombre},{self._cantidad},{self._precio}"  #  String separado por comas