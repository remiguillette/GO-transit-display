
const alertElement = document.getElementById('alert-message');

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            if (data.alerts && data.alerts.length > 0) {
                alertElement.textContent = data.alerts[0].text;
            } else {
                alertElement.textContent = 'GO Transit - All services operating normally';
            }
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alertElement.textContent = 'GO Transit - All services operating normally';
        });
}

// Update alerts every 30 seconds
setInterval(updateAlerts, 30000);
updateAlerts();
let currentAlertIndex = 0;
let alerts = [];

function updateAlerts(data) {
    alerts = data.alerts || [];
    const alertText = document.getElementById('alert-message');
    
    if (alerts.length === 0) {
        alertText.innerHTML = '<div class="alert-carousel"><div class="alert-item active">GO Transit - All services operating normally</div></div>';
        return;
    }

    // Create carousel HTML
    alertText.innerHTML = '<div class="alert-carousel">' + 
        alerts.map((alert, index) => 
            `<div class="alert-item ${index === 0 ? 'active' : ''}">${alert.text}</div>`
        ).join('') + '</div>';

    // Start rotation if more than one alert
    if (alerts.length > 1) {
        rotateAlerts();
    }
}

function rotateAlerts() {
    setInterval(() => {
        if (alerts.length <= 1) return;
        
        const items = document.querySelectorAll('.alert-item');
        items[currentAlertIndex].classList.remove('active');
        
        currentAlertIndex = (currentAlertIndex + 1) % alerts.length;
        items[currentAlertIndex].classList.add('active');
    }, 5000); // Rotate every 5 seconds
}

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
