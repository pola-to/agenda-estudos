import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QColor
from datetime import datetime, timedelta

class AnalyticsWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Criar figura do matplotlib
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def atualizar_graficos(self):
        # Limpar axes
        self.ax1.clear()
        self.ax2.clear()

        # Obter dados
        dados = self.db.get_dados_grafico()
        df = pd.DataFrame(dados, columns=['materia', 'data', 'minutos'])
        df['data'] = pd.to_datetime(df['data'])

        # Gráfico 1: Distribuição de tempo por matéria
        if not df.empty:
            materias = df.groupby('materia')['minutos'].sum()
            self.ax1.bar(materias.index, materias.values)
            self.ax1.set_title('Tempo Total por Matéria')
            self.ax1.set_xlabel('Matéria')
            self.ax1.set_ylabel('Minutos')
            plt.setp(self.ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

            # Gráfico 2: Evolução do tempo de estudo
            for materia in df['materia'].unique():
                materia_df = df[df['materia'] == materia]
                self.ax2.plot(materia_df['data'], materia_df['minutos'], 
                             label=materia, marker='o')
            
            self.ax2.set_title('Evolução do Tempo de Estudo')
            self.ax2.set_xlabel('Data')
            self.ax2.set_ylabel('Minutos')
            self.ax2.legend()
            plt.setp(self.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        else:
            self.ax1.text(0.5, 0.5, 'Sem dados para exibir', 
                         horizontalalignment='center',
                         verticalalignment='center')
            self.ax2.text(0.5, 0.5, 'Sem dados para exibir', 
                         horizontalalignment='center',
                         verticalalignment='center')

        # Ajustar layout e mostrar
        self.figure.tight_layout()
        self.canvas.draw() 

    def data_selecionada(self, date):
        """Atualiza a data selecionada e carrega os eventos do dia"""
        self.data.setDate(date)
        self.load_eventos_do_dia(date)

    def load_eventos_do_dia(self, date):
        """Carrega eventos específicos do dia selecionado"""
        try:
            # Converte QDate para datetime
            inicio_dia = datetime.datetime.combine(date.toPyDate(), datetime.time.min)
            fim_dia = datetime.datetime.combine(date.toPyDate(), datetime.time.max)
            
            # Formata as datas para o formato ISO
            inicio_dia_iso = inicio_dia.isoformat() + 'Z'
            fim_dia_iso = fim_dia.isoformat() + 'Z'

            # Busca eventos do dia
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=inicio_dia_iso,
                timeMax=fim_dia_iso,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])

            # Limpa a lista atual
            self.lista_eventos.clear()

            # Adiciona os eventos do dia
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                # Formata o horário para exibição
                start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_time = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
                
                # Formata a string do evento
                event_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {event['summary']}"
                
                # Adiciona à lista com formatação
                item = QListWidgetItem(event_str)
                
                # Adiciona estilo ao item da lista
                if 'colorId' in event:
                    cor = self.get_event_color(event['colorId'])
                    item.setForeground(QColor(cor))
                
                self.lista_eventos.addItem(item)

            if not events:
                self.lista_eventos.addItem("Nenhum evento para este dia")

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar eventos do dia: {str(e)}")

    def get_event_color(self, color_id):
        """Retorna a cor correspondente ao colorId do evento"""
        colors = {
            '1': '#7986cb',  # Lavanda
            '2': '#33b679',  # Sage
            '3': '#8e24aa',  # Uva
            '4': '#e67c73',  # Flamingo
            '5': '#f6c026',  # Banana
            '6': '#f5511d',  # Tangerina
            '7': '#039be5',  # Pavão
            '8': '#616161',  # Grafite
            '9': '#3f51b5',  # Mirtilo
            '10': '#0b8043', # Basilicão
            '11': '#d60000', # Tomate
        }
        return colors.get(color_id, '#ffffff')  # Branco como cor padrão