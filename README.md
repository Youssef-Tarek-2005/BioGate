# 🔐 BioGate - Biometric IoT Security Simulation

## 📋 Project Overview

**BioGate** is a comprehensive Python-based biometric IoT security simulation platform that demonstrates how biometric authentication and authorization systems work in IoT environments. This is an educational simulation using synthetic biometric data and simulated security features.

## 🎯 Key Features

### 🔐 Authentication System
- **Biometric Matching**: Vector similarity-based authentication using Euclidean distance
- **Multiple Biometric Types**: Face and Voice recognition simulation
- **Configurable Thresholds**: Adjustable biometric match thresholds
- **Real-time Validation**: Input validation for user and device IDs

### 🏭 IoT Device Management
- **Device Registration**: Automatic device creation with unique IDs
- **Status Tracking**: Active, Under Attack status management
- **Device Logging**: Access attempt tracking per device
- **Bulk Operations**: Reset all device statuses

### 🛡️ Security Features
- **Attack Simulation**: Simulate various attack types (Unauthorized Access, Firmware Tampering, Network Intrusion)
- **Attack Detection**: Configurable detection rates
- **Security Logging**: Comprehensive event logging with timestamps
- **Statistics Tracking**: Persistent statistics across sessions

### 📊 Data Management
- **Persistent Storage**: JSON-based data storage for users, devices, logs, and statistics
- **Data Recovery**: JSON corruption handling with recovery options
- **Collision Protection**: Robust ID generation with UUID fallback
- **Biometric Data Storage**: Original biometric templates for matching

### 🔍 User Interface
- **Command-Line Interface**: Clean, intuitive menu system
- **Search Functionality**: Find users by name with partial matching
- **Pagination**: Navigate through large log sets
- **Enhanced Statistics**: Detailed system metrics and settings display

## 🏗️ Architecture

### Class-Based Design
```python
BioGateSystem (Main Controller)
├── BiometricDevice (Device Management)
├── BiometricUser (User Management)
├── SecurityLogger (Logging System)
└── BiometricGenerator (Data Generation)
```

### Data Storage
- **`data/users.json`**: User enrollment data with biometric templates
- **`data/devices.json`**: IoT device information and status
- **`data/logs.json`**: Security event logs with timestamps
- **`data/stats.json`**: Persistent system statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- No external dependencies required

### Installation
```bash
git clone <repository-url>
cd BioGate
python main.py
```

### First Run
The system automatically creates the `data/` directory and initializes with:
- Empty user database
- Empty device database
- Empty security logs
- Default statistics

## 📖 Usage Guide

### Main Menu Options

#### 1. Enroll User
- Creates new users with unique 6-character IDs
- Automatically generates associated IoT devices
- Supports 3 biometric types via numbered menu
- Stores original biometric templates for matching

#### 2. Authenticate
- Validates user and device ID formats
- Performs biometric matching with configurable thresholds
- Supports attack simulation mode
- Resets device status from "Under Attack" to "Active"

#### 3. Show Users
- Displays all enrolled users with IDs and biometric types
- Shows user count and biometric type distribution

#### 4. Show Devices
- Lists all IoT devices with status information
- Displays device names and current states

#### 5. Show Logs
- Paginated security log viewing
- Supports filtering by user, device, or result
- Navigation hints for browsing large log sets

#### 6. Show Statistics
- Comprehensive system metrics
- User/device breakdowns with IDs
- Authentication success/failure rates
- Attack detection statistics
- Current system settings display

#### 7. Search User by Name
- Partial name matching
- Case-insensitive search
- Displays matching users with full details

#### 8. Simulate Attack
- Target specific devices for attack simulation
- Multiple attack types with randomization
- Configurable detection rates
- Automatic status updates

#### 9. Clear All Data
- Double-confirmation system for safety
- Complete data reset with warnings
- File cleanup and fresh initialization

#### 10. Configure Settings
- **Authentication Success Rate**: 0.0-1.0 (default: 80%)
- **Attack Detection Rate**: 0.0-1.0 (default: 70%)
- **Biometric Match Threshold**: 0.0-1.0 (default: 60%)
- **Reset Device Statuses**: Bulk status reset option

