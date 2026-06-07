import streamlit as st
import requests
import sqlite3
import pandas as pd
import plotly.express as px
from src.database import create_database

create_database()
#page configuration
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide"
)

#css
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    padding-top: 0.5rem;
}

.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
    margin-bottom: 1rem;
}

.card {
    padding: 1.2rem;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    margin-bottom: 1rem;
}

.stButton > button {
    width:100%;
    height:55px;
    border-radius:14px;
    font-size:18px;
    font-weight:600;
    border:none;
    transition:all .25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    border-radius:16px;
    padding:16px;
    border:1px solid rgba(255,255,255,.12);
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">

# 📊 Customer Churn Prediction System

### AI-Powered Customer Retention Analytics

Predict customer churn using machine learning, confidence scoring,
real-time API predictions, and historical prediction tracking.

</div>
""", unsafe_allow_html=True)

st.divider()

st.info(
    "💡 Hover over the ⓘ icons next to each field for explanations."
)

#KPI cards 
k1, k2, k3 = st.columns(3)

with k1:
    st.metric(
        "Prediction API",
        "Online"
    )

with k2:
    st.metric(
        "Model",
        "Logistic Regression"
    )

with k3:
    st.metric(
        "Backend",
        "Connected"
    )

#customer information section

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Customer Profile")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"],
        help="Customer's gender."
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        ["Yes", "No"],
        help="Whether the customer is 65 years or older."
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"],
        help="Whether the customer has a spouse or partner."
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"],
        help="Whether the customer has children or dependents."
    )

    tenure_months = st.number_input(
        "How long has the customer stayed with the company? (Months)",
         min_value=0,
         max_value=72,
         value=12,
         help="Total number of months the customer has been subscribed."
    )
    
#service details section
with col2:

    st.markdown("### Service Details")

    phone_service = st.selectbox(
    "Phone Service",
    ["Yes", "No"],
    help="Whether the customer subscribes to phone services."
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"],
        help="Whether the customer has multiple phone lines."
    )

    internet_service = st.selectbox(
        "Internet Connection Type",
        ["DSL", "Fiber optic", "No"],
        help="Type of internet service used by the customer."
     )

    contract = st.selectbox(
       "Subscription Contract Type",
       ["Month-to-month", "One year", "Two year"],
       help="""
       Month-to-month: Customer can cancel anytime.

       One year: Customer commits for 1 year.

        Two year: Customer commits for 2 years.
         """
    )

    payment_method = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ],
    help="How the customer pays their bills."
)
    
#security and streaming section
st.divider()

st.markdown("### Security & Streaming")

col3, col4 = st.columns(2)

with col3:

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"],
        help="Internet security protection service."
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"],
        help="Cloud or online backup service."
    )

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"],
        help="Protection plan for devices."
    )



with col4:

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"],
        help="Access to technical support services."
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"],
        help="Subscription to TV streaming services."
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"],
        help="Subscription to movie streaming services."
    )

#billing section
st.divider()

st.markdown("### Billing Information")

col5, col6 = st.columns(2)

with col5:

     monthly_charges = st.number_input(
        "Monthly Bill Amount ($)",
        min_value=0.0,
        value=80.0,
        help="Average amount charged each month."
        )

with col6:

    total_charges = st.number_input(
            "Total Amount Paid So Far ($)",
                min_value=0.0,
                value=1000.0,
                help="Total amount the customer has paid since joining."
            )
    paperless_billing = st.selectbox(
                "Paperless Billing",
                ["Yes", "No"],
                help="Whether bills are received electronically."
            )

st.divider()
 # prediction button
if st.button("🔮 Predict Churn", use_container_width=True):

    #Converts form data into JSON.
    payload = {
        "Gender": gender,
        "Senior_Citizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "Tenure_Months": tenure_months,
        "Phone_Service": phone_service,
        "Multiple_Lines": multiple_lines,
        "Internet_Service": internet_service,
        "Online_Security": online_security,
        "Online_Backup": online_backup,
        "Device_Protection": device_protection,
        "Tech_Support": tech_support,
        "Streaming_TV": streaming_tv,
        "Streaming_Movies": streaming_movies,
        "Contract": contract,
        "Paperless_Billing": paperless_billing,
        "Payment_Method": payment_method,
        "Monthly_Charges": monthly_charges,
        "Total_Charges": total_charges
    }

    try:

        with st.spinner(
                "Analyzing customer behavior..."
            ):
                #Sends user data to FastAPI.
                response = requests.post(
                     "https://customer-churn-predictor-3prs.onrender.com/predict",
                    json=payload,
                  timeout=10
                )
                
                #error handling
                if response.status_code != 200:
                    st.error("Prediction request failed")
                    st.stop()

                result = response.json()

        st.divider()

        st.subheader("Prediction Result")

        if result["prediction"] == "Churn":

            st.error(
                "🔴 High Risk Customer (Likely To Churn)"
            )

            st.warning(
                "Consider customer retention strategies."
            )

        else:

            st.success(
                "🟢 Customer Likely To Stay"
            )

            st.info(
                "Customer appears to be relatively stable."
            )

           
        #confidence score

        confidence_percent = result["confidence"] * 100
        
        if confidence_percent >= 80:
              st.success("High confidence prediction")
        elif confidence_percent >= 60:
               st.warning("Moderate confidence prediction")
        else:
               st.info("Low confidence prediction")

       #metrices
        st.metric(
            "Prediction",
            result["prediction"]
          )


        st.metric(
            "Confidence Score",
             f"{confidence_percent:.2f}%"
             )

        st.progress(
           result["confidence"]
        )

    except Exception as e:

        st.error(
            f"API Error: {str(e)}"
        )
        
st.divider()

st.subheader("📜 Recent Predictions")

#prediction history
try:

    conn = sqlite3.connect(
        "database/predictions.db"
    )

    history = pd.read_sql(
        """
        SELECT *
        FROM predictions
        ORDER BY id DESC
        LIMIT 10
        """,
        conn
    )

    if not history.empty:

        display_history = history[
            [
                "prediction",
                "confidence",
                "created_at"
            ]
        ].copy()

        display_history.columns = [
            "Prediction",
            "Confidence",
            "Timestamp"
        ]

        fig = px.histogram(
            display_history,
            x="Prediction",
            title="Prediction Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            display_history,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("📄 View Stored Input Data"):

        st.dataframe(
            history[
                [
                    "id",
                    "input_data"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
    conn.close()

except Exception as e:

    st.info(
        f"No prediction history available. ({str(e)})"
    )
    
st.markdown("---")

st.caption(
    "Built with Streamlit • FastAPI • Scikit-Learn • SQLite"
)