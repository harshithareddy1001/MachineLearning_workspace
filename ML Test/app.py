import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans

st.set_page_config(page_title="Customer Segmentation", layout="centered")
st.title("🛍️ Customer Segmentation & Recommended Offers")

df = pd.read_csv("customers.csv")  # replace with your CSV

# Gender
df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female'})

# DiscountUsage
df['DiscountUsage'] = df['DiscountUsage'].replace({'N': 'Never', 'S': 'Sometimes', 'O': 'Often'})

label_encoders = {}

# Gender
le_gender = LabelEncoder()
le_gender.fit(["Male", "Female", "Other"])
label_encoders["Gender"] = le_gender

# DiscountUsage
le_discount = LabelEncoder()
le_discount.fit(["Never", "Sometimes", "Often", "Other"])
label_encoders["DiscountUsage"] = le_discount

# PreferredShoppingTime
le_time = LabelEncoder()
le_time.fit(["Morning", "Afternoon", "Evening", "Night", "Other"])
label_encoders["PreferredShoppingTime"] = le_time

# City
le_city = LabelEncoder()
# Add "Other" for unknown cities
le_city.fit(["Delhi", "Mumbai", "Bangalore", "Chennai", "Other"])
label_encoders["City"] = le_city

def safe_transform(le, series, default="Other"):
    """Encode a pandas Series using LabelEncoder.
       Unseen values are mapped to default."""
    return series.apply(lambda x: le.transform([x])[0] if x in le.classes_ else le.transform([default])[0])


numeric_cols = ["Age", "AnnualIncome", "TotalSpent", "MonthlyPurchases",
                "AvgOrderValue", "AppTimeMinutes", "DiscountUsage", "PreferredShoppingTime"]


for col in ["Gender", "City", "DiscountUsage", "PreferredShoppingTime"]:
    df[col] = safe_transform(label_encoders[col], df[col])


X = df[numeric_cols].fillna(df[numeric_cols].median())

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)


cluster_labels = {
    0: "High-Value Loyal Customers",
    1: "Value-Seeking Regular Customers",
    2: "Price-Sensitive Occasional Customers"
}

offers = {
    "High-Value Loyal Customers": "Exclusive early access + Premium membership with free express delivery",
    "Value-Seeking Regular Customers": "Festival discounts (10–15%) + Loyalty reward points",
    "Price-Sensitive Occasional Customers": "Flash sales, coupons, free shipping on minimum order"
}

st.subheader("Enter Customer Details")

with st.form("customer_form"):
    Age = st.number_input("Age", min_value=0, max_value=100, value=30)
    Gender = st.selectbox("Gender", ["Male", "Female"])
    City = st.text_input("City (e.g., Delhi, Mumbai, etc.)", value="Delhi")
    AnnualIncome = st.number_input("Annual Income", min_value=0, value=50000)
    TotalSpent = st.number_input("Total Spent", min_value=0, value=10000)
    MonthlyPurchases = st.number_input("Monthly Purchases", min_value=0, value=5)
    AvgOrderValue = st.number_input("Average Order Value", min_value=0, value=2000)
    AppTimeMinutes = st.number_input("App Time (minutes)", min_value=0, value=120)
    DiscountUsage = st.selectbox("Discount Usage", ["Never", "Sometimes", "Often"])
    PreferredShoppingTime = st.selectbox("Preferred Shopping Time", ["Morning", "Afternoon", "Evening", "Night"])

    submitted = st.form_submit_button("Predict Segment")


if submitted:
    new_customer = pd.DataFrame([{
        "Age": Age,
        "Gender": Gender,
        "City": City,
        "AnnualIncome": AnnualIncome,
        "TotalSpent": TotalSpent,
        "MonthlyPurchases": MonthlyPurchases,
        "AvgOrderValue": AvgOrderValue,
        "AppTimeMinutes": AppTimeMinutes,
        "DiscountUsage": DiscountUsage,
        "PreferredShoppingTime": PreferredShoppingTime
    }])

    # Encode categorical columns safely
    for col in ["Gender", "City", "DiscountUsage", "PreferredShoppingTime"]:
        new_customer[col] = safe_transform(label_encoders[col], new_customer[col])

    # Scale numeric features
    X_new_scaled = scaler.transform(new_customer[numeric_cols])

    # Predict cluster
    cluster = kmeans.predict(X_new_scaled)[0]
    segment = cluster_labels[cluster]
    offer = offers[segment]

    # Display results
    st.success("✅ Prediction Complete!")
    st.write(f"**Cluster:** {cluster}")
    st.write(f"**Customer Segment:** {segment}")
    st.write(f"**Recommended Offer:** {offer}")
