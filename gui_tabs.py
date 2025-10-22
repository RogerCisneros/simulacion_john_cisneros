import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  # necesario para el export ejemplo
from generador_numeros import lcg_generate, multiplicative_lcg, middle_square
from pruebas import chi_squared_test, ks_test, runs_test
from variables import generate_uniform, generate_exponential, generate_normal_boxmuller, generate_poisson
from utils_export import export_results_to_excel


# ======================================================
# 🌟 GENERADOR DE NÚMEROS
# ======================================================
class GeneratorWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.parent = parent  # referencia al menú principal
        self.title('Generador - John Cisneros')
        self.geometry('750x500')

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, anchor='nw')

        tk.Label(frame, text='Método:').grid(row=0, column=0)
        self.method = tk.StringVar(value='lcg')
        tk.Radiobutton(frame, text='LCG', variable=self.method, value='lcg').grid(row=0, column=1)
        tk.Radiobutton(frame, text='Multiplicativo', variable=self.method, value='mult').grid(row=0, column=2)
        tk.Radiobutton(frame, text='Middle-Square', variable=self.method, value='mid').grid(row=0, column=3)

        tk.Label(frame, text='n:').grid(row=1, column=0)
        self.n_entry = tk.Entry(frame); self.n_entry.grid(row=1, column=1)
        tk.Label(frame, text='semilla:').grid(row=1, column=2)
        self.seed_entry = tk.Entry(frame); self.seed_entry.grid(row=1, column=3)

        tk.Label(frame, text='a:').grid(row=2, column=0)
        self.a_entry = tk.Entry(frame); self.a_entry.grid(row=2, column=1)
        tk.Label(frame, text='c:').grid(row=2, column=2)
        self.c_entry = tk.Entry(frame); self.c_entry.grid(row=2, column=3)
        tk.Label(frame, text='m:').grid(row=3, column=0)
        self.m_entry = tk.Entry(frame); self.m_entry.grid(row=3, column=1)

        tk.Button(frame, text='Generar', command=self._generar).grid(row=4, column=0, pady=8)
        tk.Button(frame, text='Exportar tabla', command=self._export).grid(row=4, column=1)
        tk.Button(frame, text='Mostrar histograma', command=self._hist).grid(row=4, column=2)

        self.last = None

    def _generar(self):
        try:
            n = int(self.n_entry.get())
            seed = int(self.seed_entry.get()) if self.seed_entry.get() else 1
            method = self.method.get()

            if method == 'lcg':
                a = int(self.a_entry.get()) if self.a_entry.get() else 1664525
                c = int(self.c_entry.get()) if self.c_entry.get() else 1013904223
                m = int(self.m_entry.get()) if self.m_entry.get() else 2**32
                arr = lcg_generate(n, seed, a, c, m)
            elif method == 'mult':
                a = int(self.a_entry.get()) if self.a_entry.get() else 1103515245
                m = int(self.m_entry.get()) if self.m_entry.get() else 2**31
                arr = multiplicative_lcg(n, seed, a, m)
            else:
                arr = middle_square(n, seed)

            self.last = arr

            # 🔥 Guardar en el menú principal para las demás ventanas
            if self.parent is not None:
                self.parent.datos_generados = arr

            messagebox.showinfo('Hecho', f'Generados {len(arr)} números.\nPrimeros 8: {arr[:8]}')

        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _hist(self):
        if self.last is None:
            messagebox.showerror('Error', 'Genera números primero')
            return
        plt.figure()
        plt.hist(self.last, bins=30)
        plt.title('Histograma - Generador')
        plt.show()

    def _export(self):
        if self.last is None:
            messagebox.showerror('Error', 'Genera números primero')
            return
        path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel', '*.xlsx')])
        if not path:
            return
        df = pd.DataFrame({'r': self.last})
        export_results_to_excel(df, path)
        messagebox.showinfo('Exportado', f'Archivo guardado en {path}')


# ======================================================
# 🧪 PRUEBAS ESTADÍSTICAS
# ======================================================
class TestsWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.parent = parent
        self.title('Pruebas - John Cisneros')
        self.geometry('600x350')

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text='Esta ventana usa los datos generados en "Generador"').pack()
        tk.Button(frame, text='Chi-cuadrado (p=10)', command=self._chi).pack(pady=6)
        tk.Button(frame, text='KS', command=self._ks).pack(pady=6)
        tk.Button(frame, text='Runs', command=self._runs).pack(pady=6)

    def _get_data(self):
        # 🔥 Leer los datos almacenados en el menú principal
        if self.parent is not None and hasattr(self.parent, 'datos_generados'):
            return self.parent.datos_generados
        return None

    def _chi(self):
        data = self._get_data()
        if data is None or len(data) == 0:
            messagebox.showerror('Error', 'No hay datos generados (usa la pestaña Generador primero)')
            return
        stat, p, exp = chi_squared_test(data, bins=10)
        messagebox.showinfo('Chi-cuadrado', f'χ²={stat:.4f}\nP-valor≈{p:.4f}\nEsperado por clase={exp}')

    def _ks(self):
        data = self._get_data()
        if data is None or len(data) == 0:
            messagebox.showerror('Error', 'No hay datos generados (usa la pestaña Generador primero)')
            return
        stat, p = ks_test(data)
        messagebox.showinfo('Kolmogorov-Smirnov', f'D={stat:.4f}\nP-valor≈{p:.4f}')

    def _runs(self):
        data = self._get_data()
        if data is None or len(data) == 0:
            messagebox.showerror('Error', 'No hay datos generados (usa la pestaña Generador primero)')
            return
        z, p = runs_test(data)
        messagebox.showinfo('Prueba de Corridas', f'Z={z:.4f}\nP-valor≈{p:.4f}')


