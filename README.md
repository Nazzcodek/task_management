# Task Management Project

This project is a Task Management system developed with Django and Django REST Framework (DRF). The backend provides a set of RESTful API endpoints for managing tasks, including creating, retrieving, updating, and deleting tasks. The frontend is intended to be developed in a separate phase.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

## Requirements

- Python 3.x
- Django 3.x or later
- Django REST Framework 3.x or later
- SQLite (default) or other database systems like PostgreSQL, MySQL

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/task_management.git
   cd task_management
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

## Configuration

Configuration settings can be found and modified in the `settings.py` file within the project directory. Adjust the database settings, installed apps, and middleware as needed.

## Running the Application

To start the development server, use the following command:

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/login/`. This will take you to the login page where user will be able to login into the dashboard

## API Endpoints

The backend provides the following API endpoints for managing tasks:

- **Retrieve all tasks:** `GET /api/v1/tasks/`
- **Retrieve tasks by status:** `GET /api/v1/tasks/status/{status}/`
- **Create a new task:** `POST /api/v1/tasks/`
- **Retrieve a specific task:** `GET /api/v1/tasks/{id}/`
- **Update an existing task:** `PUT /api/v1/tasks/{id}/`
- **Delete a task:** `DELETE /api/v1/tasks/{id}/`
- **Add User:** `POST /api/v1/users/add_user/`

### Authentication

This project uses Token-based authentication. To access the API, include the token in the `Authorization` header:

```http
Authorization: Token <your_token>
```

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

The tests cover the core functionalities of the Task API endpoints.

### Frontend

The frontend will be developed using a modern JavaScript JQuery, HTML and TailwindCSS

### Features

- User registration and profile management
- Task notifications and reminders
- Advanced task filtering and sorting
- Integration with third-party services (e.g., Google Calendar)

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them with clear messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure your code follows the project's coding standards and passes all tests.

---

For any questions or issues, please open an issue on GitHub or contact the project maintainers.

Happy coding!