const express = require('express');
const rateLimit = require('express-rate-limit');
const path = require('path');

const app = express();

// Get port from environment variable or use default
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || 'localhost';

// Rate limiting to prevent abuse
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  message: 'Too many requests from this IP, please try again later.'
});

// Apply rate limiting to all requests
app.use(limiter);

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Handle root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Handle 404 - keep this last
app.use((req, res) => {
  res.status(404).send('404 - Page Not Found');
});

// Start the server
app.listen(PORT, HOST, () => {
  console.log('');
  console.log('╔══════════════════════════════════════════════════════╗');
  console.log('║                                                      ║');
  console.log('║          🌌 AI-POSTER SERVER RUNNING 🚀              ║');
  console.log('║                                                      ║');
  console.log('╚══════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  🌐 Server:     http://localhost:${PORT}`);
  console.log(`  📁 Serving:    ${path.join(__dirname, 'public')}`);
  console.log(`  🔧 Node:       ${process.version}`);
  console.log('');
  console.log('  Press Ctrl+C to stop the server');
  console.log('');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('\n🛑 SIGTERM signal received: closing HTTP server');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n🛑 SIGINT signal received: closing HTTP server');
  process.exit(0);
});
