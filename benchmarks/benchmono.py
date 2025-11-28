#!/usr/bin/env python3
import hashlib
import time

def sha_benchmark(iteraciones):
    data = b"jotage_power_test"
    t0 = time.time()
    h = None

    for _ in range(iteraciones):
        h = hashlib.sha256(data).digest()

    return time.time() - t0

def main():
    print("=== BENCHMARK MONONÚCLEO ===")
    iteraciones = 10_000_000  # 10 millones

    print(f"Ejecutando {iteraciones:,} hashes SHA-256...")
    t = sha_benchmark(iteraciones)

    print(f"\nTiempo total: {t:.2f} segundos")
    print(f"Hashes por segundo: {iteraciones / t:,.0f} H/s")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import hashlib
import time

def sha_benchmark(iteraciones):
    data = b"jotage_power_test"
    t0 = time.time()
    h = None

    for _ in range(iteraciones):
        h = hashlib.sha256(data).digest()

    return time.time() - t0

def main():
    print("=== BENCHMARK MONONÚCLEO ===")
    iteraciones = 10_000_000  # 10 millones

    print(f"Ejecutando {iteraciones:,} hashes SHA-256...")
    t = sha_benchmark(iteraciones)

    print(f"\nTiempo total: {t:.2f} segundos")
    print(f"Hashes por segundo: {iteraciones / t:,.0f} H/s")

if __name__ == "__main__":
    main()
