from flask import Flask, render_template

programa = Flask(__name__)

@programa.route('/')
def index():
    return render_template("login.html")

if __name__ == '__main__':
    programa.run(host='0.0.0.0', debug=True, port='8080')

import numpy as np
import matplotlib.pyplot as plt

# # Crear una matriz de ejemplo
# matriz = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# # Imprimir la matriz
# print("Matriz original:")
# print(matriz)

# # Seleccionar un valor específico en la matriz
# valor = matriz[1, 2]
# print("\nValor seleccionado:", valor)

# # Seleccionar una fila específica en la matriz
# fila = matriz[0]
# print("\nFila seleccionada:", fila)

# # Seleccionar una columna específica en la matriz
# columna = matriz[:, 1]
# print("\nColumna seleccionada:", columna)

# # Graficar los valores de la matriz
# plt.imshow(matriz, cmap='viridis')
# plt.colorbar()
# plt.show()
