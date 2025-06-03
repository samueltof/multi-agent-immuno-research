 #!/bin/bash

# LangManus Frontend Launcher
echo "🤖 Starting LangManus Frontend..."

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if API server is running
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "✅ API server is running"
else
    echo "⚠️  Warning: API server may not be running on http://localhost:8000"
    echo "   Make sure to start your LangManus API server first"
fi

# Launch Streamlit with optimized settings
echo "🚀 Launching frontend..."
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --theme.base "light" \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f8f9fa"