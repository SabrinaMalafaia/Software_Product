import mysql.connector


class Conexao:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return "Conexão estabelecida com sucesso!"

        except mysql.connector.Error as erro:
            return f"Erro ao conectar ao banco de dados: {erro}"

    def desconectar(self):
        if self.conexao is not None and self.conexao.is_connected():
            self.conexao.close()
            return "Conexão ao banco de dados finalizada."

    def executar(self, query, values=None):
        if self.conexao is not None and self.conexao.is_connected():
            try:
                cursor = self.conexao.cursor()
                cursor.execute(query, values)

                if query.lower().startswith("select"):
                    resultado = cursor.fetchall()
                    return resultado

                else:
                    self.conexao.commit()
                    return "Query executada com sucesso!"

            except mysql.connector.Error as erro:
                self.conexao.rollback()
                return f"Erro: {erro}"

            finally:
                cursor.close()

        else:
            return "A conexão com o banco de dados não está ativa."
