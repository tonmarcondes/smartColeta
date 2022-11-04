import smtplib

class Server():

    def TryConnect(self):
        pass

    def __init__(self, _email="suporte.projetointegradorweb@gmail.com", _password="LRMmY0jl5LH6Bmov", _server="smtp.gmail.com"):
        self.email = _email
        self.password = _password
        self.server_address = _server