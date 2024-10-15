import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the pre-trained pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

# List of teams and cities
teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
         'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']

cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 
          'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 
          'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 
          'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 
          'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 
          'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 
          'Cardiff', 'Christchurch', 'Trinidad']

# Title for the app
st.title('Cricket Score Predictor')

# Input columns for teams and city
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

city = st.selectbox('Select city', sorted(cities))

# Input columns for score, overs, wickets
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score', min_value=0, step=1, format="%d")
with col4:
    overs = st.number_input('Overs done (works for over >5)', min_value=5, max_value=20, step=1, format="%d")
with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=10, step=1, format="%d")

# Input for last 5 overs
last_five = st.number_input('Runs scored in last 5 overs', min_value=0, step=1, format="%d")

# Predict button
if st.button('Predict Score'):
    # Calculations for additional inputs
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs if overs > 0 else 0

    # Create a DataFrame with the input values
    input_df = pd.DataFrame(
        {'batting_team': [batting_team], 'bowling_team': [bowling_team],
         'city': [city], 'current_score': [current_score], 'balls_left': [balls_left],
         'wickets_left': [wickets_left], 'crr': [crr], 'last_five': [last_five]})
    
    # Ensure the DataFrame is in the correct format before prediction
    try:
        result = pipe.predict(input_df)
        st.header("Predicted Score - " + str(int(result[0])))
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
