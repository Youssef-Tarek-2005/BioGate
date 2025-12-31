# BioGate - Simple Biometric IoT Security Simulation

import random
import hashlib
from datetime import datetime

# Simple data storage
users = {}
devices = {
    'DEV001': {'name': 'Smart Door', 'status': 'Active'},
    'DEV002': {'name': 'Security Camera', 'status': 'Active'},
    'DEV003': {'name': 'Access Terminal', 'status': 'Active'}
}
logs = []

# Generate fake biometric data
def generate_biometric():
    return [random.random() for _ in range(10)]

# Hash biometric for storage
def hash_biometric(bio_data):
    data_str = str(bio_data)
    return hashlib.sha256(data_str.encode()).hexdigest()

# Enroll new user
def enroll_user(user_id, name, bio_type):
    if user_id in users:
        return "Error: User already exists"
    
    bio_data = generate_biometric()
    users[user_id] = {
        'name': name,
        'bio_type': bio_type,
        'bio_hash': hash_biometric(bio_data)
    }
    
    log_event(user_id, "N/A", "Enrolled", f"User enrolled with {bio_type}")
    return f"Success: {name} enrolled!"

# Authenticate user
def authenticate(user_id, device_id, is_attack=False):
    # Check user exists
    if user_id not in users:
        log_event(user_id, device_id, "Failed", "User not found")
        return "FAILED: User not found"
    
    # Check device exists
    if device_id not in devices:
        log_event(user_id, device_id, "Failed", "Device not found")
        return "FAILED: Device not found"
    
    # Simulate attack detection
    if is_attack:
        if random.random() < 0.7:  # 70% chance to detect attack
            log_event(user_id, device_id, "Blocked", "Attack detected")
            return "BLOCKED: Security attack detected!"
    
    # Generate new biometric for authentication
    auth_bio = generate_biometric()
    
    # Simple matching (80% success for real users)
    if not is_attack and random.random() < 0.8:
        devices[device_id]['status'] = 'Active'
        log_event(user_id, device_id, "Success", "Authentication successful")
        return f"SUCCESS: {users[user_id]['name']} authenticated on {devices[device_id]['name']}"
    else:
        log_event(user_id, device_id, "Failed", "Biometric mismatch")
        return "FAILED: Biometric mismatch"

# Log events
def log_event(user_id, device_id, result, notes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append({
        'time': timestamp,
        'user': user_id,
        'device': device_id,
        'result': result,
        'notes': notes
    })

# Show all users
def show_users():
    print("\n=== ENROLLED USERS ===")
    for uid, data in users.items():
        print(f"{uid}: {data['name']} - {data['bio_type']}")

# Show all devices
def show_devices():
    print("\n=== IOT DEVICES ===")
    for did, data in devices.items():
        print(f"{did}: {data['name']} - Status: {data['status']}")

# Show logs
def show_logs():
    print("\n=== SECURITY LOGS ===")
    for log in logs[-10:]:  # Show last 10 logs
        print(f"[{log['time']}] User: {log['user']}, Device: {log['device']}, Result: {log['result']} - {log['notes']}")

# Simulate attack
def simulate_attack():
    device_id = random.choice(list(devices.keys()))
    attacks = ['Unauthorized Access', 'Firmware Tampering', 'Network Intrusion']
    attack = random.choice(attacks)
    
    devices[device_id]['status'] = 'Under Attack'
    log_event('SYSTEM', device_id, 'Attack', f'{attack} on {devices[device_id]["name"]}')
    return f"ALERT: {attack} detected on {devices[device_id]['name']}!"

# Main menu
def main():
    print("=" * 50)
    print("   BioGate - Biometric IoT Security Simulation")
    print("=" * 50)
    
    while True:
        print("\n--- MENU ---")
        print("1. Enroll User")
        print("2. Authenticate")
        print("3. Show Users")
        print("4. Show Devices")
        print("5. Show Logs")
        print("6. Simulate Attack")
        print("7. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            user_id = input("User ID: ")
            name = input("Name: ")
            bio_type = input("Biometric Type (Fingerprint/Face/Voice): ")
            print(generate_biometric())  # Show generated biometric
            result = enroll_user(user_id, name, bio_type)
            print(result)
            
        elif choice == '2':
            user_id = input("User ID: ")
            device_id = input("Device ID: ")
            attack = input("Simulate attack? (y/n): ").lower() == 'y'
            result = authenticate(user_id, device_id, attack)
            print(result)
            
        elif choice == '3':
            show_users()
            
        elif choice == '4':
            show_devices()
            
        elif choice == '5':
            show_logs()
            
        elif choice == '6':
            result = simulate_attack()
            print(result)
            
        elif choice == '7':
            print("Exiting BioGate...")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()