const alertElement = document.getElementById('alert-message');

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
                alertElement.innerHTML = '<div class="alert-carousel"><div class="alert-item active">GO Transit - All services operating normally</div></div>';
                return;
            }

            const alerts = data.alerts;
            if (alerts.length === 0) {
                alertElement.innerHTML = '<div class="alert-carousel"><div class="alert-item active">GO Transit - All services operating normally</div></div>';
            } else {
                alertElement.innerHTML = '<div class="alert-carousel">' + 
                    alerts.map((alert, index) => 
                        `<div class="alert-item ${index === 0 ? 'active' : ''}">${cleanAlertText(alert.text)}</div>`
                    ).join('') + '</div>';

                if (alerts.length > 1) {
                    rotateAlerts();
                }
            }
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alertElement.innerHTML = '<div class="alert-carousel"><div class="alert-item active">GO Transit - All services operating normally</div></div>';
        });
}

let currentAlertIndex = 0;
function rotateAlerts() {
    setInterval(() => {
        const items = document.querySelectorAll('.alert-item');
        if (items.length <= 1) return;

        items[currentAlertIndex].classList.remove('active');
        currentAlertIndex = (currentAlertIndex + 1) % items.length;
        items[currentAlertIndex].classList.add('active');
    }, 5000);
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