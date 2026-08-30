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
        category_orders={"sector": SECTOR_ORDER},
        color_discrete_map=SECTOR_COLORS,
        hover_data=["id_cliente", "region"],  # info que aparece al pasar el mouse
        trendline="ols",  # recta de regresion por sector (usa statsmodels)
        labels={"temperatura_c": "Temperatura promedio (°C)",
                "consumo_kwh": "Consumo (kWh/mes)", "sector": "Sector"},
    )
    fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color="white")))
    fig.update_layout(template="plotly_white", legend_title_text="Sector",
                      title_font_size=15)
    fig.write_html(f"{FIGURES_DIR}/fig5_interactivo_plotly.html")

    try:
        fig.write_image(f"{FIGURES_DIR}/fig5_interactivo_plotly.png", width=900, height=550, scale=2)
    except Exception:
        print("[AVISO] No se pudo exportar el PNG de Plotly (falta Chrome).")
        print("        Ejecute 'plotly_get_chrome' o tome una captura del HTML.")
