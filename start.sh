#!/bin/bash

# Render startup script för AI-Coachen
echo "🚀 Startar AI-Coachen på Render..."

# Kontrollera att Python är installerat
python --version

# Kontrollera att dependencies är installerade
echo "📦 Kontrollerar dependencies..."
pip list | grep streamlit
pip list | grep openai

# Skapa nödvändiga mappar
mkdir -p data
mkdir -p logs

# Sätt Streamlit konfiguration för produktion
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Starta applikationen
echo "🎯 Startar Streamlit applikationen..."
streamlit run main.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.fileWatcherType=none