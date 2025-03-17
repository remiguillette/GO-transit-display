
# Scrolling Text Debug Documentation

## Issue Identified
- Multiple scrolling text containers appearing in the header and footer
- Duplicate scrolling text elements causing visual conflicts
- Black box artifacts appearing over elements

## Debug Locations
1. `/templates/base.html`: Contains footer scrolling text implementation
2. `/templates/display.html`: Contains header alert container
3. `/static/css/display.css`: Contains animation and container styles

## Error Patterns
- Console logs showing "Error updating alerts" due to missing /api/alerts endpoint
- 404 errors for alert API endpoints
- Duplicate WebSocket connections for alerts

## Solution Applied
1. Removed duplicate scrolling containers
2. Cleaned up conflicting CSS styles
3. Consolidated alert containers into single implementation
4. Removed redundant footer elements

## Future Reference
- Keep single source for scrolling text
- Verify WebSocket connections aren't duplicated
- Check alert API endpoint implementation
- Monitor for style conflicts in overlays
