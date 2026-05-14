import pandas as pd
import json

xl = pd.ExcelFile('data.xlsx')
sheets = ['1 Año', '18 Meses', '6 Años', 'Rezag 2-12 Años']
col_data = {}

for s in sheets:
    if s in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=s)
        col_data[s] = df.columns.tolist()

with open('cols.json', 'w', encoding='utf-8') as f:
    json.dump(col_data, f, ensure_ascii=False, indent=2)
