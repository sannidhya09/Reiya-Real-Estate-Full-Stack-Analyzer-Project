@echo off
echo ==================================
echo REI-AI Automated Setup
echo ==================================
echo.

:: Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
echo [OK] Python found

:: Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo ==================================
echo Setting up Backend
echo ==================================
echo.

cd backend

:: Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing Python dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo [OK] Backend dependencies installed

:: Create .env if it doesn't exist
if not exist .env (
    echo Creating backend .env file...
    copy .env.example .env
    echo [OK] Created backend\.env
)

:: Initialize database
echo Initializing database...
python scripts\init_db.py
echo [OK] Database initialized with sample data

cd ..

echo.
echo ==================================
echo Setting up Frontend
echo ==================================
echo.

cd frontend

:: Install dependencies
echo Installing Node.js dependencies...
call npm install
echo [OK] Frontend dependencies installed

:: Create .env.local if it doesn't exist
if not exist .env.local (
    echo Creating frontend .env.local file...
    copy .env.example .env.local
    echo [OK] Created frontend\.env.local
)

cd ..

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload --port 8000
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:3000
echo.
echo Note: The app works with sample data.
echo Add API keys in .env files for real data.
echo.
pause
