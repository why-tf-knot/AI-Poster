import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  Linking,
  TouchableOpacity,
} from 'react-native';

const AboutScreen = () => {
  const openLink = url => {
    Linking.openURL(url);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.heroSection}>
        <Text style={styles.heroTitle}>🌌 AI-POSTER</Text>
        <Text style={styles.heroSubtitle}>
          Exoplanet Atmospheric Analysis
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>MISSION</Text>
        <Text style={styles.sectionText}>
          Harness the power of machine learning to decode atmospheric
          compositions of exoplanets, pushing the boundaries of space
          exploration and astrobiology.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>WHAT WE DO</Text>
        <Text style={styles.bulletPoint}>
          🔭 <Text style={styles.boldText}>Spectral Analysis</Text> → AI models
          decode light signatures from distant atmospheres
        </Text>
        <Text style={styles.bulletPoint}>
          🧪 <Text style={styles.boldText}>Molecular Detection</Text> → Identify
          key compounds like H₂O, CO₂, CH₄, and biosignatures
        </Text>
        <Text style={styles.bulletPoint}>
          🌍 <Text style={styles.boldText}>Habitability Assessment</Text> →
          Predict planetary conditions for potential life
        </Text>
        <Text style={styles.bulletPoint}>
          📊 <Text style={styles.boldText}>Data Visualization</Text> → Transform
          complex astronomical data into intuitive insights
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>PROJECT STRUCTURE</Text>
        <Text style={styles.structureText}>
          🧠 <Text style={styles.boldText}>models/</Text> - AI model
          architectures{'\n'}
          📊 <Text style={styles.boldText}>data/</Text> - Astronomical datasets
          {'\n'}
          🔬 <Text style={styles.boldText}>analysis/</Text> - Core analysis
          modules{'\n'}
          🎨 <Text style={styles.boldText}>visualization/</Text> - Data
          visualization tools{'\n'}
          🚀 <Text style={styles.boldText}>apps/</Text> - Web applications
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>CONTRIBUTING</Text>
        <Text style={styles.sectionText}>
          Join our cosmic journey! We need help with:
        </Text>
        <Text style={styles.bulletPoint}>🔬 New spectroscopic models</Text>
        <Text style={styles.bulletPoint}>
          🎨 Data visualization improvements
        </Text>
        <Text style={styles.bulletPoint}>📱 Mobile app development</Text>
        <Text style={styles.bulletPoint}>📚 Documentation enhancement</Text>
        <Text style={styles.bulletPoint}>🧪 Molecular database expansion</Text>
      </View>

      <View style={styles.linksSection}>
        <Text style={styles.sectionTitle}>RESOURCES</Text>
        <TouchableOpacity
          onPress={() => openLink('https://github.com/why-tf-knot/AI-Poster')}>
          <Text style={styles.link}>📖 GitHub Repository →</Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() =>
            openLink('https://exoplanetarchive.ipac.caltech.edu/')
          }>
          <Text style={styles.link}>🏛️ NASA Exoplanet Archive →</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => openLink('https://www.jwst.nasa.gov/')}>
          <Text style={styles.link}>🔭 James Webb Space Telescope →</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.quoteSection}>
        <Text style={styles.quote}>
          "We are made of star stuff. We are a way for the cosmos to know
          itself."
        </Text>
        <Text style={styles.quoteAuthor}>- Carl Sagan</Text>
      </View>

      <View style={styles.licenseSection}>
        <Text style={styles.licenseTitle}>LICENSE</Text>
        <Text style={styles.licenseText}>MIT License</Text>
        <Text style={styles.copyrightText}>
          © 2025 Why-TF-Knot Team{'\n'}
          AI-Poster: Machine Learning for Exoplanet Atmospheric Analysis
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          ⭐ Star us on GitHub if this helped your cosmic journey! ⭐
        </Text>
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
    backgroundColor: '#0a0a0a',
    alignItems: 'center',
  },
  heroTitle: {
    fontSize: 36,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 10,
    letterSpacing: 2,
  },
  heroSubtitle: {
    fontSize: 16,
    color: '#ffffff',
    opacity: 0.8,
    letterSpacing: 1,
  },
  section: {
    padding: 30,
    backgroundColor: '#1a1a1a',
    marginBottom: 2,
  },
  sectionTitle: {
    fontSize: 22,
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
    marginBottom: 15,
  },
  bulletPoint: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 24,
    opacity: 0.85,
    marginBottom: 10,
  },
  boldText: {
    fontWeight: '700',
  },
  structureText: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 26,
    opacity: 0.85,
    fontFamily: 'monospace',
  },
  linksSection: {
    padding: 30,
    backgroundColor: '#000000',
  },
  link: {
    fontSize: 15,
    color: '#ffffff',
    marginBottom: 15,
    textDecorationLine: 'underline',
    fontWeight: '600',
  },
  quoteSection: {
    padding: 40,
    backgroundColor: '#0a0a0a',
    alignItems: 'center',
  },
  quote: {
    fontSize: 18,
    color: '#ffffff',
    fontStyle: 'italic',
    textAlign: 'center',
    lineHeight: 28,
    marginBottom: 15,
    opacity: 0.9,
  },
  quoteAuthor: {
    fontSize: 14,
    color: '#ffffff',
    opacity: 0.7,
    letterSpacing: 1,
  },
  licenseSection: {
    padding: 30,
    backgroundColor: '#1a1a1a',
    alignItems: 'center',
  },
  licenseTitle: {
    fontSize: 18,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 15,
    letterSpacing: 1,
  },
  licenseText: {
    fontSize: 16,
    color: '#ffffff',
    marginBottom: 20,
    fontWeight: '600',
  },
  copyrightText: {
    fontSize: 13,
    color: '#ffffff',
    opacity: 0.7,
    textAlign: 'center',
    lineHeight: 20,
  },
  footer: {
    padding: 40,
    backgroundColor: '#000000',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.1)',
  },
  footerText: {
    fontSize: 13,
    color: '#ffffff',
    opacity: 0.7,
    textAlign: 'center',
    letterSpacing: 1,
  },
});

export default AboutScreen;
