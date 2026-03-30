"""
Sistema Inteligente de Rutas - TransMilenio Bogota
===================================================
Sistema basado en reglas logicas y busqueda heuristica (A*)
para encontrar la mejor ruta entre dos estaciones del sistema
de transporte masivo TransMilenio.

Componentes:
- Base de conocimiento: estaciones, troncales, conexiones y reglas
- Motor de inferencia: evaluacion de reglas logicas
- Algoritmo A*: busqueda heuristica para la ruta optima

Autor: Cristhian David Alviso Ortiz
Universidad: Corporacion Universitaria Iberoamericana
Materia: Inteligencia Artificial - 2026-1
"""

import heapq
from dataclasses import dataclass, field
from typing import Optional


# =============================================================================
# BASE DE CONOCIMIENTO - Estaciones y coordenadas aproximadas (lat, lon)
# =============================================================================

ESTACIONES = {
    # Troncal Caracas (Norte-Sur)
    "Portal Norte":       (4.7590, -74.0452),
    "Toberin":            (4.7480, -74.0470),
    "Cardio Infantil":    (4.7380, -74.0490),
    "Calle 146":          (4.7280, -74.0500),
    "Calle 142":          (4.7220, -74.0510),
    "Alcala":             (4.7150, -74.0520),
    "Prado":              (4.7080, -74.0530),
    "Calle 127":          (4.7010, -74.0540),
    "Pepe Sierra":        (4.6950, -74.0555),
    "Calle 106":          (4.6860, -74.0570),
    "Calle 100":          (4.6820, -74.0580),
    "Virrey":             (4.6750, -74.0590),
    "Calle 85":           (4.6680, -74.0600),
    "Heroes":             (4.6580, -74.0620),
    "Calle 72":           (4.6560, -74.0630),
    "Calle 63":           (4.6500, -74.0640),
    "Flores":             (4.6430, -74.0650),
    "Calle 45":           (4.6370, -74.0660),
    "Marly":              (4.6310, -74.0665),
    "Calle 34":           (4.6240, -74.0670),
    "Profamilia":         (4.6180, -74.0680),
    "Calle 22":           (4.6120, -74.0690),
    "Calle 19":           (4.6090, -74.0695),

    # Troncal Calle 26 (Aeropuerto - Centro)
    "Portal El Dorado":   (4.6580, -74.1170),
    "El Dorado":          (4.6590, -74.1100),
    "Modelia":            (4.6600, -74.1030),
    "Normandia":          (4.6610, -74.0960),
    "Av 68":              (4.6580, -74.0880),
    "Salitre El Greco":   (4.6570, -74.0830),
    "CAN":                (4.6560, -74.0780),
    "Gobernacion":        (4.6540, -74.0730),
    "Centro Memoria":     (4.6130, -74.0700),

    # Troncal NQS (Norte-Sur por NQS)
    "Portal 80":          (4.6910, -74.0850),
    "Polo":               (4.6850, -74.0810),
    "Escuela Militar":    (4.6780, -74.0780),
    "Av Chile":           (4.6700, -74.0730),
    "Calle 63 NQS":       (4.6580, -74.0710),
    "Simon Bolivar":      (4.6490, -74.0700),
    "NQS Calle 38A Sur":  (4.5910, -74.0710),

    # Troncal Americas
    "Portal Americas":    (4.6270, -74.1380),
    "Patio Bonito":       (4.6300, -74.1300),
    "Biblioteca Tintal":  (4.6340, -74.1220),
    "Mandalay":           (4.6380, -74.1140),
    "Mundo Aventura":     (4.6400, -74.1060),
    "Marsella":           (4.6430, -74.0970),
    "Pradera":            (4.6450, -74.0900),
    "De La Sabana":       (4.6300, -74.0780),
    "Ricaurte":           (4.6140, -74.0790),
    "San Facade":         (4.6070, -74.0750),

    # Troncal Caracas Sur
    "Tercer Milenio":     (4.5960, -74.0740),
    "Hospitales":         (4.5890, -74.0750),
    "Nari\u00f1o":               (4.5810, -74.0760),
    "Restrepo":           (4.5740, -74.0770),
    "Olaya":              (4.5670, -74.0780),
    "Quiroga":            (4.5600, -74.0790),
    "Calle 40 Sur":       (4.5530, -74.0800),
    "General Santander":  (4.5460, -74.0810),
    "Portal Sur":         (4.5390, -74.0820),

    # Troncal Usme (Portal Sur - Portal Usme)
    "Santa Lucia":        (4.5340, -74.0840),
    "Socorro":            (4.5280, -74.0870),
    "Consuelo":           (4.5220, -74.0890),
    "Molinos":            (4.5170, -74.0920),
    "Portal Usme":        (4.5100, -74.0960),

    # Troncal Suba
    "Portal Suba":        (4.7430, -74.0930),
    "La Campi\u00f1a":          (4.7360, -74.0900),
    "Suba TV 91":         (4.7280, -74.0870),
    "21 Angeles":         (4.7200, -74.0840),
    "Gratamira":          (4.7130, -74.0810),
    "Calle 100 Suba":     (4.6900, -74.0720),
    "Shaio":              (4.6980, -74.0760),
    "Humedal Cordoba":    (4.7050, -74.0780),

    # Troncal Calle 80
    "Portal 80 Calle":    (4.6910, -74.0850),
    "Av Cali Calle 80":   (4.6890, -74.0930),
    "Granja":             (4.6870, -74.1000),
    "Minuto de Dios":     (4.6850, -74.1070),
    "Ferias":             (4.6830, -74.0950),

    # Estaciones de conexion / transbordo
    "Museo Nacional":     (4.6150, -74.0690),
    "San Victorino":      (4.6030, -74.0770),
    "Las Aguas":          (4.5990, -74.0720),
}


