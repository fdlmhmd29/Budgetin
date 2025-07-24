@echo off
REM pindah ke direktori script (ubah sesuai path Anda)
cd /d "%~dp0"

REM bersihkan build sebelumnya
rmdir /s /q build dist

REM jalankan PyInstaller
pyinstaller --name "BudgetingTransport" ^
            --onefile ^        REM satu file EXE
            --windowed ^       REM tanpa console window
            --add-data "utils.py;." ^
            --add-data "constants.py;." ^
            --add-data "budgeting.py;." ^
            --add-data "gui.py;." ^
            main.py

pause
