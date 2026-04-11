"""
Modelo de Aprendizaje Supervisado - TransMilenio Bogota
=========================================================
Entrena modelos de clasificacion para predecir la categoria de
duracion de viaje (Rapido / Medio / Lento) en TransMilenio.

Modelos implementados:
- Arbol de Decision (modelo principal, alineado con Palma cap. 17)
- Random Forest (ensemble para comparacion)
- K-Nearest Neighbors (modelo basado en instancias)

Genera:
- Metricas de evaluacion (accuracy, precision, recall, F1)
- Matriz de confusion
- Visualizacion del arbol de decision
- Importancia de features
- Reporte de clasificacion

Autor: Cristian David Alvis Ortiz
Materia: Inteligencia Artificial - 2026-1
Actividad: 3 - Metodos de Aprendizaje Supervisado
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin GUI
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.preprocessing import StandardScaler


# Configuracion
DATASET_PATH = "dataset_rutas.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.25
OUTPUT_DIR = "resultados_supervisado"

# Features que usaremos para entrenar
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

TARGET = "categoria"


def cargar_y_preparar_datos():
    """Carga el dataset y lo divide en entrenamiento y prueba."""
    print("\n" + "=" * 65)
    print("  CARGA Y PREPARACION DE DATOS")
    print("=" * 65)

    df = pd.read_csv(DATASET_PATH)
    print(f"\n[OK] Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

    print(f"\n  Distribucion de clases:")
    for cat, count in df[TARGET].value_counts().items():
        pct = (count / len(df)) * 100
        print(f"    {cat:10}: {count:5} ({pct:5.1f}%)")

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    print(f"\n  Conjunto de entrenamiento: {len(X_train)} muestras")
    print(f"  Conjunto de prueba:        {len(X_test)} muestras")
    print(f"  Features utilizadas:       {len(FEATURES)}")

    return X_train, X_test, y_train, y_test, df


def evaluar_modelo(modelo, X_test, y_test, nombre: str) -> dict:
    """Calcula metricas de evaluacion para un modelo."""
    y_pred = modelo.predict(X_test)

    metricas = {
        "modelo": nombre,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "y_pred": y_pred,
    }
    return metricas


def imprimir_metricas(metricas: dict):
    """Imprime las metricas de un modelo de forma legible."""
    print(f"\n  --- {metricas['modelo']} ---")
    print(f"    Accuracy:  {metricas['accuracy']:.4f}  ({metricas['accuracy']*100:.2f}%)")
    print(f"    Precision: {metricas['precision']:.4f}")
    print(f"    Recall:    {metricas['recall']:.4f}")
    print(f"    F1-Score:  {metricas['f1']:.4f}")


def entrenar_arbol_decision(X_train, y_train, X_test, y_test):
    """Entrena un arbol de decision (modelo principal)."""
    print("\n" + "=" * 65)
    print("  MODELO 1: ARBOL DE DECISION")
    print("  (Palma cap. 17 - Aprendizaje de arboles y reglas)")
    print("=" * 65)

    modelo = DecisionTreeClassifier(
        criterion="gini",
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=RANDOM_STATE,
    )
    modelo.fit(X_train, y_train)

    metricas = evaluar_modelo(modelo, X_test, y_test, "Arbol de Decision")
    imprimir_metricas(metricas)

    print(f"\n  Profundidad del arbol: {modelo.get_depth()}")
    print(f"  Numero de hojas:       {modelo.get_n_leaves()}")

    return modelo, metricas


def entrenar_random_forest(X_train, y_train, X_test, y_test):
    """Entrena un Random Forest."""
    print("\n" + "=" * 65)
    print("  MODELO 2: RANDOM FOREST")
    print("  (Ensemble de arboles de decision)")
    print("=" * 65)

    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    modelo.fit(X_train, y_train)

    metricas = evaluar_modelo(modelo, X_test, y_test, "Random Forest")
    imprimir_metricas(metricas)

    return modelo, metricas


def entrenar_knn(X_train, y_train, X_test, y_test):
    """Entrena un KNN. Requiere normalizacion de features."""
    print("\n" + "=" * 65)
    print("  MODELO 3: K-NEAREST NEIGHBORS")
    print("  (Aprendizaje basado en instancias)")
    print("=" * 65)

    # KNN requiere features escaladas
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = KNeighborsClassifier(n_neighbors=7, weights="distance")
    modelo.fit(X_train_scaled, y_train)

    metricas = evaluar_modelo(modelo, X_test_scaled, y_test, "KNN (k=7)")
    imprimir_metricas(metricas)

    return modelo, metricas, scaler


def visualizar_arbol(modelo, output_path: str):
    """Genera una visualizacion grafica del arbol de decision."""
    print(f"\n[INFO] Generando visualizacion del arbol...")

    fig, ax = plt.subplots(figsize=(24, 14))
    plot_tree(
        modelo,
        feature_names=FEATURES,
        class_names=modelo.classes_,
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
        max_depth=4,  # Solo primeros 4 niveles para legibilidad
    )
    plt.title("Arbol de Decision - Categoria de Duracion de Viaje TransMilenio\n(Primeros 4 niveles)",
              fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Arbol guardado en: {output_path}")


def visualizar_matriz_confusion(metricas: dict, y_test, modelo, output_path: str):
    """Genera la matriz de confusion."""
    print(f"\n[INFO] Generando matriz de confusion...")

    cm = confusion_matrix(y_test, metricas["y_pred"], labels=modelo.classes_)
    fig, ax = plt.subplots(figsize=(7, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=modelo.classes_)
    disp.plot(ax=ax, cmap="Blues", values_format="d")
    plt.title(f"Matriz de Confusion - {metricas['modelo']}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Matriz de confusion guardada en: {output_path}")


def visualizar_importancia_features(modelo, output_path: str):
    """Genera grafico de importancia de features."""
    print(f"\n[INFO] Generando grafico de importancia de features...")

    importancias = modelo.feature_importances_
    indices = np.argsort(importancias)[::-1]
    features_ordenadas = [FEATURES[i] for i in indices]
    valores_ordenados = importancias[indices]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(features_ordenadas, valores_ordenados, color="#2c5f8a")
    ax.set_xlabel("Importancia", fontsize=11)
    ax.set_title("Importancia de Features - Arbol de Decision", fontsize=13, fontweight="bold")
    ax.invert_yaxis()

    # Etiquetas con valores
    for bar, val in zip(bars, valores_ordenados):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Grafico de importancia guardado en: {output_path}")

    print(f"\n  Ranking de features:")
    for i, (f, v) in enumerate(zip(features_ordenadas, valores_ordenados), 1):
        print(f"    {i}. {f:20} {v:.4f}")


def visualizar_comparacion_modelos(todas_metricas: list, output_path: str):
    """Compara las metricas de todos los modelos en un grafico."""
    print(f"\n[INFO] Generando comparacion de modelos...")

    nombres = [m["modelo"] for m in todas_metricas]
    accuracy = [m["accuracy"] for m in todas_metricas]
    precision = [m["precision"] for m in todas_metricas]
    recall = [m["recall"] for m in todas_metricas]
    f1 = [m["f1"] for m in todas_metricas]

    x = np.arange(len(nombres))
    width = 0.2

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - 1.5 * width, accuracy, width, label="Accuracy", color="#1e3a5f")
    ax.bar(x - 0.5 * width, precision, width, label="Precision", color="#2c5f8a")
    ax.bar(x + 0.5 * width, recall, width, label="Recall", color="#3b82f6")
    ax.bar(x + 1.5 * width, f1, width, label="F1-Score", color="#60a5fa")

    ax.set_xticks(x)
    ax.set_xticklabels(nombres)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title("Comparacion de Modelos - Aprendizaje Supervisado",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="lower right")
    ax.grid(axis="y", alpha=0.3)

    # Etiquetas en barras
    for i, val in enumerate(accuracy):
        ax.text(i - 1.5 * width, val + 0.01, f"{val:.3f}", ha="center", fontsize=8)
    for i, val in enumerate(precision):
        ax.text(i - 0.5 * width, val + 0.01, f"{val:.3f}", ha="center", fontsize=8)
    for i, val in enumerate(recall):
        ax.text(i + 0.5 * width, val + 0.01, f"{val:.3f}", ha="center", fontsize=8)
    for i, val in enumerate(f1):
        ax.text(i + 1.5 * width, val + 0.01, f"{val:.3f}", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"[OK] Comparacion guardada en: {output_path}")


def exportar_reglas_arbol(modelo, output_path: str):
    """Exporta las reglas del arbol como texto."""
    print(f"\n[INFO] Exportando reglas del arbol...")

    reglas = export_text(modelo, feature_names=FEATURES, max_depth=5)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("REGLAS DEL ARBOL DE DECISION (primeros 5 niveles)\n")
        f.write("=" * 70 + "\n")
        f.write(f"Modelo: DecisionTreeClassifier\n")
        f.write(f"Target: Categoria de duracion de viaje\n")
        f.write(f"Clases: Rapido, Medio, Lento\n")
        f.write("=" * 70 + "\n\n")
        f.write(reglas)
    print(f"[OK] Reglas guardadas en: {output_path}")


def guardar_reporte_completo(todas_metricas: list, modelo_arbol, X_test, y_test, output_path: str):
    """Guarda un reporte de texto con todos los resultados."""
    print(f"\n[INFO] Guardando reporte de clasificacion...")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("REPORTE DE EVALUACION - APRENDIZAJE SUPERVISADO\n")
        f.write("=" * 70 + "\n")
        f.write("Actividad 3 - Inteligencia Artificial\n")
        f.write("Cristian David Alvis Ortiz\n")
        f.write("Corporacion Universitaria Iberoamericana - 2026-1\n")
        f.write("=" * 70 + "\n\n")

        f.write("RESUMEN DE METRICAS\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Modelo':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<10}\n")
        for m in todas_metricas:
            f.write(f"{m['modelo']:<25} {m['accuracy']:<12.4f} {m['precision']:<12.4f} "
                    f"{m['recall']:<12.4f} {m['f1']:<10.4f}\n")

        f.write("\n\n")
        f.write("REPORTE DETALLADO - ARBOL DE DECISION (modelo principal)\n")
        f.write("-" * 70 + "\n")
        y_pred = modelo_arbol.predict(X_test)
        f.write(classification_report(y_test, y_pred, zero_division=0))

        f.write("\n\n")
        f.write("MATRIZ DE CONFUSION - ARBOL DE DECISION\n")
        f.write("-" * 70 + "\n")
        cm = confusion_matrix(y_test, y_pred, labels=modelo_arbol.classes_)
        f.write(f"{'':12}")
        for cls in modelo_arbol.classes_:
            f.write(f"{cls:>10}")
        f.write("\n")
        for i, cls in enumerate(modelo_arbol.classes_):
            f.write(f"{cls:12}")
            for j in range(len(modelo_arbol.classes_)):
                f.write(f"{cm[i][j]:>10}")
            f.write("\n")

    print(f"[OK] Reporte guardado en: {output_path}")


def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n" + "#" * 65)
    print("#" + " " * 63 + "#")
    print("#  ACTIVIDAD 3 - APRENDIZAJE SUPERVISADO" + " " * 23 + "#")
    print("#  Sistema de Clasificacion de Rutas TransMilenio" + " " * 14 + "#")
    print("#" + " " * 63 + "#")
    print("#" * 65)

    # 1. Cargar datos
    X_train, X_test, y_train, y_test, df = cargar_y_preparar_datos()

    # 2. Entrenar modelos
    arbol, m_arbol = entrenar_arbol_decision(X_train, y_train, X_test, y_test)
    rf, m_rf = entrenar_random_forest(X_train, y_train, X_test, y_test)
    knn, m_knn, scaler = entrenar_knn(X_train, y_train, X_test, y_test)

    todas_metricas = [m_arbol, m_rf, m_knn]

    # 3. Resumen comparativo
    print("\n" + "=" * 65)
    print("  RESUMEN COMPARATIVO DE MODELOS")
    print("=" * 65)
    print(f"\n  {'Modelo':<22} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<10}")
    print(f"  {'-'*22} {'-'*12} {'-'*12} {'-'*12} {'-'*10}")
    for m in todas_metricas:
        print(f"  {m['modelo']:<22} {m['accuracy']:<12.4f} {m['precision']:<12.4f} "
              f"{m['recall']:<12.4f} {m['f1']:<10.4f}")

    # Identificar mejor modelo
    mejor = max(todas_metricas, key=lambda m: m["f1"])
    print(f"\n  >>> Mejor modelo (F1-Score): {mejor['modelo']} con F1={mejor['f1']:.4f}")

    # 4. Visualizaciones
    print("\n" + "=" * 65)
    print("  GENERACION DE VISUALIZACIONES")
    print("=" * 65)

    visualizar_arbol(arbol, f"{OUTPUT_DIR}/arbol_decision.png")
    visualizar_matriz_confusion(m_arbol, y_test, arbol,
                                  f"{OUTPUT_DIR}/matriz_confusion_arbol.png")
    visualizar_matriz_confusion(m_rf, y_test, rf,
                                  f"{OUTPUT_DIR}/matriz_confusion_rf.png")
    visualizar_importancia_features(arbol, f"{OUTPUT_DIR}/importancia_features.png")
    visualizar_comparacion_modelos(todas_metricas, f"{OUTPUT_DIR}/comparacion_modelos.png")

    # 5. Exportar reglas y reporte
    exportar_reglas_arbol(arbol, f"{OUTPUT_DIR}/reglas_arbol.txt")
    guardar_reporte_completo(todas_metricas, arbol, X_test, y_test,
                              f"{OUTPUT_DIR}/reporte_evaluacion.txt")

    print("\n" + "=" * 65)
    print("  PROCESO COMPLETADO")
    print("=" * 65)
    print(f"  Todos los resultados estan en la carpeta: {OUTPUT_DIR}/")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
