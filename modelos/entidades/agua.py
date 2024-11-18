from modelos.entidades.bebida import Bebida

class Agua(Bebida):
    @classmethod
    def fromDiccionario(cls, diccionario:dict):
        return cls(diccionario["nombre"], diccionario["costo"], diccionario["stock"], diccionario["mililitros"], diccionario["origen"])

    def __init__(self, nombre:str, costo:float, stock:int, mililitros:int, origen: str):
        super().__init__(nombre, costo, stock, mililitros)
        if not isinstance(origen, str) or origen == "" or origen.isspace():
            raise ValueError("El origen debe ser un string y no puede estar vacío")
        self.__origen = origen
    
    def obtenerOrigen(self):
        return self.__origen
    
    def establecerOrigen(self, origen:str):
        if not isinstance(origen, str) or origen == "" or origen.isspace():
            raise ValueError("El origen no puede ser vacío")
        self.__origen = origen
    
    def obtenerPrecio(self):
        return self._costo * 1.3
    
        
    def toDiccionario(self):
        return {
            "nombre": self._nombre,
            "costo": self._costo,
            "stock": self._stock,
            "mililitros": self._mililitros,
            "origen": self.__origen,
            "precio": self.obtenerPrecio()
        }