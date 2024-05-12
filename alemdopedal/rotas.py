# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
from alemdopedal import app
from flask import render_template, request, redirect, jsonify, url_for
from alemdopedal.dados import Conexao
from alemdopedal.parceiro import Parceiro
from alemdopedal.grupo import Grupo
from alemdopedal.evento import Evento
from alemdopedal.contato import enviar_email_contato
import requests

# DEPÓSITO DE DADOS ##############
db = Conexao("bd", "3306", "root", "root", "V2")
# db = Conexao("localhost", "3307", "root", "root", "V2")


# INDEX ##############
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


# SOBRE ##############
@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template("sobre.html")


# OBJETIVO ##############
@app.route('/objetivo', methods=['GET'])
def objetivo():
    return render_template("objetivo.html")


# PARCEIROS ##############
@app.route('/parceiro', methods=['GET'])
def parceiro():
    return render_template("parceiro.html")


@app.route('/buscar_parceiro', methods=['GET'])
def buscar_parceiro():
    resultado = Parceiro.listar_parceiro()
    return render_template("parceiro_buscar.html", resultado=resultado)


@app.route('/filtro_parceiro', methods=['GET'])
def filtro_parceiro():
    parceiro = request.args.get('parceiro')
    resultado = Parceiro.buscar_parceiro(parceiro)
    return render_template('parceiro_buscar.html', resultado=resultado)


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
        Parceiro.adicionar_parceiro(parceiro)
        return redirect(url_for('home'))
    return render_template("parceiro_cadastrar.html")


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

        return redirect(url_for('home'))

    return render_template('parceiro_editar.html', parceiro=parceiro)


# GRUPOS ##############
@app.route('/grupo', methods=['GET'])
def grupo():
    return render_template("grupo.html")


@app.route('/buscar_grupo', methods=['GET'])
def buscar_grupo():
    resultado = Grupo.listar_grupo()
    return render_template('grupo_buscar.html', resultado=resultado)


@app.route('/filtro_grupo', methods=['GET'])
def filtro_grupo():
    grupo = request.args.get('grupo')
    resultado = Grupo.buscar_grupo(grupo)
    return render_template('grupo_buscar.html', resultado=resultado)


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
        Grupo.adicionar_grupo(grupo)
        return redirect(url_for('home'))
    return render_template("grupo_cadastrar.html")


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

        return redirect(url_for('home'))

    return render_template('grupo_editar.html', grupo=grupo)


# EVENTOS ##############
@app.route('/eventos', methods=['GET'])
def eventos():
    resultado = Evento.listar_evento()
    return render_template("evento.html", eventos=resultado)


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

    return render_template('evento.html', eventos=eventos)


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

        return redirect(url_for('home'))

    return render_template("evento_cadastrar.html")


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

        return redirect(url_for('eventos'))

    return render_template('evento_editar.html', evento=evento)


@app.route('/apagar_evento/<int:id>', methods=['POST', 'GET'])
def apagar_evento(id):
    evento = Evento.buscar_evento_id(id)
    if isinstance(evento, Evento):
        evento.excluir_evento()
        return redirect(url_for('eventos'))
    else:
        return evento, 404


# CONTATO ##############
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        enviar_email_contato()
        return redirect(url_for('home'))
    return render_template("contato.html")


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
        return render_template('login.html')


# ERRO ##############
@app.errorhandler(404)
def erro404(e):  # Erro
    return render_template('erro.html'), 404


# TESTE ##############
@app.route('/teste', methods=['GET'])
def teste():
    return render_template("teste.html")
