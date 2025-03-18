
// Initialize socket connection
let socket = io();

// Function to update scrolling text
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

// Fetch alerts on page load
fetch('/api/alerts')
    .then(response => response.json())
    .then(data => updateScrollingText(data.alerts))
    .catch(err => {
        console.error('Error fetching alerts:', err);
        updateScrollingText([]);
    });

// Listen for real-time alert updates
socket.on('alerts_update', (data) => {
    updateScrollingText(data.alerts);
});
