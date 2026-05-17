import json
import os

def build_html():
    json_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\ERRA\VACUNACIÓN HISTORICO\cobertura_historica_2020_2025.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data_json_str = f.read()

    # The HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histórico Sarampión 2020-2025</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f5;
        }}
        #header {{
            background-color: #1e293b;
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        #header h1 {{
            margin: 0;
            font-size: 1.5rem;
        }}
        #controls {{
            background: white;
            padding: 15px;
            margin: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        select {{
            padding: 8px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #cbd5e1;
            background: #f8fafc;
            cursor: pointer;
        }}
        #map {{
            height: calc(100vh - 160px);
            margin: 0 15px 15px 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            background-color: #e2e8f0;
        }}
        .info {{
            padding: 12px;
            font: 14px/16px Arial, Helvetica, sans-serif;
            background: white;
            background: rgba(255,255,255,0.9);
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            border-radius: 5px;
            min-width: 200px;
        }}
        .info h4 {{
            margin: 0 0 5px;
            color: #333;
            font-size: 16px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        .legend {{
            line-height: 18px;
            color: #555;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }}
        .legend i {{
            width: 18px;
            height: 18px;
            float: left;
            margin-right: 8px;
            opacity: 0.9;
            border: 1px solid #ccc;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>Cobertura Histórica de Vacunación - Sarampión</h1>
        <div style="font-size: 0.9rem; color: #cbd5e1;">Población < 49 años</div>
    </div>
    
    <div id="controls">
        <label for="yearSelect"><strong>Seleccionar Año:</strong></label>
        <select id="yearSelect">
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            <option value="2024">2024</option>
            <option value="2025" selected>2025</option>
        </select>
    </div>

    <div id="map"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="../../../Municipios/municipios_geo.js"></script>
    <script>
        const histData = {data_json_str};
        let currentYear = '2025';
        let geojsonLayer;

        const map = L.map('map').setView([24.6, -104.8], 7);

        // Capa base limpia y profesional
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }}).addTo(map);

        // Control de información superior derecha (Tooltip)
        const info = L.control();
        info.onAdd = function (map) {{
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        }};

        info.update = function (props) {{
            if (!props) {{
                this._div.innerHTML = '<h4>Municipio</h4>Pasa el cursor sobre una región';
                return;
            }}
            
            const muniName = props.NOM_MUN;
            const normName = normalizeString(muniName);
            
            let dataYear = histData[currentYear] || {{}};
            let muniData = dataYear[normName];
            
            // Fuzzy match if needed
            if (!muniData) {{
                for (let key in dataYear) {{
                    if (normalizeString(key).includes(normName) || normName.includes(normalizeString(key))) {{
                        muniData = dataYear[key];
                        break;
                    }}
                }}
            }}

            if (muniData) {{
                const pct = muniData.cobertura_pct.toFixed(2);
                let colorText = 'red';
                if(pct >= 95) colorText = 'green';
                else if(pct >= 80) colorText = '#d97706'; // dark yellow

                this._div.innerHTML = `<h4>${{muniName}} (${{currentYear}})</h4>
                    <b>Población < 49:</b> ${{muniData.poblacion_menor_49.toLocaleString()}}<br>
                    <b>Dosis Aplicadas:</b> ${{muniData.dosis_aplicadas.toLocaleString()}}<br>
                    <b style="color: ${{colorText}};">Cobertura: ${{pct}}%</b>`;
            }} else {{
                this._div.innerHTML = `<h4>${{muniName}} (${{currentYear}})</h4>No hay datos`;
            }}
        }};
        info.addTo(map);

        // Funciones auxiliares
        function normalizeString(str) {{
            return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase().trim();
        }}

        function getColor(coverage) {{
            if (coverage === undefined || coverage === null) return '#475569'; // gris
            if (coverage >= 95) return '#22c55e'; // verde
            if (coverage >= 80) return '#eab308'; // amarillo
            return '#ef4444'; // rojo
        }}

        function style(feature) {{
            const muniName = feature.properties.NOM_MUN;
            const normName = normalizeString(muniName);
            let dataYear = histData[currentYear] || {{}};
            let muniData = dataYear[normName];
            
            if (!muniData) {{
                for (let key in dataYear) {{
                    if (normalizeString(key).includes(normName) || normName.includes(normalizeString(key))) {{
                        muniData = dataYear[key];
                        break;
                    }}
                }}
            }}

            const coverage = muniData ? muniData.cobertura_pct : null;

            return {{
                fillColor: getColor(coverage),
                weight: 1.5,
                opacity: 1,
                color: '#ffffff',
                dashArray: '',
                fillOpacity: 0.8
            }};
        }}

        function highlightFeature(e) {{
            const layer = e.target;
            layer.setStyle({{
                weight: 3,
                color: '#333',
                fillOpacity: 0.9
            }});
            layer.bringToFront();
            info.update(layer.feature.properties);
        }}

        function resetHighlight(e) {{
            geojsonLayer.resetStyle(e.target);
            info.update();
        }}

        function onEachFeature(feature, layer) {{
            layer.on({{
                mouseover: highlightFeature,
                mouseout: resetHighlight
            }});
        }}

        function drawMap() {{
            if(geojsonLayer) {{
                map.removeLayer(geojsonLayer);
            }}
            geojsonLayer = L.geoJson(municipiosGeo, {{
                style: style,
                onEachFeature: onEachFeature
            }}).addTo(map);
        }}

        // Leyenda
        const legend = L.control({{position: 'bottomright'}});
        legend.onAdd = function (map) {{
            const div = L.DomUtil.create('div', 'info legend');
            div.innerHTML += '<i style="background:#22c55e"></i> ≥ 95% (Óptimo)<br>';
            div.innerHTML += '<i style="background:#eab308"></i> 80% - 94.9% (Precaución)<br>';
            div.innerHTML += '<i style="background:#ef4444"></i> < 80% (Crítico)<br>';
            div.innerHTML += '<i style="background:#475569"></i> Sin datos<br>';
            return div;
        }};
        legend.addTo(map);

        // Evento de cambio de año
        document.getElementById('yearSelect').addEventListener('change', function(e) {{
            currentYear = e.target.value;
            drawMap();
        }});

        // Dibujar inicial
        drawMap();
    </script>
</body>
</html>
"""

    target_html = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\ERRA\VACUNACIÓN HISTORICO\mapa_historico_sarampion.html'
    with open(target_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML interactivo generado en: {target_html}")

if __name__ == '__main__':
    build_html()
