import pandas as pd
import os
import requests
from io import StringIO
import sys

def main():
    print("Iniciando procesamiento de datos CONAPO...")
    
    # Intenta leer un archivo local primero
    local_file = 'pob_mit_proyecciones.csv'
    
    df = None
    if os.path.exists(local_file):
        print(f"Leyendo archivo local: {local_file}")
        try:
            df = pd.read_csv(local_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(local_file, encoding='latin1')
    else:
        print("No se encontró el archivo local de CONAPO.")
        print("Si tienes el archivo oficial de CONAPO, guárdalo como 'pob_mit_proyecciones.csv' en esta carpeta.")
        
        # Generar datos simulados precisos basados en proyecciones conocidas para Durango
        print("Generando proyecciones base de estimación temporal (sustituir con oficial de CONAPO después)...")
        # Base de municipios de Durango y una población aproximada base 2020 (total, no solo <49)
        municipios_base = {
            'Canatlán': 31401, 'Canelas': 4321, 'Coneto de Comonfort': 4530, 'Cuencamé': 33664, 
            'Durango': 688697, 'General Simón Bolívar': 10038, 'Gómez Palacio': 372750, 'Guadalupe Victoria': 36695, 
            'Guanaceví': 9869, 'Hidalgo': 3843, 'Indé': 4748, 'Lerdo': 163313, 
            'Mapimí': 32514, 'Mezquital': 48583, 'Nazas': 12894, 'Nombre de Dios': 19060, 
            'Ocampo': 8003, 'El Oro': 10384, 'Otáez': 4924, 'Pánuco de Coronado': 12656, 
            'Peñón Blanco': 11118, 'Poanas': 25623, 'Pueblo Nuevo': 51269, 'Rodeo': 12826, 
            'San Bernardo': 2837, 'San Dimas': 17333, 'San Juan de Guadalupe': 5251, 'San Juan del Río': 12213, 
            'San Luis del Cordero': 2103, 'San Pedro del Gallo': 1633, 'Santa Clara': 6727, 'Santiago Papasquiaro': 49207, 
            'Súchil': 6928, 'Tamazula': 26368, 'Tepehuanes': 11378, 'Tlahualilo': 21223, 
            'Topia': 9320, 'Vicente Guerrero': 23476, 'Nuevo Ideal': 27981
        }
        
        # Tasa de crecimiento anual aproximada y porcentaje de pob < 49 años (aprox 72%)
        crecimiento_anual = 0.012 
        porcentaje_menor_49 = 0.72
        
        records = []
        for anio in range(2020, 2026):
            for mun, pob in municipios_base.items():
                pob_estimada = int(pob * ((1 + crecimiento_anual) ** (anio - 2020)))
                pob_menor_49 = int(pob_estimada * porcentaje_menor_49)
                
                records.append({
                    'AÑO': anio,
                    'ENTIDAD': 'Durango',
                    'MUNICIPIO': mun,
                    'POBLACION_TOTAL_ESTIMADA': pob_estimada,
                    'POBLACION_MENOR_49': pob_menor_49
                })
        
        df = pd.DataFrame(records)
        df.to_csv('conapo_durango_estimado_2020_2025.csv', index=False, encoding='utf-8')
        print("Datos estimados guardados en 'conapo_durango_estimado_2020_2025.csv'")
        return

    # Si se leyó el CSV real, procesarlo
    print("Filtrando datos de CONAPO para Durango, años 2020-2025...")
    # Ajustar nombres de columnas según CSV de CONAPO
    col_anio = 'AÑO' if 'AÑO' in df.columns else 'ano' if 'ano' in df.columns else 'year'
    col_entidad = 'ENTIDAD' if 'ENTIDAD' in df.columns else 'entidad' if 'entidad' in df.columns else 'state'
    col_municipio = 'MUNICIPIO' if 'MUNICIPIO' in df.columns else 'municipio' if 'municipio' in df.columns else 'mun'
    col_edad = 'EDAD' if 'EDAD' in df.columns else 'edad' if 'edad' in df.columns else 'age'
    col_poblacion = 'POBLACION' if 'POBLACION' in df.columns else 'poblacion' if 'poblacion' in df.columns else 'pop'

    # Filtrar por años y entidad
    df_dgo = df[(df[col_anio].isin(range(2020, 2026))) & (df[col_entidad].str.contains('Durango', case=False, na=False))]
    
    # Filtrar menores de 49 años (0 a 49)
    df_dgo_menor49 = df_dgo[df_dgo[col_edad] <= 49]
    
    # Agrupar por año y municipio
    df_agrupado = df_dgo_menor49.groupby([col_anio, col_municipio])[col_poblacion].sum().reset_index()
    df_agrupado.rename(columns={col_poblacion: 'POBLACION_MENOR_49'}, inplace=True)
    
    df_agrupado.to_csv('conapo_durango_procesado_2020_2025.csv', index=False, encoding='utf-8')
    print("Datos oficiales procesados y guardados en 'conapo_durango_procesado_2020_2025.csv'")

if __name__ == '__main__':
    main()
