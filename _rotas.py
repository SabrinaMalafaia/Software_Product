from flask import Flask, render_template, request, jsonify, redirect
from flask_mail import Mail, Message
from _dados import Conexao
import _contato
import _grupo
import _parceiro
import requests

app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server
app.config['MAIL_PORT'] = 587  # Porta SMTP
app.config['MAIL_USE_TLS'] = True  # TLS para segurança
# cleoalves.p.e@gmail.com
app.config['MAIL_USERNAME'] = 'rpa.malafaia@gmail.com'
app.config['MAIL_PASSWORD'] = 'kxsw zyza mmjy atsm'
# contato@alemdopedal.com
app.config['MAIL_DEFAULT_SENDER'] = 'rpa.malafaia@gmail.com'

mail = Mail(app)

# DEPÓSITO DE DADOS ##############
db = Conexao(host="localhost", port="3306", user="root",
             password="root", database="V2")


# INDEX ##############
@app.route('/', methods=['GET'])   # OK
def home():
    return render_template("_index.html")


# SOBRE ##############
@app.route('/sobre', methods=['GET'])   # OK
def sobre():
    return render_template("_sobre.html")


# OBJETIVO ##############
@app.route('/objetivo', methods=['GET'])   # OK
def objetivo():
    return render_template("_objetivo.html")


# PARCEIROS ##############
@app.route('/parceiro', methods=['GET'])  # OK
def parceiro():
    return render_template("_parceiro.html")


@app.route('/buscar_parceiro', methods=['GET'])  # OK
def buscar_parceiro():
    return render_template("_buscarParceiro.html")


@app.route('/resultado_parceiro', methods=['GET'])  # OK
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


@app.route('/editar_parceiro/<id>', methods=['GET', 'POST'])
def editar_parceiro(id):
    parceiro = _parceiro.buscar_parceiro_id(id)

    if request.method == 'POST':
        dados = {
            'parceiro': request.form['parceiro'],
            'cep': request.form['cep'],
            'endereco': request.form['endereco'],
            'complemento': request.form['complemento'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'contato': request.form['contato'],
            'responsavel': request.form['responsavel'],
            'desconto': request.form['desconto'],
            'status': request.form['status'],
            'data': request.form['data'],
            'detalhes': request.form['detalhes']
        }

        _parceiro.atualizar_parceiro(id, dados)

        return redirect('/')

    return render_template('_editarParceiro.html', parceiro=parceiro)


# GRUPOS ##############
@app.route('/grupo', methods=['GET'])  # OK
def grupo():
    return render_template("_grupo.html")


@app.route('/buscar_grupo', methods=['GET'])  # OK
def buscar_grupo():
    return render_template("_buscarGrupo.html")


@app.route('/resultado_grupo', methods=['GET'])  # OK
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


@app.route('/editar_grupo/<id>', methods=['GET', 'POST'])
def editar_grupo(id):
    grupo = _grupo.buscar_grupo_id(id)

    if request.method == 'POST':
        dados = {
            'grupo': request.form['grupo'],
            'cep': request.form['cep'],
            'endereco': request.form['endereco'],
            'complemento': request.form['complemento'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'contato': request.form['contato'],
            'responsavel': request.form['responsavel'],
            'status': request.form['status'],
            'data': request.form['data'],
            'detalhes': request.form['detalhes']
        }

        _grupo.atualizar_grupo(id, dados)

        return redirect('/')

    return render_template('_editargrupo.html', grupo=grupo)


# CONTATO ##############
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        resposta = _contato.enviar_email_contato()
        return redirect('/')
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


# ERRO ##############
@app.errorhandler(404)
def erro404(e):  # Erro
    return render_template('_erro.html'), 404


# RUN ##############
if __name__ == '__main__':
    app.run(debug=True)

# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
