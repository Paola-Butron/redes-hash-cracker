#!/usr/bin/env python3
# guardar_hash_md5.py
import hashlib
import getpass

def calcular_md5_hex(texto: str) -> str:
    """Devuelve el digest MD5 (hex) del texto dado."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

def main():
    print("=== Guardar hash MD5 ===")
    # getpass oculta la entrada en consola (útil si es contraseña)
    texto = getpass.getpass("Ingresa la frase/contraseña a hashear: ")
    h = calcular_md5_hex(texto)
    nombre_archivo = "guardarHashes.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(h + "\n")
    print(f"Hash de '{texto}' guardado en '{nombre_archivo}':\n{h}")

if __name__ == "__main__":
    main()
