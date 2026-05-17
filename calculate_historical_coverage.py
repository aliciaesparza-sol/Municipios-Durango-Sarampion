import pandas as pd
import unicodedata

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).upper().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

def main():
    print("Iniciando cálculo de cobertura histórica de Sarampión (2020-2025)...")

    # 1. Cargar datos de población (CONAPO)
    conapo_file = 'conapo_durango_procesado_2020_2025.csv'
    conapo_estimado = 'conapo_durango_estimado_2020_2025.csv'
    
    try:
        df_pop = pd.read_csv(conapo_file)
        print(f"Cargados datos procesados de CONAPO: {conapo_file}")
    except FileNotFoundError:
        df_pop = pd.read_csv(conapo_estimado)
        print(f"Cargados datos ESTIMADOS de CONAPO: {conapo_estimado}")

    # Normalizar columnas
    df_pop['MUNICIPIO_NORM'] = df_pop['MUNICIPIO'].apply(normalize_text)
    
    # 2. Cargar datos históricos de vacunación
    hist_file = r'c:/Users/aicil/OneDrive/Escritorio/PVU/SARAMPIÓN/ERRA/VACUNACIÓN HISTORICO/sr_srp_durango_2020_2026_municipio_variable_num.csv'
    
    try:
        df_vac = pd.read_csv(hist_file)
        print(f"Cargados datos históricos de vacunación: {hist_file}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo histórico: {hist_file}")
        return

    # 3. Filtrar vacunación por años (2020-2025)
    df_vac = df_vac[df_vac['anio'].isin(range(2020, 2026))]
    df_vac['dosis'] = pd.to_numeric(df_vac['dosis'], errors='coerce').fillna(0)
    df_vac['MUNICIPIO_NORM'] = df_vac['municipio'].apply(normalize_text)

    # Agrupar dosis por año y municipio
    df_vac_agrupado = df_vac.groupby(['anio', 'MUNICIPIO_NORM'])['dosis'].sum().reset_index()
    df_vac_agrupado.rename(columns={'anio': 'AÑO', 'dosis': 'DOSIS_APLICADAS'}, inplace=True)

    # 4. Cruzar datos (Merge) a nivel municipio
    df_merge = pd.merge(df_pop, df_vac_agrupado, left_on=['AÑO', 'MUNICIPIO_NORM'], right_on=['AÑO', 'MUNICIPIO_NORM'], how='left')
    df_merge['DOSIS_APLICADAS'] = df_merge['DOSIS_APLICADAS'].fillna(0)

    # 5. Calcular Cobertura Sectorial (Municipal)
    df_merge['COBERTURA_SECTORIAL_PCT'] = (df_merge['DOSIS_APLICADAS'] / df_merge['POBLACION_MENOR_49']) * 100
    df_merge['COBERTURA_SECTORIAL_PCT'] = df_merge['COBERTURA_SECTORIAL_PCT'].round(2)

    # Preparar df sectorial final
    columnas_sectoriales = ['AÑO', 'ENTIDAD', 'MUNICIPIO', 'POBLACION_MENOR_49', 'DOSIS_APLICADAS', 'COBERTURA_SECTORIAL_PCT']
    df_sectorial = df_merge[columnas_sectoriales].sort_values(['AÑO', 'MUNICIPIO'])

    # 6. Calcular Cobertura Global (Estatal por Año)
    df_global = df_merge.groupby(['AÑO', 'ENTIDAD'])[['POBLACION_MENOR_49', 'DOSIS_APLICADAS']].sum().reset_index()
    df_global['COBERTURA_GLOBAL_PCT'] = (df_global['DOSIS_APLICADAS'] / df_global['POBLACION_MENOR_49']) * 100
    df_global['COBERTURA_GLOBAL_PCT'] = df_global['COBERTURA_GLOBAL_PCT'].round(2)

    # 7. Guardar en Excel con hojas separadas
    output_excel = 'Cobertura_Historica_Sarampion_2020_2025.xlsx'
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_global.to_excel(writer, sheet_name='Cobertura Global Estatal', index=False)
        df_sectorial.to_excel(writer, sheet_name='Cobertura Sectorial Municipal', index=False)

    print(f"Reporte generado exitosamente: {output_excel}")

if __name__ == '__main__':
    main()
