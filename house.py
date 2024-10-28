# Import necessary libraries
import streamlit as st
import numpy as np
import pickle

# Load the pre-trained model
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit app interface
st.title('🏡 House Price Prediction App')

st.write("""
### Enter the details below to predict the house price:
""")

# Get user input for all necessary features
longitude = st.number_input('Longitude', min_value=-119.0, max_value=-114.0, value=-118.0)
latitude = st.number_input('Latitude', min_value=33.0, max_value=38.0, value=34.0)
housing_median_age = st.number_input('Housing Median Age', min_value=0, value=20)
total_rooms = st.number_input('Total Rooms', min_value=1, value=6)
total_bedrooms = st.number_input('Total Bedrooms', min_value=1, value=3)
population = st.number_input('Population', min_value=1, value=5000)
households = st.number_input('Households', min_value=1, value=1500)
median_income = st.number_input('Median Income', min_value=0.0, value=3.0)

# One-hot encoding for ocean proximity
ocean_proximity = st.selectbox('Ocean Proximity', ('INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'))
ocean_proximity_INLAND = int(ocean_proximity == 'INLAND')
ocean_proximity_ISLAND = int(ocean_proximity == 'ISLAND')
ocean_proximity_NEAR_BAY = int(ocean_proximity == 'NEAR BAY')
ocean_proximity_NEAR_OCEAN = int(ocean_proximity == 'NEAR OCEAN')

# Calculate derived features
rooms_per_household = total_rooms / households if households > 0 else 0
bedrooms_per_room = total_bedrooms / total_rooms if total_rooms > 0 else 0
population_per_household = population / households if households > 0 else 0

# Button to predict
if st.button('Predict House Price'):
    # Prepare input data for prediction
    input_data = np.array([[longitude, latitude, housing_median_age, total_rooms, total_bedrooms,
                            population, households, median_income,
                            ocean_proximity_INLAND, ocean_proximity_ISLAND,
                            ocean_proximity_NEAR_BAY, ocean_proximity_NEAR_OCEAN,
                            rooms_per_household, bedrooms_per_room, population_per_household]])

    # Predict the price using the loaded model
    predicted_price = model.predict(input_data)

    # Display the prediction
    st.success(f'The predicted house price is: ${predicted_price[0]:,.2f}')
