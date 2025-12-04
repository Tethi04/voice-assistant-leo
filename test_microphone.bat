@echo off
echo Testing Microphone on Windows
echo =============================
echo.
python -c "import speech_recognition as sr; print('Microphones found:'); [print(f'  {i}: {mic}') for i, mic in enumerate(sr.Microphone.list_microphone_names())]"
echo.
echo If you see your microphone listed above, it's working!
echo If not, check Windows sound settings.
echo.
pause
