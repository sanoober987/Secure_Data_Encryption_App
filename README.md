# 🔐 Secure Vault

Secure Vault is a Streamlit-based web application designed to securely store and retrieve sensitive information using encryption and passkey protection. This project was built as a learning assignment to practice Python security concepts, encryption, authentication, and session management.

---

## 🚀 Features

- 🔒 Encrypt sensitive text using passkey-based encryption
- 🗝️ Unique Data ID generated for each stored entry
- 🔐 Passkey hashing for secure verification
- 🔄 Secure decryption only with correct passkey
- 🚫 Limited retry attempts (brute-force protection)
- ⏳ Temporary lockout after multiple failed attempts
- 🔑 Reauthorization (login) system
- 🧠 Session-based in-memory storage
- 🎨 Simple and clean Streamlit UI

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Cryptography (Fernet Encryption)**
- **Hashlib (SHA-256)**
- **UUID**
- **Base64 Encoding**

---

## 📂 How It Works

1. User enters sensitive data and creates a passkey
2. Data is encrypted using a key derived from the passkey
3. Encrypted data is stored with a unique Data ID
4. To retrieve data, user must provide:
   - Correct Data ID
   - Correct passkey
5. After 3 failed attempts, the app requires reauthorization
