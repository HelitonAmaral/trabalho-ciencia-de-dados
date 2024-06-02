from models import LibrarySystem
from database import Database


# || DATABASE FUNCTIONS ||

# Cadastro de Livro
def cadastro_de_livro(self):
  print("\nCadastro de Livro Novo")
  titulo = input("Qual o título do Livro? ")
  autor = input("Qual o autor do Livro? ")
  anopublicacao = input("Ano de Publicação: ")
  quantidade = input("quantidade de exemplares disponíveis: ")

  new_book = self.book(None, titulo, autor, anopublicacao, quantidade)
  new_book.add_to_library()
  print("\nCadastro efetuado com sucesso!")

def cadastro_de_usuarios(self):
  print("\nCadastro de usuarios")
  nome = input("Qual o nome do Usuario? ")
  sobrenome = input("sobrenome ")
  endereco = input("endereço do Usuario: ")
  email = input("E-mail atualizdo: ")
  telefone = input("Telefone com DDD: ")

  new_user = self.user(None, nome, sobrenome, endereco, email, telefone)
  new_user.add_user()
  print("\nCadastro efetuado com sucesso!")

# emprestimo de livros
def emprestimo(self):
  print("\Emprestimo de Livro")
  idlivro = int(input("ID do livro: "))
  idusuario = int(input("ID usuario que está fazendo o emprestimo: "))
  dataEmprestimo = datetime.date.today().strftime("%d/%m/%y")

  new_loan = self.loan(idlivro, idusuario, dataEmprestimo)
  new_loan.len_book()

# Devolução de livros
def devolucao(self):
  print("\nDevolução")
  idemprestimo = int(input("Id do livro que será devolvido: "))
  dataDevolucao = datetime.date.today().strftime("%d/%m/%Y")
  self.loan.return_book(idemprestimo, dataDevolucao)

# localizar livro
def buscaLivro (self):
  print("\nBusca de livros")
  localizar = input("digite o meio de busca: ")
  self.book.search_books(localizar)


# Função de emprestimos de livros
def lend_book(self):
  db = Database('basedadosbiblioteca.db')
  con = db.connect

  # Verificação de cadastro de livro
  book_available = con.execute("SELECT id FROM livros WHERE id = ?", (self.book_id,)).fetchone()
  if book_available is None:
      print("\nLivro não cadastrado.")
  else:
    # Verificação de quantidade disponível
    quantity_available = con.execute("SELECT quantidade FROM livros WHERE id = ?", (self.book_id)).fetchone()[0]
  
  # Se quantidade disponível maior que zero, então realizar o emprestimo
  if quantity_available > 0:
    con.execute("INSERT INTO emprestimos(idlivro, id_usuario, data_emprestimo) VALUES (?, ?, ?)", (self.book_id, self.user_id, self.loan_date))

    # Se o emprestimo for conluido, atualizar estoque
    con.execute("UPDATE livros SET quantidade = quantidade - 1 WHERE id = ?", (self.book_id,))
    con.commit()
    print("\nEmprestimo Realizado!")
  else:
    print("\n Não existe exemplares disponíveis.")

  con.close()

# Exibir todos os emprestimos
@staticmethod
def todos_os_emprestimos():
  db = Database('basedadosbiblioteca.db')
  con = db.connect()
  loans = con.execute("SELECT emprestimos.id, livros.titulos, usuarios.nome, usuarios.sobrenome, emprestimos.data_emprestimo, emprestimos.data_devolucao\
                      FROM livros\
                      INNER JOIN emprestimos ON livros.id = emprestimos.idlivro\
                      INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario\
                      WHERE emprestimo.data_devolucao IS NULL").fetchall()
  con.close()
# caso não exista nenhum livro emprestado
  if not loans:
      print("\nSem empréstimos no momento.")
      return
  print("\nLivro em empréstimo: \n")
  
  for loan in loans:
      print(f"ID do emprestimo: {loan[0]}")
      print(f"Titulo do livro: {loan[1]}")
      print(f"Nome do Usuario: {loan[2]} {loan[3]}")
      print(f"Data do Emprestimo: {loan[4]}")

