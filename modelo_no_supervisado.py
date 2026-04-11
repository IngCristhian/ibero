"""
Modelo de Aprendizaje No Supervisado - TransMilenio Bogota
============================================================
Aplica tecnicas de agrupamiento (clustering) sobre el dataset de
rutas de TransMilenio para descubrir perfiles naturales de viaje
sin usar las etiquetas de categoria.

Modelos implementados:
- K-Means (modelo principal, alineado con Palma cap. 16)
- DBSCAN (clustering basado en densidad)
- Clustering Jerarquico Aglomerativo

Tecnicas de soporte:
- Metodo del codo (Elbow method) para encontrar K optimo
- Coeficiente de Silhouette
- PCA para visualizacion 2D
- Caracterizacion de clusters
- Validacion contra etiquetas reales (matriz de contingencia)

Autor: Cristian David Alvis Ortiz
Materia: Inteligencia Artificial - 2026-1
Actividad: 4 - Metodos de Aprendizaje No Supervisado
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score,
    normalized_mutual_info_score,
)


# Configuracion
DATASET_PATH = "dataset_rutas.csv"
RANDOM_STATE = 42
OUTPUT_DIR = "resultados_no_supervisado"

# Features (NO usamos categoria - es no supervisado)
FEATURES = [
    "num_estaciones",
    "num_transbordos",
    "num_troncales",
    "distancia_km",
    "hora_dia",
    "dia_semana",
    "es_hora_pico",
    "es_fin_semana",
    "num_portales",
]


def cargar_y_preparar_datos():
    """Carga el dataset y normaliza las features para clustering."""
    print("\n" + "=" * 65)
    print("  CARGA Y PREPARACION DE DATOS")
    print("=" * 65)

    df = pd.read_csv(DATASET_PATH)
    print(f"\n[OK] Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")
    print(f"  Features usadas para clustering: {len(FEATURES)}")
    print(f"  IMPORTANTE: La columna 'categoria' NO se usa para entrenar")
    print(f"             solo para validacion final")

    X = df[FEATURES].copy()
    categoria_real = df["categoria"].copy()  # Solo para validacion

    # Normalizar features (clustering es sensible a la escala)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"\n[OK] Features normalizadas con StandardScaler")
    print(f"  Forma: {X_scaled.shape}")

    return X, X_scaled, categoria_real, df


def metodo_del_codo(X_scaled, k_max: int = 10):
    """Calcula la inercia para diferentes valores de K (Elbow method).

    Tambien calcula el coeficiente de Silhouette para validar.
    """
    print("\n" + "=" * 65)
    print("  METODO DEL CODO - Busqueda del K optimo")
    print("=" * 65)

    k_values = list(range(2, k_max + 1))
    inercias = []
    silhouette_scores = []

    print(f"\n  Probando K de 2 a {k_max}...")
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        inercias.append(kmeans.inertia_)
        sil = silhouette_score(X_scaled, labels)
        silhouette_scores.append(sil)
        print(f"    K={k:2d}  ->  Inercia={kmeans.inertia_:>10.2f}  "
              f"Silhouette={sil:.4f}")

    return k_values, inercias, silhouette_scores


def visualizar_metodo_codo(k_values, inercias, silhouette_scores, output_path: str):
    """Grafica el metodo del codo y el silhouette score."""
    print(f"\n[INFO] Generando grafico del metodo del codo...")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Grafico 1: Inercia (codo)
    axes[0].plot(k_values, inercias, "o-", color="#1e3a5f", linewidth=2, markersize=8)
    axes[0].set_xlabel("Numero de clusters (K)", fontsize=11)
    axes[0].set_ylabel("Inercia (WCSS)", fontsize=11)
    axes[0].set_title("Metodo del Codo", fontsize=13, fontweight="bold")
    axes[0].grid(alpha=0.3)
    axes[0].set_xticks(k_values)

    # Grafico 2: Silhouette
    axes[1].plot(k_values, silhouette_scores, "o-", color="#2c5f8a", linewidth=2, markersize=8)
    axes[1].set_xlabel("Numero de clusters (K)", fontsize=11)
    axes[1].set_ylabel("Silhouette Score", fontsize=11)
    axes[1].set_title("Coeficiente de Silhouette", fontsize=13, fontweight="bold")
    axes[1].grid(alpha=0.3)
    axes[1].set_xticks(k_values)

    # Marcar el mejor
    mejor_k_idx = np.argmax(silhouette_scores)
    mejor_k = k_values[mejor_k_idx]
    axes[1].axvline(x=mejor_k, color="red", linestyle="--", alpha=0.5, label=f"Mejor K={mejor_k}")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Grafico guardado en: {output_path}")
    print(f"  K optimo segun Silhouette: {mejor_k}")
    return mejor_k


def entrenar_kmeans(X_scaled, k: int):
    """Entrena el modelo K-Means con el K optimo."""
    print("\n" + "=" * 65)
    print(f"  MODELO 1: K-MEANS  (K={k})")
    print("  (Palma cap. 16 - Tecnicas de agrupamiento)")
    print("=" * 65)

    modelo = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels = modelo.fit_predict(X_scaled)

    sil = silhouette_score(X_scaled, labels)
    print(f"\n  Inercia (WCSS):   {modelo.inertia_:.2f}")
    print(f"  Silhouette Score: {sil:.4f}")
    print(f"  Iteraciones:      {modelo.n_iter_}")

    # Distribucion de clusters
    print(f"\n  Distribucion de clusters:")
    unique, counts = np.unique(labels, return_counts=True)
    for c, cnt in zip(unique, counts):
        pct = (cnt / len(labels)) * 100
        print(f"    Cluster {c}: {cnt:5} muestras ({pct:5.1f}%)")

    return modelo, labels, sil


def entrenar_dbscan(X_scaled, eps: float = 0.8, min_samples: int = 10):
    """Entrena el modelo DBSCAN."""
    print("\n" + "=" * 65)
    print(f"  MODELO 2: DBSCAN  (eps={eps}, min_samples={min_samples})")
    print("  (Clustering basado en densidad)")
    print("=" * 65)

    modelo = DBSCAN(eps=eps, min_samples=min_samples)
    labels = modelo.fit_predict(X_scaled)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_ruido = list(labels).count(-1)

    print(f"\n  Clusters encontrados: {n_clusters}")
    print(f"  Puntos de ruido:      {n_ruido} ({n_ruido/len(labels)*100:.1f}%)")

    if n_clusters >= 2:
        # Excluir ruido para silhouette
        mask = labels != -1
        if mask.sum() > 1:
            sil = silhouette_score(X_scaled[mask], labels[mask])
            print(f"  Silhouette Score:    {sil:.4f}  (sin ruido)")
        else:
            sil = -1
    else:
        sil = -1
        print(f"  No se pudo calcular Silhouette (clusters insuficientes)")

    return modelo, labels, sil


def entrenar_jerarquico(X_scaled, k: int):
    """Entrena clustering jerarquico aglomerativo."""
    print("\n" + "=" * 65)
    print(f"  MODELO 3: CLUSTERING JERARQUICO  (K={k})")
    print("  (Aglomerativo con linkage Ward)")
    print("=" * 65)

    modelo = AgglomerativeClustering(n_clusters=k, linkage="ward")
    labels = modelo.fit_predict(X_scaled)

    sil = silhouette_score(X_scaled, labels)
    print(f"\n  Silhouette Score: {sil:.4f}")

    print(f"\n  Distribucion de clusters:")
    unique, counts = np.unique(labels, return_counts=True)
    for c, cnt in zip(unique, counts):
        pct = (cnt / len(labels)) * 100
        print(f"    Cluster {c}: {cnt:5} muestras ({pct:5.1f}%)")

    return modelo, labels, sil


def visualizar_clusters_pca(X_scaled, labels, titulo: str, output_path: str):
    """Reduce a 2D con PCA y visualiza los clusters."""
    print(f"\n[INFO] Generando visualizacion 2D con PCA...")

    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(9, 7))

    unique_labels = sorted(set(labels))
    colors = plt.cm.tab10(np.linspace(0, 1, max(len(unique_labels), 10)))

    for i, lbl in enumerate(unique_labels):
        mask = labels == lbl
        if lbl == -1:
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                       c="lightgray", s=20, alpha=0.5, label="Ruido", marker="x")
        else:
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                       c=[colors[i]], s=30, alpha=0.7, label=f"Cluster {lbl}")

    var_exp = pca.explained_variance_ratio_
    ax.set_xlabel(f"PC1 ({var_exp[0]*100:.1f}% varianza)", fontsize=11)
    ax.set_ylabel(f"PC2 ({var_exp[1]*100:.1f}% varianza)", fontsize=11)
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Guardado en: {output_path}")


def caracterizar_clusters(df, labels, output_path: str):
    """Calcula y visualiza las caracteristicas promedio de cada cluster."""
    print(f"\n[INFO] Caracterizando clusters...")

    df_clusters = df.copy()
    df_clusters["cluster"] = labels

    # Excluir ruido si existe
    df_clusters = df_clusters[df_clusters["cluster"] != -1]

    # Estadisticas por cluster
    stats = df_clusters.groupby("cluster")[FEATURES + ["tiempo_minutos"]].mean()

    print(f"\n  Caracteristicas promedio por cluster:")
    print(stats.round(2).to_string())

    # Tabla de tamano
    print(f"\n  Tamano de cada cluster:")
    for c in sorted(df_clusters["cluster"].unique()):
        n = (df_clusters["cluster"] == c).sum()
        print(f"    Cluster {c}: {n} muestras")

    # Visualizacion: heatmap normalizado
    fig, ax = plt.subplots(figsize=(11, 6))
    stats_norm = (stats - stats.min()) / (stats.max() - stats.min() + 1e-9)
    im = ax.imshow(stats_norm.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(stats.columns)))
    ax.set_xticklabels(stats.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(stats.index)))
    ax.set_yticklabels([f"Cluster {c}" for c in stats.index])
    ax.set_title("Caracteristicas promedio normalizadas por Cluster",
                 fontsize=13, fontweight="bold")

    # Anotaciones con valores reales
    for i in range(len(stats.index)):
        for j in range(len(stats.columns)):
            ax.text(j, i, f"{stats.values[i, j]:.1f}",
                    ha="center", va="center", fontsize=9, color="black")

    plt.colorbar(im, ax=ax, label="Valor normalizado")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Heatmap guardado en: {output_path}")

    return stats


def validar_contra_categoria(labels, categoria_real, output_path: str):
    """Compara los clusters descubiertos con las categorias reales."""
    print("\n" + "=" * 65)
    print("  VALIDACION CONTRA CATEGORIAS REALES")
    print("=" * 65)

    # Excluir ruido si existe
    mask = labels != -1
    labels_clean = labels[mask]
    cat_clean = categoria_real[mask]

    # Metricas de comparacion
    ari = adjusted_rand_score(cat_clean, labels_clean)
    nmi = normalized_mutual_info_score(cat_clean, labels_clean)

    print(f"\n  Adjusted Rand Index (ARI): {ari:.4f}")
    print(f"    (1.0 = clusters perfectos, 0.0 = aleatorio)")
    print(f"\n  Normalized Mutual Info (NMI): {nmi:.4f}")
    print(f"    (1.0 = informacion perfecta compartida)")

    # Matriz de contingencia (usando pandas crosstab)
    cats = ["Rapido", "Medio", "Lento"]
    cluster_ids = sorted(set(labels_clean))

    # Construir matriz manualmente para garantizar orden
    ct = pd.crosstab(
        pd.Series(cat_clean.values, name="categoria"),
        pd.Series(labels_clean, name="cluster"),
    )
    # Reordenar filas para que sigan el orden Rapido/Medio/Lento
    ct = ct.reindex([c for c in cats if c in ct.index])
    cm = ct.values

    print(f"\n  Matriz de contingencia (Categoria real vs Cluster):")
    print(f"  {'':12}", end="")
    for c in cluster_ids:
        print(f"  Cluster{c:>2}", end="")
    print()
    for i, cat in enumerate(ct.index):
        print(f"  {cat:12}", end="")
        for cnt in cm[i]:
            print(f"  {cnt:>9}", end="")
        print()

    # Visualizacion
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(cm, aspect="auto", cmap="Blues")

    cluster_labels = [f"Cluster {c}" for c in cluster_ids]
    ax.set_xticks(range(len(cluster_labels)))
    ax.set_xticklabels(cluster_labels)
    ax.set_yticks(range(len(ct.index)))
    ax.set_yticklabels(list(ct.index))
    ax.set_xlabel("Cluster descubierto", fontsize=11)
    ax.set_ylabel("Categoria real", fontsize=11)
    ax.set_title(f"Validacion: Clusters vs Categorias\nARI={ari:.3f}  NMI={nmi:.3f}",
                 fontsize=12, fontweight="bold")

    for i in range(len(ct.index)):
        for j in range(len(cluster_labels)):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, f"{cm[i, j]}", ha="center", va="center",
                    color=color, fontsize=12, fontweight="bold")

    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"\n[OK] Matriz de validacion guardada en: {output_path}")

    return ari, nmi


def visualizar_comparacion_modelos(resultados: list, output_path: str):
    """Compara los Silhouette scores de los modelos."""
    print(f"\n[INFO] Generando comparacion de modelos...")

    nombres = [r["nombre"] for r in resultados]
    silhouette = [r["silhouette"] for r in resultados]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors_bar = ["#1e3a5f", "#8b5cf6", "#10b981"]
    bars = ax.bar(nombres, silhouette, color=colors_bar)
    ax.set_ylabel("Silhouette Score", fontsize=11)
    ax.set_title("Comparacion de Modelos - Aprendizaje No Supervisado",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, max(silhouette) * 1.2 if max(silhouette) > 0 else 1)
    ax.grid(axis="y", alpha=0.3)

    for bar, val in zip(bars, silhouette):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.005,
                f"{val:.4f}", ha="center", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Comparacion guardada en: {output_path}")


def guardar_reporte(resultados, mejor_k, ari, nmi, stats_clusters, output_path: str):
    """Guarda un reporte de texto con todos los resultados."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("REPORTE DE EVALUACION - APRENDIZAJE NO SUPERVISADO\n")
        f.write("=" * 70 + "\n")
        f.write("Actividad 4 - Inteligencia Artificial\n")
        f.write("Cristian David Alvis Ortiz\n")
        f.write("Corporacion Universitaria Iberoamericana - 2026-1\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"K optimo (segun Silhouette): {mejor_k}\n\n")

        f.write("COMPARACION DE MODELOS\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Modelo':<25} {'Silhouette':<15} {'Notas':<30}\n")
        for r in resultados:
            f.write(f"{r['nombre']:<25} {r['silhouette']:<15.4f} {r.get('notas', ''):<30}\n")

        f.write("\n\n")
        f.write("VALIDACION CONTRA CATEGORIAS REALES (K-Means)\n")
        f.write("-" * 70 + "\n")
        f.write(f"Adjusted Rand Index (ARI): {ari:.4f}\n")
        f.write(f"Normalized Mutual Info (NMI): {nmi:.4f}\n")

        f.write("\n\n")
        f.write("CARACTERIZACION DE CLUSTERS (K-Means)\n")
        f.write("-" * 70 + "\n")
        f.write(stats_clusters.round(2).to_string())
        f.write("\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n" + "#" * 65)
    print("#" + " " * 63 + "#")
    print("#  ACTIVIDAD 4 - APRENDIZAJE NO SUPERVISADO" + " " * 20 + "#")
    print("#  Clustering de Rutas TransMilenio Bogota" + " " * 21 + "#")
    print("#" + " " * 63 + "#")
    print("#" * 65)

    # 1. Cargar datos
    X, X_scaled, categoria_real, df = cargar_y_preparar_datos()

    # 2. Metodo del codo
    k_values, inercias, sil_scores = metodo_del_codo(X_scaled, k_max=10)
    mejor_k = visualizar_metodo_codo(
        k_values, inercias, sil_scores,
        f"{OUTPUT_DIR}/metodo_codo.png"
    )

    # 3. K-Means con el mejor K
    kmeans_model, kmeans_labels, kmeans_sil = entrenar_kmeans(X_scaled, mejor_k)

    # 4. DBSCAN
    dbscan_model, dbscan_labels, dbscan_sil = entrenar_dbscan(X_scaled)

    # 5. Jerarquico
    jer_model, jer_labels, jer_sil = entrenar_jerarquico(X_scaled, mejor_k)

    # 6. Resumen
    resultados = [
        {"nombre": f"K-Means (K={mejor_k})", "silhouette": kmeans_sil, "labels": kmeans_labels},
        {"nombre": "DBSCAN", "silhouette": dbscan_sil if dbscan_sil > 0 else 0, "labels": dbscan_labels,
         "notas": f"clusters={len(set(dbscan_labels))-(1 if -1 in dbscan_labels else 0)}"},
        {"nombre": f"Jerarquico (K={mejor_k})", "silhouette": jer_sil, "labels": jer_labels},
    ]

    print("\n" + "=" * 65)
    print("  RESUMEN COMPARATIVO DE MODELOS")
    print("=" * 65)
    print(f"\n  {'Modelo':<25} {'Silhouette Score':<20}")
    print(f"  {'-'*25} {'-'*20}")
    for r in resultados:
        print(f"  {r['nombre']:<25} {r['silhouette']:<20.4f}")

    mejor = max(resultados, key=lambda r: r["silhouette"])
    print(f"\n  >>> Mejor modelo: {mejor['nombre']} con Silhouette={mejor['silhouette']:.4f}")

    # 7. Visualizaciones
    print("\n" + "=" * 65)
    print("  GENERACION DE VISUALIZACIONES")
    print("=" * 65)

    visualizar_clusters_pca(X_scaled, kmeans_labels,
                            f"K-Means con K={mejor_k} - Visualizacion 2D (PCA)",
                            f"{OUTPUT_DIR}/clusters_kmeans_pca.png")
    visualizar_clusters_pca(X_scaled, dbscan_labels,
                            "DBSCAN - Visualizacion 2D (PCA)",
                            f"{OUTPUT_DIR}/clusters_dbscan_pca.png")
    visualizar_clusters_pca(X_scaled, jer_labels,
                            f"Clustering Jerarquico con K={mejor_k} - Visualizacion 2D (PCA)",
                            f"{OUTPUT_DIR}/clusters_jerarquico_pca.png")

    # 8. Caracterizacion (con K-Means)
    stats_clusters = caracterizar_clusters(df, kmeans_labels,
                                            f"{OUTPUT_DIR}/caracteristicas_clusters.png")

    # 9. Validacion contra categorias reales
    ari, nmi = validar_contra_categoria(kmeans_labels, categoria_real,
                                          f"{OUTPUT_DIR}/validacion_categorias.png")

    # 10. Comparacion de modelos
    visualizar_comparacion_modelos(resultados, f"{OUTPUT_DIR}/comparacion_modelos.png")

    # 11. Reporte
    guardar_reporte(resultados, mejor_k, ari, nmi, stats_clusters,
                    f"{OUTPUT_DIR}/reporte_evaluacion.txt")

    print("\n" + "=" * 65)
    print("  PROCESO COMPLETADO")
    print("=" * 65)
    print(f"  Todos los resultados estan en la carpeta: {OUTPUT_DIR}/")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