# =============================================================================
# BASE DE CONOCIMIENTO - Reglas logicas de conexion
# =============================================================================

class ReglaConexion:
    """Representa una regla logica de conexion entre estaciones.

    Formato logico:
        SI estacion_actual = A Y destino = B
        ENTONCES conectado(A, B, troncal, tiempo_minutos)
    """

    def __init__(self, origen: str, destino: str, troncal: str, tiempo: float):
        self.origen = origen
        self.destino = destino
        self.troncal = troncal
        self.tiempo = tiempo

    def evaluar(self, estacion_actual: str) -> bool:
        """Evalua si esta regla aplica desde la estacion actual."""
        return estacion_actual == self.origen

    def __repr__(self):
        return (f"SI estacion = '{self.origen}' "
                f"ENTONCES conectado('{self.origen}', '{self.destino}', "
                f"troncal='{self.troncal}', tiempo={self.tiempo}min)")


class ReglaTransbordo:
    """Regla logica para transbordos entre troncales.

    Formato logico:
        SI estacion_actual = A Y troncal_actual != troncal_destino
        ENTONCES transbordo(A, troncal_origen, troncal_destino, tiempo_extra)
    """

    def __init__(self, estacion: str, troncales: list, tiempo_extra: float = 3.0):
        self.estacion = estacion
        self.troncales = troncales
        self.tiempo_extra = tiempo_extra

    def evaluar(self, estacion_actual: str, troncal_actual: str, troncal_destino: str) -> bool:
        """Evalua si se puede hacer transbordo en esta estacion."""
        return (estacion_actual == self.estacion
                and troncal_actual in self.troncales
                and troncal_destino in self.troncales
                and troncal_actual != troncal_destino)


# =============================================================================
# DEFINICION DE CONEXIONES (Base de hechos)
# =============================================================================

