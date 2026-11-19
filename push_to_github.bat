@echo off
setlocal
echo ================================================================
echo    Push ke GitHub untuk Membangun APK Android TV Otomatis
echo ================================================================
echo.
echo 1. Buat repository baru di https://github.com/new
echo    (Beri nama misal: lk21-android-tv, biarkan Public atau Private)
echo.
echo 2. Salin URL repositori Anda.
echo    Contoh: https://github.com/username-anda/lk21-android-tv.git
echo.
set /p REPO_URL="Masukkan URL Git Repository GitHub Anda: "

if "%REPO_URL%"=="" (
    echo Error: URL repositori tidak boleh kosong.
    pause
    exit /b
)

echo.
echo Menghubungkan remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Mengunggah proyek ke GitHub...
git push -u origin main

echo.
echo ================================================================
echo SUKSES TERUNGGAH!
echo Sekarang buka tab 'Actions' di repositori GitHub Anda:
echo Proyek sedang dikompilasi menjadi APK secara otomatis di Cloud.
echo ================================================================
pause
