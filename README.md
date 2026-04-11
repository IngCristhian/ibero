# Actividad 3 - Metodos de Aprendizaje Supervisado

## Informacion General

- **Universidad:** Corporacion Universitaria Iberoamericana
- **Programa:** Ingenieria de Software
- **Materia:** Inteligencia Artificial - 2026-1
- **Estudiante:** Cristian David Alvis Ortiz

## Descripcion del Proyecto

Sistema de **clasificacion supervisada** que predice la **categoria de duracion**
(Rapido / Medio / Lento) de un viaje en TransMilenio Bogota a partir de
caracteristicas de la ruta como numero de estaciones, transbordos, troncales
usadas, distancia, hora del dia y dia de la semana.

El proyecto reutiliza el sistema de busqueda A* desarrollado en la **Actividad 2**
como fuente de datos sintetica para generar el dataset de entrenamiento.

## Conceptos de IA aplicados

Basados en Palma Mendez, J. T. (2008). *Inteligencia artificial: metodos,
tecnicas y aplicaciones*. McGraw-Hill Espana. **Capitulo 17 - Aprendizaje de
arboles y reglas de decision**.

1. **Arbol de Decision (modelo principal):** Algoritmo de aprendizaje supervisado
   que construye un arbol de reglas SI-ENTONCES dividiendo el espacio de features
   con el criterio de impureza Gini.
2. **Random Forest:** Ensemble de arboles que mejora la generalizacion mediante
   promediado de predicciones.
3. **K-Nearest Neighbors:** Algoritmo basado en instancias para comparacion.

## Estructura del Proyecto

```
.
|-- transmilenio_rutas.py       # Sistema A* de la Act 2 (fuente de datos)
|-- dataset_generator.py        # Generador del dataset CSV
|-- modelo_supervisado.py       # Entrenamiento y evaluacion de modelos
|-- dataset_rutas.csv           # Dataset generado (1500 muestras)
|-- resultados_supervisado/     # Salidas del modelo
|   |-- arbol_decision.png      # Visualizacion del arbol
|   |-- matriz_confusion_arbol.png
|   |-- matriz_confusion_rf.png
|   |-- importancia_features.png
|   |-- comparacion_modelos.png
|   |-- reglas_arbol.txt
|   |-- reporte_evaluacion.txt
|-- README.md
```

## Dataset

El dataset contiene **1500 muestras** generadas a partir del sistema de rutas
de TransMilenio (Actividad 2), aplicando factores realistas de variacion temporal.

### Features (variables independientes)

| Feature | Tipo | Descripcion |
|---------|------|-------------|
| `num_estaciones` | int | Numero de estaciones recorridas |
| `num_transbordos` | int | Numero de cambios entre troncales |
| `num_troncales` | int | Numero de troncales distintas usadas |
| `distancia_km` | float | Distancia geografica entre origen y destino |
| `hora_dia` | int | Hora del dia (5-23) |
| `dia_semana` | int | Dia de la semana (0=Lunes, 6=Domingo) |
| `es_hora_pico` | int | 1 si es hora pico, 0 si no |
| `es_fin_semana` | int | 1 si es sabado/domingo, 0 si no |
| `num_portales` | int | Numero de portales en origen/destino (0-2) |

### Target (variable a predecir)

| Categoria | Rango de tiempo | Distribucion |
|-----------|-----------------|--------------|
| `Rapido`  | < 25 minutos    | 52.6%        |
| `Medio`   | 25 - 50 minutos | 32.8%        |
| `Lento`   | > 50 minutos    | 14.6%        |

## Resultados

| Modelo | Accuracy | Precision | Recall | F1-Score |
|--------|----------|-----------|--------|----------|
| **Random Forest**    | **89.33%** | 0.9008 | 0.8933 | **0.8939** |
| Arbol de Decision    | 84.27%     | 0.8432 | 0.8427 | 0.8425     |
| KNN (k=7)            | 80.00%     | 0.8015 | 0.8000 | 0.7986     |

**Mejor modelo:** Random Forest con F1-Score de **0.8939**

### Importancia de Features

1. `num_estaciones`   - 0.738
2. `es_hora_pico`     - 0.095
3. `distancia_km`     - 0.061
4. `dia_semana`       - 0.048
5. `hora_dia`         - 0.034

## Requisitos

- Python 3.8 o superior
- scikit-learn
- pandas
- numpy
- matplotlib

```bash
pip install scikit-learn pandas numpy matplotlib
```

## Instrucciones de Ejecucion

```bash
# Clonar el repositorio
git clone https://github.com/IngCristhian/ibero.git
cd ibero

# Cambiar a la rama de la Actividad 3
git checkout inteligencia-artificial-act3

# Paso 1: Generar el dataset (si no existe)
python3 dataset_generator.py

# Paso 2: Entrenar y evaluar los modelos
python3 modelo_supervisado.py
```

Los resultados se guardan en la carpeta `resultados_supervisado/`.

## Referencias

- Palma Mendez, J. T. (2008). *Inteligencia artificial: metodos, tecnicas y
  aplicaciones*. Madrid: McGraw-Hill Espana.
  - Capitulo 17: Aprendizaje de arboles y reglas de decision
- Documentacion de scikit-learn: https://scikit-learn.org/stable/
