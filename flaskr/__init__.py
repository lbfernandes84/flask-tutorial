import os

# contem a aplicacao
from flask import Flask

def create_app(test_config=None):
	print("TESTE APP")
	#cria e configura a aplicacao
	#A aplicacao é uma instancia do objeto Flask
	#O primeiro parametro é o nome da aplicacao. __name__ guarda o nome do diretorio. Pode ser qualquer nome diferente
	#O segundo parametro é opcional e informa que os caminhos dos arquivos de configurações são relativos ao diretorio 
	#...que contem a instancia, tal diretorio fica fora do diretorio da aplicacao

	app = Flask(__name__, instance_relative_config=True)
	# Seta configuracoes na aplicacao
	# o parametro SECRET_KEY serve para manter os dados salvos. Usa-se 'dev'
    #...quando na versao de desenvolvimento mas deve ser substituido quando for para deploy
	# o parametro database define o caminho do banco de dados a ser usado na aplicacao
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
	)
	# Quando o objeto que representa o arquivo de configuração não é passado a aplicacao recebe como 
	# configuracao um arquivo, no caso config.py que fica sob o diretorio de instancia
	if test_config is None:
		app.config.from_pyfile('config.py',silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		# Garante que o diretorio da instancia existe, 
		# pois se caso tal diretorio nao existir o mesmo é criado
		#...esse diretorio é onde instancias do banco de dado são criadas portanto deve sempre existir
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Inicializa a aplicacao
	from . import db
	db.init_app(app)

	# Registra o blueprint de autenticacao
	from . import auth
	print("CHegou")
	app.register_blueprint(auth.bp)

	return app