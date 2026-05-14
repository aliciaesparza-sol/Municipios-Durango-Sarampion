import pandas as pd
import json

xl = pd.ExcelFile('data_2025.xlsx')
row_data = {}

if "Cobertura por Grupo (%)" in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name="Cobertura por Grupo (%)", nrows=20)
    # Filter out columns that are completely NaN in these 20 rows to make it readable
    df = df.dropna(axis=1, how='all')
    row_data["Cobertura por Grupo (%)"] = df.astype(str).values.tolist()

with open('rows_2025_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(row_data, f, ensure_ascii=False, indent=2)
