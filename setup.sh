#!/bin/bash

echo "============================================="
echo "  Configurando Captive Portal Termux"
echo "============================================="

# Atualizar Termux
echo "[1/4] Atualizando pacotes..."
pkg update -y

# Instalar dependências
echo "[2/4] Instalando Python..."
pkg install python -y

# Criar diretórios
echo "[3/4] Criando estrutura..."
mkdir -p credentials logs templates

# Verificar arquivos
echo "[4/4] Verificando instalacao..."
if [ -f "server.py" ] && [ -f "templates/login.html" ]; then
    echo "✓ Instalacao completa!"
    echo ""
    echo "Para iniciar:"
    echo "  python server.py"
    echo ""
    echo "Para ver credenciais:"
    echo "  python dashboard.py"
else
    echo "✗ Erro: Arquivos faltando"
    exit 1
fi
