import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
	_data_sql = f.read().decode('utf-8')

#Fixtures sao como os antigos SetUp nos testes de unidade no Python
@pytest.fixture
def app()
	# registra e cria um diretorio temporario
	db_fd, db_path = tempfile.mkstemp()

	# chama o factory da aplicacao passando um mapa com o caminho temporario para criar o banco de dados
	app = create_app({
		'TESTING': True# Essa flag modifica alguns comportamentos da aplicacao para que seja mais simples testa-la
		'DATABASE': db_path
		})

	with app.app_context():
		#cria um banco no diretorio temporario
		init_db()
		# Executa o script sql para testes
		get_db().executescript(_data_sql)

	yield app

	os.close(db_fd)
	os.unlink(db_path)

@pytest.fixture
def client(app):
	#Ao chamar o methodo abaixxo a aplicacao permite receber requests sem que um servidor esteja rodando
	return app.test_client()

@pytest.fixture
def runner(app):
	#permite chamar linhas de comando registradas com a aplicacao
	#...como a criada no modulo db.py para iniciar o banco de dados criando as tabelas
	return app.test_cli_runner()