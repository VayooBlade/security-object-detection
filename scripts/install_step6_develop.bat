@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
if errorlevel 1 exit /b 1

set DISTUTILS_USE_SDK=1
set USE_NINJA=1
set CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7
set CUDA_PATH=%CUDA_HOME%

set "PATH=%~dp0..\.venv\Scripts;%CUDA_HOME%\bin;%PATH%"

cd /d "%~dp0.."
where cl
where nvcc
where ninja
".\.venv\Scripts\python.exe" setup.py develop
exit /b %ERRORLEVEL%
