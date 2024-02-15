from flask import request, jsonify
from db import Conexao

cone = Conexao()

def criarTabelaLogin():
    try:
        cone.conectar()
        criar_tabela_login = """CREATE TABLE IF NOT EXISTS Grupos (
            id_grupo INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            grupo VARCHAR(100) NOT NULL,    
            endereco VARCHAR(255) NOT NULL,
            estado CHAR(2) NOT NULL,
            contato VARCHAR(255) NOT NULL,
            responsavel VARCHAR(255) NOT NULL,
            detalhes TEXT,
            data DATE
        )"""

        cone.executar(criar_tabela_login)
        return "Tabela Login criada com sucesso!"

    except:
        return "Não foi possível criar a tabela Login!"

    finally:
        if cone.connection is not None:
            cone.desconectar()
            return "Conexão Finalizada!"


def inserir_usuario():
    try:
        cone.conectar()
        if request.method == 'POST':
            grupo = request.form['grupo']
            endereco  = request.form['endereco']
            estado = request.form['estado']
            contato = request.form['contato']
            responsavel = request.form['responsavel']
            data = request.form['data']
            detalhes = request.form['detalhes']

            sql = "INSERT INTO grupos (grupo, endereco, estado, contato, responsavel, data, detalhes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (grupo, endereco, estado, contato, responsavel, data, detalhes)

            cone.executar(sql, values)

            return "Dados inseridos com sucesso!"
        
    except Exception as e:
        return f"Erro: {str(e)}"
    
    finally:
        if cone.connection is not None:
            cone.desconectar()
            return "Conexão Finalizada!"


#execute = criarTabelaLogin()