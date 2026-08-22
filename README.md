<div align="center">
    <img src="assets/images/Logo.png" width="250" alt="Logo Universidad de La Salle">
</div>

# Introducción a la visualización de datos y principios de diseño de gráficos: aplicación sobre consumo energético con Matplotlib y R

## 📋 Información General

<div align="center">
    <img src="assets/images/author/Andy Rubiano.png" width="200" alt="Foto de Andrés Giovanny Rubiano Muñoz" style="border-radius: 10px;">
</div>

| Aspecto | Detalles |
|--------|----------|
| **Autor** | Andrés Giovanny Rubiano Muñoz "Andy Rubiano" |
| **Correo** | arubiano67@unisalle.edu.co |
| **Asignatura** | Ciencia de Datos |
| **Actividad** | Actividad 1 · Introducción a la visualización de datos y principios de diseño de gráficos |
| **Unidad** | Unidad 1 · Principios de visualización |
| **Programa** | Maestría en Inteligencia Artificial |
| **Universidad** | Universidad de La Salle |
| **Docente** | Fabián Camilo Castro Riveros |
| **Formato** | Artículo IEEE (`IEEEtran`, formato *conference*) |
| **Año** | 2026 |
| **Estado** | Completado |

---

## 🎯 Descripción del Proyecto

Este repositorio contiene el **informe en formato IEEE** de la Actividad 1 de Ciencia de Datos. El documento sustenta la importancia de la visualización dentro del análisis de datos y sistematiza los **principios de diseño de gráficos** que separan una representación fiel de una engañosa, tomando como base la jerarquía de precisión de los canales visuales de **Cleveland y McGill** y los criterios de integridad gráfica de **Tufte** y **Few**.

Los principios se aplican sobre un conjunto de datos simulado de **consumo energético mensual de 120 clientes** de una empresa distribuidora (sectores Residencial, Comercial e Industrial), con figuras construidas en **Matplotlib** y replicadas con la **graficación base de R** como verificación cruzada.

El laboratorio que genera los datos, los estadísticos y las figuras vive en el repositorio hermano [`graph_visualization`](../graph_visualization); aquí se reproducen sus imágenes y sus dos scripts completos como apéndices.

### Objetivos Principales

- Sustentar la importancia de la visualización de datos en la ciencia de datos y presentar sus conceptos fundamentales (codificación visual, jerarquía de canales y correspondencia entre tarea analítica y forma gráfica).
- Sistematizar los principios de diseño de gráficos y traducirlos en decisiones concretas de código verificables línea por línea.
- Comparar herramientas de visualización y justificar la elección de Matplotlib y de la graficación base de R.
- Contrastar un gráfico deliberadamente mal diseñado con su versión corregida sobre exactamente los mismos datos.
- Verificar de forma cruzada entre Python y R que los principios de diseño y sus violaciones son independientes de la herramienta.
- Entregar el informe escrito aplicando la normativa IEEE.

---

## 📚 Estructura del Repositorio

