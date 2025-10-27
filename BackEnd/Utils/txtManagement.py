from Utils.ParabolicCalculation import calcular_tiro
import os

def guardar_datos(nombre_archivo, distancia, altura, angulo, velocidad):
    """Guarda una nueva combinación en el archivo de texto"""
    if type(nombre_archivo) != str:
        return "Error01"

    manejador = open(nombre_archivo, "a")
    linea = str(distancia) + "," + str(altura) + "," + str(angulo) + "," + str(velocidad) + "\n"
    manejador.write(linea)
    manejador.close()
    return None


def cargar_datos(nombre_archivo):
    """Carga todas las líneas del archivo y las convierte en lista"""
    if type(nombre_archivo) != str:
        return "Error02"

    manejador = open(nombre_archivo, "r")
    contenido = manejador.readlines()
    manejador.close()

    lista = []
    i = 0
    while i < len(contenido):
        linea = contenido[i].strip()
        if linea != "":
            partes = linea.split(",")
            if len(partes) == 4:
                lista.append(partes)
        i = i + 1
    return lista


def buscar_datos(nombre_archivo, distancia, altura):
    """Busca si ya existe la combinación (distancia, altura)"""
    if type(nombre_archivo) != str:
        return "Error03"
    registros = cargar_datos(nombre_archivo)
    i = 0
    while i < len(registros):
        registro = registros[i]
        if float(registro[0]) == distancia:
            if float(registro[1]) == altura:
                return [float(registro[2]), float(registro[3])]
        i = i + 1
    return None


def obtener_resultado(nombre_archivo, distancia, altura):
    """
    Si la combinación ya está guardada, la muestra.
    Si no está, la calcula con calcular_tiro() y la guarda.
    """
    if type(nombre_archivo) != str:
        return "Error04"

    existente = buscar_datos(nombre_archivo, distancia, altura)
    if existente != None:
        print("Resultado obtenido del archivo.")
        return existente

    nuevo = calcular_tiro(distancia, altura)
    if nuevo != "Error01":
        guardar_datos(nombre_archivo, distancia, altura, nuevo[0], nuevo[1])
        print("Resultado calculado y guardado.")
        return nuevo
    return "Error05"
