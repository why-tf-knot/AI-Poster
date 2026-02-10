import React from 'react';
import {StyleSheet, Text, View, ScrollView} from 'react-native';

const FeaturesScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.mainTitle}>🌌 KEY FEATURES</Text>
        <Text style={styles.subtitle}>
          Unveiling the Secrets of Distant Worlds Through AI
        </Text>
      </View>

      <View style={styles.featureBlock}>
        <Text style={styles.featureIcon}>🤖</Text>
        <Text style={styles.featureTitle}>ADVANCED AI MODELS</Text>
        <Text style={styles.featureDescription}>
          • Convolutional Neural Networks{'\n'}
          • Transformer-based spectral analysis{'\n'}
          • Ensemble methods for maximum accuracy{'\n'}
          • Real-time atmospheric composition prediction
        </Text>
      </View>

      <View style={styles.featureBlock}>
        <Text style={styles.featureIcon}>🔬</Text>
        <Text style={styles.featureTitle}>SPECTROSCOPY ANALYSIS</Text>
        <Text style={styles.featureDescription}>
          • Transit photometry processing{'\n'}
          • Emission & absorption spectra analysis{'\n'}
          • Multi-wavelength correlation{'\n'}
          • High-precision data normalization
        </Text>
      </View>

      <View style={styles.featureBlock}>
        <Text style={styles.featureIcon}>🧪</Text>
        <Text style={styles.featureTitle}>MOLECULAR DATABASE</Text>
        <Text style={styles.featureDescription}>
          • 500+ atmospheric compounds library{'\n'}
          • Biosignature indicators database{'\n'}
          • Reference compound spectra{'\n'}
          • Interactive molecular structures
        </Text>
      </View>

      <View style={styles.featureBlock}>
        <Text style={styles.featureIcon}>📊</Text>
        <Text style={styles.featureTitle}>DATA VISUALIZATION</Text>
        <Text style={styles.featureDescription}>
          • Interactive spectrum plots{'\n'}
          • Planetary analysis dashboards{'\n'}
          • 3D molecular structure viewer{'\n'}
          • Real-time data processing insights
        </Text>
      </View>

      <View style={styles.accuracySection}>
        <Text style={styles.accuracyTitle}>MODEL ACCURACY</Text>
        
        <View style={styles.accuracyRow}>
          <Text style={styles.moleculeName}>💧 Water (H₂O)</Text>
          <Text style={styles.accuracyValue}>94.3%</Text>
        </View>

        <View style={styles.accuracyRow}>
          <Text style={styles.moleculeName}>🌫️ CO₂</Text>
          <Text style={styles.accuracyValue}>91.7%</Text>
        </View>

        <View style={styles.accuracyRow}>
          <Text style={styles.moleculeName}>🔥 Methane</Text>
          <Text style={styles.accuracyValue}>88.5%</Text>
        </View>

        <View style={styles.accuracyRow}>
          <Text style={styles.moleculeName}>💨 Oxygen</Text>
          <Text style={styles.accuracyValue}>85.2%</Text>
        </View>

        <View style={styles.accuracyRow}>
          <Text style={styles.moleculeName}>🧬 Phosphine</Text>
          <Text style={styles.accuracyValue}>76.8%</Text>
        </View>
      </View>

      <View style={styles.applicationsSection}>
        <Text style={styles.applicationsTitle}>SPACE APPLICATIONS</Text>
        
        <View style={styles.applicationCard}>
          <Text style={styles.appEmoji}>🪐</Text>
          <Text style={styles.appTitle}>Exoplanet Characterization</Text>
          <Text style={styles.appStatus}>✅ Active</Text>
        </View>

        <View style={styles.applicationCard}>
          <Text style={styles.appEmoji}>🔬</Text>
          <Text style={styles.appTitle}>Biosignature Detection</Text>
          <Text style={styles.appStatus}>🚧 In Development</Text>
        </View>

        <View style={styles.applicationCard}>
          <Text style={styles.appEmoji}>🌡️</Text>
          <Text style={styles.appTitle}>Climate Modeling</Text>
          <Text style={styles.appStatus}>📋 Planned</Text>
        </View>

        <View style={styles.applicationCard}>
          <Text style={styles.appEmoji}>🚀</Text>
          <Text style={styles.appTitle}>Mission Planning</Text>
          <Text style={styles.appStatus}>✅ Active</Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  section: {
    padding: 30,
    backgroundColor: '#0a0a0a',
    alignItems: 'center',
  },
  mainTitle: {
    fontSize: 28,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 15,
    letterSpacing: 2,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: '#ffffff',
    opacity: 0.8,
    textAlign: 'center',
    letterSpacing: 1,
  },
  featureBlock: {
    padding: 30,
    backgroundColor: '#1a1a1a',
    marginBottom: 2,
  },
  featureIcon: {
    fontSize: 50,
    marginBottom: 15,
  },
  featureTitle: {
    fontSize: 20,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 15,
    letterSpacing: 1,
  },
  featureDescription: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 24,
    opacity: 0.85,
  },
  accuracySection: {
    padding: 30,
    backgroundColor: '#0a0a0a',
    marginTop: 20,
  },
  accuracyTitle: {
    fontSize: 22,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 25,
    letterSpacing: 1,
  },
  accuracyRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  moleculeName: {
    fontSize: 16,
    color: '#ffffff',
    fontWeight: '600',
  },
  accuracyValue: {
    fontSize: 18,
    color: '#ffffff',
    fontWeight: '900',
    letterSpacing: 1,
  },
  applicationsSection: {
    padding: 30,
    backgroundColor: '#000000',
    marginTop: 20,
  },
  applicationsTitle: {
    fontSize: 22,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 25,
    letterSpacing: 1,
  },
  applicationCard: {
    backgroundColor: '#1a1a1a',
    padding: 20,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  appEmoji: {
    fontSize: 35,
    marginBottom: 10,
  },
  appTitle: {
    fontSize: 16,
    color: '#ffffff',
    fontWeight: '700',
    marginBottom: 8,
    letterSpacing: 1,
  },
  appStatus: {
    fontSize: 14,
    color: '#ffffff',
    opacity: 0.7,
  },
});

export default FeaturesScreen;