```
.
├── main.tex                          # Documento principal (preámbulo + \input de secciones y apéndices)
├── IEEEtran.cls                      # Clase LaTeX del formato IEEE conference
├── README.md                         # Este archivo
├── assets/
│   └── images/
│       ├── Logo.png                  # Logo institucional (marca de agua del documento)
│       ├── author/                   # Fotografía del autor
│       └── figures/                  # Figuras del informe (citadas con \includegraphics)
│           ├── python/
│           │   ├── good_design/      # Histograma, barras, caja, dispersión y barras horizontales
│           │   └── bad_design/       # Torta con errores deliberados de diseño
│           └── r/
│               ├── good_design/      # Réplicas en R: caja, dispersión y barras horizontales
│               └── bad_design/       # Réplica en R de la torta defectuosa
├── src/
│   ├── sections/                     # Secciones del informe (en orden de compilación)
│   │   ├── introduction/             # I. Introducción (importancia de la visualización, cuarteto de Anscombe)
│   │   ├── fundamentals/             # II. Conceptos fundamentales (codificación, canales, tarea vs. gráfico)
│   │   ├── design-principles/        # III. Principios de diseño de gráficos (Few y Tufte)
│   │   ├── tools-comparison/         # IV. Comparación de herramientas y elección de Matplotlib y R
│   │   ├── methodology/              # V. Metodología (dataset simulado, flujo de trabajo y reproducibilidad)
│   │   ├── results/                  # VI. Resultados (estadística descriptiva, figuras y análisis crítico)
│   │   └── conclusions/              # VII. Conclusiones
│   └── appendices/
│       ├── python-code/              # Apéndice A: script completo de Python
│       └── r-code/                   # Apéndice B: script completo de R
├── utils/
│   ├── codes/                        # Códigos citados vía \lstinputlisting
│   │   ├── python/visualizations.py  # Genera dataset, estadísticos y figuras (Matplotlib)
│   │   └── r/visualizations.R        # Réplica y verificación cruzada (graficación base de R)
│   └── references/
│       └── references.bib            # Bibliografía IEEE (10 referencias)
└── build/                            # Artefactos de compilación LaTeX (generado)
```

---

## 🧭 Contenido del Informe

### I · Introducción

La visualización codifica información en objetos visuales para aprovechar la percepción humana y detectar patrones que una tabla numérica no revela. El punto de partida es el **cuarteto de Anscombe**: cuatro conjuntos con idéntica media, varianza, correlación y recta de regresión, pero con estructuras radicalmente distintas que solo se hacen evidentes al graficarlos.

### II · Conceptos fundamentales

Toda visualización asigna valores de datos a atributos gráficos según el tipo de variable. La **jerarquía de precisión de los canales visuales** de Cleveland y McGill ordena esas codificaciones por el error que produce cada una:

1. Posición sobre una escala común → 2. Posición sobre escalas no alineadas → 3. Longitud → 4. Ángulo y pendiente → 5. Área → 6. Volumen, curvatura y saturación de color.

| Tarea analítica | Gráfico | Canal y justificación |
|---|---|---|
| Distribución de una variable | Histograma | Posición y longitud; revela asimetría y multimodalidad |
| Comparación entre categorías | Barras | Longitud sobre línea base común desde cero |
| Relación entre dos variables | Dispersión | Posición en dos escalas comunes |
| Dispersión y atípicos por grupo | Diagrama de caja | Posición; resume cinco estadísticos |
| Composición de un total | Barras horizontales ordenadas | Longitud; sustituye al ángulo de la torta |

### III · Principios de diseño

Integridad gráfica · razón dato-tinta · etiquetado completo · uso funcional del color · escala honesta · ordenamiento significativo · jerarquía visual.

### IV · Comparación de herramientas

Tres paradigmas con compromisos distintos: **imperativo** (Matplotlib, graficación base de R), **declarativo** (seaborn, ggplot2, Altair, Plotly, D3.js) y de **interfaz gráfica** (Tableau, Power BI). Se elige Matplotlib por su control fino sobre cada elemento y su integración con pandas y NumPy, y R como contraste para validar que los principios no dependen del lenguaje.

### V · Metodología

| Aspecto | Valor |
|---|---|
| Clientes simulados | 120 |
| Sectores | Residencial (0,50) · Comercial (0,30) · Industrial (0,20) |
| Variables | `cliente_id`, `sector`, `consumo_kwh`, `costo_miles_cop` |
| Generación | Distribuciones normales por sector + tarifa diferenciada con ruido del 4 % |
| Semilla | `np.random.default_rng(42)` |
| Verificación | R lee el mismo CSV y recalcula los estadísticos de forma independiente |

### VI · Resultados

**Estadística descriptiva del consumo mensual (kWh):**

