# GO Transit Display Board

A Flask-based GO Transit display board application showing real-time train departures with proper branding and accessibility features.

## Features

- Real-time train schedule display
- GO Transit branded interface
- Accessibility-compliant design
- Mobile-responsive layout
- Station selection control panel
- Dark theme optimized display
- Polaris font integration

## Tech Stack

- Flask web framework
- SQLAlchemy ORM
- Bootstrap 5.3
- Custom CSS with GO Transit theming
- JavaScript for real-time updates

## Color Scheme

- Black background (#000000)
- White text (#FFFFFF)
- Delayed/Cancelled status (#FF0000)
- ADA-compliant blue (#0052A5)

## Quick Start

1. Fork the project on Replit
2. Click the "Run" button
3. Access the display board at the project URL
4. Use /control for the admin interface

## Installation

Please refer to the [Installation Guide](INSTALLATION.md) for detailed setup instructions.

```bash
# Quick start with Flask development server
python main.py

# Or with Gunicorn (recommended for production)
gunicorn --bind 0.0.0.0:5000 --workers=4 main:app
```

## Contributing

Contributions are welcome! Please read [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## License

MIT License - see LICENSE file