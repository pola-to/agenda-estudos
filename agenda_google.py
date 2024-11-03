import sys
import datetime
import os.path
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from database import EstudosDB  # Certifique-se de que este arquivo existe
from qt_material import apply_stylesheet, list_themes

# Configurações
SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = 'America/Campo_Grande'

# Cores personalizadas
ACCENT_COLOR_LIGHT = "#1a73e8"
ACCENT_COLOR_DARK = "#00a6ff"
BACKGROUND_DARK = "#1e1e1e"
SURFACE_DARK = "#2d2d2d"
BORDER_DARK = "#3d3d3d"

# Estilos atualizados
LIGHT_STYLE = """
    QMainWindow, QWidget {
        background-color: #ffffff;
        color: #333333;
    }
    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
    }
    QTabBar::tab {
        background-color: #f5f5f5;
        color: #333333;
        padding: 8px 12px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background-color: #ffffff;
        border-bottom: 2px solid #1a73e8;
    }
    QTabBar::tab:hover {
        background-color: #e8e8e8;
    }
    QGroupBox {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-top: 1ex;
        padding: 15px;
        font-weight: bold;
    }
    QGroupBox::title {
        color: #1a73e8;
    }
    QPushButton {
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #1557b0;
    }
    QComboBox, QLineEdit, QTextEdit, QDateEdit, QTimeEdit {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 8px;
        background-color: white;
        selection-background-color: #1a73e8;
        selection-color: white;
    }
    QComboBox:hover, QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #1a73e8;
    }
    QCalendarWidget {
        background-color: white;
    }
    QCalendarWidget QToolButton {
        color: #1a73e8;
    }
    QCalendarWidget QMenu {
        background-color: white;
        border: 1px solid #e0e0e0;
    }
    QCalendarWidget QTableView {
        selection-background-color: #1a73e8;
        selection-color: white;
    }
    QScrollBar:vertical {
        background-color: #f5f5f5;
        width: 12px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background-color: #c0c0c0;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #a0a0a0;
    }
    QToolBar {
        background-color: #f5f5f5;
        border-bottom: 1px solid #e0e0e0;
        spacing: 10px;
        padding: 5px;
    }
    QToolBar QAction {
        color: #333333;
        background-color: transparent;
        padding: 5px 15px;
        border-radius: 4px;
    }
    QToolBar QAction:hover {
        background-color: #e8e8e8;
    }
"""

DARK_STYLE = """
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #333333;
        background-color: #1e1e1e;
    }
    QTabWidget::tab-bar {
        left: 5px;
    }
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 8px 12px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background-color: #3d3d3d;
        border-bottom: 2px solid #00a6ff;
    }
    QTabBar::tab:hover {
        background-color: #353535;
    }
    QGroupBox {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        margin-top: 1ex;
        padding: 15px;
        font-weight: bold;
    }
    QGroupBox::title {
        color: #00a6ff;
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 5px;
    }
    QPushButton {
        background-color: #00a6ff;
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #0088cc;
    }
    QComboBox {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 5px;
        padding: 5px;
        color: white;
    }
    QComboBox:hover {
        border: 1px solid #00a6ff;
    }
    QComboBox::drop-down {
        border: none;
        padding-right: 15px;
    }
    QComboBox::down-arrow {
        image: none;
        border: none;
    }
    QLineEdit, QTextEdit, QDateEdit, QTimeEdit {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 5px;
        padding: 8px;
        color: white;
        selection-background-color: #00a6ff;
        selection-color: white;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #00a6ff;
    }
    QCalendarWidget {
        background-color: #2d2d2d;
        color: white;
    }
    QCalendarWidget QToolButton {
        color: white;
        background-color: #2d2d2d;
        padding: 5px;
    }
    QCalendarWidget QMenu {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #3d3d3d;
    }
    QCalendarWidget QSpinBox {
        background-color: #2d2d2d;
        color: white;
        selection-background-color: #00a6ff;
    }
    QCalendarWidget QTableView {
        background-color: #2d2d2d;
        selection-background-color: #00a6ff;
        selection-color: white;
        alternate-background-color: #353535;
    }
    QLabel {
        color: white;
    }
    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 12px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background-color: #404040;
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #4a4a4a;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
"""

