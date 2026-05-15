import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv')
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()

# Helper to sum columns
def s(cols):
    return int(sum([pd.to_numeric(mez[c], errors='coerce').fillna(0).sum() for c in cols]))

# Data for 4 tables
data = [
    ["SRP - 1RAS DOSIS", "Total: " + str(s(['SRP  PRIMERA TOTAL'])), ""],
    ["6 a 11 meses", s(['SRP 6 A 11 MESES PRIMERA']), ""],
    ["12 meses", s(['SRP 1 ANIO  PRIMERA']), ""],
    ["2 – 9 años", s(['SRP 2 A 5 ANIOS PRIMERA', 'SRP 6 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS PRIMERA']), ""],
    ["10 – 19 años", s(['SRP 10 A 19 ANIOS PRIMERA']), ""],
    ["20 – 29 años", s(['SRP 20 A 29 ANIOS PRIMERA']), ""],
    ["30 – 39 años", s(['SRP 30 A 39 ANIOS PRIMERA']), ""],
    ["40 – 49 años", s(['SRP 40 A 49 ANIOS PRIMERA']), ""],
    ["Jornaleros", s(['SRP JORNALEROS AGRICOLAS PRIMERA']), ""],
    ["", "", ""],
    ["SRP - 2DAS DOSIS", "Total: " + str(s(['SRP SEGUNDA TOTAL'])), ""],
    ["18 meses", s(['SRP 18 MESES SEGUNDA']), ""],
    ["2 – 5 años", s(['SRP 2 A 5 ANIOS SEGUNDA']), ""],
    ["6 años", s(['SRP 6 ANIOS SEGUNDA']), ""],
    ["7 – 9 años", s(['SRP 7 A 9 ANIOS SEGUNDA']), ""],
    ["Jornaleros", s(['SRP JORNALEROS AGRICOLAS SEGUNDA']), ""],
    ["", "", ""],
    ["SR - 1RAS DOSIS", "Total: " + str(s(['SR PRIMERA TOTAL'])), ""],
    ["6 a 11 meses", s(['SR 6 A 11 MESES PRIMERA']), ""],
    ["1 – 9 años", s(['SR 1 ANIO PRIMERA', 'SR 2 A 5 ANIOS PRIMERA', 'SR 6 ANIOS PRIMERA', 'SR 7 A 9 ANIOS PRIMERA']), ""],
    ["10 – 19 años", s(['SR 10 A 19 ANIOS PRIMERA']), ""],
    ["20 – 29 años", s(['SR 20 A 29 ANIOS PRIMERA']), ""],
    ["30 – 39 años", s(['SR 30 A 39 ANIOS PRIMERA']), ""],
    ["40 – 49 años", s(['SR 40 A 49 ANIOS PRIMERA']), ""],
    ["Jornaleros", s(['SR JORNALEROS AGRICOLAS PRIMERA']), ""],
    ["", "", ""],
    ["SR - 2DAS DOSIS", "Total: " + str(s(['SR SEGUNDA TOTAL'])), ""],
    ["1 – 9 años", s(['SR 18 MESES SEGUNDA', 'SR 2 A 5 ANIOS SEGUNDA', 'SR 6 ANIOS SEGUNDA', 'SR 7 A 9 ANIOS SEGUNDA']), ""],
    ["10 – 19 años", s(['SR 10 A 19 ANIOS SEGUNDA']), ""],
    ["20 – 29 años", s(['SR 20 A 29 ANIOS SEGUNDA']), ""],
    ["30 – 39 años", s(['SR 30 A 39 ANIOS SEGUNDA']), ""],
    ["40 – 49 años", s(['SR 40 A 49 ANIOS SEGUNDA']), ""],
    ["Jornaleros", s(['SR JORNALEROS AGRICOLAS SEGUNDA']), ""],
    ["", "", ""],
    ["Total de biológico aplicado SRP + SR (Mezquital)", s(['SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL', 'SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL']), " dosis"]
]

final_df = pd.DataFrame(data, columns=["Categoría", "Valor", "Unidad"])
final_df.to_excel(r'c:\Descargas_SRP\Reporte_Mezquital_Total_23453.xlsx', index=False)
print("File created successfully.")
