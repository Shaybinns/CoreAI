@echo off
echo 🚀 Universal AI Core - Quick Start
echo ==================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.template .env
)

echo.
echo ✅ Setup complete!
echo.
echo To run the examples:
echo 1. CLI Demo:  python main.py
echo 2. API Server: python api.py
echo 3. Test Client: python test_client.py (in another terminal)
echo.
echo API Docs will be available at: http://localhost:8000/docs
