import pandas as pd
from datetime import datetime

# 1. Load Source Data (Tierras Coloradas)
src_path = 'src_temp.xlsx'
src_df = pd.read_excel(src_path, sheet_name='Concentrado')
row = src_df[src_df.iloc[:, 2] == 'TIERRAS COLORADAS'].iloc[0]

# Extract data (based on previous mapping)
data_to_add = {
    'Localidad': 'TIERRAS COLORADAS',
    'Fecha(s) de Atención': '2026-04-29', # Original: 2026-04-29
    '6 a 11 meses': int(row.iloc[43]),
    '1 año': int(row.iloc[44]),
    '2 a 4 años': int(row.iloc[45]),
    '5 a 9 años': int(row.iloc[46]),
    '10 a 19 años': int(row.iloc[47]),
    '20 a 39 años': int(row.iloc[48]),
    '40 a 49 años': int(row.iloc[49]),
    'TOTAL': int(row.iloc[50]),
    'POBLACION (INEGI)': int(row.iloc[23]), # "Total de población encontrada" (416)
}
data_to_add['COBERTURA (%)'] = data_to_add['TOTAL'] / data_to_add['POBLACION (INEGI)'] if data_to_add['POBLACION (INEGI)'] > 0 else 0

# 2. Load Destination Data
dst_path = 'dst_temp.xlsx'
dst_df = pd.read_excel(dst_path, sheet_name='Desglose')

# 3. Append the new row
# Convert to DataFrame and concat
new_row_df = pd.DataFrame([data_to_add])
final_df = pd.concat([dst_df, new_row_df], ignore_index=True)

# 4. Save to a new file
output_path = 'Dosis_por_Localidad_Mezquital_Actualizado.xlsx'
final_df.to_excel(output_path, index=False)

print(f"Integration complete. New row added for Tierras Coloradas.")
print(f"Values: SRP1(6-11m): {data_to_add['6 a 11 meses']}, TOTAL: {data_to_add['TOTAL']}, Goal: {data_to_add['POBLACION (INEGI)']}")
