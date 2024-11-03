import subprocess
import sys

def install_dependencies():
    dependencies = [
        'matplotlib',
        'pandas',
        'seaborn',
        'PyQt5'
    ]

    print("=== Instalando dependências necessárias ===\n")

    for package in dependencies:
        try:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao instalar {package}: {e}")
            return False

    print("\n✅ Processo de instalação concluído!")
    return True

if __name__ == "__main__":
    print("Iniciando instalação das dependências...")
    install_dependencies() 