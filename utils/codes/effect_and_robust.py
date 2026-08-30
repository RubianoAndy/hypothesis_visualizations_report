def welch_anova(groups):
    """ANOVA de Welch: F, grados de libertad y valor p sin homocedasticidad."""
    k = len(groups)
    n = np.array([len(g) for g in groups], dtype=float)
    means = np.array([g.mean() for g in groups])
    variances = np.array([g.var(ddof=1) for g in groups])

    weights = n / variances               # peso inverso a la varianza del grupo
    total_weight = weights.sum()
    weighted_mean = (weights * means).sum() / total_weight

    numerator = (weights * (means - weighted_mean) ** 2).sum() / (k - 1)
    lam = ((1 - weights / total_weight) ** 2 / (n - 1)).sum()
    denominator = 1 + (2 * (k - 2) / (k**2 - 1)) * lam

    f_stat = numerator / denominator
    df1 = k - 1
    df2 = (k**2 - 1) / (3 * lam)
    p_value = stats.f.sf(f_stat, df1, df2)
    return f_stat, df1, df2, p_value


def games_howell(df):
    """Post-hoc de Games-Howell: la alternativa a Tukey sin varianzas iguales.

    Usa el error estandar de Welch en cada par y los grados de libertad de
    Welch-Satterthwaite, contrastando contra la distribucion del rango
    estudentizado igual que Tukey.
    """
    k = len(SECTOR_ORDER)
    rows = []
    for a, b in itertools.combinations(SECTOR_ORDER, 2):
        ga, gb = sector_series(df, a), sector_series(df, b)
        na, nb = len(ga), len(gb)
        va, vb = ga.var(ddof=1), gb.var(ddof=1)
        diff = gb.mean() - ga.mean()

        se = np.sqrt(va / na + vb / nb)
        # Grados de libertad de Welch-Satterthwaite para este par
        df_wl = (va / na + vb / nb) ** 2 / (
            (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
        )
        q_stat = abs(diff) / se * np.sqrt(2)
        p_adj = stats.studentized_range.sf(q_stat, k, df_wl)
        q_crit = stats.studentized_range.ppf(1 - ALPHA, k, df_wl)
        margin = q_crit / np.sqrt(2) * se

        rows.append(
            {
                "comparacion": f"{b} - {a}",
                "diferencia": round(diff, 3),
                "ic_inferior": round(diff - margin, 3),
                "ic_superior": round(diff + margin, 3),
                "q": round(q_stat, 3),
                "gl_welch": round(df_wl, 2),
                "p_ajustado": float(f"{p_adj:.3e}"),
                "decision": "Se rechaza H0" if p_adj < ALPHA else "No se rechaza H0",
            }
        )
    return pd.DataFrame(rows)
