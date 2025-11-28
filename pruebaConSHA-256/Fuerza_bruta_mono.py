#!/usr/bin/env python3
# bruteforce_simple.py
import hashlib
import itertools
import string
import time

def sha256_hex_bytes(b):
    return hashlib.sha256(b).hexdigest()

def intentar_fuerza_bruta(objetivo_hex, charset, max_len):
    intento = 0
    t0 = time.time()
    for length in range(1, max_len + 1):
        for combo in itertools.product(charset, repeat=length):
            intento += 1
            candidate = ''.join(combo)
            if sha256_hex_bytes(candidate.encode('utf-8')) == objetivo_hex:
                return candidate, intento, time.time() - t0
    return None, intento, time.time() - t0

def main():
    print("=== Fuerza bruta simple (single-process) ===")
    with open("guardarHashes.txt", "r", encoding="utf-8") as f:
        objetivo = f.read().strip().lower()
    print("Hash objetivo:", objetivo)
    # Charset por defecto: letras minusculas + digitos. Ajusta si quieres.
    charset = string.ascii_lowercase #+ string.ascii_uppercase + string.digits
    print("Charset:", charset)
    max_len = int(input("Longitud máxima a probar (ej 4): ").strip())
    print("Comenzando (puede tardar)...")
    found, attempts, elapsed = intentar_fuerza_bruta(objetivo, charset, max_len)
    if found:
        print(f"\nENCONTRADO: '{found}' (intentos: {attempts}, tiempo: {elapsed:.2f}s)")
    else:
        print(f"\nNo encontrado (intentos: {attempts}, tiempo: {elapsed:.2f}s).")

if __name__ == "__main__":
    main()
