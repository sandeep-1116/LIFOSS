import os

base_dir = r"c:\Users\sande\OneDrive\Desktop\E-Commerce\frontend"

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LIFOSS | {title}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="profile-body">
    <style>
        .profile-body {{ background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%); background-size: 200% 200%; animation: gradientBG 15s ease infinite; font-family: 'Inter', sans-serif; min-height: 100vh; margin: 0; padding-bottom: 3rem; color: #212121; }}
        @keyframes gradientBG {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
        .p-header {{ background: rgba(255,255,255,0.3); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); padding: 1.2rem 3rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 30px rgba(0,0,0,0.05); border-bottom: 1px solid rgba(255,255,255,0.4); position: sticky; top: 0; z-index: 100; transition: 0.3s; }}
        .p-logo {{ font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800; color: #1e3a8a; cursor: pointer; text-decoration: none; display: flex; align-items: center; gap: 10px; letter-spacing: -1px; }}
        .p-container {{ max-width: 1100px; margin: 3rem auto 0; display: grid; grid-template-columns: 300px 1fr; gap: 2.5rem; padding: 0 2rem; }}
        .glass-panel {{ background: rgba(255, 255, 255, 0.65); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.7); border-radius: 24px; padding: 2.5rem; box-shadow: 0 15px 35px rgba(0,0,0,0.05), inset 0 0 0 1px rgba(255,255,255,0.5); }}
        .avatar-box {{ text-align: center; padding-bottom: 2rem; border-bottom: 1px solid rgba(0,0,0,0.08); }}
        .avatar-circle {{ width: 110px; height: 110px; border-radius: 50%; background: white; padding: 6px; box-shadow: 0 10px 25px rgba(59,130,246,0.2); margin: 0 auto 1rem; position: relative; }}
        .avatar-circle::after {{ content: ''; position: absolute; top:-6px; left:-6px; right:-6px; bottom:-6px; border-radius: 50%; background: linear-gradient(45deg, #1e3a8a, #8b5cf6, #ec4899); z-index: -1; animation: spin 4s linear infinite; }}
        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
        .avatar-circle img {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }}
        .nav-menu {{ margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }}
        .nav-link {{ padding: 1rem 1.2rem; border-radius: 12px; color: #444; text-decoration: none; font-weight: 600; display: flex; align-items: center; gap: 12px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        .nav-link:hover, .nav-link.active {{ background: rgba(255,255,255,0.9); color: #3b82f6; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transform: translateX(8px); }}
        .info-group {{ background: rgba(255,255,255,0.5); border-radius: 18px; padding: 1.8rem; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.8); transition: all 0.3s; text-align: center; }}
        .info-group:hover {{ background: rgba(255,255,255,0.7); box-shadow: 0 8px 25px rgba(0,0,0,0.04); transform: translateY(-2px); }}
        .explore-btn {{ margin-top: 2rem; padding: 14px 34px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 30px; font-size: 1.05rem; font-weight: 800; cursor: pointer; box-shadow: 0 10px 25px rgba(59,130,246,0.3); transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }}
        .explore-btn:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 15px 35px rgba(59,130,246,0.4); }}
    </style>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

    <header class="p-header">
        <a href="index.html" class="p-logo"><i class="fa-solid fa-shapes"></i> LIFOSS</a>
        <a href="index.html" style="color: #444; text-decoration: none; font-weight: 600; transition: 0.2s;" onmouseover="this.style.color='#1e3a8a'" onmouseout="this.style.color='#444'">
            <i class="fa-solid fa-arrow-left"></i> Back to Store
        </a>
    </header>

    <div class="p-container">
        <!-- Sidebar -->
        <div class="glass-panel profile-sidebar">
            <div class="avatar-box">
                <div class="avatar-circle">
                    <img src="https://static-assets-web.flixcart.com/fk-p-linchpin-web/fk-cp-zion/img/profile-pic-male_4811a1.svg" alt="Avatar">
                </div>
                <h3 id="sidebarNameDisplay" style="margin:0; color:#111; font-size:1.5rem; font-weight:800;">User</h3>
                <span style="color:#6366f1; font-size:0.85rem; font-weight: 700;">Premium Member ✨</span>
            </div>

            <nav class="nav-menu">
                <a href="profile.html" class="nav-link {active_profile}"><i class="fa-solid fa-user-astronaut"></i> My Profile</a>
                <a href="orders.html" class="nav-link {active_orders}"><i class="fa-solid fa-box-open"></i> My Orders</a>
                <a href="wishlist.html" class="nav-link {active_wishlist}"><i class="fa-solid fa-heart"></i> Wishlist</a>
                <a href="gift-cards.html" class="nav-link {active_gift}"><i class="fa-solid fa-wallet"></i> Wallet & Cards</a>
                <a href="notifications.html" class="nav-link {active_notifications}"><i class="fa-solid fa-bell"></i> Notifications</a>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="glass-panel profile-main" style="position: relative;">
            <div style="margin-bottom: 2.5rem;" class="animated-header">
                <h1 style="margin:0; font-size: 2.2rem; color: #111; letter-spacing: -1px; font-weight:800;">{page_title}</h1>
                <p style="margin: 8px 0 0; color: #666; font-weight: 500; font-size: 0.95rem;">{page_desc}</p>
            </div>

            <!-- Content Group -->
            <div class="info-group">
                <i class="{icon}" style="font-size: 4rem; color: {icon_color}; margin-bottom: 1.5rem; display:block;"></i>
                <h2 style="font-weight: 800; font-size: 1.5rem;">Welcome to {page_title}</h2>
                <p style="margin-top: 1rem; color: #666;">This beautifully redesigned section is currently standing by for logic.</p>
                <button onclick="window.location.href='index.html'" class="explore-btn">Go to Store</button>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            // GSAP Entrance Animations
            gsap.from(".p-header", {{ y: -50, opacity: 0, duration: 0.8, ease: "power3.out" }});
            gsap.from(".profile-sidebar", {{ x: -50, opacity: 0, duration: 0.8, ease: "power3.out", delay: 0.1 }});
            gsap.from(".animated-header", {{ y: 20, opacity: 0, duration: 0.8, ease: "power3.out", delay: 0.2 }});
            gsap.from(".info-group", {{ y: 40, opacity: 0, duration: 0.6, ease: "power3.out", delay: 0.3 }});

            const userJson = localStorage.getItem('lifoss_user');
            if (!userJson) {{
                window.location.href = 'index.html';
                return;
            }}

            const user = JSON.parse(userJson);
            const sidebarName = document.getElementById('sidebarNameDisplay');
            if(sidebarName) sidebarName.innerText = user.name;
        }});
    </script>
