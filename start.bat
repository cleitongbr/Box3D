@echo off
:: Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao esta instalado ou nao foi adicionado ao PATH.
    pause
    exit /b
)

:: Instalar dependencias do requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Falha ao instalar as dependencias do requirements.txt.
    pause
    exit /b
)

:: Executar o app.py
echo Iniciando a aplicacao...
python app.py
if %errorlevel% neq 0 (
    echo Ocorreu um erro ao executar o app.py.
    pause
    exit /b
)

pause
