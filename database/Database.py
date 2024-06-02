import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

def create_database():
    
    # estabelecer conexão ao Banco de Dados
    connection = sqlite3.connect("basedadosbiblioteca.db")

    # banco de dados com informações de livros
    connection.execute('CREATE TABLE IF NOT EXISTS Livros(\
                    id INTEGER PRIMARY KEY,\
                    titulo TEXT,\
                    autor TEXT,\
                    publicacaoano INTEGER,\
                    quantidade, INTEGER)')

    # banco de dados com informações de usuários
    connection.execute('CREATE TABLE IF NOT EXISTS usuarios(\
                    id INTEGER PRIMARY KEY,\
                    nome TEXT,\
                    sobrenome TEXT,\
                    endereco TEXT,\
                    email TEXT,\
                    telefone TEXT)')

    # banco de dados com a informação de emprestimos
    connection.execute('CREATE TABLE IF NOT EXISTS emprestimos(\
                    id INTEGER PRIMARY KEY,\
                    idlivro INTEGER,\
                    idusuario INTEGER,\
                    dataemprestimo TEXT,\
                    datadevolucao TEXT,\
                    FOREIGN KEY(idlivro) REFERENCES livros(id),\
                    FOREIGN KEY(idusuario) REFERENCES usuarios(id))')
        