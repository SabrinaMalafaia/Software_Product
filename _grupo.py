from flask import request
from _dados import Conexao

db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


class Grupo():
    pass


def buscar_grupo_id(id):
    db.conectar()
    try:
        query = "SELECT * FROM grupos WHERE id_grupo = %s"
        values = (id,)
        resultado = db.executar(query, values)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def buscar_grupo(grupo):
    db.conectar()
    try:
        query = "SELECT * FROM grupos WHERE grupo LIKE %s"
        values = ('%' + grupo + '%',)
        resultado = db.executar(query, values)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def listar_grupo():
    db.conectar()
    try:
        query = "SELECT * FROM grupos WHERE status = '1'"
        resultado = db.executar(query)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def adicionar_grupo():
    try:
        db.conectar()
        if request.method == 'POST':
            grupo = request.form['grupo']
            cep = request.form['cep']
            endereco = request.form['endereco']
            complemento = request.form['complemento']
            bairro = request.form['bairro']
            cidade = request.form['cidade']
            estado = request.form['estado']
            contato = request.form['contato']
            responsavel = request.form['responsavel']
            status = request.form['status']
            data = request.form['data']
            detalhes = request.form['detalhes']

            if complemento == "":
                complemento = None

            query = "INSERT INTO grupos (grupo, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, detalhes, data, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (grupo, cep, endereco, complemento, bairro, cidade,
                      estado, contato, responsavel, detalhes, data, status)

            db.executar(query, values)

            return "Dados inseridos com sucesso!"
        else:
            return "Método Inválido!"

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def atualizar_grupo(id, dados):
    try:
        db.conectar()
        grupo = dados['grupo']
        cep = dados['cep']
        endereco = dados['endereco']
        complemento = dados['complemento']
        bairro = dados['bairro']
        cidade = dados['cidade']
        estado = dados['estado']
        contato = dados['contato']
        responsavel = dados['responsavel']
        status = dados['status']
        data = dados['data']
        detalhes = dados['detalhes']

        if not complemento:
            complemento = None

        query = """
        UPDATE grupos
        SET grupo=%s, cep=%s, endereco=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, contato=%s, responsavel=%s, detalhes=%s, data=%s, status=%s
        WHERE id_grupo = %s
        """

        values = (grupo, cep, endereco, complemento, bairro, cidade,
                  estado, contato, responsavel, detalhes, data, status, id)

        db.executar(query, values)

        return "Grupo atualizado com sucesso!"

    except Exception as e:
        return f"Erro ao atualizar grupo: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()
