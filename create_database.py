import json
from geopy.geocoders import Nominatim
import time

def create_restaurant_database():
    # Restaurant list
    restaurant_list = [
        "Egghead Cafe", "Liliha Bakery", "Double Three Ice Cream",
        "Nami Kaze", "Chau's Fresh Fruit", "Fook Lam",
        "Sing Cheong Yuan Bakery", "Tea at 1024", "Senia",
        "Podmore", "H-Mart Kaka'ako", "E.A.R.L. Sandwiches",
        "Butcher & Bird", "Hank's Haute Dogs", "Highway Inn",
        "Istanbul Hawaii", "Tali's Bagels & Shmea", "Scratch Kitchen",
        "Purvé Donut Stop", "Foodland Farms", "Island Vintage Coffee",
        "Jejubing Dessert Cafe", "Sushi Murayama", "'Ili'lli Cash & Carry",
        "Tane Vegan Izakaya", "Off The Hook Poke", "Morning Glass Coffee",
        "Katsumidori Sushi", "100 Sails", "Tim Ho Wan",
        "Honolulu Cookie Company", "Azure", "Blue Note Hawaii",
        "Moana Surfrider", "Hula Dog Kuhio", "Waikiki Leia",
        "Barefoot Beach Cafe", "Diamond Head Market & Grill",
        "Tonkatsu Tamafuji", "Kono's Honolulu", "Leonard's Bakery",
        "Breadshop", "The Curb", "The Local General Store",
        "Mud Hen Water", "Miro Kaimuki", "XO & AV Restaurants",
        "Koko Head Cafe", "Cowcow's Tea", "Chubbies Burgers",
        "The Surfing Pig"
    ]
    
    geolocator = Nominatim(user_agent="restaurant_finder")
    restaurant_data = []
    
    print("Fetching restaurant coordinates...")
    
    for i, restaurant in enumerate(restaurant_list):
        try:
            full_address = f"{restaurant}, Honolulu, Hawaii"
            print(f"Processing {i+1}/{len(restaurant_list)}: {restaurant}")
            
            location = geolocator.geocode(full_address)
            if location:
                restaurant_data.append({
                    "name": restaurant,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "address": location.address,
                    "has_coordinates": True
                })
                print(f"✓ Found coordinates for {restaurant}")
            else:
                # Add restaurant with unknown coordinates
                restaurant_data.append({
                    "name": restaurant,
                    "latitude": None,  # Using None for unknown coordinates
                    "longitude": None,
                    "address": f"{restaurant}, Honolulu, Hawaii (exact location unknown)",
                    "has_coordinates": False
                })
                print(f"⚠ Could not find coordinates for {restaurant}, adding with unknown location")
            
            # Respect rate limiting
            time.sleep(1)
        
        except Exception as e:
            # Add restaurant with unknown coordinates even when an error occurs
            restaurant_data.append({
                "name": restaurant,
                "latitude": None,
                "longitude": None,
                "address": f"{restaurant}, Honolulu, Hawaii (exact location unknown)",
                "has_coordinates": False
            })
            print(f"✗ Error processing {restaurant}: {e}, adding with unknown location")
    
    # Save as JSON
    with open("restaurants.json", "w") as f:
        json.dump(restaurant_data, f, indent=2)
    
    # Count restaurants with and without coordinates
    with_coords = sum(1 for r in restaurant_data if r.get("has_coordinates", False))
    without_coords = len(restaurant_data) - with_coords
    
    print(f"\nSaved {len(restaurant_data)} restaurants to restaurants.json:")
    print(f"  - {with_coords} restaurants with coordinates")
    print(f"  - {without_coords} restaurants with unknown locations")
    print("You can now use this JSON file with your GitHub Pages website.")

if __name__ == "__main__":
    create_restaurant_database()