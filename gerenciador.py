import sqlite3
from sqlite3 import Error
import hashlib

def hashToMd5(password):
    return hashlib.md5(password).hexdigest()

def createConnection(db_file = None):
    """
    Deve criar uma conexão com o banco de dados
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def createTable(conn):
    users = """
            CREATE TABLE IF NOT EXISTS users (
                site TEXT NOT NULL,
                login TEXT NOT NULL,
                senha TEXT NOT NULL
            );
          """
    cur = conn.cursor()
    cur.execute(users)
    conn.commit()

    admins = """
                CREATE TABLE IF NOT EXISTS admin_pass (
                    senha_admin TEXT NOT NULL
                );
             """
    cur = conn.cursor()
    cur.execute(admins)
    conn.commit()

def manipulateDatabase(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return cur.fetchall()

def login_admin(conn, password):
    """
    Método verifica se a senha é compatível com a senha no db
    """
    items = manipulateDatabase(conn, "SELECT * FROM admin_pass;")
    for i in items:
        senha_admin = i[0]
        if hashToMd5(password.encode()) == senha_admin:
            return gerenciador(conn)
        else:
            print("Senha errada!!!")
            break

def verifyPassword():
    conn = createConnection("passwords.db")
    createTable(conn)
    password = input("Digite a senha: ")
    sql = """
           SELECT EXISTS (SELECT 1 FROM admin_pass);
          """
    result = manipulateDatabase(conn, sql)
    for i in result:
        verifica_senha = i[0]
        register_admin(conn) if verifica_senha == 0 else login_admin(conn, password)
    
def register_admin(conn):
    """
    Se a senha não existir, ele cria uma senha administrativa.
    """
    senha = hashToMd5(input("Cadastre a sua senha mestra: ").encode())
    sql = f"""
            INSERT INTO admin_pass (senha_admin)
            VALUES ("{senha}")
           """
    manipulateDatabase(conn, sql)
    return login_admin(conn)

def listPassword(conn):
    site = input("Digite o site: ")
    sql = f"""
            SELECT * FROM users WHERE site = "{site}"
           """
    sites = manipulateDatabase(conn, sql)
    for site in sites:
        print(f"Site: {site[0]}, Login: {site[1]}, Senha: {site[2]}")

def addPassword(conn):
    site = input("Digite o site ou aplicação: ")
    login = input("Digite o email ou username: ")
    senha = input("Digite a senha: ")
    sql = f"""
            INSERT INTO users (site, login, senha)
            VALUES ('{site}','{login}','{senha}')
           """
    manipulateDatabase(conn, sql)
    print(f"Cadastro no site {site} cadastrado com sucesso!")

def deletePassword(conn):
    site = input("Digite o site: ")
    sql = f"""
            DELETE FROM users WHERE site = "{site}"
           """
    manipulateDatabase(conn, sql)
    print("Deletado com sucesso!")

def listAllPassswords(conn):
    sql = """
            SELECT * FROM users;
          """ 
    sites = manipulateDatabase(conn, sql)
    for site in sites:
        print(f"Site: {site[0]}, Login: {site[1]}, Senha: {site[2]}")

OPTIONS = {
    "1": listPassword,
    "2": addPassword,
    "3": deletePassword,
    "4": listAllPassswords,
    }

def gerenciador(conn):
    print("BEM VINDO AO SEU GERENCIADOR DE SENHAS!!!")
    opt = 0
    while opt != 5:
        print("""
                ------------OPÇÕES------------
                |1 - LISTAR                  |
                |2 - ACRESCENTAR             |   
                |3 - DELETAR                 |
                |4 - LISTAR TUDO             |
                |5 - SAIR                    |
                ------------------------------
            """)
        option = input("Escolha sua opção: ")
        
        if str(option) in OPTIONS:
            OPTIONS[option](conn)
        elif str(option) == "5":
            print("Ate mais!")
            break
        else:
            print("Opcao Incorreta!")

if __name__ == "__main__":
    verifyPassword()