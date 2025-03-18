
// Function to update scrolling text
function updateScrollingText(alerts) {
    const container = document.getElementById('scrolling-container');
    if (!container) return;

    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
        return;
    }

    const alertsText = alerts.map(alert => alert.text).join(' • ');
    container.innerHTML = `<div class="scrolling-text">${alertsText}</div>`;
}

// Initial fetch of alerts
fetch('/api/alerts')
    .then(response => response.json())
    .then(data => {
        console.log('Alerts data:', data);
        updateScrollingText(data.alerts);
    })
    .catch(err => {
        console.error('Error fetching alerts:', err);
        updateScrollingText([]);
    });
