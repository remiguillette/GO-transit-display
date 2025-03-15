document.getElementById('stationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const station = document.getElementById('stationSelect').value;
    
    try {
        const response = await fetch('/api/set_station', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `station=${encodeURIComponent(station)}`
        });

        if (!response.ok) {
            throw new Error('Failed to update station');
        }

        const result = await response.json();
        if (result.status === 'success') {
            alert('Station updated successfully');
        } else {
            throw new Error(result.message || 'Failed to update station');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update station. Please try again.');
    }
});
