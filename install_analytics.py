import subprocess
import sys

def install_requirements():
    packages = [
        'matplotlib',
        'pandas',
        'seaborn',
        'sqlite3',
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado com sucesso!")
        except:
            print(f"✗ Erro ao instalar {package}")

if __name__ == "__main__":
    install_requirements() 