"""
Generador de Dataset - Aprendizaje Supervisado
================================================
Genera un dataset sintetico de rutas de TransMilenio usando el
sistema de busqueda A* de la Actividad 2 como fuente de datos.

Cada fila del dataset representa una ruta entre dos estaciones,
con caracteristicas extraidas y una etiqueta de categoria de duracion.

Autor: Cristian David Alvis Ortiz
Materia: Inteligencia Artificial - 2026-1
Actividad: 3 - Metodos de Aprendizaje Supervisado
"""

import csv
import random
import io
import contextlib

# Suprimir prints de transmilenio_rutas durante la generacion masiva
with contextlib.redirect_stdout(io.StringIO()):
    from transmilenio_rutas import (
        MotorInferencia,
        buscar_ruta_a_estrella as _buscar_ruta_a_estrella,
        ESTACIONES,
        heuristica,
    )


def buscar_ruta_a_estrella(motor, origen, destino):
    """Wrapper que silencia los prints del A*."""
    with contextlib.redirect_stdout(io.StringIO()):
        return _buscar_ruta_a_estrella(motor, origen, destino)

# Semilla para reproducibilidad
random.seed(42)

# Numero de muestras a generar
N_MUESTRAS = 1500

# Categorias de tiempo
UMBRAL_RAPIDO = 25.0   # minutos
UMBRAL_MEDIO = 50.0    # minutos


def calcular_distancia_geografica(origen: str, destino: str) -> float:
    """Calcula la distancia en km entre dos estaciones usando coordenadas GPS."""
    if origen not in ESTACIONES or destino not in ESTACIONES:
        return 0.0

    lat1, lon1 = ESTACIONES[origen]
    lat2, lon2 = ESTACIONES[destino]

    # Distancia euclidiana en grados, convertida a km (1 grado ~ 111 km)
    dist_grados = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
    return dist_grados * 111


def contar_transbordos(ruta: list) -> int:
    """Cuenta el numero de transbordos en una ruta."""
    troncales = []
    for _, troncal, _ in ruta:
        if troncal != "Inicio":
            if not troncales or troncales[-1] != troncal:
                troncales.append(troncal)
    return max(0, len(troncales) - 1)


def contar_troncales(ruta: list) -> int:
    """Cuenta el numero de troncales distintas usadas."""
    troncales_unicas = set()
    for _, troncal, _ in ruta:
        if troncal != "Inicio":
            troncales_unicas.add(troncal)
    return len(troncales_unicas)


def es_portal(estacion: str) -> int:
    """Retorna 1 si la estacion es un portal, 0 si no."""
    return 1 if "Portal" in estacion else 0


def aplicar_factor_tiempo(tiempo_base: float, hora: int, dia_semana: int) -> float:
    """Aplica factor de variacion segun hora del dia y dia de la semana.

    Simula el efecto del trafico real:
    - Hora pico (6-8 AM, 5-8 PM): tiempos aumentan
    - Hora valle: tiempos cercanos al estimado
    - Fin de semana: tiempos menores
    """
    # Factor por hora
    if 6 <= hora <= 8 or 17 <= hora <= 20:
        # Hora pico
        factor_hora = random.uniform(1.25, 1.55)
    elif 9 <= hora <= 16:
        # Hora valle dia
        factor_hora = random.uniform(0.95, 1.10)
    elif 21 <= hora <= 23 or 5 <= hora <= 5:
        # Noche/madrugada
        factor_hora = random.uniform(0.85, 1.00)
    else:
        # Madrugada profunda (servicio limitado)
        factor_hora = random.uniform(0.80, 0.95)

    # Factor por dia (5=sabado, 6=domingo)
    if dia_semana == 6:  # Domingo
        factor_dia = 0.80
    elif dia_semana == 5:  # Sabado
        factor_dia = 0.90
    else:  # Lunes a viernes
        factor_dia = 1.0

    # Ruido aleatorio
    ruido = random.uniform(0.92, 1.08)

    return tiempo_base * factor_hora * factor_dia * ruido


def categorizar_tiempo(tiempo: float) -> str:
    """Categoriza el tiempo de viaje en Rapido / Medio / Lento."""
    if tiempo < UMBRAL_RAPIDO:
        return "Rapido"
    elif tiempo < UMBRAL_MEDIO:
        return "Medio"
    else:
        return "Lento"


