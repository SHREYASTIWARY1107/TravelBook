from flask import Flask, request, jsonify
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

app = Flask(__name__)

# Firebase URL
firebase_url = "YOUR_FIREBASE_URL_HERE"

# Define MultiLabelBinarizer globally
mlb = MultiLabelBinarizer()

# Define model globally
model = None

def get_past_predicted_terrains(user_id):
    firebase_endpoint = f"{firebase_url}/users/{user_id}.json"
    response = requests.get(firebase_endpoint)
    if response.status_code == 200:
        data = response.json()
        if data and 'predicted_terrains' in data:
            return data['predicted_terrains']
    return []

def train_model(user_id, past_predicted_terrains):
    # Convert terrains to binary labels
    terrains_encoded = mlb.fit_transform(past_predicted_terrains)
    
    # Train model (example with RandomForestClassifier)
    X = terrains_encoded[:-1]  # Use all past terrains except the latest one
    y = terrains_encoded[1:]   # Predict the next terrain based on past terrains
    global model
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # Save or serialize the trained model (optional)
    return model

def predict_preferred_terrain_based_on_past(user_id, latest_predicted_terrain):
    # Retrieve past predicted terrains
    past_predicted_terrains = get_past_predicted_terrains(user_id)
    
    # Train model if past predicted terrains exist
    if past_predicted_terrains:
        # Train model
        train_model(user_id, past_predicted_terrains)
        
        # Convert latest predicted terrain to binary labels
        latest_encoded = mlb.transform([latest_predicted_terrain])
        
        # Make prediction
        next_predicted_terrain_encoded = model.predict(latest_encoded)
        
        # Decode prediction
        next_predicted_terrain = mlb.inverse_transform(next_predicted_terrain_encoded)
        return next_predicted_terrain[0]
    else:
        return None

@app.route('/predict_based_on_past', methods=['POST'])
def predict_based_on_past():
    # Get user data from JSON request
    user_data = request.get_json()
    
    # Get latest predicted terrain from user data
    latest_predicted_terrain = user_data.get('latest_predicted_terrain')
    
    # Predict preferred terrain based on past predicted terrains
    prediction = predict_preferred_terrain_based_on_past(user_data['user_id'], latest_predicted_terrain)
    
    # Return prediction as JSON response
    return jsonify({'next_predicted_terrain': prediction})

if __name__ == '__main__':
    app.run(debug=True)
