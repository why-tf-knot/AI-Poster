# 🚀 Getting Started with AI-Poster

Welcome to AI-Poster! This guide will help you set up and run the application in minutes.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14.0.0 or higher) - [Download here](https://nodejs.org/)
  - Check your version: `node --version`
- **npm** (comes with Node.js)
  - Check your version: `npm --version`

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies

```bash
npm install
```

This will install all required packages, including:
- Express.js (web server framework)

### 2️⃣ (Optional) Configure Environment

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Default configuration:
- **Port**: 3000
- **Host**: 0.0.0.0 (accessible from all network interfaces)

You can customize these values by editing the `.env` file.

### 3️⃣ Start the Server

```bash
npm start
```

Or for development mode:

```bash
npm run dev
```

## 🌐 Accessing the Application

Once the server is running, you'll see:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║          🌌 AI-POSTER SERVER RUNNING 🚀              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

  🌐 Server:     http://localhost:3000
  📁 Serving:    /path/to/public
  🔧 Node:       v18.x.x
```

Open your browser and navigate to:
- **Local**: http://localhost:3000
- **Network**: http://[your-ip]:3000

## 🛠️ Troubleshooting

### Port Already in Use

If port 3000 is already in use, you can:

1. Stop the other application using that port, or
2. Use a different port by setting it in your `.env` file:
   ```
   PORT=8080
   ```

### Cannot Find Module

If you see "Cannot find module" errors:

```bash
# Remove existing node_modules
rm -rf node_modules

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install
```

### Permission Errors

On Linux/Mac, if you encounter permission errors:

```bash
# Use sudo (not recommended for production)
sudo npm install

# Or fix npm permissions (recommended)
# Follow: https://docs.npmjs.com/resolving-eacces-permissions-errors
```

## 📁 Project Structure

```
AI-Poster/
├── public/           # Static files (HTML, CSS, images)
│   ├── index.html   # Main landing page
│   └── style.css    # Styling
├── server.js        # Express server
├── package.json     # Dependencies and scripts
├── .env.example     # Environment configuration template
├── .gitignore       # Git ignore rules
└── START_HERE.md    # This file
```

## 🔄 Development Workflow

1. **Make Changes**: Edit files in the `public/` directory
2. **Refresh Browser**: Changes to HTML/CSS take effect immediately
3. **Server Changes**: Restart the server if you modify `server.js`

## 📚 Next Steps

- **Customize the Landing Page**: Edit `public/index.html` and `public/style.css`
- **Add Features**: Extend the functionality in `server.js`
- **Read Documentation**: Check out the main [README.md](README.md) for project details
- **Contribute**: See contributing guidelines in the README

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/why-tf-knot/AI-Poster/issues)
- **Documentation**: [README.md](README.md)
- **Community**: [Discussions](https://github.com/why-tf-knot/AI-Poster/discussions)

---

**Happy Coding! 🌌✨**
