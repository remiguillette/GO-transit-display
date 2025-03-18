
let currentAlertIndex = 0;
let alerts = [];

function showAlert() {
    const container = document.getElementById('scrolling-container');
    if (!container || alerts.length === 0) {
        container.textContent = 'GO Transit - All services operating normally';
        return;
    }

    // Remove existing alerts
    container.innerHTML = '';

    // Create new alert with fade effect
    const alertText = document.createElement('div');
    alertText.className = 'alert-text';
    alertText.textContent = alerts[currentAlertIndex].text;
    container.appendChild(alertText);

    // Update index for next alert
    currentAlertIndex = (currentAlertIndex + 1) % alerts.length;
}

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            alerts = data;
            if (alerts.length === 0) {
                alerts = [{ text: 'GO Transit - All services operating normally' }];
            }
            showAlert();
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alerts = [{ text: 'GO Transit - All services operating normally' }];
            showAlert();
        });
}

// Initial update
updateAlerts();

// Update alerts data every 30 seconds
setInterval(updateAlerts, 30000);

// Rotate display every 5 seconds
setInterval(showAlert, 5000);
