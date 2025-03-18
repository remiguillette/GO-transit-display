
let currentAlertIndex = 0;
let alerts = [];

function showAlert() {
    const container = document.getElementById('scrolling-container');
    if (!container || alerts.length === 0) return;

    // Remove existing alerts
    container.innerHTML = '';

    // Create new alert
    const alertText = document.createElement('div');
    alertText.className = 'alert-text';
    alertText.textContent = alerts[currentAlertIndex];
    container.appendChild(alertText);

    // Animate the alert
    alertText.style.animation = 'fadeInOut 5s ease-in-out';

    // Update index for next alert
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
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alerts = ['GO Transit - All services operating normally'];
        });
}

// Initial update
updateAlerts();

// Update alerts data every 30 seconds
setInterval(updateAlerts, 30000);

// Rotate display every 5 seconds
setInterval(showAlert, 5000);

// Show first alert immediately
setTimeout(showAlert, 100);
