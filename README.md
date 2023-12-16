# Secure Todo List API

Welcome to the Secure Todo List API project! This project aims to provide a secure and feature-rich API for managing your personal todo list. Built using FastAPI and Pydantic, the API includes robust authentication and authorization mechanisms to ensure that your todo items are accessible only to you.

## Getting Started

### Prerequisites

- Python (3.6 or later)
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/pessiMargalit/fastAPI-secure.git
   ```

2. Navigate to the project directory:

   ```bash
   cd secure-todo-api
   ```

3. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Rename the `.env.example` file to `.env`.

2. Open the `.env` file and set your environment variables, such as database connection details, JWT secret key, etc.

## Running the API

1. Run the FastAPI development server:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

2. Access the API documentation:

   Open your browser and visit `http://127.0.0.1:8000/docs` to interact with the API using the automatically generated documentation.

## Features

- User registration and login with token-based authentication.
- Create, read, update, and delete personal todo items.
- User-specific access control to ensure data privacy.
- Input validation and data serialization using Pydantic models.
- Incremental security enhancements for a robust and reliable API.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
