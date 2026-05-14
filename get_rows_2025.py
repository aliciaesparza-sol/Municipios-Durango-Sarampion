import pandas as pd
import json

xl = pd.ExcelFile('data_2025.xlsx')
row_data = {'sheets': xl.sheet_names}

for s in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=s, nrows=10)
    row_data[s] = df.astype(str).values.tolist()

with open('rows_2025.json', 'w', encoding='utf-8') as f:
    json.dump(row_data, f, ensure_ascii=False, indent=2)
