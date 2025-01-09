# Data Analysis Platform

## Overview
The Data Analysis Platform is a comprehensive solution for data analysis, visualization, and AI-powered insights. It enables users to upload datasets, perform machine learning tasks such as predictions and classifications, and visualize results interactively through a user-friendly dashboard.
---

## Key Features
### 1. **Data Uploads**
- Upload datasets in CSV or TXT formats.
- Store metadata in a PostgreSQL database for versioning and easy access.
- Optionally, trigger model training upon upload with customizable parameters.

### 2. **AI and Machine Learning**
- Train and evaluate models using TensorFlow or PyTorch.
- Support for both classification and regression tasks.
- REST API endpoints for making single or batch predictions.
- Store and retrieve model performance metrics for various versions.

### 3. **Interactive Dashboard**
- Built with **Streamlit**, the frontend allows:
  - Uploading datasets.
  - Visualizing data through line charts, scatter plots, bar charts, and histograms.
  - Generating synthetic datasets for testing.
  - Managing user profiles and preferences.

### 4. **Synthetic Data Generation**
- Quickly create large datasets with fake user data or random values.
- Useful for testing pipelines or creating demonstration scenarios.

### 5. **Authentication and Authorization**
- User management system with registration and login.
- Role-based access control (RBAC) to restrict certain actions (e.g., only admins can delete datasets).

---

## Technology Stack
### Backend
- **FastAPI**: For building the RESTful API.
- **PostgreSQL**: Relational database for storing datasets and user data.
- **SQLAlchemy**: ORM for database interactions.
- **TensorFlow and PyTorch**: For AI model training and predictions.

### Frontend
- **Streamlit**: For creating an interactive, Python-based web dashboard.

### Infrastructure and CI/CD
- **Docker**: Containerization for consistent development and deployment environments.
- **Docker Compose**: To orchestrate multi-container applications (backend, frontend, and database).
- **GitHub Actions**: Automated workflows for linting, testing, and deployment.

---

## Project Structure

The following is a comprehensive directory structure of the project, detailing each file and its purpose:

```
Data_Analysis_Platform/
├── backend/              # Backend (FastAPI) for handling APIs and business logic
│   ├── app/              # Main backend application logic
│   │   ├── config/       # Application configuration
│   │   │   ├── __init__.py          # Config module initialization
│   │   │   ├── settings.py          # Application settings (environment variables, CORS settings)
│   │   ├── crud/         # CRUD (Create, Read, Update, Delete) operations
│   │   │   ├── __init__.py          # CRUD module initialization
│   │   │   ├── crud.py             # Functions for interacting with the database
│   │   ├── database.py   # Database configuration (SQLAlchemy engine, sessions)
│   │   ├── main.py       # Entry point of the FastAPI backend
│   │   ├── middlewares/  # Middlewares for additional processing
│   │   │   ├── __init__.py          # Middleware module initialization
│   │   │   ├── middlewares.py       # Error handling middleware
│   │   ├── ml/           # Machine learning models and utilities
│   │   │   ├── bert.py              # Sentiment analysis with BERT
│   │   │   ├── feature_engineering.py # Feature engineering functions
│   │   │   ├── metrics_manager.py  # Utility for saving/loading model metrics
│   │   │   ├── model.py             # Training and evaluation of TensorFlow models
│   │   │   ├── preprocessing.py     # Data preprocessing logic
│   │   │   ├── pytorch_model.py     # PyTorch model implementations (classification/regression)
│   │   │   ├── sentiment.py         # Sentiment analysis using TextBlob
│   │   ├── models/       # SQLAlchemy ORM models
│   │   │   ├── __init__.py          # Model module initialization
│   │   │   ├── models.py            # Database table definitions (users, datasets)
│   │   ├── routers/      # API routers (grouped endpoints)
│   │   │   ├── __init__.py          # Router module initialization
│   │   │   ├── auth.py             # Authentication endpoints
│   │   │   ├── data.py             # Data management endpoints
│   │   │   ├── data_generator.py   # Synthetic data generation endpoints
│   │   │   ├── data_upload.py      # File upload endpoints
│   │   │   ├── ml_ops.py           # Machine learning operation endpoints (training, metrics)
│   │   │   ├── predict.py          # Prediction API endpoints
│   │   ├── schemas/      # Pydantic schemas for validation
│   │   │   ├── __init__.py          # Schemas module initialization
│   │   │   ├── schemas.py          # User-related schemas
│   │   │   ├── schemas_ml.py       # Schemas for ML operations
│   │   ├── services/     # Business logic services
│   │   │   ├── __init__.py          # Services module initialization
│   │   │   ├── auth_service.py     # Authentication logic (JWT, login)
│   │   ├── tests/        # Backend test cases
│   │   │   ├── conftest.py         # Test configurations
│   │   │   ├── test_auth.py        # Authentication endpoint tests
│   │   │   ├── test_data.py        # Data upload/download endpoint tests
│   │   │   ├── test_ml.py          # Machine learning model tests
│   │   │   ├── test_data_generator.py # Synthetic data generation tests
│   ├── requirements.txt  # Backend Python dependencies
│   ├── Dockerfile        # Docker configuration for the backend
│   ├── alembic/          # Database migration management
│   │   ├── env.py        # Alembic environment configuration
│   │   ├── script.py.mako # Template for new migration scripts
│   │   ├── versions/     # Migration scripts
│   │   │   ├── d0f0da722d4f_create_users_table.py # Migration to create users table
│   │   │   ├── 62472d9a96f9_create_datasets_table.py # Migration to create datasets table
│   │   │   ├── fd5e69127c23_add_role_column_to_user_model.py # Add role column to users table
│   │   ├── README        # Alembic usage guide
├── frontend/             # Frontend (Streamlit) for user interaction
│   ├── components/       # Modular UI components
│   │   ├── navbar.py              # Sidebar navigation bar
│   │   ├── pages/        # Pages of the application
│   │   │   ├── login.py           # Login page
│   │   │   ├── register.py        # Registration page
│   │   │   ├── upload_data.py     # Data upload page
│   │   │   ├── data_visualization.py # Data visualization page
│   │   │   ├── predict_page.py    # Prediction page
│   │   │   ├── model_metrics.py   # Model metrics page
│   │   │   ├── generate_data.py   # Synthetic data generation page
│   │   ├── forms.py               # Forms for input handling (e.g., login, registration)
│   │   ├── headers.py             # Page headers
│   │   ├── footers.py             # Page footers
│   ├── app.py          # Main Streamlit application logic
│   ├── requirements.txt # Frontend dependencies
│   ├── Dockerfile        # Docker configuration for the frontend
│   ├── .streamlit/       # Streamlit configuration and secrets
│   │   ├── config.toml  # UI themes
│   │   ├── secrets.toml # Backend URL and other secrets
├── scripts/              # Utility scripts for data and model management
│   ├── generate_fake_data.py # Generate synthetic users and datasets
│   ├── train_models.py   # Script to automate model training
├── .github/              # GitHub CI/CD configurations
│   ├── workflows/
│   │   ├── ci.yml        # GitHub Actions pipeline
├── docker-compose.yml    # Docker Compose configuration for multi-container setup
├── .env                  # Environment variables for the application
├── pytest.ini            # Pytest configuration
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
```

