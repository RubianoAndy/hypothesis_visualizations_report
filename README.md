<div align="center">
    <img src="assets/images/Logo.png" width="250" alt="Logo Universidad de La Salle">
</div>

# Pruebas de hipótesis y visualización avanzada sobre el consumo energético: cómo la agregación de subpoblaciones enmascara una relación estadística real

## 📋 Información General

<div align="center">
    <img src="assets/images/author/Andy Rubiano.png" width="200" alt="Foto de Andrés Giovanny Rubiano Muñoz" style="border-radius: 10px;">
</div>

| Aspecto | Detalles |
|--------|----------|
| **Autor** | Andrés Giovanny Rubiano Muñoz "Andy Rubiano" |
| **Correo** | arubiano67@unisalle.edu.co |
| **Asignatura** | Ciencia de Datos — Actividad 5 |
| **Docente** | Fabián Camilo Castro Riveros |
| **Unidad** | Unidad 2 · Pruebas de hipótesis y visualización interactiva |
| **Programa** | Maestría en Inteligencia Artificial |
| **Universidad** | Universidad de La Salle |
| **Formato** | Artículo IEEE conference (`IEEEtran`, dos columnas) |
| **Extensión** | 14 páginas: 10 de cuerpo y 4 de anexos de código y referencias |
| **Año** | 2026 |
| **Estado** | Completado |

---

## 🎯 Descripción del Proyecto

Informe en LaTeX que documenta el laboratorio de inferencia estadística del proyecto hermano [`hypothesis_visualizations`](../hypothesis_visualizations), donde se contrastan cinco hipótesis sobre el consumo energético mensual de **300 clientes** repartidos en tres sectores.

El informe no se limita a reportar valores *p*. Su tesis es que **la visualización forma parte del contraste estadístico y no de su presentación**, y la demuestra sobre un caso construido: la relación entre temperatura y consumo se introduce por diseño con una magnitud conocida y, pese a ello, la prueba de hipótesis aplicada al conjunto agregado **no la detecta**.

### El hallazgo central

> La correlación temperatura–consumo es no significativa a nivel global (r = 0,063; p = 0,277) pero sí lo es dentro del sector Residencial (r = 0,595; p < 0,001). El informe cuantifica el mecanismo con la identidad **r = b₁·s_T/s_Y**: la pendiente **sobrevive** a la agregación (b₁ = 3,42 frente al valor de diseño de 4), pero la desviación estándar del consumo se triplica al mezclar sectores —de 40,6 a 317,5 kWh—, diluyendo la correlación sin alterar el efecto subyacente.

Es decir, **el estimador del efecto sobrevive a la agregación; la medida de asociación estandarizada no**. Un valor *p* elevado admite entonces dos lecturas incompatibles —ausencia de efecto o enmascaramiento— que el estadístico no distingue y la figura sí.

### Objetivos Principales

- Formular cinco hipótesis sobre el consumo y contrastarlas con la prueba adecuada a cada caso.
- Verificar los supuestos de normalidad y homocedasticidad antes de aplicar pruebas paramétricas, y corregir el procedimiento cuando no se cumplen.
- Reportar el **tamaño del efecto** y la **potencia** junto a cada valor *p*, y contrastar la robustez de las conclusiones cuando un supuesto no se cumple.
- Representar cada resultado con su visualización, incluyendo dos figuras interactivas y un *dashboard* construidos con Plotly, replicados con ggplot2.
- Interpretar los hallazgos en términos de decisión y no solo de significancia estadística.
- Entregar el informe escrito aplicando la normativa IEEE.

---

## 📚 Estructura del Repositorio

