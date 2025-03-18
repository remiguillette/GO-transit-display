
const SCROLL_SPEED = 50; // Lower = faster

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('scrolling-container');
            container.innerHTML = '';

            const scrollingText = document.createElement('div');
            scrollingText.className = 'scrolling-text';

            if (Array.isArray(data) && data.length > 0) {
                const formattedAlerts = data.map(alert => {
                    if (typeof alert === 'string' && alert.includes('Started') && alert.includes('Until')) {
                        return alert.replace(/Started|Until/g, (match) => ` ${match} `);
                    }
                    return alert;
                });
                scrollingText.textContent = formattedAlerts.join(' • ');
            } else {
                scrollingText.textContent = 'GO Transit - All services operating normally';
            }

            container.appendChild(scrollingText);
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            const container = document.getElementById('scrolling-container');
            container.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
        });
}

// Initial update
updateAlerts();

// Update every 30 seconds instead of 60
setInterval(updateAlerts, 30000);

// Initial update
updateAlerts();

// Update every minute
setInterval(updateAlerts, 60000);