CONEXIONES_RAW = [
    # Troncal Caracas Norte
    ("Portal Norte", "Toberin", "Caracas", 2),
    ("Toberin", "Cardio Infantil", "Caracas", 2),
    ("Cardio Infantil", "Calle 146", "Caracas", 2),
    ("Calle 146", "Calle 142", "Caracas", 1.5),
    ("Calle 142", "Alcala", "Caracas", 2),
    ("Alcala", "Prado", "Caracas", 2),
    ("Prado", "Calle 127", "Caracas", 2),
    ("Calle 127", "Pepe Sierra", "Caracas", 1.5),
    ("Pepe Sierra", "Calle 106", "Caracas", 2),
    ("Calle 106", "Calle 100", "Caracas", 1.5),
    ("Calle 100", "Virrey", "Caracas", 2),
    ("Virrey", "Calle 85", "Caracas", 2),
    ("Calle 85", "Heroes", "Caracas", 2),
    ("Heroes", "Calle 72", "Caracas", 1.5),
    ("Calle 72", "Calle 63", "Caracas", 2),
    ("Calle 63", "Flores", "Caracas", 2),
    ("Flores", "Calle 45", "Caracas", 2),
    ("Calle 45", "Marly", "Caracas", 2),
    ("Marly", "Calle 34", "Caracas", 2),
    ("Calle 34", "Profamilia", "Caracas", 2),
    ("Profamilia", "Calle 22", "Caracas", 1.5),
    ("Calle 22", "Calle 19", "Caracas", 1),
    ("Calle 19", "Museo Nacional", "Caracas", 2),
    ("Museo Nacional", "Centro Memoria", "Caracas", 2),
    ("Centro Memoria", "Tercer Milenio", "Caracas", 2),

    # Troncal Caracas Sur
    ("Tercer Milenio", "Hospitales", "Caracas Sur", 2),
    ("Hospitales", "Nari\u00f1o", "Caracas Sur", 2),
    ("Nari\u00f1o", "Restrepo", "Caracas Sur", 2),
    ("Restrepo", "Olaya", "Caracas Sur", 2),
    ("Olaya", "Quiroga", "Caracas Sur", 2),
    ("Quiroga", "Calle 40 Sur", "Caracas Sur", 2),
    ("Calle 40 Sur", "General Santander", "Caracas Sur", 2),
    ("General Santander", "Portal Sur", "Caracas Sur", 2),

    # Troncal Usme (Portal Sur - Portal Usme)
    ("Portal Sur", "Santa Lucia", "Usme", 3),
    ("Santa Lucia", "Socorro", "Usme", 3),
    ("Socorro", "Consuelo", "Usme", 3),
    ("Consuelo", "Molinos", "Usme", 3),
    ("Molinos", "Portal Usme", "Usme", 4),

    # Troncal Calle 26
    ("Portal El Dorado", "El Dorado", "Calle 26", 2),
    ("El Dorado", "Modelia", "Calle 26", 2),
    ("Modelia", "Normandia", "Calle 26", 2),
    ("Normandia", "Av 68", "Calle 26", 2),
    ("Av 68", "Salitre El Greco", "Calle 26", 2),
    ("Salitre El Greco", "CAN", "Calle 26", 2),
    ("CAN", "Gobernacion", "Calle 26", 2),
    ("Gobernacion", "Calle 63", "Calle 26", 2),
    ("Calle 63", "Flores", "Calle 26", 2),
    ("Flores", "Calle 22", "Calle 26", 3),
    ("Calle 22", "Calle 19", "Calle 26", 1),
    ("Calle 19", "Museo Nacional", "Calle 26", 2),
    ("Museo Nacional", "San Victorino", "Calle 26", 2),
    ("San Victorino", "Las Aguas", "Calle 26", 2),

    # Troncal NQS
    ("Portal 80", "Polo", "NQS", 2),
    ("Polo", "Escuela Militar", "NQS", 2),
    ("Escuela Militar", "Av Chile", "NQS", 2),
    ("Av Chile", "Calle 63 NQS", "NQS", 2),
    ("Calle 63 NQS", "Simon Bolivar", "NQS", 2),
    ("Simon Bolivar", "Ricaurte", "NQS", 3),
    ("Ricaurte", "Hospitales", "NQS", 3),
    ("Hospitales", "NQS Calle 38A Sur", "NQS", 4),

    # Troncal Americas
    ("Portal Americas", "Patio Bonito", "Americas", 2),
    ("Patio Bonito", "Biblioteca Tintal", "Americas", 2),
    ("Biblioteca Tintal", "Mandalay", "Americas", 2),
    ("Mandalay", "Mundo Aventura", "Americas", 2),
    ("Mundo Aventura", "Marsella", "Americas", 2),
    ("Marsella", "Pradera", "Americas", 2),
    ("Pradera", "De La Sabana", "Americas", 2),
    ("De La Sabana", "Ricaurte", "Americas", 2),
    ("Ricaurte", "San Facade", "Americas", 2),
    ("San Facade", "Tercer Milenio", "Americas", 2),

    # Troncal Suba
    ("Portal Suba", "La Campi\u00f1a", "Suba", 2),
    ("La Campi\u00f1a", "Suba TV 91", "Suba", 2),
    ("Suba TV 91", "21 Angeles", "Suba", 2),
    ("21 Angeles", "Gratamira", "Suba", 2),
    ("Gratamira", "Humedal Cordoba", "Suba", 2),
    ("Humedal Cordoba", "Shaio", "Suba", 2),
    ("Shaio", "Calle 100 Suba", "Suba", 2),
    ("Calle 100 Suba", "Calle 100", "Suba", 2),
    ("Calle 100", "Heroes", "Suba", 3),

    # Troncal Calle 80
    ("Av Cali Calle 80", "Granja", "Calle 80", 2),
    ("Granja", "Minuto de Dios", "Calle 80", 2),
    ("Minuto de Dios", "Ferias", "Calle 80", 2),
    ("Ferias", "Portal 80", "Calle 80", 2),
    ("Portal 80", "Polo", "Calle 80", 2),
    ("Polo", "Heroes", "Calle 80", 3),
]

