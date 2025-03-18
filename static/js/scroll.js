
const SCROLL_SPEED = 50; // Lower = faster

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('scrolling-container');
            const scrollingText = document.createElement('div');
            scrollingText.className = 'scrolling-text';
            
            if (data && data.length > 0) {
                scrollingText.textContent = data.map(update => 
                    `${update.line}: ${update.status} - ${update.details}`).join(' • ');
            } else {
                scrollingText.textContent = 'GO Transit - All services operating normally';
            }
            
            container.innerHTML = '';
            container.appendChild(scrollingText);
        })
        .catch(error => {
            console.error("Error updating alerts:", error);
            const container = document.getElementById('scrolling-container');
            container.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
        });
}

updateAlerts();
setInterval(updateAlerts, 60000);
