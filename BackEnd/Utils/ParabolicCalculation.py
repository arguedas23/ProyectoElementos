import matplotlib
matplotlib.use('Agg')  # Para servidor sin interfaz gráfica
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generar_grafica_base64(distancia, altura, angulo, velocidad):
    """Genera una gráfica de trayectoria y la devuelve como base64 para el servidor web"""
    g = 9.77589
    
    # Calcular tiempo total de vuelo
    t_total = (2 * velocidad * sin_grados(angulo)) / g
    
    # Calcular puntos de la trayectoria
    x_data = []
    y_data = []
    
    t = 0
    dt = t_total / 50  # 50 puntos para suavizar la curva
    
    while t <= t_total:
        x = velocidad * cos_grados(angulo) * t
        y = velocidad * sin_grados(angulo) * t - 0.5 * g * t**2
        
        # Solo incluir puntos hasta que toque el suelo
        if y >= 0:
            x_data.append(x)
            y_data.append(y)
        
        t += dt
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, 'b-', linewidth=2, label='Trayectoria')
    plt.scatter([0, distancia], [0, 0], color='red', s=100, zorder=5, label='Puntos de referencia')
    plt.scatter([distancia/2], [altura], color='green', s=100, zorder=5, label='Altura máxima')
    
    # Línea punteada para altura máxima
    plt.axhline(y=altura, color='green', linestyle='--', alpha=0.5)
    plt.axvline(x=distancia/2, color='green', linestyle='--', alpha=0.5)
    
    plt.xlabel("Distancia (metros)")
    plt.ylabel("Altura (metros)")
    plt.title(f"Trayectoria Parabólica\nÁngulo: {angulo:.2f}°, Velocidad: {velocidad:.2f} m/s")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    
    # Convertir gráfica a base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{image_base64}"

