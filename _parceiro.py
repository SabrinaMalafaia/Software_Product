from flask import request
from _dados import Conexao

db = Conexao(host="localhost", port="3307", user="root",
             password="root", database="V2")


class Parceiro:
    pass


def buscar_parceiro_id(id):
    db.conectar()
    try:
        query = "SELECT * FROM parceiros WHERE id_parceiro = %s"
        values = (id,)
        resultado = db.executar(query, values)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def buscar_parceiro(parceiro):
    db.conectar()
    try:
        query = "SELECT * FROM parceiros WHERE parceiro LIKE %s"
        values = ('%' + parceiro + '%',)
        resultado = db.executar(query, values)
        return resultado

    except Exception as e:
        return f"Erro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


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

            if not complemento:
                complemento = None

            query = "INSERT INTO parceiros (parceiro, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, desconto, detalhes, data, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            values = (parceiro, cep, endereco, complemento, bairro, cidade,
                      estado, contato, responsavel, desconto, detalhes, data, status)

            db.executar(query, values)

            return "Dados inseridos com sucesso!"

    except Exception as e:
        return f"Erro ao adicionar parceiro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()


def atualizar_parceiro(id, dados):
    try:
        db.conectar()
        parceiro = dados['parceiro']
        cep = dados['cep']
        endereco = dados['endereco']
        complemento = dados['complemento']
        bairro = dados['bairro']
        cidade = dados['cidade']
        estado = dados['estado']
        contato = dados['contato']
        responsavel = dados['responsavel']
        desconto = dados['desconto']
        status = dados['status']
        data = dados['data']
        detalhes = dados['detalhes']

        if not complemento:
            complemento = None

        query = """
        UPDATE parceiros
        SET parceiro=%s, cep=%s, endereco=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, contato=%s, responsavel=%s, desconto=%s, detalhes=%s, data=%s, status=%s
        WHERE id_parceiro = %s
        """

        values = (parceiro, cep, endereco, complemento, bairro, cidade,
                  estado, contato, responsavel, desconto, detalhes, data, status, id)

        db.executar(query, values)

        return "Parceiro atualizado com sucesso!"

    except Exception as e:
        return f"Erro ao atualizar parceiro: {str(e)}"

    finally:
        if db.conexao is not None:
            db.desconectar()
