import pandas as pd
import json
import unicodedata

def normalize_name(name):
    if pd.isna(name): return ""
    name = str(name).strip().upper()
    # Remove accents
    name = ''.join(c for c in unicodedata.normalize('NFD', name)
                  if unicodedata.category(c) != 'Mn')
    return name

xl = pd.ExcelFile('data.xlsx')
sheets = {
    '1 Año': '1_ano',
    '18 Meses': '18_meses',
    'Rezag 2-12 Años': '6_anos'
}

data_out = {}

for sheet_name, key in sheets.items():
    if sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name)
        # Data starts at index 2 in df (row 4 in Excel)
        # The columns might be unnamed, so we access by position
        for i in range(2, len(df)):
            row = df.iloc[i]
            muni_name = row.iloc[1]
            if pd.isna(muni_name) or str(muni_name).strip() == "":
                continue
            if str(muni_name).startswith('Jurisdicc') or str(muni_name).startswith('Total') or str(muni_name).startswith('% Meta'):
                continue
                
            norm_name = normalize_name(muni_name)
            cov_str = str(row.iloc[9])
            semaforo = str(row.iloc[10])
            
            # Clean coverage string
            try:
                cov_val = float(cov_str.replace('%', '').strip())
            except:
                cov_val = 0.0

            if norm_name not in data_out:
                data_out[norm_name] = {}
            
            data_out[norm_name][key] = {
                'coverage': cov_val,
                'coverage_str': cov_str,
                'semaforo': semaforo,
                'original_name': str(muni_name).strip()
            }

with open('coverage_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_out, f, ensure_ascii=False, indent=2)

print(f"Extracted data for {len(data_out)} municipalities.")
