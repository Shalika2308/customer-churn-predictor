# Customer Churn Prediction System

## Project Overview

### Problem Statement

Customer churn is a major challenge for telecom companies, as losing existing customers directly impacts revenue and growth. Identifying customers who are likely to leave enables businesses to take proactive retention measures and improve customer satisfaction.

### Solution

This project implements an end-to-end Customer Churn Prediction System that predicts whether a customer is likely to churn based on demographic information, subscribed services, contract details, and billing data. The solution combines machine learning, API development, data persistence, and a user-friendly web interface to provide a complete prediction workflow.

### Key Components

* **Machine Learning Prediction Engine** for churn prediction
* **FastAPI REST API** for serving predictions
* **Streamlit Dashboard** for user interaction
* **SQLite Database Storage** for prediction history
* **Input Validation** for reliable and secure requests
* **Logging & Monitoring** for tracking application activity and errors
* **Prediction Confidence Scoring** to indicate model certainty
* **Feature Engineering Pipeline** for improved model performance

# Project Structure

```text
customer-churn-predictor/
│
├── data/
│   └── Telco_customer_churn.xlsx
│
├── database/
│   └── predictions.db
│
├── logs/
│   └── app.log
│
├── models/
│   ├── model.pkl
│   └── columns.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   └── database.py
│
├── api.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

# Dataset

Dataset Used:

**IBM Telco Customer Churn Dataset**
Dataset link: [IBM Telco Customer Churn Dataset]( https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)

Contains information about:

* Customer demographics
* Service subscriptions
* Billing details
* Contract information
* Churn status

**Dataset Size**

- 7,043 customer records

**Target Variable**

- **Churn Value**
  - `0` → Customer is retained (No Churn)
  - `1` → Customer has left the service (Churn)

# Feature Engineering

Three feature engineering techniques were implemented.

## 1. Derived Feature

ChargesPerMonth = TotalCharges / (TenureMonths + 1)

Purpose:

* Captures average spending behavior.
* Provides additional billing insight.

## 2. Binary Flag Feature

IsLongTermCustomer

Logic:

1 if TenureMonths > 24
0 otherwise

Purpose:

* Identifies loyal customers.
* Improves churn pattern detection.

## 3. One-Hot Encoding

Applied to all categorical variables.

Example:

Gender_Male
Contract_TwoYear
InternetService_Fiber

Purpose:

* Converts categorical values into machine-learning-compatible format.

# Machine Learning Models

Two models were evaluated.

## Logistic Regression (Selected)

Performance:

| Metric    | Score |
| --------- | ----- |
| Accuracy  | 80.6% |
| Precision | 64.7% |
| Recall    | 59.4% |
| F1 Score  | 61.9% |
| ROC-AUC   | 73.8% |

## Random Forest

| Metric    | Score |
| --------- | ----- |
| Accuracy  | 79.2% |
| Precision | 63.3% |
| Recall    | 51.6% |
| F1 Score  | 56.8% |
| ROC-AUC   | 70.4% |

Selected Model:

**Logistic Regression**

Reason:

* Higher accuracy
* Better recall
* Better overall balance

# REST API

## Health Endpoint

```http
GET /health
```

Response:

```json
{
  "status": "OK"
}
```

## Prediction Endpoint

```http
POST /predict
```

Returns:

```json
{
  "prediction": "No Churn",
  "confidence": 0.84
}
```

# Validation

Implemented using Pydantic.

Validation Rules:

* Invalid Gender Rejected
* Invalid Contract Rejected
* Negative Charges Rejected
* Negative Tenure Rejected
* Missing Fields Rejected
* Incorrect Data Types Rejected

# Database Storage

Predictions are automatically stored in SQLite.

Stored Information:

* Tenure Months
* Monthly Charges
* Contract Type
* Prediction
* Confidence Score
* Timestamp

Database File:

```text
database/predictions.db
```
# Logging

Logs are written to:

```text
logs/app.log
```

Logged Events:

* API Startup
* Prediction Requests
* Prediction Results
* Database Errors
* Runtime Exceptions

## Failure Handling

The application is designed to continue serving predictions even if database operations fail.

After a prediction is generated, the system attempts to save the prediction details to the SQLite database. Database operations are wrapped inside a separate `try-except` block.

If the database save operation fails (for example, due to a missing database file, connection issue, or write error):

- The error is recorded in the application logs.
- The prediction process is not interrupted.
- The API still returns the prediction and confidence score to the user.

This approach improves application reliability by ensuring that database failures do not prevent users from receiving prediction results.

### Workflow

```text
Prediction Request
       │
       ▼
