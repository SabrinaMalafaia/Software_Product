from _dados import Conexao

db = Conexao("localhost", "3307", "root", "root", "V2")


class Evento:
    def __init__(self, titulo, descricao, data_inicio, data_fim, localizacao):
        self.titulo = titulo
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.localizacao = localizacao
        self.id = None

    def definir_id(self, id_evento):
        self.id = id_evento

    def cadastrar_evento(self):
        db.conectar()
        try:
            query = "INSERT INTO eventos (titulo, descricao, data_inicio, data_fim, localizacao) VALUES (%s, %s, %s, %s, %s)"

            values = (self.titulo, self.descricao, self.data_inicio,
                      self.data_fim, self.localizacao)

            db.executar(query, values)

            return "Evento cadastrado com sucesso!"

        except Exception as e:
            return f"Erro ao adicionar parceiro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def editar_evento(self):
        try:
            db.conectar()

            query = """
            UPDATE eventos
            SET titulo=%s, descricao=%s, data_inicio=%s, data_fim=%s, localizacao=%s
            WHERE id_evento = %s
            """

            values = (self.titulo, self.descricao, self.data_inicio,
                      self.data_fim, self.localizacao, self.id)

            db.executar(query, values)

            return "Evento atualizado com sucesso!"

        except Exception as e:
            return f"Erro ao atualizar evento: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def excluir_evento(self):
        try:
            db.conectar()

            if self.id:

                query = """
                DELETE FROM eventos WHERE id_evento = %s
                """

                values = (self.id,)

                db.executar(query, values)

                self.id = None

                return "Evento apagado com sucesso!"

        except Exception as e:
            return f"Erro ao apagar evento: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def buscar_evento_id(id_evento):  # Fazendo
        db.conectar()
        try:
            query = "SELECT * FROM eventos WHERE id_evento = %s"
            values = (id_evento,)
            resultado = db.executar(query, values)

            if resultado:
                evento = Evento(*resultado[0][1:])
                evento.definir_id(id_evento)
                return evento
            else:
                return None

        except Exception as e:
            return f"Erro: {str(e)}"

        finally:
            if db.conexao is not None:
                db.desconectar()

    def listar_evento():
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
