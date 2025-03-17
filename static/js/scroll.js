
const SCROLL_SPEED = 50; // Lower = faster
let isScrolling = false;

function setupScrollingText() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(updates => {
            const scrollingContainer = document.getElementById('scrolling-container');
            if (!updates || updates.length === 0) {
                scrollingContainer.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
            } else {
                const scrollText = updates.map(update => 
                    `${update.line}: ${update.status} - ${update.details}`
                ).join(' • ');
                scrollingContainer.innerHTML = `<div class="scrolling-text">${scrollText}</div>`;
            }
        })
        .catch(error => {
            console.error('Error updating alerts:', error);
            const scrollingContainer = document.getElementById('scrolling-container');
            scrollingContainer.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
        });
}

// Initialize and refresh every minute
setupScrollingText();
setInterval(setupScrollingText, 60000);
