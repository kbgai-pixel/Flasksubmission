# Flask User Submission App

A simple Flask application for collecting user profile information through a web form and displaying the saved records in a table.

## Overview

This project demonstrates a lightweight Flask application with:

- A landing page
- A contact page
- A user information form
- Persistent storage for submitted records
- A page listing all saved users

The app uses SQLite by default and can fall back to MySQL when the MySQL connector is available and configured.

## Features

- Submit personal details such as full name, email, age, city, country, occupation, hobbies, and entertainment preferences
- Validate required fields and numeric inputs
- Store submissions in a database
- Display all users from the database in a simple list view
- Support both local SQLite development and optional MySQL configuration

## Project Structure

```text
Flasksubmission/
├── main.py
├── requirements.txt
├── app.db
├── static/
├── templates/
├── test_app.py
└── README.md
```

## Tech Stack

- Python 3
- Flask
- SQLite (default)
- MySQL Connector (optional)
- pytest

## Requirements

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

From the project root, start the Flask development server:

```bash
python main.py
```

Then open the app in your browser:

- http://127.0.0.1:5000/

## Routes

- `/` - Home page
- `/contact` - Contact page
- `/form` - User submission form
- `/submit-form` - Processes form data and saves to the database
- `/users` - Displays all saved users

## Environment Variables

Optional MySQL configuration:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=sys
```

If MySQL is not available, the app automatically falls back to the local SQLite database file `app.db`.

## Testing

Run the test suite with:

```bash
pytest
```

The project includes basic tests for:

- Home page rendering
- Contact page rendering
- Successful user submission and retrieval

## Notes

- The app creates the `users` table automatically when it starts.
- The default database file is stored in the project root as `app.db`.
- You can enable debug mode by setting:

```bash
export FLASK_DEBUG=1
```

## License

This project is provided as a learning/demo application and is intended for educational use.
