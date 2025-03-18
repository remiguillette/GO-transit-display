let currentAlertIndex = 0;
let alerts = [];

function showAlert() {
    const container = document.getElementById('scrolling-container');
    if (!container || alerts.length === 0) return;

    // Remove existing alerts
    const existingAlerts = container.querySelectorAll('.alert-text');
    existingAlerts.forEach(alert => {
        alert.classList.remove('active');
        alert.remove();
    });

    // Create new alert
    const alertText = document.createElement('div');
    alertText.className = 'alert-text';
    alertText.textContent = alerts[currentAlertIndex];
    container.appendChild(alertText);

    // Update index
    currentAlertIndex = (currentAlertIndex + 1) % alerts.length;
}

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            alerts = data;
            if (alerts.length === 0) {
                alerts = ['GO Transit - All services operating normally'];
            }
            showAlert();
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alerts = ['GO Transit - All services operating normally'];
            showAlert();
        });
}

// Initial update
updateAlerts();

// Update every 30 seconds
setInterval(updateAlerts, 30000);