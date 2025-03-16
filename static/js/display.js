// Update clock with HH:MM:SS format
function updateClock() {
    const now = new Date();
    const timeElem = document.getElementById('currentTime');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    timeElem.textContent = `${hours}:${minutes}:${seconds}`;
}

// Accessibility icon SVG
const accessibilityIcon = `
<span class="accessibility-icon">
    <svg width="24" height="24" viewBox="0 0 24 24">
        <path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm7 18v-2h-3v-5.604c0-.757-.615-1.373-1.372-1.373H9.372C8.615 11.023 8 11.639 8 12.396V18H5v2h14zM9.5 18v-5h5v5h-5z"/>
    </svg>
</span>`;

// Update schedules
async function updateSchedules() {
    try {
        const stationName = document.querySelector('.station-name').textContent.split('-')[0].trim();
        const response = await fetch(`/api/schedules?station=${encodeURIComponent(stationName)}`);

        if (!response.ok) {
            throw new Error('Failed to fetch schedules');
        }

        const schedules = await response.json();
        const container = document.getElementById('scheduleRows');
        container.innerHTML = '';

        schedules.forEach(schedule => {
            const row = document.createElement('div');
            row.className = 'schedule-row';

            const statusClass = schedule.status.toLowerCase() === 'delayed' 
                ? 'status-delayed' 
                : schedule.status.toLowerCase() === 'cancelled' 
                    ? 'status-cancelled' 
                    : '';

            // Format the train info with route code span
            const [routeCode, ...destinationParts] = schedule.train.split(' ');
            
            // Route code colored span
            const routeCodeSpan = `<span class="route-code" style="background-color: ${schedule.color}">${routeCode}</span>`;
            
            row.innerHTML = `
                <div class="col-scheduled">${schedule.departure}</div>
                <div class="col-to">
                    ${routeCodeSpan}
                    ${schedule.destination}
                </div>
                <div class="col-stop">
                    ${destinationParts.join(' ')}
                </div>
                <div class="col-platform ${statusClass}">
                    ${schedule.status} ${schedule.accessible ? accessibilityIcon : ''}
                </div>
            `;
            container.appendChild(row);
        });
    } catch (error) {
        console.error('Error updating schedules:', error);
        const container = document.getElementById('scheduleRows');
        container.innerHTML = `
            <div role="alert">
                Unable to load schedule data. Please try again later.
            </div>
        `;
    }
}

// Language toggle
async function toggleLanguage() {
    try {
        const currentLang = document.documentElement.lang;
        const newLang = currentLang === 'en' ? 'fr' : 'en';

        const response = await fetch('/api/set_language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `language=${newLang}`
        });

        if (response.ok) {
            window.location.reload();
        }
    } catch (error) {
        console.error('Error toggling language:', error);
    }
}

// Initialize display
setInterval(updateClock, 1000);
setInterval(updateSchedules, 30000); // Update every 30 seconds
updateClock();
updateSchedules();