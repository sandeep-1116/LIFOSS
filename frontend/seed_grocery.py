import json
import random

PRODUCT_FILE = 'backend/data/products.json'

try:
    with open(PRODUCT_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)
except FileNotFoundError:
    products = []

start_id = max([p.get('id', 0) for p in products]) + 1 if products else 1

GROCERY_DATA = {
    'Staples': {
        'items': ['Premium Sharbati Atta', 'Basmati Rice', 'Sona Masoori Rice', 'Toor Dal', 'Moong Dal', 'Chana Dal', 'Mustard Oil', 'Sunflower Oil', 'Olive Oil', 'Turmeric Powder', 'Coriander Powder', 'Red Chilli Powder', 'Salt', 'Sugar', 'Jaggery'],
        'brands': ['Aashirvaad', 'Fortune', 'India Gate', 'Patanjali', 'Tata Sampann', 'Kohinoor', 'Dhara', 'Saffola', 'Madhur', 'Catch', 'Everest', 'MDH'],
        'variants': ['1kg', '5kg', '10kg', '500g', '2kg'],
        'img': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?q=80&w=600&auto=format&fit=crop'
    },
    'Snacks': {
        'items': ['Potato Chips', 'Nachos', 'Bhujia', 'Mixture Namkeen', 'Digestive Biscuits', 'Cream Biscuits', 'Roasted Peanuts', 'Popcorn', 'Khakhra', 'Kurkure', 'Diet Snacks', 'Roasted Makhana', 'Trail Mix', 'Chocolates', 'Wafers'],
        'brands': ['Lay\'s', 'Haldiram\'s', 'Bikano', 'Britannia', 'Parle', 'Sunfeast', 'Bingo', 'Pringles', 'Doritos', 'Balaji', 'Cadbury', 'Amul'],
        'variants': ['Medium Pack', 'Family Pack', 'Party Pack', '100g', '250g'],
        'img': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?q=80&w=600&auto=format&fit=crop'
    },
    'Beverage': {
        'items': ['CTC CTC Tea', 'Green Tea', 'Filter Coffee', 'Instant Coffee', 'Apple Juice', 'Mixed Fruit Juice', 'Mango Drink', 'Cola', 'Lemon Soda', 'Energy Drink', 'Sparkling Water', 'Cold Coffee', 'Almond Milk', 'Coconut Water'],
        'brands': ['Red Label', 'Tata Tea', 'Lipton', 'Nescafe', 'Bru', 'Real', 'Tropicana', 'Coca-Cola', 'Pepsi', 'Sprite', 'Red Bull', 'Kinley', 'Paper Boat'],
        'variants': ['250ml', '500ml', '1L', '2L', '250g', '500g', '100 Tea Bags'],
        'img': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?q=80&w=600&auto=format&fit=crop'
    },
    'Packaged': {
        'items': ['Instant Noodles', 'Penne Pasta', 'Macaroni', 'Mixed Fruit Jam', 'Peanut Butter', 'Tomato Ketchup', 'Mayonnaise', 'Schezwan Chutney', 'Pickle', 'Oats', 'Corn Flakes', 'Muesli', 'Instant Soup', 'Cup Noodles'],
        'brands': ['Maggi', 'Yippee', 'Sunfeast', 'Kissan', 'Pintola', 'Dr. Oetker', 'Mother\'s Recipe', 'Chings', 'Saffola', 'Kellogg\'s', 'Knorr', 'Bambino'],
        'variants': ['Jar', 'Pouch', 'Family Pack', '500g', '1kg'],
        'img': 'https://images.unsplash.com/photo-1612800478144-884ec75c2e08?q=80&w=600&auto=format&fit=crop'
    },
    'Dairy': {
        'items': ['Toned Milk', 'Full Cream Milk', 'Cheese Slices', 'Cheese Cubes', 'Paneer', 'Salted Butter', 'Unsalted Butter', 'Fresh Curd', 'Yogurt', 'Brown Eggs', 'White Eggs', 'Ghee', 'Lassi', 'Buttermilk'],
        'brands': ['Amul', 'Mother Dairy', 'Nandini', 'Govardhan', 'Epigamia', 'Britannia', 'Desi Farm', 'Milky Mist', 'Nestle', 'Country Delight'],
        'variants': ['500ml', '1L', '200g', '500g', '1kg', 'Pack of 6', 'Pack of 30'],
        'img': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?q=80&w=600&auto=format&fit=crop'
    },
    'Personal': {
        'items': ['Bathing Soap', 'Anti-Dandruff Shampoo', 'Conditioner', 'Toothpaste', 'Toothbrush Set', 'Deodorant Body Spray', 'Face Wash', 'Moisturizing Cream', 'Hair Oil', 'Shaving Cream', 'Razor', 'Hand Wash'],
        'brands': ['Dove', 'Pears', 'Head & Shoulders', 'Pantene', 'Colgate', 'Pepsodent', 'Nivea', 'Axe', 'Garnier', 'Parachute', 'Gillette', 'Dettol'],
        'variants': ['Single Pack', 'Pack of 3', 'Pack of 4', '150ml', '500ml', '100g'],
        'img': 'https://images.unsplash.com/photo-1619451195655-b4ee52b1bdf6?q=80&w=600&auto=format&fit=crop'
    },
    'Home Care': {
        'items': ['Liquid Detergent', 'Washing Powder', 'Dishwash Liquid', 'Dishwash Bar', 'Floor Cleaner', 'Toilet Cleaner', 'Room Freshener', 'Glass Cleaner', 'Mosquito Repellent Liquid', 'Garbage Bags', 'Sponge Wipes'],
        'brands': ['Surf Excel', 'Ariel', 'Tide', 'Vim', 'Pril', 'Lizol', 'Harpic', 'Odonil', 'Colin', 'All Out', 'Good Knight'],
        'variants': ['500ml', '1L', '5L', '1kg', '3kg', 'Pack of 2', 'Pack of 5'],
        'img': 'https://images.unsplash.com/photo-1584820927508-0138ffeb2441?q=80&w=600&auto=format&fit=crop'
    },
    'Baby': {
        'items': ['Baby Diapers', 'Baby Wipes', 'Baby Soap', 'Baby Shampoo', 'Baby Massage Oil', 'Baby Powder', 'Infant Formula', 'Baby Cereal', 'Diaper Rash Cream', 'Baby Lotion'],
        'brands': ['Pampers', 'Hugges', 'MamyPoko', 'Johnson\'s', 'Sebamed', 'Himalaya', 'Nestle', 'Mee Mee', 'Pigeon'],
        'variants': ['Small (Pack of 42)', 'Medium (Pack of 74)', 'Large (Pack of 64)', '100ml', '500ml', '400g'],
        'img': 'https://images.unsplash.com/photo-1519689680058-324335c77eba?q=80&w=600&auto=format&fit=crop'
    }
}