### Key Components:
- **backend**: Implements the server-side logic, APIs, and ML operations using FastAPI.
- **frontend**: Provides an interactive user interface built with Streamlit.
- **scripts**: Contains standalone scripts for generating data or automating tasks.
- **.github**: GitHub Actions workflows for CI/CD processes such as testing, linting, and deployment.
- **docker-compose.yml**: Manages multi-container orchestration for backend, frontend, and database services.
- **README.md**: Comprehensive documentation for the project, including installation and usage instructions.

---

## Setup and Installation

### Prerequisites
- **Docker**: Ensure Docker is installed and running.
- **Python 3.10+**: For running scripts or testing locally.

### Steps
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/HubertFijolek1/Data_Analysis_Platform_with_API_and_Visualization.git
    cd Data_Analysis_Platform_with_API_and_Visualization
    ```

2. **Start the Application**:
    ```bash
    docker-compose up --build
    ```
    - The backend API will be accessible at: `http://localhost:8000`
    - The frontend dashboard will be accessible at: `http://localhost:8501`

3. **Environment Configuration**:
    - Update the `.env` files in both the backend and frontend directories to match your local environment. Example:
      ```env
      DATABASE_URL=postgresql://postgres:password@db:5432/data_db
      SECRET_KEY=your_secret_key
      BACKEND_URL=http://backend:8000
      ```

4. **Run Migrations**:
    ```bash
    cd backend
    alembic upgrade head
    ```

---

## Usage

### Backend API
The backend provides a comprehensive REST API for managing data and models. Key endpoints include:
- **User Management**:
  - `POST /auth/register`: Register a new user.
  - `POST /auth/login`: Authenticate a user and receive a token.
  - `GET /auth/me`: Retrieve current user details.
- **Dataset Management**:
  - `POST /data/upload`: Upload a dataset.
  - `GET /data/`: List all datasets.
  - `DELETE /data/{dataset_id}`: Delete a specific dataset (admin only).
- **AI and ML Operations**:
  - `POST /predict/`: Make predictions with a trained model.
  - `POST /ml/retrain`: Retrain an existing model.

Access interactive documentation at: [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Dashboard
The frontend provides an intuitive interface for:
- Uploading and visualizing datasets.
- Generating synthetic data.
- Managing models and metrics.
- Making predictions interactively.

---

## Testing

### Backend
To run backend tests, ensure dependencies are installed:
```bash
cd backend
pytest
```
For coverage reports, use:
```bash
pytest --cov=app
```

### Frontend
To test and debug the frontend:
```bash
streamlit run frontend/app.py
```

### Linting and Formatting
Run flake8 for linting and black for formatting:
```bash
flake8 backend/ frontend/
black --check backend/ frontend/
```

---

## CI/CD Workflow
This project uses GitHub Actions for CI/CD. The pipeline includes:
- **Linting and Formatting**:
  - Enforces code quality standards using flake8 and black.
- **Unit Tests**:
  - Runs backend tests to ensure functionality.
- **Database Migrations**:
  - Applies migrations to ensure database schema consistency.

Workflow configuration can be found in `.github/workflows/ci.yml`.

---

## Contact
For questions, suggestions, or collaboration, contact:

**Hubert Fijołek**
GitHub: [HubertFijolek1](https://github.com/HubertFijolek1)
Email: hubertfijolek1@gmail.com
