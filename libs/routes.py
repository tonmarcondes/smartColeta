from flask import Blueprint, render_template, redirect, session, request, abort, send_from_directory
import libs.dataformat as Formate
import libs.database as Database
import libs.encode as Encode
import libs.check as Check
from time import sleep
from colorit import *

#chaves do banco de dados
# 'U' = usuario
# 'W' = trabalhador
# 'A' = administrador

EMAIL_ADMIN = "admin@admin"
PASSWORD_ADMIN = "e6b97b5425"
DATABASE_PASSWORD = "9b642e563b"

class Routes:
    #lista de rotas do servidor
    def create_routes(self):
        routes_pages = Blueprint('routes', __name__)

        #rota de login
        @routes_pages.route('/login', methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                #usuarios bloqueados
                if request.environ.get('REMOTE_ADDR') in self.ip_ban_list: abort(403)

                #caso ocorra muitas tentativas bloqueia o usuario
                if session.get('try',None) == None: session['try'] = 0
                elif session.get('try', 0) > 100:
                    print(color("A sessão ["+request.environ.get('REMOTE_ADDR')+"] foi banida por fazer muitas tentativas de login...",Colors.red))
                    self.ip_ban_list.append(request.environ.get('REMOTE_ADDR'))
                    abort(403)
                    return
                else: session['try'] += 1

                #demorar para responder
                if session.get('try', 0) > 10: sleep(session.get('try',0) - 10)

                #banir ip
                if session.get('try', 0) > 100: return

                form = request.form #formulario

                #verifica se é o administrador
                if form.get('email', type=str) == self.admin[0]:
                    if Encode.SHA256(form.get('senha', type=str)) == self.admin[1]:
                        print(color("Administrador logado no IP ["+request.environ.get('REMOTE_ADDR')+"]...",Colors.orange))
                        session['id'] = "00000000000"
                        session['key'] = 'A'
                        session['try'] = 0
                        return redirect("/painel")
                    else: return render_template('login.html', error_email=Check.EMAIL_NOT_EXIST)

                #--------------------------------------verificações--------------------------------------#
                #verifica o formato do email email
                retorno = Check.Email(form.get('email', type=str))
                if not retorno[0]: return render_template('login.html', error_email=retorno[1])

                #verifica se o email foi registrado
                if not self.data.GetUserByValue("email",retorno[1],_justCheck=True):
                    return render_template('login.html', error_email=Check.EMAIL_NOT_EXIST)

                #verifica se a senha bate
                if self.data.GetUserByValue("email",retorno[1],_get="senha")[0][0] != Encode.SHA256(form.get('senha', type=str)):
                    return render_template('login.html', error_email=Check.INCORRECT_PASSWORD)
                #----------------------------------------------------------------------------------------#

                #atribui os valores de sessao
                session["id"] = self.data.GetUserByValue("email",retorno[1],_get="cpf")[0][0]
                session["key"] = self.data.GetUserByValue("email",retorno[1],_get="privilegio")[0][0]

                #remove tentativas
                session['try'] = 0

                #redireciona para pagina
                if session.get('key',None) == 'W': return redirect("/painel")
                else: return redirect("/")

            elif request.method == "GET": return render_template('login.html')


        #rota de registro
        @routes_pages.route('/register', methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                form = request.form #formulario
                formulario = {}
                print(form.get('date',type=str))

                #--------------------------------------verificações-------------------------------------#

                #verifica o formato do cpf
                retorno=Formate.CPF(form.get('cpf',type=str))
                if not retorno[0]: return render_template('register.html', error_cpf=retorno[1])

                #verifica o cpf
                retorno = Check.CPF(retorno[1])
                if not retorno[0]: return render_template('register.html', error_cpf=retorno[1])

                #verifica se o cpf já esta registrado
                if self.data.GetUserByValue("cpf", retorno[1], True, "cpf"): 
                    return render_template('register.html', error_cpf=Check.CPF_ALREADY_EXIST)
                else: formulario['cpf'] = retorno[1]

                #verifica o email
                retorno = Check.Email(form.get('email',type=str))
                if not retorno[0]: return render_template('register.html', error_email=retorno[1])

                #verifica se o email já esta registrado
                if self.data.GetUserByValue("email", retorno[1], True, "email"): 
                    return render_template('register.html', error_email=Check.EMAIL_ALREADY_EXIST)
                else: formulario['email'] = retorno[1]

                #verifica a senha
                retorno = Check.PasswordForce(form.get('senha',type=str))
                if not retorno[0]: return render_template('register.html', error_senha=retorno[1])

                #verifica a senha repetida
                if retorno[1] != form.get('repeatsenha',type=str):
                    return render_template('register.html', error_repeat=Check.REPEAT_PASSWORD)
                else: formulario['password'] = Encode.SHA256(retorno[1])

                #---------------------------------------------------------------------------------------#

                #registra trabalhador no banco de dados
                print(form.get('worker',type=bool))
                if session.get('key',None) == 'A' and form.get('worker',type=bool):
                    if not self.data.AddUser(formulario['cpf'], form.get('nome',type=str).lower(), formulario['email'], formulario['password'], form.get('endereco',type=str).lower(), 0, "nenhuma", "nenhuma", _privilege='W'):
                        return render_template('register.html', error_server=Check.SERVER_ERROR)
                    else: return redirect("/painel")

                #-----------------------------verificações para usuarios--------------------------------#

                #verifica se o horario esta correto
                retorno = Formate.Hour(form.get('hour_select',type=str))
                if not retorno[0]: return render_template('register.html', error_hour=retorno[1])
                else: formulario['hour'] = retorno[1]

                #verifica se a data esta correta
                retorno = Formate.Date(form.get('date',type=str))
                if not retorno[0]: return render_template('register.html', error_date=retorno[1])
                else: formulario['date'] = retorno[1]

                #verifica a descrição da coleta
                retorno = Check.Coleta(form.get('material',type=str))
                if not retorno[0]: return render_template('register.html', error_coleta=retorno[1])
                else: formulario['coleta'] = retorno[1]
                
                #---------------------------------------------------------------------------------------#

                #registra usuario no banco de dados
                if not self.data.AddUser(formulario['cpf'], form.get('nome',type=str).lower(), formulario['email'], formulario['password'], form.get('endereco',type=str).lower(), formulario['hour'], formulario['coleta'], formulario['date']):
                    return render_template('register.html', error_server=Check.SERVER_ERROR)
            
                #enviar email de confirmação
                ###########################################TO DO##################################################

                #redireciona para pagina anterior
                if session.get('key',None) == 'A': redirect("/painel")
                else: return redirect("/login")

            if request.method == "GET":
                if session.get('key',None) == 'A': return render_template('register.html', ADMIN_REGISTER_CHECK=Formate.ADMIN_REGISTER_CHECK)
                else: return render_template('register.html')


        #deslogar da conta
        @routes_pages.route("/logout")
        def logout():
            session["id"] = None
            session["key"] = None
            return redirect("/")


        #painel de controle
        @routes_pages.route("/painel", methods=["GET", "POST"])
        def painel():
            if request.method == "POST" and session.get('key',None) == 'A' and 'delete' in request.form:
                print(request.form.get('delete',None))
                self.data.DeleteUser(request.form.get('delete',"00000000000"))
                return render_template('painel.html',pessoas=self.data.GetTableList(), admin=True, REGISTER_BUTTON=Formate.PAINEL_REGISTER_BUTTON)

            elif request.method == "GET":
                if session.get('key',None) == 'A': return render_template('painel.html',pessoas=self.data.GetTableList(), admin=True, REGISTER_BUTTON=Formate.PAINEL_REGISTER_BUTTON)
                elif session.get('key',None) == 'W': return render_template('painel.html',pessoas=self.data.GetTableList(), admin=False)
                else: return redirect("/painel.")
            
            else: return redirect("/painel.")


        #painel do usuario
        @routes_pages.route('/user', methods=["GET", "POST"])
        def user(): 
            if request.method == "POST" and session.get('key',None) == 'U':

                form = request.form #formulario
                formulario = {}            

                #-----------------------------verificações para usuarios--------------------------------#

                #verifica se o horario esta correto
                print(form.get('hour_select',type=str))
                retorno = Formate.Hour(form.get('hour_select',type=str))
                if not retorno[0]: return render_template('user.html', error_hour=retorno[1])
                else: formulario['hour'] = retorno[1]

                #verifica se a data esta correta
                retorno = Formate.Date(form.get('date',type=str))
                if not retorno[0]: return render_template('user.html', error_date=retorno[1])
                else: formulario['date'] = retorno[1]

                #verifica a descrição da coleta
                retorno = Check.Coleta(form.get('material',type=str))
                if not retorno[0]: return render_template('user.html', error_coleta=retorno[1])
                else: formulario['coleta'] = retorno[1]
                
                #---------------------------------------------------------------------------------------#

                #atualiza o usuario
                self.data.UpdateUser(session.get('id',None), form.get('endereco',type=str), formulario['hour'], formulario['coleta'], formulario['date'])
                return redirect("/")

            elif request.method == "GET":
                if session.get('key',None) == 'U': 
                    retorno = self.data.GetUserByValue('cpf',session.get('id',None),_get="endereco, horario, material")[0]
                    print(retorno)
                    return render_template('user.html', endereco = retorno[0], hour=retorno[1], material=retorno[2])
                elif session.get('key',None) == None: return redirect("/login")
                else: return redirect("/")


        #rota principal
        @routes_pages.route('/')
        def welcome(): 
            if session.get('key',None) == None:  bar = Formate.TO_LOGIN
            elif session.get('key',None) == 'A' or session.get('key',None) == 'W':
                bar = Formate.INDEX_ADMIN_PAINEL + Formate.LOGED
            else: bar = Formate.USER_PAINEL + Formate.LOGED
            return render_template('index2.html',BARRA_DE_NAVEGACAO=bar)

        #icone do site
        @routes_pages.route('/favicon.ico')
        def icone(): return send_from_directory("./","favicon.ico")


        return routes_pages

    #iniciar o banco de dados
    def __init__(self,_admin=EMAIL_ADMIN ,_senha=PASSWORD_ADMIN):
        self.admin = (_admin, Encode.SHA256(_senha))
        self.ip_ban_list = []
        self.routes = self.create_routes()
        self.data = Database.database(_password=DATABASE_PASSWORD)
        self.data.TryConnect()
        self.data.InitDatabase()