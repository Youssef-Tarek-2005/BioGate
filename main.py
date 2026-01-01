# BioGate - Biometric IoT Security Simulation (Refactored OOP)
# ========================================
# LIMITATIONS & RESTRICTIONS:
# - This is a SIMULATION for educational purposes only
# - Biometric data is FAKE (random numbers)
# - Security features are SIMULATED (not real encryption)
# - No actual biometric hardware integration
# - Database is persisted to files (users.json, devices.json, logs.json)
# - Attack detection is RANDOMIZED (not ML-based)
# ========================================

import random
import hashlib
from datetime import datetime
import string
import json
import os
import uuid
from collections import defaultdict

class BiometricDevice:
    """Individual IoT Device with biometric capabilities"""
    
    def __init__(self, device_id, name, status='Active'):
        self.device_id = device_id
        self.name = name
        self.status = status
        self.access_log = []
    
    def update_status(self, new_status):
        """Update device status"""
        self.status = new_status
    
    def log_access(self, user_id, result, timestamp):
        """Log access attempt"""
        self.access_log.append({
            'user_id': user_id,
            'result': result,
            'timestamp': timestamp
        })
    
    def to_dict(self):
        """Convert device to dictionary for JSON storage"""
        return {
            'name': self.name,
            'status': self.status
        }

class BiometricUser:
    """Individual user with biometric data"""
    
    def __init__(self, user_id, name, bio_type, bio_hash):
        self.user_id = user_id
        self.name = name
        self.bio_type = bio_type
        self.bio_hash = bio_hash
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.access_attempts = 0
        self.original_biometric = None
    
    def set_original_biometric(self, bio_data):
        """Store original biometric data for matching"""
        self.original_biometric = bio_data
    
    def increment_access_attempts(self):
        """Track access attempts"""
        self.access_attempts += 1
    
    def to_dict(self):
        """Convert user to dictionary for JSON storage"""
        data = {
            'name': self.name,
            'bio_type': self.bio_type,
            'bio_hash': self.bio_hash,
            'enrollment_date': self.enrollment_date,
            'access_attempts': self.access_attempts
        }
        if self.original_biometric:
            data['original_biometric'] = self.original_biometric
        return data

class SecurityLogger:
    """Handles security event logging"""
    
    def __init__(self):
        self.logs = []
        self.LOGS_FILE = "data/logs.json"
    
    def load_logs(self):
        """Load logs from file"""
        try:
            if os.path.exists(self.LOGS_FILE):
                with open(self.LOGS_FILE, 'r') as f:
                    self.logs = json.load(f)
            else:
                self.logs = []
        except Exception as e:
            print(f"Error loading logs: {e}")
            self.logs = []
    
    def save_logs(self):
        """Save logs to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.LOGS_FILE, 'w') as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            print(f"Error saving logs: {e}")
    
    def log_event(self, user_id, device_id, result, notes):
        """Log security events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'time': timestamp,
            'user': user_id,
            'device': device_id,
            'result': result,
            'notes': notes
        }
        self.logs.append(log_entry)
        self.save_logs()
    
    def get_filtered_logs(self, filter_user=None, filter_device=None, filter_result=None):
        """Get logs with optional filters"""
        filtered_logs = self.logs
        
        if filter_user:
            filtered_logs = [log for log in filtered_logs if log['user'] == filter_user]
        
        if filter_device:
            filtered_logs = [log for log in filtered_logs if log['device'] == filter_device]
        
        if filter_result:
            filtered_logs = [log for log in filtered_logs if log['result'] == filter_result]
        
        return filtered_logs
    
    def clear_logs(self):
        """Clear all logs"""
        self.logs = []

