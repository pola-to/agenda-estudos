import sqlite3
import datetime
import pandas as pd

class EstudosDB:
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        self.conn = sqlite3.connect('estudos.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem"""
        cursor = self.conn.cursor()
        
        # Tabela de matérias
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE
        )
        ''')
        
        # Tabela de eventos de estudo
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos_estudo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE,
            hora_inicio TIME,
            hora_fim TIME,
            materia_id INTEGER,
            duracao_minutos INTEGER,
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        )
        ''')
        
        self.conn.commit()

    def add_materia(self, nome):
        """Adiciona uma nova matéria"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO materias (nome) VALUES (?)', (nome,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_materias(self):
        """Retorna lista de todas as matérias"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome FROM materias ORDER BY nome')
        return [row[0] for row in cursor.fetchall()]

    def remove_materia(self, nome):
        """Remove uma matéria"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM materias WHERE nome = ?', (nome,))
        self.conn.commit()

    def add_evento(self, data, hora_inicio, hora_fim, materia):
        """Adiciona um novo evento de estudo"""
        cursor = self.conn.cursor()
        
        # Obtém o ID da matéria
        cursor.execute('SELECT id FROM materias WHERE nome = ?', (materia,))
        result = cursor.fetchone()
        if not result:
            self.add_materia(materia)
            cursor.execute('SELECT id FROM materias WHERE nome = ?', (materia,))
            result = cursor.fetchone()
        
        materia_id = result[0]
        
        # Calcula a duração em minutos
        inicio = datetime.datetime.combine(data, hora_inicio)
        fim = datetime.datetime.combine(data, hora_fim)
        duracao = (fim - inicio).seconds // 60
        
        cursor.execute('''
        INSERT INTO eventos_estudo (data, hora_inicio, hora_fim, materia_id, duracao_minutos)
        VALUES (?, ?, ?, ?, ?)
        ''', (data.strftime('%Y-%m-%d'), hora_inicio.strftime('%H:%M'),
              hora_fim.strftime('%H:%M'), materia_id, duracao))
        
        self.conn.commit()

    def get_study_data(self, start_date, end_date):
        """Retorna dados de estudo para análise"""
        query = '''
        SELECT 
            e.data,
            e.hora_inicio,
            m.nome as materia,
            e.duracao_minutos
        FROM eventos_estudo e
        JOIN materias m ON e.materia_id = m.id
        WHERE e.data BETWEEN ? AND ?
        ORDER BY e.data, e.hora_inicio
        '''
        
        try:
            df = pd.read_sql_query(
                query, 
                self.conn,
                params=(start_date.strftime('%Y-%m-%d'), 
                       end_date.strftime('%Y-%m-%d'))
            )
            return df
        except Exception as e:
            print(f"Erro ao obter dados: {e}")
            return None

    def __del__(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()
        