# Devolução de livro
@staticmethod
def return_book(loan_id, return_date):
  db = Database('basedadosbiblioteca.db')
  con = db.connect()

  loan = con.execute("SELECT idlivro, data_devolucao FROM emprestimos WHERE id=?", (loan_id,)).fetchone()
  if loan:
    book_id, previous_return_date = loan

    if previous_return_date is not None:
      print(f"Livro devolvido na data: {previous_return_date}.")
      return

  # Atualização de data de devolução
  con.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (return_date, loan_id))
  # Somar o livro devolvido ao estoque
  con.execute("UPDATE livros SET quantidade = quantidade + 1 WHERE id = ?", (book_id,))

  con.commit()
  print("\nLivro devolvido!")

  con.close()

# Exibir todos os usuarios
@staticmethod

def todos_os_usuarios():
  db = Database('basedadosbiblioteca.db')
  con = db.connect()
  Users = con.execute("SELECT * FROM usuarios").fetchall()
  con.close()

  if not Users:
    print("\nusuarios não localizados.")
    return
  
  print("\nUsuarios cadastrados:")
  
  for user in Users:
    print(f"\nNome: {user[1]}{user[2]}")
    print(f"Endereco: {user[3]}")
    print(f"E-mail: {user[4]}")
    print(f"Telefone: {user[5]}")

# Cadastro de usuarios
def add_user(self):
  db = Database('basedadosbiblioteca.db')
  con = db.connect()
  con.execute("INSERT INTO usuarios(nome, sobrenome, endereco, email, telefone) VALUES(?, ?, ?, ?, ?)",
              (self.name, self.surname, self.address, self.email, self.phone))
  con.commit()
  con.close()

# || MENU FUNCTIONS ||

# Menu Cadastro

def exibir_cadastro(self):
  while True:
    print("\nCadastros")
    print("1 Cadastro de Usuario")
    print("2 cadastro de Livro")
    print("3 Voltar ao menu anterior")

    opcao = input("Qual opção deseja realizar: ")

    if opcao == "1":
        self.cadastro_de_usuarios()
    elif opcao == "2":
        self.cadastro_de_livro()
    elif opcao == "3":
        break
    else:
        print("Opção Inválida.")
        

# Menu Empréstimo/Devolução
def exibir_EmprestimosDevolucao(self):
    while True:
        print("\nDevoluções e Emprestimos")
        print("1 Emprestar: ")
        print("2 Devolver: ")
        print("3 Voltar ao menu anterior")

        opcao = input("Qual opção deseja realizar: ")

        if opcao == "1":
            self.emprestimo()
        elif opcao == "2":
            self.devolucao()
        elif opcao == "3":
            break
        else:
            print("Opção Inválida.")

# Menu Relatórios
def exibir_relatorios(self):
  while True:
    print("\nRelatorios")
    print("1 Mostrar todos os usuarios")
    print("2 Mostrar todos os livros")
    print("3 Mostrar todos os livros que estão disponiveis")
    print("4 Mostrar todos os livros que estão emprestados")
    print("5 Voltar ao menu anterior")

    opcao = input("Qual opção deseja realizar: ")

    if opcao == "1":
        self.user.todos_os_usuarios
    elif opcao == "2":
        self.book.todos_os_livros
    elif opcao == "3":
        self.book.Todos_os_livros_disponiveis
    elif opcao == "4":
        self.Loan.todos_os_emprestimos
    elif opcao == "5":
        break
    else:
        print("Opção Inválida.")

# Menu Principal
def exibicaoMenu (self):
  while True:
    print("\nBem-vindo ao Gerenciador\n")
    print("inicio")
    print("1 Cadastrar usuarios ou livros")
    print("2 Emprestimos ou Devoluções")
    print("3 Relatorios")
    print("4 Sair")

    opcao = input("Qual opção deseja realizar: ")

    if opcao == "1":
      self.exibir_cadastro()
    elif opcao == "2":
      self.exibir_EmprestimosDevolucao()
    elif opcao == "3":
      self.exibir_relatorios()
    elif opcao == "4":
      print("Até mais.")
      break
    else:
      print("Opção inválida.")

# Inicio

if __name__ == "_main_":
    library_system = LibrarySystem()
    library_system.exibicaoMenu()