# ======================================================
# ⚙️ VARIABLES ALEATORIAS
# ======================================================
class VariablesWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.parent = parent
        self.title('Variables - John Cisneros')
        self.geometry('700x450')
        f = tk.Frame(self)
        f.pack(padx=10, pady=10)

        tk.Label(f, text='Uniforme [a,b]').grid(row=0, column=0)
        tk.Label(f, text='a:').grid(row=1, column=0); self.ua = tk.Entry(f); self.ua.grid(row=1, column=1)
        tk.Label(f, text='b:').grid(row=1, column=2); self.ub = tk.Entry(f); self.ub.grid(row=1, column=3)
        tk.Button(f, text='Generar uniforme', command=self._gen_unif).grid(row=1, column=4)

        tk.Label(f, text='Exponencial λ').grid(row=2, column=0)
        tk.Label(f, text='λ:').grid(row=3, column=0); self.el = tk.Entry(f); self.el.grid(row=3, column=1)
        tk.Button(f, text='Generar exponencial', command=self._gen_exp).grid(row=3, column=2)

        tk.Label(f, text='Normal μ σ').grid(row=4, column=0)
        tk.Label(f, text='μ:').grid(row=5, column=0); self.mu = tk.Entry(f); self.mu.grid(row=5, column=1)
        tk.Label(f, text='σ:').grid(row=5, column=2); self.sigma = tk.Entry(f); self.sigma.grid(row=5, column=3)
        tk.Button(f, text='Generar normal', command=self._gen_norm).grid(row=5, column=4)

        tk.Label(f, text='Poisson λ').grid(row=6, column=0)
        tk.Label(f, text='λ:').grid(row=7, column=0); self.pl = tk.Entry(f); self.pl.grid(row=7, column=1)
        tk.Button(f, text='Generar poisson', command=self._gen_poi).grid(row=7, column=2)

    def _gen_unif(self):
        try:
            a = float(self.ua.get()); b = float(self.ub.get())
            data = generate_uniform(a, b, 1000)
            plt.figure(); plt.hist(data, bins=30); plt.title('Uniforme'); plt.show()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _gen_exp(self):
        try:
            l = float(self.el.get())
            data = generate_exponential(l, 1000)
            plt.figure(); plt.hist(data, bins=30); plt.title('Exponencial'); plt.show()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _gen_norm(self):
        try:
            mu = float(self.mu.get()); sigma = float(self.sigma.get())
            data = generate_normal_boxmuller(mu, sigma, 1000)
            plt.figure(); plt.hist(data, bins=30); plt.title('Normal'); plt.show()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _gen_poi(self):
        try:
            l = float(self.pl.get())
            data = generate_poisson(l, 1000)
            plt.figure(); plt.hist(data, bins=30); plt.title('Poisson'); plt.show()
        except Exception as e:
            messagebox.showerror('Error', str(e))


# ======================================================
# 💾 EXPORTAR / LEER
# ======================================================
class ExportWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.parent = parent
        self.title('Exportar / Leer - John Cisneros')
        self.geometry('600x300')
        f = tk.Frame(self)
        f.pack(padx=10, pady=10)
        tk.Button(f, text='Leer Excel (preview)', command=self._read).pack(pady=6)
        tk.Button(f, text='Crear ejemplo de resultados', command=self._create_example).pack(pady=6)

    def _read(self):
        path = filedialog.askopenfilename(filetypes=[('Excel', '*.xlsx;*.xls')])
        if not path:
            return
        try:
            xls = pd.ExcelFile(path)
            s = xls.sheet_names
            info = {}
            for sh in s:
                df = pd.read_excel(xls, sheet_name=sh)
                info[sh] = {'shape': df.shape, 'num_cols': df.select_dtypes(include=['number']).columns.tolist()}
            messagebox.showinfo('Preview', str(info))
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _create_example(self):
        df = pd.DataFrame({'i': list(range(1, 11)), 'Xi': np.arange(10), 'ri': np.random.rand(10)})
        path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel', '*.xlsx')])
        if not path:
            return
        export_results_to_excel(df, path)
        messagebox.showinfo('Creado', f'Archivo de ejemplo creado en {path}')
