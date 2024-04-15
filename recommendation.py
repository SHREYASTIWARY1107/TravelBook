import pandas as pd

# Load places data
places_data = pd.read_csv('places_data.csv')  # Assuming you have a CSV file containing places data

# Function to calculate distance (mock implementation)
def calculate_distance(location1, location2):
    # Mock implementation: Simply return a constant value for demonstration
    return 10  # Replace with actual distance calculation

# Function to recommend places based on user preferences
def recommend_places(user_data):
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
