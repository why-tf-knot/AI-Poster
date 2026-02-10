import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';

const {width} = Dimensions.get('window');

const HomeScreen = ({navigation}) => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.heroSection}>
        <Text style={styles.heroTitle}>REDEFINING ARTIFICIAL INTELLIGENCE</Text>
        <Text style={styles.heroSubtitle}>
          Next-generation AI poster creation for the future
        </Text>
        <TouchableOpacity
          style={styles.ctaButton}
          onPress={() => navigation.navigate('Features')}>
          <Text style={styles.ctaButtonText}>EXPLORE NOW</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.contentSection}>
        <Text style={styles.sectionTitle}>EXOPLANET ATMOSPHERIC ANALYSIS</Text>
        <Text style={styles.sectionText}>
          Harness the power of machine learning to decode atmospheric
          compositions of exoplanets, pushing the boundaries of space
          exploration and astrobiology.
        </Text>
      </View>

      <View style={styles.featuresGrid}>
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🤖</Text>
          <Text style={styles.featureTitle}>AI Models</Text>
          <Text style={styles.featureText}>
            Advanced deep learning with CNNs and transformer-based analysis
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🔬</Text>
          <Text style={styles.featureTitle}>Spectroscopy</Text>
          <Text style={styles.featureText}>
            High-precision transit photometry and spectral data processing
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🧪</Text>
          <Text style={styles.featureTitle}>Molecules</Text>
          <Text style={styles.featureText}>
            Comprehensive library of 500+ atmospheric compounds
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🌍</Text>
          <Text style={styles.featureTitle}>Discovery</Text>
          <Text style={styles.featureText}>
            Identify Earth-like worlds and search for biosignatures
          </Text>
        </View>
      </View>

      <View style={styles.statsSection}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>94.3%</Text>
          <Text style={styles.statLabel}>Water Detection</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>91.7%</Text>
          <Text style={styles.statLabel}>CO₂ Accuracy</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>500+</Text>
          <Text style={styles.statLabel}>Molecules</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>24/7</Text>
          <Text style={styles.statLabel}>Analysis</Text>
        </View>
      </View>

      <View style={styles.navigationSection}>
        <TouchableOpacity
          style={styles.navButton}
          onPress={() => navigation.navigate('Features')}>
          <Text style={styles.navButtonText}>VIEW FEATURES →</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.navButton}
          onPress={() => navigation.navigate('About')}>
          <Text style={styles.navButtonText}>LEARN MORE →</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>AI-POSTER © 2025</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  heroSection: {
    padding: 40,
    paddingTop: 60,
    paddingBottom: 80,
    alignItems: 'center',
    backgroundColor: '#0a0a0a',
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: '900',
    color: '#ffffff',
    textAlign: 'center',
    letterSpacing: 2,
    marginBottom: 20,
  },
  heroSubtitle: {
    fontSize: 16,
    color: '#ffffff',
    textAlign: 'center',
    opacity: 0.8,
    marginBottom: 30,
    letterSpacing: 1,
  },
  ctaButton: {
    backgroundColor: '#ffffff',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 0,
    borderWidth: 2,
    borderColor: '#ffffff',
  },
  ctaButtonText: {
    color: '#000000',
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 2,
  },
  contentSection: {
    padding: 30,
    backgroundColor: '#1a1a1a',
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 20,
    letterSpacing: 1,
  },
  sectionText: {
    fontSize: 15,
    color: '#ffffff',
    lineHeight: 24,
    opacity: 0.85,
  },
  featuresGrid: {
    padding: 20,
    backgroundColor: '#000000',
  },
  featureCard: {
    backgroundColor: '#1a1a1a',
    padding: 25,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  featureIcon: {
    fontSize: 40,
    marginBottom: 10,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#ffffff',
    marginBottom: 10,
    letterSpacing: 1,
  },
  featureText: {
    fontSize: 14,
    color: '#ffffff',
    opacity: 0.7,
    lineHeight: 20,
  },
  statsSection: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 20,
    backgroundColor: '#0a0a0a',
  },
  statCard: {
    width: (width - 60) / 2,
    padding: 20,
    margin: 5,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 10,
    letterSpacing: 1,
  },
  statLabel: {
    fontSize: 12,
    color: '#ffffff',
    opacity: 0.7,
    textAlign: 'center',
    letterSpacing: 1,
  },
  navigationSection: {
    padding: 30,
    backgroundColor: '#1a1a1a',
  },
  navButton: {
    borderBottomWidth: 2,
    borderBottomColor: '#ffffff',
    paddingVertical: 15,
    marginBottom: 20,
  },
  navButtonText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#ffffff',
    letterSpacing: 1,
  },
  footer: {
    padding: 40,
    alignItems: 'center',
    backgroundColor: '#000000',
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.1)',
  },
  footerText: {
    fontSize: 12,
    color: '#ffffff',
    opacity: 0.5,
    letterSpacing: 1,
  },
});

export default HomeScreen;
