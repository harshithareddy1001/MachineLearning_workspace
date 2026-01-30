import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Loan Approval Predictor 💰", page_icon="🏦", layout="wide")
st.title("🏦 Loan Approval Prediction Portal")
st.markdown("Fill in the details below to see if your loan is likely to be approved.")

# -----------------------------
# Backend URL
# -----------------------------
API_URL = "http://127.0.0.1:8000"  # FastAPI backend

# -----------------------------
# User Inputs
# -----------------------------
st.subheader("Personal Information")
married = st.selectbox("Married", ["No", "Yes"])
education = st.selectbox("Education", ["Not Graduate", "Graduate"])
self_employed = st.selectbox("Self Employed", ["No", "Yes"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

st.subheader("Financial Information")
applicant_income = st.number_input("Applicant Income", min_value=0, value=2500)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0, value=0)
loan_amount = st.number_input("Loan Amount", min_value=0, value=100)
loan_amount_term = st.number_input("Loan Amount Term (in months)", min_value=0, value=360)
credit_history = st.selectbox("Credit History", ["No", "Yes"])

# -----------------------------
# Predict Button
# -----------------------------
if st.button("Predict Loan Status"):
    # Prepare data
    data = {
        "Married": married,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    # Call backend API
    response = requests.post(f"{API_URL}/predict", json=data)
    if response.status_code == 200:
        prediction = response.json()["prediction"]

        # Show colorful result
        if prediction == 1:
            st.markdown(
                "<div style='background-color:#d4edda;padding:20px;border-radius:10px;"
                "text-align:center;color:#155724;font-size:24px;'>"
                "✅ Congratulations! Your loan is likely to be approved! 🎉💰</div>",
                unsafe_allow_html=True
            )
            st.balloons()
        else:
            st.markdown(
                "<div style='background-color:#f8d7da;padding:20px;border-radius:10px;"
                "text-align:center;color:#721c24;font-size:24px;'>"
                "❌ Sorry, your loan may not be approved. 😞</div>",
                unsafe_allow_html=True
            )
    else:
        st.error("Error connecting to backend API!")

# -----------------------------
# Show past applications
# -----------------------------
show_db = st.sidebar.checkbox("Show past loan applications", value=True)
if show_db:
    response = requests.get(f"{API_URL}/applications")
    if response.status_code == 200:
        applications = response.json()["applications"]
        if applications:
            df = pd.DataFrame(applications)

            # Pie chart for approved vs rejected
            status_counts = df['Prediction'].value_counts().rename({1: 'Approved', 0: 'Rejected'})
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                color=status_counts.index,
                color_discrete_map={'Approved':'green', 'Rejected':'red'},
                hole=0.4,
                title="Loan Approval vs Rejection"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Show tables
            st.markdown("### ✅ Approved Loans")
            st.dataframe(df[df['Prediction']==1])
            st.markdown("### ❌ Rejected Loans")
            st.dataframe(df[df['Prediction']==0])

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download All Applications as CSV", csv, "loan_data.csv", "text/csv")
        else:
            st.info("No applications in the database yet.")
    else:
        st.error("Error loading applications from backend!")
