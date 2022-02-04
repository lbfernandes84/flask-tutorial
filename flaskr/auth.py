import functools

# Blueprint é uma forma de organizar views e outros codigos.
# Ao invez de registrar views e codigos diretamente na aplicacao
# ...as mesmas sao agrupadas com Blueprints. Logo esse Blueprint é registrado na aplicacao
# ...quando a mesma for criada na Factory
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#Cria-se um blueprint chamada auth
# Esse objeto Blueprint precisa saber a qual aplicacao pertence,
# ...por isso o nome da aplicacao é passado como segundo parametro
# ...por ultimo, é passado qual o prefixo da url cujas views pertencem
# ...a esse blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

#Associa a funcao register com a url /register. 
# Quando a url /auth/register é chamada é feito um roteamento para essa funcao
# O protocolo http recebe o valor retornado para a funcao e devolve para o navegador
# A funcao aceita tanto os metodos get e post
bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		# O atributo form é uma especializacao de dict que possue pares key/value
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		if not username:# Mensagem de usuario requisitado quando nao vem no request
			error = 'Username is required'
		elif not password:# Mensagem de senha requisitada quando nao vem no request
			erro = 'Pasword is required'

		if error is None:
			try:
				#Caso nada estiver faltando executa-se diretamente um script no banco
				db.execute(
					"INSERT INTO user (username, password) VALUES (?, ?)",
					# Por boas praticas, um password nunca deve ser inserido diretamente no banco
					(username, generate_password_hash(password))
				)
				# Deve ser chamado para persistir os dados no banco
				db.commit()
			except db.IntegrityError:#Erro padrao quando o usuario ja esta registrado, username é UNIQUE
				error = f'User {username} is already registered'
			else:
				#Se tudo certo redireciona para a pagina login
				# Nesse caso url_for roteia para a view relacionada com o blueprint
				# Lembrese que o BluePrint bp agrupa todos as views roteadas de urls com prefixo auth
				return redirect(url_for("auth.login"))
		#flash guarda mensagens que mais tarde serao renderizadas com o template
		flash(error)
	return render_template('auth/register.html')

bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username)
		).fetchone()#Fetchone retorna apenas a primeira linha da query

		if user is None:
			error = 'Incorrect username. '
		#check_password_hash recupera o password que o usuario digitou e compara com o retornado na query
		elif not check_password_hash(user['password'] , password):
			error = 'Incorrect password'
		if error is None:
			# session é um dicionario que guarda informacoes que são compartilhadas entre requsets
			# Nesse caso, quando os dados de login sao validos o id do usuario é mantido na sessao
			# Esse objeto é guardado como cookie no website
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))
		flash(error)
	render_template('auth/login.html')