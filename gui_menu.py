import tkinter as tk
from tkinter import ttk
from gui_tabs import GeneratorWindow, TestsWindow, VariablesWindow, ExportWindow

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulación - Menú Principal")
        self.root.geometry("500x400")

        # Aquí guardaremos los datos generados para compartir entre ventanas
        self.datos_generados = []

        # Estilo general
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=8)

        # Título principal
        ttk.Label(
            self.root, 
            text="Laboratorio de Simulación", 
            font=("Arial", 18, "bold"), 
            anchor="center"
        ).pack(pady=20)

        # Botones principales
        ttk.Button(
            self.root, 
            text="🔢 Generador de Números", 
            command=self.abrir_generador
        ).pack(pady=10, fill="x", padx=80)

        ttk.Button(
            self.root, 
            text="🧮 Pruebas Estadísticas", 
            command=self.abrir_pruebas
        ).pack(pady=10, fill="x", padx=80)

        ttk.Button(
            self.root, 
            text="⚙️ Variables Aleatorias", 
            command=self.abrir_variables
        ).pack(pady=10, fill="x", padx=80)

        ttk.Button(
            self.root, 
            text="💾 Exportar / Leer Datos", 
            command=self.abrir_exportar
        ).pack(pady=10, fill="x", padx=80)

        ttk.Button(
            self.root, 
            text="❌ Salir", 
            command=self.root.quit
        ).pack(pady=20, fill="x", padx=80)

        self.root.mainloop()

    # ======== Funciones para abrir cada ventana ========

    def abrir_generador(self):
        ventana = tk.Toplevel(self.root)
        GeneratorWindow(ventana, self)  # se pasa la referencia a self (menú principal)
        ventana.transient(self.root)
        ventana.grab_set()

    def abrir_pruebas(self):
        ventana = tk.Toplevel(self.root)
        TestsWindow(ventana, self)
        ventana.transient(self.root)
        ventana.grab_set()

    def abrir_variables(self):
        ventana = tk.Toplevel(self.root)
        VariablesWindow(ventana, self)
        ventana.transient(self.root)
        ventana.grab_set()

    def abrir_exportar(self):
        ventana = tk.Toplevel(self.root)
        ExportWindow(ventana, self)
        ventana.transient(self.root)
        ventana.grab_set()


if __name__ == "__main__":
    MainMenu()
