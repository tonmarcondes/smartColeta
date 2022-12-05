from datetime import datetime, timedelta

#html
TO_LOGIN = "<li class=\"nav-button\"><a href=\"/login\"  class=\"btn btn-outline-success\">ENTRAR</a></li> <li class=\"nav-button\"><a href=\"/register\" class=\"btn btn-outline-success\">REGISTRAR</a></li>"
LOGED = "<li class=\"nav-button\"><a href=\"/logout\" class=\"btn btn-dark btn-block btn-lg\">SAIR</a></li>"
USER_PAINEL = "<li class=\"nav-button\"><a href=\"/user\">USUÁRIO</a></li>"
INDEX_ADMIN_PAINEL = "<li class=\"nav-button\"><a href=\"/painel\" class=\"btn btn-outline-dark\">PAINEL</a></li>"
PAINEL_REGISTER_BUTTON = "<li class=\"nav-button\"><a href=\"/register\" class=\"btn btn-outline-dark btn-block btn-lg\"  data-bs-toggle=\"tooltip\" data-bs-title=\"Cadastro de usuário\">USUÁRIO</a></li>"
ADMIN_REGISTER_CHECK = "<div style=\"display:flex;\"><input class=\"form-check-input\" style= \"padding: 10px;\" type=\"checkbox\" id=\"worker\" name=\"worker\" value=\"worker\" aria-label=\"...\"/> <div style=\"text-align: center; padding:2px\"> Funcionário</div></div>"

#mensagens de erro
DATE_FORMAT = "O formato da data passado está incorreto."
EARLY_DATE = "Só aceitamos pedidos 3 dias após a data de solicitação."
CPF_CARACTER = "CPF invalido, o cpf não pode conter letras ou caracters especias."
CPF_LENGTH = "CPF invalido, verifique se não esqueceu algum digito."
HOUR_FORMAT = "Formato Invalido."


#verifica o formato do cpf
def CPF(_cpf):
    #remove caracteres especiais
    cpf = _cpf.replace(".","").replace("-","")

    #verifica se não pussui letras ou caracters
    if not cpf.isdigit(): return (False, CPF_CARACTER)

    #verifica se a quantidade de numeros esta correta
    if (len(cpf) != 11): return (False, CPF_LENGTH)

    return (True, cpf)


#formatar o horario
def Hour(_hour):
    formated = _hour.split(":")[0]

    #verifica o tamanho do numero
    if len(formated) > 2: return (False, HOUR_FORMAT)
    elif len(formated) == 0: return (False, HOUR_FORMAT)

    #verifica se é um digito
    if not formated.isdigit: return (False, HOUR_FORMAT)

    formated = int(formated)

    #verifica se um dos horarios disponiveis
    if formated > 18: return (False, HOUR_FORMAT)
    elif formated < 7: return (False, HOUR_FORMAT)

    return (True, formated)


#ano-mes-dia
def Date(_date):
    accept = datetime.today() + timedelta(days=3) 

    #converte a string
    try: chosen = datetime.strptime(_date, '%Y-%m-%d')
    except: return (False, DATE_FORMAT)

    #verifica se a data esta muito cedo
    if chosen < accept: return (False, EARLY_DATE)

    #corrige a formatação
    date = chosen.strftime("%d/%m/%Y")

    return (True, date)