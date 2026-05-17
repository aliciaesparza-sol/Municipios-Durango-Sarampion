import json
import matplotlib.pyplot as plt
import unicodedata
import os

def normalize_name(name):
    if not name: return ''
    name = str(name).strip().upper()
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return name

def get_color(coverage):
    if coverage is None: return '#475569'
    if coverage >= 95: return '#22c55e'
    if coverage >= 80: return '#eab308'
    return '#ef4444'

def get_text_color(coverage):
    if coverage is None: return 'white'
    if coverage >= 95: return 'white'
    if coverage >= 80: return 'black'
    return 'white'

def generate_historical_map(year, geojson_path, data_path, output_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    with open(data_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    data_year = full_data.get(str(year), {})

    fig = plt.figure(figsize=(24, 14))
    fig.patch.set_facecolor('#ffffff')
    
    # Map area takes up 60% of the left side
    ax_map = fig.add_axes([0.0, 0.05, 0.60, 0.85])
    ax_map.set_aspect('equal')
    ax_map.axis('off')
    
    ax_map.set_title(f'Cobertura Histórica Sarampión - {year}\nEstado de Durango', fontsize=26, color='#333333', pad=20, fontweight='bold')

    for feature in geojson['features']:
        muni_name = feature['properties']['NOM_MUN']
        norm_name = normalize_name(muni_name)
        
        muni_data = None
        for key, val in data_year.items():
            if normalize_name(key) == norm_name:
                muni_data = val
                break
        if not muni_data:
            for key, val in data_year.items():
                if norm_name in normalize_name(key) or normalize_name(key) in norm_name:
                    muni_data = val
                    break

        coverage = muni_data['cobertura_pct'] if muni_data else None
        color = get_color(coverage)
        
        geom = feature['geometry']
        all_x, all_y = [], []
        if geom['type'] == 'Polygon':
            for poly in geom['coordinates']:
                x = [p[0] for p in poly]
                y = [p[1] for p in poly]
                all_x.extend(x)
                all_y.extend(y)
                ax_map.fill(x, y, color=color, edgecolor='#333333', linewidth=0.5, alpha=0.9)
        elif geom['type'] == 'MultiPolygon':
            for multi in geom['coordinates']:
                for poly in multi:
                    x = [p[0] for p in poly]
                    y = [p[1] for p in poly]
                    all_x.extend(x)
                    all_y.extend(y)
                    ax_map.fill(x, y, color=color, edgecolor='#333333', linewidth=0.5, alpha=0.9)

        if all_x and all_y and muni_data:
            cx = (min(all_x) + max(all_x)) / 2.0
            cy = (min(all_y) + max(all_y)) / 2.0
            meta = muni_data.get('poblacion_menor_49', 0)
            cov = coverage if coverage is not None else 0
            label_text = f"{muni_name[:10]}\nCov: {cov:.1f}%"
            ax_map.text(cx, cy, label_text, ha='center', va='center', fontsize=6, color='#111111', 
                    fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5, boxstyle='round,pad=0.2'))

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='≥ 95% (Óptimo)', markerfacecolor='#22c55e', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='80% - 94.9% (Precaución)', markerfacecolor='#eab308', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='< 80% (Crítico)', markerfacecolor='#ef4444', markersize=15)
    ]
    ax_map.legend(handles=legend_elements, loc='lower left', fontsize=14, frameon=False)

    # Preparar tabla
    table_data = []
    total_pob = 0
    total_dos = 0
    raw_data = []
    for muni_key, muni_val in sorted(data_year.items(), key=lambda x: x[0]):
        pob = muni_val.get('poblacion_menor_49', 0)
        dos = muni_val.get('dosis_aplicadas', 0)
        cob = muni_val.get('cobertura_pct', 0)
        total_pob += pob
        total_dos += dos
        raw_data.append({'muni': muni_key.title(), 'cob': cob})

    global_cob = (total_dos / total_pob * 100) if total_pob > 0 else 0
    raw_data.insert(0, {'muni': 'DURANGO (GLOBAL)', 'cob': global_cob})

    half = (len(raw_data) + 1) // 2
    
    cell_text = []
    cell_colors = []
    
    for i in range(half):
        item1 = raw_data[i]
        c1 = get_color(item1['cob'])
        t1 = get_text_color(item1['cob'])
        
        row_text = [item1['muni'], f"{item1['cob']:.1f}%"]
        row_colors = [['white', 'black'], [c1, t1]]
        
        if i + half < len(raw_data):
            item2 = raw_data[i + half]
            c2 = get_color(item2['cob'])
            t2 = get_text_color(item2['cob'])
            row_text.extend([item2['muni'], f"{item2['cob']:.1f}%"])
            row_colors.extend([['white', 'black'], [c2, t2]])
        else:
            row_text.extend(['', ''])
            row_colors.extend([['white', 'black'], ['white', 'black']])
            
        cell_text.append(row_text)
        cell_colors.append(row_colors)

    # Table area takes up 35% of the right side
    ax_table = fig.add_axes([0.62, 0.1, 0.35, 0.8])
    ax_table.axis('off')
    
    colLabels = ['Municipio', 'Cobertura', 'Municipio', 'Cobertura']
    
    flat_colors = []
    for rc in cell_colors:
        flat_colors.append([rc[0][0], rc[1][0], rc[2][0], rc[3][0]])
        
    table = ax_table.table(cellText=cell_text, colLabels=colLabels, cellColours=flat_colors, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)
    
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1F497D')
            cell.set_text_props(color='white', weight='bold')
        elif row > 0:
            if col == 1:
                t_color = cell_colors[row-1][1][1]
                cell.set_text_props(color=t_color, weight='bold')
            elif col == 3:
                t_color = cell_colors[row-1][3][1]
                if t_color: cell.set_text_props(color=t_color, weight='bold')
                
            if col in [0, 2]:
                text_val = cell.get_text().get_text()
                if text_val == 'DURANGO (GLOBAL)':
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#f1f5f9')

    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

if __name__ == '__main__':
    geojson_file = 'municipios.json'
    data_file = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\ERRA\VACUNACIÓN HISTORICO\cobertura_historica_2020_2025.json'
    target_dir = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\ERRA\VACUNACIÓN HISTORICO'
    
    for year in range(2020, 2026):
        out_name = os.path.join(target_dir, f'mapa_estatico_sarampion_{year}.png')
        print(f'Generando {year}...')
        generate_historical_map(year, geojson_file, data_file, out_name)
        print(f'  > {out_name}')
