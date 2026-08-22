import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# --- Rutas del proyecto (relativas a la raiz) -----
DATASET_PATH = "data/dataset/consumo_energia.csv"
PROCESSED_DIR = "data/processed"
FIGURES_DIR = "public/assets/images/figures/python/hypothesis"

# Nivel de significancia usado en todas las pruebas
ALPHA = 0.05

def run_normality_and_levene(df):
    """Shapiro-Wilk por sector (normalidad) y Levene (homogeneidad de varianzas).

    H0 (Shapiro): los datos provienen de una distribucion normal.
    H0 (Levene):  las varianzas de los grupos son iguales.
    """
    results = []
    groups = []
    for sector, data in df.groupby("sector"):
        stat, p_value = stats.shapiro(data["consumo_kwh"])
        groups.append(data["consumo_kwh"])
        results.append(
            {
                "prueba": "Shapiro-Wilk",
                "grupo": sector,
                "estadistico": round(stat, 4),
                "p_valor": round(p_value, 4),
                "decision": "No se rechaza H0 (normal)" if p_value > ALPHA else "Se rechaza H0 (no normal)",
            }
        )

    # Levene compara las varianzas de los 3 sectores a la vez
    stat, p_value = stats.levene(*groups)
    results.append(
        {
            "prueba": "Levene",
            "grupo": "Los 3 sectores",
            "estadistico": round(stat, 4),
            "p_valor": round(p_value, 4),
            "decision": "Varianzas iguales" if p_value > ALPHA else "Varianzas distintas",
        }
    )

    out = pd.DataFrame(results)
    out.to_csv(f"{PROCESSED_DIR}/normality_tests.csv", index=False, encoding="utf-8")
    print("[OK] Pruebas de normalidad y Levene -> normality_tests.csv")
    return out


def run_ttest(df):
    """t de Student para 2 muestras independientes (scipy.stats).

    H0: el consumo medio del sector Residencial es igual al del Comercial.
    H1: los consumos medios son diferentes.
    """
    residential = df[df["sector"] == "Residencial"]["consumo_kwh"]
    commercial = df[df["sector"] == "Comercial"]["consumo_kwh"]

    stat, p_value = stats.ttest_ind(residential, commercial, equal_var=False)

    out = pd.DataFrame(
        [
            {
                "prueba": "t de Student (Welch)",
                "grupo_1": "Residencial",
                "media_1": round(residential.mean(), 2),
                "grupo_2": "Comercial",
                "media_2": round(commercial.mean(), 2),
                "estadistico_t": round(stat, 4),
                "p_valor": round(p_value, 6),
                "decision": "Se rechaza H0: las medias son diferentes" if p_value < ALPHA else "No se rechaza H0",
            }
        ]
    )
    out.to_csv(f"{PROCESSED_DIR}/ttest_results.csv", index=False, encoding="utf-8")
    print("[OK] Prueba t -> ttest_results.csv")
    return out


def run_anova_tukey(df):
    """ANOVA de un factor (statsmodels) + post-hoc de Tukey.

    H0: el consumo medio es igual en los 3 sectores.
    H1: al menos un sector tiene un consumo medio diferente.
    """
    # ANOVA con formula estilo R: consumo ~ sector
    model = ols("consumo_kwh ~ C(sector)", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    anova_table.to_csv(f"{PROCESSED_DIR}/anova_results.csv", encoding="utf-8")

    # Tukey dice ENTRE CUALES sectores hay diferencias
    tukey = pairwise_tukeyhsd(df["consumo_kwh"], df["sector"], alpha=ALPHA)
    tukey_df = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])
    tukey_df.to_csv(f"{PROCESSED_DIR}/tukey_posthoc.csv", index=False, encoding="utf-8")

    print("[OK] ANOVA -> anova_results.csv | Tukey -> tukey_posthoc.csv")
    return anova_table, tukey_df


def run_correlation_regression(df):
    """Correlacion de Pearson (scipy) + regresion lineal OLS (statsmodels).

    H0: no existe relacion lineal entre temperatura y consumo (r = 0).
    H1: existe relacion lineal (r != 0).
    """
    r, p_value = stats.pearsonr(df["temperatura_c"], df["consumo_kwh"])

    # Regresion lineal simple: consumo = b0 + b1 * temperatura
    x = sm.add_constant(df["temperatura_c"])
    model = sm.OLS(df["consumo_kwh"], x).fit()

    rows = [
        {
            "prueba": "Pearson + OLS (global)",
            "r_pearson": round(r, 4),
            "p_valor": round(p_value, 6),
            "intercepto_b0": round(model.params["const"], 2),
            "pendiente_b1": round(model.params["temperatura_c"], 2),
            "r_cuadrado": round(model.rsquared, 4),
            "decision": "Relacion significativa" if p_value < ALPHA else "Sin relacion significativa",
        }
    ]

    # Insight clave: la correlacion GLOBAL se diluye porque los sectores tienen
    # niveles de consumo muy distintos. Al analizar POR SECTOR, la relacion
    # temperatura-consumo si aparece (esto se ve claramente en las figuras 4 y 5).
    for sector, data in df.groupby("sector"):
        r_s, p_s = stats.pearsonr(data["temperatura_c"], data["consumo_kwh"])
        rows.append(
            {
                "prueba": f"Pearson ({sector})",
                "r_pearson": round(r_s, 4),
                "p_valor": round(p_s, 6),
                "intercepto_b0": None,
                "pendiente_b1": None,
                "r_cuadrado": None,
                "decision": "Relacion significativa" if p_s < ALPHA else "Sin relacion significativa",
