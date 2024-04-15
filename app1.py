from flask import Flask, request, jsonify
import requests
from terrain import predict_preferred_terrain

app = Flask(__name__)

# Firebase URL
firebase_url = "YOUR_FIREBASE_URL_HERE"

def post_to_firebase(user_id, prediction):
    # Firebase endpoint
    firebase_endpoint = f"{firebase_url}/users/{user_id}.json"

    # POST data to Firebase
    response = requests.patch(firebase_endpoint, json=prediction)

    # Check if data was successfully posted
    if response.status_code == 200:
        print("Data posted to Firebase successfully!")
    else:
        print("Error posting data to Firebase!")

@app.route('/predict', methods=['POST'])
def predict():
    # Get user data from JSON request
    user_data = request.get_json()

    # Call predict_preferred_terrain function
    prediction = predict_preferred_terrain(user_data)

    # Post prediction to Firebase
    post_to_firebase(user_data['user_id'], prediction)

    # Return prediction as JSON response
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)
