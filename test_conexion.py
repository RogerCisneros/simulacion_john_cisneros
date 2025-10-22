import tkinter as tk
from tkinter import messagebox

datos_generados = []  # Variable global

def generar():
    global datos_generados
    datos_generados = [i/10 for i in range(10)]  # Genera 10 números de ejemplo
    messagebox.showinfo("Hecho", f"Generados {len(datos_generados)} números")

def pruebas():
    if not datos_generados:
        messagebox.showerror("Error", "No hay datos generados (abre Generador)")
    else:
        messagebox.showinfo("Pruebas", f"Usando {len(datos_generados)} datos: {datos_generados[:5]}")

root = tk.Tk()
root.title("Prueba de conexión")

tk.Button(root, text="Generar", command=generar).pack(padx=20, pady=10)
tk.Button(root, text="Pruebas", command=pruebas).pack(padx=20, pady=10)

root.mainloop()
