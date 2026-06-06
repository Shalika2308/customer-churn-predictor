#  Customer Churn Prediction System

##  Project Overview

Customer retention is one of the most important challenges faced by telecom companies.

This project predicts whether a customer is likely to leave (churn) based on demographic information, service subscriptions, billing details, and contract information.

The solution provides:

* Machine Learning Prediction Engine
* FastAPI REST API
* Streamlit Dashboard
* SQLite Prediction Storage
* Logging & Monitoring
* Input Validation
* Prediction Confidence Scoring

# 🎯 Business Problem

Customer acquisition is significantly more expensive than customer retention.

By identifying customers who are likely to churn, businesses can:

* Launch targeted retention campaigns
* Improve customer satisfaction
* Reduce revenue loss
* Increase customer lifetime value

# 🏗️ System Architecture

User
 │
 ▼
Streamlit Dashboard
 │
 ▼
FastAPI REST API
 │
 ▼
Machine Learning Model
 │
 ▼
Prediction + Confidence
 │
 ├────────► SQLite Database
 │
 └────────► Application Logs


# 📂 Project Structure

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

# 📈 Dataset

Dataset Used:

**IBM Telco Customer Churn Dataset**

Contains information about:

* Customer demographics
* Service subscriptions
* Billing details
* Contract information
* Churn status

Dataset Size:

* 7043 customer records

Target Variable:

Churn Value
0 = No Churn
1 = Churn

# ⚙️ Feature Engineering

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

# 🤖 Machine Learning Models

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

Logistic Regression

Reason:

* Higher accuracy
* Better recall
* Better overall balance

# 🌐 REST API

## Health Endpoint

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
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

# 🛡️ Validation

Implemented using Pydantic.

Validation Rules:

* Invalid Gender Rejected
* Invalid Contract Rejected
* Negative Charges Rejected
* Negative Tenure Rejected
* Missing Fields Rejected
* Incorrect Data Types Rejected

# 💾 Database Storage

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
# 📜 Logging

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

# ⚡ Failure Handling

The application is designed to remain available even if database operations fail.

Example:

```text
Prediction Generated
       │
       ▼
Database Save Fails
       │
       ▼
Error Logged
       │
       ▼
Prediction Still Returned
```
This ensures high availability and better user experience.

# 🖥️ Streamlit Dashboard

Features:

* Interactive Customer Form
* Confidence Visualization
* Prediction Status Indicators
* Prediction History
* Interactive Plotly Charts
* User Guidance Tooltips

# 🔧 Installation

## Clone Repository

```bash
git clone YOUR_REPOSITORY_URL
cd customer-churn-predictor
```
## Create Virtual Environment

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

# ▶️ Running the Application

## Terminal 1 — FastAPI

```bash
uvicorn api:app --reload
```
Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

## Terminal 2 — Streamlit

```bash
streamlit run app.py
```

Dashboard:

```text
http://localhost:8501
```

# 🧪 Testing

## Recommended

Open:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI.

Click:

```text
POST /predict
→ Try it out
→ Execute
```

# 🛠️ Technology Stack

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

# ⚠️ Current Limitations

* The model is trained on a single historical dataset and may require retraining for new customer behavior patterns.
* Predictions are based only on the features available in the IBM Telco Customer Churn Dataset.
* SQLite is suitable for development and small-scale deployments but not for large production workloads.
* The application currently supports single-customer predictions only.
* Authentication and user management are not included in the current version.

# 📚 Key Learnings

Through this project I gained hands-on experience with:

* Data preprocessing and feature engineering
* Machine Learning model training and evaluation
* FastAPI REST API development
* Pydantic validation
* SQLite database integration
* Application logging and monitoring
* Streamlit dashboard development
* End-to-end ML application deployment workflow

# 👩‍💻 Author

**Shalika**

Master of Computer Applications (AI & ML)

Built as an end-to-end Machine Learning + FastAPI + Streamlit project demonstrating model development, API deployment, validation, logging, persistence, and frontend integration.
