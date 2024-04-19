from flask import request, jsonify
from _dados import Conexao

db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


class Eventos:
    pass


def listar_evento():  # Ok
    db.conectar()
    try:
        query = "SELECT * FROM eventos ORDER BY data_inicio"
        resultado = db.executar(query)
        return resultado
    except Exception as e:
        return f"Erro: {str(e)}"
    finally:
        if db.conexao is not None:
            db.desconectar()


def buscar_evento_id(id):
    db.conectar()
    try:
        query = "SELECT * FROM eventos WHERE id_evento = %s"
        values = (id,)
        resultado = db.executar(query, values)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def cadastrar_evento():  # Ok
    db.conectar()
    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            localizacao = request.form['localizacao']

            query = "INSERT INTO eventos (titulo, descricao, data_inicio, data_fim, localizacao) VALUES (%s, %s, %s, %s, %s)"

            values = (titulo, descricao, data_inicio, data_fim, localizacao)

            db.executar(query, values)

            return "Evento cadastrado com sucesso!"

    except Exception as e:
        return f"Erro ao adicionar parceiro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def atualizar_evento(id, dados):
    try:
        db.conectar()
        titulo = dados['titulo']
        descricao = dados['descricao']
        data_inicio = dados['data_inicio']
        data_fim = dados['data_fim']
        localizacao = dados['localizacao']

        query = """
        UPDATE eventos
        SET titulo=%s, descricao=%s, data_inicio=%s, data_fim=%s, localizacao=%s
        WHERE id_evento = %s
        """

        values = (titulo, descricao, data_inicio, data_fim, localizacao, id)

        db.executar(query, values)

        return "Evento atualizado com sucesso!"

    except Exception as e:
        return f"Erro ao atualizar evento: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()