new_items = []
target_per_category = 160  # 8 categories * 160 = ~1280 items

for cat_key, cat_data in GROCERY_DATA.items():
    items = cat_data['items']
    brands = cat_data['brands']
    variants = cat_data['variants']
    img = cat_data['img']
    
    generated_for_this = 0
    # Create all permutations roughly to hit massive scale
    for item in items:
        for brand in brands:
            for variant in variants:
                if generated_for_this >= target_per_category:
                    break
                
                # Base variation mechanics for ultra-realism
                price_multiplier = random.uniform(0.8, 3.5)
                base = 99
                calc_val = int(base * price_multiplier) // 10 * 10 - 1  # e.g. 199, 249, 399
                
                new_product = {
                    "id": start_id,
                    "name": f"{brand} {item} ({variant})",
                    "price": calc_val,
                    "rating": round(random.uniform(3.8, 5.0), 1),
                    "reviews": random.randint(50, 4500),
                    "stock": random.randint(10, 500),
                    "image": img,
                    "category": "Grocery",
                    "description": f"Premium high-quality {cat_key} product ensuring top-tier reliability. Excellent value {item} brought to you by {brand}."
                }
                new_items.append(new_product)
                start_id += 1
                generated_for_this += 1
        
        if generated_for_this >= target_per_category:
            break

# Shuffle array randomly using Fisher-Yates so grid output is organic mixed
random.shuffle(new_items)
products.extend(new_items)

with open(PRODUCT_FILE, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2)

print(f"✅ Successfully Synthesized {len(new_items)} Grocery Products into the Database Architecture!")
