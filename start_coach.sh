#!/bin/bash
echo "🤖 AI-Coachen Setup och Start"
echo "==============================="

# Kontrollera om virtual environment finns
if [ ! -f "venv/bin/activate" ]; then
    echo "Skapar virtual environment..."
    python3 -m venv venv
fi

# Aktivera virtual environment
echo "Aktiverar virtual environment..."
source venv/bin/activate

# Installera dependencies
echo "Installerar dependencies..."
pip install -r requirements.txt

# Kontrollera om .env finns
if [ ! -f ".env" ]; then
    echo "Kopierar .env exempel..."
    cp .env.example .env
    echo ""
    echo "⚠️  VIKTIGT: Redigera .env filen och lägg till dina API-nycklar!"
    echo "   Öppna .env i en texteditor och lägg till din OpenAI API-nyckel."
    echo ""
    read -p "Tryck Enter för att fortsätta..."
fi

# Kör tester (valfritt)
echo ""
read -p "Vill du köra tester först? (y/n): " run_tests
if [[ $run_tests == "y" ]] || [[ $run_tests == "Y" ]]; then
    echo "Kör tester..."
    python test_ai_coach.py
    echo ""
    read -p "Tryck Enter för att fortsätta..."
fi

# Starta Streamlit app
echo "Startar AI-Coachen..."
echo "Öppnar webbläsaren på http://localhost:8501"
echo ""
echo "Tryck Ctrl+C för att stoppa applikationen"
streamlit run main.py