Generate Prediction
       │
       ▼
Try Saving to Database
       │
       ├── Success → Save Record
       │
       └── Failure
                │
                ▼
          Log Error
                │
                ▼
      Return Prediction
```

# Streamlit Dashboard

Features:

* Interactive Customer Form
* Confidence Visualization
* Prediction Status Indicators
* Prediction History
* Interactive Plotly Charts
* User Guidance Tooltips

# Installation & Setup

## Prerequisites

Before running the project, ensure the following software is installed:

* Python 3.10 or later
* Visual Studio Code (recommended)
* Internet connection (for installing dependencies)

**Note:** SQLite does not need to be installed separately because Python includes the built-in `sqlite3` library.


## Clone Repository

```bash
git clone https://github.com/Shalika2308/customer-churn-predictor
cd customer-churn-predictor
```

## Create Virtual Environment

A virtual environment keeps project dependencies isolated from other Python projects.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, you should see:

```text
(venv)
```

at the beginning of your terminal prompt.

## Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:**

* Installation may take several minutes depending on internet speed.
* Wait until installation completes successfully before proceeding.

#  Create Database

Before running the application, create the SQLite database:

```bash
python src/database.py
```

Expected output:

```text
Database created successfully!
```

This creates:

```text
database/predictions.db
```

The database is used to store:

* Input features
* Prediction results
* Confidence scores
* Timestamps


# Running the Application

The application requires two terminals.


## Terminal 1 — Start FastAPI

```bash
uvicorn api:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

## Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI is an interactive API testing interface automatically generated by FastAPI.

Using Swagger, you can:

* View available endpoints
* Test API requests
* Submit sample data
* View API responses

### Available Endpoints

#### Health Check

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "OK"
}
```

#### Prediction Endpoint

Endpoint:

```text
POST /predict
```

To test:

1. Open Swagger UI.
2. Expand `/predict`.
3. Click **Try it out**.
4. Enter sample customer data.
5. Click **Execute**.
6. View prediction response.


## Test Prediction Using cURL

Example:

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
-H "Content-Type: application/json" ^
-d "{\"Gender\":\"Male\",\"Senior_Citizen\":\"No\",\"Partner\":\"Yes\",\"Dependents\":\"No\",\"Tenure_Months\":24,\"Phone_Service\":\"Yes\",\"Multiple_Lines\":\"No\",\"Internet_Service\":\"DSL\",\"Online_Security\":\"Yes\",\"Online_Backup\":\"No\",\"Device_Protection\":\"No\",\"Tech_Support\":\"Yes\",\"Streaming_TV\":\"No\",\"Streaming_Movies\":\"No\",\"Contract\":\"One year\",\"Paperless_Billing\":\"Yes\",\"Payment_Method\":\"Credit card (automatic)\",\"Monthly_Charges\":70,\"Total_Charges\":1680}"
```

Expected response:

```json
{
  "prediction": "No Churn",
  "confidence": 0.84
}
```
**Note:** On Windows PowerShell, line continuation characters may differ. Alternatively, the API can be tested directly using FastAPI Swagger UI at:

http://127.0.0.1:8000/docs

## Terminal 2 — Start Streamlit Dashboard

```bash
streamlit run app.py
```

Expected output:

```text
Local URL: http://localhost:8501
```

Open:

```text
http://localhost:8501
```

The Streamlit dashboard provides:

* Customer input form
* Prediction generation
* Confidence score display
* Prediction history
* Prediction distribution chart

# Quick Verification Checklist

Before using the application:

* Virtual environment activated
* Dependencies installed successfully
* Database created successfully
* FastAPI server running
* Swagger UI accessible
* Streamlit dashboard accessible

If all steps are successful, the application is ready to use.

# Technology Stack

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy

### Backend

* FastAPI
* Pydantic

### Frontend

* Streamlit
* Plotly

### Database

* SQLite

### Utilities

* Joblib
* Logging

# Key Learnings

Through this project I gained hands-on experience with:

* Data preprocessing, feature engineering, Machine Learning model training and evaluation
* FastAPI REST API development, Pydantic validation and SQLite database integration
* Application logging and monitoring and Streamlit dashboard development
* End-to-end ML application deployment workflow

#  Author

**Shalika**

Master of Computer Applications (AI & ML)

Built as an end-to-end Machine Learning + FastAPI + Streamlit project demonstrating model development, API deployment, validation, logging, persistence, and frontend integration.
