// Advanced form validation

function validateBooking() {
    const source = document.getElementById('source').value.trim();
    const destination = document.getElementById('destination').value.trim();
    const date = document.getElementById('date').value;

    if (source === "" || destination === "") {
        showNotification('Please fill all required fields!', 'error');
        return false;
    }

    // Check if source and destination are the same
    if (source.toLowerCase() === destination.toLowerCase()) {
        showNotification('Source and destination cannot be the same!', 'error');
        return false;
    }

    // Check if date is in the future
    if (date) {
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            showNotification('Please select a future date!', 'error');
            return false;
        }
    }

    showNotification('Searching for available bookings...', 'success');
    return true;
}

// Notification function
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 9999;
        animation: slideInNotification 0.3s ease-out;
        backdrop-filter: blur(10px);
        ${type === 'error' 
            ? 'background: rgba(244, 67, 54, 0.9); border: 1px solid #f44336;' 
            : 'background: rgba(76, 175, 80, 0.9); border: 1px solid #4caf50;'
        }
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutNotification 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInNotification {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutNotification {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Welcome message and initialization
window.onload = function() {
    console.log("TravelGo Platform Loaded");
    console.log("Modern UI Active");
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Initialize tooltips
    initializeTooltips();

    // Scrolling marquee animation for navbar links (desktop only).
    initNavbarMarquee();

    // Add a consistent back button on pages where navigation context is helpful.
    initPageBackButton();

    // Initialize payment widgets only when payment page elements are present.
    initPaymentPage();
}

// Redirect to an explicit error page for uncaught fetch/network failures.
window.addEventListener('unhandledrejection', function (event) {
    const reason = event && event.reason ? String(event.reason) : '';
    if (reason.toLowerCase().includes('failed to fetch')) {
        window.location.href = '/error/failed-fetch';
    }
});

function getBackFallbackPath(pathname) {
    const route = (pathname || '').toLowerCase();
    const fallbackMap = {
        '/': '/',
        '/payment': '/dashboard',
        '/bookings': '/dashboard',
        '/booking-confirmation': '/bookings',
        '/vehicle-details': '/vehicles',
        '/vehicles': '/dashboard',
        '/flights': '/dashboard',
        '/hotels': '/dashboard',
        '/search': '/dashboard',
        '/profile': '/dashboard',
        '/notifications': '/dashboard',
        '/offers': '/dashboard',
        '/reviews': '/dashboard',
        '/tips': '/dashboard',
        '/wishlist': '/dashboard',
        '/login': '/',
        '/register': '/'
    };

    for (const prefix in fallbackMap) {
        if (route.startsWith(prefix)) {
            return fallbackMap[prefix];
        }
    }

    return '/dashboard';
}

function initPageBackButton() {
    const path = window.location.pathname;
    if (path.startsWith('/error')) return;
    if (document.querySelector('.page-back-btn')) return;
    if (document.querySelector('.back-btn')) return;

    const container = document.querySelector('.container');
    if (!container) return;

    const backBtn = document.createElement('a');
    backBtn.href = '#';
    backBtn.className = 'page-back-btn';
    backBtn.setAttribute('aria-label', 'Go back');
    backBtn.innerHTML = '<span class="page-back-icon" aria-hidden="true">←</span><span class="page-back-text">Back</span>';

    backBtn.addEventListener('click', function (event) {
        event.preventDefault();

        if (window.history.length > 1) {
            window.history.back();
            return;
        }

        window.location.href = getBackFallbackPath(path);
    });

    container.prepend(backBtn);
}

function initNavbarMarquee() {
    const navContainers = document.querySelectorAll('.nav-links');
    if (!navContainers.length) return;
    if (document.body.classList.contains('no-nav-marquee')) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (window.matchMedia('(max-width: 768px)').matches) return;

    navContainers.forEach((nav) => {
        const track = document.createElement('div');
        track.className = 'nav-links-track';
        while (nav.firstChild) {
            track.appendChild(nav.firstChild);
        }
        nav.appendChild(track);

        const clone = track.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        nav.appendChild(clone);
    });
}

// Responsive sidebar toggle
function toggleSidebar() {
    const navLinks = document.querySelector('.nav-links');
    const overlay = document.querySelector('.nav-overlay');
    const hamburger = document.querySelector('.nav-hamburger');
    if (!navLinks) return;

    navLinks.classList.toggle('open');
    if (overlay) overlay.classList.toggle('active');
    if (hamburger) hamburger.classList.toggle('active');
    document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
}

// Close sidebar on Escape key
window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        const navLinks = document.querySelector('.nav-links');
        const overlay = document.querySelector('.nav-overlay');
        const hamburger = document.querySelector('.nav-hamburger');
        if (navLinks) navLinks.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        if (hamburger) hamburger.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Initialize tooltips
function initializeTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 0.5rem 0.75rem;
                border-radius: 5px;
                font-size: 0.85rem;
                white-space: nowrap;
                z-index: 1000;
            `;
            this.appendChild(tooltip);
        });
        
        el.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// Format phone number
function formatPhoneNumber(input) {
    input.value = input.value.replace(/\D/g, '').replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
}

// Add loading animation
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        backdrop-filter: blur(5px);
    `;
    
    overlay.innerHTML = `
        <div style="
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Payment page helpers
function initPaymentPage() {
    const upiInput = document.getElementById('upiId');
    const qrImage = document.getElementById('upiQrImage');

    if (qrImage) {
        renderUpiQrCode();
    }

    if (!upiInput) return;

    upiInput.addEventListener('input', function () {
        const payBtn = document.getElementById('upiPayBtn');
        const verifyStatus = document.getElementById('upiVerifyStatus');
        if (payBtn) {
            payBtn.disabled = true;
            payBtn.classList.remove('verified');
        }
        if (verifyStatus) {
            verifyStatus.innerHTML = '';
        }
    });
}

function switchPaymentTab(tab) {
    document.querySelectorAll('.payment-tab').forEach((item) => item.classList.remove('active'));
    document.querySelectorAll('.payment-panel').forEach((item) => item.classList.remove('active'));

    const selectedTab = document.querySelector('[data-tab="' + tab + '"]');
    const panel = document.getElementById('panel-' + tab);
    if (selectedTab) selectedTab.classList.add('active');
    if (panel) panel.classList.add('active');
}

function verifyUPI() {
    const upiInput = document.getElementById('upiId');
    const status = document.getElementById('upiVerifyStatus');
    const payBtn = document.getElementById('upiPayBtn');
    if (!upiInput || !status || !payBtn) return;

    const upiId = upiInput.value.trim();
    const upiPattern = /^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z][a-zA-Z]{2,64}$/;

    if (!upiId) {
        status.innerHTML = '<span class="upi-status-error">❌ Please enter a UPI ID</span>';
        payBtn.disabled = true;
        return;
    }

    if (!upiPattern.test(upiId)) {
        status.innerHTML = '<span class="upi-status-error">❌ Invalid UPI ID format</span>';
        payBtn.disabled = true;
        return;
    }

    status.innerHTML = '<span class="upi-status-loading">⏳ Verifying UPI ID...</span>';
    payBtn.disabled = true;

    setTimeout(function () {
        status.innerHTML = '<span class="upi-status-success">✅ UPI ID verified: ' + upiId + '</span>';
        payBtn.disabled = false;
        payBtn.classList.add('verified');
    }, 1200);
}

function formatCardNumber(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.replace(/(.{4})/g, '$1 ').trim();
    input.value = value;
}

function formatExpiry(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2);
    }
    input.value = value.substring(0, 5);
}

function updateCardPreview() {
    const number = document.getElementById('cardNumber');
    const name = document.getElementById('cardName');
    const expiry = document.getElementById('cardExpiry');

    const previewNumber = document.getElementById('cardPreviewNumber');
    const previewName = document.getElementById('cardPreviewName');
    const previewExpiry = document.getElementById('cardPreviewExpiry');

    if (previewNumber && number) {
        previewNumber.textContent = number.value || '•••• •••• •••• ••••';
    }
    if (previewName && name) {
        previewName.textContent = (name.value || 'YOUR NAME').toUpperCase();
    }
    if (previewExpiry && expiry) {
        previewExpiry.textContent = expiry.value || 'MM/YY';
    }
}

function renderUpiQrCode() {
    const qrImage = document.getElementById('upiQrImage');
    const fallback = document.getElementById('upiQrFallback');
    if (!qrImage) return;

    const totalAmountEl = document.querySelector('.payment-total-amount');
    const amountText = totalAmountEl ? totalAmountEl.textContent : '';
    const numericAmount = amountText ? (amountText.match(/[\d.]+/) || ['0'])[0] : '0';
    const txnRef = 'TG' + Date.now();

    const upiUri = [
        'upi://pay',
        '?pa=travelgo@upi',
        '&pn=TravelGo',
        '&tr=' + encodeURIComponent(txnRef),
        '&am=' + encodeURIComponent(numericAmount),
        '&cu=INR',
        '&tn=' + encodeURIComponent('TravelGo Booking Payment')
    ].join('');

    const qrSource = 'https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=' + encodeURIComponent(upiUri);

    qrImage.onload = function () {
        if (fallback) fallback.textContent = 'Scan and complete payment in your UPI app.';
    };

    qrImage.onerror = function () {
        if (fallback) {
            fallback.textContent = 'Unable to load QR right now. Please use UPI ID payment below.';
        }
    };

    qrImage.src = qrSource;
}

async function handleLocationTracking(button) {
    if (!button) return;

    const statusEl = button.parentElement ? button.parentElement.querySelector('.location-track-status') : null;
    const form = button.closest('form');
    const targetIds = (button.dataset.locationTargets || '')
        .split(',')
        .map((value) => value.trim())
        .filter(Boolean);

    if (!navigator.geolocation) {
        if (statusEl) statusEl.textContent = 'Geolocation is not supported on this device.';
        showNotification('Geolocation is not supported by your browser.', 'error');
        return;
    }

    button.disabled = true;
    if (statusEl) statusEl.textContent = 'Detecting your location...';

    navigator.geolocation.getCurrentPosition(
        async function (position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            let label = `Lat ${lat.toFixed(4)}, Lng ${lng.toFixed(4)}`;
            const reverseLabel = await reverseGeocodeLocation(lat, lng);
            if (reverseLabel) {
                label = reverseLabel;
            }

            targetIds.forEach((id) => {
                const input = document.getElementById(id);
                if (input) {
                    input.value = label;
                }
            });

            if (form) {
                const latInput = form.querySelector('input[name="user_lat"]');
                const lngInput = form.querySelector('input[name="user_lng"]');
                if (latInput) latInput.value = lat.toFixed(6);
                if (lngInput) lngInput.value = lng.toFixed(6);
            }

            await saveTrackedLocation(lat, lng, accuracy, label);

            if (statusEl) {
                statusEl.textContent = `Using: ${label}`;
            }
            showNotification('Current location added to your search.', 'success');
            button.disabled = false;
        },
        function (error) {
            let message = 'Unable to get location.';
            if (error.code === error.PERMISSION_DENIED) {
                message = 'Location permission denied.';
            } else if (error.code === error.POSITION_UNAVAILABLE) {
                message = 'Location information unavailable.';
            } else if (error.code === error.TIMEOUT) {
                message = 'Location request timed out.';
            }

            if (statusEl) statusEl.textContent = message;
            showNotification(message, 'error');
            button.disabled = false;
        },
        {
            enableHighAccuracy: true,
            timeout: 12000,
            maximumAge: 60000,
        }
    );
}

async function reverseGeocodeLocation(lat, lng) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lng)}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        if (!response.ok) return null;

        const data = await response.json();
        const address = data.address || {};
        const city = address.city || address.town || address.village || address.county;
        const state = address.state;
        const country = address.country;

        const parts = [city, state, country].filter(Boolean);
        return parts.length ? parts.join(', ') : null;
    } catch (error) {
        return null;
    }
}

async function saveTrackedLocation(latitude, longitude, accuracy, label) {
    try {
        await fetch('/api/location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                latitude,
                longitude,
                accuracy,
                label
            })
        });
    } catch (error) {
        // Silent fail, location is still useful locally for the current form.
    }
}