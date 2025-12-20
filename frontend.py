import streamlit as st
import requests
import os
import time

# --- CONFIG ---
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RefundOps Bot", page_icon="✈️", layout="wide")

# --- STYLES ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .running {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .stopped {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .log-container {
        max-height: 400px;
        overflow-y: scroll;
        background-color: #0e1117;
        color: #dcdcdc;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        border-radius: 5px;
        border: 1px solid #30333d;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# --- FUNCTIONS ---
def check_status():
    try:
        res = requests.get(f"{BACKEND_URL}/status")
        if res.status_code == 200:
            return res.json().get("running", False)
    except:
        return False
    return False

def get_logs():
    try:
        res = requests.get(f"{BACKEND_URL}/logs")
        if res.status_code == 200:
            return res.json().get("logs", [])
    except:
        return []
    return []

def login(email, password):
    try:
        res = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
        if res.status_code == 200:
            return True, "Login Successful"
        else:
            return False, f"Login Failed: {res.text}"
    except Exception as e:
        return False, f"Connection Error: {e}"

def start_bot():
    try:
        requests.post(f"{BACKEND_URL}/start")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to start bot: {e}")

def stop_bot():
    try:
        requests.post(f"{BACKEND_URL}/stop")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to stop bot: {e}")

# --- PAGES ---

if not st.session_state.logged_in:
    # LOGIN PAGE
    st.title("✈️ RefundOps Login")
    
    with st.form("login_form"):
        email = st.text_input("Gmail Address")
        password = st.text_input("App Password (16 characters)", type="password")
        submitted = st.form_submit_button("Update Credentials & Login")
        
        if submitted:
            if email and password:
                success, msg = login(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please enter both email and password")
else:
    # DASHBOARD
    st.title("🤖 RefundOps Dashboard")
    st.write(f"Logged in as: **{st.session_state.user_email}**")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # STATUS SECTION
    is_running = check_status()
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if is_running:
            st.markdown('<div class="status-box running">Status: 🟢 RUNNING</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box stopped">Status: 🔴 STOPPED</div>', unsafe_allow_html=True)
            
    with col2:
        if is_running:
            if st.button("Stop Bot 🛑"):
                stop_bot()
        else:
            if st.button("Start Bot ▶️"):
                start_bot()

    st.divider()
    
    # LOGS SECTION (New)
    st.subheader("📜 Live Process Logs")
    logs = get_logs()
    
    if logs:
        # Join logs and escape HTML if necessary, but log text is usually safe for basic display
        # We put it in a scrollable container
        log_content = "<br>".join(logs)
        st.markdown(f'<div class="log-container">{log_content}</div>', unsafe_allow_html=True)
    else:
        st.info("No logs available yet. Start the bot!")

    st.divider()
    
    # SCREENSHOTS SECTION
    st.subheader("📸 Screenshot Gallery")
    if st.button("Refresh Gallery"):
        st.rerun()
        
    try:
        res = requests.get(f"{BACKEND_URL}/screenshots")
        if res.status_code == 200:
            images = res.json().get("screenshots", [])
            if images:
                # Display in grid
                cols = st.columns(3)
                for idx, img_path in enumerate(images):
                    with cols[idx % 3]:
                        st.image(img_path, caption=img_path, use_container_width=True)
            else:
                st.info("No screenshots found yet. Run the bot to generate some!")
    except Exception as e:
        st.error(f"Could not load images: {e}")
    
    # Auto-refresh if running
    if is_running:
        time.sleep(2)
        st.rerun()
