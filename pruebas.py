import numpy as np
from scipy import stats
import json
import os
import tkinter as tk
from tkinter import messagebox


# --- FUNCIONES DE PRUEBAS ---
def chi_squared_test(data, bins=10):
    arr = np.asarray(data)
    if arr.max() > 1 or arr.min() < 0:
        arr = (arr - arr.min()) / (arr.max() - arr.min())
    counts, _ = np.histogram(arr, bins=bins)
    expected = len(arr) / bins
    chi2 = ((counts - expected) ** 2 / expected).sum()
    pvalue = 1 - stats.chi2.cdf(chi2, df=bins - 1)
    return chi2, pvalue, expected


def ks_test(data):
    arr = np.asarray(data)
    if arr.max() > 1 or arr.min() < 0:
        arr = (arr - arr.min()) / (arr.max() - arr.min())
    res = stats.kstest(arr, 'uniform')
    return res.statistic, res.pvalue


def runs_test(data):
    arr = np.asarray(data)
    med = np.median(arr)
    signs = arr > med
    n1 = signs.sum()
    n2 = (~signs).sum()
    runs = 1
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            runs += 1
    expected = 1 + 2 * n1 * n2 / (n1 + n2)
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1))
    if var <= 0:
        return 0.0, 1.0
    z = (runs - expected) / (var ** 0.5)
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p


# --- FUNCIONES PARA CARGAR DATOS ---
def cargar_datos_generados():
    """Lee el archivo datos_generados.json creado por el Generador"""
    ruta = os.path.join(os.path.dirname(__file__), "datos_generados.json")
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    return None


# --- INTERFAZ PRINCIPAL ---
def ejecutar_pruebas():
    datos = cargar_datos_generados()

    if not datos or len(datos) == 0:
        messagebox.showerror("Error", "No hay datos generados (abre el Generador primero).")
        return

    chi2, p_chi, _ = chi_squared_test(datos)
    ks_stat, p_ks = ks_test(datos)
    runs_stat, p_runs = runs_test(datos)

    msg = (
        f"Resultados de las pruebas de aleatoriedad:\n\n"
        f"Chi-cuadrado: {chi2:.4f}, p = {p_chi:.4f}\n"
        f"Kolmogorov-Smirnov: {ks_stat:.4f}, p = {p_ks:.4f}\n"
        f"Runs Test: {runs_stat:.4f}, p = {p_runs:.4f}"
    )

    messagebox.showinfo("Pruebas de Aleatoriedad", msg)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pruebas de Aleatoriedad - John Cisneros")

    tk.Label(root, text="Esta ventana usa datos generados en el Generador", pady=10).pack()
    tk.Button(root, text="Ejecutar Pruebas", command=ejecutar_pruebas, padx=20, pady=10).pack(pady=20)

    root.mainloop()
