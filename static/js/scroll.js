let currentAlertIndex = 0;
let alerts = [];

function showNextAlert() {
    const container = document.getElementById('scrolling-container');
    if (!container || alerts.length === 0) return;

    // Remove all existing alerts first
    const existingAlerts = container.querySelectorAll('.scrolling-text');
    existingAlerts.forEach(alert => {
        alert.classList.remove('active');
        alert.remove();
    });

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

// Add alerts update function
function updateAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            alerts = data;
            if (alerts.length === 0) {
                alerts = ['GO Transit - All services operating normally'];
            }
            showNextAlert();
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            alerts = ['GO Transit - All services operating normally'];
            showNextAlert();
        });
}

// Initial update
updateAlerts();

// Update every 30 seconds
setInterval(updateAlerts, 30000);
function updateAlertText(text) {
    const container = document.getElementById('alert-container');
    if (!container) return;
    
    container.innerHTML = `<div class="alert-text">${text || 'Welcome to GO Transit'}</div>`;
}

// Initialize with default text
document.addEventListener('DOMContentLoaded', () => {
    updateAlertText();
});

// Update text when alerts are received
fetch('/api/alerts')
    .then(response => response.json())
    .then(data => {
        if (data && data.length > 0) {
            updateAlertText(data[0]);
        }
    })
    .catch(() => {
        updateAlertText('Welcome to GO Transit');
    });

// Update every 30 seconds
setInterval(() => {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                updateAlertText(data[0]);
            }
        })
        .catch(() => {});
}, 30000);
