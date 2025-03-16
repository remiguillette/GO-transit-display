# AI Assistant Guidelines for GO Transit Display Board

## Project Overview
This is a real-time display board application for GO Transit schedules. The application requires strict adherence to GO Transit's design guidelines, particularly regarding typography, iconography, and accessibility features.

## Key Implementation Guidelines

### Typography Implementation
1. Font Hierarchy:
   - ALWAYS use the Polaris font family
   - DO NOT fall back to system fonts except as last resort
   - MAINTAIN proper font weights and styles

2. Capitalization Rules:
   - ALWAYS capitalize first letter of sentences
   - PRESERVE station name capitalization
   - USE uppercase for line codes (BR, LW, etc.)
   - DO NOT force lowercase through CSS text-transform

### Icon Implementation
1. SVG Usage:
   - ALWAYS use SVG format for icons
   - ENSURE white fill color (#FFFFFF)
   - AVOID PNG or other bitmap formats
   - SET explicit width/height attributes

2. Common Pitfalls:
   - DON'T use PNG for accessibility icons
   - AVOID using background-image for icons
   - ENSURE proper viewBox attributes
   - MAINTAIN aspect ratios

### Error Prevention
1. Font Files:
   - VERIFY font file paths before implementation
   - CHECK font-face declarations
   - ENSURE all required weights are included
   - TEST font loading in different contexts

2. Icon Display:
   - VALIDATE SVG markup
   - CHECK fill colors
   - VERIFY icon positioning
   - TEST accessibility features

### User Interaction
1. Language Handling:
   - MAINTAIN bilingual interface
   - ENSURE proper capitalization in both languages
   - PRESERVE station names exactly as provided
   - RESPECT language-specific formatting

2. Status Updates:
   - IMPLEMENT real-time updates
   - HANDLE delayed status properly
   - SHOW accessibility information clearly
   - MAINTAIN color coding standards

## Common User Requests and Solutions

### Font Issues
```markdown
User: "The font doesn't look right"
Solution: 
1. Check font file paths in static/fonts/
2. Verify @font-face declarations
3. Ensure proper font-family assignments
4. Test fallback fonts
```

### Icon Problems
```markdown
User: "Icons are not showing/broken"
Solution:
1. Convert to SVG format
2. Set proper fill colors
3. Include width/height attributes
4. Use inline SVG or proper asset paths
```

### Capitalization Fixes
```markdown
User: "Text capitalization is wrong"
Solution:
1. Remove text-transform: lowercase
2. Implement proper capitalization in HTML
3. Preserve station name formatting
4. Follow GO Transit guidelines
```

## Testing Guidelines

### Visual Verification
1. Font Display:
   - Check all text elements use Polaris
   - Verify proper weights and styles
   - Ensure correct sizing
   - Validate capitalization rules

2. Icon Rendering:
   - Verify SVG display
   - Check color consistency
   - Validate accessibility icons
   - Test responsive behavior

### Functionality Testing
1. Real-time Updates:
   - Verify schedule refreshes
   - Check status changes
   - Test station switching
   - Validate bilingual display

2. Accessibility Features:
   - Test screen reader compatibility
   - Verify platform indicators
   - Check color contrast
   - Validate icon alternative text

## Response Templates

### Font Implementation
```css
@font-face {
    font-family: 'Polaris Bold';
    src: url('../fonts/PolarisTrial-Bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
}
```

### SVG Icon Template
```html
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <path fill="#FFFFFF" d="[path_data]"/>
</svg>
```

## Final Notes
- Always test changes thoroughly before committing
- Maintain consistent code style
- Follow GO Transit brand guidelines strictly
- Prioritize accessibility features
