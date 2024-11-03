import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

class EstudosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Estudos")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4285f4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
        """)
        self.initUI()
        self.service = self.get_calendar_service()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Campos de entrada
        form_layout = QFormLayout()
        
        self.titulo = QLineEdit()
        self.titulo.setPlaceholderText("Digite o título do evento")
        
        self.data = QDateEdit()
        self.data.setDate(QDate.currentDate())
        
        self.hora_inicio = QTimeEdit()
        self.hora_fim = QTimeEdit()
        
        form_layout.addRow("Título:", self.titulo)
        form_layout.addRow("Data:", self.data)
        form_layout.addRow("Hora Início:", self.hora_inicio)
        form_layout.addRow("Hora Fim:", self.hora_fim)

        # Botão de adicionar evento
        btn_adicionar = QPushButton("Adicionar Evento")
        btn_adicionar.clicked.connect(self.adicionar_evento)

        layout.addLayout(form_layout)
        layout.addWidget(btn_adicionar)
        
        self.setGeometry(300, 300, 400, 250)

    def get_calendar_service(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def adicionar_evento(self):
        data = self.data.date().toPyDate()
        hora_inicio = self.hora_inicio.time().toPyTime()
        hora_fim = self.hora_fim.time().toPyTime()

        inicio = datetime.datetime.combine(data, hora_inicio)
        fim = datetime.datetime.combine(data, hora_fim)

        evento = {
            'summary': self.titulo.text(),
            'start': {
                'dateTime': inicio.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': fim.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        try:
            evento = self.service.events().insert(calendarId='primary', body=evento).execute()
            QMessageBox.information(self, "Sucesso", "Evento adicionado com sucesso!")
            self.titulo.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao adicionar evento: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EstudosApp()
    ex.show()
    sys.exit(app.exec_())