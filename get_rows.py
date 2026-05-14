import pandas as pd
import json

xl = pd.ExcelFile('data.xlsx')
sheets = ['1 Año', '18 Meses', 'Rezag 2-12 Años']
row_data = {}

for s in sheets:
    if s in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=s, nrows=10)
        # Convert everything to string to avoid JSON serialization errors with NaN
        row_data[s] = df.astype(str).values.tolist()

with open('rows.json', 'w', encoding='utf-8') as f:
    json.dump(row_data, f, ensure_ascii=False, indent=2)
