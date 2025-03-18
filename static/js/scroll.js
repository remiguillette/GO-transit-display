const SCROLL_SPEED = 50; // Lower = faster
let isScrolling = false;

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('scrolling-container');
            if (data && data.length > 0) {
                container.innerHTML = data.map(update => `${update.line}: ${update.status} - ${update.details}`).join(' • ');
            } else {
                container.innerHTML = 'GO Transit - All services operating normally';
            }
        })
        .catch(error => {
            console.error("Error updating alerts:", error);
            const container = document.getElementById('scrolling-container');
            container.innerHTML = 'GO Transit - All services operating normally';
        });
}

// Initialize and refresh every minute
updateAlerts();
setInterval(updateAlerts, 60000);