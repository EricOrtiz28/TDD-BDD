from flask import Flask,jsonify,request
import status

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Crea un contador"""
    app.logger.info(f"Solicitud para crear el contador: {name}")
    global COUNTERS

    # Verifica si el contador ya existe
    if name in COUNTERS:
        return {"message": f"El contador {name} ya existe"}, status.HTTP_409_CONFLICT

    # Si no existe, inicializa el contador en 0
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

@app.put("/counters/<name>")
def update_counter(name):
    """Actualizar contador"""
    global COUNTERS
    if name in COUNTERS:
        COUNTERS[name] += 1
        return {"update_message": COUNTERS[name]}, status.HTTP_200_OK
    else:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    
@app.get("/counters/<name>")
def get_counter(name):
    """Obtenemos datos del contador"""
    global COUNTERS
    if name in COUNTERS:
        return {"message": COUNTERS[name]}, status.HTTP_200_OK
    else:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    
@app.delete("/counters/<name>")
def erase_counter(name):
    """Eliminar usuario"""
    global COUNTERS
    if name in COUNTERS:
        del COUNTERS[name]
        return {"message": "Element was deleted sucessfully"}, status.HTTP_200_OK
    else:
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    
@app.put("/counters/<name>/set")
def set_counter(name):
    if name not in COUNTERS:
        # Retorna 404 si el contador no existe
        return jsonify({"error": f"Counter '{name}' not found"}), status.HTTP_404_NOT_FOUND
    data = request.get_json()
    if "value" in data and isinstance(data["value"], int):
        COUNTERS[name] = data["value"]
        return jsonify({"message": f"Counter '{name}' updated to {data['value']}"}), status.HTTP_200_OK
    else:
        return jsonify({"error": "Invalid input, 'value' must be an integer"}), status.HTTP_400_BAD_REQUEST