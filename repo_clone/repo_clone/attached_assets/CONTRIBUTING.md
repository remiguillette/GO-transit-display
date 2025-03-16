# Contributing to GO Transit Display

Thank you for considering contributing to the GO Transit Display project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct.

## Project Structure

The project follows this structure:
```
├── static/
│   ├── css/
│   │   ├── styles.css      # Main styling
│   │   └── display.css     # Display board specific styles
│   ├── fonts/             # Polaris font files
│   ├── images/           # Project images
│   └── js/              # JavaScript files
├── templates/
│   ├── base.html        # Base template
│   ├── control.html     # Control panel template
│   └── display.html     # Main display board
├── app.py              # Flask application logic
├── main.py            # Application entry point
├── models.py         # Database models
└── scraper.py       # Schedule data handling
```

## Style Guidelines

### Python
- Follow PEP 8
- Use 4 spaces for indentation
- Include type hints
- Add docstrings for public functions

### CSS
- Use the defined color variables:
  - --go-black: #000000
  - --go-white: #FFFFFF
  - --go-gray: #4f4f4f
  - --delayed-red: #ff0000
  - --time-yellow: #ffffff
  - --ada-blue: #0052A5

### HTML/JavaScript
- Use semantic HTML elements
- Follow Bootstrap conventions where applicable
- Use ES6+ JavaScript features


## Submitting Changes

1. Create a fork of the project
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/yourusername/go-transit-display/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/go-transit-display/issues/new/choose) using the bug report template.
- Include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- **Check if the enhancement has already been suggested** by searching on GitHub under [Issues](https://github.com/yourusername/go-transit-display/issues).
- If not, [open a new issue](https://github.com/yourusername/go-transit-display/issues/new/choose) using the feature request template.
- Provide a **clear and detailed explanation** of the feature you want and why it would be beneficial.

### Pull Requests

- Fill in the required template.
- Do not include issue numbers in the PR title.
- Include screenshots and animated GIFs in your pull request whenever possible.
- Follow the [Python styleguide](#python-styleguide).
- Include thoughtfully-worded, well-structured tests.
- Document new code.
- End all files with a newline.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐎 `:racehorse:` when improving performance
    * 🚱 `:non-potable_water:` when plugging memory leaks
    * 📝 `:memo:` when writing docs
    * 🐛 `:bug:` when fixing a bug
    * 🔥 `:fire:` when removing code or files
    * 💚 `:green_heart:` when fixing the CI build
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security
    * ⬆️ `:arrow_up:` when upgrading dependencies
    * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Styleguide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

* Use 4 spaces for indentation (not tabs).
* Use docstrings for all public classes, methods, and functions.
* Keep line length to a maximum of 88 characters.
* Use meaningful variable names.
* Add type hints where appropriate.

### HTML/CSS Styleguide

* Use 2 spaces for indentation (not tabs).
* Use descriptive class names.
* Prioritize semantic HTML.
* Avoid inline styles where possible.

## Additional Notes

### Issue and Pull Request Labels

This project uses labels to help organize and prioritize issues and pull requests. Here's what they mean:

* `bug` - Issues that report broken functionality
* `documentation` - Issues or PRs related to documentation
* `enhancement` - Issues that request or PRs that implement a new feature
* `good first issue` - Issues that are good for newcomers
* `help wanted` - Issues where we're looking for help
* `question` - Questions about the project

## Development Environment Setup

The project uses:
- Python 3.11+
- Flask framework
- SQLAlchemy for database
- Bootstrap 5.3 for styling
- Polaris font family

1. Fork the repository
2. Clone your fork:
   ```
   git clone https://github.com/your-username/go-transit-display.git
   cd go-transit-display
   ```
3. Set up your development environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Or with Poetry:
   ```
   poetry install
   ```
4. Run the application:
   ```
   python main.py
   ```

Thank you for your contributions!