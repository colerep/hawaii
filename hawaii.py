import tkinter as tk
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import threading
import time
import sqlite3
import os

class RestaurantDatabase:
    def __init__(self):
        self.db_path = 'restaurants.db'
        self.create_database()
    
    def create_database(self):
        """Create the database and restaurants table if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                latitude REAL,
                longitude REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_database(self, restaurant_list, progress_callback=None):
        """Populate the database with restaurant coordinates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        geolocator = Nominatim(user_agent="restaurant_finder")
        
        total = len(restaurant_list)
        for i, restaurant in enumerate(restaurant_list):
            # Check if restaurant already exists
            cursor.execute('SELECT * FROM restaurants WHERE name = ?', (restaurant,))
            if not cursor.fetchone():
                try:
                    full_address = f"{restaurant}, Honolulu, Hawaii"
                    location = geolocator.geocode(full_address)
                    if location:
                        cursor.execute('''
                            INSERT INTO restaurants (name, latitude, longitude)
                            VALUES (?, ?, ?)
                        ''', (restaurant, location.latitude, location.longitude))
                        conn.commit()
                        time.sleep(1)  # Respect rate limiting
                    
                    if progress_callback:
                        progress = (i + 1) / total * 100
                        progress_callback(progress, f"Processing {restaurant}")
                
                except Exception as e:
                    print(f"Error processing {restaurant}: {e}")
        
        conn.close()
    
    def get_all_coordinates(self):
        """Get all restaurant coordinates from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, latitude, longitude FROM restaurants')
        results = cursor.fetchall()
        conn.close()
        return results

class RestaurantFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Finder")
        self.root.geometry("600x800")
        
        # Initialize database
        self.db = RestaurantDatabase()
        
        # Restaurant list
        self.restaurant_list = [
                "Egghead Cafe",
    "Liliha Bakery",
    "Double Three Ice Cream",
    "Nami Kaze",
    "Chau's Fresh Fruit",
    "Fook Lam",
    "Sing Cheong Yuan Bakery",
    "Tea at 1024",
    "Senia",
    "Podmore",
    "H-Mart Kaka'ako",
    "E.A.R.L. Sandwiches",
    "Butcher & Bird",
    "Hank's Haute Dogs",
    "Highway Inn",
    "Istanbul Hawaii",
    "Tali's Bagels & Shmea",
    "Scratch Kitchen",
    "Purvé Donut Stop",
    "Foodland Farms",
    "Island Vintage Coffee",
    "Jejubing Dessert Cafe",
    "Sushi Murayama",
    "'Ili'lli Cash & Carry",
    "Tane Vegan Izakaya",
    "Off The Hook Poke",
    "Morning Glass Coffee",
    "Katsumidori Sushi",
    "100 Sails",
    "Tim Ho Wan",
    "Honolulu Cookie Company",
    "Azure",
    "Blue Note Hawaii",
    "Moana Surfrider",
    "Hula Dog Kuhio",
    "Waikiki Leia",
    "Barefoot Beach Cafe",
    "Diamond Head Market & Grill",
    "Tonkatsu Tamafuji",
    "Kono's Honolulu",
    "Leonard's Bakery",
    "Breadshop",
    "The Curb",
    "The Local General Store",
    "Mud Hen Water",
    "Miro Kaimuki",
    "XO & AV Restaurants",
    "Koko Head Cafe",
    "Cowcow's Tea",
    "Chubbies Burgers",
    "The Surfing Pig"
        ]
        
        self.create_widgets()

    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Custom.TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Header.TLabel", background="#f0f0f0", font=("Arial", 12, "bold"))

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10", style="Custom.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(
            main_frame, 
            text="Find Restaurants Near You",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))

        # Update database button
        self.update_db_button = ttk.Button(
            main_frame,
            text="Update Restaurant Database",
            command=self.update_database
        )
        self.update_db_button.pack(pady=(0, 10))

        # Address entry
        address_frame = ttk.Frame(main_frame)
        address_frame.pack(fill=tk.X, pady=(0, 10))
        
        address_label = ttk.Label(
            address_frame,
            text="Enter your address:",
            style="Custom.TLabel"
        )
        address_label.pack(anchor=tk.W)
        
        self.address_entry = ttk.Entry(address_frame, width=50)
        self.address_entry.pack(fill=tk.X, pady=(5, 0))

        # Search button
        self.search_button = ttk.Button(
            main_frame,
            text="Find Restaurants",
            command=self.start_search
        )
        self.search_button.pack(pady=10)

        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="",
            style="Custom.TLabel"
        )
        self.progress_label.pack()

        # Results frame with scrollbar
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(
            results_frame,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=("Arial", 10),
            height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)

        self.results_text.tag_configure("header", font=("Arial", 11, "bold"))

    def update_progress(self, progress, message):
        """Update progress bar and message"""
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.root.update_idletasks()

    def update_database(self):
        """Update the restaurant database"""
        self.update_db_button.config(state=tk.DISABLED)
        self.search_button.config(state=tk.DISABLED)
        
        def update_task():
            self.db.populate_database(self.restaurant_list, self.update_progress)
            self.progress_label.config(text="Database updated successfully!")
            self.update_db_button.config(state=tk.NORMAL)
            self.search_button.config(state=tk.NORMAL)
            self.progress_var.set(0)
        
        thread = threading.Thread(target=update_task)
        thread.daemon = True
        thread.start()

    def get_coordinates(self, address):
        """Get coordinates for user address"""
        geolocator = Nominatim(user_agent="restaurant_finder")
        try:
            location = geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            return None
        return None

    def calculate_distances(self, user_location):
        """Calculate distances using database"""
        restaurants = self.db.get_all_coordinates()
        distances = []
        
        total = len(restaurants)
        for i, (name, lat, lon) in enumerate(restaurants):
            restaurant_coords = (lat, lon)
            distance = geodesic(user_location, restaurant_coords).miles
            distances.append((name, distance))
            
            progress = (i + 1) / total * 100
            self.update_progress(progress, f"Calculating distance to {name}")
        
        return sorted(distances, key=lambda x: x[1])

    def start_search(self):
        """Start the search process"""
        self.results_text.delete(1.0, tk.END)
        self.search_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.search_restaurants)
        thread.daemon = True
        thread.start()

    def search_restaurants(self):
        """Search for restaurants near user location"""
        address = self.address_entry.get()
        if not address:
            messagebox.showerror("Error", "Please enter an address")
            self.search_button.config(state=tk.NORMAL)
            return

        self.progress_label.config(text="Finding your location...")
        user_coords = self.get_coordinates(address)
        
        if not user_coords:
            messagebox.showerror("Error", "Could not find your location. Please check the address.")
            self.search_button.config(state=tk.NORMAL)
            return

        distances = self.calculate_distances(user_coords)
        
        self.results_text.insert(tk.END, "Restaurants sorted by distance from your location:\n", "header")
        for restaurant, distance in distances:
            self.results_text.insert(tk.END, f"{restaurant}: {distance:.2f} miles\n")

        self.progress_var.set(0)
        self.progress_label.config(text="Search complete!")
        self.search_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = RestaurantFinderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()