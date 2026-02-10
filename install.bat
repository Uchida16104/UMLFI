@echo off
echo [UMLFI] Starting Complete Installation...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python is not installed. Please install Python 3.9+ from python.org
    exit /b
)

:: Setup Virtual Env
python -m venv venv
call venv\Scripts\activate

:: Install Backend & Analysis Dependencies
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pandas scikit-learn numpy requests

:: Check for Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Node.js is not installed.
    exit /b
)

:: Setup Frontend
cd frontend
call npm install
cd ..

echo [Success] Infrastructure is ready. Run 'start_all.bat' to begin.