class BiometricGenerator:
    """Generates fake biometric data and IDs"""
    
    @staticmethod
    def generate_user_id(existing_ids=None):
        """Generate random user ID (6 characters) with proper collision protection"""
        if existing_ids is None:
            existing_ids = set()
        
        for _ in range(1000):  # Increased attempts for better collision protection
            user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if user_id not in existing_ids:
                return user_id
        # Fallback to UUID if all attempts fail
        return str(uuid.uuid4())[:8].upper()
    
    @staticmethod
    def generate_device_id(existing_ids=None):
        """Generate random device ID (DEV + 4 digits) with proper collision protection"""
        if existing_ids is None:
            existing_ids = set()
        
        for _ in range(1000):  # Increased attempts for better collision protection
            device_id = f"DEV{random.randint(1000, 9999)}"
            if device_id not in existing_ids:
                return device_id
        # Fallback to UUID if all attempts fail
        return f"DEV{str(uuid.uuid4())[:4].upper()}"
    
    @staticmethod
    def generate_biometric():
        """Generate fake biometric template (10 random values)"""
        return [round(random.random(), 6) for _ in range(10)]
    
    @staticmethod
    def hash_biometric(bio_data):
        """Simple hash of biometric data (for demo only)"""
        data_str = str(bio_data)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    @staticmethod
    def calculate_biometric_match(bio1, bio2):
        """Calculate biometric match score based on vector similarity"""
        if len(bio1) != len(bio2):
            return 0.0
        
        # Calculate Euclidean distance
        distance = sum((a - b) ** 2 for a, b in zip(bio1, bio2)) ** 0.5
        max_distance = (len(bio1) ** 0.5)  # Maximum possible distance
        
        # Convert to similarity score (0-1)
        similarity = max(0, 1 - (distance / max_distance))
        return round(similarity, 4)

