@echo off
setlocal
pushd %~dp0

:: User Settings
set project_name=pkmnsite
set app_name=pkmnapi

:: initialize venv
call %~dp0..\venv\Scripts\activate.bat

pushd %~dp0\%project_name%

echo #######################################
echo # Remove all entries from database
echo #######################################
python manage.py flush --noinput
if %errorlevel% neq 0 (
    goto :deactivate
)

echo #######################################
echo # Extract changes in the Django models
echo #######################################
python manage.py makemigrations %app_name%
if %errorlevel% neq 0 (
    goto :deactivate
)

echo #######################################
echo # Apply changes to the DB
echo #######################################
python manage.py migrate
if %errorlevel% neq 0 (
    goto :deactivate
)

:deactivate
call deactivate

:end
popd
popd