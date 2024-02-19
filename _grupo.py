from flask import request
from _dados import Conexao

db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


class Grupo():
    pass


def buscar_grupo():
    pass


def listar_grupo():
    db.conectar()
    try:
        query = "SELECT * FROM grupos"
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