```
.
├── main.tex                          # Documento principal (preámbulo + \input de secciones y anexos)
├── IEEEtran.cls                      # Clase LaTeX del formato IEEE conference
├── README.md                         # Este archivo
├── assets/
│   └── images/
│       ├── Logo.png                  # Logo institucional (marca de agua)
│       ├── author/                   # Fotografía del autor
│       └── figures/
│           ├── python/               # 9 figuras (Matplotlib, seaborn y Plotly)
│           └── r/                    # 9 réplicas en ggplot2, 5 citadas desde el informe
├── src/
│   ├── sections/                     # Secciones del informe (en orden de compilación)
│   │   ├── introduction/             # I. Introducción
│   │   ├── methodology/              # II. Metodología
│   │   ├── results/                  # III. Resultados
│   │   ├── discussion/                # IV. El papel de la visualización
│   │   ├── conclusions/               # V. Conclusiones
│   │   └── recommendations/           # VI. Recomendaciones (con el enlace al repositorio)
│   └── appendices/
│       ├── python-code/              # Anexo A: núcleo estadístico en Python
│       └── r-code/                   # Anexo B: núcleo estadístico en R
├── utils/
│   ├── codes/                        # Extractos citados vía \lstinputlisting
│   │   ├── sync_appendix.py                   # Extrae los extractos del script real (ver nota)
│   │   ├── hypothesis_testing_core.py         # Las cinco pruebas con SciPy y statsmodels
│   │   ├── effect_and_robust.py               # ANOVA de Welch y Games-Howell desde sus fórmulas
│   │   ├── plotly_figure.py                   # Construcción de la figura interactiva
│   │   └── hypothesis_testing_core.R          # Recálculo independiente en R base
│   └── references/
│       └── references.bib            # Bibliografía IEEE (16 referencias citadas)
└── build/                            # Artefactos de compilación LaTeX (generado)
```

> ℹ️ Los anexos reproducen el **núcleo estadístico** de cada script, no su totalidad: el código de generación del dataset y de las nueve figuras excede el margen razonable de un anexo. Los scripts completos están en [`hypothesis_visualizations`](../hypothesis_visualizations).

> 🔄 **Los extractos no se transcriben a mano.** [`utils/codes/sync_appendix.py`](utils/codes/sync_appendix.py) los extrae del script real —parseando el AST en Python y por marcadores de bloque en R— de modo que lo impreso en el PDF es código que efectivamente se ejecutó. Ejecútalo antes de compilar si tocaste los scripts:
>
> ```bash
> python utils/codes/sync_appendix.py
> ```

---

## 🧭 Contenido del Informe

| # | Sección | Contenido |
|---|---|---|
| — | Resumen | Las cifras principales y el hallazgo central |
| I | Introducción | Qué mide y qué no mide un valor *p*; el cuarteto de Anscombe y la agregación de subpoblaciones como marco |
| II | Metodología | Conjunto de datos (**Tabla I**), diseño del contraste (**Tabla II**), tamaño del efecto y potencia, contrastes robustos, y el **plan de visualización** que mapea cada hipótesis a su figura y biblioteca (**Tabla III**) — **11 ecuaciones** |
| III | Resultados | Supuestos con Q-Q, prueba t, ANOVA + Tukey, **tamaños de efecto y potencia**, **robustez con Welch y Games-Howell**, y regresión — **Tablas IV–X** y **Figuras 1–6** |
| IV | El papel de la visualización | La figura interactiva (**Figura 7**), la identidad *r = b₁·s_T/s_Y* descompuesta (**Figura 8**), el *dashboard* (**Figura 9**), la verificación cruzada con las réplicas en ggplot2 (**Figuras 10–13**) y las limitaciones |
| V | Conclusiones | Ocho conclusiones sobre el protocolo de contraste, la robustez y la verificación cruzada |
| VI | Recomendaciones | Cinco recomendaciones para la toma de decisiones y el enlace al repositorio del proyecto |
| A | Anexo · Python | Las cinco pruebas con SciPy y statsmodels, el ANOVA de Welch y Games-Howell implementados desde sus fórmulas, y la figura de Plotly |
| B | Anexo · R | El recálculo independiente con `shapiro.test`, `t.test`, `aov`, `TukeyHSD`, `cor.test`, `lm` y `oneway.test`, más los efectos y Games-Howell sobre `ptukey` |
| — | Referencias | 16 entradas en formato IEEE |

### Las cinco hipótesis contrastadas

| # | Hipótesis nula | Python | R |
|---|---|---|---|
| 1 | El consumo de cada sector es normal | `scipy.stats.shapiro` | `shapiro.test` |
| 2 | Las varianzas son homogéneas | `scipy.stats.levene` | `bartlett.test` |
| 3 | μ Residencial = μ Comercial | `ttest_ind` (Welch) | `t.test` |
| 4 | Las tres medias son iguales | `ols` + `anova_lm` + Tukey | `aov` + `TukeyHSD` |
| 5 | ρ(temperatura, consumo) = 0 | `pearsonr` + `sm.OLS` | `cor.test` + `lm` |

