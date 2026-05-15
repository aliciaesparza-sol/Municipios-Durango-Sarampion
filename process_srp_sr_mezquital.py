import pandas as pd

# Load the CSV
csv_path = r'c:\Descargas_SRP\SRP-SR-2025_14-05-2026 07-32-54.csv'
df = pd.read_csv(csv_path)

# Fill NaNs with 0 and convert to numeric
df = df.fillna(0)

# Filter for Mezquital
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str).str.strip().str.upper()
df = df[df['MUNICIPIO'] == 'MEZQUITAL']

if df.empty:
    print("No data found for municipality: MEZQUITAL")
else:
    numeric_cols = [c for c in df.columns if c not in ['id', 'INSTITUCION', 'DELEGACION', 'ESTADO', 'JURISDICCION', 'MUNICIPIO', 'CLUES', 'SEMANA', 'Temporada', 'Fecha de registro']]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Aggregations
    results = {}

    # 1. SRP 1RAS
    results['SRP 1RAS'] = {
        '6 A 11 MESES': df['SRP 6 A 11 MESES PRIMERA'].sum(),
        '12 MESES': df['SRP 1 ANIO  PRIMERA'].sum(),
        '2 - 9 AÑOS': df['SRP 2 A 5 ANIOS PRIMERA'].sum() + df['SRP 6 ANIOS PRIMERA'].sum() + df['SRP 7 A 9 ANIOS PRIMERA'].sum(),
        '10 - 19 AÑOS': df['SRP 10 A 19 ANIOS PRIMERA'].sum(),
        '20 - 29 AÑOS': df['SRP 20 A 29 ANIOS PRIMERA'].sum(),
        '30 - 39 AÑOS': df['SRP 30 A 39 ANIOS PRIMERA'].sum(),
        '40 - 49 AÑOS': df['SRP 40 A 49 ANIOS PRIMERA'].sum(),
        'JORNALEROS': df['SRP JORNALEROS AGRICOLAS PRIMERA'].sum(),
        'TOTAL': df['SRP  PRIMERA TOTAL'].sum()
    }

    # 2. SRP 2DAS
    results['SRP 2DAS'] = {
        '18 MESES': df['SRP 18 MESES SEGUNDA'].sum(),
        '2 - 5 AÑOS': df['SRP 2 A 5 ANIOS SEGUNDA'].sum(),
        '6 AÑOS': df['SRP 6 ANIOS SEGUNDA'].sum(),
        '7 - 9 AÑOS': df['SRP 7 A 9 ANIOS SEGUNDA'].sum(),
        'JORNALEROS': df['SRP JORNALEROS AGRICOLAS SEGUNDA'].sum(),
        'TOTAL': df['SRP SEGUNDA TOTAL'].sum()
    }

    # 3. SR 1RAS
    results['SR 1RAS'] = {
        '6 A 11 MESES': df['SR 6 A 11 MESES PRIMERA'].sum(),
        '1 - 9 AÑOS': df['SR 1 ANIO PRIMERA'].sum() + df['SR 2 A 5 ANIOS PRIMERA'].sum() + df['SR 6 ANIOS PRIMERA'].sum() + df['SR 7 A 9 ANIOS PRIMERA'].sum(),
        '10 - 19 AÑOS': df['SR 10 A 19 ANIOS PRIMERA'].sum(),
        '20 - 29 AÑOS': df['SR 20 A 29 ANIOS PRIMERA'].sum(),
        '30 - 39 AÑOS': df['SR 30 A 39 ANIOS PRIMERA'].sum(),
        '40 - 49 AÑOS': df['SR 40 A 49 ANIOS PRIMERA'].sum(),
        'JORNALEROS': df['SR JORNALEROS AGRICOLAS PRIMERA'].sum(),
        'TOTAL': df['SR PRIMERA TOTAL'].sum()
    }

    # 4. SR 2DAS
    results['SR 2DAS'] = {
        '1 - 9 AÑOS': df['SR 18 MESES SEGUNDA'].sum() + df['SR 2 A 5 ANIOS SEGUNDA'].sum() + df['SR 6 ANIOS SEGUNDA'].sum() + df['SR 7 A 9 ANIOS SEGUNDA'].sum(),
        '10 - 19 AÑOS': df['SR 10 A 19 ANIOS SEGUNDA'].sum(),
        '20 - 29 AÑOS': df['SR 20 A 29 ANIOS SEGUNDA'].sum(),
        '30 - 39 AÑOS': df['SR 30 A 39 ANIOS SEGUNDA'].sum(),
        '40 - 49 AÑOS': df['SR 40 A 49 ANIOS SEGUNDA'].sum(),
        'JORNALEROS': df['SR JORNALEROS AGRICOLAS SEGUNDA'].sum(),
        'TOTAL': df['SR SEGUNDA TOTAL'].sum()
    }

    # Create a combined dataframe for Excel
    rows = []
    for vaccine_type, data in results.items():
        rows.append([vaccine_type, '', ''])
        for group, value in data.items():
            rows.append(['', group, int(value)])
        rows.append(['', '', '']) # empty row

    # Calculate Global Total
    total_global = results['SRP 1RAS']['TOTAL'] + results['SRP 2DAS']['TOTAL'] + results['SR 1RAS']['TOTAL'] + results['SR 2DAS']['TOTAL']
    rows.append(['TOTAL DE BIOLOGICO APLICADO SRP + SR (MEZQUITAL)', '', int(total_global)])
    final_df = pd.DataFrame(rows, columns=['Tipo de Vacuna', 'Grupo de Edad', 'Total Dosis'])

    # Save to Excel
    output_excel = r'c:\Descargas_SRP\Resumen_Dosis_SRP_SR_Mezquital.xlsx'
    final_df.to_excel(output_excel, index=False)

    print(f"Excel summary for Mezquital saved to: {output_excel}")
    print(f"Mezquital Total: {total_global}")
