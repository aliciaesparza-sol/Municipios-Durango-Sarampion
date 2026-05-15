import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv')
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()

# Ensure numeric
cols = ['SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL', 'SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL']
for col in cols:
    mez[col] = pd.to_numeric(mez[col], errors='coerce').fillna(0)

print("Full Breakdown for Mezquital:")
summary = mez.groupby(['Temporada', 'INSTITUCION'])[cols].sum()
summary['Total SRP'] = summary['SRP  PRIMERA TOTAL'] + summary['SRP SEGUNDA TOTAL']
summary['Total SR'] = summary['SR PRIMERA TOTAL'] + summary['SR SEGUNDA TOTAL']
summary['GRAN TOTAL'] = summary['Total SRP'] + summary['Total SR']
print(summary)

print("\nGrand Total from Summary:")
print(summary['Row Total'].sum())

# Check for rows with NaN Temporada or Institution
nan_rows = mez[mez['Temporada'].isna() | mez['INSTITUCION'].isna()]
print("\nRows with missing Season or Institution:")
print(nan_rows)
