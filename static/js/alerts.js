const socket = io();

let currentAlertIndex = 0;
let alerts = [];

function updateScrollingText(alerts) {
    const container = document.getElementById('scrolling-container');
    if (!container) return;

    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
        return;
    }

    const alertText = alerts.map(alert => 
        `${alert.line}: ${alert.status} - ${alert.details}`
    ).join(' • ');

    container.innerHTML = `<div class="scrolling-text">${alertText}</div>`;
}


socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('alerts_update', (data) => {
    updateScrollingText(data.alerts);
});

// Initial fetch of alerts (fallback if socket is unavailable)
fetch('/api/alerts')
    .then(response => response.json())
    .then(data => updateScrollingText(data.alerts))
    .catch(err => console.error('Error updating alerts:', err));


//setInterval(showAlert, 5000); // Removed as it conflicts with real-time updates