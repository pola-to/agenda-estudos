import os
import sys
import subprocess

def verificar_ambiente():
    print("=== Verificando ambiente de desenvolvimento ===\n")
    
    # Verifica Python
    print(f"Python versão: {sys.version.split()[0]}")
    
    # Verifica arquivos necessários
    arquivos = {
        'credentials.json': 'Credenciais do Google',
        'agenda_estudos.py': 'Arquivo principal do programa'
    }
    
    print("\nVerificando arquivos necessários:")
    for arquivo, descricao in arquivos.items():
        if os.path.exists(arquivo):
            print(f"✓ {arquivo} encontrado ({descricao})")
        else:
            print(f"✗ {arquivo} não encontrado! ({descricao})")
    
    # Verifica dependências
    print("\nVerificando dependências instaladas:")
    dependencies = [
        'PyQt5',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✓ {dep} instalado")
        except ImportError:
            print(f"✗ {dep} não instalado")
            resposta = input(f"Deseja instalar {dep} agora? (s/n): ")
            if resposta.lower() == 's':
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])

    # Verifica permissões de arquivo
    print("\nVerificando permissões:")
    try:
        with open('credentials.json', 'r') as f:
            print("✓ credentials.json pode ser lido")
    except Exception as e:
        print(f"✗ Erro ao ler credentials.json: {e}")

    print("\n=== Verificação concluída ===")
    
    return True

if __name__ == "__main__":
    if verificar_ambiente():
        print("\nDeseja executar o programa agora? (s/n): ")
        resposta = input()
        if resposta.lower() == 's':
            print("\nIniciando Agenda de Estudos...")
            subprocess.call([sys.executable, 'agenda_estudos.py']) 