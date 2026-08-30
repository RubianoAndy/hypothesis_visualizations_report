# -----------------------------------------------------------------------------
# Sincroniza los extractos de codigo de los anexos con los scripts reales.
#
# Los anexos del informe no reproducen los scripts completos, sino los bloques
# que sustentan las cifras reportadas. Copiarlos a mano invita a que el informe
# y el codigo se separen sin que nadie lo note, asi que este script los extrae
# del proyecto hermano cada vez que se ejecuta: el listado del PDF es entonces
# codigo que corrio de verdad, no una transcripcion.
#
# Ejecucion (desde la raiz del informe):
#   python utils/codes/sync_appendix.py
# -----------------------------------------------------------------------------

import ast
import os
import sys

PROJECT = os.path.join("..", "hypothesis_visualizations", "utils", "codes")
PY_SOURCE = os.path.join(PROJECT, "hypothesis_testing.py")
R_SOURCE = os.path.join(PROJECT, "hypothesis_testing.R")
OUT_DIR = os.path.join("utils", "codes")

# Bloques que reproduce cada anexo, en el orden en que aparecen en el PDF
PY_CORE = ["run_normality_and_levene", "run_ttest", "run_anova_tukey",
           "run_correlation_regression"]
# Del bloque de robustez solo se listan las dos funciones que no delegan en una
# biblioteca: los tamanos de efecto aplican las ecuaciones del cuerpo del
# informe sin nada que anadir, mientras que estas dos se programaron de cero.
PY_EFFECTS = ["welch_anova", "games_howell"]
PY_FIGURE = ["plot_interactive_plotly"]

# En R no hay un arbol sintactico a mano, asi que cada bloque se delimita por
# la linea que lo abre y por la regla de comentario que abre el bloque
# siguiente.
RULE = "# ---------------------------------------------------------------------"
R_BLOCKS = [
    ("# --- 2.1 Normalidad", RULE),
    ("n1 <- length(residential)", RULE),
    ("welch <- oneway.test", RULE),
]


def extract_python(source, names):
    """Devuelve el texto original de las funciones pedidas, en ese orden."""
    text = open(source, encoding="utf-8").read()
    tree = ast.parse(text)
    found = {node.name: node for node in tree.body
             if isinstance(node, ast.FunctionDef)}
    missing = [name for name in names if name not in found]
    if missing:
        raise SystemExit(f"[ERROR] No estan en {source}: {', '.join(missing)}")

    lines = text.splitlines()
    blocks = []
    for name in names:
        node = found[name]
        # decorator_list vacio en todo el proyecto, asi que lineno es la cabecera
        blocks.append("\n".join(lines[node.lineno - 1:node.end_lineno]))
    return "\n\n\n".join(blocks) + "\n"


def extract_r(source, blocks):
    """Recorta el texto de R entre la cabecera de cada bloque y la siguiente."""
    lines = open(source, encoding="utf-8").read().splitlines()
    out = []
    for start_marker, end_marker in blocks:
        start = next((i for i, line in enumerate(lines)
                      if line.startswith(start_marker)), None)
        if start is None:
            raise SystemExit(f"[ERROR] No se encontro '{start_marker}' en {source}")
        end = next((i for i in range(start + 1, len(lines))
                    if lines[i].startswith(end_marker)), len(lines))
        out.append("\n".join(lines[start:end]).rstrip())
    return "\n\n\n".join(out) + "\n"


def write(path, content):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    print(f"[OK] {path} ({len(content.splitlines())} lineas)")


def main():
    for source in (PY_SOURCE, R_SOURCE):
        if not os.path.exists(source):
            raise SystemExit(
                f"[ERROR] No se encontro '{source}'. Ejecuta este script desde la "
                "raiz del informe, con el proyecto hermano en el directorio padre."
            )

    write(os.path.join(OUT_DIR, "hypothesis_testing_core.py"),
          extract_python(PY_SOURCE, PY_CORE))
    write(os.path.join(OUT_DIR, "effect_and_robust.py"),
          extract_python(PY_SOURCE, PY_EFFECTS))
    write(os.path.join(OUT_DIR, "plotly_figure.py"),
          extract_python(PY_SOURCE, PY_FIGURE))
    write(os.path.join(OUT_DIR, "hypothesis_testing_core.R"),
          extract_r(R_SOURCE, R_BLOCKS))
    print("\nAnexos sincronizados. Recompila el informe con: latexmk main.tex")


if __name__ == "__main__":
    sys.exit(main())
