
# Data Analysis Platform with API and Visualization

Welcome to the **Data Analysis Platform**, a comprehensive solution combining a robust API backend with an intuitive frontend for data analysis, machine learning model training, predictions, and performance monitoring. This platform is designed to empower users, from data scientists to non-technical stakeholders, to manage datasets, train models, make predictions, and monitor model performance seamlessly.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Using the Platform](#using-the-platform)
  - [User Registration and Authentication](#user-registration-and-authentication)
  - [Data Management](#data-management)
  - [Model Training](#model-training)
  - [Making Predictions](#making-predictions)
  - [Viewing Model Metrics](#viewing-model-metrics)
  - [User Profile Management](#user-profile-management)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **User Authentication**: Secure user registration and login with JWT-based authentication.
- **Data Management**: Upload, view, and delete datasets with ease.
- **Model Training**: Train various machine learning models (e.g., Logistic Regression, Random Forest) using uploaded datasets.
- **Predictions**: Make single or batch predictions using trained models.
- **Model Metrics**: View performance metrics of trained models with visualizations.
- **User Profile**: Manage user information and view associated datasets.
- **Comprehensive Testing**: Unit and integration tests to ensure reliability.
- **Continuous Integration**: Automated CI pipeline using GitHub Actions for building, testing, and linting.

---

## Architecture

![Architecture Diagram](docs/architecture_diagram.png)

The platform consists of three main components:

1. **Frontend (Streamlit)**: Provides an intuitive UI for users to interact with the platform.
2. **Backend API (FastAPI)**: Handles data management, user authentication, and communication with the ML service.
3. **ML Service**: Responsible for training models, making predictions, and storing model metrics.

Both the **Backend API** and **ML Service** share a common `saved_models/` directory using Docker volumes to ensure seamless access to trained models.

---

## Getting Started

### Prerequisites

- **Docker**: Ensure you have Docker installed. [Download Docker](https://www.docker.com/get-started)
- **Docker Compose**: Comes bundled with Docker Desktop. Verify installation with `docker-compose --version`.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HubertFijolek1/Data_Platform_with_API_and_Visualization
   cd data-analysis-platform
   ```

2. **Create Necessary Directories**

   ```bash
   mkdir -p backend/saved_models
   mkdir -p backend/uploads
   mkdir -p frontend/sample_data
   ```

3. **Generate Fake Data (Optional)**

   To populate the platform with synthetic data:

   ```bash
   python backend/scripts/generate_fake_data.py --users 100 --datasets 50
   ```

### Environment Variables

Create a `.env` file in both the `backend` and `frontend` directories with the following variables:

**backend/.env**

```env
DATABASE_URL=postgresql://postgres:password@db:5432/data_db
TEST_DATABASE_URL=postgresql://postgres:password@db:5432/data_db_test
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost", "http://127.0.0.1"]
```

**frontend/.env**

```env
BACKEND_URL=http://backend-api:8000
```

> **Note**: Replace `your_secret_key` with a strong secret key. Ensure that sensitive information is **never** committed to version control.

---

## Running the Application

Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

This command will:

- Build Docker images for the frontend, backend API, and ML service.
- Start all services, including PostgreSQL.
- Share the `saved_models/` directory between the backend API and ML service.

Access the application at: [http://localhost:8501](http://localhost:8501) (Streamlit Frontend)

---

## Using the Platform

### User Registration and Authentication

1. **Register a New User**

   - Navigate to the **Register** page.
   - Provide a unique username, valid email, and secure password.
   - Submit to create an account.

2. **Login**

   - Navigate to the **Login** page.
   - Enter registered email and password.
   - Upon successful login, you'll receive a JWT token stored in the session state.

### Data Management

1. **Upload Datasets**

   - Go to the **Data Upload** section.
   - Upload CSV files containing your data.
   - Provide a dataset name for easy identification.

2. **View Datasets**

   - Navigate to the **User Profile** page.
   - View a list of your uploaded datasets.
   - Preview dataset details and manage them (e.g., delete if necessary).

### Model Training

1. **Train a Model**

   - Access the **Train & Select Model** section.
   - Choose an algorithm (e.g., Logistic Regression).
   - Select the dataset you wish to train on.
   - Initiate the training process.

2. **Model Storage**

   - Trained models are saved in the shared `saved_models/` directory.
   - They become immediately available for predictions and metrics viewing.

### Making Predictions

1. **Single Prediction**

   - Go to the **Make Predictions** page.
   - Select a trained model from the dropdown.
   - Enter feature values manually.
   - Submit to receive predictions and probabilities.

2. **Batch Predictions**

   - Upload a CSV file containing multiple data points.
   - Ensure the CSV headers match the model's expected features.
   - Submit to receive predictions for all data points.
   - Download the results as a CSV file.

### Viewing Model Metrics

1. **Access Metrics**

   - Navigate to the **Model Metrics** page.
   - Select a trained model and specify its version.
   - Fetch and view performance metrics such as Accuracy, Precision, Recall, or MSE.

2. **Visualizations**

   - Metrics are displayed in both JSON format and visual bar charts for easy interpretation.

### User Profile Management

1. **View Profile**

   - Access the **User Profile** page to view your username, email, and associated datasets.

2. **Update Profile**

   - Update your email or password directly from the profile page.
   - Changes take effect immediately upon successful update.

3. **Manage Datasets**

   - View a list of your uploaded datasets.
   - Delete datasets if they are no longer needed.

---

### GitHub Actions

Automated testing is configured via GitHub Actions. Tests run on every push and pull request to the `master` branch, ensuring code integrity.

---

## Continuous Integration

The project uses GitHub Actions for continuous integration, automating the build, test, and deployment processes.

### CI Pipeline Overview

1. **Checkout Code**

   - The workflow checks out the repository code.

2. **Set Up Python and Docker**

   - Python environment is set up.
   - Docker Compose is installed.

3. **Install Dependencies**

   - Backend and frontend dependencies are installed in their respective directories.

4. **Build Docker Containers**

   - Docker images for backend API and ML service are built.

5. **Run Containers and Tests**

   - Containers are started in the background.
   - Tests for both backend API and ML service are executed.
   - Code is linted using `flake8`.

6. **Streamlit App Availability**

   - The CI checks if the Streamlit frontend is accessible on port `8501`.

### GitHub Actions Configuration

Located at `.github/workflows/ci.yml`, the CI pipeline ensures that all code changes are automatically tested and validated before merging.

---

## Project Structure

```
data-analysis-platform/
├── backend/
│   ├── api/
│   │   ├── app/
│   │   │   ├── routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── data.py
│   │   │   │   ├── data_generator.py
│   │   │   │   ├── data_upload.py
│   │   │   │   └── ml_ops.py
│   │   │   ├── config/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── settings.py
│   │   │   ├── database.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── models.py
│   │   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── schemas_ml.py
│   │   │   ├── crud/
│   │   │   │   ├── __init__.py
│   │   │   │   └── crud.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   └── auth_service.py
│   │   │   ├── utils/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── generators.py
│   │   │   │   ├── rate_limiter.py
│   │   │   │   └── role_checker.py
│   │   │   ├── middlewares/
│   │   │   │   ├── __init__.py
│   │   │   │   └── middlewares.py
│   │   │   ├── main.py
│   │   │   ├── ...
│   │   │   └── ...
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_auth_unit.py
│   │   │   ├── test_data.py
│   │   │   ├── test_data_generator.py
│   │   │   ├── test_data_integration.py
│   │   │   ├── test_data_upload.py
│   │   │   └── ...
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── alembic.ini
│   │   ├── alembic_migrations/
│   │   └── scripts/
│   │       ├── create_test_db.py
│   │       ├── generate_fake_data.py
│   │       ├── train_models.py
│   │       ├── cleanup_duplicates.py
│   │       └── __init__.py
│   ├── saved_models/
│   ├── uploads/
│   └── ...
├── frontend/
│   ├── components/
│   │   ├── pages/
│   │   │   ├── predict_page.py
│   │   │   ├── model_metrics.py
│   │   │   ├── user_profile.py
│   │   │   └── ...
│   │   ├── headers.py
│   │   └── footers.py
│   ├── sample_data/
│   ├── .env
│   ├── requirements.txt
│   └── ...
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── README.md
└── ...
```

---

## Contact

For any questions or suggestions, please open an issue or contact [hubertfijolek1@gmail.com](mailto:hubertfijolek1@gmail.com).
