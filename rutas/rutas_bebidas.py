from flask import Blueprint, jsonify, request
from modelos.repositorios.repositorios import obtenerRepoBebidas
from modelos.entidades.bebida import Bebida
from modelos.entidades.refresco import Refresco 
from modelos.entidades.agua import Agua

repo_bebidas = obtenerRepoBebidas()

bp_bebidas = Blueprint("bp_bebidas", __name__)

@bp_bebidas.route("/bebidas", methods = ["GET"])
def listar_bebidas():
    return jsonify([bebida.toDiccionario() for bebida in repo_bebidas.obtenerBebidas()])

@bp_bebidas.route("/bebidas/<string:nombre>", methods = ["GET"])
def obtener_bebida(nombre):
    bebida = repo_bebidas.obtenerBebidaPorNombre(nombre)
    if bebida == None:
        return jsonify({"error": "Bebida no encontrada"}), 404
    return jsonify(bebida.toDiccionario())

@bp_bebidas.route("/bebidas", methods = ["POST"])
def agregar_bebida():
    if request.is_json:
        datos = request.json
        try:
            if "origen" in datos:
                bebida = Agua.fromDiccionario(datos)
                tipo = "agua"
            else:
                bebida = Refresco.fromDiccionario(datos)
                tipo = "refresco"
            if not repo_bebidas.existeBebida(bebida.obtenerNombre()):                
                repo_bebidas.agregarBebida(bebida)
                return jsonify({"Mensaje":f"Bebida ({tipo}) agregada con éxito.","bebida":bebida.toDiccionario()}), 201
            else:
                return jsonify({"error": "Ya existe una bebida con ese nombre"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400
    
@bp_bebidas.route("/bebidas/<string:nombre>", methods = ["PUT"])
def modificar_bebida(nombre):
    datos = request.json
    try:
        if "origen" in datos:
            bebida = Agua.fromDiccionario(datos)
            tipo = "agua"
        else:
            bebida = Refresco.fromDiccionario(datos)
            tipo = "refresco"
        if repo_bebidas.actualizarBebida(nombre, bebida):
            return jsonify({"Mensaje":f"Bebida ({tipo}) actualizada con éxito.","bebida":bebida.toDiccionario()})
        return jsonify({"error": "No se encontró la bebida a actualizar"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@bp_bebidas.route("/bebidas/<string:nombre>", methods = ["DELETE"])
def eliminar_bebida(nombre):
    if repo_bebidas.eliminarBebida(nombre):
        return jsonify({"Mensaje":f"Bebida eliminada con éxito."})
    return jsonify({"error": "No se encontró la bebida a eliminar"}), 404

@bp_bebidas.route("/bebidas/<string:nombre>/precio", methods=["GET"])
def obtener_precio_bebida(nombre):
    bebida = repo_bebidas.obtenerBebidaPorNombre(nombre)
    if bebida is None:
        return jsonify({"error": "Bebida no encontrada"}), 404
    return jsonify({"nombre": bebida.obtenerNombre(), "precio": bebida.obtenerPrecio()})