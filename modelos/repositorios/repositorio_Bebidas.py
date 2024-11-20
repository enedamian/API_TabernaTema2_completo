from modelos.entidades.refresco import Refresco
from modelos.entidades.agua import Agua
from modelos.entidades.bebida import Bebida
import json

class RepositorioBebidas:
    ruta_archivo = "datos/bebidas.json"

    def __init__(self):
        self.__bebidas = []
        self.__cargarBebidas()

    def __cargarBebidas(self):
        try:
            with open(RepositorioBebidas.ruta_archivo, "r") as archivo:
                lista_dicc_bebidas = json.load(archivo)
                for bebida in lista_dicc_bebidas:
                    if "origen" in bebida:
                        self.__bebidas.append(Agua.fromDiccionario(bebida))
                    else:
                        self.__bebidas.append(Refresco.fromDiccionario(bebida))
        except FileNotFoundError:
            print("No se encontró el archivo de bebidas")
        except Exception as e:
            print("Error cargando las bebidas del archivo.\n" + str(e))

    def __guardarBebidas(self):
        try:
            with open(RepositorioBebidas.ruta_archivo, "w") as archivo:
                lista_dicc_bebidas = [bebida.toDiccionario() for bebida in self.__bebidas]
                json.dump(lista_dicc_bebidas, archivo, indent=4)
        except Exception as e:
            print("Error guardando las bebidas en el archivo.\n" + str(e))
    
    def obtenerBebidas(self):
        """Retorna una lista con todas las bebidas"""
        return self.__bebidas
    
    def obtenerBebidaPorNombre(self, nombre:str):
        """Retorna la bebida con el nombre indicado, None si no existe"""
        if not isinstance(nombre, str) or nombre == "" or nombre.isspace():
            raise ValueError("El nombre debe ser un string y no puede estar vacío")
        for bebida in self.__bebidas:
            if bebida.obtenerNombre() == nombre:
                return bebida
        return None
    
    def existeBebida(self, nombre:str):
        """Retorna True si existe una bebida con el nombre indicado, False en caso contrario"""
        if not isinstance(nombre, str) or nombre == "" or nombre.isspace():
            raise ValueError("El nombre debe ser un string y no puede estar vacío")
        return self.obtenerBebidaPorNombre(nombre) != None
    
    def agregarBebida(self, bebida: Bebida):
        """Agrega una bebida al repositorio. Lanza ValueError si ya existe una bebida con el mismo nombre"""
        if not isinstance(bebida, Bebida):
            raise ValueError("El objeto a agregar debe ser una bebida")
        if self.existeBebida(bebida.obtenerNombre()):
            raise ValueError("Ya existe una bebida con ese nombre")
        self.__bebidas.append(bebida)
        self.__guardarBebidas()

    def actualizarBebida(self, nombre:str, bebida: Bebida)->bool:
        """Actualiza los datos de una bebida en base a su nombre. Retorna True si la bebida fue actualizada, False en caso contrario"""
        if not isinstance(nombre, str) or nombre == "" or nombre.isspace():
            raise ValueError("El nombre debe ser un string y no puede estar vacío")
        if not isinstance(bebida, Bebida):
            raise ValueError("El objeto a actualizar debe ser una bebida")
        for bebida_a_modificar in self.__bebidas:
            if bebida_a_modificar.obtenerNombre() == nombre:                
                bebida_a_modificar = bebida
                self.__guardarBebidas()
                return True
        return False
    
    def eliminarBebida(self, nombre:str)->bool:
        """Elimina una bebida en base a su nombre. Retorna True si la bebida fue eliminada, False en caso contrario"""
        if not isinstance(nombre, str) or nombre == "" or nombre.isspace():
            raise ValueError("El nombre debe ser un string y no puede estar vacío")
        for bebida in self.__bebidas:
            if bebida.obtenerNombre() == nombre:
                self.__bebidas.remove(bebida)
                self.__guardarBebidas()
                return True
        return False
    
