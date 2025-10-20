#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'credentials_file': 'credentials/captured.json'}

def show_dashboard():
    config = load_config()
    cred_file = config['credentials_file']
    
    os.system('clear' if os.name != 'nt' else 'cls')
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                  DASHBOARD - CREDENCIAIS CAPTURADAS              ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    if not os.path.exists(cred_file):
        print("  [!] Nenhuma credencial capturada ainda")
        print("  [!] Arquivo: {0} nao existe\n".format(cred_file))
        return
    
    try:
        with open(cred_file, 'r') as f:
            data = json.load(f)
    except:
        print("  [!] Erro ao ler arquivo de credenciais\n")
        return
    
    if not data:
        print("  [!] Nenhuma credencial registrada\n")
        return
    
    print("  Total de capturas: {0}\n".format(len(data)))
    print("="*70)
    
    for i, entry in enumerate(data, 1):
        print("\n  [{0}] {1}".format(i, entry['timestamp']))
        print("      Email/Usuario: {0}".format(entry['email']))
        print("      Senha: {0}".format(entry['password']))
        print("      IP: {0}".format(entry['ip']))
        print("      Device: {0}".format(entry['user_agent'][:60]))
        print("  " + "-"*66)
    
    print("\n  Arquivo: {0}".format(cred_file))
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    show_dashboard()
