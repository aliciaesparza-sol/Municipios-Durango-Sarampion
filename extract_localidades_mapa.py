import pandas as pd

path = 'mez_map_temp.xlsx'

try:
    df = pd.read_excel(path)
    localidades = df['Localidad'].dropna().unique().tolist()
    print("Localities found:")
    print(localidades)
    
    with open('localidades_mezquital.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(localidades, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"Error: {e}")
