# Task Management System

Task Management System is a Django web application designed for managing tasks with user authentication and REST API endpoints.

## Features

- User authentication system for secure access to the application.
- CRUD (Create, Read, Update, Delete) operations for tasks.
- RESTful API endpoints for interacting with tasks programmatically.
- Token-based authentication for API access.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- Python (3.6 or higher)
- Django
- Django REST Framework
- Django REST Knox

### Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/task-management.git
   ```

2. Navigate to the project directory:

   ```bash
   cd task-management
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Apply migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

2. (Optional) Create a superuser account for accessing the Django admin interface:

   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

### Accessing the Application

- Access the web interface by visiting `http://127.0.0.1:8000/`.
- Access the REST API endpoints by visiting `http://127.0.0.1:8000/api/`.

### API Authentication

The API endpoints require token authentication. Obtain an authentication token by sending a POST request to `http://127.0.0.1:8000/api/login` with your username and password in the request body. The token will be returned in the response, which you can then use for subsequent API requests.

### API Endpoints

- `/api/tasks/`: List and create tasks (requires authentication).
- `/api/tasks/{id}/`: Retrieve, update, or delete a specific task by ID (requires authentication).
