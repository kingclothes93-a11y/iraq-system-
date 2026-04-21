# Android Build Configuration for Iraq System

# Build options
requirecython = True

# Proper Gradle setup
# Include necessary Gradle dependencies
apply plugin: 'com.android.application'

android {
    compileSdkVersion 30
    defaultConfig {
        applicationId "com.example.iraqsystem"
        minSdkVersion 21
        targetSdkVersion 30
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

# NDK configuration
ndk_version = 21.0.6113669

# Additional settings for stable Android builds
// Add other required configurations here if necessary
// e.g., signing configs or build flavors
