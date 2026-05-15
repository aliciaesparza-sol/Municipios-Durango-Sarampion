import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv')
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()

# Ensure numeric
cols = ['SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL', 'SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL']
for col in cols:
    mez[col] = pd.to_numeric(mez[col], errors='coerce').fillna(0)

print("CSV Totals for Mezquital (All Seasons):")
print(f"SRP 1ras: {mez['SRP  PRIMERA TOTAL'].sum()}")
print(f"SRP 2das: {mez['SRP SEGUNDA TOTAL'].sum()}")
print(f"SR 1ras: {mez['SR PRIMERA TOTAL'].sum()}")
print(f"SR 2das: {mez['SR SEGUNDA TOTAL'].sum()}")
print(f"Grand Total: {mez[cols].sum().sum()}")

# Check by Season
print("\nTotals by Season:")
print(mez.groupby('Temporada')[cols].sum())
