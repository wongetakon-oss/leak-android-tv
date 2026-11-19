@echo off
echo ========================================================
echo   Menjalankan Server Backend LK21 Netflix TV (FastAPI)
echo ========================================================
echo.
echo 1. Menginstall dependensi...
pip install -r requirements.txt
echo.
echo 2. Memulai server di http://0.0.0.0:8000 ...
echo (Pastikan Android TV dan Komputer berada dalam 1 jaringan Wi-Fi)
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
