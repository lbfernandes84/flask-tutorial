from flask import (
	Blueprint, flash,g , redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

#Esse blueprint não tem uma pagina de prefixo
# Logo apos o registro do blueprint na fabrica da aplicacao (__init__.py) é chamada a funcao app_add_url_rule('/')
# Que roteia as requests para a view index
bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT p.id, title, body, created, author_id, username'
		' FROM post p JOIN user u ON author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html',posts = posts)

@bp.route('/create', methods=("GET", "POST"))
@login_required
def create():
	if request.method == 'POST'
		title = request.form['title']
		body = request.form['body']
		error = None
		if not title:
			error = 'Title is required'
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (title, body, author_id)'
				'VALUES (?, ?, ?)'
				(title,body, g.user['id'])
			)
			db.commit()
			return redirect(url_for('blog.index'))
	return render_template('blog/create.html')

def get_post(id, check_author=True):
	post = get_db().execute(
		'SELECT p.id, title, body, created, author_id, username'
		'FROM post p JOIN user u ON p.author_id = u.id'
		'WHERE p.id = ?'
		(id,)
	).fetchone()

	if post is None:
		# abort lança uma exceção que retorna um status HTTP
		# 404 significa pagina nao encontrada
		abort(404, f"Post id {id} does not exist.")
	
	if check_author and post['author_id'] != g.user['id']
		# 403 significa nao autorizado
		abort(403)

@bp.route('/<int:id>/update', methods=("GET", "POST"))
@login_required
def update(id):
	post = get_post(id)

	if request.method = 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = 'Title is required'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE post SET title = ? , body = ?'
				'WHERE id = ?'
				(title, body, id)
			)
			db.commit()
			return redirect(url_for('blog.index'))
	render_template('blog/update.html', post=post)