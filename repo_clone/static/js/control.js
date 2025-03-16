// Global variables
let socket = null;
let lastUpdateTime = 0;
const MIN_UPDATE_INTERVAL = 3000; // 3 seconds minimum between updates

// Initialize WebSocket connection
function initializeWebSocket() {
    try {
        socket = io();
        
        socket.on('connect', () => {
            console.log('Control panel connected to WebSocket');
            showStatus('Connected to server', 'success');
        });
        
        socket.on('connect_error', error => {
            console.error('WebSocket connection error:', error);
            showStatus('Connection error', 'error');
        });
        
        socket.on('disconnect', () => {
            console.log('WebSocket disconnected');
            showStatus('Disconnected from server', 'warning');
        });
    } catch (error) {
        console.error('Error initializing WebSocket:', error);
        showStatus('Unable to initialize connection', 'error');
    }
}

// Check if enough time has passed to allow an update
function canUpdate() {
    const now = Date.now();
    return (now - lastUpdateTime) >= MIN_UPDATE_INTERVAL;
}

// Display status message
function showStatus(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Update station with rate limiting
async function updateStation(station) {
    if (!canUpdate()) {
        console.log('Skipping update - too soon since last update');
        showStatus('Please wait before submitting again', 'warning');
        return false;
    }
    
    try {
        const response = await fetch('/api/set_station', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `station=${encodeURIComponent(station)}`
        });

        if (!response.ok) {
            if (response.status === 429) {
                showStatus('Rate limit exceeded. Please wait a moment before trying again.', 'error');
                return false;
            }
            throw new Error('Failed to update station');
        }

        const result = await response.json();
        if (result.status === 'success') {
            // Update current station display
            const statusElement = document.getElementById('current-station');
            if (statusElement) {
                statusElement.textContent = station;
            }
            
            showStatus('Remote display updated successfully!', 'success');
            lastUpdateTime = Date.now();
            return true;
        } else {
            throw new Error(result.message || 'Failed to update station');
        }
    } catch (error) {
        console.error('Error:', error);
        showStatus('Failed to update station. Please try again.', 'error');
        return false;
    }
}

// Initialize control panel
function initializeControlPanel() {
    // Initialize WebSocket
    initializeWebSocket();
    
    // Handle form submission with AJAX and rate limiting
    document.getElementById('station-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const stationSelect = document.getElementById('station-select');
        const station = stationSelect.value;
        
        // Attempt to update station
        await updateStation(station);
    });
}

// Start control panel when page loads
document.addEventListener('DOMContentLoaded', initializeControlPanel);
