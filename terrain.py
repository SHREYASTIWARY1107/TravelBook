import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

# Load place data
places_data = pd.read_csv('cities_data.csv')

# Encode city names using one-hot encoding
encoder = OneHotEncoder()
city_encoded = encoder.fit_transform(places_data[['city']])

# Train random forest classifier
X = city_encoded
y = places_data['terrain']
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X, y)

# Function to preprocess user data and make predictions
def predict_preferred_terrain(user_data):
    # Extract features from user data
    last_searched_location = user_data['last_searched_location']
    
    # Encode city name
    last_searched_location_encoded = encoder.transform([[last_searched_location]])
    
    # Make prediction using trained model
    predicted_terrain = rf_classifier.predict(last_searched_location_encoded)[0]
    
    # Prepare response in JSON format
    response = {
        'user_id': user_data['user_id'],
        'preferred_terrain': predicted_terrain,
        'user_location': user_data['location']
    }
    
    return response
