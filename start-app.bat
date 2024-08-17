@echo off
echo Starting Skill Tier Classifier Application...

:: Start the backend (Flask server)
cd backend
start /min cmd /c "python app.py"

:: Wait for a moment to ensure the server has started
timeout /t 1 > nul

:: Start the frontend (npm server) silently
cd ..\frontend
start /min cmd /c "npm start > nul 2>&1"

:: Wait for the frontend to start
timeout /t 1 > nul

:: Open the frontend in the default web browser
start http://localhost:2139
:: Close the frontend window
exit