def generar_muestra(motor: MotorInferencia, estaciones_lista: list) -> dict | None:
    """Genera una muestra (fila) del dataset.

    Selecciona dos estaciones aleatorias, calcula la ruta optima con A*
    y extrae las features y la etiqueta.
    """
    # Seleccionar origen y destino aleatorios distintos
    origen, destino = random.sample(estaciones_lista, 2)

    # Calcular ruta con A*
    ruta = buscar_ruta_a_estrella(motor, origen, destino)
    if ruta is None or len(ruta) < 2:
        return None

    # Tiempo base segun A*
    tiempo_base = ruta[-1][2]

    # Variables temporales aleatorias
    hora = random.randint(5, 23)
    dia_semana = random.randint(0, 6)

    # Aplicar factor de variacion al tiempo
    tiempo_real = aplicar_factor_tiempo(tiempo_base, hora, dia_semana)

    # Extraer features
    num_estaciones = len(ruta)
    num_transbordos = contar_transbordos(ruta)
    num_troncales = contar_troncales(ruta)
    distancia_km = calcular_distancia_geografica(origen, destino)
    es_hora_pico = 1 if (6 <= hora <= 8 or 17 <= hora <= 20) else 0
    es_fin_semana = 1 if dia_semana >= 5 else 0
    origen_es_portal = es_portal(origen)
    destino_es_portal = es_portal(destino)
    num_portales = origen_es_portal + destino_es_portal

    return {
        "origen": origen,
        "destino": destino,
        "num_estaciones": num_estaciones,
        "num_transbordos": num_transbordos,
        "num_troncales": num_troncales,
        "distancia_km": round(distancia_km, 3),
        "hora_dia": hora,
        "dia_semana": dia_semana,
        "es_hora_pico": es_hora_pico,
        "es_fin_semana": es_fin_semana,
        "num_portales": num_portales,
        "tiempo_minutos": round(tiempo_real, 2),
        "categoria": categorizar_tiempo(tiempo_real),
    }


def generar_dataset(n_muestras: int = N_MUESTRAS, archivo_salida: str = "dataset_rutas.csv"):
    """Genera el dataset completo y lo guarda en CSV."""
    print(f"\n{'='*65}")
    print(f"  GENERADOR DE DATASET - TransMilenio Bogota")
    print(f"  Actividad 3 - Aprendizaje Supervisado")
    print(f"{'='*65}\n")

    motor = MotorInferencia()
    estaciones_lista = sorted(ESTACIONES.keys())

    print(f"\n[INFO] Generando {n_muestras} muestras...")
    print(f"[INFO] Total estaciones disponibles: {len(estaciones_lista)}")

    muestras = []
    intentos = 0
    max_intentos = n_muestras * 2

    while len(muestras) < n_muestras and intentos < max_intentos:
        muestra = generar_muestra(motor, estaciones_lista)
        intentos += 1
        if muestra is not None:
            muestras.append(muestra)
            if len(muestras) % 100 == 0:
                print(f"  Generadas {len(muestras)}/{n_muestras} muestras...")

    print(f"\n[OK] Total muestras generadas: {len(muestras)}")
    print(f"[OK] Intentos realizados: {intentos}")

    # Guardar como CSV
    if muestras:
        campos = list(muestras[0].keys())
        with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(muestras)

        print(f"[OK] Dataset guardado en: {archivo_salida}")

        # Estadisticas basicas
        print(f"\n{'-'*65}")
        print(f"  ESTADISTICAS DEL DATASET")
        print(f"{'-'*65}")
        print(f"  Total filas: {len(muestras)}")
        print(f"  Total columnas: {len(campos)}")

        # Distribucion de categorias
        cat_counts = {}
        for m in muestras:
            cat = m["categoria"]
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        print(f"\n  Distribucion de categorias:")
        for cat in ["Rapido", "Medio", "Lento"]:
            count = cat_counts.get(cat, 0)
            pct = (count / len(muestras)) * 100
            print(f"    {cat:10}: {count:5} ({pct:5.1f}%)")

        # Stats de tiempo
        tiempos = [m["tiempo_minutos"] for m in muestras]
        print(f"\n  Tiempo de viaje (minutos):")
        print(f"    Minimo:   {min(tiempos):.2f}")
        print(f"    Maximo:   {max(tiempos):.2f}")
        print(f"    Promedio: {sum(tiempos)/len(tiempos):.2f}")

        # Stats de features
        print(f"\n  Estaciones por ruta:")
        ests = [m["num_estaciones"] for m in muestras]
        print(f"    Min: {min(ests)}, Max: {max(ests)}, Prom: {sum(ests)/len(ests):.1f}")

        print(f"\n  Transbordos por ruta:")
        trans = [m["num_transbordos"] for m in muestras]
        print(f"    Min: {min(trans)}, Max: {max(trans)}, Prom: {sum(trans)/len(trans):.1f}")

        print(f"\n{'='*65}\n")


if __name__ == "__main__":
    generar_dataset()
