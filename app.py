from flask import Flask, render_template, request, jsonify
import hashlib
import itertools
import string
import time
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count
import math

app = Flask(__name__)

# ============================
#   HASHING FUNCTIONS
# ============================

def md5_hex_bytes(b):
    return hashlib.md5(b).hexdigest()

def sha256_hex_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha512_hex_bytes(b):   # ➕ SHA-512 agregado
    return hashlib.sha512(b).hexdigest()


# Selección automática del algoritmo ---------------------------
def get_hash_func(algoritmo):
    if algoritmo == 'md5':
        return md5_hex_bytes
    elif algoritmo == 'sha256':
        return sha256_hex_bytes
    elif algoritmo == 'sha512':            # ➕ SHA-512 agregado
        return sha512_hex_bytes
    else:
        raise ValueError("Algoritmo no soportado")


# ============================
#   BRUTE FORCE CHUNK
# ============================

def probar_chunk(args):
    objetivo_hex, charset, length, start_idx, end_idx, algoritmo = args
    hash_func = get_hash_func(algoritmo)

    intentos_locales = 0
    combinaciones = itertools.product(charset, repeat=length)

    # Saltar hasta start_idx
    for _ in range(start_idx):
        next(combinaciones, None)
 
    for i, combo in enumerate(combinaciones):
        if i >= (end_idx - start_idx):
            break
        intentos_locales += 1
        candidato = ''.join(combo)
        if hash_func(candidato.encode('utf-8')) == objetivo_hex:
            return candidato, intentos_locales

    return None, intentos_locales


# ============================
# MULTICORE BRUTE FORCE
# ============================

def fuerza_bruta_multinucleo(objetivo_hex, charset, max_len, algoritmo='md5', num_cores=None):

    if num_cores is None:
        num_cores = cpu_count()

    intentos_totales = 0
    t0 = time.time()
    timestamp_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"🔥 Usando {num_cores} núcleos para la búsqueda")

    for length in range(1, max_len + 1):
        total_combos = len(charset) ** length
        print(f"📊 Longitud {length}: {total_combos:,} combinaciones")

        chunk_size = math.ceil(total_combos / num_cores)
        tasks = []

        for i in range(num_cores):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, total_combos)

            if start_idx >= total_combos:
                break

            tasks.append((objetivo_hex, charset, length, start_idx, end_idx, algoritmo))

        # correr en paralelo
        with Pool(processes=num_cores) as pool:
            resultados = pool.map(probar_chunk, tasks)

        for resultado, intentos in resultados:
            intentos_totales += intentos
            if resultado is not None:
                timestamp_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return resultado, intentos_totales, time.time() - t0, timestamp_inicio, timestamp_fin

    timestamp_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return None, intentos_totales, time.time() - t0, timestamp_inicio, timestamp_fin


# ============================
# SINGLE CORE BRUTE FORCE
# ============================

def fuerza_bruta_simple(objetivo_hex, charset, max_len, algoritmo='md5'):
    intentos = 0
    t0 = time.time()
    timestamp_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hash_func = get_hash_func(algoritmo)

    for L in range(1, max_len + 1):
        for combo in itertools.product(charset, repeat=L):
            intentos += 1
            candidato = ''.join(combo)
            if hash_func(candidato.encode("utf-8")) == objetivo_hex:
                timestamp_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return candidato, intentos, time.time() - t0, timestamp_inicio, timestamp_fin

    timestamp_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return None, intentos, time.time() - t0, timestamp_inicio, timestamp_fin


# ============================
#  RUTAS FLASK
# ============================

@app.route('/')
def main():
    return render_template('index.html', num_cores=cpu_count())


@app.route('/generar', methods=['POST'])
def generar_hash():
    try:
        data = request.get_json()
        texto = data['texto']
        algoritmo = data.get('algoritmo', 'md5')
        incluir_timestamp = data.get('incluir_timestamp', False)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Seleccionar función hash
        hash_func = get_hash_func(algoritmo)

        # Hash normal
        hash_normal = hash_func(texto.encode('utf-8'))

        # Hash con timestamp
        texto_con_timestamp = None
        hash_con_timestamp = None

        if incluir_timestamp:
            texto_con_timestamp = f"{texto}_{timestamp}"
            hash_con_timestamp = hash_func(texto_con_timestamp.encode('utf-8'))

        return jsonify({
    'texto': texto,
    'algoritmo': algoritmo.upper(),
    'hash': hash_normal,
    'longitud': len(hash_normal),  # ✔️ AÑADIDO
    'timestamp': timestamp,
    'incluir_timestamp': incluir_timestamp,
    'texto_con_timestamp': texto_con_timestamp,
    'hash_con_timestamp': hash_con_timestamp,
    'longitud_con_timestamp': len(hash_con_timestamp) if hash_con_timestamp else None  # ✔️ AÑADIDO
})


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/crack', methods=['POST'])
def crack():
    try:
        data = request.get_json()
        objetivo = data['hash'].lower().strip()
        max_len = int(data['maxLen'])
        charset_options = data['charset']
        algoritmo = data.get('algoritmo', 'md5')
        usar_multinucleo = data.get('multinucleo', True)
        num_cores = data.get('num_cores', None)

        # Charset
        charset = ""
        if 'lowercase' in charset_options:
            charset += string.ascii_lowercase
        if 'uppercase' in charset_options:
            charset += string.ascii_uppercase
        if 'digits' in charset_options:
            charset += string.digits

        if usar_multinucleo:
            encontrado, intentos, tiempo, t_ini, t_fin = fuerza_bruta_multinucleo(
                objetivo, charset, max_len, algoritmo, num_cores
            )
        else:
            encontrado, intentos, tiempo, t_ini, t_fin = fuerza_bruta_simple(
                objetivo, charset, max_len, algoritmo
            )

        return jsonify({
            'encontrado': encontrado is not None,
            'texto': encontrado,
            'intentos': intentos,
            'tiempo': tiempo,
            'timestamp_inicio': t_ini,
            'timestamp_fin': t_fin,
            'algoritmo': algoritmo.upper(),
            'modo': "MULTINÚCLEO" if usar_multinucleo else "SIMPLE"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================
#   MAIN
# ============================

if __name__ == "__main__":
    print(f"💻 CPU disponibles: {cpu_count()} núcleos")
    app.run(debug=True, host='0.0.0.0', port=5000)
