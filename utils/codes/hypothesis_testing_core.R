normality_rows <- lapply(sector_order, function(s) {
  test <- shapiro.test(consumo(s))
  data.frame(
    prueba = "Shapiro-Wilk (R)",
    grupo = s,
    estadistico = round(test$statistic, 4),
    p_valor = round(test$p.value, 4),
    decision = ifelse(test$p.value > alpha, "No se rechaza H0 (normal)", "Se rechaza H0 (no normal)")
  )
})
normality_r <- do.call(rbind, normality_rows)

bartlett <- bartlett.test(consumo_kwh ~ sector, data = df)
normality_r <- rbind(normality_r, data.frame(
  prueba = "Bartlett (R)",
  grupo = "Los 3 sectores",
  estadistico = round(bartlett$statistic, 4),
  p_valor = round(bartlett$p.value, 4),
  decision = ifelse(bartlett$p.value > alpha, "Varianzas iguales", "Varianzas distintas")
))
write.csv(normality_r, file.path(processed_dir, "normality_tests_r.csv"), row.names = FALSE)
cat("[OK] Normalidad y Bartlett -> normality_tests_r.csv\n")

residential <- consumo("Residencial")
commercial <- consumo("Comercial")
t_result <- t.test(residential, commercial, var.equal = FALSE)  # Welch

ttest_r <- data.frame(
  prueba = "t de Student - t.test (R)",
  media_residencial = round(mean(residential), 2),
  media_comercial = round(mean(commercial), 2),
  estadistico_t = round(t_result$statistic, 4),
  p_valor = format(t_result$p.value, digits = 4),
  decision = ifelse(t_result$p.value < alpha, "Se rechaza H0: las medias son diferentes", "No se rechaza H0")
)
write.csv(ttest_r, file.path(processed_dir, "ttest_results_r.csv"), row.names = FALSE)
cat("[OK] Prueba t -> ttest_results_r.csv\n")

anova_model <- aov(consumo_kwh ~ sector, data = df)
anova_summary <- summary(anova_model)[[1]]
write.csv(anova_summary, file.path(processed_dir, "anova_results_r.csv"))

tukey <- TukeyHSD(anova_model)
tukey_df <- as.data.frame(tukey$sector)
tukey_df$comparacion <- rownames(tukey_df)
write.csv(tukey_df, file.path(processed_dir, "tukey_posthoc_r.csv"), row.names = FALSE)
cat("[OK] ANOVA (aov) -> anova_results_r.csv | TukeyHSD -> tukey_posthoc_r.csv\n")

f_anova <- anova_summary[["F value"]][1]
p_anova <- anova_summary[["Pr(>F)"]][1]

pearson <- cor.test(df$temperatura_c, df$consumo_kwh)
linear_model <- lm(consumo_kwh ~ temperatura_c, data = df)

regression_r <- data.frame(
  ambito = "Global",
  prueba = "Pearson (cor.test) + lm (R)",
  n = nrow(df),
  r_pearson = round(unname(pearson$estimate), 4),
  p_valor = round(pearson$p.value, 6),
  intercepto_b0 = round(unname(coef(linear_model)[1]), 2),
  pendiente_b1 = round(unname(coef(linear_model)[2]), 2),
  desv_consumo = round(sd(df$consumo_kwh), 2),
  r_cuadrado = round(summary(linear_model)$r.squared, 4),
  decision = ifelse(pearson$p.value < alpha, "Relacion significativa", "Sin relacion significativa")
)

sector_rows <- lapply(sector_order, function(s) {
  sub_df <- df[df$sector == s, ]
  test <- cor.test(sub_df$temperatura_c, sub_df$consumo_kwh)
  model_s <- lm(consumo_kwh ~ temperatura_c, data = sub_df)
  data.frame(
    ambito = s,
    prueba = paste0("Pearson (", s, ")"),
    n = nrow(sub_df),
    r_pearson = round(unname(test$estimate), 4),
    p_valor = round(test$p.value, 6),
    intercepto_b0 = round(unname(coef(model_s)[1]), 2),
    pendiente_b1 = round(unname(coef(model_s)[2]), 2),
    desv_consumo = round(sd(sub_df$consumo_kwh), 2),
    r_cuadrado = round(summary(model_s)$r.squared, 4),
    decision = ifelse(test$p.value < alpha, "Relacion significativa", "Sin relacion significativa")
  )
})
regression_r <- rbind(regression_r, do.call(rbind, sector_rows))

write.csv(regression_r, file.path(processed_dir, "regression_results_r.csv"), row.names = FALSE)
cat("[OK] Correlacion y regresion -> regression_results_r.csv\n")


n1 <- length(residential); n2 <- length(commercial)
s1 <- sd(residential); s2 <- sd(commercial)

