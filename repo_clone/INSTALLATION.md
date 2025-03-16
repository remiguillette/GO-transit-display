
# Installation Guide for GO Transit Display Board

## System Requirements

- Python 3.11 or higher
- Modern web browser
- Internet connection for development

## Quick Start on Replit

1. Fork the project on Replit
2. The dependencies will be automatically installed
3. Click the "Run" button to start the application
4. The application will be available at your Replit URL

## Manual Installation Steps

1. **Clone the repository in Replit**
   Fork the project using Replit's interface

2. **Install Dependencies**
   The project requires:
   - flask (>=2.3.3)
   - flask-sqlalchemy (>=3.1.1)
   - psycopg2-binary (>=2.9.10)
   - gunicorn (>=23.0.0)
   - flask-socketio (>=5.5.1)

3. **Configuration**
   Required environment variables:
   - DATABASE_URL: PostgreSQL connection string
   - SESSION_SECRET: Secret key for Flask sessions

4. **Running the Application**
   Click the "Run" button in Replit, or use:
   ```bash
   python main.py
   ```

## Port Configuration

The application runs on port 5000 by default and binds to 0.0.0.0 to be accessible through Replit's proxy.

## Verification

1. Open your Replit URL
2. Verify the display board shows train departures
3. Check /control for the admin interface

## Troubleshooting

### Common Issues

1. **Display not showing**
   - Check console for JavaScript errors
   - Verify static files are loading
   - Ensure WebSocket connection is established

2. **Styling issues**
   - Verify Polaris fonts are in static/fonts/
   - Check CSS variable definitions
   - Confirm proper unit measurements

3. **Database errors**
   - Verify DATABASE_URL is set correctly
   - Check database connectivity
   - Ensure tables are created
