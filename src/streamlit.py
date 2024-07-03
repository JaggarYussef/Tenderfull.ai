import streamlit as st
import requests

# The URL of your FastAPI endpoint
API_URL = "http://localhost:8000/user_input/"  # Adjust this to match your FastAPI server address

st.title("User Input Submission")

# Create input fields
query = st.text_area("Enter your query:")
email = st.text_input("Enter your email:")
score = st.slider("Select a score:", 0.0, 1.0, 0.5, 0.01)

# Prepare the data
data = {
    "query": query,
    "email": email,
    "score": score
}

# Create a submit button
if st.button("Submit"):
    # Send POST request to the API
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Successfully submitted! ID: {result['id']}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Display the current data
st.subheader("Current Data:")
st.json(data)