# Reglas de transbordo (estaciones donde se puede cambiar de troncal)
TRANSBORDOS_RAW = [
    ("Calle 100", ["Caracas", "Suba"], 3),
    ("Heroes", ["Caracas", "Suba", "Calle 80"], 3),
    ("Calle 72", ["Caracas", "Calle 26"], 3),
    ("Calle 63", ["Caracas", "Calle 26"], 3),
    ("Calle 22", ["Caracas", "Calle 26"], 3),
    ("Calle 19", ["Caracas", "Calle 26"], 3),
    ("Museo Nacional", ["Caracas", "Calle 26"], 3),
    ("Flores", ["Caracas", "Calle 26"], 3),
    ("Ricaurte", ["NQS", "Americas"], 3),
    ("Hospitales", ["Caracas Sur", "NQS"], 3),
    ("Tercer Milenio", ["Caracas", "Caracas Sur", "Americas"], 3),
    ("Portal Sur", ["Caracas Sur", "Usme"], 3),
    ("Portal 80", ["NQS", "Calle 80"], 3),
    ("Polo", ["NQS", "Calle 80"], 3),
]


# =============================================================================
# MOTOR DE INFERENCIA
# =============================================================================

class MotorInferencia:
    """Motor de inferencia que gestiona la base de conocimiento
    y permite consultar conexiones aplicando reglas logicas."""

    def __init__(self):
        self.reglas_conexion: list[ReglaConexion] = []
        self.reglas_transbordo: list[ReglaTransbordo] = []
        self._cargar_reglas()

    def _cargar_reglas(self):
        """Carga las reglas de conexion desde la base de hechos."""
        for origen, destino, troncal, tiempo in CONEXIONES_RAW:
            # Cada conexion genera dos reglas (bidireccional)
            self.reglas_conexion.append(ReglaConexion(origen, destino, troncal, tiempo))
            self.reglas_conexion.append(ReglaConexion(destino, origen, troncal, tiempo))

        for estacion, troncales, tiempo in TRANSBORDOS_RAW:
            self.reglas_transbordo.append(ReglaTransbordo(estacion, troncales, tiempo))

        print(f"[Motor] Base de conocimiento cargada:")
        print(f"  - {len(self.reglas_conexion)} reglas de conexion")
        print(f"  - {len(self.reglas_transbordo)} reglas de transbordo")
        print(f"  - {len(ESTACIONES)} estaciones registradas")

    def obtener_vecinos(self, estacion: str) -> list[tuple[str, str, float]]:
        """Aplica las reglas para obtener estaciones vecinas.

        Retorna: lista de (estacion_vecina, troncal, tiempo)
        """
        vecinos = []
        for regla in self.reglas_conexion:
            if regla.evaluar(estacion):
                vecinos.append((regla.destino, regla.troncal, regla.tiempo))
        return vecinos

    def es_transbordo(self, estacion: str) -> bool:
        """Verifica si una estacion permite transbordo."""
        for regla in self.reglas_transbordo:
            if regla.estacion == estacion:
                return True
        return False

    def obtener_troncales(self, estacion: str) -> list[str]:
        """Retorna las troncales disponibles en una estacion."""
        troncales = set()
        for regla in self.reglas_conexion:
            if regla.evaluar(estacion):
                troncales.add(regla.troncal)
        return list(troncales)

    def listar_estaciones(self) -> list[str]:
        """Retorna la lista de todas las estaciones disponibles."""
        return sorted(ESTACIONES.keys())

    def mostrar_reglas(self, estacion: str):
        """Muestra las reglas que aplican para una estacion."""
        print(f"\nReglas aplicables para '{estacion}':")
        for regla in self.reglas_conexion:
            if regla.evaluar(estacion):
                print(f"  {regla}")


