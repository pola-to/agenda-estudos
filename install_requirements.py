import subprocess
import sys

def install_packages():
    packages = [
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'PyQt5'
    ]
    
    print("=== Instalando dependências necessárias ===")
    for package in packages:
        try:
            print(f"\nInstalando {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {package}: {e}")
            return False
    
    print("\n=== Todas as dependências foram instaladas! ===")
    return True

if __name__ == "__main__":
    install_packages() 