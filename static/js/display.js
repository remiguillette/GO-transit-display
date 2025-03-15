// Update clock with HH:MM:SS format
function updateClock() {
    const now = new Date();
    const timeElem = document.getElementById('currentTime');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    timeElem.textContent = `${hours}:${minutes}:${seconds}`;
}

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

            row.innerHTML = `
                <div class="col-scheduled">${schedule.departure}</div>
                <div class="col-to">${schedule.destination}</div>
                <div class="col-stop">${schedule.train}</div>
                <div class="col-platform ${statusClass}">${schedule.status}</div>
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