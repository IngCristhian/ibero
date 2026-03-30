# Actividad 2 - Busqueda y Sistemas Basados en Reglas

## Informacion General

- **Universidad:** Corporacion Universitaria Iberoamericana
- **Programa:** Ingenieria de Software
- **Materia:** Inteligencia Artificial - 2026-1
- **Estudiante:** Cristhian David Alviso Ortiz

## Descripcion del Proyecto

Sistema inteligente de rutas para el sistema de transporte masivo **TransMilenio** de Bogota, que utiliza:

- **Base de conocimiento** con reglas logicas para representar estaciones, conexiones entre troncales y reglas de transbordo
- **Motor de inferencia** que evalua las reglas para determinar las conexiones validas desde cualquier estacion
- **Algoritmo A*** (busqueda heuristica) para encontrar la ruta optima entre dos estaciones

### Conceptos de IA aplicados

1. **Representacion del conocimiento:** Las estaciones, conexiones y transbordos se modelan como reglas logicas del tipo `SI estacion = A ENTONCES conectado(A, B, troncal, tiempo)`
2. **Sistemas basados en reglas:** Un motor de inferencia evalua las reglas para obtener las estaciones vecinas y sus propiedades
3. **Busqueda heuristica A*:** Se usa la distancia euclidiana entre coordenadas geograficas como funcion heuristica para guiar la busqueda hacia la ruta mas eficiente

### Cobertura del sistema

- 75 estaciones de TransMilenio
- 6 troncales principales: Caracas, Calle 26, NQS, Americas, Suba, Calle 80
- 13 puntos de transbordo entre troncales
- 162 reglas de conexion bidireccionales

## Requisitos

- Python 3.8 o superior (no requiere librerias externas)

## Instrucciones de Ejecucion

```bash
# Clonar el repositorio
git clone https://github.com/IngCristhian/ibero.git
cd ibero

# Cambiar a la rama de inteligencia artificial
git checkout inteligencia-artificial

# Ejecutar el programa
python3 transmilenio_rutas.py
```

## Uso del Programa

El programa presenta un menu interactivo con las siguientes opciones:

1. **Buscar ruta entre dos estaciones:** Ingrese el nombre (completo o parcial) de la estacion de origen y destino. El sistema encontrara la ruta optima usando A*.
2. **Listar todas las estaciones:** Muestra las 75 estaciones disponibles con sus troncales.
3. **Ver reglas de una estacion:** Muestra las reglas logicas que aplican para una estacion especifica.
4. **Ver troncales de una estacion:** Muestra en que troncales opera una estacion y si permite transbordo.
5. **Ejecutar pruebas automaticas:** Ejecuta 5 rutas de prueba predefinidas para validar el sistema.

### Ejemplo de uso

```
  Estacion de ORIGEN: portal norte
    -> Portal Norte
  Estacion de DESTINO: portal sur
    -> Portal Sur

  Buscando ruta: Portal Norte -> Portal Sur

  [A*] Ruta encontrada! Nodos explorados: 31

  RUTA OPTIMA - TransMilenio Bogota
  =================================================================
    Tiempo total estimado: 53.0 minutos
    Estaciones recorridas: 28
    Troncales usadas:      Caracas, Caracas Sur
```

## Estructura del Codigo

```
transmilenio_rutas.py
|
|-- ESTACIONES              # Diccionario con coordenadas geograficas
|-- CONEXIONES_RAW          # Base de hechos: conexiones entre estaciones
|-- TRANSBORDOS_RAW         # Base de hechos: puntos de transbordo
|
|-- ReglaConexion           # Clase: regla logica de conexion
|-- ReglaTransbordo         # Clase: regla logica de transbordo
|-- MotorInferencia         # Motor que gestiona y evalua reglas
|
|-- heuristica()            # Funcion heuristica (distancia euclidiana)
|-- buscar_ruta_a_estrella()# Algoritmo A*
|
|-- main()                  # Interfaz de usuario interactiva
```

## Referencias

- Benitez, R. (2014). *Inteligencia artificial avanzada*. Barcelona: Editorial UOC.
  - Capitulo 2: Logica y representacion del conocimiento
  - Capitulo 3: Sistemas basados en reglas
  - Capitulo 9: Tecnicas basadas en busquedas heuristicas
