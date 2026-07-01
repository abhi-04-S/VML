const API_URL = "http://127.0.0.1:8000";

// --- DOM Elements ---
const authSection = document.getElementById("auth-section");
const appSection = document.getElementById("app-section");
const logoutBtn = document.getElementById("logout-btn");

const authForm = document.getElementById("auth-form");
const authTitle = document.getElementById("auth-title");
const authUsernameInput = document.getElementById("auth-username");
const authPasswordInput = document.getElementById("auth-password");
const authSubmitBtn = document.getElementById("auth-submit-btn");
const authToggleBtn = document.getElementById("auth-toggle-btn");
const authToggleText = document.getElementById("auth-toggle-text");

const noteForm = document.getElementById("note-form");
const noteTitleInput = document.getElementById("note-title");
const noteContentInput = document.getElementById("note-content");
const notesGrid = document.getElementById("notes-grid");

// --- State ---
let isLoginMode = true;

// --- Authentication Logic ---

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    if (isLoginMode) {
        authTitle.innerText = "Login to Your Account";
        authSubmitBtn.innerText = "Login";
        authToggleText.innerText = "Don't have an account?";
        authToggleBtn.innerText = "Register here";
    } else {
        authTitle.innerText = "Create an Account";
        authSubmitBtn.innerText = "Register";
        authToggleText.innerText = "Already have an account?";
        authToggleBtn.innerText = "Login here";
    }
}

authToggleBtn.addEventListener("click", toggleAuthMode);

authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = authUsernameInput.value;
    const password = authPasswordInput.value;

    if (isLoginMode) {
        await login(username, password);
    } else {
        await register(username, password);
    }
});

async function register(username, password) {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            alert("Registration successful! Please log in.");
            toggleAuthMode(); // Switch back to login
            authPasswordInput.value = ""; // Clear password for safety
        } else {
            const data = await response.json();
            alert(`Registration failed: ${data.detail}`);
        }
    } catch (error) {
        console.error("Register Error:", error);
    }
}

async function login(username, password) {
    try {
        // FastAPI's OAuth2 expects form data for login
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            // Save the token securely in the browser's local storage
            localStorage.setItem("note_token", data.access_token);
            showApp();
        } else {
            alert("Login failed: Incorrect username or password.");
        }
    } catch (error) {
        console.error("Login Error:", error);
    }
}

function logout() {
    localStorage.removeItem("note_token");
    showAuth();
}
logoutBtn.addEventListener("click", logout);

function showApp() {
    authSection.classList.add("hidden");
    appSection.classList.remove("hidden");
    logoutBtn.classList.remove("hidden");
    fetchNotes(); // Load notes when app is shown
}

function showAuth() {
    appSection.classList.add("hidden");
    logoutBtn.classList.add("hidden");
    authSection.classList.remove("hidden");
    authUsernameInput.value = "";
    authPasswordInput.value = "";
}

// Helper to get the auth headers for API requests
function getAuthHeaders() {
    const token = localStorage.getItem("note_token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

// --- Note Application Logic ---

async function fetchNotes() {
    try {
        const response = await fetch(`${API_URL}/notes/`, {
            headers: getAuthHeaders()
        });

        if (response.status === 401) {
            // Token expired or invalid
            logout();
            return;
        }

        const notes = await response.json();
        notesGrid.innerHTML = "";

        if (notes.length === 0) {
            notesGrid.innerHTML = `<div class="loading-state">No notes yet. Create your first secure note above!</div>`;
            return;
        }

        notes.forEach(note => {
            const noteElement = document.createElement("div");
            noteElement.classList.add("note-card");
            noteElement.innerHTML = `
                <h3>${note.title}</h3>
                <p>${note.content}</p>
            `;
            notesGrid.appendChild(noteElement);
        });
    } catch (error) {
        console.error("Error fetching notes:", error);
    }
}

async function saveNote(title, content) {
    try {
        const response = await fetch(`${API_URL}/notes/`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({ title, content })
        });

        if (response.ok) {
            fetchNotes();
            noteTitleInput.value = "";
            noteContentInput.value = "";
        } else if (response.status === 401) {
            logout();
        } else {
            alert("Failed to save note");
        }
    } catch (error) {
        console.error("Error saving note:", error);
    }
}

noteForm.addEventListener("submit", function (event) {
    event.preventDefault();
    saveNote(noteTitleInput.value, noteContentInput.value);
});

// --- Initialization ---
// Check if user is already logged in when the page loads
if (localStorage.getItem("note_token")) {
    showApp();
} else {
    showAuth();
}