# =============================================================================
# ALGORITMO A* - Busqueda heuristica
# =============================================================================

@dataclass(order=True)
class Nodo:
    """Nodo para el algoritmo A*."""
    f: float
    g: float = field(compare=False)
    estacion: str = field(compare=False)
    troncal: str = field(compare=False)
    padre: Optional['Nodo'] = field(compare=False, default=None)


def heuristica(estacion_actual: str, estacion_destino: str) -> float:
    """Calcula la distancia heuristica entre dos estaciones.

    Usa la distancia euclidiana entre coordenadas geograficas
    convertida a una estimacion de tiempo en minutos.
    Factor de escala: 1 grado ~ 111 km, velocidad promedio TM ~ 25 km/h.
    """
    if estacion_actual not in ESTACIONES or estacion_destino not in ESTACIONES:
        return 0

    lat1, lon1 = ESTACIONES[estacion_actual]
    lat2, lon2 = ESTACIONES[estacion_destino]

    # Distancia euclidiana en grados, convertida a km aprox
    dist_grados = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
    dist_km = dist_grados * 111  # 1 grado ~ 111 km

    # Tiempo estimado a 25 km/h promedio, convertido a minutos
    tiempo_estimado = (dist_km / 25) * 60

    return tiempo_estimado


def buscar_ruta_a_estrella(motor: MotorInferencia, origen: str, destino: str) -> Optional[list[tuple[str, str, float]]]:
    """Busqueda A* para encontrar la ruta optima.

    Args:
        motor: Motor de inferencia con la base de conocimiento
        origen: Estacion de origen
        destino: Estacion de destino

    Returns:
        Lista de tuplas (estacion, troncal, tiempo_acumulado) o None si no hay ruta
    """
    if origen not in ESTACIONES:
        print(f"Error: Estacion '{origen}' no existe en la base de conocimiento.")
        return None
    if destino not in ESTACIONES:
        print(f"Error: Estacion '{destino}' no existe en la base de conocimiento.")
        return None
    if origen == destino:
        print("Origen y destino son la misma estacion.")
        return [(origen, "-", 0)]

    # Inicializar A*
    nodo_inicio = Nodo(
        f=heuristica(origen, destino),
        g=0,
        estacion=origen,
        troncal="Inicio"
    )

    abiertos = [nodo_inicio]  # Cola de prioridad (min-heap)
    cerrados = set()  # Estaciones ya visitadas
    mejor_g = {origen: 0}  # Mejor costo g conocido para cada estacion

    nodos_explorados = 0

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)
        nodos_explorados += 1

        # Llegamos al destino
        if nodo_actual.estacion == destino:
            ruta = []
            nodo = nodo_actual
            while nodo is not None:
                ruta.append((nodo.estacion, nodo.troncal, nodo.g))
                nodo = nodo.padre
            ruta.reverse()
            print(f"\n[A*] Ruta encontrada! Nodos explorados: {nodos_explorados}")
            return ruta

        if nodo_actual.estacion in cerrados:
            continue

        cerrados.add(nodo_actual.estacion)

        # Obtener vecinos usando el motor de inferencia
        vecinos = motor.obtener_vecinos(nodo_actual.estacion)

        for vecino, troncal, tiempo in vecinos:
            if vecino in cerrados:
                continue

            nuevo_g = nodo_actual.g + tiempo
            h = heuristica(vecino, destino)
            nuevo_f = nuevo_g + h

            # Solo expandir si encontramos un mejor camino
            if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                mejor_g[vecino] = nuevo_g
                nodo_vecino = Nodo(
                    f=nuevo_f,
                    g=nuevo_g,
                    estacion=vecino,
                    troncal=troncal,
                    padre=nodo_actual
                )
                heapq.heappush(abiertos, nodo_vecino)

    print(f"\n[A*] No se encontro ruta. Nodos explorados: {nodos_explorados}")
    return None


