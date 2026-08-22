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
| **Extensión** | 9 páginas, incluidos anexos y referencias |
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
- Representar cada resultado con su visualización, incluyendo una figura interactiva construida con Plotly.
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
│           ├── python/               # 5 figuras (Matplotlib, seaborn y Plotly)
│           └── r/                    # 2 réplicas en ggplot2 citadas desde el informe
├── src/
│   ├── sections/                     # Secciones del informe (en orden de compilación)
│   │   ├── introduction/             # I. Introducción
│   │   ├── methodology/              # II. Metodología
│   │   ├── results/                  # III. Resultados
│   │   ├── discussion/               # IV. El papel de la visualización
│   │   └── conclusions/              # V. Conclusiones y recomendaciones
│   └── appendices/
│       ├── python-code/              # Anexo A: núcleo estadístico en Python
│       └── r-code/                   # Anexo B: núcleo estadístico en R
├── utils/
│   ├── codes/                        # Extractos citados vía \lstinputlisting
│   │   ├── hypothesis_testing_core.py         # Las cinco pruebas con SciPy y statsmodels
│   │   ├── plotly_figure.py                   # Construcción de la figura interactiva
│   │   └── hypothesis_testing_core.R          # Recálculo independiente en R base
│   └── references/
│       └── references.bib            # Bibliografía IEEE (18 referencias)
└── build/                            # Artefactos de compilación LaTeX (generado)
```

> ℹ️ Los anexos reproducen el **núcleo estadístico** de cada script, no su totalidad: la actividad limita el informe a 10 páginas incluyendo anexos, y el código de generación del dataset y de las figuras 1 a 4 excede ese margen. Los scripts completos están en [`hypothesis_visualizations`](../hypothesis_visualizations).

---

## 🧭 Contenido del Informe

| # | Sección | Contenido |
|---|---|---|
| — | Resumen | Las cifras principales y el hallazgo central |
| I | Introducción | Qué mide y qué no mide un valor *p*; el cuarteto de Anscombe y la agregación de subpoblaciones como marco |
| II | Metodología | Conjunto de datos (**Tabla I**), diseño del contraste (**Tabla II**) y las **6 ecuaciones** de las pruebas |
| III | Resultados | Supuestos, prueba t, ANOVA + Tukey y regresión — **Tablas III–VII** y **Figuras 1–4** |
| IV | El papel de la visualización | La figura interactiva (**Figura 5**), la identidad *r = b₁·s_T/s_Y*, la verificación cruzada con sus réplicas en ggplot2 (**Figura 6**) y las limitaciones |
| V | Conclusiones | Seis conclusiones y tres recomendaciones para la toma de decisiones |
| A | Anexo · Python | Las cinco pruebas con SciPy y statsmodels + la figura de Plotly |
| B | Anexo · R | El recálculo independiente con `shapiro.test`, `t.test`, `aov`, `TukeyHSD`, `cor.test` y `lm` |
| — | Referencias | 18 entradas en formato IEEE |

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
| Pearson global | r = 0,063 | 0,277 | **No significativa** |
| Pearson Residencial | r = 0,595 | < 0,001 | **Significativa** |

Todos los estadísticos coinciden **dígito a dígito** entre Python y R. La única discrepancia esperada es Levene vs. Bartlett, por tratarse de pruebas distintas que aquí conducen a la misma decisión.

---

## 🛠️ Compilación

### Opción 1: `latexmk` (recomendado)

```bash
latexmk -pdf -outdir=build main.tex
```

> ⚠️ BibTeX se ejecuta con el directorio de trabajo en `build/`, así que la ruta relativa `utils/references/references.bib` no se resuelve sola. Si aparece `I couldn't open database file`, exporta `BIBINPUTS` apuntando a la raíz del proyecto:
>
> ```bash
> BIBINPUTS=".:..:$PWD:" latexmk -pdf -outdir=build main.tex
> ```

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

El informe está **terminado**: compila en **9 páginas** —dentro del límite de 5 a 10 que fija la actividad— sin desbordes de caja y sin referencias ni citas sin resolver.

- ✅ **6 figuras** referenciadas desde el texto (Matplotlib, seaborn, Plotly y ggplot2)
- ✅ **9 tablas** con las cifras reales de la ejecución
- ✅ **7 ecuaciones** numeradas y referenciadas
- ✅ **2 anexos** con el núcleo estadístico de ambos scripts
- ✅ Bibliografía IEEE con **18 referencias**
- ✅ Compilación sin `Overfull` ni `Underfull \hbox`/`\vbox`

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
