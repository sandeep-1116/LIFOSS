// Auth UI Toggling
function toggleAuthMode(mode) {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const forgotForm = document.getElementById('forgotForm');
    const leftLoginText = document.getElementById('left-login-text');
    const leftSignupText = document.getElementById('left-signup-text');
    const leftForgotText = document.getElementById('left-forgot-text');
    
    // Forms
    loginForm.style.display = 'none';
    signupForm.style.display = 'none';
    forgotForm.style.display = 'none';
    
    // Texts
    leftLoginText.style.display = 'none';
    leftSignupText.style.display = 'none';
    leftForgotText.style.display = 'none';

    if (mode === 'signup') {
        signupForm.style.display = 'flex';
        leftSignupText.style.display = 'block';
    } else if (mode === 'forgot') {
        forgotForm.style.display = 'flex';
        leftForgotText.style.display = 'block';
        // Reset Steps
        document.getElementById('forgotStep1').style.display = 'block';
        document.getElementById('forgotStep2').style.display = 'none';
    } else {
        loginForm.style.display = 'flex';
        leftLoginText.style.display = 'block';
    }
}

// Store email temporarily for reset
let resetEmail = "";

async function requestOTP() {
    const input = document.getElementById('forgotEmail').value;
    const errObj = document.getElementById('forgotError');
    errObj.style.display = 'none';

    if (!input) {
        errObj.innerText = "Please enter email or mobile.";
        errObj.style.display = 'block';
        return;
    }

    try {
        const res = await fetch('http://127.0.0.1:5000/api/forgot_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: input, phone: input })
        });
        const data = await res.json();

        if (res.ok) {
            resetEmail = data.email;
            alert(data.message); // Simulated OTP send
            document.getElementById('forgotStep1').style.display = 'none';
            document.getElementById('forgotStep2').style.display = 'block';
        } else {
            errObj.innerText = data.error;
            errObj.style.display = 'block';
        }
    } catch (e) {
        errObj.innerText = "Network Error: " + e.message;
        errObj.style.display = 'block';
    }
}

async function resetPasswordSubmit(e) {
    e.preventDefault();
    const otp = document.getElementById('forgotOTP').value;
    const newPass = document.getElementById('forgotNewPass').value;
    const errObj = document.getElementById('resetError');
    errObj.style.display = 'none';

    if (!otp || !newPass) {
        errObj.innerText = "Please fill all fields.";
        errObj.style.display = 'block';
        return;
    }

    try {
        const res = await fetch('http://127.0.0.1:5000/api/reset_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: resetEmail, otp: otp, new_password: newPass })
        });
        const data = await res.json();

        if (res.ok) {
            alert(data.message);
            toggleAuthMode('login');
        } else {
            errObj.innerText = data.error;
            errObj.style.display = 'block';
        }
    } catch (e) {
        errObj.innerText = "Network Error: " + e.message;
        errObj.style.display = 'block';
    }
}

// Ensure logged out users can't glitch forms if someone was logged in
document.addEventListener('DOMContentLoaded', () => {
    const user = localStorage.getItem('lifoss_user');
    if (user) {
        // Technically they shouldn't be here, redirect to home
        window.location.href = 'index.html';
    }
});

// Signup Form Submit
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const phone = document.getElementById('signupPhone').value;
    const password = document.getElementById('signupPassword').value;
    const errObj = document.getElementById('signupError');

    try {
        const res = await fetch('http://127.0.0.1:5000/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, password })
        });
        const data = await res.json();
        
        if (res.ok) {
            localStorage.setItem('lifoss_user', JSON.stringify(data.user));
            window.location.href = 'index.html'; // redirect to home
        } else {
            errObj.innerText = data.error || 'Registration failed.';
            errObj.style.display = 'block';
        }
    } catch (error) {
        console.error(error);
        errObj.innerText = 'System error: ' + (error.message === 'Failed to fetch' ? 'Backend server not responding. Please make sure the Flask server is running.' : error.message);
        errObj.style.display = 'block';
    }
});

// Login Form Submit
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const phone = document.getElementById('loginPhone').value;
    const password = document.getElementById('loginPassword').value;
    const errObj = document.getElementById('loginError');

    try {
        const res = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, phone, password })
        });
        const data = await res.json();
        
        if (res.ok) {
            localStorage.setItem('lifoss_user', JSON.stringify(data.user));
            window.location.href = 'index.html'; // redirect to home
        } else {
            errObj.innerText = data.error || 'Login failed.';
            errObj.style.display = 'block';
        }
    } catch (error) {
        console.error(error);
        errObj.innerText = 'System error: ' + (error.message === 'Failed to fetch' ? 'Backend server not responding. Please make sure the Flask server is running.' : error.message);
        errObj.style.display = 'block';
    }
});
