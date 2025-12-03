from flask import Flask, request, jsonify, send_from_directory
import sys
import os

# Agregar el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar las funciones necesarias
try:
    from Utils.ParabolicCalculation import calcular_tiro, calcular_tiempo_vuelo, calcular_velocidad_horizontal
    from Utils.txtManagement import obtener_resultado
    USE_CACHE = True
except ImportError:
    # Si no se pueden importar los módulos, usar solo las funciones locales
    print("Advertencia: No se pudieron importar los módulos de Utils. Usando modo standalone.")
    USE_CACHE = False
    
    # Definir las funciones localmente si no se pueden importar
    PI = 3.141592653589793
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado
    
    def sin_grados(angulo, terms=7):
        x = angulo * (PI / 180)
        x = ((x + PI) % (2 * PI)) - PI
        seno = 0
        for n in range(terms):
            signo = (-1) ** n
            termino = (x ** (2 * n + 1)) / factorial(2 * n + 1)
            seno += signo * termino
        return seno
    
    def arctan(x):
        if x >= -1 and x <= 1:
            arc = 0
            i = 0
            while i < 10:
                signo = (-1) ** i
                termino = (x ** (2 * i + 1)) / (2 * i + 1)
                arc = arc + signo * termino
                i = i + 1
            return arc
        if x > 1:
            return (PI / 2) - arctan(1 / x)
        if x < -1:
            return (-PI / 2) - arctan(1 / x)
    
    def radianes_a_grados(radianes):
        return radianes * (180 / PI)
    
    def calcular_tiro(distancia, altura):
        if not isinstance(distancia, (int, float)) or not isinstance(altura, (int, float)):
            return "Error01"
        
        g = 9.77589
        relacion = (4 * altura) / distancia
        theta_radianes = arctan(relacion)
        angulo = radianes_a_grados(theta_radianes)
        seno_theta = sin_grados(angulo)
        seno_cuadrado = seno_theta * seno_theta
        v0 = ((2 * g * altura) / seno_cuadrado) ** 0.5
        return angulo, v0
    
    def calcular_tiempo_vuelo(v0, angulo):
        g = 9.8
        seno = sin_grados(angulo)
        T = (2 * v0 * seno) / g
        return T
    
    def calcular_velocidad_horizontal(v0, angulo):
        seno = sin_grados(angulo)
        coseno_cuadrado = 1 - (seno * seno)
        if coseno_cuadrado < 0:
            coseno_cuadrado = 0
        coseno = coseno_cuadrado ** 0.5
        Vx = v0 * coseno
        return Vx

app = Flask(__name__, static_folder='.', static_url_path='')

# Ruta del archivo de datos
DATA_FILE = "data.txt"

