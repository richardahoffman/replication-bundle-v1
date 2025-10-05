@echo off
setlocal
python "%~dp0run_all.py" --validate --strict
if errorlevel 1 (
  echo Validation failed. See errors above.
  exit /b 1
)
echo All required checks passed.
endlocal
