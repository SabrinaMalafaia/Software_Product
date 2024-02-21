from flask import Flask, render_template, request, jsonify
from _dados import Conexao
import _grupo
import _parceiro
import requests

app = Flask(__name__)

# DEPÓSITO DE DADOS ##############
db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


# INDEX ##############
@app.route('/', methods=['GET'])
def home():
    return render_template("_index.html")


# SOBRE ##############
@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template("_sobre.html")


# OBJETIVO ##############
@app.route('/objetivo', methods=['GET'])
def objetivo():
    return render_template("_objetivo.html")


# PARCEIROS ##############
@app.route('/parceiro', methods=['GET'])  # OK
def parceiro():
    return render_template("_parceiro.html")


@app.route('/buscar_parceiro', methods=['GET'])
def buscar_parceiro():
    return render_template("_buscarParceiro.html")


@app.route('/resultado_parceiro', methods=['GET'])
def resultado_parceiro():
    parceiro = request.args.get('parceiro')
    resultado = _parceiro.buscar_parceiro(parceiro)
    return render_template('_buscarParceiro.html', resultado=resultado)


@app.route('/listar_parceiro', methods=['GET'])  # OK
def listar_parceiro():
    resultado = _parceiro.listar_parceiro()
    return render_template("_listarParceiros.html", parceiros=resultado)


@app.route('/cadastrar_parceiro', methods=['GET', 'POST'])  # OK
def cadastrar_parceiro():
    if request.method == 'POST':
        resposta = _parceiro.adicionar_parceiro()
        return render_template("_index.html", re=resposta)
    return render_template("_cadastrarParceiro.html")


# GRUPOS ##############
@app.route('/grupo', methods=['GET'])  # OK
def grupo():
    return render_template("_grupo.html")


@app.route('/buscar_grupo', methods=['GET'])
def buscar_grupo():
    return render_template("_buscarGrupo.html")


@app.route('/resultado_grupo', methods=['GET'])
def resultado_grupo():
    grupo = request.args.get('grupo')
    resultado = _grupo.buscar_grupo(grupo)
    return render_template('_buscarGrupo.html', resultado=resultado)


@app.route('/listar_grupo', methods=['GET'])  # OK
def listar_grupo():
    resultado = _grupo.listar_grupo()
    return render_template('_listarGrupos.html', grupos=resultado)


@app.route('/cadastrar_grupo', methods=['GET', 'POST'])  # OK
def cadastrar_grupo():
    if request.method == 'POST':
        resposta = _grupo.adicionar_grupo()
        return render_template("_index.html")
    return render_template("_cadastrarGrupo.html")


# CONTATO ##############
@app.route('/contato', methods=['GET'])
def contato():
    return render_template("_contato.html")


# CEP ##############
@app.route('/buscar_cep', methods=['POST'])
def buscar_cep():
    cep = request.form['cep']
    url = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)


# LOGIN ##############
@app.route('/login', methods=['GET'])  # Rota que exibe a tela de Login
def entrar():
    return render_template('_login.html')


# RUN ##############
if __name__ == '__main__':
    app.run(debug=True)

# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
