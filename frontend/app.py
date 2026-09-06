
import streamlit as st
import requests
import pandas as pd
import json
import numpy as np
import io

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction App")
st.markdown("Enter product and store details to predict sales, or upload a CSV for batch predictions.")

# Flask API URL (assuming it runs within the same Docker network)
FLASK_API_URL = "http://backend:7860/v1/predict"
FLASK_BATCH_API_URL = "http://backend:7860/v1/predictbatch"
FLASK_HOME_URL = "http://backend:7860/"


# Test Flask API connection
try:
    response = requests.get(FLASK_HOME_URL)
    if response.status_code == 200:
        st.sidebar.success(f"Backend API Status: {response.json().get('message', 'Running')}")
    else:
        st.sidebar.error(f"Backend API Status: Error {response.status_code}")
except requests.exceptions.ConnectionError:
    st.sidebar.error("Backend API Status: Not connected. Ensure backend service is running.")


# Input fields for online prediction
st.header("Online Prediction")
st.subheader("Enter Product and Store Details:")

# Collect user inputs
col1, col2 = st.columns(2)

with col1:
    product_weight = st.number_input("Product Weight", min_value=0.0, max_value=50.0, value=12.66, step=0.1)
    product_mrp = st.number_input("Product MRP", min_value=0.0, max_value=500.0, value=117.08, step=0.01)
    store_establishment_year = st.number_input("Store Establishment Year", min_value=1900, max_value=2024, value=2009, step=1)
    product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, step=0.001, format="%.3f")

with col2:
    product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    product_type = st.selectbox("Product Type", ["Frozen Foods", "Dairy", "Canned", "Baking Goods", "Health and Hygiene", "Meat", "Snack Foods", "Soft Drinks", "Breads", "Hard Drinks", "Others", "Starchy Foods", "Breakfast", "Seafood", "Fruits and Vegetables", "Household"])
    store_id = st.selectbox("Store ID", ["OUT004", "OUT001", "OUT003", "OUT002"])
    store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
    store_location_city_type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1", "Food Mart"])

# Prepare payload for API call
payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_Type": product_type,
    "Product_MRP": product_mrp,
    "Store_Id": store_id,
    "Store_Establishment_Year": store_establishment_year,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
}

if st.button("Predict Sales (Online)"):
    try:
        response = requests.post(FLASK_API_URL, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Product Store Sales Total: ${result['Predicted_Product_Store_Sales_Total']:.2f}")
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Ensure it is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("---")

# Batch prediction section
st.header("Batch Prediction")
st.subheader("Upload a CSV file for multiple predictions:")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    if st.button("Predict Sales (Batch)"):
        try:
            # Read the CSV file into a pandas DataFrame
            file_contents = uploaded_file.getvalue()
            data = pd.read_csv(io.BytesIO(file_contents))

            # Send the CSV file to the batch prediction endpoint
            files = {'file': (uploaded_file.name, file_contents, 'text/csv')}
            batch_response = requests.post(FLASK_BATCH_API_URL, files=files, timeout=60)

            if batch_response.status_code == 200:
                predictions_data = batch_response.json().get('predictions')
                if predictions_data:
                    predictions_df = pd.DataFrame(predictions_data)
                    st.success("Batch predictions generated successfully!")
                    st.dataframe(predictions_df)
                else:
                    st.error("No predictions received from batch API.")
            else:
                st.error(f"Error from Batch API: {batch_response.status_code} - {batch_response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API for batch predictions. Ensure it is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred during batch prediction: {e}")
