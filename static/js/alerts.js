const alertElementEn = document.getElementById('alert-message-en');
const alertElementFr = document.getElementById('alert-message-fr');

function cleanAlertText(text) {
    // Remove date/time patterns
    text = text.replace(/Started.*?(?=Until|$)/i, '');
    text = text.replace(/Until.*?(?=\n|$)/i, '');
    text = text.replace(/\d{1,2}:\d{2}\s*(?:AM|PM)/gi, '');
    text = text.replace(/(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}/gi, '');

    // Clean up any remaining artifacts
    text = text.replace(/\s+/g, ' ').trim();
    text = text.replace(/\s*https?:\/\/\S+/g, ''); // Remove URLs

    // If text starts with "Service alert:", keep it, otherwise add "Service alert:" if it's not a service adjustment
    if (!text.toLowerCase().includes('service adjustment')) {
        text = text.startsWith('Service alert:') ? text : 'Service alert: ' + text;
    }

    return text;
}

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            if (!data || !data.alerts) {
                alertElementEn.textContent = 'GO Transit - All services operating normally';
                alertElementFr.textContent = 'GO Transit - Tous les services fonctionnent normalement';
                return;
            }

            const alerts = data.alerts;
            if (alerts.length === 0) {
                alertElementEn.textContent = 'GO Transit - All services operating normally';
                alertElementFr.textContent = 'GO Transit - Tous les services fonctionnent normalement';
            } else {
                const enAlerts = alerts.map(alert => cleanAlertText(alert.text));
                const frAlerts = alerts.map(alert => alert.fr || ''); //Handle missing translations gracefully

                alertElementEn.textContent = enAlerts.join(' • ');
                alertElementFr.textContent = frAlerts.join(' • ');
            }
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alertElementEn.textContent = 'GO Transit - All services operating normally';
            alertElementFr.textContent = 'GO Transit - Tous les services fonctionnent normalement';
        });
}


// Update alerts every 30 seconds
setInterval(updateAlerts, 30000);
updateAlerts();

// Setup SSE connection for alerts
const alertsSource = new EventSource('/api/alerts/stream');
alertsSource.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        updateAlerts(data);
    } catch (error) {
        console.error('Error updating alerts:', error);
    }
};