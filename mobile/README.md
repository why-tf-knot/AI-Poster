# AI-Poster Mobile Application

🚀 **Cross-platform mobile application for AI-Poster: Exoplanet Atmospheric Analysis**

Available for both **Android** and **iOS** platforms.

---

## 📱 Overview

The AI-Poster mobile app brings the power of exoplanet atmospheric analysis to your smartphone. Built with React Native, this cross-platform application provides:

- 🌌 Interactive exploration of AI-powered exoplanet analysis
- 🔬 Access to spectroscopy and molecular detection features
- 📊 Real-time data visualization
- 🤖 Advanced AI model insights
- 🌍 Biosignature detection information

---

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:

### General Requirements
- **Node.js** >= 18
- **npm** or **yarn**
- **React Native CLI**: `npm install -g react-native-cli`

### For Android Development
- **Android Studio** with Android SDK
- **Java Development Kit (JDK)** 11 or newer
- **Android SDK Platform 34**
- **Android Build Tools**
- Environment variables:
  - `ANDROID_HOME` pointing to your Android SDK location
  - Add `$ANDROID_HOME/platform-tools` to your PATH

### For iOS Development (macOS only)
- **Xcode** 14 or newer
- **CocoaPods**: `sudo gem install cocoapods`
- **iOS Simulator** or a physical iOS device

---

## 🚀 Installation

### 1. Navigate to the mobile directory

```bash
cd mobile
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. iOS-specific setup (macOS only)

```bash
cd ios
pod install
cd ..
```

---

## 📲 Running the Application

### Android

1. **Start Metro bundler** (in one terminal):
   ```bash
   npm start
   ```

2. **Run on Android** (in another terminal):
   ```bash
   npm run android
   ```

   Or manually:
   ```bash
   react-native run-android
   ```

**Note:** Make sure you have an Android emulator running or a physical device connected via USB with USB debugging enabled.

### iOS (macOS only)

1. **Start Metro bundler** (in one terminal):
   ```bash
   npm start
   ```

2. **Run on iOS** (in another terminal):
   ```bash
   npm run ios
   ```

   Or manually:
   ```bash
   react-native run-ios
   ```

   To run on a specific simulator:
   ```bash
   react-native run-ios --simulator="iPhone 15"
   ```

---

## 🏗 Project Structure

```
mobile/
├── android/                 # Android-specific files
│   ├── app/
│   │   ├── build.gradle    # Android build configuration
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── res/        # Android resources
│   ├── build.gradle        # Root build configuration
│   └── settings.gradle     # Project settings
│
├── ios/                    # iOS-specific files
│   ├── Podfile            # CocoaPods dependencies
│   └── Info.plist         # iOS app configuration
│
├── src/                   # React Native source code
│   ├── App.js            # Main app component with navigation
│   ├── screens/          # App screens
│   │   ├── HomeScreen.js      # Home/landing screen
│   │   ├── FeaturesScreen.js  # Features showcase
│   │   └── AboutScreen.js     # About and project info
│   ├── components/       # Reusable components (future)
│   └── navigation/       # Navigation configuration (future)
│
├── package.json          # Dependencies and scripts
├── index.js             # App entry point
├── babel.config.js      # Babel configuration
└── README.md           # This file
```

---

## 🎨 Features

### Home Screen
- Hero section with app branding
- Overview of AI-powered exoplanet analysis
- Feature cards showcasing capabilities
- Performance statistics
- Quick navigation to other screens

### Features Screen
- Detailed feature descriptions
- AI model information
- Spectroscopy analysis details
- Molecular database overview
- Model accuracy metrics
- Space applications showcase

### About Screen
- Project mission and goals
- Team information
- Contributing guidelines
- Resource links
- External documentation
- License information

---

## 🔧 Configuration

### App Name and Package ID

#### Android
Edit `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">AI-Poster</string>
```

Edit `android/app/build.gradle` to change package ID:
```gradle
defaultConfig {
    applicationId "com.aiposter"
    ...
}
```

#### iOS
Edit `ios/Info.plist`:
```xml
<key>CFBundleDisplayName</key>
<string>AI-Poster</string>
```

### App Icons

#### Android
Replace icons in `android/app/src/main/res/mipmap-*` directories

#### iOS
Replace icons in `ios/AIposter/Images.xcassets/AppIcon.appiconset/`

---

## 🧪 Testing

Run tests with:
```bash
npm test
```

---

## 🐛 Troubleshooting

### Android Issues

**Build fails with "SDK location not found":**
- Create `android/local.properties` with:
  ```
  sdk.dir=/path/to/your/Android/sdk
  ```

**App doesn't connect to Metro:**
- Run `adb reverse tcp:8081 tcp:8081`

**Clean build:**
```bash
cd android
./gradlew clean
cd ..
```

### iOS Issues

**Pod install fails:**
```bash
cd ios
pod install --repo-update
cd ..
```

**Build fails:**
- Clean Xcode build: `xcodebuild clean` in the ios directory
- Reset simulator: Device → Erase All Content and Settings

**Metro bundler issues:**
```bash
npm start -- --reset-cache
```

---

## 📦 Building for Production

### Android APK

```bash
cd android
./gradlew assembleRelease
```

APK will be at: `android/app/build/outputs/apk/release/app-release.apk`

### Android Bundle (for Google Play)

```bash
cd android
./gradlew bundleRelease
```

AAB will be at: `android/app/build/outputs/bundle/release/app-release.aab`

### iOS (requires Apple Developer Account)

1. Open `ios/AIposter.xcworkspace` in Xcode
2. Select your team in Signing & Capabilities
3. Select Product → Archive
4. Follow the distribution workflow

---

## 🤝 Contributing

We welcome contributions! Areas where you can help:

- 🎨 UI/UX improvements
- 📱 New features and screens
- 🐛 Bug fixes
- 📚 Documentation
- 🧪 Test coverage
- 🌐 Internationalization

Please follow these steps:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🔗 Links

- 📖 [Main Project Repository](https://github.com/why-tf-knot/AI-Poster)
- 🌐 [React Native Documentation](https://reactnative.dev/)
- 📱 [Android Developer Guide](https://developer.android.com/)
- 🍎 [iOS Developer Guide](https://developer.apple.com/ios/)

---

## 💡 Notes

- This app requires internet connectivity to access external resources
- For the best experience, use devices running Android 6.0+ or iOS 13.4+
- The app is optimized for both portrait and landscape orientations

---

## 🌟 Future Enhancements

- [ ] Real-time spectral data visualization
- [ ] Interactive 3D molecular viewer
- [ ] Offline data caching
- [ ] Push notifications for new discoveries
- [ ] User authentication and profiles
- [ ] Social sharing features
- [ ] Dark/light theme toggle
- [ ] Augmented reality features

---

<div align="center">

**🌌 "We are made of star stuff. We are a way for the cosmos to know itself." - Carl Sagan 🌌**

⭐ Star the repository if this helped your cosmic journey! ⭐

</div>
