
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("superkart_sales_prediction_model.joblib")

model = load_model()

# Streamlit UI
st.title("Superkart Sales Prediction App")

st.write(
    "This tool predicts the total sales of a product in a store "
    "based on product and store details."
)

st.subheader("Enter the product and store details:")

# -----------------------------
# Product Details
# -----------------------------

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.65,
    step=0.01
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.068,
    step=0.001
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=147.03,
    step=0.01
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

# -----------------------------
# Store Details
# -----------------------------

store_id = st.selectbox(
    "Store ID",
    ["OUT004", "OUT001", "OUT003", "OUT002"]
)

store_size = st.selectbox(
    "Store Size",
    ["Medium", "High", "Small"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 2", "Tier 1", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type2",
        "Supermarket Type1",
        "Departmental Store",
        "Food Mart"
    ]
)

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1987,
    max_value=2009,
    value=2009,
    step=1
)

# -----------------------------
# Create input DataFrame
# -----------------------------

input_data = pd.DataFrame([{
    "Product_Weight": product_weight,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Establishment_Year": store_establishment_year,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Type": product_type,
    "Store_Id": store_id,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type
}])

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Sales"):

    prediction = model.predict(input_data)

    predicted_sales = prediction[0]

    st.success(
        f"Predicted Product Store Sales Total: {predicted_sales:.2f}"
    )
