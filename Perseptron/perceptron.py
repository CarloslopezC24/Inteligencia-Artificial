import requests
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

class Perceptron:
    def __init__(self, tasa_aprendizaje=1e-6, iteraciones=1000):
        self.lr = tasa_aprendizaje
        self.n_iter = iteraciones

    def entrenar(self, X, y):
        self.pesos = np.zeros(X.shape[1] + 1)  # +1 para el sesgo
        for _ in range(self.n_iter):
            for xi, objetivo in zip(X, y):
                salida = self.predecir(xi)
                error = objetivo - salida
                self.pesos[1:] += self.lr * error * xi
                self.pesos[0] += self.lr * error  # sesgo

    def entrada_neta(self, X):
        return np.dot(X, self.pesos[1:]) + self.pesos[0]

    def predecir(self, X):
        return self.entrada_neta(X)

class AplicacionPerceptron:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Modelo Lineal: Edad vs Ingreso")
        self.raiz.geometry("350x240")
        self.cargar_datos()
        self.entrenar_modelo()
        self.construir_interfaz()
        self.raiz.mainloop()

    def cargar_datos(self):
        url = "https://dummyjson.com/users?limit=100"
        respuesta = requests.get(url).json()

        self.edades, self.salarios = [], []
        self.nombres, self.trabajos, self.paises = [], [], []

        for usuario in respuesta["users"]:
            edad = usuario["age"]
            nombre = f"{usuario['firstName']} {usuario['lastName']}"
            puesto = usuario["company"]["title"]
            pais = usuario["address"]["country"]
            ingreso = edad * 1000 + np.random.randint(-5000, 5000)

            self.edades.append(edad)
            self.salarios.append(ingreso)
            self.nombres.append(nombre)
            self.trabajos.append(puesto)
            self.paises.append(pais)

        self.X = np.array(self.edades).reshape(-1, 1)
        self.y = np.array(self.salarios)

    def entrenar_modelo(self):
        self.modelo = Perceptron(tasa_aprendizaje=1e-6, iteraciones=50)
        self.modelo.entrenar(self.X, self.y)

    def construir_interfaz(self):
        marco = ttk.LabelFrame(self.raiz, text="Opciones")
        marco.pack(padx=15, pady=15, fill="both", expand=True)

        ttk.Label(marco, text="Relación: Edad → Ingreso estimado").pack(pady=10)

        ttk.Button(marco, text="Ver gráfica", command=self.mostrar_grafico).pack(pady=5)
        ttk.Button(marco, text="Ver tabla de datos", command=self.mostrar_tabla).pack(pady=5)

    def mostrar_grafico(self):
        predicciones = self.modelo.predecir(self.X)

        plt.figure(figsize=(8, 5))
        plt.scatter(self.X, self.y, color='blue', label="Datos reales")
        plt.plot(self.X, predicciones, color='red', label="Modelo Lineal")
        plt.xlabel("Edad")
        plt.ylabel("Ingreso (USD)")
        plt.title("Modelo Lineal: Edad vs Ingreso")
        plt.legend()
        plt.grid(True)

        m = self.modelo.pesos[1]
        b = self.modelo.pesos[0]
        plt.text(self.X.min(), self.y.max(), f"y = {m:.2f}x + {b:.2f}", color='green')

        plt.tight_layout()
        plt.show()

    def mostrar_tabla(self):
        ventana = tk.Toplevel(self.raiz)
        ventana.title("Listado de Usuarios")
        ventana.geometry("850x500")

        columnas = ("Nombre", "Edad", "Ingreso", "Trabajo", "País")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor=tk.CENTER)

        for edad, ingreso, nombre, trabajo, pais in zip(self.edades, self.salarios, self.nombres, self.trabajos, self.paises):
            tabla.insert("", tk.END, values=(nombre, edad, f"${ingreso:,.2f}", trabajo, pais))

        tabla.pack(expand=True, fill="both")

# Ejecutar la app
if __name__ == "__main__":
    AplicacionPerceptron()
