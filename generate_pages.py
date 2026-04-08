import os

# Titles and file mapping
pages = {
    "profile.html": "My Profile",
    "plus-zone.html": "Flipkart Plus Zone",
    "orders.html": "Orders",
    "wishlist.html": "Wishlist",
    "seller.html": "Become a Seller",
    "rewards.html": "Rewards",
    "gift-cards.html": "Gift Cards",
    "notifications.html": "Notification Preferences",
    "support.html": "24x7 Customer Care",
    "advertise.html": "Advertise",
    "download-app.html": "Download App",
}

# The header/footer boilerplate (extracted from index)
header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LIFOSS | {TITLE}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body style="background-color: #f1f3f6;">
    <header class="fk-header">
        <div class="header-main">
            <div class="header-container-flex" style="justify-content: space-between; padding: 0 4rem;">
                <div class="header-left">
                    <div class="lifoss-logo" style="cursor:pointer;" onclick="window.location.href='index.html'">LIFOSS</div>
                </div>
                <div class="header-actions">
                    <div class="header-item" onclick="window.location.href='index.html'">
                        <i class="fa-solid fa-house"></i>
                        <span>Home</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <div style="margin-top: 100px; padding: 2rem 5rem; display: flex; gap: 2rem;">
        
        <!-- Shared User Sidebar -->
        <div style="width: 280px; background: white; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); padding: 1rem; align-self: flex-start;">
            <div style="padding-bottom: 1rem; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 1rem;">
                <img src="https://static-assets-web.flixcart.com/fk-p-linchpin-web/fk-cp-zion/img/profile-pic-male_4811a1.svg" width="50" alt="profile">
                <div>
                    <div style="font-size: 0.8rem; color: #878787;">Hello,</div>
                    <div style="font-weight: 600; font-size: 1.1rem;">LIFOSS User</div>
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <!-- Links -->
                <a href="orders.html" style="display: block; padding: 0.8rem; color: #878787; text-decoration: none; font-weight: 500;"><i class="fa-solid fa-box text-blue"></i> &nbsp; MY ORDERS <i class="fa-solid fa-chevron-right" style="float: right;"></i></a>
                
                <div style="padding: 0.8rem; font-weight: 500; color: #878787; border-top: 1px solid #f0f0f0; margin-top: 0.5rem;"><i class="fa-solid fa-user text-blue"></i> &nbsp; ACCOUNT SETTINGS</div>
                <a href="profile.html" style="display: block; padding: 0.5rem 1rem 0.5rem 2.8rem; text-decoration: none; color: #212121;">Profile Information</a>
                <a href="notifications.html" style="display: block; padding: 0.5rem 1rem 0.5rem 2.8rem; text-decoration: none; color: #212121;">Notification Preferences</a>

                <div style="padding: 0.8rem; font-weight: 500; color: #878787; border-top: 1px solid #f0f0f0; margin-top: 0.5rem;"><i class="fa-solid fa-wallet text-blue"></i> &nbsp; PAYMENTS</div>
                <a href="gift-cards.html" style="display: block; padding: 0.5rem 1rem 0.5rem 2.8rem; text-decoration: none; color: #212121;">Gift Cards</a>

                <div style="padding: 0.8rem; font-weight: 500; color: #878787; border-top: 1px solid #f0f0f0; margin-top: 0.5rem;"><i class="fa-solid fa-folder text-blue"></i> &nbsp; MY STUFF</div>
                <a href="rewards.html" style="display: block; padding: 0.5rem 1rem 0.5rem 2.8rem; text-decoration: none; color: #212121;">My Rewards</a>
                <a href="wishlist.html" style="display: block; padding: 0.5rem 1rem 0.5rem 2.8rem; text-decoration: none; color: #212121;">My Wishlist</a>
            </div>
        </div>

        <!-- Main Content Area -->
        <div style="flex: 1; background: white; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); padding: 2rem;">
            <h1 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 2rem; border-bottom: 1px solid #eee; padding-bottom: 1rem;">{TITLE}</h1>
            <div style="padding: 3rem; text-align: center; color: #878787;">
                <i class="{ICON}" style="font-size: 4rem; color: #2874f0; margin-bottom: 1rem;"></i>
                <h2 style="font-weight: 500;">Welcome to {TITLE}</h2>
                <p style="margin-top: 1rem;">This is a fully functional destination page for the {TITLE} section. You can integrate advanced logic here.</p>
                <button onclick="window.location.href='index.html'" style="margin-top: 2rem; padding: 10px 30px; background: #fb641b; color: white; border: none; border-radius: 2px; font-weight: 600; cursor: pointer;">Explore Products</button>
            </div>
        </div>
    </div>
</body>
</html>"""

# Icon mapping for the generic generation
icons = {
    "profile.html": "fa-solid fa-user",
    "plus-zone.html": "fa-solid fa-star-half-stroke",
    "orders.html": "fa-solid fa-box-open",
    "wishlist.html": "fa-regular fa-heart",
    "seller.html": "fa-solid fa-store",
    "rewards.html": "fa-solid fa-gift",
    "gift-cards.html": "fa-solid fa-ticket",
    "notifications.html": "fa-regular fa-bell",
    "support.html": "fa-solid fa-headset",
    "advertise.html": "fa-solid fa-chart-line",
    "download-app.html": "fa-solid fa-download",
}

for filename, title in pages.items():
    filepath = os.path.join(r"c:\Users\sande\OneDrive\Desktop\E-Commerce\frontend", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header.replace("{TITLE}", title).replace("{ICON}", icons[filename]))
        
print("11 pages successfully generated!")
