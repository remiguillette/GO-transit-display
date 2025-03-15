# Installation Guide for GO Transit Display Board

This document provides detailed installation instructions for setting up the GO Transit Display Board application.

## System Requirements

- Python 3.11 or higher
- pip or Poetry package manager
- Modern web browser
- Internet connection for development

## Step-by-Step Installation

### Using pip (Standard Method)

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/go-transit-display.git
   cd go-transit-display
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate on Linux/macOS
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install the required packages**

   The project requires the following Python packages:
   - flask (>=2.3.3)
   - flask-sqlalchemy (>=3.1.1)
   - psycopg2-binary (>=2.9.10)
   - email-validator (>=2.2.0)
   - gunicorn (>=23.0.0)
   - pytest (>=7.4.0) [for development/testing]

   Install all dependencies with:

   ```bash
   pip install flask flask-sqlalchemy psycopg2-binary email-validator gunicorn pytest
   ```

### Using Poetry (Alternative Method)

1. **Install Poetry** (if not already installed)

   Follow the [official Poetry installation guide](https://python-poetry.org/docs/#installation)

2. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/go-transit-display.git
   cd go-transit-display
   ```

3. **Install dependencies using Poetry**

   ```bash
   poetry install
   ```

4. **Activate the Poetry environment**

   ```bash
   poetry shell
   ```

## Running the Application

### Development Mode

```bash
python main.py
```

This will start the application in development mode with debugging enabled. The application will be accessible at http://localhost:5000.

### Production Mode (using Gunicorn)

```bash
gunicorn --bind 0.0.0.0:5000 --workers=4 main:app
```

For automatic reloading during development:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Verification

To verify that the installation was successful:

1. Start the application
2. Open your web browser and navigate to http://localhost:5000
3. You should see the GO Transit display board showing train departures
4. Navigate to http://localhost:5000/control to verify that the station selection works

## Troubleshooting

### Common Issues

1. **Port already in use**
   - If port 5000 is already in use, change the port number in the run command:
     ```bash
     python main.py --port=5001
     ```
     or
     ```bash
     gunicorn --bind 0.0.0.0:5001 main:app
     ```

2. **Static files not loading**
   - Ensure that the static directory structure is preserved
   - Check browser console for path-related errors

3. **Font display issues**
   - The application falls back to system fonts if the Polaris fonts are not available
   - Make sure the font files are in the correct location (static/fonts/)

## Platform-Specific Notes

### Windows

- When using Gunicorn, consider using Waitress instead as Gunicorn is primarily for Unix systems
- Install with: `pip install waitress`
- Run with: `waitress-serve --port=5000 main:app`

### Linux/macOS

- No special considerations required
- For production deployment, consider setting up a proper WSGI server with Nginx

## Next Steps

After installation:

1. Visit the [README.md](README.md) for usage instructions
2. Explore the [control panel](http://localhost:5000/control) to change stations
3. Check the real-time updates of the schedule display