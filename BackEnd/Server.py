from Utils.txtManagement import obtener_resultado
from flask import Flask, request, jsonify
import os 

app = Flask(__name__)

# Ruta global del archivo de datos (accesible por POST y GET)
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "Assets/data.txt"))

@app.route('/parabolicComponents', methods=['POST'])
def getParabolicComponents():
    data = request.get_json()
    height = data.get("height")
    distance = data.get("distance")
    
    if height is None or distance is None:
        return jsonify({"error": "Faltan parámetros: height o distance"}), 400

    res = obtener_resultado(DATA_PATH, distance, height)

    result = {
        "degrees": res[0],
        "speed": res[1]
    }

    return jsonify(result)


# GET: permite acceder directamente desde el navegador
@app.route('/parabolicComponents', methods=['GET'])
def get_parabolic_components():
    distance = request.args.get("distance")
    height = request.args.get("height")

    res = obtener_resultado(DATA_PATH, float(distance), float(height))

    return jsonify({
        "degrees": res[0],
        "speed": res[1]
    })


if __name__ == '__main__':
    print("Servidor ejecutándose en http://127.0.0.1:5000/parabolicComponents")
    app.run(debug=True, host='0.0.0.0', port=5000)



