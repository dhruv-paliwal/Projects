@echo off
title LPG Distribution & Consumer Management System Launcher
echo =======================================================================
echo  SHREE GANESH LPG AGENCY - DISTRIBUTION & OPERATIONS MANAGEMENT
echo  Kanpur & Hamirpur Territory Command Center (Code: UP-KNP-78401)
echo =======================================================================
echo.
echo Starting Django Backend & AngularJS Single-Page Application on Port 8000...
start "Django Backend Server (Port 8000)" cmd /k "cd /d %~dp0backend && python manage.py runserver 127.0.0.1:8000"

timeout /t 2 >nul

echo Starting Streamlit Operational Deployment Interface on Port 8501...
start "Streamlit Operations Hub (Port 8501)" cmd /k "cd /d %~dp0 && python -m streamlit run streamlit_app.py --server.port 8501"

echo.
echo =======================================================================
echo  SERVERS ACTIVE:
echo   - AngularJS SPA Frontend:  http://127.0.0.1:8000/
echo   - Streamlit Operations Hub: http://127.0.0.1:8501/
echo   - Django Admin Registry:   http://127.0.0.1:8000/admin/
echo =======================================================================
echo.
pause
