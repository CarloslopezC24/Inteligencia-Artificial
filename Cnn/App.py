import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Preparar datos de MNIST
(mnist_train_x, mnist_train_y), (mnist_test_x, mnist_test_y) = tf.keras.datasets.mnist.load_data()
mnist_train_x = mnist_train_x[..., np.newaxis] / 255.0
mnist_test_x = mnist_test_x[..., np.newaxis] / 255.0

# Crear modelo CNN
cnn = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

cnn.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

cnn.fit(mnist_train_x, mnist_train_y, epochs=5, validation_split=0.1)
loss, acc = cnn.evaluate(mnist_test_x, mnist_test_y)
print(f"Precisión del modelo: {acc:.2%}")

# Obtener predicciones
predicciones = cnn.predict(mnist_test_x)
pred_clases = np.argmax(predicciones, axis=1)

# Función para graficar matriz de confusión
def mostrar_matriz_confusion():
    matriz = confusion_matrix(mnist_test_y, pred_clases)
    plt.figure(figsize=(8, 6))
    sns.heatmap(matriz, annot=True, fmt='d', cmap='YlGnBu', 
                xticklabels=range(10), yticklabels=range(10))
    plt.title("Matriz de Confusión")
    plt.xlabel("Etiqueta Predicha")
    plt.ylabel("Etiqueta Verdadera")
    plt.tight_layout()
    plt.show()

# Función para mostrar tabla con cantidades
def mostrar_tabla_cantidades():
    cantidades = [np.sum(mnist_test_y == i) for i in range(10)]
    ventana_sec = tk.Toplevel()
    ventana_sec.title("Cantidad de imágenes por dígito")
    tabla = ttk.Treeview(ventana_sec, columns=("Dígito", "Cantidad"), show='headings')
    tabla.heading("Dígito", text="Dígito")
    tabla.heading("Cantidad", text="Cantidad")
    for i in range(10):
        tabla.insert('', 'end', values=(i, cantidades[i]))
    tabla.pack(expand=True, fill='both')

# Interfaz gráfica
app = tk.Tk()
app.title("Análisis MNIST con CNN")
app.geometry("400x200")

tk.Button(app, text="Ver Matriz de Confusión", command=mostrar_matriz_confusion, height=2).pack(pady=10)
tk.Button(app, text="Ver Tabla de Cantidades", command=mostrar_tabla_cantidades, height=2).pack(pady=10)

app.mainloop()
