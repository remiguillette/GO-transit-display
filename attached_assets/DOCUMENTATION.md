# GO Transit Information Display - Documentation

This document provides detailed information about the GO Transit Information Display application, with a focus on the scrolling information bar and other key components.

## Table of Contents

1. [System Overview](#system-overview)
2. [Display Components](#display-components)
3. [Scrolling Information Bar](#scrolling-information-bar)
4. [Fullscreen Mode](#fullscreen-mode)
5. [Data Sources](#data-sources)
6. [Customization Guide](#customization-guide)

## System Overview

The GO Transit Information Display is a standalone web application designed to simulate a transit information board. It shows:

- Real-time clock
- GO Transit network information
- Service updates for different train lines
- A scrolling information bar for important alerts

The application is designed to run in fullscreen mode on dedicated display hardware like a Raspberry Pi or Arduino-controlled screen.

## Display Components

### Header Section
- GO Transit logo
- Real-time clock display
- Last updated timestamp

### Main Content
- Table displaying all GO Transit train lines
- Status information for each line
- Details about service changes or disruptions

### Footer
- Scrolling information bar highlighting important service alerts

## Scrolling Information Bar

The scrolling information bar (also known as a "ticker" or "marquee") is implemented using CSS animations and JavaScript. Here's how it works:

### HTML Structure

```html
<footer class="board-footer">
  <div id="scrolling-container" class="scrolling-container">
    <!-- The scrolling text will be inserted here -->
  </div>
</footer>
```

### CSS Styling

```css
.board-footer {
  background-color: #111;
  border-top: 2px solid #097F5C;
  height: 2.5rem;
  overflow: hidden;
}

.scrolling-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.scrolling-text {
  color: #ffeb3b;
  font-weight: bold;
  position: absolute;
  white-space: nowrap;
  padding: 0.5rem 0;
  font-size: 1.1rem;
}
```

### JavaScript Implementation

The scrolling effect is created using CSS transitions controlled by JavaScript. The key functions are:

1. **Setup Function**: Creates the scrolling text content from important service updates
```javascript
function setupScrollingText(updates) {
  // Filter for important updates (delays, cancellations, etc.)
  const importantUpdates = updates.filter(update => {
    const status = update.status.toLowerCase();
    const details = update.details.toLowerCase();
    return status.includes('delay') || 
           status.includes('cancel') || 
           details.includes('delay') || 
           details.includes('cancel') ||
           details.includes('emergency');
  });

  if (importantUpdates.length === 0) {
    // If no important updates, show a default message
    scrollingContainer.innerHTML = '<div class="scrolling-text">GO Transit - All services operating normally</div>';
  } else {
    // Create scrolling text for important updates
    const scrollText = importantUpdates.map(update => 
      `${update.line}: ${update.status} - ${update.details}`
    ).join(' • ');
    
    scrollingContainer.innerHTML = `<div class="scrolling-text">${escapeHtml(scrollText)}</div>`;
  }

  // Start the scrolling animation
  startScrolling();
}
```

2. **Animation Start Function**: Calculates the animation duration based on text length and starts the animation
```javascript
function startScrolling() {
  if (isScrolling) return;
  
  const scrollingText = document.querySelector('.scrolling-text');
  if (!scrollingText) return;
  
  // Set initial position (offscreen to the right)
  scrollingText.style.transform = 'translateX(100%)';
  
  // Calculate duration based on text length for consistent speed
  const textWidth = scrollingText.offsetWidth;
  const containerWidth = scrollingContainer.offsetWidth;
  const totalDistance = textWidth + containerWidth;
  const duration = totalDistance * SCROLL_SPEED; // ms
  
  // Set the animation (CSS transition)
  scrollingText.style.transition = `transform ${duration}ms linear`;
  
  // Start the animation after a small delay
  setTimeout(() => {
    // Move text from right to left (beyond the left edge)
    scrollingText.style.transform = `translateX(-${textWidth}px)`;
    isScrolling = true;
    
    // Reset the animation when it completes
    scrollingText.addEventListener('transitionend', resetScrolling);
  }, 100);
}
```

3. **Animation Reset Function**: Resets the animation to create a continuous loop effect
```javascript
function resetScrolling() {
  const scrollingText = document.querySelector('.scrolling-text');
  if (!scrollingText) return;
  
  // Remove the transition temporarily to avoid visible reset
  scrollingText.style.transition = 'none';
  
  // Reset to initial position (off-screen right)
  scrollingText.style.transform = 'translateX(100%)';
  
  // Force a reflow (repaint) to ensure the style change takes effect immediately
  scrollingText.offsetHeight;
  
  // Remove this event listener to avoid duplicates
  scrollingText.removeEventListener('transitionend', resetScrolling);
  
  // Restart the scrolling after a short delay
  setTimeout(startScrolling, 1000);
  isScrolling = false;
}
```

### How to Customize the Scrolling Bar

To modify the scrolling information bar:

1. **Speed**: Adjust the `SCROLL_SPEED` constant at the top of `web-renderer.js` (lower values = faster scrolling)
2. **Appearance**: Modify the CSS styles for `.scrolling-text` in `styles.css`
3. **Content**: Update the filtering logic in `setupScrollingText()` to show different types of messages

## Fullscreen Mode

The display automatically enters fullscreen mode when loaded. This is implemented using the Fullscreen API:

```javascript
function enableFullscreen() {
  // Only try a limited number of times to avoid infinite loops
  if (fullscreenAttempts >= MAX_FULLSCREEN_ATTEMPTS) return;
  
  // Don't attempt if already in fullscreen
  if (document.fullscreenElement) return;
  
  const docElement = document.documentElement;
  
  try {
    // Try to request fullscreen using various browser prefixes
    if (docElement.requestFullscreen) {
      docElement.requestFullscreen();
    } else if (docElement.mozRequestFullScreen) { // Firefox
      docElement.mozRequestFullScreen();
    } else if (docElement.webkitRequestFullscreen) { // Chrome, Safari, Opera
      docElement.webkitRequestFullscreen();
    } else if (docElement.msRequestFullscreen) { // IE/Edge
      docElement.msRequestFullscreen();
    }
  } catch (error) {
    console.error('Fullscreen error:', error);
  }
}
```

### Running in Kiosk Mode

For Raspberry Pi setups, you can use one of these approaches to launch the browser in kiosk mode:

#### Chromium (Raspberry Pi):
```bash
chromium-browser --kiosk --disable-restore-session-state --noerrdialogs --disable-session-crashed-bubble http://localhost:5000
```

#### Firefox (Raspberry Pi):
```bash
firefox --kiosk http://localhost:5000
```

## Data Sources

The display uses preset GO Transit data that's stored in `server.js`. The data provides accurate information about:

- All current GO Transit train lines
- Realistic service statuses
- Construction updates and notices

The server provides this data through a simple API endpoint at `/api/service-updates`.

## Customization Guide

### Adding or Modifying Transit Lines

To add or modify transit lines, edit the `generateGoTransitInfo()` function in `server.js`:

```javascript
function generateGoTransitInfo() {
  return [
    // Example of adding a new line:
    {
      line: "New Transit Line",
      status: "Normal Service",
      details: "Trains operating on schedule"
    },
    // ... existing lines ...
  ];
}
```

### Color Scheme

The color scheme can be customized by editing the CSS variables in `styles.css`. The main colors used are:

- Background: Black (#000)
- GO Transit Green: #097F5C
- Normal Status: #4caf50 (green)
- Delay Status: #ff6b6b (red)
- Alert Text: #ffeb3b (yellow)

### Refresh Rate

The display refreshes service information every 5 minutes by default. To change this, modify the `REFRESH_INTERVAL` constant in `web-renderer.js`:

```javascript
// Change from 5 minutes to your desired interval (in milliseconds)
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes
```

## Conclusion

This documentation provides a comprehensive guide to understanding and customizing the GO Transit Information Display. The scrolling information bar and fullscreen mode are key features that create an authentic transit board experience.

For any further questions or support, please refer to the source code comments or create issues in the project repository.