pooled_sd <- sqrt(((n1 - 1) * s1^2 + (n2 - 1) * s2^2) / (n1 + n2 - 2))
cohen_d <- (mean(commercial) - mean(residential)) / pooled_sd
hedges_g <- cohen_d * (1 - 3 / (4 * (n1 + n2) - 9))
se_d <- sqrt((n1 + n2) / (n1 * n2) + cohen_d^2 / (2 * (n1 + n2)))
d_ci <- cohen_d + c(-1, 1) * qnorm(1 - alpha / 2) * se_d

ss_between <- anova_summary[["Sum Sq"]][1]
ss_within <- anova_summary[["Sum Sq"]][2]
df_between <- anova_summary[["Df"]][1]
df_within <- anova_summary[["Df"]][2]
ss_total <- ss_between + ss_within
ms_within <- ss_within / df_within

eta_sq <- ss_between / ss_total
omega_sq <- (ss_between - df_between * ms_within) / (ss_total + ms_within)
cohen_f <- sqrt(eta_sq / (1 - eta_sq))

ncp_t <- abs(cohen_d) * sqrt(n1 * n2 / (n1 + n2))
df_t <- n1 + n2 - 2
crit_t <- qt(1 - alpha / 2, df_t)
power_t <- pt(crit_t, df_t, ncp = ncp_t, lower.tail = FALSE) +
  pt(-crit_t, df_t, ncp = ncp_t, lower.tail = TRUE)

ncp_f <- nrow(df) * cohen_f^2
power_anova <- pf(qf(1 - alpha, df_between, df_within), df_between, df_within,
                  ncp = ncp_f, lower.tail = FALSE)

r_detectable <- tanh((qnorm(1 - alpha / 2) + qnorm(0.80)) / sqrt(nrow(df) - 3))

effects_r <- data.frame(
  medida = c("d de Cohen (Res. vs Com.)", "g de Hedges (Res. vs Com.)",
             "eta cuadrado (ANOVA sector)", "omega cuadrado (ANOVA sector)",
             "f de Cohen (ANOVA sector)", "Potencia observada (t de Welch)",
             "Potencia observada (ANOVA)",
             "r minimo detectable (n = 300, potencia 0,80)"),
  valor = round(c(cohen_d, hedges_g, eta_sq, omega_sq, cohen_f,
                  power_t, power_anova, r_detectable), 4),
  ic_inferior = c(round(d_ci[1], 4), rep(NA, 7)),
  ic_superior = c(round(d_ci[2], 4), rep(NA, 7))
)
write.csv(effects_r, file.path(processed_dir, "effect_sizes_r.csv"), row.names = FALSE)
cat("[OK] Tamanos de efecto y potencia -> effect_sizes_r.csv\n")


welch <- oneway.test(consumo_kwh ~ sector, data = df, var.equal = FALSE)
welch_r <- data.frame(
  prueba = "ANOVA de Welch (oneway.test)",
  estadistico_f = round(unname(welch$statistic), 4),
  gl_numerador = round(unname(welch$parameter[1]), 2),
  gl_denominador = round(unname(welch$parameter[2]), 2),
  p_valor = format(welch$p.value, digits = 4),
  decision = ifelse(welch$p.value < alpha, "Se rechaza H0", "No se rechaza H0")
)
write.csv(welch_r, file.path(processed_dir, "welch_anova_r.csv"), row.names = FALSE)

games_howell <- function(data) {
  k <- length(sector_order)
  pairs <- combn(sector_order, 2, simplify = FALSE)
  rows <- lapply(pairs, function(pair) {
    ga <- data$consumo_kwh[data$sector == pair[1]]
    gb <- data$consumo_kwh[data$sector == pair[2]]
    na <- length(ga); nb <- length(gb)
    va <- var(ga); vb <- var(gb)
    diff <- mean(gb) - mean(ga)

    se <- sqrt(va / na + vb / nb)
    df_wl <- (va / na + vb / nb)^2 /
      ((va / na)^2 / (na - 1) + (vb / nb)^2 / (nb - 1))
    q_stat <- abs(diff) / se * sqrt(2)
    p_adj <- ptukey(q_stat, nmeans = k, df = df_wl, lower.tail = FALSE)
    margin <- qtukey(1 - alpha, nmeans = k, df = df_wl) / sqrt(2) * se

    data.frame(
      comparacion = paste(pair[2], "-", pair[1]),
      diferencia = round(diff, 3),
      ic_inferior = round(diff - margin, 3),
      ic_superior = round(diff + margin, 3),
      q = round(q_stat, 3),
      gl_welch = round(df_wl, 2),
      p_ajustado = signif(p_adj, 4),
      decision = ifelse(p_adj < alpha, "Se rechaza H0", "No se rechaza H0")
    )
  })
  do.call(rbind, rows)
}
gh_r <- games_howell(df)
write.csv(gh_r, file.path(processed_dir, "games_howell_r.csv"), row.names = FALSE)
cat("[OK] ANOVA de Welch -> welch_anova_r.csv | Games-Howell -> games_howell_r.csv\n")