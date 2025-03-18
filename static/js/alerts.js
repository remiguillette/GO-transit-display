
// Alert update handling
let lastUpdate = 0;
const updateInterval = 30000; // 30 seconds

function updateAlerts() {
    const now = Date.now();
    if (now - lastUpdate < updateInterval) {
        console.log("Skipping update - too soon since last update");
        return;
    }
    
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            if (data.alerts && data.alerts.length > 0) {
                const alert = data.alerts[0];
                document.getElementById('alert-message-en').textContent = alert.text || "No current alerts";
                document.getElementById('alert-message-fr').textContent = alert.text || "Aucune alerte en cours";
            } else {
                document.getElementById('alert-message-en').textContent = "Service operating normally";
                document.getElementById('alert-message-fr').textContent = "Service fonctionne normalement";
            }
            lastUpdate = now;
        })
        .catch(error => {
            console.error("Error updating alerts:", error);
        });
}

// Initialize SSE connection
function initializeSSE() {
    console.log("Initializing SSE connection...");
    const evtSource = new EventSource('/api/alerts/stream');
    
    evtSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.alerts && data.alerts.length > 0) {
            const alert = data.alerts[0];
            document.getElementById('alert-message-en').textContent = alert.text || "No current alerts";
            document.getElementById('alert-message-fr').textContent = alert.text || "Aucune alerte en cours";
        }
    };

    evtSource.onerror = function() {
        console.log("SSE connection error, retrying in 5 seconds...");
        evtSource.close();
        setTimeout(initializeSSE, 5000);
    };
}

// Initial update
updateAlerts();

// Set up periodic updates
setInterval(updateAlerts, updateInterval);

// Initialize SSE
initializeSSE();
