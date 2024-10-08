﻿## Overview

This project demonstrates a CRUD (Create, Read, Update, Delete) RESTful service built with Flask. The application showcases best practices for structuring a Flask project, handling configurations, and performing database operations.

### Project Structure

The project follows a modular structure to ensure clarity and separation of concerns:

- **`app.py`**: The entry point of the application, where the Flask app is created and configured.
- **`config/`**: Contains configuration files for different environments and logging.
    - `config.py`: Configuration settings for development, testing, and production environments.
    - `logconfig.py`: Logging configuration.
- **`controllers/`**: Houses route handlers and request/response logic.
    - `user_controller.py`: Defines endpoints for user-related operations.
- **`dtos/`**: Data Transfer Objects used to structure data for requests and responses.
    - `request/`: DTOs for incoming requests.
        - `user_request_dto.py`: Defines the structure for user creation and update requests.
    - `response/`: DTOs for outgoing responses.
        - `user_response_dto.py`: Defines the structure for user-related responses.
    - `response_helper.py`: Utility functions for response formatting.
- **`models/`**: Defines the database models.
    - `user.py`: Contains the User model.
- **`repositories/`**: Handles data access and interactions with the database.
    - `user_repository.py`: Contains methods for user data operations.
- **`services/`**: Contains business logic.
    - `user_service.py`: Implements logic for user-related operations.
- **`mappers/`**: Maps data between different layers of the application.
    - `user_mapper.py`: Transforms data between DTOs and models.
- **`errors/`**: Manages error handling.
    - `error_handlers.py`: Defines custom error handlers.
    - `user_not_found.py`: Error handling for cases where a user is not found.
- **`tests/`**: Contains test cases and fixtures.
    - `test_user_controller.py`: Tests for user-related endpoints.
    - `conftest.py`: Configuration for test fixtures.
    - `unittest/`: Unit tests for services.
        - `test_user_service.py`: Unit tests for user service logic.

### Running the Application

#### Without Docker

1. **Install Dependencies**

   Ensure you have Python 3.6+ installed. Install the required packages with:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**

   Create a `.env` file by copying from `.env.example` and set your database credentials:

   **For example:**
   ```plaintext
   # Application Configuration
   APP_NAME=Flask-crud
   APP_ENV=development
   APP_HOST=0.0.0.0
   APP_PORT=4000
   APP_DEBUG=true

   # Postgres Configuration
   FLASK_ENV=development
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   
   # MongoDB Configuration
    MONGO_DB_HOST=your_db_host

    # Docker Environment Flag
    IS_DOCKER=false

   # Profiler Credentials
   PROFILER_USERNAME=admin
   PROFILER_PASSWORD=password
   ```

3. **Run the Application**

   Start the Flask application with:

   ```bash
   flask run
   ```

   The application will be accessible at `http://localhost:4000`.

#### With Docker

1. **Build the Docker Image**

   Build the Docker image using:

   ```bash
   docker build -t flask_crud .
   ```

2. **Run the Docker Container**

   Start the container with:

   ```bash
   docker-compose up
   ```

   The application will be accessible at `http://localhost:4000`.

### Running Tests

To run the test suite, use:

```bash
pytest
```

### Profiler and Metrics Access

- **Profiler**: The profiler can be accessed at [http://localhost:4000/flask-profiler](http://localhost:4000/flask-profiler).
- **Metrics**: The Prometheus metrics can be accessed at [http://localhost:4000/my-metrics](http://localhost:4000/my-metrics).

### Base URI

The base URI for accessing the API is:

- **Local Development**: `http://localhost:4000`
- **Docker**: `http://localhost:4000`

### API Endpoints

| Method | URI                | Description                        |
|--------|--------------------|------------------------------------|
| POST   | /users             | Create a new user                  |
| GET    | /users             | Retrieve all users                 |
| GET    | /users/{id}        | Retrieve a specific user by ID     |
| PUT    | /users/{id}        | Update a specific user by ID       |
| DELETE | /users/{id}        | Delete a specific user by ID       |

### Endpoint Details

#### Create a New User

- **URL**: `/users`
- **Method**: `POST`
- **Payload**:

  ```json
  {
    "username": "test_user",
    "email": "testuser@example.com"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "status": 201,
    "message": "User created successfully"
  }
  ```

#### Retrieve All Users

- **URL**: `/users`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "status": 200,
    "message": "Users retrieved successfully",
    "data": [
        {
            "id": 4,
            "username": "test_user",
            "email": "testuser@example.com"
        }
    ]
  }
  ```

#### Retrieve User by ID

- **URL**: `/users/{id}`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "username": "test_user",
      "email": "testuser@example.com"
    }
  }
  ```

#### Update User by ID

- **URL**: `/users/{id}`
- **Method**: `PUT`
- **Payload**:

  ```json
  {
    "username": "updated_user",
    "email": "updateduser@example.com"
  }
  ```

- **Response**:

  ```json
    {
      "success": true,
      "status": 200,
      "message": "User updated successfully",
      "data": {
          "id": 4,
          "username": "updated_user",
          "email": "updateduser@example.com"
       }
    }
  ```

#### Delete User by ID

- **URL**: `/users/{id}`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "success": true,
    "status": 200,
    "message": "User deleted successfully"
  }
  ```
  
## 🤓 Author

- [Ikechukwu Michael](mailto:mikeikechi3@gmail.com)
