def run_normality_and_levene(df):
    """Shapiro-Wilk por sector (normalidad) y Levene (homogeneidad de varianzas).

    H0 (Shapiro): los datos provienen de una distribucion normal.
    H0 (Levene):  las varianzas de los grupos son iguales.
    """
    results = []
    groups = []
    for sector in SECTOR_ORDER:
        data = sector_series(df, sector)
        stat, p_value = stats.shapiro(data)
        groups.append(data)
        results.append(
            {
                "prueba": "Shapiro-Wilk",
                "grupo": sector,
                "estadistico": round(stat, 4),
                "p_valor": round(p_value, 4),
                "decision": "No se rechaza H0 (normal)" if p_value > ALPHA else "Se rechaza H0 (no normal)",
            }
        )

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
    residential = sector_series(df, "Residencial")
    commercial = sector_series(df, "Comercial")

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
    model = ols("consumo_kwh ~ C(sector)", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    anova_table.to_csv(f"{PROCESSED_DIR}/anova_results.csv", encoding="utf-8")

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

    x = sm.add_constant(df["temperatura_c"])
    model = sm.OLS(df["consumo_kwh"], x).fit()

    rows = [
        {
            "ambito": "Global",
            "prueba": "Pearson + OLS (global)",
            "n": len(df),
            "r_pearson": round(r, 4),
            "p_valor": round(p_value, 6),
            "intercepto_b0": round(model.params["const"], 2),
            "pendiente_b1": round(model.params["temperatura_c"], 2),
            "desv_consumo": round(df["consumo_kwh"].std(ddof=1), 2),
            "r_cuadrado": round(model.rsquared, 4),
            "decision": "Relacion significativa" if p_value < ALPHA else "Sin relacion significativa",
        }
    ]

    for sector in SECTOR_ORDER:
        data = df[df["sector"] == sector]
        r_s, p_s = stats.pearsonr(data["temperatura_c"], data["consumo_kwh"])
        x_s = sm.add_constant(data["temperatura_c"])
        model_s = sm.OLS(data["consumo_kwh"], x_s).fit()
        rows.append(
            {
                "ambito": sector,
                "prueba": f"Pearson ({sector})",
                "n": len(data),
                "r_pearson": round(r_s, 4),
                "p_valor": round(p_s, 6),
                "intercepto_b0": round(model_s.params["const"], 2),
                "pendiente_b1": round(model_s.params["temperatura_c"], 2),
                "desv_consumo": round(data["consumo_kwh"].std(ddof=1), 2),
                "r_cuadrado": round(model_s.rsquared, 4),
                "decision": "Relacion significativa" if p_s < ALPHA else "Sin relacion significativa",
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(f"{PROCESSED_DIR}/regression_results.csv", index=False, encoding="utf-8")
    print("[OK] Correlacion y regresion -> regression_results.csv")
    return model, out
