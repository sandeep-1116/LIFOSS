document.addEventListener('DOMContentLoaded', () => {
    const API_URL = window.location.origin + '/api';
    const productGrid = document.getElementById('productGrid');
    const mainSearch = document.getElementById('mainSearch');
    const cartToggle = document.getElementById('cartToggle');
    const cartSidebar = document.getElementById('cartSidebar');
    const closeCart = document.getElementById('closeCart');
    const cartOverlay = document.getElementById('cartOverlay');
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalDisplay = document.getElementById('cartTotal');
    const cartCountDisplay = document.querySelector('.cart-count');
    const catItems = document.querySelectorAll('.cat-item');
    const sortSelect = document.getElementById('sortSelect');
    const categoryTitle = document.getElementById('currentCategoryTitle');
    const productModal = document.getElementById('productModal');
    const toast = document.getElementById('toast');
    const backToTopBtn = document.getElementById('backToTop');
    const closeModal = document.getElementById('closeModal');
    const modalImg = document.getElementById('modalImg');
    const modalTitle = document.getElementById('modalTitle');
    const modalRating = document.getElementById('modalRating');
    const modalPrice = document.getElementById('modalPrice');
    const modalDesc = document.getElementById('modalDesc');
    const modalCat = document.getElementById('modalCat');
    const modalAddToCart = document.getElementById('modalAddToCart');
    
    // --- Travel Identity Flow ---
    const travelIdModal = document.getElementById('travelIdentityModal');

    window.handleTravelAccess = function() {
        console.log("Travel access triggered...");
        const user = localStorage.getItem('lifoss_user');
        
        if (!user) {
            showToast("Login required for Travel Services! ✈️");
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1200);
            return;
        }

        // Check if identity is already saved
        const hasIdentity = localStorage.getItem('lifoss_travel_id_verified');
        console.log("User verified:", hasIdentity);

        if (hasIdentity === 'true') {
            window.location.href = 'travel.html';
        } else {
            const travelIdModal = document.getElementById('travelIdentityModal');
            if (travelIdModal) {
                travelIdModal.style.display = 'flex';
                console.log("Displaying identity modal...");
            } else {
                console.error("Travel Identity Modal not found in DOM!");
            }
        }
    };

    window.closeTravelIdentityModal = function() {
        if (travelIdModal) travelIdModal.style.display = 'none';
    };

    window.submitTravelIdentity = function(e) {
        e.preventDefault();
        
        // Simulating validation and storage
        const idName = document.getElementById('idFullName').value;
        const idType = document.getElementById('idType').value;
        const idNum = document.getElementById('idPartialNum').value;
        
        if (idName && idNum.length === 4) {
            localStorage.setItem('lifoss_travel_id_verified', 'true');
            localStorage.setItem('lifoss_travel_id_name', idName);
            
            showToast("Identity Verified! Opening Travel 🚀");
            setTimeout(() => {
                window.location.href = 'travel.html';
            }, 1500);
        } else {
            showToast("Please fill all fields correctly.");
        }
    };

    let products = []; // This will now always store ALL products
    let filteredProducts = [];
    let cart = [];
    let activeFilter = window.LIFOSS_PAGE_MODE || 'all';

    // --- Core Logic ---
    init();

    async function init() {
        checkAuthState();
        
        // Show welcome toast on load if not logged in
        if(!localStorage.getItem('lifoss_user')) {
            showToast("Welcome to LIFOSS! 🚀");
        }
        
        await fetchProducts();
        setupEventListeners();

        // Check for travel trigger from redirect (to show modal)
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('triggerTravel') === 'true') {
            console.log("Triggering auto-verification modal...");
            handleTravelAccess();
        }
    }

    function checkAuthState() {
        const userJson = localStorage.getItem('lifoss_user');
        if(userJson) {
            const user = JSON.parse(userJson);
            
            // Adjust Header Login Text
            const loginText = document.getElementById('loginText');
            if(loginText) {
                loginText.innerText = 'Hi, ' + user.name.split(' ')[0];
                document.querySelector('.login-dropdown').removeAttribute('onclick'); // Disable full direct link
            }
            // Sync Location Data to Header & Modal
            if (user.location || user.pincode) {
                const headerLoc = document.getElementById('headerLocText');
                if (headerLoc) headerLoc.innerText = `Deliver to ${user.name.split(' ')[0]} - ${user.pincode || 'Saved Address'}`;
                
                const locLogin = document.getElementById('locLoginBox');
                const locSaved = document.getElementById('locSavedBox');
                if (locLogin && locSaved) {
                    locLogin.style.display = 'none';
                    locSaved.style.display = 'block';
                    document.getElementById('userSavedName').innerText = user.name;
                    document.getElementById('userSavedAddress').innerText = user.location || `Pincode: ${user.pincode}`;
                }
            }
            
            // Reconfigure the Dropdown Header Area to 'Logout'
            const menuHeaderBox = document.getElementById('menuHeaderBox');
            if(menuHeaderBox) {
                menuHeaderBox.innerHTML = `
                    <span class="new-cust" style="font-weight:600;">Welcome back!</span>
                    <a href="#" class="signup-link" id="logoutBtn" style="color:#ff6161;">Logout</a>
                `;
                
                document.getElementById('logoutBtn').addEventListener('click', (e) => {
                    e.preventDefault();
                    localStorage.removeItem('lifoss_user');
                    window.location.reload();
                });
            }
        }
    }

    function showToast(msg) {
        if (!toast) return;
        toast.innerText = msg;
        toast.className = "toast show";
        setTimeout(() => { if (toast) toast.className = "toast"; }, 3000);
    }

    // --- API Interactions ---
    async function fetchProducts() {
        try {
            const res = await fetch(`${API_URL}/products`);
            const allProducts = await res.json();
            products = allProducts; // Keep the full list here
            
            // Initial filter based on page mode or 'all'
            applyFilters();
            renderMarquee(products);
        } catch (err) {
            console.error('Fetch error:', err);
            productGrid.innerHTML = '<p class="error">Database connection lost. Please restart the backend.</p>';
        }
    }

    async function updateCartAPI(item) {
        try {
            const res = await fetch(`${API_URL}/cart`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(item)
            });
            const updated = await res.json();
            syncCart(updated);
        } catch (err) {
            console.error('Cart sync error:', err);
        }
    }

    async function clearCartAPI() {
        try {
            await fetch(`${API_URL}/cart`, { method: 'DELETE' });
            syncCart([]);
        } catch (err) {
            console.error('Clear cart error:', err);
        }
    }

    // --- Rendering Core ---
    function renderProducts(items) {
        productGrid.innerHTML = '';
        
        if (items.length === 0) {
            productGrid.innerHTML = '<p class="no-results">No products found matching your search!</p>';
            return;
        }

        items.forEach((p, index) => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <div class="product-img-wrapper" style="position:relative;">
                    <i class="fa-regular fa-heart wishlist-icon" style="position:absolute; top:8px; right:8px; color:#c2c2c2; font-size:1.3rem; cursor:pointer;" onclick="event.stopPropagation(); this.classList.toggle('fa-solid'); this.classList.toggle('fa-regular'); this.style.color = this.classList.contains('fa-solid') ? '#ff4343' : '#c2c2c2';"></i>
                    <img src="${p.image}" alt="${p.name}" class="product-img">
                </div>
                <div class="product-info" style="text-align: left; margin-top: 0.5rem;">
                    <h3 class="product-name" title="${p.name}" style="font-weight: 500; font-size: 0.9rem; color: #212121; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: auto;">${p.name}</h3>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 5px;">
                        <span class="rating-badge" style="margin:0; background: #388e3c; padding: 2px 5px; font-size: 0.7rem;">${p.rating} <i class="fa-solid fa-star" style="font-size: 0.6rem;"></i></span>
                        <img src="assets/images/lifoss_assured.svg" height="18" alt="LIFOSS Assured">
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                        <div class="product-price" style="font-size: 1.1rem; font-weight: 600; color: #212121;">₹${p.price.toLocaleString('en-IN')}</div>
                        <div style="color: #878787; text-decoration: line-through; font-size: 0.85rem;">₹${(p.price * 1.4).toLocaleString('en-IN')}</div>
                        <div style="color: #388e3c; font-size: 0.85rem; font-weight: 600;">${Math.floor(Math.random() * 40 + 10)}% off</div>
                    </div>
                    <div style="font-size: 0.75rem; font-weight: 500; color: #212121;">Free delivery</div>
                </div>
            `;
            
            productGrid.appendChild(card);

            // Open Modal on Card Click (except button)
            card.addEventListener('click', (e) => {
                if (e.target.tagName !== 'BUTTON') {
                    openProductModal(p);
                }
            });

            // Staggered GSAP Entry
            gsap.from(card, {
                opacity: 0,
                y: 30,
                duration: 0.5,
                delay: index * 0.05,
                scrollTrigger: {
                    trigger: card,
                    start: 'top 95%'
                }
            });
        });

        // Add to cart listeners
        document.querySelectorAll('.add-to-cart-simple').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.getAttribute('data-id'));
                const p = products.find(prod => prod.id === id);
                if (p) {
                    addToCart(p);
                    animateBtn(btn);
                }
            });
        });
    }

    // --- Dynamic Marquee Rendering ---
    function renderMarquee(items) {
        const track = document.getElementById('runningDealsTrack');
        if (!track) return;
        
        track.innerHTML = '';
        
        let dealItems = items.filter(p => p.rating >= 4.5);
        if (dealItems.length < 5) dealItems = items.slice(0, 8);
        
        // Clone array 4 times to construct infinite scroll math
        const infiniteList = [...dealItems, ...dealItems, ...dealItems, ...dealItems];
        
        infiniteList.forEach(p => {
            const el = document.createElement('div');
            el.className = 'marquee-item';
            el.innerHTML = `
                <div class="mq-img-box"><img src="${p.image}" alt="${p.name}"></div>
                <div class="mq-title" title="${p.name}">${p.name.length > 25 ? p.name.substring(0, 22) + '...' : p.name}</div>
                <div class="mq-price">₹${p.price.toLocaleString('en-IN')}</div>
            `;
            el.onclick = () => openProductModal(p);
            track.appendChild(el);
        });
    }

    function syncCart(newCart) {
        cart = newCart;
        updateCartUI();
    }

    function updateCartUI() {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        let count = 0;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="empty-msg">Bag is empty</p>';
            cartTotalDisplay.innerText = '₹0.00';
            cartCountDisplay.innerText = '0';
            return;
        }

        cart.forEach(item => {
            total += item.price * item.quantity;
            count += item.quantity;
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';
            itemEl.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="cart-item-img">
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">₹${item.price.toLocaleString('en-IN')} x ${item.quantity}</div>
                </div>
            `;
            cartItemsContainer.appendChild(itemEl);
        });

        cartTotalDisplay.innerText = `₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        cartCountDisplay.innerText = count;
        gsap.fromTo(cartCountDisplay, { scale: 0.5 }, { scale: 1, duration: 0.2 });
    }

    // --- Interactive Logic ---
    function setupEventListeners() {
        // Toggle Cart
        cartToggle.addEventListener('click', () => {
            cartSidebar.classList.toggle('open');
            cartOverlay.classList.toggle('show');
        });

        closeCart.addEventListener('click', closeAllOverlays);
        cartOverlay.addEventListener('click', closeAllOverlays);

        // Search Bar Event (Real-time)
        mainSearch.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            
            // If user is searching, we usually want to show results across all categories
            // unless they specifically want to filter within a category.
            // For "Flipkart-like" feel, searching often resets the category tab.
            if (query && activeFilter !== 'all') {
                activeFilter = 'all';
                catItems.forEach(i => i.classList.remove('active'));
                const forYouTab = document.querySelector('.cat-item[data-filter="all"]');
                if (forYouTab) forYouTab.classList.add('active');
            }

            applyFilters();
        });

        // Add handler for Search Button
        const searchBtn = document.querySelector('.search-icon-btn');
        if (searchBtn) {
            searchBtn.addEventListener('click', applyFilters);
        }
        
        mainSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                applyFilters();
                mainSearch.blur();
            }
        });

        // Category Filter
        catItems.forEach(item => {
            item.addEventListener('click', () => {
                catItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                
                activeFilter = item.getAttribute('data-filter');
                categoryTitle.innerText = activeFilter === 'all' ? 'All Products' : `Top Results in ${activeFilter}`;
                
                applyFilters();
            });
        });

        // Sorting Logic
        sortSelect.addEventListener('change', (e) => {
            const mode = e.target.value;
            if (mode === 'price-low') {
                filteredProducts.sort((a, b) => a.price - b.price);
            } else if (mode === 'price-high') {
                filteredProducts.sort((a, b) => b.price - a.price);
            } else if (mode === 'popularity') {
                filteredProducts.sort((a, b) => b.rating - a.rating);
            }
            renderProducts(filteredProducts);
        });

        // Checkout Button
        document.querySelector('.checkout-btn').addEventListener('click', () => {
            if (cart.length === 0) return showToast('Your cart is empty! 🛒');
            showToast('Order placed successfully! 🎊');
            cart = [];
            updateCartUI(); // Fixed to use UI sync
            closeAllOverlays();
        });

        // Back to Top Logic
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                backToTopBtn.style.display = "block";
            } else {
                backToTopBtn.style.display = "none";
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Modal Close
        closeModal.addEventListener('click', closeProductModal);
        productModal.addEventListener('click', (e) => {
            if (e.target === productModal) closeProductModal();
        });

        // Modal Add to Cart
        modalAddToCart.addEventListener('click', () => {
            const id = parseInt(modalAddToCart.getAttribute('data-id'));
            const p = products.find(prod => prod.id === id);
            if (p) {
                addToCart(p);
                animateBtn(modalAddToCart);
            }
        });

        // Pincode Check
        const pincodeBtn = document.getElementById('pincodeBtn');
        const pincodeCheck = document.getElementById('pincodeCheck');
        pincodeBtn.addEventListener('click', () => {
            if (pincodeCheck.value.length === 6) {
                pincodeBtn.innerText = 'VALID ✓';
                pincodeBtn.style.color = '#388e3c';
            } else {
                alert('Please enter a valid 6-digit pincode');
            }
        });

        // Color Selection
        document.querySelectorAll('.color-circle').forEach(c => {
            c.addEventListener('click', () => {
                document.querySelectorAll('.color-circle').forEach(x => x.classList.remove('active'));
                c.classList.add('active');
            });
        });
    }

    function openProductModal(p) {
        modalImg.src = p.image;
        modalTitle.innerText = p.name;
        modalRating.innerHTML = `${p.rating} <i class="fa-solid fa-star"></i>`;
        modalPrice.innerText = `₹${p.price.toLocaleString('en-IN')}`;
        modalDesc.innerText = p.description || "Premium high-quality product tested for long-lasting durability and exceptional performance. This item meets all national quality standards.";
        modalCat.innerText = p.category;
        modalAddToCart.setAttribute('data-id', p.id);

        // Populate Highlights based on category
        const highlightsUl = document.getElementById('modalHighlights');
        if (p.category === 'Mobiles') {
            highlightsUl.innerHTML = `
                <li>12 GB RAM | 256 GB ROM</li>
                <li>17.02 cm (6.7 inch) Super Retina XDR Display</li>
                <li>50MP + 12MP + 12MP | 12MP Front Camera</li>
                <li>Flagship Processor, High Performance</li>
            `;
        } else if (p.category === 'Electronics') {
            highlightsUl.innerHTML = `
                <li>Advanced Noise Cancellation</li>
                <li>Up to 40 Hours Battery Life</li>
                <li>Quick Charging Support</li>
                <li>Seamless Multi-device Connectivity</li>
            `;
        } else {
            highlightsUl.innerHTML = `
                <li>Premium Quality Material</li>
                <li>Highly Durable and Stylis</li>
                <li>1 Year Brand Warranty</li>
                <li>7 Days Easy Return Policy</li>
            `;
        }

        productModal.style.display = 'flex';
        gsap.fromTo('.product-modal-container', { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(1.7)' });
    }

    function closeProductModal() {
        gsap.to('.product-modal-container', { scale: 0.8, opacity: 0, duration: 0.3, onComplete: () => {
            productModal.style.display = 'none';
        }});
    }

    function applyFilters() {
        const query = mainSearch.value.toLowerCase();
        const queryTerms = query.split(' ').filter(t => t.length > 0);
        
        filteredProducts = products.filter(p => {
            // Logic: 
            // 1. If there's a search query, we do a GLOBAL search (matchesSearch) 
            //    BUT we also respect category IF the user specifically clicked a category tab.
            //    However, if they are on a specific Page Mode (like Grocery), we usually want 
            //    to allow them to search the whole site from the top bar.
            
            const matchesCat = (activeFilter === 'all') || (p.category === activeFilter);
            
            const matchesSearch = queryTerms.every(term => 
                p.name.toLowerCase().includes(term) || 
                p.category.toLowerCase().includes(term) ||
                (p.subcategory && p.subcategory.toLowerCase().includes(term)) ||
                p.description.toLowerCase().includes(term)
            );

            // If user is searching, we ignore the category filter UNLESS it's not 'all' 
            // and they haven't just started typing.
            // Simplified: If searching, prioritize the search terms globally if the category doesn't match.
            // But to keep it consistent: category and search are usually "AND"ed.
            return matchesCat && matchesSearch;
        });

        // Update Title UI
        if (query) {
            categoryTitle.innerText = `Showing results for "${mainSearch.value}" (${filteredProducts.length} items)`;
        } else {
            categoryTitle.innerText = activeFilter === 'all' ? 'All Products' : `${activeFilter} (${filteredProducts.length} items)`;
        }

        renderProducts(filteredProducts);
    }

    function closeAllOverlays() {
        cartSidebar.classList.remove('open');
        cartOverlay.classList.remove('show');
    }

    function addToCart(p) {
        const existing = cart.find(item => item.id === p.id);
        if (existing) {
            existing.quantity++;
        } else {
            cart.push({ ...p, quantity: 1 });
        }
        updateCartUI();
        showToast(`${p.name} added to cart! 🛍️`);
        gsap.fromTo(cartCountDisplay, { scale: 1.5, color: '#ff9f00' }, { scale: 1, color: '#fff', duration: 0.4 });
    }

    function animateBtn(btn) {
        gsap.to(btn, { backgroundColor: '#388e3c', scale: 0.95, duration: 0.1, yoyo: true, repeat: 1 });
        const originalText = btn.innerText;
        btn.innerText = 'ADDED ✓';
        setTimeout(() => btn.innerText = originalText, 1000);
    }

    // --- Hero Slider Logic ---
    let currentSlide = 0;
    const slides = document.querySelectorAll('.banner-slide');
    if (slides.length > 1) {
        setInterval(() => {
            gsap.to(slides[currentSlide], { opacity: 0, duration: 1, onComplete: () => {
                slides[currentSlide].style.display = 'none';
                currentSlide = (currentSlide + 1) % slides.length;
                slides[currentSlide].style.display = 'flex';
                gsap.fromTo(slides[currentSlide], { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 0.8 });
            }});
        }, 5000);
    }

    // --- Tab Switching ---
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.classList.contains('travel-tab') && !window.location.href.includes('travel.html')) {
                return; // Let the onclick in HTML handle it
            }
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            gsap.fromTo(tab, { scale: 0.95 }, { scale: 1, duration: 0.2 });
        });
    });

    // Pure CSS handles login dropdown animations robustly.

    // Make category icon frame hoverable
    document.querySelectorAll('.cat-item').forEach(item => {
        item.addEventListener('mouseenter', () => {
            gsap.to(item.querySelector('i'), { scale: 1.1, duration: 0.2 });
        });
        item.addEventListener('mouseleave', () => {
            gsap.to(item.querySelector('i'), { scale: 1, duration: 0.2 });
        });
    });

    // Scroll Progress Bar
    window.onscroll = function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.getElementById("progress-bar").style.width = scrolled + "%";
    };

    // --- Location Modal Logic ---
    const locationModal = document.getElementById('locationModal');
    const openLocModal = document.getElementById('openLocModal');
    const closeLocModal = document.getElementById('closeLocModal');
    const locCurrentBtn = document.getElementById('locCurrentBtn');
    
    if (openLocModal && locationModal) {
        openLocModal.addEventListener('click', (e) => {
            e.preventDefault();
            locationModal.style.display = 'flex';
        });
        
        closeLocModal.addEventListener('click', () => {
            locationModal.style.display = 'none';
        });
        
        locationModal.addEventListener('click', (e) => {
            if (e.target === locationModal) {
                locationModal.style.display = 'none';
            }
        });
    }

    if (locCurrentBtn) {
        locCurrentBtn.addEventListener('click', () => {
            locCurrentBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Fetching location...';
            
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(async (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    try {
                        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                        const data = await response.json();
                        const pin = data.address.postcode || data.address.city || 'Location Found';
                        
                        document.getElementById('headerLocText').innerText = `Deliver to ${pin}`;
                        locationModal.style.display = 'none';
                        showToast("Location updated successfully!");
                        locCurrentBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Use my current location';
                    } catch (error) {
                        locCurrentBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Use my current location';
                        alert('Could not pinpoint exact location. Please use search.');
                    }
                }, () => {
                    locCurrentBtn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> Use my current location';
                    alert('Permission denied. Please allow location access in your browser.');
                });
            } else {
                alert("Geolocation is not supported by your browser.");
            }
        });
    }

    // Handle Manual Search Apply
    const locApplyBtn = document.getElementById('locApplyBtn');
    if (locApplyBtn) {
        locApplyBtn.addEventListener('click', () => {
            const val = document.getElementById('locSearchInput').value;
            if(val) {
                document.getElementById('headerLocText').innerText = `Deliver to ${val}`;
                locationModal.style.display = 'none';
                showToast("Delivery location set!");
            }
        });
    }

    // Global hook for the logged-in saved item box
    window.selectSavedLocation = function() {
        const userJson = localStorage.getItem('lifoss_user');
        if(userJson) {
            const user = JSON.parse(userJson);
            if(user.pincode) {
                document.getElementById('headerLocText').innerText = `Deliver to ${user.name.split(' ')[0]} - ${user.pincode}`;
            } else {
                document.getElementById('headerLocText').innerText = `Deliver to Saved Address`;
            }
            document.getElementById('locationModal').style.display = 'none';
            showToast("Set to saved delivery address.");
        }
    };
});
