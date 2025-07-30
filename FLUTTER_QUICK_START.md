# 🚀 STOKY Mobile Quick Start

Get STOKY running on your Android device in 5 simple steps!

## Step 1: Install Flutter (5 minutes)

### Windows:
```cmd
# Option 1: Download and extract
1. Download Flutter from: https://docs.flutter.dev/get-started/install/windows
2. Extract to C:\flutter
3. Add C:\flutter\bin to your system PATH
4. Restart command prompt

# Option 2: Using Git (if you have it)
git clone https://github.com/flutter/flutter.git -b stable C:\flutter
set PATH=%PATH%;C:\flutter\bin
```

### macOS:
```bash
# Using Homebrew (recommended)
brew install flutter

# Or manual download
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_3.16.0-stable.zip
unzip flutter_macos_*.zip
export PATH="$PATH:`pwd`/flutter/bin"
```

### Linux:
```bash
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.0-stable.tar.xz
tar xf flutter_linux_*.tar.xz
export PATH="$PATH:`pwd`/flutter/bin"
```

## Step 2: Install Android Studio (10 minutes)

1. **Download**: https://developer.android.com/studio
2. **Install** with default settings
3. **Open** Android Studio
4. **Install** Android SDK when prompted
5. **Create** a virtual device (AVD) OR connect your Android phone

### For Physical Device:
- Enable Developer Options: Settings → About Phone → Tap "Build Number" 7 times
- Enable USB Debugging: Settings → Developer Options → USB Debugging

## Step 3: Verify Setup (2 minutes)

```bash
flutter doctor
```

This will show you what's working and what needs fixing. Address any red ❌ items.

## Step 4: Get STOKY Mobile (2 minutes)

```bash
# Navigate to STOKY project
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY\stoky_mobile"

# Install dependencies
flutter pub get

# Check devices
flutter devices
```

## Step 5: Configure and Run (3 minutes)

### A. Update Backend URL
Edit `lib/utils/constants.dart`:
```dart
// Find your computer's IP address:
// Windows: ipconfig
// Mac/Linux: ifconfig

static const String baseUrl = 'http://YOUR_IP_HERE:8000';
// Example: 'http://192.168.1.100:8000'
```

### B. Start Backend
```bash
# In main STOKY folder
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
python app.py
```

### C. Run Mobile App
```bash
# In stoky_mobile folder
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY\stoky_mobile"
flutter run
```

## 🎉 That's It!

Your STOKY app should now be running on your Android device!

## 📱 Quick Test

1. **Search** for a stock (try: AAPL, GOOGL, PETR4.SA)
2. **View** real-time price and AI prediction
3. **Switch** between basic and advanced AI models
4. **Check** multi-currency support with international stocks

## 🆘 Quick Fixes

**"No devices found":**
```bash
# Check USB connection and enable USB debugging
adb devices
```

**"Connection refused":**
- Check backend is running: `python app.py`
- Verify IP address in constants.dart
- Ensure phone and computer on same WiFi

**"Flutter command not found":**
- Restart terminal/command prompt
- Check PATH includes Flutter bin directory

**Gradle build fails:**
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

## 🔥 Pro Tips

- Use `flutter run --hot-reload` for faster development
- Install Flutter extension in VS Code for better experience
- Keep Android Studio open for device management
- Use `flutter doctor --verbose` for detailed diagnostics

---

**Enjoy your AI-powered stock advisor! 📱💹**

Need help? Check the full README.md for detailed troubleshooting.
