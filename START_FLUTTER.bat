@echo off
REM BakeSmart Flutter Emulator Launcher
REM Run Flutter app on Android Emulator

echo.
echo ======================================================================
echo.                    🍰 BakeSmart Flutter Emulator
echo.
echo ======================================================================
echo.

echo Checking for connected emulators...
adb devices

cd prediksi_stok_kue

echo.
echo Starting Flutter app on emulator...
echo Make sure Android Emulator is already running!
echo.

flutter run -d emulator-5554 --no-fast-start

pause
