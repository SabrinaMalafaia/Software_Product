from app.dados import Conexao

db = Conexao("localhost", "3307", "root", "root", "V2")


class Grupo:
    def __init__(self, grupo, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, status, data, detalhes):
        self.grupo = grupo
        self.cep = cep
        self.endereco = endereco
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.contato = contato
        self.responsavel = responsavel
        self.status = status
        self.data = data
        self.detalhes = detalhes

    def buscar_grupo_id(id_grupo):
        db.conectar()
        try:
            query = "SELECT * FROM grupos WHERE id_grupo = %s"
            values = (id_grupo,)
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

    def adicionar_grupo(self):
        try:
            db.conectar()

            query = "INSERT INTO grupos (grupo, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, detalhes, data, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)"
            values = (self.grupo, self.cep, self.endereco, self.complemento, self.bairro, self.cidade,
                      self.estado, self.contato, self.responsavel, self.detalhes, self.status)

            db.executar(query, values)

            return "Dados inseridos com sucesso!"

        except Exception as e:
            return f"Erro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def editar_grupo(dados):
        try:
            db.conectar()

            query = """
            UPDATE grupos
            SET grupo=%s, cep=%s, endereco=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, contato=%s, responsavel=%s, detalhes=%s, data=%s, status=%s
            WHERE id_grupo = %s
            """

            values = (
                dados['grupo'], dados['cep'], dados['endereco'], dados['complemento'], dados['bairro'], dados['cidade'],
                dados['estado'], dados['contato'], dados['responsavel'], dados['detalhes'], dados['data'], dados['status'], dados['id_grupo']
            )

            db.executar(query, values)

            return "Grupo atualizado com sucesso!"

        except Exception as e:
            return f"Erro ao atualizar grupo: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()
