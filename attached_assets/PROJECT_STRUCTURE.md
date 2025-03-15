# GO Transit Display Board - Project Structure

## Essential Files and Directories

### Root Directory
- `main.py` - Main Flask application entry point
- `scraper.py` - GO Transit schedule data handling and demo data generation
- `pyproject.toml` - Python project dependencies
- `.replit` - Replit configuration and workflow definitions
- `UPDATE.md` - Implementation guidelines and current status
- `AI_GUIDELINES.md` - AI assistant guidelines for development
- `PROJECT_STRUCTURE.md` - This file, documenting project organization

### /static
#### /assets
- `accessibility-icon.svg` - Accessibility icon in SVG format
- `.gitkeep` - Placeholder for git

#### /css
- `style.css` - Main stylesheet with typography, layout, and colors

#### /fonts
- `PolarisTrial-Bold.ttf` - GO Transit brand font (Bold)
- `PolarisTrial-Medium.ttf` - GO Transit brand font (Medium)
- `PolarisTrial-Light.ttf` - GO Transit brand font (Light)
- `.gitkeep` - Placeholder for git

### /templates
- `index.html` - Main display board template
- `control.html` - Station control interface
- `schedule_partial.html` - Schedule display partial template

## Implementation Notes

### Typography
- Fonts are properly loaded using @font-face
- Polaris font family implementation across all elements
- Capitalization rules follow GO Transit guidelines

### SVG Icons
- Icons use pure SVG with proper fill colors
- Train icon and accessibility icon implementations
- White fill color (#FFFFFF) for consistency

### Station Data
- Demo data generation with realistic schedules
- Proper station and line code mappings
- Accessibility information for platforms

### Styling
- GO Transit official colors
- Responsive grid layouts
- Status indicators with animations
- Accessibility-focused design

## Known Issues and Solutions
1. Image Display:
   - Use SVG format instead of PNG
   - Ensure proper path references
   - Maintain fill colors in SVGs

2. Typography:
   - Verify font file paths
   - Use proper font weights
   - Follow capitalization rules

3. Icon Implementation:
   - Use inline SVG where possible
   - Set explicit dimensions
   - Maintain proper aspect ratios

## Project Requirements
- Python 3.11+
- Flask web framework
- PostgreSQL (for future implementation)
- Required Python packages listed in pyproject.toml

## Future Considerations
1. Database Integration:
   - PostgreSQL implementation planned
   - Data persistence strategy
   - Migration planning

2. Real-time Data:
   - GO Transit API integration pending
   - Fallback mechanisms needed
   - Error handling improvements

## Archive Contents Checklist
- [ ] All source code files
- [ ] Configuration files
- [ ] Static assets and fonts
- [ ] Templates
- [ ] Documentation files
- [ ] Font licenses and attribution
