
# GO Transit Display Board

A Flask-based GO Transit display board application showing real-time train departures with proper branding and accessibility features.

## Features

- Real-time train schedule display
- GO Transit branded interface with Polaris typography
- Bilingual support (English/French)
- Accessibility-compliant design
- Mobile-responsive layout with precise measurements
- Station selection control panel
- WebSocket-based real-time updates

## Layout Structure

### Display Board (/):
- Fixed header (6rem height)
- Real-time clock display (3rem font)
- Grid-based schedule display
- Responsive columns (4-column grid)
- Station name display (2.625rem font)

### Control Panel (/control):
- Centered container (max-width: 50rem)
- Station selector dropdown
- Update button with status indicator
- Live preview link
- Feedback notifications

## Quick Start

1. Fork the project on Replit
2. Click the "Run" button
3. Access the display board at your Replit URL
4. Use /control for the admin interface

## Project Structure

- `main.py` - Flask application entry point
- `scraper.py` - Schedule data handling
- `/templates` - HTML templates
- `/static` - Assets (CSS, fonts, SVG icons)
  - `/css` - Stylesheets with precise measurements
  - `/fonts` - Polaris font family
  - `/images` - SVG icons and logos

## Contributing

See [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

MIT License - see LICENSE file

## Acknowledgments

- GO Transit for branding guidelines
- Polaris font family for typography
