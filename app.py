from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime
from scraper import load_rental_data, scrape_rental_data, LOCATIONS
import json

app = Flask(__name__)

# Initialize model
model = LogisticRegression(max_iter=1000)
scaler = StandardScaler()

def find_similar_listings(rental_data, area, bedrooms, location, num_persons):
    similar_listings = []
    
    # Define ranges for similarity (more lenient)
    area_range = 500  # Increased from 200 to 500 sq ft
    bedroom_range = 2  # Increased from 1 to 2 bedrooms
    
    print(f"Searching for properties in {location} with area {area} and {bedrooms} bedrooms")
    print(f"Total listings available: {len(rental_data)}")
    
    for listing in rental_data:
        # Check if location matches
        if listing['location'] != location:
            continue
            
        # Check if area is within range
        if abs(listing['area'] - area) > area_range:
            continue
            
        # Check if bedrooms are within range
        if abs(listing['bedrooms'] - bedrooms) > bedroom_range:
            continue
            
        # Calculate similarity score (more lenient scoring)
        area_diff = min(abs(listing['area'] - area) / area, 1)
        bedroom_diff = min(abs(listing['bedrooms'] - bedrooms) / bedrooms, 1)
        similarity_score = 1 - (area_diff + bedroom_diff) / 2
        
        # Add to similar listings if similarity score is good enough (lowered threshold)
        if similarity_score > 0.3:  # Lowered from 0.5 to 0.3
            listing['similarity_score'] = similarity_score
            similar_listings.append(listing)
    
    print(f"Found {len(similar_listings)} similar listings")
    
    # Sort by similarity score and limit to top 5
    similar_listings.sort(key=lambda x: x['similarity_score'], reverse=True)
    return similar_listings[:5]

def initialize_model():
    # Load or scrape rental data
    rental_data = load_rental_data()
    if not rental_data:
        print("No existing data found. Scraping new data...")
        rental_data = scrape_rental_data()
    
    if not rental_data:
        print("Failed to get rental data. Using sample data.")
        # Fallback to sample data with more entries
        rental_data = [
            {'location': 'Anna Nagar', 'area': 1000, 'bedrooms': 2, 'rent': 20000, 'source': '99acres'},
            {'location': 'T Nagar', 'area': 800, 'bedrooms': 2, 'rent': 18000, 'source': '99acres'},
            {'location': 'Velachery', 'area': 1200, 'bedrooms': 3, 'rent': 25000, 'source': '99acres'},
            {'location': 'Adyar', 'area': 600, 'bedrooms': 1, 'rent': 12000, 'source': '99acres'},
            {'location': 'Anna Nagar', 'area': 1500, 'bedrooms': 3, 'rent': 30000, 'source': 'Magicbricks'},
            {'location': 'T Nagar', 'area': 1000, 'bedrooms': 2, 'rent': 22000, 'source': 'Magicbricks'},
            {'location': 'Velachery', 'area': 900, 'bedrooms': 2, 'rent': 16000, 'source': 'Magicbricks'},
            {'location': 'Adyar', 'area': 800, 'bedrooms': 2, 'rent': 15000, 'source': 'Magicbricks'},
            {'location': 'Anna Nagar', 'area': 2000, 'bedrooms': 4, 'rent': 40000, 'source': '99acres'},
            {'location': 'T Nagar', 'area': 1200, 'bedrooms': 3, 'rent': 28000, 'source': '99acres'},
            {'location': 'Velachery', 'area': 1500, 'bedrooms': 3, 'rent': 25000, 'source': '99acres'},
            {'location': 'Adyar', 'area': 1000, 'bedrooms': 2, 'rent': 20000, 'source': '99acres'}
        ]
        # Save sample data
        os.makedirs('data', exist_ok=True)
        with open('data/rental_data.json', 'w') as f:
            json.dump(rental_data, f)
    
    # Process data for model training
    X = []
    y = []
    for listing in rental_data:
        location_encoded = LOCATIONS.get(listing['location'], 0)
        X.append([
            listing['area'],
            listing['bedrooms'],
            2,  # Default number of persons
            location_encoded
        ])
        
        # Convert rent to range category
        rent = listing['rent']
        if rent < 15000:
            y.append(0)
        elif rent < 25000:
            y.append(1)
        elif rent < 35000:
            y.append(2)
        else:
            y.append(3)
    
    X = np.array(X)
    y = np.array(y)
    
    global scaler, model
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    model.fit(X_scaled, y)

@app.route('/')
def home():
    return render_template('index.html', locations=LOCATIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        area = float(data['area'])
        bedrooms = int(data['bedrooms'])
        num_persons = int(data['num_persons'])
        location = data['location']

        # Load rental data
        rental_data = load_rental_data()
        if not rental_data:
            rental_data = scrape_rental_data()

        # Find similar listings
        similar_listings = find_similar_listings(rental_data, area, bedrooms, location, num_persons)

        # Format similar listings for response
        formatted_listings = []
        for listing in similar_listings:
            formatted_listings.append({
                'location': listing['location'],
                'area': listing['area'],
                'bedrooms': listing['bedrooms'],
                'rent': listing['rent'],
                'source': listing.get('source', 'Unknown'),
                'similarity_score': round(listing['similarity_score'] * 100, 1)
            })

        # Make prediction using the model
        location_encoded = LOCATIONS.get(location, 0)
        input_data = np.array([[area, bedrooms, num_persons, location_encoded]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]

        # Convert prediction to rent range
        if prediction == 0:
            rent_range = "₹10,000 - ₹15,000"
            annual_cost = "₹1,20,000 - ₹1,80,000"
        elif prediction == 1:
            rent_range = "₹15,000 - ₹25,000"
            annual_cost = "₹1,80,000 - ₹3,00,000"
        elif prediction == 2:
            rent_range = "₹25,000 - ₹35,000"
            annual_cost = "₹3,00,000 - ₹4,20,000"
        else:
            rent_range = "₹35,000+"
            annual_cost = "₹4,20,000+"

        # Get current month for seasonal advice
        current_month = datetime.now().month
        if current_month in [6, 7, 8]:  # Summer vacation time
            season_advice = "Current season: Peak rental season due to academic year start. Prices might be higher."
        elif current_month in [11, 12, 1]:  # Winter
            season_advice = "Current season: Off-peak season. Better chances of finding good deals."
        else:
            season_advice = "Current season: Moderate rental season. Regular market rates apply."

        return jsonify({
            'success': True,
            'similar_listings': formatted_listings,
            'prediction': {
                'monthly_range': rent_range,
                'annual_cost': annual_cost
            },
            'seasonal_advice': season_advice
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/refresh_data', methods=['POST'])
def refresh_data():
    try:
        new_data = scrape_rental_data()
        initialize_model()
        return jsonify({
            'success': True,
            'message': f'Successfully refreshed data with {len(new_data)} new listings'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    initialize_model()
    app.run(debug=True) 