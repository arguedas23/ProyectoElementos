
PI = 3.141592653589793

# FUNCIONES MATEMÁTICAS


def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    return n * factorial(n - 1)


def sin_grados(angulo):
    # Normalizar ángulo entre 0 y 360
    while angulo >= 360:
        angulo = angulo - 360
    while angulo < 0:
        angulo = angulo + 360

    # Convertir a radianes
    x = angulo * (PI / 180)

    # Serie de Taylor del seno
    seno = 0
    i = 0
    while i < 7:
        signo = (-1) ** i
        termino = (x ** (2 * i + 1)) / factorial(2 * i + 1)
        seno = seno + signo * termino
        i = i + 1

    return seno


def arctan(x):
    # arctan(x) ≈ x - x^3/3 + x^5/5 - ...
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

    # Si x > 1
    if x > 1:
        return (PI / 2) - (1 / x)

    # Si x < -1
    if x < -1:
        return (-PI / 2) - (1 / x)


def radianes_a_grados(radianes):
    return radianes * (180 / PI)


# FUNCIÓN PRINCIPAL

def calcular_tiro(distancia, altura):
    # Verificación del tipo básico
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

    # Constante gravitacional
    g = 9.8

    # Calcular ángulo θ0 = arctan(4H / R)
    relacion = (4 * altura) / distancia
    theta_radianes = arctan(relacion)
    angulo = radianes_a_grados(theta_radianes)

    # Calcular seno(θ0)
    seno_theta = sin_grados(angulo)
    seno_cuadrado = seno_theta * seno_theta

    # Calcular velocidad inicial v0 = sqrt((2*g*H) / sin²θ)
    v0 = ((2 * g * altura) / seno_cuadrado) ** 0.5

    return angulo, v0


# PRUEBA DESDE TERMINAL

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
        es_numero_R = 0
        if texto_R.isnumeric():
            es_numero_R = 1

        es_numero_H = 0
        if texto_H.isnumeric():
            es_numero_H = 1

        if es_numero_R == 1:
            if es_numero_H == 1:
                R = float(texto_R)
                H = float(texto_H)
                resultado = calcular_tiro(R, H)

                if resultado != "Error01":
                    angulo = resultado[0]
                    velocidad = resultado[1]
                    print("\nResultados:")
                    print("  Ángulo de lanzamiento:", round(angulo, 4), "°")
                    print("  Velocidad inicial:", round(velocidad, 4), "m/s\n")

        if es_numero_R == 0:
            print("Entrada no válida. Escriba solo números o 'salir'.\n")
        if es_numero_H == 0:
            print("Entrada no válida. Escriba solo números o 'salir'.\n")

print("Programa finalizado.")
