// Initialize the map centered on Durango, Mexico
const map = L.map('map', {
    zoomControl: false,
    attributionControl: false
}).setView([24.93, -104.91], 7);

// Add a premium dark base map (CartoDB Dark Matter)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19
}).addTo(map);

// Add zoom control to a custom position
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

let geojsonData = null;
let coverageData = null;
let geojsonLayer = null;
let currentAgeGroup = '1_ano'; // default

// Listen for age group changes
document.getElementById('age-group').addEventListener('change', function(e) {
    currentAgeGroup = e.target.value;
    updateMap();
});

// Normalize string for matching
function normalizeName(name) {
    if (!name) return "";
    return name.toString().trim().toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

// Function to get color based on coverage (Semaforización)
function getColor(coverage) {
    if (coverage === null || coverage === undefined) return '#475569'; // No data (gray)
    if (coverage >= 95) return '#22c55e'; // Green (Óptimo)
    if (coverage >= 80) return '#eab308'; // Yellow (En Riesgo)
    return '#ef4444'; // Red (Crítico)
}

function getSemaforoColorFromText(text) {
    if (!text) return '#475569';
    if (text.includes('ÓPTIMO')) return '#22c55e';
    if (text.includes('RIESGO')) return '#eab308';
    if (text.includes('CRÍTICO')) return '#ef4444';
    return '#475569';
}

// Get the specific data for a municipality
function getMuniData(featureName) {
    if (!coverageData || !featureName) return null;
    const normName = normalizeName(featureName);
    // Try exact match first
    if (coverageData[normName]) {
        return coverageData[normName][currentAgeGroup];
    }
    
    // Fuzzy match
    for (const key in coverageData) {
        if (normName.includes(key) || key.includes(normName)) {
            return coverageData[key][currentAgeGroup];
        }
    }
    return null;
}

// Style function for each feature
function style(feature) {
    const data = getMuniData(feature.properties.NOM_MUN);
    let fillColor = '#475569'; // default
    
    if (data) {
        fillColor = getColor(data.coverage);
        // Fallback to the text semaforo if coverage parsing failed
        // if (fillColor === '#ef4444' && data.coverage === 0) fillColor = getSemaforoColorFromText(data.semaforo);
    }

    return {
        fillColor: fillColor,
        weight: 1,
        opacity: 1,
        color: 'rgba(255, 255, 255, 0.3)',
        fillOpacity: 0.7
    };
}

// Highlight on hover
function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 2,
        color: '#fff',
        fillOpacity: 0.9,
        dashArray: ''
    });
    layer.bringToFront();
}

// Reset highlight on mouseout
function resetHighlight(e) {
    if (geojsonLayer) {
        geojsonLayer.resetStyle(e.target);
    }
}

// On each feature: Add popup and hover events
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });
    
    // The popup content is dynamically generated when opened to reflect current data
    layer.on('popupopen', function() {
        const name = feature.properties.NOM_MUN;
        const data = getMuniData(name);
        
        let covStr = 'Sin datos';
        let semStr = 'N/A';
        let dotColor = '#475569';
        
        if (data) {
            covStr = data.coverage_str;
            semStr = data.semaforo;
            dotColor = getColor(data.coverage);
        }

        const popupContent = `
            <div class="municipality-info">
                <h3>${name}</h3>
                <div class="stat">
                    <span class="stat-label">Cobertura:</span>
                    <span class="stat-value">${covStr}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Estado:</span>
                    <span class="stat-value"><span class="semaforo-dot" style="background: ${dotColor};"></span> ${semStr}</span>
                </div>
            </div>
        `;
        layer.setPopupContent(popupContent);
    });
    
    layer.bindPopup('Cargando...');
}

// Function to render/update the map
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

// Load both JSON files
Promise.all([
    fetch('municipios.json').then(res => res.json()),
    fetch('coverage_data.json').then(res => res.json())
]).then(results => {
    geojsonData = results[0];
    coverageData = results[1];
    
    updateMap();
    map.fitBounds(geojsonLayer.getBounds());
}).catch(error => {
    console.error('Error cargando los datos:', error);
});
