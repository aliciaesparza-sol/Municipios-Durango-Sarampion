import json
import matplotlib.pyplot as plt
import unicodedata
import os
import pandas as pd

def normalize_name(name):
    if pd.isna(name) or not name: return ''
    name = str(name).strip().upper()
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return name

def get_color(coverage):
    if coverage is None: return '#475569'
    if coverage >= 95.0: return '#22c55e'
    if coverage >= 80.0: return '#eab308'
    return '#ef4444'

def get_text_color(coverage):
    if coverage is None: return 'white'
    if coverage >= 95.0: return 'white'
    if coverage >= 80.0: return 'black'
    return 'white'

def parse_float(val):
    if pd.isna(val): return 0.0
    val = str(val).replace('%', '').replace(',', '').strip()
    try: return float(val)
    except: return 0.0

def parse_int(val):
    if pd.isna(val): return 0
    val = str(val).replace(',', '').strip()
    try: return int(float(val))
    except: return 0

def main():
    excel_path = r'c:\Users\aicil\OneDrive\Escritorio\Municipios\COBERTURA_SARAMPION_POR_MUNICIPIO_2026_13mayo2026.xlsx'
    df = pd.read_excel(excel_path, sheet_name='RESUMEN MUNICIPIOS', header=None)

    start_row = 7
    data_dict = {}
    total_meta = 0
    total_dosis = 0

    for idx, row in df.iloc[start_row:].iterrows():
        muni = row[1]
        if pd.isna(muni) or str(muni).strip() == '':
            continue
        muni_str = str(muni).strip()
        if muni_str.upper() in ['MUNICIPIO', 'DURANGO', 'TOTAL']:
            continue
            
        meta = parse_int(row[3])
        dosis = parse_int(row[7])
        cob = parse_float(row[9]) # % Cob vs Meta
        
        # Ensure it is a pure percentage number (e.g. 61.1 instead of 0.611 if read as fraction)
        # If the file had 0.611 formatted as %, pandas reads 0.611. Let's multiply by 100 if it's less than 1.5 but meta > 0
        if cob > 0 and cob < 2.0:
            cob = cob * 100.0

        total_meta += meta
        total_dosis += dosis
        
        data_dict[normalize_name(muni_str)] = {
            'nombre_original': muni_str,
            'meta': meta,
            'dosis': dosis,
            'cobertura_pct': cob
        }

    global_cob = (total_dosis / total_meta * 100) if total_meta > 0 else 0

    geojson_path = r'c:\Users\aicil\OneDrive\Escritorio\Municipios\municipios.json'
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson = json.load(f)

    fig = plt.figure(figsize=(24, 14))
    fig.patch.set_facecolor('#ffffff')

    ax_map = fig.add_axes([0.0, 0.05, 0.60, 0.85])
    ax_map.set_aspect('equal')
    ax_map.axis('off')

    ax_map.set_title(f'Cobertura Sectorial Sarampión - 2026\nEstado de Durango (Corte: 13 Mayo)', fontsize=26, color='#333333', pad=20, fontweight='bold')

    for feature in geojson['features']:
        muni_name = feature['properties']['NOM_MUN']
        norm_name = normalize_name(muni_name)
        
        muni_data = None
        for key, val in data_dict.items():
            if key == norm_name or key in norm_name or norm_name in key:
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
            cov = coverage if coverage is not None else 0
            label_text = f"{muni_name[:10]}\n{cov:.1f}%"
            ax_map.text(cx, cy, label_text, ha='center', va='center', fontsize=5, color='#111111', 
                    fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.3, boxstyle='round,pad=0.1'))

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='≥ 95% (Óptimo)', markerfacecolor='#22c55e', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='80% - 94.9% (Precaución)', markerfacecolor='#eab308', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='< 80% (Crítico)', markerfacecolor='#ef4444', markersize=15)
    ]
    ax_map.legend(handles=legend_elements, loc='lower left', fontsize=12, frameon=False)

    raw_data = [{'muni': 'DURANGO (GLOBAL)', 'cob': global_cob}]
    for muni_key, muni_val in sorted(data_dict.items(), key=lambda x: x[0]):
        raw_data.append({'muni': muni_val['nombre_original'].title()[:15], 'cob': muni_val['cobertura_pct']})

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

    ax_table = fig.add_axes([0.62, 0.1, 0.35, 0.8])
    ax_table.axis('off')

    colLabels = ['Municipio', 'Cob %', 'Municipio', 'Cob %']

    flat_colors = []
    for rc in cell_colors:
        flat_colors.append([rc[0][0], rc[1][0], rc[2][0], rc[3][0]])
        
    table = ax_table.table(cellText=cell_text, colLabels=colLabels, cellColours=flat_colors, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.0)

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
                if "DURANGO (GLOBAL)" in text_val:
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#f1f5f9')

    target_dir = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\ERRA\VACUNACIÓN HISTORICO'
    out_name = os.path.join(target_dir, 'mapa_estatico_sarampion_2026_actualizado.png')
    plt.savefig(out_name, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print('Generado:', out_name)

if __name__ == '__main__':
    main()
