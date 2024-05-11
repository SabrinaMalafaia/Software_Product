from alemdopedal.dados import Conexao

db = Conexao("localhost", "3307", "root", "root", "V2")


class Parceiro:
    def __init__(self, parceiro, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, desconto, status, data, detalhes):
        self.parceiro = parceiro
        self.cep = cep
        self.endereco = endereco
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.contato = contato
        self.responsavel = responsavel
        self.desconto = desconto
        self.status = status
        self.data = data
        self.detalhes = detalhes

    def buscar_parceiro_id(id_parceiro):
        db.conectar()
        try:
            query = "SELECT * FROM parceiros WHERE id_parceiro = %s"
            values = (id_parceiro,)
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
            query = "SELECT * FROM parceiros WHERE status = '1'"
            resultado = db.executar(query)
            return resultado

        except Exception as e:
            return f"Erro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def adicionar_parceiro(self):
        try:
            db.conectar()

            query = "INSERT INTO parceiros (parceiro, cep, endereco, complemento, bairro, cidade, estado, contato, responsavel, desconto, detalhes, data, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)"

            values = (self.parceiro, self.cep, self.endereco, self.complemento, self.bairro, self.cidade,
                      self.estado, self.contato, self.responsavel, self.desconto, self.detalhes, self.status)

            db.executar(query, values)

            return "Dados inseridos com sucesso!"

        except Exception as e:
            return f"Erro ao adicionar parceiro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def editar_parceiro(dados):
        try:
            db.conectar()

            query = """
            UPDATE parceiros
            SET parceiro=%s, cep=%s, endereco=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, contato=%s, responsavel=%s, desconto=%s, detalhes=%s, data=%s, status=%s
            WHERE id_parceiro = %s
            """

            values = (dados['parceiro'], dados['cep'], dados['endereco'], dados['complemento'], dados['bairro'], dados['cidade'], dados['estado'],
                      dados['contato'], dados['responsavel'], dados['desconto'], dados['detalhes'], dados['data'], dados['status'], dados['id_parceiro'])

            db.executar(query, values)

            return "Parceiro atualizado com sucesso!"

        except Exception as e:
            return f"Erro ao atualizar parceiro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()
