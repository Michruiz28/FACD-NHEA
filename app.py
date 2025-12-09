import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURACIÓN DEL DASHBOARD
st.set_page_config(
    page_title="Análisis NHEA 1960–2023",
    layout="wide"
)

st.title("Análisis – National Health Expenditures (1960–2023)")
st.write("Michelle Dayana Ruiz Carranza - FACD")

# NAVEGACIÓN ENTRE SECCIONES

tabs = st.tabs(["Inicio", "Primer Reto", "Segundo Reto"])

# TAB 0 – DESCRIPCIÓN GENERAL
with tabs[0]:

    st.subheader("Descripción General")
    st.markdown("""
Analizamos el dataset NHE2023 del Grupo Nacional de Estadísticas de Salud de los Centers for Medicare & Medicaid Services (CMS).
Los datos provienen de las Cuentas Nacionales de Salud de Estados Unidos y contienen información histórica del gasto nacional en salud desde 1960 hasta 2023.

Fuente oficial del dataset:  
https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/NationalHealthExpendData/NationalHealthAccountsHistorical

Incluye:

- Tendencia del gasto total en salud (Primer Reto).
- Análisis de calidad y consistencia del subconjunto Workers' Compensation (Segundo Reto).
    """)
# TAB 1 – PRIMER RETO
with tabs[1]:

    st.header("Primer Reto: Total National Health Expenditures (1960–2023)")

    # Cargar datos
    df = pd.read_csv("outputs/time_series_total_nhe_by_year.csv")

    # Gráfica principal
    st.subheader("Serie histórica del gasto total")
    fig = px.line(
        df,
        x="year",
        y="Total NHE",
        title="Total National Health Expenditures (1960–2023)",
        labels={"year": "Año", "Total NHE": "Gasto Total (millones USD)"}
    )
    fig.update_traces(line_color="#ff69b4", line_width=3)
    st.plotly_chart(fig, use_container_width=True)

    # Cálculos
    df["pct_change"] = df["Total NHE"].pct_change() * 100
    df["diff"] = df["Total NHE"].diff()

    st.subheader("Análisis Estadístico del Primer Reto")

    # Resumen estadístico general
    st.markdown("### 1. Resumen estadístico general del gasto total")
    st.write(df["Total NHE"].describe())

    st.markdown("""
El gasto presenta una tendencia creciente con alta variabilidad.
La desviación estándar es elevada debido a que el gasto se incrementa sustancialmente
a lo largo de seis décadas. Esto es característico de series con crecimiento estructural.
    """)

    # Variación absoluta por década
    st.markdown("### 2. Variación absoluta interanual (muestra completa)")
    st.dataframe(df[["year", "diff"]])

    st.markdown("""
La variación absoluta muestra incrementos anuales consistentes.
Se observan tres patrones:

- Entre 1960 y 1980 los aumentos son moderados.
- Entre 1980 y 2000 los incrementos anuales crecen de forma acelerada.
- Desde 2000 los aumentos anuales superan ampliamente los valores observados en décadas previas.

Este comportamiento confirma que el gasto en salud no solo crece, sino que lo hace a un ritmo cada vez mayor.
    """)

    # Variación porcentual anual
    st.markdown("### 3. Variación porcentual anual")
    st.dataframe(df[["year", "pct_change"]])

    st.markdown("""
La tasa de crecimiento porcentual presenta un patrón relativamente estable entre 1960 y el año 2000,
con variaciones generalmente entre 6 % y 12 % por año.

Se identifican incrementos más altos en la década de 2020, particularmente en los años asociados
a los efectos de la pandemia. Estos valores reflejan presiones excepcionales sobre el sistema
de salud, incluyendo aumento en servicios, infraestructura, tratamientos y costos operativos.
    """)

    # Interpretación estructurada
    st.markdown("### Interpretación del Primer Reto")
    st.markdown("""
El análisis estadístico indica que el gasto nacional en salud de Estados Unidos ha crecido
de forma sostenida desde 1960 hasta 2023, pasando de aproximadamente 27 mil millones a más
de 4.8 billones de dólares. Esto representa un incremento superior a 175 veces en un periodo
de 63 años.

La variación absoluta y porcentual confirman un patrón de crecimiento estructural:
las tasas porcentuales se mantienen relativamente estables durante varias décadas,
pero la variación absoluta aumenta fuertemente con el tiempo, lo cual refleja el tamaño
cada vez mayor del sistema de salud.

En las décadas recientes el gasto muestra incrementos amplios, y en los años post-2020
se observa un crecimiento particularmente fuerte que podemos asumir que esta asociado al impacto de la pandemia.
Con base en estos indicadores, se concluye que la serie presenta una tendencia creciente
de largo plazo, con aceleración del crecimiento en periodos recientes.
    """)
