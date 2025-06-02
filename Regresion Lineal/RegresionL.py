import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import ttk, messagebox

def cargar_datos():
    try:
        url = "https://dummyjson.com/users?limit=100"
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()['users']
    except Exception as e:
        messagebox.showerror("Error de red", f"No se pudo obtener datos: {e}")
        return pd.DataFrame()
    
    lista = []
    np.random.seed(0) 

    for usuario in datos:
        edad = usuario['age']
        salario = edad * 950 + np.random.randint(-4000, 4000)
        lista.append({
            'Nombre': f"{usuario['firstName']} {usuario['lastName']}",
            'Edad': edad,
            'Salario': salario,
            'Trabajo': usuario['company']['title'],
            'País': usuario['address']['country']
        })
    
    return pd.DataFrame(lista)

ventana = tk.Tk()
ventana.title("Edad vs Salario - Regresión Lineal")
ventana.geometry("350x250")

df = cargar_datos()

if df.empty:
    ventana.destroy()
    exit()

# Preparar modelo
X = df[['Edad']].values
y = df['Salario'].values
modelo = LinearRegression()
modelo.fit(X, y)

def ver_grafica():
    y_pred = modelo.predict(X)

    plt.figure(figsize=(8, 5))
    plt.scatter(df['Edad'], df['Salario'], color='blue', label="Datos reales")
    plt.plot(df['Edad'], y_pred, color='red', label="Regresión")
    plt.title("Relación Edad vs Salario")
    plt.xlabel("Edad")
    plt.ylabel("Salario (USD)")
    plt.legend()
    plt.grid(True)

    m = modelo.coef_[0]
    b = modelo.intercept_
    plt.text(df['Edad'].min(), df['Salario'].max(), f"y = {m:.2f}x + {b:.2f}", color='green')

    plt.tight_layout()
    plt.show()
  
def ver_tabla():
    top = tk.Toplevel(ventana)
    top.title("Listado de usuarios")
    top.geometry("850x500")

    tree = ttk.Treeview(top, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill='both')

titulo = tk.Label(ventana, text="Simulación: Regresión Lineal\nEdad vs Salario", font=("Arial", 12))
titulo.pack(pady=15)

boton1 = tk.Button(ventana, text="Ver Gráfica", command=ver_grafica, width=20)
boton1.pack(pady=10)

boton2 = tk.Button(ventana, text="Ver Listado de Datos", command=ver_tabla, width=20)
boton2.pack(pady=5)

ventana.mainloop()
