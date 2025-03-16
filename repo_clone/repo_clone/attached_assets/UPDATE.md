# GO Transit Display Board - Development Updates and Guidelines

## Current Implementation Status
- Real-time train departure tracking with demo data
- Bilingual interface (English/French)
- Station selection and display
- Responsive design for train station visibility
- Line icons with official GO Transit colors
- Large format display optimization
- Accessibility status indicators for platforms
- Color-coded status displays
- Polaris font family implementation
- SVG-based accessibility icons

## Key Display Guidelines

### Text Formatting and Capitalization
1. Capitalization Rules:
   - First letter of sentences: Capitalize (e.g., "Train departures")
   - Station names: Keep capitalized (e.g., "Union", "Barrie")
   - Headers: Capitalize first letter (e.g., "Scheduled", "Platform")
   - Status messages: Capitalize first letter ("On time", "Delayed", "Cancelled")
   - Line codes: Always uppercase in colored boxes (e.g., "BR", "LW")

2. Bilingual Elements:
   - Column headers bilingual with consistent capitalization
   - Status messages in English only
   - Train information displayed in both languages where applicable
   - First word capitalized in both languages

### Font Implementation
1. Font Files Required:
   - PolarisTrial-Bold.ttf
   - PolarisTrial-Medium.ttf
   - PolarisTrial-Light.ttf

2. Font Usage:
   - Headers and Important Text: Polaris Bold
   - Subheaders and Station Names: Polaris Medium
   - Body Text: Polaris Light
   - Time Display: Polaris Bold (with monospace fallback)

3. Font Size Guidelines:
   - Main Headers: 42px
   - Time Display: 48px
   - Schedule Text: 36px
   - Station Names: 36px minimum

### Icon Implementation
1. SVG Requirements:
   - Use SVG format for all icons (train, accessibility)
   - Ensure fill color is set to "#FFFFFF"
   - Remove any fill-rule or clip-rule attributes
   - Set proper viewBox for scaling
   - Include width and height attributes

2. Accessibility Icon:
   - Use SVG implementation instead of PNG
   - Set background color to #0052A5 (ADA blue)
   - Maintain 24x24px size
   - Use white fill color for icon
   - Position next to platform numbers

3. Line Icons:
   - Size: 36px x 36px
   - Border radius: 4px
   - Font: Polaris Bold, 22px
   - Letter spacing: -0.5px
   - 2px padding
   - Line height: 1 for vertical centering

### Status Indicators
1. Color Specifications:
   - Delayed status: Red (#ff0000) with blinking animation
   - Normal status: Green (#7db610)
   - Time display: Light yellow (#d5d695)

2. Platform Display:
   - Show platform number when on time
   - Display status message when delayed/cancelled
   - Include accessibility icon for accessible platforms

### Error Prevention
1. Common Issues:
   - Always use SVG for icons instead of PNG
   - Ensure proper font file paths in CSS
   - Maintain capitalization rules consistently
   - Use proper class names for styling

2. Image Handling:
   - Store SVG files in static/assets/
   - Use url_for() for file paths
   - Set explicit width/height attributes
   - Include descriptive alt text

## Technical Implementation

### Font Setup
```css
@font-face {
    font-family: 'Polaris Bold';
    src: url('../fonts/PolarisTrial-Bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
}
```

### SVG Icon Implementation
```html
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <path fill="#FFFFFF" d="[path_data]"/>
</svg>
```

### Directory Structure
```
├── static/
│   ├── assets/
│   │   └── accessibility-icon.svg
│   ├── css/
│   │   └── style.css
│   └── fonts/
│       ├── PolarisTrial-Bold.ttf
│       ├── PolarisTrial-Medium.ttf
│       └── PolarisTrial-Light.ttf
```

## Future Considerations
1. Database Integration:
   - PostgreSQL implementation pending
   - Will require proper migration strategy
   - Consider data persistence requirements

2. Real-time Data:
   - Currently using demo data
   - Future integration with GO Transit API needed
   - Consider fallback mechanisms for API failures
