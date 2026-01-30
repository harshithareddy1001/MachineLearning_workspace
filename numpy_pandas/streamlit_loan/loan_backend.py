from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from db_utils import save_application, load_applications
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# Load trained model pipeline
# -----------------------------
model = joblib.load("loan_model_pipeline.pkl")

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Loan Approval API")

# Enable CORS so Streamlit frontend can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pydantic model for request
# -----------------------------
class LoanRequest(BaseModel):
    Married: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: str
    Property_Area: str

# -----------------------------
# API endpoint: Predict loan status
# -----------------------------
@app.post("/predict")
def predict_loan(data: LoanRequest):
    # Convert to DataFrame
    X_new = pd.DataFrame([{
        "Married": data.Married,
        "Education": data.Education,
        "Self_Employed": data.Self_Employed,
        "ApplicantIncome": data.ApplicantIncome,
        "CoapplicantIncome": data.CoapplicantIncome,
        "LoanAmount": data.LoanAmount,
        "Loan_Amount_Term": data.Loan_Amount_Term,
        "Credit_History": 1 if data.Credit_History=="Yes" else 0,
        "Property_Area": data.Property_Area
    }])

    # Predict
    prediction = model.predict(X_new)[0]

    # Save to DB
    X_new['Prediction'] = prediction
    save_application(X_new)

    # Return result
    return {"prediction": int(prediction)}

# -----------------------------
# API endpoint: Get all applications
# -----------------------------
@app.get("/applications")
def get_applications():
    df = load_applications()
    if df.empty:
        return {"applications": []}
    return {"applications": df.to_dict(orient="records")}
