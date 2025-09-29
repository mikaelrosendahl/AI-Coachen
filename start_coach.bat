@echo off
echo 🤖 AI-Coachen Setup och Start
echo ===============================

REM Kontrollera om virtual environment finns
if not exist "venv\Scripts\activate.bat" (
    echo Skapar virtual environment...
    python -m venv venv
)

REM Aktivera virtual environment
echo Aktiverar virtual environment...
call venv\Scripts\activate.bat

REM Installera dependencies
echo Installerar dependencies...
pip install -r requirements.txt

REM Kontrollera om .env finns
if not exist ".env" (
    echo Kopierar .env exempel...
    copy .env.example .env
    echo.
    echo ⚠️  VIKTIGT: Redigera .env filen och lägg till dina API-nycklar!
    echo    Öppna .env i en texteditor och lägg till din OpenAI API-nyckel.
    echo.
    pause
)

REM Kör tester (valfritt)
echo.
set /p run_tests="Vill du köra tester först? (y/n): "
if /i "%run_tests%"=="y" (
    echo Kör tester...
    python test_ai_coach.py
    echo.
    pause
)

REM Starta Streamlit app
echo Startar AI-Coachen...
echo Öppnar webbläsaren på http://localhost:8501
echo.
echo Tryck Ctrl+C för att stoppa applikationen
streamlit run main.py

pause