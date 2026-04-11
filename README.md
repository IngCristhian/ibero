# Actividad 4 - Metodos de Aprendizaje No Supervisado

## Informacion General

- **Universidad:** Corporacion Universitaria Iberoamericana
- **Programa:** Ingenieria de Software
- **Materia:** Inteligencia Artificial - 2026-1
- **Estudiante:** Cristian David Alvis Ortiz

## Descripcion del Proyecto

Sistema de **aprendizaje no supervisado** que aplica tecnicas de **clustering**
sobre el dataset de rutas de TransMilenio Bogota para descubrir **perfiles
naturales de viaje** sin usar las etiquetas de categoria.

A diferencia del aprendizaje supervisado de la Actividad 3 (que usa la columna
`categoria` para entrenar), aqui el modelo debe encontrar agrupaciones naturales
basandose unicamente en las features numericas. Las etiquetas se usan solo al
final para validar la calidad de los clusters encontrados.

## Conceptos de IA aplicados

Basados en Palma Mendez, J. T. (2008). *Inteligencia artificial: metodos,
tecnicas y aplicaciones*. McGraw-Hill Espana. **Capitulo 16 - Tecnicas de
agrupamiento**.

1. **K-Means (modelo principal):** Algoritmo de particionado que divide los
   datos en K clusters minimizando la inercia (distancia cuadratica al centroide).
2. **DBSCAN:** Clustering basado en densidad que identifica regiones densas y
   marca como ruido los puntos aislados.
3. **Clustering Jerarquico Aglomerativo (Ward):** Construye un dendrograma fusionando
   clusters cercanos iterativamente.

### Tecnicas de soporte

- **Metodo del Codo (Elbow):** Para encontrar el K optimo
- **Coeficiente de Silhouette:** Validacion de calidad de los clusters
- **PCA:** Reduccion de dimensionalidad para visualizacion 2D
- **StandardScaler:** Normalizacion previa al clustering
- **Adjusted Rand Index (ARI) y NMI:** Validacion contra etiquetas reales

## Estructura del Proyecto

```
.
|-- transmilenio_rutas.py          # Sistema A* (Act 2)
|-- dataset_generator.py           # Generador (Act 3)
|-- dataset_rutas.csv              # Dataset (1500 muestras)
|-- modelo_no_supervisado.py       # Clustering principal
|-- resultados_no_supervisado/     # Salidas
|   |-- metodo_codo.png
|   |-- clusters_kmeans_pca.png
|   |-- clusters_dbscan_pca.png
|   |-- clusters_jerarquico_pca.png
|   |-- caracteristicas_clusters.png
|   |-- validacion_categorias.png
|   |-- comparacion_modelos.png
|   |-- reporte_evaluacion.txt
|-- README.md
```

## Dataset

Mismo dataset de la Actividad 3 (1500 muestras de rutas TransMilenio), pero
**sin usar la columna `categoria`** para el entrenamiento del modelo.

| Feature | Tipo | Descripcion |
|---------|------|-------------|
| `num_estaciones` | int | Numero de estaciones recorridas |
| `num_transbordos` | int | Numero de cambios entre troncales |
| `num_troncales` | int | Numero de troncales distintas usadas |
| `distancia_km` | float | Distancia geografica entre origen y destino |
| `hora_dia` | int | Hora del dia (5-23) |
| `dia_semana` | int | Dia de la semana (0=Lunes, 6=Domingo) |
| `es_hora_pico` | int | 1 si es hora pico, 0 si no |
| `es_fin_semana` | int | 1 si sabado/domingo, 0 si no |
| `num_portales` | int | Numero de portales en origen/destino (0-2) |

Las features se normalizan con `StandardScaler` antes del clustering.

## Resultados

### K optimo encontrado

Segun el metodo del codo y el coeficiente de Silhouette, el **K optimo es 3**.

### Comparacion de modelos

| Modelo | Silhouette Score | Notas |
|--------|------------------|-------|
| **DBSCAN**            | **0.3158** | Encuentra 15 clusters + 71% ruido |
| K-Means (K=3)         | 0.2360     | Modelo principal, 3 clusters balanceados |
| Jerarquico (K=3)      | 0.2156     | 3 clusters con linkage Ward |

### Perfiles de viaje descubiertos (K-Means)

| Cluster | % | Estaciones | Transbordos | Distancia | Tiempo | Perfil |
|---------|---|------------|-------------|-----------|--------|--------|
| **0** | 25% | 10.5 | 2.0 | 7 km | 21 min | Rutas medianas en **fines de semana** |
| **1** | 25% | 20.8 | 4.2 | 16 km | 54 min | **Rutas largas extremo a extremo** |
| **2** | 50% | 9.5 | 1.8 | 6 km | 22 min | **Rutas cortas en dias laborales** |

### Validacion contra categorias reales

- **Adjusted Rand Index (ARI):** 0.2117
- **Normalized Mutual Info (NMI):** 0.2489

Los valores indican que los clusters tienen correspondencia parcial con las
categorias reales (Rapido/Medio/Lento), lo cual es esperable porque el
clustering descubrio estructuras adicionales (laboral/fin de semana) que
no estaban capturadas en la categorizacion supervisada.

## Requisitos

- Python 3.8+
- scikit-learn, pandas, numpy, matplotlib

```bash
pip install scikit-learn pandas numpy matplotlib
```

## Instrucciones de Ejecucion

```bash
git clone https://github.com/IngCristhian/ibero.git
cd ibero
git checkout inteligencia-artificial-act4

# (Opcional) regenerar el dataset
python3 dataset_generator.py

# Ejecutar clustering
python3 modelo_no_supervisado.py
```

Los resultados se guardan en `resultados_no_supervisado/`.

## Referencias

- Palma Mendez, J. T. (2008). *Inteligencia artificial: metodos, tecnicas y
  aplicaciones*. Madrid: McGraw-Hill Espana.
  - Capitulo 16: Tecnicas de agrupamiento
- Documentacion de scikit-learn: https://scikit-learn.org/stable/
