library(ggplot2)

# --- Rutas del proyecto (relativas a la raiz) -----
dataset_path <- "data/dataset/consumo_energia.csv"
processed_dir <- "data/processed"
figures_dir <- "public/assets/images/figures/r/hypothesis"

dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

# Nivel de significancia
alpha <- 0.05

# --------------------------------------------------
# 1. LECTURA DEL DATASET (el mismo generado por Python, semilla 42)
# --------------------------------------------------
df <- read.csv(dataset_path, encoding = "UTF-8")
df$sector <- as.factor(df$sector)
cat("[OK] Dataset leido:", nrow(df), "filas\n")

# --------------------------------------------------
# 2. PRUEBAS DE HIPOTESIS (funciones base de R)
# --------------------------------------------------

# --- 2.1 Normalidad con shapiro.test por sector ---
# H0: los datos provienen de una distribucion normal
normality_rows <- lapply(levels(df$sector), function(s) {
  test <- shapiro.test(df$consumo_kwh[df$sector == s])
  data.frame(
    prueba = "Shapiro-Wilk (R)",
    grupo = s,
    estadistico = round(test$statistic, 4),
    p_valor = round(test$p.value, 4),
    decision = ifelse(test$p.value > alpha, "No se rechaza H0 (normal)", "Se rechaza H0 (no normal)")
  )
})
normality_r <- do.call(rbind, normality_rows)

# Homogeneidad de varianzas con bartlett.test (equivalente a Levene)
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

# --- 2.2 Prueba t con t.test ----------------------
# H0: consumo medio Residencial == consumo medio Comercial
residential <- df$consumo_kwh[df$sector == "Residencial"]
commercial <- df$consumo_kwh[df$sector == "Comercial"]
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

# --- 2.3 ANOVA con aov + TukeyHSD -----------------
# H0: el consumo medio es igual en los 3 sectores
anova_model <- aov(consumo_kwh ~ sector, data = df)
anova_summary <- summary(anova_model)[[1]]
write.csv(anova_summary, file.path(processed_dir, "anova_results_r.csv"))

tukey <- TukeyHSD(anova_model)
write.csv(as.data.frame(tukey$sector), file.path(processed_dir, "tukey_posthoc_r.csv"))
cat("[OK] ANOVA (aov) -> anova_results_r.csv | TukeyHSD -> tukey_posthoc_r.csv\n")

# --- 2.4 Correlacion (cor.test) y regresion lineal (lm) ---
# H0: no hay relacion lineal entre temperatura y consumo (r = 0)
pearson <- cor.test(df$temperatura_c, df$consumo_kwh)
linear_model <- lm(consumo_kwh ~ temperatura_c, data = df)

regression_r <- data.frame(
  prueba = "Pearson (cor.test) + lm (R)",
  r_pearson = round(pearson$estimate, 4),
  p_valor = format(pearson$p.value, digits = 4),
  intercepto_b0 = round(coef(linear_model)[1], 2),
  pendiente_b1 = round(coef(linear_model)[2], 2),
  r_cuadrado = round(summary(linear_model)$r.squared, 4),
  decision = ifelse(pearson$p.value < alpha, "Relacion significativa", "Sin relacion significativa")
)
# Insight clave: la correlacion global se diluye porque los sectores tienen
# niveles de consumo muy distintos; por sector la relacion si aparece.
sector_rows <- lapply(levels(df$sector), function(s) {
  sub_df <- df[df$sector == s, ]
  test <- cor.test(sub_df$temperatura_c, sub_df$consumo_kwh)
  data.frame(
    prueba = paste0("Pearson (", s, ")"),
    r_pearson = round(test$estimate, 4),
    p_valor = format(test$p.value, digits = 4),
    intercepto_b0 = NA, pendiente_b1 = NA, r_cuadrado = NA,
    decision = ifelse(test$p.value < alpha, "Relacion significativa", "Sin relacion significativa")
  )
})
regression_r <- rbind(regression_r, do.call(rbind, sector_rows))

write.csv(regression_r, file.path(processed_dir, "regression_results_r.csv"), row.names = FALSE)
cat("[OK] Correlacion y regresion -> regression_results_r.csv\n")
