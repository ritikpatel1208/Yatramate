from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Real Location Coordinates added for Interactive Maps
TOURISM_DATA = {
    "jaipur": {
        "city_name": "Jaipur, Rajasthan",
        "center": [26.9124, 75.7873], # Jaipur Center
        "heritage": [
            {"name": "Amber Fort", "lat": 26.9855, "lng": 75.8513, "type": "Heritage", "time": "3 hrs", "cost": 200, "is_offbeat": False},
            {"name": "Panna Meena ka Kund", "lat": 26.9880, "lng": 75.8539, "type": "Hidden Gem", "time": "1 hr", "cost": 0, "is_offbeat": True},
            {"name": "Anokhi Printing Museum", "lat": 26.9912, "lng": 75.8510, "type": "Culture", "time": "2 hrs", "cost": 100, "is_offbeat": True}
        ],
        "adventure": [
            {"name": "Nahargarh Biological Park", "lat": 26.9950, "lng": 75.8100, "type": "Adventure", "time": "3 hrs", "cost": 50, "is_offbeat": True},
            {"name": "Hawa Mahal Viewpoint", "lat": 26.9239, "lng": 75.8267, "type": "Sightseeing", "time": "1.5 hrs", "cost": 50, "is_offbeat": False}
        ],
        "stays": [
            {"name": "Vedic Eco Homestay (Local Vendor)", "lat": 26.9200, "lng": 75.7900, "price": 1200, "rating": "4.8 ★", "type": "Homestay"},
            {"name": "Heritage Haveli Stay", "lat": 26.9300, "lng": 75.8000, "price": 3500, "rating": "4.6 ★", "type": "Hotel"}
        ]
    },
    "manali": {
        "city_name": "Manali, Himachal Pradesh",
        "center": [32.2432, 77.1892], # Manali Center
        "heritage": [
            {"name": "Naggar Castle", "lat": 32.1158, "lng": 77.1706, "type": "Culture", "time": "2.5 hrs", "cost": 100, "is_offbeat": True},
            {"name": "Hadimba Temple Forest", "lat": 32.2483, "lng": 77.1804, "type": "Nature", "time": "1.5 hrs", "cost": 0, "is_offbeat": False}
        ],
        "adventure": [
            {"name": "Solang Valley Adventure Spot", "lat": 32.3166, "lng": 77.1578, "type": "Extreme", "time": "4 hrs", "cost": 1800, "is_offbeat": False},
            {"name": "Sethan Offbeat Igloo Village", "lat": 32.2030, "lng": 77.2250, "type": "Hidden Gem", "time": "4 hrs", "cost": 500, "is_offbeat": True}
        ],
        "stays": [
            {"name": "Riverside Wooden Cottage", "lat": 32.2400, "lng": 77.1850, "price": 1800, "rating": "4.9 ★", "type": "Homestay"},
            {"name": "Backpacker Hostel Hub", "lat": 32.2450, "lng": 77.1870, "price": 700, "rating": "4.5 ★", "type": "Hostel"}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    data = request.get_json() or {}
    city_key = data.get('city', 'jaipur').lower()
    category = data.get('category', 'heritage')
    days = int(data.get('days', 1))

    city_info = TOURISM_DATA.get(city_key, TOURISM_DATA['jaipur'])
    places = city_info.get(category, city_info['heritage'])
    stays = city_info['stays']

    # Smart Budget Calculation
    total_entry_cost = sum(p['cost'] for p in places)
    avg_stay_cost = stays[0]['price'] * days
    est_total_budget = total_entry_cost + avg_stay_cost + (days * 500)

    return jsonify({
        "city": city_info['city_name'],
        "center": city_info['center'],
        "places": places,
        "stays": stays,
        "summary": {
            "days": days,
            "places_count": len(places),
            "estimated_budget": f"₹{est_total_budget}"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)