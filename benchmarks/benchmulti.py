#!/usr/bin/env python3
import hashlib
import multiprocessing as mp
import time

ITERACIONES_POR_PROCESO = 3_000_000  # 3 millones por núcleo

def sha_worker(_):
    data = b"jotage_power_test"
    h = None
    for _ in range(ITERACIONES_POR_PROCESO):
        h = hashlib.sha256(data).digest()
    return True

def main():
    print("=== BENCHMARK MULTINÚCLEO ===")

    nucleos = int(input("¿Cuántos núcleos usar? "))

    print(f"Usando {nucleos} proceso(s), {ITERACIONES_POR_PROCESO:,} hashes cada uno...")

    t0 = time.time()

    with mp.Pool(nucleos) as pool:
        pool.map(sha_worker, range(nucleos))

    t = time.time() - t0

    total_hashes = nucleos * ITERACIONES_POR_PROCESO
    print(f"\nTiempo total: {t:.2f} segundos")
    print(f"Hashes totales: {total_hashes:,}")
    print(f"Hashes por segundo global: {total_hashes / t:,.0f} H/s")

if __name__ == "__main__":
    main()
