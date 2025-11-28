#!/usr/bin/env python3
# guardar_hash.py
import hashlib
import getpass

def calcular_sha256_hex(texto: str) -> str:
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def main():
    print("=== Guardar hash SHA-256 ===")
    # usa getpass si no quieres que aparezca en pantalla
    texto = getpass.getpass("Ingresa la frase/contraseña a hashear: ")
    h = calcular_sha256_hex(texto)
    nombre_archivo = "guardarHashes.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(h + "\n")
    print(f"Hash de '{texto}' guardado en '{nombre_archivo}':\n{h}")

if __name__ == "__main__":
    main()
    