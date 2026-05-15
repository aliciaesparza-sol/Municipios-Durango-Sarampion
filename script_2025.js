// Initialize the map centered on Durango, Mexico
const map = L.map('map', {
    zoomControl: false,
    attributionControl: false
}).setView([24.93, -104.91], 7);

// Add a premium light base map (CartoDB Voyager)
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    maxZoom: 19
}).addTo(map);

L.control.zoom({
    position: 'bottomright'
}).addTo(map);

// Data is now loaded from global variables (municipiosGeo and coverageData2025)
const geojsonData = municipiosGeo;
const coverageData = coverageData2025;
let geojsonLayer = null;
let currentAgeGroup = '1_ano';

document.getElementById('age-group').addEventListener('change', function(e) {
    currentAgeGroup = e.target.value;
    updateMap();
});

function normalizeName(name) {
    if (!name) return "";
    return name.toString().trim().toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function getColor(coverage) {
    if (coverage === null || coverage === undefined) return '#eaddca';
    if (coverage >= 95) return '#16a34a';
    if (coverage >= 80) return '#eab308';
    return '#dc2626';
}

function getMuniData(featureName) {
    if (!coverageData || !featureName) return null;
    const normName = normalizeName(featureName);
    if (coverageData[normName]) {
        return coverageData[normName][currentAgeGroup];
    }
    for (const key in coverageData) {
        if (normName === key || normName.includes(key) || key.includes(normName)) {
            return coverageData[key][currentAgeGroup];
        }
    }
    return null;
}

function style(feature) {
    const data = getMuniData(feature.properties.NOM_MUN);
    let fillColor = '#eaddca';
    if (data) {
        fillColor = getColor(data.coverage);
    }
    return {
        fillColor: fillColor,
        weight: 2.5,
        opacity: 1,
        color: '#000000', // Solid black
        fillOpacity: 0.85
    };
}

function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 3,
        color: '#000',
        fillOpacity: 0.95
    });
    layer.bringToFront();
}

function resetHighlight(e) {
    if (geojsonLayer) {
        geojsonLayer.resetStyle(e.target);
    }
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });
    
    layer.on('popupopen', function() {
        const name = feature.properties.NOM_MUN;
        const data = getMuniData(name);
        
        let covStr = 'Sin datos';
        let statusStr = 'N/A';
        let dotColor = '#cbd5e1';
        
        if (data) {
            covStr = data.coverage_str;
            dotColor = getColor(data.coverage);
            statusStr = data.coverage >= 95 ? 'ÓPTIMO' : (data.coverage >= 80 ? 'EN RIESGO' : 'CRÍTICO');
        }

        const popupContent = `
            <div class="municipality-info">
                <h3 style="margin-bottom:10px;">${name}</h3>
                <div class="stat">
                    <span class="stat-label">Cobertura (2025):</span>
                    <span class="stat-value">${covStr}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Estado:</span>
                    <span class="stat-value"><span class="semaforo-dot" style="background: ${dotColor};"></span> ${statusStr}</span>
                </div>
            </div>
        `;
        layer.setPopupContent(popupContent);
    });
    
    layer.bindPopup('Cargando...');
}

function updateMap() {
    if (!geojsonData || !coverageData) return;
    if (geojsonLayer) {
        map.removeLayer(geojsonLayer);
    }
    geojsonLayer = L.geoJson(geojsonData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
}

// Initial render
updateMap();
if (geojsonLayer) {
    map.fitBounds(geojsonLayer.getBounds());
}
