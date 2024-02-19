from flask import request
from _dados import Conexao

db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


class Parceiro():
    pass


def buscar_parceiro():
    pass


def listar_parceiro():
    db.conectar()
    try:
        query = "SELECT * FROM parceiros"
        resultado = db.executar(query)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def adicionar_parceiro():
    try:
        db.conectar()
        if request.method == 'POST':
            parceiro = request.form['parceiro']
            cep = request.form['cep']
            endereco = request.form['endereco']
            complemento = request.form['complemento']
            bairro = request.form['bairro']
            cidade = request.form['cidade']
            estado = request.form['estado']
            contato = request.form['contato']
            responsavel = request.form['responsavel']
            desconto = request.form['desconto']
            status = request.form['status']
            data = request.form['data']
            detalhes = request.form['detalhes']

            query = "INSERT INTO parceiros (parceiro, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, desconto, detalhes, data, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (parceiro, cep, endereco, complemento, bairro, cidade,
                      estado, contato, responsavel, desconto, detalhes, data, status)

            db.executar(query, values)

            return "Dados inseridos com sucesso!"
        else:
            return "Método Inválido!"

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()