@app.route('/')
def index():
    """Ruta principal que sirve el archivo HTML"""
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def index_html():
    """Ruta alternativa para index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/parabolicComponents', methods=['POST'])
def parabolic_components():
    """
    Endpoint que recibe distancia y altura, y devuelve:
    - Ángulo de lanzamiento (degrees)
    - Velocidad inicial (speed)
    - Tiempo de vuelo (tiempo_vuelo)
    - Velocidad horizontal (velocidad_horizontal)
    """
    try:
        # Obtener datos del request JSON
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        distance = data.get('distance')
        height = data.get('height')
        
        # Validar que se recibieron los datos
        if distance is None or height is None:
            return jsonify({'error': 'Faltan parámetros: distance y height son requeridos'}), 400
        
        # Convertir a float
        try:
            distance = float(distance)
            height = float(height)
        except (ValueError, TypeError):
            return jsonify({'error': 'Los valores deben ser números válidos'}), 400
        
        # Validar que los valores sean positivos
        if distance <= 0 or height <= 0:
            return jsonify({'error': 'Los valores deben ser mayores a 0'}), 400
        
        # Intentar obtener resultado del archivo si está disponible el cache
        if USE_CACHE:
            try:
                resultado = obtener_resultado(DATA_FILE, distance, height)
                
                # Si hay error o no existe, calcular directamente
                if isinstance(resultado, str) and resultado.startswith("Error"):
                    resultado = calcular_tiro(distance, height)
            except Exception as e:
                print(f"Error al usar cache: {e}")
                resultado = calcular_tiro(distance, height)
        else:
            # Sin cache, calcular directamente
            resultado = calcular_tiro(distance, height)
        
        # Verificar si hubo error en el cálculo
        if isinstance(resultado, str) and resultado == "Error01":
            return jsonify({'error': 'Error en el cálculo de tiro parabólico'}), 500
        
        # resultado es una tupla (angulo, v0) o una lista [angulo, v0]
        angulo = float(resultado[0])
        v0 = float(resultado[1])
        
        # Calcular tiempo de vuelo y velocidad horizontal
        tiempo_vuelo = calcular_tiempo_vuelo(v0, angulo)
        velocidad_horizontal = calcular_velocidad_horizontal(v0, angulo)
        
        # Preparar respuesta
        response = {
            'degrees': angulo,
            'speed': v0,
            'tiempo_vuelo': tiempo_vuelo,
            'velocidad_horizontal': velocidad_horizontal
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error en parabolic_components: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/calcular', methods=['GET', 'POST'])
def calcular_manual():
    """
    Ruta alternativa para cálculos manuales
    Acepta tanto GET con parámetros de query como POST con form data
    """
    try:
        if request.method == 'POST':
            distance = request.form.get('distance')
            height = request.form.get('height')
        else:
            distance = request.args.get('distance')
            height = request.args.get('height')
        
        if not distance or not height:
            return jsonify({'error': 'Parámetros distance y height son requeridos'}), 400
        
        distance = float(distance)
        height = float(height)
        
        if distance <= 0 or height <= 0:
            return jsonify({'error': 'Los valores deben ser mayores a 0'}), 400
        
        # Calcular usando el archivo de cache si está disponible
        if USE_CACHE:
            try:
                resultado = obtener_resultado(DATA_FILE, distance, height)
                if isinstance(resultado, str) and resultado.startswith("Error"):
                    resultado = calcular_tiro(distance, height)
            except Exception:
                resultado = calcular_tiro(distance, height)
        else:
            resultado = calcular_tiro(distance, height)
        
        if isinstance(resultado, str) and resultado.startswith("Error"):
            return jsonify({'error': 'Error en el cálculo'}), 500
        
        angulo = float(resultado[0])
        v0 = float(resultado[1])
        
        tiempo = calcular_tiempo_vuelo(v0, angulo)
        vx = calcular_velocidad_horizontal(v0, angulo)
        
        return jsonify({
            'angulo': angulo,
            'velocidad_inicial': v0,
            'tiempo_vuelo': tiempo,
            'velocidad_horizontal': vx
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Los valores deben ser números válidos'}), 400
    except Exception as e:
        print(f"Error en calcular_manual: {str(e)}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'Servidor Flask funcionando correctamente',
        'cache_enabled': USE_CACHE
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    # Verificar estructura de archivos
    print("\n" + "="*60)
    print("Verificando archivos necesarios...")
    print("="*60)
    
    # Verificar index.html
    if os.path.exists('index.html'):
        print("✓ index.html encontrado")
    else:
        print("✗ ADVERTENCIA: index.html no encontrado en el directorio actual")
    
    # Verificar data.txt
    if USE_CACHE:
        if not os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'w') as f:
                    pass
                print(f"✓ Archivo {DATA_FILE} creado")
            except Exception as e:
                print(f"✗ No se pudo crear el archivo {DATA_FILE}: {e}")
        else:
            print(f"✓ {DATA_FILE} encontrado")
    
    # Verificar carpeta Utils
    if os.path.exists('Utils'):
        print("✓ Carpeta Utils encontrada")
    else:
        print("✗ Carpeta Utils no encontrada (modo standalone activo)")
    
    # Iniciar servidor Flask
    print("\n" + "="*60)
    print("Servidor Flask iniciado")
    print("="*60)
    print(f"URL: http://127.0.0.1:5000/")
    print(f"Cache habilitado: {USE_CACHE}")
    print(f"Modo debug: Activado")
    print("="*60)
    print("Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)