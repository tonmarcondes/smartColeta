from colorit import *
import mysql.connector
import datetime

#configurações de comandos
TABLE_ADD_USERS = """
INSERT INTO usuarios VALUES('{}','{}','{}','{}','{}','{}',{},'{}','{}');
"""

TABLE_DELETE_USERS = """
DELETE FROM usuarios
where cpf = {cpf};
"""

TABLE_FIND = """
SELECT {get} FROM usuarios
WHERE {key} = '{value}'
"""

TABLE_GET = """
SELECT nome, endereco, horario, material, cpf FROM usuarios
WHERE privilegio = 'U'
ORDER BY horario;
"""

CREATE_TABLE = """
CREATE TABLE usuarios(
    cpf varchar(11) NOT NULL,
    privilegio enum('A','W','U') DEFAULT 'U',
    nome char(40) NOT NULL,
    email varchar(40) NOT NULL,
    senha varchar(64) NOT NULL,
    endereco varchar(256),
    horario tinyint NOT NULL,
    material varchar(40) NOT NULL,
    ultima_modificacao datetime NOT NULL,
    PRIMARY KEY(cpf)
)DEFAULT CHARSET = utf8;
"""

CREATE_DATABASE = """
CREATE DATABASE {}
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
"""

DATA_FORMAT = "{}-{}-{} {}:{}:{}"

#pegar horario atual
def GetTimeNow():
    now = datetime.datetime.now()
    return DATA_FORMAT.format(now.year, now.month, now.day, now.hour, now.minute, now.second)


class database():
    #adiciona usuario na tabela
    def AddUser(self, _cpf, _name, _email, _password, _endereco, _hour, _material, _privilege = 'U'):
        #retorna se não estiver conectado
        if not self.connect:
            print(color("Conexão com a Banco de Dados não estabelecida.", Colors.red))
            return False
        
        #adiciona usuario na tabela
        self.mycursor.execute(TABLE_ADD_USERS.format(_cpf, _privilege, _name, _email, _password, _endereco, str(_hour), _material, GetTimeNow()))
        self.mydb.commit()
        print(color("Usuario "+_name+" registrado.", Colors.blue))
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
        
        #verifica se a o banco já existe
        exists = False
        self.mycursor.execute("SHOW DATABASES")
        for column in self.mycursor:
            for database in column: 
                if database == _name:
                    exists = True
                    break

        #cria o banco de dados se ele não existir
        if not exists:
            self.mycursor.execute(CREATE_DATABASE.format(_name))
            self.mycursor.execute("USE {};".format(_name))
            self.mycursor.execute(CREATE_TABLE)
            print(color("Banco de Dados criado com sucesso.", Colors.blue))

        #entra no banco de dados
        else: self.mycursor.execute("USE {};".format(_name))
        return True


    #tenta conectar com o banco de dados
    def TryConnect(self):
        try: 
            self.mydb = mysql.connector.connect(host=self.address, port=self.port, user=self.user, password=self.password)
            print(color("Conexão com o servidor MySQL estabelecido.", Colors.purple))
            self.mycursor = self.mydb.cursor()
            self.connect = True
            return True
        except mysql.connector.errors as _error:
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