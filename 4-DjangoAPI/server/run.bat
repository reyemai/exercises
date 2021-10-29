@echo off
setlocal
pushd %~dp0

:: User Settings
set project_name=pkmnsite
set app_name=pkmnapi

:: initialize venv
call %~dp0..\venv\Scripts\activate.bat

pushd %~dp0\%project_name%

:: start server
python manage.py runserver

:deactivate
call deactivate

:end
popd
popd