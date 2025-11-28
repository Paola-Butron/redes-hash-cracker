#!/usr/bin/env python3
# buscar_md5_simple.py
import hashlib
import itertools
import string
import time
import os

def md5_hex_bytes(b):
    return hashlib.md5(b).hexdigest()

def leer_hash_desde_archivo(ruta="guardarHashes.txt"):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read().strip().lower()

def fuerza_bruta_simple(objetivo_hex, charset, max_len):
    intentos = 0
    t0 = time.time()
    for L in range(1, max_len + 1):
        for combo in itertools.product(charset, repeat=L):
            intentos += 1
            candidato = ''.join(combo)
            if md5_hex_bytes(candidato.encode('utf-8')) == objetivo_hex:
                return candidato, intentos, time.time() - t0
    return None, intentos, time.time() - t0

def main():
    print("=== Buscar MD5 (simple) ===")
    objetivo = leer_hash_desde_archivo()
    print("Hash objetivo (MD5):", objetivo)
    # Charset por defecto: letras minúsculas (añade + string.digits si quieres)
    charset = string.ascii_lowercase
    print("Charset por defecto:", charset)
    max_len = int(input("Longitud máxima a probar (ej: 4): ").strip())
    print("Comenzando... (esto puede tardar según max_len y charset)")

    encontrado, intentos, tiempo = fuerza_bruta_simple(objetivo, charset, max_len)
    if encontrado:
        print(f"\nENCONTRADO: '{encontrado}'  (intentos: {intentos}, tiempo: {tiempo:.2f}s)")
    else:
        print(f"\nNo encontrado (intentados: {intentos}, tiempo: {tiempo:.2f}s).")

if __name__ == "__main__":
    main()
