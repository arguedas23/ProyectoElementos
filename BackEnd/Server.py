from Utils.txtManagement import obtener_resultado

ruta_txt = "Assets/data.txt"

print("=== Simulador de Tiro Parabólico con Registro ===")
print("Escriba 'salir' para terminar.\n")

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
        # Verifica que las entradas sean números válidos (solo dígitos y un punto)
        valido_R = 1
        valido_H = 1

        i = 0
        puntos_R = 0
        while i < len(texto_R):
            c = texto_R[i]
            if c == ".":
                puntos_R = puntos_R + 1
            else:
                if c < "0" or c > "9":
                    valido_R = 0
            i = i + 1
        if puntos_R > 1:
            valido_R = 0

        i = 0
        puntos_H = 0
        while i < len(texto_H):
            c = texto_H[i]
            if c == ".":
                puntos_H = puntos_H + 1
            else:
                if c < "0" or c > "9":
                    valido_H = 0
            i = i + 1
        if puntos_H > 1:
            valido_H = 0

        if valido_R == 1:
            if valido_H == 1:
                R = float(texto_R)
                H = float(texto_H)
                resultado = obtener_resultado(ruta_txt, R, H)
                if resultado != "Error05":
                    print("\nResultados:")
                    print("  Ángulo de lanzamiento:", round(resultado[0], 4), "°")
                    print("  Velocidad inicial:", round(resultado[1], 4), "m/s\n")
                else:
                    print("Error en el cálculo.\n")
            else:
                print("Altura no válida.\n")
        else:
            print("Distancia no válida.\n")

print("Programa finalizado.")