</body>
</html>"""

configs = [
    {
        "file": "orders.html", "title": "Orders", 
        "page_title": "My Orders", "page_desc": "Track your shipments and view order history.",
        "icon": "fa-solid fa-box-open", "icon_color": "#3b82f6",
        "active_profile": "", "active_orders": "active", "active_wishlist": "", "active_gift": "", "active_notifications": ""
    },
    {
        "file": "wishlist.html", "title": "Wishlist", 
        "page_title": "Wishlist", "page_desc": "Keep track of all the items you love.",
        "icon": "fa-solid fa-heart", "icon_color": "#ec4899",
        "active_profile": "", "active_orders": "", "active_wishlist": "active", "active_gift": "", "active_notifications": ""
    },
    {
        "file": "gift-cards.html", "title": "Wallet", 
        "page_title": "Wallet & Cards", "page_desc": "Manage your payment methods and gift card balances.",
        "icon": "fa-solid fa-wallet", "icon_color": "#8b5cf6",
        "active_profile": "", "active_orders": "", "active_wishlist": "", "active_gift": "active", "active_notifications": ""
    },
    {
        "file": "notifications.html", "title": "Notifications", 
        "page_title": "Notifications", "page_desc": "Manage your platform alerts and messages.",
        "icon": "fa-solid fa-bell", "icon_color": "#f59e0b",
        "active_profile": "", "active_orders": "", "active_wishlist": "", "active_gift": "", "active_notifications": "active"
    }
]

for cfg in configs:
    path = os.path.join(base_dir, cfg["file"])
    content = html_template.format(**cfg)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("All done!")
