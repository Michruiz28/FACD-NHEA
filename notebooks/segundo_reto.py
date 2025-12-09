
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "NHE2023.xlsx")
OUT_DIR = os.path.join(ROOT, "outputs", "segundo_reto")
os.makedirs(OUT_DIR, exist_ok=True)

def find_year_columns(df):
    for r in range(1, 5):
        row = df.iloc[r, 1:]
        nums = pd.to_numeric(row, errors="coerce")
        if ((nums >= 1900) & (nums <= 2100)).sum() > 10:
            year_cols = nums[(nums >= 1900) & (nums <= 2100)].index.tolist()
            years = nums.loc[year_cols].astype(int).tolist()
            return year_cols, years
    return list(range(1, 65)), list(range(1960, 1960+64))

def main():
    df_raw = pd.read_excel(DATA_PATH, sheet_name="NHE23", header=None)

    year_cols, years = find_year_columns(df_raw)

    row_mask = df_raw.iloc[:,0].astype(str).str.contains("workers", case=False, na=False)
    df_workers = df_raw.loc[row_mask, [0] + year_cols].copy()

    df_workers.columns = ["category"] + years
    for col in years:
        df_workers[col] = pd.to_numeric(df_workers[col], errors="coerce")
    df_workers.to_csv(os.path.join(OUT_DIR, "workers_compensation_raw.csv"), index=False)
    missing_counts = df_workers.isna().sum()
    missing_pct = (df_workers.isna().sum() / len(df_workers) * 100).round(2)
    quality_report = pd.DataFrame({
        "missing_count": missing_counts,
        "missing_pct": missing_pct
    })
    quality_report.to_csv(os.path.join(OUT_DIR, "quality_report.csv"))
    vars_sorted = quality_report.loc[years].sort_values("missing_count", ascending=False)
    vars_sorted.to_csv(os.path.join(OUT_DIR, "missing_sorted.csv"))
    summary_with_na = df_workers.describe(include="all").T
    summary_with_na.to_csv(os.path.join(OUT_DIR, "summary_with_na.csv"))

    summary_no_na = df_workers.dropna().describe(include="all").T
    summary_no_na.to_csv(os.path.join(OUT_DIR, "summary_no_na.csv"))
    for _, row in df_workers.iterrows():
        category = row["category"]
        serie = row[years]

        plt.figure(figsize=(9,4))
        plt.plot(years, serie.values, color="#ff69b4")
        plt.title(f"{category} (Workers' Comp)")
        plt.xlabel("Año")
        plt.ylabel("Valor (millones)")
        plt.grid(True)
        plt.tight_layout()

        fname = category.replace(" ", "_").replace("/", "_")
        plt.savefig(os.path.join(OUT_DIR, f"{fname}.png"), dpi=140)
        plt.close()

    print("Segundo reto completado. Archivos generados en:", OUT_DIR)

if __name__ == "__main__":
    main()
