import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import unicodedata

def normalize_name(name):
    if not name: return ""
    name = str(name).strip().upper()
    name = ''.join(c for c in unicodedata.normalize('NFD', name)
                  if unicodedata.category(c) != 'Mn')
    return name

def get_color(coverage):
    if coverage is None: return '#475569'
    if coverage >= 95: return '#22c55e'
    if coverage >= 80: return '#eab308'
    return '#ef4444'

def generate_map(year, age_group, geojson_path, data_path, output_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    title_map = {
        '1_ano': '1 Año (1ra Dosis)',
        '18_meses': '18 Meses (2da Dosis)',
        '6_anos': '6 Años (2da Dosis)'
    }
    plt.title(f'Cobertura {year}\n{title_map[age_group]}', fontsize=16, color='white', pad=20)
    fig.patch.set_facecolor('#0a0a0c')

    for feature in geojson['features']:
        muni_name = feature['properties']['NOM_MUN']
        norm_name = normalize_name(muni_name)
        
        # Link data
        muni_data = data.get(norm_name, {}).get(age_group)
        if not muni_data:
            # Fuzzy match
            for key in data:
                if norm_name in key or key in norm_name:
                    muni_data = data[key].get(age_group)
                    break
        
        color = get_color(muni_data['coverage'] if muni_data else None)
        
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            for poly in geom['coordinates']:
                x = [p[0] for p in poly]
                y = [p[1] for p in poly]
                ax.fill(x, y, color=color, edgecolor='white', linewidth=0.3, alpha=0.8)
        elif geom['type'] == 'MultiPolygon':
            for multi in geom['coordinates']:
                for poly in multi:
                    x = [p[0] for p in poly]
                    y = [p[1] for p in poly]
                    ax.fill(x, y, color=color, edgecolor='white', linewidth=0.3, alpha=0.8)

    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

if __name__ == "__main__":
    maps_to_gen = [
        ('2026', '1_ano', 'coverage_data.json', 'map_2026_12m.png'),
        ('2026', '18_meses', 'coverage_data.json', 'map_2026_18m.png'),
        ('2026', '6_anos', 'coverage_data.json', 'map_2026_6y.png'),
        ('2025', '1_ano', 'coverage_data_2025.json', 'map_2025_12m.png'),
        ('2025', '18_meses', 'coverage_data_2025.json', 'map_2025_18m.png'),
        ('2025', '6_anos', 'coverage_data_2025.json', 'map_2025_6y.png'),
    ]
    
    for year, age, data_file, out in maps_to_gen:
        try:
            generate_map(year, age, 'municipios.json', data_file, out)
            print(f"Generated: {out}")
        except Exception as e:
            print(f"Error generating {out}: {e}")