### Resultados principales

| Prueba | Estadístico | *p* | Conclusión |
|---|---|---|---|
| Shapiro-Wilk (3 sectores) | 0,987 – 0,993 | > 0,42 | Normalidad admisible |
| Levene / Bartlett | 60,43 / 199,39 | < 0,001 | Varianzas **heterogéneas** → Welch |
| t de Welch (Res. vs Com.) | −23,54 | 2,3 × 10⁻⁴⁹ | 186,98 vs 431,30 kWh |
| ANOVA de un factor | F = 775,99 | 1,2 × 10⁻¹¹⁸ | El sector explica el **83,9 %** |
| Tukey (3 comparaciones) | — | < 0,001 | Ningún par es equivalente |
| **ANOVA de Welch** | F = 830,22 | < 0,001 | Misma decisión **sin** homocedasticidad |
| **Games-Howell** (3 comparaciones) | — | < 0,001 | Misma decisión; cambia la precisión |
| **Tamaño del efecto** | *d* = 3,33 · ω² = 0,838 | — | Efecto **muy grande**, no solo significativo |
| **Potencia** (*t* y ANOVA) | > 0,999 | — | La significancia no viene del tamaño muestral |
| Pearson global | r = 0,063 | 0,277 | **No significativa** |
| Pearson Residencial | r = 0,595 | < 0,001 | **Significativa** |
| **$r_{mín}$ detectable** (n = 300) | 0,161 | — | El *r* global queda **por debajo** del umbral |

Todos los estadísticos coinciden **dígito a dígito** entre Python y R, incluidos los tamaños de efecto, la potencia y Games-Howell —que no existen en `scipy`/`statsmodels` ni en R base y se implementaron de cero en cada entorno, lo que hace la verificación más exigente que comparar dos bibliotecas del mismo algoritmo. La única discrepancia esperada es Levene vs. Bartlett, por tratarse de pruebas distintas que aquí conducen a la misma decisión.

---

## 🖼️ Galería de Figuras

Las 13 figuras del informe, en el orden en que aparecen citadas en el texto.

### Sección III · Resultados (Figuras 1–6, Python)

| | |
|---|---|
| ![Figura 1](assets/images/figures/python/hypothesis/histograma_normalidad.png) | ![Figura 3](assets/images/figures/python/hypothesis/boxplot_sectores.png) |
| **Figura 1 · Normalidad (Matplotlib)** — histograma del sector Residencial con la densidad normal teórica superpuesta | **Figura 3 · Violín y caja por sector (seaborn)** — distribución del consumo por sector, con el ANOVA y su η² rotulados |
| ![Figura 4](assets/images/figures/python/hypothesis/medias_ic95.png) | ![Figura 6](assets/images/figures/python/hypothesis/regresion_temperatura.png) |
| **Figura 4 · Medias con IC del 95 % (Matplotlib)** — las letras (a), (b) y (c) codifican Tukey: letras distintas significan diferencia significativa | **Figura 6 · Regresión agregada (seaborn)** — temperatura vs. consumo con la recta OLS, su banda de confianza y el contraste de Pearson |

<div align="center">
    <img src="assets/images/figures/python/hypothesis/qqplots_normalidad.png" width="900" alt="Q-Q plots por sector">
</div>

**Figura 2 · Q-Q plots por sector (Matplotlib)** — diagnóstico gráfico de normalidad en los tres sectores, cada panel rotula el estadístico *W* de Shapiro-Wilk y su valor *p*.

<div align="center">
    <img src="assets/images/figures/python/hypothesis/tukey_forest.png" width="820" alt="Forest plot de Tukey frente a Games-Howell">
</div>

**Figura 5 · Tukey HSD frente a Games-Howell (Matplotlib)** — intervalos de confianza del 95 % de ambos post-hoc; las diferencias puntuales son idénticas, cambia la precisión.

### Sección IV · El papel de la visualización (Figuras 7–9, Python)

