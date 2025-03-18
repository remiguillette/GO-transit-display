// Alert ticker functionality
function updateAlertTicker(alerts) {
    const tickerContent = document.querySelector('.ticker-content');
    if (!tickerContent) return;

    const alertText = Array.isArray(alerts) && alerts.length > 0
        ? alerts.map(alert => alert.text || 'Service operating normally').join(' • ')
        : ''; // Removed default message

    tickerContent.textContent = alertText;
    if (alertText) { //Only show if there is text
        tickerContent.style.display = 'block';
        tickerContent.style.animation = 'ticker 30s linear infinite';
    } else {
        tickerContent.style.display = 'none';
    }
}

// Fetch alerts every 30 seconds
function fetchAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            console.log('Alerts data:', data);
            updateAlertTicker(data.alerts);
        })
        .catch(err => {
            console.error('Error fetching alerts:', err);
            updateAlertTicker([]);
        });
}

// Initial fetch and setup interval
fetchAlerts();
setInterval(fetchAlerts, 30000);