# =============================================================================
# INTERFAZ DE USUARIO
# =============================================================================

def mostrar_ruta(ruta: list[tuple[str, str, float]]):
    """Muestra la ruta encontrada de forma legible."""
    print("\n" + "=" * 65)
    print("  RUTA OPTIMA - TransMilenio Bogota")
    print("=" * 65)

    troncal_actual = None
    for i, (estacion, troncal, tiempo) in enumerate(ruta):
        if troncal != troncal_actual and troncal != "Inicio":
            troncal_actual = troncal
            print(f"\n  --- Troncal: {troncal_actual} ---")

        if i == 0:
            marcador = ">>> ORIGEN"
        elif i == len(ruta) - 1:
            marcador = ">>> DESTINO"
        else:
            marcador = "   "

        print(f"  {marcador}  {estacion:<25} ({tiempo:.1f} min)")

    tiempo_total = ruta[-1][2]
    num_estaciones = len(ruta)

    # Contar transbordos
    troncales_usadas = []
    for _, troncal, _ in ruta:
        if troncal != "Inicio" and (not troncales_usadas or troncales_usadas[-1] != troncal):
            troncales_usadas.append(troncal)

    num_transbordos = max(0, len(troncales_usadas) - 1)

    print(f"\n{'=' * 65}")
    print(f"  Resumen:")
    print(f"    Tiempo total estimado: {tiempo_total:.1f} minutos")
    print(f"    Estaciones recorridas: {num_estaciones}")
    print(f"    Transbordos:           {num_transbordos}")
    print(f"    Troncales usadas:      {', '.join(troncales_usadas)}")
    print(f"{'=' * 65}\n")


def mostrar_menu():
    """Muestra el menu principal."""
    print("\n" + "=" * 65)
    print("  SISTEMA INTELIGENTE DE RUTAS - TransMilenio Bogota")
    print("  Basado en reglas logicas y busqueda heuristica A*")
    print("=" * 65)
    print("\n  Opciones:")
    print("    1. Buscar ruta entre dos estaciones")
    print("    2. Listar todas las estaciones")
    print("    3. Ver reglas de una estacion")
    print("    4. Ver troncales de una estacion")
    print("    5. Ejecutar pruebas automaticas")
    print("    6. Salir")
    print()