class DataManager:
    """Handles data persistence and loading operations"""
    
    def __init__(self):
        self.USERS_FILE = "data/users.json"
        self.DEVICES_FILE = "data/devices.json"
        self.STATS_FILE = "data/stats.json"
        os.makedirs("data", exist_ok=True)
    
    def load_users(self):
        """Load users from file with error handling"""
        try:
            if os.path.exists(self.USERS_FILE):
                with open(self.USERS_FILE, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except json.JSONDecodeError as e:
            print(f"JSON corruption in users file: {e}")
            choice = input("Reset users data? (y/n): ").lower()
            if choice == 'y':
                print("Users data reset.")
                return {}
            else:
                print("Keeping existing users in memory.")
                return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def load_devices(self):
        """Load devices from file with error handling"""
        try:
            if os.path.exists(self.DEVICES_FILE):
                with open(self.DEVICES_FILE, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except json.JSONDecodeError as e:
            print(f"JSON corruption in devices file: {e}")
            choice = input("Reset devices data? (y/n): ").lower()
            if choice == 'y':
                print("Devices data reset.")
                return {}
            else:
                print("Keeping existing devices in memory.")
                return {}
        except Exception as e:
            print(f"Error loading devices: {e}")
            return {}
    
    def save_users(self, users):
        """Save users to file"""
        try:
            with open(self.USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def save_devices(self, devices):
        """Save devices to file"""
        try:
            with open(self.DEVICES_FILE, 'w') as f:
                json.dump(devices, f, indent=2)
        except Exception as e:
            print(f"Error saving devices: {e}")
    
    def clear_all_data_files(self):
        """Delete all data files"""
        files_to_delete = [self.USERS_FILE, self.DEVICES_FILE]
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                os.remove(file_path)

class StatisticsManager:
    """Manages system statistics tracking and persistence"""
    
    def __init__(self):
        self.STATS_FILE = "data/stats.json"
        self.stats = defaultdict(int)
        self.load_statistics()
    
    def load_statistics(self):
        """Load statistics from file"""
        try:
            if os.path.exists(self.STATS_FILE):
                with open(self.STATS_FILE, 'r') as f:
                    loaded_stats = json.load(f)
                    self.stats.update(loaded_stats)
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def save_statistics(self):
        """Save statistics to file"""
        try:
            with open(self.STATS_FILE, 'w') as f:
                json.dump(dict(self.stats), f, indent=2)
        except Exception as e:
            print(f"Error saving statistics: {e}")
    
    def increment_stat(self, stat_name):
        """Increment a statistic"""
        self.stats[stat_name] += 1
    
    def get_stat(self, stat_name):
        """Get a statistic value"""
        return self.stats.get(stat_name, 0)
    
    def get_all_stats(self):
        """Get all statistics"""
        return dict(self.stats)
    
    def clear_stats(self):
        """Clear all statistics"""
        self.stats.clear()

class InputValidator:
    """Handles input validation for the system"""
    
    @staticmethod
    def validate_user_id(user_id):
        """Validate user ID format"""
        if not user_id:
            return False, "User ID cannot be empty"
        
        user_id = user_id.strip()
        if len(user_id) != 6:
            return False, "User ID must be 6 characters"
        
        if not user_id.isalnum():
            return False, "User ID must be alphanumeric"
        
        return True, "Valid"
    
    @staticmethod
    def validate_device_id(device_id):
        """Validate device ID format"""
        if not device_id:
            return False, "Device ID cannot be empty"
        
        device_id = device_id.strip()
        if not device_id.startswith('DEV'):
            return False, "Device ID must start with 'DEV'"
        
        if len(device_id) != 7:
            return False, "Device ID must be 7 characters (DEV + 4 digits)"
        
        if not device_id[3:].isdigit():
            return False, "Device ID must have 4 digits after 'DEV'"
        
        return True, "Valid"
    
    @staticmethod
    def validate_rate(rate, rate_name):
        """Validate rate input (0.0-1.0)"""
        try:
            rate_value = float(rate)
            if 0.0 <= rate_value <= 1.0:
                return True, rate_value
            else:
                return False, f"{rate_name} must be between 0.0 and 1.0"
        except ValueError:
            return False, f"Please enter a valid number for {rate_name}"

class AuthenticationEngine:
    """Handles biometric authentication logic"""
    
    def __init__(self, biometric_threshold=0.6, auth_success_rate=0.8):
        self.biometric_threshold = biometric_threshold
        self.auth_success_rate = auth_success_rate
    
    def authenticate_user(self, user, device, is_attack=False):
        """Perform authentication with biometric matching"""
        # Generate new biometric for authentication attempt
        auth_bio = BiometricGenerator.generate_biometric()
        
        # Calculate biometric match score
        if hasattr(user, 'original_biometric') and user.original_biometric:
            stored_bio = user.original_biometric
            match_score = BiometricGenerator.calculate_biometric_match(stored_bio, auth_bio)
            
            # Use configurable threshold + match score for more realistic authentication
            success = match_score >= self.biometric_threshold and random.random() < self.auth_success_rate
            
            return success, match_score
        else:
            # Fallback to random authentication for backward compatibility
            success = not is_attack and random.random() < self.auth_success_rate
            return success, 0.0
    
    def update_threshold(self, new_threshold):
        """Update biometric match threshold"""
        self.biometric_threshold = new_threshold
    
    def update_auth_rate(self, new_rate):
        """Update authentication success rate"""
        self.auth_success_rate = new_rate

class AttackSimulator:
    """Handles attack simulation and detection"""
    
    def __init__(self, attack_detection_rate=0.7):
        self.attack_detection_rate = attack_detection_rate
        self.attack_types = ['Unauthorized Access', 'Firmware Tampering', 'Network Intrusion']
    
    def simulate_attack(self, device_id, device_name):
        """Simulate an attack on a device"""
        attack = random.choice(self.attack_types)
        
        # Check if attack is detected
        if random.random() < self.attack_detection_rate:
            return True, attack, f"🚫 BLOCKED: Security attack detected! {attack} on {device_name}"
        else:
            return False, attack, f"🚨 ALERT: {attack} detected on {device_name}!"
    
    def update_detection_rate(self, new_rate):
        """Update attack detection rate"""
        self.attack_detection_rate = new_rate

class UserInterface:
    """Handles user interface and menu operations"""
    
    def __init__(self):
        self.valid_biometric_types = ['Face', 'Voice']
    
    def get_valid_biometric_type(self):
        """Get valid biometric type from user input with numbered menu"""
        print("\nSelect Biometric Type:")
        for i, bio_type in enumerate(self.valid_biometric_types, 1):
            print(f"{i}. {bio_type}")
        
        while True:
            try:
                choice = input("Enter choice (1-2): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.valid_biometric_types):
                    return self.valid_biometric_types[int(choice) - 1]
                else:
                    print(f"❌ Invalid choice! Please enter 1-{len(self.valid_biometric_types)}")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n--- MENU ---")
        print("1. Enroll User")
        print("2. Authenticate")
        print("3. Show Users")
        print("4. Show Devices")
        print("5. Show Logs")
        print("6. Show Statistics")
        print("7. Search User by Name")
        print("8. Simulate Attack")
        print("9. Clear All Data")
        print("10. Configure Settings")
        print("11. Exit")
    
    def get_user_choice(self):
        """Get user menu choice"""
        return input("\nEnter choice: ").strip()
    
    def search_users_by_name(self, users, search_term):
        """Search for users by name (partial match)"""
        name = search_term.lower().strip()
        matches = []
        
        for user_id, user_data in users.items():
            if name in user_data['name'].lower():
                matches.append((user_id, user_data))
        
        return matches

class BioGateController:
    """Main controller that coordinates all system components"""
    
    def __init__(self):
        # Initialize all components
        self.data_manager = DataManager()
        self.statistics_manager = StatisticsManager()
        self.logger = SecurityLogger()
        self.biometric_gen = BiometricGenerator()
        self.input_validator = InputValidator()
        self.auth_engine = AuthenticationEngine()
        self.attack_simulator = AttackSimulator()
        self.ui = UserInterface()
        
        # Load existing data
        self.users = {}
        self.devices = {}
        self.load_system_data()
    
    def load_system_data(self):
        """Load all system data"""
        self.users = self.data_manager.load_users()
        self.devices = self.data_manager.load_devices()
        self.logger.load_logs()
        
        # Ensure all users have original_biometric field
        for user_id, user_data in self.users.items():
            if 'original_biometric' not in user_data:
                user_data['original_biometric'] = self.biometric_gen.generate_biometric()
    
    def save_system_data(self):
        """Save all system data"""
        self.data_manager.save_users(self.users)
        self.data_manager.save_devices(self.devices)
        self.statistics_manager.save_statistics()
    
    def enroll_user(self, name, bio_type):
        """Enroll a new user with biometric data"""
        # Generate random user ID (ensure uniqueness)
        user_id = self.biometric_gen.generate_user_id(self.users.keys())
        
        # Generate random device and add it
        device_id = self.biometric_gen.generate_device_id(self.devices.keys())
        
        # Create device object
        device = BiometricDevice(device_id, f'IoT Device {device_id}', 'Active')
        self.devices[device_id] = device.to_dict()
        
        # Generate biometric data and create user
        bio_data = self.biometric_gen.generate_biometric()
        bio_hash = self.biometric_gen.hash_biometric(bio_data)
        user = BiometricUser(user_id, name, bio_type, bio_hash)
        user.set_original_biometric(bio_data)
        self.users[user_id] = user.to_dict()
        
        # Update statistics
        self.statistics_manager.increment_stat('total_enrollments')
        self.statistics_manager.increment_stat(f'enrollments_{bio_type.lower()}')
        
        # Log enrollment
        self.logger.log_event(user_id, device_id, "Enrolled", f"User enrolled with {bio_type}")
        self.save_system_data()
        return f"✅ Success: {name} enrolled!\n🆔 User ID: {user_id}\n🔧 Device ID: {device_id}"
    
    def authenticate_user(self, user_id, device_id, is_attack=False):
        """Authenticate user and grant/deny access"""
        # Validate input formats
        user_valid, user_msg = self.input_validator.validate_user_id(user_id)
        if not user_valid:
            return f"❌ FAILED: {user_msg}"
        
        device_valid, device_msg = self.input_validator.validate_device_id(device_id)
        if not device_valid:
            return f"❌ FAILED: {device_msg}"
        
        # Check user exists
        if user_id not in self.users:
            self.logger.log_event(user_id, device_id, "Failed", "User not found")
            self.statistics_manager.increment_stat('failed_authentications')
            self.save_system_data()
            return "❌ FAILED: User not found"
        
        # Check device exists
        if device_id not in self.devices:
            self.logger.log_event(user_id, device_id, "Failed", "Device not found")
            self.statistics_manager.increment_stat('failed_authentications')
            self.save_system_data()
            return "❌ FAILED: Device not found"
        
        # Reset device status if it was under attack
        if self.devices[device_id]['status'] == 'Under Attack':
            self.devices[device_id]['status'] = 'Active'
            print(f"🔄 Device {device_id} status reset to Active")
        
        # Simulate attack detection if needed
        if is_attack:
            detected, attack_type, message = self.attack_simulator.simulate_attack(device_id, self.devices[device_id]['name'])
            if detected:
                self.logger.log_event(user_id, device_id, "Blocked", "Attack detected")
                self.statistics_manager.increment_stat('attacks_blocked')
                self.save_system_data()
                return message
            else:
                self.statistics_manager.increment_stat('attacks_succeeded')
                self.devices[device_id]['status'] = 'Under Attack'
                self.logger.log_event('SYSTEM', device_id, 'Attack', f'{attack_type} on {self.devices[device_id]["name"]}')
                self.save_system_data()
                return message
        
        # Perform biometric authentication
        user_data = self.users[user_id]
        success, match_score = self.auth_engine.authenticate_user(user_data, self.devices[device_id], is_attack)
        
        if success:
            self.devices[device_id]['status'] = 'Active'
            self.logger.log_event(user_id, device_id, "Success", f"Authentication successful (match: {match_score:.2%})")
            self.statistics_manager.increment_stat('successful_authentications')
            self.save_system_data()
            return f"✅ SUCCESS: {user_data['name']} authenticated on {self.devices[device_id]['name']} (Match: {match_score:.2%})"
        else:
            self.logger.log_event(user_id, device_id, "Failed", f"Biometric mismatch (match: {match_score:.2%})")
            self.statistics_manager.increment_stat('failed_authentications')
            self.save_system_data()
            return f"❌ FAILED: Biometric mismatch (Match: {match_score:.2%})"
    
    def show_users(self):
        """Display all enrolled users"""
        print("\n=== ENROLLED USERS ===")
        if not self.users:
            print("No users enrolled yet. Use option 1 to enroll a user.")
        else:
            for uid, data in self.users.items():
                print(f"{uid}: {data['name']} - {data['bio_type']}")
    
    def show_devices(self):
        """Display all IoT devices"""
        print("\n=== IOT DEVICES ===")
        if not self.devices:
            print("No devices available. Enroll a user to create devices.")
        else:
            for did, data in self.devices.items():
                print(f"{did}: {data['name']} - Status: {data['status']}")
    
    def show_logs(self, page=1, per_page=10, filter_user=None, filter_device=None, filter_result=None):
        """Display security logs with pagination and filtering"""
        print("\n=== SECURITY LOGS ===")
        
        filtered_logs = self.logger.get_filtered_logs(filter_user, filter_device, filter_result)
        
        if not filtered_logs:
            print("No security logs available. Perform actions to generate logs.")
            return
        
        total_logs = len(filtered_logs)
        total_pages = (total_logs + per_page - 1) // per_page
        
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        print(f"Page {page} of {total_pages} (Total: {total_logs} logs)")
        
        if filter_user or filter_device or filter_result:
            filters = []
            if filter_user:
                filters.append(f"User: {filter_user}")
            if filter_device:
                filters.append(f"Device: {filter_device}")
            if filter_result:
                filters.append(f"Result: {filter_result}")
            print(f"Filters: {', '.join(filters)}")
        
        for log in filtered_logs[start_idx:end_idx]:
            print(f"[{log['time']}] User: {log['user']}, Device: {log['device']}, Result: {log['result']} - {log['notes']}")
        
        if total_pages > 1:
            print(f"\nNavigation: Use 'show_logs {page+1}' for next page, 'show_logs {page-1}' for previous")
    
    def show_statistics(self):
        """Display system statistics and summary"""
        print("\n📊 === SYSTEM STATISTICS ===")
        
        stats = self.statistics_manager.get_all_stats()
        
        # User statistics
        total_users = len(self.users)
        print(f"\n👥 Users: {total_users}")
        if total_users > 0:
            bio_types = defaultdict(int)
            for user in self.users.values():
                bio_types[user['bio_type']] += 1
            for bio_type, count in bio_types.items():
                print(f"   {bio_type}: {count}")
            
            # Show user details
            print("\n📋 User Details:")
            for user_id, user_data in list(self.users.items())[:5]:
                print(f"   {user_id}: {user_data['name']} ({user_data['bio_type']})")
            if total_users > 5:
                print(f"   ... and {total_users - 5} more users")
        
        # Device statistics
        total_devices = len(self.devices)
        active_devices = sum(1 for d in self.devices.values() if d['status'] == 'Active')
        print(f"\n🔧 Devices: {total_devices} total, {active_devices} active")
        
        if total_devices > 0:
            # Show device details
            print("\n📋 Device Details:")
            for device_id, device_data in list(self.devices.items())[:5]:
                print(f"   {device_id}: {device_data['name']} ({device_data['status']})")
            if total_devices > 5:
                print(f"   ... and {total_devices - 5} more devices")
        
        # Authentication statistics
        total_auth = stats.get('successful_authentications', 0) + stats.get('failed_authentications', 0)
        print(f"\n🔐 Authentications: {total_auth} total")
        if total_auth > 0:
            success_rate = (stats.get('successful_authentications', 0) / total_auth) * 100
            print(f"   ✅ Successful: {stats.get('successful_authentications', 0)} ({success_rate:.1f}%)")
            print(f"   ❌ Failed: {stats.get('failed_authentications', 0)} ({100-success_rate:.1f}%)")
        
        # Attack statistics
        total_attacks = stats.get('attacks_blocked', 0) + stats.get('attacks_succeeded', 0)
        print(f"\n🚨 Attacks: {total_attacks} total")
        if total_attacks > 0:
            block_rate = (stats.get('attacks_blocked', 0) / total_attacks) * 100
            print(f"   🚫 Blocked: {stats.get('attacks_blocked', 0)} ({block_rate:.1f}%)")
            print(f"   ⚠️  Succeeded: {stats.get('attacks_succeeded', 0)} ({100-block_rate:.1f}%)")
        
        # Enrollment statistics
        print(f"\n📝 Enrollments: {stats.get('total_enrollments', 0)} total")
        
        # Log statistics
        total_logs = len(self.logger.logs)
        print(f"\n📋 Logs: {total_logs} total entries")
        
        if total_logs > 0:
            print(f"   Recent activity: {min(total_logs, 10)} latest entries available")
        
        # System settings
        print(f"\n⚙️ Current Settings:")
        print(f"   Authentication Success Rate: {self.auth_engine.auth_success_rate:.0%}")
        print(f"   Attack Detection Rate: {self.attack_simulator.attack_detection_rate:.0%}")
        print(f"   Biometric Match Threshold: {self.auth_engine.biometric_threshold:.0%}")
    
    def search_user_menu(self):
        """Handle user search menu"""
        print("\n🔍 === SEARCH USER ===")
        
        if not self.users:
            print("No users enrolled yet. Use option 1 to enroll a user.")
            return
        
        search_term = input("Enter name to search (or 'cancel'): ").strip()
        if search_term.lower() == 'cancel':
            return
        
        matches = self.ui.search_users_by_name(self.users, search_term)
        
        if matches:
            print(f"\nFound {len(matches)} user(s) matching '{search_term}':")
            for user_id, user_data in matches:
                print(f"🆔 {user_id}: {user_data['name']} - {user_data['bio_type']}")
        else:
            print(f"No users found matching '{search_term}'")
    
    def simulate_attack_menu(self):
        """Handle attack simulation menu"""
        if not self.devices:
            return "Error: No devices available to attack! Enroll a user first."
        
        print("\nAvailable devices:")
        for did, data in self.devices.items():
            print(f"{did}: {data['name']} - Status: {data['status']}")
        
        device_id = input("\nEnter device ID to attack: ").strip()
        
        if device_id not in self.devices:
            return f"Error: Device {device_id} not found!"
        
        return self.authenticate_user("ATTACKER", device_id, is_attack=True)
    
    def clear_all_data(self):
        """Clear all users, devices, and logs with confirmation"""
        print("\n⚠️ === DATA CLEARING WARNING ===")
        print("This will PERMANENTLY delete:")
        print(f"• {len(self.users)} enrolled users")
        print(f"• {len(self.devices)} IoT devices")
        print(f"• {len(self.logger.logs)} security logs")
        print(f"• All statistics and history")
        print("\nThis action CANNOT be undone!")
        
        confirm = input("Type 'DELETE' to confirm: ").strip()
        if confirm != 'DELETE':
            return "❌ Data clear cancelled. No changes made."
        
        try:
            # Clear in-memory data
            self.users = {}
            self.devices = {}
            self.logger.clear_logs()
            self.statistics_manager.clear_stats()
            
            # Delete data files
            self.data_manager.clear_all_data_files()
            
            # Save fresh state
            self.save_system_data()
            self.logger.save_logs()
            
            return "✅ All data cleared successfully! System reset to default state."
        except Exception as e:
            return f"❌ Error clearing data: {e}"
    
    def configure_settings(self):
        """Configure system settings"""
        print("\n⚙️ === SYSTEM SETTINGS ===")
        print(f"1. Authentication Success Rate: {self.auth_engine.auth_success_rate:.0%}")
        print(f"2. Attack Detection Rate: {self.attack_simulator.attack_detection_rate:.0%}")
        print(f"3. Biometric Match Threshold: {self.auth_engine.biometric_threshold:.0%}")
        print("4. Reset All Device Statuses")
        print("5. Back to main menu")
        
        choice = input("\nSelect setting to configure: ").strip()
        
        if choice == '1':
            valid, new_rate = self.input_validator.validate_rate(
                input("Enter new authentication success rate (0.0-1.0): "), 
                "Authentication success rate"
            )
            if valid:
                self.auth_engine.update_auth_rate(new_rate)
                print(f"✅ Authentication success rate set to {new_rate:.0%}")
            else:
                print(f"❌ {new_rate}")
        
        elif choice == '2':
            valid, new_rate = self.input_validator.validate_rate(
                input("Enter new attack detection rate (0.0-1.0): "), 
                "Attack detection rate"
            )
            if valid:
                self.attack_simulator.update_detection_rate(new_rate)
                print(f"✅ Attack detection rate set to {new_rate:.0%}")
            else:
                print(f"❌ {new_rate}")
        
        elif choice == '3':
            valid, new_threshold = self.input_validator.validate_rate(
                input("Enter new biometric match threshold (0.0-1.0): "), 
                "Biometric match threshold"
            )
            if valid:
                self.auth_engine.update_threshold(new_threshold)
                print(f"✅ Biometric match threshold set to {new_threshold:.0%}")
            else:
                print(f"❌ {new_threshold}")
        
        elif choice == '4':
            self.reset_device_statuses()
        
        elif choice == '5':
            return
        
        else:
            print("❌ Invalid choice")
    
    def reset_device_statuses(self):
        """Reset all device statuses to Active"""
        devices_reset = 0
        for device_id in self.devices:
            if self.devices[device_id]['status'] != 'Active':
                self.devices[device_id]['status'] = 'Active'
                devices_reset += 1
        
        if devices_reset > 0:
            self.save_system_data()
            print(f"✅ Reset {devices_reset} device(s) to Active status")
        else:
            print("ℹ️  All devices already have Active status")
    
    def run(self):
        """Run the main application"""
        print("=" * 50)
        print("   BioGate - Biometric IoT Security Simulation")
        print("=" * 50)
        
        while True:
            self.ui.display_menu()
            choice = self.ui.get_user_choice()
            
            if choice == '1':
                name = input("Name: ")
                bio_type = self.ui.get_valid_biometric_type()
                result = self.enroll_user(name, bio_type)
                print(result)
                
            elif choice == '2':
                user_id = input("User ID: ")
                device_id = input("Device ID: ")
                attack = input("Simulate attack? (y/n): ").lower() == 'y'
                result = self.authenticate_user(user_id, device_id, attack)
                print(result)
                
            elif choice == '3':
                self.show_users()
                
            elif choice == '4':
                self.show_devices()
                
            elif choice == '5':
                self.show_logs()
                
            elif choice == '6':
                self.show_statistics()
                
            elif choice == '7':
                self.search_user_menu()
                
            elif choice == '8':
                result = self.simulate_attack_menu()
                print(result)
                
            elif choice == '9':
                result = self.clear_all_data()
                print(result)
                
            elif choice == '10':
                self.configure_settings()
                
            elif choice == '11':
                print("Exiting BioGate...")
                break
            
            else:
                print("Invalid choice!")

# Main execution
if __name__ == "__main__":
    # Create and run BioGate system
    biogate = BioGateController()
    biogate.run()
