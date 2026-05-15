import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv')
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
mezquital = df[df['MUNICIPIO'] == 'MEZQUITAL']

print("Seasons found in Mezquital:")
print(mezquital['Temporada'].unique())

print("\nInstitutions found in Mezquital:")
print(mezquital['INSTITUCION'].unique())

# Aggregate by Season and Institution
summary = mezquital.groupby(['Temporada', 'INSTITUCION']).agg({
    'SRP  PRIMERA TOTAL': 'sum',
    'SRP SEGUNDA TOTAL': 'sum',
    'SR PRIMERA TOTAL': 'sum',
    'SR SEGUNDA TOTAL': 'sum'
})
print("\nSummary per Season and Institution:")
print(summary)
