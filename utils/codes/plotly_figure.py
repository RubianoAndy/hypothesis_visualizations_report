def plot_interactive_plotly(df):
    """Figura 5 (Plotly): grafico INTERACTIVO de dispersion por sector.

    Se guarda en HTML (interactivo, se abre en el navegador) y en PNG
    (version estatica para insertar en el informe PDF).
    """
    fig = px.scatter(
        df,
        x="temperatura_c",
        y="consumo_kwh",
        color="sector",
        hover_data=["id_cliente", "region"],  # info que aparece al pasar el mouse
        trendline="ols",  # recta de regresion por sector (usa statsmodels)
        title="Figura 5. Consumo vs temperatura por sector (interactivo - Plotly)",
        labels={"temperatura_c": "Temperatura promedio (°C)", "consumo_kwh": "Consumo (kWh/mes)"},
    )
    fig.write_html(f"{FIGURES_DIR}/fig5_interactivo_plotly.html")

    # El PNG estatico requiere Chrome instalado (lo usa kaleido).
    # Si no esta disponible, el HTML interactivo igual queda generado.
    try:
        fig.write_image(f"{FIGURES_DIR}/fig5_interactivo_plotly.png", width=900, height=550, scale=2)
    except Exception:
