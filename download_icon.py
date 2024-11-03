import os
import requests

def download_calendar_icon():
    """Baixa um ícone de calendário e salva na pasta assets"""
    # Cria a pasta assets se não existir
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # URL de um ícone de calendário bonito (você pode trocar por outro se preferir)
    icon_url = "https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Calendar/SVG/ic_fluent_calendar_48_regular.svg"
    
    try:
        # Baixa o ícone
        response = requests.get(icon_url)
        response.raise_for_status()
        
        # Salva o arquivo
        with open('assets/calendar.png', 'wb') as f:
            f.write(response.content)
        
        print("✓ Ícone baixado com sucesso!")
        return True
    except Exception as e:
        print(f"✗ Erro ao baixar ícone: {e}")
        return False

if __name__ == "__main__":
    download_calendar_icon() 