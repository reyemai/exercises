@echo off
setlocal
pushd %~dp0

:: User Settings
set project_name=pkmnsite
set app_name=pkmnapi
set python39_path=<path_to_your_python39>

:: Initialization
set venv=%~dp0..\venv
set python=%python39_path%\python.exe
set path=%python39_path%;%python39_path%\Scripts;%path%
set PYTHONHOME=%python39_path%

if not exist "%venv%" (
    echo ###############################
    echo # VIRTUAL ENVIRONMENT MISSING #
    echo ###############################
    %python% -m venv %venv%

    echo ###############################
    echo # ACTIVATE VIRTUAL ENV        #
    echo ###############################
    call %venv%\Scripts\activate.bat

    if exist "%~dp0requirements.txt" (
        echo ###############################
        echo # INSTALLING PIP REQUIREMENTS #
        echo ###############################
        python -m pip install -r %~dp0requirements.txt
    )
) else (
    echo ###############################
    echo # ACTIVATE VIRTUAL ENV        #
    echo ###############################
    call %venv%\Scripts\activate.bat
)

if not exist "%~dp0%project_name%" (
    echo ###############################
    echo # DJANGO PROJECT INIT         #
    echo ###############################
    pushd %~dp0
    django-admin startproject %project_name%
    popd
)

pushd %~dp0%project_name%

rem set db=%~dp0%project_name%\db.sqlite3
rem if not exist "%db%" (
rem     echo Create the tables in the database...
rem     python manage.py migrate
rem )

if not exist "%~dp0%project_name%\%app_name%" (
    python manage.py startapp %app_name%
)

echo #####################
echo # Add app to project:
echo #  add one line in:
echo #       %~dp0%project_name%\%project_name%\settings.py
echo #  INSTALLED_APPS = [
echo #     '%app_name%.apps.%app_name%Config' (in CamelCode)
echo #     ...
echo #  ]
echo #####################


:deactivate
call deactivate

:end
popd
popd