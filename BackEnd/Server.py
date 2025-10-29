from Utils.txtManagement import obtener_resultado, cargar_datos, guardar_datos
from Utils.ParabolicCalculation import calcular_tiro, graficar_trayectoria, generar_grafica_base64
from flask import Flask, request, jsonify, render_template, send_file
import os 
import io
import base64

app = Flask(__name__)

# Ruta global del archivo de datos (accesible por POST y GET)
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "Assets/data.txt"))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/parabolicComponents', methods=['POST'])
def getParabolicComponents():
    data = request.get_json()
    height = data.get("height")
    distance = data.get("distance")
    
    if height is None or distance is None:
        return jsonify({"error": "Faltan parámetros: height o distance"}), 400

    try:
        height = float(height)
        distance = float(distance)
    except (TypeError, ValueError):
        return jsonify({"error": "Los parámetros deben ser números válidos"}), 400

    res = obtener_resultado(DATA_PATH, distance, height)
    
    if isinstance(res, str) and res.startswith("Error"):
        return jsonify({"error": "Error en el cálculo de parámetros"}), 500

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
    
    if distance is None or height is None:
        return jsonify({"error": "Faltan parámetros: distance y height"}), 400

    try:
        distance = float(distance)
        height = float(height)
    except (TypeError, ValueError):
        return jsonify({"error": "Los parámetros deben ser números válidos"}), 400

    res = obtener_resultado(DATA_PATH, distance, height)
    
    if isinstance(res, str) and res.startswith("Error"):
        return jsonify({"error": "Error en el cálculo de parámetros"}), 500

    return jsonify({
        "degrees": res[0],
        "speed": res[1]
    })

# Nueva ruta para generar gráficas
@app.route('/plotTrajectory', methods=['GET'])
def plot_trajectory():
    distance = request.args.get("distance")
    height = request.args.get("height")
    
    if distance is None or height is None:
        return jsonify({"error": "Faltan parámetros: distance y height"}), 400

    try:
        distance = float(distance)
        height = float(height)
    except (TypeError, ValueError):
        return jsonify({"error": "Los parámetros deben ser números válidos"}), 400

    # Calcular parámetros
    res = calcular_tiro(distance, height)
    
    if isinstance(res, str) and res.startswith("Error"):
        return jsonify({"error": "Error en el cálculo de la trayectoria"}), 500

    angulo, velocidad = res
    
    # Generar gráfica en base64 para enviar al frontend
    img_base64 = generar_grafica_base64(distance, height, angulo, velocidad)
    
    return jsonify({
        "image": img_base64,
        "parameters": {
            "distance": distance,
            "height": height,
            "angle": angulo,
            "speed": velocidad
        }
    })

# Ruta para ver todas las trayectorias guardadas
@app.route('/savedTrajectories', methods=['GET'])
def saved_trajectories():
    try:
        datos = cargar_datos(DATA_PATH)
        return jsonify({
            "count": len(datos),
            "trajectories": datos
        })
    except Exception as e:
        return jsonify({"error": f"Error cargando datos: {str(e)}"}), 500

# Ruta para la página de gráficas
@app.route('/graph')
def graph_page():
    return render_template("graph.html")

if __name__ == '__main__':
    print("Servidor ejecutándose en http://127.0.0.1:5000/")
    print("Rutas disponibles:")
    print("  GET  /parabolicComponents?distance=X&height=Y")
    print("  POST /parabolicComponents (JSON: {distance: X, height: Y})")
    print("  GET  /plotTrajectory?distance=X&height=Y")
    print("  GET  /savedTrajectories")
    print("  GET  /graph")
    app.run(debug=True, host='0.0.0.0', port=5000)
