@echo off
cd %~dp0

call .\venv\Scripts\activate.bat

echo activate!
pyinstaller -F -w .\main.py

xcopy .\Load2Desktop.dll .\dist\Load2Desktop.dll /y
xcopy .\assets\ .\dist\assets /s/y