def seleccionar_estacion(motor: MotorInferencia, mensaje: str) -> Optional[str]:
    """Permite al usuario seleccionar una estacion con busqueda parcial."""
    entrada = input(f"  {mensaje}: ").strip()
    if not entrada:
        return None

    # Busqueda exacta
    if entrada in ESTACIONES:
        return entrada

    # Busqueda parcial (case-insensitive)
    coincidencias = [e for e in ESTACIONES if entrada.lower() in e.lower()]

    if len(coincidencias) == 1:
        print(f"    -> {coincidencias[0]}")
        return coincidencias[0]
    elif len(coincidencias) > 1:
        print(f"    Varias coincidencias encontradas:")
        for i, est in enumerate(coincidencias, 1):
            print(f"      {i}. {est}")
        try:
            seleccion = int(input("    Seleccione el numero: ")) - 1
            if 0 <= seleccion < len(coincidencias):
                return coincidencias[seleccion]
        except (ValueError, IndexError):
            pass
        print("    Seleccion invalida.")
        return None
    else:
        print(f"    No se encontro la estacion '{entrada}'.")
        return None


def ejecutar_pruebas(motor: MotorInferencia):
    """Ejecuta un conjunto de pruebas automaticas."""
    print("\n" + "=" * 65)
    print("  PRUEBAS AUTOMATICAS")
    print("=" * 65)

    pruebas = [
        ("Portal Norte", "Portal Sur",
         "Recorrido completo Norte-Sur por Troncal Caracas"),
        ("Portal El Dorado", "Tercer Milenio",
         "Desde el aeropuerto hacia el centro"),
        ("Portal Suba", "Portal Americas",
         "Cruce entre troncal Suba y Americas"),
        ("Portal 80", "Portal Usme",
         "Desde Portal 80 hacia el sur por NQS y Caracas"),
        ("Calle 100", "Ricaurte",
         "Ruta media con posible transbordo"),
    ]

    for i, (origen, destino, descripcion) in enumerate(pruebas, 1):
        print(f"\n{'~' * 65}")
        print(f"  Prueba {i}: {descripcion}")
        print(f"  Origen: {origen} -> Destino: {destino}")
        print(f"{'~' * 65}")

        ruta = buscar_ruta_a_estrella(motor, origen, destino)
        if ruta:
            mostrar_ruta(ruta)
        else:
            print("  No se encontro ruta.\n")


def main():
    """Funcion principal del sistema."""
    motor = MotorInferencia()

    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            print("\n  --- Buscar Ruta ---")
            origen = seleccionar_estacion(motor, "Estacion de ORIGEN")
            if not origen:
                continue
            destino = seleccionar_estacion(motor, "Estacion de DESTINO")
            if not destino:
                continue

            print(f"\n  Buscando ruta: {origen} -> {destino}")
            motor.mostrar_reglas(origen)

            ruta = buscar_ruta_a_estrella(motor, origen, destino)
            if ruta:
                mostrar_ruta(ruta)

        elif opcion == "2":
            print("\n  Estaciones disponibles:")
            for i, est in enumerate(motor.listar_estaciones(), 1):
                troncales = motor.obtener_troncales(est)
                print(f"    {i:3}. {est:<25} [{', '.join(troncales)}]")

        elif opcion == "3":
            estacion = seleccionar_estacion(motor, "Estacion para ver reglas")
            if estacion:
                motor.mostrar_reglas(estacion)

        elif opcion == "4":
            estacion = seleccionar_estacion(motor, "Estacion para ver troncales")
            if estacion:
                troncales = motor.obtener_troncales(estacion)
                print(f"    Troncales en {estacion}: {', '.join(troncales)}")
                if motor.es_transbordo(estacion):
                    print(f"    * Esta estacion permite transbordo")

        elif opcion == "5":
            ejecutar_pruebas(motor)

        elif opcion == "6":
            print("\n  Hasta luego!\n")
            break

        else:
            print("  Opcion no valida. Intente de nuevo.")


if __name__ == "__main__":
    main()
