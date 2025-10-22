PI = 3.141592653589793

# Calcula el factorial de un número (usado en las series de Taylor)
def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return n * factorial(n - 1)

# Calcula el seno de un ángulo en grados usando la serie de Taylor
def sin_grados(angulo):
    while angulo >= 360:
        angulo = angulo - 360
    while angulo < 0:
        angulo = angulo + 360
    x = angulo * (PI / 180)
    seno = 0
    i = 0
    while i < 7:
        signo = (-1) ** i
        termino = (x ** (2 * i + 1)) / factorial(2 * i + 1)
        seno = seno + signo * termino
        i = i + 1
    return seno

# Calcula arctan(x) en radianes usando la serie de Taylor (aproximación)
def arctan(x):
    if x >= -1:
        if x <= 1:
            arc = 0
            i = 0
            while i < 10:
                signo = (-1) ** i
                termino = (x ** (2 * i + 1)) / (2 * i + 1)
                arc = arc + signo * termino
                i = i + 1
            return arc
    if x > 1:
        return (PI / 2) - (1 / x)
    if x < -1:
        return (-PI / 2) - (1 / x)

# Convierte radianes a grados
def radianes_a_grados(radianes):
    return radianes * (180 / PI)

# Verifica si una cadena es un número (entero o decimal)
def es_numero(texto):
    i = 0
    puntos = 0
    if len(texto) == 0:
        return 0
    while i < len(texto):
        c = texto[i]
        if c == ".":
            puntos = puntos + 1
        else:
            if c < "0":
                return 0
            if c > "9":
                return 0
        i = i + 1
    if puntos > 1:
        return 0
    return 1

# Calcula el ángulo (θ0) y la velocidad inicial (v0)
# usando las fórmulas físicas del movimiento parabólico
def calcular_tiro(distancia, altura):
    es_numero_dist = 0
    if type(distancia) == int:
        es_numero_dist = 1
    if type(distancia) == float:
        es_numero_dist = 1
    es_numero_alt = 0
    if type(altura) == int:
        es_numero_alt = 1
    if type(altura) == float:
        es_numero_alt = 1
    if es_numero_dist == 0:
        return "Error01"
    if es_numero_alt == 0:
        return "Error01"

    g = 9.8
    relacion = (4 * altura) / distancia               # Relación 4H/R
    theta_radianes = arctan(relacion)                 # Ángulo en radianes
    angulo = radianes_a_grados(theta_radianes)        # Ángulo en grados
    seno_theta = sin_grados(angulo)                   # Seno del ángulo
    seno_cuadrado = seno_theta * seno_theta
    v0 = ((2 * g * altura) / seno_cuadrado) ** 0.5    # Fórmula de velocidad inicial
    return angulo, v0

# Programa principal interactivo desde terminal
print("=== Simulador matemático de tiro parabólico ===")
print("Use 'salir' para terminar.\n")

seguir = 1
while seguir == 1:
    texto_R = input("Distancia horizontal máxima (m): ")
    if texto_R == "salir":
        seguir = 0
    if seguir == 1:
        texto_H = input("Altura máxima (m): ")
        if texto_H == "salir":
            seguir = 0

    if seguir == 1:
        valido_R = es_numero(texto_R)
        valido_H = es_numero(texto_H)
        if valido_R == 1:
            if valido_H == 1:
                R = float(texto_R)
                H = float(texto_H)
                resultado = calcular_tiro(R, H)
                if resultado != "Error01":
                    angulo = resultado[0]
                    velocidad = resultado[1]
                    print("\nResultados:")
                    print("  Ángulo de lanzamiento:", round(angulo, 4), "°")
                    print("  Velocidad inicial:", round(velocidad, 4), "m/s\n")
        if valido_R == 0:
            print("Entrada no válida.\n")
        if valido_H == 0:
            print("Entrada no válida.\n")

print("Programa finalizado.")