CUSTOM_STYLE = """
/* Estilo geral */
QMainWindow {
    background-color: #f5f5f5;
}

/* Painéis */
#leftPanel, #rightPanel {
    background-color: white;
    border-radius: 10px;
}

/* Calendário */
#calendar {
    background-color: white;
    border-radius: 8px;
    padding: 10px;
}

/* Lista de eventos */
#eventosList {
    border: none;
    border-radius: 8px;
    padding: 5px;
}

#eventosList::item {
    padding: 8px;
    margin: 2px 0;
    border-radius: 4px;
}

#eventosList::item:selected {
    background-color: #00897b;
    color: white;
}

/* Botões */
#deleteButton {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

#actionButton {
    padding: 8px 16px;
    border-radius: 4px;
}

/* Campos de formulário */
#formField {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
}

#descriptionField {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
}

/* Grupos */
QGroupBox {
    font-weight: bold;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 1ex;
    padding: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
"""

def get_google_calendar_service():
    """Função para obter o serviço do Google Calendar"""
    creds = None
    
    # Verifica se existe token salvo
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se não há credenciais válidas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Salva as credenciais
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    
    # Retorna o serviço do Google Calendar
    return build('calendar', 'v3', credentials=creds)

class AnalyticsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.is_dark_mode = True  # Adiciona o atributo is_dark_mode
        self.setup_ui()
        self.configure_dark_plot_style()

    def configure_dark_plot_style(self):
        """Configura o estilo dark para os gráficos"""
        plt.rcParams.update({
            'figure.facecolor': '#1e1e1e',
            'axes.facecolor': '#2d2d2d',
            'axes.edgecolor': '#ffffff',
            'axes.labelcolor': '#ffffff',
            'axes.grid': True,
            'grid.color': '#404040',
            'grid.alpha': 0.3,
            'text.color': '#ffffff',
            'xtick.color': '#ffffff',
            'ytick.color': '#ffffff',
            'figure.dpi': 100,
            'axes.spines.top': False,
            'axes.spines.right': False,
        })

    def configure_light_plot_style(self):
        """Configura o estilo light para os gráficos"""
        plt.style.use('default')
        plt.rcParams.update({
            'figure.facecolor': '#ffffff',
            'axes.facecolor': '#ffffff',
            'axes.edgecolor': '#333333',
            'axes.labelcolor': '#333333',
            'axes.grid': True,
            'grid.color': '#e0e0e0',
            'grid.alpha': 0.5,
            'text.color': '#333333',
            'xtick.color': '#333333',
            'ytick.color': '#333333',
            'figure.dpi': 100,
            'axes.spines.top': False,
            'axes.spines.right': False,
        })

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Controles superiores
        controls_layout = QHBoxLayout()
        
        # Seletor de tipo de gráfico
        self.chart_type = QComboBox()
        self.chart_type.addItems([
            "📊 Gráfico de Barras",
            "🥧 Grfico de Pizza",
            "📈 Evolução Temporal",
            "📉 Distribuição por Horário"
        ])
        self.chart_type.currentIndexChanged.connect(self.update_chart)
        
        # Seletor de período
        self.period_type = QComboBox()
        self.period_type.addItems([
            "Última Semana",
            "Último Mês",
            "Último Trimestre",
            "Último Ano",
            "Todo o Período"
        ])
        self.period_type.currentIndexChanged.connect(self.update_chart)
        
        controls_layout.addWidget(QLabel("Tipo de Gráfico:"))
        controls_layout.addWidget(self.chart_type)
        controls_layout.addWidget(QLabel("Período:"))
        controls_layout.addWidget(self.period_type)
        
        layout.addLayout(controls_layout)
        
        # Área do grfico
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Área de estatísticas
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(100)
        layout.addWidget(self.stats_text)

    def set_dark_mode(self, is_dark):
        """Atualiza o modo escuro/claro"""
        self.is_dark_mode = is_dark
        if is_dark:
            self.configure_dark_plot_style()
        else:
            self.configure_light_plot_style()
        self.update_chart()

    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Obter dados do banco
        data = self.get_filtered_data()
        
        chart_type = self.chart_type.currentText()
        
        if "Barras" in chart_type:
            self.plot_bar_chart(ax, data)
        elif "Pizza" in chart_type:
            self.plot_pie_chart(ax, data)
        elif "Evolução" in chart_type:
            self.plot_evolution_chart(ax, data)
        elif "Horário" in chart_type:
            self.plot_time_distribution(ax, data)
        else:
            self.show_statistics(data)

        self.canvas.draw()

    def plot_bar_chart(self, ax, data):
        if data.empty:
            ax.text(0.5, 0.5, 'Sem dados para exibir',
                   ha='center', va='center',
                   color='gray' if not self.is_dark_mode else 'white')
            return
            
        labels = data['materia'].unique()
        values = data.groupby('materia')['duracao_minutos'].sum()
        
        bars = ax.bar(labels, values, color='#00a6ff', alpha=0.7)
        ax.set_title('Tempo Total de Estudo por Matéria', pad=20)
        ax.set_ylabel('Minutos')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}min',
                   ha='center', va='bottom',
                   color='white' if self.is_dark_mode else 'black')
        
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.1)

    def plot_pie_chart(self, ax, data):
        if data.empty:
            ax.text(0.5, 0.5, 'Sem dados para exibir',
                   ha='center', va='center',
                   color='gray' if not self.is_dark_mode else 'white')
            return
            
        total_by_subject = data.groupby('materia')['duracao_minutos'].sum()
        colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(total_by_subject)))
        
        patches, texts, autotexts = ax.pie(
            total_by_subject,
            labels=total_by_subject.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        for autotext in autotexts:
            autotext.set_color('white' if self.is_dark_mode else 'black')
        for text in texts:
            text.set_color('white' if self.is_dark_mode else 'black')
            
        ax.set_title('Distribuição do Tempo de Estudo')

    def plot_evolution_chart(self, ax, data):
        if data.empty:
            ax.text(0.5, 0.5, 'Sem dados para exibir',
                   ha='center', va='center',
                   color='gray' if not self.is_dark_mode else 'white')
            return
            
        daily_study = data.groupby(['data', 'materia'])['duracao_minutos'].sum().unstack()
        
        for column in daily_study.columns:
            ax.plot(daily_study.index, daily_study[column], 
                   marker='o', label=column)
        
        ax.set_title('Evolução do Tempo de Estudo')
        ax.set_xlabel('Data')
        ax.set_ylabel('Minutos')
        ax.legend()
        plt.xticks(rotation=45)

    def plot_time_distribution(self, ax, data):
        # Agrupa por hora do dia
        data['hora'] = pd.to_datetime(data['hora_inicio']).dt.hour
        hourly_study = data.groupby('hora')['duracao_minutos'].sum()
        
        ax.plot(hourly_study.index, hourly_study.values, 
               marker='o', linestyle='-')
        ax.set_title('Distribuição de Estudos por Horário')
        ax.set_xlabel('Hora do Dia')
        ax.set_ylabel('Minutos Totais')
        
        # Adiciona grade para melhor visualização
        ax.grid(True, linestyle='--', alpha=0.7)

    def show_statistics(self, data):
        if data.empty:
            stats = """
            📊 Sem dados para análise
            
            Adicione alguns eventos de estudo para ver as estatísticas!
            """
        else:
            total_horas = data['duracao_minutos'].sum() / 60
            media_diaria = data.groupby('data')['duracao_minutos'].sum().mean() / 60
            materia_mais_estudada = data.groupby('materia')['duracao_minutos'].sum().idxmax()
            dias_estudo = data['data'].nunique()
            
            stats = f"""
            📊 Resumo Estatístico:
            
            Total de Horas Estudadas: {total_horas:.1f}h
            Média Diária: {media_diaria:.1f}h
            Matéria Mais Estudada: {materia_mais_estudada}
            Dias de Estudo: {dias_estudo}
            """
        
        self.stats_text.setText(stats)

    def get_filtered_data(self):
        """Obtém dados filtrados baseado no período selecionado"""
        try:
            period = self.period_type.currentText()
            
            # Define o período
            end_date = datetime.datetime.now(datetime.UTC)
            if period == "Última Semana":
                start_date = end_date - datetime.timedelta(days=7)
            elif period == "Último Mês":
                start_date = end_date - datetime.timedelta(days=30)
            elif period == "Último Trimestre":
                start_date = end_date - datetime.timedelta(days=90)
            elif period == "Último Ano":
                start_date = end_date - datetime.timedelta(days=365)
            else:  # Todo o Período
                start_date = datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC)

            # Obtém os dados do banco
            data = self.db.get_study_data(start_date, end_date)
            
            # Garante que sempre retorne um DataFrame, mesmo que vazio
            if data is None:
                return pd.DataFrame(columns=['data', 'hora_inicio', 'materia', 'duracao_minutos'])
                
            return data
            
        except Exception as e:
            print(f"Erro ao filtrar dados: {e}")
            return pd.DataFrame(columns=['data', 'hora_inicio', 'materia', 'duracao_minutos'])

class AgendaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicializa com modo escuro desligado
        self.is_dark_mode = False
        
        # Configura o estilo inicial da janela
        self.setup_window_style()
        self.setMinimumSize(1000, 700)
        
        # Inicializa o banco de dados
        try:
            self.db = EstudosDB()
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro ao inicializar banco de dados: {str(e)}")
            sys.exit(1)
        
        # Inicializa o serviço do Google Calendar
        try:
            self.service = get_google_calendar_service()
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro ao conectar com Google Calendar: {str(e)}")
            sys.exit(1)
        
        self.setup_ui()
        self.apply_theme()  # Aplica o tema inicial
        self.load_eventos()

    def setup_window_style(self):
        """Configura o estilo da janela"""
        # Título da janela com emoji como ícone
        self.setWindowTitle("📅 Agenda de Estudos")
        
        # Estilo da barra de título
        if self.is_dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #3d3d3d;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                }
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #333333;
                }
                QMenuBar::item:selected {
                    background-color: #e0e0e0;
                }
                QStatusBar {
                    background-color: #f0f0f0;
                    color: #333333;
                }
            """)

    def setup_ui(self):
        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Adiciona botão de alternar tema
        self.theme_button = QPushButton("☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro")
        self.theme_button.clicked.connect(self.toggle_theme)
        main_layout.addWidget(self.theme_button)
        
        # Criar TabWidget
        self.tab_widget = QTabWidget()
        
        # Aba do calendário
        calendar_tab = QWidget()
        calendar_layout = QHBoxLayout(calendar_tab)
        
        # Painéis
        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        calendar_layout.addWidget(left_panel)
        calendar_layout.addWidget(right_panel)
        
        # Aba de análises
        analytics_tab = AnalyticsTab(self.db)
        
        # Adicionar abas
        self.tab_widget.addTab(calendar_tab, "📅 Calendário")
        self.tab_widget.addTab(analytics_tab, "📊 Análises")
        
        main_layout.addWidget(self.tab_widget)
        self.setCentralWidget(main_widget)

        # Estilo especial para o botão de tema
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """ if self.is_dark_mode else """
            QPushButton {
                background-color: #e0e0e0;
                color: #333333;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Calendário
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.clicked.connect(self.data_selecionada)
        layout.addWidget(self.calendar_widget)

        # Grupo de Eventos
        eventos_group = QGroupBox("📅 Eventos do Dia")
        eventos_layout = QVBoxLayout(eventos_group)
        
        # Lista de eventos
        self.lista_eventos = QListWidget()
        eventos_layout.addWidget(self.lista_eventos)
        
        # Botão de excluir
        btn_layout = QHBoxLayout()
        self.btn_excluir_evento = QPushButton("🗑️ Excluir")
        self.btn_excluir_evento.setEnabled(False)
        self.btn_excluir_evento.clicked.connect(self.excluir_evento_selecionado)
        
        btn_layout.addWidget(self.btn_excluir_evento)
        eventos_layout.addLayout(btn_layout)
        
        # Conecta a seleção da lista
        self.lista_eventos.itemSelectionChanged.connect(self.atualizar_botao_excluir)
        
        layout.addWidget(eventos_group)
        return panel

    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Formulário
        form_group = QGroupBox("📝 Novo Evento")
        form_layout = QFormLayout(form_group)
        
        self.titulo = QLineEdit()
        self.materia = QComboBox()
        self.materia.setEditable(True)
        
        self.data = QDateEdit()
        self.data.setDate(QDate.currentDate())
        self.data.setCalendarPopup(True)
        
        self.hora_inicio = QTimeEdit()
        self.hora_fim = QTimeEdit()
        self.hora_fim.setTime(QTime.currentTime().addSecs(3600))
        
        self.descricao = QTextEdit()
        self.descricao.setMaximumHeight(100)
        
        # Adiciona botão para gerenciar matérias
        btn_gerenciar = QPushButton("📚 Gerenciar Matérias")
        btn_gerenciar.clicked.connect(self.show_gerenciar_materias)
        form_layout.addRow("", btn_gerenciar)
        
        form_layout.addRow("Título:", self.titulo)
        form_layout.addRow("Matéria:", self.materia)
        form_layout.addRow("Data:", self.data)
        form_layout.addRow("Início:", self.hora_inicio)
        form_layout.addRow("Fim:", self.hora_fim)
        form_layout.addRow("Descrição:", self.descricao)
        
        layout.addWidget(form_group)
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("💾 Salvar")
        btn_limpar = QPushButton("🧹 Limpar")
        
        btn_salvar.clicked.connect(self.adicionar_evento)
        btn_limpar.clicked.connect(self.limpar_formulario)
        
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_limpar)
        
        layout.addLayout(btn_layout)
        
        return panel

    def atualizar_botao_excluir(self):
        """Habilita/desabilita o botão de excluir baseado na seleção"""
        self.btn_excluir_evento.setEnabled(len(self.lista_eventos.selectedItems()) > 0)

    def excluir_evento_selecionado(self):
        """Exclui o evento selecionado na lista"""
        item_selecionado = self.lista_eventos.currentItem()
        if not item_selecionado:
            return
            
        evento_texto = item_selecionado.text()
        
        # Confirmação
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Tem certeza que deseja excluir este evento?")
        msg.setInformativeText(evento_texto)
        msg.setWindowTitle("Confirmar Exclusão")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            try:
                eventos = self.obter_eventos_do_dia()
                for evento in eventos:
                    if evento['summary'] in evento_texto:
                        self.service.events().delete(
                            calendarId='primary',
                            eventId=evento['id']
                        ).execute()
                        
                        self.lista_eventos.takeItem(self.lista_eventos.row(item_selecionado))
                        QMessageBox.information(self, "Sucesso", "✅ Evento excluído com sucesso!")
                        break
                        
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"❌ Erro ao excluir evento: {str(e)}")

    def load_eventos(self):
        """Carrega eventos do Google Calendar"""
        try:
            # Usa datetime.UTC para timezone aware
            now = datetime.datetime.now(datetime.UTC).isoformat()
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            self.lista_eventos.clear()
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                self.lista_eventos.addItem(f"{start}: {event['summary']}")

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar eventos: {str(e)}")

    def data_selecionada(self, date):
        self.data.setDate(date)

    def limpar_formulario(self):
        self.titulo.clear()
        self.materia.setCurrentIndex(0)
        self.data.setDate(QDate.currentDate())
        self.hora_inicio.setTime(QTime.currentTime())
        self.hora_fim.setTime(QTime.currentTime().addSecs(3600))
        self.descricao.clear()

    def adicionar_evento(self):
        if not self.titulo.text().strip():
            QMessageBox.warning(self, "Aviso", "Por favor, insira um título!")
            return

        data = self.data.date().toPyDate()
        hora_inicio = self.hora_inicio.time().toPyTime()
        hora_fim = self.hora_fim.time().toPyTime()

        inicio = datetime.datetime.combine(data, hora_inicio)
        fim = datetime.datetime.combine(data, hora_fim)

        evento = {
            'summary': f"[{self.materia.currentText()}] {self.titulo.text()}",
            'description': self.descricao.toPlainText(),
            'start': {
                'dateTime': inicio.isoformat(),
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': fim.isoformat(),
                'timeZone': TIMEZONE,
            },
        }

        try:
            self.service.events().insert(calendarId='primary', body=evento).execute()
            QMessageBox.information(self, "Sucesso", "✅ Evento adicionado com sucesso!")
            self.limpar_formulario()
            self.load_eventos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"❌ Erro ao adicionar evento: {str(e)}")

    def toggle_theme(self):
        """Alterna entre modo claro e escuro"""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
        
        # Atualiza o texto do botão
        self.theme_button.setText("☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro")
        
        # Atualiza o tema dos gráficos na aba de análises
        analytics_tab = self.tab_widget.widget(1)  # Assume que Analytics é a segunda aba
        if isinstance(analytics_tab, AnalyticsTab):
            analytics_tab.set_dark_mode(self.is_dark_mode)

    def apply_theme(self):
        """Aplica o tema claro ou escuro"""
        base_style = """
            QMainWindow {
                background-color: %(bg)s;
            }
            QWidget {
                background-color: %(bg)s;
                color: %(text)s;
            }
            QTabWidget::pane {
                border: 1px solid %(border)s;
                background-color: %(bg)s;
            }
            QTabBar::tab {
                background-color: %(tab_bg)s;
                color: %(text)s;
                padding: 8px 20px;
                border: 1px solid %(border)s;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
                color: white;
            }
            QLineEdit, QTextEdit, QComboBox, QTimeEdit, QDateEdit {
                background-color: %(input_bg)s;
                color: %(text)s;
                border: 1px solid %(border)s;
                padding: 5px;
                border-radius: 4px;
            }
            QGroupBox {
                border: 1px solid %(border)s;
                margin-top: 10px;
                padding-top: 10px;
                color: %(text)s;
            }
        """

        if self.is_dark_mode:
            colors = {
                'bg': '#1a1a1a',
                'text': '#ffffff',
                'border': '#404040',
                'tab_bg': '#2d2d2d',
                'input_bg': '#333333'
            }
            self.theme_button.setText("☀️ Modo Claro")
        else:
            colors = {
                'bg': '#ffffff',
                'text': '#333333',
                'border': '#dddddd',
                'tab_bg': '#f5f5f5',
                'input_bg': '#ffffff'
            }
            self.theme_button.setText("🌙 Modo Escuro")

        # Aplica o estilo base
        self.setStyleSheet(base_style % colors)

        # Estilo específico para o calendário
        calendar_style = """
            QCalendarWidget {
                background-color: %(bg)s;
            }
            QCalendarWidget QWidget {
                alternate-background-color: %(alt_bg)s;
                background-color: %(bg)s;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: %(text)s;
                background-color: %(bg)s;
                selection-background-color: #0078d4;
                selection-color: white;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: %(nav_bg)s;
            }
            QCalendarWidget QToolButton {
                color: %(text)s;
                background-color: %(nav_bg)s;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
        """ % {
            'bg': colors['bg'],
            'alt_bg': '#2d2d2d' if self.is_dark_mode else '#f5f5f5',
            'text': colors['text'],
            'nav_bg': '#2d2d2d' if self.is_dark_mode else '#f5f5f5'
        }
        
        self.calendar_widget.setStyleSheet(calendar_style)

    def obter_eventos_do_dia(self):
        """Obtém eventos do dia selecionado"""
        data = self.calendar_widget.selectedDate().toPyDate()
        inicio_dia = datetime.datetime.combine(data, datetime.time.min)
        fim_dia = datetime.datetime.combine(data, datetime.time.max)
        
        inicio_dia_iso = inicio_dia.isoformat() + 'Z'
        fim_dia_iso = fim_dia.isoformat() + 'Z'
        
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=inicio_dia_iso,
            timeMax=fim_dia_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

    def editar_evento(self):
        """Abre o formulário de edição do evento selecionado"""
        item_selecionado = self.lista_eventos.currentItem()
        if not item_selecionado:
            return
            
        evento_texto = item_selecionado.text()
        eventos = self.obter_eventos_do_dia()
        
        for evento in eventos:
            if evento['summary'] in evento_texto:
                # Preenche o formulário com os dados do evento
                self.titulo.setText(evento['summary'])
                
                # Extrai a matéria do título (assumindo formato "[Matéria] Título")
                if '[' in evento['summary'] and ']' in evento['summary']:
                    materia = evento['summary'].split(']')[0].replace('[', '')
                    index = self.materia.findText(materia)
                    if index >= 0:
                        self.materia.setCurrentIndex(index)
                
                # Define data e horários
                start = datetime.datetime.fromisoformat(
                    evento['start'].get('dateTime', evento['start'].get('date')).replace('Z', '+00:00'))
                end = datetime.datetime.fromisoformat(
                    evento['end'].get('dateTime', evento['end'].get('date')).replace('Z', '+00:00'))
            
                
                self.data.setDate(QDate(start.year, start.month, start.day))
                self.hora_inicio.setTime(QTime(start.hour, start.minute))
                self.hora_fim.setTime(QTime(end.hour, end.minute))
                
                if 'description' in evento:
                    self.descricao.setText(evento['description'])
                
                # Armazena o ID do evento para atualização
                self.evento_em_edicao = evento['id']
                break

    def show_gerenciar_materias(self):
        dialog = GerenciarMateriasDialog(self.db, self)
        dialog.exec_()
        # Atualiza o combobox de matérias após fechar o diálogo
        self.materia.clear()
        self.materia.addItems(self.db.get_materias())

class GerenciarMateriasDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setup_ui()
        self.load_materias()
        
        # Aplica estilo dark/light mode
        if parent and hasattr(parent, 'is_dark_mode'):
            self.is_dark_mode = parent.is_dark_mode
            self.apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Gerenciar Matérias")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Lista de matérias
        self.lista_materias = QListWidget()
        layout.addWidget(self.lista_materias)

        # Campo para adicionar nova matéria
        input_layout = QHBoxLayout()
        self.nova_materia = QLineEdit()
        self.nova_materia.setPlaceholderText("Digite o nome da nova matéria...")
        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.clicked.connect(self.adicionar_materia)
        
        # Permite adicionar com Enter
        self.nova_materia.returnPressed.connect(self.adicionar_materia)
        
        input_layout.addWidget(self.nova_materia)
        input_layout.addWidget(self.btn_adicionar)
        layout.addLayout(input_layout)

        # Botão remover
        self.btn_remover = QPushButton("Remover Selecionada")
        self.btn_remover.clicked.connect(self.remover_materia)
        layout.addWidget(self.btn_remover)

    def load_materias(self):
        """Carrega matérias do banco de dados"""
        self.lista_materias.clear()
        materias = self.db.get_materias()
        self.lista_materias.addItems(materias)

    def adicionar_materia(self):
        nome = self.nova_materia.text().strip()
        if nome:
            if self.db.add_materia(nome):
                self.load_materias()
                self.nova_materia.clear()
                # Atualiza o combobox na janela principal
                if self.parent():
                    self.parent().materia.clear()
                    self.parent().materia.addItems(self.db.get_materias())
            else:
                QMessageBox.warning(self, "Erro", 
                    "Esta matéria já existe!")

    def remover_materia(self):
        item = self.lista_materias.currentItem()
        if item:
            reply = QMessageBox.question(self, "Confirmar", 
                f"Deseja remover a matéria '{item.text()}'?",
                QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.db.remove_materia(item.text())
                self.load_materias()
                # Atualiza o combobox na janela principal
                if self.parent():
                    self.parent().materia.clear()
                    self.parent().materia.addItems(self.db.get_materias())

    def apply_theme(self):
        """Aplica o tema dark/light"""
        if self.is_dark_mode:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1a1a1a;
                    color: white;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: white;
                    border: 1px solid #404040;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: white;
                    border: 1px solid #404040;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1084d9;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: white;
                    color: #333333;
                }
                QListWidget {
                    background-color: white;
                    border: 1px solid #dddddd;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #dddddd;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1084d9;
                }
            """)

def main():
    import sys
    
    app = QApplication(sys.argv)
    
    # Aplica o tema material
    apply_stylesheet(app, theme='dark_teal.xml')
    
    # Aplica estilos personalizados
    app.setStyleSheet(CUSTOM_STYLE)
    
    ex = AgendaApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 