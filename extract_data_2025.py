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

xl = pd.ExcelFile('data_2025.xlsx')
sheet_name = 'Cobertura por Grupo (%)'

data_out = {}

if sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet_name)
    # Based on inspection: Col 0: Name, Col 1: 12m, Col 2: 18m, Col 3: 6y
    for i in range(len(df)):
        row = df.iloc[i]
        muni_name = row.iloc[0]
        if pd.isna(muni_name) or str(muni_name).strip() == "" or "TOTAL" in str(muni_name).upper():
            continue
            
        norm_name = normalize_name(muni_name)
        
        def parse_cov(val):
            try:
                return float(str(val).replace('%', '').strip())
            except:
                return 0.0

        if norm_name not in data_out:
            data_out[norm_name] = {}
        
        data_out[norm_name]['1_ano'] = {
            'coverage': parse_cov(row.iloc[1]),
            'coverage_str': str(row.iloc[1]),
            'semaforo': 'Calculado',
            'original_name': str(muni_name).strip()
        }
        data_out[norm_name]['18_meses'] = {
            'coverage': parse_cov(row.iloc[2]),
            'coverage_str': str(row.iloc[2]),
            'semaforo': 'Calculado',
            'original_name': str(muni_name).strip()
        }
        data_out[norm_name]['6_anos'] = {
            'coverage': parse_cov(row.iloc[3]),
            'coverage_str': str(row.iloc[3]),
            'semaforo': 'Calculado',
            'original_name': str(muni_name).strip()
        }

with open('coverage_data_2025.json', 'w', encoding='utf-8') as f:
    json.dump(data_out, f, ensure_ascii=False, indent=2)

print(f"Extracted 2025 data for {len(data_out)} municipalities.")
