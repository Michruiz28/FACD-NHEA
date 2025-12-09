# notebooks/primer_reto.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "NHE2023.xlsx")
OUT_DIR = os.path.join(ROOT, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def find_row_with_label(df, label_snippet):
    """Busca la primera fila cuya primera columna contiene label_snippet (case-insensitive)."""
    col0 = df.iloc[:, 0].astype(str).str.strip().str.lower()
    matches = col0[col0.str.contains(label_snippet.lower(), na=False)]
    if not matches.empty:
        return matches.index[0]
    return None

def find_year_columns(df):
    """Detecta columnas que contienen años (fila donde hay números 1960..2023). 
       Retorna lista de índices de columnas y la fila donde están los años."""
    for r in range(min(8, len(df))): 
        row = df.iloc[r, 1:] 
        try:
            nums = pd.to_numeric(row, errors='coerce')
            count_years = ((nums >= 1900) & (nums <= 2100)).sum()
            if count_years >= 10:   # heurística: al menos 10 valores plausibles de año
                year_cols = nums[(nums >= 1900) & (nums <= 2100)].index.tolist()
                years = nums.loc[year_cols].astype(int).tolist()
                return year_cols, r, years
        except Exception:
            continue
    # fallback: asumir columnas 1..64 (1960-2023)
    return list(range(1, 65)), 1, list(range(1960, 1960 + 64))

def main():
    df_raw = pd.read_excel(DATA_PATH, sheet_name="NHE23", header=None)
    year_cols, year_row_idx, year_values = find_year_columns(df_raw)
    print(f"Fila detectada con años: {year_row_idx}; columnas años: {year_cols[:5]}... (total {len(year_cols)})")
    target_label = "Total National Health Expenditures"
    total_row_idx = find_row_with_label(df_raw, target_label)
    if total_row_idx is None:
        raise ValueError(f"No se encontró la fila con la etiqueta '{target_label}' en la primera columna.")
    print(f"Fila detectada para '{target_label}': {total_row_idx}")

    # extraer valores
    values = df_raw.loc[total_row_idx, year_cols]
    # convertir a numérico (puede contener NaN/strings)
    values = pd.to_numeric(values, errors="coerce").reset_index(drop=True)
    # create pandas Series with explicit years from year_values
    years = pd.Index(year_values, name="year")
    ts = pd.Series(values.values, index=years, name="Total NHE")
    ts = ts.dropna()  # eliminar años sin datos
    csv_path = os.path.join(OUT_DIR, "time_series_total_nhe_by_year.csv")
    ts.to_csv(csv_path, header=True)
    print(f"Guardado CSV: {csv_path}")

    print("\nResumen:")
    print(ts.describe())
    plt.figure(figsize=(10,5))
    plt.plot(ts.index.astype(int), ts.values,color="#ff69b4")
    plt.title("Total National Health Expenditures (1960–2023)")
    plt.xlabel("Año")
    plt.ylabel("Gasto total (millones)")
    plt.grid(True)
    plt.tight_layout()
    png_path = os.path.join(OUT_DIR, "total_nhe_trend.png")
    plt.savefig(png_path, dpi=160)
    plt.close()
    print(f"Guardado PNG: {png_path}")

    # graf interactivo Plotly
    fig = px.line(x=ts.index.astype(int), y=ts.values,
                  labels={"x":"Año", "y":"Total NHE (millones)"},
                  title="Total NHE (1960-2023) - Interactivo")
    fig.update_traces(line_color="#ff69b4")
    html_path = os.path.join(OUT_DIR, "total_nhe_trend.html")
    fig.write_html(html_path)
    print(f"Guardado HTML interactivo: {html_path}")

if __name__ == "__main__":
    main()
