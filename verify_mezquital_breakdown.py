import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv')
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()

# Helper to sum columns and handle NaNs
def sum_cols(df, cols):
    return sum([pd.to_numeric(df[c], errors='coerce').fillna(0).sum() for c in cols])

print("SRP 1ra Breakdown:")
print(f"6-11m: {sum_cols(mez, ['SRP 6 A 11 MESES PRIMERA'])}")
print(f"12m: {sum_cols(mez, ['SRP 1 ANIO  PRIMERA'])}")
print(f"2-9y: {sum_cols(mez, ['SRP 2 A 5 ANIOS PRIMERA', 'SRP 6 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS PRIMERA'])}")
print(f"10-19y: {sum_cols(mez, ['SRP 10 A 19 ANIOS PRIMERA'])}")
print(f"20-29y: {sum_cols(mez, ['SRP 20 A 29 ANIOS PRIMERA'])}")
print(f"30-39y: {sum_cols(mez, ['SRP 30 A 39 ANIOS PRIMERA'])}")
print(f"40-49y: {sum_cols(mez, ['SRP 40 A 49 ANIOS PRIMERA'])}")
print(f"Jornaleros: {sum_cols(mez, ['SRP JORNALEROS AGRICOLAS PRIMERA'])}")
print(f"TOTAL: {sum_cols(mez, ['SRP  PRIMERA TOTAL'])}")

print("\nSRP 2da Breakdown:")
print(f"18m: {sum_cols(mez, ['SRP 18 MESES SEGUNDA'])}")
print(f"2-5y: {sum_cols(mez, ['SRP 2 A 5 ANIOS SEGUNDA'])}")
print(f"6y: {sum_cols(mez, ['SRP 6 ANIOS SEGUNDA'])}")
print(f"7-9y: {sum_cols(mez, ['SRP 7 A 9 ANIOS SEGUNDA'])}")
print(f"Jornaleros: {sum_cols(mez, ['SRP JORNALEROS AGRICOLAS SEGUNDA'])}")
print(f"TOTAL: {sum_cols(mez, ['SRP SEGUNDA TOTAL'])}")

print("\nSR 1ra Breakdown:")
print(f"6-11m: {sum_cols(mez, ['SR 6 A 11 MESES PRIMERA'])}")
print(f"1-9y: {sum_cols(mez, ['SR 1 ANIO PRIMERA', 'SR 2 A 5 ANIOS PRIMERA', 'SR 6 ANIOS PRIMERA', 'SR 7 A 9 ANIOS PRIMERA'])}")
print(f"10-19y: {sum_cols(mez, ['SR 10 A 19 ANIOS PRIMERA'])}")
print(f"20-29y: {sum_cols(mez, ['SR 20 A 29 ANIOS PRIMERA'])}")
print(f"30-39y: {sum_cols(mez, ['SR 30 A 39 ANIOS PRIMERA'])}")
print(f"40-49y: {sum_cols(mez, ['SR 40 A 49 ANIOS PRIMERA'])}")
print(f"Jornaleros: {sum_cols(mez, ['SR JORNALEROS AGRICOLAS PRIMERA'])}")
print(f"TOTAL: {sum_cols(mez, ['SR PRIMERA TOTAL'])}")

print("\nSR 2da Breakdown:")
print(f"1-9y: {sum_cols(mez, ['SR 18 MESES SEGUNDA', 'SR 2 A 5 ANIOS SEGUNDA', 'SR 6 ANIOS SEGUNDA', 'SR 7 A 9 ANIOS SEGUNDA'])}")
print(f"10-19y: {sum_cols(mez, ['SR 10 A 19 ANIOS SEGUNDA'])}")
print(f"20-29y: {sum_cols(mez, ['SR 20 A 29 ANIOS SEGUNDA'])}")
print(f"30-39y: {sum_cols(mez, ['SR 30 A 39 ANIOS SEGUNDA'])}")
print(f"40-49y: {sum_cols(mez, ['SR 40 A 49 ANIOS SEGUNDA'])}")
print(f"Jornaleros: {sum_cols(mez, ['SR JORNALEROS AGRICOLAS SEGUNDA'])}")
print(f"TOTAL: {sum_cols(mez, ['SR SEGUNDA TOTAL'])}")
