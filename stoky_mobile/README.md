# STOKY Mobile - Flutter Android App Setup

Welcome to STOKY Mobile! This guide will help you set up and run the Flutter app on your Android device.

## 📱 What is STOKY Mobile?

STOKY Mobile is the Android companion app for the STOKY Stock Advisor platform. It provides:

- **AI-Powered Stock Predictions**: Advanced machine learning models for accurate price forecasting
- **Real-Time Market Data**: Live stock prices and comprehensive market information
- **Multi-Currency Support**: Global markets with localized currency display
- **Technical Analysis**: Professional-grade indicators and analysis tools
- **User-Friendly Interface**: Beautiful, intuitive design optimized for mobile

## 🚀 Quick Setup Guide

### Prerequisites

1. **Flutter SDK** (Latest stable version)
2. **Android Studio** with Android SDK
3. **Android Device** or Emulator (Android 5.0+ / API Level 21+)
4. **STOKY Backend** running (see backend setup in root folder)

### Step 1: Install Flutter

**Windows:**
```cmd
# Download Flutter SDK from https://docs.flutter.dev/get-started/install/windows
# Extract to C:\flutter
# Add C:\flutter\bin to your PATH

# Verify installation
flutter doctor
```

**macOS:**
```bash
# Using Homebrew
brew install flutter

# Or download from https://docs.flutter.dev/get-started/install/macos
# Verify installation
flutter doctor
```

**Linux:**
```bash
# Download Flutter SDK
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.0-stable.tar.xz
tar xf flutter_linux_*.tar.xz

# Add to PATH
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

### Step 2: Set Up Android Development

1. **Install Android Studio**: Download from https://developer.android.com/studio
2. **Install Android SDK**: Use Android Studio's SDK Manager
3. **Create Virtual Device** (optional): Use Android Studio's AVD Manager
4. **Enable Developer Options** on your physical device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go to Settings > Developer Options
   - Enable "USB Debugging"

### Step 3: Clone and Setup Project

```bash
# Navigate to the STOKY project folder
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"

# Navigate to Flutter app
cd stoky_mobile

# Get dependencies
flutter pub get

# Check for any issues
flutter doctor

# Verify devices
flutter devices
```

### Step 4: Configure Backend Connection

Edit `lib/utils/constants.dart` to match your backend URL:

```dart
class Constants {
  // Update this to your backend URL
  static const String baseUrl = 'http://YOUR_COMPUTER_IP:8000';
  
  // For local development, use your computer's IP address
  // Find it with: ipconfig (Windows) or ifconfig (Mac/Linux)
  // Example: 'http://192.168.1.100:8000'
}
```

### Step 5: Run the App

```bash
# Run on connected device/emulator
flutter run

# Or run in debug mode
flutter run --debug

# For release build
flutter build apk --release
```

## 📋 Backend Setup Requirements

Make sure your STOKY backend is running:

```bash
# In the main STOKY folder
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

The backend should be accessible at `http://localhost:8000` or your computer's IP address.

## 🔧 Troubleshooting

### Common Issues:

**1. Flutter Doctor Issues:**
```bash
flutter doctor --verbose
```
Follow the suggestions to fix any issues.

**2. Android License Issues:**
```bash
flutter doctor --android-licenses
```
Accept all licenses.

**3. Gradle Build Fails:**
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

**4. Network Connection Issues:**
- Ensure your phone and computer are on the same WiFi network
- Check Windows Firewall settings
- Verify the backend URL in `constants.dart`

**5. USB Debugging Not Working:**
- Install device drivers
- Try different USB cables
- Enable "Install via USB" in developer options

### Device-Specific Setup:

**Samsung Devices:**
- May need Samsung USB drivers
- Enable "Install via USB" in addition to USB debugging

**Xiaomi/MIUI Devices:**
- Enable "Install via USB" and "USB debugging (Security settings)"
- May need to add account in Developer Options

**Huawei Devices:**
- Install HiSuite for drivers
- Enable "Verify apps over USB"

## 📱 App Features

### Home Screen
- Stock search with autocomplete
- Popular stocks quick access
- Real-time market data display

### Stock Analysis
- Comprehensive stock information
- Price charts and technical indicators
- AI-powered price predictions

### Prediction Models
- **Basic Prediction**: Random Forest model
- **Advanced Prediction**: Ensemble AI models with confidence scoring

### Multi-Currency Support
- Automatic currency detection
- Localized formatting for global markets
- Support for 12+ major currencies

## 🏗️ Project Structure

```
stoky_mobile/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── models/                   # Data models
│   │   ├── stock_info.dart       # Stock information model
│   │   ├── historical_data.dart  # Historical data model
│   │   └── prediction.dart       # Prediction models
│   ├── screens/                  # App screens
│   │   └── home_screen.dart      # Main home screen
│   ├── widgets/                  # Reusable UI components
│   │   ├── stock_card.dart       # Stock information card
│   │   ├── prediction_card.dart  # Prediction display card
│   │   ├── loading_indicator.dart # Loading animations
│   │   └── error_dialog.dart     # Error handling UI
│   ├── services/                 # API and business logic
│   │   └── api_service.dart      # Backend API communication
│   └── utils/                    # Utilities
│       ├── constants.dart        # App constants
│       ├── theme.dart           # App theming
│       └── currency_formatter.dart # Currency formatting
├── android/                      # Android-specific files
├── pubspec.yaml                  # Dependencies
└── README.md                     # This file
```

## 🎨 Customization

### Changing Colors:
Edit `lib/utils/theme.dart` to customize the app's appearance.

### Adding Features:
The app is designed to be modular. Add new screens in `lib/screens/` and new widgets in `lib/widgets/`.

### API Integration:
All API calls are handled in `lib/services/api_service.dart`. Modify this file to add new endpoints.

## 📊 Performance

### Optimization Tips:
- The app is optimized for smooth performance
- Uses efficient state management
- Implements proper error handling and loading states
- Optimized for both debug and release builds

### Memory Usage:
- Minimal memory footprint
- Efficient image and data caching
- Proper disposal of resources

## 🔒 Security

- Secure HTTP connections (ensure backend uses HTTPS in production)
- No sensitive data stored locally
- Proper input validation

## 📈 Analytics & Monitoring

The app includes comprehensive error handling and can be extended with:
- Crash reporting (Firebase Crashlytics)
- Analytics (Firebase Analytics)
- Performance monitoring

## 🤝 Support

If you encounter issues:

1. Check this README for common solutions
2. Run `flutter doctor` to verify setup
3. Check backend connectivity
4. Verify device compatibility

## 🚀 Deployment

### Testing:
```bash
flutter test
```

### Building Release APK:
```bash
flutter build apk --release
```

### Building App Bundle (for Play Store):
```bash
flutter build appbundle --release
```

## 📝 Notes

- Minimum Android version: 5.0 (API Level 21)
- Target Android version: 14 (API Level 34)
- Supports both light and dark themes
- Responsive design for various screen sizes
- Optimized for both phones and tablets

---

**STOKY Mobile** - Your AI-powered stock advisor in your pocket! 📱💹
