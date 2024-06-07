# para comentar o código no vscode é só selecionar o que quer comentar e prescionar ctrl+;
from app import app, mail
import os
from flask import render_template, request, redirect, jsonify, url_for, flash, session, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from app.dados import Conexao
from app.parceiro import Parceiro
from app.grupo import Grupo
from app.evento import Evento
from app.contato import enviar_email_contato, enviar_email_senha
import requests
import mysql.connector


# DEPÓSITO DE DADOS ##############
# db = Conexao("bd", "3306", "root", "root", "V2")
db = Conexao("localhost", "3307", "root", "root", "V2")

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

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
    if resultado:
        return render_template('parceiro_buscar.html', resultado=resultado)
    else:
        flash('Não há!', 'warning')
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
        flash('Parceiro cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_parceiro'))
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
    if resultado:
        return render_template('grupo_buscar.html', resultado=resultado)
    else:
        flash('Não há!', 'warning')
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
        flash('Grupo cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_grupo'))
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

        flash('Evento criado com sucesso!', 'success')

        return redirect(url_for('cadastrar_evento'))

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
        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('contato'))

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
@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email and password:
            senha_hash = generate_password_hash(password)
            foto_padrao = 'default.jpg'

            db.conectar()

            resultado = db.executar(
                "SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))

            if resultado[0][0] > 0:
                flash('E-mail já cadastrado!', 'danger')
            else:
                try:
                    resultado = db.executar("INSERT INTO usuarios (nome, email, senha, foto_perfil) VALUES (%s, %s, %s, %s)",
                                            (username, email, senha_hash, foto_padrao))

                    db.desconectar()

                    flash('Conta criada com sucesso!', 'success')
                    return redirect(url_for('login'))

                except mysql.connector.Error as erro:
                    flash(f'Ocorreu um erro: {erro}', 'danger')
        else:
            flash('Todos os campos devem ser preenchidos!', 'danger')

    return render_template('criar_conta.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginEmail = request.form.get('loginEmail')
        loginSenha = request.form.get('loginSenha')

        db.conectar()

        query = "SELECT * FROM usuarios WHERE email = %s"
        resposta = db.executar(query, (loginEmail,))

        if resposta:
            user = resposta[0]
            senha_hash = user[3]
            if check_password_hash(senha_hash, loginSenha):
                session['email'] = user[2]
                db.desconectar()
                return redirect(url_for('perfil'))

        db.desconectar()
        flash('E-mail ou senha inválidos!', 'danger')

    return render_template('login.html')


@app.route('/perfil')
def perfil():
    if 'email' in session:
        loginEmail = session['email']

        db.conectar()

        query = "SELECT * FROM usuarios WHERE email = %s"
        resposta = db.executar(query, (loginEmail,))

        if resposta:
            user = resposta[0]
            db.desconectar()
            return render_template('perfil.html', user=user)
        else:
            db.desconectar()
            flash('Usuário não encontrado!', 'danger')
    else:
        return redirect(url_for('login'))


@app.route('/mudar_foto', methods=['GET', 'POST'])
def mudar_foto():
    if 'email' in session:
        loginEmail = session['email']

        if 'foto_perfil' in request.files:
            imagem = request.files['foto_perfil']
            if imagem.filename != '':
                caminho = os.path.join(
                    current_app.root_path, 'static/perfil_fotos', imagem.filename)
                imagem.save(caminho)

                db.conectar()
                query = "UPDATE usuarios SET foto_perfil = %s WHERE email = %s"
                db.executar(query, (imagem.filename, loginEmail))
                db.desconectar()

                flash('Imagem de perfil atualizada com sucesso!', 'success')
                return redirect(url_for('perfil'))

        flash('Nenhuma imagem selecionada!', 'danger')
        return redirect(url_for('perfil'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


# SENHA ##############
@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']

        db.conectar()
        user = db.executar('SELECT * FROM usuarios WHERE email = %s', (email,))
        db.desconectar()

        if user:
            token = serializer.dumps(email, salt='recovery-salt')
            link = url_for('redefinir_senha', token=token, _external=True)

            enviar_email_senha(email, 'Redefinição de Senha',
                               f'Clique no link para redefinir sua senha: {link}')
            flash(
                'Um e-mail foi enviado com instruções para redefinir a sua senha.', 'success')
        else:
            flash('E-mail não encontrado.', 'warning')

        return redirect(url_for('esqueci_senha'))

    return render_template('senha_esqueci.html')


@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    try:
        email = serializer.loads(token, salt='recovery-salt', max_age=3600)
    except SignatureExpired:
        flash('Link expirado!', 'warning')
        return redirect(url_for('esqueci_senha'))

    if request.method == 'POST':
        nova_senha = request.form['senha']
        senha_hash = generate_password_hash(nova_senha)
        db.conectar()
        db.executar('UPDATE usuarios SET senha=%s WHERE email=%s',
                    (senha_hash, email))
        db.desconectar()

        flash('Sua senha foi alterada com sucesso!', 'success')

        return redirect(url_for('login'))

    return render_template('senha_redefinir.html', token=token)


# ERRO ##############
@app.errorhandler(404)
def erro404(e):
    return render_template('erro.html'), 404


# TESTE ##############
@app.route('/teste', methods=['GET'])
def teste():
    return render_template("teste.html")