# TAB 2 – SEGUNDO RETO
with tabs[2]:

    st.header("Segundo Reto: Calidad del subdataset Workers' Compensation")

    st.subheader("Valores faltantes por año")
    df_missing = pd.read_csv("outputs/segundo_reto/missing_sorted.csv")
    st.dataframe(df_missing)

    st.subheader("Reporte de calidad")
    df_quality = pd.read_csv("outputs/segundo_reto/quality_report.csv")
    st.dataframe(df_quality)

    st.subheader("Resumen estadístico (sin NA)")
    df_summary = pd.read_csv("outputs/segundo_reto/summary_no_na.csv", index_col=0)

    # Mostrar tabla
    st.dataframe(df_summary)
    df_clean = df_summary.drop(index="category", errors="ignore")
    df_ts = df_clean[["mean"]].reset_index()
    df_ts.columns = ["year", "value"]
    df_ts["year"] = df_ts["year"].astype(int)
    df_ts["value"] = df_ts["value"].astype(float)
    # Gráfico de la serie temporal
    st.subheader("Serie histórica de Workers' Compensation (media anual)")

    fig2 = px.line(
        df_ts,
        x="year",
        y="value",
        title="Workers' Compensation – Tendencia histórica (1960–2023)",
        labels={"year": "Año", "value": "Valor promedio (USD)"},
    )

    fig2.update_traces(line_color="#ff69b4", line_width=3)

    st.plotly_chart(fig2, use_container_width=True)
    # Interpretación

    st.markdown("### Interpretación del Segundo Reto")

    st.markdown("""
El análisis del subdataset *Workers' Compensation* muestra una serie completa, sin valores faltantes
y con estructura consistente entre 1960 y 2023. Los indicadores estadísticos confirman que la información
es confiable para realizar análisis longitudinales. A partir de la gráfica generada, se identifican varios
patrones relevantes en la evolución histórica del gasto:

### 1. Crecimiento general de largo plazo
El gasto aumenta desde menos de 200 millones en 1960 hasta superar los 16 000 millones en 2023,
lo cual representa un incremento de más de 80 veces. Este comportamiento refleja el aumento progresivo
de los costos médicos, la evolución de los sistemas de compensación laboral y el crecimiento del mercado
asegurador.

### 2. Evolución por periodos

**2.1. 1960–1975: Crecimiento lento y estable**  
Los valores se mantienen por debajo de 1 000 millones. Los incrementos son pequeños y reflejan
una etapa inicial de desarrollo del sistema de compensación laboral en Estados Unidos.

**2.2. 1975–1995: Aceleración moderada**  
Se observa un crecimiento más pronunciado. Cambios regulatorios y la expansión del aseguramiento estatal
explican estos incrementos. El gasto pasa de valores cercanos a 1 000 millones a más de 4 500 millones.

**2.3. 1995–2008: Crecimiento acelerado**  
Es el periodo de mayor expansión. El gasto aumenta de aproximadamente 4 000 millones
a más de 14 000 millones. Factores clave:
- Incremento de costos médicos.  
- Cambios demográficos en la fuerza laboral.  
- Nuevos estándares de compensación y cobertura.

**2.4. 2008–2010: Caída significativa**  
La Gran Recesión provoca una reducción súbita en el gasto. La disminución del empleo industrial,
junto con recortes en beneficios, explica esta caída.

**2.5. 2010–2017: Recuperación y máximos históricos**  
El gasto vuelve a crecer, alcanzando valores entre 15 000 y 16 000 millones.
Este periodo marca el punto más alto de la serie.

**2.6. 2020: Descenso atribuible a la pandemia**  
Se observa una caída asociada a:
- Menor actividad económica.  
- Reducción de la siniestralidad laboral.  
- Cierres temporales de empresas.  

**2.7. 2021–2023: Recuperación posterior**  
La tendencia vuelve a ser creciente y el gasto alcanza niveles similares a los máximos previos.
La reactivación económica impulsa este repunte.

### 3. Conclusión general
El comportamiento del gasto en *Workers’ Compensation* muestra una tendencia creciente sostenida,
con fluctuaciones coherentes con eventos económicos de gran escala. El dataset es consistente,
completo y adecuado para análisis estadísticos y comparativos dentro del contexto de las Cuentas
Nacionales de Salud.
    """)
