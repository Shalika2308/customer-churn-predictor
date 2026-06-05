from fastapi import FastAPI
import pandas as pd
import joblib
from src.database import save_prediction
import logging
from enum import Enum
from pydantic import BaseModel, Field
app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0"
)

# =========================
# Load Model
# =========================

model = joblib.load("models/model.pkl")
columns = joblib.load("models/columns.pkl")

print("Model loaded successfully!")
print("Columns loaded successfully!")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Customer Churn API Started")
class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"


class YesNoEnum(str, Enum):
    Yes = "Yes"
    No = "No"


class ContractEnum(str, Enum):
    MonthToMonth = "Month-to-month"
    OneYear = "One year"
    TwoYear = "Two year"


class InternetServiceEnum(str, Enum):
    DSL = "DSL"
    Fiber = "Fiber optic"
    No = "No"


class PaymentMethodEnum(str, Enum):
    ElectronicCheck = "Electronic check"
    MailedCheck = "Mailed check"
    BankTransfer = "Bank transfer (automatic)"
    CreditCard = "Credit card (automatic)"
    
class CustomerData(BaseModel):

    Gender: GenderEnum

    Senior_Citizen: YesNoEnum
    Partner: YesNoEnum
    Dependents: YesNoEnum

    Tenure_Months: int = Field(
        ...,
        ge=0,
        le=72
    )

    Phone_Service: YesNoEnum
    Multiple_Lines: str

    Internet_Service: InternetServiceEnum

    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str

    Streaming_TV: str
    Streaming_Movies: str

    Contract: ContractEnum

    Paperless_Billing: YesNoEnum

    Payment_Method: PaymentMethodEnum

    Monthly_Charges: float = Field(
        ...,
        ge=0
    )

    Total_Charges: float = Field(
        ...,
        ge=0
    )
    
@app.get("/")
def root():
    return {
        "message": "Customer Churn Prediction API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/predict")
def predict(data: CustomerData):

    try:

        logging.info("Prediction request received")

        # Convert request into dataframe
        input_data = {
            "Gender": data.Gender,
            "Senior Citizen": data.Senior_Citizen,
            "Partner": data.Partner,
            "Dependents": data.Dependents,
            "Tenure Months": data.Tenure_Months,
            "Phone Service": data.Phone_Service,
            "Multiple Lines": data.Multiple_Lines,
            "Internet Service": data.Internet_Service,
            "Online Security": data.Online_Security,
            "Online Backup": data.Online_Backup,
            "Device Protection": data.Device_Protection,
            "Tech Support": data.Tech_Support,
            "Streaming TV": data.Streaming_TV,
            "Streaming Movies": data.Streaming_Movies,
            "Contract": data.Contract,
            "Paperless Billing": data.Paperless_Billing,
            "Payment Method": data.Payment_Method,
            "Monthly Charges": data.Monthly_Charges,
            "Total Charges": data.Total_Charges
        }

        df = pd.DataFrame([input_data])

        # =========================
        # Feature Engineering
        # =========================

        df["ChargesPerMonth"] = (
            df["Total Charges"] /
            (df["Tenure Months"] + 1)
        )

        df["IsLongTermCustomer"] = (
            df["Tenure Months"] > 24
        ).astype(int)

        # =========================
        # One Hot Encoding
        # =========================

        df = pd.get_dummies(df)

        # =========================
        # Match Training Columns
        # =========================

        df = df.reindex(
            columns=columns,
            fill_value=0
        )

        # =========================
        # Prediction
        # =========================

        prediction = model.predict(df)[0]

        confidence = float(
            model.predict_proba(df)[0].max()
        )

        result = (
            "Churn"
            if prediction == 1
            else "No Churn"
        )

        logging.info(
            f"Prediction={result}, Confidence={confidence:.4f}"
        )

        try:

            save_prediction(
            data.Tenure_Months,
            data.Monthly_Charges,
            data.Contract,
            result,
            confidence
          )

        except Exception as db_error:

            logging.error(
                f"Database Save Error: {str(db_error)}"
                 )

        return {
            "prediction": result,
            "confidence": round(confidence, 4)
        }

    except Exception as e:

        logging.error(f"Prediction Error: {str(e)}")

        return {
            "error": str(e)
        }