<div align="center">
    <img src="assets/images/figures/python/hypothesis/dispersion_sectores.png" width="820" alt="Consumo vs temperatura por sector">
</div>

**Figura 7 · Consumo vs. temperatura por sector (Plotly)** — versión estática de la figura interactiva; tres rectas de regresión paralelas y de pendiente positiva, separadas por el nivel de cada sector.

<div align="center">
    <img src="assets/images/figures/python/hypothesis/atenuacion.png" width="900" alt="Descomposición de la atenuación por agregación">
</div>

**Figura 8 · Descomposición de la atenuación (seaborn)** — los tres paneles descomponen la identidad *r = b₁·s_T/s_Y*: la pendiente global se mantiene cerca del valor de diseño, la desviación del consumo se multiplica por casi ocho al mezclar sectores y la correlación se desploma en la misma proporción.

<div align="center">
    <img src="assets/images/figures/python/hypothesis/dashboard.png" width="900" alt="Dashboard de cuatro paneles en Plotly">
</div>

**Figura 9 · Dashboard del protocolo de contraste (Plotly)** — versión estática del tablero interactivo que reúne las cuatro decisiones del protocolo en una sola vista.

### Verificación cruzada · Réplicas en ggplot2 (Figuras 10–13, R)

| | |
|---|---|
| ![Figura 10](assets/images/figures/r/hypothesis/histograma_normalidad.png) | ![Figura 11](assets/images/figures/r/hypothesis/medias_ic95.png) |
| **Figura 10 · Réplica en ggplot2** — verificación de normalidad del sector Residencial | **Figura 11 · Réplica en ggplot2** — consumo medio por sector con IC del 95 % y letras de Tukey |

<div align="center">
    <img src="assets/images/figures/r/hypothesis/tukey_forest.png" width="820" alt="Forest plot en ggplot2">
</div>

**Figura 12 · Réplica en ggplot2** — comparaciones múltiples de Tukey y Games-Howell.

<div align="center">
    <img src="assets/images/figures/r/hypothesis/dashboard.png" width="900" alt="Dashboard replicado en ggplot2">
</div>

**Figura 13 · Réplica en ggplot2 del tablero de la Figura 9** — compuesta en una retícula de cuatro paneles y exportada también como versión interactiva mediante `ggplotly`.

---

## 🛠️ Compilación

### Opción 1: `latexmk` (recomendado)

```bash
latexmk main.tex
```

No hacen falta banderas: [`.latexmkrc`](.latexmkrc) fija `$pdf_mode`, `$out_dir = 'build'` y `$bibtex_fudge = 0`.

> ℹ️ Ese último ajuste resuelve un fallo real. Por defecto latexmk invoca bibtex situándose **dentro** de `build/`, y entonces la ruta relativa que el `.aux` declara en `\bibdata{utils/references/references}` deja de resolver: aparece `I couldn't open database file` y la bibliografía sale vacía. Con `$bibtex_fudge = 0` bibtex corre desde la raíz del proyecto y encuentra el `.bib` sin tocar `BIBINPUTS`.

> ⚠️ No mezcles `pdflatex` suelto con `latexmk`: una invocación manual deja el `.fdb_latexmk` marcado con error y latexmk se niega a continuar (`gave an error in previous invocation`). Si ocurre, borra `build/` y vuelve a empezar.

### Opción 2: `pdflatex` manual

```bash
pdflatex -output-directory=build main.tex
bibtex build/main
pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex
```

### Paquetes del preámbulo

| Paquete | Para qué |
|---|---|
| `babel` (spanish) | Idioma, guionado y etiquetas |
| `amsmath`, `amssymb`, `amsfonts` | Las 6 ecuaciones de las pruebas |
| `graphicx` | Inclusión de las figuras |
| `array` | Columnas `p{}` con `\raggedright` en las Tablas I y II |
| `multirow` | Celdas combinadas en la tabla de la prueba t |
| `listings` + `xcolor` | Resaltado diferenciado de Python y R en los anexos |
| `float` | Especificador `[H]` para anclar las tablas |
| `cuted` + `capt-of` | Entorno `strip` — cargados de reserva |
| `tcolorbox` | Recuadros destacados — cargado de reserva |
| `eso-pic` + `transparent` | Marca de agua institucional |
| `hyperref` | Enlaces y anclas del PDF (**se carga de último**) |

