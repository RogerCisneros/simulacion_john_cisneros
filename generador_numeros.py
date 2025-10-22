import numpy as np
import json
import os

# ==============================
# MÉTODOS DE GENERACIÓN
# ==============================

def lcg_generate(n, seed, a=1664525, c=1013904223, m=2**32):
    """Generador congruencial lineal (LCG)"""
    nums = []
    x = int(seed)
    for _ in range(int(n)):
        x = (a * x + c) % m
        nums.append(x / m)
    return np.array(nums)

def multiplicative_lcg(n, seed, a=1103515245, m=2**31):
    """Generador congruencial multiplicativo"""
    nums = []
    x = int(seed)
    for _ in range(int(n)):
        x = (a * x) % m
        nums.append(x / m)
    return np.array(nums)

def middle_square(n, seed, k_digits=None):
    """Método del cuadrado medio"""
    s = str(seed)
    if k_digits is None:
        k = len(s)
        if k % 2 == 1:
            k += 1
    else:
        k = int(k_digits)

    x = int(seed)
    results = []
    for _ in range(int(n)):
        sq = str(x * x).zfill(2 * k)
        mid = sq[len(sq)//2 - k//2 : len(sq)//2 + k//2]
        x = int(mid)
        results.append(x / (10**k))
    return np.array(results)


# ==============================
# GUARDADO DE DATOS
# ==============================

def guardar_datos_generados(datos):
    """Guarda los números generados en un archivo JSON"""
    ruta = os.path.join(os.path.dirname(__file__), "datos_generados.json")
    with open(ruta, "w") as f:
        json.dump(datos.tolist(), f, indent=4)
    print(f"✅ {len(datos)} datos guardados en {ruta}")


# ==============================
# PRUEBA DIRECTA (solo si se ejecuta este archivo)
# ==============================

if __name__ == "__main__":
    # Ejemplo: genera 100 números usando LCG
    numeros = lcg_generate(100, seed=12345)

    # Guarda los datos en archivo JSON
    guardar_datos_generados(numeros)

    print("Primeros 5 números generados:", numeros[:5])
