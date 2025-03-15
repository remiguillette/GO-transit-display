// Update clock
function updateClock() {
    const now = new Date();
    const timeElem = document.getElementById('currentTime');
    timeElem.textContent = now.toLocaleTimeString();
}

// Update schedules
async function updateSchedules() {
    try {
        const station = document.getElementById('stationName').textContent;
        const response = await fetch(`/api/schedules?station=${encodeURIComponent(station)}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch schedules');
        }

        const schedules = await response.json();
        const container = document.getElementById('scheduleRows');
        container.innerHTML = '';

        schedules.forEach(schedule => {
            const row = document.createElement('div');
            row.className = 'schedule-row';
            row.innerHTML = `
                <div class="col-train">${schedule.train}</div>
                <div class="col-destination">${schedule.destination}</div>
                <div class="col-time">${schedule.departure}</div>
                <div class="col-status">${schedule.status}</div>
                <div class="col-track">${schedule.track}</div>
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
setInterval(updateSchedules, 60000);
updateClock();
updateSchedules();
