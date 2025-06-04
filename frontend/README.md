# LangManus Frontend

A modern, aesthetic Streamlit interface for the LangManus multiagent system.

## Features

🎨 **Modern UI Design**
- Clean, gradient-based design with smooth animations
- Responsive layout that works on different screen sizes
- Professional color scheme and typography

🤖 **Full Multiagent Integration**
- Real-time streaming responses from the LangManus API
- Support for all configuration options (debug, deep thinking, search before planning)
- Live event logging and system status monitoring

💬 **Enhanced Chat Experience**
- Beautiful message bubbles with role-based styling
- Conversation history management
- Export chat functionality
- Quick example queries

⚙️ **Configuration & Monitoring**
- Real-time server status checking
- Configurable API endpoint
- Performance metrics display
- Event log viewer

## 🎨 Custom Theme Configuration

The Streamlit app now uses a custom theme configuration that's automatically loaded from `.streamlit/config.toml`.

### Theme Settings
- **Base**: Light theme
- **Primary Color**: `#667eea` (Modern blue)
- **Background**: `#ffffff` (Pure white)
- **Secondary Background**: `#f8f9fa` (Light gray)
- **Text Color**: `#262730` (Dark gray)

### Server Settings
- **Port**: 8501
- **Address**: 0.0.0.0 (accessible from network)
- **Browser stats**: Disabled for privacy

## 🚀 Running the App

### Method 1: Using the Run Script (Recommended)
```bash
# From the project root directory
./run_app.sh
```

### Method 2: Manual Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the app
cd frontend && streamlit run app.py
```

### Method 3: With Custom Parameters (Override defaults)
```bash
source .venv/bin/activate
cd frontend
streamlit run app.py --server.port 8502 --theme.primaryColor "#ff6b6b"
```

## 📁 Configuration Files

### `.streamlit/config.toml`
Contains all default settings for the Streamlit app:
- Server configuration
- Theme settings  
- Browser options
- Logger settings
- Runner options

## 🔧 Execution Modes

The app supports three execution modes:

1. **Auto** - Automatically chooses best available mode
2. **API Only** - Forces API server execution
3. **Direct Only** - Forces local workflow execution

### Requirements for Direct Mode
- Virtual environment must be activated
- All dependencies must be installed in `.venv`
- Must be run from project root or with proper path setup

## 🌐 Access URLs

When running with default configuration:
- **Local**: http://localhost:8501
- **Network**: http://[your-ip]:8501

## 📝 Notes

- The configuration file automatically loads when Streamlit starts
- No need to specify theme parameters on command line anymore
- Virtual environment activation is required for Direct Mode to work
- Configuration can be overridden with command line parameters if needed

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```