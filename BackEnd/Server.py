from Utils.txtManagement import obtener_resultado
from flask import Flask, request, jsonify
import os 

app = Flask(__name__)

@app.route('/parabolicComponents', methods=['POST'])
def getParabolicComponents():
    data = request.get_json()
    height = data.get("height")
    distance = data.get("distance")

    if height is None or distance is None:
        return jsonify({"error": "Faltan parámetros: height o distance"}), 400

    path = os.path.join(os.path.dirname(__file__), "./Assets/data.txt")
    path = os.path.abspath(path)

    res = obtener_resultado(path, distance, height)

    result = {
        "degrees": res[0],
        "speed": res[1]
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

