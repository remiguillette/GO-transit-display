# Installation Guide for GO Transit Display Board

## System Requirements

- Python 3.11 or higher
- Modern web browser
- Internet connection

## Installation Steps

1. **Fork the project on Replit**

   Use Replit's interface to fork the project.

2. **Install Dependencies**

   The project requires:
   - flask (>=2.3.3)
   - flask-sqlalchemy (>=3.1.1)
   - psycopg2-binary (>=2.9.10)
   - gunicorn (>=23.0.0)

3. **Configuration**

   The application uses these environment variables:
   - DATABASE_URL: PostgreSQL connection string
   - SESSION_SECRET: Secret key for Flask sessions

4. **Running the Application**

   Click the "Run" button in Replit, or use:
   ```bash
   python main.py
   ```

   The application will be available at port 5000.

## Verification

1. Open your web browser to the Replit URL
2. Verify the display board shows train departures
3. Check /control for the admin interface

## Troubleshooting

### Common Issues

1. **Display not showing**
   - Check console for JavaScript errors
   - Verify static files are loading

2. **Styling issues**
   - Ensure Polaris fonts are in static/fonts/
   - Check CSS variable definitions

3. **Database errors**
   - Verify DATABASE_URL is set correctly
   - Check database connectivity

4. **Port already in use (Replit)**  If the port is in use on Replit, check your Replit project settings to ensure the port is available.  If not, modify the port number in `main.py`.