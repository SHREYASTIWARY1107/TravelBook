from flask import Flask, jsonify, request
import pandas as pd
from recommendation import recommend_places

app = Flask(__name__)

# Load places data (assuming you already have this)
places_data = pd.read_csv('places_data.csv')

# Function to calculate distance (mock implementation)
def calculate_distance(location1, location2):
    # Mock implementation: Simply return a constant value for demonstration
    return 10  # Replace with actual distance calculation

# Function to recommend places based on user preferences
def get_recommendations_for_user(user_data):
    # Extract user information from JSON input
    user_id = user_data['user_id']
    location = user_data['location']
    preferred_terrain = user_data['preferred_terrain']
    
    # Filter places by preferred terrain
    filtered_places = places_data[places_data['terrain'] == preferred_terrain]
    
    # Calculate distance for each place and add to DataFrame
    filtered_places['distance'] = filtered_places['location'].apply(lambda x: calculate_distance(location, x))
    
    # Rank places by distance
    ranked_places = filtered_places.sort_values(by='distance')
    
    return ranked_places[['place_name', 'distance']].to_dict('records')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    user_data = request.json
    recommendations = get_recommendations_for_user(user_data)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
