import sqlite3

import pytest
from flaskr.db import get_db

def test_singleton_get_db(app):
	#Garante que a funcao get_db retorna sempre o mesmo objeto (singleton)
	with app.app_context():
		db = get_db()
		assert db is get_db()

	#Garante que o objeto retornado é um ADO do sqlite3
	with pytest.raises(sqlite3.ProgrammingError) as e:
		db.execute('SELECT 1')

	#Se é um ADO a mensagem de erro ao executar um SQL invalido possui a palavra closed
	assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):

	class Recorder(object):
		called = False

	def fake_init_db():
		Recorder.called = True

	monkeypatch.settattr('flaskr.db.initi_db', fake_init_db)
	result = 