#importacion de Matplotlib

import matplotlib.pylot as plt

def generar_grafico():
    """
    Esta funcion utiliza los datos del usuario para generar un grafico utilizando matplotlib
    """
    x_data = []
    y_data = []

    print("Digite los datos del grafico (si desea finalizar, digite stop):")

    while True:
        x = input("Enter the x-value (or 'stop' to finish): ")
        if x.lower() == 'stop':
            break
        y = input("Enter the y-value: ")
        x_data.append(float(x))
        y_data.append(float(y))

    plt.figure(figsize=(8, 6))
    plt.plot(x_data, y_data)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("User-generated Graph")
    plt.grid(True)
    plt.show()


generar_grafico()
