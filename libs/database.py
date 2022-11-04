from colorit import *
import sqlite3
import datetime

#configurações de comandos
TABLE_ADD_USERS = """
INSERT INTO usuarios VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
"""

UPDATE_USERS = """
UPDATE usuarios SET
endereco = '{}',
horario = '{}',
material = '{}',
data = '{}'
WHERE cpf = '{cpf}';
"""

TABLE_DELETE_USERS = """
DELETE FROM usuarios
where cpf = {cpf};
"""

TABLE_FIND = """
SELECT {get} FROM usuarios
WHERE {key} = '{value}';
"""

TABLE_GET = """
SELECT nome, endereco, horario, material, cpf, data FROM usuarios
WHERE privilegio = 'U'
ORDER BY horario;
"""

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS usuarios(
    cpf TEXT NOT NULL PRIMARY KEY,
    privilegio TEXT DEFAULT 'U',
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    endereco TEXT,
    horario TEXT NOT NULL,
    material TEXT NOT NULL,
    data TEXT NOT NULL,
    ultima_modificacao TEXT NOT NULL
);
"""

DATA_FORMAT = "{}-{}-{} {}:{}:{}"

#pegar horario atual
def GetTimeNow():
    now = datetime.datetime.now()
    return DATA_FORMAT.format(now.year, now.month, now.day, now.hour, now.minute, now.second)


class database():
    #adiciona usuario na tabela
    def AddUser(self, _cpf, _name, _email, _password, _endereco, _hour, _material, _date, _privilege = 'U'):
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return False
        
        #adiciona usuario na tabela
        self.mycursor.execute(TABLE_ADD_USERS.format(_cpf, _privilege, _name, _email, _password, _endereco, str(_hour), _material, _date, GetTimeNow()))
        self.mydb.commit()
        print(color("Usuario "+_name+" registrado.", Colors.blue))
        return True

    def UpdateUser(self, _cpf, _endereco, _hour, _material, _date):
        print(_date)
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return False
        
        #atualiza usuario
        self.mycursor.execute(UPDATE_USERS.format(_endereco, str(_hour), _material, _date, cpf=str(_cpf)))
        self.mydb.commit()
        return True

    #deleta usuario adicionado
    def DeleteUser(self, _cpf):
        print(_cpf)
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return False

        #verifica se ja foi deletado
        if not self.GetUserByValue('cpf', str(_cpf), _justCheck = True): return False

        #deleta usuario
        self.mycursor.execute(TABLE_DELETE_USERS.format(cpf=str(_cpf)))
        self.mydb.commit()


    #consultar valor na lista
    def GetUserByValue(self, _key, _value, _justCheck = False, _get="*"):
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return None
        
        #consulta valor
        self.mycursor.execute(TABLE_FIND.format(key=_key, get=_get, value=_value))
        if _justCheck:
            if len(self.mycursor.fetchall()) == 0: return False
            else: return True
        return self.mycursor.fetchall()


    #pega usuarios registrados
    def GetTableList(self):
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return None

        #consulta tabela
        self.mycursor.execute(TABLE_GET)
        return self.mycursor.fetchall()


    #inicia o banco de dados no servidor
    def InitDatabase(self, _name='servidor_web'):
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com o servidor MySQL não estabelecida.", Colors.red))
            return False

        #cria o a tabela    
        self.mycursor.execute(CREATE_TABLE)
        print(color("Banco de Dados criado com sucesso.", Colors.blue))
        return True


    #tenta conectar com o banco de dados
    def TryConnect(self):
        try: 
            self.mydb = sqlite3.connect('database.db', check_same_thread=False)
            print(color("Conexão com o servidor MySQL estabelecido.", Colors.purple))
            self.mycursor = self.mydb.cursor()
            self.connect = True
            return True
        except sqlite3.Error as _error:
            print(color("Ocorreu um erro ao tentar estabelecer uma conexão com o servidor MySQL.", Colors.red))
            print(color(_error, Colors.red))
            self.connect = False
            return False


    #seta as configurações
    def __init__(self, _address="localhost", _port=3306, _user="root", _password="root"):
        self.connect = False
        self.address = _address
        self.port = _port
        self.user = _user
        self.password = _password