@echo off
setlocal
pushd %~dp0
color


call ..\venv\Scripts\activate.bat
call python -m invoke all


:deactivate
call deactivate
:end
endlocal
popd