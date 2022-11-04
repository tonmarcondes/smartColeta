import numpy as np

#mensagens de erro
CPF_ALREADY_EXIST = "O cpf já foi registrado em outra conta, entre em contato com um dos nossos atendentes caso nunca tenha o registrado."
EMAIL_ALREADY_EXIST = "Já existe um conta registrada com esse email, por favor coloque outro email ou logue com a conta já registrada."
CPF_ERROR_MENSAGE = "CPF invalido, verifique se trocou um digito."
EMAIL_INVALID = "O E-Mail solicitado não é valido."
EMAIL_HOST = "Provedor de E-Mail desconhecido."
SHORT_PASSWORD = "A senha deve conter pelo menos 8 caracteres."
LONG_PASSWORD = "A senha pode conter no maximo 64 caracteres."
NOT_NUMBER_PASSWORD = "Sua senha deve conter pelo menos um numero."
NOT_CHAR_PASSWORD = "Sua senha deve conter pelo menos uma letra."
REPEAT_PASSWORD = "A senha digita não corresponde com a anterior."
SERVER_ERROR = "Não foi possivel efetuar o registro por favor tente novante mais tarde."
EMAIL_NOT_EXIST = "O email digitado não está registrado."
INCORRECT_PASSWORD = "A senha digitada está incorreta."
COLETA_LEGTH = "A descrição da coleta não pode ultrapassar 40 caracteres."

validos = ["gmail.com","outlook.com","hotmail.com","yahoo.com","ig.com","terra.com","apple.com","qwerty.com"]


def NotIsDigit(a):return not a.isdigit()


def Email(_email):
    splited = _email.split("@")

    #verifica a formatação do email
    if (len(splited) != 2): return (False,EMAIL_INVALID)
    if (splited[0] == ""): return (False,EMAIL_INVALID)

    #verifica o suporte ao provedor
    if (splited[1] not in validos): return (False,EMAIL_HOST)

    return (True, _email)


def CPF(_cpf):
    #validando o primeiro digito
    cpf_array = np.array(list(_cpf[0:9])).astype(np.int32)
    calculation = cpf_array * [10,9,8,7,6,5,4,3,2]
    calculation = 11 - (np.sum(calculation) % 11)

    if (calculation < 10 and int(_cpf[9]) != calculation): 
        return (False,CPF_ERROR_MENSAGE)
    elif (calculation > 10 and int(_cpf[9]) != 0): 
        return (False,CPF_ERROR_MENSAGE)

    #validando o segundo digito
    cpf_array = np.array(list(_cpf[0:10])).astype(np.int32)
    calculation = cpf_array * [11,10,9,8,7,6,5,4,3,2]
    calculation = 11 - (np.sum(calculation) % 11)

    if (calculation < 10 and int(_cpf[10]) != calculation): 
        return (False,CPF_ERROR_MENSAGE)
    elif (calculation > 10 and int(_cpf[10]) != 0): 
        return (False,CPF_ERROR_MENSAGE)

    return (True,_cpf)


def PasswordForce(_password):
    #verifica o tamanho da senha
    if len(_password) < 8: return (False, SHORT_PASSWORD)
    elif len(_password) > 64: return (False, LONG_PASSWORD)

    #verifica sem contem pelo menos um digito e uma letra
    elif not any(map(str.isdigit, _password)): return (False, NOT_NUMBER_PASSWORD)
    elif not any(map(NotIsDigit, _password)): return (False, NOT_CHAR_PASSWORD)

    return (True, _password)


def Coleta(_coleta):
    if len(_coleta) > 40: return (False, COLETA_LEGTH)
    return (True, _coleta)