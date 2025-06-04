#!/bin/bash

# LangManus Streamlit App Runner
# This script activates the virtual environment and runs the Streamlit app

echo "🚀 Starting LangManus Streamlit App..."
echo "📁 Activating virtual environment..."

# Activate virtual environment
source .venv/bin/activate

# Check if activation was successful
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Change to frontend directory
cd frontend

echo "🌐 Starting Streamlit app with custom theme..."
echo "📋 Configuration loaded from .streamlit/config.toml"
echo ""

# Run Streamlit app (configuration will be loaded automatically from config.toml)
streamlit run app.py

echo "👋 Streamlit app stopped." 