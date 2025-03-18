
const SCROLL_SPEED = 50; // Lower = faster

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('scrolling-container');
            container.innerHTML = '';

            const scrollingText = document.createElement('div');
            scrollingText.className = 'scrolling-text';

            // Check if data is an array (the format returned by get_go_transit_updates)
            if (Array.isArray(data) && data.length > 0) {
                scrollingText.textContent = data.join(' • ');
            } else {
                scrollingText.textContent = 'GO Transit - No Service Updates';
            }

            container.appendChild(scrollingText);
        })
        .catch(error => {
            console.log('Error updating alerts:', error);
            const container = document.getElementById('scrolling-container');
            container.innerHTML = '<div class="scrolling-text">GO Transit - No Service Updates</div>';
        });
}

// Initial update
updateAlerts();

// Update every minute
setInterval(updateAlerts, 60000);
