from setuptools import find_packages, setup

setup(
	name='flaskr',
	version='1.0.0',
	packages=find_packages(),
	# Esse parametro diz para o empacotador que outros dados serao inclusos
	# Tais dados precisam ser inseridos em um arquivo na mesma localizacao do setup.py
	# ...deve se chamar MANIFEST.in
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'flaskr',
	],
)

# O conteudo do arquivo MANIFEST.in é o seguinte:
# include flask/schema.sql
# graft flaskr/static
# graft flaskr/templates
# global-exclude *.pyc
# Logo na instalacao sera adicionado o schema para criar o banco
# os arquivos dentro das pastas static e templates
# arquivos pyc serao ignorados