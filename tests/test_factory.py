from flaskr import create_app


#apenas assegura que o ambiente de teste está sendo configurado
#...quando passado como configuracao para o factory
def test_config():
	assert not create_app().testing
	assert create_app({'TESTING': True}).testing

def test_hello(client):
	response = client.get('/hello')
	assert 'data' not in response