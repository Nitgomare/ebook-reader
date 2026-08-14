@echo off
setlocal
set "READER_DIR=%~dp0"
set "READER_PYTHON=%READER_DIR%..\knowledge-base\.venv\Scripts\python.exe"

if not exist "%READER_PYTHON%" (
  echo [ERROR] Python environment was not found:
  echo %READER_PYTHON%
  echo.
  echo Expected workspace layout:
  echo   mkdocstutorial\ebook-reader
  echo   mkdocstutorial\knowledge-base\.venv
  pause
  exit /b 1
)

"%READER_PYTHON%" "%READER_DIR%manage.py" preview %*
exit /b %ERRORLEVEL%

