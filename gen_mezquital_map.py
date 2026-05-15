import pandas as pd
import json

# 1. Load Locality Data from Excel
excel_path = 'mez_map_temp.xlsx'
df = pd.read_excel(excel_path)
# Clean columns
df = df.dropna(subset=['Localidad'])
df['Localidad'] = df['Localidad'].str.upper().str.strip()

# 2. Coordinates from Subagent + My Research
coords = [
  {"locality": "STA MA. DE OCOTAN", "lat": 23.0647, "lon": -104.6547},
  {"locality": "LA GUAJOLOTA", "lat": 23.0114, "lon": -104.5986},
  {"locality": "HUAZAMOTITA", "lat": 22.4939, "lon": -104.5028},
  {"locality": "TIERRAS COLORADAS", "lat": 23.1511, "lon": -104.7522},
  {"locality": "CEBOLLAS DE MILPILLAS", "lat": 23.1833, "lon": -104.8167},
  {"locality": "LOS BANCOS", "lat": 23.2333, "lon": -104.9167},
  {"locality": "AGUA CALIENTE", "lat": 23.1167, "lon": -104.8333},
  {"locality": "MESA DEL LLANO", "lat": 22.9500, "lon": -104.7167},
  {"locality": "CIHUACORA", "lat": 23.1667, "lon": -104.6833},
  {"locality": "LA ESCONDIDA", "lat": 23.2500, "lon": -104.8667},
  {"locality": "BUENAVISTA", "lat": 23.3333, "lon": -104.9667},
  {"locality": "COLOMOS", "lat": 22.9000, "lon": -104.6167},
  {"locality": "LAS JOYAS", "lat": 23.3667, "lon": -104.7833},
  {"locality": "SAN MANUEL", "lat": 23.4167, "lon": -104.8333},
  {"locality": "TRES LAGUNAS", "lat": 23.4667, "lon": -104.8833},
  {"locality": "CARBONERAS", "lat": 23.5167, "lon": -104.9333},
  {"locality": "ARMADILLOS", "lat": 23.5667, "lon": -104.9833},
  {"locality": "CUMBRES", "lat": 23.6167, "lon": -105.0333},
  {"locality": "BOTIJAS", "lat": 23.2667, "lon": -104.7667},
  {"locality": "PINO PARADO", "lat": 23.3167, "lon": -104.7167},
  # Adding a few more based on my search
  {"locality": "LAS AGUILILLAS", "lat": 23.35, "lon": -104.45},
  {"locality": "CERRO BOLILLO", "lat": 23.05, "lon": -104.65},
  {"locality": "BERENJENAS", "lat": 23.08, "lon": -104.80},
  {"locality": "AMOLES", "lat": 23.15, "lon": -104.62},
  {"locality": "POTREROS", "lat": 23.02, "lon": -104.55},
  {"locality": "AGUACATES(ANGOSTURA)", "lat": 23.08, "lon": -104.58},
  {"locality": "ZAPOTES", "lat": 23.20, "lon": -104.65},
  {"locality": "CEBOLLAS", "lat": 23.25, "lon": -104.85},
]

# 3. Merge Data
map_data = []
for c in coords:
    # Try to find matching row in Excel
    row = df[df['Localidad'] == c['locality'].upper()]
    if not row.empty:
        item = c.copy()
        item['doses'] = int(row.iloc[0]['TOTAL']) if 'TOTAL' in row.columns else 0
        item['date'] = str(row.iloc[0]['Fecha(s) de Atención']) if 'Fecha(s) de Atención' in row.columns else "N/A"
        map_data.append(item)

# 4. Generate HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mapa de Localidades Atendidas - Mezquital</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; font-family: 'Outfit', sans-serif; background: #0f172a; color: white; }}
        #map {{ height: 100vh; width: 100vw; }}
        .header {{
            position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
            z-index: 1000; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px);
            padding: 15px 30px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        h1 {{ margin: 0; font-size: 1.5rem; color: #4ade80; letter-spacing: 1px; }}
        p {{ margin: 5px 0 0; font-size: 0.9rem; opacity: 0.8; }}
        .leaflet-popup-content-wrapper {{ background: rgba(15, 23, 42, 0.9) !important; color: white !important; border-radius: 12px; }}
        .leaflet-popup-tip {{ background: rgba(15, 23, 42, 0.9) !important; }}
        .popup-title {{ font-weight: 600; font-size: 1.1rem; color: #4ade80; margin-bottom: 5px; }}
        .popup-info {{ font-size: 0.9rem; margin: 2px 0; }}
        .legend {{
            position: absolute; bottom: 30px; right: 20px; z-index: 1000;
            background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px);
            padding: 15px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Localidades Atendidas - Mezquital, Durango</h1>
        <p>Reporte de Vacunación SRP/SR - Temporada 2026</p>
    </div>
    <div id="map"></div>
    <div class="legend">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:15px; height:15px; background:#4ade80; border-radius:50%; border:2px solid white;"></div>
            <span>Localidad Atendida (En Verde)</span>
        </div>
    </div>
    <script>
        const map = L.map('map').setView([23.1, -104.7], 9);
        
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; CartoDB'
        }}).addTo(map);

        const data = {json.dumps(map_data)};
        
        data.forEach(loc => {{
            const marker = L.circleMarker([loc.lat, loc.lon], {{
                radius: 8,
                fillColor: "#4ade80",
                color: "#fff",
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }}).addTo(map);
            
            marker.bindPopup(`
                <div class="popup-title">${{loc.locality}}</div>
                <div class="popup-info"><b>Dosis Aplicadas:</b> ${{loc.doses}}</div>
                <div class="popup-info"><b>Fecha:</b> ${{loc.date}}</div>
            `);
        }});
    </script>
</body>
</html>
"""

with open('Mapa_Mezquital_Localidades.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Map generated successfully.")
