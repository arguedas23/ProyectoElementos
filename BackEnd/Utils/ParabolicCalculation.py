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
    # Si estÃ¡ en el rango [-1, 1]
    if x >= -1 and x <= 1:
        arc = 0
        i = 0
        while i < 10:  # nÃºmero de tÃ©rminos de la serie
            signo = (-1) ** i
            termino = (x ** (2 * i + 1)) / (2 * i + 1)
            arc = arc + signo * termino
            i = i + 1
        return arc

    # Si es mayor a 1 â†’ usar reducciÃ³n
    if x > 1:
        return (PI / 2) - arctan(1 / x)

    # Si es menor a -1 â†’ usar reducciÃ³n
    if x < -1:
        return (-PI / 2) - arctan(1 / x)


# Convierte radianes a grados
def radianes_a_grados(radianes):
    return radianes * (180 / PI)

# Verifica si una cadena es un nÃºmero (entero o decimal)
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

# Calcula el Ã¡ngulo (Î¸0) y la velocidad inicial (v0)
# usando las fÃ³rmulas fÃ­sicas del movimiento parabÃ³lico
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

    g = 9.77589
    relacion = (4 * altura) / distancia               # RelaciÃ³n 4H/R
    theta_radianes = arctan(relacion)                 # Ãngulo en radianes
    angulo = radianes_a_grados(theta_radianes)        # Ãngulo en grados
    seno_theta = sin_grados(angulo)                   # Seno del Ã¡ngulo
    seno_cuadrado = seno_theta * seno_theta
    v0 = ((2 * g * altura) / seno_cuadrado) ** 0.5    # FÃ³rmula de velocidad inicial
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

# Programa principal interactivo desde terminal
if __name__ == "__main__": 
    print("=== Simulador matemÃ¡tico de tiro parabÃ³lico ===")
    print("Use 'salir' para terminar.\n")

    seguir = 1
    while seguir == 1:
        texto_R = input("Distancia horizontal mÃ¡xima (m): ")
        if texto_R == "salir":
            seguir = 0
        if seguir == 1:
            texto_H = input("Altura mÃ¡xima (m): ")
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
                        print("  Ãngulo de lanzamiento:", round(angulo, 4), "Â°")
                        print("  Velocidad inicial:", round(velocidad, 4), "m/s\n")
            if valido_R == 0:
                print("Entrada no vÃ¡lida.\n")
            if valido_H == 0:
                print("Entrada no vÃ¡lida.\n")

    print("Programa finalizado.")