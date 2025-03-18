
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
