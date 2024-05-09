from flask import Flask, render_template, request, jsonify, redirect
from flask_mail import Mail
from _dados import Conexao
import _contato
from _grupo import Grupo
from _parceiro import Parceiro
from _evento import Evento
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
db = Conexao("db", "3306", "root", "root", "V2")

# db = Conexao("localhost", "3307", "root", "root", "V2")


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
@app.route('/parceiro', methods=['GET'])
def parceiro():
    return render_template("_parceiro.html")


@app.route('/buscar_parceiro', methods=['GET'])
def buscar_parceiro():
    return render_template("_buscarParceiro.html")


@app.route('/resultado_parceiro', methods=['GET'])
def resultado_parceiro():
    parceiro = request.args.get('parceiro')
    resultado = Parceiro.buscar_parceiro(parceiro)
    return render_template('_buscarParceiro.html', resultado=resultado)


@app.route('/listar_parceiro', methods=['GET'])
def listar_parceiro():
    resultado = Parceiro.listar_parceiro()
    return render_template("_listarParceiros.html", parceiros=resultado)


@app.route('/cadastrar_parceiro', methods=['GET', 'POST'])
def cadastrar_parceiro():
    if request.method == 'POST':
        parceiro = Parceiro(
            request.form['parceiro'],
            request.form['cep'],
            request.form['endereco'],
            request.form['complemento'],
            request.form['bairro'],
            request.form['cidade'],
            request.form['estado'],
            request.form['contato'],
            request.form['responsavel'],
            request.form['desconto'],
            request.form['status'],
            request.form['data'],
            request.form['detalhes']
        )
        Parceiro.adicionar_parceiro()
        return redirect('/')
    return render_template("_cadastrarParceiro.html")


@app.route('/editar_parceiro/<id>', methods=['GET', 'POST'])
def editar_parceiro(id):
    parceiro = Parceiro.buscar_parceiro_id(id)

    if request.method == 'POST':
        dados = {
            'id_parceiro': id,
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

        Parceiro.editar_parceiro(dados)

        return redirect('/')

    return render_template('_editarParceiro.html', parceiro=parceiro)


# GRUPOS ##############
@app.route('/grupo', methods=['GET'])
def grupo():
    return render_template("_grupo.html")


@app.route('/buscar_grupo', methods=['GET'])
def buscar_grupo():
    return render_template("_buscarGrupo.html")


@app.route('/resultado_grupo', methods=['GET'])
def resultado_grupo():
    grupo = request.args.get('grupo')
    resultado = Grupo.buscar_grupo(grupo)
    return render_template('_buscarGrupo.html', resultado=resultado)


@app.route('/listar_grupo', methods=['GET'])
def listar_grupo():
    resultado = Grupo.listar_grupo()
    return render_template('_listarGrupos.html', grupos=resultado)


@app.route('/cadastrar_grupo', methods=['GET', 'POST'])
def cadastrar_grupo():
    if request.method == 'POST':
        grupo = Grupo(
            request.form['grupo'],
            request.form['cep'],
            request.form['endereco'],
            request.form['complemento'],
            request.form['bairro'],
            request.form['cidade'],
            request.form['estado'],
            request.form['contato'],
            request.form['responsavel'],
            request.form['status'],
            request.form['data'],
            request.form['detalhes']
        )
        grupo.adicionar_grupo()
        return redirect('/')
    return render_template("_cadastrarGrupo.html")


@app.route('/editar_grupo/<id>', methods=['GET', 'POST'])
def editar_grupo(id):
    grupo = Grupo.buscar_grupo_id(id)

    if request.method == 'POST':
        dados = {
            'id_grupo': id,
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

        Grupo.editar_grupo(dados)

        return redirect('/')

    return render_template('_editarGrupo.html', grupo=grupo)


# EVENTOS ##############
@app.route('/eventos', methods=['GET'])
def eventos():
    resultado = Evento.listar_evento()
    return render_template("_evento.html", eventos=resultado)


@app.route('/filtrar_eventos', methods=['GET'])
def filtrar_eventos():
    estado = request.args.get('estado')
    if estado == "ALL":
        eventos = Evento.listar_evento()
    else:
        estado = "%" + estado
        db.conectar()
        query = "SELECT * FROM eventos WHERE localizacao LIKE %s"
        values = (estado,)
        eventos = db.executar(query, values)

    return render_template('_evento.html', eventos=eventos)


@app.route('/cadastrar_evento', methods=['GET', 'POST'])
def cadastrar_evento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        localizacao = request.form['localizacao']

        novo_evento = Evento(
            titulo, descricao, data_inicio, data_fim, localizacao)

        novo_evento.cadastrar_evento()

        return render_template("_index.html")

    return render_template("_cadastrarEvento.html")


@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    evento = Evento.buscar_evento_id(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        localizacao = request.form['localizacao']

        evento_editado = Evento(
            titulo, descricao, data_inicio, data_fim, localizacao)

        evento_editado.definir_id(id)

        evento_editado.editar_evento()

        return redirect('/eventos')

    return render_template('_editarEvento.html', evento=evento)


@app.route('/apagar_evento/<int:id>', methods=['POST', 'GET'])
def apagar_evento(id):
    evento = Evento.buscar_evento_id(id)
    if isinstance(evento, Evento):
        evento.excluir_evento()
        return redirect('/eventos')
    else:
        return evento, 404


# CONTATO ##############
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        _contato.enviar_email_contato()
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de verificação de login
        return 'Login bem-sucedido!'
    else:
        return render_template('_login.html')


# ERRO ##############
@app.errorhandler(404)
def erro404(e):  # Erro
    return render_template('_erro.html'), 404


# RUN ##############
if __name__ == '__main__':
    app.run(debug=True)

# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
