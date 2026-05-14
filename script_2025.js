// Initialize the map centered on Durango, Mexico
const map = L.map('map', {
    zoomControl: false,
    attributionControl: false
}).setView([24.93, -104.91], 7);

// Add a premium dark base map
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19
}).addTo(map);

L.control.zoom({
    position: 'bottomright'
}).addTo(map);

let geojsonData = null;
let coverageData = null;
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
    if (coverage === null || coverage === undefined) return '#475569';
    if (coverage >= 95) return '#22c55e';
    if (coverage >= 80) return '#eab308';
    return '#ef4444';
}

function getMuniData(featureName) {
    if (!coverageData || !featureName) return null;
    const normName = normalizeName(featureName);
    if (coverageData[normName]) {
        return coverageData[normName][currentAgeGroup];
    }
    for (const key in coverageData) {
        if (normName.includes(key) || key.includes(normName)) {
            return coverageData[key][currentAgeGroup];
        }
    }
    return null;
}

function style(feature) {
    const data = getMuniData(feature.properties.NOM_MUN);
    let fillColor = '#475569';
    if (data) {
        fillColor = getColor(data.coverage);
    }
    return {
        fillColor: fillColor,
        weight: 1,
        opacity: 1,
        color: 'rgba(255, 255, 255, 0.3)',
        fillOpacity: 0.7
    };
}

function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 2,
        color: '#fff',
        fillOpacity: 0.9
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
        let dotColor = '#475569';
        
        if (data) {
            covStr = data.coverage_str;
            dotColor = getColor(data.coverage);
            statusStr = data.coverage >= 95 ? 'ÓPTIMO' : (data.coverage >= 80 ? 'EN RIESGO' : 'CRÍTICO');
        }

        const popupContent = `
            <div class="municipality-info">
                <h3>${name}</h3>
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

Promise.all([
    fetch('municipios.json').then(res => res.json()),
    fetch('coverage_data_2025.json').then(res => res.json())
]).then(results => {
    geojsonData = results[0];
    coverageData = results[1];
    updateMap();
    map.fitBounds(geojsonLayer.getBounds());
}).catch(error => {
    console.error('Error cargando los datos 2025:', error);
});
