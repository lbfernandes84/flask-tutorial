import sqlite3

import click

# g é um objeto especial que é único pra cada requisicao
# ... é usado para guardar informações que podem ser acessadas
# ... por multiplas funcoes durante uma requisicao
# ... no caso esse objeto é usado para guardar uma referencia ao banco de dados (db)
# ...g é uma contração de global
from flask import g

# current_app é tambem um objeto especial que aponta para a aplicacao flask que esta manipulando a conexão
# ...como utilizamos uma factory para criar a aplicacao no arquivo __init__
from flask import current_app
from flask.cli import with_appcontext

def get_db():
	if 'db' not in g:
		# Estabelece a conexão com o banco de dados,
		# ...o primeiro parametro é a string de conexao que no caso esta mantida no objeto de configuracao da aplicacao
		# ...o segundo parametro é utilizado para configurar como a conexao deve ser feita, é parte da API do sqlite3
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types = sqlite3.PARSE_DECLTYPES
		)
		# sqlite.Row informa a conexão que dados serao retornados como dicionarios
		# exemplo em uma tabela Pessoa com as colunas nome e idade com os valores: Lucas 37
		# sera retornado {"Nome":"Lucas": , "idade":37}
		g.db.row_factory = sqlite3.Row
	return g.db

#Essa funcao funciona como esperado, quando a requisicao deseja fechar a conexao com o banco
# ...verifica se existe objeto de banco de dados e se caso positivo fecha a conexao
def close_db(e=None):
	a =1
	db = g.pop("db", None)
	if db is not None:
		db.close()

def init_db():
	db = get_db()

	# current_app.open_resource abre um arquivo que é relativo ao pacote da instalacao
	# ...é muito util pois o caminho do arquivo pode mudar de acordo com a versao que estamos rodando
	# ...por exemplo se fosse a versao de producao poderia estar em um local diferente
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf-8'))#executa os comandos sql contidos no arquivo

@click.command('init-db')# define a linha de comando init-db que chama a funcao init_db
@with_appcontext
def init_db_command():
	init_db()
	click.echo("Initializing database...")

# As funcoes close_db e init_db_command precisam ser registradas com o objeto de aplicacao flask
# A funcao abaixo é colocada na Factory da aplicacao que a inicia com o que é necessario
def init_app(app):
	app.teardown_appcontext(close_db)#informa a aplicacao uma funcao a ser chamada quando for encerrada
	app.cli.add_command(init_db_command)#cria um comando para ser chamado com o flask