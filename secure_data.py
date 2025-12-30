import streamlit as st
import hashlib
import json
import time
from cryptography.fernet import Fernet
import base64
import uuid

st.set_page_config(page_title= "Secure Vault" , page_icon= "🔐", layout="centered")

# --- Session State Initialization ---
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0

 # --- Utility Functions ---
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def generate_key_form_passkey(passkey):
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def encrypt_data(text, passkey):
    key = generate_key_form_passkey(passkey)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey, data_id):
    try:
        hashed_passkey = hash_passkey(passkey)
        if data_id in st.session_state.stored_data and st.session_state.stored_data[data_id]["passkey"] == hashed_passkey:
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attempts = 0
            return decrypted
        else:
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt_time = time.time()
            return None
    except Exception:
         st.session_state.failed_attempts += 1
         st.session_state.last_attempt_time = time.time()
         return None   

def generate_data_id():
    return str(uuid.uuid4())

def reset_failed_attempts():
    st.session_state.failed_attempts = 0

def change_page(page):
    st.session_state.current_page = page

 # --- App Layout ---
st.markdown("""
<style>
            .stButton>button{
            width : 100%;
            padding: 0,6em;
            font-weight: 600;
            border-radius: 0.5em;
            }
            .stTextInput input, .stTextArea textarea{
            border_radius: 0.5em;
            }
            </style>""" , unsafe_allow_html= True)

st.title("🔐 Secure Vault")
st.caption("Your private data is encrypted, protected, and only accessible with your unique passkey.")

 # --- Navigation ---
menu = ["Home", "Stored Data", "Retrieve Data", "Login"]
choice = st.sidebar.radio("📌 Navigate", menu , index=menu.index(st.session_state.current_page))
st.session_state.current_page = choice

if st.session_state.failed_attempts >= 3:
    st.session_state.current_page = "Login"
    st.warning("🔒 Too many failed attempts! Please reauthorize.")

 # --- Home Page ---
if st.session_state.current_page == "Home":
    st.subheader("🏠 Welcome")
    st.write("This app helps you **encrypt and protect your sensitive information** with a passkey. Store data securely and retrieve it with your unique ID.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Store New Data"):
            change_page("Stored Data")
    with col2:
        if st.button("🔍 Retrieve Data"):
            change_page("Retrieve Data")

    st.info("📦 Currently storing **{len(st.session_state.stored_data)}** secure data entries.")

 # --- Store Data ---
elif st.session_state.current_page == "Store Data":
    st.subheader("🛡️ Store Data Securely")
    user_data = st.text_area("🔏 Enter your secret message: ")
    passkey = st.audio_input("🔑 Choose a passkey:", type= "password")
    confirm_passkey = st.text_input("🔁 Confirm passkey:", type= "password")

    if st.button("💾 Encrypt & Save"):
        if not(user_data and passkey and confirm_passkey):
            st.error("❗ All fields are required!")
        elif passkey != confirm_passkey:
            st.error("❗ Passkeys do not match!")
        else:
            data_id = generate_data_id()
            encrypted_text = encrypt_data(user_data, passkey)  
            hashed_passkey = hash_passkey(passkey)

            st.session_state.stored_data[data_id] = {
                "encrypted_text": encrypted_text,
                "passkey" : hashed_passkey
            } 

            st.success("✅ Your data has been safely stored!")
            st.code(data_id, language= "text")
            st.info("📌 Keep this ID safe — it's the only way to retrieve your data.")

 # --- Retrieve Data ---
elif st.session_state.current_page == "Retrieve Data":
    st.subheader("🔓 Retrieve Stored Data")
    attempts_remaining = 3 - st.session_state.failed_attempts
    st.info(f"🔐 Attempts remaining: **{attempts_remaining}**")

    data_id = st.text_input("📄 Enter your Data ID: ")
    passkey = st.text_input("🔑 Enter your passkey:", type="password")

    if st.button("🚀 Decrypt"):
        if not (data_id and passkey):
            st.error("❗ Both fields are required!")
        elif data_id not in st.session_state.stored_data:
            st.error("❌ Data ID not found!")
        else:
            encrypted_text = st.session_state.stored_data[data_id["encrypted_text"]]
            decrypted_text = decrypt_data(encrypted_text, passkey, data_id)

            if decrypted_text:
                st.success("🎉 Decryption successful!")
                st.markdown("### 🔍 Your Decrypted Data: ")
                st.code(decrypted_text, language= "text")
            else:
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3 :
                    st.warning("🔒 Redirecting to login for reauthorization...")
                    st.rerun()

 # --- Login Page ---
elif st.session_state.current_page == "Login":
    st.subheader("🔑 Reauthorization Required")

    if time.time() - st.session_state.last_attempt_time < 10:
        remaining_time = int(10 - (time.time() - st.session_state.last_attempt_time))
        st.warning(f"🕒 Please wait {remaining_time} seconds before trying again.")
    else:
        login_pass = st.text_input("🛡️ Enter Master Password:", type="password")
        if st.button("✅ Login"):
            if login_pass == "admin123" : # replace in production
                reset_failed_attempts()
                st.success("🔓 Reauthorized successfully.")
                change_page("Home")
                st.rerun()
            else:
                st.error("❌ Incorrect password.")


# --- For Footer ---
st.markdown("---")
st.markdown("<center>🔐 <strong> Secure Vault</strong> | Built with ❤️ for learning and protection</center>", unsafe_allow_html= True)