#### 11. Exit
- Saves all data before exit
- Clean program termination

## 🔧 Technical Details

### Biometric Matching Algorithm
```python
# Euclidean distance calculation
distance = sum((a - b) ** 2 for a, b in zip(bio1, bio2)) ** 0.5
similarity = max(0, 1 - (distance / max_distance))
```

### ID Generation
- **User IDs**: 6 alphanumeric characters with collision protection
- **Device IDs**: "DEV" + 4 digits with UUID fallback
- **Uniqueness**: 1000 attempts before UUID fallback

### Input Validation
- **User IDs**: 6-character alphanumeric validation
- **Device IDs**: "DEV####" format validation
- **Empty Input**: Prevention and error handling

### Error Handling
- **JSON Corruption**: Recovery options with user choice
- **File Permissions**: Graceful degradation
- **Data Loss**: Prevention with validation checks

## 📊 System Statistics

### Tracked Metrics
- Total enrollments by biometric type
- Successful/failed authentication counts
- Attack blocked/succeeded counts
- User and device counts
- Log entry counts

### Persistence
- Statistics saved to `data/stats.json`
- Automatic loading on startup
- Continuous tracking across sessions

## 🔒 Security Features

### Attack Simulation
- **Unauthorized Access**: Basic authentication bypass attempts
- **Firmware Tampering**: Device-level compromise simulation
- **Network Intrusion**: Communication-based attacks

### Detection System
- Configurable detection probability
- Randomized detection for realism
- Event logging with timestamps
- Status updates and alerts

## 🛠️ Development Notes

### Code Quality
- **Object-Oriented Design**: Modular class structure
- **Error Handling**: Comprehensive exception management
- **Documentation**: Detailed docstrings and comments
- **Type Safety**: Input validation and format checking

### Performance
- **Efficient Storage**: JSON-based persistence
- **Memory Management**: Optimized data structures
- **Collision Avoidance**: Robust ID generation
- **Scalability**: Designed for expansion

## 🚨 Limitations

### Educational Purpose
- **Simulation Only**: Not for production use
- **Synthetic Data**: No real biometric information
- **Simplified Security**: Educational demonstration, not real security
- **No Hardware**: Software-only simulation

### Technical Constraints
- **JSON Storage**: Not suitable for large-scale deployments
- **Single-Threaded**: No concurrent access handling
- **Local Only**: No network capabilities
- **Random Logic**: Attack detection uses probability, not ML

## 🔮 Future Enhancements

### Potential Improvements
- **GUI Interface**: PyQt5 or Tkinter frontend
- **Machine Learning**: Real biometric pattern recognition
- **Database Integration**: SQLite or MongoDB support
- **Network Features**: MQTT or HTTP communication
- **Multi-User**: Concurrent user support
- **Advanced Attacks**: More sophisticated attack simulations

### Scalability
- **Cloud Storage**: Remote data persistence
- **Load Balancing**: Multi-instance support
- **API Integration**: RESTful endpoints
- **Real Hardware**: Actual biometric device support

## 📝 License & Usage

### Educational Use
- **Free to Use**: Educational and learning purposes
- **Open Source**: Modify and distribute freely
- **Attribution**: Credit appreciated but not required
- **No Warranty**: Use at your own risk

### Restrictions
- **Commercial Use**: Not intended for production
- **Security Applications**: Not for real security systems
- **Data Privacy**: No real biometric data handling

---

## 🤝 Contributing

### Development
- **Bug Reports**: Submit issues with details
- **Feature Requests**: Open enhancement tickets
- **Code Contributions**: Fork and pull requests
- **Documentation**: Help improve README and comments

### Testing
- **Unit Tests**: Located in `tests/` directory
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing

---

**BioGate** - *Educational Biometric IoT Security Simulation* 🔐

*Version: 2.0 Enhanced Class-Based*  
*Last Updated: 2026*  
*Language: Python 3.8+*  
*Storage: JSON Files*  
*Interface: Command Line*