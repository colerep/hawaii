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
                    "address": location.address
                })
                print(f"✓ Found coordinates for {restaurant}")
            else:
                print(f"✗ Could not find coordinates for {restaurant}")
            
            # Respect rate limiting
            time.sleep(1)
        
        except Exception as e:
            print(f"✗ Error processing {restaurant}: {e}")
    
    # Save as JSON
    with open("restaurants.json", "w") as f:
        json.dump(restaurant_data, f, indent=2)
    
    print(f"\nSaved {len(restaurant_data)} restaurants to restaurants.json")
    print("You can now use this JSON file with your GitHub Pages website.")

if __name__ == "__main__":
    create_restaurant_database()