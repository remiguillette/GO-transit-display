
const socket = io();
let lastUpdate = 0;
const updateThreshold = 1000; // 1 second

function updateScrollingText(alerts) {
    const container = document.getElementById('scrolling-container');
    if (!container) return;
    
    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<div class="scrolling-text">No current service alerts</div>';
        return;
    }

    const alertText = alerts.map(alert => alert.message).join(' • ');
    container.innerHTML = `<div class="scrolling-text">${alertText}</div>`;
}

socket.on('alerts', function(data) {
    const now = Date.now();
    if (now - lastUpdate < updateThreshold) {
        console.log("Skipping update - too soon since last update");
        return;
    }
    lastUpdate = now;
    updateScrollingText(data.alerts);
});

// Initial load
fetch('/api/alerts')
    .then(response => response.json())
    .then(data => {
        updateScrollingText(data.alerts);
    })
    .catch(error => {
        console.error('Error updating alerts:', error);
        updateScrollingText([]);
    });
