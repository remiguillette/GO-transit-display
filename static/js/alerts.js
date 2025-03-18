const alertElement = document.getElementById('alert-message');

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
                        `<div class="alert-item ${index === 0 ? 'active' : ''}">${alert.text}</div>`
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