---

## 🎨 Notas de Composición

### Reglas decorativas en los listados

Los comentarios de separación de los scripts originales miden 79 caracteres, y `listings` no puede partir una secuencia continua de guiones: cada una desbordaba la columna en **111 pt**. En los extractos de [`utils/codes/`](utils/codes/) esas reglas se acortaron a **52 caracteres**, el ancho real de una columna a `\scriptsize\ttfamily`. Es un ajuste puramente cosmético sobre comentarios; ninguna línea de código se modificó.

### Símbolo de porcentaje dentro de ecuaciones

`babel` con opción `spanish` redefine `\%` mediante `\es@sppercent`, que inspecciona `\lastskip`. En modo matemático el último *skip* es un `muskip` y se produce `Incompatible glue units`; la solución es envolverlo en `\text{\%}` (de `amsmath`). En modo texto corriente, `83,9\,\%` funciona sin problema.

### Figuras

La Figura 5 usa `figure*[!t]`, el flotante de doble columna de IEEE, porque es la única de proporción apaisada y a una sola columna resulta ilegible. Las cuatro restantes usan `figure[!htbp]`: no conviene anclarlas con `[H]`, ya que si no caben en lo que resta de columna desbordan la página en vez de moverse.

### Etiquetas en español

`babel` reasigna `\tablename` a *Cuadro* al iniciar el documento, así que un `\renewcommand` en el preámbulo no basta; la redefinición debe inyectarse dentro de `\captionsspanish`.

---

## 📋 Estado del Documento

El informe está **terminado**: compila en **14 páginas** —10 de cuerpo y 4 de anexos de código y referencias— sin desbordes de caja y sin referencias ni citas sin resolver.

- ✅ **13 figuras** referenciadas desde el texto (Matplotlib, seaborn, Plotly y ggplot2), cada una con su estadístico impreso
- ✅ **12 tablas** con las cifras reales de la ejecución
- ✅ **12 ecuaciones** numeradas y referenciadas
- ✅ **2 anexos** con el núcleo estadístico de ambos scripts, extraídos automáticamente del código real
- ✅ Bibliografía IEEE con **16 referencias**
- ✅ Compilación limpia: sin `Overfull`, sin `Underfull \hbox`/`\vbox` y sin referencias ni citas indefinidas

---

## 🔑 Palabras Clave

`Pruebas de Hipótesis` · `ANOVA` · `Tukey HSD` · `Prueba t de Welch` · `Correlación de Pearson` · `Agregación de Subpoblaciones` · `Paradoja de Simpson` · `Visualización Interactiva` · `SciPy` · `statsmodels` · `Plotly` · `ggplot2` · `LaTeX` · `IEEE`

---

## 🔗 Recursos

- [Proyecto hermano `hypothesis_visualizations` — scripts, dataset y figuras](../hypothesis_visualizations)
- [Documentación de SciPy](https://docs.scipy.org/doc/scipy/)
- [Documentación de statsmodels](https://www.statsmodels.org/stable/)
- [Documentación de Plotly](https://plotly.com/python/)
- [Documentación de ggplot2](https://ggplot2.tidyverse.org/)
- [Documentación LaTeX](https://www.latex-project.org/)
- [Paquete listings](https://www.ctan.org/pkg/listings)

---

## 📧 Contacto

**Andrés Giovanny Rubiano Muñoz**
Maestría en Inteligencia Artificial · Universidad de La Salle
arubiano67@unisalle.edu.co

---

## 📄 Derechos Reservados

© 2026 Andrés Giovanny Rubiano Muñoz (Andy Rubiano). Todos los derechos reservados.

Este trabajo académico y su contenido —investigación, código, metodologías y documentación— son propiedad intelectual conjunta de:

- **Andrés Giovanny Rubiano Muñoz** (Andy Rubiano) — Autor
- **Universidad de La Salle** — Institución académica

El uso, reproducción o distribución requiere autorización previa escrita de los titulares de derechos.

---

<div align="center">
  Universidad de La Salle | Bogotá D. C., Colombia
</div>