| Sector | n | Media | Mediana | Desv. est. | Mín. | Máx. |
|---|---|---|---|---|---|---|
| Residencial | 62 | 248,3 | 240,6 | 61,1 | 121,2 | 424,8 |
| Comercial | 40 | 878,1 | 866,6 | 207,3 | 430,9 | 1.339,3 |
| Industrial | 18 | 2.654,0 | 2.666,8 | 686,9 | 1.674,0 | 3.777,1 |
| **Global** | 120 | 819,1 | 378,6 | 873,8 | 121,2 | 3.777,1 |

Hallazgos principales:

- La distribución global no es una población con atípicos, sino la **superposición de tres grupos** con escalas distintas (asimetría de 1,85; la media global duplica a la mediana).
- El consumo industrial promedio equivale a **10,7 veces** el residencial.
- La relación consumo–costo alcanza **r = 0,998** (R² = 0,997), pero la tarifa efectiva no es única (0,820 · 0,710 · 0,647 miles de COP/kWh), de modo que la recta global está dominada por los clientes industriales.
- El sector Industrial, con apenas el **15 % de los clientes**, concentra el **48,6 % del consumo total**.

**Análisis crítico — la torta defectuosa acumula siete violaciones:** título sin contexto, ausencia de etiquetas de datos, comparación por ángulo y área, colores saturados sin función, sombra y desplazamiento radial, ángulo de inicio arbitrario y leyenda desacoplada. La versión corregida conserva los datos y cambia únicamente la codificación: barras horizontales ordenadas, escala de 0 a 100 %, un solo color y porcentaje impreso junto a cada barra.

### VII · Conclusiones

La visualización es un componente del análisis y no una etapa posterior; la calidad del diseño resulta medible y no es una preferencia estética; y la verificación cruzada entre Python y R —medias sectoriales, participaciones y correlación de 0,998 coincidentes— descarta errores de implementación en ambos entornos.

---

## 🛠️ Compilación

El documento se compila con `pdflatex` + `bibtex` (MiKTeX o TeX Live). Desde la raíz del repositorio:

```bash
latexmk -pdf -bibtexfudge- -outdir=build main.tex
```

> ℹ️ La opción `-bibtexfudge-` evita que `latexmk` ejecute `bibtex` desde `build/`, para que la ruta relativa `utils/references/references.bib` se resuelva correctamente.

Alternativamente, en secuencia manual:

```bash
pdflatex -output-directory=build main.tex
bibtex build/main
pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex
```

El resultado queda en `build/main.pdf` (9 páginas).

> ℹ️ **Colocación de figuras y tablas.** Ambas quedan continuas a la narrativa, no flotando al inicio de página. Las tablas anchas usan el entorno `widetable` (definido sobre `strip` de `cuted`) para ocupar las dos columnas en el punto exacto del texto; las figuras usan `figure[H]` a una columna con sus paneles apilados, porque `[H]` pasa el bloque completo a la página siguiente cuando no cabe, mientras que un `strip` demasiado alto se partiría y dejaría el rótulo separado de sus gráficas.

### Paquetes requeridos

`IEEEtran` · `babel` (spanish) · `amsmath` · `graphicx` · `listings` · `xcolor` · `float` · `cuted` · `capt-of` · `tcolorbox` · `eso-pic` · `transparent` · `hyperref`

---

## 📖 Referencias

El informe cita 10 referencias en formato IEEE, entre ellas:

1. W. S. Cleveland y R. McGill, *Graphical perception: Theory, experimentation, and application to the development of graphical methods*, JASA, 1984.
2. S. Few, *Show Me the Numbers: Designing Tables and Graphs to Enlighten*, 2.ª ed., 2012.
5. E. R. Tufte, *The Visual Display of Quantitative Information*, 2.ª ed., 2001.
6. L. Wilkinson, *The Grammar of Graphics*, 2.ª ed., 2005.
8. J. D. Hunter, *Matplotlib: A 2D graphics environment*, CiSE, 2007.

La lista completa está en [`utils/references/references.bib`](utils/references/references.bib).

---

<div align="center">
    <strong>Universidad de La Salle · Maestría en Inteligencia Artificial · 2026</strong>
</div>
