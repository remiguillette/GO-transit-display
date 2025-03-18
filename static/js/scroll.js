let currentAlertIndex = 0;
let alerts = [];

function showNextAlert() {
    const container = document.getElementById('scrolling-container');
    if (!container || alerts.length === 0) return;

    // Remove existing alert
    const oldAlert = container.querySelector('.scrolling-text');
    if (oldAlert) {
        oldAlert.classList.remove('active');
        setTimeout(() => oldAlert.remove(), 500);
    }

    // Create new alert
    const scrollingText = document.createElement('div');
    scrollingText.className = 'scrolling-text';

    const alert = alerts[currentAlertIndex];

    const englishText = document.createElement('div');
    englishText.className = 'scrolling-text-en';
    englishText.textContent = alert;

    scrollingText.appendChild(englishText);
    container.appendChild(scrollingText);

    // Trigger fade in
    setTimeout(() => scrollingText.classList.add('active'), 50);

    // Update index
    currentAlertIndex = (currentAlertIndex + 1) % alerts.length;
}

function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('scrolling-container');
            if (!container) return;

            container.innerHTML = '';
            const scrollingText = document.createElement('div');
            scrollingText.className = 'scrolling-text active';

            if (Array.isArray(data) && data.length > 0 && data[0] !== "GO Transit - All services operating normally") {
                alerts = data.map(alert => {
                    if (typeof alert === 'string' && alert.includes('Started') && alert.includes('Until')) {
                        return alert.replace(/Started|Until/g, (match) => ` ${match} `);
                    }
                    return alert;
                });
                const alert = alerts[currentAlertIndex];

                const englishText = document.createElement('div');
                englishText.className = 'scrolling-text-en';
                englishText.textContent = alert;

                scrollingText.appendChild(englishText);

            } else {
                scrollingText.textContent = 'GO Transit - All services operating normally';
            }

            container.appendChild(scrollingText);
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            const container = document.getElementById('scrolling-container');
            if (container) {
                container.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
            }
        });
}

// Initial update
updateAlerts();

// Update every 30 seconds
setInterval(updateAlerts, 30000);