#!/bin/bash

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python não está instalado ou não foi adicionado ao PATH."
    exit 1
fi

# Instalar dependências do requirements.txt
echo "Instalando dependências..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Falha ao instalar as dependências do requirements.txt."
    exit 1
fi

# Executar o app.py
echo "Iniciando a aplicação..."
python3 app.py
if [ $? -ne 0 ]; then
    echo "Ocorreu um erro ao executar o app.py."
    exit 1
fi

# Manter o terminal aberto
echo "Aplicação encerrada. Pressione qualquer tecla para continuar..."
read -n 1
