import json
import random

# Base configurations
file_path = r"c:\Users\sande\OneDrive\Desktop\E-Commerce\backend\data\products.json"

brands = ["Neon", "Aura", "Quantum", "Apex", "Zenith", "Pulse", "Vortex", "Stellar", "Lunar", "Core"]
categories = {
    "Electronics": ["Smartphone", "Gaming Laptop", "Wireless Earbuds", "Smartwatch", "Mechanical Keyboard", "Monitor"],
    "Fashion": ["Denim Jacket", "Sneakers", "Cotton T-Shirt", "Formal Trousers", "Designer Sunglasses", "Backpack"],
    "Home": ["Coffee Maker", "Air Purifier", "Smart LED Bulb", "Vacuum Cleaner", "Table Lamp"],
    "Appliances": ["Microwave Oven", "Washing Machine", "Refrigerator", "Smart AC"],
    "Beauty": ["Vitamin C Serum", "Matte Lipstick", "Hydrating Moisturizer", "Sunscreen SPF 50"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Running Shoes", "Tennis Racket", "Football"]
}
adjectives = ["Pro", "Max", "Ultra", "Elite", "Advanced", "Essential", "Classic", "Smart", "X"]

# Corresponding generic image mappings (reusing existing assets)
img_map = {
    "Electronics": "assets/images/laptop.png",
    "Fashion": "assets/images/mens_shirt.png",
    "Home": "assets/images/watch.png",
    "Appliances": "assets/images/mouse.png",
    "Beauty": "assets/images/beauty_serum.png",
    "Sports": "assets/images/almonds.png"
}

with open(file_path, 'r', encoding='utf-8') as f:
    products = json.load(f)

current_ids = {p['id'] for p in products}
next_id = max(current_ids) + 1 if current_ids else 1

# Generate 80 new products
for _ in range(80):
    cat = random.choice(list(categories.keys()))
    base_item = random.choice(categories[cat])
    brand = random.choice(brands)
    adj = random.choice(adjectives)
    
    name = f"{brand} {base_item} {adj}"
    
    # Generate realistic pricing based on category
    if cat in ["Electronics", "Appliances"]:
        price = random.randint(5000, 150000)
    elif cat in ["Fashion", "Sports"]:
        price = random.randint(499, 8999)
    else:
        price = random.randint(299, 4999)
        
    rating = round(random.uniform(3.5, 4.9), 1)
    
    new_product = {
        "id": next_id,
        "name": name,
        "price": price,
        "category": cat,
        "subcategory": "General",
        "description": f"High quality {name.lower()} engineered for maximum performance and everyday reliability.",
        "image": img_map[cat],
        "stock": random.randint(5, 500),
        "rating": rating
    }
    
    products.append(new_product)
    next_id += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=4)

print(f"Successfully generated database. Total Products: {len(products)}")
