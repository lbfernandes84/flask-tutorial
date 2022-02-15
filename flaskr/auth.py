# modulo de programacao funcional do python. Iterage sobre objetos chamaveis (callable)
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
@bp.route('/register', methods=('GET', 'POST'))
def register():
	print("TEST REGISTER")	
	if request.method == 'POST':
		# O atributo form é uma especializacao de dict que possue pares key/value
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		if not username:# Mensagem de usuario requisitado quando nao vem no request
			error = 'Username is required'
		elif not password:# Mensagem de senha requisitada quando nao vem no request
			error = 'Pasword is required'

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
		print(f'Error{error}')
		flash(error)
	return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
	print("TEST LOGIN")	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()#Fetchone retorna apenas a primeira linha da query

		if user is None:
			error = 'Incorrect username. '
		#check_password_hash recupera o password que o usuario digitou e compara com o retornado na query
		elif not check_password_hash(user['password'] , password):
			error = 'Incorrect password'
		if error is None:
			# session é um dicionario que guarda informacoes que são compartilhadas entre requests
			# Nesse caso, quando os dados de login sao validos o id do usuario é mantido na sessao
			# Esse objeto é guardado como cookie no website
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))
		flash(error)
	return render_template('auth/login.html')

#before_app_request executa antes de qualquer view, independente da URL chamada
@bp.before_app_request
def load_logged_in_user():
	#recupera o id do usuario registrado na sessao
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?',(user_id,)
		).fetchone()


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

# O conceito abaixo é complexo quando visto pela primeira vez
# ...a funcao login_required retorna uma funcao decorada com functools.wraps
# ...a funcao wrapped_view decorada com functools.wraps quando chamada faz o seguinte:
# - verifica se o usuario esta ativo
# - Caso negativo direciona o usuario a pagina de login
# - Caso positivo retorna a funcao que é a view "wrapped" com o functools.wraps e os argumentos necessarios

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			#a funcao url_for funciona para chamar a view correspondente ao argumento
			# ...o nome da view é o nome da funcao implementada como wrapped_view
			# ...para views decoradas com blueprints o nome do argumento é o nome do Blueprint.nome_da_view
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view