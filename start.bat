@echo off
REM Short Report Rebuttal Assistant - Start Script for Windows (OpenAI)

echo 🚀 Starting Short Report Rebuttal Assistant with OpenAI...
echo.

REM Check if .env exists in backend, create from .env.example if not
if not exist "backend\.env" (
    if exist "backend\.env.example" (
        echo ⚠️  backend\.env file not found. Creating from .env.example...
        copy "backend\.env.example" "backend\.env" >nul
        echo ✅ Created backend\.env file. Please edit it and add your OPENAI_API_KEY.
        echo.
        echo Opening backend\.env in notepad for editing...
        timeout /t 2 /nobreak >nul
        notepad "backend\.env"
        echo.
        echo Please save the file and close Notepad, then press any key to continue...
        pause
    ) else (
        echo ❌ backend\.env.example file not found!
        echo Please create backend\.env file manually.
        pause
        exit /b 1
    )
)

REM Check if OpenAI API key is set (not the example value)
findstr /C:"OPENAI_API_KEY" backend\.env | findstr /V /C:"sk-your-key-here" >nul
if errorlevel 1 (
    echo ❌ OPENAI_API_KEY is not set or still using example value in backend\.env
    echo Please edit backend\.env and replace 'sk-your-key-here' with your actual OpenAI API key
    echo.
    echo Opening backend\.env in notepad...
    timeout /t 2 /nobreak >nul
    notepad "backend\.env"
    echo.
    echo Please save the file and close Notepad, then press any key to continue...
    pause
    REM Check again after editing
    findstr /C:"OPENAI_API_KEY" backend\.env | findstr /V /C:"sk-your-key-here" >nul
    if errorlevel 1 (
        echo ❌ OPENAI_API_KEY still not configured correctly. Exiting.
        pause
        exit /b 1
    )
)

echo ✅ OpenAI configuration found
echo.

REM Start backend server
echo 📡 Starting backend server...
start "Backend Server" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo.
    echo 📦 Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

REM Start frontend server
echo.
echo 🎨 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

REM Wait for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎉 All services are running!
echo.
echo 📍 Access points:
echo    • Frontend:     http://localhost:3000
echo    • Backend API:  http://localhost:8000
echo    • API Docs:     http://localhost:8000/docs
echo.
echo Press any key to exit (services will continue running)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Open browser
start http://localhost:3000

pause
