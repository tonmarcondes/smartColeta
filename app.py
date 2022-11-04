from flask import Flask
from libs.routes import Routes
from flask_session import Session

# criando aplicação e registrando as bibliotecas
app = Flask(__name__, template_folder = 'html')
app.register_blueprint(Routes().routes)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == '__main__': app.run()